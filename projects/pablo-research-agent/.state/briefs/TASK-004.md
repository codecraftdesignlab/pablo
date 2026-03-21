# TASK-004: Register the Researcher in Pablo's configuration

## Objective
Update Pablo's root documentation and configuration to register the Researcher as a permanent team member. This makes the agent discoverable and documents the web search capability.

## Context
Pablo's root `CLAUDE.md` has an Agent Team table listing all agents. The `config/accounts.yaml` lists all connected services. Both need updating to reflect the new Researcher agent and its web search tools.

## Scope

### Files to read
- `CLAUDE.md` (project root) — find the Agent Team table and Connected Services table
- `config/accounts.yaml` — understand current service entries
- `agents/researcher/CLAUDE.md` — confirm the agent exists (dependency: TASK-002 must be done first)

### Files to modify
- `CLAUDE.md` (project root) — add Researcher to the Agent Team table; optionally note web search in Connected Services
- `config/accounts.yaml` — add a `web_search` service entry documenting native tool availability

### Out of scope
- Do not modify any agent CLAUDE.md files
- Do not modify pablo.sh
- Do not modify skills/ files
- Do not add Brave Search MCP configuration (DEC-001: using native tools)

## Acceptance Criteria
- [ ] Root `CLAUDE.md` Agent Team table includes: `| Researcher | Web research, domain analysis, competitive intel | agents/researcher/CLAUDE.md |`
- [ ] `config/accounts.yaml` includes a `web_search` entry with status `active`, access `native-tools`, and a note explaining it uses Claude Code's built-in WebSearch and WebFetch
- [ ] No other files modified
- [ ] EN-UK spelling throughout changes

## Output
Write results to `.state/handoff.md`. Update task status in `.state/tasks.jsonl`.
