# TASK-004: Competitor Gap Analysis — Custom Kit Set

## Objective

Analyse the organic keyword presence of Stolen Goat's custom kit competitors and identify keyword gaps — terms they rank for that SG doesn't. Focus on custom cycling jerseys, club kit, team kit, bespoke cycling clothing.

## Context

This is part of Milestone 2 (Research) for the SG SEO project. The CK competitor set is:

| Competitor | Domain |
|---|---|
| Santini | santinisms.com |
| Kalas | kalas.cz |
| Le Col | lecol.cc |

SG domain: `stolengoat.com`

SG's CK business is growing fast (+152% YoY) but does not rank for "custom cycling jersey uk" (not in top 20). This is a significant gap.

The SEO tooling is at `tools/seo/`. Use the Python modules directly via `sys.path.insert(0, 'C:/ClaudeProjects/pablo')`.

## Scope

### Files to read
- `C:/ClaudeProjects/pablo/tools/seo/CLAUDE.md`

### Files to create
- `C:/ClaudeProjects/pablo/projects/sg-seo/.state/research/competitor-ck.md` — full findings

### Out of scope
- Lifestyle competitors (TASK-003)
- Keyword expansion (TASK-005)
- Strategy (TASK-006)

## Required Analysis

### 1. CK Keyword Landscape
Use `get_keyword_data()` to get volumes for key CK seed terms:
```python
import sys
sys.path.insert(0, 'C:/ClaudeProjects/pablo')
from tools.seo.seo_research import get_keyword_data
results = get_keyword_data([
    'custom cycling jersey', 'custom cycling kit', 'custom cycling clothing',
    'bespoke cycling jersey', 'club cycling kit', 'team cycling jersey',
    'custom cycling jersey uk', 'design your own cycling jersey',
    'personalised cycling jersey', 'custom bike jersey',
    'custom cycling shorts', 'custom cycling gilet',
    'custom sportswear', 'custom team kit',
])
```

### 2. Competitor Keyword Profiles
For each CK competitor, pull ranked keywords:
```python
from tools.seo.competitor import get_competitor_keywords
data = get_competitor_keywords('santinisms.com', limit=200, min_volume=20)
```

Filter to CK-relevant terms (custom, bespoke, club, team, personalised, design). Report top keywords per competitor.

### 3. Keyword Gap Analysis
```python
from tools.seo.competitor import get_keyword_gap
gap = get_keyword_gap(
    our_domain='stolengoat.com',
    competitor_domains=['santinisms.com', 'kalas.cz', 'lecol.cc'],
    limit=100,
    min_volume=20,
)
```

Filter to CK-relevant terms. Lower volume threshold (20) since CK is a niche market.

### 4. SERP Analysis for Priority CK Terms
For the top 5-10 CK keywords by volume, run SERP analysis:
```python
from tools.seo.seo_research import get_serp_results
results = get_serp_results('custom cycling jersey uk')
```

Note: who ranks, what type of page (product page, landing page, blog post), and where SG would need to appear.

### 5. Opportunity Summary
Top 15 CK keyword opportunities:
- Volume, difficulty, current competition
- What type of content/page would rank
- Whether SG has an existing page that could be optimised or needs a new one

## Acceptance Criteria
- [ ] CK seed keyword volumes extracted
- [ ] All three competitor keyword profiles
- [ ] Keyword gap analysis with CK-relevant filtering
- [ ] SERP analysis for priority CK terms
- [ ] Top 15 opportunities identified
- [ ] Findings written to `competitor-ck.md`

## Cost Awareness
Budget: ~$1-2 max for this task.

## Testing
- Test framework: none (research task)
- Tests required: no

## Output
Write findings to `.state/research/competitor-ck.md`. Append summary to `.state/handoff.md`. Update task status in `.state/tasks.jsonl`.
