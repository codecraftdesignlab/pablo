# TASK-002 through TASK-006: Milestone 1 — Foundation & Data Layer

## Objective

Build the complete foundation for the SG Analysis reporting tool: project scaffolding, data loader, section plugin system, one proof-of-concept section (Season Performance), and Markdown output to the SG Vault.

## Context

SG Analysis is a Python tool that generates daily business reports for Stolen Goat. It loads data from JSON files into pandas DataFrames and runs pre-built analytical sections. No AI SQL generation — all business logic is hardcoded.

**This is a NEW project** — you are creating everything from scratch at `C:\ClaudeProjects\sg-analysis\`.

## Data Sources

The tool loads 4 JSON files from the SkynetPowerDash Repository:
- `C:\Users\timbl\stolen goat Dropbox\tim bland\Stolen Goat\SkynetPowerDash\Repository\articles.json`
- `C:\Users\timbl\stolen goat Dropbox\tim bland\Stolen Goat\SkynetPowerDash\Repository\operationalSkus.json`
- `C:\Users\timbl\stolen goat Dropbox\tim bland\Stolen Goat\SkynetPowerDash\Repository\orders.json`
- `C:\Users\timbl\stolen goat Dropbox\tim bland\Stolen Goat\SkynetPowerDash\Repository\products.json`

**IMPORTANT**: Before writing the loader, READ the first few records of each JSON file to understand the exact structure, field names, and nesting. Do NOT assume field names — inspect the actual data.

## Database Schema Reference

Read the full schema reference to understand the data model:
`C:\Users\timbl\stolen goat Dropbox\tim bland\Stolen Goat\Multichannel Manager\Tools\data-diver\src\DataDiver\DataDiver.AI\Prompts\SchemaProvider.cs`

Key points:
- **orders** have nested `line_items` and `coupon_lines` arrays
- **operationalSkus** fields include: sku, article_number, product_id, label, design_name, backstage_number, status, category, gender, size, supplier, cost_price, rrp, available, sold_7d/30d/90d/6m/12m, open_supplier_order, is_custom_kit, etc.
- **articles** have: article, sku_stem, description, supplier, category, gender, cost_price, rrp, moq, is_custom
- **products** have: id, name, short_description, web_sku, status

## Business Rules (MUST be baked into the data layer)

1. **Collection** = `is_custom_kit == 0` (or `is_custom_kit == False`) AND SKU does NOT start with "CK". Sold B2C. Needs reorder analysis.
2. **Custom Kit** = `is_custom_kit == 1` (or `is_custom_kit == True`). Made to order. No reorder analysis needed.
3. **Lead time** = 8 weeks (56 days) for collection production.
4. **Revenue** = always ex-VAT: `line_item.total - line_item.total_tax`
5. **Bioracer** = dead supplier. Exclude from ALL reorder recommendations (but include in sales/performance reports).
6. **Order exclusions**: status NOT IN ('cancelled', 'refunded', 'pending_payment', 'on-hold', 'internal')
7. **Seasonal status** values: SS26, SS25, AW25, AW24, CORE, ARCHIVE, RETIRE, CUSTOM
8. **Gender** values: MENS, WOMENS, NONE, UNISEX, KIDS (uppercase)
9. **Product grouping**: Multiple SKUs share the same `product_id` (different sizes). Group by product_id for product-level analysis.

## What to Build

### 1. Project Scaffolding
Create at `C:\ClaudeProjects\sg-analysis\`:

**pyproject.toml** with dependencies:
- pandas
- jinja2
- python-dotenv

(Do NOT include google-api-python-client yet — that's for a later milestone)

**Package structure:**
```
sg_analysis/
├── __init__.py
├── main.py
├── config.py
├── data/
│   ├── __init__.py
│   ├── loader.py
│   └── models.py
├── sections/
│   ├── __init__.py
│   └── season_performance.py
└── output/
    ├── __init__.py
    └── markdown.py
