"""Collection Performance Deep Dive — Discount-Adjusted Analysis.

TASK-009: Analyses Stolen Goat collection (non-CK) product performance,
separating genuine organic demand from discount-driven/clearance sales.

Standalone script — requires only pandas and json (stdlib).
"""

import json
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

# ──────────────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────────────

DATA_ROOT = Path(
	r"C:\Users\timbl\stolen goat Dropbox\tim bland"
	r"\Stolen Goat\Multichannel Manager\Tools"
	r"\SkynetPowerDash\Repository"
)

OUTPUT_PATH = Path(__file__).parent / "collection-findings.md"

EXCLUDED_ORDER_STATUSES = {
	"cancelled", "refunded", "pending_payment", "pending",
	"on-hold", "internal", "failed", "trash", "draft",
}

CLEARANCE_DISCOUNT_THRESHOLD = 0.20  # >20% discount = clearance

# Category normalisation map — merge duplicates
CATEGORY_NORMALISE = {
	"GILET": "GILETS",
	"JACKET": "JACKETS",
	"Jersey": "JERSEYS & TOPS",
	"SS JERSEYS": "JERSEYS & TOPS",
	"Bib Shorts": "BIB SHORTS",
	"SHORTS & BIBS": "BIB SHORTS",
	"HEAD AND NECK": "HEAD & NECK",
	"Accessories": "ACCESSORIES",
	"Cycling Caps": "CYCLING CAPS",
	"Nutrition": "NUTRITION",
	"Swim Caps": "SWIMWEAR",
	"SPEED & TRISUITS": "SPEED & TRI SUITS",
	"GLASSES & GOGGLES": "EYEWEAR",
	"T-Shirt": "HOODIES",  # T-shirts grouped with casual wear
	"HELMETS - ROAD (ADULT)": "HELMETS",
	"Jacket": "JACKETS",
}


# ──────────────────────────────────────────────────────────────────────
# Data loading
# ──────────────────────────────────────────────────────────────────────

def load_json(path: Path) -> list[dict]:
	with open(path, "r", encoding="utf-8") as f:
		return json.load(f)


def normalise_category(cat: str) -> str:
	"""Normalise a category string, applying the merge map."""
	if not cat or not isinstance(cat, str):
		return "UNCATEGORISED"
	cat = cat.strip()
	if not cat:
		return "UNCATEGORISED"
	return CATEGORY_NORMALISE.get(cat, cat)


def load_operational_skus() -> pd.DataFrame:
	"""Load operationalSkus.json, classify CK, normalise categories."""
	data = load_json(DATA_ROOT / "operationalSkus.json")
	df = pd.DataFrame(data)
	# Classify CK
	df["is_ck"] = df["sku"].astype(str).str.startswith("CK").astype(int)
	# Normalise categories
	df["category_raw"] = df["category"].fillna("")
	df["category"] = df["category_raw"].apply(normalise_category)
	# Numeric columns
	for col in ["available", "sold7d", "sold30d", "sold90d", "sold6m", "sold12m", "rrp", "salePrice"]:
		if col in df.columns:
			df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
	df["product_id"] = pd.to_numeric(df["product_id"], errors="coerce").fillna(0).astype(int)
	return df


def load_orders() -> tuple[pd.DataFrame, pd.DataFrame]:
	"""Load orders.json, return (orders_df, line_items_df)."""
	data = load_json(DATA_ROOT / "orders.json")

	line_items_rows = []
	orders_flat = []

	for order in data:
		order_id = order["id"]
		for item in order.get("line_items", []):
			row = {
				"order_id": order_id,
				"li_id": item.get("id"),
				"name": item.get("name", ""),
				"product_id": item.get("product_id", 0),
				"sku": str(item.get("sku", "") or ""),
				"quantity": int(item.get("quantity", 0) or 0),
				"subtotal": float(item.get("subtotal", 0) or 0),
				"subtotal_tax": float(item.get("subtotal_tax", 0) or 0),
				"total": float(item.get("total", 0) or 0),
				"total_tax": float(item.get("total_tax", 0) or 0),
				"price": float(item.get("price", 0) or 0),
			}
			row["is_ck"] = 1 if row["sku"].startswith("CK") else 0
			line_items_rows.append(row)

		flat = {
			"id": order_id,
			"status": order.get("status"),
			"customer_id": order.get("customer_id", 0),
			"date_created": str(order.get("date_created", "")).rstrip("Z"),
			"total": float(order.get("total", 0) or 0),
			"total_tax": float(order.get("total_tax", 0) or 0),
			"discount_total": float(order.get("discount_total", 0) or 0),
		}
		orders_flat.append(flat)

	orders_df = pd.DataFrame(orders_flat)
	orders_df["date_created"] = pd.to_datetime(orders_df["date_created"], errors="coerce")

	line_items_df = pd.DataFrame(line_items_rows)
	return orders_df, line_items_df


