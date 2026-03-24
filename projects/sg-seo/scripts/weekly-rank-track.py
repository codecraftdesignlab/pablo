"""Weekly SEO rank tracking script.

Pulls current GSC rankings for target keywords, compares with previous
snapshot, saves a new snapshot, and outputs a summary for the Monday briefing.

Run: python projects/sg-seo/scripts/weekly-rank-track.py
"""

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, "C:/ClaudeProjects/pablo")

from tools.seo.tracker import (
	compare_snapshots,
	get_latest_snapshot,
	pull_keyword_rankings,
	save_snapshot,
)

# Target keywords from the keyword universe — all CRITICAL and HIGH priority
TARGET_KEYWORDS = [
	# Cluster 1: Women's Shorts (CRITICAL)
	{"keyword": "cycling shorts women", "niche": "womens-shorts"},
	{"keyword": "women's cycling shorts", "niche": "womens-shorts"},
	{"keyword": "womens bib shorts", "niche": "womens-shorts"},
	# Cluster 2: Cycling Clothing (HIGH)
	{"keyword": "cycling clothing", "niche": "cycling-clothing"},
	{"keyword": "cycling apparel", "niche": "cycling-clothing"},
	{"keyword": "uk cycling clothing brands", "niche": "cycling-clothing"},
	# Cluster 3: Men's Jerseys (HIGH)
	{"keyword": "cycling jersey", "niche": "mens-jerseys"},
	{"keyword": "mens cycling jersey", "niche": "mens-jerseys"},
	{"keyword": "cycling jersey mens", "niche": "mens-jerseys"},
	{"keyword": "long sleeve cycling jersey", "niche": "mens-jerseys"},
	{"keyword": "cycling jerseys", "niche": "mens-jerseys"},
	{"keyword": "cycling jerseys uk", "niche": "mens-jerseys"},
	# Cluster 4: Gilets (HIGH)
	{"keyword": "cycling gilet", "niche": "gilets"},
	{"keyword": "cycling gilet men", "niche": "gilets"},
	{"keyword": "cycling gilet womens", "niche": "gilets"},
	{"keyword": "mens cycling gilet", "niche": "gilets"},
	# Cluster 5: Socks (HIGH)
	{"keyword": "cycling socks", "niche": "socks"},
	{"keyword": "cycling socks mens", "niche": "socks"},
	{"keyword": "cycle socks", "niche": "socks"},
	# Cluster 6: Gloves (HIGH)
	{"keyword": "cycling gloves", "niche": "gloves"},
	{"keyword": "cycling mitts", "niche": "gloves"},
	# Cluster 7: Men's Shorts (HIGH)
	{"keyword": "cycling shorts men", "niche": "mens-shorts"},
	{"keyword": "bib shorts", "niche": "mens-shorts"},
	{"keyword": "cycling bib shorts", "niche": "mens-shorts"},
	# Cluster 8: Custom Kit (CRITICAL)
	{"keyword": "custom cycling jersey", "niche": "custom-kit"},
	{"keyword": "custom cycling kit", "niche": "custom-kit"},
	{"keyword": "custom cycling clothing", "niche": "custom-kit"},
	{"keyword": "custom cycling jersey uk", "niche": "custom-kit"},
	{"keyword": "custom triathlon suit", "niche": "custom-kit"},
	{"keyword": "custom running vest", "niche": "custom-kit"},
	# Cluster 9: Arm Warmers (MEDIUM)
	{"keyword": "cycling arm warmers", "niche": "arm-warmers"},
	{"keyword": "leg warmers", "niche": "arm-warmers"},
	# Cluster 10: Jackets (MEDIUM)
	{"keyword": "best winter cycling jacket", "niche": "jackets"},
]


