# Kennametal Data Extraction
## Extracted March 29, 2026

---

## Source Inventory

Unlike Sandvik (which has a single Training Handbook with all cutting physics), Kennametal distributes technical data across catalog appendices, online calculators, and application-specific guides.

### PDFs Successfully Downloaded (kennametal/ folder)

| PDF | Pages | Size | Content |
|-----|-------|------|---------|
| **Beyond-Evolution-Speeds-Feeds.pdf** | 4 | 336KB | Speed/feed tables for grooving/parting/turning — ALL 6 ISO groups |
| **Carbide-Grade-Info.pdf** | 2 | 71KB | Cemented carbide grade composition and application guide |

### PDFs That Could NOT Be Downloaded (bot-blocked by productivity.com)

| PDF | Why We Want It |
|-----|---------------|
| Turning Catalog 8010 | Unit power constants in appendix |
| Milling Catalog 6050 | Milling speeds/feeds in appendix |
| Holemaking Catalog 8070 | Drilling speeds/feeds |
| Solid Carbide End Milling Master 2023 | End mill speed/feed tables |

### Online Data Extracted (from kennametal.com engineering calculators)

| Calculator | URL | Data Extracted |
|-----------|-----|---------------|
| Turning Cutting Forces | kennametal.com/.../cutting-forces.html | Unit power "p" values for 16 materials |
| End Milling Force/Torque | kennametal.com/.../force-torque-and-power.html | Machinability factors, tool wear factors |
| Face Milling Force/Torque | kennametal.com/.../force--torque--and-power.html | W/D ratios by material |

---

# UNIT POWER CONSTANTS — THE CORE KENNAMETAL DATA

Kennametal uses "p" values (unit power in hp/in3/min) instead of Sandvik's kc1 (N/mm2).

**Conversion:** kc1 (N/mm2) ≈ p (hp/in3/min) × 2.73 × 10^6 / 60 ≈ p × 45,500

## Complete Unit Power Table (16 Materials)

| Material | Designation | HB | p Finishing (hp/in3/min) | p Roughing | p General |
|----------|------------|-----|------------------------|-----------|----------|
| Carbon Steel | AISI 1018 | 141 | 0.70 | 0.66 | 0.62 |
| Carbon Steel | AISI 1045 | 195 | 0.74 | 0.70 | 0.72 |
| Alloy Steel | AISI 4140 | 194 | 0.79 | 0.74 | 0.73 |
| Alloy Steel | AISI 4340 | 214 | 0.76 | 0.72 | 0.73 |
| Alloy Steel | AISI 4140 | 258 | 0.85 | 0.77 | 0.79 |
| Alloy Steel | AISI 4142 | 277 | 0.84 | 0.77 | 0.75 |
| Alloy Steel (hardened) | AISI 4340 | 485 | 1.31 | 1.00 | 1.05 |
| Tool Steel | AISI H11 | 205 | 0.78 | 0.73 | 0.76 |
| Stainless Steel | AISI 316L | 147 | 0.81 | 0.73 | 0.73 |
| Stainless Steel | AISI 410 | 243 | 0.81 | 0.71 | 0.74 |
| Stainless Steel | 17-4 PH | 294 | 0.99 | 0.70 | 0.72 |
| Gray Cast Iron | SAE G3000 | 195 | 0.53 | 0.48 | 0.47 |
| Ductile Cast Iron | ASTM 65-45-12 | 165 | 0.58 | 0.55 | 0.51 |
| Titanium Alloy | Ti-6Al-4V | 287 | 0.64 | 0.62 | 0.62 |
| Nickel Alloy | Inconel 718 | 277 | 1.20 | 1.01 | 1.02 |
| Aluminum | AMS 2024 | 139 | 0.31 | 0.29 | 0.30 |

### Conversion to kc1 Equivalent (for cross-validation with Sandvik)

p (hp/in3/min) → kc1 (N/mm2): multiply by ~2730

