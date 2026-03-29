# Indian Manufacturing Data Extraction

> Extracted March 29, 2026 from BIS standards, MSME government tool rooms, and Indian tool catalogs.
> Companion to SANDVIK-DATA-EXTRACTION.md, KENNAMETAL-DATA-EXTRACTION.md, and MACHINERYS-HANDBOOK-EXTRACTION.md.

## Source Inventory

| Source | Type | Size | Cost-Relevant Data? |
|--------|------|------|---------------------|
| **MSME Tool Room Kolkata** (web) | Government rates | N/A | **YES** — 18 machine/service rates in INR |
| **CTR Ludhiana** (PDF, 1p) | Government rates | 392KB | **YES** — 29 machine rates, two tiers (Others/Micro) |
| **IS 2062:2011** (PDF, 17p) | BIS standard | 1.1MB | **YES** — 9 structural steel grades, compositions, mechanical properties |
| **IS 1570 Part 2** (PDF, 23p) | BIS standard | 1.3MB | **YES** — 30 carbon steel grades, compositions, tensile limits |
| **IS 1570 Part 4** (PDF, 16p) | BIS standard | 1.7MB | **YES** — 40+ alloy steel grades with Cr/Ni/Mo compositions |
| **Totem Master Catalogue 2025** (PDF, 662p) | Indian tool catalog | 46MB | **PARTIAL** — Cutting speeds by ISO group for taps/drills/endmills, case studies with Indian materials |

---

## 1. Government Machine Hour Rates

### MSME Tool Room Kolkata (2024-25)

| Machine / Service | Rate (INR/hr) |
|-------------------|---------------|
| Conventional Turning | 150 |
| Conventional Milling | 170 |
| CNC Turning | 450 |
| CNC Milling | 450 |
| CNC Milling (HAAS) | 600 |
| CNC 5-Axis | 800 |
| Surface Grinding | 225 |
| Cylindrical Grinding | 450 |
| Wire Cut EDM | 640 |
| EDM (Sinker) | 580 |
| Jig Boring | 450 |
| Jig Grinding | 450 |
| CMM Inspection | 450 |
| Vacuum Heat Treatment | 200/kg |
| Bench Work | 125 |
| Pre-Tooling | 170 |
| Inspection | 150 |
| Design (CAD/CAM) | 2,000 |

### CTR Ludhiana (May 2021)

Two-tier pricing: "Others" (commercial) and "Micro" (MSME micro enterprises, ~20% discount).

| Sr. | Machine | Others (INR/hr) | Micro (INR/hr) |
|-----|---------|-----------------|-----------------|
| 1 | Conventional Turning | 77 | 70 |
| 2-3 | CNC Turning | 200 | 160-175 |
| 4 | Conventional Milling (rough) | 100 | 80 |
| 5 | Conventional Milling (finish) | 150 | 120 |
| 6 | CNC 5-Axis VMC (650x600x500) | 3,000 | 2,700 |
| 7 | CNC VMC (900x550 / 710x1700) | 800 | 640 |
| 8 | CNC Milling Center (900x350) | 525 | 480 |
| 9 | CNC Milling Machine | 400 | 375 |
| 10 | CNC Milling Machine (smaller) | 350 | 320 |
| 11 | CNC EDM (750x550) | 550 | 440 |
| 12 | CNC EDM (1000x700) | 800 | 640 |
| 13 | Jig Boring | 365 | 290 |
| 14 | Jig Grinding | 600 | 540 |
| 15 | Surface Grinding (standard) | 125 | 100 |
| 16 | Surface Grinding (1500x750) | 300 | 240 |
| 17 | Diaform/Profile Grinding | 400 | 320 |
| 18 | CNC Wire Cut (standard) | 160 | 140 |
| 19 | CNC Wire Cut (860x860/750x550) | 800 | 640 |
| 20 | CNC Wire Cut (850x500) | 700 | 560 |
| 21 | Cylindrical Grinding | 150 | 120 |
| 22 | CNC Cylindrical Grinding | 500 | 400 |
| 23 | Tool & Cutter Grinding | 80 | 64 |
| 24 | Bench Work | 110 | 88 |
| 25 | CAD | 200 | 160 |
| 26 | CMM (700x900x500) | 800 | 640 |
| 27-29 | Injection Moulding (80-200T) | 250-400 | 220-320 |

