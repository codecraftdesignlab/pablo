# TASK-015: Multi-Report Output — sg-analysis + collection-performance + custom-performance

## Objective

Extend sg-analysis to generate 3 daily reports instead of 1. Create new CK sections based on the Analyst's findings (TASK-014). Restructure main.py to support report profiles — each report gets a different composition of sections.

## Context

Currently sg-analysis outputs a single `sg-analysis.md` with 11 sections. Tim wants 3 daily reports:

1. **`sg-analysis.md`** — the full overview (existing 11 sections, unchanged)
2. **`collection-performance.md`** — collection-focused deep dive (reuses Collection Category Performance + Top Collection Products from existing sections)
3. **`custom-performance.md`** — CK-focused deep dive (new sections built from TASK-014 findings)

All 3 write to the same output directory: `C:/Users/timbl/stolen goat Dropbox/tim bland/SG Vault/reports/`

## Files to Read

- `C:/ClaudeProjects/sg-analysis/sg_analysis/main.py` — current single-report runner
- `C:/ClaudeProjects/sg-analysis/sg_analysis/output/markdown.py` — report renderer
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/__init__.py` — section registry
- `C:/ClaudeProjects/sg-analysis/sg_analysis/data/models.py` — utility functions
- `C:/ClaudeProjects/sg-analysis/sg_analysis/data/loader.py` — DataStore
- `C:/ClaudeProjects/sg-analysis/sg_analysis/config.py` — constants
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/top_ck_projects.py` — existing CK section (reference)
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/collection_category_performance.py` — reference
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/gender_split.py` — reference for trend pattern
- `C:/ClaudeProjects/pablo/projects/sg-analysis/.state/research/ck-findings.md` — Analyst findings for CK section content

## Implementation

### 1. Create new CK sections in `sg_analysis/sections/`

**a) `ck_project_performance.py`** — Top CK projects ranked by revenue

Data flow:
- Filter line items to CK only (is_custom_kit == 1)
- Group by product_id (= project proxy), join to products for names
- For each project: total revenue (ex-VAT), total orders, FP %, first/last order date
- Classify as "Growing" (90d rev > prior 90d) / "Declining" / "New" (first order within 90d)

Output tables:
- Top 20 projects by revenue (Product, Revenue, Orders, FP %, Status [Growing/Declining/New])
- New projects (last 90 days): name, revenue, orders

Summary: "**X** active CK projects, **Y** new in last 90 days. Top project: Z with £N revenue."

Insights:
- Revenue concentration: top 5 projects = X% of CK revenue
- New project acquisition: X new projects in last 90 days contributing Y% of CK revenue
- Any declining projects worth flagging (>£1k revenue, declining >50%)

**b) `ck_webshop_performance.py`** — Webshop vs non-webshop split

Webshop classification on orders:
```python
is_webshop = (
    (orders["transaction_id"].fillna("").astype(str).str.strip() != "")
    | orders["number"].astype(str).str.startswith("GE")
)
```

Data flow:
- Join CK line items to orders to get webshop flag
- Split revenue: webshop vs non-webshop
- YoY trend comparison (like-for-like period, same pattern as channel_mix.py)

Output tables:
- Webshop vs Non-webshop: Revenue, Orders, AOV, % of CK revenue
- YoY trend table: channel, current year %, prior year %, change (pp)

Summary: "**Webshop {X}%**, Non-webshop {Y}% of £Z CK revenue. Webshop {direction} {delta}pp YoY."

Insights:
- Webshop growth vs non-webshop growth
- AOV comparison (webshop tends to be smaller individual orders)

**c) `ck_growth_trends.py`** — CK growth trajectory

Data flow:
- Monthly CK revenue (group by year-month from order date_created)
- YoY CK revenue comparison (like-for-like)
- New project count per month
- Revenue concentration (HHI or top-5 share)

Output tables:
- Monthly CK revenue table (last 12 months): Month, Revenue, Orders, New Projects
- YoY comparison: metric, current, prior, change

Summary: "CK revenue **{growth}%** YoY. **{N}** new projects per month average. Top 5 projects = **{X}%** of revenue."

Insights:
- Growth rate
- Revenue concentration risk (high/low)
- Monthly trend direction

