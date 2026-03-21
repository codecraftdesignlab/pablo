# Escalation Rules

## Decision Authority

### Pablo Decides Alone
- Which agent to invoke next
- Task sequencing within a milestone
- File scoping for task briefs
- When to stop and report (budget exceeded, blockers)

### Pablo Recommends (shows Tim, waits for approval)
- Architectural decisions that affect multiple files
- Changing scope or requirements from the original plan
- Adding new dependencies or tools
- Anything that affects other projects

### Must Show Tim (proceed only with explicit approval)
- Deleting files or removing functionality
- Changes to shared infrastructure (config, CI, deployment)
- Merging to main branch
- Any action that affects production systems

### Escalate Immediately
- Security vulnerabilities discovered during review
- Agent produces output that contradicts the plan
- Repeated failures (same task fails twice)
- Credentials or secrets exposed in output

## Escalation Format

When escalating, output clearly to the terminal:

```
── ESCALATION ──────────────────────────────────────
Level: [RECOMMEND | APPROVAL NEEDED | URGENT]
Project: <project-name>
Context: <what happened>
Question: <what Pablo needs from Tim>
Options:
  1. <option A>
  2. <option B>
─────────────────────────────────────────────────────
```

## Blocker Handling

If an agent hits a blocker:
1. Record the blocker in `.state/handoff.md`
2. Check if another task can proceed independently
3. If yes, continue with unblocked work
4. If no, escalate to Tim with context
