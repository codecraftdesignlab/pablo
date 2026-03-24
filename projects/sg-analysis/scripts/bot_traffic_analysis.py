"""
Bot Traffic Analysis — stolengoat.com
Queries GA4 for signals of bot/non-human traffic.
"""

import json
from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest, DateRange, Dimension, Metric,
    FilterExpression, Filter, OrderBy
)

KEY_FILE = 'C:/ClaudeProjects/pablo/google-service-account-key.json'
PROPERTY_ID = 'properties/310109076'
creds = service_account.Credentials.from_service_account_file(KEY_FILE)
client = BetaAnalyticsDataClient(credentials=creds)

DATE_RANGE = DateRange(start_date="30daysAgo", end_date="today")


def run_report(dimensions, metrics, order_by=None, limit=None):
    """Run a GA4 report and return rows as dicts."""
    dim_objs = [Dimension(name=d) for d in dimensions]
    met_objs = [Metric(name=m) for m in metrics]

    kwargs = dict(
        property=PROPERTY_ID,
        date_ranges=[DATE_RANGE],
        dimensions=dim_objs,
        metrics=met_objs,
    )
    if order_by:
        kwargs["order_bys"] = order_by
    if limit:
        kwargs["limit"] = limit

    request = RunReportRequest(**kwargs)
    response = client.run_report(request)

    rows = []
    for row in response.rows:
        d = {}
        for i, dim in enumerate(dimensions):
            d[dim] = row.dimension_values[i].value
        for i, met in enumerate(metrics):
            d[met] = row.metric_values[i].value
        rows.append(d)
    return rows


def query_1_channel_engagement():
    """Session duration / engagement by channel group."""
    print("\n=== QUERY 1: Channel Engagement ===")
    rows = run_report(
        dimensions=["sessionDefaultChannelGroup"],
        metrics=["sessions", "averageSessionDuration", "engagedSessions", "engagementRate", "bounceRate"],
        order_by=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
    )
    for r in rows:
        print(f"  {r['sessionDefaultChannelGroup']:25s} | sessions={r['sessions']:>8s} | avgDur={r['averageSessionDuration']:>10s} | engaged={r['engagedSessions']:>8s} | engRate={r['engagementRate']:>8s} | bounce={r['bounceRate']:>8s}")
    return rows


def query_2_source_medium_engagement():
    """Engagement rate by source/medium — top 50 by sessions."""
    print("\n=== QUERY 2: Source/Medium Engagement (top 50) ===")
    rows = run_report(
        dimensions=["sessionSourceMedium"],
        metrics=["sessions", "engagementRate", "averageSessionDuration", "bounceRate", "conversions"],
        order_by=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
        limit=50,
    )
    for r in rows:
        print(f"  {r['sessionSourceMedium']:45s} | sessions={r['sessions']:>8s} | engRate={r['engagementRate']:>8s} | avgDur={r['averageSessionDuration']:>10s} | bounce={r['bounceRate']:>8s} | conv={r['conversions']:>6s}")
    return rows


def query_3_browser_os():
    """Browser/OS breakdown."""
    print("\n=== QUERY 3: Browser/OS ===")
    rows = run_report(
        dimensions=["browser", "operatingSystem"],
        metrics=["sessions", "engagementRate", "bounceRate"],
        order_by=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
        limit=40,
    )
    for r in rows:
        print(f"  {r['browser']:20s} | {r['operatingSystem']:15s} | sessions={r['sessions']:>8s} | engRate={r['engagementRate']:>8s} | bounce={r['bounceRate']:>8s}")
    return rows


def query_4_screen_resolution():
    """Screen resolution breakdown — top 30."""
    print("\n=== QUERY 4: Screen Resolution ===")
    rows = run_report(
        dimensions=["screenResolution"],
        metrics=["sessions", "engagementRate"],
        order_by=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
        limit=30,
    )
    for r in rows:
        print(f"  {r['screenResolution']:20s} | sessions={r['sessions']:>8s} | engRate={r['engagementRate']:>8s}")
    return rows


def query_5_country_city():
    """Country/city distribution — top 50 by sessions."""
    print("\n=== QUERY 5: Country/City ===")
    rows = run_report(
        dimensions=["country", "city"],
        metrics=["sessions", "engagementRate", "bounceRate"],
        order_by=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
        limit=50,
    )
    for r in rows:
        print(f"  {r['country']:20s} | {r['city']:25s} | sessions={r['sessions']:>8s} | engRate={r['engagementRate']:>8s} | bounce={r['bounceRate']:>8s}")
    return rows


def query_6_hourly():
    """Hourly traffic pattern."""
    print("\n=== QUERY 6: Hourly Pattern ===")
    rows = run_report(
        dimensions=["hour"],
        metrics=["sessions", "engagementRate"],
        order_by=[OrderBy(dimension=OrderBy.DimensionOrderBy(dimension_name="hour"))],
    )
    for r in rows:
        print(f"  Hour {r['hour']:>2s} | sessions={r['sessions']:>8s} | engRate={r['engagementRate']:>8s}")
    return rows


def query_7_new_vs_returning():
    """New vs returning by channel."""
    print("\n=== QUERY 7: New vs Returning by Channel ===")
    rows = run_report(
        dimensions=["newVsReturning", "sessionDefaultChannelGroup"],
        metrics=["sessions", "engagementRate", "conversions"],
        order_by=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
    )
    for r in rows:
        print(f"  {r['newVsReturning']:10s} | {r['sessionDefaultChannelGroup']:25s} | sessions={r['sessions']:>8s} | engRate={r['engagementRate']:>8s} | conv={r['conversions']:>6s}")
    return rows


if __name__ == "__main__":
    results = {}
    results["channel_engagement"] = query_1_channel_engagement()
    results["source_medium"] = query_2_source_medium_engagement()
    results["browser_os"] = query_3_browser_os()
    results["screen_resolution"] = query_4_screen_resolution()
    results["country_city"] = query_5_country_city()
    results["hourly"] = query_6_hourly()
    results["new_vs_returning"] = query_7_new_vs_returning()

    # Save raw JSON for report generation
    with open("C:/ClaudeProjects/pablo/projects/sg-analysis/scripts/bot_analysis_raw.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n\nDone. Raw data saved to bot_analysis_raw.json")
