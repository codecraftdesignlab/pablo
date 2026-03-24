"""WordPress REST API wrapper for Stolen Goat.

Auth: HTTP Basic Auth with username + application password.
URL format: {site}/?rest_route=/wp/v2/...
(LiteSpeed blocks /wp-json/ pretty permalinks for WP endpoints.)
"""

import json
import requests

CREDENTIALS_FILE = "C:/ClaudeProjects/pablo/wordpress-credentials.json"

HEADERS = {"User-Agent": "Pablo/1.0"}


def _load_credentials():
	with open(CREDENTIALS_FILE, "r") as f:
		creds = json.load(f)
	return creds["site_url"], creds["wp_rest_api"]


def _base_url():
	site_url, _ = _load_credentials()
	return site_url


def _auth():
	_, wp = _load_credentials()
	return (wp["username"], wp["password"])


def _get(rest_route, params=None):
	"""GET request to WP REST API using ?rest_route= format."""
	url = _base_url()
	all_params = {"rest_route": rest_route}
	if params:
		all_params.update(params)
	resp = requests.get(url, params=all_params, auth=_auth(), headers=HEADERS, timeout=30)
	resp.raise_for_status()
	return resp


def _post(rest_route, data):
	"""POST request to WP REST API using ?rest_route= format."""
	url = _base_url()
	params = {"rest_route": rest_route}
	resp = requests.post(url, params=params, json=data, auth=_auth(), headers=HEADERS, timeout=30)
	resp.raise_for_status()
	return resp.json()


# --- Pages ---

def get_page(page_id):
	"""Fetch a single page by ID."""
	return _get(f"/wp/v2/pages/{page_id}").json()


def get_pages(per_page=10, page=1):
	"""List pages (paginated)."""
	return _get("/wp/v2/pages", {"per_page": per_page, "page": page}).json()


def find_page(slug):
	"""Find a page by its slug. Returns the page dict or None."""
	results = _get("/wp/v2/pages", {"slug": slug}).json()
	return results[0] if results else None


def update_page(page_id, **kwargs):
	"""Update a page. Common fields: title, content, excerpt, status."""
	return _post(f"/wp/v2/pages/{page_id}", kwargs)