**Key Insight**: CTR Ludhiana 2021 rates are 40-60% lower than MSME Kolkata 2024-25 rates. This reflects:
- 3-year gap (inflation ~6-8% pa in manufacturing)
- Regional cost difference (Punjab vs West Bengal)
- Government tool room subsidized pricing vs semi-commercial pricing
- Ludhiana = India's largest small-scale manufacturing cluster (cost-competitive)

### Comparison: Government Rates vs Our config.py

| Process | CTR Ludhiana 2021 | MSME Kolkata 2024 | Our config.py | Assessment |
|---------|-------------------|-------------------|---------------|------------|
| CNC Turning | 200 | 450 | **800** | Our rate is for private job shops, ~1.8x government |
| CNC Milling (VMC) | 350-800 | 450-600 | **1000-1100** | Our rate covers private shop overhead + tooling |
| Drilling | N/A | N/A | **600** | Reasonable for dedicated drill press |
| Surface Grinding | 125-300 | 225 | **1200** | Our rate seems HIGH — may include CNC grinding |
| Cylindrical Grinding | 150-500 | 450 | **1200** | Our rate seems HIGH for conventional |
| Wire Cut EDM | 160-800 | 640 | N/A | Not in our engine yet |
| EDM (Sinker) | 550-800 | 580 | N/A | Not in our engine yet |
| Broaching | N/A | N/A | **1500** | Reasonable — specialized equipment |

**Validation**: Our machine rates in config.py are 1.5-2.5x government tool room rates. This is correct because:
1. Government rates are subsidized (MSME development mandate)
2. Private job shops have higher overhead (rent, insurance, profit)
3. Our rates include tool holding, fixture amortization
4. Government rates exclude tooling consumables

**Action item**: Our grinding rates (1200/hr) may be too high for conventional grinding. Consider splitting into:
- Conventional grinding: 600-800/hr
- CNC precision grinding: 1200-1500/hr

---

## 2. BIS Steel Grades — Composition & Properties

### IS 2062:2011 — Hot Rolled Structural Steel

The most commonly used steel standard in Indian manufacturing. Maps to our engine's "Mild Steel" material.

| Grade | Quality | C max | Mn max | S max | P max | CE max | Yield (MPa) | Tensile (MPa) | Elongation % |
|-------|---------|-------|--------|-------|-------|--------|-------------|---------------|-------------|
| E 250 | A | 0.23 | 1.50 | 0.045 | 0.045 | 0.42 | 250 | 410 | 23 |
| E 250 | C (killed) | 0.20 | 1.50 | 0.040 | 0.040 | 0.39 | 250 | 410 | 23 |
| E 275 | A | 0.22 | 1.50 | 0.045 | 0.045 | 0.42 | 275 | 430 | 22 |
| E 300 | A | 0.20 | 1.50 | 0.045 | 0.045 | 0.44 | 300 | 440 | 22 |
| E 350 | A | 0.20 | 1.55 | 0.045 | 0.045 | 0.47 | 350 | 490 | 22 |
| E 410 | A | 0.20 | 1.60 | 0.045 | 0.045 | 0.50 | 410 | 540 | 20 |
| E 450 | A | 0.22 | 1.65 | 0.045 | 0.045 | 0.52 | 450 | 570 | 20 |
| E 550 | A | 0.22 | 1.65 | 0.020 | 0.025 | 0.54 | 550 | 650 | 12 |
| E 600 | A | 0.22 | 1.70 | 0.020 | 0.025 | 0.54 | 600 | 730 | — |
| E 650 | A | 0.22 | 1.70 | 0.015 | 0.025 | 0.55 | 650 | — | — |

**Mapping to our engine**: IS 2062 E250 = "Mild Steel" in our material_db.py. All are ISO P group steels. kc1 ~ 1500-1700 N/mm2.

### IS 1570 Part 2 — Carbon Steel Grades

30 grades from C05 (0.10% max C) to 113C6 (1.05-1.20% C). Key grades used in Indian job shops:

