"""
Stolen Goat Prospect Finder
Searches the web for new potential custom kit clients, evaluates them,
and writes prospect files to the SG Vault.

Usage:
  python prospect_finder.py [OPTIONS]

Options:
  --focus TEXT           Search focus (e.g. "charity cycling events Yorkshire")
  --prospect-type TYPE   charity | corporate | event | club (default: all)
  --count N             Max prospects to write per run (default: 5)
  --budget N            Max SerpAPI calls per run (default: 20)
  --dry-run             Print to console, don't write to vault
  --verbose             Show detailed progress
"""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

from config import PROSPECTS_DIR
from dedup import DedupChecker
from researcher import search_web, fetch_search_results, extract_candidates, BudgetTracker
from analyst import evaluate_candidate
from vault_writer import write_prospect


STRATEGIES_FILE = Path(__file__).parent / "search_strategies.yaml"


def load_strategies():
	"""Load search strategies from YAML config."""
	with open(STRATEGIES_FILE, encoding="utf-8") as f:
		return yaml.safe_load(f)


def select_queries(strategies, prospect_type, focus):
	"""
	Select and prepare search queries based on type and focus.
	Returns list of (query_string, weight) sorted by weight descending.
	"""
	defaults = strategies.get("defaults", {})
	tiers = strategies.get("tiers", [])

	# Determine focus terms
	if focus:
		focus_terms = [focus]
	elif prospect_type and prospect_type in defaults:
		focus_terms = defaults[prospect_type]
	else:
		# Use all defaults
		focus_terms = []
		for terms in defaults.values():
			focus_terms.extend(terms)
		# Limit to avoid explosion
		focus_terms = focus_terms[:4]

	# Filter tiers by prospect type if specified
	type_tier_map = {
		"charity": "discovery_charity",
		"corporate": "discovery_corporate",
		"event": "discovery_event",
		"club": "discovery_club",
	}

	# Build query list, replacing {focus}
	queries = []
	for tier in sorted(tiers, key=lambda t: t.get("weight", 0), reverse=True):
		weight = tier.get("weight", 1)
		tier_name = tier.get("name", "")

		# Skip general awareness tier unless budget is large
		if not focus and weight < 2:
			continue

		# If prospect type specified, skip discovery tiers for other types
		if prospect_type and tier_name.startswith("discovery_"):
			target_tier = type_tier_map.get(prospect_type)
			if target_tier and tier_name != target_tier:
				continue

		for template in tier.get("queries", []):
			for ft in focus_terms:
				q = template.replace("{focus}", ft)
				queries.append((q, weight))

	return queries