def run():
	print(f"SEO Rank Tracker — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
	print(f"Tracking {len(TARGET_KEYWORDS)} keywords across {len(set(k['niche'] for k in TARGET_KEYWORDS))} clusters")
	print()

	# Pull current rankings
	print("Pulling GSC rankings...")
	current = pull_keyword_rankings(TARGET_KEYWORDS)

	# Load previous snapshot
	previous = get_latest_snapshot()
	if previous:
		print(f"Previous snapshot: {previous['date']}")
	else:
		print("No previous snapshot — this is the first run")

	# Compare
	comparison = compare_snapshots(current, previous)

	# Save new snapshot
	today = datetime.now().strftime("%Y-%m-%d")
	path = save_snapshot(current, today)
	print(f"Snapshot saved: {path}")
	print()

	# Summary stats
	ranking = [k for k in comparison if k["gsc_position"] is not None]
	not_ranking = [k for k in comparison if k["gsc_position"] is None]
	improved = [k for k in comparison if k["status"] == "improved"]
	declined = [k for k in comparison if k["status"] == "declined"]
	stable = [k for k in comparison if k["status"] == "stable"]
	new_rankings = [k for k in comparison if k["status"] == "new"]
	lost = [k for k in comparison if k["status"] == "lost"]

	print(f"=== Summary ===")
	print(f"  Ranking:      {len(ranking)}/{len(comparison)}")
	print(f"  Not ranking:  {len(not_ranking)}")
	if previous:
		print(f"  Improved:     {len(improved)}")
		print(f"  Declined:     {len(declined)}")
		print(f"  Stable:       {len(stable)}")
		print(f"  New:          {len(new_rankings)}")
		print(f"  Lost:         {len(lost)}")
	print()

	# Detail: keywords we're ranking for
	if ranking:
		print("=== Currently Ranking ===")
		for k in sorted(ranking, key=lambda x: x["gsc_position"]):
			change_str = ""
			if k.get("change") is not None:
				arrow = "+" if k["change"] > 0 else ""
				change_str = f" ({arrow}{k['change']:.1f})"
			print(f"  {k['keyword']:40s} pos {k['gsc_position']:5.1f}{change_str}  [{k['niche']}]")
		print()

	# Detail: significant movements
	if improved:
		print("=== Improved (moved up 2+ positions) ===")
		for k in sorted(improved, key=lambda x: x["change"], reverse=True):
			print(f"  {k['keyword']:40s} {k['prev_position']:.1f} -> {k['gsc_position']:.1f} (+{k['change']:.1f})")
		print()

	if declined:
		print("=== Declined (dropped 2+ positions) ===")
		for k in sorted(declined, key=lambda x: x["change"]):
			print(f"  {k['keyword']:40s} {k['prev_position']:.1f} -> {k['gsc_position']:.1f} ({k['change']:.1f})")
		print()

	# Generate briefing markdown
	briefing = generate_briefing_markdown(comparison, today, previous)
	briefing_path = Path("C:/ClaudeProjects/pablo/projects/sg-seo/reports") / f"seo-weekly-{today}.md"
	briefing_path.parent.mkdir(parents=True, exist_ok=True)
	briefing_path.write_text(briefing, encoding="utf-8")
	print(f"Briefing report: {briefing_path}")

	return comparison


def generate_briefing_markdown(comparison, date, previous):
	"""Generate a Monday briefing-ready markdown summary."""
	ranking = [k for k in comparison if k["gsc_position"] is not None]
	not_ranking = [k for k in comparison if k["gsc_position"] is None]
	improved = [k for k in comparison if k["status"] == "improved"]
	declined = [k for k in comparison if k["status"] == "declined"]

	lines = [
		f"# SEO Weekly Report — {date}",
		"",
		f"**Keywords tracked:** {len(comparison)}",
		f"**Currently ranking:** {len(ranking)}/{len(comparison)}",
	]

	if previous:
		lines.append(f"**Improved:** {len(improved)} | **Declined:** {len(declined)}")
	lines.append("")

	if improved:
		lines.append("## Improved")
		lines.append("")
		lines.append("| Keyword | Previous | Current | Change |")
		lines.append("|---|---|---|---|")
		for k in sorted(improved, key=lambda x: x["change"], reverse=True):
			lines.append(f"| {k['keyword']} | {k['prev_position']:.1f} | {k['gsc_position']:.1f} | +{k['change']:.1f} |")
		lines.append("")

	if declined:
		lines.append("## Declined")
		lines.append("")
		lines.append("| Keyword | Previous | Current | Change |")
		lines.append("|---|---|---|---|")
		for k in sorted(declined, key=lambda x: x["change"]):
			lines.append(f"| {k['keyword']} | {k['prev_position']:.1f} | {k['gsc_position']:.1f} | {k['change']:.1f} |")
		lines.append("")

	# Top positions
	lines.append("## Current Rankings")
	lines.append("")
	lines.append("| Keyword | Position | Clicks | Impressions | Page |")
	lines.append("|---|---|---|---|---|")
	for k in sorted(ranking, key=lambda x: x["gsc_position"]):
		page = k.get("page", "").replace("https://stolengoat.com", "")[:40]
		lines.append(f"| {k['keyword']} | {k['gsc_position']:.1f} | {k['gsc_clicks']} | {k['gsc_impressions']} | {page} |")
	lines.append("")

	# Not ranking
	if not_ranking:
		lines.append("## Not Ranking")
		lines.append("")
		niche_groups = {}
		for k in not_ranking:
			niche_groups.setdefault(k["niche"], []).append(k["keyword"])
		for niche, keywords in sorted(niche_groups.items()):
			lines.append(f"- **{niche}:** {', '.join(keywords)}")
		lines.append("")

	return "\n".join(lines)


if __name__ == "__main__":
	run()
