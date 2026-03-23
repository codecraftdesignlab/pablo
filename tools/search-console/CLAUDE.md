# Google Search Console Integration

**Status:** ACTIVE

## Connection Details

- **Auth:** Service account (direct, no impersonation needed)
- **Service account:** pablo-766@pablo-490815.iam.gserviceaccount.com
- **Credentials:** `google-service-account-key.json` (project root, in .gitignore)
- **API:** Google Search Console API (webmasters v3)

## Sites

| Site | Description |
|---|---|
| `https://stolengoat.com/` | Stolen Goat main site |
| `sc-domain:chessfolio.io` | Chessfolio |

## How to Use

All access via Python with `googleapiclient`. Run scripts with `python -c "..."` from Bash.

### Authentication Pattern

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_FILE = 'C:/ClaudeProjects/pablo/google-service-account-key.json'
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
service = build('searchconsole', 'v1', credentials=creds)
```

**Important:** Do NOT use `.with_subject()` — direct service account auth.

### Common Queries

#### Top Search Queries (last 30 days)

```python
response = service.searchanalytics().query(
	siteUrl='https://stolengoat.com/',
	body={
		'startDate': '2026-02-21',
		'endDate': '2026-03-22',
		'dimensions': ['query'],
		'rowLimit': 25,
	}
).execute()

for row in response.get('rows', []):
	query = row['keys'][0]
	clicks = row.get('clicks', 0)
	impressions = row.get('impressions', 0)
	ctr = row.get('ctr', 0) * 100
	position = row.get('position', 0)
```

#### Queries Containing a Keyword

```python
response = service.searchanalytics().query(
	siteUrl='https://stolengoat.com/',
	body={
		'startDate': '2026-01-01',
		'endDate': '2026-03-22',
		'dimensions': ['query'],
		'dimensionFilterGroups': [{
			'filters': [{
				'dimension': 'query',
				'operator': 'contains',
				'expression': 'gilet',
			}]
		}],
		'rowLimit': 20,
	}
).execute()
```

#### Top Pages by Clicks

```python
response = service.searchanalytics().query(
	siteUrl='https://stolengoat.com/',
	body={
		'startDate': '2026-02-21',
		'endDate': '2026-03-22',
		'dimensions': ['page'],
		'rowLimit': 25,
	}
).execute()
```

#### Query Performance by Date (trend)

```python
response = service.searchanalytics().query(
	siteUrl='https://stolengoat.com/',
	body={
		'startDate': '2026-01-01',
		'endDate': '2026-03-22',
		'dimensions': ['date'],
		'dimensionFilterGroups': [{
			'filters': [{
				'dimension': 'query',
				'operator': 'contains',
				'expression': 'cycling gilet',
			}]
		}],
	}
).execute()
```

#### Queries by Device

```python
response = service.searchanalytics().query(
	siteUrl='https://stolengoat.com/',
	body={
		'startDate': '2026-02-21',
		'endDate': '2026-03-22',
		'dimensions': ['query', 'device'],
		'rowLimit': 25,
	}
).execute()
```

## Available Dimensions

| Dimension | Description |
|---|---|
| `query` | Search query text |
| `page` | URL that appeared in results |
| `device` | DESKTOP, MOBILE, TABLET |
| `country` | Country code (GBR, USA, etc.) |
| `date` | Date (for trends) |
| `searchAppearance` | How the result appeared (e.g., RICHCARD) |

## Available Metrics (per row)

| Metric | Description |
|---|---|
| `clicks` | Number of clicks from search results |
| `impressions` | Number of times URL appeared in results |
| `ctr` | Click-through rate (0.0 to 1.0, multiply by 100 for %) |
| `position` | Average position in search results (1.0 = top) |

## Filter Operators

| Operator | Description |
|---|---|
| `contains` | Query/page contains the expression |
| `equals` | Exact match |
| `notContains` | Excludes results containing expression |
| `notEquals` | Excludes exact match |

## Rules

- **Read-only** — cannot modify anything
- Data has a 2-3 day delay — the most recent data is typically 2 days old
- Always specify `startDate` and `endDate`
- Use `rowLimit` to cap results (max 25,000)
- `position` is an average — a query at position 5.3 means it typically appears around result 5-6
- CTR is returned as a decimal (0.28 = 28%) — multiply by 100 for display
