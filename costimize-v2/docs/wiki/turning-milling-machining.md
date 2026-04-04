---
slug: turning-milling-machining
title: CNC Turning and Milling — Cost Drivers, Formulas, and Rates
keywords: CNC turning, CNC milling, machining, MRR, material removal rate, cutting speed, feed rate, depth of cut, Taylor tool life, Sandvik power formula, setup time, machine hour rate, derating, Big 6 processes, cycle time, nonproductive time
sources: PHYSICS-ENGINE-KNOWLEDGE-MAP.md, PRACTICAL-MACHINING-DATA.md, process_db.py, cost_engine.py
updated: 2026-04-04
---

# CNC Turning and Milling

Turning and milling are the two most common manufacturing processes, covering roughly 60-65% of all machined parts (the "Big 6" processes: turning, milling, drilling, grinding, sheet metal, and casting account for the vast majority).

## Core Formulas

### Turning MRR

```
MRR (mm3/min) = Vc (m/min) x 1000 x f (mm/rev) x ap (mm)
```

Where Vc = cutting speed, f = feed per revolution, ap = depth of cut.

### Milling MRR

```
MRR (mm3/min) = ae (mm) x ap (mm) x Vf (mm/min)
Vf = fz x z x n
n = Vc x 1000 / (pi x D_tool)
```

Where ae = radial engagement, fz = feed per tooth, z = number of teeth, n = spindle RPM.

### Drilling Time

```
Time (min) = depth / (f x n)
n = Vc x 1000 / (pi x d_drill)
```

Peck drilling adds 10% per diameter beyond 3x depth.

### Sandvik Power Formula

```
kc = kc1 x (1/hm)^mc x (1 - gamma0/100)
hm = fn x sin(KAPR)
Pc = (Vc x ap x fn x kc) / (60 x 10^3)  [kW]
```

### Taylor Tool Life

```
V x T^n = C
T = (C/V)^(1/n)
Tool cost per min = edge_cost / T
```

Where edge_cost = 12.5 INR (50 INR insert / 4 edges), n = Taylor exponent (0.22-0.30 for carbide).

## Cutting Parameters by Material

### CNC Turning (Carbide Insert)

| Material | Rough Vc (m/min) | Finish Vc | Rough Feed (mm/rev) | Finish Feed | Rough DoC (mm) | Finish DoC |
|----------|-----------------|-----------|---------------------|-------------|----------------|------------|
| Aluminum 6061 | 400 | 500 | 0.30 | 0.10 | 2.0 | 0.3 |
| Mild Steel IS2062 | 180 | 220 | 0.25 | 0.10 | 2.0 | 0.3 |
| EN8 Steel | 150 | 200 | 0.25 | 0.10 | 2.0 | 0.3 |
| EN24 Steel | 100 | 140 | 0.20 | 0.08 | 1.5 | 0.25 |
| Stainless Steel 304 | 120 | 160 | 0.20 | 0.08 | 1.5 | 0.25 |
| Brass IS319 | 280 | 350 | 0.25 | 0.10 | 2.0 | 0.3 |
| Cast Iron | 120 | 160 | 0.25 | 0.10 | 2.0 | 0.3 |
| Titanium Grade 5 | 45 | 65 | 0.15 | 0.06 | 1.0 | 0.2 |

### CNC Milling 3-Axis (Carbide End Mill)

| Material | Rough Vc (m/min) | Finish Vc | Feed/tooth (mm) | ae/D Rough | ap Rough (mm) |
|----------|-----------------|-----------|-----------------|------------|---------------|
| Aluminum 6061 | 350 | 450 | 0.15 | 0.70 | 3.0 |
| Mild Steel IS2062 | 160 | 200 | 0.15 | 0.65 | 2.5 |
| EN8 Steel | 130 | 180 | 0.12 | 0.60 | 2.0 |
| Stainless Steel 304 | 100 | 140 | 0.12 | 0.55 | 2.0 |
| EN24 Steel | 90 | 120 | 0.10 | 0.50 | 1.5 |

Standard tools: 63mm face mill (6 teeth) for face milling, 16mm endmill (4 teeth) for slot/pocket.

## Theory vs Shop Floor: Derating Factors

Textbook cutting speeds assume ideal conditions. Indian job shops run slower due to machine rigidity, insert wear management, and operator practice.

