# Practical Machining Data — Theory vs Shop Floor Reality

> Compiled from: Boothroyd Ch6 extraction, Sandvik catalogs, Machinery's Handbook,
> Kennametal/Walter/Iscar recommendations, Haas Automation guidelines, Practical Machinist forums
> Date: March 29, 2026

---

## 1. Theory vs Practice Derating Factors

### Cutting Speed Derating (Textbook → Shop Floor)

| Material | Textbook Speed (m/min) | Practical Speed (m/min) | Derating Factor | Reason |
|----------|----------------------|------------------------|----------------|--------|
| EN8 (C45) | 150-180 | 100-130 | 0.65-0.75 | Rigid setup, insert life, surface finish |
| EN24 (AISI 4340) | 100-120 | 70-90 | 0.70-0.75 | Hardness variation, interrupted cuts |
| SS304 | 80-100 | 50-70 | 0.60-0.70 | Work hardening, heat buildup |
| SS316 | 70-90 | 45-65 | 0.65-0.72 | Similar to 304, more gummy |
| Aluminum 6061-T6 | 300-500 | 200-350 | 0.65-0.70 | BUE concerns, chip evacuation |
| Aluminum 7075-T6 | 250-400 | 180-300 | 0.70-0.75 | Better machinability than 6061 |
| Cast Iron (FG 260) | 120-150 | 90-120 | 0.75-0.80 | Abrasive, tool wear |
| Brass (CuZn39Pb3) | 200-300 | 180-250 | 0.85-0.90 | Free-cutting, minimal derating |
| Titanium Ti-6Al-4V | 40-60 | 25-40 | 0.60-0.65 | Heat management critical |

### Feed Rate Derating

| Operation | Textbook Feed | Practical Feed | Derating | Reason |
|-----------|--------------|---------------|----------|--------|
| Rough turning | 0.3-0.5 mm/rev | 0.2-0.35 mm/rev | 0.70 | Vibration, part deflection |
| Finish turning | 0.1-0.15 mm/rev | 0.08-0.12 mm/rev | 0.80 | Surface finish requirement |
| Rough milling | 0.15-0.25 mm/tooth | 0.10-0.18 mm/tooth | 0.70 | Chatter, fixture rigidity |
| Drilling (HSS) | 0.2-0.3 mm/rev | 0.15-0.22 mm/rev | 0.75 | Chip evacuation, drill wander |
| Drilling (carbide) | 0.15-0.25 mm/rev | 0.12-0.20 mm/rev | 0.80 | Better rigidity |

### Recommended Overall Derating Factor for Indian Job Shops

| Shop Type | Speed Factor | Feed Factor | Combined Time Factor |
|-----------|-------------|-------------|---------------------|
| Modern CNC (Mazak, DMG, Haas) | 0.75-0.85 | 0.80-0.90 | 1.20-1.40× textbook time |
| Standard CNC (Indian brands) | 0.65-0.75 | 0.70-0.80 | 1.50-1.80× textbook time |
| Old CNC / Turret lathes | 0.55-0.65 | 0.60-0.70 | 2.0-2.5× textbook time |
| Conventional (manual) | 0.40-0.50 | 0.50-0.60 | 3.0-4.0× textbook time |

**Our engine default: 0.70 speed derating (already conservative for Indian CNC shops)**

---

## 2. Non-Productive Time Breakdown

### Per-Part Non-Productive Time (t_l in Boothroyd's notation)

| Operation | CNC (s) | Conventional (s) | Notes |
|-----------|---------|------------------|-------|
| Load/unload (chuck) | 30-60 | 60-120 | 3-jaw chuck, manual clamp |
| Load/unload (vise) | 20-40 | 40-80 | Quick-action vise |
| Load/unload (fixture) | 45-90 | 90-180 | Custom fixture, alignment |
| Rapid traverse to part | 5-10 | N/A | CNC only |
| Tool approach/retract | 3-5 per tool | 10-20 per tool | Per tool change |
| Part probing/measurement | 15-30 | 30-60 | Every part or sample |
| Deburr at machine | 10-30 | 20-60 | Manual deburring |
| **Typical total per part** | **60-150** | **150-400** | - |

