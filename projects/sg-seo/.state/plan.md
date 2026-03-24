# SG SEO — Project Plan

## Team: marketing
**Borrowed agents:** Builder (build team, Milestone 1 & 4), Analyst (analysis team, Milestone 2)

## Goal

Build automated keyword research tooling and deliver a data-driven SEO strategy for Stolen Goat. Identify high-value keywords across three niches (brand/lifestyle, custom kit, product categories), produce a prioritised content plan, and establish ongoing rank monitoring.

## Budget

**Large** — 5 milestones, 10+ tasks across tooling, research, strategy, and monitoring.

## Scope

### In Scope
- Python tooling wrapping DataForSEO API (`tools/seo/`)
- Competitor keyword gap analysis (lifestyle + CK competitor sets)
- Keyword research with volume, difficulty, and intent clustering
- Prioritised keyword strategy document
- Content briefs for new pages/posts
- Quick wins (on-page optimisation recommendations)
- Weekly rank tracking via GSC
- SEO section in Monday morning briefing

### Out of Scope
- Technical SEO (site speed, schema, crawl errors)
- Link building
- Paid search / Google Ads
- WordPress write integration (deferred to Milestone 5)

## Competitors

### Lifestyle / Brand
| Competitor | Domain |
|---|---|
| Le Col | lecol.cc |
| Cycology | cycology.com |
| Castelli | castelli-cycling.com |
| Rapha | rapha.cc |

### Custom Kit
| Competitor | Domain |
|---|---|
| Santini | santinisms.com |
| Kalas | kalas.cz |
| Le Col | lecol.cc |

## Milestones

### Milestone 1 — Tooling (Builder)
Build `tools/seo/` Python modules and agent guide.
- [ ] `seo_research.py` — DataForSEO wrapper
- [ ] `competitor.py` — competitor domain keywords and gap analysis
- [ ] `tracker.py` — rank tracking with GSC weekly snapshots
- [ ] `CLAUDE.md` — agent guide
- [ ] End-to-end test

### Milestone 2 — Research (Researcher + Analyst)
- [ ] Audit current GSC position
- [ ] Validate GA4 site search availability
- [ ] Competitor gap analysis: lifestyle set
- [ ] Competitor gap analysis: CK set
- [ ] Keyword universe building

### Milestone 3 — Strategy (Strategist)
- [ ] Prioritised keyword map
- [ ] Content gap report
- [ ] Quick wins list
- [ ] Content briefs
- [ ] On-site optimisation recommendations

### Milestone 4 — Monitoring — Complete (2026-03-24)
- [x] Weekly rank tracking script (`scripts/weekly-rank-track.py`)
- [x] Windows scheduled task: "Pablo - SEO Weekly Rank Track" (Mondays 06:30)
- [x] First baseline: 26/33 keywords ranking, 7 not ranking
- [ ] Monday morning briefing SEO section (integrate into `/morning` skill — future)
- [ ] Monthly competitor refresh workflow (future)
- [ ] `/seo-report` skill (future)

### Milestone 5 — On-Site Optimisation (Builder)
WordPress and WooCommerce REST API access confirmed (`wordpress-credentials.json`).
- [ ] Build `tools/wordpress/` integration (WP REST + WC REST wrappers)
- [ ] Detect SEO plugin (Yoast/Rank Math) and target correct meta fields
- [ ] Read current page SEO state for quick-win pages
- [ ] Generate changeset (current vs proposed) for Tim's approval
- [ ] Apply approved changes via API
- [ ] Verify changes applied correctly

**Dropped from scope:** Custom MTB Kit (CONTENT-005) — too small, doesn't work for SG.
