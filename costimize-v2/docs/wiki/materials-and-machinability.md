---
slug: materials-and-machinability
title: Materials and Machinability — Grades, Properties, and Cost Impact
keywords: material, machinability, kc1, specific cutting force, aluminum, steel, stainless steel, titanium, brass, cast iron, EN8, EN24, IS2062, material price, density, hardness, cutting speed, ISO material group
sources: SANDVIK-DATA-EXTRACTION.md, KENNAMETAL-DATA-EXTRACTION.md, MACHINERYS-HANDBOOK-EXTRACTION.md, material_db.py, cutting_data.py
updated: 2026-04-04
---

# Materials and Machinability

Material choice is one of the largest cost drivers in manufacturing. A part in titanium costs 5-10x more to machine than the same part in aluminum -- not just because titanium is more expensive per kg, but because it machines 10x slower, wears tools 5x faster, and requires specialized cutting parameters.

## Materials in the Database

Newton-Metre supports 9 materials with full cutting data, plus a machinability-based fallback for any material AI can identify.

| Material | Price (INR/kg) | Density (kg/m3) | Machinability | UTS (MPa) | Hardness (BHN) | AISI Equivalent |
|----------|---------------|-----------------|---------------|-----------|----------------|-----------------|
| Aluminum 6061 | ~220 | 2,700 | 0.80 | 310 | 95 | 6061-T6 |
| Mild Steel IS2062 | ~65 | 7,850 | 0.60 | 410 | 120 | AISI 1018 |
| EN8 Steel | ~75 | 7,850 | 0.50 | 600 | 180 | AISI 1045 |
| EN24 Steel | ~95 | 7,850 | 0.35 | 850 | 260 | AISI 4340 |
| Stainless Steel 304 | ~250 | 8,000 | 0.40 | 515 | 170 | AISI 304 |
| Brass IS319 | ~550 | 8,500 | 0.75 | 360 | 80 | CuZn39Pb3 |
| Copper | ~750 | 8,960 | 0.65 | 220 | 45 | C11000 |
| Cast Iron | ~55 | 7,200 | 0.55 | 250 | 200 | ASTM A48 Cl.30 |
| Titanium Grade 5 | ~3,500 | 4,430 | 0.20 | 950 | 334 | Ti-6Al-4V |

### Indian Grade Mapping (IS to AISI/ISO)

Indian drawings use IS/BIS/EN grades. Key mappings from P.N. Rao:

| Indian Grade | International Equivalent | ISO Group |
|-------------|------------------------|-----------|
| IS 2062 E250 | AISI 1018/1020 | P1 (Steel) |
| EN8 (45C8, C45) | AISI 1045 | P2 (Steel) |
| EN19 (40Cr4) | AISI 4140 | P2 (Steel) |
| EN24 (40NiCrMo6) | AISI 4340 | P2 (Steel) |
| EN31 (100Cr6) | AISI 52100 | P2 (Steel) |
| IS 319 (CuZn39Pb3) | Free-cutting brass | N3 (Non-ferrous) |

## Sandvik ISO Material Classification

The ISO P/M/K/N/S/H system is the global standard for cutting parameter selection:

| ISO Group | Material | kc1 Range (N/mm2) | Machinability |
|-----------|----------|-------------------|---------------|
| **P** | Steel | 1,500-3,100 | Varies widely |
| **M** | Stainless Steel | 1,800-2,850 | Difficult (work hardening) |
| **K** | Cast Iron | 790-1,350 | Moderate (abrasive) |
| **N** | Non-ferrous (Al, Cu, Brass) | 350-700 | Easy (Al) to moderate (Cu) |
| **S** | HRSA + Titanium | 1,300-3,100 | Very difficult |
| **H** | Hardened Steel (>45 HRC) | 2,550-4,870 | Extremely difficult |

## Specific Cutting Force (kc1)

kc1 is the specific cutting force at 1mm chip thickness (N/mm2). It is the core constant for power and force calculations.

