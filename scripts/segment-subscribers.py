"""Segment Stolen Goat subscribers by syncing WooCommerce order data from
Supabase into Mailchimp tags and merge fields.

Usage:
    python scripts/segment-subscribers.py              # full sync (push to Mailchimp)
    python scripts/segment-subscribers.py --dry-run    # analyse only, no Mailchimp writes
    python scripts/segment-subscribers.py --sample 50  # process only 50 subscribers (for testing)

Runs daily via Windows Task Scheduler at 05:00.
"""

import argparse
import hashlib
import json
import logging
import os
import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone

import psycopg2
import requests
from dotenv import load_dotenv

# --- Setup ---

sys.path.insert(0, "C:/ClaudeProjects/pablo")
load_dotenv("C:/ClaudeProjects/pablo/.env")

from tools.mailchimp.mailchimp import (
	AUTH,
	BASE_URL,
	HEADERS,
	SG_LIST_ID,
	create_merge_field,
	get_all_members,
	get_merge_fields,
	subscriber_hash,
	submit_batch,
	wait_for_batch,
)

LOG_DIR = "C:/Users/timbl/stolen goat Dropbox/tim bland/Obsidian/agents/logging"
STATE_FILE = "C:/ClaudeProjects/pablo/scripts/.state/segment-sync.json"

logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s %(levelname)s %(message)s",
	datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("segment")

# --- Supabase Connection ---

SUPABASE_CONFIG = {
	"host": "db.joqbwksjjahfmkfzsynm.supabase.co",
	"port": 5432,
	"dbname": "postgres",
	"user": "postgres",
	"password": "HFIdzClsxJ13FO2dR9POM7Rgr4GXVi9h",
}

# --- Category Mapping ---

# Map operational_skus.category (uppercased) to interest tags.
# Anything not listed here is assumed road-cycling.
RUNNING_CATEGORIES = {"RUN"}

NON_CYCLING_CATEGORIES = {
	"SWIMWEAR", "SWIM CAPS", "TOWELS", "NUTRITION",
	"BABY NIK", "BESPOKE",
}

GENDER_MAP = {
	"MENS": "mens",
	"WOMENS": "womens",
	"Mens": "mens",
	"Womens": "womens",
}

# Lifecycle thresholds (days since last order)
ACTIVE_DAYS = 90
LAPSED_DAYS = 365

# VIP thresholds
VIP_MIN_ORDERS = 3

# Emails to exclude from segmentation (internal, wholesale, test)
EXCLUDE_EMAIL_DOMAINS = {"stolengoat.com", "velovixen.com"}
EXCLUDE_EMAILS = set()  # specific addresses to exclude

# All segment tags managed by this script — anything not in this set is left alone.
MANAGED_TAGS = {
	"mens", "womens", "road-cycling", "running", "custom-kit",
	"vip", "active", "lapsed", "dormant", "prospect",
}

# Lifecycle tags are mutually exclusive.
LIFECYCLE_TAGS = {"vip", "active", "lapsed", "dormant", "prospect"}

# Merge fields we manage.
REQUIRED_MERGE_FIELDS = {
	"LASTORDER": ("Last Order Date", "text"),
	"ORDERCOUNT": ("Order Count", "text"),
	"TOTSPEND": ("Total Spend", "text"),
	"LIFECYCLE": ("Lifecycle Stage", "text"),
	"SEGTAGS": ("Interests", "text"),
}


# --- Data Extraction ---

def get_supabase_connection():
	return psycopg2.connect(**SUPABASE_CONFIG)


def build_sku_lookup(conn) -> dict:
	"""Build SKU -> {gender, category} lookup from operational_skus."""
	cur = conn.cursor()
	cur.execute("SELECT sku, gender, category FROM operational_skus")
	lookup = {}
	for sku, gender, category in cur.fetchall():
		lookup[sku] = {
			"gender": (gender or "").upper().strip(),
			"category": (category or "").upper().strip(),
		}
	cur.close()
	log.info("Loaded %d SKUs into lookup", len(lookup))
	return lookup


