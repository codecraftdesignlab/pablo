---
title: SEO Changeset — Quick Wins (Category Page Optimisation)
date: 2026-03-24
type: changeset
project: sg-seo
status: awaiting-approval
tags:
  - seo
  - woocommerce
  - category-pages
  - stolen-goat
---

# SEO Changeset — Quick Wins

**Date:** 2026-03-24
**Status:** Awaiting Tim's approval
**Scope:** 9 WooCommerce category pages — on-page optimisation via API

---

## Platform Limitation

**There is no SEO plugin installed** on stolengoat.com (no Yoast, Rank Math, or AIOSEO). This means:

- The **title tag** is auto-generated as `{category name} – Stolen Goat`
- The **H1** on category pages equals the category name
- **Title tag and H1 cannot be set independently** — both are derived from the WooCommerce category `name` field
- **Meta descriptions cannot be set** without installing an SEO plugin — there is no API mechanism to store them
- The only SEO-relevant fields we can change via the WC API are `name` (affects title + H1) and `description` (on-page content)

**Recommendation:** Install Yoast SEO or Rank Math to unlock independent title tags, meta descriptions, and OG tags. This changeset documents the ideal meta descriptions for when a plugin is installed.

### What This Changeset Can Do via API

| Field | API Field | Effect |
|---|---|---|
| Category name | `name` | Changes both title tag and H1 |
| Description | `description` | On-page content below product grid |

### What Requires an SEO Plugin

| Field | Status |
|---|---|
| Custom title tag (independent of H1) | Needs Yoast/Rank Math |
| Meta description | Needs Yoast/Rank Math |
| OG tags | Needs Yoast/Rank Math |

---

## Change 1: Men's Cycling Jerseys

**Category ID:** 64
**Slug:** `jerseys-tops`
**URL:** `/product-category/mens/jerseys-tops/`
**Content brief:** CONTENT-010
**Phase:** 1 (week 1)
**Addressable volume:** ~13,200/mo

### Name Change

| | Value |
|---|---|
| **Current name** | Jerseys & Tops |
| **Proposed name** | Men's Cycling Jerseys |
| **Current title tag** | Jerseys & Tops – Stolen Goat |
| **Resulting title tag** | Men's Cycling Jerseys – Stolen Goat |
| **Current H1** | Jerseys & Tops |
| **Resulting H1** | Men's Cycling Jerseys |

**Rationale:** "Jerseys & Tops" contains no SEO keywords. Adding "Cycling" and "Men's" targets the high-volume cluster: cycling jersey (4,580/mo, pos 12.2), mens cycling jersey (2,543/mo, pos 11.2), cycling jerseys (2,402/mo, pos 9.0). This page has 59,120 impressions over 90 days but sits on page 2 with only 1.0% CTR.

**Note:** The brief recommends title tag `Men's Cycling Jerseys — Short & Long Sleeve | Stolen Goat` but without an SEO plugin, the title tag will be `Men's Cycling Jerseys – Stolen Goat` (39 chars). The shorter version still targets the primary keywords effectively.

### Meta Description (requires SEO plugin)

| | Value |
|---|---|
| **Current** | (none) |
| **Proposed** | Shop men's cycling jerseys from Stolen Goat. Bold short sleeve and long sleeve cycling jerseys for road, gravel and MTB. UK-designed, premium fabrics. (152 chars) |

### Description Change

| | Value |
|---|---|
| **Current** | 721 chars — generic copy about Ibex, Kiko, Climbers, and Epic jersey ranges. No keyword targeting. |
| **Proposed** | Keep existing brand copy. Prepend a keyword-rich intro paragraph and append internal links section. See CONTENT-010 brief for full content outline. |

**Action required:** Copywriter to produce final description content per CONTENT-010 brief before API update.

---

## Change 2: Cycling Socks

**Category ID:** 263
**Slug:** `socks`
**URL:** `/product-category/accessories/body/socks/`
**Content brief:** CONTENT-011
**Phase:** 1 (week 2)
**Addressable volume:** ~11,500/mo

### Name Change

| | Value |
|---|---|
| **Current name** | Socks |
| **Proposed name** | Cycling Socks |
| **Current title tag** | Socks – Stolen Goat |
| **Resulting title tag** | Cycling Socks – Stolen Goat |
| **Current H1** | Socks |
| **Resulting H1** | Cycling Socks |

**Rationale:** "Socks" alone misses the entire "cycling socks" cluster (6,090/mo, pos 10.7) and "cycle socks" (3,600/mo, not ranking). Adding "Cycling" directly targets the primary keyword. Currently 19,634 impressions, 282 clicks, 1.4% CTR — position 12.8 average.

