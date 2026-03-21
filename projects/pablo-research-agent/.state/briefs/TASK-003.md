# TASK-003: Create research directory in project template and current project

## Objective
Establish the `.state/research/` directory convention by:
1. Adding it to the new-project template so all future projects have it
2. Creating it in the current project (`projects/pablo-research-agent/.state/research/`)

## Context
Research reports are written to `.state/research/<topic-slug>.md` (see DEC-002 in `.state/decisions.md`). This directory needs to exist before the Researcher agent can write to it. It also needs to be part of the project template so new projects get it automatically.

### Template location
New projects are scaffolded from `templates/new-project/.state/`. See `pablo.sh` line 97:
```bash
cp -r "$TEMPLATES_DIR/.state" "$project_dir/.state"
```

## Scope

### Files to read
- `templates/new-project/.state/` — understand current template structure (use `ls` via Bash)
- `pablo.sh` — confirm template copy logic (lines 94-101)

### Files to create
- `templates/new-project/.state/research/.gitkeep` — empty file to preserve directory in git
- `projects/pablo-research-agent/.state/research/.gitkeep` — empty file for current project

### Out of scope
- Do not modify any existing template files
- Do not modify pablo.sh
- Do not create any research report files (those are written by the Researcher at runtime)

## Acceptance Criteria
- [ ] Directory exists: `templates/new-project/.state/research/`
- [ ] File exists: `templates/new-project/.state/research/.gitkeep`
- [ ] Directory exists: `projects/pablo-research-agent/.state/research/`
- [ ] File exists: `projects/pablo-research-agent/.state/research/.gitkeep`
- [ ] No existing template files modified

## Output
Write results to `.state/handoff.md`. Update task status in `.state/tasks.jsonl`.
