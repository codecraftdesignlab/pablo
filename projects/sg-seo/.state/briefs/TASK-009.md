# TASK-009: WordPress Integration & On-Site Optimisation

## Objective

Build `tools/wordpress/` integration for reading and updating WordPress/WooCommerce pages, then implement the Phase 1 quick wins from the SEO strategy — on-page optimisation of existing category pages (meta titles, descriptions, H1s).

## Context

### WordPress Access
- **Credentials:** `wordpress-credentials.json` in project root (in .gitignore)
- **WP REST API:** username + application password → Basic Auth for pages/posts
- **WC REST API:** consumer_key + consumer_secret → query string auth for products/categories
- **Site:** https://stolengoat.com

### What Needs Changing
The strategy report identified 16 quick-win keywords on existing pages where on-page optimisation can improve rankings. The content briefs (CONTENT-007 through CONTENT-012) specify exact current vs proposed meta titles, descriptions, and H1s.

### Approval Gate
ALL changes must be presented to Tim for approval before being applied. Pablo prepares a changeset showing current vs proposed for each page, Tim reviews and approves.

## Scope

### Part 1: Build tools/wordpress/

Create a WordPress/WooCommerce integration module:

```
tools/wordpress/
  CLAUDE.md           — agent guide (auth, API patterns, rules)
  wordpress.py        — WP REST API wrapper (pages, posts, meta)
  woocommerce.py      — WC REST API wrapper (products, categories)
```

**wordpress.py functions:**
- `get_page(page_id)` → page content, title, slug, meta, Yoast/RankMath SEO fields
- `get_pages(params)` → list pages with filtering
- `update_page_seo(page_id, title=None, meta_description=None)` → update SEO meta fields
- `get_post(post_id)` / `get_posts(params)` → same for blog posts
- `search_pages(slug_contains)` → find pages by URL pattern

**woocommerce.py functions:**
- `get_product_category(category_id)` → category details, name, description, meta
- `get_product_categories(params)` → list categories
- `update_category_seo(category_id, name=None, description=None)` → update category SEO fields
- `get_product(product_id)` → product details

**Key consideration:** WooCommerce product category pages are the main target for SEO optimisation. These are the `/product-category/mens/jerseys-tops/` style URLs. The WC REST API manages these via the `products/categories` endpoint.

**SEO plugin detection:** The first thing to determine is which SEO plugin is installed (Yoast SEO, Rank Math, All in One SEO, or none). This affects how meta titles and descriptions are stored and accessed. The WP REST API may expose SEO fields as custom meta, or the SEO plugin may add its own REST endpoints.

### Part 2: Quick Win Optimisation Workflow

1. **Read current state** — for each page in CONTENT-007 through CONTENT-012, fetch current meta title, description, H1
2. **Generate changeset** — produce a clear "current vs proposed" table for Tim's review
3. **Wait for approval** — present changeset to Tim, do NOT apply changes until approved
4. **Apply changes** — update pages via the API
5. **Verify** — re-read pages to confirm changes were applied correctly

## Files to Read
- `wordpress-credentials.json` — auth details (DO NOT log contents)
- `.state/briefs/CONTENT-007.md` through `CONTENT-012.md` — the quick win content briefs
- `.state/research/keyword-universe.md` — quick wins section for reference
- `tools/search-console/CLAUDE.md` and `tools/analytics/CLAUDE.md` — patterns to follow

## Files to Create
- `tools/wordpress/CLAUDE.md` — agent guide
- `tools/wordpress/__init__.py`
- `tools/wordpress/wordpress.py` — WP REST wrapper
- `tools/wordpress/woocommerce.py` — WC REST wrapper

## Acceptance Criteria
- [ ] WordPress and WooCommerce API wrappers work end-to-end
- [ ] Can read current page titles, meta descriptions, and content for category pages
- [ ] Can update page SEO fields (meta title, meta description)
- [ ] SEO plugin detected and correct meta fields targeted
- [ ] Changeset prepared for quick-win pages (current vs proposed)
- [ ] All changes require Tim's explicit approval before application

## Testing
- Test framework: manual (API integration)
- Tests: verify read/write round-trip on a test page before touching production category pages

## Output
Append to `.state/handoff.md`. Update `.state/tasks.jsonl`.
