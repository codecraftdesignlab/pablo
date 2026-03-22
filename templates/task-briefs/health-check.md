# TASK-NNN: Health Check — <project-name>

## Objective
Verify that <project-name> is still functioning correctly. Run the project, check output, and report status.

## Context
This is a routine health check, not a feature task. The goal is to confirm the project still works as expected and flag any issues.

## Scope
- Files to read: <project entry point, config files>
- Files to create/modify: none (read-only check)
- Out of scope: code changes, new features, refactoring

## Checks
- [ ] Project runs without errors
- [ ] Output matches expected format
- [ ] External dependencies are reachable (APIs, databases, services)
- [ ] No new warnings or deprecation notices
- [ ] Scheduled tasks are still running (if applicable)

## Testing
- Test framework: <as per project>
- Tests required: no (health check only)
- Run existing tests if present and report pass/fail

## Output
Append results to `.state/handoff.md`. Report:
- **Status:** Healthy | Degraded | Broken
- **Details:** What was checked and what was found
- **Action needed:** Any issues requiring attention (or "None")
