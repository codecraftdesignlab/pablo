# Collection Performance Deep Dive — Findings

**Generated:** 2026-03-23
**Scope:** Collection products only (CK excluded)
**Orders analysed:** 22,916 valid orders, 34,266 collection line items
**Date range:** 2024-01-01 to 2026-03-22

## Part 1: Collection Category Performance

### 1.1 Revenue by Category

| Category | Revenue (ex-VAT) | Units | SKUs | AOV |
|---|---|---|---|---|
| JERSEYS & TOPS | £414,121.84 (37.7%) | 10,931 | 4541 | £37.89 |
| BIB SHORTS | £181,790.88 (16.6%) | 3,371 | 618 | £53.93 |
| GLOVES | £106,520.06 (9.7%) | 5,855 | 360 | £18.19 |
| JACKETS | £96,372.74 (8.8%) | 1,178 | 545 | £81.81 |
| UNCATEGORISED | £71,424.77 (6.5%) | 1,704 | 0 | £41.92 |
| GILETS | £39,321.21 (3.6%) | 1,165 | 465 | £33.75 |
| BIB-TIGHTS AND TROUSERS | £36,570.51 (3.3%) | 508 | 118 | £71.99 |
| SOCKS | £34,810.27 (3.2%) | 4,997 | 354 | £6.97 |
| HEAD & NECK | £25,177.34 (2.3%) | 2,902 | 165 | £8.68 |
| SPEED & TRI SUITS | £20,951.06 (1.9%) | 242 | 288 | £86.57 |
| BASE LAYERS | £20,009.93 (1.8%) | 979 | 251 | £20.44 |
| ARM / LEG WARMERS | £9,742.26 (0.9%) | 659 | 254 | £14.78 |
| ACCESSORIES | £9,469.39 (0.9%) | 317 | 58 | £29.87 |
| RUN | £9,220.04 (0.8%) | 523 | 168 | £17.63 |
| SWIMWEAR | £5,695.39 (0.5%) | 514 | 72 | £11.08 |
| BAGS & PANNIERS | £5,106.92 (0.5%) | 196 | 12 | £26.06 |
| TOWELS | £1,886.42 (0.2%) | 198 | 39 | £9.53 |
| BOTTLES | £1,685.09 (0.2%) | 519 | 4 | £3.25 |
| HATS | £1,535.01 (0.1%) | 354 | 12 | £4.34 |
| HELMETS | £1,370.54 (0.1%) | 15 | 4 | £91.37 |
| EYEWEAR | £1,276.51 (0.1%) | 46 | 22 | £27.75 |
| MUDGUARDS | £1,007.72 (0.1%) | 234 | 3 | £4.31 |
| BABY NIK | £865.81 (0.1%) | 148 | 16 | £5.85 |
| HOODIES | £619.48 (0.1%) | 23 | 40 | £26.93 |
| TRI TOPS | £477.51 (0.0%) | 23 | 40 | £20.76 |
| BAGS | £417.90 (0.0%) | 14 | 7 | £29.85 |
| NUTRITION | £191.36 (0.0%) | 44 | 11 | £4.35 |
| SHOES & OVERSHOES | £9.33 (0.0%) | 1 | 4 | £9.33 |
| **TOTAL** | **£1,097,647.29** | **37,660** | **8471** | **£29.15** |

### 1.2 Full-Price vs Clearance Split by Category

Clearance = line item discount > 20%.

