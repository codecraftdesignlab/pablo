# TASK-013: Review All Milestone 6 Changes

## Objective

Review all code changes from TASK-011 and TASK-012 — the discount awareness foundation, existing section updates, and two new collection performance sections.

## Context

This milestone added discount classification to the sg-analysis tool:
- TASK-011: Added `classify_discount()`, `discount_percentage()`, `normalise_category()` to models.py. Updated all 7 existing sections with discount awareness and CK filtering fixes.
- TASK-012: Created 2 new sections — Collection Category Performance and Top Collection Products.

The tool now has 11 sections total and 31 passing tests.

## Files to Review

**Data layer:**
- `C:/ClaudeProjects/sg-analysis/sg_analysis/data/models.py` — new utility functions

**Modified sections:**
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/season_performance.py`
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/reorder_alerts.py`
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/stock_health.py`
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/yoy_growth.py`
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/velocity_trends.py`
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/gender_split.py`
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/cross_sell.py`

**New sections:**
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/collection_category_performance.py`
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/top_collection_products.py`
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/__init__.py` — registration

**Tests:**
- `C:/ClaudeProjects/sg-analysis/tests/test_models.py`
- `C:/ClaudeProjects/sg-analysis/tests/test_new_sections.py`

**Generated output (for validation):**
- `C:/Users/timbl/stolen goat Dropbox/tim bland/SG Vault/reports/sg-analysis.md`

## Known Issues to Check

The Builder flagged these — verify they are handled:
1. Empty-string category appears in stock risk insight (blank category SKUs slipping through normalisation)
2. `normalise_category()` applied twice in top_collection_products — harmless but redundant
3. 30-day cutoff uses `pd.Timestamp.now()` rather than a configurable report date
4. Collection FP YoY shows -23.2% — verify this is a real number, not a calculation bug

## Review Checklist

- [ ] Utility functions are correct (classify_discount threshold, edge cases, normalisation coverage)
- [ ] CK filtering is consistent across all sections (same method used everywhere)
- [ ] Discount columns don't break existing output (new columns added, not replacing)
- [ ] Category normalisation covers all variants found in the data
- [ ] Revenue calculations are correct (ex-VAT = total - total_tax)
- [ ] Tests are meaningful (not just asserting True)
- [ ] EN-UK spelling, tabs not spaces throughout
- [ ] No security issues (no hardcoded paths that should be in config, no data leaks)
- [ ] Generated report is readable and accurate

## Output

Append review verdict and findings to `.state/handoff.md`. Update TASK-013 status in `.state/tasks.jsonl`.
