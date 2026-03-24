# TASK-012: New Collection Performance Sections

## Objective

Create two new report sections for the sg-analysis tool: Collection Category Performance (P2) and Top Collection Products (P3). Register them in the section plugin system.

## Context

TASK-011 added discount classification utilities to `models.py`. This task uses those utilities to build two new sections focused on collection (non-CK) performance tracking.

The section plugin architecture: each section is a class inheriting from `Section` in `sections/__init__.py`, implementing `name` (property) and `analyse(data: DataStore) -> SectionResult`. Registration is in `get_sections()` in `__init__.py`.

## Files to Read

- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/__init__.py` — Section ABC and registration
- `C:/ClaudeProjects/sg-analysis/sg_analysis/data/models.py` — business logic utilities (classify_collection, classify_discount, normalise_category, ex_vat_revenue, filter_valid_orders, filter_valid_line_items, group_skus_to_product_level, daily_velocity, days_of_stock_cover)
- `C:/ClaudeProjects/sg-analysis/sg_analysis/data/loader.py` — DataStore class
- `C:/ClaudeProjects/sg-analysis/sg_analysis/config.py` — constants (EXCLUDED_ORDER_STATUSES, CURRENT_YEAR, etc.)
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/season_performance.py` — reference for style and patterns
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/stock_health.py` — reference for category-level analysis
- `C:/ClaudeProjects/pablo/projects/sg-analysis/.state/research/collection-findings.md` — Analyst findings for reference on what data to surface

## Implementation

### 1. Create `collection_category_performance.py` (P2)

New section: `sg_analysis/sections/collection_category_performance.py`

This section provides a category-level view of collection performance — the equivalent of a daily category dashboard. It answers: "How is each collection category performing?"

**Data flow:**
1. Get valid orders + line items (using `filter_valid_orders`, `filter_valid_line_items`)
2. Filter to collection only (line items where SKU does NOT start with "CK")
3. Join line items to SKU data to get category (via `sku` field)
4. Normalise categories using `normalise_category()`
5. Classify each line item as full-price or clearance using `classify_discount(subtotal, total)`
6. Aggregate by category

**Output table:**

| Category | Revenue (ex-VAT) | FP Revenue | FP % | Units | Sold 30d | Acceleration | Stock | Zero-Stock % |
|---|---|---|---|---|---|---|---|---|

Where:
- Revenue = total ex-VAT revenue from all valid orders
- FP Revenue = ex-VAT revenue from full-price line items only
- FP % = FP Revenue / Revenue * 100
- Units = total quantity sold
- Sold 30d = aggregate sold_30d from operational SKUs in this category
- Acceleration = sold_30d / (prior 60d monthly avg) where prior 60d monthly avg = (sold_90d - sold_30d) / 2. If prior avg is 0, show "New"
- Stock = total available units from operational SKUs
- Zero-Stock % = percentage of SKUs at zero available stock

**Sort by:** FP Revenue descending

**Summary text:** "Collection performance across {N} categories. Total: £X FP revenue (Y% of total)."

**Insights:**
- Top 3 accelerating categories (>1.0x acceleration, >5 units sold_30d)
- Categories with >30% clearance revenue (warning)
- Categories with >80% zero-stock SKUs and >10 units sold_30d (stock risk)

### 2. Create `top_collection_products.py` (P3)

New section: `sg_analysis/sections/top_collection_products.py`

The collection equivalent of Top CK Projects. Shows the top 20 collection products by full-price revenue in the last 30 days.

**Data flow:**
1. Get valid orders + line items, filtered to last 30 days (using order `date_created`)
2. Filter to collection only (not CK)
3. Classify discount on each line item
4. Filter to full-price line items only
5. Aggregate by product_id: FP revenue, units, quantity
6. Join to products table for names, to SKU data for category/gender/stock/velocity

**Output table:**

| # | Product | Category | Gender | FP Revenue (30d) | Units | Velocity Trend | Stock |
|---|---|---|---|---|---|---|---|

Where:
- FP Revenue (30d) = full-price ex-VAT revenue in the last 30 days
- Velocity Trend = sold_7d annualised vs sold_30d annualised — "↑" if 7d rate > 30d rate, "↓" if lower, "→" if similar (within 20%)
- Stock = total available units from operational SKUs for this product

**Sort by:** FP Revenue (30d) descending, top 20

**Summary text:** "Top 20 collection products by full-price revenue in the last 30 days."

**Insights:**
- Top seller name and revenue
- How many of the top 20 have <2 weeks of stock (risk)
- Categories represented in the top 20 (diversity indicator)

### 3. Register both sections in `sections/__init__.py`

Add imports and append to the `get_sections()` return list. Place them after the existing sections:

```python
from sg_analysis.sections.collection_category_performance import CollectionCategoryPerformanceSection
from sg_analysis.sections.top_collection_products import TopCollectionProductsSection

# In the return list, add after VelocityTrendsSection:
CollectionCategoryPerformanceSection(),
TopCollectionProductsSection(),
```

## Scope

- Files to create: `collection_category_performance.py`, `top_collection_products.py`
- Files to modify: `sections/__init__.py` (registration only)
- Out of scope: modifying any existing section, modifying models.py, modifying config.py

## Acceptance Criteria

- [ ] Both new sections produce valid SectionResult output
- [ ] Collection Category Performance shows all categories with FP/clearance split
- [ ] Top Collection Products shows top 20 by FP revenue (last 30 days)
- [ ] Both sections filter out CK products
- [ ] Categories normalised using `normalise_category()`
- [ ] Both sections registered and appearing in report output
- [ ] `python -m sg_analysis` runs successfully with all 11 sections
- [ ] EN-UK spelling, tabs not spaces, follow existing code conventions

## Testing

- Test framework: pytest
- Tests required: yes — at least one test per section verifying it returns a valid SectionResult
- Test file: `C:/ClaudeProjects/sg-analysis/tests/test_new_sections.py`
- Run: `cd C:/ClaudeProjects/sg-analysis && python -m pytest tests/ -v`
- Also run `python -m sg_analysis` end-to-end

## Output

Append results to `.state/handoff.md`. Update TASK-012 status to `done` in `.state/tasks.jsonl`.
