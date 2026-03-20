"""
Pablo — Inbox Tidy Script
Runs on a schedule to clean Gmail inbox noise.

Rules:
  NEVER TOUCH (keep unread):
    - *@stolengoat.com (from or in CC/To)
    - d.mealingbland@gmail.com
    - gtitim@gmail.com
    - codecraftdesignlab@gmail.com
    - Emails that look personal (no unsubscribe header, single sender, not bulk)

  MARK AS READ:
    - Promotions category
    - Social category (LinkedIn, etc.)
    - Automated notifications (Veeqo, Shopify, Postiz, RunThrough, etc.)
    - Newsletters with unsubscribe headers

  TRASH:
    - Known spam patterns (configurable)
"""

import sys
import io
import json
import re
import base64
from datetime import datetime, timezone

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from google.oauth2 import service_account
from googleapiclient.discovery import build

# ── Config ────────────────────────────────────────────────────────────────────

KEY_FILE = "C:/ClaudeProjects/pablo/google-service-account-key.json"
USER = "tim.bland@stolengoat.com"
SCOPES = [
	"https://www.googleapis.com/auth/gmail.modify",
]

# Senders whose emails are NEVER touched
WHITELIST_DOMAINS = [
	"stolengoat.com",
]

WHITELIST_EMAILS = [
	"d.mealingbland@gmail.com",
	"gtitim@gmail.com",
	"codecraftdesignlab@gmail.com",
]

# The user's own email — excluded from whitelist domain checks on To/Cc
# (otherwise every inbound email matches @stolengoat.com)
USER_EMAIL = "tim.bland@stolengoat.com"

# Known automated senders → mark as read (substring match on sender email)
AUTO_SENDERS = [
	"noreply@",
	"no-reply@",
	"notifications@",
	"mailer.",
	"newsletter@",
	"news@",
	"marketing@",
	"info@runthrough.co.uk",
	"noreply@mailer.veeqo.com",
	"@t.shopifyemail.com",
	"noreply@postiz.com",
	"nevo@postiz.com",
	"invitations@linkedin.com",
	"messages-noreply@linkedin.com",
	"@mail.teemill.com",
	"@newsletters.ft.",
	"noreply@news.bfi.org.uk",
	"googleaistudio-noreply@",
	"tina@endurancesportswire.com",
	"noreply@swisstransfer.com",
	"@retailsector.",
	"@flippa.com",
	"@fresh-escapes.co.uk",
	"@ebay.co.uk",
	"@ebay.com",
	"@amazon.co.uk",
	"@amazon.com",
	"@paypal.co.uk",
	"@paypal.com",
	"@pinterest.com",
	"@substack.com",
	"@linkdaddy.com",
	"@healthassured.co.uk",
	"@champ-sys.com",
	"@firelabel.co.uk",
	"britainsgotstartups.co.uk",
]

