# TASK-011: Discount Awareness Foundation + Existing Section Updates

## Objective

Add a discount classification utility to the data layer, then update all 7 existing report sections with discount awareness, CK filtering fixes, and category-level improvements.

## Context

The collection performance analysis (TASK-009) identified 7 gaps in the sg-analysis tool. This task implements the foundation utility and applies it across all existing sections. A separate task (TASK-012) will create the 2 new sections.

The sg-analysis tool lives at `C:/ClaudeProjects/sg-analysis/`. It's a Python package (`sg_analysis`) with a plugin-based section architecture.

## Files to Read

- `C:/ClaudeProjects/sg-analysis/sg_analysis/data/models.py` — existing business logic functions
- `C:/ClaudeProjects/sg-analysis/sg_analysis/data/loader.py` — DataStore class
- `C:/ClaudeProjects/sg-analysis/sg_analysis/config.py` — constants
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/__init__.py` — Section ABC
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/season_performance.py`
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/reorder_alerts.py`
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/stock_health.py`
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/yoy_growth.py`
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/velocity_trends.py`
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/gender_split.py`
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/cross_sell.py`
- `C:/ClaudeProjects/pablo/projects/sg-analysis/.state/research/collection-findings.md` — Analyst findings for reference

## Implementation

### 1. Add utility functions to `models.py`

Add these functions to `sg_analysis/data/models.py`:

```python
def classify_discount(subtotal: pd.Series, total: pd.Series, threshold: float = 0.20) -> pd.Series:
	"""Classify line items as full-price or clearance based on discount percentage.

	Clearance = discount > threshold (default 20%).

	Returns:
		Boolean Series — True where the item is clearance.
	"""
	discount_pct = (subtotal - total) / subtotal
	# Guard against division by zero (subtotal == 0)
	discount_pct = discount_pct.fillna(0.0)
	return discount_pct > threshold


def discount_percentage(subtotal: pd.Series, total: pd.Series) -> pd.Series:
	"""Calculate discount percentage for each line item.

	Returns:
		Series of discount percentages (0.0 to 1.0).
	"""
	pct = (subtotal - total) / subtotal
	return pct.fillna(0.0).clip(lower=0.0)


CATEGORY_NORMALISATION = {
	"GILET": "GILETS",
	"HEAD AND NECK": "HEAD & NECK",
	"SPEED & TRISUITS": "SPEED & TRI SUITS",
	"BIB SHORTS": "BIB SHORTS",
	"Bib Shorts": "BIB SHORTS",
	"Jersey": "JERSEYS & TOPS",
	"Jacket": "JACKETS",
	"JACKET": "JACKETS",
	"Accessories": "ACCESSORIES",
	"Nutrition": "NUTRITION",
	"Swim Caps": "HEAD & NECK",
	"Cycling Caps": "HEAD & NECK",
	"CYCLING CAPS": "HEAD & NECK",
	"T-Shirt": "JERSEYS & TOPS",
	"SS JERSEYS": "JERSEYS & TOPS",
	"RACE SUITS": "SPEED & TRI SUITS",
	"SHORTS": "BIB SHORTS",
	"TIGHTS": "BIB-TIGHTS AND TROUSERS",
	"BAGS": "BAGS & PANNIERS",
	"GLASSES & GOGGLES": "EYEWEAR",
}


def normalise_category(category: pd.Series) -> pd.Series:
	"""Normalise category names to canonical forms."""
	return category.replace(CATEGORY_NORMALISATION)
```

### 2. Update `season_performance.py` — Add FP/clearance columns (P1)

After calculating `revenue_ex_vat`, also calculate:
- `is_clearance` using `classify_discount(subtotal, total)`
- Split the revenue aggregation into `fp_revenue` (where not clearance) and `cl_revenue` (where clearance)
- Add columns to the display table: `FP Revenue`, `Clearance Revenue`, `FP %`

### 3. Update `reorder_alerts.py` — Discount-aware velocity (P5)

When showing reorder candidates:
- Join line items to calculate what % of recent sales are clearance
- Add an `Organic Velocity` column showing full-price-only sold_30d
- Flag products where >30% of velocity comes from clearance with a warning: "⚠ clearance-driven"

### 4. Update `stock_health.py` — Category-level summary (P7)

Add a summary table at the TOP of the section showing category-level stock health:
- Category, Available Units, Total SKUs, Zero-Stock SKU %, Weeks of Cover (at current velocity)
- Use `normalise_category()` to merge duplicate categories
- Keep the existing per-product tables below

### 5. Update `yoy_growth.py` — Full-price YoY comparison (P6)

Add a second comparison showing FP revenue only:
- Current year FP revenue vs prior year FP revenue for the same period
- Show both total and FP YoY growth side by side
- This requires joining line items to orders (for date filtering) and using `classify_discount()`

### 6. Update `velocity_trends.py` — Note discount status (P1)

In the velocity tables (accelerating/decelerating products):
- Add a column showing the product's clearance revenue % (from order line items)
- This helps distinguish "genuinely accelerating" from "accelerating because we discounted it"

### 7. Update `gender_split.py` — Filter to collection only (P4)

The gender split currently includes CK data. Filter line items to collection only:
- Join line items to SKU data and filter where `is_custom_kit == 0`
- OR filter line items where SKU doesn't start with "CK"

### 8. Update `cross_sell.py` — Filter to collection only (P4)

Same as gender_split — filter to collection-only line items before analysing cross-sell patterns.

## Scope

- Files to modify: `models.py`, `season_performance.py`, `reorder_alerts.py`, `stock_health.py`, `yoy_growth.py`, `velocity_trends.py`, `gender_split.py`, `cross_sell.py`
- Out of scope: creating new section files, modifying `main.py`, modifying `config.py`, modifying `loader.py`

## Acceptance Criteria

- [ ] `classify_discount()`, `discount_percentage()`, `normalise_category()` added to models.py
- [ ] All 7 existing sections updated with discount awareness or CK filtering
- [ ] Revenue columns formatted as £X,XXX.XX throughout
- [ ] Existing section output preserved (new columns added, not replacing existing ones)
- [ ] `python -m sg_analysis` runs successfully with all changes
- [ ] EN-UK spelling in all text
- [ ] Tabs, not spaces
- [ ] Follow existing code conventions (check imports, naming, docstring style)

## Testing

- Test framework: pytest
- Tests required: yes — test `classify_discount()`, `discount_percentage()`, `normalise_category()` utility functions
- Test file: `C:/ClaudeProjects/sg-analysis/tests/test_models.py`
- Run: `cd C:/ClaudeProjects/sg-analysis && python -m pytest tests/ -v`
- Also run `python -m sg_analysis` end-to-end to verify no regressions

## Output

Append results to `.state/handoff.md`. Update TASK-011 status to `done` in `.state/tasks.jsonl`.