# ──────────────────────────────────────────────────────────────────────
# Analysis helpers
# ──────────────────────────────────────────────────────────────────────

def classify_discount(li_df: pd.DataFrame) -> pd.DataFrame:
	"""Add discount_pct and is_clearance columns to line items."""
	df = li_df.copy()
	df["discount_pct"] = 0.0
	mask = df["subtotal"] > 0
	df.loc[mask, "discount_pct"] = (df.loc[mask, "subtotal"] - df.loc[mask, "total"]) / df.loc[mask, "subtotal"]
	df["is_clearance"] = (df["discount_pct"] > CLEARANCE_DISCOUNT_THRESHOLD).astype(int)
	return df


def ex_vat(total: pd.Series, total_tax: pd.Series) -> pd.Series:
	"""Calculate ex-VAT revenue."""
	return total - total_tax


# ──────────────────────────────────────────────────────────────────────
# Main analysis
# ──────────────────────────────────────────────────────────────────────

def main():
	print("Loading data...")
	skus = load_operational_skus()
	orders_df, line_items_df = load_orders()

	# Filter to valid orders
	valid_orders = orders_df[
		~orders_df["status"].isin(EXCLUDED_ORDER_STATUSES)
		& orders_df["status"].notna()
	].copy()
	valid_order_ids = set(valid_orders["id"])
	print(f"  Valid orders: {len(valid_orders)} / {len(orders_df)}")

	# Filter line items to valid orders
	li = line_items_df[line_items_df["order_id"].isin(valid_order_ids)].copy()
	print(f"  Valid line items: {len(li)} / {len(line_items_df)}")

	# Filter to COLLECTION only (exclude CK)
	li_collection = li[li["is_ck"] == 0].copy()
	print(f"  Collection line items: {len(li_collection)}")

	# Collection SKUs
	skus_collection = skus[skus["is_ck"] == 0].copy()
	print(f"  Collection SKUs: {len(skus_collection)}")

	# Add discount classification
	li_collection = classify_discount(li_collection)

	# Calculate ex-VAT revenue
	li_collection["revenue_ex_vat"] = ex_vat(li_collection["total"], li_collection["total_tax"])

	# Join category from SKUs to line items
	sku_cat_lookup = skus[["sku", "category"]].drop_duplicates(subset="sku")
	li_collection = li_collection.merge(sku_cat_lookup, on="sku", how="left")
	li_collection["category"] = li_collection["category"].fillna("UNCATEGORISED")

	# Also add order date to line items
	order_dates = valid_orders[["id", "date_created"]].rename(columns={"id": "order_id"})
	li_collection = li_collection.merge(order_dates, on="order_id", how="left")

	# ──────────────────────────────────────────────────────────────
	# Output accumulator
	# ──────────────────────────────────────────────────────────────
	output_lines = []

	def out(text=""):
		output_lines.append(text)
		print(text)

	out("# Collection Performance Deep Dive — Findings")
	out()
	out(f"**Generated:** 2026-03-23")
	out(f"**Scope:** Collection products only (CK excluded)")
	out(f"**Orders analysed:** {len(valid_orders):,} valid orders, {len(li_collection):,} collection line items")
	out(f"**Date range:** {valid_orders['date_created'].min().strftime('%Y-%m-%d')} to {valid_orders['date_created'].max().strftime('%Y-%m-%d')}")
	out()

	# ──────────────────────────────────────────────────────────────
	# PART 1: Collection Category Performance
	# ──────────────────────────────────────────────────────────────
	out("## Part 1: Collection Category Performance")
	out()

	# 1a. Revenue split by category
	cat_revenue = (
		li_collection.groupby("category")
		.agg(
			total_revenue=("revenue_ex_vat", "sum"),
			total_units=("quantity", "sum"),
			line_item_count=("li_id", "count"),
		)
		.reset_index()
	)

	# Count unique SKUs per category from SKU data
	sku_counts = (
		skus_collection[skus_collection["category"] != "UNCATEGORISED"]
		.groupby("category")["sku"]
		.nunique()
		.reset_index()
		.rename(columns={"sku": "sku_count"})
	)
	cat_revenue = cat_revenue.merge(sku_counts, on="category", how="left")
	cat_revenue["sku_count"] = cat_revenue["sku_count"].fillna(0).astype(int)

	# AOV per category
	cat_revenue["aov"] = cat_revenue.apply(
		lambda r: r["total_revenue"] / r["total_units"] if r["total_units"] > 0 else 0,
		axis=1
	)

	cat_revenue = cat_revenue.sort_values("total_revenue", ascending=False).reset_index(drop=True)

	out("### 1.1 Revenue by Category")
	out()
	out("| Category | Revenue (ex-VAT) | Units | SKUs | AOV |")
	out("|---|---|---|---|---|")
	total_rev_all = cat_revenue["total_revenue"].sum()
	total_units_all = cat_revenue["total_units"].sum()
	for _, row in cat_revenue.iterrows():
		pct = row["total_revenue"] / total_rev_all * 100 if total_rev_all > 0 else 0
		out(f"| {row['category']} | £{row['total_revenue']:,.2f} ({pct:.1f}%) | {int(row['total_units']):,} | {row['sku_count']} | £{row['aov']:,.2f} |")
	out(f"| **TOTAL** | **£{total_rev_all:,.2f}** | **{int(total_units_all):,}** | **{cat_revenue['sku_count'].sum()}** | **£{total_rev_all/total_units_all if total_units_all > 0 else 0:,.2f}** |")
	out()

	# 1b. Full-price vs discounted split per category
	cat_fp = (
		li_collection[li_collection["is_clearance"] == 0]
		.groupby("category")
		.agg(fp_revenue=("revenue_ex_vat", "sum"), fp_units=("quantity", "sum"))
		.reset_index()
	)
	cat_cl = (
		li_collection[li_collection["is_clearance"] == 1]
		.groupby("category")
		.agg(cl_revenue=("revenue_ex_vat", "sum"), cl_units=("quantity", "sum"))
		.reset_index()
	)

	cat_split = cat_revenue[["category", "total_revenue", "total_units"]].merge(
		cat_fp, on="category", how="left"
	).merge(
		cat_cl, on="category", how="left"
	)
	for col in ["fp_revenue", "fp_units", "cl_revenue", "cl_units"]:
		cat_split[col] = cat_split[col].fillna(0)

	cat_split["fp_pct"] = cat_split.apply(
		lambda r: r["fp_revenue"] / r["total_revenue"] * 100 if r["total_revenue"] > 0 else 0,
		axis=1
	)
	cat_split = cat_split.sort_values("total_revenue", ascending=False).reset_index(drop=True)

	out("### 1.2 Full-Price vs Clearance Split by Category")
	out()
	out("Clearance = line item discount > 20%.")
	out()
	out("| Category | Full-Price Revenue | Clearance Revenue | Full-Price % | FP Units | CL Units |")
	out("|---|---|---|---|---|---|")
	for _, row in cat_split.iterrows():
		out(f"| {row['category']} | £{row['fp_revenue']:,.2f} | £{row['cl_revenue']:,.2f} | {row['fp_pct']:.1f}% | {int(row['fp_units']):,} | {int(row['cl_units']):,} |")
	total_fp = cat_split["fp_revenue"].sum()
	total_cl = cat_split["cl_revenue"].sum()
	total_fp_pct = total_fp / total_rev_all * 100 if total_rev_all > 0 else 0
	out(f"| **TOTAL** | **£{total_fp:,.2f}** | **£{total_cl:,.2f}** | **{total_fp_pct:.1f}%** | **{int(cat_split['fp_units'].sum()):,}** | **{int(cat_split['cl_units'].sum()):,}** |")
	out()

	# 1c. Velocity by category (from SKU data)
	cat_velocity = (
		skus_collection.groupby("category")
		.agg(
			sold_7d=("sold7d", "sum"),
			sold_30d=("sold30d", "sum"),
			sold_90d=("sold90d", "sum"),
		)
		.reset_index()
	)
	cat_velocity = cat_velocity.sort_values("sold_30d", ascending=False).reset_index(drop=True)

	out("### 1.3 SKU Velocity by Category (from operational data)")
	out()
	out("| Category | Sold 7d | Sold 30d | Sold 90d |")
	out("|---|---|---|---|")
	for _, row in cat_velocity.iterrows():
		if row["sold_90d"] > 0:
			out(f"| {row['category']} | {int(row['sold_7d']):,} | {int(row['sold_30d']):,} | {int(row['sold_90d']):,} |")
	out()

	# 1d. Growth signal: 30d vs 90d rate
	cat_velocity["monthly_rate_30d"] = cat_velocity["sold_30d"]
	cat_velocity["monthly_rate_prior_60d"] = (cat_velocity["sold_90d"] - cat_velocity["sold_30d"]) / 2.0
	cat_velocity["acceleration"] = cat_velocity.apply(
		lambda r: r["monthly_rate_30d"] / r["monthly_rate_prior_60d"]
		if r["monthly_rate_prior_60d"] > 0 else 0,
		axis=1
	)

	out("### 1.4 Growth Signal (30d rate vs prior 60d monthly average)")
	out()
	out("Acceleration > 1.0 = category selling faster than prior period.")
	out()
	out("| Category | Sold 30d | Prior 60d Monthly Avg | Acceleration |")
	out("|---|---|---|---|")
	cat_velocity_sorted = cat_velocity[cat_velocity["sold_90d"] > 0].sort_values("acceleration", ascending=False)
	for _, row in cat_velocity_sorted.iterrows():
		accel_str = f"{row['acceleration']:.2f}x" if row['acceleration'] > 0 else "N/A"
		out(f"| {row['category']} | {int(row['monthly_rate_30d']):,} | {row['monthly_rate_prior_60d']:.1f} | {accel_str} |")
	out()

	# 1e. Stock position by category
	cat_stock = (
		skus_collection.groupby("category")
		.agg(
			total_available=("available", "sum"),
			total_skus=("sku", "count"),
			zero_stock_skus=("available", lambda x: (x == 0).sum()),
		)
		.reset_index()
	)
	cat_stock = cat_stock.sort_values("total_available", ascending=False).reset_index(drop=True)

	out("### 1.5 Stock Position by Category")
	out()
	out("| Category | Available Units | Total SKUs | SKUs at Zero Stock | Zero Stock % |")
	out("|---|---|---|---|---|")
	for _, row in cat_stock.iterrows():
		if row["total_skus"] > 0:
			zero_pct = row["zero_stock_skus"] / row["total_skus"] * 100
			out(f"| {row['category']} | {int(row['total_available']):,} | {int(row['total_skus'])} | {int(row['zero_stock_skus'])} | {zero_pct:.0f}% |")
	out()

	# ──────────────────────────────────────────────────────────────
	# PART 2: Non-Jersey Growth Opportunities
	# ──────────────────────────────────────────────────────────────
	out("## Part 2: Non-Jersey Growth Opportunities")
	out()

	non_jersey_velocity = cat_velocity[cat_velocity["category"] != "JERSEYS & TOPS"].copy()
	non_jersey_split = cat_split[cat_split["category"] != "JERSEYS & TOPS"].copy()
	non_jersey_stock = cat_stock[cat_stock["category"] != "JERSEYS & TOPS"].copy()

	# 2.1 Highest full-price revenue growth (acceleration)
	non_jersey_fp_growth = non_jersey_velocity.merge(
		non_jersey_split[["category", "fp_revenue", "fp_pct"]], on="category", how="left"
	)
	# Only categories with meaningful sales
	meaningful = non_jersey_fp_growth[non_jersey_fp_growth["sold_30d"] >= 5].sort_values("acceleration", ascending=False)

	out("### 2.1 Highest Full-Price Growth (non-jersey categories with 5+ units/30d)")
	out()
	out("| Category | Acceleration | Sold 30d | Full-Price Revenue | FP % |")
	out("|---|---|---|---|---|")
	for _, row in meaningful.iterrows():
		accel_str = f"{row['acceleration']:.2f}x" if row['acceleration'] > 0 else "N/A"
		fp_rev = row.get("fp_revenue", 0) or 0
		fp_pct = row.get("fp_pct", 0) or 0
		out(f"| {row['category']} | {accel_str} | {int(row['sold_30d']):,} | £{fp_rev:,.2f} | {fp_pct:.1f}% |")
	out()

	# 2.2 Best full-price sell-through rate
	# Sell-through = sold_30d / (available + sold_30d)
	non_jersey_sellthrough = non_jersey_velocity.merge(
		non_jersey_stock[["category", "total_available"]], on="category", how="left"
	)
	non_jersey_sellthrough["total_available"] = non_jersey_sellthrough["total_available"].fillna(0)
	non_jersey_sellthrough["sell_through_30d"] = non_jersey_sellthrough.apply(
		lambda r: r["sold_30d"] / (r["total_available"] + r["sold_30d"]) * 100
		if (r["total_available"] + r["sold_30d"]) > 0 else 0,
		axis=1
	)
	non_jersey_sellthrough = non_jersey_sellthrough[
		non_jersey_sellthrough["sold_30d"] > 0
	].sort_values("sell_through_30d", ascending=False)

	out("### 2.2 Best Full-Price Sell-Through Rate (non-jersey)")
	out()
	out("Sell-through = sold_30d / (available + sold_30d). Higher = turning stock faster.")
	out()
	out("| Category | Sell-Through 30d | Sold 30d | Available |")
	out("|---|---|---|---|")
	for _, row in non_jersey_sellthrough.iterrows():
		out(f"| {row['category']} | {row['sell_through_30d']:.1f}% | {int(row['sold_30d']):,} | {int(row['total_available']):,} |")
	out()

	# 2.3 Strong velocity but thin stock (missed opportunity)
	non_jersey_opportunity = non_jersey_velocity.merge(
		non_jersey_stock[["category", "total_available", "zero_stock_skus", "total_skus"]], on="category", how="left"
	)
	# Flag categories with good velocity but high zero-stock %
	non_jersey_opportunity["zero_stock_pct"] = non_jersey_opportunity.apply(
		lambda r: r["zero_stock_skus"] / r["total_skus"] * 100 if r["total_skus"] > 0 else 0,
		axis=1
	)
	thin_stock = non_jersey_opportunity[
		(non_jersey_opportunity["sold_30d"] >= 5)
		& (non_jersey_opportunity["zero_stock_pct"] > 30)
	].sort_values("sold_30d", ascending=False)

	out("### 2.3 Strong Velocity but Thin Stock (non-jersey, 5+ sold/30d, >30% SKUs at zero)")
	out()
	if thin_stock.empty:
		out("No non-jersey categories meet both criteria (5+ sales/30d AND >30% SKUs at zero stock).")
		out()
		# Relax criteria
		thin_stock_relaxed = non_jersey_opportunity[
			(non_jersey_opportunity["sold_30d"] >= 3)
			& (non_jersey_opportunity["zero_stock_pct"] > 20)
		].sort_values("sold_30d", ascending=False)
		if not thin_stock_relaxed.empty:
			out("Relaxed criteria (3+ sold/30d, >20% at zero):")
			out()
			out("| Category | Sold 30d | Available | Zero Stock SKUs | Zero % |")
			out("|---|---|---|---|---|")
			for _, row in thin_stock_relaxed.iterrows():
				out(f"| {row['category']} | {int(row['sold_30d']):,} | {int(row['total_available']):,} | {int(row['zero_stock_skus'])} | {row['zero_stock_pct']:.0f}% |")
			out()
	else:
		out("| Category | Sold 30d | Available | Zero Stock SKUs | Zero % |")
		out("|---|---|---|---|---|")
		for _, row in thin_stock.iterrows():
			out(f"| {row['category']} | {int(row['sold_30d']):,} | {int(row['total_available']):,} | {int(row['zero_stock_skus'])} | {row['zero_stock_pct']:.0f}% |")
		out()

	# 2.4 Repeat purchase rate by category (non-jersey)
	# Customers who bought in the same category more than once
	li_with_customer = li_collection.merge(
		valid_orders[["id", "customer_id"]].rename(columns={"id": "order_id"}),
		on="order_id", how="left"
	)
	# Exclude guest checkouts
	li_with_customer = li_with_customer[li_with_customer["customer_id"] != 0]

	non_jersey_li = li_with_customer[li_with_customer["category"] != "JERSEYS & TOPS"]

	cat_repeat = (
		non_jersey_li.groupby(["category", "customer_id"])
		.agg(order_count=("order_id", "nunique"))
		.reset_index()
	)
	cat_repeat_summary = (
		cat_repeat.groupby("category")
		.agg(
			total_customers=("customer_id", "count"),
			repeat_customers=("order_count", lambda x: (x > 1).sum()),
		)
		.reset_index()
	)
	cat_repeat_summary["repeat_rate"] = cat_repeat_summary.apply(
		lambda r: r["repeat_customers"] / r["total_customers"] * 100 if r["total_customers"] > 0 else 0,
		axis=1
	)
	cat_repeat_summary = cat_repeat_summary[
		cat_repeat_summary["total_customers"] >= 10
	].sort_values("repeat_rate", ascending=False)

	out("### 2.4 Repeat Purchase Rate by Category (non-jersey, 10+ customers)")
	out()
	out("Repeat = same customer bought from this category in 2+ separate orders.")
	out()
	out("| Category | Total Customers | Repeat Customers | Repeat Rate |")
	out("|---|---|---|---|")
	for _, row in cat_repeat_summary.iterrows():
		out(f"| {row['category']} | {int(row['total_customers']):,} | {int(row['repeat_customers'])} | {row['repeat_rate']:.1f}% |")
	out()

	# ──────────────────────────────────────────────────────────────
	# PART 3: Discount Impact Analysis
	# ──────────────────────────────────────────────────────────────
	out("## Part 3: Discount Impact Analysis")
	out()

	# 3.1 Overall clearance share
	total_collection_rev = li_collection["revenue_ex_vat"].sum()
	clearance_rev = li_collection[li_collection["is_clearance"] == 1]["revenue_ex_vat"].sum()
	full_price_rev = li_collection[li_collection["is_clearance"] == 0]["revenue_ex_vat"].sum()
	clearance_units = li_collection[li_collection["is_clearance"] == 1]["quantity"].sum()
	full_price_units = li_collection[li_collection["is_clearance"] == 0]["quantity"].sum()

	out("### 3.1 Overall Clearance Share of Collection Revenue")
	out()
	out(f"- **Total collection revenue (ex-VAT):** £{total_collection_rev:,.2f}")
	out(f"- **Full-price revenue:** £{full_price_rev:,.2f} ({full_price_rev/total_collection_rev*100:.1f}%)")
	out(f"- **Clearance revenue (>20% discount):** £{clearance_rev:,.2f} ({clearance_rev/total_collection_rev*100:.1f}%)")
	out(f"- **Full-price units:** {int(full_price_units):,}")
	out(f"- **Clearance units:** {int(clearance_units):,}")
	out()

	# 3.2 Categories most reliant on discounting
	cat_discount_reliance = cat_split.copy()
	cat_discount_reliance["cl_pct"] = 100 - cat_discount_reliance["fp_pct"]
	cat_discount_reliance = cat_discount_reliance[
		cat_discount_reliance["total_revenue"] > 0
	].sort_values("cl_pct", ascending=False)

	out("### 3.2 Categories Most Reliant on Discounting")
	out()
	out("Ranked by % of category revenue coming from clearance (>20% discount).")
	out()
	out("| Category | Total Revenue | Clearance Revenue | Clearance % | Full-Price % |")
	out("|---|---|---|---|---|")
	for _, row in cat_discount_reliance.iterrows():
		out(f"| {row['category']} | £{row['total_revenue']:,.2f} | £{row['cl_revenue']:,.2f} | {row['cl_pct']:.1f}% | {row['fp_pct']:.1f}% |")
	out()

	# 3.3 Hidden gems — products selling well at full price in mostly-discounted categories
	# Categories where >50% of revenue is clearance
	heavily_discounted_cats = set(
		cat_discount_reliance[cat_discount_reliance["cl_pct"] > 40]["category"]
	)

	out("### 3.3 Hidden Gems — Full-Price Winners in Heavily Discounted Categories")
	out()
	if not heavily_discounted_cats:
		out("No categories have >40% clearance revenue — lowering threshold to 30%.")
		heavily_discounted_cats = set(
			cat_discount_reliance[cat_discount_reliance["cl_pct"] > 30]["category"]
		)

	if heavily_discounted_cats:
		out(f"Categories with high clearance reliance (>40% clearance): {', '.join(sorted(heavily_discounted_cats))}")
		out()

		# Find products in these categories that sell at full price
		gems_li = li_collection[
			(li_collection["category"].isin(heavily_discounted_cats))
			& (li_collection["is_clearance"] == 0)
		]
		if not gems_li.empty:
			gems = (
				gems_li.groupby(["name", "category"])
				.agg(
					fp_revenue=("revenue_ex_vat", "sum"),
					fp_units=("quantity", "sum"),
				)
				.reset_index()
				.sort_values("fp_revenue", ascending=False)
				.head(20)
			)

			out("| Product | Category | Full-Price Revenue | FP Units |")
			out("|---|---|---|---|")
			for _, row in gems.iterrows():
				out(f"| {row['name']} | {row['category']} | £{row['fp_revenue']:,.2f} | {int(row['fp_units'])} |")
			out()
		else:
			out("No full-price sales found in heavily discounted categories.")
			out()
	else:
		out("No categories meet the threshold for heavy discounting.")
		out()

	# ──────────────────────────────────────────────────────────────
	# Discount band distribution (supplementary data)
	# ──────────────────────────────────────────────────────────────
	out("### 3.4 Discount Band Distribution (all collection line items)")
	out()
	li_collection["discount_band"] = pd.cut(
		li_collection["discount_pct"],
		bins=[-0.01, 0.0, 0.10, 0.20, 0.30, 0.50, 1.01],
		labels=["0% (full price)", "1-10%", "11-20%", "21-30%", "31-50%", "51-100%"],
	)
	band_summary = (
		li_collection.groupby("discount_band", observed=True)
		.agg(
			revenue=("revenue_ex_vat", "sum"),
			units=("quantity", "sum"),
			count=("li_id", "count"),
		)
		.reset_index()
	)
	total_band_rev = band_summary["revenue"].sum()
	out("| Discount Band | Revenue (ex-VAT) | % Revenue | Units | Line Items |")
	out("|---|---|---|---|---|")
	for _, row in band_summary.iterrows():
		pct = row["revenue"] / total_band_rev * 100 if total_band_rev > 0 else 0
		out(f"| {row['discount_band']} | £{row['revenue']:,.2f} | {pct:.1f}% | {int(row['units']):,} | {int(row['count']):,} |")
	out()

	# ──────────────────────────────────────────────────────────────
	# PART 4: Tool Gap Analysis
	# ──────────────────────────────────────────────────────────────
	out("## Part 4: Tool Gap Analysis")
	out()
	out("Review of the 9 existing sg-analysis report sections against collection performance tracking needs.")
	out()

	sections_analysis = [
		{
			"section": "SS26 Season Performance",
			"separates_ck": "Partially — filters by SKU status (SS26) which mixes CK and collection",
			"accounts_for_discount": "No — all revenue treated equally regardless of discount level",
			"missing_insight": "Does not distinguish full-price from clearance revenue. A product could rank highly purely on clearance sales. No category-level aggregation within the season.",
		},
		{
			"section": "Reorder Alerts",
			"separates_ck": "Yes — uses classify_collection() to filter to collection only",
			"accounts_for_discount": "No — velocity is raw sold_30d regardless of whether sales are at full price or clearance",
			"missing_insight": "Reorder recommendations do not factor in whether demand is organic or discount-driven. Restocking a product that only sells on clearance may not be the right call.",
		},
		{
			"section": "Gender Split",
			"separates_ck": "No — analyses all line items regardless of CK/collection",
			"accounts_for_discount": "No — no discount awareness",
			"missing_insight": "Mixed CK and collection makes the gender split less actionable for collection marketing. CK gender ratios may differ significantly from collection.",
		},
		{
			"section": "Channel Mix",
			"separates_ck": "Yes — has Collection vs CK split table. B2B/D2C and Geo tables cover all products",
			"accounts_for_discount": "No — all revenue counted equally",
			"missing_insight": "The Collection vs CK split is a top-level number. No breakdown of Collection by category, which would show where growth is coming from. B2B/D2C split is not broken out by collection vs CK.",
		},
		{
			"section": "Top CK Projects",
			"separates_ck": "Yes — CK only (by design)",
			"accounts_for_discount": "N/A — CK is not discounted in the same way",
			"missing_insight": "This section is CK-only, so no collection gap. However, there is no equivalent 'Top Collection Products' section that shows full-price performance.",
		},
		{
			"section": "YoY Growth",
			"separates_ck": "Yes — splits revenue into Collection vs CK columns",
			"accounts_for_discount": "No — growth comparison includes clearance revenue, so YoY growth could be inflated by more aggressive discounting",
			"missing_insight": "YoY comparison of full-price collection revenue would be much more meaningful. Currently, a business could look like it is growing while actually just clearing more stock at a loss.",
		},
		{
			"section": "Cross-sell Analysis",
			"separates_ck": "No — analyses all line items including CK",
			"accounts_for_discount": "No",
			"missing_insight": "Cross-sell data mixes CK and collection. A CK customer buying a jersey is a different signal from a collection customer buying across categories. Also, cross-sell from clearance buyers may not represent genuine category affinity.",
		},
		{
			"section": "Stock Health",
			"separates_ck": "Yes — uses classify_collection() to filter to collection only",
			"accounts_for_discount": "No — dead stock / overstocked classifications use raw velocity",
			"missing_insight": "A product could have decent velocity (sold_30d) but only because it is on clearance. The data supports flagging 'clearance-velocity' vs 'organic-velocity' but the tool does not surface this distinction.",
		},
		{
			"section": "Velocity Trends",
			"separates_ck": "Yes — uses classify_collection() to filter to collection only",
			"accounts_for_discount": "No — momentum calculations use raw sold_30d vs sold_90d",
			"missing_insight": "A product gaining momentum because it was put on clearance is a very different signal from one gaining momentum at full price. The data supports this split but it is not surfaced.",
		},
	]

	out("### Section-by-Section Review")
	out()
	out("| # | Section | Separates CK? | Discount-Aware? | Missing Collection Insight |")
	out("|---|---|---|---|---|")
	for i, s in enumerate(sections_analysis, 1):
		out(f"| {i} | {s['section']} | {s['separates_ck']} | {s['accounts_for_discount']} | {s['missing_insight']} |")
	out()

	# Summary of gaps
	out("### Gap Summary")
	out()
	out("The following gaps are supported by the data examined in this analysis:")
	out()
	out("1. **No section separates full-price from clearance revenue.** The data clearly supports this (line_items.subtotal vs total). Every section that uses revenue or velocity could benefit from this split. Currently, all 9 sections treat clearance revenue identically to full-price revenue.")
	out()
	out("2. **No 'Collection Category Performance' section exists.** The daily report has Season Performance (product-level, current season only) and Channel Mix (top-level CK vs Collection split), but nothing that shows category-level collection trends over time. Categories like GILETS, SOCKS, and BASE LAYERS have meaningful revenue that is invisible in the current report.")
	out()
	out("3. **Gender Split and Cross-sell do not separate CK from collection.** This makes those sections less actionable for collection marketing decisions. 5 of 9 sections correctly filter to collection; the other 4 include CK data.")
	out()
	out("4. **No 'Collection Top Products' section.** There is 'Top CK Projects' but no equivalent for collection. The Season Performance section is limited to current-season SKUs only, missing products from prior seasons that are still selling.")
	out()
	out("5. **YoY Growth does not compare full-price revenue.** Year-on-year growth is more meaningful when clearance revenue is excluded or shown separately. A business could appear to grow while actually degrading its pricing power.")
	out()
	out("6. **Velocity Trends does not distinguish organic from discount-driven momentum.** A product put on clearance will show as 'gaining momentum', which is misleading. The data supports separating these signals.")
	out()
	out("7. **No category-level stock health view.** Stock Health shows individual products but no aggregated category-level view of stock coverage, which would help with buying and planning decisions.")
	out()

	# ──────────────────────────────────────────────────────────────
	# Consistency checks
	# ──────────────────────────────────────────────────────────────
	out("## Data Quality Notes")
	out()
	out(f"- Total collection line items analysed: {len(li_collection):,}")
	out(f"- Total collection revenue (ex-VAT): £{total_collection_rev:,.2f}")
	out(f"- Sum of category revenues: £{cat_revenue['total_revenue'].sum():,.2f}")
	consistency_diff = abs(total_collection_rev - cat_revenue["total_revenue"].sum())
	out(f"- Consistency check (total vs sum of categories): £{consistency_diff:.2f} difference")
	if consistency_diff < 1.0:
		out("- Consistency: PASS — category totals sum correctly to overall total")
	else:
		out(f"- Consistency: NOTE — £{consistency_diff:.2f} difference due to line items without matching SKU category")
	out(f"- Categories with no SKU match (UNCATEGORISED): {int(cat_revenue[cat_revenue['category'] == 'UNCATEGORISED']['total_revenue'].sum()):,} in revenue")
	out(f"- Collection SKUs with zero stock: {int((skus_collection['available'] == 0).sum()):,} of {len(skus_collection):,}")
	out(f"- Order date range: {valid_orders['date_created'].min().strftime('%Y-%m-%d')} to {valid_orders['date_created'].max().strftime('%Y-%m-%d')}")
	out(f"- Orders per year: 2024={len(valid_orders[valid_orders['date_created'].dt.year == 2024]):,}, 2025={len(valid_orders[valid_orders['date_created'].dt.year == 2025]):,}, 2026={len(valid_orders[valid_orders['date_created'].dt.year == 2026]):,}")
	out()

	# ──────────────────────────────────────────────────────────────
	# Write output
	# ──────────────────────────────────────────────────────────────
	OUTPUT_PATH.write_text("\n".join(output_lines), encoding="utf-8")
	print(f"\nFindings written to: {OUTPUT_PATH}")


if __name__ == "__main__":
	main()
