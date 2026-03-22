# Agent Team Presets — Design Spec

**Date:** 2026-03-22
**Status:** Approved
**Author:** Pablo + Tim

## Problem

Pablo's agent team is hardcoded to four agents (Planner, Builder, Reviewer, Researcher) suited for software projects. Different types of work — marketing, business analysis, visual design — need different specialist agents. There's no way to swap teams or borrow agents across domains.

## Solution

Introduce **team presets**: named groups of agents that Pablo loads based on the project type. Teams are defined in `config/teams.yaml`. Each project has a primary team, and Pablo can borrow individual agents from other teams when needed.

## Agent Folder Structure

```
agents/
  shared/                        # Available to all teams
    researcher/CLAUDE.md         # (moved from agents/)
    reviewer/CLAUDE.md           # (moved from agents/)
    designer/CLAUDE.md           # NEW — Canva + polished code output
  build/                         # Software projects
    planner/CLAUDE.md            # (moved from agents/)
    builder/CLAUDE.md            # (moved from agents/)
  marketing/                     # Campaigns, content, brand
    strategist/CLAUDE.md         # NEW — positioning, channels, audiences
    copywriter/CLAUDE.md         # NEW — copy, content, messaging
  analysis/                      # Business analysis, reporting
    analyst/CLAUDE.md            # NEW — data analysis, trends, insights
    report-writer/CLAUDE.md      # NEW — polished executive-ready reports
```

### Canonical Agent Names

These are the `"agent"` values used in `tasks.jsonl` and for folder resolution:

| Agent | Canonical name | Path |
|---|---|---|
| Planner | `planner` | `agents/build/planner/CLAUDE.md` |
| Builder | `builder` | `agents/build/builder/CLAUDE.md` |
| Researcher | `researcher` | `agents/shared/researcher/CLAUDE.md` |
| Reviewer | `reviewer` | `agents/shared/reviewer/CLAUDE.md` |
| Designer | `designer` | `agents/shared/designer/CLAUDE.md` |
| Strategist | `strategist` | `agents/marketing/strategist/CLAUDE.md` |
| Copywriter | `copywriter` | `agents/marketing/copywriter/CLAUDE.md` |
| Analyst | `analyst` | `agents/analysis/analyst/CLAUDE.md` |
| Report Writer | `report-writer` | `agents/analysis/report-writer/CLAUDE.md` |

Pablo resolves agent names to paths using `config/teams.yaml`. The `tasks.jsonl` `"agent"` field uses the short canonical name (e.g., `"agent": "copywriter"`). Pablo looks up the agent's team membership in `teams.yaml` to determine the full path.

### Shared Agents

Available to every team without borrowing:

- **Researcher** — web research and source evaluation (unchanged)
- **Reviewer** — quality gate, spec compliance, security checks (unchanged)
- **Designer** — visual output via Canva MCP or polished frontend code (new)

### Build Team

For software projects — apps, tools, scripts, APIs:

- **Planner** — specs, architecture, task breakdowns (unchanged)
- **Builder** — code implementation, tests, documentation (unchanged)

### Marketing Team

For campaigns, content, positioning, brand work:

- **Strategist** — campaign strategy, positioning, audience personas, content calendars. Analogous to Planner but for marketing. Does not write copy or create designs — delegates to Copywriter and Designer.
- **Copywriter** — compelling copy: social posts, email sequences, landing page text, ad copy, blog posts. Takes briefs from Strategist with tone, audience, and message. Follows brand voice. Analogous to Builder but for words.

### Analysis Team

For business analysis, market research, reporting:

- **Analyst** — examines data, identifies trends, finds insights. Can write Python/SQL for data extraction. Works with existing data sources (SG database, vault, web). Data-focused Builder equivalent.
- **Report Writer** — takes Analyst findings and produces polished, readable reports. Markdown, HTML, or PDF-ready output. Can delegate visual polish to Designer. Structures information for executive consumption.

## Designer Agent (Shared)

Dual-mode agent controlled by the task brief:

### Canva Mode (`## Design Mode: canva`)
- Uses Canva MCP tools to create/edit designs
- Social media graphics, presentations, brand materials
- Works with existing brand kits (via `list-brand-kits`)
- Can search, create from templates, or generate new designs
- Output: Canva design URL + export
- **Dependency:** Requires Canva MCP to be configured and active. If Canva MCP is unavailable, Pablo should flag this to Tim and skip Canva tasks or suggest code mode as a fallback.

### Code Mode (`## Design Mode: code`)
- Writes visually polished frontend code
- HTML/CSS/Tailwind landing pages, dashboards, email templates
- PDF report templates (HTML-to-PDF)
- Styled components that go beyond functional
- Output: code files

### Identity
- Visual craftsperson — does not make architectural decisions or write backend logic
- Takes a brief that says "make this look good" and delivers visual output
- Planner/Strategist decides what needs designing; Designer executes

## Team Configuration

### config/teams.yaml

The YAML structure is kept flat enough for shell parsing with `grep`/`sed`. Each team has a simple key-value format with comma-separated agent lists.

```yaml
teams:
  build:
    description: "Software projects — planning, coding, reviewing"
    team-agents: planner, builder
    shared-agents: researcher, reviewer, designer
    keywords: build, code, implement, feature, app, tool, script, api, website

  marketing:
    description: "Campaigns, content, positioning, brand"
    team-agents: strategist, copywriter
    shared-agents: researcher, reviewer, designer
    keywords: marketing, campaign, content, social, brand, launch, copy, email campaign, SEO

  analysis:
    description: "Business analysis, market research, reporting"
    team-agents: analyst, report-writer
    shared-agents: researcher, reviewer, designer
    keywords: analyse, report, metrics, data, research, market, competitors, benchmark
```

