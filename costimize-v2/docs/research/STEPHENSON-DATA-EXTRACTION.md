# Stephenson & Agapiou — Metal Cutting Theory and Practice (3rd Ed.) Data Extraction

Source: *Metal Cutting Theory and Practice*, David A. Stephenson & John S. Agapiou, CRC Press, 3rd Edition. 956 pages.

---

## 1. Specific Cutting Energy / Unit Power (Table 2.1, p.52)

The specific cutting energy `us` is the power required to machine a unit volume of work material.

| Material | Unit Power (kW/cm3/min) | Unit Power (HP/in.3/min) |
|----------|------------------------|-------------------------|
| Cast irons | 0.044 - 0.08 | 0.97 - 1.76 |
| Steels — Soft | 0.05 - 0.066 | 1.10 - 1.45 |
| Steels — 0 < Rc < 45 | 0.065 - 0.09 | 1.43 - 1.98 |
| Steels — 50 < Rc < 60 | 0.09 - 0.2 | 1.98 - 4.40 |
| Stainless steels | 0.055 - 0.09 | 1.21 - 1.98 |
| Magnesium alloys | 0.007 - 0.009 | 0.15 - 0.20 |
| Titanium | 0.053 - 0.066 | 1.16 - 1.45 |
| Aluminum alloys | 0.012 - 0.022 | 0.26 - 0.48 |
| High temp alloys (Ni, Co based) | 0.09 - 0.15 | 1.98 - 3.30 |
| Free-machining brass | 0.056 - 0.07 | 1.23 - 1.54 |
| Copper alloys — RB < 80 | 0.027 - 0.04 | 0.59 - 0.88 |
| Copper alloys — 80 < RB < 100 | 0.04 - 0.057 | 0.88 - 1.25 |

**Conditions:** Zero effective rake angle tools, 0.25 mm undeformed chip thickness, continuous chips without BUE.

**Unit conversion:** W = N m/s, 1 kW = 1.341 HP.

**Usage:** Cutting power `Pc = us x MRR`, where `MRR = V x f x d` (m/min x mm/rev x mm -> cm3/min with /1000 factor).

---

## 2. Power and Force Formulas (Ch. 2 & Ch. 6)

### 2.1 Power Consumption

**Turning/boring** (Eq. 2.7, p.52):
```
Ps = us x Q
```
Where:
- `Ps` = spindle power (kW)
- `us` = specific cutting energy from Table 2.1 (kW/cm3/min)
- `Q` = MRR = V x f x d (cm3/min)

**Motor power** (Eq. 2.8):
```
Pm = Ps/eta + Pt
```
Where:
- `eta` = drive efficiency (typically 0.75-0.85)
- `Pt` = tare/idling power

### 2.2 Material Removal Rate

**Turning** (Eq. 2.6, p.66):
```
MRR = V x f x d x 1000 (mm3/min)
```
Where V in m/min, f in mm/rev, d in mm.

### 2.3 Specific Cutting Power Definition

**Turning/boring** (Eq. 6.18, p.403):
```
us = Ft / (f x d)
```
Where `Ft` is tangential cutting force (N), `f` is feed (mm), `d` is depth of cut (mm). Units: N/mm2 = MPa.

**Drilling** (Eq. 6.19, p.403):
```
us = 8M / (D^2 x f)
```
Where `M` is torque (N-mm), `D` is drill diameter (mm), `f` is feed (mm/rev).

**Milling** (Eq. 6.21, p.403):
```
us = 2M / (D x f x d)
```
Where `M` is torque on cutter.

### 2.4 Machining Time

**Turning** (Eq. 2.5, p.66):
```
tm = (L + La) / (f x N) [min]
```
Where `L` = axial length of cut, `La` = approach allowance (~3 mm), `N` = spindle RPM.

**Spindle RPM** (Eq. 2.1):
```
N = (2V x 1000) / (pi x (D1 + D2))
```
Where `D1` = initial diameter, `D2` = final diameter = D1 - 2d.

---

## 3. Empirical Force Models (Ch. 6, Table 6.1, p.402)

### 3.1 Exponential Force Equations