| Category | Full-Price Revenue | Clearance Revenue | Full-Price % | FP Units | CL Units |
|---|---|---|---|---|---|
| JERSEYS & TOPS | £343,994.33 | £70,127.51 | 83.1% | 8,317 | 2,614 |
| BIB SHORTS | £148,360.83 | £33,430.05 | 81.6% | 2,566 | 805 |
| GLOVES | £92,264.16 | £14,255.90 | 86.6% | 4,515 | 1,340 |
| JACKETS | £73,042.36 | £23,330.38 | 75.8% | 800 | 378 |
| UNCATEGORISED | £67,519.54 | £3,905.23 | 94.5% | 1,543 | 161 |
| GILETS | £33,749.82 | £5,571.39 | 85.8% | 939 | 226 |
| BIB-TIGHTS AND TROUSERS | £22,787.42 | £13,783.09 | 62.3% | 270 | 238 |
| SOCKS | £23,959.69 | £10,850.58 | 68.8% | 2,834 | 2,163 |
| HEAD & NECK | £17,330.87 | £7,846.47 | 68.8% | 1,693 | 1,209 |
| SPEED & TRI SUITS | £17,806.89 | £3,144.17 | 85.0% | 188 | 54 |
| BASE LAYERS | £14,625.81 | £5,384.12 | 73.1% | 659 | 320 |
| ARM / LEG WARMERS | £7,799.38 | £1,942.88 | 80.1% | 470 | 189 |
| ACCESSORIES | £8,979.81 | £489.58 | 94.8% | 266 | 51 |
| RUN | £6,909.23 | £2,310.81 | 74.9% | 371 | 152 |
| SWIMWEAR | £5,040.43 | £654.96 | 88.5% | 423 | 91 |
| BAGS & PANNIERS | £5,043.34 | £63.58 | 98.8% | 183 | 13 |
| TOWELS | £1,358.79 | £527.63 | 72.0% | 125 | 73 |
| BOTTLES | £1,499.51 | £185.58 | 89.0% | 397 | 122 |
| HATS | £1,168.66 | £366.35 | 76.1% | 230 | 124 |
| HELMETS | £1,370.54 | £0.00 | 100.0% | 15 | 0 |
| EYEWEAR | £1,100.11 | £176.40 | 86.2% | 33 | 13 |
| MUDGUARDS | £780.07 | £227.65 | 77.4% | 157 | 77 |
| BABY NIK | £570.92 | £294.89 | 65.9% | 81 | 67 |
| HOODIES | £493.04 | £126.44 | 79.6% | 16 | 7 |
| TRI TOPS | £399.45 | £78.06 | 83.7% | 18 | 5 |
| BAGS | £317.60 | £100.30 | 76.0% | 9 | 5 |
| NUTRITION | £146.00 | £45.36 | 76.3% | 26 | 18 |
| SHOES & OVERSHOES | £0.00 | £9.33 | 0.0% | 0 | 1 |
| **TOTAL** | **£898,418.60** | **£199,228.69** | **81.8%** | **27,144** | **10,516** |

### 1.3 SKU Velocity by Category (from operational data)

| Category | Sold 7d | Sold 30d | Sold 90d |
|---|---|---|---|
| JERSEYS & TOPS | 78 | 275 | 636 |
| GLOVES | 35 | 143 | 695 |
| BIB SHORTS | 17 | 88 | 257 |
| SOCKS | 38 | 87 | 187 |
| HEAD & NECK | 16 | 59 | 162 |
| GILETS | 13 | 38 | 73 |
| ACCESSORIES | 8 | 34 | 72 |
| RUN | 16 | 34 | 74 |
| JACKETS | 5 | 32 | 174 |
| UNCATEGORISED | 15 | 21 | 65 |
| BIB-TIGHTS AND TROUSERS | 8 | 21 | 94 |
| BASE LAYERS | 6 | 19 | 70 |
| ARM / LEG WARMERS | 6 | 18 | 46 |
| HATS | 1 | 17 | 35 |
| BAGS & PANNIERS | 4 | 10 | 29 |
| SWIMWEAR | 1 | 6 | 22 |
| BABY NIK | 1 | 4 | 7 |
| SPEED & TRI SUITS | 0 | 3 | 11 |
| TRI TOPS | 0 | 1 | 3 |
| EYEWEAR | 1 | 1 | 3 |
| BOTTLES | 0 | 0 | 10 |
| HOODIES | 0 | 0 | 2 |
| TOWELS | 0 | 0 | 18 |

### 1.4 Growth Signal (30d rate vs prior 60d monthly average)

Acceleration > 1.0 = category selling faster than prior period.

| Category | Sold 30d | Prior 60d Monthly Avg | Acceleration |
|---|---|---|---|
| BABY NIK | 4 | 1.5 | 2.67x |
| GILETS | 38 | 17.5 | 2.17x |
| HATS | 17 | 9.0 | 1.89x |
| ACCESSORIES | 34 | 19.0 | 1.79x |
| SOCKS | 87 | 50.0 | 1.74x |
| RUN | 34 | 20.0 | 1.70x |
| JERSEYS & TOPS | 275 | 180.5 | 1.52x |
| ARM / LEG WARMERS | 18 | 14.0 | 1.29x |
| HEAD & NECK | 59 | 51.5 | 1.15x |
| BAGS & PANNIERS | 10 | 9.5 | 1.05x |
| BIB SHORTS | 88 | 84.5 | 1.04x |
| EYEWEAR | 1 | 1.0 | 1.00x |
| TRI TOPS | 1 | 1.0 | 1.00x |
| UNCATEGORISED | 21 | 22.0 | 0.95x |
| SPEED & TRI SUITS | 3 | 4.0 | 0.75x |
| SWIMWEAR | 6 | 8.0 | 0.75x |
| BASE LAYERS | 19 | 25.5 | 0.75x |
| BIB-TIGHTS AND TROUSERS | 21 | 36.5 | 0.58x |
| GLOVES | 143 | 276.0 | 0.52x |
| JACKETS | 32 | 71.0 | 0.45x |
| BOTTLES | 0 | 5.0 | N/A |
| HOODIES | 0 | 1.0 | N/A |
| TOWELS | 0 | 9.0 | N/A |

