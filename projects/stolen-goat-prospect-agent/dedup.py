"""
Prospect Finder — Deduplication
Checks candidates against all known contacts and existing prospects in the SG Vault.
"""

import re
from pathlib import Path

from config import CONTACTS_DIR, PROSPECTS_DIR, DEDUP_THRESHOLD

try:
	from rapidfuzz import fuzz
	def fuzzy_ratio(a, b):
		return fuzz.ratio(a, b)
except ImportError:
	from difflib import SequenceMatcher
	def fuzzy_ratio(a, b):
		return SequenceMatcher(None, a, b).ratio() * 100


# Words to strip when normalising org names
STRIP_WORDS = {
	"ltd", "limited", "plc", "inc", "llc", "cc", "rfc", "fc", "afc",
	"club", "charity", "trust", "foundation", "association", "society",
	"cycling", "cycle", "bike", "bicycle", "triathlon", "tri",
	"the", "of", "and", "&",
}

# Noise domains to ignore
NOISE_DOMAINS = {
	"gmail.com", "yahoo.com", "hotmail.com", "outlook.com",
	"googlemail.com", "icloud.com", "aol.com",
}


def _normalise_name(name):
	"""Lowercase, strip punctuation, remove common suffixes."""
	name = name.lower()
	name = re.sub(r"[''\".,\-–—()\[\]{}]", " ", name)
	words = [w for w in name.split() if w not in STRIP_WORDS]
	return " ".join(words).strip()


def _extract_domain(url_or_email):
	"""Extract domain from a URL or email address."""
	if not url_or_email:
		return None
	s = url_or_email.strip().lower()
	# Email
	if "@" in s and "/" not in s:
		domain = s.split("@")[1]
	else:
		# URL — strip protocol and path
		s = re.sub(r"^https?://", "", s)
		s = re.sub(r"^www\.", "", s)
		domain = s.split("/")[0].split("?")[0]
	if domain in NOISE_DOMAINS:
		return None
	return domain or None


def _parse_frontmatter(text):
	"""Extract YAML frontmatter fields from markdown text."""
	fm = {}
	match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
	if not match:
		return fm
	for line in match.group(1).splitlines():
		m = re.match(r"^(\w[\w_]*):\s*(.+)$", line)
		if m:
			key = m.group(1).strip()
			val = m.group(2).strip().strip('"').strip("'")
			fm[key] = val
	return fm


def _extract_urls(text):
	"""Find all URLs in body text."""
	return re.findall(r"https?://[^\s\)>\]\"']+", text)


class DedupChecker:
	"""Loads all contacts and existing prospects, provides duplicate checking."""

	def __init__(self):
		self.contacts = []  # list of dicts: {path, title, normalised, domains, body}
		self._load_directory(CONTACTS_DIR)
		self._load_directory(PROSPECTS_DIR)

	def _load_directory(self, directory):
		if not directory.exists():
			return
		for f in directory.glob("*.md"):
			try:
				text = f.read_text(encoding="utf-8", errors="replace")
			except OSError:
				continue
			fm = _parse_frontmatter(text)
			title = fm.get("title", f.stem.replace("-", " ").title())
			normalised = _normalise_name(title)

			# Collect domains from frontmatter fields + body URLs
			domains = set()
			for field in ("website", "email"):
				d = _extract_domain(fm.get(field, ""))
				if d:
					domains.add(d)
			# URLs in frontmatter
			for key, val in fm.items():
				if val.startswith("http"):
					d = _extract_domain(val)
					if d:
						domains.add(d)
			# URLs in body
			for url in _extract_urls(text):
				d = _extract_domain(url)
				if d:
					domains.add(d)

			self.contacts.append({
				"path": str(f.relative_to(f.parent.parent)),
				"title": title,
				"normalised": normalised,
				"domains": domains,
				"body": text.lower(),
			})

	def is_duplicate(self, org_name, website=None, email=None):
		"""
		Check if a candidate org is already known.
		Returns (is_dup: bool, detail: str | None).
		"""
		candidate_norm = _normalise_name(org_name)

		# Collect candidate domains
		candidate_domains = set()
		for val in (website, email):
			d = _extract_domain(val)
			if d:
				candidate_domains.add(d)

		best_score = 0
		best_match = None

		for contact in self.contacts:
			# Fuzzy name match
			score = fuzzy_ratio(candidate_norm, contact["normalised"])
			if score > best_score:
				best_score = score
				best_match = contact

			# Domain match — instant duplicate
			if candidate_domains and candidate_domains & contact["domains"]:
				return (True, f"domain match: {contact['path']} ({contact['title']})")

			# Body text search — check if candidate name appears in the contact body
			if len(candidate_norm) > 4 and candidate_norm in contact["body"]:
				return (True, f"mentioned in: {contact['path']} ({contact['title']})")

		if best_score >= DEDUP_THRESHOLD and best_match:
			return (True, f"name match ({best_score:.0f}%): {best_match['path']} ({best_match['title']})")

		return (False, None)
