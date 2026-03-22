# Vault Sync

Pablo mirrors key project state to the Obsidian vault so Tim has visibility without digging into `.state/` directories.

## Vault Path

```
C:\Users\timbl\stolen goat Dropbox\tim bland\Obsidian\projects\<project-name>\
```

## When to Sync

| Trigger | Action |
|---|---|
| Project creation | Create vault folder, write `brief.md` |
| After Planner completes | Sync `plan.md` to vault |
| After any agent completes | Append to `activity-log.md` |
| After decisions are logged | Sync `decisions.md` to vault |
| End of session | Update `project-dashboard.md` |

## Vault Folder Structure

```
Obsidian/projects/<project-name>/
  brief.md           # Initial concept — written once
  plan.md            # Goals, scope, architecture, milestones
  decisions.md       # Decision log with rationale
  activity-log.md    # Timeline of agent activity
```

## File Formats

All files use the standard vault frontmatter and include wiki-links to sibling files.

### brief.md

```markdown
---
title: "<Project Name> — Brief"
date: DD-MM-YYYY
tags:
  - project
  - <project-slug>
type: project
---

# <Project Name> — Brief

**Created:** YYYY-MM-DD
**Instruction:** <the original instruction Tim gave>

## Context
<any additional context from the first session>

See also: [[<Project Name> — Plan]] | [[<Project Name> — Decisions]] | [[<Project Name> — Activity Log]]
```

### plan.md

```markdown
---
title: "<Project Name> — Plan"
date: DD-MM-YYYY
tags:
  - project
  - <project-slug>
type: project
---

# <Project Name> — Plan

See also: [[<Project Name> — Brief]] | [[<Project Name> — Decisions]] | [[<Project Name> — Activity Log]]

<copy of .state/plan.md content>
```

### decisions.md

```markdown
---
title: "<Project Name> — Decisions"
date: DD-MM-YYYY
tags:
  - project
  - <project-slug>
type: project
---

# <Project Name> — Decisions

See also: [[<Project Name> — Brief]] | [[<Project Name> — Plan]] | [[<Project Name> — Activity Log]]

<copy of .state/decisions.md content>
```

### activity-log.md

```markdown
---
title: "<Project Name> — Activity Log"
date: DD-MM-YYYY
tags:
  - project
  - <project-slug>
type: project
---

# <Project Name> — Activity Log

See also: [[<Project Name> — Brief]] | [[<Project Name> — Plan]] | [[<Project Name> — Decisions]]

### YYYY-MM-DD HH:MM — <Agent> (TASK-NNN)
**Task:** <title>
**Status:** Complete | In Progress | Blocked | Failed
**Verdict:** PASS | FAIL | PASS WITH NOTES (reviewer only)
**Files changed:** <list>
**Notes:** <brief summary>
```

Each agent completion appends a new entry at the bottom. Never overwrite previous entries.

## Project Dashboard

Pablo maintains a cross-project dashboard at:

```
Obsidian/projects/project-dashboard.md
```

### Format

```markdown
---
title: "Project Dashboard"
date: DD-MM-YYYY
tags:
  - project
  - dashboard
type: project
---

# Project Dashboard

*Last updated: YYYY-MM-DD HH:MM by Pablo*

| Project | Status | Progress | Last Activity | Blockers |
|---|---|---|---|---|
| [[<Project> — Brief\|<Project>]] | <status> | N/N tasks | YYYY-MM-DD | <blockers or None> |

## Needs Attention
- Items requiring Tim's input or with unresolved Critical/Major review issues

## Recently Completed
- Projects completed in the last 7 days
```

### When to Update

- At the end of every orchestrator session
- During `/morning` briefing (read and report)
- When `./pablo.sh --status` is run

To update: read all vault project folders, check `.state/tasks.jsonl` for each project, and regenerate the dashboard table.

## Rules

1. **Vault is a mirror** — `.state/` is the source of truth, vault is the readable copy
2. **Frontmatter always** — every vault file gets the standard frontmatter block
3. **Wiki-links** — every file links to its siblings and dashboard links to all projects
4. **EN-UK spelling** — organise, colour, behaviour
5. **Reuse tags** — use existing vault tags; add `<project-slug>` tag per project
6. **Never delete vault files** — update or archive, never remove
