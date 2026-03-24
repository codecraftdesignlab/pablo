# Custom Kit Performance Deep Dive

**Generated:** 2026-03-23 11:56
**Date range:** 2024-01-02 to 2026-03-22
**CK line items analysed:** 4915
**CK orders:** 3075
**Total CK revenue (ex-VAT):** £273,387.10
**Methodology:** Revenue = total - total_tax (ex-VAT). Clearance = >20% discount. Webshop = has transaction_id OR order number starts with 'GE'. Order statuses excluded: cancelled, refunded, pending_payment, pending, on-hold, internal, failed, trash, draft.

## Part 1: CK Project Performance

### 1.1 Top 20 Projects by Revenue

| # | Project | Revenue (ex-VAT) | Orders | Unique Order Dates | Units | First Order | Last Order | AOV |
|---|---------|-----------------|--------|-------------------|-------|-------------|------------|-----|
| 1 | READING CC | £17,335.40 | 7 | 7 | 332 | 2025-04-09 | 2026-02-09 | £2,476.49 |
| 2 | PACK | £9,227.69 | 80 | 18 | 166 | 2026-02-21 | 2026-03-10 | £115.35 |
| 3 | AUDAX UK | £6,592.89 | 130 | 107 | 160 | 2024-07-10 | 2026-03-15 | £50.71 |
| 4 | PHOENIX RISING | £6,237.59 | 72 | 31 | 108 | 2024-10-28 | 2026-03-20 | £86.63 |
| 5 | PHOENIX TRI | £6,025.58 | 68 | 44 | 125 | 2025-01-28 | 2026-02-16 | £88.61 |
| 6 | NHRC | £5,730.21 | 80 | 35 | 112 | 2024-06-04 | 2026-02-24 | £71.63 |
| 7 | ROYAL AUTOMOBILE CLUB | £5,440.00 | 1 | 1 | 136 | 2025-06-24 | 2025-06-24 | £5,440.00 |
| 8 | AEONIAN | £5,259.57 | 70 | 35 | 141 | 2024-01-31 | 2026-03-02 | £75.14 |
| 9 | MARLOW 15TH ANNIVERSARY | £5,217.72 | 149 | 37 | 152 | 2025-04-14 | 2026-02-02 | £35.02 |
| 10 | STIRLING | £5,200.62 | 36 | 15 | 155 | 2025-09-09 | 2026-03-04 | £144.46 |
| 11 | MARLOW RIDERS | £4,483.79 | 97 | 76 | 115 | 2024-01-17 | 2026-03-06 | £46.22 |
| 12 | WORLD BICYCLE RELIEF | £4,413.23 | 19 | 16 | 139 | 2025-10-14 | 2026-03-21 | £232.28 |
| 13 | CHASE THE SUN 25 | £4,387.34 | 249 | 100 | 409 | 2025-04-19 | 2026-03-22 | £17.62 |
| 14 | VELOCLINIC | £4,359.00 | 1 | 1 | 135 | 2026-02-13 | 2026-02-13 | £4,359.00 |
| 15 | Chase The Sun Hoodie | £4,220.50 | 126 | 80 | 140 | 2024-05-12 | 2026-02-17 | £33.50 |
| 16 | AUDAX CLUB BRISTOL | £4,074.75 | 1 | 1 | 88 | 2025-10-29 | 2025-10-29 | £4,074.75 |
| 17 | HMT DIRTY DOZEN | £4,004.16 | 68 | 17 | 71 | 2024-04-26 | 2024-12-19 | £58.88 |
| 18 | UKCE FREESTYLER | £3,982.33 | 57 | 12 | 58 | 2025-11-18 | 2026-03-15 | £69.87 |
| 19 | WOKINGHAM CC | £3,893.82 | 58 | 29 | 75 | 2025-06-13 | 2025-12-04 | £67.13 |
| 20 | BEALACH NA BÁ | £3,667.08 | 35 | 21 | 80 | 2025-02-20 | 2025-09-10 | £104.77 |

Total CK projects: 187
Total CK revenue (ex-VAT): £273,387.10
Top 5 projects: £45,419.15 (16.6%)
Top 10 projects: £72,267.27 (26.4%)
Top 20 projects: £113,753.27 (41.6%)

### 1.2 Project Health (Projects with >3 Orders)

