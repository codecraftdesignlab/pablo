"""Import WooCommerce products into Medusa via Admin API.

Usage:
    python import-products.py              # Full import
    python import-products.py --dry-run    # Validate only, no API calls
    python import-products.py --limit 10   # Import only first N published products

Source: productsFull.json (local WC export)
Target: Medusa Admin API (http://localhost:9000)
Enrichment: Supabase operational_skus + articles tables
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime

import psycopg2
import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv("C:/ClaudeProjects/sg-backend/.env")

PRODUCTS_JSON = (
    r"C:\Users\timbl\stolen goat Dropbox\tim bland\Stolen Goat"
    r"\Multichannel Manager\Tools\SkynetPowerDash\Repository\productsFull.json"
)
VAULT_LOG_DIR = (
    r"C:\Users\timbl\stolen goat Dropbox\tim bland\Obsidian\agents\logging"
)

# Medusa (JWT auth — no API key available)
MEDUSA_URL = os.environ.get("MEDUSA_API_URL", "http://localhost:9000")
DB_URL = os.environ["DATABASE_URL"]

# Known IDs from Task 1 setup
SALES_CHANNEL_ID = "sc_01KMQSH9FTN30J0GQH4QYB6922"
SHIPPING_PROFILE_ID = "sp_01KMQSGVKEGG6CQ5BBYT12VQMR"
STOCK_LOCATION_ID = "sloc_01KMT8E45ZYPGVWQ2927NT2R6N"
REGION_ID = "reg_01KMT8DQDXQ92RHQPBFKJ99FMW"

# Import settings
BATCH_SIZE = 10
BATCH_DELAY = 0.5  # seconds between batches
VAT_RATE = 1.20


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def get_auth_token():
    """Get JWT token from Medusa auth endpoint."""
    resp = requests.post(
        f"{MEDUSA_URL}/auth/user/emailpass",
        json={"email": "tim.bland@stolengoat.com", "password": "SG-admin-2026!"},
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["token"]


# Global — set at startup
MEDUSA_HEADERS = {}


# ---------------------------------------------------------------------------
# Stats tracker
# ---------------------------------------------------------------------------

class Stats:
    """Track import statistics."""

    def __init__(self):
        self.products_created = 0
        self.products_skipped = 0
        self.products_failed = 0
        self.variants_created = 0
        self.categories_created = 0
        self.categories_existing = 0
        self.tags_created = 0
        self.tags_existing = 0
        self.articles_matched = 0
        self.articles_unmatched = 0
        self.skus_total = 0
        self.skus_matched = 0
        self.sale_prices_count = 0
        self.skus_unmatched_list = []
        self.errors = []


# ---------------------------------------------------------------------------
# Medusa API helpers
# ---------------------------------------------------------------------------

def medusa_get(path, params=None):
    """GET request to Medusa Admin API."""
    resp = requests.get(
        f"{MEDUSA_URL}{path}",
        params=params,
        headers=MEDUSA_HEADERS,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def medusa_post(path, data):
    """POST request to Medusa Admin API. Returns (json, None) or (None, error)."""
    resp = requests.post(
        f"{MEDUSA_URL}{path}",
        json=data,
        headers=MEDUSA_HEADERS,
        timeout=60,
    )
    if resp.status_code >= 400:
        return None, resp.text
    return resp.json(), None


# ---------------------------------------------------------------------------
# Supabase lookups
# ---------------------------------------------------------------------------

def load_supabase_lookups():
    """Load operational_skus and articles from Supabase for matching."""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    # SKU lookup: sku -> {article_number, barcode, grams, cost_price, supplier, location}
    cur.execute("""
        SELECT sku, article_number, barcode, grams, cost_price, supplier, location
        FROM operational_skus
        WHERE sku IS NOT NULL AND sku != ''
    """)
    sku_lookup = {}
    for row in cur.fetchall():
        sku_lookup[row[0]] = {
            "article_number": row[1],
            "barcode": row[2],
            "grams": row[3],
            "cost_price": float(row[4]) if row[4] else None,
            "supplier": row[5],
            "location": row[6],
        }

    # Article lookup: article_number -> {grams, cost_price, supplier}
    cur.execute("""
        SELECT article, grams, cost_price, supplier
        FROM articles
        WHERE article IS NOT NULL
    """)
    article_lookup = {}
    for row in cur.fetchall():
        article_lookup[row[0]] = {
            "grams": row[1],
            "cost_price": float(row[2]) if row[2] else None,
            "supplier": row[3],
        }

    conn.close()
    print(f"  Loaded {len(sku_lookup)} operational SKUs")
    print(f"  Loaded {len(article_lookup)} articles")
    return sku_lookup, article_lookup


# ---------------------------------------------------------------------------
# Category import
# ---------------------------------------------------------------------------

def import_categories(dry_run=False):
    """Fetch WC categories and create in Medusa. Returns wc_id -> medusa_id map."""
    sys.path.insert(0, "C:/ClaudeProjects/pablo")
    from tools.wordpress.woocommerce import get_categories

    wc_cats = get_categories()
    print(f"  Fetched {len(wc_cats)} WC categories")

    # Sort: parents first (parent == 0), then children
    wc_cats.sort(key=lambda c: (c.get("parent", 0) != 0, c.get("parent", 0)))

    wc_to_medusa = {}  # wc_category_id -> medusa_category_id
    created = 0
    existing = 0

    for cat in wc_cats:
        if dry_run:
            wc_to_medusa[cat["id"]] = f"dry-run-{cat['id']}"
            created += 1
            continue

        # Check if already exists by handle
        result = medusa_get(
            "/admin/product-categories", {"handle": cat["slug"]}
        )
        if result.get("product_categories"):
            wc_to_medusa[cat["id"]] = result["product_categories"][0]["id"]
            existing += 1
            continue

        payload = {
            "name": cat["name"],
            "handle": cat["slug"],
            "description": cat.get("description") or "",
            "is_active": True,
            "is_internal": False,
        }

        # Link to parent if exists in our map
        wc_parent = cat.get("parent", 0)
        if wc_parent and wc_parent in wc_to_medusa:
            payload["parent_category_id"] = wc_to_medusa[wc_parent]

        result, error = medusa_post("/admin/product-categories", payload)
        if error:
            print(f"    WARN: Failed to create category '{cat['name']}': {error[:200]}")
            continue

        wc_to_medusa[cat["id"]] = result["product_category"]["id"]
        created += 1

    print(f"  Categories created: {created}, already existed: {existing}")
    return wc_to_medusa, created, existing


# ---------------------------------------------------------------------------
# Tag import
# ---------------------------------------------------------------------------

def import_tags(dry_run=False):
    """Fetch WC tags and create in Medusa. Returns wc_id -> medusa_id map."""
    sys.path.insert(0, "C:/ClaudeProjects/pablo")
    from tools.wordpress.woocommerce import get_tags

    wc_tags = get_tags()
    print(f"  Fetched {len(wc_tags)} WC tags")

    wc_to_medusa = {}
    created = 0
    existing = 0

    for tag in wc_tags:
        if dry_run:
            wc_to_medusa[tag["id"]] = f"dry-run-{tag['id']}"
            created += 1
            continue

        # Check if already exists by value
        result = medusa_get("/admin/product-tags", {"q": tag["name"]})
        found = False
        for t in result.get("product_tags", []):
            if t["value"] == tag["name"]:
                wc_to_medusa[tag["id"]] = t["id"]
                existing += 1
                found = True
                break
        if found:
            continue

        result, error = medusa_post("/admin/product-tags", {"value": tag["name"]})
        if error:
            print(f"    WARN: Failed to create tag '{tag['name']}': {error[:200]}")
            continue

        wc_to_medusa[tag["id"]] = result["product_tag"]["id"]
        created += 1

    print(f"  Tags created: {created}, already existed: {existing}")
    return wc_to_medusa, created, existing


# ---------------------------------------------------------------------------
# Product payload builder
# ---------------------------------------------------------------------------

def build_product_payload(wc_product, sku_lookup, article_lookup, cat_map, tag_map):
    """Build a Medusa product creation payload from WC product data.

    Returns: (payload, sale_prices, error_message)
    """
    # --- Variants ---
    variations = wc_product.get("variations_") or []
    if not variations and wc_product.get("type") == "simple":
        # Simple product: treat the product itself as a single variant
        variations = [
            {
                "id": wc_product["id"],
                "sku": wc_product.get("sku", ""),
                "regular_price": wc_product.get("regular_price") or wc_product.get("price", ""),
                "sale_price": wc_product.get("sale_price", ""),
                "price": wc_product.get("price", ""),
                "weight": wc_product.get("weight", ""),
                "attributes": [],
            }
        ]

    # Extract variation attribute definitions from product attributes
    wc_attrs = wc_product.get("attributes", [])
    variation_attrs = [a for a in wc_attrs if a.get("variation")]

    # Collect all option values actually used by variants (product-level attrs can be incomplete)
    actual_values = {}  # attr_name -> ordered set of values
    for var in variations:
        for attr in var.get("attributes", []):
            name = attr["name"]
            val = attr["option"]
            if name not in actual_values:
                actual_values[name] = []
            if val not in actual_values[name]:
                actual_values[name].append(val)

    # Build options for Medusa: [{title: "Size", values: ["S","M","L"]}]
    # Merge product-level options with actual variant values to catch missing sizes
    options = []
    for attr in variation_attrs:
        declared = list(attr["options"])
        actual = actual_values.get(attr["name"], [])
        # Add any variant values missing from declared options
        merged = list(declared)
        for v in actual:
            if v not in merged:
                merged.append(v)
        options.append({
            "title": attr["name"],
            "values": merged,
        })

    # Simple products with no variation attributes need a synthetic option
    if not options:
        options = [{"title": "Default", "values": ["Default"]}]

    # Build variants
    medusa_variants = []
    article_number = None  # Set from first matched SKU
    sale_prices = []  # Collect for Price List

    for var in variations:
        sku = var.get("sku", "")
        if not sku:
            continue

        # Enrich from operational_skus
        op_sku = sku_lookup.get(sku, {})
        art_num = op_sku.get("article_number")
        if art_num and not article_number:
            article_number = art_num

        # Weight priority: operational_skus.grams -> articles.grams -> WC weight
        weight = op_sku.get("grams")
        if not weight and art_num and art_num in article_lookup:
            weight = article_lookup[art_num].get("grams")
        if not weight and var.get("weight"):
            try:
                weight_val = float(var["weight"])
                if weight_val > 0:
                    weight = weight_val * 1000  # WC stores in kg, convert to grams
            except (ValueError, TypeError):
                weight = None

        # Price: convert from inc-VAT string to ex-VAT float
        prices = []
        reg_price = var.get("regular_price") or var.get("price", "")
        if reg_price and reg_price != "0":
            try:
                ex_vat = round(float(reg_price) / VAT_RATE, 2)
                prices.append({"currency_code": "gbp", "amount": ex_vat})
            except (ValueError, TypeError):
                pass

        # Track sale prices for Price List
        sale_price = var.get("sale_price", "")
        if sale_price and sale_price != "0" and sale_price != "":
            try:
                sale_ex_vat = round(float(sale_price) / VAT_RATE, 2)
                sale_prices.append({"sku": sku, "amount": sale_ex_vat})
            except (ValueError, TypeError):
                pass

        # Build variant option values: {"Size": "M"}
        var_options = {}
        for attr in var.get("attributes", []):
            var_options[attr["name"]] = attr["option"]

        # Simple products: if no variant-level attributes, derive from product options
        if not var_options:
            if variation_attrs:
                # Use first value of each variation attribute (e.g. Size: "One Size")
                for attr in variation_attrs:
                    if attr["options"]:
                        var_options[attr["name"]] = attr["options"][0]
            if not var_options:
                var_options = {"Default": "Default"}

        variant = {
            "title": f"{wc_product['name']} - {' / '.join(var_options.values())}" if len(var_options) > 0 and "Default" not in var_options else wc_product["name"],
            "sku": sku,
            "manage_inventory": True,
            "options": var_options,
            "prices": prices,
            "metadata": {
                "wc_variation_id": var.get("id"),
                "article_number": art_num,
                "cost_price": op_sku.get("cost_price"),
                "supplier": op_sku.get("supplier"),
            },
        }

        # Optional fields
        barcode = op_sku.get("barcode")
        if barcode:
            variant["barcode"] = barcode
        if weight:
            variant["weight"] = weight

        medusa_variants.append(variant)

    if not medusa_variants:
        return None, None, "No valid variants found"

    # --- Product payload ---
    # Categories
    categories = []
    for cat in wc_product.get("categories", []):
        medusa_cat_id = cat_map.get(cat["id"])
        if medusa_cat_id:
            categories.append({"id": medusa_cat_id})

    # Tags
    tags = []
    for tag in wc_product.get("tags", []):
        medusa_tag_id = tag_map.get(tag["id"])
        if medusa_tag_id:
            tags.append({"id": medusa_tag_id})

    # Images
    images = []
    for img in wc_product.get("images", []):
        if img.get("src"):
            images.append({"url": img["src"]})

    # Sanitise handle — skip trashed/invalid slugs
    import re
    handle = wc_product.get("slug") or None
    if handle and (handle.startswith("__") or handle.startswith("--") or "trashed" in handle
                   or not all(c.isalnum() or c in "-_" for c in handle)):
        handle = re.sub(r"[^a-z0-9-]", "", handle.lower().replace("_", "-"))
        handle = handle.strip("-")  # Remove leading/trailing dashes
        if not handle or "trashed" in handle:
            # Generate a handle from the product title
            handle = re.sub(r"[^a-z0-9]+", "-", wc_product["name"].lower()).strip("-")

    payload = {
        "title": wc_product["name"],
        "handle": handle,
        "description": wc_product.get("description", ""),
        "subtitle": wc_product.get("short_description", "") or None,
        "status": "published",
        "options": options,
        "variants": medusa_variants,
        "sales_channels": [{"id": SALES_CHANNEL_ID}],
        "metadata": {
            "wc_product_id": wc_product["id"],
            "wc_parent_sku": wc_product.get("sku", ""),
            "article_number": article_number,
        },
    }

    if images:
        payload["images"] = images
    if categories:
        payload["categories"] = categories
    if tags:
        payload["tags"] = tags

    return payload, sale_prices, None


# ---------------------------------------------------------------------------
# Main import loop
# ---------------------------------------------------------------------------

def import_products(wc_products, sku_lookup, article_lookup, cat_map, tag_map,
                    stats, dry_run=False):
    """Import all products into Medusa.

    Returns list of {variant_id, amount} for Price List creation.
    """
    total = len(wc_products)
    all_sale_prices = []

    for i, wc_prod in enumerate(wc_products, 1):
        name = wc_prod.get("name", "Unknown")
        handle = wc_prod.get("slug", "")

        # Batch delay
        if i > 1 and (i - 1) % BATCH_SIZE == 0:
            time.sleep(BATCH_DELAY)

        print(f"  [{i}/{total}] {name}...", end=" ", flush=True)

        # Duplicate check by handle
        if not dry_run and handle:
            try:
                existing = medusa_get("/admin/products", {"handle": handle})
                if existing.get("products"):
                    print("SKIPPED (exists)")
                    stats.products_skipped += 1
                    continue
            except Exception as e:
                print(f"WARN (dup check failed: {e})")

        # Build payload
        payload, sale_prices, error = build_product_payload(
            wc_prod, sku_lookup, article_lookup, cat_map, tag_map,
        )

        if error:
            print(f"SKIPPED ({error})")
            stats.products_skipped += 1
            continue

        # Track SKU match stats
        for v in payload["variants"]:
            stats.skus_total += 1
            if v.get("metadata", {}).get("article_number"):
                stats.skus_matched += 1

        # Track article match at product level
        art = payload["metadata"].get("article_number")
        if art:
            stats.articles_matched += 1
        else:
            stats.articles_unmatched += 1

        if dry_run:
            variant_count = len(payload["variants"])
            sale_count = len(sale_prices) if sale_prices else 0
            stats.products_created += 1
            stats.variants_created += variant_count
            stats.sale_prices_count += sale_count
            print(f"DRY RUN ({variant_count} variants, article: {art or 'none'}, sales: {sale_count})")
            continue

        # Create in Medusa
        result, error = medusa_post("/admin/products", payload)
        if error:
            # Handle "already exists" as a skip, not a failure
            if "already exists" in error:
                print("SKIPPED (handle conflict)")
                stats.products_skipped += 1
                continue
            print(f"FAILED: {error[:150]}")
            stats.products_failed += 1
            stats.errors.append(f"{name}: {error[:300]}")
            continue

        created_product = result.get("product", {})
        created_variants = created_product.get("variants", [])
        variant_count = len(created_variants)
        stats.products_created += 1
        stats.variants_created += variant_count

        # Map created variant IDs to SKUs for sale price collection
        if sale_prices:
            sku_to_variant_id = {
                v["sku"]: v["id"] for v in created_variants if v.get("sku")
            }
            for sp in sale_prices:
                vid = sku_to_variant_id.get(sp["sku"])
                if vid:
                    all_sale_prices.append({
                        "variant_id": vid,
                        "amount": sp["amount"],
                    })
            stats.sale_prices_count += len(sale_prices)

        print(f"OK ({variant_count} variants)")

    return all_sale_prices


# ---------------------------------------------------------------------------
# Sale price list creation
# ---------------------------------------------------------------------------

def create_sale_price_list(all_sale_prices):
    """Create a Medusa Price List with sale prices.

    Medusa v2 price lists can be large — batch if needed.
    """
    if not all_sale_prices:
        return

    print(f"\n7. Creating sale price list ({len(all_sale_prices)} variants)...")

    # Medusa price list prices format
    prices = [
        {
            "variant_id": sp["variant_id"],
            "currency_code": "gbp",
            "amount": sp["amount"],
        }
        for sp in all_sale_prices
    ]

    payload = {
        "title": "WC Import Sale Prices",
        "description": f"Sale prices imported from WooCommerce on {datetime.now().strftime('%d %B %Y')} (converted ex-VAT)",
        "type": "sale",
        "status": "active",
        "prices": prices,
    }

    result, error = medusa_post("/admin/price-lists", payload)
    if error:
        print(f"  WARN: Price List creation failed: {error[:300]}")
        # Try in smaller batches
        if len(prices) > 500:
            print("  Retrying in batches of 500...")
            for batch_start in range(0, len(prices), 500):
                batch = prices[batch_start : batch_start + 500]
                batch_payload = {
                    "title": f"WC Import Sale Prices (batch {batch_start // 500 + 1})",
                    "description": f"Sale prices imported from WooCommerce (batch {batch_start // 500 + 1})",
                    "type": "sale",
                    "status": "active",
                    "prices": batch,
                }
                r, e = medusa_post("/admin/price-lists", batch_payload)
                if e:
                    print(f"  WARN: Batch {batch_start // 500 + 1} failed: {e[:200]}")
                else:
                    print(f"  Batch {batch_start // 500 + 1}: OK ({len(batch)} prices)")
    else:
        print(f"  OK -- {len(all_sale_prices)} sale prices applied")


# ---------------------------------------------------------------------------
# Log writer
# ---------------------------------------------------------------------------

def write_log(stats, dry_run, duration_secs):
    """Save import log to Obsidian vault."""
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    log_path = os.path.join(VAULT_LOG_DIR, f"product-import-{timestamp}.md")

    mode = "DRY RUN" if dry_run else "LIVE"
    duration_min = round(duration_secs / 60, 1)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"---\n")
        f.write(f"title: Product Import Log -- {datetime.now().strftime('%d %B %Y')}\n")
        f.write(f"date: {datetime.now().strftime('%d-%m-%Y')}\n")
        f.write(f"tags:\n  - import\n  - medusa\n  - sg-rebuild\ntype: journal\n---\n\n")
        f.write(f"# Product Import Log ({mode})\n\n")
        f.write(f"**Duration:** {duration_min} minutes\n\n")
        f.write(f"| Metric | Value |\n|---|---|\n")
        f.write(f"| Products created | {stats.products_created} |\n")
        f.write(f"| Products skipped (duplicates) | {stats.products_skipped} |\n")
        f.write(f"| Products failed | {stats.products_failed} |\n")
        f.write(f"| Variants created | {stats.variants_created} |\n")
        f.write(f"| Categories created | {stats.categories_created} |\n")
        f.write(f"| Categories existing | {stats.categories_existing} |\n")
        f.write(f"| Tags created | {stats.tags_created} |\n")
        f.write(f"| Tags existing | {stats.tags_existing} |\n")
        f.write(f"| Articles matched (product level) | {stats.articles_matched} |\n")
        f.write(f"| Articles unmatched | {stats.articles_unmatched} |\n")
        f.write(f"| SKU-level matches | {stats.skus_matched}/{stats.skus_total} |\n")
        f.write(f"| Sale prices | {stats.sale_prices_count} |\n")

        if stats.errors:
            f.write(f"\n## Errors ({len(stats.errors)})\n\n")
            for err in stats.errors[:50]:
                f.write(f"- {err}\n")

    print(f"\nLog saved: {log_path}")
    return log_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    global MEDUSA_HEADERS

    parser = argparse.ArgumentParser(description="Import WC products into Medusa")
    parser.add_argument("--dry-run", action="store_true", help="Validate only, no API calls")
    parser.add_argument("--limit", type=int, default=0, help="Import only first N published products")
    args = parser.parse_args()

    start_time = time.time()

    print("=" * 60)
    print(f"WC -> Medusa Product Import {'(DRY RUN)' if args.dry_run else ''}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    stats = Stats()

    # Step 1: Authenticate
    if not args.dry_run:
        print("\n1. Authenticating with Medusa...")
        token = get_auth_token()
        MEDUSA_HEADERS = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        print("  OK")
    else:
        print("\n1. DRY RUN -- skipping auth")

    # Step 2: Load Supabase lookup data
    print("\n2. Loading Supabase lookup data...")
    sku_lookup, article_lookup = load_supabase_lookups()

    # Step 3: Import categories
    print("\n3. Importing categories...")
    cat_map, cats_created, cats_existing = import_categories(dry_run=args.dry_run)
    stats.categories_created = cats_created
    stats.categories_existing = cats_existing

    # Step 4: Import tags
    print("\n4. Importing tags...")
    tag_map, tags_created, tags_existing = import_tags(dry_run=args.dry_run)
    stats.tags_created = tags_created
    stats.tags_existing = tags_existing

    # Step 5: Load products from JSON
    print(f"\n5. Loading products from JSON...")
    with open(PRODUCTS_JSON, "r", encoding="utf-8") as f:
        all_products = json.load(f)

    # Filter: published only, skip gift-cards
    products = [
        p for p in all_products
        if p.get("status") == "publish" and p.get("type") != "gift-card"
    ]
    print(f"  {len(all_products)} total -> {len(products)} published (non-gift-card)")

    if args.limit > 0:
        products = products[: args.limit]
        print(f"  Limited to first {args.limit} products")

    # Step 6: Import products
    print(f"\n6. Importing {len(products)} products...")
    all_sale_prices = import_products(
        products, sku_lookup, article_lookup, cat_map, tag_map, stats,
        dry_run=args.dry_run,
    )

    # Step 7: Create sale price list
    if all_sale_prices and not args.dry_run:
        create_sale_price_list(all_sale_prices)
    elif args.dry_run and stats.sale_prices_count > 0:
        print(f"\n7. DRY RUN -- would create Price List with {stats.sale_prices_count} sale prices")

    # Step 8: Report
    duration = time.time() - start_time
    print("\n" + "=" * 60)
    print("IMPORT SUMMARY")
    print("=" * 60)
    print(f"Products created:     {stats.products_created}")
    print(f"Products skipped:     {stats.products_skipped}")
    print(f"Products failed:      {stats.products_failed}")
    print(f"Variants created:     {stats.variants_created}")
    print(f"Categories created:   {stats.categories_created} (existing: {stats.categories_existing})")
    print(f"Tags created:         {stats.tags_created} (existing: {stats.tags_existing})")
    print(f"Articles matched:     {stats.articles_matched}")
    print(f"Articles unmatched:   {stats.articles_unmatched}")
    print(f"SKU-level matches:    {stats.skus_matched}/{stats.skus_total}")
    print(f"Sale prices:          {stats.sale_prices_count}")
    print(f"Duration:             {round(duration / 60, 1)} minutes")

    if stats.errors:
        print(f"\nErrors ({len(stats.errors)}):")
        for err in stats.errors[:20]:
            print(f"  - {err}")

    # Save log
    log_path = write_log(stats, args.dry_run, duration)

    print("\nDone.")
    return stats


if __name__ == "__main__":
    main()
