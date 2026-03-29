# Sandvik Coromant Data Extraction
## Extracted March 29, 2026 from 5 Sandvik PDFs (800MB total)
## Expanded March 29, 2026 — systematic page-by-page extraction of all 391 Training Handbook pages

### PDF Inventory & What Each Contains

| PDF | Pages | Size | Content Type | Cost Data? |
|-----|-------|------|-------------|-----------|
| **Training Handbook** | 391 | 161MB | Theory, formulas, kc1, economics | **YES — the gold standard** |
| Latest Cutting Tools 2026 | 450 | 28MB | Product catalog, ordering codes | No — tool dimensions only |
| Indexable Milling Tools 2025 | ~350 | 101MB | Product catalog, insert specs | No — tool geometries only |
| Parting & Grooving Tools 2026 | 272 | 77MB | Product catalog, tool systems | No — tool specs only |
| Solid Round Tools 2026 | 674 | 449MB | Product catalog (drills, taps, endmills) | No — ordering codes only |

**Key finding:** Only the Training Handbook contains cutting data. All 4 catalogs are product selection guides with ordering codes, dimensions, and insert specs. They explicitly say: "For cutting data, use CoroPlus Tool Guide online."

---

# TRAINING HANDBOOK (The Gold Standard — 391 pages)

## ISO Material Classification (P/M/K/N/S/H)

| ISO Group | Material | Subgroups |
|-----------|----------|-----------|
| **P** | Steel | P1: Unalloyed, P2: Low-alloyed (<=5%), P3: High-alloyed (>5%), P4: Sintered |
| **M** | Stainless Steel | M1: Ferritic/Martensitic, M2: Austenitic, M3: Duplex, M5: Super-austenitic |
| **K** | Cast Iron | K1: Malleable, K2: Gray (GCI), K3: Nodular (NCI), K4: CGI, K5: ADI |
| **N** | Non-ferrous | N1: Aluminum, N2: Magnesium, N3: Copper, N4: Zinc |
| **S** | HRSA & Titanium | S1: Iron-based, S2: Nickel-based, S3: Cobalt-based, S4: Titanium |
| **H** | Hardened Steel | H1: 45-65 HRC, H2: Chilled cast iron, H3: Stellites |

## Specific Cutting Force kc1 Values (N/mm2) — THE CORE DATA

kc1 = specific cutting force at 1mm chip thickness. Used in ALL power calculations.

### Steel (ISO P) Detailed

| MC Code | CMC | Description | kc1 (N/mm2) | HB | mc |
|---------|-----|-------------|-------------|-----|-----|
| P1.1.Z.AN | 01.1 | Unalloyed C 0.1-0.25% | 1500 | 125 | 0.25 |
| P1.2.Z.AN | 01.2 | Unalloyed C 0.25-0.55% | 1600 | 150 | 0.25 |
| P1.3.Z.AN | 01.3 | Unalloyed C 0.55-0.80% | 1700 | 170 | 0.25 |
| P1.3.Z.AN | 01.4 | High carbon, annealed | 1800 | 210 | 0.25 |
| P1.3.Z.HT | 01.5 | Non-hardened | 2000 | 300 | 0.25 |
| P2.1.Z.AN | 02.1 | Low-alloyed, H&T | 1700 | 175 | 0.25 |
| P2.5.Z.HT | 02.2 | Low-alloyed, H&T | 1900 | 300 | 0.25 |

### Summary by ISO Group

| ISO Group | Material | kc1 Range (N/mm2) |
|-----------|----------|-------------------|
| P | Steel | 1500-3100 |
| M | Stainless Steel | 1800-2850 |
| K | Cast Iron | 790-1350 |
| N | Non-ferrous (Al) | 350-700 |
| S (HRSA) | Nickel/Cobalt | 2400-3100 |
| S (Ti) | Titanium | 1300-1400 |
| H | Hardened Steel | 2550-4870 |

### Mapping to Our Materials

| Our Material | ISO Group | kc1 (N/mm2) | mc |
|-------------|-----------|-------------|-----|
| Aluminum 6061 | N1 | 600 | 0.25 |
| Mild Steel IS2062 | P1.2 | 1600 | 0.25 |
| Stainless Steel 304 | M2 | 2000 | 0.25 |
| Brass IS319 | N3 | 750 | 0.25 |
| EN8 Steel | P2.1 | 1700 | 0.25 |
| EN24 Steel | P2.5 | 1900 | 0.25 |
| Copper | N3 | 800 | 0.25 |
| Cast Iron | K2 | 1100 | 0.25 |
| Titanium Grade 5 | S4 | 1350 | 0.25 |

