---
slug: physics-engine
title: Physics-Based Cost Engine Architecture
keywords: physics engine, MRR, material removal rate, Sandvik, kc1, Taylor tool life, cutting force, machining economics, cost estimation, process time, machine hour rate, validation, turning, milling, drilling, grinding, Big 6 processes
sources: PHYSICS-ENGINE-KNOWLEDGE-MAP.md, PROCESS-80-20-ANALYSIS.md
updated: 2026-04-04
---

# Physics-Based Cost Engine Architecture

Newton-Metre's cost engine uses physics-based models as the foundation -- not machine learning, not heuristics, not lookup tables. This is a deliberate architectural decision with specific advantages over alternatives.

## Why Physics-First Beats ML-First

| Advantage | Explanation |
|-----------|-------------|
| **Zero training data needed** | Works on day one with zero historical parts. No cold-start problem. |
| **Explainability** | Line-by-line breakdown: "CNC turning took 4.2 min at Rs 800/hr = Rs 56". Users trust this. Procurement teams can defend costs to management with physics formulas. |
| **Generalizes perfectly** | A new material or process just needs its MRR/kc1 values. No retraining. |
| **Handles novel parts** | First-of-kind parts estimated correctly if dimensions and processes are known. |
| **Regulatory/audit trail** | Required for defense procurement. Physics formulas are auditable. |

ML is added later as a correction layer (after 50-100 estimate-actual pairs), not as a replacement. The hybrid approach `Final_Cost = Physics_Cost x ML_Correction_Factor` is validated by a 2024 Taylor & Francis review showing hybrid models outperform pure ML.

## Core Formulas

### 1. Material Removal Rate (MRR)

The fundamental calculation driving machining time estimation:

```
MRR_turning (mm3/min) = Vc (m/min) x 1000 x f (mm/rev) x ap (mm)
MRR_milling (mm3/min) = ae (mm) x ap (mm) x Vf (mm/min)
  where Vf = fz x z x n,  n = Vc x 1000 / (pi x D_tool)
Drilling time = depth / (f x n)
  where n = Vc x 1000 / (pi x d)
Tapping time = 2 x depth / (pitch x n)  [synchronized in+out stroke]
```

### 2. Taylor Tool Life Equation

```
V x T^n = C
T = (C / V) ^ (1/n)
Tool cost per minute = edge_cost / T
  where edge_cost = Rs 12.5 (Rs 50 insert / 4 edges)
```

Taylor constants are material-specific: n=0.25 for carbide tools, C ranges from 150 (Ti Gr5) to 900 (Al 6061).

### 3. Cutting Power

```
Pc (kW) = Kp x MRR (cm3/min) / machine_efficiency
```

Alternative Sandvik formula: `Pc = (vc x ap x fn x kc) / (60 x 10^3)`

### 4. Total Part Cost

```
Cost = Material
     + Sum(Process_Time x Machine_Rate)
     + (Setup_Time x Rate / Qty)
     + Tooling_Wear
     + Power
     + Labour
     + Overhead (15%)
     + Profit (20%)
```

## Cutting Parameter Data

All cutting parameters sourced from Machinery's Handbook 30th Ed, Sandvik Coromant training handbook, Walter Titex drilling data, and Kennametal catalogs. Cross-validated against multiple sources.

### Turning (Carbide)

| Material | Vc_rough (m/min) | Vc_finish | f_rough (mm/rev) | f_finish | ap_rough (mm) | Kp (kW/cm3/min) | Taylor C |
|----------|-----------------|-----------|-------------------|----------|---------------|-----------------|----------|
| Al 6061 | 400 | 500 | 0.30 | 0.10 | 2.0 | 0.25 | 900 |
| MS IS2062 | 180 | 220 | 0.25 | 0.10 | 2.0 | 0.74 | 400 |
| SS 304 | 120 | 160 | 0.20 | 0.08 | 1.5 | 0.78 | 280 |
| Brass IS319 | 280 | 350 | 0.25 | 0.10 | 2.0 | 0.40 | 600 |
| EN8 | 150 | 200 | 0.25 | 0.10 | 2.0 | 0.74 | 350 |
| EN24 | 100 | 140 | 0.20 | 0.08 | 1.5 | 0.82 | 250 |
| Ti Gr5 | 45 | 65 | 0.15 | 0.06 | 1.0 | 0.65 | 150 |

### Sandvik kc1 Specific Cutting Force

The Kienzle kc1.1 formula is the de facto standard across all open-source machining tools:
```
kc = kc1.1 x (hm / h0) ^ (-mc) x Kg x Kw
```

Confirmed by cross-validation against 10+ open-source implementations (FreeCAD CamScripts, pymachining, r3ditor, JustTheChip) and Kennametal unit power constants for 16 AISI material grades.

## 18 Machining Processes

The engine models 18 processes with MRR-based time estimation (not heuristics):

**Turning operations**: turning, facing, boring, threading (multi-pass at 0.1mm/pass + spring passes)
**Milling operations**: face milling (63mm 6-tooth), slot milling, pocket milling (16mm 4-tooth endmill)
**Hole-making**: drilling (with peck cycle for deep holes), reaming, tapping
**Finishing**: grinding (cylindrical, surface -- infeed per pass + sparkout), knurling
**Other**: broaching

