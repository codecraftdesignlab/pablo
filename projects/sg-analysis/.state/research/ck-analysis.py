"""Custom Kit Performance Deep Dive — TASK-014

Standalone analysis script. Loads orders, operational SKUs, and articles
data, filters to CK line items only, and produces findings across five
analysis areas: project performance, webshop performance, growth trends,
gender & article analysis, and discount patterns.

Revenue is always ex-VAT (total - total_tax at line-item level).
"""

import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATA_ROOT = Path(
	r"C:\Users\timbl\stolen goat Dropbox\tim bland"
	r"\Stolen Goat\Multichannel Manager\Tools"
	r"\SkynetPowerDash\Repository"
)

EXCLUDED_ORDER_STATUSES = [
	"cancelled",
	"refunded",
	"pending_payment",
	"pending",
	"on-hold",
	"internal",
	"failed",
	"trash",
	"draft",
]

CATEGORY_NORMALISATION = {
	"GILET": "GILETS",
	"HEAD AND NECK": "HEAD & NECK",
	"SPEED & TRISUITS": "SPEED & TRI SUITS",
	"Bib Shorts": "BIB SHORTS",
	"Jersey": "JERSEYS & TOPS",
	"Jacket": "JACKETS",
	"JACKET": "JACKETS",
	"Accessories": "ACCESSORIES",
	"Nutrition": "NUTRITION",
	"Swim Caps": "HEAD & NECK",
	"Cycling Caps": "HEAD & NECK",
	"CYCLING CAPS": "HEAD & NECK",
	"T-Shirt": "JERSEYS & TOPS",
	"SS JERSEYS": "JERSEYS & TOPS",
	"RACE SUITS": "SPEED & TRI SUITS",
	"SHORTS": "BIB SHORTS",
	"TIGHTS": "BIB-TIGHTS AND TROUSERS",
	"BAGS": "BAGS & PANNIERS",
	"GLASSES & GOGGLES": "EYEWEAR",
	"ARM / LEG WARMERS": "ARM & LEG WARMERS",
}

DISCOUNT_THRESHOLD = 0.20  # >20% = clearance

NOW = datetime.now()
TODAY = NOW.date()

# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------

def load_json(path: Path) -> list:
	"""Load a JSON file and return the parsed list."""
	with open(path, "r", encoding="utf-8") as f:
		return json.load(f)


def parse_date(date_str: str) -> datetime | None:
	"""Parse a WooCommerce date string, stripping trailing Z."""
	if not date_str:
		return None
	date_str = date_str.rstrip("Z")
	try:
		return datetime.fromisoformat(date_str)
	except (ValueError, TypeError):
		return None


def normalise_category(cat: str) -> str:
	"""Normalise a category name using the standard mapping."""
	if not cat:
		return "UNCATEGORISED"
	return CATEGORY_NORMALISATION.get(cat, cat)


def is_webshop_order(order: dict) -> bool:
	"""Classify an order as webshop or non-webshop.

	Webshop = has a non-empty transaction_id OR order number starts with 'GE'.
	"""
	txn = order.get("transaction_id", "") or ""
	number = str(order.get("number", ""))
	return bool(txn) or number.startswith("GE")


def ex_vat(total, total_tax) -> float:
	"""Calculate ex-VAT revenue."""
	return float(total or 0) - float(total_tax or 0)


def discount_pct(subtotal, total) -> float:
	"""Calculate discount percentage."""
	s = float(subtotal or 0)
	t = float(total or 0)
	if s <= 0:
		return 0.0
	return max(0.0, (s - t) / s)


def is_clearance(subtotal, total) -> bool:
	"""Check if a line item is clearance (>20% discount)."""
	return discount_pct(subtotal, total) > DISCOUNT_THRESHOLD


# ---------------------------------------------------------------------------
# Build SKU lookup from operationalSkus.json
# ---------------------------------------------------------------------------

def build_sku_lookup(skus_data: list) -> dict:
	"""Build a dict mapping SKU -> {designName, articleNumber, category, gender, supplier}."""
	lookup = {}
	for s in skus_data:
		sku = s.get("sku", "")
		if not sku:
			continue
		lookup[sku] = {
			"designName": (s.get("designName") or "").strip(),
			"articleNumber": s.get("articleNumber", ""),
			"category": normalise_category(s.get("category", "")),
			"gender": (s.get("gender") or "UNKNOWN").strip(),
			"supplier": (s.get("supplier") or "").strip(),
			"label": (s.get("label") or "").strip(),
			"product_id": s.get("product_id", 0),
		}
	return lookup


# ---------------------------------------------------------------------------
# Extract CK line items
# ---------------------------------------------------------------------------

