---
slug: sheet-metal-processes
title: Sheet Metal Processes — Laser Cutting, Bending, Welding, and Nesting
keywords: sheet metal, laser cutting, fiber laser, press brake, bending, tonnage, nesting, utilization, welding, MIG, TIG, spot weld, pierce time, cutting speed, powder coating, Indian sheet sizes, stamping, deep drawing, bend allowance, K-factor
sources: sheet-metal-cost-estimation.md, cost_engine.py, cutting_db.py, bending_db.py
updated: 2026-04-04
---

# Sheet Metal Processes

Sheet metal manufacturing follows a different cost model than machining. Material is typically 30-50% of total cost (up to 86% for simple flat parts), with cutting and bending as the main process costs.

## Master Cost Formula

```
Total Cost = Material + Cutting + Bending + Welding + Surface Finish + Overhead (15%) + Profit (20%)

Material Cost = blank_weight x price_per_kg / (utilization% / 100)
```

## Laser Cutting

### Reference Machine: 3kW Fiber Laser

The most common setup in Indian job shops. Machine rate: 2,500 INR/hr. Gas cost: ~150 INR/hr (N2 average). Total power draw: ~12 kW including chiller.

### Cutting Speeds (m/min) at 3kW Fiber Laser

| Thickness | Mild Steel | Stainless Steel | Aluminum | Galvanized | Brass | Copper |
|-----------|-----------|-----------------|----------|------------|-------|--------|
| 1mm | 35 | 28 | 25 | 33 | 18 | 15 |
| 2mm | 20 | 16 | 13 | 18 | 10 | 8 |
| 3mm | 10 | 8 | 7 | 9 | 5 | 4 |
| 5mm | 5 | 4 | 3.5 | 4.5 | 2.5 | 2 |
| 8mm | 2.5 | 2 | 1.8 | 2.3 | 1.2 | -- |
| 10mm | 1.8 | 1.5 | 1.2 | 1.6 | -- | -- |
| 12mm | 1.2 | 1.0 | 0.8 | 1.1 | -- | -- |
| 15mm | 0.8 | 0.6 | -- | -- | -- | -- |
| 20mm | 0.4 | -- | -- | -- | -- | -- |

Mild steel uses O2 assist gas; stainless and aluminum use N2 for clean edges.

### Pierce Times (seconds per pierce at 3kW)

| Thickness | Base Time | Stainless (1.5x) | Aluminum (1.2x) |
|-----------|-----------|-------------------|------------------|
| 1mm | 0.3 | 0.45 | 0.36 |
| 2mm | 0.5 | 0.75 | 0.60 |
| 3mm | 0.8 | 1.2 | 0.96 |
| 5mm | 1.5 | 2.25 | 1.8 |
| 8mm | 3.0 | 4.5 | 3.6 |
| 10mm | 5.0 | 7.5 | 6.0 |
| 12mm | 8.0 | 12.0 | 9.6 |
| 15mm | 12.0 | 18.0 | 14.4 |

Thick plate (>12mm) may require pulse piercing at 5-15 seconds.

### Cutting Time Calculation

```
Total time = (cutting_length / speed + pierce_count x pierce_time) x 1.15
```

The 1.15 factor covers non-productive time: head positioning, acceleration/deceleration between cuts.

### Laser Machine Hourly Rates (India)

| Machine | Rate (INR/hr) |
|---------|--------------|
| Fiber Laser 1-2kW | 1,200-1,800 |
| Fiber Laser 3-6kW | 2,000-3,500 |
| Fiber Laser 8-12kW | 3,500-5,000 |
| CO2 Laser (legacy) | 800-1,500 |
| Plasma Cutter | 600-1,000 |
| Waterjet | 1,500-2,500 |
| Turret Punch | 800-1,200 |

## Press Brake Bending

### Tonnage Formula

```
F (kN) = (UTS x T^2 x L) / (V x 1000)

Where:
  UTS = ultimate tensile strength (N/mm2)
  T   = sheet thickness (mm)
  L   = bend length (mm)
  V   = die opening (mm) = 8 x T (rule of thumb)
```

Tonnage in metric tons = F(kN) / 9.81

### Material Factors for Tonnage

| Material | UTS (N/mm2) | Relative Tonnage |
|----------|-------------|-----------------|
| Aluminum 5052 | 230 | 0.5x |
| Copper | 220 | 0.45x |
| Brass | 350 | 0.55x |
| Mild Steel | 400-500 | 1.0x (baseline) |
| Stainless Steel 304 | 500-700 | 1.5x |
| Spring Steel | 800-1200 | 2.0x |

### Press Brake Selection

| Tonnage Required | Category | Rate (INR/hr) |
|-----------------|----------|--------------|
| Up to 50T | Small (manual) | 600 |
| 50-100T | Medium (CNC) | 900 |
| 100-250T | Large (CNC) | 1,200 |
| 250-600T | Heavy (CNC) | 1,800 |

### Time per Bend

| Complexity | Time (sec) | Description |
|-----------|------------|-------------|
| Simple | 10 | Single straight 90-degree bend |
| Standard | 12 | 2-3 bends, same tool |
| Complex | 25 | Tool change needed per bend |
| Hemming | 20 | Two-step: acute + close |
| Z-bend | 32 | Requires repositioning |

Setup: 20 min first setup + 8 min per additional tool change.

### Bending Force Multipliers

| Method | Force Multiplier | Use Case |
|--------|-----------------|----------|
| Air Bending | 1.0x | Most common, flexible angles |
| Bottom Bending | 1.5x | Better accuracy, spring-back control |
| Coining | 5-10x | Highest precision, no spring-back |

### Bend Allowance (K-Factor)

```
Bend Allowance = angle_rad x (R + K x T)
```

| Material | K-factor |
|----------|----------|
| Soft (Al, Cu) | 0.33 |
| Medium (Mild Steel) | 0.40-0.45 |
| Hard (Stainless, Spring Steel) | 0.45-0.50 |
| Industry default | 0.446 |

## Welding

| Type | Rate | Setup |
|------|------|-------|
| MIG | 18 INR/meter | 20 min |
| TIG | 40 INR/meter | 20 min |
| Spot | 4 INR/spot | 20 min |

Setup cost is amortized over quantity.

## Surface Finishing

| Finish | Rate (INR/sq.m) |
|--------|----------------|
| Powder Coating | 120 |
| Zinc Plating | 250 |
| Anodizing | 350 |
| Passivation | 50 |
| Wet Paint | 100 |
| Galvanizing | 60 |

Applied to both sides of the part: area = 2 x L x W.

## Nesting and Material Utilization

Nesting determines how many parts can be cut from a standard sheet, directly affecting material cost. Newton-Metre estimates utilization based on part bounding box size:

- Small parts (<200mm): 75-85% utilization
- Medium parts (200-600mm): 65-75%
- Large parts (>600mm): 55-65%

### Standard Indian Sheet Sizes

- 1220 x 2440 mm (4' x 8') -- most common
- 1250 x 2500 mm
- 1500 x 3000 mm (5' x 10')

## Stamping vs Laser: Volume Decision

| Factor | Laser Cutting | Stamping/Punching |
|--------|--------------|-------------------|
| Setup cost | Low (program only) | High (die: 50K-5L INR) |
| Per-part cost | Higher | Much lower |
| Crossover | -- | 500-5,000 parts |
| Flexibility | Any shape, instant change | Fixed to die geometry |
| Thickness range | Up to 20-25mm | Up to 6-8mm typical |

For quantities below 500-1,000 parts, laser cutting is almost always cheaper. Above 5,000 parts, progressive die stamping dominates on per-part cost.