def extract_customer_data(conn, sku_lookup: dict) -> dict:
	"""Pull all completed orders from Supabase and aggregate per customer email.

	Returns: {email: {orders, total_spend, last_order, genders, categories, has_ck}}
	"""
	cur = conn.cursor()

	# Pull billing email, date, total, and line items for non-cancelled orders.
	cur.execute("""
		SELECT
			data->'billing'->>'email' AS email,
			data->>'date_created' AS date_created,
			(data->>'total')::numeric AS total,
			(data->>'total_tax')::numeric AS total_tax,
			data->'line_items' AS line_items
		FROM orders
		WHERE data->>'status' IN ('completed', 'processing', 'backorder')
			AND data->'billing'->>'email' IS NOT NULL
			AND data->'billing'->>'email' != ''
	""")

	customers = defaultdict(lambda: {
		"order_count": 0,
		"total_spend": 0.0,
		"last_order": None,
		"genders": set(),
		"is_running": False,
		"is_road_cycling": False,
		"has_ck": False,
	})

	row_count = 0
	for email, date_created, total, total_tax, line_items in cur:
		row_count += 1
		email = email.lower().strip()
		if not email:
			continue

		# Skip internal/wholesale/test emails
		domain = email.split("@")[-1] if "@" in email else ""
		if domain in EXCLUDE_EMAIL_DOMAINS or email in EXCLUDE_EMAILS:
			continue

		c = customers[email]
		c["order_count"] += 1

		# Revenue ex-VAT
		spend = float(total or 0) - float(total_tax or 0)
		c["total_spend"] += spend

		# Parse order date
		if date_created:
			try:
				order_date = datetime.fromisoformat(date_created.replace("Z", "+00:00"))
				# Ensure timezone-aware
				if order_date.tzinfo is None:
					order_date = order_date.replace(tzinfo=timezone.utc)
				if c["last_order"] is None or order_date > c["last_order"]:
					c["last_order"] = order_date
			except ValueError:
				pass

		# Process line items
		if not line_items:
			continue
		for item in line_items:
			sku = item.get("sku", "")
			if not sku:
				continue

			# Custom kit detection
			if sku.upper().startswith("CK"):
				c["has_ck"] = True

			# Look up SKU for gender and category
			sku_info = sku_lookup.get(sku)
			if sku_info:
				gender = sku_info["gender"]
				category = sku_info["category"]

				# Gender
				if gender in GENDER_MAP:
					c["genders"].add(GENDER_MAP[gender])

				# Category -> interest
				if category in RUNNING_CATEGORIES:
					c["is_running"] = True
				elif category and category not in NON_CYCLING_CATEGORIES:
					c["is_road_cycling"] = True

	cur.close()
	log.info("Processed %d order rows -> %d unique customers", row_count, len(customers))
	return dict(customers)


def calculate_segments(customer_data: dict, vip_spend_threshold: float) -> dict:
	"""Calculate tags and merge fields for each customer.

	Returns: {email: {tags: set, lifecycle: str, merge_fields: dict}}
	"""
	now = datetime.now(timezone.utc)
	results = {}

	for email, c in customer_data.items():
		tags = set()

		# Interest tags
		for g in c["genders"]:
			tags.add(g)
		if c["is_road_cycling"]:
			tags.add("road-cycling")
		if c["is_running"]:
			tags.add("running")
		if c["has_ck"]:
			tags.add("custom-kit")

		# Lifecycle tag
		last_order = c["last_order"]
		if last_order:
			days_since = (now - last_order).days

			if c["order_count"] >= VIP_MIN_ORDERS or c["total_spend"] >= vip_spend_threshold:
				lifecycle = "vip"
			elif days_since <= ACTIVE_DAYS:
				lifecycle = "active"
			elif days_since <= LAPSED_DAYS:
				lifecycle = "lapsed"
			else:
				lifecycle = "dormant"
		else:
			lifecycle = "prospect"

		tags.add(lifecycle)

		# Merge fields
		merge_fields = {
			"LASTORDER": last_order.strftime("%Y-%m-%d") if last_order else "",
			"ORDERCOUNT": str(c["order_count"]),
			"TOTSPEND": f"{c['total_spend']:.0f}",
			"LIFECYCLE": lifecycle,
			"SEGTAGS": ",".join(sorted(tags - LIFECYCLE_TAGS)),
		}

		results[email] = {
			"tags": tags,
			"lifecycle": lifecycle,
			"merge_fields": merge_fields,
		}

	return results


