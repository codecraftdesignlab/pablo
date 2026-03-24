# TASK-009: Collection Performance Deep Dive — Discount-Adjusted Analysis

## Objective

Analyse Stolen Goat's **collection** (non-custom-kit) product performance across all categories. Separate genuine organic demand from discount-driven/clearance sales. Identify which categories and products are genuinely growing — especially outside jerseys. Also review the sg-analysis tool's existing sections and identify gaps for better collection performance tracking.

## Context

Stolen Goat sells two types of product:
- **Collection** — standard retail products sold B2C on the website. Needs stock management.
- **Custom Kit (CK)** — bespoke team/club kit, made to order. SKUs start with "CK" or have `is_custom` flag.

**This analysis focuses on Collection only — exclude all CK products.**

Tim's key question: "What's genuinely growing outside our bread-and-butter (jerseys)? Where should marketing focus?"

Business rule: if a product is selling at >20% discount, it's likely clearance — don't count it as organic growth. Still report it, but separately.

### Data date note
The orders.json date field was fixed (Z suffix stripping) and covers 2024–2026 with ~25,700 orders and ~43,900 line items. Use `date_created` for time filtering.

### Category cleanup
Categories in SKU data have some inconsistencies (e.g. "GILET" vs "GILETS", "HEAD AND NECK" vs "HEAD & NECK"). Normalise these in your analysis.

## Files to Read

**Data files (all in `C:/Users/timbl/stolen goat Dropbox/tim bland/Stolen Goat/Multichannel Manager/Tools/SkynetPowerDash/Repository/`):**
- `orders.json` — order data with line_items, coupon_lines, date_created, status
- `products.json` — product catalogue with categories, prices, status
- `operationalSkus.json` — SKU-level data with category, gender, velocity (sold7d/30d/90d/6m/12m), salePrice, onOutlet, supplier, status, available stock

**SG Analysis tool (for gap analysis):**
- `C:/ClaudeProjects/sg-analysis/sg_analysis/config.py` — business rules and field mappings
- `C:/ClaudeProjects/sg-analysis/sg_analysis/sections/*.py` — all 9 existing report sections
- `C:/ClaudeProjects/sg-analysis/sg_analysis/main.py` — report orchestration

**Today's report:**
- `C:/Users/timbl/stolen goat Dropbox/tim bland/SG Vault/reports/sg-analysis-2026-03-23.md`

## Analysis Required

Write a Python script and run it to produce the findings below. Save the script to `.state/research/collection-analysis.py` and raw output to `.state/research/collection-findings.md`.

### Part 1: Collection Category Performance

For each product category (normalised — merge duplicates like GILET/GILETS):

1. **Revenue split**: total revenue (ex-VAT), units sold, number of SKUs, average order value
2. **Full-price vs discounted split**:
   - For each order line item: `discount_pct = (subtotal - total) / subtotal * 100`
   - If `discount_pct > 20%`: classify as "clearance"
   - Report: full-price revenue, clearance revenue, % of category revenue at full price
3. **Velocity**: aggregate sold7d, sold30d, sold90d across SKUs in each category
4. **Growth signal**: compare sold30d rate vs sold90d rate (is the category accelerating or decelerating?)
5. **Stock position**: total available units, number of SKUs at zero stock

### Part 2: Non-Jersey Growth Opportunities

Focus on categories OTHER than "JERSEYS & TOPS":

1. Which categories have the highest full-price revenue growth (30d vs 90d acceleration)?
2. Which have the best full-price sell-through rate?
3. Which have strong velocity but thin stock (opportunity being missed)?
4. Any categories with unexpectedly high repeat purchase rate?

### Part 3: Discount Impact Analysis

Across all collection products:

1. What % of total collection revenue is clearance (>20% discount)?
2. Which categories rely most heavily on discounting?
3. Are there products that sell well at full price in categories that are mostly discounted? (hidden gems)

### Part 4: Tool Gap Analysis

Review the 9 existing sg-analysis sections. For each, note:
- Does it separate CK from collection? (most do, but verify)
- Does it account for discount/clearance?
- What collection-specific insight is missing?

Then list recommended new sections or improvements that would make the daily report more useful for tracking collection performance. Frame as findings ("the data supports X analysis but the tool doesn't surface it"), not recommendations.

## Scope

- Files to create: `.state/research/collection-analysis.py`, `.state/research/collection-findings.md`
- Files to modify: `.state/tasks.jsonl`, `.state/handoff.md`
- Out of scope: modifying the sg-analysis tool code, modifying any data files

## Acceptance Criteria

- [ ] All analysis uses collection products only (CK excluded)
- [ ] Discount classification uses line item subtotal vs total, threshold 20%
- [ ] Categories normalised (no duplicate category names)
- [ ] Findings include raw numbers, not just percentages
- [ ] Tool gap analysis covers all 9 existing sections
- [ ] Orders exclude cancelled, refunded, pending_payment, on-hold, internal, pending, failed, trash, draft statuses
- [ ] Script is runnable standalone

## Testing

- Test framework: none
- Tests required: no (analysis script, not production code)
- Validate: script runs without errors, output numbers are internally consistent (category totals sum to overall total)

## Output

Save findings to `.state/research/collection-findings.md`. Append summary to `.state/handoff.md`. Update task status in `.state/tasks.jsonl`.