def extract_ck_line_items(orders_data: list, sku_lookup: dict) -> list:
	"""Extract all CK line items from valid orders.

	Returns a list of dicts with enriched fields.
	"""
	items = []
	for order in orders_data:
		status = order.get("status")
		if status in EXCLUDED_ORDER_STATUSES or status is None:
			continue

		order_date = parse_date(order.get("date_created", ""))
		if order_date is None:
			continue

		order_id = order.get("id")
		order_number = str(order.get("number", ""))
		webshop = is_webshop_order(order)

		for li in order.get("line_items", []):
			sku = str(li.get("sku") or "")
			if not sku.startswith("CK"):
				continue

			revenue = ex_vat(li.get("total"), li.get("total_tax"))
			subtotal = float(li.get("subtotal") or 0)
			total = float(li.get("total") or 0)
			quantity = int(li.get("quantity") or 0)

			# Enrich from SKU lookup
			sku_info = sku_lookup.get(sku, {})
			design_name = sku_info.get("designName", "")
			article_number = sku_info.get("articleNumber", "")
			category = sku_info.get("category", "UNCATEGORISED")
			gender = sku_info.get("gender", "UNKNOWN")

			# If no designName from SKU lookup, try to extract project from product name
			product_name = li.get("name", "")
			if not design_name:
				design_name = _extract_project_from_name(product_name)

			items.append({
				"order_id": order_id,
				"order_number": order_number,
				"order_date": order_date,
				"is_webshop": webshop,
				"sku": sku,
				"product_id": li.get("product_id", 0),
				"product_name": product_name,
				"design_name": design_name if design_name else "UNKNOWN PROJECT",
				"article_number": article_number,
				"category": category if category else "UNCATEGORISED",
				"gender": gender,
				"revenue": revenue,
				"subtotal": subtotal,
				"total": total,
				"quantity": quantity,
				"is_clearance": is_clearance(subtotal, total),
				"discount_pct": discount_pct(subtotal, total),
			})

	return items


def _extract_project_from_name(name: str) -> str:
	"""Try to extract a project/club name from a product name.

	CK product names typically follow patterns like:
	- 'Mens Chase The Sun Ibex Everyday SS Jersey - XL'
	- 'Chase The Sun Printed Socks - S'
	- 'MENS GOATS & GORILLAS CC IBEX BODYLINE GILET M'

	We strip gender prefixes, size suffixes, and known garment types.
	"""
	if not name:
		return ""

	# Remove size suffix (after last ' - ')
	if " - " in name:
		name = name.rsplit(" - ", 1)[0]

	# Remove gender prefix
	lower = name.lower()
	for prefix in ["new mens ", "new womens ", "mens ", "womens ", "unisex ", "mens's ", "women's "]:
		if lower.startswith(prefix):
			name = name[len(prefix):]
			lower = name.lower()
			break

	# Remove known garment type suffixes (working backwards)
	garment_types = [
		"ibex everyday ss jersey", "ibex bodyline ss jersey",
		"ibex advanced ss jersey", "ibex everyday ls jersey",
		"ibex bodyline ls jersey", "ibex advanced ls jersey",
		"ibex bodyline gilet", "ibex everyday gilet",
		"alpine advanced jacket", "thermal arm warmers",
		"thermal leg warmers", "printed socks",
		"cycling cap", "bandido", "run singlet",
		"run top", "contrast hoodie", "t shirt",
		"ibex everyday ss road race suit",
		"ibex advanced ss road race suit",
		"ibex bodyline bib shorts",
		"ibex everyday bib shorts",
		"mtb ss jersey", "adventure caddy",
	]
	lower = name.lower().strip()
	for gt in sorted(garment_types, key=len, reverse=True):
		if lower.endswith(gt):
			name = name[:len(name) - len(gt)].strip()
			break

	return name.strip()


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------

def fmt_gbp(amount: float) -> str:
	"""Format a GBP amount."""
	return f"\u00a3{amount:,.2f}"


def fmt_pct(value: float) -> str:
	"""Format a percentage."""
	return f"{value:.1f}%"