## Power Calculation Formulas (Sandvik Standard)

### Turning
```
vc = (pi * Dm * n) / 1000            [m/min]
n = (vc * 1000) / (pi * Dm)          [rpm]
Tc = lm / (fn * n)                    [min] (machining time)
Q = vc * ap * fn                      [cm3/min] (MRR)
kc = kc1 * (1/hm)^mc * (1 - gamma0/100)  [N/mm2]
hm = fn * sin(KAPR)                   [mm] (average chip thickness)
Pc = (vc * ap * fn * kc) / (60 * 10^3)    [kW] (net cutting power)
```

### Milling
```
vf = fz * zc * n                      [mm/min] (table feed)
vc = (pi * Dcap * n) / 1000          [m/min]
Q = (ap * ae * vf) / 1000            [cm3/min] (MRR)
Pc = (ae * ap * vf * kc) / (60 * 10^6)    [kW]
Mc = (Pc * 30 * 10^3) / (pi * n)     [Nm] (torque)
```

### Drilling
```
vf = fn * n                           [mm/min] (penetration rate)
Q = (vc * DC * fn) / 4               [cm3/min] (MRR)
Pc = (fn * vc * DC * kc) / (240 * 10^3)   [kW]
Mc = (Pc * 30 * 10^3) / (pi * n)     [Nm]
Ff = 0.5 * kc * (DC/2) * fn * sin(KAPR)   [N] (feed force)
```

### Boring
```
Pc = (vc * ap * fn * kc) / (60 * 10^3) * (1 - ap/DC)  [kW]
```

### Key Variable
- gamma0 = effective rake angle (reduces kc by 1% per degree)
- KAPR = entering/lead angle (affects chip thickness)

## Tool Life Data

**Sandvik base tool life: 15 minutes** (all their recommendations assume this)

### Tool Life Correction Factors (multiply recommended Vc)

| Target Tool Life (min) | Speed Factor |
|----------------------|-------------|
| 10 | 1.11 |
| 15 (base) | 1.00 |
| 20 | 0.93 |
| 25 | 0.88 |
| 30 | 0.84 |
| 45 | 0.75 |
| 60 | 0.70 |

### Hardness Compensation Factors

| ISO | Base HB | -60 HB | -40 HB | -20 HB | +20 HB | +40 HB | +60 HB |
|-----|---------|--------|--------|--------|--------|--------|--------|
| P (P2) | 180 | 1.44 | 1.25 | 1.11 | 0.91 | 0.84 | 0.77 |
| M (M1) | 180 | 1.42 | 1.24 | 1.11 | 0.91 | 0.84 | 0.78 |
| K (K2) | 220 | 1.21 | 1.13 | 1.06 | 0.95 | 0.90 | 0.86 |
| N (N1) | 75 | - | - | 1.05 | 0.95 | - | - |
| S (S2) | 350 | - | - | 1.12 | 0.89 | - | - |

## Machining Economics (Critical Insight)

### Typical Cost Breakdown
- Tooling: **3%** (variable)
- Workpiece material: **17%** (variable)
- Machine & holders: **27%** (fixed)
- Labour: **31%** (fixed)
- Buildings & admin: **22%** (fixed)

### The 15% Rule
- Reducing tool price by 30% saves only **1%** on component cost
- Increasing tool life by 50% saves only **1%** on component cost
- **Increasing cutting data by 20% saves 15% on component cost**

### Optimization Priority (THIS ORDER)
1. **Maximize depth of cut (ap)** — fewest passes
2. **Maximize feed rate (fn)** — shortest cutting time
3. **Then optimize cutting speed (vc)** — best economy

### Actual Cutting Time
Only **24%** of planned production time is actual cutting:
- 60% machine utilization × 50% cutting time × 80% availability = 24%

## Chip Breaking Working Areas (Steel CMC 02.1)