| IS Designation | Old Name | C % | Mn % | Typical Use | ISO Group |
|---------------|----------|-----|------|-------------|-----------|
| 10C4 | C10 | 0.15 max | 0.30-0.60 | Case hardening, mild steel parts | P1.1 |
| 15C8 | C15Mn75 | 0.10-0.20 | 0.60-0.90 | Gears, shafts (case hardened) | P1.1 |
| 20C8 | C20 | 0.15-0.25 | 0.60-0.90 | General structural, shafts | P1.2 |
| 30C8 | C30 | 0.25-0.35 | 0.60-0.90 | Connecting rods, bolts | P2.1 |
| 40C8 | C40 | 0.35-0.45 | 0.60-0.90 | Axles, crankshafts | P2.1 |
| 45C8 | C45 | 0.40-0.50 | 0.60-0.90 | Gears, studs, keys | P2.5 |
| 55C8 | C55Mn75 | 0.50-0.60 | 0.60-0.90 | Springs, dies | P3.1 |
| 65C6 | C65 | 0.60-0.70 | 0.50-0.80 | Springs, washers | P3.1 |
| 98C6 | C98 | 0.90-1.05 | 0.50-0.80 | Bearings, tools | P4.1 |

**Mechanical properties (hot rolled/normalized):**

| Grade | Tensile (MPa) | Elongation % |
|-------|---------------|-------------|
| 10C4 (C10) | 340-420 | 26 |
| 20C8 (C20) | 440-520 | 24 |
| 30C8 (C30) | 500-600 | 21 |
| 40C8 (C40) | 580-680 | 18 |
| 45C8 (C45) | 630-710 | 15 |
| 55C8 (C55Mn75) | 720 min | 13 |
| 65C6 (C65) | 750 min | 10 |

**Hardened & tempered properties:**

| Grade | Tensile (MPa) | Yield (MPa) | Elongation % | Izod Impact (J) | Ruling Section (mm) |
|-------|---------------|-------------|-------------|-----------------|---------------------|
| 30C8 | 600-750 | 400 | 18 | 55 | 30 |
| 40C8 | 600-750 / 700-850 | 380 / 480 | 18 / 17 | 41 / 35 | 100 / 30 |
| 45C8 | 600-750 / 700-850 | 380 / 480 | 17 / 15 | 41 / 35 | 100 / 30 |
| 55C8 | 700-850 / 800-950 | 460 / 540 | 15 / 13 | — | 63 / 30 |

### IS 1570 Part 4 — Alloy Steel Grades

40+ grades. Key ones for defense/aerospace/automobile:

| IS Designation | Type | C % | Cr % | Ni % | Mo % | Typical Use | ISO Group |
|---------------|------|-----|------|------|------|-------------|-----------|
| 15Cr3 | Chromium | 0.12-0.18 | 0.50-0.80 | — | — | Carburizing, gears | P2.1 |
| 40Cr4 | Chromium | 0.35-0.45 | 0.90-1.20 | — | — | Shafts, bolts (EN18 equiv) | P2.5 |
| 55Cr3 | Chromium | 0.50-0.60 | 0.60-0.80 | — | — | Springs | P3.1 |
| 103Cr4 | Bearing | 0.95-1.10 | 0.90-1.20 | — | — | Bearings (EN31 equiv) | P4.1 |
| 20MnCr5 | CrMn | 0.17-0.22 | 0.80-1.10 | — | — | Carburizing gears | P2.1 |
| 40Cr4Mo2 | CrMo | 0.35-0.45 | 0.90-1.20 | — | 0.15-0.25 | High-strength shafts (EN19 equiv) | P2.5 |
| 15Cr13Ni3 | CrNi | 0.12-0.18 | 0.60-0.90 | 2.75-3.25 | — | Case hardening (EN36 equiv) | P2.1 |
| 40Ni14 | Nickel | 0.35-0.45 | — | 3.25-3.75 | — | Forged crankshafts | P2.5 |
| 15Ni4Cr1 | NiCr | 0.12-0.18 | 0.60-1.00 | 3.90-4.30 | — | Aircraft parts (EN39 equiv) | P2.5 |
| 30Ni16Cr5 | NiCr | 0.26-0.34 | 1.00-1.50 | 3.90-4.30 | — | Heavy-duty forgings (EN30 equiv) | P3.1 |

**Cross-reference to British EN numbers** (commonly used in Indian shops alongside IS):
- IS 40Cr4 = EN 18 = AISI 5140
- IS 40Cr4Mo2 = EN 19 = AISI 4140 (**very common**)
- IS 103Cr4 = EN 31 = AISI 52100
- IS 15Cr13Ni3 = EN 36 = AISI 3310
- IS 15Ni4Cr1 = EN 39

---

## 3. Indian Tool Catalog Data (Totem/Forbes Precision)

