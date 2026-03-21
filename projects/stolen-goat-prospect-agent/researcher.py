"""
Prospect Finder — Web Search & Scraping
SerpAPI search + page fetching, with candidate extraction.
"""

import re
from html.parser import HTMLParser
from urllib.parse import urlparse

import requests

from config import SERP_API_KEY, MAX_SEARCH_RESULTS, MAX_PAGES


# ── Noise filters ────────────────────────────────────────────────────────────

# Domains to skip when extracting candidates (directories, aggregators, own site)
SKIP_DOMAINS = {
	"stolengoat.com", "www.stolengoat.com",
	"facebook.com", "twitter.com", "x.com", "instagram.com",
	"linkedin.com", "youtube.com", "reddit.com", "tiktok.com",
	"wikipedia.org", "en.wikipedia.org",
	"amazon.co.uk", "amazon.com", "ebay.co.uk", "ebay.com",
	"gov.uk", "www.gov.uk",
	"bbc.co.uk", "bbc.com",
	"google.com", "google.co.uk",
}

# Known competitor / kit supplier domains to skip
COMPETITOR_DOMAINS = {
	"impsport.com", "champsys.com", "champ-sys.com",
	"kalas.co.uk", "bioracer.com", "castelli-cycling.com",
	"rapha.cc", "assos.com",
}


# ── HTML stripper ────────────────────────────────────────────────────────────

class _HTMLStripper(HTMLParser):
	def __init__(self):
		super().__init__()
		self._parts = []
		self._skip = False

	def handle_starttag(self, tag, attrs):
		if tag in ("script", "style", "nav", "header", "footer"):
			self._skip = True

	def handle_endtag(self, tag):
		if tag in ("script", "style", "nav", "header", "footer"):
			self._skip = False

	def handle_data(self, data):
		if not self._skip:
			self._parts.append(data)

	def get_text(self):
		text = " ".join(self._parts)
		# Collapse whitespace
		text = re.sub(r"\s+", " ", text).strip()
		return text


def _strip_html(html):
	"""Convert HTML to plain text."""
	stripper = _HTMLStripper()
	try:
		stripper.feed(html)
	except Exception:
		return html
	return stripper.get_text()


# ── Budget tracker ───────────────────────────────────────────────────────────

class BudgetTracker:
	"""Tracks SerpAPI calls against a budget."""

	def __init__(self, budget):
		self.budget = budget
		self.used = 0

	@property
	def remaining(self):
		return max(0, self.budget - self.used)

	@property
	def exhausted(self):
		return self.used >= self.budget

	def use(self):
		self.used += 1


# ── Search ───────────────────────────────────────────────────────────────────

def search_web(query, budget, max_results=None):
	"""
	Search via SerpAPI. Returns list of {title, link, snippet}.
	Decrements the budget tracker.
	"""
	if budget.exhausted:
		return []

	if max_results is None:
		max_results = MAX_SEARCH_RESULTS

	budget.use()

	try:
		resp = requests.get(
			"https://serpapi.com/search",
			params={
				"q": query,
				"api_key": SERP_API_KEY,
				"engine": "google",
				"num": max_results,
				"gl": "uk",
				"hl": "en",
			},
			timeout=30,
		)
		resp.raise_for_status()
	except requests.exceptions.RequestException as e:
		print(f"  Warning: search failed ({e})")
		return []
	data = resp.json()

	results = []
	for item in data.get("organic_results", []):
		results.append({
			"title": item.get("title", ""),
			"link": item.get("link", ""),
			"snippet": item.get("snippet", ""),
		})
	return results


# ── Page fetching ────────────────────────────────────────────────────────────

def fetch_page(url, timeout=15):
	"""Fetch a URL and return plain text content. Returns None on failure."""
	try:
		resp = requests.get(
			url,
			timeout=timeout,
			headers={"User-Agent": "Mozilla/5.0 (compatible; StolenGoatResearch/1.0)"},
		)
		resp.raise_for_status()
		content_type = resp.headers.get("Content-Type", "")
		if "text/html" not in content_type and "text/plain" not in content_type:
			return None
		text = _strip_html(resp.text)
		# Truncate very long pages
		if len(text) > 15000:
			text = text[:15000] + "\n[...truncated]"
		return text
	except Exception:
		return None


def fetch_search_results(results, max_pages=None):
	"""Fetch top N result pages, returning {url: text} dict."""
	if max_pages is None:
		max_pages = MAX_PAGES
	pages = {}
	for item in results[:max_pages]:
		url = item["link"]
		domain = urlparse(url).netloc.lower().replace("www.", "")
		if domain in SKIP_DOMAINS or domain in COMPETITOR_DOMAINS:
			continue
		text = fetch_page(url)
		if text:
			pages[url] = text
	return pages


# ── Candidate extraction ────────────────────────────────────────────────────

def extract_candidates(search_results):
	"""
	From search results, extract potential org names + URLs.
	Filters out noise (directories, news, own site, competitors).
	Returns list of {name, url, snippet}.
	"""
	candidates = []
	seen_domains = set()

	for item in search_results:
		url = item.get("link", "")
		title = item.get("title", "")
		snippet = item.get("snippet", "")

		parsed = urlparse(url)
		domain = parsed.netloc.lower().replace("www.", "")

		# Skip noise
		if domain in SKIP_DOMAINS or domain in COMPETITOR_DOMAINS:
			continue

		# Skip duplicate domains
		if domain in seen_domains:
			continue
		seen_domains.add(domain)

		# Try to extract org name from title
		# Remove common suffixes like "| Home", "- Official Site", etc.
		name = re.sub(r"\s*[\|–—\-]\s*(Home|Official|Website|Site|About|Events|Contact).*$", "", title, flags=re.IGNORECASE)
		name = name.strip()

		if not name or len(name) < 3:
			continue

		candidates.append({
			"name": name,
			"url": url,
			"snippet": snippet,
		})

	return candidates