### Setup Time (Per Batch — Amortized)

| Operation | CNC (min) | Conventional (min) | Notes |
|-----------|-----------|-------------------|-------|
| First article setup | 30-90 | 60-180 | Tool offset, program load |
| Tool change (between ops) | 2-5 | 5-15 | ATC vs manual turret |
| Fixture change | 15-30 | 30-60 | Bolt-down, indicate |
| Program load/verify | 5-10 | N/A | USB/network transfer |
| **Typical total per batch** | **45-120 min** | **90-240 min** | - |

### From Boothroyd Table 6.1 (verified against industry):
- **Nonproductive time per part:** 120-300s (2-5 min) — our config uses 15-60 min setup amortized, which aligns
- **Tool changing time:** 60s (disposable insert) to 300s (brazed/regrindable)

---

## 3. Machine Utilization & Efficiency

### Indian Job Shop Utilization Rates

| Metric | Modern CNC Shop | Average CNC Shop | Small Job Shop |
|--------|----------------|------------------|----------------|
| Machine utilization (uptime) | 75-85% | 55-70% | 35-50% |
| Spindle running time | 55-65% | 35-50% | 20-35% |
| Actual cutting time / cycle | 40-55% | 25-40% | 15-25% |
| Shifts per day | 2-3 | 1-2 | 1 |
| Days per year | 300-310 | 280-300 | 260-280 |
| Effective hours/year/machine | 4,500-6,000 | 2,500-4,000 | 1,200-2,500 |

### Cycle Time Breakdown (Typical CNC Turning)

| Component | % of Cycle Time | Notes |
|-----------|----------------|-------|
| Actual cutting (chip making) | 30-45% | The productive work |
| Rapid traverse / positioning | 10-15% | Moving between cuts |
| Tool change (ATC) | 5-10% | Each tool change 3-8s on CNC |
| Load/unload | 15-25% | Manual chuck, door open/close |
| Measurement/inspection | 5-15% | In-process gauging |
| Idle/waiting | 5-15% | Program dwell, operator delay |

### Cycle Time Breakdown by Operation Type

| Operation | Cutting % | Non-Cutting % | Typical Cycle (for 100mm OD × 50mm part) |
|-----------|-----------|---------------|------------------------------------------|
| CNC Turning (production) | 40-50% | 50-60% | 3-8 min |
| CNC Turning (job shop) | 25-35% | 65-75% | 8-15 min |
| CNC Milling 3-axis | 35-45% | 55-65% | 5-20 min |
| CNC Milling 5-axis | 30-40% | 60-70% | 10-45 min |
| Drilling (standalone) | 45-55% | 45-55% | 1-5 min |
| Grinding | 35-45% | 55-65% | 5-15 min |

---

## 4. Practical Cutting Parameters by Material

### CNC Turning (Carbide Insert, Dry/Flood Coolant)