| Project | Total Revenue | Orders | Recent 90d | Prior 90d | Growth | Status |
|---------|--------------|--------|-----------|----------|--------|--------|
| PACK | £9,227.69 | 80 | £9,227.69 | £0.00 | NEW | Growing |
| READING CC | £17,335.40 | 7 | £4,256.58 | £879.84 | +383.8% | Growing |
| UKCE FREESTYLER | £3,982.33 | 57 | £3,942.33 | £40.00 | +9755.8% | Growing |
| UKCE CAMBRIDGE CLASSIC | £1,875.00 | 30 | £1,835.00 | £40.00 | +4487.5% | Growing |
| MELLOW JERSEY | £3,091.32 | 4 | £1,425.00 | £0.00 | NEW | Growing |
| MAPPERLEY CC | £1,469.00 | 15 | £1,324.98 | £53.34 | +2384.0% | Growing |
| PHOENIX TRI | £6,025.58 | 68 | £1,048.13 | £291.96 | +259.0% | Growing |
| BEALACH NA BÁ 2026 | £1,013.46 | 19 | £1,013.46 | £0.00 | NEW | Growing |
| UKCE NEW FOREST CLASSIC | £849.34 | 13 | £769.34 | £80.00 | +861.7% | Growing |
| DENIZENS OF THE PEDAL | £748.77 | 11 | £748.77 | £0.00 | NEW | Growing |
| RONDE CC BLACK | £2,678.34 | 47 | £715.69 | £394.83 | +81.3% | Growing |
| LOUDOUN RC | £710.46 | 9 | £710.46 | £0.00 | NEW | Growing |
| UKCE WILTSHIRE CLASSIC | £605.00 | 9 | £605.00 | £0.00 | NEW | Growing |
| NHRC | £5,730.21 | 80 | £528.26 | £0.00 | NEW | Growing |
| CHASE THE SUN 26 | £453.28 | 6 | £453.28 | £0.00 | NEW | Growing |
| AEONIAN | £5,259.57 | 70 | £437.14 | £215.31 | +103.0% | Growing |
| PHOENIX RISING | £6,237.59 | 72 | £319.59 | £0.00 | NEW | Growing |
| RONDE CC WHITE | £2,229.72 | 51 | £286.50 | £0.00 | NEW | Growing |
| UKCE TINTO | £325.00 | 5 | £275.00 | £50.00 | +450.0% | Growing |
| STIRLING BC 25TH ANNIVERSARY | £1,788.02 | 34 | £270.00 | £125.00 | +116.0% | Growing |
| UKCE SUFFOLK SPING CLASSIC | £265.00 | 4 | £265.00 | £0.00 | NEW | Growing |
| HAMPSHIRE HILLY HUNDRED | £263.30 | 4 | £263.30 | £0.00 | NEW | Growing |
| SUN UP | £908.00 | 16 | £100.00 | £0.00 | NEW | Growing |
| MSK65 PINK | £1,816.00 | 5 | £96.00 | £0.00 | NEW | Growing |
| CYCLING UK | £3,050.12 | 48 | £76.49 | £0.00 | NEW | Growing |
| CYCLING UK HERITAGE | £1,764.20 | 48 | £66.42 | £44.61 | +48.9% | Growing |
| STIRLING BC | £893.30 | 10 | £50.00 | £0.00 | NEW | Growing |
| CYCLING UK 24 | £342.50 | 9 | £50.00 | £0.00 | NEW | Growing |
| NEWBURY VELO | £519.92 | 15 | £46.66 | £0.00 | NEW | Growing |
| BLACK | £288.00 | 24 | £24.00 | £12.00 | +100.0% | Growing |
| FREEHAND PIINK | £196.00 | 11 | £20.00 | £0.00 | NEW | Growing |
| RONDE CC | £1,504.01 | 21 | £199.98 | £186.68 | +7.1% | Stable |
| SKYSCAPE | £565.00 | 7 | £70.00 | £75.00 | -6.7% | Stable |
| MARLOW 15TH ANNIVERSARY | £5,217.72 | 149 | £42.66 | £42.66 | +0.0% | Stable |
| HMT DIRTY DOZEN | £4,004.16 | 68 | £0.00 | £0.00 | +0.0% | Stable |
| BEALACH NA BÁ | £3,667.08 | 35 | £0.00 | £0.00 | +0.0% | Stable |
| CSC | £3,172.20 | 20 | £0.00 | £0.00 | +0.0% | Stable |
| HMT RIDE DAY THE 13TH | £3,094.56 | 49 | £0.00 | £0.00 | +0.0% | Stable |
| LONDON RC | £2,515.15 | 19 | £0.00 | £0.00 | +0.0% | Stable |
| BARRACUDA TRI | £2,205.00 | 24 | £0.00 | £0.00 | +0.0% | Stable |
| TAW | £1,703.61 | 23 | £0.00 | £0.00 | +0.0% | Stable |
| MICROSOFT 25 | £1,547.93 | 17 | £0.00 | £0.00 | +0.0% | Stable |
| ROAD CC | £1,137.49 | 38 | £0.00 | £0.00 | +0.0% | Stable |
| BIKEALICIOUS | £1,063.16 | 14 | £0.00 | £0.00 | +0.0% | Stable |
| SOMER VALLEY | £1,039.62 | 17 | £0.00 | £0.00 | +0.0% | Stable |
| THORNBURY CC STANDARD | £1,022.04 | 16 | £0.00 | £0.00 | +0.0% | Stable |
| BOLDMERE BULLETS | £966.64 | 10 | £0.00 | £0.00 | +0.0% | Stable |
| BOLDMERE BULLETS DRAGON | £950.00 | 10 | £0.00 | £0.00 | +0.0% | Stable |
| THORNBURY CC SUMMER | £803.32 | 13 | £0.00 | £0.00 | +0.0% | Stable |
| MICROSOFT | £732.73 | 9 | £0.00 | £0.00 | +0.0% | Stable |
| PRJ22-003522 | £731.32 | 26 | £0.00 | £0.00 | +0.0% | Stable |
| BIKESTOW GREEN | £713.24 | 4 | £0.00 | £0.00 | +0.0% | Stable |
| NORFOLK 360 | £649.60 | 5 | £0.00 | £0.00 | +0.0% | Stable |
| Girls Alive | £603.32 | 12 | £0.00 | £0.00 | +0.0% | Stable |
| RIPPLE | £577.33 | 12 | £0.00 | £0.00 | +0.0% | Stable |
| NO LIMIT MAJORCA 25 | £549.56 | 8 | £0.00 | £0.00 | +0.0% | Stable |
| Microsoft | £451.51 | 4 | £0.00 | £0.00 | +0.0% | Stable |
| SURLY100 | £353.46 | 12 | £0.00 | £0.00 | +0.0% | Stable |
| NO LIMIT LIMITED EDITION 25 | £333.16 | 5 | £0.00 | £0.00 | +0.0% | Stable |
| COWLEY CONDORS WHITE | £325.74 | 12 | £0.00 | £0.00 | +0.0% | Stable |
| STONE CIRCLE - REBEL | £325.72 | 20 | £0.00 | £0.00 | +0.0% | Stable |
| WALTON VELO | £270.02 | 4 | £0.00 | £0.00 | +0.0% | Stable |
| RAPIDA II | £256.00 | 7 | £0.00 | £0.00 | +0.0% | Stable |
| STONE CIRCLE - JESTER | £108.32 | 8 | £0.00 | £0.00 | +0.0% | Stable |
| STONE CIRCLE = BASTARD | £99.96 | 6 | £0.00 | £0.00 | +0.0% | Stable |
| TEAL | £60.00 | 5 | £0.00 | £0.00 | +0.0% | Stable |
| VCGH RACE TEAM | £3,046.68 | 27 | £853.30 | £2,193.38 | -61.1% | Declining |
| MARLOW RIDERS | £4,483.79 | 97 | £734.20 | £1,192.21 | -38.4% | Declining |
| STIRLING | £5,200.62 | 36 | £589.96 | £2,541.70 | -76.8% | Declining |
| CHASE THE SUN 25 | £4,387.34 | 249 | £384.94 | £594.97 | -35.3% | Declining |
| CHEVALIERS CC | £2,745.41 | 37 | £355.39 | £953.34 | -62.7% | Declining |
| AUDAX UK | £6,592.89 | 130 | £186.81 | £613.98 | -69.6% | Declining |
| GIRLS THAT RIDE BIKES | £1,604.64 | 27 | £149.00 | £245.32 | -39.3% | Declining |
| VCGH | £1,854.18 | 18 | £93.34 | £1,760.84 | -94.7% | Declining |
| WORLD BICYCLE RELIEF 20TH ANNIVERSARY | £675.59 | 10 | £76.34 | £599.25 | -87.3% | Declining |
| COWLEY CONDORS | £2,417.35 | 58 | £62.66 | £122.66 | -48.9% | Declining |
| AEONIAN NAVY | £620.27 | 39 | £57.39 | £105.88 | -45.8% | Declining |
| FREEHAND BLUE | £1,475.09 | 67 | £55.00 | £157.50 | -65.1% | Declining |
| POPPY BLAZE | £1,317.61 | 20 | £55.00 | £67.50 | -18.5% | Declining |
| WORLD BICYCLE RELIEF | £4,413.23 | 19 | £51.93 | £4,361.30 | -98.8% | Declining |
| FREEHAND PINK | £790.00 | 14 | £45.00 | £178.00 | -74.7% | Declining |
| Chase The Sun Hoodie | £4,220.50 | 126 | £34.00 | £168.27 | -79.8% | Declining |
| ZINGY UNTAMED | £1,821.82 | 77 | £30.00 | £131.49 | -77.2% | Declining |
| AEONIAN WHITE | £527.88 | 37 | £21.32 | £65.70 | -67.5% | Declining |
| Chase The Sun T-Shirt | £2,117.40 | 109 | £19.34 | £118.66 | -83.7% | Declining |
| OUT VELO | £1,988.32 | 35 | £12.00 | £319.98 | -96.2% | Declining |
| COWLEY ROAD CONDORS | £1,047.58 | 130 | £10.52 | £311.75 | -96.6% | Declining |
| Girls That Ride Bikes | £73.60 | 8 | £10.00 | £49.60 | -79.8% | Declining |
| CONDORS ANNIVERSARY | £317.02 | 15 | £6.66 | £13.32 | -50.0% | Declining |
| BUBBA | £1,170.00 | 35 | £6.00 | £73.50 | -91.8% | Declining |
| WOKINGHAM CC | £3,893.82 | 58 | £0.00 | £1,179.00 | -100.0% | Declining |
| LIOS BIKES | £2,893.00 | 4 | £0.00 | £975.00 | -100.0% | Declining |
| STONE CIRCLE | £2,681.40 | 52 | £0.00 | £112.00 | -100.0% | Declining |
| RONDE CC ORANGE | £1,765.05 | 32 | £0.00 | £666.60 | -100.0% | Declining |
| GIRLS ALIVE | £1,636.23 | 26 | £0.00 | £739.51 | -100.0% | Declining |
| GIRLS THAT RIDE BIKES EVENT | £1,366.32 | 10 | £0.00 | £126.66 | -100.0% | Declining |
| AURORA | £1,197.82 | 22 | £0.00 | £45.00 | -100.0% | Declining |
| NO LIMIT PINK | £1,079.37 | 10 | £0.00 | £524.97 | -100.0% | Declining |
| THE JOLLIES | £1,023.34 | 20 | £0.00 | £1,023.34 | -100.0% | Declining |
| NO LIMIT | £867.69 | 8 | £0.00 | £212.49 | -100.0% | Declining |
| LONSDALE WHEELERS | £854.95 | 6 | £0.00 | £854.95 | -100.0% | Declining |
| NO LIMIT WHITE | £779.79 | 10 | £0.00 | £174.99 | -100.0% | Declining |
| NO LIMIT GOLD | £779.79 | 11 | £0.00 | £174.99 | -100.0% | Declining |
| STONE CIRCLE - BASTARD | £195.28 | 15 | £0.00 | £10.00 | -100.0% | Declining |
| WOKINGHAM CC BLACK | £146.14 | 9 | £0.00 | £13.34 | -100.0% | Declining |
| BIKEWAY TO HELL | £113.45 | 12 | £0.00 | £55.50 | -100.0% | Declining |
| WOKINGHAM CC WHITE | £66.70 | 5 | £0.00 | £13.34 | -100.0% | Declining |