| Type | ap (mm) | fn (mm/rev) |
|------|---------|-------------|
| Finishing (F) | 0.25-1.5 | 0.07-0.3 |
| Medium (M) | 0.5-5.5 | 0.15-0.5 |
| Roughing (R) | 1.0-7.5 | 0.25-0.7 |

## Tool Wear — Max Recommended
- Max flank wear: **0.5mm**
- Tool life sensitivity order: Speed (largest) > Feed > Depth of cut (smallest)

## MC Code Structure (Material Classification)

Format: `{ISO Group}{Material Group}.{Subgroup}.{Manufacturing Process}.{Heat Treatment}`

| Field | Values |
|-------|--------|
| ISO Group | P, M, K, N, S, H |
| Manufacturing Process | Z = forged/rolled/cold drawn, C = casting |
| Heat Treatment | AN = annealed, HT = hardened & tempered, UT = untreated |

Example: `P1.2.Z.AN` = Steel, unalloyed, carbon 0.25-0.55%, forged/rolled, annealed

This is more precise than old CMC codes because it captures manufacturing process and heat treatment, which affect machinability.

## Insert Geometry Working Areas — Detailed

### Turning (Steel CMC 02.1)

| Geometry | Operation | ap (mm) | fn (mm/rev) | CNMG Insert |
|----------|-----------|---------|-------------|-------------|
| **-PF** | Finishing | 0.25-1.5 | 0.07-0.3 | CNMG 120404-PF |
| **-PM** | Medium | 0.5-5.5 | 0.15-0.5 | CNMG 120408-PM |
| **-PR** | Roughing | 1.0-7.5 | 0.25-0.7 | CNMM 120412-PR |

### Insert Shape Selection by Entering Angle

| Insert Shape | KAPR | hex/fn Ratio | Contact Length at ap=2mm |
|-------------|------|-------------|------------------------|
| CNMG (80° rhombic) | 95° | 0.96 | 2.08 mm |
| SNMG (square) | 75° | 0.87 | 2.30 mm |
| DNMG (55° rhombic) | 45° | 0.71 | 2.82 mm |
| WNMG (trigon) | 45° | 0.71 | 2.82 mm |

**Rule:** Smaller entering angle → thinner chip, wider contact → more stable but higher radial force.

## Entering Angle Selection Guide

| KAPR | Best For | Trade-off |
|------|----------|-----------|
| **95°** | General turning, shoulders, facing | Good all-around, slightly thinner wall risk |
| **75°** | General turning, first choice | Good balance of forces |
| **45°** | Long overhang, vibration-prone setups | Reduces vibration, but 0.71× chip thickness |
| **Round (RCMT)** | Variable approach, profiling | Most stable, but requires more power |

## Milling Theory — Key Rules

### Cutter Diameter Selection
- Cutter diameter should be **20-40% larger** than width of cut
- **2/3 rule**: 2/3 in cut, 1/3 out of cut (e.g., 150mm cutter → 100mm in cut)
- Moving cutter off center gives more constant, favorable cutting forces

### Always Use Climb Milling
- Insert starts cut with large chip thickness (good)
- Avoids burnishing/rubbing that conventional milling causes
- Less heat, minimal work-hardening

### Approach Angle Effects on Milling

| Angle | hex Calculation | Best For |
|-------|----------------|----------|
| **90°** | hex = fz | Thin walls, unstable fixtures, true shoulders |
| **45°** | hex = fz × 0.71 | General purpose first choice, reduces vibration |
| **Round inserts** | hex varies with ap | Robust, profiling, heavy roughing |
| **10-15°** | hex = fz × 0.17-0.26 | Extreme feed rates at very shallow ap |

## Drilling — Key Data

### Drill Types by Depth

| Max Hole Depth | Tool Type |
|---------------|-----------|
| 3×DC | Standard solid carbide (CoroDrill 860) |
| 5×DC | Long series solid carbide |
| 5-8×DC | Indexable (CoroDrill 880) |
| >8×DC | Gun drill / BTA |

### Drilling Power Formula (Accurate)
```
kc = kc1 × (fz × sin(KAPR))^(-mc) × (1 - gamma0/100)
Pc = (fn × vc × DC × kc) / (240 × 10^3)    [kW, metric]
```
Where:
- KAPR = 70° for indexable drills (CoroDrill 880)
- KAPR = 88° for solid carbide drills (CoroDrill Delta-C)
- gamma0 = 30° typical for solid carbide drills