Forces per unit width of cut normal (N) and parallel (P) to rake face (Eq. 6.16-6.17, p.401):
```
N/b = C1 x a^a1 x V^b1 x (1 - sin(alpha))^c1
P/b = C2 x a^a2 x V^b2 x (1 - sin(alpha))^c2
```
Where:
- `a` = uncut chip thickness (mm)
- `b` = width of cut (mm)
- `V` = cutting speed (m/min)
- `alpha` = normal rake angle (degrees)

### 3.2 Force Coefficients for WC Tools (Table 6.1, p.402)

| Material | C1 | a1 | b1 | c1 | C2 | a2 | b2 | c2 |
|----------|-----|-------|-------|-------|------|-------|-------|--------|
| Gray cast iron (180 BHN) | 1106.6 | 0.011 | 0.760 | 1.277 | 436.2 | -0.042 | 0.595 | 0.065 |
| Nodular cast iron (280 BHN) | 1820.7 | -0.092 | 0.649 | 0.849 | 1526.9 | -0.091 | 0.400 | -0.082 |
| 1018 Steel (cold drawn) | 2032.4 | -0.080 | 0.730 | 1.425 | 889.8 | 0.000 | 0.641 | 0.958 |
| 10L45 Steel (cold drawn) | 1571.8 | -0.101 | 0.682 | 0.853 | 567.4 | -0.096 | 0.515 | -0.491 |
| 319 Aluminum (cast) | 673.2 | 0.083 | 0.936 | 1.109 | 288.9 | 0.200 | 0.912 | 0.000 |
| 2024-T6 Aluminum (cold drawn) | 863.1 | -0.018 | 0.800 | 1.007 | 566.2 | 0.000 | 0.688 | 0.000 |

**Valid range:** V < 300 m/min, 0.1 < a < 0.5 mm, -10deg < alpha < 0deg (iron/steel), 0deg < alpha < 20deg (aluminum).

**Units:** N and P in N/mm2 when V in m/min, a in mm, alpha in degrees.

---

## 4. Cutting Pressure Equations for Process Simulation (Ch. 8, Table 8.2, p.504)

### 4.1 Normal and Frictional Cutting Pressures

```
Kn = Cn x t_avg^an x V^bn x (1 - sin(alpha))^cn    (Eq. 8.52)
Kf = Cf x t_avg^af x V^bf x (1 - sin(alpha))^cf    (Eq. 8.53)
```

Where `t_avg` is average uncut chip thickness (mm), `V` is cutting speed (m/min).

### 4.2 Cutting Pressure Coefficients (Table 8.2, p.504)

| Parameter | Gray Cast Iron (170 BHN, Si3N4) | Nodular Iron (270 BHN, Coated WC) | 390 Al (110 BHN, PCD) | 356 Al (73 BHN, PCD) | 1018 Steel (163 BHN, Coated WC) |
|-----------|------|------|------|------|------|
| Cn | 1227 | 1730 | 470 | 356 | 2119 |
| an | -0.338 | -0.336 | -0.243 | -0.475 | -0.231 |
| bn | -0.121 | -0.089 | 0.060 | -0.040 | -0.080 |
| cn | 1.190 | 1.183 | 1.065 | 1.149 | — |
| Cf | 0.405 | 0.304 | 0.303 | 0.453 | 0.453 |
| af | -0.363 | -0.258 | -0.306 | -0.368 | -0.095 |
| bf | 0 | 0 | 0.025 | -0.085 | -0.090 |
| cf | -2.126 | -1.392 | -1.810 | -0.233 | — |

### 4.3 Average Chip Thickness (Eq. 8.54, p.504)

```
t_avg = rn^0.5334 x (f/rn)^0.0921 x (d/f)^0.3827 x (cos(gamma_L))^1.0317
```
Valid for: 5deg < gamma_L < 45deg, 0.5 < d < 5.0 mm, 0.1 < f < 1.0 mm, 0.4 < rn < 4.4 mm, rn > f.

### 4.4 Effective Lead Angle (Eq. 8.51, p.503)

```
tan(gamma_Le) = 0.5053 x tan(gamma_L) + 1.0473 x (rn/d) + 0.4654 x (f/rn)
```
Valid for: -5deg < gamma_L < 45deg.

---

## 5. Force Ratios and Rules of Thumb (Ch. 6, p.400)

### 5.1 Turning Force Ratios

