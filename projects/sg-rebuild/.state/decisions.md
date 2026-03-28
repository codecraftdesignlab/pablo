# SG Rebuild — Decision Log

## D001: Data Architecture — Option A (Unified Medusa)

**Date:** 2026-03-27
**Decision:** Merge everything into Medusa with custom modules. No dual-system sync.

**What this means:**

### Native Medusa Modules
- **Product Module** — products, variants (sku, barcode, prices), options, categories, tags, images
- **Inventory Module** — stock levels per location, reservations
- **Stock Location Module** — warehouse locations

### Custom Modules (to build)
- **Article Module** — shared product blueprints (size charts, features, specs, commodity codes, weight, materials). Linked to products via Module Links (one article → many products).
- **Operations Module** — cost price, supplier, MOQ, wholesale price, sales velocity, reorder data, procurement scheduling. Linked to variants via Module Links.

### What Gets Retired
- Daily WooCommerce ↔ Supabase sync — no longer needed
- `operational_skus` table — data migrates into Medusa Inventory Module + Operations Module
- `articles` table — data migrates into Article Module

### Migration Path
1. Scaffold Medusa (in progress)
2. Build Article Module + Operations Module
3. Import WooCommerce products → Medusa Product Module
4. Import operational_skus → Inventory Module + Operations Module
5. Import articles → Article Module
6. Link articles to products, operations data to variants
7. Validate, then retire the old tables

**Why:** Eliminates the fragile daily sync between WooCommerce and Supabase. Single source of truth for all product, stock, and operational data. Articles become a first-class entity queryable on the frontend (size charts, features, "other designs in this style").
