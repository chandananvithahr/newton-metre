# Ghosh & Mallik — Manufacturing Science (2nd Ed.) Data Extraction

**Source:** Manufacturing Science, 2nd Edition, Amitabha Ghosh & Ashok Kumar Mallik
**ISBN:** 8176710633 / 9788176710633
**Publisher:** East-West Press (Indian textbook)
**Extracted:** 2026-03-29

This document extracts ALL numerical data relevant to cost estimation from the textbook.
The book is organized into chapters: (1) Manufacturing Properties of Materials, (2) Casting Processes, (3) Forming Processes, (4) Machining Processes.

Note: Page numbers refer to the book's printed page numbers (visible in headers), not PDF page indices. The PDF is a compressed scanned version with 139 image pages covering the full book.

---

## 1. Material Properties (Chapter 1)

### Table 1.1 — Crystal Structure of Common Metals (p.4)

| bcc | fcc | cph |
|-----|-----|-----|
| Chromium | Aluminium | Titanium |
| Tungsten | Copper | Zinc |
| Vanadium | Lead | Zirconium |
| Molybdenum | Nickel | Magnesium |
| Iron (except in temperature range 910-1400 C) | Silver | Cobalt |
| | Iron (910-400 C) | |

**Key insight:** bcc structures are usually harder; fcc structures are more ductile; cph structures have low ductility.

### Table 1.2 — Properties Dependent on Crystal Structure and Defects (p.5)

| Property dependent on basic crystal structure | Property dependent on crystal imperfection |
|---|---|
| Density | Electrical conductivity |
| Specific heat | Yield stress |
| Coefficient of thermal expansion | Creep |
| Melting point | Fracture strength |
| Elastic constants | Semiconductivity |
| Hardness and ductility | Work hardening |
| | Fatigue strength |

### Table 1.3 — Effects of Alloying Elements on Steel (pp.25-27)

| Element | Effect(s) | Typical % | Remarks |
|---------|-----------|-----------|---------|
| Al | Deoxidizer | - | Restricts grain growth |
| B | Increases hardenability | - | Used with Mo, Cr, and V |
| Cr | Increases strength, toughness, red hardness; enhances corrosion and erosion resistance | 0.5-2 | Used in HSSS, cutting tools, springs, roller bearings |
| Mn | Increases hardenability; improves hot workability | 0.25-0.40 | Typical percentage in carbon steel |
| Mo | Improves hardenability; improves machinability; increases creep resistance | 12-30 | Typical percentage for stainless steel |
| Ni | Increases strength of ferrite; improves corrosion resistance | 2.5-5 | Typical percentage to increase toughness and strength |
| P | Strengthens low alloy steels; increases machinability | - | Free-cutting steels |
| S | Improves machinability of low surface finish | 0.08-0.15 | Normally considered an impurity |
| Si | Used as deoxidizer; increases strength when present in ferrite | 0.2-0.4 | Typical percentage |
| Ti | Fixes carbon in inert particles; reduces martensitic hardness | 0.15 | Fixes carbon in inert particles |
| V | Increases strength while retaining ductility; increases hardenability | 0.1-0.4 | Normally used in combination with Cr |
| W | Imparts red hardness and wear resistance | 4 | Typical percentage (imparts red hardness) |
| | Significantly improves hot hardness | 12-30 | Typical percentage range for hot hardness tools |
| | Improves strength at high temperature | 1+ | Typical percentage 1 to improve hot hardness |

### Heat Treatment Effects — Cooling Rate on Microstructure (p.25)

Properties for steel (austenite at 723 C cooled at different rates):

| Cooling Method | Resulting Structure | Tensile Stress (N/mm^2) | Yield Stress (N/mm^2) | Reduction in area (%) | Rockwell Hardness (C) |
|---|---|---|---|---|---|
| Water quenched | Martensite | 175 x 10^4 | 56 x 10^4 | Low | 65 |
| Oil quenched | Very fine pearlite | 112 x 10^4 | 28 x 10^4 | 22 | 35 |
| Air cooled | Fine pearlite | 88 x 10^4 | 28 x 10^4 | 27 | 25 |
| Furnace cooled | Coarse pearlite | 52 x 10^4 | 14 x 10^4 | 30 | 15 |

**Note:** Values given per Fig 1.29 table on p.25. Units are N/mm^2 (scaled by 10^4 for tensile/yield).

### Iron-Carbon Phase Diagram Key Temperatures (p.13)

- Pure iron melting point: 1537 C
- Eutectic temperature: 1130 C (4.3% C)
- Eutectoid temperature: 723 C (0.8% C)
- Maximum solubility of carbon in gamma-iron: 2% at 1130 C
- Maximum solubility of carbon in alpha-iron: 0.025% at 723 C
- Peritectoid: 1492 C
- delta-iron (bcc): 1400-1537 C
- gamma-iron (fcc): 910-1400 C
- alpha-iron (bcc): below 910 C

### TTT Diagram Key Temperatures (p.28-29)

- Nose of TTT diagram: ~550 C (minimum time for transformation)
- Martensite start: ~220 C
- Bainite forms below ~550 C but above martensite start
- At 600 C: transformation starts after minimum lag time

### Stress-Strain Curve Data for Engineering Materials (p.19, Fig 1.24)

Typical stress-strain curves shown for:
- **Mild steel:** Shows upper and lower yield points, elongation ~25%, UTS ~400-500 N/mm^2
- **Copper:** Continuous yielding, elongation ~40-50%
- **Cast iron:** Brittle, elongation ~1-2%, breaks ~200-300 N/mm^2

### Hydrogen Solubility in Metals (Table 2.2, p.42)

| Metal | Liquid phase solubility (ml/100g) | Solid phase solubility at melting point (ml/100g) |
|---|---|---|
| Aluminium | 0.69 | 0.036 |
| Copper | 5.42 | 2.24 |
| Iron | 27 | 5-11 |
| Magnesium | 26 | 20 |
| Nickel | 45 | 29 |

