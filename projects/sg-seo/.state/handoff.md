# Handoff — SG SEO

## Project Setup (orchestrator, 2026-03-24)

Project initialised. Spec at `Obsidian/projects/sg-seo/seo-keyword-strategy-design.md`.

- Primary team: marketing (strategist, copywriter)
- Borrowed: builder (build team), analyst (analysis team), researcher (shared)
- DataForSEO credentials stored in `.env`
- 5 milestones planned, 6 tasks created
- Starting with Milestone 1 (tooling) — building directly, then delegating M2/M3 to team

---
## TASK-002: Audit Current GSC Position (analyst, 2026-03-24)

Completed full organic search audit using GSC and GA4 data (90-day window: 2025-12-22 to 2026-03-21). All GA4 queries excluded Chinese bot traffic.

### Key Findings

- **Brand-dependent traffic:** 62% of top-200 query clicks are branded (25 queries). Non-branded queries have 167K impressions but only 1.0% CTR.
- **12,783 organic sessions** over 90 days, 153 purchases, GBP 11,181 revenue (1.20% conversion rate).
- **1,031 striking distance keywords** (position 5-20, min 10 impressions) — major untapped opportunity.
- **Category pages rank poorly:** mens jerseys category has 59,120 impressions but sits at position 15.0 (page 2). Similar pattern for socks (pos 10.7), gilets (pos 13.6), arm warmers (pos 10.3).
- **Blog content drives traffic but not conversions:** cycling events 2026 post (1,330 clicks, 0 purchases); running tips post has 75,473 impressions at position 8.4.
- **Top organic product by revenue:** Climb & Conquer gloves — 178 sessions, 13 purchases, GBP 555 (7.3% CVR).
- **Site search active:** Gloves (199 sessions), Socks (120), Swim (49), Gilet (36), Arm warmers (30) are top searched terms.

### Output

- Full audit: `.state/research/gsc-audit.md`
- Raw data: `.state/research/_top_queries.json`, `_striking_distance.json`, `_top_pages.json`, `_site_search.json`, `_organic_overview.json`, `_organic_landing_pages.json`

---
## TASK-003: Competitor Gap Analysis — Lifestyle Set (researcher, 2026-03-24)

Analysed keyword profiles for all four lifestyle competitors (Le Col, Rapha, Castelli, Cycology) and ran keyword gap analysis against stolengoat.com. DataForSEO spend: $0.00 (cached data within TTL).

### Key Findings

