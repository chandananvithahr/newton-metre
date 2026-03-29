# Machinery's Handbook 30th Edition — Key Data Extraction

> Source: `papers/toaz.info-machinery39s-handbook-large-print-pr_...pdf` (2896 pages, full text)
> Extracted: March 29, 2026
> Focus: Data tables directly useful for our cost estimation engine

---

## 1. Book Structure (Key Sections for Cost Estimation)

| Section | Pages | What We Need |
|---------|-------|-------------|
| Material Properties | 357-595 | UTS, hardness, machinability ratings |
| Tooling & Toolmaking | 803-1046 | Carbide grades, drill/tap/reamer specs |
| **Machining Operations** | **1047-1354** | **Speeds/feeds, power constants, econometrics** |
| **Sheet Metal Working** | **1355-1419** | **Bend allowance, blank calculations, forces** |
| Threads & Threading | 1854-2137 | Tap drill sizes, thread cutting data |
| Grinding | 1233-1310 | Grinding speeds, wheel selection |

---

## 2. Cutting Speed & Feed Tables (p.1064-1116)

### 2a. Turning — Plain Carbon & Alloy Steels (Table 1, p.1069)

Units: f = feed (0.001 in/rev → ×25.4 = mm/rev), s = speed (ft/min → ×0.3048 = m/min)

| Material | AISI/SAE | BHN | HSS (fpm) | Coated Carbide Opt f/s | Coated Carbide Avg f/s | Ceramic Opt f/s |
|----------|----------|-----|-----------|----------------------|----------------------|----------------|
| Free-machining (resulfurized) | 1212, 1213, 1215 | 100-150 | 150 | 17/1165 | 8/1295 | 15/3340 |
| Free-machining (resulfurized) | 1212, 1213, 1215 | 150-200 | 160 | 28/915 | 13/1130 | 15/1795 |
| Plain carbon | 1108, 1109, 1115, 1117, 1120, 1211 | 100-150 | 130 | 17/1090 | 8/1410 | 15/1610 |
| Medium carbon | 1132, 1137, 1140, 1144, 1151 | 175-225 | 120 | 17/865 | 8/960 | 13/1400 |
| Medium carbon | same | 275-325 | 75 | 17/720 | 8/805 | 10/1430 |
| Leaded | 11L17, 12L13, 12L14 | 100-150 | 140 | 28/915 | 13/1130 | 15/1795 |
| Alloy steels | 4130, 4140, 4340 | 175-225 | 85 | 17/735 | 8/890 | 13/1155 |
| Alloy steels | 4130, 4140, 4340 | 275-325 | 65 | 17/610 | 8/735 | 10/1070 |
| Alloy steels | 4130, 4140, 4340 | 325-375 | 50 | 15/520 | 8/620 | — |

**Conversion to our engine units (metric):**
- Feed: Opt 17 thou = 0.43 mm/rev (rough), Avg 8 thou = 0.20 mm/rev (finish)
- Speed: 865 fpm = 264 m/min (coated carbide, medium carbon steel, rough)

### 2b. Turning — Stainless Steels (Table 1, p.1074)

| Material | BHN | HSS (fpm) | Coated Carbide Opt f/s | Coated Carbide Avg f/s |
|----------|-----|-----------|----------------------|----------------------|
| Austenitic (301, 302, 304, 316) | 135-185 | 80 | 15/755 | 8/900 |
| Austenitic (301, 302, 304, 316) | 225-275 | 65 | 15/655 | 8/780 |
| Martensitic (403, 410, 420) | 135-175 | 110 | 17/765 | 8/930 |
| Martensitic (403, 410, 420) | 275-325 | 70 | 15/555 | 8/660 |
| PH (17-4PH, 15-5PH) | 150-200 | 75 | 15/635 | 8/755 |

**Metric conversions:**
- SS304 at 135-185 BHN: Coated carbide avg = 900 fpm = **274 m/min** (textbook), practical ~180-200 m/min
- SS304 rough feed: 15 thou = 0.38 mm/rev (textbook), practical ~0.25 mm/rev

### 2c. Turning — Cast Metals (Table 1, p.1075-1077)

| Material | BHN | Coated Carbide Avg s (fpm) | Ceramic Avg s (fpm) |
|----------|-----|--------------------------|---------------------|
| Gray cast iron (class 20) | 120-150 | 730 | 2355 |
| Gray cast iron (class 30) | 190-220 | 595 | 1920 |
| Gray cast iron (class 40) | 220-260 | 510 | 1690 |
| Ductile iron (60-40-18) | 140-190 | 685 | 1725 |
| Ductile iron (80-55-06) | 190-225 | 575 | 1440 |
| Malleable iron | 110-160 | 710 | 1940 |

