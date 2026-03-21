# Agent Delegation

## Invocation Pattern

Pablo invokes agents as sub-processes using Claude Code's `-p` flag with an appended system prompt:

```bash
cd <project-dir>
claude -p --append-system-prompt "$(cat /c/ClaudeProjects/pablo/agents/<agent>/CLAUDE.md)" \
  "Read your task brief at .state/briefs/TASK-NNN.md and execute it. Write your output to .state/handoff.md and update .state/tasks.jsonl when done."
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

## Output
Write results to `.state/handoff.md`. Update task status in `.state/tasks.jsonl`.
```

## Scoping Rules

- Each task should touch **5 files max**
- List every file the agent needs to read
- List every file the agent may create or modify
- Never give an agent blanket access — scope explicitly

## Agent Output Expectations

After completing a task, agents must:
1. Update `.state/handoff.md` with what they did, what changed, and any issues
2. Update their task entry in `.state/tasks.jsonl` (status → done)
3. Flag any blockers or questions in handoff.md

## Delegation Flow

1. Pablo reads `.state/plan.md` and `.state/tasks.jsonl`
2. Identifies next task to execute
3. Writes task brief to `.state/briefs/TASK-NNN.md`
4. Invokes appropriate agent
5. Reads `.state/handoff.md` after agent completes
6. Decides next action: another agent, escalate to Tim, or done

## Session Budget

Max **5 agent invocations** per session. If more are needed, pause and report status to Tim. Tim can approve additional invocations.
