# Physics-Based Cost Engine — Knowledge Map
## March 2026 — Consolidated from 8 PDFs, 6 research docs, 30+ referenced papers

---

# WHAT WAS BUILT

## Files Created/Modified (Session: Mar 29, 2026)

### NEW: `engines/mechanical/cutting_data.py`
- 9 materials with real cutting parameters from Machinery's Handbook
- Per-material: turning speeds/feeds, milling speeds/feeds, drilling speeds/feeds, grinding params
- Kp power constants (Al 0.25, MS 0.74, SS304 0.78, EN24 0.82, Ti 0.65 kW/cm3/min)
- Taylor tool life constants (n=0.25 carbide, C varies 150-900 by material)
- Machinability-based fallback for unknown materials
- Standard tool assumptions: 63mm face mill (6-tooth), 16mm endmill (4-tooth)
- Carbide insert edge cost: Rs 12.5 (Rs 50 insert / 4 edges)

### UPGRADED: `engines/mechanical/process_db.py`
- Replaced heuristic formulas with MRR-based physics
- Turning: volume from machining allowance, rough + finish passes, MRR = Vc x 1000 x f x ap
- Milling: face mill vs endmill with correct ae/ap per operation type
- Drilling: time = depth/(f x n), with peck cycle factor for deep holes
- Tapping: 2 x depth/(pitch x n) for synchronized in+out stroke
- Threading: multi-pass at 0.1mm/pass, spring passes included
- Grinding: infeed per pass + sparkout passes
- 25% non-cutting overhead factor

### UPGRADED: `engines/mechanical/cost_engine.py`
- Tooling cost: Taylor tool life -> Rs/min wear cost (replaces flat Rs 8/part)
- Passes material_name for exact cutting data lookup
- Power cost still uses static config (upgrade path: Kp x MRR when we track per-op MRR)

### Tests: 8 -> 16 (43 total suite, all passing)

---

# KNOWLEDGE SOURCES READ

## Books/PDFs Read (All in papers/ directory)

| Source | Pages | Key Data Extracted |
|--------|-------|--------------------|
| Machinery's Handbook 30th Ed | 2896 | 50+ material cutting speed tables (HSS + carbide), Kp power constants for 30+ materials, Taylor tool life V*T^n=C, Gilbert's economic cutting speed, IT grade tolerances by process, surface roughness by process, cost formula CTOT |
| Fundamentals of CNC Machining (Autodesk/Titans) | 256 | RPM = (SFM x 3.82)/Dia, Feed(IPM) = RPM x CL x NumFlutes, milling speeds for 6 materials (Al 800 SFM, Steel 350, SS 300), stepover 50-80%, stepdown 25-50%, tap/drill charts |
| Walter Titex Drilling/Threading | 53 | Drilling time = depth/(f x n), tapping time = 2 x depth/(pitch x n), 20+ material groups with vc and f by drill diameter, core hole formulas, power scales as d^2 |
| Machining 1-14 (Walker) | 260 | Drilling speeds for 30+ materials with cutting fluid recs, turning speeds HSS: Cast iron 70-120, Low carbon 130-160, Al 600-1000 fpm, carbide = 3-4x HSS |
| Deburring & Surface Finishing (Scheider) | 169 | Cycle times 4-14 sec/part automated brush/buff, consumable $0.002-$0.04/part, surface finish 4-32 rms, only covers power brush/buff (NOT tumbling/vibratory) |
| Boothroyd Machining & Machine Tools | FAILED | Auth error on large PDF. Content covered by Machinery's Handbook |

## Key Papers Read (in papers/ directory)

| Paper | Key Contribution |
|-------|------------------|
| ARKNESS (2506.13026v1) | KG: 4,329 triples from 9 docs. Pipeline: Docling -> paragraph split -> GPT-4o triple extraction -> PostgreSQL -> embeddings -> beam search. 3B Llama = GPT-4o. "Fundamentals of CNC Machining" = 44% of all triples |
| CAPP-GPT (1297057) | Feature->process mapping for 12 types. Part Encoder: 2-stage hierarchical transformer. Macro-CAPP (sequencing). Synthetic training via OR+ML hybrid |

## Referenced Papers (from ARKNESS + CAPP-GPT, researched via web)

| Paper | Finding |
|-------|---------|
| arXiv 2508.12440 (DXF+XGBoost) | 3.91% MAPE from 200 DXF geometric features. MOST relevant to us |
| AAGNet (Wu 2024) | State-of-art B-Rep feature recognition, open-source + MFInstSeg dataset (60K STEP files) |
| MFCAD++ (Colligan 2022) | 59,665 labeled STEP files — training dataset for feature recognition |
| FeatureNet (Zhang 2018) | 24 machining feature taxonomy, 97.4% classification from voxels |
| MPKE-GPT (2025) | LLM-built machining KG from 50 enterprise parts, 48% faster than manual |
| ChatCNC (Jeon 2025) | Multi-agent RAG for CNC monitoring, 93.3% accuracy |
| Yoo & Kang 2021 | Explainable cost estimation with 3D Grad-CAM showing WHICH features drive cost |