- **Cycology has zero UK organic visibility** on cycology.com — their UK presence is via cycologygear.co.uk.
- **Rapha has the broadest keyword footprint** (2,928 keywords) — nearly 3x SG's 1,051.
- **69 actionable gap keywords** identified after filtering brand/navigational queries.
- **Biggest gap: Women's cycling shorts** — SG has zero visibility across a 250,000+ monthly search cluster where Le Col ranks #2 and Rapha ranks #16-20. A single well-optimised collection page could capture 20+ keyword variants.
- **SG invisible for "cycling clothing" head terms** — Le Col, Castelli, and Rapha all rank top 20; SG absent (combined ~60,000 monthly searches).
- **Men's shorts underperformance** — SG ranks #90-96 despite having product; competitors hold top-10 positions.
- **Quick wins identified:** "leg warmers" (14,800 vol — SG ranks for variant), "cycle socks" (3,600 vol — SG ranks #6 for "cycling socks"), "cycling bib shorts" (2,900 vol — SG at #18).
- **Competitors rank via collection/category pages**, not blog content — SG should prioritise category page SEO.

### Top 5 Priorities

1. Create/optimise women's cycling shorts collection page (250,000+ monthly search opportunity)
2. Optimise for broad "cycling clothing/apparel" terms (60,000 monthly searches)
3. Fix men's shorts rankings — existing pages rank #90-96 (27,000 monthly searches)
4. Improve cycling gloves category page — SG at #82, Castelli at #9 (16,200 monthly searches)
5. Capture keyword variants for existing strong pages (leg warmers, cycle socks, bib shorts)

### Output

- Full analysis: `.state/research/competitor-lifestyle.md`
- Cached API data: `data/competitor/`, `data/gap/`, `data/serp/`

---
## TASK-004: Competitor Gap Analysis — CK Set (researcher, 2026-03-24)

Analysed keyword profiles for the three CK competitors (Santini, Kalas, Le Col) and ran full SERP analysis across 12 CK search terms. DataForSEO spend: ~$0.24.

### Key Findings

- **SG has ZERO organic visibility for CK keywords.** Not in top 20 for any of the 8 primary CK terms tested. This is a complete blind spot despite +152% YoY CK revenue growth.
- **Santini (santinisms.com) has no UK organic presence** — zero keywords. Not an organic search competitor.
- **Kalas operates via kalas.co.uk** (not kalas.cz) — 1,363 UK keywords, ranks top-10 for 10+ CK terms including "custom bike jersey" (#2) and "custom cycling shirts" (#5). The strongest CK organic competitor.
- **Le Col's keyword profile is lifestyle/retail**, not CK-specific. Not a meaningful CK search competitor.
- **owayo.co.uk dominates CK SERPs** — appears in top 10 across all 8 primary CK keywords, ranking #1 five times. They are the domain to beat.
- **CK keyword universe totals ~3,690 monthly searches** with high CPC (£2–5+) confirming strong commercial intent.
- **Strong seasonality:** volumes peak March–June. Content must be live by February.
- **Dedicated landing pages win** — not blog posts. Ranking pages have "custom" in URL, process info, galleries, and strong CTAs.

### Top 5 Content Priorities

1. **Custom Cycling Kit hub page** — target "custom cycling jersey" + 9 synonyms (~2,800/mo combined)
2. **Custom Running Kit page** — "custom running vest" (320/mo)
3. **Custom Triathlon Kit page** — "custom triathlon suit" (210/mo), Kalas already #1
4. **Custom MTB Kit page** — "custom mtb jersey" (170/mo)
5. **Club/Team Kit page** — "team cycling jersey" + "custom team kit" (~210/mo)

### Output

- Full analysis: `.state/research/competitor-ck.md`
- Cached API data: `data/competitor/`, `data/gap/`, `data/serp/`, `data/keywords/`, `data/suggestions/`

---
## TASK-005: Keyword Universe Building (analyst, 2026-03-24)

Synthesised all three research outputs (GSC audit, lifestyle competitor gap, CK competitor gap) into a unified keyword universe with 156 deduplicated keywords across 11 intent-clustered groups.

### Key Outputs

- **11 keyword clusters** mapped by priority, status, and addressable volume
- **2 CRITICAL gaps:** Women's shorts (~250K/mo, zero visibility) and Custom Kit (~3,700/mo, zero visibility)
- **6 HIGH priority clusters:** Cycling clothing, men's jerseys, gilets, socks, gloves, men's shorts
- **16 quick wins** identified — existing pages ranking position 5-20 that can improve with on-page optimisation (combined ~34,000 monthly searches)
- **7 new pages required** — women's shorts collection, 5 CK landing pages, cycling clothing hub
- **Priority matrix** ready for Strategist to build actionable plan

### Output

- Full keyword universe: `.state/research/keyword-universe.md`

---
## TASK-006: Keyword Strategy and Content Briefs (strategist, 2026-03-24)

Produced the full SEO keyword strategy report and 12 content briefs covering all CRITICAL and HIGH priority clusters.

### Strategy Report

Saved to: `C:/Users/timbl/stolen goat Dropbox/tim bland/SG Vault/reports/seo-keyword-strategy-2026-03-24.md`

**Structure:**
1. Executive Summary — 5 key findings
2. Current Position — organic baseline (12,783 sessions, 153 purchases, GBP 11,181, 1.20% CVR)
3. Priority Actions — quick wins (16 keywords, ~34K/mo), new pages (7 pages), strategic plays (5 actions)
4. Keyword Target Map — all 11 clusters with target pages and recommended meta titles/H1s
5. Competitor Intelligence — Le Col, Rapha, Castelli, owayo, Kalas positioning analysis
6. Content Calendar — 4-phase approach over 12 weeks
7. On-Site Recommendations — specific current vs proposed meta titles and H1s for 10 existing pages
8. Measurement — target positions, traffic projections, KPIs

### Content Briefs (12 total)

| Brief | Page | Type | Priority |
|---|---|---|---|
| CONTENT-001 | Women's Cycling Shorts collection | NEW page | CRITICAL |
| CONTENT-002 | Custom Cycling Kit hub | NEW page | CRITICAL |
| CONTENT-003 | Custom Running Kit | NEW page | HIGH |
| CONTENT-004 | Custom Triathlon Kit | NEW page | HIGH |
| CONTENT-005 | Custom MTB Kit | NEW page | HIGH |
| CONTENT-006 | Club & Team Kit | NEW page | HIGH |
| CONTENT-007 | Men's Cycling Shorts overhaul | Existing page | HIGH |
| CONTENT-008 | Cycling Gloves overhaul | Existing page | HIGH |
| CONTENT-009 | Cycling Clothing homepage/hub | Existing page | HIGH |
| CONTENT-010 | Men's Cycling Jerseys optimisation | Existing page | HIGH |
| CONTENT-011 | Cycling Socks optimisation | Existing page | HIGH |
| CONTENT-012 | Men's Cycling Gilets optimisation | Existing page | HIGH |

### Key Decisions

- **Quick wins first:** Phase 1 (weeks 1-4) focuses entirely on on-page optimisation of existing pages — fastest path to results
- **CK pages before peak season:** Phase 2 (weeks 4-8) builds CK landing pages to capture March-June peak demand
- **Major gaps in Phase 3:** Women's shorts and men's shorts require more effort (new page creation or major overhauls)
- **Category pages over blogs:** Strategy follows the competitor-proven approach of ranking via collection/category pages, not editorial content
- **12-week programme:** Phased to deliver value incrementally — quick wins, then CK, then major new pages

### Traffic Projections

| Timeframe | Target | Change |
|---|---|---|
| Current | ~4,300 organic sessions/mo | Baseline |
| 60 days | ~5,200/mo | +20% |
| 90 days | ~5,800/mo | +35% |
| 6 months | ~7,500/mo | +75% |

---
## TASK-007/008: Milestone 4 — Monitoring Setup (builder, 2026-03-24)

### Weekly Rank Tracking

- **Script:** `projects/sg-seo/scripts/weekly-rank-track.py`
- **Scheduled task:** "Pablo - SEO Weekly Rank Track" — runs every Monday at 06:30
- **Tracks:** 33 keywords across 10 clusters (all CRITICAL and HIGH priority)
- **Output:** JSON snapshot to `data/rankings/YYYY-MM-DD.json` + markdown report to `reports/seo-weekly-YYYY-MM-DD.md`

### First Baseline (2026-03-24)

- **26/33 keywords ranking** (7 not ranking)
- **Best positions:** uk cycling clothing brands (4.6), cycling gilet womens (5.7), cycling jerseys uk (5.9)
- **Custom kit:** custom cycling clothing (38.3), custom cycling jersey (49.4) — barely visible
- **Not ranking:** cycling shorts women, cycling shorts men, women's cycling shorts, custom cycling kit, custom triathlon suit, custom running vest, leg warmers

### Decisions

- **MTB dropped:** Custom MTB kit removed from scope per Tim's direction — too small, doesn't work for SG. CONTENT-005 brief deleted.
- **WordPress access confirmed:** `wordpress-credentials.json` has WP REST API (username + app password) and WC REST API (consumer key/secret). Site was in maintenance during testing but credentials are present.

---
## TASK-009: WordPress Integration and SEO Changeset (builder, 2026-03-24)

Built the WordPress/WooCommerce integration tooling and produced the full SEO changeset for quick-win category page optimisation.

### WordPress Tools Built

- **`tools/wordpress/__init__.py`** — package init
- **`tools/wordpress/woocommerce.py`** — WC REST API wrapper: `get_category()`, `get_categories()`, `find_category()`, `update_category()`, `get_product()`
- **`tools/wordpress/wordpress.py`** — WP REST API wrapper: `get_page()`, `get_pages()`, `find_page()`, `update_page()`
- **`tools/wordpress/CLAUDE.md`** — agent guide with auth patterns, URL format quirks, SEO context, and rules

**Key API detail:** WP REST API requires `?rest_route=` format (LiteSpeed blocks `/wp-json/` for WP endpoints). WC REST API uses standard pretty permalinks with query string auth.

### Live Category Audit

Fetched current state of all 9 target categories via WC API. Key findings:

- **6 categories need name changes:** Jerseys & Tops, Socks, Gloves & Mitts, Men's Cycling Bib Shorts, Cycling Gilets (women's), Men's Long Sleeved Cycling Jerseys
- **3 categories already well-named:** Men's Cycling Gilets, Women's Cycling Bib Shorts, Cycling Arm Warmers
- **All 9 need description enhancements** — existing copy is brand-focused but lacks keyword targeting
- **Socks page has a duplicate H1** — `<h1>Cycling Socks</h1>` tag inside the description field
- **No SEO plugin installed** — title tag and H1 cannot be set independently (both derive from category name)

### SEO Changeset

- **Report:** `projects/sg-seo/reports/seo-changeset-quick-wins.md`
- **SG Vault copy:** `SG Vault/reports/seo-changeset-quick-wins.md`
- **Status:** Awaiting Tim's approval

### Decisions

- **SEO plugin strongly recommended:** Installing Yoast or Rank Math would unlock independent title tags, meta descriptions, and OG tags. Without it, we can only change the category name (which controls both title and H1) and the description content.
- **Copywriter needed:** All 9 description updates require final copy per the content briefs before API execution.
- **No changes pushed to production** — changeset is a plan document only, awaiting approval.

### Next Steps

1. Tim reviews and approves the changeset
2. Decision on SEO plugin installation
3. Copywriter produces final description content for all 9 categories
4. Builder executes approved changes via WC API
5. QA verifies pages render correctly
6. Monitor rank movements via weekly tracker

---
## M5 Execution: On-Site Optimisation Complete (orchestrator, 2026-03-24)

### Rank Math Installed
Tim installed Rank Math SEO plugin. Confirmed active via REST API (`rankmath/v1` namespace). The `updateMeta` endpoint accepts `objectType: "term"`, `objectID`, and `meta` (including `rank_math_title` and `rank_math_description`).

### Changes Pushed to Production

**Category name changes (6):** via WP REST API (`/wp/v2/product_cat/{id}`)
- 64: Jerseys & Tops → Men's Cycling Jerseys
- 263: Socks → Cycling Socks
- 353: Gloves & Mitts → Cycling Gloves & Mitts
- 450: Men's Cycling Bib Shorts → Men's Cycling Shorts & Bib Shorts
- 1380: Cycling Gilets → Women's Cycling Gilets
- 448: Men's Long Sleeved Cycling Jerseys → Men's Long Sleeve Cycling Jerseys

**Rank Math SEO meta (9):** via Rank Math REST API (`/rankmath/v1/updateMeta`)
- All 9 categories now have custom title tags (keyword-rich, 49-60 chars) and meta descriptions (147-160 chars)

**Description content (9):** via WP REST API
- All 9 categories updated with SEO-enhanced descriptions (150-300 words each)
- Copywriter maintained existing brand voice, added keyword targeting, internal links
- Socks page duplicate H1 tag removed
- Gloves page now features Climb & Conquer range prominently

**WC API note:** The WooCommerce API key has read-only permissions. All write operations used the WP REST API instead.

### Verified Live
All 9 pages verified in browser — title tags, meta descriptions, H1s, and descriptions rendering correctly.

### For Tomorrow
1. **New page creation:** CONTENT-001 (women's shorts), CONTENT-002-006 (CK landing pages), CONTENT-009 (cycling clothing hub)
2. **Technical SEO plan:** Site speed, schema markup, crawl errors, sitemaps — separate workstream