Projects with >3 orders: 107
Growing: 31 | Stable: 35 | Declining: 41

### 1.3 New Projects (First Order in Last 90 Days)

| # | Project | Revenue | Orders | Units | First Order |
|---|---------|---------|--------|-------|-------------|
| 1 | PACK | £9,227.69 | 80 | 166 | 2026-02-21 |
| 2 | VELOCLINIC | £4,359.00 | 1 | 135 | 2026-02-13 |
| 3 | BP C2C 17 | £3,153.15 | 1 | 69 | 2026-03-05 |
| 4 | DELTA VELO | £2,109.92 | 1 | 24 | 2026-03-03 |
| 5 | BEALACH NA BÁ 2026 | £1,013.46 | 19 | 19 | 2026-02-01 |
| 6 | GS HENLEY LA REINE | £933.28 | 1 | 20 | 2026-03-10 |
| 7 | HEXAVELO | £900.00 | 1 | 12 | 2026-03-02 |
| 8 | DENIZENS OF THE PEDAL | £748.77 | 11 | 13 | 2026-03-05 |
| 9 | LOUDOUN RC | £710.46 | 9 | 13 | 2026-02-13 |
| 10 | UKCE WILTSHIRE CLASSIC | £605.00 | 9 | 9 | 2026-01-13 |
| 11 | DADS IN LYCRA 26 PINK | £592.47 | 1 | 9 | 2026-01-23 |
| 12 | DADS IN LYCRA 26 BLUE | £592.47 | 1 | 9 | 2026-01-23 |
| 13 | LUCHOS | £467.50 | 1 | 11 | 2026-02-06 |
| 14 | CHASE THE SUN 26 | £453.28 | 6 | 8 | 2026-03-21 |
| 15 | UKCE SUFFOLK SPING CLASSIC | £265.00 | 4 | 4 | 2026-02-12 |
| 16 | HAMPSHIRE HILLY HUNDRED | £263.30 | 4 | 5 | 2026-03-02 |
| 17 | CAVERSHAM VIPS | £261.30 | 1 | 8 | 2026-03-09 |
| 18 | UKCE JURASSIC CLASSIC | £190.00 | 3 | 4 | 2026-01-01 |
| 19 | JAMIE BAKER 02 | £186.66 | 1 | 3 | 2026-03-09 |
| 20 | DADS IN LYCRA 26 | £150.00 | 1 | 10 | 2026-01-23 |
| 21 | NEWBURY VELO WINNERS POLKA | £131.66 | 1 | 2 | 2026-01-06 |
| 22 | NEWBURY VELO WINNERS BLUE | £131.66 | 1 | 2 | 2026-01-06 |
| 23 | UKCE NEW FOREST TOUR | £130.00 | 3 | 3 | 2026-02-11 |
| 24 | JAMIE BAKER 01 | £120.00 | 1 | 2 | 2026-03-09 |
| 25 | LET'S GO VELO GOLD | £105.32 | 2 | 2 | 2026-02-23 |
| 26 | UKCE SURREY HILLS CLASSIC | £75.00 | 1 | 1 | 2026-03-06 |
| 27 | NEWBURY VELO WINNERS GREEN | £65.83 | 1 | 1 | 2026-01-06 |
| 28 | NEWBURY VELO WINNERS PINK | £65.83 | 1 | 1 | 2026-01-06 |
| 29 | NEWBURY VELO WINNERS YELLOW | £65.83 | 1 | 1 | 2026-01-06 |
| 30 | ZINGY | £60.00 | 1 | 1 | 2025-12-24 |