## Process Planning Books (researched via web)

| Book | Contribution |
|------|-------------|
| DFMA (Boothroyd, Dewhurst, Knight) | Part cost = Material + (Process Time x Rate) + (Tooling/Volume) + Secondary. 200K+ data points in commercial software |
| Kalpakjian & Schmid | Taylor equation, Gilbert's optimal speed formula, machining economics |
| Realistic Cost Estimating (Lembersky/SME) | Practitioner handbook, process-by-process cost breakdown, 15+ processes |
| Halevi & Weill | Logical CAPP framework: drawing -> process selection -> parameter optimization -> time/cost |
| Chang - Computer-Aided Manufacturing | Variant vs generative CAPP, process selection rules, operation sequencing |

---

# CORE FORMULAS IMPLEMENTED

## 1. Material Removal Rate (MRR)
```
MRR_turning (mm3/min) = Vc(m/min) x 1000 x f(mm/rev) x ap(mm)
MRR_milling (mm3/min) = ae(mm) x ap(mm) x Vf(mm/min)
  where Vf = fz x z x n, n = Vc*1000 / (pi*D_tool)
Drilling time = depth / (f x n)
  where n = Vc*1000 / (pi*d)
Tapping time = 2 x depth / (pitch x n)
```

## 2. Taylor Tool Life
```
V x T^n = C
T = (C/V)^(1/n)
Tool cost per minute = edge_cost / T
  where edge_cost = Rs 12.5 (Rs 50 insert / 4 edges)
```

## 3. Cutting Power
```
P (kW) = Kp x MRR (cm3/min) / machine_efficiency
```

## 4. Total Part Cost
```
Cost = Material + Sum(Process_Time x Machine_Rate) + (Setup_Time x Rate / Qty) + Tooling_Wear + Power + Labour
  + Overhead(15%) + Profit(20%)
```

---

# CUTTING PARAMETERS (Summary — full data in cutting_data.py)

## Turning (Carbide)

| Material | Vc_rough (m/min) | Vc_finish | f_rough (mm/rev) | f_finish | ap_rough (mm) | ap_finish | Kp (kW/cm3/min) | Taylor C |
|----------|-----------------|-----------|-------------------|----------|---------------|-----------|-----------------|----------|
| Al 6061 | 400 | 500 | 0.30 | 0.10 | 2.0 | 0.3 | 0.25 | 900 |
| MS IS2062 | 180 | 220 | 0.25 | 0.10 | 2.0 | 0.3 | 0.74 | 400 |
| SS 304 | 120 | 160 | 0.20 | 0.08 | 1.5 | 0.25 | 0.78 | 280 |
| Brass IS319 | 280 | 350 | 0.25 | 0.10 | 2.0 | 0.3 | 0.40 | 600 |
| EN8 | 150 | 200 | 0.25 | 0.10 | 2.0 | 0.3 | 0.74 | 350 |
| EN24 | 100 | 140 | 0.20 | 0.08 | 1.5 | 0.25 | 0.82 | 250 |
| Copper | 200 | 280 | 0.25 | 0.10 | 2.0 | 0.3 | 0.35 | 500 |
| Cast Iron | 120 | 160 | 0.25 | 0.10 | 2.0 | 0.3 | 0.55 | 300 |
| Ti Gr5 | 45 | 65 | 0.15 | 0.06 | 1.0 | 0.2 | 0.65 | 150 |

## Drilling (Carbide, ~10mm drill)

| Material | Vc (m/min) | f (mm/rev) |
|----------|-----------|-----------|
| Al 6061 | 120 | 0.20 |
| MS IS2062 | 80 | 0.18 |
| SS 304 | 50 | 0.12 |
| Brass IS319 | 100 | 0.18 |
| EN8 | 70 | 0.15 |
| EN24 | 50 | 0.12 |
| Copper | 90 | 0.18 |
| Cast Iron | 70 | 0.18 |
| Ti Gr5 | 25 | 0.08 |

---

# FEATURE -> PROCESS MAPPING (From CAPP-GPT)