---

## 2. Casting Data (Chapter 2)

### Casting Solidification Data (p.79)

Steel casting example values:
- theta_s = 1550 C (solidus)
- theta_f = 1500 C (freezing)
- L' = 268 kJ/kg (latent heat)
- rho_m = 7680 kg/m^3 (density of molten steel)
- c_m = 0.67 kJ/kg-K (specific heat liquid)
- c_sw = 0.755 kJ/kg-K
- k_s = 76 W/m-K (thermal conductivity of steel)

### Pattern Allowances (Table 2.1, p.36)

Machining allowances for various metals:
- Cast iron (surfaces), Grey iron, malleable iron
- Range typically: 1.5-6 mm depending on dimension and surface

### Melting Furnace Temperatures (p.44-45)

- Induction furnace: 1750 C
- Side-blow converter: 1700 C
- Cupola: 1650 C

### Continuous Casting Data (p.99)

- Iron slab density: rho_m = 7600 kg/m^3
- Production rate: 25,000 kg/hr per strand
- Nozzle discharge coefficient: 0.8
- Vacuum pressure: 10^-3 atm

---

## 3. Forming Processes — Forces and Parameters (Chapter 3)

### 3.1 Rolling

#### Rolling Force Formulas (pp.108-119)

The rolling force per unit width:
```
p = 2K[exp(2mu*x_n/h) + 1/(2mu) * (x - x_n)]    (eq 3.33)
```

Where:
- K = shear yield stress = sigma_y / sqrt(3)
- mu = coefficient of friction
- h = strip thickness at point
- x_n = neutral point position

**Example 3.4 (p.118-119):**
- Strip: 24 mm x 24 mm cross-section
- Final size: 6 mm x 96 mm x 150 mm
- mu = 0.25 (coefficient of friction)
- Average yield stress of lead in tension: 7 N/mm^2
- K = 1/sqrt(3) * sigma_y = 4.04 N/mm^2

Neutral point location:
```
x_n = h/(2mu) * ln(1/(2mu * sqrt(R/h)))    (eq 3.34)
```
With mu = 0.25:
- x_n = 6/(2 x 0.25) * ln(1/(2 x 0.25)) = 8.3 mm

Pressure distribution:
- Nonsticking zone: p = 8.08 * e^(0.083x) N/mm^2 (0 <= x <= 8.3 mm)
- Sticking zone: p = 8.08(0.614 + 0.167x) N/mm^2 (8.3 <= x <= 48 mm)
- Total forging force: 150 x 3602.5 N = 0.54 x 10^6 N

#### Roll Deflection (p.152)

```
delta = (F*l^2)/(4*E*I) + (F*l)/(G*A)    (eq 3.106)
```

Where:
- lambda_1, lambda_2 = factor for nature of load distribution
- Typical values: lambda_1 = 1.0 and lambda_2 = 0.2 for strip width > l/2
- lambda_1 = 1.0 and lambda_2 = 0.1 for strip width < l/2

### 3.2 Drawing (Wire/Rod)

#### Drawing Stress and Maximum Reduction (pp.126-127)

Drawing stress formula:
```
sigma_d = sigma_y_avg * [1 + (1-cos(alpha))/(mu*cos(alpha))] * [1 - (d_f/d_i)^(2mu/tan(alpha))]
```

**Example 3.7 (p.126-127):**
- Steel wire: initial diameter 12.7 mm, final diameter 10.2 mm
- Die half angle: 6 degrees
- Speed: 90 m/min
- Coefficient of friction: 0.1
- Tensile yield stress: 207 N/mm^2 (original steel specimen)
- True fracture strain: 414 N/mm^2
- Strain: 0.438 (linear stress-strain assumed)
- Average yield stress: 297.5 N/mm^2
- Maximum allowable reduction D_max: 0.652 (i.e., max ~65% reduction)

Drawing power:
```
P = F * V_d    (eq 3.56)
```

**Example:** Drawing power = 211.2 x (pi/4) x (10.2)^2 x 90/60 W = 25.887 kW

### 3.3 Extrusion

#### Extrusion Force Formulas (pp.138-139)

Work load from energy consideration:
```
W_b = (pi/sqrt(3)) * sigma_y * d_i^2 * V_b * ln(d_i/d_f)    (eq 3.81)
```

Average deformation energy:
```
W_d = integral of sigma * d(epsilon) = 2 * sigma_y * ln(d_i/d_f)
```

### 3.4 Deep Drawing

#### Deep Drawing Force (pp.126-131)

Drawing force estimate (neglecting friction):
```
F = sigma_0 * 2*pi*r_p * t    (eq 3.66)
```

Where:
- sigma_0 = maximum allowable stress of material
- r_p = punch radius
- t = sheet thickness

**Blank holder force (p.129):**
```
F_b = B * pi * r_b^2 * K    (eq 3.65)
```
Where B = 0.02 to 0.08 (beta coefficient).

**Example 3.8 (p.130):**
- Cold rolled steel cup with inside radius 30 mm
- Thickness: 3 mm
- Blank radius: 40 mm
- Maximum allowable stress: 210 N/mm^2 and 600 N/mm^2
- mu = 0.1, beta = 0.05
- Blank holder force F_b = 0.05 x pi x 40^2 x 210 = 52,778 N
- sigma_r at r = r_p: 94.8 N/mm^2 (using eq 3.64) = 110.9 N/mm^2
- Drawing force F = 2*pi*r_p * 3 x 110.9 = 62,680 N
- With sigma_0 = 600 N/mm^2: F = sigma * pi * d * t = 512.8 N/mm^2 => 62,680 N
- Minimum possible r_p = 9.2 mm (limit before buckling)

#### Limiting Drawing Ratio (p.156, Fig 3.43)