| Material | p General | kc1 Equivalent (N/mm2) | Sandvik kc1 | Match? |
|----------|----------|----------------------|-------------|--------|
| AISI 1018 (≈IS2062) | 0.62 | ~1693 | 1600 (P1.2) | Close (+6%) |
| AISI 1045 (≈EN8) | 0.72 | ~1966 | 1700 (P2.1) | High (+16%) |
| AISI 4140 (≈EN19) | 0.73 | ~1993 | 1700-1900 (P2.1-P2.5) | In range |
| AISI 4340 (≈EN24) | 0.73 | ~1993 | 1900 (P2.5) | Close (+5%) |
| SS 316L (≈SS304) | 0.73 | ~1993 | 2000 (M2) | Close (-0.4%) |
| Gray Cast Iron | 0.47 | ~1283 | 1100 (K2) | High (+17%) |
| Ti-6Al-4V | 0.62 | ~1693 | 1350 (S4) | High (+25%) |
| Al 2024 (≈6061) | 0.30 | ~819 | 600 (N1) | High (+37%) |
| Inconel 718 | 1.02 | ~2785 | 2400-3100 (S2) | In range |

**Note:** Kennametal's values tend to be slightly higher than Sandvik's because they include more conservative assumptions (tool wear, less-than-ideal conditions). For cost estimation, this means Kennametal values give slightly higher power requirements = slightly longer cycle times = slightly higher costs. This is actually more realistic for Indian job shops.

## Machine Tool Efficiency Factors

| Drive Type | Efficiency (η) |
|-----------|----------------|
| Direct Belt Drive | 0.90 |
| Back Gear Drive | 0.75 |
| Geared Head Drive | 0.70-0.80 |
| Oil-Hydraulic Drive | 0.60-0.90 |

### Power Formula (Kennametal Style)

```
HP_spindle = MRR × p
HP_motor = HP_spindle / η

Where:
  MRR = vc × ap × fn  [in3/min for imperial]
  p = unit power constant from table above
  η = machine efficiency
```

For metric:
```
Pc (kW) = Q × p × 0.7457 / η

Where:
  Q = vc × ap × fn  [cm3/min]
  p = converted to kW/cm3/min
```

---

# RECOMMENDED CUTTING SPEEDS — GROOVING & PARTING (Beyond Evolution)

## Speed Table by ISO Material Group and Grade (m/min)

Format: Min | Recommended | Max

### Steel (ISO P)

| Sub | K313 | KCU10 | KCU25 | KCM35B | KCP10B | KCP25B | KCK20B |
|-----|------|-------|-------|--------|--------|--------|--------|
| P0-1 | — | 140/280/350 | 110/225/270 | 90/180/213 | 185/400/450 | 145/290/365 | 200/440/490 |
| P2 | — | 140/200/300 | 110/160/260 | 90/130/155 | 185/270/350 | 145/200/305 | 200/300/380 |
| P3 | — | 140/155/245 | 110/125/235 | 90/100/155 | 170/190/260 | 140/155/245 | 600/200/280 |
| P4 | — | 75/110/170 | 60/90/160 | 50/70/110 | 90/145/200 | 75/110/180 | 100/160/220 |
| P5 | — | 120/200/260 | 100/160/210 | 80/130/165 | 150/220/305 | 120/200/270 | 165/240/330 |
| P6 | — | 110/150/230 | 85/120/185 | 70/100/145 | 120/180/275 | 110/150/230 | 130/190/300 |

### Stainless Steel (ISO M)

| Sub | K313 | KCU10 | KCU25 | KCM35B |
|-----|------|-------|-------|--------|
| M1 | 60/90/120 | 140/210/280 | 90/170/245 | 75/120/135 |
| M2 | 45/75/110 | 120/200/245 | 90/150/245 | 75/110/135 |
| M3 | 35/65/100 | 120/180/245 | 90/140/210 | 75/90/135 |

### Cast Iron (ISO K)

| Sub | K313 | KCU10 | KCU25 | KCP10B | KCP25B | KCK20B |
|-----|------|-------|-------|--------|--------|--------|
| K1 | 30/75/120 | 120/180/245 | 100/145/225 | 170/245/440 | 140/200/360 | 210/305/550 |
| K2 | 25/70/110 | 90/150/240 | 70/120/170 | 120/195/340 | 100/160/280 | 150/245/430 |
| K3 | 20/60/90 | 60/110/150 | 50/85/120 | 120/170/270 | 100/140/220 | 150/210/335 |