### 2d. Turning — Copper Alloys (Table 1, p.1079)

| Material | BHN | HSS (fpm) | Coated Carbide Avg s (fpm) |
|----------|-----|-----------|--------------------------|
| Free-cutting brass (C36000) | — | 300 | 1250 |
| Bronze (C22000) | — | 200 | 800 |
| Phosphor bronze (C51000) | — | 80 | 400 |

### 2e. Turning — Titanium (Table 1, p.1080)

| Material | BHN | HSS (fpm) | Uncoated Carbide Avg s (fpm) |
|----------|-----|-----------|----------------------------|
| Ti-6Al-4V (solution treated) | 310-350 | 40 | 175 |
| Ti-6Al-4V (aged) | 340-380 | 30 | 130 |
| Commercially pure Ti | 110-150 | 95 | 325 |

---

## 3. Milling Speed & Feed Tables (p.1082-1101)

### 3a. Face Milling — Carbon & Alloy Steels (Table 10, p.1087)

| Material | BHN | Coated Carbide Opt f/s | Coated Carbide Avg f/s |
|----------|-----|----------------------|----------------------|
| Free-machining (1212, 1213) | 100-150 | 10/970 | 5/1225 |
| Plain carbon (1020, 1030) | 125-175 | 10/685 | 5/855 |
| Medium carbon (1040, 1050) | 175-225 | 10/575 | 5/740 |
| Alloy (4130, 4140, 4340) | 175-225 | 10/530 | 5/680 |
| Alloy (4130, 4140, 4340) | 275-325 | 10/405 | 5/520 |

(f = feed in thou/tooth, s = speed in fpm)

**Metric:** 4140 at 225 BHN: 680 fpm = **207 m/min**, feed 5 thou/tooth = **0.127 mm/tooth**

### 3b. End Milling (Table 11, p.1087-1091)

| Material | BHN | Coated Carbide Avg s (fpm) | Feed Avg (thou/tooth) |
|----------|-----|--------------------------|---------------------|
| 1020-1050 | 175-225 | 540 | 4 |
| 4130-4340 | 175-225 | 500 | 4 |
| 4130-4340 | 275-325 | 380 | 3 |
| SS 304, 316 | 135-185 | 375 | 3 |

### 3c. Slit/Slot Milling (Table 12, p.1085-1086)

Generally 50-70% of face milling speeds, same feeds.

---

## 4. Drilling Speed & Feed Tables (p.1102-1116)

### 4a. Drilling — Carbon & Alloy Steels (Table 15, p.1103)

| Material | BHN | HSS Speed (fpm) | HSS Feed (thou/rev) for 1/2" drill | Carbide Speed (fpm) |
|----------|-----|-----------------|----------------------------------|-------------------|
| Free-machining (1212) | 100-150 | 100 | 8 | 525 |
| Plain carbon (1020) | 125-175 | 70 | 8 | 370 |
| Medium carbon (1040) | 175-225 | 55 | 7 | 310 |
| Alloy (4130-4340) | 175-225 | 50 | 6 | 280 |
| Alloy (4130-4340) | 275-325 | 40 | 5 | 220 |
| SS 304 | 135-185 | 35 | 5 | 200 |
| Ti-6Al-4V | 310-350 | 20 | 4 | 80 |

### 4b. Reaming — Typical Speeds

Generally 50-66% of drilling speeds, 2-3× drilling feeds.

### 4c. Tapping/Threading (p.1114-1115)

| Material | HSS Tap Speed (fpm) | Carbide Speed (fpm) |
|----------|--------------------|--------------------|
| Free-machining steel | 70-90 | — |
| Medium carbon steel | 30-50 | — |
| Alloy steel | 20-35 | — |
| Stainless steel | 15-25 | — |
| Aluminum | 80-100 | — |
| Cast iron | 40-60 | — |

---

## 5. Power Constants Kp (p.1119-1125)

### Table 1a & 1b: Power Constants Using Sharp Cutting Tools

**Formula:** `Pc = Kp × C × Q × W` where:
- Pc = cutting power (hp or kW)
- Kp = power constant (hp per in³/min, or kW per cm³/s)
- C = feed factor (Table 2)
- Q = metal removal rate (in³/min or cm³/s)
- W = tool wear factor (Table 3)