New projects in last 90 days: 34
Revenue from new projects: £28,280.82 (10.3% of CK total)

## Part 2: Webshop Performance

### 2.1 Webshop vs Non-Webshop Overview

| Metric | Webshop | Non-Webshop | Total |
|--------|---------|-------------|-------|
| Revenue (ex-VAT) | £153,318.62 | £120,068.48 | £273,387.10 |
| Revenue Share | 56.1% | 43.9% | 100.0% |
| Orders | 2809 | 266 | 3075 |
| Units | 4169 | 3812 | 7981 |
| AOV | £54.58 | £451.39 | £88.91 |

### 2.2 Webshop Project Performance

| # | Project | Webshop Revenue | Orders | Units | AOV |
|---|---------|----------------|--------|-------|-----|
| 1 | PACK | £9,227.69 | 80 | 166 | £115.35 |
| 2 | AUDAX UK | £6,376.23 | 126 | 156 | £50.60 |
| 3 | PHOENIX RISING | £6,237.59 | 71 | 107 | £87.85 |
| 4 | NHRC | £5,663.55 | 79 | 111 | £71.69 |
| 5 | PHOENIX TRI | £5,556.46 | 60 | 116 | £92.61 |
| 6 | AEONIAN | £5,259.57 | 70 | 141 | £75.14 |
| 7 | MARLOW 15TH ANNIVERSARY | £4,791.12 | 139 | 142 | £34.47 |
| 8 | CHASE THE SUN 25 | £4,332.34 | 244 | 403 | £17.76 |
| 9 | MARLOW RIDERS | £4,157.13 | 89 | 107 | £46.71 |
| 10 | Chase The Sun Hoodie | £3,980.50 | 119 | 132 | £33.45 |
| 11 | HMT DIRTY DOZEN | £3,954.16 | 67 | 70 | £59.02 |
| 12 | WOKINGHAM CC | £3,667.16 | 55 | 71 | £66.68 |
| 13 | HMT RIDE DAY THE 13TH | £3,094.56 | 49 | 52 | £63.15 |
| 14 | VCGH RACE TEAM | £3,046.68 | 27 | 42 | £112.84 |
| 15 | CSC | £2,956.86 | 19 | 75 | £155.62 |
| 16 | CHEVALIERS CC | £2,745.41 | 37 | 53 | £74.20 |
| 17 | STIRLING | £2,708.92 | 35 | 65 | £77.40 |
| 18 | RONDE CC BLACK | £2,594.99 | 46 | 58 | £56.41 |
| 19 | STONE CIRCLE | £2,403.90 | 51 | 61 | £47.14 |
| 20 | COWLEY CONDORS | £2,322.03 | 54 | 62 | £43.00 |

