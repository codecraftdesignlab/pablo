# State Management

## The Fresh-Start Principle

State files replace conversation history. Every agent session starts fresh — the `.state/` directory is the single source of truth.

## .state/ Directory Structure

```
.state/
├── plan.md          # Project goals, scope, architecture, milestones
├── tasks.jsonl      # Task backlog with status tracking
├── decisions.md     # Decision log with rationale
├── handoff.md       # Cumulative agent outputs (append-only)
├── briefs/          # Individual task briefs for agents
│   ├── TASK-001.md
│   ├── TASK-002.md
│   └── ...
└── research/        # Research reports (Researcher agent)
```

## File Descriptions

### plan.md
The project's north star. Contains:
- **Goal:** What the project achieves
- **Scope:** What's in and out
- **Architecture:** Key design decisions and structure
- **Milestones:** Ordered list of deliverables
- **Budget:** Expected session budget tier (Small/Medium/Large)

Updated by the planner agent. Pablo and Tim review changes.

### tasks.jsonl
One JSON object per line. Each task:

```json
{"id": "TASK-001", "title": "...", "status": "todo", "agent": "builder", "milestone": 1, "brief": "briefs/TASK-001.md", "created": "2026-03-21"}
```

**Status values:** `todo` | `in-progress` | `done` | `blocked` | `review` | `fix`

The `fix` status is used for review fix tasks (see delegation.md). Fix tasks follow the naming convention `TASK-NNN-fix`.

### decisions.md
Append-only log:

```markdown
## DEC-001: <title> (2026-03-21)
**Decision:** What was decided
**Rationale:** Why
**Alternatives considered:** What else was on the table
```

### handoff.md
Append-only log of agent outputs. Each agent appends with a separator header:

```markdown
---
## TASK-NNN: <title> (<agent>, YYYY-MM-DD)

- What was done
- Files changed
- Issues or blockers
- Recommendations for next steps
```

**Archive rule:** When handoff.md exceeds 500 lines, move everything above the latest entry to `handoff-archive.md`. Add a note at the top of handoff.md:

```markdown
> Earlier entries archived in handoff-archive.md
```

### briefs/
Pablo writes these before invoking an agent. One file per task. See `delegation.md` for the format.

### research/
Research reports written by the Researcher agent. One file per topic: `<topic-slug>.md`.

## Hygiene Rules

1. **Never delete state files** — archive old content, don't remove it
2. **Tasks are append-only** — update status, don't delete entries from tasks.jsonl
3. **Decisions are permanent** — once logged, a decision stays in the log
4. **Handoff is append-only** — each agent appends with a separator header
5. **Briefs accumulate** — keep all briefs for audit trail
6. **Archive when files grow** — handoff.md at 500 lines, tasks at milestone boundaries

## Archive Pattern

When a milestone completes:
1. Copy `tasks.jsonl` to `tasks-milestone-N.jsonl.bak`
2. Clear completed tasks from active `tasks.jsonl`
3. Add a milestone summary to `plan.md`
4. Keep `decisions.md` intact (it's the full history)
5. Keep `handoff.md` intact (archive if over 500 lines)

## Milestone Summaries

After completing a milestone, Pablo adds to `plan.md`:

```markdown
### Milestone N — Complete (2026-03-21)
- What was delivered
- Key decisions made
- Metrics or observations
```