| Drawing Operation | Limiting Drawing Ratio (D_max/d) |
|---|---|
| First draw | ~2.0 |
| Second draw (redraw) | ~1.3 |
| Third draw | ~1.2 |

Values without blank holder:
- For first draw: slightly lower, ~1.8

### 3.5 Bending

#### Bending Force Determination (pp.130-131)

Bending force for V-die bending:
```
F = (K * UTS * w * t^2) / W    (general bending force formula)
```

Minimum bend radius formula (p.131):
```
r_min = t * [(1/(2*e_f)) - 1]
```
Where e_f = fracture strain of material.

**Neutral plane shift (p.131):**
- Shift of neutral plane = 5% for practical bending
- Limiting value of r_min for strain hardening: r_min/t = f(n, material)

**Bend allowance (p.131):**
```
r_min/t = ln[1 + (1.82(e_f))/(0.63 + 1.32*e_f)] - (0.43 + 0.5*e_f)/(0.63 + 1.32*e_f) + 0.5*e_f + 0.43
```

Where e_f = engineering fracture strain.

#### Spring-back Angle Relation (p.131):
```
alpha_i/alpha_f = 1 - (3*Y*r_i)/(E*t) + (r_i*Y/E*t)^3
```

### 3.6 Punching and Blanking

#### Punching/Blanking Force (pp.143-149)

Maximum punching force:
```
F_max = sigma_u * pi * d * t    (for round punch)    (eq 3.103)
```
or
```
F_max = sigma_u * c * t    (general, c = cutting perimeter)    (eq 3.105)
```

Where:
- sigma_u = true rupture stress
- c = perimeter of cut
- t = sheet thickness

**Work done for punching:**
```
W = integral of F dp = F_max * p    (eq 3.104)
```
Where p = depth of penetration = delta + c_p

**Example 3.12 (p.149):**
- Punch a hole of 50 mm diameter
- Material: 3-mm-thick sheet steel
- True fracture stress: 1.75 kN/mm^2 (1750 N/mm^2)
- True fracture strain: 2.1 kN/mm^2 (2100 N/mm^2)

Solution:
- Optimum clearance c_p: from eq 3.101
- F_max = 2100 x 0.33 x pi x 50 N = 108.9 kN

#### Optimum Clearance for Punching (p.147)

| e_f (fracture strain) | 1 | 1.5 | 2.0 | 2.5 |
|---|---|---|---|---|
| c_p/t | 0.215 | 0.133 | 0.082 | 0.05 |
| (delta + c_p)/t | 0.278 | 0.289 | 0.296 | 0.3 |

**Key insight:** Clearance varies from 5% to 20% of sheet thickness depending on ductility. Percentage penetration is about 30% of sheet thickness and increases very slowly with ductility.

#### Gap Between Blank Edge and Strip (Table 3.1, p.166)

| Strip thickness t (mm) | Gap b (mm) |
|---|---|
| t <= 0.8 | 0.8 |
| 0.8 < t <= 3.2 | t |
| t > 3.2 | 3.2 |

**Empirical rule:** Gap g = t + 0.015b, where t = thickness and b = width on the blank.

### 3.7 Explosive Forming (p.167)

Pressure relation:
```
p = C*W^(1/3) * D^(-n) N/mm^2    (eq 3.107)
```
Where:
- W = weight of explosive in newtons
- D = distance from explosive (standoff)
- Typical value of n ~ 1.15
- C = constant of proportionality

| Explosive | C | Pentolite | TNT | Tetryl |
|---|---|---|---|---|
| | | 4500 | 4320 | 4280 |

With pressures up to 35 kN/mm^2 for high explosives placed directly on workpiece. With low explosives, pressures limited to 350 N/mm^2.

---

## 4. Machining Processes — Cutting Data (Chapter 4)

### 4.1 Chip Formation Theory

#### Merchant's Circle Analysis (pp.196-197)

Force components:
```
F_c = F_t = resultant cutting force tangential component
F_n = F_r = thrust (radial) component
F_s = shear force on shear plane
N_s = normal force on shear plane
F = friction force on rake face
N = normal force on rake face
```

Relations:
```
F_c = R cos(eta - alpha)    (eq 4.7)
F_t = R sin(eta - alpha)    (eq 4.8)
F_s = F_c cos(phi) - F_t sin(phi)    (eq 4.9)
N_s = F_c sin(phi) + F_t cos(phi)
```

Where:
- phi = shear angle
- alpha = rake angle
- eta = angle of resultant force
- mu = tan(lambda) = F/N = coefficient of friction

#### Specific Energy / Cutting Energy (pp.198-199)

**Specific energy in machining:**
```
U_c = F_c / (b * t_1)    (eq 4.23)
```

Where:
- F_c = cutting force
- b = width of cut
- t_1 = uncut chip thickness
- U_c = specific cutting energy (also called specific cutting pressure)

**Power consumption formula:**
```
P_c = F_c * v    (eq 4.21a)
```

The energy consumption per unit volume of material removed is:
```
U_c = P_c / (rate of material removal) = F_c * v / (b * t_1 * v) = F_c / (b * t_1)
```

This is the specific energy, also known as specific cutting force (kc).

### Table 4.2 — Machining Constant C_c (Shear Angle, degrees) (p.202)

| Work material (hot rolled steel) | C_c (degrees) |
|---|---|
| AISI 1010 | 69.3 |
| AISI 1020 | 68.6 |
| AISI 1035 | 64.7 |
| AISI 2340 | 76.2 |
| AISI 3140 | 70.3 |
| AISI 4340 | 68.6 |
| Stainless 304 | 82 |

The machining constant tends to increase with cold working.

### Table 4.3 — Shear Angle Relations (p.202)

| Source | Shear angle relation |
|---|---|
| Ernst and Merchant | 2*phi + lambda - alpha = C_c |
| Merchant's second solution | 2*phi + lambda - alpha = cot^-1(k) |
| Lee and Shaffer | phi + lambda - alpha = pi/4 |
| Stabler | phi + lambda - alpha = pi/4 |

