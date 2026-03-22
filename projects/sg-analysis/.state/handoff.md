# Handoff — SG Analysis Complete (2026-03-22)

## Status: ALL MILESTONES COMPLETE

## What was built

Full SG Analysis reporting tool at `C:\ClaudeProjects\sg-analysis\`. Generates daily business reports for Stolen Goat with 10 analytical sections, outputs Markdown + HTML, and creates Gmail drafts.

### Report Sections (10)
1. SS26 Season Performance — current season products ranked by revenue
2. Reorder Alerts — collection products under 8 weeks cover, by supplier (excl. Bioracer), with data-diver commands
3. Gender Split — revenue/units by gender YTD
4. Channel Mix — Collection vs CK, B2B vs D2C, International vs Domestic
5. Top CK Projects — custom kit projects ranked by revenue
6. YoY Growth — year-on-year collection vs CK comparison
7. Cross-sell Analysis — category pairs and post-jersey purchases
8. Stock Health — dead stock, overstocked, critically understocked
9. Velocity Trends — products gaining/losing momentum

### Output
- Markdown: `SG Vault\reports\sg-analysis-YYYY-MM-DD.md`
- HTML: `SG Vault\reports\sg-analysis-YYYY-MM-DD.html`
- Gmail draft: HTML email to tim.bland@stolengoat.com

### CLI
- `python -m sg_analysis` — full run
- `python -m sg_analysis --no-email` — skip email
- `python -m sg_analysis --markdown-only` — markdown only

## Bugs found and fixed
1. Empty supplier names in reorder alerts — filtered out
2. CSS `centre` vs `center` — fixed
3. Hardcoded `_CURRENT_YEAR = 2026` in 4 sections — now uses `config.CURRENT_YEAR`
4. Missing order status exclusions (`pending`, `failed`, `trash`, `draft`) — added

## Known data limitations
- Only 518/25,669 orders have dates (all March 2026) — limits YoY and time-filtered analysis
- This is a data source issue, not a code bug

## Integration pending
- [ ] Add to Pablo's /morning skill
- [ ] Windows Task Scheduler for daily automated run
