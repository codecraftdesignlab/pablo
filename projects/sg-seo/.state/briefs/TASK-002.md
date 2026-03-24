# TASK-002: Audit Current GSC Position and GA4 Site Search

## Objective

Audit Stolen Goat's current organic search performance using Google Search Console and GA4. Produce a comprehensive baseline of what the site currently ranks for, which pages drive organic traffic, and what visitors search for on-site.

## Context

This is the first research task for the SG SEO project. The output will feed into keyword universe building (TASK-005) and the final strategy (TASK-006). We need to understand the current baseline before targeting new keywords.

- SG main site: `https://stolengoat.com/`
- GSC guide: `C:/ClaudeProjects/pablo/tools/search-console/CLAUDE.md`
- GA4 guide: `C:/ClaudeProjects/pablo/tools/analytics/CLAUDE.md`
- GA4 property: `properties/310109076` (main site) — **MUST exclude Chinese bot traffic** (see GA4 guide)
- GA4 CK property: `properties/515401720`

## Scope

### Files to read
- `C:/ClaudeProjects/pablo/tools/search-console/CLAUDE.md`
- `C:/ClaudeProjects/pablo/tools/analytics/CLAUDE.md`

### Files to create
- `C:/ClaudeProjects/pablo/projects/sg-seo/.state/research/gsc-audit.md` — full findings

### Out of scope
- Competitor analysis (TASK-003 and TASK-004)
- Keyword expansion (TASK-005)
- Strategy recommendations (TASK-006)

## Required Analysis

### 1. Top Queries (GSC)
Pull top 200 queries by clicks over the last 90 days. For each:
- Query text, clicks, impressions, CTR, average position
- Group by: branded (contains "stolen goat" or "stolengoat") vs non-branded

### 2. Striking Distance Keywords (GSC)
Pull queries where average position is between 5.0 and 20.0 over the last 90 days. These are keywords close to page 1 or top 3 that could be improved with on-page optimisation. Minimum 10 impressions to filter noise.

### 3. Top Landing Pages (GSC)
Pull top 50 pages by organic clicks over the last 90 days. Include clicks, impressions, CTR, average position.

### 4. On-Site Search Terms (GA4)
Pull site search terms from GA4 (dimension: `searchTerm`) over the last 90 days. If the data is not available (site search tracking not configured), note this as a finding and skip.

### 5. Organic Traffic Overview (GA4)
Pull organic traffic summary for last 90 days (bot traffic excluded):
- Total organic sessions, users
- Organic conversion rate (ecommerce purchases / sessions)
- Top organic landing pages by sessions (top 20)

## Acceptance Criteria
- [ ] Top 200 queries extracted and categorised (branded vs non-branded)
- [ ] Striking distance keywords identified (position 5-20, min 10 impressions)
- [ ] Top 50 landing pages by organic clicks
- [ ] GA4 site search terms pulled (or flagged as unavailable)
- [ ] Organic traffic overview with conversion context
- [ ] All findings written to `gsc-audit.md` with clear tables

## Testing
- Test framework: none (research task)
- Tests required: no

## Output
Write findings to `.state/research/gsc-audit.md`. Append summary to `.state/handoff.md`. Update task status in `.state/tasks.jsonl`.