| Material | Roughing Speed (m/min) | Finish Speed (m/min) | Rough Feed (mm/rev) | Finish Feed (mm/rev) | DoC Rough (mm) | DoC Finish (mm) |
|----------|----------------------|---------------------|--------------------|--------------------|---------------|----------------|
| EN8 (C45) | 100-130 | 130-170 | 0.20-0.35 | 0.08-0.12 | 2.0-4.0 | 0.3-0.8 |
| EN24 (4340) | 70-100 | 100-130 | 0.15-0.30 | 0.06-0.10 | 1.5-3.0 | 0.2-0.5 |
| EN19 (4140) | 80-110 | 110-150 | 0.18-0.32 | 0.08-0.12 | 2.0-3.5 | 0.3-0.6 |
| SS304 | 50-80 | 80-120 | 0.12-0.25 | 0.05-0.10 | 1.0-2.5 | 0.2-0.5 |
| SS316 | 45-70 | 70-100 | 0.10-0.20 | 0.05-0.08 | 1.0-2.0 | 0.2-0.4 |
| Al 6061-T6 | 200-350 | 350-500 | 0.20-0.40 | 0.08-0.15 | 2.0-5.0 | 0.3-1.0 |
| Al 7075-T6 | 180-300 | 300-450 | 0.18-0.35 | 0.08-0.12 | 2.0-4.0 | 0.3-0.8 |
| Cast Iron FG260 | 90-130 | 130-180 | 0.20-0.35 | 0.08-0.12 | 2.0-4.0 | 0.3-0.8 |
| Brass (free-cut) | 180-280 | 280-400 | 0.15-0.30 | 0.08-0.12 | 1.5-3.0 | 0.3-0.6 |
| Ti-6Al-4V | 25-50 | 50-80 | 0.10-0.20 | 0.05-0.10 | 0.5-2.0 | 0.2-0.5 |

### CNC Milling 3-Axis (Carbide End Mill, Dry/MQL)

| Material | Roughing Speed (m/min) | Finish Speed (m/min) | Feed/tooth (mm) | Ae (% of D) | Ap (mm) |
|----------|----------------------|---------------------|----------------|-------------|---------|
| EN8 (C45) | 80-120 | 120-160 | 0.08-0.15 | 40-70% | 1.0-3.0 |
| EN24 (4340) | 60-90 | 90-120 | 0.06-0.12 | 30-50% | 0.8-2.5 |
| SS304 | 40-70 | 70-100 | 0.05-0.10 | 25-40% | 0.5-2.0 |
| Al 6061-T6 | 200-400 | 400-600 | 0.10-0.20 | 50-80% | 2.0-5.0 |
| Cast Iron | 80-120 | 120-170 | 0.08-0.15 | 40-60% | 1.0-3.0 |

### Drilling (Carbide Drill, Through-Coolant)

| Material | Speed (m/min) | Feed (mm/rev) for 10mm drill | Notes |
|----------|--------------|------------------------------|-------|
| EN8 | 80-120 | 0.15-0.25 | Peck drill >3D depth |
| EN24 | 60-90 | 0.10-0.20 | Peck drill >2D depth |
| SS304 | 30-50 | 0.08-0.15 | Low speed, high feed |
| Al 6061 | 150-250 | 0.20-0.35 | Parabolic flute for chips |
| Cast Iron | 70-100 | 0.15-0.25 | No peck needed usually |

---

## 5. Tool Life Expectations (Practical)

### Carbide Insert Life (Turning, Production Conditions)

| Material | Tool Life (min) at Practical Speed | Parts per Edge (typical) | Taylor n |
|----------|-----------------------------------|-------------------------|----------|
| EN8 | 15-25 | 20-50 | 0.25 |
| EN24 | 10-18 | 10-30 | 0.22 |
| SS304 | 8-15 | 8-25 | 0.20 |
| Al 6061 | 30-60 | 50-200 | 0.30 |
| Cast Iron | 20-35 | 25-60 | 0.25 |
| Ti-6Al-4V | 5-12 | 5-15 | 0.15 |

### End Mill Life (Milling, Carbide)

| Material | Tool Life (min) | Notes |
|----------|----------------|-------|
| EN8 | 45-90 | Full slotting reduces by 50% |
| SS304 | 20-45 | TiAlN coating essential |
| Al 6061 | 90-180+ | Uncoated or ZrN preferred |
| Cast Iron | 60-120 | TiN or AlTiN coating |

---

## 6. Cost Per Part — Boothroyd's Framework Applied to Indian Rates

### Example: Turning an EN8 shaft (OD 50mm × L 100mm, 2mm DoC)

Using Boothroyd's Eq. 6.2: `C_p = M·t_l + M·t_m + (N_t/N_b)·(M·t_ct + C_t)`

