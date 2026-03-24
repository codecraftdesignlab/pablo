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

### Bot Traffic Exclusion (MANDATORY)

**All GA4 queries for the main site MUST exclude Chinese bot traffic.** Analysis in March 2026 found that ~50% of sessions on `properties/310109076` are from a Chinese botnet (3840x2160 resolution, ~1s sessions, zero engagement). This inflates session counts and deflates conversion/engagement metrics.

Use the helper below or apply the filter manually to every query.

#### Helper: Build a bot-excluded request

```python
def exclude_bots(dimension_filter=None):
	"""Wrap an optional dimension filter with the mandatory CN exclusion.

	Returns a FilterExpression that excludes country='China'.
	If you have your own filter, it is ANDed with the exclusion.
	"""
	cn_exclude = FilterExpression(
		not_expression=FilterExpression(
			filter=Filter(
				field_name='country',
				string_filter=Filter.StringFilter(
					match_type=Filter.StringFilter.MatchType.EXACT,
					value='China',
				),
			),
		),
	)
	if dimension_filter is None:
		return cn_exclude
	return FilterExpression(
		and_group=FilterExpression.AndGroup(
			expressions=[cn_exclude, dimension_filter],
		),
	)
```

Usage — every `RunReportRequest` should include `dimension_filter=exclude_bots()`:

```python
request = RunReportRequest(
	property='properties/310109076',
	date_ranges=[DateRange(start_date='30daysAgo', end_date='today')],
	metrics=[Metric(name='sessions')],
	dimension_filter=exclude_bots(),  # Always include this
)
```

With an additional filter (e.g. product pages only):

```python
page_filter = FilterExpression(
	filter=Filter(
		field_name='pagePath',
		string_filter=Filter.StringFilter(
			match_type=Filter.StringFilter.MatchType.CONTAINS,
			value='/product/',
		),
	),
)
request = RunReportRequest(
	property='properties/310109076',
	date_ranges=[DateRange(start_date='30daysAgo', end_date='today')],
	dimensions=[Dimension(name='pagePath')],
	metrics=[Metric(name='screenPageViews')],
	dimension_filter=exclude_bots(page_filter),  # CN excluded + page filter
)
```

**When NOT to exclude:** Only skip the filter if you are specifically analysing the bot traffic itself (e.g. monitoring whether blocking is working).

### Common Queries

All examples below include bot exclusion.

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
	dimension_filter=exclude_bots(),
)
response = client.run_report(request)
```

#### Page Views by URL (e.g. product pages)

```python
page_filter = FilterExpression(
	filter=Filter(
		field_name='pagePath',
		string_filter=Filter.StringFilter(
			match_type=Filter.StringFilter.MatchType.CONTAINS,
			value='/product/',
		),
	),
)
request = RunReportRequest(
	property='properties/310109076',
	date_ranges=[DateRange(start_date='30daysAgo', end_date='today')],
	dimensions=[Dimension(name='pagePath')],
	metrics=[
		Metric(name='screenPageViews'),
		Metric(name='sessions'),
	],
	dimension_filter=exclude_bots(page_filter),
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
	dimension_filter=exclude_bots(),
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
	dimension_filter=exclude_bots(),
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
	dimension_filter=exclude_bots(),
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

- **Exclude bot traffic** — ALL queries to `properties/310109076` (main site) MUST use `exclude_bots()` to filter out Chinese bot traffic. See "Bot Traffic Exclusion" section above. The CK property (515401720) is not affected.
- **Read-only** — analytics scope is readonly, cannot modify anything
- Always specify `date_ranges` — never query without a date range
- Use `limit` to cap results — GA4 can return thousands of rows
- The CK property (515401720) will have much less traffic than the main site
- Revenue in GA4 may not match WooCommerce exactly — use WooCommerce/sg-analysis for authoritative revenue figures, GA4 for traffic and conversion behaviour