### Feed Force and Torque
```
Ff ≈ 0.5 × kc × (DC/2) × fn × sin(KAPR)    [N]
Mc = (Pc × 30 × 10^3) / (pi × n)            [Nm]
```

### Drilling Speed Effects
- **Too high vc:** rapid flank wear, plastic deformation, poor hole quality, bad tolerance
- **Too low vc:** built-up edge, bad chip evacuation, higher risk of breakage
- **Higher vc beneficial** for chip formation in soft, long-chipping materials (low carbon steel)

## Boring — Additional Data

### Boring Power Formula (with correction factor)
```
Pc = (vc × ap × fn × kc) / (60 × 10^3) × (1 - ap/DC)    [kW]
```
The `(1 - ap/DC)` term reduces power as depth of cut approaches bore diameter — unique to boring.

## Threading — Key Data

### Thread Types and Selection
- **Multi-point inserts**: 2+ teeth, halves number of passes, needs stable setup
- **V-profile inserts**: Flexible (one insert fits multiple pitches), may leave burr
- **Full profile (topping)**: Best thread form control, one insert per pitch

### Threading Infeed Methods
Infeed method significantly impacts chip control, insert wear, thread quality, and tool life.

### Shim Inclination
- Standard shim = **1°** (default in all holders)
- Larger pitches on smaller diameters need higher inclination (up to 3°+)
- Check inclination chart: diameter vs pitch determines shim angle

## Cutting Tool Materials — Hierarchy

Listed from hardest/most wear-resistant to toughest:

| Material | Code | Vc Range | Best For |
|----------|------|----------|----------|
| **Diamond (PCD)** | DP | Highest | Non-ferrous (Al, Cu), composites. Dissolves in iron! |
| **Cubic Boron Nitride (CBN)** | BN | Very high | Hardened steel (>45 HRC), chilled cast iron |
| **Ceramics** | CA/CN/CC | High | Cast iron at high speed, hardened steel, HRSA |
| **Cermet** | HT/HC | Medium-high | Finishing with close tolerances, good surface finish |
| **Coated Carbide** | HC | Medium | **Dominant — 70%+ of all inserts.** All materials, all operations |
| **Uncoated Carbide** | HW | Medium | Sharp edges needed, sticky materials (Al, HRSA) |
| **HSS** | HSS | Lowest | Taps, complex geometry tools |

### Cemented Carbide Composition
- **WC (tungsten carbide)**: ~80% — provides hardness and abrasive wear resistance
- **Co (cobalt)**: 4-15% — binder phase, more Co = more toughness but less hardness
- **TiC/TaC/NbC (gamma phase)**: ~5-13% — better hot hardness, less reactive at high temps
- **WC grain size**: Finer grain = harder but more brittle

### Coating Types

| Type | Temp | Thickness | Properties | Best For |
|------|------|-----------|-----------|----------|
| **CVD** | ~1000°C | 5-20 μm | Thick, wear-resistant, Al2O3 layer | Turning, general machining |
| **PVD** | ~500°C | 3-6 μm | Tough, sharp edges preserved | Milling, drilling, grooving, sharp-edge tools |

Key coating layers:
- **TiN** (titanium nitride): gold color, general purpose
- **Ti(C,N)** (titanium carbonitride): MTCVD, mechanical wear resistance
- **Al2O3** (aluminum oxide): chemical and thermal wear resistance — **key for high-speed steel turning**
- **TiAlN** (titanium aluminum nitride): PVD, good for milling

### ISO Grade Classification (P area example)

| ISO Code | Application |
|----------|------------|
| **P01** | Internal/external finishing, high vc, small chip area, tight tolerance |
| **P10** | Turning, copying, threading, milling, high vc, small-medium chip area |
| **P20** | Turning, copying, medium vc, facing, medium-difficult conditions |
| **P30** | Turning, milling, facing, medium-low vc, medium-large chip area, tough conditions |
| **P40** | Turning, facing, milling, grooving, low vc, large chip area, very tough conditions |
| **P50** | Extreme toughness needed, lowest vc, largest chip area |

**Lower number = more wear resistant, higher number = more tough**

## Machining Economy — Expanded

### Production Time Breakdown (Sandvik Data)

