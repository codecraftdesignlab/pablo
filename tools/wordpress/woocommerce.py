"""WooCommerce REST API wrapper for Stolen Goat.

Auth: query string with consumer_key + consumer_secret.
URL format: {site}/wp-json/wc/v3/...
"""

import json
import requests

CREDENTIALS_FILE = "C:/ClaudeProjects/pablo/wordpress-credentials.json"

HEADERS = {"User-Agent": "Pablo/1.0"}


def _load_credentials():
	with open(CREDENTIALS_FILE, "r") as f:
		creds = json.load(f)
	return creds["site_url"], creds["wc_rest_api"]


def _base_url():
	site_url, _ = _load_credentials()
	return f"{site_url}/wp-json/wc/v3"


def _auth_params():
	_, wc = _load_credentials()
	return {"consumer_key": wc["consumer_key"], "consumer_secret": wc["consumer_secret"]}


def _get(endpoint, params=None):
	"""GET request to WC REST API with auth."""
	url = f"{_base_url()}/{endpoint}"
	all_params = _auth_params()
	if params:
		all_params.update(params)
	resp = requests.get(url, params=all_params, headers=HEADERS, timeout=30)
	resp.raise_for_status()
	return resp


def _put(endpoint, data):
	"""PUT request to WC REST API with auth."""
	url = f"{_base_url()}/{endpoint}"
	params = _auth_params()
	resp = requests.put(url, params=params, json=data, headers=HEADERS, timeout=30)
	resp.raise_for_status()
	return resp.json()


# --- Categories ---

def get_category(category_id):
	"""Fetch a single product category by ID."""
	return _get(f"products/categories/{category_id}").json()


def get_categories(per_page=100):
	"""Fetch all product categories (handles pagination)."""
	categories = []
	page = 1
	while True:
		resp = _get("products/categories", {"per_page": per_page, "page": page})
		batch = resp.json()
		if not batch:
			break
		categories.extend(batch)
		# Check WC pagination headers
		total_pages = int(resp.headers.get("X-WP-TotalPages", 1))
		if page >= total_pages:
			break
		page += 1
	return categories


def find_category(slug):
	"""Find a category by its slug. Returns the category dict or None."""
	resp = _get("products/categories", {"slug": slug})
	results = resp.json()
	return results[0] if results else None


def update_category(category_id, **kwargs):
	"""Update a product category. Common fields: name, description, slug."""
	return _put(f"products/categories/{category_id}", kwargs)


# --- Products ---

def get_product(product_id):
	"""Fetch a single product by ID."""
	return _get(f"products/{product_id}").json()
