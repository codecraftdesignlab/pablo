"""Push all Medusa product variants to Veeqo.

One-off script -- run after import-products.py completes.

Groups Medusa variants by product (matching Veeqo's product->variants structure).
For each Medusa product: checks if any of its SKUs already exist in Veeqo,
creates the product (with all its variants) if not.

Usage:
    python bulk-veeqo-sync.py                # Full sync
    python bulk-veeqo-sync.py --dry-run      # Preview only, no API calls
    python bulk-veeqo-sync.py --limit 10     # Process only first N products
"""

import argparse
import os
import sys
import time
from collections import OrderedDict
from datetime import datetime

import psycopg2
from dotenv import load_dotenv

load_dotenv("C:/ClaudeProjects/sg-backend/.env")

sys.path.insert(0, "C:/ClaudeProjects/pablo")
from tools.veeqo.veeqo import create_product, find_by_sku, VeeqoAPIError

DB_URL = os.environ["DATABASE_URL"]
VAULT_LOG_DIR = (
    r"C:\Users\timbl\stolen goat Dropbox\tim bland\Obsidian\agents\logging"
)
BATCH_DELAY = 0.5  # seconds between Veeqo API calls


# ---------------------------------------------------------------------------
# Stats tracker
# ---------------------------------------------------------------------------

class Stats:
    """Track sync statistics."""

    def __init__(self):
        self.products_created = 0
        self.products_skipped = 0  # already in Veeqo
        self.products_failed = 0
        self.variants_created = 0
        self.variants_skipped = 0  # part of skipped products
        self.skus_total = 0
        self.errors = []


# ---------------------------------------------------------------------------
# Medusa data fetch
# ---------------------------------------------------------------------------

def get_medusa_products():
    """Fetch all Medusa products with their variants, grouped by product.

    Returns: OrderedDict of product_id -> {
        "title": str,
        "variants": [{"sku", "variant_title", "weight", "price"}, ...]
    }
    """
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    cur.execute("""
        SELECT
            p.id AS product_id,
            p.title AS product_title,
            pv.sku,
            pv.title AS variant_title,
            pv.weight,
            pr.amount AS price
        FROM product_variant pv
        JOIN product p ON p.id = pv.product_id
        LEFT JOIN product_variant_price_set pvps ON pvps.variant_id = pv.id
        LEFT JOIN price pr ON pr.price_set_id = pvps.price_set_id
                          AND pr.currency_code = 'gbp'
        WHERE pv.sku IS NOT NULL AND pv.sku != ''
          AND p.status = 'published'
          AND pv.deleted_at IS NULL
          AND p.deleted_at IS NULL
        ORDER BY p.title, pv.title
    """)

    rows = cur.fetchall()
    conn.close()

    # Group by product
    products = OrderedDict()
    for product_id, product_title, sku, variant_title, weight, price in rows:
        if product_id not in products:
            products[product_id] = {
                "title": product_title,
                "variants": [],
            }
        products[product_id]["variants"].append({
            "sku": sku,
            "variant_title": variant_title,
            "weight": weight,
            "price": float(price) if price is not None else None,
        })

    return products


# ---------------------------------------------------------------------------
# Veeqo sync
# ---------------------------------------------------------------------------

def check_product_exists_in_veeqo(variants):
    """Check if any of this product's SKUs already exist in Veeqo.

    Only checks the first SKU to avoid excessive API calls. If the first
    variant exists, the whole product was likely already pushed.
    """
    if not variants:
        return True  # no variants = skip

    first_sku = variants[0]["sku"]
    try:
        result = find_by_sku(first_sku)
        return result is not None
    except VeeqoAPIError:
        return False


def build_veeqo_variants(variants):
    """Convert Medusa variants to Veeqo variant format."""
    veeqo_variants = []
    for v in variants:
        variant = {
            "sku_code": v["sku"],
            "title": v["variant_title"] or v["sku"],
            "tax_rate": 20.0,
        }

        if v["price"] is not None:
            variant["price"] = float(v["price"])

        if v["weight"] is not None and v["weight"] > 0:
            variant["weight"] = {
                "value": int(v["weight"]),
                "unit": "g",
            }

        veeqo_variants.append(variant)

    return veeqo_variants