### 1.5 Stock Position by Category

| Category | Available Units | Total SKUs | SKUs at Zero Stock | Zero Stock % |
|---|---|---|---|---|
| JERSEYS & TOPS | 1,997 | 4541 | 3902 | 86% |
| GLOVES | 1,545 | 360 | 259 | 72% |
| SOCKS | 1,520 | 354 | 296 | 84% |
| HEAD & NECK | 986 | 165 | 129 | 78% |
| BIB SHORTS | 870 | 618 | 501 | 81% |
| RUN | 477 | 168 | 23 | 14% |
| JACKETS | 406 | 545 | 456 | 84% |
| ACCESSORIES | 345 | 58 | 18 | 31% |
| UNCATEGORISED | 341 | 818 | 659 | 81% |
| BASE LAYERS | 321 | 251 | 182 | 73% |
| HATS | 287 | 12 | 5 | 42% |
| ARM / LEG WARMERS | 237 | 254 | 193 | 76% |
| GILETS | 169 | 465 | 404 | 87% |
| BIB-TIGHTS AND TROUSERS | 163 | 118 | 86 | 73% |
| SWIMWEAR | 144 | 72 | 63 | 88% |
| BAGS & PANNIERS | 116 | 12 | 10 | 83% |
| BABY NIK | 81 | 16 | 12 | 75% |
| SPEED & TRI SUITS | 63 | 288 | 269 | 93% |
| EYEWEAR | 23 | 22 | 20 | 91% |
| TRI TOPS | 15 | 40 | 32 | 80% |
| BESPOKE | 12 | 1 | 0 | 0% |
| BAGS | 0 | 7 | 7 | 100% |
| CYCLING CAPS | 0 | 2 | 2 | 100% |
| BOTTLES | 0 | 4 | 4 | 100% |
| RACE SUITS | 0 | 1 | 1 | 100% |
| MUDGUARDS | 0 | 3 | 3 | 100% |
| HOODIES | 0 | 40 | 40 | 100% |
| HELMETS | 0 | 4 | 4 | 100% |
| NUTRITION | 0 | 11 | 11 | 100% |
| SHOES & OVERSHOES | 0 | 4 | 4 | 100% |
| TOWELS | 0 | 39 | 39 | 100% |

## Part 2: Non-Jersey Growth Opportunities

### 2.1 Highest Full-Price Growth (non-jersey categories with 5+ units/30d)

| Category | Acceleration | Sold 30d | Full-Price Revenue | FP % |
|---|---|---|---|---|
| GILETS | 2.17x | 38 | £33,749.82 | 85.8% |
| HATS | 1.89x | 17 | £1,168.66 | 76.1% |
| ACCESSORIES | 1.79x | 34 | £8,979.81 | 94.8% |
| SOCKS | 1.74x | 87 | £23,959.69 | 68.8% |
| RUN | 1.70x | 34 | £6,909.23 | 74.9% |
| ARM / LEG WARMERS | 1.29x | 18 | £7,799.38 | 80.1% |
| HEAD & NECK | 1.15x | 59 | £17,330.87 | 68.8% |
| BAGS & PANNIERS | 1.05x | 10 | £5,043.34 | 98.8% |
| BIB SHORTS | 1.04x | 88 | £148,360.83 | 81.6% |
| UNCATEGORISED | 0.95x | 21 | £67,519.54 | 94.5% |
| SWIMWEAR | 0.75x | 6 | £5,040.43 | 88.5% |
| BASE LAYERS | 0.75x | 19 | £14,625.81 | 73.1% |
| BIB-TIGHTS AND TROUSERS | 0.58x | 21 | £22,787.42 | 62.3% |
| GLOVES | 0.52x | 143 | £92,264.16 | 86.6% |
| JACKETS | 0.45x | 32 | £73,042.36 | 75.8% |

