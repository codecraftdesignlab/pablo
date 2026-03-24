# TASK-003: Competitor Gap Analysis — Lifestyle Set

## Objective

Analyse the organic keyword presence of Stolen Goat's lifestyle/brand competitors and identify keyword gaps — terms they rank for that SG doesn't. Focus on cycling clothing, gear, and lifestyle terms.

## Context

This is part of Milestone 2 (Research) for the SG SEO project. The lifestyle competitor set is:

| Competitor | Domain |
|---|---|
| Le Col | lecol.cc |
| Cycology | cycology.com |
| Castelli | castelli-cycling.com |
| Rapha | rapha.cc |

SG domain: `stolengoat.com`

The SEO tooling is at `tools/seo/`. Use the Python modules directly via `sys.path.insert(0, 'C:/ClaudeProjects/pablo')`.

## Scope

### Files to read
- `C:/ClaudeProjects/pablo/tools/seo/CLAUDE.md`

### Files to create
- `C:/ClaudeProjects/pablo/projects/sg-seo/.state/research/competitor-lifestyle.md` — full findings

### Out of scope
- CK competitors (TASK-004)
- Keyword expansion (TASK-005)
- Strategy (TASK-006)

## Required Analysis

### 1. Competitor Keyword Profiles
For each competitor, pull their top ranked keywords (limit 200, min volume 50):
```python
import sys
sys.path.insert(0, 'C:/ClaudeProjects/pablo')
from tools.seo.competitor import get_competitor_keywords
data = get_competitor_keywords('lecol.cc', limit=200, min_volume=50)
```

Report for each competitor:
- Total keywords they rank for
- Top 20 keywords by search volume (with rank and URL)
- Keyword themes (what topics do they rank for?)

### 2. Keyword Gap Analysis
Run gap analysis against all four competitors:
```python
from tools.seo.competitor import get_keyword_gap
gap = get_keyword_gap(
    our_domain='stolengoat.com',
    competitor_domains=['lecol.cc', 'cycology.com', 'castelli-cycling.com', 'rapha.cc'],
    limit=100,
    min_volume=50,
)
```

Filter the results to cycling/clothing-relevant terms only (exclude navigational queries like brand names, "le col", "rapha", etc.). Categorise the remaining gaps by theme:
- Product terms (jersey, gilet, bib shorts, etc.)
- Lifestyle/editorial terms (best cycling..., cycling in winter, etc.)
- Gift/seasonal terms (cycling gifts, christmas cycling, etc.)

### 3. Competitor Content Analysis
For each competitor, note:
- Do they have a blog? What topics do they cover?
- Do they have buying guides or editorial content?
- What pages rank for their highest-volume keywords?

Use `get_serp_results()` for 5-10 high-value keywords to see the full SERP landscape.

### 4. Opportunity Summary
Identify the top 20 gap keywords that represent real opportunities for SG:
- High volume (>100 monthly searches)
- Relevant to SG's product range
- Achievable (not dominated by massive retailers)
- Include which competitors rank and at what position

## Acceptance Criteria
- [ ] All four competitor keyword profiles extracted
- [ ] Keyword gap analysis completed with cycling-relevant filtering
- [ ] Gap keywords categorised by theme
- [ ] Top 20 opportunities identified with rationale
- [ ] Findings written to `competitor-lifestyle.md`

## Cost Awareness
Monitor DataForSEO spend. The competitor analysis uses ~$0.05 per domain query. Budget for this task: ~$1-2 max. Check spend with:
```python
from tools.seo.seo_research import get_session_spend
print(f'Spend: ${get_session_spend():.2f}')
```

## Testing
- Test framework: none (research task)
- Tests required: no

## Output
Write findings to `.state/research/competitor-lifestyle.md`. Append summary to `.state/handoff.md`. Update task status in `.state/tasks.jsonl`.