| Material | Textbook Speed (m/min) | Practical Speed (m/min) | Derating Factor |
|----------|----------------------|------------------------|----------------|
| EN8 (C45) | 150-180 | 100-130 | 0.65-0.75 |
| EN24 (4340) | 100-120 | 70-90 | 0.70-0.75 |
| SS304 | 80-100 | 50-70 | 0.60-0.70 |
| Aluminum 6061 | 300-500 | 200-350 | 0.65-0.70 |
| Titanium Ti-6Al-4V | 40-60 | 25-40 | 0.60-0.65 |
| Brass | 200-300 | 180-250 | 0.85-0.90 |

### Shop Type Impact

| Shop Type | Speed Factor | Feed Factor | Time Multiplier vs Textbook |
|-----------|-------------|-------------|---------------------------|
| Modern CNC (Mazak, DMG, Haas) | 0.75-0.85 | 0.80-0.90 | 1.2-1.4x |
| Standard CNC (Indian brands) | 0.65-0.75 | 0.70-0.80 | 1.5-1.8x |
| Old CNC / Turret lathes | 0.55-0.65 | 0.60-0.70 | 2.0-2.5x |
| Conventional (manual) | 0.40-0.50 | 0.50-0.60 | 3.0-4.0x |

**Newton-Metre uses 0.75 as the default shop floor efficiency** -- midpoint for Indian CNC shops.

## Nonproductive Time: The Hidden Cost Driver

Boothroyd's research (Chapter 6, "Fundamentals of Machining") confirms that nonproductive time dominates:

| Component | % of CNC Turning Cycle |
|-----------|----------------------|
| Actual cutting (chip making) | 30-45% |
| Rapid traverse / positioning | 10-15% |
| Tool change (ATC) | 5-10% |
| Load/unload | 15-25% |
| Measurement/inspection | 5-15% |
| Idle/waiting | 5-15% |

Newton-Metre applies a 1.40x non-cutting time factor on top of calculated cutting time (covering rapid traverse, tool change, measurement, load/unload). Setup time is tracked separately and amortized over quantity.

## Machine Hour Rates (Indian Job Shops, 2026)

| Process | Rate (INR/hr) | Setup Time (min) |
|---------|--------------|------------------|
| Turning | 800 | 30 |
| Facing | 800 | 10 |
| Boring | 900 | 25 |
| Milling (face) | 1,000 | 45 |
| Milling (slot) | 1,000 | 45 |
| Milling (pocket) | 1,100 | 50 |
| Drilling | 600 | 15 |
| Reaming | 700 | 15 |
| Tapping | 600 | 15 |
| Threading | 600 | 20 |
| Grinding (cylindrical) | 1,200 | 40 |
| Grinding (surface) | 1,200 | 35 |
| Broaching | 1,500 | 60 |

## Tool Life Expectations (Production Conditions)

| Material | Carbide Insert Life (min) | Parts per Edge (typical) | Taylor n |
|----------|--------------------------|-------------------------|----------|
| EN8 | 15-25 | 20-50 | 0.25 |
| EN24 | 10-18 | 10-30 | 0.22 |
| SS304 | 8-15 | 8-25 | 0.20 |
| Aluminum 6061 | 30-60 | 50-200 | 0.30 |
| Cast Iron | 20-35 | 25-60 | 0.25 |
| Titanium Ti-6Al-4V | 5-12 | 5-15 | 0.15 |

**Key insight from Sandvik:** Tool cost is only 3% of total component cost. Machine + labour is 58%. Increasing cutting data by 20% saves 15% on component cost -- far more impact than buying cheaper tools.

## Boothroyd's Cost Formula

Production cost per component:

```
C_pr = M*t_l + M*t_m + (N_t/N_b)*(M*t_ct + C_t)
```

Where M = machine+operator rate, t_l = nonproductive time/part, t_m = machining time, N_t/N_b = tools used per part, t_ct = tool change time, C_t = tool edge cost.

Optimum cutting speed for minimum cost is independent of batch size and nonproductive time:

```
v_c = v_r * (n/(1-n) * M*t_r / (M*t_ct + C_t))^n
```

## How Newton-Metre Calculates Turning Cost

For each turning operation:
1. Calculate stock OD = part OD + 3mm machining allowance
2. Calculate rough passes: (stock_radius - finish_radius) / ap_rough
3. Calculate rough volume and time from MRR
4. Calculate finish pass volume and time
5. Apply 1.40x non-cutting factor
6. Divide by 0.75 shop floor efficiency
7. Multiply time by machine rate (800 INR/hr for turning)
8. Add Taylor-based tooling wear cost
9. Add power cost (5 kW x time x 8 INR/kWh)
10. Amortize setup (30 min x 800 INR/hr / quantity)