### 2.2 Best Full-Price Sell-Through Rate (non-jersey)

Sell-through = sold_30d / (available + sold_30d). Higher = turning stock faster.

| Category | Sell-Through 30d | Sold 30d | Available |
|---|---|---|---|
| GILETS | 18.4% | 38 | 169 |
| BIB-TIGHTS AND TROUSERS | 11.4% | 21 | 163 |
| BIB SHORTS | 9.2% | 88 | 870 |
| ACCESSORIES | 9.0% | 34 | 345 |
| GLOVES | 8.5% | 143 | 1,545 |
| BAGS & PANNIERS | 7.9% | 10 | 116 |
| JACKETS | 7.3% | 32 | 406 |
| ARM / LEG WARMERS | 7.1% | 18 | 237 |
| RUN | 6.7% | 34 | 477 |
| TRI TOPS | 6.2% | 1 | 15 |
| UNCATEGORISED | 5.8% | 21 | 341 |
| HEAD & NECK | 5.6% | 59 | 986 |
| HATS | 5.6% | 17 | 287 |
| BASE LAYERS | 5.6% | 19 | 321 |
| SOCKS | 5.4% | 87 | 1,520 |
| BABY NIK | 4.7% | 4 | 81 |
| SPEED & TRI SUITS | 4.5% | 3 | 63 |
| EYEWEAR | 4.2% | 1 | 23 |
| SWIMWEAR | 4.0% | 6 | 144 |

### 2.3 Strong Velocity but Thin Stock (non-jersey, 5+ sold/30d, >30% SKUs at zero)

| Category | Sold 30d | Available | Zero Stock SKUs | Zero % |
|---|---|---|---|---|
| GLOVES | 143 | 1,545 | 259 | 72% |
| BIB SHORTS | 88 | 870 | 501 | 81% |
| SOCKS | 87 | 1,520 | 296 | 84% |
| HEAD & NECK | 59 | 986 | 129 | 78% |
| GILETS | 38 | 169 | 404 | 87% |
| ACCESSORIES | 34 | 345 | 18 | 31% |
| JACKETS | 32 | 406 | 456 | 84% |
| UNCATEGORISED | 21 | 341 | 659 | 81% |
| BIB-TIGHTS AND TROUSERS | 21 | 163 | 86 | 73% |
| BASE LAYERS | 19 | 321 | 182 | 73% |
| ARM / LEG WARMERS | 18 | 237 | 193 | 76% |
| HATS | 17 | 287 | 5 | 42% |
| BAGS & PANNIERS | 10 | 116 | 10 | 83% |
| SWIMWEAR | 6 | 144 | 63 | 88% |

### 2.4 Repeat Purchase Rate by Category (non-jersey, 10+ customers)

Repeat = same customer bought from this category in 2+ separate orders.

| Category | Total Customers | Repeat Customers | Repeat Rate |
|---|---|---|---|
| BIB SHORTS | 1,078 | 251 | 23.3% |
| SOCKS | 790 | 130 | 16.5% |
| GLOVES | 1,388 | 222 | 16.0% |
| JACKETS | 494 | 78 | 15.8% |
| SWIMWEAR | 166 | 23 | 13.9% |
| BIB-TIGHTS AND TROUSERS | 246 | 34 | 13.8% |
| BASE LAYERS | 356 | 49 | 13.8% |
| HEAD & NECK | 672 | 90 | 13.4% |
| GILETS | 389 | 52 | 13.4% |
| EYEWEAR | 23 | 3 | 13.0% |
| SPEED & TRI SUITS | 64 | 8 | 12.5% |
| RUN | 189 | 21 | 11.1% |
| UNCATEGORISED | 242 | 25 | 10.3% |
| TRI TOPS | 10 | 1 | 10.0% |
| NUTRITION | 11 | 1 | 9.1% |
| BOTTLES | 139 | 11 | 7.9% |
| MUDGUARDS | 104 | 8 | 7.7% |
| BABY NIK | 48 | 3 | 6.2% |
| ARM / LEG WARMERS | 235 | 14 | 6.0% |
| TOWELS | 71 | 4 | 5.6% |
| HATS | 113 | 6 | 5.3% |
| ACCESSORIES | 74 | 3 | 4.1% |
| BAGS & PANNIERS | 74 | 1 | 1.4% |
| HOODIES | 14 | 0 | 0.0% |

