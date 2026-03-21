# Research: Best Practices for Structuring AI Coding Agent Teams

**Date:** 2026-03-21
**Brief:** briefs/TASK-005.md
**Query:** What are the current best practices for structuring AI coding agent teams? Focus on multi-agent orchestration patterns, task delegation, and state management.

## Executive Summary

The field of multi-agent AI coding teams has matured significantly by early 2026, with clear consensus emerging around a small number of proven orchestration patterns. The dominant production pattern is the **orchestrator-worker** model (accounting for roughly 70% of deployments), where a central coordinator decomposes tasks and routes them to specialised agents. File-based state management using Markdown and JSON/JSONL has emerged as a practical, transparent, and git-friendly approach for smaller agent systems, whilst production-scale systems increasingly use dedicated infrastructure (Redis, vector databases) for sub-millisecond coordination. The optimal team size for most workflows is **3-7 agents**, with diminishing returns beyond that unless hierarchical sub-teams are introduced.

## Findings

### Finding 1: Five Core Orchestration Patterns

- **Source:** [AI Agent Orchestration Patterns — Microsoft Azure Architecture Centre](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- **Detail:** Microsoft identifies five fundamental orchestration patterns for multi-agent systems:
  1. **Sequential** (pipeline/prompt chaining) — agents process in a predefined linear order, each building on the previous output. Best for step-by-step refinement with clear dependencies.
  2. **Concurrent** (fan-out/fan-in) — multiple agents work simultaneously on the same input from different perspectives. Best for independent analysis and latency-sensitive scenarios.
  3. **Group Chat** (roundtable/debate) — agents collaborate through a shared conversation thread managed by a chat manager. Best for consensus-building and iterative maker-checker validation. Recommended to limit to 3 or fewer agents.
  4. **Handoff** (routing/triage/delegation) — dynamic delegation where agents assess tasks and transfer to more appropriate specialists. Best when the right specialist emerges during processing.
  5. **Magentic** (adaptive planning) — a manager agent dynamically builds and refines a task ledger, iterating and backtracking as needed. Best for open-ended problems with no predetermined solution path.
- **Relevance:** Pablo's current architecture most closely resembles a hybrid of sequential and handoff patterns — Pablo (orchestrator) routes tasks to specialised agents in a mostly sequential flow, but with manual routing decisions. The magentic pattern's task-ledger concept maps closely to Pablo's `.state/tasks.jsonl` approach.

### Finding 2: The Orchestrator-Worker Pattern Dominates Production

- **Source:** [Multi-Agent Orchestration Patterns — ai-agentsplus.com](https://www.ai-agentsplus.com/blog/multi-agent-orchestration-patterns-2026)
- **Detail:** The orchestrator-worker pattern is the most deployed multi-agent orchestration pattern in production, accounting for approximately 70% of deployments. A central orchestrator receives incoming tasks, classifies intent, decomposes complex requests into subtasks, routes each subtask to a specialised worker agent, and combines results into a final response. This pattern is favoured because it provides clear accountability (the orchestrator owns the outcome), simple debugging (each worker's input/output is traceable), and natural scaling (add workers without changing the orchestration logic).
- **Relevance:** Pablo already implements this pattern. The orchestrator (Pablo) delegates to Planner, Builder, Reviewer, and now Researcher agents. This validates Pablo's architectural choice as aligned with industry best practice.

### Finding 3: Claude Code Agent Teams — Official Patterns

- **Source:** [Orchestrate teams of Claude Code sessions — Anthropic](https://code.claude.com/docs/en/agent-teams)
- **Detail:** Claude Code provides two approaches for multi-agent work:
  - **Subagents** — lightweight workers spawned within a single session that report results back to the main agent. Lower token cost, no inter-agent communication. Best for focused tasks where only the result matters.
  - **Agent Teams** — full separate Claude Code instances coordinated by a team lead through a shared task list and mailbox system. Higher token cost but teammates can communicate directly with each other. Best for complex work requiring discussion and collaboration.

  Key best practices from Anthropic:
  - Start with **3-5 teammates** for most workflows
  - Aim for **5-6 tasks per teammate** to keep everyone productive
  - Size tasks as self-contained units producing clear deliverables
  - Avoid file conflicts by ensuring each teammate owns different files
  - Use **plan approval gates** for complex or risky tasks
  - Teammates are **ephemeral** — no persistent identity or session resumption
  - CLAUDE.md files provide project-specific guidance to all agents automatically
- **Relevance:** Pablo's approach of permanent agent definitions (via CLAUDE.md files) with ephemeral invocations matches Anthropic's recommended pattern. The `.state/` directory approach effectively serves the same purpose as Claude Code's shared task list but with persistence across sessions — an advantage Pablo has over the built-in agent teams feature.

### Finding 4: Anthropic's Workflow Pattern Selection Framework

- **Source:** [Common workflow patterns for AI agents — Anthropic](https://claude.com/blog/common-workflow-patterns-for-ai-agents-and-when-to-use-them)
- **Detail:** Anthropic recommends three core patterns covering most use cases:
  1. **Sequential** — default starting point; only split when one agent cannot handle reliably
  2. **Parallel** — for independent subtasks or multiple perspectives on the same problem
  3. **Evaluator-Optimizer** — iterative cycles pairing a generator and evaluator agent

  The selection framework is: choose the simplest pattern that solves the problem. Upgrade paths exist — sequential can add parallel processing at bottlenecks, any pattern can add evaluation when quality standards tighten. The key advice is to "try a single agent first before splitting into steps."
- **Relevance:** This validates Pablo's incremental approach — starting with a simple sequential delegation model (Planner then Builder then Reviewer) and adding agents (Researcher) only when a clear need is identified, rather than designing a complex multi-agent system upfront.

### Finding 5: Google ADK Multi-Agent Patterns

- **Source:** [Developer's guide to multi-agent patterns in ADK — Google Developers Blog](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)
- **Detail:** Google's Agent Development Kit documents eight patterns, with two key insights for state management:
  - **State is the whiteboard:** `session.state` (or equivalent) serves as a shared workspace. Agents use `output_key` to write results, and downstream agents reference prior outputs via placeholder syntax. This shared-state-via-keys approach is more robust than passing context through conversation history.
  - **Sub-agent descriptions are API documentation:** The description field of sub-agents is effectively API documentation for the LLM orchestrator. Being precise in agent descriptions directly improves routing accuracy.
  - **Start simple, add complexity:** "Do not build a nested loop system on day one. Start with a sequential chain, debug it, and then add complexity."
- **Relevance:** Pablo's CLAUDE.md files for each agent serve the same purpose as ADK's agent descriptions — they are the "API documentation" that tells the orchestrator what each agent can do. The `.state/` directory serves as the shared whiteboard. The recommendation to start simple and iterate validates Pablo's approach.

### Finding 6: File-Based State Management — The Three-File Pattern

- **Source:** [Scaling AI Agents: A Three-File State Management Pattern — Dev|Journal](https://earezki.com/ai-news/2026-03-09-the-state-management-pattern-that-runs-our-5-agent-system-24-7/)
- **Detail:** A production pattern for file-based multi-agent coordination uses three files:
  1. **current-task.json** — tracks immediate agent state, prevents redundant execution
  2. **memory/today.md** — records recent actions and daily context
  3. **MEMORY.md** — stores long-term standing rules and guidelines

  The execution loop is: read current task, read recent memory, read standing rules, do work, update task status, log what was done. Multi-agent coordination uses filesystem-based handoff files as a message bus, with each handoff containing source agent, destination agent, task payload, and timestamp. Key principles: idempotency (check before executing), observability (human-readable formats), resilience (read-before-write survives restarts).
- **Relevance:** Pablo's `.state/` directory implements a very similar pattern: `tasks.jsonl` maps to current-task.json, `handoff.md` maps to the handoff file concept, and `plan.md`/`decisions.md` map to the long-term rules. This validates Pablo's file-based approach as production-viable for small-to-medium agent systems.

### Finding 7: Markdown as Agent Memory — Industry Convergence

- **Source:** [AI Agent Memory Management — When Markdown Files Are All You Need — DEV Community](https://dev.to/imaginex/ai-agent-memory-management-when-markdown-files-are-all-you-need-5ekk)
- **Detail:** Three major AI agent projects (Manus, OpenClaw, Claude Code) independently converged on markdown-based memory management. Benefits include:
  - **Transparency** — memory is human-readable and editable
  - **Version control** — lives in Git with full history, rollbacks, and branching
  - **Portability** — no vendor lock-in; standard format
  - **Cost** — local disk at ~$0.02/GB/month vs $50-200/GB/month for managed vector databases

  Limitations: scalability issues above 5MB of memory files; linear retrieval cannot match semantic search. The recommended approach is progressive: start with MEMORY.md and daily logs, add basic search, upgrade to vector search only when usage patterns demonstrate need.
- **Relevance:** Pablo's Obsidian vault integration and `.state/` directory approach align perfectly with this pattern. The markdown-first approach is validated by industry convergence. The 5MB scalability threshold is unlikely to be an issue for Pablo's current scale.

### Finding 8: The Conductor-to-Orchestrator Evolution

- **Source:** [Conductors to Orchestrators: The Future of Agentic Coding — Addy Osmani / O'Reilly](https://addyosmani.com/blog/future-agentic-coding/)
- **Detail:** The role of the software engineer is evolving through two distinct models:
  - **Conductor** (single-agent, interactive) — real-time, synchronous interaction with one AI agent, fine-grained control but limited parallelisation
  - **Orchestrator** (multi-agent, asynchronous) — managing multiple autonomous agents concurrently, producing persistent artefacts (branches, PRs, commits)

  Best practices for orchestrator-model systems:
  - Specialised agent types: planning, coding, testing, review, documentation
  - Workspace isolation: each agent on separate Git branches or isolated environments
  - Front-loaded human effort: quality specifications and clear task descriptions are critical
  - Flexible mode switching: engineers may conduct for complex tasks whilst orchestrating simpler parallel work
  - Quality control remains human: "trust, but verify" with security scanning and standards checks
- **Relevance:** Tim currently operates as a conductor (interactive with Pablo) moving towards orchestrator (delegating to agent teams). The recommendation for workspace isolation is relevant if Pablo expands to parallel agent execution. The emphasis on front-loaded specifications (good task briefs) validates Pablo's brief-first delegation model.

### Finding 9: Framework Comparison — CrewAI vs LangGraph

- **Source:** [The 2026 AI Agent Framework Decision Guide — DEV Community](https://dev.to/linou518/the-2026-ai-agent-framework-decision-guide-langgraph-vs-crewai-vs-pydantic-ai-b2h)
- **Detail:** The two dominant frameworks take different approaches:
  - **CrewAI** — role-based abstraction ("we need a researcher, an analyst, and a writer" translates to code almost literally). Built-in delegation where agents can proactively hand off to more capable agents. Fast prototyping (idea-to-production in under a week). Best for content generation, research, and analysis workflows.
  - **LangGraph** — graph-based state machine model with typed state channels. Explicit conditional branching, parallel execution with merging, and complex retry strategies. Better for precise state control and long-term maintenance.

  Key insight: CrewAI's role-based model maps directly to how product teams think about workflows, but LangGraph provides more robust state management for complex production systems.
- **Relevance:** Pablo's architecture is philosophically closer to CrewAI's role-based model (permanent agent roles defined in CLAUDE.md, with clear specialisations), but its state management approach (JSONL + markdown files) is more explicit and controllable, akin to LangGraph's typed state approach. This hybrid is a pragmatic choice.

### Finding 10: Production Reliability and Anti-Patterns

- **Source:** [AI Agent Orchestration Patterns — Microsoft Azure Architecture Centre](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- **Detail:** Microsoft documents critical implementation considerations for production agent systems:

  **Reliability:**
  - Implement timeout and retry mechanisms
  - Validate agent output before passing to the next agent
  - Design circuit breaker patterns for agent dependencies
  - Use checkpoints to recover from interrupted orchestrations
  - Ensure compute isolation between agents

  **Common anti-patterns:**
  - Creating unnecessary coordination complexity when simpler patterns would suffice
  - Adding agents that don't provide meaningful specialisation
  - Overlooking latency impacts of multi-hop communication
  - Sharing mutable state between concurrent agents
  - Consuming excessive model resources as context windows grow

  **Cost optimisation:**
  - Assign each agent a model matching the complexity of its task (not every agent needs the most capable model)
  - Monitor token consumption per agent and per orchestration run
  - Apply context compaction between agents to reduce token volume

  **Human-in-the-loop:**
  - Identify mandatory vs optional human gates
  - Persist state at human checkpoints to allow resumption without replaying prior agent work
  - Scope HITL gates to specific tool invocations rather than full agent outputs
- **Relevance:** Pablo already implements several of these practices: human-in-the-loop (Tim approves agent invocations), session budgets (max 5 invocations), and state persistence (`.state/` files allow resumption). Areas for potential improvement include output validation between agents and model selection per agent (using cheaper models for simpler tasks).

## Comparison Table

| Pattern | Coordination | Best For | State Approach | Pablo Alignment |
|---|---|---|---|---|
| Sequential (Pipeline) | Linear; each agent builds on previous output | Step-by-step refinement, clear dependencies | Passed context or shared state | High — Planner then Builder then Reviewer |
| Concurrent (Fan-out) | Parallel; agents work independently | Independent analysis, latency reduction | Separate output keys, aggregation | Low — Pablo runs agents sequentially |
| Orchestrator-Worker | Central coordinator delegates to specialists | Most production workloads (~70%) | Orchestrator manages shared state | Very High — Pablo's core model |
| Handoff (Routing) | Dynamic delegation, one active agent | Unknown specialist requirements | Full context transfer between agents | Medium — manual routing via Pablo |
| Magentic (Adaptive) | Manager builds/refines task ledger dynamically | Open-ended problems | Dynamic task ledger with progress tracking | Medium — tasks.jsonl is a static version |
| Group Chat (Debate) | Shared conversation thread | Consensus-building, brainstorming | Accumulating chat thread | Low — agents don't converse |

## Recommendations

1. **Pablo's architecture is well-aligned with best practice.** The orchestrator-worker pattern with permanent agent roles, file-based state management, and human-in-the-loop approval matches the dominant production pattern. No fundamental architectural changes are needed.

2. **Consider adding output validation between agents.** Microsoft's guidance emphasises validating agent output before passing to the next agent. Pablo could add a lightweight validation step (e.g., checking that Builder output compiles, or that Researcher output matches the report format) before marking tasks as done.

3. **Explore model tiering per agent.** Not every agent needs the most capable model. The Researcher agent (which primarily searches and synthesises) could potentially use a faster, cheaper model, reserving the most capable model for the Planner and Builder where reasoning quality is most critical.

4. **Keep the file-based state approach for now.** The convergence of Manus, OpenClaw, and Claude Code on markdown-based memory validates Pablo's `.state/` directory pattern. The 5MB scalability threshold is unlikely to be reached at current scale. If Pablo grows to manage many concurrent projects, consider a lightweight database (SQLite with JSONL export, as Beads does).

5. **Add explicit agent descriptions to the orchestrator.** Google's ADK finding that "agent descriptions are API documentation for the LLM" suggests Pablo could benefit from a structured registry (beyond the CLAUDE.md agent table) that the orchestrator consults when routing tasks — a concise summary of each agent's capabilities, inputs, and outputs.

6. **Consider parallel agent execution as a future enhancement.** Pablo currently runs agents sequentially, but the research shows significant time savings from concurrent execution (e.g., running Builder and Researcher in parallel when tasks are independent). This would require workspace isolation (Git worktrees) to prevent file conflicts.

7. **Maintain the 3-7 agent sweet spot.** With four agents (Planner, Builder, Reviewer, Researcher), Pablo sits comfortably within the recommended range. Adding a fifth or sixth agent (e.g., a Deployer or a Documenter) would still be within best practice, but beyond seven, hierarchical sub-teams should be considered.

## Sources

- [AI Agent Orchestration Patterns — Microsoft Azure Architecture Centre](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) — Comprehensive reference for five orchestration patterns with implementation considerations, anti-patterns, and cost guidance. Updated February 2026.
- [Orchestrate teams of Claude Code sessions — Anthropic](https://code.claude.com/docs/en/agent-teams) — Official documentation for Claude Code's experimental agent teams feature, covering architecture, best practices, and team sizing.
- [Common workflow patterns for AI agents — Anthropic](https://claude.com/blog/common-workflow-patterns-for-ai-agents-and-when-to-use-them) — Anthropic's guide to sequential, parallel, and evaluator-optimizer patterns with selection framework.
- [Developer's guide to multi-agent patterns in ADK — Google Developers Blog](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) — Eight multi-agent patterns in Google's Agent Development Kit with state management guidance.
- [Conductors to Orchestrators: The Future of Agentic Coding — Addy Osmani / O'Reilly](https://addyosmani.com/blog/future-agentic-coding/) — Analysis of the conductor vs orchestrator model for AI coding teams, with practical implementation patterns.
- [Scaling AI Agents: A Three-File State Management Pattern — Dev|Journal](https://earezki.com/ai-news/2026-03-09-the-state-management-pattern-that-runs-our-5-agent-system-24-7/) — Production pattern for file-based multi-agent coordination using JSON and Markdown.
- [AI Agent Memory Management: When Markdown Files Are All You Need — DEV Community](https://dev.to/imaginex/ai-agent-memory-management-when-markdown-files-are-all-you-need-5ekk) — Analysis of markdown-based memory across Manus, OpenClaw, and Claude Code.
- [Multi-Agent Orchestration Patterns — ai-agentsplus.com](https://www.ai-agentsplus.com/blog/multi-agent-orchestration-patterns-2026) — Survey of orchestration patterns with production deployment statistics.
- [The 2026 AI Agent Framework Decision Guide — DEV Community](https://dev.to/linou518/the-2026-ai-agent-framework-decision-guide-langgraph-vs-crewai-vs-pydantic-ai-b2h) — Comparison of CrewAI, LangGraph, and Pydantic AI frameworks.
- [AI agent orchestration for production systems — Redis](https://redis.io/blog/ai-agent-orchestration/) — Infrastructure-level state management for production multi-agent systems.

## Open Questions

- **Token cost tracking:** How much does each agent invocation cost in practice? Monitoring this would inform model tiering decisions (Recommendation 3).
- **Parallel execution feasibility:** Would Git worktree isolation work reliably on Windows for Pablo's use case, given that Claude Code's split-pane mode requires tmux (not natively available on Windows)?
- **Agent self-routing:** Several frameworks (CrewAI, Claude Code Agent Teams) support agents proactively delegating to other agents. Would this be beneficial for Pablo, or does the current human-in-the-loop routing provide better control?
- **Context compaction:** As projects grow, how should Pablo handle growing `.state/` files to prevent context window overload when agents read them?