# Known spam patterns → trash (substring match on sender email)
TRASH_SENDERS = [
	# Add specific senders to auto-trash here
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def extract_email(header_value):
	"""Extract email address from a header like 'Name <email@example.com>'."""
	match = re.search(r"<([^>]+)>", header_value)
	if match:
		return match.group(1).lower()
	return header_value.strip().lower()


def extract_all_emails(headers):
	"""Get all email addresses from From, To, Cc headers."""
	emails = []
	for field in ["From", "To", "Cc"]:
		val = headers.get(field, "")
		# Handle comma-separated addresses
		for part in val.split(","):
			part = part.strip()
			if part:
				emails.append(extract_email(part))
	return emails


def get_domain(email):
	"""Extract domain from email address."""
	if "@" in email:
		return email.split("@")[1].lower()
	return ""


def is_whitelisted(headers):
	"""Check if any participant (other than the user) is whitelisted."""
	all_emails = extract_all_emails(headers)
	for email in all_emails:
		# Skip the user's own address
		if email == USER_EMAIL:
			continue
		# Check exact email match
		if email in WHITELIST_EMAILS:
			return True
		# Check domain match
		domain = get_domain(email)
		for wd in WHITELIST_DOMAINS:
			if domain == wd or domain.endswith("." + wd):
				return True
	return False


def is_auto_sender(sender_email):
	"""Check if sender matches known automated patterns."""
	for pattern in AUTO_SENDERS:
		if pattern in sender_email:
			return True
	return False


def is_trash_sender(sender_email):
	"""Check if sender matches known spam patterns."""
	for pattern in TRASH_SENDERS:
		if pattern in sender_email:
			return True
	return False


def has_unsubscribe(msg):
	"""Check if message has List-Unsubscribe header (bulk mail indicator)."""
	for header in msg.get("payload", {}).get("headers", []):
		if header["name"].lower() == "list-unsubscribe":
			return True
	return False


def looks_personal(msg, headers, sender_email):
	"""Heuristic: does this email look like it might be personal?"""
	# Has unsubscribe = bulk mail, not personal
	if has_unsubscribe(msg):
		return False
	# noreply/no-reply = not personal
	if "noreply" in sender_email or "no-reply" in sender_email:
		return False
	# Automated system addresses
	if any(x in sender_email for x in ["notifications@", "mailer.", "newsletter@", "marketing@", "digest@", "updates@", "alert@"]):
		return False
	# If we got here, it could be a real person emailing
	return True


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
	dry_run = "--dry-run" in sys.argv

	creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
	creds = creds.with_subject(USER)
	service = build("gmail", "v1", credentials=creds)

	# Fetch unread messages (up to 100 per run)
	result = service.users().messages().list(
		userId="me", q="is:unread", maxResults=100
	).execute()
	messages = result.get("messages", [])

	if not messages:
		print("Inbox tidy: no unread messages. Nothing to do.")
		return

	stats = {"skipped_whitelist": 0, "skipped_personal": 0, "marked_read": 0, "trashed": 0, "total": len(messages)}
	actions_log = []

	for m in messages:
		msg = service.users().messages().get(
			userId="me", id=m["id"], format="metadata",
			metadataHeaders=["From", "To", "Cc", "Subject", "Date", "List-Unsubscribe"]
		).execute()

		headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
		labels = msg.get("labelIds", [])
		sender = headers.get("From", "")
		sender_email = extract_email(sender)
		subject = headers.get("Subject", "(no subject)")

		# ── Rule 1: Whitelist — never touch ──
		if is_whitelisted(headers):
			stats["skipped_whitelist"] += 1
			continue

		# ── Rule 2: Trash senders ──
		if is_trash_sender(sender_email):
			if not dry_run:
				service.users().messages().trash(userId="me", id=m["id"]).execute()
			stats["trashed"] += 1
			actions_log.append(f"TRASHED: {sender_email} — {subject[:60]}")
			continue

		# ── Rule 3: Promotions / Social categories → mark read ──
		if "CATEGORY_PROMOTIONS" in labels or "CATEGORY_SOCIAL" in labels:
			if not dry_run:
				service.users().messages().modify(
					userId="me", id=m["id"],
					body={"removeLabelIds": ["UNREAD"]}
				).execute()
			cat = "PROMO" if "CATEGORY_PROMOTIONS" in labels else "SOCIAL"
			stats["marked_read"] += 1
			actions_log.append(f"READ [{cat}]: {sender_email} — {subject[:60]}")
			continue

		# ── Rule 4: Known automated senders → mark read ──
		if is_auto_sender(sender_email):
			if not dry_run:
				service.users().messages().modify(
					userId="me", id=m["id"],
					body={"removeLabelIds": ["UNREAD"]}
				).execute()
			stats["marked_read"] += 1
			actions_log.append(f"READ [AUTO]: {sender_email} — {subject[:60]}")
			continue

		# ── Rule 5: Has unsubscribe header (bulk) but not caught above → mark read ──
		if has_unsubscribe(msg):
			if not dry_run:
				service.users().messages().modify(
					userId="me", id=m["id"],
					body={"removeLabelIds": ["UNREAD"]}
				).execute()
			stats["marked_read"] += 1
			actions_log.append(f"READ [BULK]: {sender_email} — {subject[:60]}")
			continue

		# ── Rule 6: Looks personal → don't touch ──
		if looks_personal(msg, headers, sender_email):
			stats["skipped_personal"] += 1
			actions_log.append(f"KEPT (personal?): {sender_email} — {subject[:60]}")
			continue

		# ── Fallback: anything else → mark read ──
		if not dry_run:
			service.users().messages().modify(
				userId="me", id=m["id"],
				body={"removeLabelIds": ["UNREAD"]}
			).execute()
		stats["marked_read"] += 1
		actions_log.append(f"READ [OTHER]: {sender_email} — {subject[:60]}")

	# ── Report ────────────────────────────────────────────────────────────────
	mode = "DRY RUN" if dry_run else "LIVE"
	timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
	print(f"Inbox tidy [{mode}] — {timestamp}")
	print(f"  Processed: {stats['total']}")
	print(f"  Kept (whitelist): {stats['skipped_whitelist']}")
	print(f"  Kept (personal): {stats['skipped_personal']}")
	print(f"  Marked read: {stats['marked_read']}")
	print(f"  Trashed: {stats['trashed']}")

	if actions_log:
		print()
		for line in actions_log:
			print(f"  {line}")


if __name__ == "__main__":
	main()