### Table 4.4 — Values of U_c (Specific Cutting Energy) for Various Materials (p.204)

| Material | Hardness | U_c (N/mm^2) | Approximate kc |
|---|---|---|---|
| Steel | 85-200 HB | 1.4 - ... (range) | ~1400-3400 |
| | (varies with BHN) | | |
| Steel | 85-200 | 1.4 x 10^3 | 1400 |
| Steel (harder) | 200-350 | (higher values) | ~2400-3400 |
| Cast iron | - | 1100-1600 | 1100-1600 |
| Aluminium | - | 400-700 | 400-700 |
| Brass | - | 560-830 | 560-830 |
| Copper alloys | - | 900-1260 | 900-1260 |
| Cast iron | 190-320 HB | ~1100-1600 | 1100-1600 |

**Note:** Values from the table image (p.204). The specific cutting energy U_c has units of N/mm^2 (equivalent to J/mm^3).

**Detailed Table 4.4 values (as read from p.204):**

| Material | Hardness (BHN) | U_c (N/mm^2) |
|---|---|---|
| Steel | 85-200 | 1.4 x 10^3 |
| Steel | (higher) | ~1500-1600 |
| Cast iron | 190-320 | 1.1 x 10^3 |
| Alloy steel | - | 1.1-1.6 x 10^3 |
| Copper alloy | - | ~1060 x 10^0 |

**Formula correction factor for uncut chip thickness:**
```
U_c = U_0 * (t_0/t_1)^a    (eq 4.22)
```
Where t_0 = 1 mm and a = constant. Some typical values are given (the correction increases as uncut thickness decreases).

### 4.2 Heat Generation and Cutting Temperature

#### Temperature Rise During Machining (pp.206-209)

**Total heat generated:**
```
Q = P_c / J = F_c * v / J    (in heat units)
```

**Average temperature rise of chip:**
```
theta_avg = (1-lambda) * Q / (rho * c * b * t_1 * v)    (eq 4.25)
```
Where lambda = fraction of heat going to workpiece (typically 0.1-0.3).

**Maximum temperature on rake face:**
The maximum interface temperature theta_max is proportional to sqrt(v):
```
theta_max = theta_0 + C * sqrt(v * t_1)    (approximately)
```

**Example 4.5 (p.208):**
- SAE 1040 steel being machined at cutting speed 200 m/min
- Tool rake angle 17 degrees
- Width of cut: 2 mm, uncut thickness: 0.25 mm
- Chip thickness ratio r = 0.4
- Coefficient of friction mu = 0.6
- sigma_s (shear stress of work) = 400 N/mm^2

