"""DataForSEO keyword research wrapper.

Provides keyword volume, difficulty, and SERP data for SEO analysis.
All queries default to UK (location code 2826).
"""

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

DATAFORSEO_LOGIN = os.getenv("DATAFORSEO_LOGIN")
DATAFORSEO_PASSWORD = os.getenv("DATAFORSEO_PASSWORD")
BASE_URL = "https://api.dataforseo.com/v3"
DEFAULT_LOCATION = 2826  # United Kingdom
DEFAULT_LANGUAGE = "en"

# Cache config
CACHE_DIR = Path("C:/ClaudeProjects/pablo/projects/sg-seo/data")
KEYWORD_CACHE_TTL_DAYS = 7
SERP_CACHE_TTL_DAYS = 1

# Cost tracking
_session_spend = 0.0
SESSION_COST_CEILING = 5.0  # USD

# Approximate costs per request type
COST_PER_KEYWORD_BATCH = 0.05  # per 100 keywords
COST_PER_SERP = 0.02
COST_PER_LABS = 0.05


def _check_budget(estimated_cost: float):
	"""Raise if session spend would exceed ceiling."""
	global _session_spend
	if _session_spend + estimated_cost > SESSION_COST_CEILING:
		raise RuntimeError(
			f"Session cost ceiling reached: ${_session_spend:.2f} spent, "
			f"${estimated_cost:.2f} requested, ceiling is ${SESSION_COST_CEILING:.2f}"
		)


def _track_spend(cost: float):
	global _session_spend
	_session_spend += cost


def _auth():
	return (DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD)


def _post(endpoint: str, payload: list[dict], max_retries: int = 3) -> dict:
	"""POST to DataForSEO with retry on transient errors."""
	url = f"{BASE_URL}/{endpoint}"
	for attempt in range(max_retries):
		resp = requests.post(url, auth=_auth(), json=payload)
		if resp.status_code in (429, 500, 502, 503):
			wait = 2 ** attempt
			time.sleep(wait)
			continue
		if resp.status_code in (401, 403):
			raise RuntimeError(f"DataForSEO auth error: {resp.status_code} {resp.text[:200]}")
		resp.raise_for_status()
		return resp.json()
	raise RuntimeError(f"DataForSEO request failed after {max_retries} retries: {endpoint}")


def _cache_path(cache_type: str, key: str) -> Path:
	path = CACHE_DIR / cache_type
	path.mkdir(parents=True, exist_ok=True)
	safe_key = key.replace("/", "_").replace("\\", "_").replace(":", "_").replace(" ", "_")[:100]
	return path / f"{safe_key}.json"


def _read_cache(cache_type: str, key: str, ttl_days: int) -> dict | None:
	path = _cache_path(cache_type, key)
	if not path.exists():
		return None
	data = json.loads(path.read_text(encoding="utf-8"))
	cached_at = datetime.fromisoformat(data.get("_cached_at", "2000-01-01"))
	if datetime.now() - cached_at > timedelta(days=ttl_days):
		return None
	return data


def _write_cache(cache_type: str, key: str, data: dict):
	data["_cached_at"] = datetime.now().isoformat()
	path = _cache_path(cache_type, key)
	path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


def get_keyword_data(
	keywords: list[str],
	location: int = DEFAULT_LOCATION,
	language: str = DEFAULT_LANGUAGE,
) -> list[dict]:
	"""Get search volume, competition, CPC, and trend for a list of keywords.

	Returns a list of dicts, one per keyword:
		{keyword, search_volume, competition, cpc, monthly_searches (list of 12)}
	"""
	cache_key = f"kw_{'_'.join(sorted(keywords[:10]))}_{location}"
	cached = _read_cache("keywords", cache_key, KEYWORD_CACHE_TTL_DAYS)
	if cached and cached.get("results"):
		return cached["results"]

	cost = COST_PER_KEYWORD_BATCH * (len(keywords) / 100)
	_check_budget(cost)

	data = _post("keywords_data/google_ads/search_volume/live", [{
		"keywords": keywords,
		"location_code": location,
		"language_code": language,
	}])
	_track_spend(cost)

	results = []
	for task in data.get("tasks", []):
		for item in task.get("result") or []:
			results.append({
				"keyword": item.get("keyword"),
				"search_volume": item.get("search_volume"),
				"competition": item.get("competition"),
				"cpc": item.get("cpc"),
				"monthly_searches": item.get("monthly_searches") or [],
			})

	_write_cache("keywords", cache_key, {"results": results})
	return results


def get_serp_results(
	keyword: str,
	location: int = DEFAULT_LOCATION,
	language: str = DEFAULT_LANGUAGE,
	depth: int = 20,
) -> list[dict]:
	"""Get top organic SERP results for a keyword.

	Returns a list of dicts:
		{rank, domain, url, title, snippet}
	"""
	cache_key = f"serp_{keyword}_{location}"
	cached = _read_cache("serp", cache_key, SERP_CACHE_TTL_DAYS)
	if cached and cached.get("results"):
		return cached["results"]

	_check_budget(COST_PER_SERP)

	data = _post("serp/google/organic/live/regular", [{
		"keyword": keyword,
		"location_code": location,
		"language_code": language,
		"depth": depth,
	}])
	_track_spend(COST_PER_SERP)

	results = []
	for task in data.get("tasks", []):
		for result_set in task.get("result") or []:
			for item in result_set.get("items") or []:
				if item.get("type") == "organic":
					results.append({
						"rank": item.get("rank_group"),
						"domain": item.get("domain"),
						"url": item.get("url"),
						"title": item.get("title"),
						"snippet": item.get("description"),
					})

	_write_cache("serp", cache_key, {"results": results})
	return results


def get_keyword_suggestions(
	seed_keyword: str,
	location: int = DEFAULT_LOCATION,
	language: str = DEFAULT_LANGUAGE,
	limit: int = 50,
) -> list[dict]:
	"""Get related keyword suggestions from a seed keyword.

	Returns a list of dicts:
		{keyword, search_volume, competition, cpc, keyword_difficulty}
	"""
	cache_key = f"suggest_{seed_keyword}_{location}"
	cached = _read_cache("suggestions", cache_key, KEYWORD_CACHE_TTL_DAYS)
	if cached and cached.get("results"):
		return cached["results"]

	_check_budget(COST_PER_LABS)

	data = _post("dataforseo_labs/google/related_keywords/live", [{
		"keyword": seed_keyword,
		"location_code": location,
		"language_code": language,
		"limit": limit,
	}])
	_track_spend(COST_PER_LABS)

	results = []
	for task in data.get("tasks", []):
		for result_set in task.get("result") or []:
			for item in result_set.get("items") or []:
				kd = item.get("keyword_data", {})
				ki = kd.get("keyword_info", {})
				results.append({
					"keyword": kd.get("keyword"),
					"search_volume": ki.get("search_volume"),
					"competition": ki.get("competition"),
					"cpc": ki.get("cpc"),
					"keyword_difficulty": item.get("keyword_difficulty"),
				})

	_write_cache("suggestions", cache_key, {"results": results})
	return results


def get_session_spend() -> float:
	"""Return total estimated spend for this session."""
	return _session_spend


def reset_session_spend():
	"""Reset the session spend counter."""
	global _session_spend
	_session_spend = 0.0
