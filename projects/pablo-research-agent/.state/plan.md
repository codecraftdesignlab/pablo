# Research Agent — Project Plan

## Goal
Design and build a Research agent that slots into Pablo's agent team as a fourth permanent member (alongside Planner, Builder, Reviewer). It provides deep web research capabilities using Claude Code's native `WebSearch` and `WebFetch` tools, and can be invoked either:
- **Before the Planner** — when a project needs domain research before planning begins
- **By recommendation of the Planner** — when the Planner identifies research gaps during task breakdown

## Status
- **Phase:** Planning complete — ready for build
- **Started:** 2026-03-21
- **Last updated:** 2026-03-21

---

## Architecture

### Agent Identity & Role

The Researcher is a **read-and-report** agent. It does not modify code, create features, or make architectural decisions. It gathers information from the web, synthesises findings, and writes structured research reports that other agents (primarily the Planner) consume.

**Key characteristics:**
- Uses `WebSearch` for broad discovery queries
- Uses `WebFetch` for deep-reading specific pages
- Writes findings to `.state/research/<topic-slug>.md`
- Summarises key takeaways in `.state/handoff.md`
- Never modifies code or config files

### Tools Available

The agent uses Claude Code's **native tools** — no MCP configuration required:

| Tool | Purpose |
|---|---|
| `WebSearch` | Broad web search queries with domain filtering |
| `WebFetch` | Fetch and analyse specific web pages |
| `Read` | Read existing project files for context |
| `Write` | Write research reports to `.state/research/` |

### Research Output Format

Research reports are written to `.state/research/<topic-slug>.md` with a standardised structure:

```markdown
# Research: <Topic Title>

**Date:** YYYY-MM-DD
**Brief:** briefs/TASK-NNN.md
**Query:** The original research question

## Executive Summary
2-3 sentence overview of key findings.

## Findings

### Finding 1: <Title>
- **Source:** [Name](URL)
- **Detail:** What was found
- **Relevance:** Why it matters to the project

### Finding 2: <Title>
...

## Comparison Table (if applicable)
| Option | Pros | Cons | Notes |
|---|---|---|---|

## Recommendations
Numbered list of actionable recommendations based on findings.

## Sources
- [Source 1](URL) — brief description
- [Source 2](URL) — brief description

## Open Questions
- Things that couldn't be resolved and may need follow-up
```

### Invocation Flow

```
Tim or Pablo identifies research need
        │
        ▼
Pablo writes research brief to .state/briefs/TASK-NNN.md
        │
        ▼
Pablo invokes Researcher:
  claude -p --append-system-prompt "$(cat agents/researcher/CLAUDE.md)" \
    "Read your task brief at .state/briefs/TASK-NNN.md and execute it."
        │
        ▼
Researcher reads brief → searches web → writes report
        │
        ▼
Outputs:
  - .state/research/<topic>.md  (full report)
  - .state/handoff.md           (summary + recommendations)
        │
        ▼
Pablo reads handoff → passes findings to Planner (or Tim)
```

### Integration with Existing Agents

**Planner → Researcher (indirect):**
The Planner cannot invoke agents directly. Instead, it writes a recommendation in `.state/handoff.md`:
```markdown
## Research Needed
- **Topic:** <what to research>
- **Questions:** <specific questions>
- **Suggested brief:** <enough detail for Pablo to write a brief>
```
Pablo then decides whether to invoke the Researcher before continuing.

**Researcher → Planner (via state):**
The Researcher writes its report to `.state/research/`. The Planner's next task brief includes the research report in its "Files to read" list, so the Planner can consume the findings.

### File Structure (new files)

```
pablo/
├── agents/
│   └── researcher/
│       └── CLAUDE.md          # Researcher agent instructions
├── projects/<any-project>/
│   └── .state/
│       └── research/          # Research output directory
│           └── <topic-slug>.md
└── templates/
    └── new-project/
        └── .state/
            └── research/      # Empty dir in template (created by builder)
```

### Orchestrator Updates

`pablo.sh` needs no structural changes. The Researcher follows the identical invocation pattern as all other agents. However, the root `CLAUDE.md` and `config/accounts.yaml` need minor updates to register the new agent:

1. **`CLAUDE.md`** — add Researcher to the Agent Team table
2. **`config/accounts.yaml`** — add `web_search` service entry (documents native tool availability)
3. **`skills/orchestrator/delegation.md`** — add Researcher to the delegation examples (optional, nice-to-have)

---

## Scope Boundaries

### In scope
- `agents/researcher/CLAUDE.md` — full agent instructions
- `.state/research/` directory convention
- Research output format specification
- Updates to root `CLAUDE.md` (agent table)
- Template update for new projects

### Out of scope
- Brave Search MCP configuration (native tools are sufficient — see DEC-001)
- Changes to `pablo.sh` (invocation pattern already works)
- Modifications to other agents' `CLAUDE.md` files
- Automated Planner→Researcher chaining (manual via Pablo for now)

---

## Milestones

### Milestone 1: Core Agent (TASK-002, TASK-003)
Build the Researcher agent's `CLAUDE.md` and establish the `.state/research/` directory convention.

**Deliverables:**
- `agents/researcher/CLAUDE.md` — complete agent instructions
- `templates/new-project/.state/research/.gitkeep` — template directory
- Research output format documented within the agent instructions

### Milestone 2: Registration & Integration (TASK-004)
Register the new agent in Pablo's configuration and documentation.

**Deliverables:**
- Root `CLAUDE.md` updated with Researcher in Agent Team table
- `config/accounts.yaml` updated with web search service entry

### Milestone 3: Validation (TASK-005)
Verify the agent works end-to-end with a real research task.

**Deliverables:**
- Test research brief written
- Agent invoked and produces valid output
- Review of output quality and format compliance
