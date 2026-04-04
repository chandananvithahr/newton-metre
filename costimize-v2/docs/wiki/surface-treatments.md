---
slug: surface-treatments
title: Surface Treatments and Heat Treatments — 40+ Processes with Indian Rates
keywords: surface treatment, electroplating, anodizing, zinc plating, nickel plating, chrome plating, powder coating, PVD, CVD, heat treatment, hardening, nitriding, carburizing, hydrogen embrittlement, mil-spec, defense, aerospace, conversion coating, phosphating, black oxide, passivation
sources: SURFACE-TREATMENT-PROCESSES.md, surface_treatment_db.py, heat_treatment_db.py
updated: 2026-04-04
---

# Surface Treatments and Heat Treatments

Newton-Metre covers 40+ surface treatments and 15 heat treatments, all priced at Indian job shop rates. Surface treatments use area-based costing (INR/sq.dm), heat treatments use weight-based costing (INR/kg).

## Surface Treatment Categories

### Electroplating (12 processes)

Area-based costing. Requires pre-treatment (degrease, clean, pickle, rinse) which typically adds 15-30% to total cost.

| Process | Rate (INR/sq.dm) | Min Batch (INR) | Substrate | Spec | Industry |
|---------|-----------------|-----------------|-----------|------|----------|
| Zinc (Clear) | 5 | 800 | Steel, CI | ASTM B633 | All |
| Zinc (Yellow Passivation) | 6 | 800 | Steel, CI | ASTM B633 | All |
| Zinc (Black Passivation) | 7 | 800 | Steel, CI | ASTM B633 | Defense/Aero |
| Nickel (Bright) | 12 | 1,500 | Steel, Cu, Brass | ASTM B689 | All |
| Electroless Nickel (EN) | 18 | 3,000 | Most metals | MIL-C-26074 | Defense/Aero |
| Hard Chrome | 15 | 3,000 | Steel, CI, SS | MIL-STD-1501 | Defense/Aero |
| Decorative Chrome (Ni+Cr) | 22 | 2,000 | Steel, Cu, Brass | ASTM B456 | Auto |
| Cadmium | 25 | 5,000 | Steel | QQ-P-416 | Defense/Aero |
| Copper Plating | 8 | 1,000 | Steel, CI | MIL-C-14550 | All |
| Tin | 8 | 1,000 | Steel, Cu, Brass | MIL-T-10727 | All |
| Silver | 50 | 5,000 | Cu, Brass, Steel | QQ-S-365 | Defense/Aero |
| Gold | 150 | 10,000 | Cu, Brass, Steel | MIL-G-45204 | Defense/Aero |

**Key cost drivers:**
- Electroless nickel costs 2-3x more than electrolytic nickel but gives perfectly uniform thickness in blind holes
- Hard chrome: environmental compliance (hex Cr6+) is 30-40% of total cost
- Cadmium: very few CPCB-approved shops remain in India; lead time 2-4 weeks
- Gold/silver: commodity price dominates; selective plating (masking) critical to control cost

### Anodizing (5 processes, aluminum only)

| Process | Rate (INR/sq.dm) | Min Batch (INR) | Spec | Notes |
|---------|-----------------|-----------------|------|-------|
| Type I (Chromic Acid) | 12 | 2,000 | MIL-A-8625 Type I | Aerospace, 2-7um |
| Type II (Sulfuric, Clear) | 8 | 1,500 | MIL-A-8625 Type II | Most common, 5-25um |
| Type II (Color) | 12 | 1,500 | MIL-A-8625 Type II | Dyed after anodize |
| Type III (Hard Anodize) | 22 | 3,000 | MIL-A-8625 Type III | Wear resistance, 25-75um |
| Type III + PTFE Infusion | 35 | 4,000 | MIL-A-8625 Type III | Low friction + wear |

### Chemical Conversion Coatings (8 processes)

Low-cost treatments for corrosion protection or paint adhesion.

| Process | Rate (INR/sq.dm) | Min Batch (INR) | Spec | Substrate |
|---------|-----------------|-----------------|------|-----------|
| Chromate Conversion (Alodine) | 4 | 500 | MIL-DTL-5541 | Aluminum |
| Zinc Phosphating | 3 | 500 | MIL-DTL-16232 | Steel |
| Manganese Phosphating | 5 | 600 | MIL-DTL-16232 Type M | Steel |
| Iron Phosphating | 2 | 400 | TT-C-490 | Steel |
| Black Oxide (Hot) | 3 | 500 | MIL-DTL-13924 | Steel |
| Black Oxide (Cold) | 2 | 300 | -- | Steel |
| Passivation (Nitric) | 4 | 600 | ASTM A967 | Stainless |
| Passivation (Citric) | 5 | 600 | ASTM A967 | Stainless |

### Paint and Organic Coatings (5 processes)

| Process | Rate (INR/sq.dm) | Min Batch (INR) | Spec | Notes |
|---------|-----------------|-----------------|------|-------|
| Powder Coating (Standard) | 8 | 800 | -- | Most common for steel/Al |
| Powder Coating (Premium/Epoxy) | 12 | 1,000 | -- | Automotive |
| E-Coat (Cathodic) | 6 | 1,500 | -- | Automotive, high volume |
| Wet Paint (Primer + Topcoat) | 15 | 500 | -- | General |
| CARC (Military Paint) | 50 | 8,000 | MIL-DTL-53072 | Defense only |

### Thermal/Spray Coatings (3 processes)