def calculate_vip_threshold(customer_data: dict) -> float:
	"""Top 10% by spend = VIP."""
	spends = sorted(
		(c["total_spend"] for c in customer_data.values() if c["total_spend"] > 0),
		reverse=True,
	)
	if not spends:
		return 999999
	index = max(0, int(len(spends) * 0.10) - 1)
	return spends[index]


# --- Mailchimp Sync ---

def ensure_merge_fields():
	"""Create any missing merge fields on the SG audience."""
	existing = {f["tag"] for f in get_merge_fields(SG_LIST_ID)}
	for tag, (name, field_type) in REQUIRED_MERGE_FIELDS.items():
		if tag not in existing:
			log.info("Creating merge field: %s (%s)", tag, name)
			try:
				create_merge_field(name, tag, field_type, SG_LIST_ID)
			except Exception as e:
				# 400 = already exists (race condition or case mismatch) — safe to ignore
				if "400" in str(e):
					log.info("Merge field %s already exists, skipping", tag)
				else:
					raise


def build_batch_operations(
	mc_members: dict,
	segments: dict,
) -> list[dict]:
	"""Build Mailchimp batch operations for tag and merge field updates.

	mc_members: {email: {current_tags: set}}
	segments: {email: {tags, merge_fields}}

	Returns list of batch operation dicts.
	"""
	operations = []

	skipped = 0
	for email, mc_data in mc_members.items():
		email_lower = email.lower().strip()
		seg = segments.get(email_lower)

		# Determine desired tags
		if seg:
			desired_tags = seg["tags"]
			merge_fields = seg["merge_fields"]
		else:
			# Not in Supabase — mark as prospect
			desired_tags = {"prospect"}
			merge_fields = {
				"LASTORDER": "",
				"ORDERCOUNT": "0",
				"TOTSPEND": "0",
				"LIFECYCLE": "prospect",
				"SEGTAGS": "",
			}

		current_tags = mc_data.get("current_tags", set())
		current_merge = mc_data.get("current_merge_fields", {})

		# Build tag changes (only for managed tags)
		tag_changes = []
		for tag in MANAGED_TAGS:
			if tag in desired_tags and tag not in current_tags:
				tag_changes.append({"name": tag, "status": "active"})
			elif tag not in desired_tags and tag in current_tags:
				tag_changes.append({"name": tag, "status": "inactive"})

		# Check if merge fields have changed
		merge_changed = False
		for field, value in merge_fields.items():
			if str(current_merge.get(field, "")) != str(value):
				merge_changed = True
				break

		# Skip if nothing needs updating
		if not tag_changes and not merge_changed:
			skipped += 1
			continue

		sub_hash = subscriber_hash(email)

		# Tag update operation
		if tag_changes:
			operations.append({
				"method": "POST",
				"path": f"/lists/{SG_LIST_ID}/members/{sub_hash}/tags",
				"body": json.dumps({"tags": tag_changes}),
			})

		# Merge field update operation
		if merge_changed:
			operations.append({
				"method": "PATCH",
				"path": f"/lists/{SG_LIST_ID}/members/{sub_hash}",
				"body": json.dumps({"merge_fields": merge_fields}),
			})

	log.info("Skipped %d subscribers (already up to date)", skipped)

	return operations