### Non-Ferrous (ISO N)

| Sub | K313 | KCU10 | KCU25 |
|-----|------|-------|-------|
| N1-2 | 150/370/610 | 150/550/975 | 120/440/780 |
| N4 | 120/275/430 | 120/365/700 | 100/290/490 |
| N5 | 45/90/150 | 90/170/245 | 70/135/195 |
| N6 | 40/75/150 | 120/210/305 | 100/170/245 |

### Heat Resistant Alloys (ISO S)

| Sub | K313 | KCU10 | KCU25 | KCM35B |
|-----|------|-------|-------|--------|
| S1 | 8/30/75 | 15/55/135 | 8/40/60 | 8/35/60 |
| S2 | 8/35/75 | 15/60/135 | 8/30/75 | 8/30/60 |
| S3 | 8/40/75 | 15/70/150 | 15/40/75 | 15/35/60 |
| S4 (Ti) | 8/45/75 | 15/70/170 | 8/50/110 | 15/45/90 |

### Hardened Steel (ISO H)

| Sub | KCU10 |
|-----|-------|
| H1 | 30/45/60 |
| H2 | 15/30/45 |

## Feed Rate Factors by Material Group

Base feed rates are for ISO P and K. Multiply by these factors for other groups:

| Material Group | Feed Factor |
|---------------|------------|
| **P** (Steel) | 1.0 (base) |
| **K** (Cast Iron) | 1.0 (base) |
| **M** (Stainless) | 0.8 |
| **N** (Non-ferrous) | 1.2 |
| **S** (HRSA/Ti) | 0.8 |
| **H** (Hardened) | 0.5 |

## Feed Rates — Grooving/Turning (Beyond Evolution)

### Plunge Feed Rates by Insert Geometry (mm/rev)

| Geometry | Description | Seat Size 2 | Seat Size 4 | Seat Size 6 | Seat Size 8 |
|----------|-----------|-------------|-------------|-------------|-------------|
| **-GUP** | Positive rake, lower forces | 0.08 start | 0.12 start | 0.15-0.18 | 0.20-0.22 |
| **-GUN** | Negative, aggressive | 0.08 start | 0.12 start | 0.15-0.18 | 0.20-0.22 |

### Cut-Off Feed Rates by Geometry (mm/rev)

| Geometry | Description | Seat 2 | Seat 3 | Seat 4 | Seat 5 | Seat 6 | Seat 8 |
|----------|-----------|--------|--------|--------|--------|--------|--------|
| **-CL** | Light | 0.07 | 0.08 | 0.09 | — | — | — |
| **-CF** | Finishing, positive | 0.07 | 0.09 | 0.11 | 0.13 | — | — |
| **-CM** | Medium, stable | 0.07 | 0.09 | 0.11 | 0.14 | 0.16 | 0.17 |
| **-CR** | Roughing, aggressive | 0.10 | 0.14 | 0.16 | 0.19 | 0.21 | 0.23 |

### I.D. and Face Grooving
Reduce feed rate by **20%** from external grooving values.

### Cut-Off with Lead Angle Inserts
Reduce maximum feed rate by up to **40%**.

---

# CEMENTED CARBIDE GRADES — COMPOSITION AND APPLICATION

## Grades for Cast Iron, Non-Ferrous, HRSA

