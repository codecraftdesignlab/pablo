# TASK-005: Validate Researcher agent with a test research task

## Objective
Write a test research brief, invoke the Researcher agent, and verify that it produces a correctly-formatted research report. This is a **reviewer task** — the Reviewer checks the output against the spec.

## Context
By this point, TASK-002 (agent CLAUDE.md), TASK-003 (research directory), and TASK-004 (registration) should all be complete. This task validates the entire chain works end-to-end.

### Test research topic
Use a simple, verifiable topic: **"What are the current best practices for structuring Claude Code agent teams in 2026?"**

This is meta-research about the very pattern Pablo uses, making it easy to evaluate quality.

## Scope

### This is a two-step task

**Step 1 — Pablo writes and invokes (manual):**
Pablo should write a research brief (this file serves as that brief) and invoke the Researcher:
```bash
cd /c/ClaudeProjects/pablo/projects/pablo-research-agent
claude -p --append-system-prompt "$(cat /c/ClaudeProjects/pablo/agents/researcher/CLAUDE.md)" \
  "Read your task brief at .state/briefs/TASK-005.md and execute it. Research the topic: What are the current best practices for structuring AI coding agent teams? Focus on multi-agent orchestration patterns, task delegation, and state management. Write your findings to .state/research/ai-agent-team-patterns.md"
```

**Step 2 — Reviewer validates output:**
The Reviewer checks that the Researcher's output at `.state/research/ai-agent-team-patterns.md` conforms to the research output format defined in `agents/researcher/CLAUDE.md`.

### Files to read (for review)
- `agents/researcher/CLAUDE.md` — the spec to validate against
- `.state/research/ai-agent-team-patterns.md` — the output to review
- `.state/handoff.md` — the Researcher's summary

### Files to create/modify
- `.state/handoff.md` — review verdict

### Out of scope
- Do not modify the Researcher's CLAUDE.md
- Do not modify the research output (report issues, don't fix them)

## Acceptance Criteria
- [ ] Research report exists at `.state/research/ai-agent-team-patterns.md`
- [ ] Report follows the standardised format (Executive Summary, Findings with sources, Recommendations, Sources list)
- [ ] At least 3 distinct sources cited with URLs
- [ ] Handoff.md contains a summary of findings and recommendations
- [ ] Task status updated in tasks.jsonl
- [ ] No files modified outside `.state/`

## Output
Reviewer writes verdict to `.state/handoff.md`. Updates task status in `.state/tasks.jsonl`.
