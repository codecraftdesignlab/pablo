#!/usr/bin/env bash
# Pablo — Unified EA + Orchestrator Entry Point
# Usage:
#   ./pablo.sh <project-name> "instruction"   — work on a project
#   ./pablo.sh --status                        — cross-project summary
#   ./pablo.sh --list                          — list all projects
#   ./pablo.sh --help                          — show this help

set -euo pipefail

PABLO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECTS_DIR="$PABLO_DIR/projects"
TEMPLATES_DIR="$PABLO_DIR/templates/new-project"
LOGS_DIR="$PABLO_DIR/logs"
LOG_FILE="$LOGS_DIR/orchestration.jsonl"
PROJECTS_YAML="$PABLO_DIR/config/projects.yaml"
TEAMS_YAML="$PABLO_DIR/config/teams.yaml"

# ── Helpers ────────────────────────────────────────────────────────────────────

log_event() {
	# Events logged by pablo.sh: session-start, session-end, project-created, state-seeded
	# Events logged by Pablo (orchestrator) during sessions:
	#   agent-invoked (detail: "<agent> TASK-NNN")
	#   agent-completed (detail: "<agent> TASK-NNN [verdict]")
	#   escalation (detail: "<level>: <summary>")
	#   budget-upgrade (detail: "<old-tier> -> <new-tier>")
	local event="$1"
	local project="${2:-}"
	local detail="${3:-}"
	local ts
	ts="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
	mkdir -p "$LOGS_DIR"
	echo "{\"ts\":\"$ts\",\"event\":\"$event\",\"project\":\"$project\",\"detail\":\"$detail\"}" >> "$LOG_FILE"
}

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

usage() {
	echo "Pablo — AI Project Manager & Executive Assistant"
	echo ""
	echo "Usage:"
	echo "  ./pablo.sh <project-name> \"instruction\"   Work on a project"
	echo "  ./pablo.sh --status                        Cross-project summary"
	echo "  ./pablo.sh --list                          List all projects"
	echo "  ./pablo.sh --teams                         List available teams"
	echo "  ./pablo.sh --help                          Show this help"
	echo ""
	echo "Projects live in: $PROJECTS_DIR"
}

resolve_project_dir() {
	local project="$1"
	# Check internal projects first
	if [ -d "$PROJECTS_DIR/$project" ]; then
		echo "$PROJECTS_DIR/$project"
		return
	fi
	# Check external projects registry
	if [ -f "$PROJECTS_YAML" ]; then
		local ext_path
		ext_path="$(grep -A1 "^  $project:" "$PROJECTS_YAML" | grep "path:" | sed 's/.*path: *"//' | sed 's/".*//' | tr '\\' '/')"
		if [ -n "$ext_path" ] && [ -d "$ext_path" ]; then
			echo "$ext_path"
			return
		fi
	fi
	# Not found — return internal path (will be created)
	echo "$PROJECTS_DIR/$project"
}

# ── Commands ───────────────────────────────────────────────────────────────────

project_status() {
	local dir="$1"
	local status="no state"
	if [ -f "$dir/.state/plan.md" ]; then
		status="has plan"
	fi
	if [ -f "$dir/.state/tasks.jsonl" ] && [ -s "$dir/.state/tasks.jsonl" ]; then
		local total done
		total="$(wc -l < "$dir/.state/tasks.jsonl" | tr -d ' ')"
		done="$(grep -c '"done"' "$dir/.state/tasks.jsonl" 2>/dev/null || echo 0)"
		status="$done/$total tasks done"
	fi
	echo "$status"
}

cmd_list() {
	echo "Managed Projects"
	echo "════════════════"
	local found=0

	# Internal projects
	if [ -d "$PROJECTS_DIR" ] && [ -n "$(ls -A "$PROJECTS_DIR" 2>/dev/null)" ]; then
		for dir in "$PROJECTS_DIR"/*/; do
			local name
			name="$(basename "$dir")"
			echo "  $name [$(get_project_team "$dir")] ($(project_status "$dir"))"
			found=1
		done
	fi

	# External projects
	if [ -f "$PROJECTS_YAML" ]; then
		local ext_names
		ext_names="$(grep -E "^  [a-z]" "$PROJECTS_YAML" | sed 's/:.*//' | tr -d ' ')"
		if [ -n "$ext_names" ]; then
			for name in $ext_names; do
				local ext_path
				ext_path="$(resolve_project_dir "$name")"
				if [ -d "$ext_path" ]; then
					local status
					status="$(project_status "$ext_path")"
					echo "  $name [$(get_project_team "$ext_path")] ($status) [external]"
					found=1
				fi
			done
		fi
	fi

	if [ "$found" -eq 0 ]; then
		echo "  (none)"
	fi
}