- **Rough turning** (zero or small lead angle): `Ft : Fa : Fr = 4 : 2 : 1`
- As lead angle increases, `Fa/Ft` and `Fr/Ft` ratios change; axial and radial forces approach tangential force in finishing (small DOC).

### 5.2 Milling Force Ratios

- **Peripheral/end milling:** Radial force = 30%-50% of tangential cutting force.
- Axial force depends on lead angle and edge corner geometry.

### 5.3 Drilling Force Ratios

- **Small diameter drills:** Thrust = 1.0-1.5 x tangential force.
- **Large drills (spade/indexable):** Thrust ~ 0.5 x tangential force.

---

## 6. Taylor Tool Life Equation (Ch. 9, Section 9.7, p.549-550)

### 6.1 Basic Taylor Equation (Eq. 9.8)

```
V x T^n = Ct
```
Where:
- `V` = cutting speed (m/min)
- `T` = tool life (min)
- `n` = exponent (depends on tool material)
- `Ct` = constant (cutting speed for 1 min tool life)

### 6.2 Taylor Exponent n — Typical Values by Tool Material

| Tool Material | n Range |
|--------------|---------|
| HSS | 0.10 - 0.17 |
| Uncoated WC (carbide) | 0.20 - 0.25 |
| TiC or TiN coated WC | 0.30 |
| Al2O3-coated WC | 0.40 |
| Solid ceramic | 0.40 - 0.60 |

**Ct** is typically ~100 m/min for rough machining of low carbon steels.

### 6.3 Extended Taylor Equation (Eq. 9.9)

```
V x T^n x f^a x d^b = Kt
```
Where `f` = feed (mm/rev or in/rev), `d` = depth of cut (mm or in).

**Typical HSS values:** n = 0.17, a = 0.77, b = 0.37 (T in min, V in ft/min, f and d in inches).

**Kt** ~ 500 for mild steels, ~200 for cast iron.

**Key insight:** n < a < b, meaning speed has larger influence on tool life than feed, and feed has larger influence than depth of cut. A 50% increase in speed reduces tool life by 80%-90%. A 50% increase in DOC reduces tool life by only ~15% (when DOC > 10x feed).

### 6.4 Worked Example: Alloy Steel with Carbide Insert (p.564-565)

Test conditions: 2.54 mm DOC, 0.18 mm/rev feed, carbide insert on alloy steel.

| Speed (m/min) | Tool Life (min) |
|---------------|----------------|
| 90 | 50 |
| 120 | 16 |
| 150 | 6 |
| 180 | 3 |

Result: `V x T^0.25 = 237` (n = 0.25, Ct = 237 m/min)

### 6.5 Tool Life Data for Carbide Tools — Three Materials (Table 9.5, p.569)

#### A. Gray 30 Cast Iron

| Speed (m/min) | Tool Life (min) |
|---------------|----------------|
| 30 | 350 |
| 45 | 115 |
| 60 | 53 |
| 75 | 29 |
| 90 | 17.5 |
| 105 | 11.5 |

#### B. 1020 CRS (Cold Rolled Steel)

| Speed (m/min) | Tool Life (min) |
|---------------|----------------|
| 105 | 900 |
| 120 | 520 |
| 135 | 330 |
| 150 | 200 |
| 165 | 145 |
| 180 | 100 |

#### C. Pearlitic Malleable Iron (180 BHN)

| Speed (m/min) | Tool Life (min) |
|---------------|----------------|
| 60 | 580 |
| 75 | 270 |
| 90 | 150 |
| 105 | 80 |
| 120 | 50 |
| 135 | 35 |
| 150 | 24 |
| 180 | 13 |

### 6.6 Extended Taylor Example: Drilling Steel with Carbide (p.565-566)

| V (m/min) | f (mm/rev) | T (min) |
|-----------|-----------|---------|
| 70 | 0.15 | 120 |
| 70 | 0.25 | 105 |
| 140 | 0.15 | 24 |

Result: `V x T^0.43 x f^0.11 = 445`

Key finding: 100% increase in speed decreases tool life by 80%; 67% increase in feed decreases tool life by only 13%.

---

## 7. Tool Wear Types, Mechanisms, and Countermeasures (Table 9.1, p.542-543)

