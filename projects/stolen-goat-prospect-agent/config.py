"""
Prospect Finder — Configuration
Paths, API keys, and constants.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# ── Load environment ─────────────────────────────────────────────────────────

PABLO_DIR = Path("C:/ClaudeProjects/pablo")
load_dotenv(PABLO_DIR / ".env")

def _require_env(key):
	val = os.environ.get(key)
	if not val:
		raise SystemExit(f"Missing required environment variable: {key}. Check {PABLO_DIR / '.env'}")
	return val

ANTHROPIC_API_KEY = _require_env("ANTHROPIC_API_KEY")
SERP_API_KEY = _require_env("SERP_API_KEY")

# ── Vault paths ──────────────────────────────────────────────────────────────

SG_VAULT = Path("C:/Users/timbl/stolen goat Dropbox/tim bland/SG Vault")
CONTACTS_DIR = SG_VAULT / "contacts"
PROSPECTS_DIR = SG_VAULT / "prospect-research"

# ── Constants ────────────────────────────────────────────────────────────────

DEDUP_THRESHOLD = 85
MAX_SEARCH_RESULTS = 5
MAX_PAGES = 3
CLAUDE_MODEL = "claude-sonnet-4-6"