## Part 3: Discount Impact Analysis

### 3.1 Overall Clearance Share of Collection Revenue

- **Total collection revenue (ex-VAT):** £1,097,647.29
- **Full-price revenue:** £898,418.60 (81.8%)
- **Clearance revenue (>20% discount):** £199,228.69 (18.2%)
- **Full-price units:** 27,144
- **Clearance units:** 10,516

### 3.2 Categories Most Reliant on Discounting

Ranked by % of category revenue coming from clearance (>20% discount).

| Category | Total Revenue | Clearance Revenue | Clearance % | Full-Price % |
|---|---|---|---|---|
| SHOES & OVERSHOES | £9.33 | £9.33 | 100.0% | 0.0% |
| BIB-TIGHTS AND TROUSERS | £36,570.51 | £13,783.09 | 37.7% | 62.3% |
| BABY NIK | £865.81 | £294.89 | 34.1% | 65.9% |
| SOCKS | £34,810.27 | £10,850.58 | 31.2% | 68.8% |
| HEAD & NECK | £25,177.34 | £7,846.47 | 31.2% | 68.8% |
| TOWELS | £1,886.42 | £527.63 | 28.0% | 72.0% |
| BASE LAYERS | £20,009.93 | £5,384.12 | 26.9% | 73.1% |
| RUN | £9,220.04 | £2,310.81 | 25.1% | 74.9% |
| JACKETS | £96,372.74 | £23,330.38 | 24.2% | 75.8% |
| BAGS | £417.90 | £100.30 | 24.0% | 76.0% |
| HATS | £1,535.01 | £366.35 | 23.9% | 76.1% |
| NUTRITION | £191.36 | £45.36 | 23.7% | 76.3% |
| MUDGUARDS | £1,007.72 | £227.65 | 22.6% | 77.4% |
| HOODIES | £619.48 | £126.44 | 20.4% | 79.6% |
| ARM / LEG WARMERS | £9,742.26 | £1,942.88 | 19.9% | 80.1% |
| BIB SHORTS | £181,790.88 | £33,430.05 | 18.4% | 81.6% |
| JERSEYS & TOPS | £414,121.84 | £70,127.51 | 16.9% | 83.1% |
| TRI TOPS | £477.51 | £78.06 | 16.3% | 83.7% |
| SPEED & TRI SUITS | £20,951.06 | £3,144.17 | 15.0% | 85.0% |
| GILETS | £39,321.21 | £5,571.39 | 14.2% | 85.8% |
| EYEWEAR | £1,276.51 | £176.40 | 13.8% | 86.2% |
| GLOVES | £106,520.06 | £14,255.90 | 13.4% | 86.6% |
| SWIMWEAR | £5,695.39 | £654.96 | 11.5% | 88.5% |
| BOTTLES | £1,685.09 | £185.58 | 11.0% | 89.0% |
| UNCATEGORISED | £71,424.77 | £3,905.23 | 5.5% | 94.5% |
| ACCESSORIES | £9,469.39 | £489.58 | 5.2% | 94.8% |
| BAGS & PANNIERS | £5,106.92 | £63.58 | 1.2% | 98.8% |
| HELMETS | £1,370.54 | £0.00 | 0.0% | 100.0% |

### 3.3 Hidden Gems — Full-Price Winners in Heavily Discounted Categories

Categories with high clearance reliance (>40% clearance): SHOES & OVERSHOES

No full-price sales found in heavily discounted categories.

### 3.4 Discount Band Distribution (all collection line items)

| Discount Band | Revenue (ex-VAT) | % Revenue | Units | Line Items |
|---|---|---|---|---|
| 0% (full price) | £732,237.47 | 66.7% | 22,189 | 21,320 |
| 1-10% | £74,383.75 | 6.8% | 2,243 | 2,197 |
| 11-20% | £91,797.38 | 8.4% | 2,712 | 2,613 |
| 21-30% | £78,821.59 | 7.2% | 2,949 | 2,794 |
| 31-50% | £116,358.72 | 10.6% | 5,690 | 3,846 |
| 51-100% | £4,048.38 | 0.4% | 1,877 | 1,496 |

## Part 4: Tool Gap Analysis

Review of the 9 existing sg-analysis report sections against collection performance tracking needs.

### Section-by-Section Review