**Note:** The existing description already contains an H1 tag `<h1>Cycling Socks</h1>` inside the description field — this is a duplicate H1 and should be removed when the category name is updated, as the category name already renders as the page H1.

### Meta Description (requires SEO plugin)

| | Value |
|---|---|
| **Current** | (none) |
| **Proposed** | Shop cycling socks from Stolen Goat. Bold designs in performance fabrics. Men's and women's cycling socks for road, gravel and indoor riding. UK designed. (155 chars) |

### Description Change

| | Value |
|---|---|
| **Current** | 286 chars — includes a duplicate `<h1>Cycling Socks</h1>` tag plus casual brand copy. |
| **Proposed** | Remove duplicate H1 tag. Enhance copy to 150-200 words covering sock types, materials, height options. Naturally include "cycling socks", "cycle socks", "cycling socks mens". See CONTENT-011 brief. |

**Action required:** Copywriter to produce final description content per CONTENT-011 brief. Remove the `<h1>` tag from description field.

---

## Change 3: Cycling Gloves & Mitts

**Category ID:** 353
**Slug:** `cycling-gloves`
**URL:** `/product-category/accessories/hands/cycling-gloves/`
**Content brief:** CONTENT-008
**Phase:** 1 (week 3) for quick win; Phase 3 (week 12) for full overhaul
**Addressable volume:** ~18,000/mo

### Name Change

| | Value |
|---|---|
| **Current name** | Gloves & Mitts |
| **Proposed name** | Cycling Gloves & Mitts |
| **Current title tag** | Gloves & Mitts – Stolen Goat |
| **Resulting title tag** | Cycling Gloves & Mitts – Stolen Goat |
| **Current H1** | Gloves & Mitts |
| **Resulting H1** | Cycling Gloves & Mitts |

**Rationale:** "Gloves & Mitts" is generic — adding "Cycling" targets the primary keyword cluster: cycling gloves (5,400/mo, not ranking), cycling mitts (1,774/mo, pos 7.6). The page currently ranks #82 for "bike cycling gloves". Climb & Conquer gloves are SG's top organic revenue product (7.3% CVR, GBP 555 over 90 days) but the category page doesn't capitalise on this.

### Meta Description (requires SEO plugin)

| | Value |
|---|---|
| **Current** | (none) |
| **Proposed** | Shop cycling gloves and mitts from Stolen Goat. From Climb & Conquer winter gloves to lightweight summer mitts. Premium UK-designed cycling handwear. (150 chars) |

### Description Change

| | Value |
|---|---|
| **Current** | 287 chars — generic copy about keeping hands protected. No mention of Climb & Conquer (top converter). |
| **Proposed** | Expand to 250-300 words. Feature Climb & Conquer range prominently. Cover winter gloves vs summer mitts, technology, sizing. See CONTENT-008 brief. |

**Action required:** Copywriter to produce final description content per CONTENT-008 brief.

---

## Change 4: Men's Cycling Gilets

**Category ID:** 453
**Slug:** `cycling-gilets`
**URL:** `/product-category/mens/cycling-gilets/` (assumed from parent structure)
**Content brief:** CONTENT-012
**Phase:** 1 (week 3)
**Addressable volume:** ~5,000/mo

### Name Change

| | Value |
|---|---|
| **Current name** | Men's Cycling Gilets |
| **Proposed name** | Men's Cycling Gilets |
| **Current title tag** | Men's Cycling Gilets – Stolen Goat |
| **Resulting title tag** | Men's Cycling Gilets – Stolen Goat |
| **Current H1** | Men's Cycling Gilets |
| **Resulting H1** | Men's Cycling Gilets |

**NO NAME CHANGE NEEDED.** The current name already contains the target keywords. The title tag `Men's Cycling Gilets – Stolen Goat` effectively targets "cycling gilet men" (1,141/mo, pos 7.9) and "mens cycling gilet" (1,009/mo, pos 14.7).

**Note:** The brief recommends `Men's Cycling Gilets — Lightweight & Windproof | Stolen Goat` as the ideal title tag, but this would require an SEO plugin. The current auto-generated title is already well-targeted.

### Meta Description (requires SEO plugin)

| | Value |
|---|---|
| **Current** | (none) |
| **Proposed** | Shop men's cycling gilets from Stolen Goat. Lightweight, packable and windproof cycling gilets for road, gravel and MTB. UK designed, bold designs. (148 chars) |