| Material | BHN | Kp (inch) | Kp (SI metric) |
|----------|-----|-----------|----------------|
| **Steels** | | | |
| AISI 1020 | 150-175 | 0.62 | 1.69 |
| AISI 1040 | 175-200 | 0.72 | 1.97 |
| AISI 1050 | 200-250 | 0.82 | 2.24 |
| AISI 4130 | 180-200 | 0.62 | 1.69 |
| AISI 4140 | 200-250 | 0.88 | 2.40 |
| AISI 4340 | 250-300 | 0.98 | 2.68 |
| AISI 4340 | 300-350 | 1.20 | 3.28 |
| **Stainless** | | | |
| SS 304/316 (austenitic) | 135-185 | 0.60 | 1.64 |
| SS 304/316 (austenitic) | 175-225 | 0.72 | 1.97 |
| **Cast Metals** | | | |
| Gray cast iron (class 20) | 120-150 | 0.32 | 0.87 |
| Gray cast iron (class 30) | 190-220 | 0.42 | 1.15 |
| Gray cast iron (class 40) | 220-260 | 0.52 | 1.42 |
| Ductile iron | 140-190 | 0.72 | 1.97 |
| **Nonferrous** | | | |
| Aluminum (cast) | — | 0.25 | 0.68 |
| Aluminum (rolled, hard) | — | 0.33 | 0.90 |
| Brass (medium) | — | 0.50 | 1.36 |
| Brass (hard) | — | 0.83 | 2.27 |
| Copper (pure) | — | 0.91 | 2.48 |
| Magnesium | — | 0.10 | 0.27 |
| Ti-6Al-4V | 310-350 | 0.65 | 1.77 |
| **Tool Steels** | | | |
| Tool steel | 175-200 | 0.75 | 2.05 |
| Tool steel | 250-300 | 0.98 | 2.68 |
| Tool steel | 350-400 | 1.30 | 3.55 |
| **Superalloys** | | | |
| Inconel 700/702 | 230-330 | 1.10-1.12 | 3.00-3.06 |
| Hastelloy-B | 230 | 1.10 | 3.00 |

### Table 2: Feed Factors C for Power Constants

| Feed (mm/rev) | C factor |
|---------------|----------|
| 0.05 | 1.40 |
| 0.10 | 1.25 |
| 0.15 | 1.15 |
| 0.20 | 1.08 |
| 0.25 | 1.04 |
| 0.30 | 1.00 |
| 0.40 | 0.94 |
| 0.50 | 0.90 |
| 0.75 | 0.83 |
| 1.00 | 0.78 |

### Table 3: Tool Wear Factors W

| Operation | W factor |
|-----------|----------|
| Sharp tools (all operations) | 1.00 |
| Finish turning (light cuts) | 1.10 |
| Normal rough/semifinish turning | 1.30 |
| Extra-heavy-duty rough turning | 1.60-2.00 |
| Slab milling | 1.10 |
| End milling | 1.10 |
| Light/medium face milling | 1.10-1.25 |
| Heavy-duty face milling | 1.30-1.60 |
| Normal drilling | 1.30 |
| Drilling hard materials / dull drill | 1.50 |
| Normal broaching | 1.05-1.10 |
| Heavy-duty broaching | 1.20-1.30 |

### Table 4: Machine Tool Efficiency E

| Drive Type | E |
|-----------|---|
| Direct belt drive | 0.90 |
| Back gear drive | 0.75 |
| Geared head drive | 0.70-0.80 |
| Oil-hydraulic drive | 0.60-0.90 |

### Power Formula

```
Pc = Kp × C × Q × W           (cutting power, hp or kW)
Pm = Pc / E                    (motor power)
Q = V × f × d / 60             (MRR in cm³/s for SI, where V in m/min, f in mm, d in mm)
Q = 12 × V × f × d             (MRR in in³/min for inch, where V in fpm)
```

---

## 6. Machining Econometrics (p.1168-1230)

### Taylor Tool Life Equation
```
V × T^n = C                    (Eq. 1a)
```

Where n = Taylor slope, C = cutting speed for T = 1 min

### Extended Taylor (Colding) Equation
```
V × T^(N0 - L×ln(ECT)) × ECT^(H/4M - ln(ECT)/4M) = e^(K - H/4M)
```
5-constant model (H, K, L, M, N0) — more accurate than simple Taylor for optimization.

