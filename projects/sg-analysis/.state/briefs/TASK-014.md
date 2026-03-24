# TASK-014: Custom Kit Performance Deep Dive

## Objective

Analyse Stolen Goat's Custom Kit (CK) business comprehensively — project performance, webshop vs non-webshop, growth trends, gender splits, article performance, and any other useful insights. This will inform the creation of a daily `custom-performance.md` report.

## Context

Custom Kit is Stolen Goat's made-to-order business — clubs, teams, and corporates order bespoke cycling kit. CK is identified by:
- **SKU prefix:** starts with "CK"
- **Line items:** `is_custom_kit == 1`
- **Webshop orders:** orders with a `transaction_id` present OR order number starting with "GE". Webshop orders are self-service via a branded online store per project.

CK currently accounts for 42.2% of total revenue (up from 18.5% last year — massive growth). Tim wants to grow CK very quickly, so insights that help with strategy are valuable.

### Key CK concepts
- **Project:** a club/team/org that orders CK. Identified by the product name or a project identifier.
- **Webshop:** a self-service branded store for a project. Webshop orders are lower-touch (customers order directly). Non-webshop orders are manual/invoice-based.
- **Article:** the underlying design/template. Multiple projects may use the same article. Article data links via `article_number` in SKU data.
- **Repeat orders:** same project ordering multiple times = a healthy project.

## Files to Read

**Data files (all in `C:/Users/timbl/stolen goat Dropbox/tim bland/Stolen Goat/Multichannel Manager/Tools/SkynetPowerDash/Repository/`):**
- `orders.json` — order data with line_items, date_created, status, transaction_id, number (order number)
- `products.json` — product catalogue with categories, names
- `operationalSkus.json` — SKU data with category, gender, article_number, design_name, supplier, velocity fields
- `articles.json` — article data with cost_price, wholesale_price, custom_price, is_custom flag

**Reference:**
- `C:/ClaudeProjects/sg-analysis/sg_analysis/config.py` — existing business rules
- `C:/ClaudeProjects/sg-analysis/sg_analysis/data/models.py` — utility functions

## Analysis Required

Write a Python script and run it. Save script to `.state/research/ck-analysis.py` and findings to `.state/research/ck-findings.md`.

### Part 1: CK Project Performance

1. **Revenue by project:** group CK line items by product (product_id or product name = project proxy). Top 20 projects by revenue.
2. **Project health:** for each project — total revenue, number of orders, number of unique order dates (= order frequency), first order date, last order date, average order value
3. **Successful vs struggling:** projects with >3 orders and growing vs declining (compare recent 90d to prior 90d)
4. **New projects:** projects whose first order is within the last 90 days

### Part 2: Webshop Performance

1. **Classify orders:** webshop = has `transaction_id` (non-empty, not null) OR order number starts with "GE"
2. **Webshop vs non-webshop:** revenue split, order count, AOV, growth trend
3. **Webshop project performance:** which projects have webshops and how are they performing
4. **Webshop growth trend:** compare webshop share YTD vs prior year

### Part 3: CK Growth Trends

1. **YoY growth:** CK revenue this year vs last year (like-for-like period)
2. **Monthly trend:** CK revenue by month (as far back as data allows)
3. **New project acquisition rate:** how many new CK projects per month
4. **Revenue concentration:** what % of CK revenue comes from top 5/10 projects (risk indicator)

### Part 4: Gender & Article Analysis

1. **Gender split within CK:** revenue by gender, trend vs prior year
2. **Article performance:** which articles/designs generate the most revenue across all projects
3. **Top articles:** top 15 articles by revenue with project count (how many different projects use each article)
4. **Article category performance:** which CK categories (jerseys, shorts, etc.) are growing

### Part 5: Discount Analysis

1. **CK discount patterns:** what % of CK revenue is discounted (same >20% threshold)
2. **Compare to collection:** is CK more or less discount-dependent?
3. **Discount by project size:** do larger projects get deeper discounts?

## Scope

- Files to create: `.state/research/ck-analysis.py`, `.state/research/ck-findings.md`
- Files to modify: `.state/tasks.jsonl`, `.state/handoff.md`
- Out of scope: modifying sg-analysis code, modifying data files

## Acceptance Criteria

- [ ] All analysis uses CK products only (collection excluded)
- [ ] Webshop classification uses transaction_id and GE prefix correctly
- [ ] Orders exclude invalid statuses (cancelled, refunded, etc.)
- [ ] Revenue is ex-VAT throughout
- [ ] Findings include raw numbers and percentages
- [ ] Script is runnable standalone
- [ ] Trends use like-for-like period comparison where applicable

## Testing

- Test framework: none
- Tests required: no (analysis script)
- Validate: script runs without errors, totals are internally consistent

## Output

Save findings to `.state/research/ck-findings.md`. Append summary to `.state/handoff.md`. Update task status in `.state/tasks.jsonl`.
