# SG Analysis — Project Plan

## Goal

Build a standalone Python analytics tool that produces daily reports for Stolen Goat's business data. Outputs to the SG Vault as Markdown and as a polished PDF/HTML emailed to Tim. Replaces the need for complex ad-hoc data-diver queries with pre-built, accurate analytical views that understand the business context (collection vs custom kit, seasonal status, supplier relationships, lead times).

## Context

Data-diver is a natural language → SQL tool that works well for simple one-off questions but struggles with:
- Compound queries (supplier + status + velocity threshold)
- Pre-built analytical views ("show me what matters")
- Business context baked into the logic (CK is made-to-order, collection needs reordering)

SG Analysis is a separate tool that complements data-diver — not a replacement. Data-diver stays for ad-hoc questions and flo-bot integration.

## Data Sources

- **Supabase** (PostgreSQL): articles, SKUs, orders, order line items, products
- **JSON files** (SkynetPowerDash Repository): articles.json, operationalSkus.json, orders.json, products.json
- Same sources as data-diver — 24k+ SKUs, 25k+ orders, 2+ years of history

## Business Rules

- **Collection** = standard retail (is_custom_kit=0, SKUs NOT starting with CK). Sold B2C on website. Needs stock management and reorder analysis.
- **Custom Kit** = bespoke for clubs/groups (is_custom_kit=1). Made to order. Does NOT need reorder analysis.
- **Lead time** = 8 weeks (56 days) for collection production
- **Seasonal status** = SS26, AW25, CORE, ARCHIVE, RETIRE etc.
- **Revenue** = always ex-VAT: SUM(oli.total - oli.total_tax)
- **Bioracer is a dead supplier** — exclude from reorder recommendations
- **Order exclusions**: status NOT IN ('cancelled','refunded','pending_payment','on-hold','internal')

## Report Sections

Sections are modular — new sections can be added over time without restructuring.

1. **Season Performance** — SS26 products: revenue, units sold, ranked by performance
2. **Reorder Alerts** — Collection products under 8 weeks stock cover, grouped by supplier (excl. Bioracer)
3. **Supplier Order Sheets** — Per-supplier view of what needs reordering (qty, cost, MOQ). Includes a ready-to-run data-diver command for each supplier to generate the actual order sheet.
4. **Cross-sell Analysis** — What do customers buy together? What do they buy next after a jersey?
5. **Gender Split** — Revenue and units by gender, trending over time
6. **Channel Mix** — Collection vs Custom Kit revenue, B2B vs D2C, international vs domestic
7. **Stock Health** — Dead stock (no sales in 90d), overstocked, understocked
8. **Velocity Trends** — Products gaining/losing momentum vs prior period
9. **Top CK Projects** — Custom kit projects ranked by revenue this year
10. **YoY Growth** — Year-on-year comparison: B2C collection sales vs custom kit sales

## Output & Delivery

- **Markdown** → `C:\Users\timbl\stolen goat Dropbox\tim bland\SG Vault\reports\` (daily file, e.g. `sg-analysis-2026-03-22.md`)
- **PDF or HTML** → emailed to Tim (tim.bland@stolengoat.com) via existing Gmail integration
- **Trigger** → runs as part of Pablo's `/morning` routine
- **Design** → report must look good — clean typography, clear tables, visual hierarchy

## Scope

### In Scope
- Python CLI tool generating daily Markdown + PDF/HTML reports
- Connects to same data sources as data-diver (Supabase preferred, JSON fallback)
- Pre-built queries with hardcoded business logic (no AI SQL generation)
- Modular section architecture — easy to add new report sections
- Data-diver integration: supplier reorder sections output ready-to-run data-diver commands
- Runs as part of /morning routine
- Emailed report via Gmail API

### Out of Scope
- Interactive dashboard (future phase — potential)
- Replacing data-diver or flo-bot
- Real-time data (batch is fine — daily refresh)
- Write access to any data source

## Architecture

_To be defined by Planner agent._

## Milestones

### Milestone 1 — Foundation & Data Layer
- [ ] Project scaffolding (Python, dependencies, config)
- [ ] Data connection to Supabase (with JSON fallback)
- [ ] Core business logic module (collection vs CK, velocity calcs, stock cover, supplier rules)
- [ ] Section plugin architecture (modular, extensible)
- [ ] Basic report generation (single section proof of concept)

### Milestone 2 — Core Report Sections
- [ ] Season performance view
- [ ] Reorder alerts by supplier (with data-diver command output)
- [ ] Gender split analysis
- [ ] Channel mix breakdown
- [ ] Top CK projects
- [ ] YoY growth comparison

### Milestone 3 — Advanced Analytics
- [ ] Cross-sell / next-purchase analysis
- [ ] Velocity trends (momentum detection)
- [ ] Stock health scoring

### Milestone 4 — Polish & Automation
- [ ] PDF/HTML output formatting (must look good)
- [ ] Markdown output to SG Vault
- [ ] Email delivery via Gmail API
- [ ] Integration with Pablo /morning skill
- [ ] Documentation