```

**config.py** — All paths and business rule constants:
- JSON source paths
- SG Vault reports output path: `C:\Users\timbl\stolen goat Dropbox\tim bland\SG Vault\reports`
- Lead time (56 days)
- Dead suppliers list: ['Bioracer']
- Excluded order statuses
- Current season: 'SS26'

### 2. Data Loader (`data/loader.py`)
- Function to load each JSON file into a pandas DataFrame
- Flatten nested structures (e.g., order line_items should become their own DataFrame with order_id reference)
- `DataStore` class that holds all DataFrames and provides convenience methods

### 3. Business Logic (`data/models.py`)
- Functions/methods to:
  - Classify SKUs as collection or custom kit
  - Calculate daily velocity from sold_30d: `sold_30d / 30`
  - Calculate days of stock cover: `available / daily_velocity`
  - Calculate ex-VAT revenue from line items
  - Filter valid orders (exclude cancelled etc.)
  - Group SKUs to product level

### 4. Section Plugin System (`sections/__init__.py`)
- `Section` abstract base class with:
  - `name: str` — display name
  - `analyse(data: DataStore) -> SectionResult` — run the analysis
  - `render_markdown(result: SectionResult) -> str` — format as markdown
- `SectionResult` dataclass holding: title, summary text, tables (list of DataFrames), insights (list of strings)
- `get_sections() -> list[Section]` — returns all registered sections in order

### 5. Season Performance Section (`sections/season_performance.py`)
Implement the first section as proof of concept:
- Filter to current season (SS26) products
- Join SKUs to order line items to calculate actual revenue and units sold
- Group by product (product_id), summing revenue and quantity
- Rank by revenue descending
- Show top 20 products with: product name, category, gender, revenue (ex-VAT), units sold
- Include a brief summary insight (e.g., "SS26 has generated £X from Y products")

### 6. Markdown Output (`output/markdown.py`)
- `render_report(sections: list[tuple[Section, SectionResult]], date: str) -> str`
- Combines all section outputs into a single markdown document
- Header with report title and date
- Table of contents
- Each section with its rendered markdown

### 7. CLI Runner (`main.py`)
- `main()` function that:
  1. Loads data via DataStore
  2. Runs all registered sections
  3. Renders to markdown
  4. Writes to SG Vault reports folder as `sg-analysis-YYYY-MM-DD.md`
  5. Prints summary to stdout
- Runnable via `python -m sg_analysis`

## Files to Read
- The 4 JSON source files (first few records only — to understand structure)
- `C:\Users\timbl\stolen goat Dropbox\tim bland\Stolen Goat\Multichannel Manager\Tools\data-diver\src\DataDiver\DataDiver.AI\Prompts\SchemaProvider.cs` — schema reference

## Files to Create
- `C:\ClaudeProjects\sg-analysis\pyproject.toml`
- `C:\ClaudeProjects\sg-analysis\sg_analysis/__init__.py`
- `C:\ClaudeProjects\sg-analysis\sg_analysis/main.py`
- `C:\ClaudeProjects\sg-analysis\sg_analysis/config.py`
- `C:\ClaudeProjects\sg-analysis\sg_analysis/data/__init__.py`
- `C:\ClaudeProjects\sg-analysis\sg_analysis/data/loader.py`
- `C:\ClaudeProjects\sg-analysis\sg_analysis/data/models.py`
- `C:\ClaudeProjects\sg-analysis\sg_analysis/sections/__init__.py`
- `C:\ClaudeProjects\sg-analysis\sg_analysis/sections/season_performance.py`
- `C:\ClaudeProjects\sg-analysis\sg_analysis/output/__init__.py`
- `C:\ClaudeProjects\sg-analysis\sg_analysis/output/markdown.py`

## Out of Scope
- HTML/PDF output (later milestone)
- Email delivery (later milestone)
- Any sections beyond Season Performance (later milestone)
- Tests (skip for now — focus on getting the foundation working)
- Git setup

## Acceptance Criteria
- [ ] `python -m sg_analysis` runs without errors from `C:\ClaudeProjects\sg-analysis\`
- [ ] Loads all 4 JSON files into DataFrames successfully
- [ ] Season Performance section produces correct data (SS26 products ranked by revenue)
- [ ] Revenue is calculated ex-VAT
- [ ] Invalid orders are excluded
- [ ] Products are grouped by product_id (not individual SKUs)
- [ ] Markdown report written to `C:\Users\timbl\stolen goat Dropbox\tim bland\SG Vault\reports\sg-analysis-YYYY-MM-DD.md`
- [ ] Adding a new section only requires creating one file in `sections/`

## Coding Standards
- **Tabs** for indentation, never spaces
- **EN-UK spelling** in all text (organise, colour, behaviour)
- Clean, readable code with minimal comments (only where logic isn't self-evident)

## Output
Write results to `.state/handoff.md` in the Pablo project at `C:\ClaudeProjects\pablo\projects\sg-analysis\.state\handoff.md`. Update task status in `C:\ClaudeProjects\pablo\projects\sg-analysis\.state\tasks.jsonl`.