| Category | % of Planned Time |
|----------|------------------|
| Machine utilization | 60% |
| Of utilized time: actual cutting | 50% |
| Machine availability | 80% |
| **Actual cutting as % of planned time** | **24%** |

This means **76% of planned production time is NOT cutting**. Breakdown:
- Workpiece change
- Tool change
- Setup and gauging
- Machine stopped/breakdowns
- Other non-cutting time

### High Efficiency Range (Sandvik Definition)

The "High Efficiency Range" is the speed zone between:
- **Economic cutting speed** (lowest cost per part) — lower end
- **Maximum production speed** (most parts per hour) — upper end

Operating within this range is optimal. Below = wasted time. Above = excessive tool cost.

### Productivity vs Cost Trade-off

| Parameter | Effect on Tool Life | Effect on Productivity |
|-----------|-------------------|----------------------|
| Increase ap | Smallest reduction | Direct MRR increase |
| Increase fn | Moderate reduction | Direct MRR increase |
| Increase vc | **Largest reduction** | Direct MRR increase |

**Therefore: maximize ap first, then fn, then vc last** — this is the correct optimization order.

### Worked Example (from p367)

| Scenario | Tooling | Material | Machinery | Labour | Building | **Total** |
|----------|---------|----------|-----------|--------|----------|-----------|
| Today | $0.45 | $1.70 | $2.70 | $3.10 | $2.20 | **$10.15** |
| Lower tool price -30% | $0.20 | $1.70 | $2.70 | $3.10 | $2.20 | **$9.90** (-1%) |
| Increase tool life +50% | $0.21 | $1.70 | $2.70 | $3.10 | $2.20 | **$9.91** (-1%) |
| **Increase cutting data +20%** | $0.30 | $1.70 | $2.16 | $2.48 | $1.76 | **$8.55** (**-15%**) |

The 20% cutting data increase reduces fixed costs (machinery, labour, building) because more parts are made per hour, spreading fixed costs over more units.

## Complete Formula Reference (from p379-391)

### Turning — Metric
```
vc = (pi × Dm × n) / 1000                           [m/min]
n  = (vc × 1000) / (pi × Dm)                        [rpm]
Tc = lm / (fn × n)                                   [min]
Q  = vc × ap × fn                                    [cm3/min]
hm = fn × sin(KAPR)                                  [mm]
kc = kc1 × (1/hm)^mc × (1 - gamma0/100)            [N/mm2]
Pc = (vc × ap × fn × kc) / (60 × 10^3)             [kW]
```

### Milling — Metric
```
vf = fz × zc × n                                     [mm/min]
vc = (pi × Dcap × n) / 1000                          [m/min]
n  = (vc × 1000) / (pi × Dcap)                       [rpm]
fz = vf / (n × zc)                                    [mm/tooth]
fn = vf / n                                            [mm/rev]
Q  = (ap × ae × vf) / 1000                           [cm3/min]
Pc = (ae × ap × vf × kc) / (60 × 10^6)              [kW]
Mc = (Pc × 30 × 10^3) / (pi × n)                    [Nm]
kc = kc1 × (1/hm)^mc × (1 - gamma0/100)            [N/mm2]
```

### Drilling — Metric
```
vf = fn × n                                           [mm/min]
vc = (pi × DC × n) / 1000                            [m/min]
n  = (vc × 1000) / (pi × DC)                         [rpm]
Q  = (vc × DC × fn) / 4                              [cm3/min]
Pc = (fn × vc × DC × kc) / (240 × 10^3)             [kW]
Mc = (Pc × 30 × 10^3) / (pi × n)                    [Nm]
Ff = 0.5 × kc × (DC/2) × fn × sin(KAPR)            [N]
```

### Boring — Metric
```
vf = fn × n                                           [mm/min]
vc = (pi × DC × n) / 1000                            [m/min]
Q  = (vc × DC × fn) / 4                              [cm3/min]
Pc = (vc × ap × fn × kc) / (60 × 10^3) × (1 - ap/DC)  [kW]
Mc = (Pc × 30 × 10^3) / (pi × n)                    [Nm]
Ff = 0.5 × kc × ap × fn × sin(KAPR)                 [N]
```

## Missing from Training Handbook — Where to Get It