Total webshop projects: 127

### 2.3 Webshop Growth Trend (YTD vs Prior Year)

| Metric | 2026 YTD | 2025 LfL | Growth |
|--------|----------|----------|--------|
| Webshop Revenue | £22,460.55 | £12,130.65 | +85.2% |
| Non-Webshop Revenue | £29,349.10 | £8,418.69 | +248.6% |
| Webshop Share | 43.4% | 59.0% | -15.7% pts |

## Part 3: CK Growth Trends

### 3.1 Year-on-Year Growth

| Metric | 2026 YTD | 2025 LfL (Jan-Mar 23) | 2025 Full Year | YoY Growth (LfL) |
|--------|----------|----------|----------|----------|
| CK Revenue (ex-VAT) | £51,809.65 | £20,549.34 | £161,030.77 | +152.1% |

### 3.2 Monthly Revenue Trend

| Month | Revenue (ex-VAT) | Orders | Units | New Projects |
|-------|-----------------|--------|-------|--------------|
| 2024-01 | £2,757.18 | 65 | 92 | 24 |
| 2024-02 | £3,672.57 | 36 | 512 | 3 |
| 2024-03 | £5,083.92 | 74 | 127 | 2 |
| 2024-04 | £4,068.68 | 87 | 93 | 3 |
| 2024-05 | £6,399.66 | 154 | 201 | 6 |
| 2024-06 | £6,373.59 | 125 | 168 | 7 |
| 2024-07 | £7,390.76 | 116 | 188 | 4 |
| 2024-08 | £3,151.00 | 74 | 93 | 1 |
| 2024-09 | £7,800.46 | 84 | 563 | 6 |
| 2024-10 | £5,907.96 | 60 | 143 | 4 |
| 2024-11 | £5,838.29 | 111 | 142 | 5 |
| 2024-12 | £2,102.61 | 45 | 109 | 1 |
| 2025-01 | £3,760.31 | 39 | 78 | 3 |
| 2025-02 | £10,830.96 | 85 | 248 | 8 |
| 2025-03 | £10,393.63 | 59 | 251 | 5 |
| 2025-04 | £27,477.34 | 275 | 730 | 14 |
| 2025-05 | £9,486.40 | 193 | 344 | 4 |
| 2025-06 | £19,585.64 | 194 | 494 | 11 |
| 2025-07 | £15,905.36 | 168 | 471 | 9 |
| 2025-08 | £6,798.76 | 89 | 195 | 3 |
| 2025-09 | £22,169.30 | 211 | 544 | 13 |
| 2025-10 | £10,020.77 | 73 | 260 | 5 |
| 2025-11 | £15,339.32 | 143 | 490 | 10 |
| 2025-12 | £9,262.98 | 80 | 282 | 3 |
| 2026-01 | £13,605.03 | 107 | 328 | 10 |
| 2026-02 | £19,090.17 | 173 | 452 | 9 |
| 2026-03 | £19,114.45 | 155 | 383 | 14 |

