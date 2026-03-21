"""
Prospect Finder — Vault Writer
Writes prospect files to the SG Vault prospect-research directory.
"""

import re
from datetime import datetime, timezone
from pathlib import Path

from config import PROSPECTS_DIR


def _slugify(name):
	"""Convert org name to a filename slug."""
	s = name.lower().strip()
	s = re.sub(r"[^a-z0-9\s-]", "", s)
	s = re.sub(r"[\s_]+", "-", s)
	s = re.sub(r"-+", "-", s)
	return s.strip("-")


def _format_urls_yaml(urls):
	"""Format a list of URLs as YAML list items."""
	if not urls:
		return "[]"
	lines = []
	for url in urls:
		lines.append(f'  - "{url}"')
	return "\n" + "\n".join(lines)


def write_prospect(yaml_fields, markdown_sections, dedup_checker):
	"""
	Write a prospect file to the SG Vault.
	Returns the file path on success, or None if skipped.
	"""
	group_name = yaml_fields.get("group_name", "").strip()
	if not group_name:
		return None

	# Belt-and-braces dedup check
	is_dup, detail = dedup_checker.is_duplicate(
		group_name,
		website=yaml_fields.get("website"),
		email=yaml_fields.get("email"),
	)
	if is_dup:
		return None

	slug = _slugify(group_name)
	if not slug:
		return None

	filepath = PROSPECTS_DIR / f"{slug}.md"

	# Don't overwrite existing files
	if filepath.exists():
		return None

	now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
	prospect_id = "PRO-" + re.sub(r"[^A-Z0-9-]", "", slug.upper().replace("-", "-"))

	# Build frontmatter
	urls_yaml = _format_urls_yaml(yaml_fields.get("urls", []))

	frontmatter = f"""---
title: "{group_name}"
type: prospect
prospect_id: {prospect_id}
prospect_type: {yaml_fields.get("prospect_type", "unknown")}
group_name: "{group_name}"
contact_name: "{yaml_fields.get("contact_name", "")}"
website: "{yaml_fields.get("website", "")}"
urls: {urls_yaml}
phone: "{yaml_fields.get("phone", "")}"
email: "{yaml_fields.get("email", "")}"
signal_strength: {yaml_fields.get("signal_strength", 1)}
signal_type: {yaml_fields.get("signal_type", "awareness")}
discovered_at: "{now}"
discovered_by: prospect-finder
status: new
---"""

	body = f"""
## Prospect Research

**Discovered:** {now} by prospect-finder

{markdown_sections}
"""

	# Ensure output directory exists
	PROSPECTS_DIR.mkdir(parents=True, exist_ok=True)

	filepath.write_text(frontmatter + "\n" + body, encoding="utf-8")
	return filepath
