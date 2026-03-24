# TASK-010: Executive Report — Collection Performance & Tool Improvements

## Objective

Produce a polished, executive-readable report from the Analyst's collection performance findings (TASK-009). The report should answer Tim's questions: what's genuinely growing, where should marketing focus, and how should the sg-analysis tool improve.

## Context

Tim (Founder/Developer) wants to understand collection (non-CK) performance. He's specifically interested in:
- Categories growing on genuine demand (not clearance discounts)
- Growth opportunities outside jerseys (the bread-and-butter)
- Where the marketing team should focus
- How the daily sg-analysis report could better track collection performance

The audience is Tim — he's technical, data-literate, and wants direct conclusions, not hedged language.

## Files to Read

1. `.state/handoff.md` — Analyst's findings summary (TASK-009 section)
2. `.state/research/collection-findings.md` — Analyst's raw findings
3. `.state/briefs/TASK-009.md` — original analysis brief (for context on methodology)

## Report Structure

Write to: `C:/Users/timbl/stolen goat Dropbox/tim bland/SG Vault/reports/collection-performance-2026-03-23.md`

Use this structure:

```markdown
---
title: "Collection Performance Analysis — 23 March 2026"
date: 23-03-2026
tags:
  - stolen-goat
  - analysis
  - collection
  - strategy
type: report
---

# Collection Performance Analysis

> [!summary] Executive Summary
> - Key finding 1
> - Key finding 2
> - Key finding 3
> - Marketing recommendation

## Key Metrics
[Table: category, full-price revenue, clearance revenue, organic %, velocity trend, stock position]

## What's Growing (Full Price)
[Categories with genuine organic growth, ranked. Exclude jersey commentary — Tim knows jerseys sell.]

## Hidden Gems
[Products or categories doing well at full price that might be overlooked]

## What's Declining
[Categories losing momentum or relying on discounting]

## Discount Dependency
[Which categories are clearance-heavy? What does this mean?]

## Where Marketing Should Focus
[Concrete recommendation based on the data. Which 2-3 categories have the best growth potential and why?]

## Tool Improvements
[What the sg-analysis daily report should add or change to better track collection performance. Specific section recommendations with rationale.]

## Data Notes
[Caveats, methodology, date ranges, exclusions]
```

## Scope

- Files to create: `C:/Users/timbl/stolen goat Dropbox/tim bland/SG Vault/reports/collection-performance-2026-03-23.md`
- Files to modify: `.state/tasks.jsonl`, `.state/handoff.md`
- Out of scope: modifying any code, modifying data files

## Acceptance Criteria

- [ ] Executive summary is 4-5 bullet points, directly answers Tim's questions
- [ ] All numbers sourced from Analyst findings — no invented figures
- [ ] Marketing recommendation is concrete and backed by specific data points
- [ ] Tool improvement section has specific, actionable suggestions
- [ ] EN-UK spelling throughout
- [ ] Report is Obsidian-compatible (frontmatter, wiki-links, callout blocks)
- [ ] Report saved to SG Vault reports folder

## Testing

- Test framework: none
- Tests required: no
- Validate: report is readable, numbers are consistent with Analyst findings

## Output

Write report to SG Vault. Append summary to `.state/handoff.md`. Update task status in `.state/tasks.jsonl`.
