# Agent Team Presets — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Introduce team presets so Pablo can load different agent groups (build, marketing, analysis) based on project type, with a shared pool of cross-team agents including a new Designer.

**Architecture:** Restructure `agents/` into team folders (`build/`, `marketing/`, `analysis/`) with a `shared/` pool. Add `config/teams.yaml` for team definitions. Pablo auto-detects team from instruction keywords and records it in `.state/plan.md`. Agent path resolution happens inside Pablo's orchestrator session, not in `pablo.sh`.

**Tech Stack:** Bash (pablo.sh), Markdown (CLAUDE.md files), YAML (teams.yaml)

**Spec:** `docs/superpowers/specs/2026-03-22-agent-team-presets-design.md`

---

### Task 1: Create teams.yaml

**Files:**
- Create: `config/teams.yaml`

- [ ] **Step 1: Write teams.yaml**

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

- [ ] **Step 2: Verify YAML is parseable by grep/sed**

Run: `grep "team-agents:" config/teams.yaml`
Expected: 3 lines with comma-separated agent names

- [ ] **Step 3: Commit**

```bash
git add config/teams.yaml
git commit -m "feat: add teams.yaml — team preset definitions"
```

---

### Task 2: Move existing agents into team folders

**Files:**
- Move: `agents/planner/CLAUDE.md` → `agents/build/planner/CLAUDE.md`
- Move: `agents/builder/CLAUDE.md` → `agents/build/builder/CLAUDE.md`
- Move: `agents/reviewer/CLAUDE.md` → `agents/shared/reviewer/CLAUDE.md`
- Move: `agents/researcher/CLAUDE.md` → `agents/shared/researcher/CLAUDE.md`

- [ ] **Step 1: Create new directories**

```bash
mkdir -p agents/build agents/shared
```

- [ ] **Step 2: Move build team agents**

```bash
git mv agents/planner agents/build/planner
git mv agents/builder agents/build/builder
```

- [ ] **Step 3: Move shared agents**

```bash
git mv agents/reviewer agents/shared/reviewer
git mv agents/researcher agents/shared/researcher
```

- [ ] **Step 4: Remove empty old directories if any remain**

```bash
# git mv should handle this, but verify:
ls agents/
# Expected: build/ shared/ logging/ (logging stays)
```

- [ ] **Step 5: Verify all CLAUDE.md files exist at new paths**

```bash
cat agents/build/planner/CLAUDE.md | head -1
cat agents/build/builder/CLAUDE.md | head -1
cat agents/shared/reviewer/CLAUDE.md | head -1
cat agents/shared/researcher/CLAUDE.md | head -1
```
Expected: Each prints its `# <Agent> Agent` header

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "refactor: move agents into team folders (build/, shared/)"
```

---

### Task 3: Create Designer agent (shared)

**Files:**
- Create: `agents/shared/designer/CLAUDE.md`

- [ ] **Step 1: Write Designer CLAUDE.md**

**Template:** Use `agents/build/builder/CLAUDE.md` as the structural template. Copy its section headings (Identity, Inputs, Outputs, File Reading Rules, Coding Standards, What NOT to Do) and adapt the content. The Designer is a dual-mode shared agent. Key sections:

- Identity: visual craftsperson, not an architect or backend developer
- Design Mode: brief specifies `canva` or `code`
- Canva mode: list available MCP tools (`generate-design`, `create-design-from-candidate`, `get-design`, `export-design`, `list-brand-kits`, `search-designs`, `upload-asset-from-url`)
- Code mode: HTML/CSS/Tailwind, responsive, polished aesthetic, PDF-ready templates
- Outputs: append to handoff.md with separator header `(designer, YYYY-MM-DD)`
- Canva fallback: if MCP unavailable, note in handoff.md and suggest code mode
- Standards: EN-UK spelling, tabs

- [ ] **Step 2: Verify file exists**

```bash
head -3 agents/shared/designer/CLAUDE.md
```
Expected: `# Designer Agent`

- [ ] **Step 3: Commit**

```bash
git add agents/shared/designer/
git commit -m "feat: add Designer agent — Canva + code dual-mode (shared)"
```

---

### Task 4: Create Marketing team agents

**Files:**
- Create: `agents/marketing/strategist/CLAUDE.md`
- Create: `agents/marketing/copywriter/CLAUDE.md`

- [ ] **Step 1: Create marketing directory**

```bash
mkdir -p agents/marketing/strategist agents/marketing/copywriter
```

- [ ] **Step 2: Write Strategist CLAUDE.md**