def part1_project_performance(items: list, output: list):
	"""Part 1: CK Project Performance."""
	output.append("## Part 1: CK Project Performance\n")

	# Group by design_name (project)
	projects = defaultdict(lambda: {
		"revenue": 0.0,
		"orders": set(),
		"order_dates": set(),
		"first_date": None,
		"last_date": None,
		"quantity": 0,
	})

	for item in items:
		proj = projects[item["design_name"]]
		proj["revenue"] += item["revenue"]
		proj["orders"].add(item["order_id"])
		proj["order_dates"].add(item["order_date"].date())
		proj["quantity"] += item["quantity"]
		d = item["order_date"]
		if proj["first_date"] is None or d < proj["first_date"]:
			proj["first_date"] = d
		if proj["last_date"] is None or d > proj["last_date"]:
			proj["last_date"] = d

	# Top 20 by revenue
	sorted_projects = sorted(projects.items(), key=lambda x: x[1]["revenue"], reverse=True)

	output.append("### 1.1 Top 20 Projects by Revenue\n")
	output.append("| # | Project | Revenue (ex-VAT) | Orders | Unique Order Dates | Units | First Order | Last Order | AOV |")
	output.append("|---|---------|-----------------|--------|-------------------|-------|-------------|------------|-----|")

	for i, (name, data) in enumerate(sorted_projects[:20], 1):
		order_count = len(data["orders"])
		aov = data["revenue"] / order_count if order_count > 0 else 0
		output.append(
			f"| {i} | {name} | {fmt_gbp(data['revenue'])} | {order_count} | "
			f"{len(data['order_dates'])} | {data['quantity']} | "
			f"{data['first_date'].strftime('%Y-%m-%d')} | {data['last_date'].strftime('%Y-%m-%d')} | "
			f"{fmt_gbp(aov)} |"
		)

	total_revenue = sum(d["revenue"] for d in projects.values())
	top5_revenue = sum(d["revenue"] for _, d in sorted_projects[:5])
	top10_revenue = sum(d["revenue"] for _, d in sorted_projects[:10])
	top20_revenue = sum(d["revenue"] for _, d in sorted_projects[:20])
	output.append(f"\nTotal CK projects: {len(projects)}")
	output.append(f"Total CK revenue (ex-VAT): {fmt_gbp(total_revenue)}")
	output.append(f"Top 5 projects: {fmt_gbp(top5_revenue)} ({fmt_pct(top5_revenue / total_revenue * 100 if total_revenue else 0)})")
	output.append(f"Top 10 projects: {fmt_gbp(top10_revenue)} ({fmt_pct(top10_revenue / total_revenue * 100 if total_revenue else 0)})")
	output.append(f"Top 20 projects: {fmt_gbp(top20_revenue)} ({fmt_pct(top20_revenue / total_revenue * 100 if total_revenue else 0)})")

	# Project health: >3 orders, compare recent 90d vs prior 90d
	output.append("\n### 1.2 Project Health (Projects with >3 Orders)\n")

	cutoff_recent = NOW - timedelta(days=90)
	cutoff_prior = NOW - timedelta(days=180)

	healthy_projects = []
	for name, data in sorted_projects:
		if len(data["orders"]) <= 3:
			continue

		# Calculate recent vs prior revenue
		recent_rev = 0.0
		prior_rev = 0.0
		for item in items:
			if item["design_name"] != name:
				continue
			if item["order_date"] >= cutoff_recent:
				recent_rev += item["revenue"]
			elif item["order_date"] >= cutoff_prior:
				prior_rev += item["revenue"]

		if prior_rev > 0:
			growth = (recent_rev - prior_rev) / prior_rev * 100
		elif recent_rev > 0:
			growth = float("inf")
		else:
			growth = 0.0

		status = "Growing" if growth > 10 else ("Declining" if growth < -10 else "Stable")
		healthy_projects.append((name, data, recent_rev, prior_rev, growth, status))

	# Sort: growing first, then stable, then declining
	status_order = {"Growing": 0, "Stable": 1, "Declining": 2}
	healthy_projects.sort(key=lambda x: (status_order.get(x[5], 3), -x[2]))

	output.append("| Project | Total Revenue | Orders | Recent 90d | Prior 90d | Growth | Status |")
	output.append("|---------|--------------|--------|-----------|----------|--------|--------|")

	for name, data, recent_rev, prior_rev, growth, status in healthy_projects:
		growth_str = f"{growth:+.1f}%" if growth != float("inf") else "NEW"
		output.append(
			f"| {name} | {fmt_gbp(data['revenue'])} | {len(data['orders'])} | "
			f"{fmt_gbp(recent_rev)} | {fmt_gbp(prior_rev)} | {growth_str} | {status} |"
		)

	growing = sum(1 for _, _, _, _, _, s in healthy_projects if s == "Growing")
	declining = sum(1 for _, _, _, _, _, s in healthy_projects if s == "Declining")
	stable = sum(1 for _, _, _, _, _, s in healthy_projects if s == "Stable")
	output.append(f"\nProjects with >3 orders: {len(healthy_projects)}")
	output.append(f"Growing: {growing} | Stable: {stable} | Declining: {declining}")

	# New projects (first order in last 90 days)
	output.append("\n### 1.3 New Projects (First Order in Last 90 Days)\n")

	new_projects = [
		(name, data) for name, data in sorted_projects
		if data["first_date"] >= cutoff_recent
	]
	new_projects.sort(key=lambda x: x[1]["revenue"], reverse=True)

	output.append("| # | Project | Revenue | Orders | Units | First Order |")
	output.append("|---|---------|---------|--------|-------|-------------|")

	for i, (name, data) in enumerate(new_projects[:30], 1):
		output.append(
			f"| {i} | {name} | {fmt_gbp(data['revenue'])} | {len(data['orders'])} | "
			f"{data['quantity']} | {data['first_date'].strftime('%Y-%m-%d')} |"
		)

	output.append(f"\nNew projects in last 90 days: {len(new_projects)}")
	new_rev = sum(d["revenue"] for _, d in new_projects)
	output.append(f"Revenue from new projects: {fmt_gbp(new_rev)} ({fmt_pct(new_rev / total_revenue * 100 if total_revenue else 0)} of CK total)")
	output.append("")


