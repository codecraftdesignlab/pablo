"""
Prospect Finder — Claude API Evaluation
Evaluates candidate organisations and produces structured prospect assessments.
"""

import re
from datetime import date

import anthropic

from config import ANTHROPIC_API_KEY, CLAUDE_MODEL


def _system_prompt():
	today = date.today().strftime("%Y-%m-%d")
	return f"""\
You are a prospect researcher for Stolen Goat, a UK company that designs and manufactures \
premium custom cycling and sports kit (jerseys, bib shorts, accessories). Your clients are \
cycling clubs, charities, corporate teams, and event organisers.

Today's date is {today}. Use this when assessing timing — if a website only shows events in \
the past with no evidence of upcoming editions, that weakens the signal (the event may have \
folded or the website may be stale). Recommendations must reference realistic future dates, \
not dates that have already passed. Stolen Goat's production lead time is approximately 10 weeks.

You are evaluating a potential new client that was found via web search. Your job is to:
1. Assess whether this organisation is a genuine prospect for custom cycling kit
2. Determine the type of prospect (charity, corporate, event, club)
3. Evaluate the strength of the buying signal
4. Extract key contact information
5. Recommend an approach

Be realistic and specific. Reject candidates that are not genuine prospects (e.g. other kit \
suppliers, news articles about cycling, organisations with no cycling connection, organisations \
outside the UK, or organisations too small to need custom kit).\
"""


def _build_user_prompt(candidate_name, candidate_url, search_snippet, page_texts):
	"""Build the user prompt with all gathered research."""
	parts = [
		f"# Candidate Organisation: {candidate_name}",
		f"**URL:** {candidate_url}",
		f"**Search snippet:** {search_snippet}",
		"",
		"## Web Research",
	]
	for url, text in page_texts.items():
		# Trim to keep within token limits
		trimmed = text[:8000] if len(text) > 8000 else text
		parts.append(f"\n### Page: {url}\n{trimmed}")

	parts.append("""
## Instructions

Based on the research above, produce your assessment in EXACTLY this format:

First, a YAML block (fenced with ```yaml):
```yaml
verdict: strong | moderate | weak | reject
prospect_type: charity | corporate | event | club
group_name: "Exact organisation name"
contact_name: "Name if found, or empty string"
website: "Primary URL"
urls:
  - "social media or other relevant URLs"
phone: "Phone if found, or empty string"
email: "Email if found, or empty string"
signal_strength: 1-5
signal_type: buying | timing | dissatisfaction | new_entrant | awareness
```

Then these markdown sections:
### Organisation Overview
### Events & Activities
### Custom Kit Opportunity
### Key Contacts
### Recommended Approach
### Signal Assessment
""")
	return "\n".join(parts)


def evaluate_candidate(candidate_name, candidate_url, search_snippet, page_texts):
	"""
	Send candidate data to Claude for evaluation.
	Returns (verdict, yaml_fields, markdown_sections) or None on failure.
	"""
	client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

	user_prompt = _build_user_prompt(candidate_name, candidate_url, search_snippet, page_texts)

	message = client.messages.create(
		model=CLAUDE_MODEL,
		max_tokens=4096,
		system=_system_prompt(),
		messages=[{"role": "user", "content": user_prompt}],
	)

	response_text = message.content[0].text

	# Parse YAML block
	yaml_match = re.search(r"```yaml\s*\n(.*?)```", response_text, re.DOTALL)
	if not yaml_match:
		return None

	yaml_fields = _parse_yaml_block(yaml_match.group(1))
	verdict = yaml_fields.get("verdict", "reject")

	# Extract markdown sections (everything after the YAML block)
	sections_start = yaml_match.end()
	markdown_sections = response_text[sections_start:].strip()

	return (verdict, yaml_fields, markdown_sections)


def _parse_yaml_block(yaml_text):
	"""Simple YAML parser for the structured fields."""
	fields = {}
	urls = []
	in_urls = False

	for line in yaml_text.splitlines():
		line = line.strip()
		if not line:
			continue

		if line.startswith("- "):
			if in_urls:
				val = line[2:].strip().strip('"').strip("'")
				if val:
					urls.append(val)
			continue

		in_urls = False
		match = re.match(r"^(\w[\w_]*):\s*(.*)$", line)
		if match:
			key = match.group(1)
			val = match.group(2).strip().strip('"').strip("'")
			if key == "urls":
				in_urls = True
				continue
			if key == "signal_strength":
				try:
					val = int(val)
				except ValueError:
					val = 1
			fields[key] = val

	fields["urls"] = urls
	return fields