| Wear Type | Mechanism | Characteristics | Countermeasures |
|-----------|-----------|----------------|-----------------|
| Flank wear | Abrasion | Even wear scar | Harder tool, coated tool, filter fluid, clean parts, refine microstructure |
| Flank wear | Thermal softening | — | Reduce speed |
| Flank wear | Feed too low | Poor finish | Increase feed |
| Crater wear | Diffusion | Rapid wear rate | Reduce speed, improve cooling, increase coolant volume/pressure |
| Crater wear | Chemical | Smooth wear scar | Change tool/coating material or coolant |
| Notch wear | Abrasion | At part free surface | Vary DOC, harder tool, increase lead angle |
| Notch wear | Oxidation | Discoloration | Change coolant, reduce speed |
| Nose radius wear | Abrasion | Rough uneven scar | Reduce feed, harder tool, increase nose radius |
| Edge cracking | Thermal fatigue | Cracks normal to edge | Reduce speed, machine dry, tougher tool |
| Edge cracking | Mechanical fatigue | Cracks parallel to edge | Reduce feed, tougher tool |
| BUE | Adhesion | Poor surface finish | Increase speed, increase rake angle, increase coolant lubricity |
| Edge deformation | Overload/thermal | Occurs rapidly | Reduce feed, harder tool, reduce speed |
| Edge chipping | Abrasion/vibration | — | Tougher tool, stronger edge prep, reduce feed |
| Chip hammering | Improper chip flow | Damage away from edge | Change lead angle or nose radius |
| Gross fracture | Overload/vibration | Occurs rapidly | Tougher tool, increase nose radius, stronger edge prep |

---

## 8. Maximum Cutting Speeds by Tool Material (Ch. 9 & 11)

### 8.1 Speed Limits Before Thermal Softening Failure

| Tool Material | Max Speed (m/min) | Thermal Limit (deg C) | Workpiece |
|--------------|------------------|----------------------|-----------|
| HSS | ~35 | ~540 | Soft steels |
| HSS-Co | ~50 | ~570 | Soft steels |
| Uncoated WC | ~100-150 | ~700 | Low carbon steels |
| Coated carbide | ~150+ | >700 | Cast iron |
| Si3N4 ceramic | 800-1300 | — | Gray cast iron |
| PCBN | 800-1300 | — | Gray cast iron |

### 8.2 Aluminum Alloy Cutting Speeds

| Alloy Type | Tool | Speed (m/min) |
|-----------|------|---------------|
| Eutectic Al-Si (319, 356, 380) — turning | Carbide | up to 450 |
| Eutectic Al-Si — milling | PCD | up to 4000 |
| Hypereutectic Al-Si (390) — turning | Uncoated WC | ~100 |
| Hypereutectic Al-Si — milling | PCD | up to 1000 |

### 8.3 Steel Cutting Speeds (General)

| Material | Operation | Tool | Typical Speed |
|----------|-----------|------|--------------|
| Low carbon steel | Turning | Coated WC | ~200 m/min |
| Low carbon steel | Drilling | HSS | < 20 m/min |
| Low carbon steel | Turning | Coated WC | ~200 m/min, 0.15 mm/rev feed |

---

## 9. Surface Finish Formulas (Ch. 10, p.583-584)

### 9.1 Geometric Roughness — Sharp-Nosed Tool (Eq. 10.7-10.8)

**Peak-to-valley:**
```
Rtg = f / (cot(kappa_re) + cot(kappa'_re))
```

**Average roughness:**
```
Rag = Rtg / 4 = f / (4 x (cot(kappa_re) + cot(kappa'_re)))
```

### 9.2 Geometric Roughness — Tool with Nose Radius (Eq. 10.9-10.10)

**Peak-to-valley:**
```
Rtg = f^2 / (8 x rn)
```

**Average roughness:**
```
Rag = 0.0321 x f^2 / rn
```

Where:
- `f` = feed per revolution (mm/rev)
- `rn` = tool nose radius (mm)
- Results in micrometers (um)

### 9.3 Practical Roughness vs. Geometric Roughness

- When tool wear and vibrations are not excessive, actual Ra is usually **< 2x geometric Ra**.
- **Ratio decreases** (toward 1.0) as cutting speed increases — especially for soft materials prone to BUE.
- Ratio also reduced by increasing rake angle and proper coolant application.

### 9.4 Actual/Geometric Roughness Ratio by Material (from Fig. 10.13, p.585)

