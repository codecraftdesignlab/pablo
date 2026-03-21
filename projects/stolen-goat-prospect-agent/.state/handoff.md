# Handoff

## Last action
Reviewer audit — 2026-03-21

## Status
Review complete. Verdict: **PASS WITH NOTES**.

---

## Review — Stolen Goat Prospect Agent (Initial Build)

**Verdict:** PASS WITH NOTES

The implementation is solid, well-structured, and faithfully follows the plan. The pipeline logic is sound, deduplication is thorough, and the CLI interface covers all required flags. There are a handful of issues worth addressing before this goes into regular use -- two important, the rest minor.

---

### Spec Compliance

- [x] Deep deduplication: fuzzy name match (85% threshold) -- met
- [x] Deep deduplication: domain matching -- met
- [x] Deep deduplication: body text search -- met
- [x] SerpAPI search with budget tracking (default 20 calls) -- met
- [x] Claude evaluation producing verdict (strong/moderate/weak/reject) -- met
- [x] Claude evaluation producing structured YAML + markdown -- met
- [x] Prospect files written to `SG Vault/prospect-research/` -- met
- [x] Correct frontmatter format (type, prospect_type, signal_strength, etc.) -- met
- [x] CLI with --focus, --prospect-type, --count, --budget, --dry-run, --verbose -- met
- [x] Summary report with queries, candidates, duplicates, rejections, new prospects -- met
- [x] No hardcoded API keys -- met (loaded from pablo `.env`)
- [x] Belt-and-braces dedup before writing (double check) -- met (vault_writer.py:42)

All acceptance criteria are satisfied.

---

### Issues Found

#### Important (should fix)

1. **[Important]** `config.py:16-17` -- API keys loaded with bare `os.environ[]` will raise an unhandled `KeyError` with a cryptic traceback if the key is missing from `.env`. This is the most likely failure mode (first run, wrong .env path, missing variable). Should catch the error and provide a clear message.

   Suggested fix:
   ```python
   def _require_env(key):
       val = os.environ.get(key)
       if not val:
           raise SystemExit(f"Missing required environment variable: {key}. Check {PABLO_DIR / '.env'}")
       return val

   ANTHROPIC_API_KEY = _require_env("ANTHROPIC_API_KEY")
   SERP_API_KEY = _require_env("SERP_API_KEY")
   ```

2. **[Important]** No `requirements.txt` or `pyproject.toml`. The project imports `requests`, `anthropic`, `python-dotenv`, `pyyaml`, and optionally `rapidfuzz`. Without a dependency manifest, setting this up on a fresh machine (or after a reinstall) means guessing. This is especially relevant since Tim's MEMORY.md notes he is "new to TS/Next/Bun" -- a clear dependency list removes friction.

   Suggested fix: add a `requirements.txt`:
   ```
   requests>=2.31
   anthropic>=0.40
   python-dotenv>=1.0
   pyyaml>=6.0
   rapidfuzz>=3.0
   ```

#### Minor (nice to fix)

3. **[Minor]** `analyst.py:81` -- a new `anthropic.Anthropic()` client is instantiated on every call to `evaluate_candidate()`. For a typical run evaluating 5-10 candidates, this creates unnecessary overhead. Consider creating the client once (e.g. module-level or passed in).

4. **[Minor]** `prospect_finder.py:169` -- the deep research query is hardcoded as `'"{name}" cycling kit OR events OR club'`. If the candidate name contains double quotes or special characters, this will produce a malformed search query. A simple `name.replace('"', '')` before interpolation would be prudent.

5. **[Minor]** `vault_writer.py:61` -- the `prospect_id` generation logic `re.sub(r"[^A-Z0-9-]", "", slug.upper().replace("-", "-"))` contains a no-op replacement (`"-"` replaced with `"-"`). The intent appears to be to produce a clean ID like `PRO-ACME-CYCLING`, but the regex strips all hyphens from the slug after uppercasing, then the `replace` does nothing. The result is IDs like `PRO-ACMECYCLING` with no separators. If hyphens are desired, change the regex to `[^A-Z0-9-]` and drop the replace, or if the intent was hyphens-to-something-else, fix the replacement target.