### Description Change

| | Value |
|---|---|
| **Current** | 236 chars — decent brand copy about layering and changeable weather. |
| **Proposed** | Expand to 200-250 words. Add gilet types (packable, windproof, insulated), temperature guidance, layering system narrative. Naturally include "cycling gilet", "cycling gilet men", "mens cycling gilet". See CONTENT-012 brief. |

**Action required:** Copywriter to expand description per CONTENT-012 brief.

---

## Change 5: Men's Cycling Bib Shorts

**Category ID:** 450
**Slug:** `cycling-bib-shorts`
**URL:** `/product-category/mens/cycling-bib-shorts/` (assumed from parent structure)
**Content brief:** CONTENT-007
**Phase:** 3 (weeks 9-10) — overhaul
**Addressable volume:** ~30,000/mo

### Name Change

| | Value |
|---|---|
| **Current name** | Men's Cycling Bib Shorts |
| **Proposed name** | Men's Cycling Shorts & Bib Shorts |
| **Current title tag** | Men's Cycling Bib Shorts – Stolen Goat |
| **Resulting title tag** | Men's Cycling Shorts & Bib Shorts – Stolen Goat |
| **Current H1** | Men's Cycling Bib Shorts |
| **Resulting H1** | Men's Cycling Shorts & Bib Shorts |

**Rationale:** The current name targets only "bib shorts" queries. The massive keyword cluster includes "cycling shorts men" (5,400/mo), "cycling shorts mens" (5,400/mo), and "bicycle shorts men" (5,400/mo) — all with zero SG visibility. Adding "Shorts &" broadens the page's keyword targeting to capture both "shorts" and "bib shorts" searchers. Currently at position 96 for "cycle shorts men's" and 16.7 for "bib shorts".

### Meta Description (requires SEO plugin)

| | Value |
|---|---|
| **Current** | (none) |
| **Proposed** | Shop men's cycling shorts and bib shorts. Premium padded cycling shorts with Italian chamois. UK-designed for road, gravel and MTB. Free delivery over GBP 50. (155 chars) |

### Description Change

| | Value |
|---|---|
| **Current** | 409 chars — decent copy about chamois and comfort, but no keyword targeting for "cycling shorts men". |
| **Proposed** | Expand to 300-350 words. Add bib shorts vs shorts comparison, chamois technology detail, range overview (road, gravel, MTB), fit and sizing link. Naturally include "cycling shorts men", "cycling bib shorts", "bib shorts". See CONTENT-007 brief. |

**Action required:** Copywriter to produce full overhaul content per CONTENT-007 brief.

---

## Change 6: Women's Cycling Bib Shorts