| Feature | Process Sequence |
|---------|-----------------|
| Through Hole | Center drill -> Drill -> Bore -> Ream |
| Blind Hole | Center drill -> Drill -> Bore -> Flat-bottom clean -> Ream |
| Through Threaded Hole | Center drill -> Drill -> Bore -> Chamfer -> Tap -> Deburr |
| Blind Threaded Hole | Center drill -> Drill -> Bore -> Chamfer -> Flat-bottom -> Tap -> Deburr |
| Closed/Open Pocket | Rough mill -> Semi-finish -> Precision finish -> Deburr |
| Boss | Rough face -> Rough mill -> Semi-finish -> Precision finish -> Deburr |
| Slot | Rough mill -> Semi-finish -> Precision finish -> Deburr |
| Chamfer | Rough mill -> Semi-finish chamfer -> Finish -> Deburr |
| Fillet | Rough mill -> Semi-finish -> Ball-end finish -> Deburr |
| T-slot | Mill narrow slot -> T-slot cutter undercut -> Deburr |

---

# DRAWING INTERPRETATION RULES

## 1st vs 3rd Angle Projection
- **India = 1st angle** (IS/ISO standard, SP 46:2003)
- **USA/Japan = 3rd angle** (ASME Y14.5)
- **Detection**: truncated cone symbol in title block
  - 1st angle: large end on right (India, Europe, China)
  - 3rd angle: large end on left (USA, Japan, Canada)
- **If missing**: default to 1st angle for Indian drawings
- **CRITICAL**: getting this wrong mirrors the entire part

## View Layout
- 1st angle: top view BELOW front view, right view to the LEFT
- 3rd angle: top view ABOVE front view, right view to the RIGHT
- Front + Top share X coordinates
- Front + Side share Y coordinates

## Units
- India: mm (IS standard)
- USA: inches (3-4 decimal places)
- Detection: title block states "ALL DIMENSIONS IN MM" or similar
- Conversion: 1 inch = 25.4 mm

## Decimal Points
- Indian mm drawings: typically 0-2 decimal places (25, 25.0, 25.00)
- US inch drawings: typically 3-4 decimal places (0.984, 0.9843)
- **Critical**: decimal precision indicates tolerance class
  - X.X = +/- 0.5mm (rough)
  - X.XX = +/- 0.1mm (standard)
  - X.XXX = +/- 0.01mm (precision, needs grinding)

## GD&T Cost Multipliers
| Symbol | Multiplier | Process Required |
|--------|-----------|-----------------|
| Flatness | 1.5-2.0x | Surface grinding |
| Straightness | 1.2-1.5x | Precision turning/grinding |
| Circularity | 1.5-2.0x | Precision turning |
| Cylindricity | 2.0-3.0x | Cylindrical grinding |
| Position (>0.1mm) | 1.2-1.5x | CNC machining |
| Position (<0.05mm) | 3.0-5.0x | Jig boring + CMM |
| Concentricity | 2.5-4.0x | Multi-setup grinding |
| Parallelism | 1.3-1.8x | Surface grinding |
| Perpendicularity | 1.3-1.8x | Milling + grinding |
| Total runout | 2.0-3.5x | Between-centers grinding |
| Surface finish Ra<0.8um | 2.0-3.0x | Grinding or lapping |
| Surface finish Ra<0.4um | 3.0-5.0x | Lapping or superfinishing |

## Common Annotations -> Cost Impact
| Annotation | Cost Impact |
|------------|------------|
| "BREAK ALL SHARP EDGES" | +deburr (4-14 sec/part) |
| "DEBURR ALL OVER" | +deburr (4-14 sec/part) |
| "HEAT TREAT TO 58-62 HRC" | +heat treatment process |
| "ZINC PLATING" | +surface treatment |
| "BLACK OXIDE" | +surface treatment |
| "ANODIZE" | +surface treatment (Al only) |
| "CASE HARDEN 0.5mm" | +case hardening process |
| "STRESS RELIEVE" | +heat treatment (separate) |

---

# WHAT'S STILL NEEDED

## From User (Must Have)
1. 5-10 real engineering drawings (PDF) with actual costs/prices
2. 3-5 real supplier quotations for calibration
3. Which part types customers send most (turned vs milled vs both)

## From User (Nice to Have)
4. Any DXF/DWG files for testing extraction pipeline
5. Process rate sheet if different from config.py rates
6. Books: "Realistic Cost Estimating" (Lembersky/SME), "Principles of Process Planning" (Halevi & Weill)

## Next Build Steps
1. ~~Upgrade process_db.py with real cutting params~~ DONE
2. ~~Implement MRR-based time calculation~~ DONE
3. ~~Add Taylor tool life for tooling cost~~ DONE
4. Build feature->process mapping module (CAPP-GPT tables) — NEXT
5. Validate against real quotes — NEEDS USER DATA
6. Build STEP extractor (PythonOCC) — independent
7. Build DXF extractor (ezdxf) — independent
8. Tolerance->cost multiplier engine — NEXT
9. GD&T symbol detection + cost impact — requires drawing samples
