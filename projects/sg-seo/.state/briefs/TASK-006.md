# TASK-006: Produce Keyword Strategy and Content Briefs

## Objective

Take the keyword universe and research findings from Milestone 2 and produce an actionable SEO strategy document. This should be a polished, executive-ready report that Tim can review and approve, plus individual content briefs the Copywriter can execute against.

## Context

The research phase is complete:
- **GSC audit** (`.state/research/gsc-audit.md`): Current rankings, striking distance keywords, organic traffic baseline
- **Lifestyle competitor gap** (`.state/research/competitor-lifestyle.md`): 69 gap keywords, Le Col/Rapha/Castelli analysis
- **CK competitor gap** (`.state/research/competitor-ck.md`): Complete CK keyword landscape, SERP analysis, owayo/Kalas as key competitors
- **Keyword universe** (`.state/research/keyword-universe.md`): 156 keywords in 11 clusters, priority matrix, quick wins, new pages needed

Key findings to build strategy around:
1. **Women's cycling shorts** — 250K+/mo, zero SG visibility. Single largest gap.
2. **Custom kit** — 3,700/mo, zero visibility despite +152% YoY CK growth. 5 new pages needed.
3. **"Cycling clothing" head terms** — 60K/mo, SG invisible. Competitors rank via category pages.
4. **Men's jerseys** — 20K/mo, SG on page 2. Existing pages need optimisation.
5. **Quick wins** — 16 keywords already ranking position 5-20, combined 34K/mo. On-page optimisation only.
6. **Category pages beat blogs** — all competitors rank through collection/category pages, not editorial content.

## Scope

### Files to read
- `.state/research/keyword-universe.md` — **PRIMARY INPUT** (the synthesised keyword map)
- `.state/research/gsc-audit.md` — for current ranking baselines
- `.state/research/competitor-lifestyle.md` — for competitor positioning context
- `.state/research/competitor-ck.md` — for CK SERP landscape

### Files to create
- `C:/Users/timbl/stolen goat Dropbox/tim bland/SG Vault/reports/seo-keyword-strategy-2026-03-24.md` — the strategy report (Obsidian-compatible Markdown)
- `.state/briefs/CONTENT-001.md` through `CONTENT-NNN.md` — individual content briefs for new pages

### Out of scope
- Implementing changes (separate tasks)
- Technical SEO (site speed, schema, etc.)
- Link building strategy
- Paid search

## Strategy Document Structure

The report should follow this structure:

### 1. Executive Summary
3-5 bullet points: what the research found, the scale of the opportunity, the recommended approach.

### 2. Current Position
Brief summary of where SG stands organically (from GSC audit). Key numbers: organic sessions, conversion rate, branded vs non-branded split, number of striking distance keywords.

### 3. Priority Actions
Ordered by impact. For each action:
- What to do
- Which keywords it targets (with volumes)
- Expected difficulty (easy / medium / hard)
- Whether it's a new page or optimisation of existing

Group into:
- **Quick wins** (on-page optimisation, existing pages, 1-4 weeks)
- **New pages** (new content creation, 4-8 weeks)
- **Strategic plays** (longer-term positioning, ongoing)

### 4. Keyword Target Map
The full prioritised keyword map from the universe, but presented as an actionable roadmap with target pages and recommended meta titles/H1s.

### 5. Competitor Intelligence
Brief summary of what competitors do well and how SG should position differently. Key insight: category pages beat blogs.

### 6. Content Calendar
Recommended phasing:
- **Phase 1 (weeks 1-4):** Quick wins — on-page optimisation of existing category pages
- **Phase 2 (weeks 4-8):** CK landing pages (must be live before March peak season)
- **Phase 3 (weeks 8-12):** New collection pages (women's shorts, cycling clothing hub)
- **Phase 4 (ongoing):** Monitor, iterate, expand to lower-priority clusters

### 7. On-Site Recommendations
For each page that needs optimisation, provide:
- Current meta title → recommended meta title
- Current H1 → recommended H1
- Content recommendations (what to add/change)
- Internal linking suggestions

### 8. Measurement
How to track success:
- Weekly rank tracking via GSC (tool already built)
- Target positions for each priority keyword
- Traffic and conversion targets at 30/60/90 days

## Content Brief Format

Each content brief at `.state/briefs/CONTENT-NNN.md` should include:
- **Page:** URL (existing or proposed)
- **Target keywords:** primary + secondary with volumes
- **Intent:** transactional / commercial / informational
- **Recommended title tag:** (60 chars max)
- **Recommended meta description:** (155 chars max)
- **Recommended H1:**
- **Content outline:** key sections and what to cover
- **Competitor benchmark:** which competitor page to beat
- **Success metric:** target position and clicks

## Acceptance Criteria
- [ ] Strategy report written and saved to SG Vault
- [ ] Minimum 10 content briefs covering the CRITICAL and HIGH priority clusters
- [ ] Quick wins section with specific on-page recommendations (current vs proposed)
- [ ] Content calendar with phased approach
- [ ] All keyword data sourced from the research files (no fabricated numbers)
- [ ] EN-UK spelling throughout
- [ ] Obsidian-compatible frontmatter on the strategy report

## Testing
- Test framework: none (strategy document)
- Tests required: no

## Output
Write strategy report to SG Vault path above. Write content briefs to `.state/briefs/`. Append summary to `.state/handoff.md`. Update task status in `.state/tasks.jsonl`.
