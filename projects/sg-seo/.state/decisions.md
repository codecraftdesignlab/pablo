# SG SEO — Decision Log

## DEC-001: Use DataForSEO as keyword research API (2026-03-24)
**Decision:** DataForSEO over free Google stack or SEMrush
**Rationale:** API-first, pay-per-request pricing (~$3-5/mo), exact search volumes, competitor gap analysis. Free Google Keyword Planner gives bucketed ranges and no competitor data. SEMrush is £100+/mo — overkill for current scope.
**Alternatives considered:** Google Keyword Planner (free but limited), SEMrush (gold standard but expensive), Ubersuggest (GUI-first, no proper API)

## DEC-002: Prioritise brand/lifestyle and CK keywords over product categories (2026-03-24)
**Decision:** Research order: 1. Brand/lifestyle, 2. Custom kit, 3. Product categories
**Rationale:** Brand and CK terms are where SEO can drive the most incremental value. Product category terms (e.g., "cycling jersey") are dominated by large retailers and harder to compete for.
**Alternatives considered:** Starting with product categories (rejected — highest competition), equal weighting (rejected — better to focus)

## DEC-003: Drop Custom MTB Kit from scope (2026-03-24)
**Decision:** Remove custom MTB jersey/kit from the keyword targets and content briefs
**Rationale:** Tim confirmed MTB is too small and doesn't work for SG's business. CONTENT-005 brief deleted.
**Alternatives considered:** Keep as low priority (rejected — not worth the effort)

## DEC-004: WordPress REST API access confirmed for M5 (2026-03-24)
**Decision:** WordPress and WooCommerce REST API credentials exist in `wordpress-credentials.json`. M5 can proceed with programmatic on-site optimisation.
**Rationale:** Spec previously stated WordPress access didn't exist — this was incorrect. Credentials were already configured (WP REST: username + app password, WC REST: consumer key/secret). Site was in maintenance during verification but auth pattern is clear.
**Alternatives considered:** Manual on-site changes (rejected — now unnecessary)

## DEC-005: Defer WordPress write integration to Milestone 5 (2026-03-24)
**Decision:** On-site optimisation recommendations only in Milestone 3; programmatic implementation deferred until WordPress API integration is built
**Rationale:** WordPress write access does not currently exist in Pablo's tooling. Building it is a separate piece of work requiring auth setup, SEO plugin API discovery, and new tool guides.
**Alternatives considered:** Building WordPress integration first (rejected — delays the research value)