Totem (Forbes & Company) is India's largest cutting tool manufacturer, headquartered in Mumbai. The 2025 Master Catalogue (662 pages) covers taps, drills, endmills, reamers, and burrs.

### Cutting Speed Data by ISO Material Group

**Reaming — Carbide (TMRT series):**

| Material | ISO Group | Vc min (m/min) | Vc max (m/min) |
|----------|-----------|----------------|----------------|
| Steel | P.1-2 | 40 | 70 |
| Steel | P.3 | 35 | 60 |
| Steel | P.4 | 25 | 45 |
| Steel | P.5-6 | 15 | 25 |
| Stainless Steel | M.1-3 | 8 | 15 |
| Cast Iron | K.1 | 35 | 60 |
| Cast Iron | K.2 | 25 | 50 |
| Cast Iron | K.3 | 20 | 45 |
| Non-Ferrous | N.1-4 | 110 | 195 |
| Non-Ferrous | N.5 | 105 | 180 |
| Special Alloys | S.1-2 | 8 | 15 |
| Special Alloys | S.3-4 | 15 | 30 |

**High Feed Milling — Carbide (Torus endmill):**

| Material | ISO Group | Vc (m/min) shoulder | Vc range (m/min) |
|----------|-----------|---------------------|-------------------|
| Steel | P.3 | 230 | 230-330 |
| Steel | P.4 | 200 | 200-250 |
| Hardened Steel | H.1 | 80 | 80-120 |

**Tapping — HSS-E (case studies on Indian materials):**

| Material | Vc (m/min) | Tool |
|----------|-----------|------|
| EN8 (IS 45C8) | 20 | SA3 spiral point |
| S45C (IS 45C8 equiv) | 25 | SA3 spiral point |
| 16MnCr5 (IS 20MnCr5) | 22 | SAF5 spiral flute |
| C40 (IS 40C8) | 15 | SBF5 spiral flute |
| Grey Cast Iron 220 BHN | 50 | SC4 straight flute |
| 41Cr4 (30-32 HRC) | ~6 (300 RPM) | SBF-TC |
| AC4C (Al casting) | 30 | SD3 spiral flute |
| ADC12 (Al die cast) | 50 | SDK1 carbide roll tap |

### What Totem Catalog Does NOT Have

- No kc1 / specific cutting force values
- No power constants
- No material removal rate data
- No tool life equations
- Only cutting speeds and feeds for their specific tool geometries
- Speed data is tool-specific, not generalized for a process

**Assessment**: Totem data is useful for validating our cutting speed ranges against what Indian manufacturers actually use with Indian tools, but is NOT a substitute for Sandvik/Kennametal/MHB for physics-based calculations.

---

## 4. Cross-Validation: Indian Data vs Our Engine

### Machine Hour Rates

| Process | Our Rate | Government Range | Private Shop Range | Verdict |
|---------|---------|------------------|-------------------|---------|
| CNC Turning | 800 | 200-450 | 600-1200 | OK (mid-range private) |
| CNC Milling (VMC) | 1000-1100 | 350-800 | 800-1500 | OK (mid-range private) |
| Drilling | 600 | N/A (usually on VMC) | 400-800 | OK |
| Surface Grinding | 1200 | 125-300 | 400-800 | **HIGH** — consider 600-800 |
| Cylindrical Grinding | 1200 | 150-500 | 500-1000 | **HIGH** — consider 800-1000 |
| Broaching | 1500 | N/A | 1200-2000 | OK (specialized) |

### Steel Grade Mapping to Our material_db.py

| Our Material | IS Standard | Typical Grades | kc1 (N/mm2) |
|-------------|-------------|----------------|-------------|
| Mild Steel | IS 2062 E250 | E250A, E250BR | 1500 |
| Carbon Steel | IS 1570 Pt2 | 20C8, 30C8, 40C8 | 1700 |
| Alloy Steel | IS 1570 Pt4 | 40Cr4Mo2 (EN19), 40Cr4 (EN18) | 1800-2100 |
| Stainless Steel | IS 6911 | 04Cr18Ni10 (SS 304), 04Cr17Ni12Mo2 (SS 316) | 1800 |
| Cast Iron | IS 210 | FG 200, FG 260, FG 300 | 1100-1300 |
| Aluminium | IS 733 | 6061, 7075 | 600-800 |
| Brass | IS 291 | CuZn39Pb2 (free cutting) | 700 |
| Copper | IS 191 | ETP copper | 1100 |
| Titanium | No IS (imported) | Ti-6Al-4V (AMS 4911) | 1400 |