Note: `team-agents` and `shared-agents` are comma-separated strings (not YAML lists) for easy shell parsing.

## Team Detection and Selection

### Auto-detection
On first session (including external projects), Pablo matches the instruction against keywords in `config/teams.yaml`. Detection uses keyword counting: count matches per team, and if the top two teams are within 1 match of each other, ask Tim to confirm. Otherwise, announce the detected team and proceed.

### Recording
The detected team is stored in `.state/plan.md` immediately after the title, before `## Goal`:

```markdown
# Project: [Name]

## Team: marketing

## Goal
...
```

### Subsequent sessions
Pablo reads the team from plan.md instead of re-detecting. Tim can override at any time ("switch to the build team").

### Team changes mid-project
When Tim switches teams, Pablo updates `## Team` in plan.md. Existing tasks in `tasks.jsonl` that reference agents from the old team are left as-is — they can still be executed via the borrowing mechanism. No tasks are reassigned or marked blocked automatically.

### Borrowing agents
Pablo can pull individual agents from other teams when the brief requires it. This is a delegation decision — Pablo resolves the borrowed agent's path via `teams.yaml` and includes it in the invocation. No config change needed.

## Integration Changes

### pablo.sh

**Agent path resolution:** Pablo (the orchestrator, running inside Claude) resolves agent paths — not `pablo.sh`. The shell script injects the `teams.yaml` path and the agents directory into Pablo's system context. Pablo reads `teams.yaml`, determines the team (from plan.md or auto-detection), and builds the correct agent path for each invocation.

**`cmd_project` system context additions:**
```
Teams config: /c/ClaudeProjects/pablo/config/teams.yaml
Agents directory: /c/ClaudeProjects/pablo/agents/
```

**`cmd_list`:** show team per project (read from `.state/plan.md`, default "build" if absent).

**`--teams` flag:** Parse `config/teams.yaml` using `grep`/`sed` (the flat YAML format supports this) and display:
```
Teams:
  build — Software projects — planning, coding, reviewing
    team: planner, builder
    shared: researcher, reviewer, designer

  marketing — Campaigns, content, positioning, brand
    team: strategist, copywriter
    shared: researcher, reviewer, designer
  ...
```

### Invocation pattern update
```bash
cd <project-dir>
claude -p --append-system-prompt "$(cat /c/ClaudeProjects/pablo/agents/<team|shared>/<agent>/CLAUDE.md)" \
  "Read your task brief at .state/briefs/TASK-NNN.md and execute it. Append your output to .state/handoff.md and update .state/tasks.jsonl when done."
```

Pablo resolves `<team|shared>` by looking up the agent name in `teams.yaml`: if the agent is in the project's `team-agents`, use the team folder; if in `shared-agents`, use `shared/`.

### skills/orchestrator/delegation.md
- Update invocation pattern to use team-aware paths
- Add team detection logic documentation
- Update the agent team table
- Document borrowing mechanism

### skills/orchestrator/state-management.md
- Add `## Team` to the plan.md format documentation (after title, before Goal)

### Root CLAUDE.md
- Update Agent Team table to show teams and shared agents
- Document team preset concept

### Vault dashboard
- Add team column to projects table

### Backward compatibility
- Existing projects with no `## Team:` in plan.md default to `build`
- All three completed projects continue to work unchanged
- Team detection runs on first session for all new projects (internal and external)

## Files to Create

| File | Description |
|---|---|
| `agents/shared/designer/CLAUDE.md` | Designer agent — Canva + code modes |
| `agents/marketing/strategist/CLAUDE.md` | Marketing strategy agent |
| `agents/marketing/copywriter/CLAUDE.md` | Copywriting agent |
| `agents/analysis/analyst/CLAUDE.md` | Data/business analysis agent |
| `agents/analysis/report-writer/CLAUDE.md` | Report writing agent |
| `config/teams.yaml` | Team definitions and keywords |

## Files to Move

| From | To |
|---|---|
| `agents/planner/CLAUDE.md` | `agents/build/planner/CLAUDE.md` |
| `agents/builder/CLAUDE.md` | `agents/build/builder/CLAUDE.md` |
| `agents/reviewer/CLAUDE.md` | `agents/shared/reviewer/CLAUDE.md` |
| `agents/researcher/CLAUDE.md` | `agents/shared/researcher/CLAUDE.md` |

## Files to Modify

| File | Changes |
|---|---|
| `pablo.sh` | Team-aware context, --teams flag, team in project list |
| `skills/orchestrator/delegation.md` | Team-aware paths, detection logic, borrowing docs |
| `skills/orchestrator/state-management.md` | Add `## Team` to plan.md format |
| `CLAUDE.md` | Updated agent team table with teams |
| `skills/orchestrator/vault-sync.md` | Team column in dashboard |
| `templates/new-project/.state/plan.md` | Add `## Team` placeholder |

## Verification

1. Run `./pablo.sh --teams` — should list all teams with agents
2. Run `./pablo.sh --list` — existing projects show "build" team
3. Start a new marketing project — Pablo should auto-detect and confirm
4. Verify existing build projects still work with moved agent paths
5. Test Designer agent in both Canva and code modes (code mode first; Canva mode requires MCP)
6. Test borrowing: use Copywriter from a build project
7. Test keyword collision: instruction matching multiple teams should prompt Tim
8. Verify template plan.md includes `## Team` placeholder