**Template:** Use `agents/build/planner/CLAUDE.md` as the structural template. Key differences from Planner:
- Identity: marketing strategist, not software architect
- Outputs: campaign briefs, content calendars, channel strategies, audience personas
- Writes tasks for Copywriter and Designer (not Builder)
- Appends to handoff.md with separator `(strategist, YYYY-MM-DD)`
- Declares budget in plan.md like Planner does
- Logs decisions to decisions.md
- EN-UK spelling, tabs

- [ ] **Step 3: Write Copywriter CLAUDE.md**

**Template:** Use `agents/build/builder/CLAUDE.md` as the structural template. Key differences from Builder:
- Identity: writes compelling copy, not code
- Inputs: task brief + brand guidelines + tone references
- Outputs: copy files (markdown), not code files
- No testing section — replaced with "Quality" section (tone consistency, call-to-action clarity, brand alignment)
- Appends to handoff.md with separator `(copywriter, YYYY-MM-DD)`
- EN-UK spelling, tabs

- [ ] **Step 4: Verify files exist**

```bash
head -3 agents/marketing/strategist/CLAUDE.md
head -3 agents/marketing/copywriter/CLAUDE.md
```

- [ ] **Step 5: Commit**

```bash
git add agents/marketing/
git commit -m "feat: add Marketing team — Strategist + Copywriter agents"
```

---

### Task 5: Create Analysis team agents

**Files:**
- Create: `agents/analysis/analyst/CLAUDE.md`
- Create: `agents/analysis/report-writer/CLAUDE.md`

- [ ] **Step 1: Create analysis directory**

```bash
mkdir -p agents/analysis/analyst agents/analysis/report-writer
```

- [ ] **Step 2: Write Analyst CLAUDE.md**

**Template:** Use `agents/build/builder/CLAUDE.md` as the structural template. Key characteristics:
- Identity: data analyst, finds trends and insights
- Can write Python/SQL for data extraction (unlike Researcher who only reads web)
- Works with: SG database, vault data, web research outputs
- Outputs: structured findings with evidence, data extracts, trend analysis
- Appends to handoff.md with separator `(analyst, YYYY-MM-DD)`
- Testing section: validate data extracts run without errors
- EN-UK spelling, tabs

- [ ] **Step 3: Write Report Writer CLAUDE.md**

**Template:** Use `agents/build/builder/CLAUDE.md` as the structural template. Key characteristics:
- Identity: turns analyst findings into polished, executive-readable reports
- Inputs: analyst handoff + raw findings
- Outputs: markdown reports, HTML reports, PDF-ready templates
- Can delegate visual polish to Designer via brief recommendation
- Structures for executive consumption: headlines, key metrics, recommendations, next steps
- Appends to handoff.md with separator `(report-writer, YYYY-MM-DD)`
- EN-UK spelling, tabs

- [ ] **Step 4: Verify files exist**

```bash
head -3 agents/analysis/analyst/CLAUDE.md
head -3 agents/analysis/report-writer/CLAUDE.md
```

- [ ] **Step 5: Commit**

```bash
git add agents/analysis/
git commit -m "feat: add Analysis team — Analyst + Report Writer agents"
```

---

### Task 6: Update pablo.sh — team-aware context and new commands

**Files:**
- Modify: `pablo.sh`

- [ ] **Step 1: Add TEAMS_YAML variable**

After line 16 (`PROJECTS_YAML=...`), add:

```bash
TEAMS_YAML="$PABLO_DIR/config/teams.yaml"
```

- [ ] **Step 2: Add get_project_team helper**

After the `log_event` function, add a helper that reads team from `.state/plan.md`:

```bash
get_project_team() {
	local dir="$1"
	if [ -f "$dir/.state/plan.md" ]; then
		local team
		team="$(grep -m1 '^## Team:' "$dir/.state/plan.md" 2>/dev/null | sed 's/## Team: *//' | tr -d ' ')"
		if [ -n "$team" ]; then
			echo "$team"
			return
		fi
	fi
	echo "build"
}
```

- [ ] **Step 3: Update cmd_list to show team per project**

In `cmd_list`, replace the internal project echo (currently `echo "  $name ($(project_status "$dir"))"`) with:

```bash
echo "  $name [$(get_project_team "$dir")] ($(project_status "$dir"))"
```

And replace the external project echo (currently `echo "  $name ($status) [external]"`) with:

```bash
echo "  $name [$(get_project_team "$ext_path")] ($status) [external]"
```

- [ ] **Step 4: Add cmd_teams command**