**Indian rates (2026):**
| Parameter | Value | Notes |
|-----------|-------|-------|
| M (machine + operator rate) | ₹600/hr = ₹0.167/s | Mid-range CNC turning |
| t_l (nonproductive time/part) | 90 s | Load, unload, measure |
| Cutting speed v | 120 m/min = 2.0 m/s | Practical for EN8 |
| Feed f | 0.25 mm/rev | Standard rough |
| K (cut distance) | π × 50 × 100 / 0.25 = 62,832 mm = 62.8 m | |
| t_m (machining time) | 62.8 / 2.0 = 31.4 s | One pass |
| t_ct (tool change time) | 30 s | ATC on CNC |
| C_t (insert cost per edge) | ₹80 | CNMG 120408, Indian brand |
| Tool life at v=120 m/min | 20 min = 1200 s | Practical for EN8 |
| Parts per edge | 1200 / 31.4 ≈ 38 | |
| N_t/N_b | 1/38 = 0.026 | |

**Cost breakdown:**
| Component | Calculation | Cost (₹) | % |
|-----------|------------|-----------|---|
| Nonproductive | 0.167 × 90 | 15.03 | 53% |
| Machining | 0.167 × 31.4 | 5.24 | 19% |
| Tool cost | 0.026 × (0.167×30 + 80) | 2.21 | 8% |
| Setup (amortized 30min over 100 parts) | 600×0.5/100 | 3.00 | 11% |
| **Subtotal machining** | | **25.48** | 91% |
| Material (0.15kg EN8 at ₹65/kg) | | 9.75 | - |
| Overhead (15%) | | 3.82 | - |
| **Total per part** | | **~39** | - |

**Key insight:** Nonproductive time is 53% of machining cost — exactly matching Boothroyd's finding that nonproductive time is the largest cost lever.

---

## 7. Non-Productive Time Factor for Our Engine

### Recommended NON_CUT_TIME_FACTOR by process

| Process | Current Factor | Recommended Factor | Basis |
|---------|---------------|-------------------|-------|
| CNC Turning | 1.15 | 1.40-1.60 | Boothroyd: 50-60% nonproductive |
| CNC Milling | 1.15 | 1.50-1.80 | More tool changes, complex paths |
| Drilling | 1.15 | 1.30-1.50 | Peck cycles, retract time |
| Grinding | 1.15 | 1.60-2.00 | Dressing, spark-out, measurement |
| Manual Turning | N/A | 2.50-3.50 | Conventional lathe |

### Components of the factor:
```
NON_CUT_TIME_FACTOR = 1.0 (cutting)
  + 0.15-0.25  (rapid traverse, positioning)
  + 0.10-0.15  (tool change time per part)
  + 0.05-0.10  (approach/retract)
  + 0.05-0.15  (measurement/inspection)
  + 0.05-0.10  (chip/coolant management)
  = 1.40-1.75 typical
```

---

## 8. Key Takeaways for Costimize Engine

1. **Theory-to-practice derating: 0.70× speed is a good default** for Indian CNC shops. Our engine already uses conservative speeds from Sandvik/Machinery's Handbook, so an additional 0.85× is appropriate (net ~0.70× from textbook peak).

2. **Non-productive time is 50-60% of cycle time** (Boothroyd confirmed). Our current NON_CUT_TIME_FACTOR of 1.15 is too low. Should be 1.40-1.60 for CNC, 2.5+ for manual.

3. **Tool cost is only 8-15% of machining cost** — far less important than nonproductive time and machining time. Current flat ₹5-15 per unit is reasonable for estimation.

4. **Setup time amortization matters hugely at low quantities** — at qty=1, setup is 50%+ of cost. At qty=100, it's <5%. Our engine handles this correctly.

5. **Machine utilization varies 2× between shops** — a modern 3-shift shop gets 6000 hrs/year vs a small job shop at 2500 hrs/year. This affects machine hourly rate by 2.4×.

6. **Feed maximization before speed** (Boothroyd's Rule #1): Our engine should check if requested speed/feed combination is sensible — high speed + low feed is wasteful.
