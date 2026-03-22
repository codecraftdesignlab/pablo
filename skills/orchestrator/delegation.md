# Agent Delegation

## Invocation Pattern

Pablo invokes agents as sub-processes using Claude Code's `-p` flag with an appended system prompt:

```bash
cd <project-dir>
claude -p --append-system-prompt "$(cat /c/ClaudeProjects/pablo/agents/<agent>/CLAUDE.md)" \
  "Read your task brief at .state/briefs/TASK-NNN.md and execute it. Append your output to .state/handoff.md and update .state/tasks.jsonl when done."
```

## Task Brief Format

Before invoking an agent, Pablo writes a task brief to `.state/briefs/TASK-NNN.md`:

```markdown
# TASK-NNN: <title>

## Objective
What the agent should accomplish.

## Context
Background the agent needs. Reference specific files.

## Scope
- Files to read: list explicitly
- Files to create/modify: list explicitly
- Out of scope: what NOT to touch

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Testing
- Test framework: <pytest|vitest|jest|none>
- Tests required: yes | no (with reason)
- Test file: <expected test file path>

## Output
Append results to `.state/handoff.md`. Update task status in `.state/tasks.jsonl`.
```

## Scoping Rules

- Each task should touch **5 files max**
- List every file the agent needs to read
- List every file the agent may create or modify
- Never give an agent blanket access — scope explicitly

## Agent Output Expectations

After completing a task, agents must:
1. **Append** to `.state/handoff.md` with a separator header (see state-management.md)
2. Update their task entry in `.state/tasks.jsonl` (status -> done)
3. Flag any blockers or questions in handoff.md

## Delegation Flow

1. Pablo reads `.state/plan.md` and `.state/tasks.jsonl`
2. Identifies next task to execute
3. Writes task brief to `.state/briefs/TASK-NNN.md`
4. Logs `agent-invoked` event (agent name, task ID)
5. Invokes appropriate agent
6. Reads `.state/handoff.md` after agent completes
7. Logs `agent-completed` event (verdict if reviewer)
8. Syncs to Obsidian vault (see vault-sync.md)
9. Decides next action: another agent, fix loop, escalate to Tim, or done

## Review Fix Loop

When the Reviewer returns a verdict:

| Verdict | Action |
|---|---|
| **PASS** | Mark task done, proceed to next task |
| **PASS WITH NOTES** (Minor only) | Mark task done, log Minor issues in `decisions.md` as tech debt |
| **PASS WITH NOTES** (Critical/Major) | Enter fix loop (see below) |
| **FAIL** | Enter fix loop (see below) |

### Fix Loop

1. Pablo creates a `TASK-NNN-fix` brief containing only the Reviewer's Critical/Major issues from the `## Fix Required` section
2. Builder executes the fix brief (scoped to only the flagged files)
3. Reviewer re-reviews only the fixed items (not a full re-review)
4. If verdict is still FAIL or has Critical/Major issues after **2 fix iterations**, escalate to Tim

Fix tasks use the status value `fix` and follow the naming convention `TASK-NNN-fix` (or `TASK-NNN-fix-2` for a second iteration).

## Iteration Section

The standard review-fix cycle is:

```
Builder -> Reviewer -> [PASS: done] | [FAIL/Critical: fix loop]
                                          |
                                    Builder (fix) -> Reviewer (re-review)
                                          |
                                    [PASS: done] | [FAIL: escalate after 2 attempts]
```

Pablo manages this loop automatically. No need for Tim's input unless:
- The same issue persists after 2 fix attempts
- The fix would require architectural changes (escalate per escalation.md)

## Session Budget

Budget is tiered by project size:

| Tier | Criteria | Max Invocations |
|---|---|---|
| **Small** | Single milestone, <=5 tasks | 5 |
| **Medium** | Multi-milestone, 6-10 tasks | 8 |
| **Large** | 10+ tasks | 12 |

- Planner declares expected budget in `plan.md` under a `## Budget` section
- Pablo can upgrade tier mid-session if scope grows, but logs the upgrade as `budget-upgrade` event
- If budget is exhausted, pause and report status to Tim