def sync_product(product_title, variants, stats, dry_run=False):
    """Sync a single Medusa product (with all its variants) to Veeqo.

    Returns: "created", "skipped", or "failed"
    """
    stats.skus_total += len(variants)

    # Check if already exists in Veeqo
    if not dry_run:
        try:
            exists = check_product_exists_in_veeqo(variants)
        except Exception as e:
            stats.products_failed += 1
            stats.errors.append(f"{product_title}: existence check failed: {e}")
            return "failed"

        if exists:
            stats.products_skipped += 1
            stats.variants_skipped += len(variants)
            return "skipped"

    elif dry_run:
        # In dry-run, still check existence for accurate reporting
        try:
            exists = check_product_exists_in_veeqo(variants)
            if exists:
                stats.products_skipped += 1
                stats.variants_skipped += len(variants)
                return "skipped"
        except Exception:
            pass  # In dry-run, if check fails, assume it would be created

    # Build Veeqo payload
    veeqo_variants = build_veeqo_variants(variants)

    if dry_run:
        stats.products_created += 1
        stats.variants_created += len(veeqo_variants)
        return "created"

    # Create in Veeqo
    try:
        create_product(
            title=product_title,
            variants=veeqo_variants,
        )
        stats.products_created += 1
        stats.variants_created += len(veeqo_variants)
        return "created"
    except VeeqoAPIError as e:
        stats.products_failed += 1
        stats.errors.append(f"{product_title}: {e.status_code} {e.message[:200]}")
        return "failed"
    except Exception as e:
        stats.products_failed += 1
        stats.errors.append(f"{product_title}: {str(e)[:200]}")
        return "failed"


# ---------------------------------------------------------------------------
# Log writer
# ---------------------------------------------------------------------------

def write_log(stats, dry_run, duration_secs):
    """Save sync log to Obsidian vault."""
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    log_path = os.path.join(VAULT_LOG_DIR, f"veeqo-sync-{timestamp}.md")

    mode = "DRY RUN" if dry_run else "LIVE"
    duration_min = round(duration_secs / 60, 1)

    os.makedirs(VAULT_LOG_DIR, exist_ok=True)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(f"title: Veeqo Sync Log -- {datetime.now().strftime('%d %B %Y')}\n")
        f.write(f"date: {datetime.now().strftime('%d-%m-%Y')}\n")
        f.write("tags:\n  - veeqo\n  - sync\n  - sg-rebuild\ntype: journal\n---\n\n")
        f.write(f"# Veeqo SKU Sync Log ({mode})\n\n")
        f.write(f"**Duration:** {duration_min} minutes\n\n")
        f.write("| Metric | Value |\n|---|---|\n")
        f.write(f"| Products created | {stats.products_created} |\n")
        f.write(f"| Products skipped (already in Veeqo) | {stats.products_skipped} |\n")
        f.write(f"| Products failed | {stats.products_failed} |\n")
        f.write(f"| Variants created | {stats.variants_created} |\n")
        f.write(f"| Variants skipped | {stats.variants_skipped} |\n")
        f.write(f"| Total SKUs processed | {stats.skus_total} |\n")

        if stats.errors:
            f.write(f"\n## Errors ({len(stats.errors)})\n\n")
            for err in stats.errors[:100]:
                f.write(f"- {err}\n")

    print(f"\nLog saved: {log_path}")
    return log_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Push all Medusa product variants to Veeqo"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Check existence but don't create products in Veeqo",
    )
    parser.add_argument(
        "--limit", type=int, default=0,
        help="Process only first N products (0 = all)",
    )
    args = parser.parse_args()

    start_time = time.time()

    print("=" * 60)
    print(f"Medusa -> Veeqo SKU Sync {'(DRY RUN)' if args.dry_run else ''}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Step 1: Fetch Medusa products
    print("\n1. Fetching products from Medusa (Supabase)...")
    products = get_medusa_products()
    total_variants = sum(len(p["variants"]) for p in products.values())
    print(f"   {len(products)} products, {total_variants} variants with SKUs")

    # Apply limit
    product_items = list(products.items())
    if args.limit > 0:
        product_items = product_items[: args.limit]
        print(f"   Limited to first {args.limit} products")

    # Step 2: Sync to Veeqo
    print(f"\n2. Syncing {len(product_items)} products to Veeqo...")
    stats = Stats()

    for i, (product_id, product_data) in enumerate(product_items, 1):
        title = product_data["title"]
        variant_count = len(product_data["variants"])
        skus_preview = ", ".join(
            v["sku"] for v in product_data["variants"][:3]
        )
        if variant_count > 3:
            skus_preview += f" (+{variant_count - 3} more)"

        print(f"   [{i}/{len(product_items)}] {title} ({variant_count} variants)...", end=" ", flush=True)

        result = sync_product(
            title, product_data["variants"], stats, dry_run=args.dry_run
        )

        if result == "created":
            label = "DRY RUN OK" if args.dry_run else "CREATED"
            print(f"{label}")
        elif result == "skipped":
            print("SKIPPED (exists)")
        else:
            print("FAILED")

        # Rate limiting delay between API calls
        if i < len(product_items):
            time.sleep(BATCH_DELAY)

    # Step 3: Summary
    duration = time.time() - start_time
    print("\n" + "=" * 60)
    print("SYNC SUMMARY")
    print("=" * 60)
    print(f"Products created:     {stats.products_created}")
    print(f"Products skipped:     {stats.products_skipped} (already in Veeqo)")
    print(f"Products failed:      {stats.products_failed}")
    print(f"Variants created:     {stats.variants_created}")
    print(f"Variants skipped:     {stats.variants_skipped}")
    print(f"Total SKUs processed: {stats.skus_total}")
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
