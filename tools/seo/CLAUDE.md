# SEO Research Integration

**Status:** ACTIVE

## Connection Details

- **Auth:** HTTP Basic Auth via DataForSEO API
- **Credentials:** `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` in `.env`
- **Base URL:** `https://api.dataforseo.com/v3`
- **Default location:** United Kingdom (code 2826)

## How to Use

All SEO research is via Python modules in `tools/seo/`. Run scripts from the pablo project root.

### Authentication Pattern

```python
import sys
sys.path.insert(0, 'C:/ClaudeProjects/pablo')
from tools.seo.seo_research import get_keyword_data, get_serp_results, get_keyword_suggestions
from tools.seo.competitor import get_competitor_keywords, get_keyword_gap
from tools.seo.tracker import generate_weekly_report, pull_keyword_rankings
```

Authentication is handled automatically — the modules load credentials from `.env`.

### Keyword Research

#### Get search volumes for a list of keywords

```python
from tools.seo.seo_research import get_keyword_data

results = get_keyword_data(["cycling gilet", "cycling jersey", "bib shorts"])
for kw in results:
	print(f"{kw['keyword']}: vol={kw['search_volume']}, comp={kw['competition']}, cpc={kw['cpc']}")
```

#### Get related keyword suggestions from a seed

```python
from tools.seo.seo_research import get_keyword_suggestions

results = get_keyword_suggestions("cycling gilet", limit=30)
for kw in results:
	print(f"{kw['keyword']}: vol={kw['search_volume']}, difficulty={kw['keyword_difficulty']}")
```

#### Get SERP results for a keyword

```python
from tools.seo.seo_research import get_serp_results

results = get_serp_results("best cycling jersey uk")
for r in results:
	print(f"#{r['rank']}: {r['domain']} — {r['title']}")
```

### Competitor Analysis

#### Get keywords a competitor ranks for

```python
from tools.seo.competitor import get_competitor_keywords

data = get_competitor_keywords("lecol.cc", limit=50, min_volume=100)
print(f"Total keywords: {data['total_count']}")
for kw in data['keywords']:
	print(f"  {kw['keyword']}: vol={kw['search_volume']}, rank={kw['rank']}")
```

#### Find keyword gaps (competitors rank, we don't)

```python
from tools.seo.competitor import get_keyword_gap

gap = get_keyword_gap(
	our_domain="stolengoat.com",
	competitor_domains=["lecol.cc", "cycology.com", "castelli-cycling.com"],
	limit=50,
	min_volume=100,
)
for kw in gap['gap_keywords']:
	print(f"{kw['keyword']}: vol={kw['search_volume']}, competitors: {list(kw['competitor_positions'].keys())}")
```

### Rank Tracking

#### Pull current rankings for target keywords

```python
from tools.seo.tracker import pull_keyword_rankings

targets = [
	{"keyword": "cycling gilet", "niche": "lifestyle"},
	{"keyword": "custom cycling jersey", "niche": "ck"},
]
rankings = pull_keyword_rankings(targets)
for r in rankings:
	print(f"{r['keyword']}: pos={r['gsc_position']}, clicks={r['gsc_clicks']}")
```

#### Generate weekly ranking report

```python
from tools.seo.tracker import generate_weekly_report

report = generate_weekly_report(targets)
print(f"Tracking {report['total_tracked']} keywords: {report['improved']} improved, {report['declined']} declined")
```

## Cost Awareness

DataForSEO charges per request. Approximate costs:

| Operation | Cost |
|---|---|
| Keyword volumes (batch of 100) | ~$0.05 |
| SERP results (single keyword) | ~$0.02 |
| Competitor domain keywords | ~$0.05 |
| Keyword gap analysis | ~$0.05 |
| Related keyword suggestions | ~$0.05 |

**Session cost ceiling:** $5.00 per script execution (configurable via `SESSION_COST_CEILING` in `seo_research.py`). The wrapper tracks cumulative spend and raises `RuntimeError` if the ceiling is reached.

Check spend at any time:

```python
from tools.seo.seo_research import get_session_spend
print(f"Session spend: ${get_session_spend():.2f}")
```

## Caching

Results are cached to `projects/sg-seo/data/` as JSON:

| Data type | Cache TTL | Directory |
|---|---|---|
| Keyword volumes | 7 days | `data/keywords/` |
| SERP results | 1 day | `data/serp/` |
| Keyword suggestions | 7 days | `data/suggestions/` |
| Competitor keywords | 7 days | `data/competitor/` |
| Keyword gaps | 7 days | `data/gap/` |

Cached results are returned automatically. To force a fresh fetch, delete the relevant cache file.

## Integration with GSC & GA4

- **GSC** (`tools/search-console/CLAUDE.md`): Use for current ranking data, clicking queries, top pages. The rank tracker (`tracker.py`) uses GSC directly.
- **GA4** (`tools/analytics/CLAUDE.md`): Use for traffic volumes, conversion data, on-site search terms. **Always apply bot exclusion** for main site queries (see GA4 guide).
- **DataForSEO**: Use for keyword discovery, competitor analysis, search volumes, and difficulty — the things GSC and GA4 can't provide.

## Location Override

All functions default to UK (2826). To query other locations:

```python
results = get_keyword_data(["cycling gilet"], location=2840)  # USA
```

Common location codes: 2826 (UK), 2840 (US), 2276 (Germany), 2250 (France).

## Rules

- **Check session spend** before running large batches
- **Use caching** — don't re-fetch data that's within TTL
- **UK default** — all queries target UK unless specifically analysing international
- **stolengoat.com** is the primary domain for gap analysis and rank tracking
- **Competitor domains:** lecol.cc, cycology.com, castelli-cycling.com, rapha.cc (lifestyle); santinisms.com, kalas.cz, lecol.cc (CK)
