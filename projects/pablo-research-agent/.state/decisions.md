# Decisions Log

## DEC-001: Use native WebSearch/WebFetch instead of Brave Search MCP (2026-03-21)

**Decision:** The Research agent will use Claude Code's built-in `WebSearch` and `WebFetch` tools rather than configuring Brave Search as an MCP server.

**Rationale:**
- Claude Code already provides `WebSearch` (broad web search with domain filtering) and `WebFetch` (fetch and analyse specific URLs) as native tools
- These tools are available to all agents without any configuration — no `.mcp.json` setup, no API keys, no external dependencies
- `WebSearch` supports domain allow/block lists, which covers the filtering needs
- `WebFetch` includes AI-powered content extraction and summarisation, which is more capable than raw page scraping
- Adding Brave Search MCP would introduce an external dependency (API key management, rate limits, potential breakage) for no material benefit over what's already available
- If native tools prove insufficient in future, Brave Search MCP can be added as an enhancement without changing the agent's interface

**Alternatives considered:**
1. **Brave Search MCP** — would require `.mcp.json` config, a Brave API key in `.env`, and dependency on an external service. More complex with no clear advantage.
2. **SerpAPI** — already in Pablo's `.env` for other purposes, but would require custom scripts. Native tools are simpler.
3. **Hybrid (native + MCP)** — unnecessary complexity. Start simple, add MCP later if needed.

## DEC-002: Research output goes to .state/research/ not .state/handoff.md (2026-03-21)

**Decision:** Research reports are written to `.state/research/<topic-slug>.md` as persistent files. Only a summary goes to `.state/handoff.md`.

**Rationale:**
- `handoff.md` is ephemeral — overwritten each agent run (per state-management.md)
- Research findings are valuable long-term artefacts that the Planner and other agents need to reference across multiple sessions
- Keeping reports in a dedicated directory makes them easy to list, reference in task briefs, and audit
- The Planner's task brief can include `research/<topic>.md` in its "Files to read" section, which is cleaner than parsing handoff.md

**Alternatives considered:**
1. **Write everything to handoff.md** — would lose research when the next agent runs. Unacceptable for multi-session projects.
2. **Write to project root** — clutters the project directory. `.state/research/` keeps state contained.
3. **Write to Obsidian vault** — research is project-specific, not general knowledge. Vault is for cross-project knowledge.

## DEC-003: Planner-to-Researcher invocation is manual via Pablo (2026-03-21)

**Decision:** When the Planner identifies a research gap, it writes a recommendation in `handoff.md`. Pablo (the orchestrator) decides whether to invoke the Researcher. There is no automatic chaining.

**Rationale:**
- The existing orchestration model is simple: Pablo reads handoff, decides next agent. This is working well.
- Automatic chaining (Planner auto-triggers Researcher) would require changes to `pablo.sh` and add complexity
- Manual routing lets Tim/Pablo decide if research is worth the token cost and time
- Keeps the session budget (5 invocations) under Pablo's control
- Can be automated later if the pattern proves common enough

**Alternatives considered:**
1. **Auto-chain via pablo.sh** — would need conditional logic in the shell script to detect "research needed" signals. Over-engineering for now.
2. **Let Planner invoke Researcher directly** — breaks the principle that agents are independent sub-processes. Agents don't invoke other agents.

## DEC-004: No changes to pablo.sh required (2026-03-21)

**Decision:** The orchestrator shell script needs no modifications. The Researcher uses the identical invocation pattern as all other agents.

**Rationale:**
- `pablo.sh` invokes agents via: `claude -p --append-system-prompt "$(cat agents/<agent>/CLAUDE.md)" "..."`
- This pattern works for any agent — just substitute `researcher` for the agent name
- No new flags, routes, or special handling needed
- Keeping pablo.sh unchanged reduces risk and review scope

**Alternatives considered:**
1. **Add `--research` flag to pablo.sh** — unnecessary. The existing `cmd_project` function handles everything.