| # | Section | Separates CK? | Discount-Aware? | Missing Collection Insight |
|---|---|---|---|---|
| 1 | SS26 Season Performance | Partially — filters by SKU status (SS26) which mixes CK and collection | No — all revenue treated equally regardless of discount level | Does not distinguish full-price from clearance revenue. A product could rank highly purely on clearance sales. No category-level aggregation within the season. |
| 2 | Reorder Alerts | Yes — uses classify_collection() to filter to collection only | No — velocity is raw sold_30d regardless of whether sales are at full price or clearance | Reorder recommendations do not factor in whether demand is organic or discount-driven. Restocking a product that only sells on clearance may not be the right call. |
| 3 | Gender Split | No — analyses all line items regardless of CK/collection | No — no discount awareness | Mixed CK and collection makes the gender split less actionable for collection marketing. CK gender ratios may differ significantly from collection. |
| 4 | Channel Mix | Yes — has Collection vs CK split table. B2B/D2C and Geo tables cover all products | No — all revenue counted equally | The Collection vs CK split is a top-level number. No breakdown of Collection by category, which would show where growth is coming from. B2B/D2C split is not broken out by collection vs CK. |
| 5 | Top CK Projects | Yes — CK only (by design) | N/A — CK is not discounted in the same way | This section is CK-only, so no collection gap. However, there is no equivalent 'Top Collection Products' section that shows full-price performance. |
| 6 | YoY Growth | Yes — splits revenue into Collection vs CK columns | No — growth comparison includes clearance revenue, so YoY growth could be inflated by more aggressive discounting | YoY comparison of full-price collection revenue would be much more meaningful. Currently, a business could look like it is growing while actually just clearing more stock at a loss. |
| 7 | Cross-sell Analysis | No — analyses all line items including CK | No | Cross-sell data mixes CK and collection. A CK customer buying a jersey is a different signal from a collection customer buying across categories. Also, cross-sell from clearance buyers may not represent genuine category affinity. |
| 8 | Stock Health | Yes — uses classify_collection() to filter to collection only | No — dead stock / overstocked classifications use raw velocity | A product could have decent velocity (sold_30d) but only because it is on clearance. The data supports flagging 'clearance-velocity' vs 'organic-velocity' but the tool does not surface this distinction. |
| 9 | Velocity Trends | Yes — uses classify_collection() to filter to collection only | No — momentum calculations use raw sold_30d vs sold_90d | A product gaining momentum because it was put on clearance is a very different signal from one gaining momentum at full price. The data supports this split but it is not surfaced. |

### Gap Summary

The following gaps are supported by the data examined in this analysis:

1. **No section separates full-price from clearance revenue.** The data clearly supports this (line_items.subtotal vs total). Every section that uses revenue or velocity could benefit from this split. Currently, all 9 sections treat clearance revenue identically to full-price revenue.

2. **No 'Collection Category Performance' section exists.** The daily report has Season Performance (product-level, current season only) and Channel Mix (top-level CK vs Collection split), but nothing that shows category-level collection trends over time. Categories like GILETS, SOCKS, and BASE LAYERS have meaningful revenue that is invisible in the current report.

3. **Gender Split and Cross-sell do not separate CK from collection.** This makes those sections less actionable for collection marketing decisions. 5 of 9 sections correctly filter to collection; the other 4 include CK data.

4. **No 'Collection Top Products' section.** There is 'Top CK Projects' but no equivalent for collection. The Season Performance section is limited to current-season SKUs only, missing products from prior seasons that are still selling.

5. **YoY Growth does not compare full-price revenue.** Year-on-year growth is more meaningful when clearance revenue is excluded or shown separately. A business could appear to grow while actually degrading its pricing power.

6. **Velocity Trends does not distinguish organic from discount-driven momentum.** A product put on clearance will show as 'gaining momentum', which is misleading. The data supports separating these signals.

7. **No category-level stock health view.** Stock Health shows individual products but no aggregated category-level view of stock coverage, which would help with buying and planning decisions.

## Data Quality Notes

- Total collection line items analysed: 34,266
- Total collection revenue (ex-VAT): £1,097,647.29
- Sum of category revenues: £1,097,647.29
- Consistency check (total vs sum of categories): £0.00 difference
- Consistency: PASS — category totals sum correctly to overall total
- Categories with no SKU match (UNCATEGORISED): 71,424 in revenue
- Collection SKUs with zero stock: 7,634 of 9,293
- Order date range: 2024-01-01 to 2026-03-22
- Orders per year: 2024=10,825, 2025=10,263, 2026=1,828