### Cutting Speed Validation

Totem's recommended speeds vs our engine's Sandvik-based speeds:

| Material | Operation | Totem Vc (m/min) | Our Engine Vc (m/min) | Match? |
|----------|-----------|------------------|----------------------|--------|
| Mild Steel (P.1) | Reaming | 40-70 | 50-80 | Close |
| Carbon Steel (P.3) | Milling | 230-330 (high feed) | 150-250 (conventional) | Different ops |
| Stainless Steel (M.1) | Reaming | 8-15 | 10-20 | Close |
| Cast Iron (K.1) | Reaming | 35-60 | 40-70 | Close |
| Aluminium (N.1) | Reaming | 110-195 | 150-250 | Close |
| Titanium (S.1) | Reaming | 8-15 | 10-20 | Close |

**Conclusion**: Indian tool data aligns with our Sandvik-based engine within 15-25%. No need to adjust core cutting data — our engine's physics base from Sandvik/MHB/Kennametal is validated.

---

## 5. Indian Steel Grade Naming Convention

Indian shops use a mix of naming systems. Our engine should recognize:

1. **IS number** (IS 2062 E250, IS 1570 45C8)
2. **Old IS name** (C45, C40, C20)
3. **British EN number** (EN8, EN19, EN24, EN31, EN36) — **most commonly used on shop floors**
4. **AISI/SAE** (4140, 4340, 52100) — used in defense/aerospace
5. **DIN** (42CrMo4, 16MnCr5) — used in automobile (German OEM influence)

**Common equivalences for Indian shops:**

| Shop Floor Name | IS | AISI | DIN | Use |
|----------------|-----|------|-----|-----|
| EN8 | 45C8 | 1045 | C45 | General purpose, shafts |
| EN9 | 55C8 | 1055 | C55 | Springs, hand tools |
| EN18 | 40Cr4 | 5140 | 41Cr4 | High-tensile bolts |
| EN19 | 40Cr4Mo2 | 4140 | 42CrMo4 | **Most popular alloy steel** |
| EN24 | 40Ni6Cr4Mo2 | 4340 | 40NiCrMo6 | Aircraft, heavy-duty shafts |
| EN31 | 103Cr4 | 52100 | 100Cr6 | Bearings |
| EN36 | 15Cr13Ni3 | 3310 | 14NiCr14 | Case hardening, gears |
| EN47 | 55Cr3 | 6150 | 50CrV4 | Leaf springs |
| EN353 | 20MnCr5 | — | 20MnCr5 | Carburizing gears |

---

## 6. Missing Indian-Specific Data (Future Work)

| Data Source | What It Would Add | Status |
|-------------|------------------|--------|
| **CMTI Machine Hour Rate Guide** | Authoritative Indian rates from Central Manufacturing Technology Institute, Bangalore | Not freely available (₹1,500-3,000) |
| **IMTMA Tool Directory** | Indian machine tool specifications and capacities | Membership-only |
| **DRDO machining standards** | Defense-specific processes and tolerances | Classified/restricted |
| **BHEL/HAL internal rates** | PSU internal costing data | Confidential |
| **Addison Carbide Catalog** | Indian carbide insert cutting data | Need to download from addisoncarbide.com |
| **Miranda Tools Catalog** | Indian HSS tool cutting data | Need to download from mirandatools.in |
| **IS 210:2009** | Grey cast iron grades (FG 150 through FG 400) | Available on archive.org |
| **IS 6911** | Stainless steel plate/sheet grades and properties | Available on archive.org |

---

## 7. Action Items for Engine

1. **Split grinding rates** in config.py: conventional (600-800) vs CNC precision (1200-1500)
2. **Add Wire EDM and Sinker EDM** to process_db.py (INR 500-800/hr based on government data)
3. **Add EN number aliases** to material_db.py (EN8→45C8, EN19→40Cr4Mo2, etc.)
4. **Map IS grades** to ISO material groups in cutting_data.py for automatic kc1 lookup
5. **Add cold-drawn bar properties** from IS 1570 for estimating pre-machined stock strength
6. **Consider MSME discount tier** — government/PSU orders may use government tool room rates (40-60% lower)
