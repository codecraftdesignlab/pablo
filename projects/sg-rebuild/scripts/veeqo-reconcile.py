"""Veeqo sync reconciliation script.

Checks pg_net HTTP responses for pending Veeqo sync requests,
updates veeqo_sync_log with synced/failed status, and retries
failed pushes using the Veeqo wrapper.

Usage:
    python veeqo-reconcile.py           # reconcile + retry failures
    python veeqo-reconcile.py --dry-run # show what would happen
    python veeqo-reconcile.py --status  # summary counts only
"""

import sys
import os
import json
import argparse

import psycopg2
import psycopg2.extras

# Add Pablo root so we can import the Veeqo wrapper
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from tools.veeqo.veeqo import create_product, find_by_sku, VeeqoAPIError

from dotenv import load_dotenv

load_dotenv("C:/ClaudeProjects/sg-backend/.env")

DATABASE_URL = os.environ["DATABASE_URL"]


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def show_status(cur):
    """Print summary counts by status."""
    cur.execute("""
        SELECT status, count(*)
          FROM veeqo_sync_log
         GROUP BY status
         ORDER BY status
    """)
    rows = cur.fetchall()
    print("=== Veeqo Sync Status ===")
    total = 0
    for status, count in rows:
        print(f"  {status:10s}  {count:>6d}")
        total += count
    print(f"  {'TOTAL':10s}  {total:>6d}")
    return rows


def reconcile_pending(cur, dry_run=False):
    """Check pg_net responses for pending sync log entries."""
    cur.execute("""
        SELECT sl.id, sl.variant_id, sl.sku, sl.product_title, sl.variant_title,
               sl.http_request_id,
               hr.status_code, hr.content, hr.error_msg, hr.timed_out
          FROM veeqo_sync_log sl
          LEFT JOIN net._http_response hr ON hr.id = sl.http_request_id
         WHERE sl.status = 'pending'
           AND sl.http_request_id IS NOT NULL
         ORDER BY sl.created_at
    """)
    rows = cur.fetchall()
    if not rows:
        print("No pending entries with HTTP request IDs to reconcile.")
        return 0, 0

    synced = 0
    failed = 0

    for row in rows:
        log_id, variant_id, sku, product_title, variant_title, req_id, \
            status_code, content, error_msg, timed_out = row

        if status_code is None and not timed_out:
            # Response not yet available
            print(f"  [{sku}] request {req_id}: still in flight")
            continue

        if timed_out:
            msg = f"HTTP request timed out (req_id={req_id})"
            print(f"  [{sku}] TIMED OUT: {msg}")
            if not dry_run:
                cur.execute("""
                    UPDATE veeqo_sync_log
                       SET status = 'failed', error_message = %s, updated_at = now()
                     WHERE id = %s
                """, (msg, log_id))
            failed += 1
            continue

        if error_msg:
            msg = f"pg_net error: {error_msg}"
            print(f"  [{sku}] ERROR: {msg}")
            if not dry_run:
                cur.execute("""
                    UPDATE veeqo_sync_log
                       SET status = 'failed', error_message = %s, updated_at = now()
                     WHERE id = %s
                """, (msg, log_id))
            failed += 1
            continue

        if 200 <= status_code < 300:
            print(f"  [{sku}] SYNCED (HTTP {status_code})")
            if not dry_run:
                cur.execute("""
                    UPDATE veeqo_sync_log
                       SET status = 'synced', updated_at = now()
                     WHERE id = %s
                """, (log_id,))
            synced += 1
        else:
            # Veeqo returned an error
            msg = f"Veeqo HTTP {status_code}: {(content or '')[:500]}"
            print(f"  [{sku}] FAILED: {msg}")
            if not dry_run:
                cur.execute("""
                    UPDATE veeqo_sync_log
                       SET status = 'failed', error_message = %s, updated_at = now()
                     WHERE id = %s
                """, (msg, log_id))
            failed += 1

    print(f"\nReconciled: {synced} synced, {failed} failed, "
          f"{len(rows) - synced - failed} still in flight")
    return synced, failed


def retry_failed(cur, dry_run=False):
    """Retry failed sync entries using the Python Veeqo wrapper."""
    cur.execute("""
        SELECT sl.id, sl.variant_id, sl.sku, sl.product_title, sl.variant_title,
               sl.price_gbp
          FROM veeqo_sync_log sl
         WHERE sl.status = 'failed'
         ORDER BY sl.created_at
    """)
    rows = cur.fetchall()
    if not rows:
        print("No failed entries to retry.")
        return 0, 0

    retried = 0
    still_failed = 0

    for row in rows:
        log_id, variant_id, sku, product_title, variant_title, price_gbp = row

        # Check if already in Veeqo (may have been pushed manually)
        existing = find_by_sku(sku)
        if existing:
            print(f"  [{sku}] already in Veeqo (product {existing['id']}), marking synced")
            if not dry_run:
                cur.execute("""
                    UPDATE veeqo_sync_log
                       SET status = 'synced', error_message = NULL, updated_at = now()
                     WHERE id = %s
                """, (log_id,))
            retried += 1
            continue

        if dry_run:
            print(f"  [{sku}] would retry: {product_title} / {variant_title}")
            continue

        # Build variant payload
        variant_payload = {
            "title": variant_title or sku,
            "sku_code": sku,
            "price": float(price_gbp) if price_gbp else 0.0,
            "tax_rate": 20.0,
            "weight": {"value": 0, "unit": "g"},
        }

        try:
            result = create_product(
                title=product_title or sku,
                variants=[variant_payload],
            )
            print(f"  [{sku}] RETRIED OK -> Veeqo product {result.get('id', '?')}")
            cur.execute("""
                UPDATE veeqo_sync_log
                   SET status = 'synced', error_message = NULL, updated_at = now()
                 WHERE id = %s
            """, (log_id,))
            retried += 1

        except VeeqoAPIError as e:
            msg = f"Retry failed: {e.status_code} {e.message[:300]}"
            print(f"  [{sku}] RETRY FAILED: {msg}")
            cur.execute("""
                UPDATE veeqo_sync_log
                   SET error_message = %s, updated_at = now()
                 WHERE id = %s
            """, (msg, log_id))
            still_failed += 1

        except Exception as e:
            msg = f"Retry exception: {str(e)[:300]}"
            print(f"  [{sku}] RETRY ERROR: {msg}")
            cur.execute("""
                UPDATE veeqo_sync_log
                   SET error_message = %s, updated_at = now()
                 WHERE id = %s
            """, (msg, log_id))
            still_failed += 1

    print(f"\nRetry results: {retried} synced, {still_failed} still failed")
    return retried, still_failed


def main():
    parser = argparse.ArgumentParser(description="Veeqo sync reconciliation")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--status", action="store_true", help="Show status counts only")
    args = parser.parse_args()

    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor()

    try:
        show_status(cur)

        if args.status:
            return

        print()
        print("--- Reconciling pending HTTP requests ---")
        reconcile_pending(cur, dry_run=args.dry_run)

        print()
        print("--- Retrying failed entries ---")
        retry_failed(cur, dry_run=args.dry_run)

        print()
        show_status(cur)

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