| Material | Ra_actual/Ra_geometric at ~30 m/min | Ra_actual/Ra_geometric at ~120 m/min |
|----------|------|------|
| Free cutting alloys | ~1.4 | ~1.15 |
| Carbon steel | ~1.6 | ~1.2 |
| AISI alloy steel | ~1.9 | ~1.3 |
| Cast iron | ~2.0 | ~1.4 |
| Ductile material | ~2.4 | ~1.5 |

### 9.5 Wiper Inserts

Wiper inserts reduce Ra by **2x or more** compared to standard nose radius inserts. The improvement increases with feed rate. Example: standard insert (r=0.8mm) gives ~6 um Ra at 0.3 mm/rev feed; wiper insert (r=0.4mm) gives ~3 um Ra at same feed (Fig. 10.12).

---

## 10. Chip Formation — Correction Factors (Ch. 6, p.407-410)

### 10.1 Shear Strain (Eq. 6.24)

```
gamma = tan(phi - alpha) + cot(phi)
```
or equivalently:
```
gamma = cos(alpha) / (cos(phi - alpha) x sin(phi))
```

Where `phi` = shear angle, `alpha` = rake angle.

**Typical strains:** 100%+ (from Fig. 6.16):
- 1112 Steel at 0deg rake: gamma ~ 2.7
- 1112 Steel at 20deg rake: gamma ~ 2.0
- 2024 Aluminum at 0deg rake: gamma ~ 2.2
- 2024 Aluminum at 20deg rake: gamma ~ 1.6
- Brass at 0deg rake: gamma ~ 2.4
- Brass at 20deg rake: gamma ~ 1.5

### 10.2 Cutting Ratio / Chip Thickness Ratio (Eq. 6.25-6.26)

```
tan(phi) = rc x cos(alpha) / (1 - rc x sin(alpha))
rc = a / ac = sin(phi) / cos(phi - alpha)
```

Where `rc` = cutting ratio, `a` = uncut chip thickness, `ac` = chip thickness.

### 10.3 Strain Rate (Eq. 6.28)

```
gamma_dot = V x cos(alpha) / (Delta_y x cos(phi - alpha))
```

Typical: ~10^5 s^-1 at cutting speeds up to 250 m/min; ~10^6 s^-1 above 1000 m/min.

### 10.4 Tool-Chip Contact Length (Eq. 6.32)

```
Lc = Cl x ac
```

Where Cl ~ 1.75-2.0 for ductile metals, ~1.5 for brittle materials (e.g., cast iron).

### 10.5 Friction Coefficient

- `mu_e = P/N` (ratio of forces parallel/normal to rake face)
- Typical values > standard friction; values above 1.0 are not uncommon in metal cutting.
- Increases with rake angle.
- Often maximum in speed range where BUE forms.

---

## 11. Machining Economics (Ch. 13, p.757-763)

### 11.1 Production Cost per Part (Eq. 13.8, p.760)

```
Cu = Co x (tm + tm/T x (t_l + Cte/Co)) + Co x (tcs + te + tr + tp + td + tx + ta)
```

Where:
- `Co` = operating cost ($/min)
- `tm` = machining time (min)
- `T` = tool life (min)
- `t_l` = tool loading/unloading time (min)
- `Cte` = tool cost per edge ($)
- `tcs` = tool interchange time
- Other t terms = non-productive times

### 11.2 Optimum Speed for Minimum Cost (Eq. 13.9, p.760)

```
Vopc = Kt / (fh^a x dc^b) x [(1/n - 1) x (t_l + Cte/Co)]^(-n)
```

Where `fh` = highest possible feed, `dc` = depth of cut, and a, b, n from extended Taylor equation.

### 11.3 Optimum Speed for Maximum Production Rate (Eq. 13.10, p.760)

```
Vopt = Kt / (fh^a x dc^b) x [(1/n - 1) x t_l]^(-n)
```

**Vopt is always higher than Vopc.** The range [Vopc, Vopt] is the "Hi-E" (high efficiency) range.

### 11.4 High-Efficiency Range

Any speed in the range Vopc to Vopt is preferable from an economic standpoint. A 50% increase in cutting speed typically decreases tool life by 80%-90%.

### 11.5 Feed Selection (Eq. 13.17, p.762)

```
fh = min(fc_max, fs_max, fF_max)
```