Each process uses material-specific cutting speeds from the data tables. A 25% non-cutting overhead factor is applied for tool changes, measurement, and chip clearing.

## Machine Hour Rates

| Process | Rate (Rs/hr) | Setup Time (min) |
|---------|-------------|-----------------|
| CNC Turning | 600-800 | 15-30 |
| CNC Milling (3-axis) | 800-1000 | 20-45 |
| CNC Milling (5-axis) | 1200-1500 | 30-60 |
| Surface Grinding | 600-800 | 15-30 |
| Cylindrical Grinding | 800-1000 | 20-40 |

Power consumption tracked per process (kW) at Rs 8/kWh. Labour rate Rs 250/hr. Material wastage factor 15%. Tight tolerance surcharge 30% for tolerances below +/-0.05mm.

## The Big 6 Processes = 60-65% of All Parts

Cross-sector analysis across Indian defense, aerospace, and automobile manufacturing reveals 6 processes covering the majority of all manufactured parts:

| Process | Defense | Aerospace | Auto | Weighted Avg |
|---------|---------|-----------|------|-------------|
| CNC Milling (3/4/5-axis) | 25-30% | 25-35% | 6-8% | 18-22% |
| CNC Turning | 18-22% | 12-18% | 8-12% | 12-16% |
| Die Casting (HPDC) | 3-4% | 2-3% | 18-22% | 10-12% |
| Closed Die Forging | 8-12% | 5-8% | 14-18% | 10-13% |
| Sheet Metal (Laser + Bend) | 12-15% | 10-15% | 3-5% | 8-11% |
| Stamping / Press Work | 3-4% | 1-2% | 12-16% | 6-8% |

Machining (turning + milling + drilling + grinding) accounts for 45-60% of parts across all three sectors. Sheet metal is implemented. Casting, forging, and stamping are the high-impact additions on the roadmap.

## Secondary Processes (Cost Adders)

These are applied to 50-90% of all parts:

- **Heat treatment** (50-70% of parts): 15 processes modeled, weight-based Rs/kg costing with AMS 2759 references
- **Surface treatment** (80-90% of parts): 40+ processes modeled, area-based Rs/sq.dm costing with mil-spec references
- **Deburring** (90%+ of parts): 4-14 sec/part for automated brush/buff
- **Inspection** (100% defense/aero, 50% auto): CMM rate Rs 1500-3000/hr

## Feature-to-Process Mapping

From CAPP-GPT research, deterministic feature-to-process-sequence rules:

| Feature | Process Sequence |
|---------|-----------------|
| Through Hole | Center drill -> Drill -> Bore -> Ream |
| Blind Threaded Hole | Center drill -> Drill -> Bore -> Chamfer -> Flat-bottom -> Tap -> Deburr |
| Closed/Open Pocket | Rough mill -> Semi-finish -> Precision finish -> Deburr |
| Slot | Rough mill -> Semi-finish -> Precision finish -> Deburr |
| T-slot | Mill narrow slot -> T-slot cutter undercut -> Deburr |

## 4-Tier Validation Pipeline

Every estimate is validated by running physics engine and Gemini in parallel:

| Tier | Delta | Confidence | Action |
|------|-------|------------|--------|
| HIGH | <3% | Physics and Gemini agree closely | Accept physics result |
| MEDIUM | 3-7% | Minor discrepancy | Flag for review, accept physics |
| LOW | 7-15% | Significant gap | AI arbitrator analyzes line-by-line discrepancies via Gemini |
| INSUFFICIENT | >15% | Major disagreement | Interactive loop: max 2 rounds of clarifying questions |

The validation pipeline uses ThreadPoolExecutor for parallel execution. Every validated estimate is auto-saved to `data/validation/` as training data for future ML correction models.

## GD&T Cost Multipliers

| Requirement | Multiplier | Process Required |
|-------------|-----------|-----------------|
| Flatness | 1.5-2.0x | Surface grinding |
| Cylindricity | 2.0-3.0x | Cylindrical grinding |
| Position (<0.05mm) | 3.0-5.0x | Jig boring + CMM |
| Concentricity | 2.5-4.0x | Multi-setup grinding |
| Total runout | 2.0-3.5x | Between-centers grinding |
| Surface finish Ra<0.4um | 3.0-5.0x | Lapping or superfinishing |

## Knowledge Sources

Data extracted from 8 PDFs, 6 research docs, and 30+ referenced papers:
- Machinery's Handbook 30th Ed: 50+ material cutting speed tables, Kp power constants, Taylor tool life
- Sandvik Coromant training handbook: kc1 values, power formulas, tool life factors
- Walter Titex: drilling/threading data for 20+ material groups
- Kennametal NOVO: unit power constants for 16 AISI materials, carbide grades
- Boothroyd: machining economics, nonproductive time analysis (50-60% of cycle -- key insight)
- ARKNESS paper: Knowledge Graph approach matches GPT-4o with only 3B Llama model