def part2_webshop_performance(items: list, output: list):
	"""Part 2: Webshop Performance."""
	output.append("## Part 2: Webshop Performance\n")

	ws_items = [i for i in items if i["is_webshop"]]
	nws_items = [i for i in items if not i["is_webshop"]]

	ws_revenue = sum(i["revenue"] for i in ws_items)
	nws_revenue = sum(i["revenue"] for i in nws_items)
	total_revenue = ws_revenue + nws_revenue

	ws_orders = len(set(i["order_id"] for i in ws_items))
	nws_orders = len(set(i["order_id"] for i in nws_items))

	ws_aov = ws_revenue / ws_orders if ws_orders > 0 else 0
	nws_aov = nws_revenue / nws_orders if nws_orders > 0 else 0

	ws_units = sum(i["quantity"] for i in ws_items)
	nws_units = sum(i["quantity"] for i in nws_items)

	output.append("### 2.1 Webshop vs Non-Webshop Overview\n")
	output.append("| Metric | Webshop | Non-Webshop | Total |")
	output.append("|--------|---------|-------------|-------|")
	output.append(f"| Revenue (ex-VAT) | {fmt_gbp(ws_revenue)} | {fmt_gbp(nws_revenue)} | {fmt_gbp(total_revenue)} |")
	output.append(f"| Revenue Share | {fmt_pct(ws_revenue / total_revenue * 100 if total_revenue else 0)} | {fmt_pct(nws_revenue / total_revenue * 100 if total_revenue else 0)} | 100.0% |")
	output.append(f"| Orders | {ws_orders} | {nws_orders} | {ws_orders + nws_orders} |")
	output.append(f"| Units | {ws_units} | {nws_units} | {ws_units + nws_units} |")
	output.append(f"| AOV | {fmt_gbp(ws_aov)} | {fmt_gbp(nws_aov)} | {fmt_gbp(total_revenue / (ws_orders + nws_orders) if (ws_orders + nws_orders) > 0 else 0)} |")

	# Webshop project performance
	output.append("\n### 2.2 Webshop Project Performance\n")

	ws_projects = defaultdict(lambda: {"revenue": 0.0, "orders": set(), "quantity": 0})
	for item in ws_items:
		proj = ws_projects[item["design_name"]]
		proj["revenue"] += item["revenue"]
		proj["orders"].add(item["order_id"])
		proj["quantity"] += item["quantity"]

	sorted_ws = sorted(ws_projects.items(), key=lambda x: x[1]["revenue"], reverse=True)

	output.append("| # | Project | Webshop Revenue | Orders | Units | AOV |")
	output.append("|---|---------|----------------|--------|-------|-----|")

	for i, (name, data) in enumerate(sorted_ws[:20], 1):
		order_count = len(data["orders"])
		aov = data["revenue"] / order_count if order_count > 0 else 0
		output.append(
			f"| {i} | {name} | {fmt_gbp(data['revenue'])} | {order_count} | "
			f"{data['quantity']} | {fmt_gbp(aov)} |"
		)

	output.append(f"\nTotal webshop projects: {len(ws_projects)}")

	# Webshop growth trend: YTD vs prior year
	output.append("\n### 2.3 Webshop Growth Trend (YTD vs Prior Year)\n")

	current_year = NOW.year
	prior_year = current_year - 1
	ytd_cutoff_month = NOW.month
	ytd_cutoff_day = NOW.day

	ws_ytd_rev = 0.0
	ws_prior_rev = 0.0
	nws_ytd_rev = 0.0
	nws_prior_rev = 0.0

	for item in items:
		yr = item["order_date"].year
		mn = item["order_date"].month
		dy = item["order_date"].day

		if yr == current_year:
			if item["is_webshop"]:
				ws_ytd_rev += item["revenue"]
			else:
				nws_ytd_rev += item["revenue"]
		elif yr == prior_year and (mn < ytd_cutoff_month or (mn == ytd_cutoff_month and dy <= ytd_cutoff_day)):
			if item["is_webshop"]:
				ws_prior_rev += item["revenue"]
			else:
				nws_prior_rev += item["revenue"]

	total_ytd = ws_ytd_rev + nws_ytd_rev
	total_prior = ws_prior_rev + nws_prior_rev

	ws_ytd_share = ws_ytd_rev / total_ytd * 100 if total_ytd else 0
	ws_prior_share = ws_prior_rev / total_prior * 100 if total_prior else 0

	ws_growth = (ws_ytd_rev - ws_prior_rev) / ws_prior_rev * 100 if ws_prior_rev else float("inf")
	nws_growth = (nws_ytd_rev - nws_prior_rev) / nws_prior_rev * 100 if nws_prior_rev else float("inf")

	output.append(f"| Metric | {current_year} YTD | {prior_year} LfL | Growth |")
	output.append("|--------|----------|----------|--------|")

	ws_growth_str = f"{ws_growth:+.1f}%" if ws_growth != float("inf") else "N/A"
	nws_growth_str = f"{nws_growth:+.1f}%" if nws_growth != float("inf") else "N/A"

	output.append(f"| Webshop Revenue | {fmt_gbp(ws_ytd_rev)} | {fmt_gbp(ws_prior_rev)} | {ws_growth_str} |")
	output.append(f"| Non-Webshop Revenue | {fmt_gbp(nws_ytd_rev)} | {fmt_gbp(nws_prior_rev)} | {nws_growth_str} |")
	output.append(f"| Webshop Share | {fmt_pct(ws_ytd_share)} | {fmt_pct(ws_prior_share)} | {fmt_pct(ws_ytd_share - ws_prior_share)} pts |")
	output.append("")