6. **[Minor]** `researcher.py:110` -- `search_web()` calls `resp.raise_for_status()` without a try/except. A SerpAPI 429 (rate limit) or 401 (bad key) will produce an unhandled `requests.exceptions.HTTPError` that kills the entire run. Consider catching HTTP errors and returning an empty list with a warning, so one failed search does not abort the whole pipeline.

7. **[Minor]** `dedup.py:157` -- the body text search (`candidate_norm in contact["body"]`) matches substrings, which could produce false positives. For example, a candidate named "Bath" would match any contact body containing the word "bath". The `len(candidate_norm) > 4` guard helps, but a word-boundary check (e.g. `re.search(rf"\b{re.escape(candidate_norm)}\b", contact["body"])`) would be more precise.

---

### Security

- [x] No hardcoded secrets -- API keys loaded from `.env` via `dotenv`
- [x] `.env` is not committed (Pablo's `.gitignore` covers it at root level)
- [x] Input validation: URLs and names are sanitised before use
- [x] No injection vulnerabilities -- no shell commands, no SQL, file paths are constructed from slugified names
- [x] User-Agent header on HTTP requests identifies the tool (researcher.py:142) -- good practice
- [ ] **Note:** No rate limiting or backoff on API calls (SerpAPI or Anthropic). Not a security issue per se, but could lead to account-level rate limiting. Low risk given the budget cap of 20 calls.

---

### Test Coverage

- [ ] No tests exist for any module

This is an internal tool for Tim's personal use, so the absence of automated tests is understandable and not a blocker. However, if this tool is run regularly, a few smoke tests would be valuable -- particularly for `dedup.py` (the fuzzy matching and domain extraction logic) and `_parse_yaml_block` in `analyst.py` (which does hand-rolled YAML parsing that could break on unexpected Claude output).

Not blocking on this, but flagging it as a future improvement.

---

### Notes

**What was done well:**

- **Clean module separation.** Each file has a single clear responsibility. The pipeline flow (config -> dedup -> research -> analyse -> write) is easy to follow and easy to modify.
- **Thoughtful deduplication.** Three layers (fuzzy name, domain match, body text search) plus the belt-and-braces recheck in vault_writer is exactly right for avoiding duplicate outreach.
- **Budget management.** The BudgetTracker class and the discovery/deep-research budget split (prospect_finder.py:115) show good thinking about API cost control.
- **Graceful fallbacks.** The rapidfuzz/difflib fallback in dedup.py, the page truncation in researcher.py, and the snippet-only fallback when budget is exhausted are all sensible.
- **Search strategies YAML.** Externalising query templates with weight-based prioritisation is a smart design that makes it easy to tune without touching code.
- **Competitor and noise domain filtering.** The SKIP_DOMAINS and COMPETITOR_DOMAINS sets in researcher.py show domain knowledge baked into the tool.

**Observations:**

- The `__pycache__` directory is present despite the `.gitignore`. Confirm it is not tracked. The `.gitignore` looks correct (`__pycache__/`, `*.pyc`), so this is likely fine.
- The `search_strategies.yaml` references "2025 OR 2026" in several queries. These will need updating as time passes. Consider using `{year}` as a template variable alongside `{focus}`.
- The hand-rolled YAML parser in `analyst.py:109-143` is a pragmatic choice for the small structured block Claude returns, but it will break silently on edge cases (e.g. multi-line values, colons in values). Since `pyyaml` is already a dependency, consider using `yaml.safe_load()` on the extracted YAML block as a more robust alternative.

**Recommendations for future iterations:**

- Add a `--strategy` flag to select specific tier groups (e.g. only buying signals, only discovery)
- Consider logging runs to `agents/logging/` as per Pablo's default behaviours
- A `--recheck` mode that re-evaluates existing weak/moderate prospects could add value over time

---

### Summary

| Metric | Result |
|---|---|
| Spec compliance | 12/12 criteria met |
| Critical issues | 0 |
| Important issues | 2 (env error handling, missing requirements.txt) |
| Minor issues | 5 |
| Security | Clean |
| Tests | None (acceptable for internal tool) |

**Verdict: PASS WITH NOTES.** Ship it, but address the two Important issues before the first real run to avoid a frustrating first experience.