### Equivalent Chip Thickness (ECT)
```
ECT = Area / CEL = (f × d) / CEL
```
Where CEL = cutting edge contact length. ECT unifies all cutting variables into one parameter.

### Cost Function
```
CTOT = HR × tc/60 + (tc × CE) / (T × 60) + TRPL × HR × tc / (T × 60)
```
Where:
- HR = hourly rate ($/hr)
- tc = cutting time (s)
- CE = cost per cutting edge ($)
- T = tool life (min)
- TRPL = tool replacement time (min)

### Economic Tool Life
```
TV = (CE/HR + TRPL/60)
TE = TV × (1/n - 1)
```

### Key Insights from Econometrics Section:
1. **ECT principle:** When feed × depth of cut is constant, tool life is constant regardless of individual feed/depth values
2. **Global optimum usually at maximum feed** — true optimum often requires feeds that would break the insert
3. **Higher machine cost → higher optimal speed** — expensive machines should run faster to justify their cost
4. **Tool wear factor W = 1.30 for normal rough turning** — tools should be replaced before catastrophic failure
5. **Taylor slope n varies with ECT** — not truly constant, Colding equation more accurate

---

## 7. Sheet Metal Working (p.1355-1419)

### Bend Allowance Formulas (p.1374)

**90° bends in soft brass/copper:**
```
L = 0.55T + 1.57R                          (Eq. 32)
```

**90° bends in half-hard copper/brass, soft steel, aluminum:**
```
L = 0.64T + 1.57R                          (Eq. 33)
```

**90° bends in hard copper, cold-rolled steel, spring steel:**
```
L = 0.71T + 1.57R                          (Eq. 34)
```

Where L = length of straight stock for bend, T = thickness, R = inside bend radius

### Minimum Bend Radius (p.1374)
```
Rmin = T × (50/r - 1)                      (Eq. 30)
```
Where r = percentage reduction in tensile test (% elongation)

### Maximum Bend Radius (p.1374)
```
Rmax = T × E / (2 × YS)                    (Eq. 31)
```
Where E = modulus of elasticity, YS = yield strength

### Blanking/Punching Force (p.1369)
```
F = L × T × UTS                            (Force in lbs or N)
```
Where L = perimeter of cut, T = thickness, UTS = ultimate tensile strength

### Fine Blanking (p.1370)
Requires 3× the force of conventional blanking but produces parts with smooth, square edges (no die break).

### Deep Drawing — Blank Diameter for Cylindrical Shell (p.1382)
```
D = sqrt(d² + 4dh)                         (for simple cylinder)
```
Where D = blank diameter, d = shell diameter, h = shell height

### Springback (p.1378)
- Typically 1-5° for mild steel
- Higher for stainless, aluminum, spring steel
- Compensate by overbending

---

## 8. Material Properties — Key Tables

### Mechanical Properties of Carbon Steels (p.410-420)

| AISI | Condition | UTS (MPa) | YS (MPa) | Elongation (%) | BHN | Indian Equiv. |
|------|-----------|-----------|----------|----------------|-----|---------------|
| 1020 | HR | 450 | 330 | 36 | 131 | IS 2062 E250 |
| 1040 | HR | 590 | 370 | 25 | 170 | EN8 / C45 |
| 1045 | HR | 620 | 380 | 23 | 179 | EN8 |
| 1050 | HR | 640 | 390 | 20 | 187 | — |
| 4130 | Normalized | 670 | 430 | 25 | 197 | EN19 approx |
| 4140 | Q&T | 900-1100 | 700-900 | 12-18 | 260-330 | EN19 / 42CrMo4 |
| 4340 | Q&T | 1000-1300 | 860-1100 | 10-15 | 300-390 | EN24 / 40NiCrMo |

### Stainless Steel Properties (p.394, 403-408)

| Grade | UTS (MPa) | YS (MPa) | Elongation (%) | BHN | Machinability Rating |
|-------|-----------|----------|----------------|-----|---------------------|
| 304 | 515-620 | 205-310 | 40-60 | 150-190 | 36% (of B1112) |
| 316 | 515-620 | 205-310 | 40-55 | 150-190 | 36% |
| 410 | 480-520 | 275 | 20-30 | 155-170 | 54% |
| 17-4PH | 900-1300 | 700-1100 | 10-18 | 280-380 | 48% |

### Aluminum Alloy Properties