### 3.3 New Project Acquisition Rate

| Month | New Projects | Cumulative Projects |
|-------|-------------|-------------------|
| 2024-01 | 24 | 24 |
| 2024-02 | 3 | 27 |
| 2024-03 | 2 | 29 |
| 2024-04 | 3 | 32 |
| 2024-05 | 6 | 38 |
| 2024-06 | 7 | 45 |
| 2024-07 | 4 | 49 |
| 2024-08 | 1 | 50 |
| 2024-09 | 6 | 56 |
| 2024-10 | 4 | 60 |
| 2024-11 | 5 | 65 |
| 2024-12 | 1 | 66 |
| 2025-01 | 3 | 69 |
| 2025-02 | 8 | 77 |
| 2025-03 | 5 | 82 |
| 2025-04 | 14 | 96 |
| 2025-05 | 4 | 100 |
| 2025-06 | 11 | 111 |
| 2025-07 | 9 | 120 |
| 2025-08 | 3 | 123 |
| 2025-09 | 13 | 136 |
| 2025-10 | 5 | 141 |
| 2025-11 | 10 | 151 |
| 2025-12 | 3 | 154 |
| 2026-01 | 10 | 164 |
| 2026-02 | 9 | 173 |
| 2026-03 | 14 | 187 |

Total unique projects: 187