Where fc_max, fs_max, fF_max are maximum feeds due to chip-breaking, surface finish, and force limitations respectively.

### 11.6 Depth of Cut Guidelines

- DOC has least impact on tool life of the three cutting parameters.
- 50% increase in DOC typically produces only ~15% reduction in tool life (when DOC > 10x feed).
- Use maximum permissible DOC for roughing cuts.

### 11.7 Worked Example: Turning Economics (Example 13.2-13.3, p.770-771)

**Parameters:**
| Parameter | Value |
|-----------|-------|
| Machine spindle RPM | 700 |
| Feed | 0.3 mm/rev |
| Operating cost Co | $60/hr = $1/min |
| Tool life equation | V x T^0.25 = 500 |
| Tool cost per insert | $9 |
| Cutting edges per insert | 3 |
| Tool interchange time | 8 s |
| Part load/unload time | 20 s |
| Tool load/unload time | 1 min |

At V = 154 m/min: T = 111 min, tm = 0.962 min, **Cu = $1.51/part**

**With optimization** (fh = 0.5 mm/rev max):
Vopc = 380 m/min, T = 5.2 min, tm = 0.234 min, **Cu = $0.928/part** (39% cost reduction)

---

## 12. Machinability Ratings (Ch. 11, p.627)

### 12.1 Machinability Index Definition (Eq. 11.1)

```
Im = (V60_material / V60_reference) x 100
```

Where V60 is the cutting speed yielding 60 min tool life for specified conditions.

**Reference material:** SAE B1113 sulfurized free-machining steel (Im = 100).

### 12.2 HSS Speed Limits by Tool Material

| Tool Material | Max Speed (m/min) | Notes |
|--------------|-------------------|-------|
| HSS | ~35 | Soft steels; thermal softening above ~540 deg C |
| HSS-Co | ~50 | Improved hot hardness |

---

## 13. Drill Wear Model (Ch. 9, p.557)

### 13.1 Number of Holes to Failure (Eq. 9.16)

```
N = C1 x VB x f / V^a
```

### 13.2 Time to Failure (Eq. 9.17)

```
T = C2 x VB / V^(a+1)
```

Where C1, C2, a are empirical constants, VB = flank wear width, f = feed, V = cutting speed.

**Key insight:** Number of holes to failure depends directly on feed (higher feed = more holes). Time to failure is independent of feed. Both decrease with increasing speed.

---

## 14. Chisel Edge Thrust in Drilling (Table 8.1, p.500)

### 14.1 Chisel Edge Thrust Equation (Eq. 8.42)

```
Ftce = Cce x f^a x Lce^b x H^c
```

Where Lce = chisel edge length (mm), f = feed (mm/rev), H = Brinell hardness (kg/mm2).

### 14.2 Coefficients for Gray Cast Iron with WC Drills

| Parameter | Conventional/Split Point | Helical Point |
|-----------|------------------------|---------------|
| Cce | 121.5 | 32.1 |
| a | 0.97 | 1.00 |
| b | 1.10 | 0.42 |
| c | 0.54 | 0.82 |

**Units:** Ftce in N. For 3-fluted drills, multiply by 1.5.

---

## 15. Deformation Zone Temperatures (Ch. 6, Fig. 6.18, p.410)

Average primary deformation zone temperatures measured by infrared:

| Material | ~50 m/min | ~100 m/min | ~200 m/min | ~300 m/min |
|----------|-----------|------------|------------|------------|
| 1018 Steel | ~120 deg C | ~170 deg C | ~225 deg C | ~270 deg C |
| 2024 Aluminum | ~60 deg C | ~80 deg C | ~100 deg C | ~110 deg C |
| CA330 Brass | ~80 deg C | ~120 deg C | ~165 deg C | ~195 deg C |

---

## 16. Coating Effectiveness Guidelines (Ch. 9, p.544-545)

### 16.1 Coating Types

| Coating | Color | Best For | Advantage |
|---------|-------|----------|-----------|
| TiN-based | Gold | Steels at high speed | Reduces friction, temperatures, flank wear |
| Al2O3-based | Black | Cast/nodular irons | Higher hardness, chemical inertness, abrasion resistance |

### 16.2 Optimum Coating Thickness

~0.010 mm (10 um). Too thin = rapid abrasive failure. Too thick = thermal stress spalling.