| Grade | Temper | UTS (MPa) | YS (MPa) | BHN |
|-------|--------|-----------|----------|-----|
| 6061 | T6 | 310 | 276 | 95 |
| 7075 | T6 | 572 | 503 | 150 |
| 2024 | T4 | 470 | 325 | 120 |

### Machinability Ratings (relative to B1112 = 100%)

| Material | Rating |
|----------|--------|
| B1112 (free-machining) | 100% |
| 1020 | 72% |
| 1040 | 64% |
| 1045 | 57% |
| 4140 | 54% |
| 4340 | 50% |
| 304 SS | 36% |
| 316 SS | 36% |
| Ti-6Al-4V | 22% |
| Inconel 718 | 12% |

---

## 9. Tolerances & Surface Finish (p.596-802)

### ISO Tolerance Grades — Typical Achievable by Process

| Process | Typical IT Grade | Tolerance for 50mm (μm) |
|---------|-----------------|------------------------|
| Lapping/honing | IT4-5 | 7-11 |
| Cylindrical grinding | IT5-7 | 11-25 |
| Boring (precision) | IT6-8 | 16-39 |
| CNC turning (finish) | IT7-9 | 25-62 |
| CNC milling | IT7-10 | 25-100 |
| Drilling | IT10-12 | 100-250 |
| Reaming | IT7-9 | 25-62 |

### Surface Roughness by Process

| Process | Ra (μm) | Ra (μin) |
|---------|---------|----------|
| Lapping | 0.025-0.2 | 1-8 |
| Cylindrical grinding | 0.1-0.8 | 4-32 |
| Honing | 0.05-0.4 | 2-16 |
| Finish turning | 0.4-3.2 | 16-125 |
| Rough turning | 3.2-12.5 | 125-500 |
| Face milling (finish) | 0.8-3.2 | 32-125 |
| End milling | 1.6-6.3 | 63-250 |
| Drilling | 1.6-6.3 | 63-250 |
| Broaching | 0.4-3.2 | 16-125 |

---

## 10. Mapping to Our Engine

### What we already have vs what Machinery's Handbook adds:

| Data Point | Our Engine | Machinery's HB | Gap? |
|-----------|-----------|---------------|------|
| Cutting speeds (turning) | Sandvik data, 9 materials | 50+ materials, 5 tool types | ⚠️ Could expand materials |
| Cutting speeds (milling) | Sandvik data | 50+ materials, face/end/slit | ⚠️ More detail available |
| Drilling speeds | Basic per-material | Per-material × drill size | ⚠️ Could add drill size factor |
| Power constants Kp | Sandvik kc1 values | Kp + feed factor + wear factor | ✅ Similar approach |
| Feed factors | Fixed feeds per process | Feed factor table C | ❌ Not using feed adjustment |
| Tool wear factor W | Not implemented | 1.00-2.00 by operation | ❌ Should add |
| Machine efficiency E | 0.80 fixed | 0.60-0.90 by drive type | ⚠️ Could vary |
| Taylor slope n | Per-material | Per-material + ECT approach | ✅ Have this |
| Machinability ratings | Per-material factor | AISI B1112 = 100% system | ✅ Similar |
| Bend allowance | K-factor approach | L = aT + 1.57R formulas | ⚠️ Different but equivalent |
| Blanking force | UTS × T × L | Same formula | ✅ Already match |
| Tolerance cost | 30% surcharge for tight | IT grade system | ⚠️ Could be more granular |

### Recommended Engine Improvements from Machinery's HB:

1. **Add tool wear factor W** to power/force calculations:
   - Rough turning: W = 1.30 (tools are never truly sharp in production)
   - Finish turning: W = 1.10
   - Drilling: W = 1.30

2. **Add feed factor C** to power calculation:
   - Small feeds (0.10 mm/rev) use 25% more specific power than baseline
   - Large feeds (0.50 mm/rev) use 10% less

3. **Expand material coverage** — our 9 materials should include:
   - EN19 (4140) — very common in Indian shops
   - Free-machining steels (12L14) — baseline comparison
   - Inconel 718 — aerospace
   - Phosphor bronze — bearings

4. **Add process-specific tolerance cost** instead of flat 30%:
   - IT7 (standard CNC finish): no surcharge
   - IT6 (precision boring): +20%
   - IT5 (grinding): +50%
   - IT4 (lapping/honing): +100%

5. **Use Machinery's Handbook as validation** — cross-check our Sandvik-derived speeds against these tables. Our speeds should be within 20% of the HB values for same BHN range.
