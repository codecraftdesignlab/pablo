# TASK-001: Architecture and task breakdown for SG Analysis

## Objective

Design the full architecture for the SG Analysis reporting tool and break Milestone 1 (Foundation & Data Layer) into builder-ready tasks. Produce a clear technical spec that the Builder can execute without ambiguity.

## Context

SG Analysis is a new Python tool that generates daily business reports for Stolen Goat. It reads from the same data sources as the existing data-diver tool (.NET/C#) but takes a fundamentally different approach: pre-built queries with hardcoded business logic instead of AI-generated SQL.

### Key facts
- **Data sources**: Supabase PostgreSQL (primary) with JSON file fallback. Schema documented in `.state/plan.md`.
- **Database schema**: Same as data-diver — see the full schema reference at `C:\Users\timbl\stolen goat Dropbox\tim bland\Stolen Goat\Multichannel Manager\Tools\data-diver\src\DataDiver\DataDiver.AI\Prompts\SchemaPrompt.cs` for table definitions, views, and business rules.
- **Supabase connection**: `C:\Users\timbl\stolen goat Dropbox\tim bland\Stolen Goat\Multichannel Manager\Tools\data-diver\supabase-connection.txt`
- **JSON source files**: Located at `C:\Users\timbl\stolen goat Dropbox\tim bland\Stolen Goat\SkynetPowerDash\Repository\` (articles.json, operationalSkus.json, orders.json, products.json)
- **Output**: Markdown file to `C:\Users\timbl\stolen goat Dropbox\tim bland\SG Vault\reports\`, plus PDF/HTML emailed via Gmail API
- **10 report sections** defined in plan.md — must be modular/pluggable so new sections can be added easily
- **Data-diver integration**: Reorder sections should output ready-to-run data-diver CLI commands
- **Runs as part of Pablo's /morning skill** — needs to be invocable from Pablo's Python/bash infrastructure
- **Existing Pablo infrastructure**: Gmail sending via Google service account (see `C:\ClaudeProjects\pablo\tools\gmail\CLAUDE.md`), Obsidian vault integration

### Business rules (critical — must be baked into the data layer)
- Collection = is_custom_kit=0, SKUs not starting with CK. Needs reorder analysis.
- Custom Kit = is_custom_kit=1. Made to order. No reorder analysis.
- Lead time = 8 weeks (56 days)
- Revenue = always ex-VAT: SUM(oli.total - oli.total_tax)
- Bioracer = dead supplier, exclude from reorder recommendations
- Order exclusions: status NOT IN ('cancelled','refunded','pending_payment','on-hold','internal')

## Scope

- Files to read:
  - `.state/plan.md` — project plan with sections and milestones
  - `.state/decisions.md` — existing decisions
  - `.state/tasks.jsonl` — current task backlog
  - `C:\Users\timbl\stolen goat Dropbox\tim bland\Stolen Goat\Multichannel Manager\Tools\data-diver\src\DataDiver\DataDiver.AI\Prompts\SchemaPrompt.cs` — full database schema reference
  - `C:\ClaudeProjects\pablo\tools\gmail\CLAUDE.md` — Gmail integration reference

- Files to create/modify:
  - `.state/plan.md` — add Architecture section
  - `.state/tasks.jsonl` — add builder tasks for Milestone 1
  - `.state/briefs/TASK-002.md` through `.state/briefs/TASK-00N.md` — task briefs for each builder task
  - `.state/decisions.md` — log architectural decisions
  - `.state/handoff.md` — summary and next steps

- Out of scope: writing any implementation code

## Acceptance Criteria

- [ ] Architecture section in plan.md covers: project structure, data layer design, section plugin pattern, output pipeline, config approach
- [ ] Technology choices documented with rationale (database driver, PDF library, email sending, etc.)
- [ ] Milestone 1 broken into 3-6 builder tasks, each scoped to ≤5 files
- [ ] Each task has a brief in `.state/briefs/` with clear acceptance criteria
- [ ] Data layer design handles both Supabase and JSON fallback
- [ ] Section architecture is modular — adding a new section should be a single file
- [ ] Decisions logged in decisions.md

## Output

Write results to `.state/handoff.md`. Update task status in `.state/tasks.jsonl`.