def run(args):
	"""Main pipeline."""
	now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")

	# ── Load config ──────────────────────────────────────────────────────
	strategies = load_strategies()
	queries = select_queries(strategies, args.prospect_type, args.focus)

	if args.verbose:
		print(f"Prepared {len(queries)} search queries")

	# ── Init dedup ───────────────────────────────────────────────────────
	if args.verbose:
		print("Loading vault for deduplication...")
	dedup = DedupChecker()
	if args.verbose:
		print(f"  Loaded {len(dedup.contacts)} contacts/prospects")

	# ── Search ───────────────────────────────────────────────────────────
	budget = BudgetTracker(args.budget)
	# Reserve half the budget for deep research on candidates
	discovery_limit = max(3, args.budget // 2)
	all_candidates = []
	seen_names = set()
	queries_run = 0

	for query, weight in queries:
		if budget.exhausted or budget.used >= discovery_limit:
			break

		if args.verbose:
			print(f"  Searching: {query}")

		results = search_web(query, budget)
		queries_run += 1
		candidates = extract_candidates(results)

		for c in candidates:
			name_key = c["name"].lower().strip()
			if name_key not in seen_names:
				seen_names.add(name_key)
				c["weight"] = weight
				all_candidates.append(c)

	if args.verbose:
		print(f"\nFound {len(all_candidates)} unique candidates from {queries_run} queries")

	# ── Evaluate candidates ──────────────────────────────────────────────
	prospects_written = 0
	duplicates = []
	rejected = []
	written = []

	for candidate in all_candidates:
		if prospects_written >= args.count:
			break

		name = candidate["name"]
		url = candidate["url"]
		snippet = candidate.get("snippet", "")

		if args.verbose:
			print(f"\nEvaluating: {name}")

		# Dedup check
		is_dup, detail = dedup.is_duplicate(name, website=url)
		if is_dup:
			duplicates.append((name, detail))
			if args.verbose:
				print(f"  SKIP (duplicate): {detail}")
			continue

		# Deep research — additional search on the specific org
		page_texts = {}
		if not budget.exhausted:
			safe_name = name.replace('"', '').replace("'", "")
			deep_results = search_web(f'"{safe_name}" cycling kit OR events OR club', budget)
			# Also fetch the candidate's own page
			all_results = [{"link": url, "title": name, "snippet": snippet}] + deep_results
			if not budget.exhausted:
				page_texts = fetch_search_results(all_results)
			else:
				# Budget nearly exhausted — use snippets only
				page_texts = {url: snippet}
		else:
			page_texts = {url: snippet}

		if args.verbose:
			print(f"  Fetched {len(page_texts)} pages")

		# Claude evaluation
		result = evaluate_candidate(name, url, snippet, page_texts)
		if result is None:
			if args.verbose:
				print("  SKIP (evaluation failed)")
			continue

		verdict, yaml_fields, markdown_sections = result

		if verdict == "reject":
			rejected.append((name, yaml_fields.get("signal_type", "unknown")))
			if args.verbose:
				print(f"  REJECTED: {name}")
			continue

		# Use analyst's group_name if available, else search title
		display_name = yaml_fields.get("group_name") or name

		# Write to vault
		if args.dry_run:
			print(f"\n{'='*60}")
			print(f"DRY RUN — would write: {display_name}")
			print(f"  Verdict: {verdict} | Signal: {yaml_fields.get('signal_strength', '?')}")
			print(f"  Type: {yaml_fields.get('prospect_type', '?')}")
			print(f"{'='*60}")
			prospects_written += 1
			written.append((display_name, yaml_fields.get("prospect_type", "?"), yaml_fields.get("signal_strength", "?")))
		else:
			filepath = write_prospect(yaml_fields, markdown_sections, dedup)
			if filepath:
				prospects_written += 1
				rel = filepath.relative_to(filepath.parent.parent)
				written.append((display_name, yaml_fields.get("prospect_type", "?"), yaml_fields.get("signal_strength", "?")))
				if args.verbose:
					print(f"  WROTE: {rel}")
			else:
				if args.verbose:
					print(f"  SKIP (write failed or duplicate)")

	# ── Summary report ───────────────────────────────────────────────────
	mode = "DRY RUN" if args.dry_run else "LIVE"
	print(f"\nProspect Finder [{mode}] — {now}")
	print("=" * 50)
	if args.focus:
		print(f"Focus: {args.focus} | Type: {args.prospect_type or 'all'}")
	else:
		print(f"Type: {args.prospect_type or 'all'}")

	print(f"\nSearched: {queries_run} queries, {len(all_candidates)} candidates")
	print(f"SerpAPI budget: {budget.used}/{budget.budget} used ({budget.remaining} remaining)")
	print(f"Duplicates skipped: {len(duplicates)} | Rejected: {len(rejected)}")

	if duplicates:
		print("\nDuplicates:")
		for name, detail in duplicates:
			print(f'  - "{name}" ({detail})')

	if rejected:
		print("\nRejected:")
		for name, reason in rejected:
			print(f'  - "{name}" ({reason})')

	print(f"\nNEW PROSPECTS: {len(written)}")
	if written:
		for i, (name, ptype, signal) in enumerate(written, 1):
			slug_name = name.lower().replace(" ", "-")
			print(f"  {i}. prospect-research/{slug_name}.md ({ptype}, signal: {signal})")


def main():
	parser = argparse.ArgumentParser(description="Stolen Goat Prospect Finder")
	parser.add_argument("--focus", type=str, default=None, help="Search focus text")
	parser.add_argument("--prospect-type", type=str, default=None,
		choices=["charity", "corporate", "event", "club"],
		help="Prospect type filter")
	parser.add_argument("--count", type=int, default=5, help="Max prospects per run (default: 5)")
	parser.add_argument("--budget", type=int, default=20, help="Max SerpAPI calls per run (default: 20)")
	parser.add_argument("--dry-run", action="store_true", help="Print to console, don't write")
	parser.add_argument("--verbose", action="store_true", help="Detailed progress output")
	args = parser.parse_args()

	run(args)


if __name__ == "__main__":
	main()
