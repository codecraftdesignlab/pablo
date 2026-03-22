# Decision Log

## DEC-001: Separate tool from data-diver (2026-03-22)
**Decision:** Build SG Analysis as a standalone tool, not an extension of data-diver
**Rationale:** Data-diver uses AI-generated SQL which is unreliable for compound queries and lacks baked-in business context. A separate tool with pre-built queries will be more accurate and maintainable. Data-diver continues to serve ad-hoc questions and flo-bot.
**Alternatives considered:** Extending data-diver with report templates; building a dashboard app

## DEC-002: Exclude Bioracer from reorder analysis (2026-03-22)
**Decision:** Bioracer is a dead supplier — exclude from all reorder recommendations
**Rationale:** Tim confirmed Bioracer is no longer used for new orders. Existing stock sells through but no reorders.
**Alternatives considered:** None — business decision

## DEC-003: Python tech stack (2026-03-22)
**Decision:** Build in Python (not .NET like data-diver)
**Rationale:** Tim wants fast and effective — Python has the strongest ecosystem for data analysis (pandas), report generation (weasyprint/reportlab), and integrates easily with existing Pablo infrastructure (Gmail API, Obsidian vault).
**Alternatives considered:** .NET (same as data-diver) — rejected for speed of development and library ecosystem

## DEC-004: Output to SG Vault + email (2026-03-22)
**Decision:** Daily report saved as .md to SG Vault reports folder, plus PDF/HTML emailed to Tim
**Rationale:** Markdown in the vault makes it searchable and linkable from Obsidian. Emailed PDF/HTML is shareable with the team and looks professional.
**Alternatives considered:** Vault only; email only; Dropbox PDF only

## DEC-005: Run as part of /morning routine (2026-03-22)
**Decision:** SG Analysis runs as part of Pablo's daily /morning briefing skill
**Rationale:** Tim already runs /morning daily — adding report generation here means no extra step and the data is always fresh for the briefing.
**Alternatives considered:** Separate Windows Task Scheduler job; on-demand only

## DEC-006: Data-diver integration for supplier order sheets (2026-03-22)
**Decision:** Reorder alert sections will include ready-to-run data-diver commands so the team can generate actual supplier order sheets
**Rationale:** The team will see "Diem needs reordering" and immediately want the order sheet. Rather than rebuilding that capability, leverage data-diver's existing supplier_order template. Bridge the gap between insight and action.
**Alternatives considered:** Building full order sheet generation into sg-analysis; manual lookup