def part3_growth_trends(items: list, output: list):
	"""Part 3: CK Growth Trends."""
	output.append("## Part 3: CK Growth Trends\n")

	current_year = NOW.year
	prior_year = current_year - 1
	ytd_cutoff_month = NOW.month
	ytd_cutoff_day = NOW.day

	# YoY growth
	ytd_rev = 0.0
	prior_lfl_rev = 0.0
	prior_full_rev = 0.0

	for item in items:
		yr = item["order_date"].year
		mn = item["order_date"].month
		dy = item["order_date"].day

		if yr == current_year:
			ytd_rev += item["revenue"]
		elif yr == prior_year:
			prior_full_rev += item["revenue"]
			if mn < ytd_cutoff_month or (mn == ytd_cutoff_month and dy <= ytd_cutoff_day):
				prior_lfl_rev += item["revenue"]

	yoy_growth = (ytd_rev - prior_lfl_rev) / prior_lfl_rev * 100 if prior_lfl_rev else float("inf")

	output.append("### 3.1 Year-on-Year Growth\n")
	yoy_str = f"{yoy_growth:+.1f}%" if yoy_growth != float("inf") else "N/A"
	output.append(f"| Metric | {current_year} YTD | {prior_year} LfL (Jan-{NOW.strftime('%b')} {ytd_cutoff_day}) | {prior_year} Full Year | YoY Growth (LfL) |")
	output.append("|--------|----------|----------|----------|----------|")
	output.append(f"| CK Revenue (ex-VAT) | {fmt_gbp(ytd_rev)} | {fmt_gbp(prior_lfl_rev)} | {fmt_gbp(prior_full_rev)} | {yoy_str} |")

	# Monthly trend
	output.append("\n### 3.2 Monthly Revenue Trend\n")

	monthly = defaultdict(lambda: {"revenue": 0.0, "orders": set(), "quantity": 0, "new_projects": set()})
	project_first_month = {}

	for item in items:
		key = item["order_date"].strftime("%Y-%m")
		monthly[key]["revenue"] += item["revenue"]
		monthly[key]["orders"].add(item["order_id"])
		monthly[key]["quantity"] += item["quantity"]

		proj = item["design_name"]
		if proj not in project_first_month or key < project_first_month[proj]:
			project_first_month[proj] = key

	# Tag new projects per month
	for proj, first_month in project_first_month.items():
		if first_month in monthly:
			monthly[first_month]["new_projects"].add(proj)

	sorted_months = sorted(monthly.keys())

	output.append("| Month | Revenue (ex-VAT) | Orders | Units | New Projects |")
	output.append("|-------|-----------------|--------|-------|--------------|")

	for month in sorted_months:
		data = monthly[month]
		output.append(
			f"| {month} | {fmt_gbp(data['revenue'])} | {len(data['orders'])} | "
			f"{data['quantity']} | {len(data['new_projects'])} |"
		)

	# New project acquisition rate
	output.append("\n### 3.3 New Project Acquisition Rate\n")

	output.append("| Month | New Projects | Cumulative Projects |")
	output.append("|-------|-------------|-------------------|")

	cumulative = 0
	for month in sorted_months:
		new = len(monthly[month]["new_projects"])
		cumulative += new
		output.append(f"| {month} | {new} | {cumulative} |")

	output.append(f"\nTotal unique projects: {len(project_first_month)}")

	# Revenue concentration
	output.append("\n### 3.4 Revenue Concentration\n")

	project_revenues = defaultdict(float)
	for item in items:
		project_revenues[item["design_name"]] += item["revenue"]

	total_rev = sum(project_revenues.values())
	sorted_rev = sorted(project_revenues.values(), reverse=True)

	top5 = sum(sorted_rev[:5]) if len(sorted_rev) >= 5 else sum(sorted_rev)
	top10 = sum(sorted_rev[:10]) if len(sorted_rev) >= 10 else sum(sorted_rev)
	top20 = sum(sorted_rev[:20]) if len(sorted_rev) >= 20 else sum(sorted_rev)

	output.append("| Metric | Revenue | % of Total |")
	output.append("|--------|---------|-----------|")
	output.append(f"| Top 5 projects | {fmt_gbp(top5)} | {fmt_pct(top5 / total_rev * 100 if total_rev else 0)} |")
	output.append(f"| Top 10 projects | {fmt_gbp(top10)} | {fmt_pct(top10 / total_rev * 100 if total_rev else 0)} |")
	output.append(f"| Top 20 projects | {fmt_gbp(top20)} | {fmt_pct(top20 / total_rev * 100 if total_rev else 0)} |")
	output.append(f"| All {len(project_revenues)} projects | {fmt_gbp(total_rev)} | 100.0% |")

	# Herfindahl index for concentration
	if total_rev > 0:
		shares = [r / total_rev for r in sorted_rev]
		hhi = sum(s * s for s in shares)
		output.append(f"\nHerfindahl-Hirschman Index (HHI): {hhi:.4f} (lower = more diversified; 1.0 = single project)")
	output.append("")


