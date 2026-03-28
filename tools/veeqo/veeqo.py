"""Veeqo REST API wrapper for Stolen Goat.

Auth: API key in x-api-key header.
Base URL: https://api.veeqo.com/
"""

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv("C:/ClaudeProjects/sg-backend/.env")

API_KEY = os.environ["VEEQO_API_KEY"]
BASE_URL = "https://api.veeqo.com"
HEADERS = {
	"x-api-key": API_KEY,
	"Content-Type": "application/json",
	"User-Agent": "Pablo/1.0",
}

MAX_RETRIES = 3
RETRY_BACKOFF = 2


class VeeqoAPIError(Exception):
	def __init__(self, status_code, message):
		self.status_code = status_code
		self.message = message
		super().__init__(f"Veeqo API {status_code}: {message}")


def _request(method, path, json=None, params=None):
	url = f"{BASE_URL}/{path.lstrip('/')}"
	for attempt in range(MAX_RETRIES):
		resp = requests.request(
			method, url, json=json, params=params,
			headers=HEADERS, timeout=30,
		)
		remaining = resp.headers.get("X-RateLimit-Remaining")
		if remaining and int(remaining) < 5:
			reset = resp.headers.get("X-RateLimit-Reset")
			if reset:
				wait = max(0, int(reset) - int(time.time())) + 1
				time.sleep(wait)

		if resp.status_code in (429, 500, 502, 503, 504):
			wait = RETRY_BACKOFF * (2 ** attempt)
			time.sleep(wait)
			continue

		if resp.status_code >= 400:
			raise VeeqoAPIError(resp.status_code, resp.text)

		return resp.json() if resp.content else {}

	raise VeeqoAPIError(resp.status_code, f"Failed after {MAX_RETRIES} retries: {resp.text}")


def _get(path, params=None):
	return _request("GET", path, params=params)


def _post(path, data):
	return _request("POST", path, json=data)


def search_products(query: str, page: int = 1, page_size: int = 50) -> list:
	return _get("products", params={"query": query, "page": page, "page_size": page_size})


def get_product(product_id: int) -> dict:
	return _get(f"products/{product_id}")


def create_product(title: str, variants: list, **kwargs) -> dict:
	payload = {"product": {"title": title, "variants": variants, **kwargs}}
	return _post("products", payload)


def find_by_sku(sku: str) -> dict | None:
	results = search_products(sku)
	if isinstance(results, list):
		for product in results:
			for variant in product.get("sellables", []):
				if variant.get("sku_code") == sku:
					return product
	return None
