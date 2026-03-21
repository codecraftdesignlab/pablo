# Project Plan — Stolen Goat Agent

## Goal

Build a research agent for Stolen Goat custom kit prospects. The agent connects to flo-bot's enricher pipeline, searches the web for prospect information, and produces structured research reports written to vault contact files.

## Scope

### In Scope
- Web research agent that takes a prospect name/organisation and produces a structured report
- Integration with FLO API to read prospect data
- Web search (SerpAPI) for organisation details, team info, social presence
- Output as structured markdown written to SG Vault contact files
- Callable from flo-bot's enricher pipeline

### Out of Scope
- Direct Slack integration (flo-bot handles that)
- Email drafting (flo-bot handles that)
- CRM functionality
- UI or dashboard

## Architecture

- **Input:** Prospect data from FLO API (name, organisation, email, notes)
- **Processing:** Web search via SerpAPI, data extraction and structuring
- **Output:** Markdown report in SG Vault format with frontmatter
- **Integration:** Called by flo-bot's enricher when a new prospect enters the pipeline

Key decisions:
- Use SerpAPI (key already in pablo's .env) for web searches
- Output to SG Vault in standard frontmatter format
- Keep the agent stateless — input in, report out

## Milestones

### Milestone 1 — Core Research Agent
- [ ] Define input/output schema
- [ ] Build web search module (SerpAPI)
- [ ] Build report generator (structured markdown)
- [ ] Test with sample prospects

### Milestone 2 — FLO Integration
- [ ] Connect to FLO API to read prospect data
- [ ] Build enricher pipeline hook
- [ ] End-to-end test with live prospects
- [ ] Document usage for flo-bot integration