**d) `ck_article_performance.py`** — Which designs/articles perform best

Data flow:
- Join CK SKUs to articles via article_number
- Group CK line items by article: revenue, units, project count (unique product_ids using that article)
- Normalise categories

Output tables:
- Top 15 articles: Article Number, Design Name, Revenue, Units, Projects Using, Category
- CK category performance: Category, Revenue, Units, FP %

Summary: "Top article: {name} (£X across Y projects). CK spans Z categories."

Insights:
- Most versatile articles (used by most projects)
- Category performance within CK

**e) `ck_gender_split.py`** — Gender split within CK with trend

Data flow:
- Same pattern as collection gender_split.py but filtered to CK only
- YoY trend comparison

Output tables:
- Revenue by gender: Gender, Revenue, %, Units
- YoY trend: Gender, current share, prior share, change

Summary: "CK gender split: **Mens {X}%**, **Womens {Y}%**. {trend insight}."

Insights:
- Gender trend direction and magnitude

### 2. Modify `main.py` for multi-report output

Replace the single report generation with a report profile system:

```python
REPORT_PROFILES = {
    "sg-analysis": {
        "title": "SG Analysis Report",
        "filename": "sg-analysis.md",
        "sections": None,  # None = all registered sections
    },
    "collection-performance": {
        "title": "Collection Performance",
        "filename": "collection-performance.md",
        "sections": [
            "CollectionCategoryPerformanceSection",
            "TopCollectionProductsSection",
        ],
    },
    "custom-performance": {
        "title": "Custom Kit Performance",
        "filename": "custom-performance.md",
        "sections": [
            "CKProjectPerformanceSection",
            "CKWebshopPerformanceSection",
            "CKGrowthTrendsSection",
            "CKArticlePerformanceSection",
            "CKGenderSplitSection",
        ],
    },
}
```

Main flow:
1. Load data once (DataStore)
2. Run ALL sections once (dedup — each section runs exactly once even if it appears in multiple reports)
3. Render each report profile to its own file using `render_report()`
4. Print summary for each report

The `render_report()` function in markdown.py needs a `title` parameter so each report can have its own heading.

### 3. Register all new CK sections in `sections/__init__.py`

Add the 5 new sections after the existing ones. They need to appear in `get_sections()` so they run in the full sg-analysis.md report too.

### 4. Update `render_report()` in `output/markdown.py`

Add a `title` parameter (default to current behaviour). The frontmatter title and `# heading` should use this title, not hardcoded "SG Analysis Report".

## Scope

- Files to create: `ck_project_performance.py`, `ck_webshop_performance.py`, `ck_growth_trends.py`, `ck_article_performance.py`, `ck_gender_split.py`
- Files to modify: `main.py`, `sections/__init__.py`, `output/markdown.py`
- Out of scope: modifying existing sections, modifying config.py, modifying data layer

## Acceptance Criteria

- [ ] `python -m sg_analysis` generates 3 report files in the SG Vault reports folder
- [ ] sg-analysis.md contains all sections (existing 11 + 5 new CK = 16 total)
- [ ] collection-performance.md contains Collection Category Performance + Top Collection Products
- [ ] custom-performance.md contains the 5 new CK sections
- [ ] Data is loaded exactly once regardless of how many reports are generated
- [ ] Each section runs exactly once
- [ ] All CK sections correctly filter to CK only
- [ ] Webshop classification uses transaction_id and GE prefix
- [ ] Revenue is ex-VAT throughout, formatted as £X,XXX.XX
- [ ] YoY trends use like-for-like period comparison
- [ ] EN-UK spelling, tabs not spaces
- [ ] All existing tests still pass + new tests for CK sections

## Testing

- Test framework: pytest
- Tests required: yes — at least 1 test per new CK section
- Test file: `C:/ClaudeProjects/sg-analysis/tests/test_ck_sections.py`
- Run: `cd C:/ClaudeProjects/sg-analysis && python -m pytest tests/ -v`
- Also run: `python -m sg_analysis` end-to-end — verify 3 reports generated

## Output

Append results to `.state/handoff.md`. Update TASK-015 status to `done` in `.state/tasks.jsonl`.