| Process | Rate (INR/sq.dm) | Min Batch (INR) | Spec |
|---------|-----------------|-----------------|------|
| HVOF Coating | 150 | 10,000 | AMS 2447 |
| Plasma Spray | 100 | 8,000 | AMS 2437 |
| Flame Spray | 60 | 5,000 | -- |

### Vapor Deposition (3 processes)

| Process | Rate (INR/sq.dm) | Min Batch (INR) | Notes |
|---------|-----------------|-----------------|-------|
| PVD Coating | 80 | 8,000 | 1-5um, aerospace |
| CVD Coating | 120 | 10,000 | 5-20um, tooling |
| DLC (Diamond-Like Carbon) | 150 | 15,000 | 1-4um, automotive |

### Mechanical Surface Treatments (4 processes)

| Process | Rate (INR/sq.dm) | Min Batch (INR) | Spec |
|---------|-----------------|-----------------|------|
| Shot Peening | 5 | 1,000 | AMS 2430 |
| Shot Blasting | 3 | 500 | -- |
| Electropolishing | 12 | 2,000 | ASTM B912 |
| Tumble/Vibratory Deburring | 3 | 500 | -- |

## Hydrogen Embrittlement Baking

**Critical for defense and aerospace.** When high-strength steel (>31 HRC) is electroplated, hydrogen absorbed during plating can cause delayed brittle fracture.

- **Requirement:** Bake at 190-220 C within 4 hours of plating
- **Duration:** 8-24 hours depending on tensile strength
- **Cost:** 15 INR/kg
- **Applies to:** All electroplating processes on high-strength steel (zinc, nickel, chrome, cadmium, copper, tin, silver, gold)
- **Does NOT apply to:** Anodizing, conversion coatings, paint, spray coatings, mechanical treatments

Newton-Metre automatically adds H.E. baking cost when the part is high-strength steel and the treatment is electroplating.

## Heat Treatments (15 processes)

Weight-based costing (INR/kg) with minimum batch charges.

### Through Hardening

| Process | Rate (INR/kg) | Min Batch (INR) | Temp (C) | Time (hr) | Spec |
|---------|--------------|-----------------|----------|-----------|------|
| Through Hardening (Q+T) | 25 | 1,500 | 800-870 | 2-6 | AMS 2759 |
| Tempering | 15 | 800 | 150-650 | 1-4 | AMS 2759 |
| Annealing (Full) | 18 | 1,000 | 750-900 | 3-8 | -- |
| Normalizing | 18 | 1,000 | 850-920 | 2-4 | -- |
| Stress Relieving | 15 | 800 | 550-650 | 1-4 | AMS 2759 |

### Case Hardening

| Process | Rate (INR/kg) | Min Batch (INR) | Temp (C) | Time (hr) | Spec |
|---------|--------------|-----------------|----------|-----------|------|
| Carburizing (Gas) | 35 | 2,500 | 870-940 | 4-20 | AMS 2759/7 |
| Carbonitriding | 30 | 2,000 | 820-870 | 2-6 | -- |
| Nitriding (Gas) | 45 | 3,000 | 500-570 | 20-70 | AMS 2759/10 |
| Nitriding (Ion/Plasma) | 55 | 4,000 | 400-580 | 10-40 | AMS 2759/12 |
| Induction Hardening | 20 | 800 | 850-1000 | <0.1 | -- |

### Specialty

| Process | Rate (INR/kg) | Min Batch (INR) | Spec | Notes |
|---------|--------------|-----------------|------|-------|
| Solution + Aging (Al) | 30 | 1,500 | AMS 2770 | T6 temper |
| Solution + Aging (Ti) | 80 | 5,000 | AMS 2801 | Aerospace |
| Precipitation Hardening | 50 | 3,000 | AMS 2759/3 | 17-4PH, Inconel |
| Cryogenic (-196 C) | 40 | 2,000 | -- | Tool steel, defense |
| Vacuum Hardening | 60 | 5,000 | AMS 2759/5 | Aerospace, no decarb |

## Common Treatment Combinations by Industry

### Defense

1. Steel parts: Through harden + Manganese phosphating (Parkerizing) + CARC paint
2. Aluminum parts: Hard anodize Type III + Chromate conversion on mating surfaces
3. Fasteners: Cadmium plating (being replaced by zinc-nickel) + H.E. baking
4. Precision shafts: Hard chrome + Cylindrical grinding to final dimension

### Aerospace

1. Landing gear: Cadmium or zinc-nickel plating + H.E. baking + Shot peening
2. Aluminum structure: Type II anodize + Alodine on faying surfaces + Primer
3. Engine components: Plasma spray thermal barrier + PVD wear coating
4. Fasteners: Silver plating (anti-galling) or cadmium

### Automotive

1. Body panels: E-coat + Primer + Basecoat + Clearcoat
2. Engine parts: Nitriding or induction hardening + Black oxide
3. Suspension: Through harden + Zinc plating (yellow or black)
4. Interior: Decorative chrome (Ni + Cr) on plastic or zinc die-cast

## Masking

Masking adds 10-25% to per-piece surface treatment cost for typical machined parts.

| Type | Cost Range |
|------|-----------|
| Simple tape (threads, bores) | 5-15 INR/piece |
| Wax/lacquer (complex geometry) | 10-30 INR/piece |
| Silicone plugs (reusable) | 50-200 INR/piece |
| Custom jig (high volume) | 500-5,000 INR one-time |