Calculated:
- phi = 18.47 degrees (shear angle from Lee & Shaffer)
- F_s = 400 N, F_c = 632.6 N (from Merchant's equations)
- theta_s = 26.57 degrees
- F_c = 632.6 N
- W_s (shear zone heat) = 1135 W, W_f (friction heat) = 1155 W
- Thermal number R = 0.333
- lambda = 0.15 (fraction to workpiece)
- theta_chip_avg = 613.1 C (average chip temperature)
- theta_max_rake = 821 C (maximum rake face temperature)

**Important insight (p.209, Fig 4.17):** Maximum temperature is proportional to sqrt(cutting speed). At 0.06 mm/rev and 100 m/min, temperature ~350 C; at 500 m/min, temperature ~600 C.

### 4.3 Tool Wear and Tool Life

#### Flank Wear Criteria (Table 4.9, p.217)

| Tool | Wear criterion |
|---|---|
| HSS | 0.3 mm (when used for finishing) |
| | Catastrophic failure |
| HSS | 0.75 mm (for rough machining) |
| WC (cemented carbide) | 0.3-0.4 mm (when used for finishing) |
| | 0.5 mm (rough machining) |
| Ceramic | 0.3 mm |

#### Taylor's Tool Life Equation (p.218-219)

```
V * T^n = C
```

Where:
- V = cutting speed (m/min)
- T = tool life (min)
- n = exponent (depends on tool/work combination)
- C = constant (cutting speed for 1-minute tool life)

### Table 4.10 — Constants and Exponents of Generalized Taylor's Equation (p.219)

**(After Sen, G.C. and Bhattacharyya, A., Principles of Metal Cutting, New Central Book Agency, Calcutta, 1969)**

| Work material | Tool | n | C | p | q | Restriction |
|---|---|---|---|---|---|---|
| Steel (free cutting) | WC | 0.2 | - | - | - | - |
| | HSS | 0.125 | - | - | - | - |
| Steel | WTiC | 0.27 | - | - | - | - |
| Steel (10% C) | WC | 0.25 | 0.33 | 0.33 | - | - |
| | HSS | 0.14 | 0.18 | - | - | - |
| Steel (40% C) | WC | 0.27 | - | 0.3 | c/c 0.75 | - |
| Cast iron | WC | 0.25 | 0.28 | 0.4 | 0.15 | - |
| | Ceramic | 0.18 | - | - | - | - |

**Note:** The generalized Taylor equation is:
```
V * T^n * f^p * d^q = C_1
```
Where f = feed and d = depth of cut. The units of V, T, f are m/min, min, mm, respectively.

**Key insight:** n is observed to be smaller than p, indicating tool life is more sensitive to thickness than to width of cut. Typical n values:
- HSS: n = 0.1-0.15
- WC (carbide): n = 0.2-0.3
- Ceramic: ~0.4-0.6

#### Cutting Speed-Tool Life Graph Data (Fig 4.23, p.218-219)

Work material: AISI 1045, hardness 170 BHN:
- HSS tool: V*T^0.13 = C (from graph)
- WC tool: V*T^0.25 = C
- Ceramic: V*T^0.4-0.5 = C (estimated from graph)

At T = 60 min tool life:
- HSS: ~30 m/min
- WC: ~100-150 m/min
- Ceramic: ~200-400 m/min

### 4.4 Tool Materials

### Table 4.5 — Performance of Various Tool/Work Combinations (p.212)

| Tool | Work | Static hardness ratio | Modified hardness ratio | Remarks |
|---|---|---|---|---|
| Copper | Zinc | 1.98 | w1 | No successful machining possible |
| Zinc | Cadmium | 2.2 | w1 | No successful machining possible |
| Tin | Lead | 1.25 | w1 | No machining possible |
| Cemented carbide | Lead | - | w1 | No successful machining (but lead too soft) |
| Heat-treat. Steel alloy | Mild steel | 1.45 | w1 | No successful machining of mild steel possible |

**Key insight:** Hardness ratio alone does not predict machinability. The tool must be harder AND have different properties.

### Table 4.6 — Per Cent Composition of Tool Steels (p.214)

| Material | C | W | Cr | V | Mo |
|---|---|---|---|---|---|
| Carbon tool steel | 0.8-1.3 | - | - | - | - |
| High speed steel | 0.75 | 18.0 | 4.0 | 1.0 | - |

### Table 4.7 — Per Cent Composition of Carbides (p.214)

| Grade | Co | TiC | TaC | WC | Ni alloy steels |
|---|---|---|---|---|---|
| (Grade 1) | 94 | 6 | - | - | - |
| (Grade 2) | 70.7 | 4.5 | 12.5 | 12.6 | - |

(Specific grade numbers were partially visible)

### Table 4.8 — Cutting Speed for Various Tool Materials (p.214)

| Tool material | Cutting speed (m/min) |
|---|---|
| Carbon steel | 5 |
| High speed steel | 30 |
| Cemented carbide | 150 |
| Coated carbide | 350 |
| Ceramic | 600 |

**Variation of hardness with temperature (Fig 4.21, p.213):**
- HSS maintains hardness up to ~600 C, drops rapidly above
- Cemented carbide: maintains hardness up to ~800-900 C
- High carbon steel: drops rapidly above 300 C

### 4.5 Machining Operations

#### Drill Angles (Table 4.12, p.238)

| Material(s) | Helix angle (degrees) | Point angle (degrees) | Lip relief (degrees) | Chisel edge angle (degrees) |
|---|---|---|---|---|
| Brass and hard | 22-33 | 80 | 6-8 | 55 |
| (lower values for smaller sizes) | | | | |
| Steels and cast irons | 22-33 | 118 (lower value for smaller drills) | 8-12 | 55 |
| Soft materials | 22-33 | 140 | 6-8 | 71 |

#### Milling Specific Data

**Milling force components (Fig 4.48, p.245):**
```
F_t = specific cutting force per unit width * b * t_max * sin(beta)
F_r = approximately 0.3 * F_t to 0.5 * F_t
```

### Table 4.13 — Values of A and k for Milling (p.249)

| Material | A | k |
|---|---|---|
| Alloy steel | 1100 | 1.06 |
| Mild steel | 900 | 0.88 |
| CI (Cast iron) | 500 | 0.70 |
| Bronze | 300 | 0.4-0.5 |

**Milling force formula:**
```
F_c = A * t_1^k    (tangential cutting force, per unit width)
```

Where t_1 is the average uncut thickness in mm, and F_c is in N/mm.

### Table 4.14 — Values of Specific Energy for Milling (p.250)

| Material | U_c (J/mm^3) |
|---|---|
| Steel (BHN 100) | 3.5 |
| Steel (BHN 400) | 5.5 |
| Cast iron | 1.5-3.5 |
| Aluminium | 0.6-1.0 |
| Bronze | 1.0-1.5 |

### 4.6 Surface Finish

### Table 4.17 — R_a for Various Machining and Abrasive Processes (p.272)

| Process | R_a range (micrometers) |
|---|---|
| Turning, boring | 0.05-21 |
| Milling | 0.25-25 |
| Planing, shaping | 0.375-25 |
| Drilling | 0.375-12.5 |
| Reaming, broaching | 0.5-6.25 |
| Grinding | 0.025-6.25 |
| Honing | 0.025-0.375 |
| Lapping | 0.013-0.75 |

#### Ideal Surface Roughness in Turning (pp.270-271)

For tool without nose radius:
```
R_max = f / (cot(C_s) + cot(C_e))    (eq 4.76)
```
Where f = feed rate, C_s = side cutting edge angle, C_e = end cutting edge angle.

For tool with nose radius r:
```
R_max = f^2 / (8*r)    (approximately)    (eq 4.77)
```

**Example 4.31 (p.271):**
- Nose radius r = 1.2 mm
- Feed f = 0.15 mm/rev
- R_max = 0.15^2 / (8 x 1.2) = 0.002 mm = 2 micrometers
- R_a = R_max/4 = 0.5 micrometers (approx)

#### Surface Roughness in Milling (p.272)

For slab milling with straight cutter:
```
R_max = f^2 / (4*D)    (approximately)
```
Where f = feed per tooth, D = cutter diameter.

#### Surface Roughness Variation (Fig 4.69, p.273)

Experimentally, R_max varies with cutting speed:
- Below ~50 m/min: R_max relatively high (built-up edge region)
- BUE peak: around 30-50 m/min for mild steel
- Above 100 m/min: R_max decreases, BUE eliminated
- Optimal: high speed with small feed

---

## 5. Machining Economics (Chapter 4, Section 4.6)

### Cost Model for Turning Operations (pp.274-281)

**Total cost per piece:**
```
C_p = C_m * t_c + C_m * t_l + C_m * (t_c/T) * t_g + (C_e + C_m * t_g) * (t_c/T)    (eq 4.79, expanded)
```

Where:
- C_m = cost/min of labour and overheads (Rs/min)
- t_c = cutting time per piece
- t_l = loading/unloading and idle time per piece
- T = tool life
- t_g = time to change/regrind tool
- C_e = cost per cutting edge

The total cost has four components:
1. **Material cost** — independent of cutting conditions
2. **Machining cost** = C_m * t_c
3. **Setting-up and idle time cost** = C_m * t_l
4. **Tool changing and regrinding cost** = (C_e + C_m * t_g) * (t_c/T)

#### Feed Rate Expression (p.274)

The cutting time:
```
t_c = (L * D) / (f * v * 1000)    (min)
```
Where:
- L = length of job (mm)
- D = diameter (mm)
- f = feed (mm/rev)
- v = cutting speed (m/min)

**Using Taylor's equation V*T^n = C:**
```
t_c = (pi * D * L) / (1000 * f * v)    (simplified)
```

#### Optimum Cutting Speed for Minimum Cost (p.277)

```
v_opt = C / [(1/n - 1) * (C_e/(C_m) + t_g)]^n    (eq 4.83)
```

Or equivalently:
```
T_opt = (1/n - 1) * (C_e/C_m + t_g)    (optimum tool life)    (eq 4.82)
```

#### Optimum Cutting Speed for Maximum Production (p.281)

```
T_opt_production = (1/n - 1) * t_g    (eq 4.85)
```

**Key insight:** The optimum speed for maximum production is ALWAYS higher than the optimum speed for minimum cost. The optimum for minimum time ignores tool cost (C_e).

### Example 4.26 (pp.279-280)

A cylindrical bar is to be turned. Given:
- Feed: 0.25 mm/rev
- Taylor's tool life: v * T^0.13 = C (for HSS), equivalently n = 0.13
- Maximum allowable feed f = 0.25 mm/rev
- Cost of tool regrinding and overheads: Rs 0.51 per resharpening (total C_e)
- Machining cost rate C_m = Rs 3/hr for tool handling (implied from the problem)
- Tool changing time t_g = 2 minutes
- Total cost per tool including regrinding = Rs 0.51

Optimum cutting speed:
```
T_opt = (1/0.13 - 1) * (0.51/C_m + 2) minutes
```

Solving: T_opt = 71 minutes, giving v_opt = 21.45 m/min (approximately).

### Example 4.27 (p.280)

- 500-mm-long bar with 50 mm diameter to be turned
- Allowable feed: 0.25 mm/rev
- Tool cost and regrinding = Rs 0.25
- Overheads = Rs 3/hr (implied from context)

Cost comparison for Material X vs Material Y:
- **Material X:** n = 0.13, C = 75
  - T_opt = 71 min → v = 13.33 m/min
  - Minimum cost piece: Rs 0.29 + tool cost portions

- **Material Y:** n = 0.13, C = 75 (different constants)
  - Different optimum values

**Conclusion:** Material Y was recommended despite being more expensive because its machinability was much better.

### Example 4.28 — Maximum Production Rate (p.281)

Finding optimum cutting speed for max production:
```
T_opt = (1/n - 1) * t_g = (1/0.13 - 1) * 2 = 6.69 * 2 ≈ 13.38 minutes
```

This gives a higher optimum speed than minimum cost, confirming the theoretical insight.

---

## 6. Grinding Data (Chapter 4, Section 4.4)

### Grinding Specific Energy (pp.256-258)

Specific energy for grinding is significantly higher than conventional machining:
```
U_c (grinding) >> U_c (turning)
```

**Example 4.20 (p.256):**
- Plunge grinding of mild steel
- Wheel: 250 mm diameter, 13 mm width
- Grinding speed: 250 x pi x 13 = using 3 grits/mm^2
- Wheel speed: 2000 rpm
- Depth of cut: 0.05 mm
- Chip thickness estimated: 0.00027 mm (very thin)
- Specific energy: much higher than Table 4.4 values

**Example 4.21 (p.258):**
- Surface grinding of mild steel block
- Depth of cut: 0.05 mm
- Feed rate: 200 mm/sec
- Wheel diameter: 200 mm, speed 3000 rpm
- Maximum uncut thickness to = 15 micrometers
- Power required: 0.25 W per mm^3/sec of MRR

### Grinding Temperature (pp.260-261)

Surface temperature during grinding:
```
theta_s = 1.13 * (q/k) * sqrt(alpha * l_c / V_w)    (eq 4.71)
```

Where:
- q = heat flux at grinding zone
- k = thermal conductivity
- alpha = thermal diffusivity
- l_c = contact length
- V_w = workpiece velocity

**Critical temperature:** Workpiece can reach 1000 C+ at the grinding zone, causing:
- Thermal damage (burning)
- Residual stresses
- Metallurgical transformation (martensite formation)
- Maximum depth before burning: depends on specific energy and MRR

**Surface grinding depth limit for no burning (Example 4.22, p.261):**
- Depth of cut 0.03 mm, feed rate 200 mm/min
- Surface temperature = 0.053 (consistent unit) → below critical
- For same material removal but different depth (0.05 mm): temperature = 200+ C

### Grinding Wheel Specification (pp.262-265)

Standard wheel specification system: A-N-36-K-V

Where:
- A = Abrasive type (A = aluminium oxide, C = silicon carbide)
- N = Hardness grade (A-Z, soft to hard)
- 36 = Grain size (8-600, coarse to very fine)
- K = Grade (hardness of bond)
- V = Bond type (V = vitrified, B = resinoid, R = rubber, S = shellac, E = epoxy)

**Abrasive selection rules:**
- Aluminium oxide (Al2O3): for steel, wrought iron, tough bronze
- Silicon carbide (SiC): for cast iron, brass, aluminium, copper, non-ferrous
- Diamond: for tungsten carbide, glass, gems, stone
- CBN (Borazon): for hardened steels, super alloys

### Honing and Lapping Data (p.269)

- **Honing:** removes material up to 0.5 mm, produces Ra 0.05-0.5 micrometers
- Honing pressure: typically 1-3 MPa
- Honing speed: 15-30 m/min (rotational) + 10-20 m/min (reciprocating)

- **Lapping:** produces flatness of 0.025 mm over 300 mm
- Lapping pressure: 0.01-0.1 MPa (very light)
- Material removal: 0.0025 mm per pass (typical)
- Ra achievable: 0.013-0.05 micrometers

### Superfinishing (p.269)

- Ra achievable: 0.005-0.05 micrometers
- Pressure: 0.1-0.35 MPa
- Stone oscillation: 1-5 mm amplitude at 200-1000 cycles/min
- Speed: 5-30 m/min

---

## 7. Shaping/Planing Data (Chapter 4, Section 4.3.1)

### Metal Removal Rate (p.228)

```
MRR = f * d * L * N_s    (mm^3/min)
```
Where:
- f = feed per stroke (mm)
- d = depth of cut (mm)
- L = stroke length (mm)
- N_s = number of strokes per minute

Quick return ratio:
```
N_s = n * (1 + 1/r)    (strokes per min)
```
Where r = quick return ratio.

### Example 4.8 (p.229)

Orthogonal machining during shaping:
- Feed rate: 0.25 mm, depth: 0.25 mm
- Cutting speed: 30 m/min
- Material: HB 110 BHN
- Specific power consumption U_c = 0.51 J/mm^3 (from Table 4.4 for this hardness)
- MRR = 0.25 x 0.25 x 30 x 10^3 / 60 = 200 mm^3/sec (approximately)
- Power = U_c x MRR = 0.51 x 200 = 220 W (approximately)

### Example 4.9 — Shaping Force Calculation (p.229)

- Tool: 10-degree rake angle, orthogonal cutting
- Cutting speed: 30 m/min
- Uncut thickness: 0.25 mm, width of cut: 25 mm
- Using Lee and Shaffer's relationship: phi = 45 - (lambda - alpha)
- Computed F_c = 565 N, F_t = 211 N
- Power = F_c x v = 565 x 0.5 = 283 W
- Specific power = 1.47 J/mm^3

---

## 8. Turning Detailed Data (Chapter 4, Section 4.3.2)

### Turning Speed and Feed Relations (pp.230-235)

Cutting speed in turning:
```
v = pi * D * N / 1000    (m/min)    (eq 4.43)
```

MRR in turning:
```
MRR = f * d * v    (mm^3/min)
```

Or:
```
MRR = pi * D * f * d * N    (mm^3/min)    (eq 4.44)
```

### Example 4.11 (p.234)

Turning a mild steel bar of 100 mm diameter:
- Tool specification: 0-10-7, 5-10-97-0.45 (ASA system)
- Cutting speed: 200 m/min
- Depth of cut: 2.5 mm, feed: 0.125 mm/rev
- Coefficient of friction: 0.6
- Specific shear stress: 400 N/mm^2

Computed:
- Effective rake angle: close to orthogonal
- F_c = 400 x 0.125 x 2.5 x cos(31-11.8) / [cos(19.3+31-11.8) x sin 31] = ~334 N
- F_t (thrust) = ~136 N

### Face Turning Tool Life Relationship (p.235)

During face turning, the instantaneous wear rate:
```
dh/dt = K * V^(1/n)
```

For fast turning method with multiple speed changes:
```
N_1 * T_1 + N_2 * T_2 = total available flank wear
```

### Example 4.12 (p.234-235)

A mild steel bar of 100 mm diameter:
- Tool: 0-10, 7-5-10-97-0.45
- Speed: v calculated based on constraints
- F_c calculation using Merchant's equations
- sigma_s = 400 N/mm^2 (shear stress)
- F_c = ~334 N, F_t = ~136 N (computed)

---

## 9. Drilling Data (Chapter 4, Section 4.3.3)

### Drilling Geometry and Forces (pp.236-241)

Drill geometry:
```
t_1 = (f/2) * sin(kappa)    (uncut chip thickness per lip)    (eq 4.59)
b = d / (2 * sin(kappa))    (width of cut per lip)
```

Where:
- f = feed per revolution (mm/rev)
- kappa = half point angle
- d = drill diameter

### Drilling Torque and Thrust (pp.238-241)

Torque:
```
M = F_c * d/4 + M_chisel    (eq 4.65)
```

Where:
- F_c = cutting force at the cutting lips
- M_chisel = torque contribution from chisel edge (~80% of total torque is from lips)
- F_chisel = significant (~50% of thrust)

Thrust force:
```
F = F_t_lips + F_chisel    (eq 4.66)
```

### Example 4.14 (p.240)

Drilling with HSS drill:
- Drill diameter: 2 mm (implied from calculation)
- Point angle 2kappa = 118 degrees → kappa = 59 degrees
- Normal rake angle at middle cutting edge lip: from tables
- Feed: 0.23 mm/rev
- Coefficient of friction: 0.6
- t_1 (uncut chip thickness) = 0.1 mm
- sigma_s = 400 N/mm^2

Computed:
- phi = 45 degrees (using Lee & Shaffer)
- F_c = 1317 N (per lip)
- F_t = 350 N (per lip)
- Total torque M = 12.2 N-m
- Total thrust F = 1300 N (approximately)

---

## 10. Broaching Data (Chapter 4, Section 4.3.5)

### Broaching Parameters (pp.250-253)

Tooth spacing:
```
p = 1.75 * sqrt(L)    (eq 4.56)
```
Where L = length of surface to be broached (mm).

Cut per tooth: typically in range 0.05-0.5 mm.

Cutting speed for broaching: 6-15 m/min (relatively slow).

Broaching force per tooth:
```
F = specific cutting force * b * t_per_tooth
```

### Broaching Material Properties (p.253)

Hardness of some broach materials:
- Buttons carbide: 70-100 HRB
- Carbide-tipped tools: higher
- HSS broaches: most common for production

---

## 11. Key Formulas Summary for Cost Estimation

### Material Removal Rate (MRR) by Process

| Process | MRR Formula |
|---|---|
| Turning | MRR = v * f * d (mm^3/min) where v in mm/min, f in mm/rev, d in mm |
| Milling | MRR = w * d * v_f (mm^3/min) where w = width, d = depth, v_f = feed speed |
| Drilling | MRR = (pi * d^2 / 4) * f * N (mm^3/min) |
| Shaping/Planing | MRR = f * d * v_stroke * N_strokes |
| Grinding | MRR = v_w * d * b (mm^3/min) where d = depth of cut, very small |
| Broaching | MRR = n_teeth_engaged * cut_per_tooth * b * v_broach |

### Cutting Force (General Orthogonal)

```
F_c = tau_s * b * t_1 * cos(lambda - alpha) / [sin(phi) * cos(phi + lambda - alpha)]
```

### Power Consumption

```
P = F_c * v / 60    (watts, if v in m/min)
P = U_c * MRR    (watts, if U_c in J/mm^3 and MRR in mm^3/sec)
```

### Taylor's Tool Life

```
V * T^n = C    (basic form)
V * T^n * f^p * d^q = C    (generalized form)
```

### Economic Cutting Speed

```
v_min_cost = C * [(1/n - 1) * (C_e/C_m + t_g)]^(-n)
v_max_prod = C * [(1/n - 1) * t_g]^(-n)
```

### Punching Force

```
F = sigma_u * perimeter * thickness
```

### Deep Drawing Force

```
F = sigma_0 * pi * d * t * [ln(D/d) + correction for friction and bending]
```

### Bending Force (V-die)

```
F = K * sigma_u * w * t^2 / W
```
Where K = constant (1.2-1.33 for V-die), W = die opening width.

---

## 12. Indian Context Notes

### Indian Standards Referenced

The textbook is published by East-West Press, New Delhi, and is a standard Indian engineering textbook. Key Indian context:

1. **IS grade steels** are not directly tabulated in this edition, but AISI equivalents are given (see Table 4.2). The mapping to IS grades is:
   - AISI 1010 → approximately IS 2062 Grade E250 (mild steel)
   - AISI 1020 → approximately IS 1570 20C8
   - AISI 1035 → approximately IS 1570 35C8
   - AISI 4340 → approximately IS 1570 40Cr1Mo28

2. **Indian manufacturing practices** referenced:
   - Ghosh, A. and Mallik, A.K., "Mechanics of Stamping and Blanking," Proceedings of 9th All India Machine Tool Design and Research Conference, Kanpur, 1980 (p.145)
   - Sen, G.C. and Bhattacharyya, A., "Principles of Metal Cutting," New Central Book Agency, Calcutta, 1969 (p.219)

3. **Indian university standard:** This textbook is the prescribed text for manufacturing engineering courses at IITs, NITs, and most Indian engineering colleges. The data and examples use SI units throughout.

4. **Currency context:** While no rupee rates are given in the textbook (it focuses on physics/engineering), the machining economics section (Section 4.6) uses generic cost variables that can be parameterized with Indian shop floor rates.

### Key Physical Constants Used Throughout

| Constant | Value | Unit |
|---|---|---|
| Density of steel | 7680-7860 | kg/m^3 |
| Density of cast iron | 7200 | kg/m^3 |
| Density of aluminium | 2700 | kg/m^3 |
| Density of copper | 8900 | kg/m^3 |
| Density of lead | 11340 | kg/m^3 |
| Latent heat of steel | 268 | kJ/kg |
| Specific heat (steel, solid) | 0.755 | kJ/kg-K |
| Specific heat (steel, liquid) | 0.67 | kJ/kg-K |
| Thermal conductivity of steel | 76 | W/m-K |
| Melting point of pure iron | 1537 | C |
| Eutectic temperature (Fe-C) | 1130 | C |
| Eutectoid temperature (Fe-C) | 723 | C |

---

## 13. Cross-Reference to Costimize Engine Parameters

### Direct applicability to costimize-v2 engines:

| Ghosh-Mallik Data | Costimize Engine | File |
|---|---|---|
| Table 4.4 (U_c values) | Specific cutting force kc | engines/mechanical/cutting_data.py |
| Table 4.10 (Taylor constants n, C) | Tool life calculation | engines/mechanical/process_db.py |
| Table 4.8 (cutting speeds by tool) | Base cutting speed selection | engines/mechanical/cutting_data.py |
| Table 4.17 (Ra values) | Surface finish quality estimation | engines/mechanical/process_db.py |
| Table 4.13 (milling A, k) | Milling force estimation | engines/mechanical/process_db.py |
| Table 4.14 (milling specific energy) | Milling power consumption | engines/mechanical/process_db.py |
| Punching force formula | Blanking force for sheet metal | engines/sheet_metal/cutting_db.py |
| Bending force formula | Press brake tonnage | engines/sheet_metal/bending_db.py |
| Deep drawing formulas | Drawing force estimation | (future: engines/sheet_metal/) |
| Section 4.6 (machining economics) | Cost model structure | engines/mechanical/cost_engine.py |
| Optimum clearance table | Blanking die clearance | engines/sheet_metal/cutting_db.py |

### Values to validate/update in costimize engines:

1. **Specific cutting energy (kc/Uc):** Ghosh-Mallik gives Steel 85-200 BHN as 1400 N/mm^2. Compare with Sandvik kc1 values currently in cutting_data.py.

2. **Taylor exponents:** n = 0.125 for HSS, n = 0.2-0.3 for WC, n = 0.4-0.6 for ceramic. These should match our tool life calculations.

3. **Surface roughness:** Ra ranges by process (Table 4.17) can be used to set quality-based surcharges.

4. **Punching force:** F = sigma_u * perimeter * thickness — directly usable for blanking cost estimation.

5. **Grinding specific energy:** Much higher than cutting (5-50x), explaining why grinding is expensive per unit volume removed.