```bash
cmd_teams() {
	echo "Available Teams"
	echo "═══════════════"
	if [ -f "$TEAMS_YAML" ]; then
		local current_team=""
		while IFS= read -r line; do
			# Team name line (e.g., "  build:")
			if echo "$line" | grep -qE "^  [a-z].*:$"; then
				current_team="$(echo "$line" | sed 's/:.*//' | tr -d ' ')"
			fi
			# Description
			if echo "$line" | grep -q "description:"; then
				local desc
				desc="$(echo "$line" | sed 's/.*description: *"//' | sed 's/".*//')"
				echo ""
				echo "  $current_team — $desc"
			fi
			# Team agents
			if echo "$line" | grep -q "team-agents:"; then
				local agents
				agents="$(echo "$line" | sed 's/.*team-agents: *//')"
				echo "    team: $agents"
			fi
			# Shared agents
			if echo "$line" | grep -q "shared-agents:"; then
				local agents
				agents="$(echo "$line" | sed 's/.*shared-agents: *//')"
				echo "    shared: $agents"
			fi
		done < "$TEAMS_YAML"
	else
		echo "  No teams.yaml found at $TEAMS_YAML"
	fi
}
```

- [ ] **Step 5: Update cmd_project system context**

In `cmd_project`, add these lines to the existing `system_context` variable. Insert after `State directory: $project_dir/.state`:

```
Teams config: $TEAMS_YAML
Agents directory: $PABLO_DIR/agents/
```

And replace the final `Refer to agents/` line with:

```
Read config/teams.yaml to understand available teams and agents.
Resolve agent paths: team agents at agents/<team>/<agent>/CLAUDE.md, shared agents at agents/shared/<agent>/CLAUDE.md.
Refer to skills/orchestrator/ for delegation, escalation, state management, and vault sync rules.
```

Also update the plan.md bullet to read: `- .state/plan.md — project goals, scope, and team assignment`

- [ ] **Step 6: Add --teams to case statement**

In the main case statement, add between `--status` and `--*`:

```bash
	--teams|-t)
		cmd_teams
		;;
```

- [ ] **Step 7: Update usage to include --teams**

```bash
echo "  ./pablo.sh --teams                         List available teams"
```

- [ ] **Step 8: Test all commands**

Run: `./pablo.sh --help`
Expected: Shows --teams in usage

Run: `./pablo.sh --teams`
Expected: Lists build, marketing, analysis with agents

Run: `./pablo.sh --list`
Expected: Existing projects show [build]

- [ ] **Step 9: Commit**

```bash
git add pablo.sh
git commit -m "feat: team-aware pablo.sh — context injection, --teams, team in project list"
```

---

### Task 7: Update orchestrator docs and root CLAUDE.md

**Files:**
- Modify: `skills/orchestrator/delegation.md`
- Modify: `skills/orchestrator/state-management.md`
- Modify: `skills/orchestrator/vault-sync.md`
- Modify: `CLAUDE.md`
- Modify: `templates/new-project/.state/plan.md`

- [ ] **Step 1: Update delegation.md invocation pattern**

Change the invocation pattern from:
```
agents/<agent>/CLAUDE.md
```
To:
```
agents/<team|shared>/<agent>/CLAUDE.md
```

Add a "Team Detection" section after the Delegation Flow:

```markdown
## Team Detection

On first session for a new project:
1. Read `config/teams.yaml` for available teams and keywords
2. Count keyword matches from the instruction against each team
3. If top two teams are within 1 match of each other, ask Tim to confirm
4. Record the team in `.state/plan.md` as `## Team: <team-name>`

On subsequent sessions, read team from plan.md. Tim can override at any time.

## Borrowing Agents

Pablo can invoke agents from other teams when the brief requires it. Resolve the borrowed agent's path via `teams.yaml` — use the agent's home team folder, not the project's team folder.
```

- [ ] **Step 2: Update state-management.md plan.md description**

Add `## Team` to the plan.md section. Change line 25-31 to include:

```markdown
### plan.md
The project's north star. Contains:
- **Team:** Which agent team this project uses (build/marketing/analysis)
- **Goal:** What the project achieves
- **Scope:** What's in and out
- **Architecture:** Key design decisions and structure
- **Milestones:** Ordered list of deliverables
- **Budget:** Expected session budget tier (Small/Medium/Large)
```

- [ ] **Step 3: Update vault-sync.md dashboard format**

Add `Team` column to the dashboard table format:

```markdown
| Project | Team | Status | Progress | Last Activity | Blockers |
```

- [ ] **Step 4: Update root CLAUDE.md Agent Team table**

Replace the current flat table with:

