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

# ── Helpers ────────────────────────────────────────────────────────────────────

log_event() {
	local event="$1"
	local project="${2:-}"
	local detail="${3:-}"
	local ts
	ts="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
	mkdir -p "$LOGS_DIR"
	echo "{\"ts\":\"$ts\",\"event\":\"$event\",\"project\":\"$project\",\"detail\":\"$detail\"}" >> "$LOG_FILE"
}

usage() {
	echo "Pablo — AI Project Manager & Executive Assistant"
	echo ""
	echo "Usage:"
	echo "  ./pablo.sh <project-name> \"instruction\"   Work on a project"
	echo "  ./pablo.sh --status                        Cross-project summary"
	echo "  ./pablo.sh --list                          List all projects"
	echo "  ./pablo.sh --help                          Show this help"
	echo ""
	echo "Projects live in: $PROJECTS_DIR"
}

# ── Commands ───────────────────────────────────────────────────────────────────

cmd_list() {
	echo "Managed Projects"
	echo "════════════════"
	if [ ! -d "$PROJECTS_DIR" ] || [ -z "$(ls -A "$PROJECTS_DIR" 2>/dev/null)" ]; then
		echo "  (none)"
		return
	fi
	for dir in "$PROJECTS_DIR"/*/; do
		local name
		name="$(basename "$dir")"
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
		echo "  $name ($status)"
	done
}

cmd_status() {
	echo "Pablo — Cross-Project Status"
	echo "═══════════════════════════════"
	echo ""
	cmd_list
	echo ""
	if [ -f "$LOG_FILE" ]; then
		echo "Recent Activity (last 5)"
		echo "────────────────────────"
		tail -5 "$LOG_FILE" | while IFS= read -r line; do
			local ts project event
			ts="$(echo "$line" | grep -o '"ts":"[^"]*"' | cut -d'"' -f4)"
			project="$(echo "$line" | grep -o '"project":"[^"]*"' | cut -d'"' -f4)"
			event="$(echo "$line" | grep -o '"event":"[^"]*"' | cut -d'"' -f4)"
			echo "  $ts  $event  $project"
		done
	else
		echo "No activity log yet."
	fi
}

cmd_project() {
	local project="$1"
	local instruction="${2:-}"
	local project_dir="$PROJECTS_DIR/$project"

	# Auto-create from template if project doesn't exist
	if [ ! -d "$project_dir" ]; then
		echo "Creating new project: $project"
		mkdir -p "$project_dir"
		cp -r "$TEMPLATES_DIR/.state" "$project_dir/.state"
		log_event "project-created" "$project"
		echo "  Created at $project_dir"
		echo "  Seeded .state/ from template"
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

Read the project state files before acting:
- .state/plan.md — project goals and scope
- .state/tasks.jsonl — task backlog
- .state/decisions.md — decision log
- .state/handoff.md — last agent output
$state_summary

Refer to skills/orchestrator/ for delegation, escalation, and state management rules.
Refer to agents/ for agent identities and instructions."

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
	--*)
		echo "Unknown option: $1"
		usage
		exit 1
		;;
	*)
		cmd_project "$1" "${2:-}"
		;;
esac