| Material | kc1 (N/mm2) | mc | Source |
|----------|------------|-----|--------|
| Aluminum 6061 | 700 | 0.25 | Sandvik N1=600, cross-validated median 700 |
| Mild Steel IS2062 | 1,650 | 0.25 | Sandvik P1.2=1700, adjusted for IS2062 |
| EN8 Steel | 1,700 | 0.25 | Sandvik P2.1 |
| EN24 Steel | 1,900 | 0.25 | Sandvik P2.5 |
| Stainless Steel 304 | 2,050 | 0.25 | Sandvik M2=2100 |
| Brass IS319 | 750 | 0.25 | Ghosh & Mallik Uc range |
| Copper | 800 | 0.25 | Ghosh & Mallik |
| Cast Iron | 1,100 | 0.25 | Sandvik K2 |
| Titanium Grade 5 | 1,420 | 0.23 | Sandvik S4=1500 |

**How kc1 is used:** The Sandvik power formula corrects kc1 for actual chip thickness and rake angle:

```
kc = kc1 x (1/hm)^mc x (1 - gamma0/100)
Pc = (Vc x ap x fn x kc) / (60 x 10^3)  [kW]
```

### Cross-Validation: Sandvik vs Kennametal vs Machinery's Handbook

Kennametal uses unit power "p" (hp/in3/min) instead of kc1. Converting via p x 2730 = kc1 equivalent:

| Material | Sandvik kc1 | Kennametal kc1 equiv. | Match |
|----------|------------|----------------------|-------|
| AISI 1018 (IS2062) | 1,600 | 1,693 | +6% |
| AISI 1045 (EN8) | 1,700 | 1,966 | +16% |
| AISI 4340 (EN24) | 1,900 | 1,993 | +5% |
| SS 316L | 2,000 | 1,993 | -0.4% |
| Gray Cast Iron | 1,100 | 1,283 | +17% |
| Ti-6Al-4V | 1,350 | 1,693 | +25% |
| Aluminum | 600 | 819 | +37% |

Kennametal values run higher because they include more conservative assumptions (tool wear, non-ideal conditions). For Indian job shops, this is actually more realistic.

## Material Impact on Cost

A simple turned shaft (OD 50mm x L 100mm) illustrates how material drives cost:

| Material | Turning Speed (m/min) | Tool Life (min) | Relative Cost |
|----------|---------------------|-----------------|---------------|
| Aluminum 6061 | 400 (rough) | 30-60 | 1.0x (baseline) |
| Brass IS319 | 280 | 20-35 | 1.3x |
| Mild Steel IS2062 | 180 | 15-25 | 1.8x |
| EN8 Steel | 150 | 15-25 | 2.0x |
| Stainless Steel 304 | 120 | 8-15 | 2.8x |
| EN24 Steel | 100 | 10-18 | 3.2x |
| Titanium Grade 5 | 45 | 5-12 | 7-10x |

## Machinability Ratings

Based on AISI 1212 = 1.00 baseline (Machinery's Handbook / Carbide Depot):

- **Easy (>1.0):** 12L14 (1.70), 1213 (1.36), Al cold-drawn (3.60), Al cast (4.50)
- **Medium (0.5-1.0):** 1018 (0.78), EN8/1045 (0.57), 4140 (0.66), Brass (1.00)
- **Difficult (0.3-0.5):** SS 304 (0.45), EN24/4340 (0.57 mapped as EN24=0.42), 52100 (0.40)
- **Very difficult (<0.3):** D-2 tool steel (0.27), A286 superalloy (0.33)

Indian grades mapped: IS2062-E250 = 0.72, EN8 = 0.57, EN24 = 0.42, EN31 = 0.40.

## Sandvik Optimization Priority

The 15% rule from Sandvik machining economics:
- Reducing tool price by 30% saves only 1% on component cost
- Increasing tool life by 50% saves only 1%
- **Increasing cutting data by 20% saves 15%**

Optimization order: (1) maximize depth of cut, (2) maximize feed rate, (3) then optimize cutting speed.