def submit_batches(operations: list[dict], dry_run: bool = False) -> dict:
	"""Submit operations in batches of 500, wait for each to complete."""
	total = len(operations)
	batch_size = 500
	batches_submitted = 0
	batches_completed = 0
	errors = 0
	max_retries = 3

	for i in range(0, total, batch_size):
		chunk = operations[i:i + batch_size]
		batches_submitted += 1

		if dry_run:
			log.info("[DRY RUN] Would submit batch %d (%d operations)", batches_submitted, len(chunk))
			continue

		log.info("Submitting batch %d/%d (%d operations)...",
			batches_submitted, (total + batch_size - 1) // batch_size, len(chunk))

		for attempt in range(1, max_retries + 1):
			try:
				result = submit_batch(chunk)
				batch_id = result["id"]
				status = wait_for_batch(batch_id, poll_interval=5, timeout=300)
				batches_completed += 1
				err_count = status.get("errored_operations", 0)
				errors += err_count
				if err_count:
					log.warning("Batch %s completed with %d errors", batch_id, err_count)
				else:
					log.info("Batch %s completed successfully", batch_id)
				break  # success — exit retry loop
			except Exception as e:
				if attempt < max_retries:
					wait = 10 * attempt
					log.warning("Batch %d attempt %d failed: %s — retrying in %ds",
						batches_submitted, attempt, e, wait)
					time.sleep(wait)
				else:
					log.error("Batch %d failed after %d attempts: %s",
						batches_submitted, max_retries, e)
					errors += len(chunk)

	return {
		"batches_submitted": batches_submitted,
		"batches_completed": batches_completed,
		"total_operations": total,
		"errors": errors,
	}


# --- Reporting ---

def print_summary(segments: dict, mc_members: dict, batch_result: dict | None, dry_run: bool):
	"""Print a summary of the sync."""
	total_customers = len(segments)
	matched = sum(1 for e in mc_members if e.lower().strip() in segments)

	# Count by lifecycle
	lifecycle_counts = defaultdict(int)
	for seg in segments.values():
		lifecycle_counts[seg["lifecycle"]] += 1

	# Count by interest
	interest_counts = defaultdict(int)
	for seg in segments.values():
		for tag in seg["tags"] - LIFECYCLE_TAGS:
			interest_counts[tag] += 1

	print("\n" + "=" * 60)
	print("SEGMENTATION SYNC SUMMARY")
	print("=" * 60)
	print(f"\nSupabase customers with orders:  {total_customers:,}")
	print(f"Mailchimp subscribers:           {len(mc_members):,}")
	print(f"Matched (email overlap):         {matched:,}")
	print(f"Prospects (no orders found):     {len(mc_members) - matched:,}")

	print("\n--- Lifecycle Segments ---")
	for stage in ["vip", "active", "lapsed", "dormant", "prospect"]:
		# Include MC-only prospects
		count = lifecycle_counts.get(stage, 0)
		if stage == "prospect":
			count += len(mc_members) - matched
		print(f"  {stage:12s}  {count:>6,}")

	print("\n--- Interest Tags ---")
	for tag in sorted(interest_counts.keys()):
		print(f"  {tag:15s}  {interest_counts[tag]:>6,}")

	if batch_result:
		print(f"\n--- Mailchimp Updates ---")
		print(f"  Operations:  {batch_result['total_operations']:,}")
		print(f"  Batches:     {batch_result['batches_submitted']}")
		print(f"  Errors:      {batch_result['errors']}")

	if dry_run:
		print("\n** DRY RUN — no changes pushed to Mailchimp **")

	print("=" * 60 + "\n")


def save_state(segments: dict, batch_result: dict | None):
	"""Save sync state for incremental runs."""
	os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
	state = {
		"last_sync": datetime.now(timezone.utc).isoformat(),
		"customers_processed": len(segments),
		"batch_result": batch_result,
	}
	with open(STATE_FILE, "w") as f:
		json.dump(state, f, indent=2)


def save_log(segments: dict, mc_members: dict, batch_result: dict | None, dry_run: bool):
	"""Save a log entry to the Obsidian vault."""
	os.makedirs(LOG_DIR, exist_ok=True)
	now = datetime.now()
	filename = f"segment-sync-{now.strftime('%Y-%m-%d-%H%M')}.md"

	matched = sum(1 for e in mc_members if e.lower().strip() in segments)

	lifecycle_counts = defaultdict(int)
	for seg in segments.values():
		lifecycle_counts[seg["lifecycle"]] += 1

	interest_counts = defaultdict(int)
	for seg in segments.values():
		for tag in seg["tags"] - LIFECYCLE_TAGS:
			interest_counts[tag] += 1

	lines = [
		"---",
		f'title: "Segment Sync — {now.strftime("%d %B %Y %H:%M")}"',
		f"date: {now.strftime('%d-%m-%Y')}",
		"tags:",
		"  - automation",
		"  - email-marketing",
		"  - stolen-goat",
		"type: note",
		"---",
		"",
		f"## Segment Sync {'(Dry Run) ' if dry_run else ''}— {now.strftime('%d %B %Y %H:%M')}",
		"",
		f"- Supabase customers: {len(segments):,}",
		f"- Mailchimp subscribers: {len(mc_members):,}",
		f"- Matched: {matched:,}",
		f"- Prospects: {len(mc_members) - matched:,}",
		"",
		"### Lifecycle",
		"",
		"| Stage | Count |",
		"|---|---|",
	]
	for stage in ["vip", "active", "lapsed", "dormant", "prospect"]:
		count = lifecycle_counts.get(stage, 0)
		if stage == "prospect":
			count += len(mc_members) - matched
		lines.append(f"| {stage} | {count:,} |")

	lines += [
		"",
		"### Interests",
		"",
		"| Tag | Count |",
		"|---|---|",
	]
	for tag in sorted(interest_counts.keys()):
		lines.append(f"| {tag} | {interest_counts[tag]:,} |")

	if batch_result:
		lines += [
			"",
			"### Mailchimp Updates",
			"",
			f"- Operations: {batch_result['total_operations']:,}",
			f"- Batches: {batch_result['batches_submitted']}",
			f"- Errors: {batch_result['errors']}",
		]

	filepath = os.path.join(LOG_DIR, filename)
	with open(filepath, "w", encoding="utf-8") as f:
		f.write("\n".join(lines) + "\n")
	log.info("Log saved to %s", filepath)


# --- Main ---

def main():
	parser = argparse.ArgumentParser(description="Segment SG subscribers via Supabase + Mailchimp")
	parser.add_argument("--dry-run", action="store_true", help="Analyse only, no Mailchimp writes")
	parser.add_argument("--sample", type=int, default=0, help="Process only N subscribers (for testing)")
	args = parser.parse_args()

	start_time = time.time()
	log.info("Starting segmentation sync%s", " (DRY RUN)" if args.dry_run else "")

	# 1. Connect to Supabase and build data
	log.info("Connecting to Supabase...")
	conn = get_supabase_connection()

	log.info("Building SKU lookup...")
	sku_lookup = build_sku_lookup(conn)

	log.info("Extracting customer data from orders...")
	customer_data = extract_customer_data(conn, sku_lookup)
	conn.close()

	# 2. Calculate VIP threshold and segments
	vip_threshold = calculate_vip_threshold(customer_data)
	log.info("VIP spend threshold (top 10%%): £%.0f", vip_threshold)

	segments = calculate_segments(customer_data, vip_threshold)
	log.info("Calculated segments for %d customers", len(segments))

	# 3. Ensure merge fields exist
	if not args.dry_run:
		log.info("Ensuring merge fields exist on Mailchimp...")
		ensure_merge_fields()

	# 4. Pull Mailchimp members
	log.info("Fetching Mailchimp subscriber list...")
	mc_raw = get_all_members(SG_LIST_ID)
	log.info("Fetched %d Mailchimp subscribers", len(mc_raw))

	# Build MC member dict
	mc_members = {}
	for m in mc_raw:
		email = m["email_address"]
		current_tags = {t["name"] for t in m.get("tags", [])}
		current_merge = m.get("merge_fields", {})
		mc_members[email] = {
			"current_tags": current_tags,
			"current_merge_fields": current_merge,
		}

	# Apply sample limit
	if args.sample > 0:
		limited = dict(list(mc_members.items())[:args.sample])
		mc_members = limited
		log.info("Sampling %d subscribers", len(mc_members))

	# 5. Build and submit batch operations
	log.info("Building batch operations...")
	operations = build_batch_operations(mc_members, segments)
	log.info("Built %d operations for %d subscribers", len(operations), len(mc_members))

	batch_result = None
	if operations:
		batch_result = submit_batches(operations, dry_run=args.dry_run)

	# 6. Report
	elapsed = time.time() - start_time
	log.info("Sync completed in %.1f seconds", elapsed)

	print_summary(segments, mc_members, batch_result, args.dry_run)
	save_state(segments, batch_result)
	save_log(segments, mc_members, batch_result, args.dry_run)


if __name__ == "__main__":
	main()