The Training Handbook does NOT contain:
1. **Recommended cutting speeds (Vc) by material** — these are in CoroPlus Tool Guide (online tool, not PDF)
2. **Recommended feeds (fn/fz) by material** — same, CoroPlus Tool Guide
3. **Detailed kc1 values beyond P1-P2.5** — full table is in Sandvik's online technical guide

This is by design — Sandvik wants you to use their online tools for specific Vc/fn recommendations, as these depend on the exact insert geometry + grade + material combination. The handbook gives the physics framework; the online tool gives the specific numbers.

**For our engine:** We already have Vc data from Machinery's Handbook. Sandvik's contribution is the physics framework (kc1, power formulas, tool life corrections, hardness compensation) that makes our calculations more accurate.

---

# MILLING CATALOG 2025 (~350 pages)

Product selection catalog — tool geometries and specifications, NOT cutting data.

## Key Tool Families

### Face Milling
| Tool | KAPR | Max ap (mm) | Edges | Best For |
|------|------|-------------|-------|----------|
| CoroMill 245 | 45 deg | 6.5-9.8 | 4 | Heavy roughing to mirror finish |
| CoroMill 345 | 45 deg | 6.0 | 8 | High MRR, economy |
| CoroMill 745 | 42 deg | 5.2 | multi | Best cost per edge |
| CoroMill Century | 90 deg | 11.0 | - | HSM aluminum, PCD/CBN |

### Shoulder Milling
| Tool | Max ap (mm) | Best For |
|------|-------------|----------|
| CoroMill MS20 | 9.0 | True 90 deg, unmanned |
| CoroMill 390 | 5.8-16.0 | Versatile, deep shoulders |
| CoroMill 490 | 5.5-10.0 | 4 edges, roughing-finishing |

### High Feed Milling (for pocketing/facing at extreme feeds)
| Tool | KAPR | Max ap (mm) |
|------|------|-------------|
| CoroMill MH20 | 15 deg | 0.8-1.2 |
| CoroMill 210 | 10 deg | 1.2-2.0 |

## Approach Angle Selection
- **90 deg**: thin walls, unstable fixtures
- **45 deg**: general purpose first choice, reduces vibration
- **10-15 deg**: extreme feed rates at shallow ap

## Insert Geometry Selection
- **Light (-L)**: low forces, good finish, low feed
- **Medium (-M)**: first choice general purpose
- **Heavy (-H)**: strong edge, interrupted cuts, high feeds

---

# PARTING & GROOVING CATALOG 2026 (272 pages)

Product selection catalog — tool systems and insert specifications.

## Tool Systems

| System | Max Part Dia (mm) | Width Range (mm) |
|--------|-------------------|-----------------|
| CoroCut QD | 38-160 | 1-8 |
| CoroCut 2 | <40 | 1.5-8 |
| CoroCut 3 | small | 0.5-3.18 |

## Key Rule
Max parting diameter ≈ 2× cutting depth (CDX)

## Insert Grades per ISO Group
- **P/M (Steel/SS)**: GC1125/1225 (first choice), GC1135 (interrupted), GC4425 (stable high speed)
- **K (Cast Iron)**: Same as P/M grades
- **N (Aluminum)**: H13A (uncoated), GC1205 (PVD)
- **S (Ti/HRSA)**: H13A, S205, GC1105/1205

## No Cutting Speed Data in This Catalog
Vc/fn data is in Training Handbook or CoroPlus Tool Guide online.

---

# LATEST CUTTING TOOLS 2026 (450 pages)

Product selection catalog — complete indexable insert and tool holder ordering guide.

## Contents
- Turning inserts (CoroTurn TR, T-Max P, CoroTurn 107, CoroTurn PI)
- Parting & grooving inserts (CoroCut 2, QD, QF, QI, XS, 3, MB)
- Milling inserts (CoroMill MR20, MS20, MS40, MS60, 390, 490, 245, 345, etc.)
- Drilling tools (CoroDrill DE10, DS20, 881)
- Boring tools (CoroBore BR20, XL, 825)
- Threading tools (CoroThread 266)
- Tapping tools (CoroTap 100/200/300)
- Tool holding and adaptors

**No cutting data.** All pages are ordering codes, dimensions, and insert specifications.

---

# SOLID ROUND TOOLS 2026 (674 pages — largest catalog)

Product selection catalog — solid carbide end mills, drills, taps, and reamers.

## Tool Families

