# Google Analytics Integration

**Status:** ACTIVE

## Connection Details

- **Auth:** Service account (direct, no impersonation needed)
- **Service account:** pablo-766@pablo-490815.iam.gserviceaccount.com
- **Credentials:** `google-service-account-key.json` (project root, in .gitignore)
- **API:** Google Analytics Data API v1beta (GA4)

## Properties

| Property | ID | Use |
|---|---|---|
| Stolen Goat (main site) | `properties/310109076` | Collection + all D2C traffic |
| Stolen Goat Custom Kit | `properties/515401720` | CK webshop traffic |

## How to Use

All GA4 access is via Python with `google-analytics-data`. Run scripts with `python -c "..."` from Bash.

### Authentication Pattern

```python
from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
	RunReportRequest, DateRange, Metric, Dimension, FilterExpression,
	Filter, OrderBy,
)

KEY_FILE = 'C:/ClaudeProjects/pablo/google-service-account-key.json'
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
client = BetaAnalyticsDataClient(credentials=creds)
```

**Important:** Do NOT use `.with_subject()` — GA4 uses direct service account auth, not domain-wide delegation.

### Common Queries

#### Sessions & Users (last 7 days)

```python
request = RunReportRequest(
	property='properties/310109076',
	date_ranges=[DateRange(start_date='7daysAgo', end_date='today')],
	metrics=[
		Metric(name='sessions'),
		Metric(name='totalUsers'),
		Metric(name='ecommercePurchases'),
	],
)
response = client.run_report(request)
```

#### Page Views by URL (e.g. product pages)

```python
request = RunReportRequest(
	property='properties/310109076',
	date_ranges=[DateRange(start_date='30daysAgo', end_date='today')],
	dimensions=[Dimension(name='pagePath')],
	metrics=[
		Metric(name='screenPageViews'),
		Metric(name='sessions'),
	],
	dimension_filter=FilterExpression(
		filter=Filter(
			field_name='pagePath',
			string_filter=Filter.StringFilter(
				match_type=Filter.StringFilter.MatchType.CONTAINS,
				value='/product/',
			),
		),
	),
	order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name='screenPageViews'), desc=True)],
	limit=50,
)
```

#### Traffic Sources

```python
request = RunReportRequest(
	property='properties/310109076',
	date_ranges=[DateRange(start_date='30daysAgo', end_date='today')],
	dimensions=[
		Dimension(name='sessionSource'),
		Dimension(name='sessionMedium'),
	],
	metrics=[
		Metric(name='sessions'),
		Metric(name='totalUsers'),
		Metric(name='ecommercePurchases'),
		Metric(name='purchaseRevenue'),
	],
	order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name='sessions'), desc=True)],
	limit=20,
)
```

#### Conversion Rate by Product Category

```python
request = RunReportRequest(
	property='properties/310109076',
	date_ranges=[DateRange(start_date='30daysAgo', end_date='today')],
	dimensions=[Dimension(name='itemCategory')],
	metrics=[
		Metric(name='itemsViewed'),
		Metric(name='itemsAddedToCart'),
		Metric(name='itemsPurchased'),
		Metric(name='itemRevenue'),
	],
	order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name='itemRevenue'), desc=True)],
	limit=30,
)
```

#### Site Search Terms

```python
request = RunReportRequest(
	property='properties/310109076',
	date_ranges=[DateRange(start_date='30daysAgo', end_date='today')],
	dimensions=[Dimension(name='searchTerm')],
	metrics=[
		Metric(name='sessions'),
	],
	order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name='sessions'), desc=True)],
	limit=30,
)
```

## Available Metrics

Key GA4 metrics for marketing analysis:

| Metric | Description |
|---|---|
| `sessions` | Total sessions |
| `totalUsers` | Unique users |
| `screenPageViews` | Page views |
| `ecommercePurchases` | Purchase transactions |
| `purchaseRevenue` | Revenue from purchases |
| `addToCarts` | Add-to-cart events |
| `itemsViewed` | Product detail views |
| `itemsAddedToCart` | Items added to cart |
| `itemsPurchased` | Items purchased |
| `itemRevenue` | Revenue by item |
| `sessionConversionRate` | Session-level conversion rate |
| `averageSessionDuration` | Avg session length |
| `bounceRate` | Single-page session rate |
| `userEngagementDuration` | Total engagement time |

## Available Dimensions

| Dimension | Description |
|---|---|
| `pagePath` | Page URL path |
| `pageTitle` | Page title |
| `sessionSource` | Traffic source (google, direct, etc.) |
| `sessionMedium` | Traffic medium (organic, cpc, email, etc.) |
| `sessionCampaignName` | Campaign name (UTM) |
| `itemName` | Product/item name |
| `itemCategory` | Product category |
| `deviceCategory` | Desktop, mobile, tablet |
| `country` | User country |
| `city` | User city |
| `searchTerm` | Site search query |
| `date` | Date (YYYYMMDD) |
| `month` | Month |
| `dayOfWeek` | Day of week |

## Rules

- **Read-only** — analytics scope is readonly, cannot modify anything
- Always specify `date_ranges` — never query without a date range
- Use `limit` to cap results — GA4 can return thousands of rows
- The CK property (515401720) will have much less traffic than the main site
- Revenue in GA4 may not match WooCommerce exactly — use WooCommerce/sg-analysis for authoritative revenue figures, GA4 for traffic and conversion behaviour