### 3.4 Revenue Concentration

| Metric | Revenue | % of Total |
|--------|---------|-----------|
| Top 5 projects | £45,419.15 | 16.6% |
| Top 10 projects | £72,267.27 | 26.4% |
| Top 20 projects | £113,753.27 | 41.6% |
| All 187 projects | £273,387.10 | 100.0% |

Herfindahl-Hirschman Index (HHI): 0.0148 (lower = more diversified; 1.0 = single project)

## Part 4: Gender & Article Analysis

### 4.1 Gender Split

| Gender | Revenue | Share | Units | Unit Share | YTD Rev | Prior LfL | YoY Growth |
|--------|---------|-------|-------|------------|---------|----------|------------|
| MENS | £164,378.86 | 60.1% | 3067 | 38.4% | £37,771.64 | £11,900.36 | +217.4% |
| WOMENS | £66,389.05 | 24.3% | 1483 | 18.6% | £8,949.80 | £5,376.50 | +66.5% |
| NONE | £36,930.35 | 13.5% | 3292 | 41.2% | £4,199.71 | £2,118.38 | +98.3% |
| UNKNOWN | £3,933.76 | 1.4% | 66 | 0.8% | £159.32 | £881.10 | -81.9% |
| UNISEX | £1,755.08 | 0.6% | 73 | 0.9% | £729.18 | £273.00 | +167.1% |

### 4.2 Top 15 Articles by Revenue

| # | Article | Category | Revenue | Units | Projects | Orders | Description |
|---|---------|----------|---------|-------|----------|--------|-------------|
| 1 | 01.323 | UNCATEGORISED | £70,848.89 | 1368 | 92 | 845 | Ibex Everyday SS Jersey |
| 2 | 01.323W | UNCATEGORISED | £23,776.10 | 503 | 66 | 296 | Ibex Everyday SS Jersey |
| 3 | 21 | UNCATEGORISED | £15,833.12 | 306 | 38 | 160 | Ibex Bodyline Gilet |
| 4 | 01.252.0.SRL5 | JERSEYS & TOPS | £10,604.37 | 159 | 22 | 106 | Thermal LS Jersey |
| 5 | 94 | SOCKS | £9,109.55 | 792 | 25 | 315 | Printed Socks |
| 6 | 120 | JERSEYS & TOPS | £8,714.64 | 343 | 12 | 268 | Contrast Hoodie |
| 7 | 01.155.7 | UNCATEGORISED | £7,880.11 | 113 | 15 | 51 | Ibex Everyday Bib Shorts |
| 8 | 01.155.8 | SHORTS & BIBS | £7,072.48 | 93 | 8 | 80 | Ibex Everyday Bib Shorts |
| 9 | 01.147.7.BSRP | UNCATEGORISED | £6,795.79 | 58 | 7 | 32 | Ibex Advanced SS Road Race Suit |
| 10 | 8 | HEAD & NECK | £5,825.15 | 1045 | 18 | 166 | Bandido |
| 11 | 23 | UNCATEGORISED | £5,426.57 | 118 | 26 | 90 | Ibex Bodyline Gilet |
| 12 | 01.340.0.RTA1 | JERSEYS & TOPS | £5,389.15 | 110 | 7 | 13 | Kalahari Bodyline SS Jersey  |
| 13 | 51336D | JERSEYS & TOPS | £5,337.41 | 150 | 13 | 143 | Bodyline SS Jersey |
| 14 | 01.323.L | UNCATEGORISED | £4,973.13 | 100 | 12 | 18 | Ibex Everyday LS Jersey |
| 15 | 78 | HEAD & NECK | £4,541.01 | 403 | 18 | 178 | Cycling Cap |