**Category ID:** 1389
**Slug:** `womens-cycling-bib-shorts`
**URL:** `/product-category/womens/womens-cycling-bib-shorts/`
**Content brief:** Referenced in strategy report (Section 7)
**Phase:** 1 (week 4) — quick win
**Addressable volume:** ~1,500/mo (as quick win; full women's shorts opportunity is ~250,000/mo via new page)

### Name Change

| | Value |
|---|---|
| **Current name** | Women's Cycling Bib Shorts |
| **Proposed name** | Women's Cycling Bib Shorts |
| **Current title tag** | Women's Cycling Bib Shorts – Stolen Goat |
| **Resulting title tag** | Women's Cycling Bib Shorts – Stolen Goat |
| **Current H1** | Women's Cycling Bib Shorts |
| **Resulting H1** | Women's Cycling Bib Shorts |

**NO NAME CHANGE NEEDED.** The current name already targets "womens bib shorts" (1,082/mo, pos 12.3) and "womens cycling bib shorts" (480/mo). The auto-generated title tag is adequate.

**Note:** The strategy recommends `Women's Cycling Bib Shorts — Padded & Performance | Stolen Goat` as the ideal title tag (requires SEO plugin). When the dedicated women's cycling shorts collection page (CONTENT-001) is created, this page should cross-link to it.

### Meta Description (requires SEO plugin)

| | Value |
|---|---|
| **Current** | (none) |
| **Proposed** | Shop women's cycling bib shorts from Stolen Goat. Premium women's-specific chamois, bold designs, performance fabrics. UK designed for road, gravel and indoor riding. (160 chars) |

### Description Change

| | Value |
|---|---|
| **Current** | 409 chars — good copy about chamois quality and comfort. |
| **Proposed** | Expand to 200-250 words. Add chamois detail, fit guidance, range overview. Naturally include "womens bib shorts", "womens cycling bib shorts". Add cross-link to women's shorts page when live. See strategy Section 7. |

**Action required:** Copywriter to expand description. Cross-link to CONTENT-001 page when it launches.

---

## Change 7: Women's Cycling Gilets

**Category ID:** 1380
**Slug:** `womens-gilets`
**URL:** `/product-category/womens/womens-gilets/` (assumed from slug)
**Content brief:** Referenced in strategy report (Cluster 4 + Section 7)
**Phase:** 1 (week 3) — quick win
**Addressable volume:** ~1,600/mo

### Name Change

| | Value |
|---|---|
| **Current name** | Cycling Gilets |
| **Proposed name** | Women's Cycling Gilets |
| **Current title tag** | Cycling Gilets – Stolen Goat |
| **Resulting title tag** | Women's Cycling Gilets – Stolen Goat |
| **Current H1** | Cycling Gilets |
| **Resulting H1** | Women's Cycling Gilets |

**Rationale:** The current name "Cycling Gilets" is gender-neutral despite this being the women's category (slug: `womens-gilets`). Adding "Women's" targets "cycling gilet womens" (840/mo, pos 5.4 — already almost top 5) and "womens cycling gilet" (762/mo, pos 12.0). This also differentiates from the men's gilets page and prevents keyword cannibalisation.

### Meta Description (requires SEO plugin)

| | Value |
|---|---|
| **Current** | (none) |
| **Proposed** | Shop women's cycling gilets from Stolen Goat. Lightweight, packable and windproof gilets for road, gravel and commuting. Bold designs, UK designed. (147 chars) |

### Description Change

| | Value |
|---|---|
| **Current** | 313 chars — decent copy about lightweight layering. Already mentions "women's cycling gilets". |
| **Proposed** | Expand to 150-200 words. Naturally include "cycling gilet womens", "womens cycling gilet". Cross-link to men's gilets and women's jackets. See strategy Section 7. |

**Action required:** Copywriter to expand description.

---

## Change 8: Men's Long Sleeve Cycling Jerseys

**Category ID:** 448
**Slug:** `long-sleeve-cycling-jerseys`
**URL:** `/product-category/mens/long-sleeve-cycling-jerseys/` (assumed from parent structure)
**Content brief:** Referenced in strategy report (Cluster 3 + Section 7)
**Phase:** 1 (week 1) — quick win
**Addressable volume:** ~2,700/mo

### Name Change

| | Value |
|---|---|
| **Current name** | Men's Long Sleeved Cycling Jerseys |
| **Proposed name** | Men's Long Sleeve Cycling Jerseys |
| **Current title tag** | Men's Long Sleeved Cycling Jerseys – Stolen Goat |
| **Resulting title tag** | Men's Long Sleeve Cycling Jerseys – Stolen Goat |
| **Current H1** | Men's Long Sleeved Cycling Jerseys |
| **Resulting H1** | Men's Long Sleeve Cycling Jerseys |

**Rationale:** Minor wording adjustment. The target keyword is "long sleeve cycling jersey" (2,714/mo, pos 8.5) — using "Long Sleeve" (without the "d") is a closer match to the search term. This is a low-risk, high-confidence change.

### Meta Description (requires SEO plugin)

| | Value |
|---|---|
| **Current** | (none) |
| **Proposed** | Shop men's long sleeve cycling jerseys from Stolen Goat. Lightweight UV options and thermal styles for year-round riding. Premium quality, UK designed. (151 chars) |

### Description Change

| | Value |
|---|---|
| **Current** | 279 chars — decent copy about lightweight and thermal options. |
| **Proposed** | Expand to 150-200 words. Mention "long sleeve cycling jersey" naturally. Add seasonal guidance (UV vs thermal). Link to base layers, gilets, arm warmers. See strategy Section 7. |

**Action required:** Copywriter to expand description.

---

## Change 9: Cycling Arm Warmers

**Category ID:** 303
**Slug:** `cycling-arm-warmers`
**URL:** `/product-category/accessories/cycling-arm-warmers/` (assumed from slug)
**Content brief:** Referenced in strategy report (Cluster 9 + Section 7)
**Phase:** 1 (week 2) — quick win
**Addressable volume:** ~7,400/mo

### Name Change

| | Value |
|---|---|
| **Current name** | Cycling Arm Warmers |
| **Proposed name** | Cycling Arm Warmers |
| **Current title tag** | Cycling Arm Warmers – Stolen Goat |
| **Resulting title tag** | Cycling Arm Warmers – Stolen Goat |
| **Current H1** | Cycling Arm Warmers |
| **Resulting H1** | Cycling Arm Warmers |

**NO NAME CHANGE NEEDED.** The current name already targets "cycling arm warmers" (2,174/mo, pos 6.6) and "arm warmers" (5,201/mo, pos 7.9). The title tag is well-targeted.

**Note:** The brief recommends `Cycling Arm Warmers — UV Protection & Thermal | Stolen Goat` as the ideal title tag (requires SEO plugin). The current auto-generated title is already effective.

### Meta Description (requires SEO plugin)

| | Value |
|---|---|
| **Current** | (none) |
| **Proposed** | Shop cycling arm warmers from Stolen Goat. Lightweight UV arm screens and thermal arm warmers for year-round riding. Easy to stash, bold designs. UK designed. (158 chars) |

### Description Change

| | Value |
|---|---|
| **Current** | 404 chars — includes a hyperlink to short sleeve jerseys. Mentions Ibex arm screens (UV) and Kiko arm warmers (thermal). |
| **Proposed** | Expand to 150-200 words. Naturally include "arm warmers" and "cycling arm warmers". Add layering system links to leg warmers, neck warmers, gilets. See strategy Section 7. |

**Action required:** Copywriter to expand description.

---

## Summary of API Changes

### Name Changes (4 categories)

These are the only categories that need a `name` field update:

| # | ID | Current Name | Proposed Name | Impact |
|---|---|---|---|---|
| 1 | 64 | Jerseys & Tops | Men's Cycling Jerseys | Title + H1 change |
| 2 | 263 | Socks | Cycling Socks | Title + H1 change |
| 3 | 353 | Gloves & Mitts | Cycling Gloves & Mitts | Title + H1 change |
| 4 | 450 | Men's Cycling Bib Shorts | Men's Cycling Shorts & Bib Shorts | Title + H1 change |
| 5 | 1380 | Cycling Gilets | Women's Cycling Gilets | Title + H1 change |
| 6 | 448 | Men's Long Sleeved Cycling Jerseys | Men's Long Sleeve Cycling Jerseys | Minor wording fix |

### No Name Change Needed (3 categories)

| # | ID | Current Name | Reason |
|---|---|---|---|
| 1 | 453 | Men's Cycling Gilets | Already well-targeted |
| 2 | 1389 | Women's Cycling Bib Shorts | Already well-targeted |
| 3 | 303 | Cycling Arm Warmers | Already well-targeted |

### Description Updates (all 9 categories)

All 9 categories need description content enhancements — either expansion of existing copy or addition of keyword-rich paragraphs. This requires copywriter input before execution.

### SEO Plugin Recommendation

Installing Yoast SEO or Rank Math would unlock:
- **Independent title tags** — e.g. `Men's Cycling Jerseys — Short & Long Sleeve | Stolen Goat` instead of being limited to `{name} – Stolen Goat`
- **Meta descriptions** — 9 proposed meta descriptions documented above are ready to deploy once a plugin is installed
- **OG tags** — social media sharing optimisation
- **XML sitemap control** — better crawl management
- **Schema markup** — enhanced SERP features

This is a **high-impact, low-effort recommendation** that would significantly increase the effectiveness of these changes.

---

## Execution Plan

1. **Tim approves** this changeset (name changes + description approach)
2. **Install SEO plugin** (recommended — unlocks meta descriptions and independent titles)
3. **Copywriter produces** final description content for all 9 categories per their respective briefs
4. **Builder executes** name changes via WC API (6 categories)
5. **Builder executes** description updates via WC API (all 9 categories)
6. **QA verifies** each page renders correctly (title tag, H1, description, no broken layouts)
7. **Monitor rankings** via weekly rank tracker (already running every Monday at 06:30)

### API Commands (for execution phase)

```python
from tools.wordpress.woocommerce import update_category

# Change 1: Men's Cycling Jerseys
update_category(64, name="Men's Cycling Jerseys")

# Change 2: Cycling Socks
update_category(263, name="Cycling Socks")

# Change 3: Cycling Gloves & Mitts
update_category(353, name="Cycling Gloves & Mitts")

# Change 5: Men's Cycling Shorts & Bib Shorts
update_category(450, name="Men's Cycling Shorts & Bib Shorts")

# Change 7: Women's Cycling Gilets
update_category(1380, name="Women's Cycling Gilets")

# Change 8: Men's Long Sleeve Cycling Jerseys
update_category(448, name="Men's Long Sleeve Cycling Jerseys")
```

**Do not execute until Tim approves.**