### 16.3 Two-Stage Wear of Coated Tools

1. While coating intact: low abrasive wear rate
2. After coating failure: rapid cratering due to diffusion/chemical wear of exposed substrate

---

## 17. Grinding Specific Energy (Ch. 2, p.59)

The specific grinding energy us is typically **10x** the specific cutting energy for the same material (Table 2.1 values x 10).

**Grinding ratio G** (Eq. 2.65):
```
G = Qw / Qh
```
Ranges from 0.018 to 60,000. Higher G = more productive wheel.

---

## 18. Feed Rate and Depth of Cut — General Guidelines (Ch. 13)

### 18.1 Roughing Operations

- Use maximum possible DOC first (limited by tool strength, machine power, chatter).
- Then maximize feed (limited by force on cutting edge, chip breaking, machine power).
- Finally optimize speed (has greatest impact on tool life).

### 18.2 Finishing Operations

- DOC determined by stock allowance.
- Feed limited by surface finish requirement: `Ra ~ 0.0321 x f^2 / rn`.
- Speed can often be higher than roughing (lower forces, less heat).

### 18.3 Single-Pass Optimization Strategy

Use highest feed consistent with:
- Chip breaking requirements
- Surface finish requirements: `f < sqrt(Ra_required x rn / 0.0321)`
- Force limitations on tool and machine

Then calculate speed from:
- Minimum cost: `Vopc` (Eq. 13.9)
- Maximum production: `Vopt` (Eq. 13.10)

---

## 19. Material-Specific Machining Data (Ch. 11)

### 19.1 Magnesium Alloys

- Tool life: ~5x longer than aluminum wet machining under comparable conditions.
- PCD tools: tool lives approaching 1 million parts in milling/drilling.
- Surface finish: Ra down to 0.1 um achievable by turning/milling.
- HSS speed limit: not limited by thermal softening (Mg melts below 600 deg C).

### 19.2 Copper Alloys

- Pure copper: difficult (highly ductile); cut at > 200 m/min with sharp tools.
- Alpha brass (70/30): discontinuous chips, poor finish at low speed.
- Alpha-beta brass (60/40): easiest to machine of the copper alloys.
- Free-cutting brass: leaded grades are among the most machinable metals.

### 19.3 Cast Irons

| Type | Carbide Speed | Ceramic/PCBN Speed | Tool Life (parts) |
|------|--------------|-------------------|-------------------|
| Gray iron — carbide | up to 150 m/min | — | 1,000-2,000 |
| Gray iron — Si3N4 | — | 800-1300 m/min | 2,000-10,000 |
| Nodular iron | Similar to mild steel | — | — |
| CGI | ~67% of gray iron speed | — | — |

### 19.4 Carbon Steels

| Grade | Typical Turning Speed (m/min) | Feed (mm/rev) | Notes |
|-------|------------------------------|---------------|-------|
| Low carbon (1005-1029) | ~200 | ~0.15 | Best machinability at 0.15-0.25%C |
| Medium carbon (1030-1059) | Lower than low C | Progressive reduction | Higher cutting forces |
| High carbon (1060-1095) | Lower still | Lower | Cementite increases abrasion |
| AISI 1008/1010 | ~200 | 0.15 | BUE problems in annealed condition |

### 19.5 Stainless Steels

| Type | Relative Machinability | Key Concerns |
|------|----------------------|--------------|
| Ferritic | Best of stainless steels | Machinability decreases with Cr content |
| Martensitic | Moderate | Influenced by hardness, C content, Ni content |
| Austenitic | Most difficult | High forces/temps, BUE, chip control, work hardening |
| Duplex | Difficult | Combined ferritic/austenitic difficulties |

### 19.6 Nickel-Based Superalloys

- Unit power: 0.09-0.15 kW/cm3/min (highest of common materials).
- Typical speed with carbide: very low (see Figure 11.21 for deformation limits).

---

## 20. Abrasive Wear Equation (Eq. 9.7, p.539)

```
v = kw x N x Ls / H
```

Where:
- `v` = volume worn away
- `kw` = wear coefficient
- `N` = normal force on sliding interface
- `Ls` = sliding distance
- `H` = penetration hardness of tool

**Key insight:** Increase tool hardness (H) or reduce forces (N) to reduce wear. Using harder tool materials or coatings is the most effective strategy.