cmd_status() {
	echo "Pablo — Cross-Project Status"
	echo "═══════════════════════════════"
	echo ""
	cmd_list
	echo ""

	# Show blocked tasks across all projects
	echo "Blocked Tasks"
	echo "─────────────"
	local found_blocked=0
	for dir in "$PROJECTS_DIR"/*/; do
		if [ -f "$dir/.state/tasks.jsonl" ] && [ -s "$dir/.state/tasks.jsonl" ]; then
			local name
			name="$(basename "$dir")"
			local blocked
			blocked="$(grep '"blocked"' "$dir/.state/tasks.jsonl" 2>/dev/null || true)"
			if [ -n "$blocked" ]; then
				echo "  $name:"
				echo "$blocked" | while IFS= read -r line; do
					local title
					title="$(echo "$line" | grep -o '"title":"[^"]*"' | cut -d'"' -f4)"
					local id
					id="$(echo "$line" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)"
					echo "    $id: $title"
				done
				found_blocked=1
			fi
		fi
	done
	# Check external projects too
	if [ -f "$PROJECTS_YAML" ]; then
		local ext_names
		ext_names="$(grep -E "^  [a-z]" "$PROJECTS_YAML" | sed 's/:.*//' | tr -d ' ')"
		if [ -n "$ext_names" ]; then
			for name in $ext_names; do
				local ext_path
				ext_path="$(resolve_project_dir "$name")"
				if [ -f "$ext_path/.state/tasks.jsonl" ] && [ -s "$ext_path/.state/tasks.jsonl" ]; then
					local blocked
					blocked="$(grep '"blocked"' "$ext_path/.state/tasks.jsonl" 2>/dev/null || true)"
					if [ -n "$blocked" ]; then
						echo "  $name [external]:"
						echo "$blocked" | while IFS= read -r line; do
							local title
							title="$(echo "$line" | grep -o '"title":"[^"]*"' | cut -d'"' -f4)"
							local id
							id="$(echo "$line" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)"
							echo "    $id: $title"
						done
						found_blocked=1
					fi
				fi
			done
		fi
	fi
	if [ "$found_blocked" -eq 0 ]; then
		echo "  (none)"
	fi
	echo ""

	# Recent activity
	if [ -f "$LOG_FILE" ]; then
		echo "Recent Activity (last 10)"
		echo "─────────────────────────"
		tail -10 "$LOG_FILE" | while IFS= read -r line; do
			local ts project event detail
			ts="$(echo "$line" | grep -o '"ts":"[^"]*"' | cut -d'"' -f4)"
			project="$(echo "$line" | grep -o '"project":"[^"]*"' | cut -d'"' -f4)"
			event="$(echo "$line" | grep -o '"event":"[^"]*"' | cut -d'"' -f4)"
			detail="$(echo "$line" | grep -o '"detail":"[^"]*"' | cut -d'"' -f4)"
			if [ -n "$detail" ]; then
				echo "  $ts  $event  $project  ($detail)"
			else
				echo "  $ts  $event  $project"
			fi
		done
	else
		echo "No activity log yet."
	fi
}

cmd_teams() {
	echo "Available Teams"
	echo "═══════════════"
	if [ -f "$TEAMS_YAML" ]; then
		local current_team=""
		while IFS= read -r line; do
			if echo "$line" | grep -qE "^  [a-z].*:$"; then
				current_team="$(echo "$line" | sed 's/:.*//' | tr -d ' ')"
			fi
			if echo "$line" | grep -q "description:"; then
				local desc
				desc="$(echo "$line" | sed 's/.*description: *"//' | sed 's/".*//')"
				echo ""
				echo "  $current_team — $desc"
			fi
			if echo "$line" | grep -q "team-agents:"; then
				local agents
				agents="$(echo "$line" | sed 's/.*team-agents: *//')"
				echo "    team: $agents"
			fi
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

cmd_project() {
	local project="$1"
	local instruction="${2:-}"
	local project_dir
	project_dir="$(resolve_project_dir "$project")"

	# Auto-create project or seed .state/ if missing
	if [ ! -d "$project_dir" ]; then
		echo "Creating new project: $project"
		mkdir -p "$project_dir"
		cp -r "$TEMPLATES_DIR/.state" "$project_dir/.state"
		log_event "project-created" "$project"
		echo "  Created at $project_dir"
		echo "  Seeded .state/ from template"
		echo ""
	elif [ ! -d "$project_dir/.state" ]; then
		echo "Seeding .state/ for existing project: $project"
		cp -r "$TEMPLATES_DIR/.state" "$project_dir/.state"
		log_event "state-seeded" "$project"
		echo "  Seeded .state/ from template at $project_dir"
		echo ""
	fi

	log_event "session-start" "$project" "$instruction"

	# Build context for Pablo
	local state_summary=""
	if [ -f "$project_dir/.state/handoff.md" ]; then
		state_summary="Last handoff exists. Read .state/handoff.md for context."
	fi

	local system_context="You are Pablo in ORCHESTRATOR MODE for project '$project'.
Project directory: $project_dir
State directory: $project_dir/.state
Teams config: $TEAMS_YAML
Agents directory: $PABLO_DIR/agents/

Read the project state files before acting:
- .state/plan.md — project goals, scope, and team assignment
- .state/tasks.jsonl — task backlog
- .state/decisions.md — decision log
- .state/handoff.md — last agent output
$state_summary

Read config/teams.yaml to understand available teams and agents.
Resolve agent paths: team agents at agents/<team>/<agent>/CLAUDE.md, shared agents at agents/shared/<agent>/CLAUDE.md.
Refer to skills/orchestrator/ for delegation, escalation, state management, and vault sync rules."

	if [ -n "$instruction" ]; then
		# Non-interactive: run with -p
		cd "$project_dir"
		claude -p --append-system-prompt "$system_context" "$instruction"
		log_event "session-end" "$project"
	else
		# Interactive: launch claude in the project dir
		echo "Launching interactive session for: $project"
		echo "Project dir: $project_dir"
		echo ""
		cd "$project_dir"
		claude --append-system-prompt "$system_context"
		log_event "session-end" "$project"
	fi
}

# ── Main ───────────────────────────────────────────────────────────────────────

if [ $# -eq 0 ]; then
	usage
	exit 0
fi

case "$1" in
	--help|-h)
		usage
		;;
	--list|-l)
		cmd_list
		;;
	--status|-s)
		cmd_status
		;;
	--teams|-t)
		cmd_teams
		;;
	--*)
		echo "Unknown option: $1"
		usage
		exit 1
		;;
	*)
		cmd_project "$1" "${2:-}"
		;;
esac
