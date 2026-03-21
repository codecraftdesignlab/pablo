# TASK-002: Create the Researcher agent CLAUDE.md

## Objective
Create the Researcher agent's instruction file at `agents/researcher/CLAUDE.md`. This is the core deliverable — it defines who the Researcher is, what it does, and how it operates within Pablo's agent team.

## Context

### Agent pattern
All agents follow the same structure. See the existing agents for the pattern:
- `agents/planner/CLAUDE.md` — the Planner's instructions
- `agents/builder/CLAUDE.md` — the Builder's instructions
- `agents/reviewer/CLAUDE.md` — the Reviewer's instructions

Each agent CLAUDE.md has these sections: Identity, Inputs, Outputs, File Reading Rules, and role-specific guidance.

### Research output format
The Researcher writes reports to `.state/research/<topic-slug>.md` with this structure:

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

### Tools available to the Researcher
- `WebSearch` — Claude Code's native web search (supports domain allow/block lists)
- `WebFetch` — fetch and analyse specific URLs with AI-powered extraction
- `Read` — read project files for context
- `Write` — write research reports to `.state/research/`

### Design decisions (from .state/decisions.md)
- DEC-001: Use native WebSearch/WebFetch, not Brave Search MCP
- DEC-002: Research output goes to `.state/research/`, summary to `handoff.md`
- DEC-003: Planner-to-Researcher invocation is manual via Pablo

## Scope

### Files to read
- `agents/planner/CLAUDE.md` — reference for agent structure and style
- `agents/builder/CLAUDE.md` — reference for agent structure and style
- `agents/reviewer/CLAUDE.md` — reference for agent structure and style

### Files to create
- `agents/researcher/CLAUDE.md` — the new agent instructions

### Out of scope
- Do not modify any existing agent CLAUDE.md files
- Do not modify pablo.sh
- Do not create the `.state/research/` directory (that's TASK-003)

## Acceptance Criteria
- [ ] File created at `agents/researcher/CLAUDE.md`
- [ ] Has Identity section defining the Researcher's role (research only, no code, no architecture decisions)
- [ ] Has Inputs section (reads task brief, reads project state files for context)
- [ ] Has Outputs section specifying: (1) research report to `.state/research/<topic-slug>.md`, (2) summary to `.state/handoff.md`, (3) task status update to `.state/tasks.jsonl`
- [ ] Includes the full research output format template (as shown in Context above)
- [ ] Has Search Strategy section with guidance on: multi-query approach, source evaluation, domain filtering, depth vs breadth
- [ ] Has File Reading Rules section (consistent with other agents — scoped, not blanket)
- [ ] Has "What NOT to Do" section (no code changes, no architectural decisions, no modifying files outside `.state/`)
- [ ] Uses EN-UK spelling throughout
- [ ] Follows the same structural pattern as other agent CLAUDE.md files
- [ ] Includes guidance on when to use WebSearch vs WebFetch

## Output
Write results to `.state/handoff.md`. Update task status in `.state/tasks.jsonl`.
