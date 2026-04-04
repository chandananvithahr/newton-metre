---
slug: should-cost-estimation
title: Should-Cost Estimation — How Newton-Metre Calculates Part Costs
keywords: should-cost, cost estimation, MRR, material removal rate, physics-based, mechanical, sheet metal, PCB, cable, validation, confidence tier, Indian manufacturing, machining cost, unit cost
sources: MASTER-RESEARCH-REPORT.md, BOOTHROYD-ECONOMICS-EXTRACTION.md, PRACTICAL-MACHINING-DATA.md, config.py
updated: 2026-04-04
---

# Should-Cost Estimation

Should-cost estimation answers: "What should this part cost to manufacture, based on physics and economics?" Newton-Metre calculates this from first principles -- no historical database required, no 3D CAD needed.

## How It Works

Upload a 2D drawing (PDF, DXF, DWG, or image). AI extracts dimensions, material, tolerances, and processes. The physics engine calculates costs line-by-line.

**Total Part Cost = Material + Machining + Setup + Tooling + Labour + Power + Overhead (15%) + Profit (20%)**

## Four Part Types

### 1. Mechanical (Turned, Milled, Ground)

The core engine. Uses Material Removal Rate (MRR) to calculate machining time for 18 processes:

- **Turning/Facing/Boring** -- MRR = Vc x 1000 x f x ap (mm3/min)
- **Milling (face/slot/pocket)** -- MRR = ae x ap x Vf, where Vf = fz x z x n
- **Drilling** -- time = depth / (f x n)
- **Tapping** -- time = 2 x depth / (pitch x n) for in + out stroke
- **Grinding** -- infeed per pass + sparkout passes
- **Threading, reaming, knurling, broaching**

Each process uses material-specific cutting parameters from Sandvik and Machinery's Handbook, with 9 materials in the database.

### 2. Sheet Metal (Laser Cut, Bent, Welded)

Laser cutting speeds from a 3kW fiber laser database (6 material groups x 9 thicknesses), press brake tonnage formula for bending, MIG/TIG/spot welding rates, nesting utilization.

### 3. PCB Assembly

BOM-based: SMD at 1.5 INR/pad, THT at 3.0 INR/pin, stencil cost (500 INR amortized), test at 25 INR/board, plus scraped component prices from DigiKey/Mouser.

### 4. Cable Assembly

BOM-based: labour at 200 INR/hr, 2 min/wire, 0.5 min/connector, plus sleeving and labelling time.

## Key Cost Drivers (Mechanical Parts)

### Material Cost
Raw material weight (including 15% wastage) x price per kg. Bar stock sized with 3mm diameter allowance and 5mm length allowance.

### Machining Time
The dominant cost factor. Calculated from MRR using real cutting parameters:
- Roughing and finishing passes calculated separately
- Non-cutting time factor of 1.40x applied (rapid traverse, tool change, measurement, load/unload)
- Shop floor efficiency of 0.75x applied (real shops run at 65-85% of catalog speeds)

### Setup Time (Amortized)
Setup time per process (15-60 min) divided by quantity. At qty=1, setup is 50%+ of cost. At qty=100, it drops below 5%.

### Tooling Wear
Taylor tool life equation: V x T^n = C. Tool cost = carbide edge cost (12.5 INR) / tool life in minutes.

### Nonproductive Time
Boothroyd's key finding: nonproductive time (load/unload, measurement, rapid traverse) accounts for 50-60% of total cycle time. This is the largest cost lever, not cutting speed.

## Indian Manufacturing Rates (from config.py)

| Process | Machine Rate (INR/hr) | Setup (min) | Power (kW) | Tooling (INR/unit) |
|---------|----------------------|-------------|------------|-------------------|
| Turning | 800 | 30 | 5 | 8 |
| Milling (face) | 1,000 | 45 | 7 | 12 |
| Milling (pocket) | 1,100 | 50 | 7 | 15 |
| Drilling | 600 | 15 | 3 | 5 |
| Grinding (cyl.) | 1,200 | 40 | 4 | 4 |
| Broaching | 1,500 | 60 | 10 | 20 |

**General rates:** Labour 250 INR/hr, Power 8 INR/kWh, Overhead 15%, Profit margin 20%.

## Validation Pipeline

Every mechanical estimate runs through a parallel validation:

1. **Physics engine** calculates the cost (as above)
2. **Gemini AI** independently estimates the cost
3. **Orchestrator** compares them and assigns a confidence tier:

| Tier | Delta | Action |
|------|-------|--------|
| HIGH | <=3% | Accept physics result |
| MEDIUM | 3-7% | Accept with note |
| LOW | 7-15% | AI arbitrator analyzes line-by-line discrepancies |
| INSUFFICIENT | >15% | Interactive loop -- up to 2 rounds of clarifying questions |

## Accuracy and Uncertainty

- Known materials (9 in database): +/-10% uncertainty band shown to users
- Dynamic/AI-fetched materials: +/-15% uncertainty band
- Tight tolerance surcharge: +30% on machining cost when tolerance < +/-0.05mm

## What Makes This Different

- **Physics-based, not ML** -- works from day one with zero training data
- **2D drawings, not 3D CAD** -- because 60-70% of Indian procurement uses PDFs
- **Indian economics** -- INR rates calibrated to real job shop pricing
- **Line-by-line breakdown** -- every process shows time, machine cost, tooling, labour, power separately
- **No competitor** does this: aPriori needs 3D, CADDi does similarity only, IndustrialMind wraps APIs