---

## 21. Usui Wear Model (Eq. 9.13-9.14, p.551-552)

```
dv/dLs = C1 x q x exp(-C2/theta)
```

Where:
- `q` = normal stress at the point
- `theta` = interfacial temperature (K)
- `C1` proportional to tool hardness
- `C2` = empirical constant

Stress distribution on rake face:
```
q(x) = D1 x exp(1 - x/Lc)
```

This model captures the exponential dependence of wear on temperature and was validated for 1020 steel with P20 carbide.

---

## 22. Machining Time Formulas (Ch. 13, p.759)

### 22.1 Turning, Boring, Drilling (Eq. 13.2)

```
tm = pi x D x L / (1000 x V x f) [min]
```

### 22.2 Milling (Eq. 13.3)

```
tm = pi x D x (L + epsilon) / (1000 x nt x V x f)
```

Where nt = number of inserts, epsilon = overtravel.

### 22.3 Total Production Time (Eq. 13.1)

```
Tu = tm + tm/T x t_l + tcs + te + tr + tp + td + tx + ta
```

Where the t terms are:
- t_l = tool loading/unloading time
- tcs = tool interchange time
- te, tr, tp = approach, table index, acceleration times
- td, tx, ta = deceleration, rapid travel, other times

---

## Cross-Reference to Existing Engine Data

### Comparison with Sandvik kc1 Values

The Stephenson specific cutting energy values (Table 2.1) can be cross-validated against Sandvik kc1:
- `kc1` (Sandvik) = specific cutting force at 1mm chip thickness (N/mm2)
- `us` (Stephenson) = specific cutting energy (kW/cm3/min)

Conversion: `kc1 ~ us x 60,000` (since 1 kW/cm3/min = 1000 N-m/s per cm3/min = 60,000 N/mm2 roughly). However the exact relationship depends on cutting conditions. Both sources agree on relative material ranking.

| Material | Stephenson us (kW/cm3/min) | Equivalent kc1 approx (N/mm2) | Sandvik kc1 typical |
|----------|---------------------------|-------------------------------|---------------------|
| Aluminum | 0.012-0.022 | 700-1300 | 700-800 |
| Cast iron | 0.044-0.08 | 2600-4800 | 1000-1400 |
| Soft steel | 0.05-0.066 | 3000-4000 | 1500-1700 |
| Steel Rc<45 | 0.065-0.09 | 3900-5400 | 1700-2200 |
| Titanium | 0.053-0.066 | 3200-4000 | 1400-1600 |
| Ni superalloys | 0.09-0.15 | 5400-9000 | 2400-2800 |

Note: The conversion is approximate. Stephenson's us values are at 0.25 mm chip thickness and zero rake angle, while Sandvik kc1 is at 1 mm chip thickness. Since us increases as chip thickness decreases, the apparent values are higher than direct kc1.

---

## Summary of Key Constants for Cost Estimation Engine

| Parameter | Value | Source |
|-----------|-------|--------|
| Taylor n — HSS | 0.10-0.17 | p.549 |
| Taylor n — Uncoated WC | 0.20-0.25 | p.549 |
| Taylor n — Coated WC (TiN/TiC) | 0.30 | p.549 |
| Taylor n — Coated WC (Al2O3) | 0.40 | p.549 |
| Taylor n — Ceramic | 0.40-0.60 | p.549 |
| Taylor Ct — Mild steel rough | ~100 m/min | p.549 |
| Extended Taylor a (feed exp) — HSS | 0.77 | p.550 |
| Extended Taylor b (DOC exp) — HSS | 0.37 | p.550 |
| Extended Taylor Kt — Mild steel | ~500 | p.550 |
| Extended Taylor Kt — Cast iron | ~200 | p.550 |
| Optimum coating thickness | 0.010 mm | p.545 |
| Grinding us vs cutting us | ~10x | p.59 |
| Force ratio Ft:Fa:Fr (rough turning) | 4:2:1 | p.400 |
| Speed effect on tool life | 50% increase -> 80-90% life reduction | p.763 |
| DOC effect on tool life | 50% increase -> ~15% life reduction | p.762 |
| Actual/geometric Ra ratio | 1.0 - 2.4 (material dependent) | p.585 |
| Contact length to chip thickness ratio | 1.5-2.0 | p.415 |
