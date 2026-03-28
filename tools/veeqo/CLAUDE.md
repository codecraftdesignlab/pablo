# Veeqo Integration

**Status:** ACTIVE

## Connection Details

- **API Key:** stored in `C:/ClaudeProjects/sg-backend/.env` as `VEEQO_API_KEY`
- **Base URL:** `https://api.veeqo.com`
- **Auth:** `x-api-key` header (not Basic Auth)
- **Wrapper:** `tools/veeqo/veeqo.py`

## How to Use

```python
import sys
sys.path.insert(0, 'C:/ClaudeProjects/pablo')
from tools.veeqo.veeqo import (
	search_products, get_product, create_product, find_by_sku,
)

# Search products
results = search_products("jersey", page=1, page_size=25)
for p in results:
	print(p["title"], [s["sku_code"] for s in p.get("sellables", [])])

# Get a single product by ID
product = get_product(12345)

# Find a product by SKU
product = find_by_sku("SG-JERSEY-BLU-M")
if product:
	print(product["title"])

# Create a product
new = create_product(
	title="Alpine Jersey - Blue",
	variants=[
		{
			"sku_code": "SG-ALP-BLU-S",
			"price": 89.99,
			"tax_rate": 20.0,
			"weight": {"value": 180, "unit": "g"},
		},
		{
			"sku_code": "SG-ALP-BLU-M",
			"price": 89.99,
			"tax_rate": 20.0,
			"weight": {"value": 190, "unit": "g"},
		},
	],
)
```

## Create Product Payload

The `create_product` function wraps the payload in `{"product": {...}}` automatically.

Required fields:
- `title` (str) — product name
- `variants` (list) — at least one variant

Variant fields:
- `sku_code` (str) — unique SKU
- `price` (float) — selling price
- `tax_rate` (float) — VAT rate (20.0 for UK standard)
- `weight` (dict) — `{"value": 180, "unit": "g"}`

Additional kwargs are passed through to the product object (e.g. `description`, `notes`).

## Error Handling

The wrapper raises `VeeqoAPIError` for non-retryable HTTP errors (4xx except 429). Retryable errors (429, 5xx) are retried up to 3 times with exponential backoff.

```python
from tools.veeqo.veeqo import VeeqoAPIError

try:
	product = get_product(99999)
except VeeqoAPIError as e:
	print(e.status_code, e.message)
```

## Rate Limits

- Veeqo applies rate limiting via `X-RateLimit-Remaining` and `X-RateLimit-Reset` headers
- The wrapper automatically pauses when fewer than 5 requests remain in the window
- 429 responses are retried with exponential backoff

## Rules

1. **Never delete products** — only create or update
2. **Check before creating** — always use `find_by_sku()` before `create_product()` to avoid duplicates
3. **Do not expose the API key** — it lives in `.env`, never log or display it