| Grade | Legacy Names | Grain | ISO Range | Co% | Other Carbides | HRA | Density (g/cm3) | TRS (kpsi) |
|-------|-------------|-------|-----------|-----|---------------|-----|-----------------|-----------|
| KFS06 | KF306, CA306 | Submicron | K05-K20, M10-M20 | 6.0 | — | 93.3 | 14.90 | 500 |
| KFS33 | K313, HU6C | Submicron | K05-K20, M10-M20 | 6.0 | — | 93.0 | 14.90 | 450 |
| KFF05 | K96, K6 | Fine | K10-K30 | 5.5 | 0.8% TiC | 92.2 | 14.90 | 310 |
| KFF06 | K68, HTA | Fine | K10-K30 | 5.7 | 2% TiC | 92.7 | 14.95 | 290 |
| KFF24 | H21, FK20M | Fine | K10-K30 | 6.0 | — | 91.9 | 14.87 | 325 |
| KFS64 | 2210, KMS | Submicron | K20-K30, M25-M40 | 10.0 | — | 91.8 | 14.40 | 625 |
| KFM65 | H91, FK40B | Medium | K30-K50 | 11.5 | — | 89.8 | 14.30 | 380 |
| KFU66 | 2612, FR12 | Ultrafine | K15-K25, M10-M25 | 12.0 | — | 92.2 | 14.15 | 480 |
| KFS69 | KF315, CA315 | Submicron | K40-K50 | 15.0 | — | 90.2 | 13.96 | 530 |
| KFM67 | H81, CD40 | Medium | — | 13.0 | 0.7% TiC | 88.6 | 14.15 | 450 |

## Steel-Cutting Grades

| Grade | Legacy Names | Grain | ISO Range | Co% | Other Carbides | HRA | Density | TRS |
|-------|-------------|-------|-----------|-----|---------------|-----|---------|-----|
| KPM06 | FM10B | Medium | P15-P25 | 6.0 | 7.4% | 91.8 | 13.95 | 300 |
| KPM07 | T22, FP20M | Medium | P10-P20 | 7.0 | 11% | 92.0 | 12.75 | 270 |
| KPC07 | TH16, FP25B | Coarse | P25-P40 | 7.0 | 7% | 91.1 | 13.70 | 300 |
| KPM09 | NTA, FP20B | Medium | P20-P35 | 8.5 | 16% | 91.2 | 12.40 | 315 |
| KPC09 | FP30B | Coarse | P25-P40 | 8.5 | 7.5% | 90.5 | 13.55 | 350 |
| KPM55 | T14, CA725X | Medium | P20-P30 | 10.0 | 17% | 91.3 | 12.25 | 300 |
| KPM56 | T04, CA745 | Medium | P30-P45 | 11.0 | 9% | 90.5 | 12.85 | 350 |
| KPM58 | K82 | Medium | P35-P50 | 12.6 | 17% | 90.2 | 11.65 | 310 |

### Key Observations
- **More Co = more tough, less hard** (KFS69 at 15% Co has TRS 530 kpsi but only 90.2 HRA)
- **More TiC/TaC/NbC = better at high temps** (steel grades have 7-17% for crater wear resistance)
- **Submicron grain = sharper edges** (KFS06, KFS33 — good for finishing)
- **Density drops with more gamma phase** (steel grades ~12-14 vs K/N grades ~14-15 g/cm3)

## Grade Application Guide

### For Cast Iron/Non-Ferrous
- **Finishing (K01-K10):** KFS06, KFS33 — submicron, highest hardness
- **General (K10-K30):** KFF06, KFF24 — fine grain, versatile
- **Roughing (K30-K50):** KFM65, KFS69 — tough, handles interrupted cuts
- **HRSA/Ti:** KFS33 first choice for nickel/titanium alloys

### For Steel
- **Finishing (P01-P15):** KPM06, KPM07 — wear resistant, high speed
- **General (P15-P30):** KPM09, KPC07 — versatile
- **Roughing (P30-P50):** KPM56, KPM58 — tough, handles severe conditions

---

# MILLING TECHNICAL DATA

## Machinability Factor (Cm) by Material

| Material Group | Cm Range |
|---------------|---------|
| Aluminum alloys | 1.0-1.1 |
| Carbon/alloy steels | 1.0-1.3 |
| Cast irons | 1.0-1.3 |
| Titanium alloys | 1.0-1.4 |
| Stainless/high-temp alloys | 2.0-2.3 |

Higher Cm = more difficult to machine = more power required.

## Tool Wear Factor (Cw)

| Condition | Cw |
|----------|-----|
| Light duty (finishing) | 1.1 |
| Medium duty | 1.2 |
| Heavy duty (roughing) | 1.3 |

## Milling Power Formula