```markdown
## Agent Teams

Pablo uses team presets defined in `config/teams.yaml`. Each project has a primary team.

### Shared Agents (available to all teams)

| Agent | Role | CLAUDE.md |
|---|---|---|
| Researcher | Web research, domain analysis, competitive intel | `agents/shared/researcher/CLAUDE.md` |
| Reviewer | Code/content audit, security, quality checks | `agents/shared/reviewer/CLAUDE.md` |
| Designer | Visual output — Canva designs or polished code | `agents/shared/designer/CLAUDE.md` |

### Build Team

| Agent | Role | CLAUDE.md |
|---|---|---|
| Planner | Specs, architecture, task breakdowns | `agents/build/planner/CLAUDE.md` |
| Builder | Code implementation, tests, docs | `agents/build/builder/CLAUDE.md` |

### Marketing Team

| Agent | Role | CLAUDE.md |
|---|---|---|
| Strategist | Campaign strategy, positioning, content calendars | `agents/marketing/strategist/CLAUDE.md` |
| Copywriter | Copy, content, messaging | `agents/marketing/copywriter/CLAUDE.md` |

### Analysis Team

| Agent | Role | CLAUDE.md |
|---|---|---|
| Analyst | Data analysis, trends, insights | `agents/analysis/analyst/CLAUDE.md` |
| Report Writer | Polished executive-ready reports | `agents/analysis/report-writer/CLAUDE.md` |
```

Also update the session budget line to reference the tiered system.

- [ ] **Step 5: Update template plan.md**

Add `## Team` placeholder after the title:

```markdown
# Project Plan

## Team

_Detected automatically by Pablo. Override with "switch to <team> team"._

## Goal
...
```

- [ ] **Step 6: Commit**

```bash
git add skills/orchestrator/ CLAUDE.md templates/
git commit -m "docs: update orchestrator docs, root CLAUDE.md, and template for team presets"
```

---

### Task 8: Update vault dashboard format

**Files:**
- Modify: `C:\Users\timbl\stolen goat Dropbox\tim bland\Obsidian\projects\project-dashboard.md`

- [ ] **Step 1: Add Team column to dashboard**

Update the projects table to include the Team column:

```markdown
| Project | Team | Status | Progress | Last Activity | Blockers |
|---|---|---|---|---|---|
| [[SG Analysis — Brief\|SG Analysis]] | build | Complete | 8/8 tasks | 2026-03-22 | None |
| [[Stolen Goat Prospect Agent — Brief\|Prospect Agent]] | build | Complete | Initial build done | 2026-03-22 | None |
| [[Pablo Research Agent — Brief\|Research Agent]] | build | Complete | 5/5 tasks | 2026-03-21 | None |
```

Note: This file is in the Obsidian vault (outside the git repo). No git commit needed — Dropbox syncs it automatically.

---

### Task 9: End-to-end verification

- [ ] **Step 1: Verify folder structure**

```bash
find agents/ -name "CLAUDE.md" | sort
```
Expected:
```
agents/analysis/analyst/CLAUDE.md
agents/analysis/report-writer/CLAUDE.md
agents/build/builder/CLAUDE.md
agents/build/planner/CLAUDE.md
agents/marketing/copywriter/CLAUDE.md
agents/marketing/strategist/CLAUDE.md
agents/shared/designer/CLAUDE.md
agents/shared/researcher/CLAUDE.md
agents/shared/reviewer/CLAUDE.md
```

- [ ] **Step 2: Verify pablo.sh commands**

```bash
./pablo.sh --teams
./pablo.sh --list
```

- [ ] **Step 3: Verify backward compatibility**

Check that existing project tasks.jsonl files use canonical agent names:

```bash
grep '"agent"' projects/pablo-research-agent/.state/tasks.jsonl | head -3
grep '"agent"' projects/stolen-goat-prospect-agent/.state/tasks.jsonl | head -3
```
Expected: `"agent": "planner"`, `"agent": "builder"`, `"agent": "reviewer"`, `"agent": "researcher"` — all short canonical names that Pablo can resolve via teams.yaml.

- [ ] **Step 4: Verify template**

```bash
grep "## Team" templates/new-project/.state/plan.md
```
Expected: `## Team` line present

- [ ] **Step 5: Verify all agent CLAUDE.md files have consistent structure**

```bash
for f in $(find agents/ -name "CLAUDE.md"); do
  echo "=== $f ==="
  grep -c "## Identity\|## Inputs\|## Outputs\|## File Reading Rules\|What NOT to Do" "$f"
done
```
Expected: Each file has at least 4-5 matching section headers.

- [ ] **Step 6: Generalise Reviewer references**

The Reviewer's CLAUDE.md references "the builder's report" — since Reviewer is now shared across all teams, update to "the implementing agent's report" or similar. Check for any other build-specific language in shared agent docs.

- [ ] **Step 7: Manual verification (interactive)**

These checks require running Pablo in orchestrator mode:
- Start a new marketing project — verify Pablo auto-detects team
- Test keyword collision (instruction matching multiple teams) — verify Pablo asks Tim
- Test borrowing: invoke Copywriter from a build project
- Test Designer in code mode (Canva mode requires MCP to be active)

- [ ] **Step 8: Final commit if any fixes needed**

```bash
git add -A
git commit -m "fix: verification pass cleanup"
```
