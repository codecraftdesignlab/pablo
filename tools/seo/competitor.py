"""Competitor keyword analysis via DataForSEO Labs.

Provides competitor domain keyword extraction and keyword gap analysis.
"""

import json
from pathlib import Path

from tools.seo.seo_research import (
	BASE_URL,
	CACHE_DIR,
	COST_PER_LABS,
	DEFAULT_LANGUAGE,
	DEFAULT_LOCATION,
	KEYWORD_CACHE_TTL_DAYS,
	_auth,
	_check_budget,
	_post,
	_read_cache,
	_track_spend,
	_write_cache,
)


def get_competitor_keywords(
	domain: str,
	location: int = DEFAULT_LOCATION,
	language: str = DEFAULT_LANGUAGE,
	limit: int = 100,
	min_volume: int = 10,
	filters: list | None = None,
) -> dict:
	"""Get keywords a competitor domain ranks for.

	Args:
		domain: competitor domain (e.g., 'lecol.cc')
		location: DataForSEO location code (default UK)
		language: language code
		limit: max results to return
		min_volume: minimum monthly search volume
		filters: optional DataForSEO filters list

	Returns dict:
		{domain, total_count, keywords: [{keyword, search_volume, rank, url, competition, cpc, keyword_difficulty}]}
	"""
	cache_key = f"comp_{domain}_{location}_{limit}"
	cached = _read_cache("competitor", cache_key, KEYWORD_CACHE_TTL_DAYS)
	if cached and cached.get("keywords"):
		return cached

	_check_budget(COST_PER_LABS)

	payload = {
		"target": domain,
		"location_code": location,
		"language_code": language,
		"limit": limit,
		"order_by": ["keyword_data.keyword_info.search_volume,desc"],
	}

	if filters:
		payload["filters"] = filters
	elif min_volume > 0:
		payload["filters"] = [
			"keyword_data.keyword_info.search_volume", ">", min_volume
		]

	data = _post("dataforseo_labs/google/ranked_keywords/live", [payload])
	_track_spend(COST_PER_LABS)

	keywords = []
	total_count = 0
	for task in data.get("tasks", []):
		for result_set in task.get("result") or []:
			total_count = result_set.get("total_count", 0)
			for item in result_set.get("items") or []:
				kd = item.get("keyword_data", {})
				ki = kd.get("keyword_info", {})
				serp = item.get("ranked_serp_element", {}).get("serp_item", {})
				keywords.append({
					"keyword": kd.get("keyword"),
					"search_volume": ki.get("search_volume"),
					"rank": serp.get("rank_group"),
					"url": serp.get("url"),
					"competition": ki.get("competition"),
					"cpc": ki.get("cpc"),
					"keyword_difficulty": ki.get("keyword_difficulty"),
				})

	result = {
		"domain": domain,
		"total_count": total_count,
		"keywords": keywords,
	}
	_write_cache("competitor", cache_key, result)
	return result


def get_keyword_gap(
	our_domain: str,
	competitor_domains: list[str],
	location: int = DEFAULT_LOCATION,
	language: str = DEFAULT_LANGUAGE,
	limit: int = 100,
	min_volume: int = 50,
) -> dict:
	"""Find keywords competitors rank for that our domain does not.

	Pulls top keywords from each competitor, deduplicates, then checks which
	ones our domain doesn't rank for. This is more reliable than the
	domain_intersection endpoint for gap analysis.

	Args:
		our_domain: our domain (e.g., 'stolengoat.com')
		competitor_domains: list of competitor domains
		location: DataForSEO location code
		language: language code
		limit: max gap keywords to return
		min_volume: minimum monthly search volume

	Returns dict:
		{our_domain, competitors, gap_keywords: [{keyword, search_volume, competition, cpc,
		  competitor_positions: {domain: {rank, url}}}]}
	"""
	comp_key = "_".join(sorted(competitor_domains))
	cache_key = f"gap_{our_domain}_{comp_key}_{location}_{limit}"
	cached = _read_cache("gap", cache_key, KEYWORD_CACHE_TTL_DAYS)
	if cached and cached.get("gap_keywords"):
		return cached

	# Step 1: Gather keywords from all competitors
	all_keywords = {}  # keyword -> {search_volume, competition, cpc, competitor_positions}
	for comp_domain in competitor_domains:
		comp_data = get_competitor_keywords(
			comp_domain, location, language,
			limit=200, min_volume=min_volume,
		)
		for kw in comp_data.get("keywords", []):
			keyword = kw.get("keyword")
			if not keyword:
				continue
			vol = kw.get("search_volume") or 0
			if vol < min_volume:
				continue

			if keyword not in all_keywords:
				all_keywords[keyword] = {
					"keyword": keyword,
					"search_volume": vol,
					"competition": kw.get("competition"),
					"cpc": kw.get("cpc"),
					"competitor_positions": {},
				}
			all_keywords[keyword]["competitor_positions"][comp_domain] = {
				"rank": kw.get("rank"),
				"url": kw.get("url"),
			}

	# Step 2: Check which keywords our domain ranks for
	our_data = get_competitor_keywords(
		our_domain, location, language,
		limit=1000, min_volume=0,
	)
	our_keywords = {kw.get("keyword") for kw in our_data.get("keywords", []) if kw.get("keyword")}

	# Step 3: Filter to gap keywords (competitors rank, we don't or rank >50)
	our_ranked_poorly = {}
	for kw in our_data.get("keywords", []):
		keyword = kw.get("keyword")
		rank = kw.get("rank")
		if keyword and rank and rank > 50:
			our_ranked_poorly[keyword] = rank

	gap_keywords = []
	for keyword, data in all_keywords.items():
		our_rank = None
		if keyword in our_keywords:
			# Check if we rank well (top 50) — if so, skip
			our_kw = next((k for k in our_data.get("keywords", []) if k.get("keyword") == keyword), None)
			if our_kw and our_kw.get("rank") and our_kw["rank"] <= 50:
				continue
			our_rank = our_kw.get("rank") if our_kw else None

		data["our_rank"] = our_rank
		gap_keywords.append(data)

	# Sort by search volume descending, limit results
	gap_keywords.sort(key=lambda x: x.get("search_volume") or 0, reverse=True)
	gap_keywords = gap_keywords[:limit]

	result = {
		"our_domain": our_domain,
		"competitors": competitor_domains,
		"gap_keywords": gap_keywords,
	}
	_write_cache("gap", cache_key, result)
	return result


def compare_domains(
	domains: list[str],
	location: int = DEFAULT_LOCATION,
	language: str = DEFAULT_LANGUAGE,
) -> list[dict]:
	"""Get a quick comparison of multiple domains' organic presence.

	Returns a list of dicts:
		{domain, total_keywords, estimated_traffic}
	"""
	results = []
	for domain in domains:
		comp = get_competitor_keywords(domain, location, language, limit=1)
		results.append({
			"domain": domain,
			"total_keywords": comp.get("total_count", 0),
		})
	return results