Total unique articles with revenue: 105
Line items with no article number: 44 (£2,946.00 revenue)

### 4.3 CK Category Performance

| Category | Revenue | Share | Units | Projects | YTD Rev | Prior LfL | YoY Growth |
|----------|---------|-------|-------|----------|---------|----------|------------|
| JERSEYS & TOPS | £134,289.49 | 49.1% | 2976 | 122 | £12,516.66 | £10,213.94 | +22.5% |
| UNCATEGORISED | £65,007.82 | 23.8% | 1879 | 79 | £33,270.01 | £2,866.83 | +1060.5% |
| GILETS | £17,976.92 | 6.6% | 361 | 39 | £1,179.14 | £1,502.93 | -21.5% |
| SHORTS & BIBS | £14,506.34 | 5.3% | 204 | 28 | £925.72 | £2,496.83 | -62.9% |
| SPEED & TRI SUITS | £10,142.39 | 3.7% | 88 | 9 | £2,133.26 | £1,480.41 | +44.1% |
| HEAD & NECK | £8,371.45 | 3.1% | 1137 | 31 | £364.99 | £385.65 | -5.4% |
| SOCKS | £7,239.77 | 2.6% | 724 | 20 | £584.79 | £388.68 | +50.5% |
| JACKETS | £4,417.95 | 1.6% | 48 | 15 | £339.83 | £363.15 | -6.4% |
| RUN | £3,836.68 | 1.4% | 165 | 5 | £203.62 | £346.58 | -41.2% |
| ARM & LEG WARMERS | £3,121.71 | 1.1% | 171 | 20 | £222.02 | £425.00 | -47.8% |
| GLOVES | £1,864.92 | 0.7% | 123 | 4 | £25.00 | £75.00 | -66.7% |
| BIB-TIGHTS AND TROUSERS | £1,513.76 | 0.6% | 17 | 4 | £0.00 | £0.00 | N/A |
| BASE LAYERS | £867.62 | 0.3% | 52 | 6 | £16.00 | £0.00 | N/A |
| TOWELS | £196.13 | 0.1% | 31 | 4 | £28.61 | £4.34 | +559.2% |
| BABY NIK | £34.15 | 0.0% | 5 | 1 | £0.00 | £0.00 | N/A |

## Part 5: Discount Analysis

### 5.1 CK Full-Price vs Clearance

| Metric | Full-Price | Clearance | Total |
|--------|-----------|-----------|-------|
| Revenue (ex-VAT) | £255,250.53 | £18,136.57 | £273,387.10 |
| Revenue Share | 93.4% | 6.6% | 100.0% |
| Units | 6858 | 1123 | 7981 |

### 5.2 Discount by Project Size

| Project Size | Projects | Revenue | Clearance Rev | Clearance % | Avg Discount % |
|-------------|----------|---------|--------------|------------|----------------|
| Large (>£5k) | 10 | £72,267.27 | £5,940.69 | 8.2% | 3.9% |
| Medium (£1k-£5k) | 71 | £160,772.78 | £11,103.75 | 6.9% | 5.6% |
| Small (<£1k) | 106 | £40,347.05 | £1,092.13 | 2.7% | 3.6% |

### 5.3 Most Discounted CK Projects (Revenue > £500)

| # | Project | Revenue | Avg Discount % | Clearance % |
|---|---------|---------|---------------|------------|
| 1 | CYCLING UK | £3,050.12 | 42.2% | 53.1% |
| 2 | GIRLS THAT RIDE BIKES EVENT | £1,366.32 | 35.8% | 82.7% |
| 3 | GIRLS THAT RIDE BIKES | £1,604.64 | 31.1% | 72.8% |
| 4 | WORLD BICYCLE RELIEF | £4,413.23 | 30.8% | 59.8% |
| 5 | NORFOLK 360 | £649.60 | 30.0% | 69.3% |
| 6 | BEALACH NA BÁ | £3,667.08 | 23.3% | 44.0% |
| 7 | MARLOW 15TH ANNIVERSARY | £5,217.72 | 19.5% | 77.0% |
| 8 | MAPPERLEY CC | £1,469.00 | 16.6% | 53.0% |
| 9 | FREEHAND PINK | £790.00 | 16.4% | 11.1% |
| 10 | NHRC | £5,730.21 | 14.0% | 28.5% |