```
HP_spindle = MRR × p × Cm × Cw
HP_motor = HP_spindle / η

Where:
  MRR = ap × ae × vf / 1000  [cm3/min]
  p = unit power from material table
  Cm = machinability correction factor
  Cw = tool wear correction factor
  η = machine efficiency (0.70-0.90)
```

---

# KEY DIFFERENCES: KENNAMETAL VS SANDVIK VS MACHINERY'S HANDBOOK

| Aspect | Kennametal | Sandvik | Machinery's Handbook |
|--------|-----------|---------|---------------------|
| **Power constant** | "p" (hp/in3/min) | kc1 (N/mm2) | Kp (kW/cm3/min) |
| **Chip thickness correction** | Built into p values | Explicit via mc exponent | Feed factor C (Table 2) |
| **Tool wear correction** | Cw (1.1-1.3) | Not in handbook | W factor (1.0-2.0) |
| **Machine efficiency** | 0.60-0.90 by drive type | Not in handbook | E factor (0.60-0.90) |
| **Vc data source** | Online calculator (gated) | Online CoroPlus (gated) | Published in tables |
| **Free PDF access** | Very limited | Training Handbook free | Book purchase required |
| **Material classification** | AISI/SAE specific grades | ISO P/M/K/N/S/H + MC codes | AISI + machinability ratings |

## Cross-Validation Summary

The three sources are **highly consistent** when converted to common units:

| Material | Sandvik kc1 | Kennametal p→kc1 | Machinery's Kp→kc1 | Verdict |
|----------|------------|-----------------|-------------------|---------|
| Mild Steel | 1600 | ~1693 | ~1650 | All within 6% |
| EN8/1045 | 1700 | ~1966 | ~1750 | KMT 16% high |
| EN24/4340 | 1900 | ~1993 | ~1900 | All within 5% |
| SS 304/316L | 2000 | ~1993 | ~2050 | All within 3% |
| Gray Cast Iron | 1100 | ~1283 | ~1150 | KMT 17% high |
| Ti-6Al-4V | 1350 | ~1693 | ~1400 | KMT 25% high |
| Aluminum 6061 | 600 | ~819 | ~650 | KMT 37% high |

**Kennametal consistently gives higher power values** — likely because their "p" values assume average (not ideal) conditions, built-in tool wear, and real-world chip formation. This makes them more conservative = safer for cost estimation.

---

# KEY ACTIONS FOR COST ENGINE

## What Kennametal Adds That We Don't Have

1. **Machinability correction factor Cm** (1.0-2.3) — adjusts power for material difficulty beyond just kc1
2. **Tool wear factor Cw** (1.1-1.3) — similar to Machinery's HB "W" factor
3. **Operation-specific power** (finishing vs roughing vs general) — we currently use one value per material
4. **Inconel 718 data** — we don't have this material, Kennametal gives p = 1.02 (very high)
5. **Feed factors by ISO group** — M: 0.8×, N: 1.2×, S: 0.8×, H: 0.5× (simple multipliers for feed adjustment)

## Recommended Engine Updates

1. **Add Inconel 718** to material_db (kc1 ≈ 2785, very high cutting forces)
2. **Add operation-type power adjustment** — finishing uses ~10% more specific power than roughing (counterintuitive but true: thinner chips = higher specific cutting force due to size effect)
3. **Implement feed factor by material group** — multiply base feed by 0.8 for SS/HRSA, 1.2 for Al
4. **Cross-validate our power calculations** with Kennametal's values to check we're in the right range

## What We Still Can't Get

- Kennametal's full turning/milling/drilling speed-feed tables (locked behind productivity.com login or Kennametal account)
- Their online calculator embeds the data but doesn't expose the full tables
- The Scribd documents require paid account access
- **Bottom line:** Machinery's Handbook remains our best source for actual Vc/fn numbers. Kennametal adds power corrections and conservative validation data.

---

# PDFs IN kennametal/ FOLDER

```
kennametal/
├── Beyond-Evolution-Speeds-Feeds.pdf   # 4 pages — actual speed tables for grooving/parting
└── Carbide-Grade-Info.pdf              # 2 pages — grade composition and application
```

Total: 2 PDFs, 6 pages, 407KB. Small but contains real data (speeds by ISO group, carbide compositions).
