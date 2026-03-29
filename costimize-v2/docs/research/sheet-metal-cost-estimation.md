# Sheet Metal Manufacturing Cost Estimation Research

> Research conducted March 2026 for Costimize v2 sheet metal module.

---

## Table of Contents

1. [Cost Model Overview](#1-cost-model-overview)
2. [Laser/Plasma/Waterjet Cutting](#2-laserplasmawaterjet-cutting)
3. [Press Brake Bending](#3-press-brake-bending)
4. [Stamping/Punching](#4-stampingpunching)
5. [Deep Drawing](#5-deep-drawing)
6. [Welding (Sheet Metal Assemblies)](#6-welding-sheet-metal-assemblies)
7. [Surface Finishing](#7-surface-finishing)
8. [Material Data & Indian Context](#8-material-data--indian-context)
9. [Nesting & Material Utilization](#9-nesting--material-utilization)
10. [Open-Source Tools & References](#10-open-source-tools--references)
11. [Implementation Plan for Costimize](#11-implementation-plan-for-costimize)

---

## 1. Cost Model Overview

### Master Formula

```
Total Cost = Material Cost + Process Costs + Surface Finish + Overhead + Profit

Where:
  Material Cost   = sheet_area × thickness × density × price_per_kg / utilization%
  Process Costs   = SUM(setup_time + cycle_time) × machine_rate for each process
  Surface Finish  = area × rate_per_sqm
  Overhead        = subtotal × overhead%
  Profit          = (subtotal + overhead) × profit%
```

### Cost Breakdown (Typical)

| Component | % of Total |
|-----------|-----------|
| Raw Material | 30-50% (up to 86% for simple parts) |
| Cutting (laser/punch) | 15-25% |
| Bending | 10-20% |
| Welding/Assembly | 5-15% |
| Surface Finish | 5-15% |
| Overhead + Profit | 15-35% |

---

## 2. Laser/Plasma/Waterjet Cutting

### 2.1 Cost Formula

```
Cutting Cost = machine_rate × cutting_time + pierce_cost + gas_cost

Where:
  cutting_time  = cutting_length_m / cutting_speed_m_per_min
  pierce_cost   = pierce_count × pierce_time × machine_rate
  gas_cost      = gas_flow_rate × cutting_time × gas_price
```

### 2.2 Fiber Laser Cutting Speeds (m/min) — Oxygen Assist for Mild Steel, N2 for SS/Al

#### Mild Steel (Carbon Steel) — O2 Assist

| Thickness | 1kW | 2kW | 3kW | 4kW | 6kW | 8kW | 12kW |
|-----------|-----|-----|-----|-----|-----|-----|------|
| 1mm | 15 | 25 | 35 | 45 | 60 | 75 | 90 |
| 2mm | 8 | 14 | 20 | 26 | 35 | 45 | 60 |
| 3mm | 4 | 7 | 10 | 14 | 20 | 26 | 38 |
| 5mm | 2 | 3.5 | 5 | 7 | 10 | 13 | 20 |
| 8mm | 0.9 | 1.8 | 2.5 | 3.5 | 5 | 6.5 | 10 |
| 10mm | 0.6 | 1.2 | 1.8 | 2.5 | 3.5 | 4.5 | 7 |
| 12mm | — | 0.8 | 1.2 | 1.7 | 2.5 | 3.2 | 5 |
| 15mm | — | 0.5 | 0.8 | 1.2 | 1.8 | 2.3 | 3.5 |
| 20mm | — | — | 0.4 | 0.6 | 1 | 1.4 | 2 |
| 25mm | — | — | — | — | 0.5 | 0.7 | 1.2 |

#### Stainless Steel (304/316) — N2 Assist

| Thickness | 1kW | 2kW | 3kW | 4kW | 6kW | 8kW | 12kW |
|-----------|-----|-----|-----|-----|-----|-----|------|
| 1mm | 12 | 20 | 28 | 38 | 50 | 62 | 75 |
| 2mm | 6.5 | 11 | 16 | 22 | 30 | 38 | 50 |
| 3mm | 3 | 5.5 | 8 | 11 | 16 | 21 | 30 |
| 5mm | 1.5 | 2.8 | 4 | 5.5 | 8 | 10.5 | 16 |
| 8mm | — | 1.5 | 2 | 2.8 | 4.2 | 5.5 | 8.5 |
| 10mm | — | 1 | 1.5 | 2 | 2.8 | 3.8 | 6 |
| 12mm | — | — | 1 | 1.4 | 2 | 2.8 | 4.5 |
| 15mm | — | — | 0.6 | 0.9 | 1.4 | 2 | 3 |
| 20mm | — | — | — | — | 0.8 | 1.2 | 1.8 |

#### Aluminum (5000/6000 Series) — N2 Assist

| Thickness | 1kW | 2kW | 3kW | 4kW | 6kW | 8kW | 12kW |
|-----------|-----|-----|-----|-----|-----|-----|------|
| 1mm | 10 | 18 | 25 | 35 | 45 | 55 | 70 |
| 2mm | 5 | 9 | 13 | 18 | 25 | 32 | 42 |
| 3mm | 2.5 | 5 | 7 | 10 | 14 | 18 | 26 |
| 5mm | 1.2 | 2.5 | 3.5 | 5 | 7 | 9.5 | 14 |
| 8mm | — | 1.2 | 1.8 | 2.5 | 3.8 | 5 | 7.5 |
| 10mm | — | 0.8 | 1.2 | 1.8 | 2.5 | 3.5 | 5.5 |
| 12mm | — | — | 0.8 | 1.2 | 1.8 | 2.5 | 4 |
| 15mm | — | — | — | — | 1.2 | 1.7 | 2.8 |

**Source:** LaserSpecHub compiled data from multiple OEMs. Speeds assume clean, flat sheet with proper focus.

### 2.3 Pierce Times (seconds per pierce)

| Thickness | Fiber 2kW | Fiber 4kW | Fiber 6kW |
|-----------|-----------|-----------|-----------|
| 1mm | 0.3 | 0.2 | 0.1 |
| 2mm | 0.5 | 0.3 | 0.2 |
| 3mm | 0.8 | 0.5 | 0.3 |
| 5mm | 1.5 | 0.8 | 0.5 |
| 8mm | 3.0 | 1.5 | 0.8 |
| 10mm | 5.0 | 2.0 | 1.2 |
| 12mm | — | 3.0 | 1.8 |
| 15mm | — | 5.0 | 2.5 |
| 20mm | — | — | 4.0 |

**Note:** Pierce times increase dramatically for stainless steel (1.5x) and aluminum (1.2x). Thick plate (>12mm) may require pulse piercing taking 5-15 seconds.

### 2.4 Assist Gas Costs

| Gas | Use Case | Flow Rate | Cost (India) |
|-----|----------|-----------|-------------|
| Oxygen (O2) | Mild steel cutting | 5-15 L/min | ₹15-20/m3 |
| Nitrogen (N2) | SS, Al (clean edge) | 15-40 L/min | ₹30-50/m3 |
| Compressed Air | Thin mild steel | 10-20 L/min | ₹5-8/m3 (compressor electricity) |

**Gas cost per meter of cut (approximate):**
- Mild steel with O2: ₹0.5-2/m
- SS/Al with N2: ₹3-10/m (N2 consumption is much higher at high pressure)

### 2.5 Laser Cutting Rates — India (INR)

**Per-mm-of-cut-length pricing (job shop rates):**

| Material | Thickness Range | Cost per mm of cut (₹) |
|----------|----------------|----------------------|
| Mild Steel | 1-25mm | ₹0.40 – ₹2.50 |
| Stainless Steel | 1-20mm | ₹0.50 – ₹3.00 |
| Aluminum | 1-15mm | ₹0.60 – ₹3.50 |
| Brass/Copper | 1-10mm | ₹0.70 – ₹4.00 |

**Machine hourly rates (in-house estimation):**

| Machine Type | Rate (₹/hr) | Notes |
|-------------|-------------|-------|
| Fiber Laser 1-2kW | ₹1,200-1,800 | Most common in Indian job shops |
| Fiber Laser 3-6kW | ₹2,000-3,500 | Medium shops, ≤15mm capacity |
| Fiber Laser 8-12kW | ₹3,500-5,000 | Large shops, thick plate |
| CO2 Laser | ₹800-1,500 | Legacy, being replaced by fiber |
| Plasma Cutter | ₹600-1,000 | >10mm thick, lower precision |
| Waterjet | ₹1,500-2,500 | No heat-affected zone, any material |
| Turret Punch | ₹800-1,200 | High-volume simple features |

**Running cost breakdown (fiber laser 3kW):**
- Electricity: ~₹80-120/hr (10-15 kW total including chiller)
- Gas (N2 for SS): ~₹150-300/hr
- Consumables (nozzle, lens): ~₹30-50/hr amortized
- Operator: ~₹150-250/hr
- Total running cost: ~₹400-700/hr (excluding machine depreciation)

---

## 3. Press Brake Bending

### 3.1 Cost Formula

```
Bending Cost = (setup_time + n_bends × time_per_bend) × machine_rate

Where:
  setup_time     = base_setup + tool_change_time × n_tool_changes
  time_per_bend  = depends on complexity (see table below)
```

### 3.2 Tonnage Calculation (Metric)

```
F = (K × S² × L) / V

Where:
  F = bending force (kN)
  K = material factor (see below)
  S = sheet thickness (mm)
  L = bend length (mm)
  V = die opening width (mm)
```

**Simplified metric formula:**
```
F (metric tons) = (650 × σb × T² × L) / (V × 1000)

Where:
  σb = ultimate tensile strength (N/mm²)
  T  = thickness (mm)
  L  = bend length (m)
  V  = die opening (mm)
```

### 3.3 Material Factors for Tonnage

| Material | K-factor (tonnage) | UTS (N/mm²) |
|----------|-------------------|-------------|
| Mild Steel | 1.0 | 400-500 |
| Stainless Steel 304 | 1.5 | 500-700 |
| Stainless Steel 316 | 1.7 | 500-700 |
| Aluminum 5052 | 0.5 | 230 |
| Aluminum 6061 | 0.65 | 310 |
| Brass | 0.55 | 350 |
| Copper | 0.45 | 220 |
| Spring Steel | 2.0 | 800-1200 |

### 3.4 Die Opening Rule of Thumb

```
V (die opening) = 8 × T (material thickness)
```

| Thickness (mm) | Recommended Die Opening (mm) | Min Bend Radius (mm) |
|----------------|-----------------------------|--------------------|
| 0.5 | 4 | 0.5 |
| 1.0 | 8 | 1.0 |
| 1.5 | 12 | 1.5 |
| 2.0 | 16 | 2.0 |
| 3.0 | 24 | 3.0 |
| 4.0 | 32 | 4.0 |
| 5.0 | 40 | 5.0 |
| 6.0 | 50 | 6.0 |
| 8.0 | 64 | 8.0 |
| 10.0 | 80 | 10.0 |

### 3.5 Bending Method Force Multipliers

| Method | Force Multiplier | Use Case |
|--------|-----------------|----------|
| Air Bending | 1.0x (baseline) | Most common, flexible angles |
| Bottom Bending | 1.5x | Better accuracy, spring-back control |
| Coining | 5-10x | Highest precision, no spring-back |

### 3.6 K-Factor for Bend Allowance (NOT tonnage — different K)

```
Bend Allowance = Angle × (π / 180) × (R + K × T)

Where:
  R = inside bend radius (mm)
  K = neutral axis position factor (0.3-0.5)
  T = material thickness (mm)
```

```
Bend Deduction = 2 × OSSB - BA

Where:
  OSSB = outside setback = (R + T) × tan(angle/2)
  BA   = bend allowance
```

**Common K-factor values (bend allowance):**

| Material | K-factor |
|----------|----------|
| Soft materials (Al, Cu) | 0.33 |
| Medium (Mild Steel) | 0.40-0.45 |
| Hard (Stainless, Spring Steel) | 0.45-0.50 |
| Industry default | 0.446 |

### 3.7 Time per Bend

| Bend Complexity | Time per Bend (sec) | Description |
|----------------|--------------------|----|
| Simple (single straight) | 8-12 | Standard 90-degree bend |
| Standard (2-3 bends, same tool) | 10-15 | Multiple bends, no tool change |
| Complex (tool change needed) | 20-30 | Different die/punch per bend |
| Hemming | 15-25 | Two-step: acute + close |
| Return bend (Z-bend) | 25-40 | Requires repositioning |

**Setup times:**

| Scenario | Time (min) |
|---------|-----------|
| First setup (tool install) | 15-30 |
| Tool change (different V-die) | 5-10 |
| Program change (CNC) | 2-5 |
| Part flip/reposition | 5-10 |

### 3.8 Press Brake Rates — India

| Machine | Rate (₹/hr) | Notes |
|---------|-------------|-------|
| Manual Press Brake ≤50T | ₹400-600 | Small job shops |
| CNC Press Brake 50-100T | ₹600-900 | Standard shops |
| CNC Press Brake 100-250T | ₹900-1,400 | Medium fabrication |
| CNC Press Brake 250-600T | ₹1,400-2,200 | Large parts, thick plate |

---

## 4. Stamping/Punching

### 4.1 Cost Formula

```
Stamping Cost = (die_cost / total_lifetime_parts) + (material_cost_per_part) + (press_time × press_rate)

Where:
  press_time = 1 / (SPM × 60)  # seconds per part
  SPM = strokes per minute
```

### 4.2 Die Costs

| Die Type | Cost Range (₹) | Lifetime (parts) | Best For |
|----------|----------------|------------------|----------|
| Single-hit simple | ₹50,000-2,00,000 | 100K-500K | Low volume, simple shapes |
| Compound die | ₹2,00,000-8,00,000 | 500K-2M | Multiple operations per stroke |
| Progressive die (simple) | ₹10,00,000-25,00,000 | 1M-5M | High volume, multi-station |
| Progressive die (complex) | ₹25,00,000-50,00,000 | 2M-10M | Automotive, complex geometries |

**International reference:** Progressive dies typically $15,000-$60,000+ USD.

### 4.3 Strokes per Minute (SPM) by Application

| Application | SPM Range | Press Tonnage |
|-------------|-----------|---------------|
| Automotive structural | 18-60 | 200-1000T |
| General stamping | 40-100 | 50-200T |
| Small parts/brackets | 80-200 | 25-100T |
| Stator/rotor laminations | 100-200 | 100-400T |
| Terminal/connectors | 800-2000 | 5-50T |

### 4.4 Punching Force

```
F = L × T × UTS

Where:
  F   = punching force (N)
  L   = perimeter of punch (mm)
  T   = material thickness (mm)
  UTS = ultimate tensile strength (N/mm²)
```

### 4.5 Turret Punch Press Rates — India

| Machine | Rate (₹/hr) | Hits/min |
|---------|-------------|----------|
| Single-station punch | ₹400-600 | 20-60 |
| CNC Turret Punch 20T | ₹800-1,200 | 200-600 |
| CNC Turret Punch 30T | ₹1,200-1,800 | 200-800 |

---

## 5. Deep Drawing

### 5.1 Drawing Ratio

```
Drawing Ratio (DR) = D_blank / D_punch

Where:
  D_blank = blank diameter (mm)
  D_punch = punch diameter (mm)
```

**Limiting Drawing Ratio (LDR):**
- First draw: DR ≤ 2.0 (reduction ≤ 50%)
- Second draw: DR ≤ 1.3 (reduction ≤ 25%)
- Third draw: DR ≤ 1.2 (reduction ≤ 20%)
- Fourth draw: DR ≤ 1.15 (reduction ≤ 15%)

### 5.2 Blank Size Calculation

**For cylindrical shells (no flange):**
```
D_blank = sqrt(d² + 4 × d × h)

Where:
  d = finished part diameter (mm)
  h = finished part height (mm)
```

**For cylindrical shells with flange:**
```
D_blank = sqrt(d² + 4 × d × h + D_f² - d²)
       = sqrt(4 × d × h + D_f²)

Where:
  D_f = flange diameter (mm)
```

### 5.3 Number of Draws Required

```
n = 1 + ceil(log(d / D_blank) / log(max_reduction_ratio))
```

**Rule of thumb:** If DR > 2.0, multiple draws needed. Each successive draw achieves smaller reduction.

### 5.4 Drawing Force

```
F = π × d × T × UTS × ((D_blank / d) - C)

Where:
  C = friction/bending constant (0.6-0.7)
```

### 5.5 Deep Drawing Costs — India

| Operation | Rate (₹/hr) | Notes |
|-----------|-------------|-------|
| Hydraulic Press ≤100T | ₹500-800 | Small draws |
| Hydraulic Press 100-400T | ₹800-1,500 | Medium parts |
| Hydraulic Press 400-1000T | ₹1,500-3,000 | Large/deep parts |
| Die cost (simple cylindrical) | ₹2,00,000-5,00,000 | Amortize over volume |
| Die cost (complex shape) | ₹5,00,000-20,00,000 | Multi-draw tooling |

---

## 6. Welding (Sheet Metal Assemblies)

### 6.1 Cost Formula

```
Welding Cost = (weld_length × time_per_mm + setup_time + fixture_time) × labour_rate
             + filler_material_cost + gas_cost + power_cost

Where:
  time_per_mm = 1 / travel_speed  (varies by process)
```

### 6.2 Welding Speed and Rates by Process

| Process | Travel Speed (mm/min) | Typical Sheet Thickness | Best For |
|---------|----------------------|------------------------|----------|
| MIG (GMAW) | 200-800 | 1-8mm | General fabrication, high speed |
| TIG (GTAW) | 50-250 | 0.5-4mm | Precision, aesthetic welds |
| Spot Welding | 20-60 spots/min | 0.5-3mm | Overlap joints, automotive |
| Laser Welding | 1000-5000 | 0.5-4mm | High precision, minimal distortion |

### 6.3 Welding Deposition Efficiency

| Process | Efficiency | Meaning |
|---------|-----------|---------|
| SMAW (Stick) | 60-75% | 25-40% waste as spatter/stub |
| GMAW (MIG) | 90-98% | Very low waste |
| GTAW (TIG) | 95-99% | Near-zero waste, slow |
| FCAW | 80-90% | Good balance |

### 6.4 Welding Costs — India

| Component | MIG | TIG | Spot |
|-----------|-----|-----|------|
| Labour rate (₹/hr) | 250-400 | 350-600 | 200-300 |
| Wire/filler cost (₹/kg) | 80-150 | 200-500 | N/A |
| Gas cost (₹/hr) | 30-60 | 40-80 | N/A |
| Power cost (₹/hr) | 20-40 | 15-30 | 10-20 |
| **Effective rate (₹/m of weld)** | **₹8-25** | **₹20-60** | **₹3-8/spot** |
| Setup + fixture time (min) | 15-30 | 15-30 | 10-20 |

**Rule of thumb for Indian shops:**
- MIG welding: ₹15-20 per meter of weld (1-3mm sheet)
- TIG welding: ₹30-50 per meter of weld (1-3mm sheet)
- Spot welding: ₹3-5 per spot
- Daily production: ~100 meters welding per operator per day

### 6.5 Joint Preparation Time

| Joint Type | Prep Time (min/m) | Notes |
|-----------|-------------------|-------|
| Butt (no prep) | 1-2 | Thin sheet, gap fit |
| Butt (V-groove) | 5-10 | Thick sheet, grinding |
| Lap joint | 0.5-1 | Sheet overlap, minimal prep |
| Corner joint | 2-4 | Tack + align |
| T-joint | 1-3 | Fillet weld, easy prep |

---

## 7. Surface Finishing

### 7.1 Common Sheet Metal Finishes — India

| Finish | Rate (₹/sq.m) | Min Batch | Lead Time |
|--------|---------------|-----------|-----------|
| Powder Coating | ₹80-200 | 10 pcs | 1-2 days |
| Zinc Plating (electroplating) | ₹150-400 | 20 pcs | 2-3 days |
| Hot-Dip Galvanizing | ₹40-80/kg | 100 kg | 1-2 days |
| Anodizing (aluminum) | ₹200-500 | 10 pcs | 2-4 days |
| Chromate Conversion | ₹50-120 | 20 pcs | 1-2 days |
| Passivation (SS) | ₹30-80 | 10 pcs | 1 day |
| Wet Paint (primer + topcoat) | ₹60-150 | 5 pcs | 1-2 days |
| Deburring (tumble) | ₹20-50 | 50 pcs | Same day |
| Deburring (manual) | ₹5-15/edge-meter | 1 pc | Same day |

---

## 8. Material Data & Indian Context

### 8.1 Standard Sheet Sizes Available in India

| Size (mm) | Common Name | Availability |
|-----------|------------|-------------|
| 1250 × 2500 | 4' × 8' | Most common, all materials |
| 1220 × 2440 | 4' × 8' (imperial exact) | Common for imported sheets |
| 1500 × 3000 | 5' × 10' | Available for MS, SS |
| 1000 × 2000 | Small sheet | Common for aluminum |
| 1524 × 6096 | 5' × 20' | Coil-cut, large fabricators |

### 8.2 Common Sheet Thicknesses (Gauge → mm)

| Gauge | Mild Steel (mm) | Stainless Steel (mm) | Aluminum (mm) |
|-------|-----------------|---------------------|---------------|
| 26 | 0.46 | 0.46 | 0.46 |
| 24 | 0.61 | 0.61 | 0.51 |
| 22 | 0.76 | 0.76 | 0.64 |
| 20 | 0.91 | 0.91 | 0.81 |
| 18 | 1.21 | 1.21 | 1.02 |
| 16 | 1.52 | 1.52 | 1.29 |
| 14 | 1.90 | 1.90 | 1.63 |
| 12 | 2.66 | 2.66 | 2.05 |
| 10 | 3.42 | 3.42 | 2.59 |
| 8 | 4.17 | 4.17 | 3.26 |
| 7 | 4.55 | 4.55 | — |
| 3 | 6.07 | 6.07 | — |

**Note:** Indian job shops commonly stock 0.5mm, 0.8mm, 1.0mm, 1.2mm, 1.5mm, 2.0mm, 2.5mm, 3.0mm, 4.0mm, 5.0mm, 6.0mm, 8.0mm, 10.0mm, 12.0mm, and 16.0mm.

### 8.3 Material Prices — India (2025-2026 approximate)

| Material | Density (kg/m3) | Price (₹/kg) | Notes |
|----------|----------------|-------------|-------|
| Mild Steel (CR) | 7,850 | ₹55-70 | Cold Rolled, most common |
| Mild Steel (HR) | 7,850 | ₹48-60 | Hot Rolled, ≥3mm usually HR |
| Stainless Steel 304 | 8,000 | ₹200-280 | Most common SS grade |
| Stainless Steel 316 | 8,000 | ₹300-400 | Marine/chemical environments |
| Aluminum 5052 | 2,680 | ₹250-320 | Good formability |
| Aluminum 6061 | 2,700 | ₹280-350 | Higher strength |
| Galvanized Steel | 7,850 | ₹65-85 | Pre-coated |
| Copper | 8,960 | ₹750-900 | Electrical enclosures |
| Brass | 8,530 | ₹500-650 | Decorative, electrical |

### 8.4 Material Cost Calculation

```
Material Cost = (sheet_length × sheet_width × thickness × density × price_per_kg) / utilization%

Example:
  Part requires 300mm × 200mm blank, 2mm MS CR
  Sheet: 1250 × 2500 × 2mm
  Parts per sheet = floor(1250/300) × floor(2500/200) = 4 × 12 = 48
  Utilization = (48 × 300 × 200) / (1250 × 2500) = 92.2%

  Material per part = (0.3 × 0.2 × 0.002 × 7850 × 65) / 0.922 = ₹66.5
```

### 8.5 Fiber Laser vs CO2 in India

| Factor | Fiber Laser | CO2 Laser |
|--------|------------|-----------|
| Market share (India) | ~70% of new installs | Declining, legacy |
| Running cost | ₹400-700/hr | ₹600-1200/hr |
| Speed advantage | 2-3x faster on <6mm | Better on >20mm thick |
| Reflective metals (Al, Cu, Brass) | Handles well | Reflects, damages optics |
| Maintenance | Lower, solid-state | Higher, mirrors/gas/tubes |
| Capital cost (India) | ₹25-60 lakh (1-3kW) | ₹15-30 lakh (used) |
| Common power in Indian shops | 1kW, 1.5kW, 2kW, 3kW | 1kW, 2kW (legacy) |

**For Costimize: Default to 3kW fiber laser as the reference machine.** This is the most common mid-range machine in Indian job shops with capacity up to 15mm MS, 10mm SS, and 8mm Al.

---

## 9. Nesting & Material Utilization

### 9.1 Typical Utilization by Part Geometry

| Part Type | Utilization % | Notes |
|-----------|--------------|-------|
| Rectangular/square parts | 85-95% | Grid nesting, very efficient |
| L-shaped brackets | 75-85% | Some interlocking possible |
| Circular/round parts | 65-78% | Inherent gap waste |
| Complex irregular shapes | 60-75% | Depends on nesting software |
| Mixed batch (variety) | 70-85% | Multi-part nesting helps |

### 9.2 Default Values for Cost Estimation

For a cost estimator without actual nesting:
- **Conservative default: 75%** — use when part geometry is unknown
- **Rectangular parts: 85%**
- **Simple shapes with cutouts: 78%**
- **Complex/irregular: 68%**

### 9.3 Skeleton and Clamp Allowances

```
Usable sheet area = (sheet_length - 2 × edge_margin) × (sheet_width - 2 × edge_margin)

Where:
  edge_margin = 10-15mm (laser clamp zone / sheet edge scrap)
```

---

## 10. Open-Source Tools & References

### 10.1 Open-Source Projects

| Project | Language | Description |
|---------|----------|-------------|
| [sheet-metal-cost-calculator](https://github.com/rudloffl/sheet-metal-cost-calculator) | Python/Jupyter | DXF-based cost prediction for sheet metal parts |
| [FreeCAD Sheet Metal Workbench](https://github.com/shaise/FreeCAD_SheetMetal) | Python/C++ | Sheet metal design with unfolding |
| [JETCAM QuickCost](https://www.jetcam.net/quickcost.php) | Proprietary (free tier) | Quick cost estimation tool |

### 10.2 Commercial Tools (Reference)

| Tool | Approach | Notes |
|------|----------|-------|
| aPriori | Physics-based, 3D model required | Enterprise, $100K+ |
| Paperless Parts | ML + manual input | SaaS for job shops |
| MTI Costimator | Formula-based | Legacy, formula library |
| SecturaSOFT | Flat pattern analysis | DXF/DWG import |
| SheetMetal.Me | Online calculators | Free reference |

### 10.3 Key Research Papers

- "Nesting of Complex Sheet Metal Parts" — ResearchGate, algorithms for optimal material utilization
- MIT thesis: "Optimization of Throughput in Sheet Metal Manufacturing by Tuning Sheet Metal Nesting Strategy" (2023)
- "Analysis and optimization of the piercing process in laser beam cutting" — ScienceDirect (2021)

### 10.4 Useful Online Calculators

- [LaserSpecHub Cutting Time Calculator](https://laser-spec-hub.vercel.app/tools/cutting-time-calculator)
- [ESAB Weld Cost Calculator (QWPA)](https://esab.com/us/nam_en/support/tools/calculators/quick-weld-productivity-analyzer/)
- [Pacific Press Brake Tonnage Calculator](https://www.pacific-press.com/hydraulic-press-and-press-brake-calculators/press-brake-bending-force-calculator/)
- [CustomPartNet Deep Drawing Force Calculator](https://www.custompartnet.com/calculator/deep-drawing-force)

---

## 11. Implementation Plan for Costimize

### 11.1 Recommended config.py Additions

```python
# --- Sheet Metal: Laser Cutting ---
LASER_MACHINE_RATE = 2500          # ₹/hr (3kW fiber laser, India default)
LASER_POWER_KW = 3                 # kW (reference machine)
LASER_PIERCE_TIME_BASE = 0.5      # seconds (for 1mm, scales with thickness)
LASER_GAS_COST_PER_HR = 150       # ₹/hr average (N2)
LASER_OPERATOR_RATE = 200         # ₹/hr

# --- Sheet Metal: Bending ---
BEND_MACHINE_RATE = 800           # ₹/hr (CNC press brake 100T)
BEND_SETUP_TIME_MIN = 20         # minutes first setup
BEND_TOOL_CHANGE_MIN = 8         # minutes per tool change
BEND_TIME_SIMPLE_SEC = 10        # seconds per simple bend
BEND_TIME_COMPLEX_SEC = 25       # seconds per complex bend

# --- Sheet Metal: Welding ---
WELD_MIG_RATE_PER_M = 18         # ₹/meter of weld
WELD_TIG_RATE_PER_M = 40         # ₹/meter of weld
WELD_SPOT_RATE_EACH = 4          # ₹/spot
WELD_SETUP_MIN = 20              # minutes

# --- Sheet Metal: Surface Finish ---
FINISH_POWDER_COAT_PER_SQM = 120  # ₹/sq.m
FINISH_ZINC_PLATE_PER_SQM = 250   # ₹/sq.m
FINISH_ANODIZE_PER_SQM = 350      # ₹/sq.m
FINISH_PASSIVATE_PER_SQM = 50     # ₹/sq.m
FINISH_PAINT_PER_SQM = 100        # ₹/sq.m
FINISH_DEBURR_PER_EDGE_M = 10     # ₹/edge meter

# --- Sheet Metal: Nesting ---
DEFAULT_UTILIZATION_PCT = 75      # % (conservative, no nesting engine)
RECT_UTILIZATION_PCT = 85         # % for rectangular parts
SHEET_EDGE_MARGIN_MM = 12         # mm clamp zone

# --- Sheet Metal: Material ---
SHEET_SIZES_MM = [
    (1250, 2500),  # Standard 4' × 8'
    (1500, 3000),  # Standard 5' × 10'
    (1000, 2000),  # Small sheet
]
```

### 11.2 Cutting Speed Lookup Structure

```python
# Nested dict: LASER_SPEEDS[material][thickness_mm] = speed_m_per_min (at 3kW)
LASER_SPEEDS_3KW = {
    "mild_steel": {1: 35, 2: 20, 3: 10, 5: 5, 8: 2.5, 10: 1.8, 12: 1.2, 15: 0.8, 20: 0.4},
    "stainless_steel": {1: 28, 2: 16, 3: 8, 5: 4, 8: 2, 10: 1.5, 12: 1.0, 15: 0.6},
    "aluminum": {1: 25, 2: 13, 3: 7, 5: 3.5, 8: 1.8, 10: 1.2, 12: 0.8},
    "galvanized_steel": {1: 33, 2: 18, 3: 9, 5: 4.5, 8: 2.3, 10: 1.6, 12: 1.1},
    "copper": {1: 15, 2: 8, 3: 4, 5: 2},
    "brass": {1: 18, 2: 10, 3: 5, 5: 2.5, 8: 1.2},
}
```

### 11.3 Proposed Engine Structure

```
engines/
  sheet_metal/
    __init__.py
    cost_engine.py        # Main calculator (frozen dataclass output)
    cutting_db.py         # Laser speeds, pierce times, gas costs
    bending_db.py         # Tonnage calc, K-factors, bend times
    material_db.py        # Sheet materials, densities, prices, sizes
    welding_db.py         # Weld rates by process
    finish_db.py          # Surface finish rates
```

### 11.4 Input Requirements (from AI Vision or Manual)

```
Required inputs:
  - Material type + thickness (mm)
  - Total cutting perimeter (mm) — from DXF or AI vision
  - Number of pierce points (holes + outer contour)
  - Number of bends + bend complexity
  - Part bounding box (for nesting/utilization estimate)
  - Quantity
  - Surface finish type (optional)
  - Weld length + type (optional, for assemblies)
  - Tolerances (optional, for surcharges)
```

---

## Sources

- [Laser Cutting Cost in India 2026 — Cyclotron Industries](https://cyclotronindustries.com/laser-cutting-cost-in-india/)
- [Laser Cutting Charges India — Sawant Group](https://www.sawantgroup.co.in/laser-cutting-charges-india/)
- [Fiber Laser Cutting Speed Chart — LaserSpecHub](https://laser-spec-hub.vercel.app/guides/cutting-speed-chart)
- [Four Steps to Calculate Manufacturing Cost — Dallan](https://www.dallan.com/en/news/four-steps-to-calculate-the-manufacturing-cost-of-sheet-metal-products/)
- [Sheet Metal Fabrication Cost Guide — Komacut](https://www.komacut.com/blog/sheet-metal-fabrication-cost-guide/)
- [Sheet Metal Fabrication Cost Calculator — Xometry](https://www.xometry.com/resources/sheet/sheet-metal-fabrication-cost-calculator/)
- [Press Brake Bending Basics — The Fabricator](https://www.thefabricator.com/thefabricator/article/bending/press-brake-bending-basics-die-angles-tonnage-and-k-factors)
- [Press Brake Bending Force and Tonnage — MaxtorMetal](https://maxtormetal.com/how-to-calculate-press-brake-bending-force-and-tonnage/)
- [Four Steps to Calculate Press Brake Tonnage — The Fabricator](https://www.thefabricator.com/thefabricator/article/bending/four-steps-to-calculate-press-brake-tonnage-limits)
- [K-factors, Y-factors, and Press Brake Bending — The Fabricator](https://www.thefabricator.com/thefabricator/article/bending/k-factors-y-factors-and-press-brake-bending-precision)
- [How to Calculate Metal Stamping Cost — Be-Cu](https://be-cu.com/blog/how-to-calculate-metal-stamping-cost-and-tooling-prices/)
- [Stamping Tonnage in Progressive Stamping — The Fabricator](https://www.thefabricator.com/thefabricator/article/bending/stamping-calculation-calculating-tonnage-in-progressive-stamping)
- [Deep Drawing Calculations — EMS Metalworking](https://ems-metalworking.com/deep-drawing-calculations/)
- [Deep Drawing Force Calculator — CustomPartNet](https://www.custompartnet.com/calculator/deep-drawing-force)
- [ESAB Weld Cost Calculator](https://esab.com/us/nam_en/support/tools/calculators/quick-weld-productivity-analyzer/)
- [Sheet Metal Cost Calculator — GitHub](https://github.com/rudloffl/sheet-metal-cost-calculator)
- [Sheet Metal Gauge Chart — SheetMetal.Me](https://sheetmetal.me/sheet-metal-gauge-chart/)
- [MIT Thesis: Nesting Strategy Optimization](https://dspace.mit.edu/handle/1721.1/152702)
- [Sheet Metal Nesting Strategy Guide — Anebon](https://www.anebon.com/news/sheet-metal-nesting-strategy-guide-optimizing-layouts-to-minimize-scrap-and-cut-costs/)
- [Estimate Sheet Metal Fabrication Costs — Eabel](https://www.eabel.com/estimate-sheet-metal-fabrication-costs/)
- [Sheet Metal Fabrication Cost Breakdown — TZR Metal](https://tzrmetal.com/sheet-metal-fabrication-cost/)
