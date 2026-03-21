# Stolen Goat Prospect Agent — Project Plan

## Goal
Proactively find new potential custom kit clients (clubs, charities, corporates, events) via web search, evaluate them with Claude, and write prospect files to the SG Vault — with deep deduplication against existing contacts.

## Status
- **Phase:** Initial build
- **Started:** 2026-03-21

## Architecture
Python CLI tool: `prospect_finder.py`
- `config.py` — paths, API keys, constants
- `dedup.py` — vault deduplication checker
- `researcher.py` — SerpAPI search + page scraping
- `search_strategies.yaml` — query templates by signal tier
- `analyst.py` — Claude API evaluation + structuring
- `vault_writer.py` — write prospect files to SG Vault

## Output
Files written to `SG Vault/prospect-research/` with `type: prospect` frontmatter.

## Lifecycle
Discovery only. Tim reviews manually. Promotion to contacts is out of scope.
