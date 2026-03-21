# TASK-001: Design the Research Agent

## Objective
Design a Research agent that becomes the fourth permanent member of Pablo's agent team (alongside Planner, Builder, Reviewer). It provides deep web research capabilities using Brave Search MCP, and can be invoked either:
- **Before the Planner** — when a project needs domain research before planning begins
- **By the Planner** — when the Planner identifies research gaps during task breakdown

## Context

### Existing team structure
- **Planner** (`agents/planner/CLAUDE.md`) — specs, architecture, task breakdowns. Reads/writes `.state/` files.
- **Builder** (`agents/builder/CLAUDE.md`) — code implementation. Executes task briefs exactly.
- **Reviewer** (`agents/reviewer/CLAUDE.md`) — code audit, quality checks. Reads changed files only.
- **Orchestrator** (`pablo.sh`) — invokes agents via `claude -p --append-system-prompt`, manages state.
- All agents follow the same pattern: read task brief → do work → write to `.state/handoff.md`

### Invocation pattern (from pablo.sh)
```bash
claude -p --append-system-prompt "$(cat agents/<agent>/CLAUDE.md)" \
  "Read your task brief at .state/briefs/TASK-NNN.md and execute it."
```

### Brave Search MCP
- Not yet configured in the project
- Needs adding to `.mcp.json` (Claude Code's MCP config)
- Provides web search and page content retrieval via MCP tools
- The Research agent would be the primary consumer of Brave Search

### What the Research agent should enable
1. **Domain research** — "What does the landscape look like for X?" before starting a project
2. **Technical research** — "What's the best library/approach for Y?" to inform the Planner
3. **Competitive research** — "Who else does Z and how?" for business context
4. **Fact-checking** — "Is this still current? Has anything changed?" to validate assumptions

### How the Planner might invoke it
The Planner could write a research brief to `.state/briefs/` and recommend Pablo invoke the Researcher before continuing. This keeps the existing pattern intact — Pablo always decides who runs next.

## Scope

### Files to read (for context)
- `agents/planner/CLAUDE.md` — understand the Planner's interface
- `agents/builder/CLAUDE.md` — understand the Builder's interface
- `agents/reviewer/CLAUDE.md` — understand the Reviewer's interface
- `skills/orchestrator/delegation.md` — task brief format and scoping rules
- `skills/orchestrator/escalation.md` — escalation rules
- `pablo.sh` — orchestrator invocation pattern

### Files to create/modify
- `.state/plan.md` — update with architecture and milestones
- `.state/tasks.jsonl` — create task backlog for building the agent
- `.state/decisions.md` — log design decisions
- `.state/handoff.md` — planning summary
- `.state/briefs/TASK-002.md` through `TASK-00N.md` — task briefs for builder

### Out of scope
- Actually building the agent (that's for the Builder)
- Modifying existing agent CLAUDE.md files
- Changing pablo.sh (that comes later, in a builder task)

## Acceptance Criteria
- [ ] Research agent's role, identity, inputs, and outputs are fully specified
- [ ] The agent fits the existing team pattern (reads brief → does work → writes handoff)
- [ ] Brave Search MCP integration is designed (what tools, how configured)
- [ ] Clear interface defined: how Pablo and the Planner invoke the Researcher
- [ ] Research output format is defined (where findings go, what structure)
- [ ] Task breakdown produced for the Builder to implement (CLAUDE.md, MCP config, orchestrator updates)
- [ ] Each builder task scoped to 5 files max

## Output
Update `.state/plan.md` with the full design. Write builder tasks to `.state/tasks.jsonl` and briefs to `.state/briefs/`. Summarise in `.state/handoff.md`.