def part4_gender_article(items: list, sku_lookup: dict, articles_data: list, output: list):
	"""Part 4: Gender & Article Analysis."""
	output.append("## Part 4: Gender & Article Analysis\n")

	current_year = NOW.year
	prior_year = current_year - 1
	ytd_cutoff_month = NOW.month
	ytd_cutoff_day = NOW.day

	# Gender split
	output.append("### 4.1 Gender Split\n")

	gender_data = defaultdict(lambda: {"revenue": 0.0, "quantity": 0, "ytd_rev": 0.0, "prior_rev": 0.0})

	for item in items:
		g = item["gender"]
		gender_data[g]["revenue"] += item["revenue"]
		gender_data[g]["quantity"] += item["quantity"]

		yr = item["order_date"].year
		mn = item["order_date"].month
		dy = item["order_date"].day

		if yr == current_year:
			gender_data[g]["ytd_rev"] += item["revenue"]
		elif yr == prior_year and (mn < ytd_cutoff_month or (mn == ytd_cutoff_month and dy <= ytd_cutoff_day)):
			gender_data[g]["prior_rev"] += item["revenue"]

	total_rev = sum(d["revenue"] for d in gender_data.values())
	total_units = sum(d["quantity"] for d in gender_data.values())

	sorted_genders = sorted(gender_data.items(), key=lambda x: x[1]["revenue"], reverse=True)

	output.append("| Gender | Revenue | Share | Units | Unit Share | YTD Rev | Prior LfL | YoY Growth |")
	output.append("|--------|---------|-------|-------|------------|---------|----------|------------|")

	for gender, data in sorted_genders:
		rev_share = data["revenue"] / total_rev * 100 if total_rev else 0
		unit_share = data["quantity"] / total_units * 100 if total_units else 0
		if data["prior_rev"] > 0:
			growth = (data["ytd_rev"] - data["prior_rev"]) / data["prior_rev"] * 100
			growth_str = f"{growth:+.1f}%"
		else:
			growth_str = "N/A"
		output.append(
			f"| {gender} | {fmt_gbp(data['revenue'])} | {fmt_pct(rev_share)} | "
			f"{data['quantity']} | {fmt_pct(unit_share)} | "
			f"{fmt_gbp(data['ytd_rev'])} | {fmt_gbp(data['prior_rev'])} | {growth_str} |"
		)

	# Article performance
	output.append("\n### 4.2 Top 15 Articles by Revenue\n")

	article_data = defaultdict(lambda: {
		"revenue": 0.0,
		"quantity": 0,
		"projects": set(),
		"category": "",
		"orders": set(),
	})

	for item in items:
		art = item["article_number"]
		if not art:
			continue
		article_data[art]["revenue"] += item["revenue"]
		article_data[art]["quantity"] += item["quantity"]
		article_data[art]["projects"].add(item["design_name"])
		article_data[art]["orders"].add(item["order_id"])
		if not article_data[art]["category"]:
			article_data[art]["category"] = item["category"]

	# Enrich with articles.json data
	articles_lookup = {}
	for a in articles_data:
		art_num = a.get("article", "")
		if art_num:
			articles_lookup[art_num] = {
				"description": a.get("description", ""),
				"cost_price": a.get("costPrice", 0),
				"custom_price": a.get("customPrice", 0),
				"rrp": a.get("rrp", 0),
				"supplier": a.get("supplier", ""),
			}

	sorted_articles = sorted(article_data.items(), key=lambda x: x[1]["revenue"], reverse=True)

	output.append("| # | Article | Category | Revenue | Units | Projects | Orders | Description |")
	output.append("|---|---------|----------|---------|-------|----------|--------|-------------|")

	for i, (art, data) in enumerate(sorted_articles[:15], 1):
		art_info = articles_lookup.get(art, {})
		desc = art_info.get("description", "")
		output.append(
			f"| {i} | {art} | {data['category']} | {fmt_gbp(data['revenue'])} | "
			f"{data['quantity']} | {len(data['projects'])} | {len(data['orders'])} | {desc} |"
		)

	no_article = sum(1 for item in items if not item["article_number"])
	no_article_rev = sum(item["revenue"] for item in items if not item["article_number"])
	output.append(f"\nTotal unique articles with revenue: {len(article_data)}")
	output.append(f"Line items with no article number: {no_article} ({fmt_gbp(no_article_rev)} revenue)")

	# Article category performance
	output.append("\n### 4.3 CK Category Performance\n")

	cat_data = defaultdict(lambda: {
		"revenue": 0.0,
		"quantity": 0,
		"ytd_rev": 0.0,
		"prior_rev": 0.0,
		"projects": set(),
	})

	for item in items:
		cat = item["category"]
		cat_data[cat]["revenue"] += item["revenue"]
		cat_data[cat]["quantity"] += item["quantity"]
		cat_data[cat]["projects"].add(item["design_name"])

		yr = item["order_date"].year
		mn = item["order_date"].month
		dy = item["order_date"].day
		if yr == current_year:
			cat_data[cat]["ytd_rev"] += item["revenue"]
		elif yr == prior_year and (mn < ytd_cutoff_month or (mn == ytd_cutoff_month and dy <= ytd_cutoff_day)):
			cat_data[cat]["prior_rev"] += item["revenue"]

	sorted_cats = sorted(cat_data.items(), key=lambda x: x[1]["revenue"], reverse=True)

	output.append("| Category | Revenue | Share | Units | Projects | YTD Rev | Prior LfL | YoY Growth |")
	output.append("|----------|---------|-------|-------|----------|---------|----------|------------|")

	for cat, data in sorted_cats:
		rev_share = data["revenue"] / total_rev * 100 if total_rev else 0
		if data["prior_rev"] > 0:
			growth = (data["ytd_rev"] - data["prior_rev"]) / data["prior_rev"] * 100
			growth_str = f"{growth:+.1f}%"
		else:
			growth_str = "N/A"
		output.append(
			f"| {cat} | {fmt_gbp(data['revenue'])} | {fmt_pct(rev_share)} | "
			f"{data['quantity']} | {len(data['projects'])} | "
			f"{fmt_gbp(data['ytd_rev'])} | {fmt_gbp(data['prior_rev'])} | {growth_str} |"
		)

	output.append("")