### Milling
- **CoroMill Dura**: Versatile solid carbide end mills, multi-material
- **CoroMill Plura**: Optimized for specific materials/applications (heavy duty, finishing, hard part, ceramic)
- **CoroMill 316**: Modular exchangeable-head system

### Drilling
- **CoroDrill 860-PM**: Optimized for steel (ISO P)
- **CoroDrill 860-MM**: Optimized for stainless (ISO M)
- **CoroDrill 860-SD**: Optimized for HRSA/titanium (ISO S)
- **CoroDrill 860-GM**: General multi-material
- **CoroDrill 860-NM**: Optimized for non-ferrous (ISO N)
- **CoroDrill 862**: Micro drills

### Tapping
- **CoroTap 100**: Straight flute (through holes)
- **CoroTap 200**: Spiral point (through holes)
- **CoroTap 300**: Spiral flute (blind holes)
- **CoroTap 400**: Forming taps (thread forming, no chips)

### Reaming
- **CoroReamer 435/830/835**: Solid carbide reamers for precision holes

**No cutting data.** Tool reconditioning info on p667.

---

# KEY ACTIONS FOR COST ENGINE

## Already Implemented (from Sandvik data)
- ✅ kc1 values mapped to our 9 materials
- ✅ Sandvik power formula (Pc = vc×ap×fn×kc / 60×10³)
- ✅ NON_CUT_TIME_FACTOR = 1.40 (validated by Sandvik's 24% actual cutting time finding)

## Immediate Updates Needed

1. **Add hardness compensation factors** — real-world parts aren't at reference hardness
   - Simple multiplier table from p369: deviation from base HB → speed correction
   - P steel: ±60 HB = 0.77-1.44× speed factor
   - Implementation: add hardness_factor to material_db, multiply against Vc

2. **Add tool life correction factors** — adjust Vc for different target tool lives
   - Our Taylor equation gives tool life; Sandvik's table lets us cross-validate
   - 15 min base → 30 min target = 0.84× speed, 60 min = 0.70× speed

3. **Implement entering angle (KAPR) effect on chip thickness**
   - hex = fn × sin(KAPR) — chip thickness varies with tool geometry
   - 95° → hex/fn = 0.96, 75° → 0.87, 45° → 0.71
   - Affects surface finish and cutting force calculations

4. **Add boring power correction** — `(1 - ap/DC)` factor unique to boring
   - Currently our boring uses same formula as turning
   - Boring requires less power as depth of cut approaches bore diameter

5. **The 15% rule validates our approach** — optimizing cutting parameters (what our engine does) saves 15% per part. Tool cost is only 3% of total. Our approach of physics-based parameter optimization is exactly what Sandvik recommends.

## Future Enhancements
- CoroPlus Tool Guide API (if available) for real-time Sandvik cutting data
- Insert grade recommendation engine (map ISO P01-P50 to operations)
- Parting width optimization (minimize material waste)
- CVD vs PVD grade selection logic (CVD for turning, PVD for milling/drilling)

## Cross-Reference with Machinery's Handbook

| Data Point | Sandvik Source | Machinery's HB Source | Status |
|-----------|---------------|----------------------|--------|
| kc1 (specific cutting force) | Training Handbook p194-195 | Power constants Kp (Table 1a/1b) | Both available, kc1 more precise |
| Cutting speeds by material | NOT in PDFs (CoroPlus online) | Tables for 20+ materials × 5 tool types | HB is our primary Vc source |
| Tool life model | Tool life correction table | Taylor + Colding + ECT models | HB has more theoretical depth |
| Power formula | Pc = vc×ap×fn×kc / 60×10³ | Pc = Kp × Q (simpler) | Sandvik's includes chip thickness correction |
| Feed factors | Not in handbook | Table 2 (C factors) | HB unique data |
| Tool wear factor | Not in handbook | Table 3 (W = 1.0-2.0) | HB unique data |
| Machine efficiency | Not in handbook | Table 4 (E = 0.60-0.90) | HB unique data |
| Economics | 15% rule, cost breakdown | Boothroyd Ch6 formulas | Complementary approaches |

**Summary:** Sandvik provides the physics framework (kc1, power formulas, corrections). Machinery's Handbook provides the actual Vc/fn numbers and additional factors (W, C, E) that Sandvik keeps behind their online tool.
