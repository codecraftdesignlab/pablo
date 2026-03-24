"""Rank tracking via Google Search Console.

Pulls weekly snapshots of target keyword rankings from GSC and stores them
as JSON files for trend comparison.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_FILE = "C:/ClaudeProjects/pablo/google-service-account-key.json"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
SITE_URL = "https://stolengoat.com/"
RANKINGS_DIR = Path("C:/ClaudeProjects/pablo/projects/sg-seo/data/rankings")


def _gsc_client():
	creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
	return build("searchconsole", "v1", credentials=creds)


def pull_keyword_rankings(
	keywords: list[dict],
	days: int = 28,
) -> list[dict]:
	"""Pull current GSC rankings for a list of target keywords.

	Args:
		keywords: list of dicts with at least {keyword, niche}
		days: lookback period (GSC data has 2-3 day delay)

	Returns list of dicts:
		{keyword, niche, gsc_position, gsc_clicks, gsc_impressions, gsc_ctr, page}
	"""
	client = _gsc_client()
	end_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
	start_date = (datetime.now() - timedelta(days=days + 3)).strftime("%Y-%m-%d")

	results = []
	for kw in keywords:
		keyword = kw["keyword"]
		niche = kw.get("niche", "unknown")

		response = client.searchanalytics().query(
			siteUrl=SITE_URL,
			body={
				"startDate": start_date,
				"endDate": end_date,
				"dimensions": ["query", "page"],
				"dimensionFilterGroups": [{
					"filters": [{
						"dimension": "query",
						"operator": "equals",
						"expression": keyword,
					}]
				}],
				"rowLimit": 1,
			}
		).execute()

		rows = response.get("rows", [])
		if rows:
			row = rows[0]
			results.append({
				"keyword": keyword,
				"niche": niche,
				"gsc_position": round(row.get("position", 0), 1),
				"gsc_clicks": row.get("clicks", 0),
				"gsc_impressions": row.get("impressions", 0),
				"gsc_ctr": round(row.get("ctr", 0), 4),
				"page": row["keys"][1] if len(row.get("keys", [])) > 1 else "",
			})
		else:
			results.append({
				"keyword": keyword,
				"niche": niche,
				"gsc_position": None,
				"gsc_clicks": 0,
				"gsc_impressions": 0,
				"gsc_ctr": 0,
				"page": "",
			})

	return results


def save_snapshot(rankings: list[dict], date: str | None = None) -> Path:
	"""Save a ranking snapshot to the rankings directory.

	Args:
		rankings: list of keyword ranking dicts from pull_keyword_rankings()
		date: optional date string (YYYY-MM-DD), defaults to today

	Returns path to the saved snapshot file.
	"""
	if date is None:
		date = datetime.now().strftime("%Y-%m-%d")

	RANKINGS_DIR.mkdir(parents=True, exist_ok=True)
	path = RANKINGS_DIR / f"{date}.json"

	snapshot = {
		"date": date,
		"keywords": rankings,
	}

	path.write_text(json.dumps(snapshot, indent=2, default=str), encoding="utf-8")
	return path


def load_snapshot(date: str) -> dict | None:
	"""Load a ranking snapshot by date."""
	path = RANKINGS_DIR / f"{date}.json"
	if not path.exists():
		return None
	return json.loads(path.read_text(encoding="utf-8"))


def get_latest_snapshot() -> dict | None:
	"""Get the most recent ranking snapshot."""
	RANKINGS_DIR.mkdir(parents=True, exist_ok=True)
	files = sorted(RANKINGS_DIR.glob("*.json"), reverse=True)
	if not files:
		return None
	return json.loads(files[0].read_text(encoding="utf-8"))


def compare_snapshots(current: list[dict], previous: dict | None) -> list[dict]:
	"""Compare current rankings with previous snapshot.

	Returns list of dicts with change data:
		{keyword, niche, gsc_position, prev_position, change, page, status}

	status is one of: improved, declined, new, lost, stable
	"""
	prev_map = {}
	if previous:
		for kw in previous.get("keywords", []):
			prev_map[kw["keyword"]] = kw

	results = []
	for kw in current:
		keyword = kw["keyword"]
		prev = prev_map.get(keyword)

		entry = {
			"keyword": keyword,
			"niche": kw.get("niche", "unknown"),
			"gsc_position": kw.get("gsc_position"),
			"gsc_clicks": kw.get("gsc_clicks", 0),
			"gsc_impressions": kw.get("gsc_impressions", 0),
			"gsc_ctr": kw.get("gsc_ctr", 0),
			"prev_position": None,
			"change": None,
			"page": kw.get("page", ""),
			"status": "new",
		}

		if prev and prev.get("gsc_position") is not None:
			entry["prev_position"] = prev["gsc_position"]
			if kw.get("gsc_position") is not None:
				# Positive change = improved (moved up in rankings)
				entry["change"] = round(prev["gsc_position"] - kw["gsc_position"], 1)
				if entry["change"] > 2:
					entry["status"] = "improved"
				elif entry["change"] < -2:
					entry["status"] = "declined"
				else:
					entry["status"] = "stable"
			else:
				entry["status"] = "lost"
		elif kw.get("gsc_position") is not None:
			entry["status"] = "new"
		else:
			entry["status"] = "not_ranking"

		results.append(entry)

	return results


def generate_weekly_report(target_keywords: list[dict]) -> dict:
	"""Pull current rankings, compare with previous snapshot, save, and return report.

	Args:
		target_keywords: list of {keyword, niche} dicts

	Returns dict:
		{date, total_tracked, ranking, not_ranking, improved, declined, stable, new, lost, keywords: [...]}
	"""
	current = pull_keyword_rankings(target_keywords)

	previous = get_latest_snapshot()
	comparison = compare_snapshots(current, previous)

	today = datetime.now().strftime("%Y-%m-%d")
	save_snapshot(current, today)

	summary = {
		"date": today,
		"total_tracked": len(comparison),
		"ranking": sum(1 for k in comparison if k["gsc_position"] is not None),
		"not_ranking": sum(1 for k in comparison if k["gsc_position"] is None),
		"improved": sum(1 for k in comparison if k["status"] == "improved"),
		"declined": sum(1 for k in comparison if k["status"] == "declined"),
		"stable": sum(1 for k in comparison if k["status"] == "stable"),
		"new": sum(1 for k in comparison if k["status"] == "new"),
		"lost": sum(1 for k in comparison if k["status"] == "lost"),
		"keywords": comparison,
	}

	return summary