def part5_discount_analysis(items: list, output: list):
	"""Part 5: Discount Analysis."""
	output.append("## Part 5: Discount Analysis\n")

	total_revenue = sum(i["revenue"] for i in items)
	total_units = sum(i["quantity"] for i in items)
	clearance_items = [i for i in items if i["is_clearance"]]
	fullprice_items = [i for i in items if not i["is_clearance"]]

	clearance_rev = sum(i["revenue"] for i in clearance_items)
	fullprice_rev = sum(i["revenue"] for i in fullprice_items)
	clearance_units = sum(i["quantity"] for i in clearance_items)
	fullprice_units = sum(i["quantity"] for i in fullprice_items)

	output.append("### 5.1 CK Full-Price vs Clearance\n")
	output.append("| Metric | Full-Price | Clearance | Total |")
	output.append("|--------|-----------|-----------|-------|")
	output.append(f"| Revenue (ex-VAT) | {fmt_gbp(fullprice_rev)} | {fmt_gbp(clearance_rev)} | {fmt_gbp(total_revenue)} |")
	output.append(f"| Revenue Share | {fmt_pct(fullprice_rev / total_revenue * 100 if total_revenue else 0)} | {fmt_pct(clearance_rev / total_revenue * 100 if total_revenue else 0)} | 100.0% |")
	output.append(f"| Units | {fullprice_units} | {clearance_units} | {total_units} |")

	# Discount by project size
	output.append("\n### 5.2 Discount by Project Size\n")

	project_data = defaultdict(lambda: {
		"total_revenue": 0.0,
		"clearance_revenue": 0.0,
		"total_discount_value": 0.0,
		"total_subtotal": 0.0,
	})

	for item in items:
		proj = project_data[item["design_name"]]
		proj["total_revenue"] += item["revenue"]
		proj["clearance_revenue"] += item["revenue"] if item["is_clearance"] else 0
		proj["total_subtotal"] += item["subtotal"]
		proj["total_discount_value"] += item["subtotal"] - item["total"]

	sorted_proj = sorted(project_data.items(), key=lambda x: x[1]["total_revenue"], reverse=True)

	# Group into buckets by project size
	buckets = {
		"Large (>£5k)": {"revenue": 0.0, "clearance": 0.0, "subtotal": 0.0, "discount_value": 0.0, "count": 0},
		"Medium (£1k-£5k)": {"revenue": 0.0, "clearance": 0.0, "subtotal": 0.0, "discount_value": 0.0, "count": 0},
		"Small (<£1k)": {"revenue": 0.0, "clearance": 0.0, "subtotal": 0.0, "discount_value": 0.0, "count": 0},
	}

	for name, data in sorted_proj:
		rev = data["total_revenue"]
		if rev > 5000:
			bucket = "Large (>£5k)"
		elif rev > 1000:
			bucket = "Medium (£1k-£5k)"
		else:
			bucket = "Small (<£1k)"

		buckets[bucket]["revenue"] += rev
		buckets[bucket]["clearance"] += data["clearance_revenue"]
		buckets[bucket]["subtotal"] += data["total_subtotal"]
		buckets[bucket]["discount_value"] += data["total_discount_value"]
		buckets[bucket]["count"] += 1

	output.append("| Project Size | Projects | Revenue | Clearance Rev | Clearance % | Avg Discount % |")
	output.append("|-------------|----------|---------|--------------|------------|----------------|")

	for bucket_name in ["Large (>£5k)", "Medium (£1k-£5k)", "Small (<£1k)"]:
		b = buckets[bucket_name]
		cl_pct = b["clearance"] / b["revenue"] * 100 if b["revenue"] else 0
		avg_disc = b["discount_value"] / b["subtotal"] * 100 if b["subtotal"] else 0
		output.append(
			f"| {bucket_name} | {b['count']} | {fmt_gbp(b['revenue'])} | "
			f"{fmt_gbp(b['clearance'])} | {fmt_pct(cl_pct)} | {fmt_pct(avg_disc)} |"
		)

	# Top 10 most discounted CK projects (with meaningful revenue)
	output.append("\n### 5.3 Most Discounted CK Projects (Revenue > £500)\n")

	discounted_projects = []
	for name, data in sorted_proj:
		if data["total_revenue"] < 500:
			continue
		avg_disc = data["total_discount_value"] / data["total_subtotal"] * 100 if data["total_subtotal"] else 0
		cl_pct = data["clearance_revenue"] / data["total_revenue"] * 100 if data["total_revenue"] else 0
		discounted_projects.append((name, data["total_revenue"], avg_disc, cl_pct))

	discounted_projects.sort(key=lambda x: x[2], reverse=True)

	output.append("| # | Project | Revenue | Avg Discount % | Clearance % |")
	output.append("|---|---------|---------|---------------|------------|")

	for i, (name, rev, avg_disc, cl_pct) in enumerate(discounted_projects[:10], 1):
		output.append(f"| {i} | {name} | {fmt_gbp(rev)} | {fmt_pct(avg_disc)} | {fmt_pct(cl_pct)} |")

	output.append("")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
	print("Loading data...")
	orders_data = load_json(DATA_ROOT / "orders.json")
	skus_data = load_json(DATA_ROOT / "operationalSkus.json")
	articles_data = load_json(DATA_ROOT / "articles.json")

	print(f"  Orders: {len(orders_data)}")
	print(f"  Operational SKUs: {len(skus_data)}")
	print(f"  Articles: {len(articles_data)}")

	print("Building SKU lookup...")
	sku_lookup = build_sku_lookup(skus_data)
	ck_skus_count = sum(1 for k in sku_lookup if k.startswith("CK"))
	print(f"  CK SKUs in lookup: {ck_skus_count}")

	print("Extracting CK line items...")
	items = extract_ck_line_items(orders_data, sku_lookup)
	print(f"  CK line items: {len(items)}")

	total_revenue = sum(i["revenue"] for i in items)
	total_orders = len(set(i["order_id"] for i in items))
	date_range = (
		min(i["order_date"] for i in items).strftime("%Y-%m-%d"),
		max(i["order_date"] for i in items).strftime("%Y-%m-%d"),
	)
	print(f"  Total CK revenue (ex-VAT): {fmt_gbp(total_revenue)}")
	print(f"  Total CK orders: {total_orders}")
	print(f"  Date range: {date_range[0]} to {date_range[1]}")

	# Spot-check: items with no design name
	unknown = sum(1 for i in items if i["design_name"] == "UNKNOWN PROJECT")
	print(f"  Items with unknown project: {unknown}")

	# Run analysis
	output = []
	output.append("# Custom Kit Performance Deep Dive\n")
	output.append(f"**Generated:** {NOW.strftime('%Y-%m-%d %H:%M')}")
	output.append(f"**Date range:** {date_range[0]} to {date_range[1]}")
	output.append(f"**CK line items analysed:** {len(items)}")
	output.append(f"**CK orders:** {total_orders}")
	output.append(f"**Total CK revenue (ex-VAT):** {fmt_gbp(total_revenue)}")
	output.append(f"**Methodology:** Revenue = total - total_tax (ex-VAT). Clearance = >20% discount. Webshop = has transaction_id OR order number starts with 'GE'. Order statuses excluded: {', '.join(EXCLUDED_ORDER_STATUSES)}.")
	output.append("")

	print("\nRunning Part 1: Project Performance...")
	part1_project_performance(items, output)

	print("Running Part 2: Webshop Performance...")
	part2_webshop_performance(items, output)

	print("Running Part 3: Growth Trends...")
	part3_growth_trends(items, output)

	print("Running Part 4: Gender & Article Analysis...")
	part4_gender_article(items, sku_lookup, articles_data, output)

	print("Running Part 5: Discount Analysis...")
	part5_discount_analysis(items, output)

	# Write findings
	findings_path = Path(r"C:\ClaudeProjects\pablo\projects\sg-analysis\.state\research\ck-findings.md")
	findings_path.parent.mkdir(parents=True, exist_ok=True)

	findings_content = "\n".join(output)
	with open(findings_path, "w", encoding="utf-8") as f:
		f.write(findings_content)

	print(f"\nFindings written to: {findings_path}")
	print(f"Total output lines: {len(output)}")
	print("Done.")


if __name__ == "__main__":
	main()
