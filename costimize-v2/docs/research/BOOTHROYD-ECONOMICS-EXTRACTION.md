# Boothroyd & Knight - Chapter 6: Economics of Metal-Cutting Operations

> Extracted from "Fundamentals of Machining and Machine Tools" (3rd Edition)
> by G. Boothroyd & W.A. Knight, Chapter 6, pages 175-204.
> Scanned PDF, OCR'd via vision model, March 2026.

---

## 6.1 Introduction (p.175)

**Key definitions:**
- **Production time** = average time to produce one component
- **Production cost** = total average cost of performing the machining operation on a component using one machine tool

**Critical insight:** Maximum production rate does NOT give minimum production cost. The manufacturing conditions for each are different. A compromise must be sought.

**Cost components for a batch of N_b components:**
1. Nonproductive time: `N_b * t_l` (load/unload per part)
2. Total machining time: `N_b * t_m` (cutting time per part)
3. Total tool changing time: `N_t * t_ct` (N_t = number of tools used, t_ct = tool change time)

---

## 6.2 Choice of Feed (p.177)

**Guiding principle:** Feed should always be set at the maximum possible.

**Rationale:**
- Changes in cutting speed affect neither the cutting operation nor the specific energy consumption by the same amount. An increase in feed will not affect the relative speed of sliding at the wearing surface of the tool, whereas the speed of sliding will change in proportion to the cutting speed.
- Since tool wear is a function of both temperature and relative speed of sliding, it can be approximated that increases in cutting speed will result in a greater reduction in tool life than similar increases in feed.
- If increased production rate is required in rough machining, it will always be preferable to increase the feed rather than increase the speed.
- A faster-cut feed will increase cutting forces and will depend on the maximum tool force the machine tool is able to withstand.

**Feed constraints (in order of priority):**
1. Maximum force the machine tool can withstand
2. Required surface finish (for finishing cuts)
3. Power available on the machine

---

## 6.3 Choice of Cutting Speed (p.178)

Two optimization criteria: **minimum production cost** and **minimum production time**.

### Production Cost Equation

Total machine and operator costs for a batch:

```
Total cost = M * (N_b * t_l + N_b * t_m + N_t * t_ct)
```

where `M` = total machine and operator rate (including overheads), $/s

Average production cost per component:

```
Eq. (6.2):  C_pr = M*t_l + M*t_m + (M * N_t/N_b * t_ct) + (N_t/N_b * C_t)
```

Where:
- `M` = machine + operator rate ($/s)
- `t_l` = nonproductive (load/unload) time per component (s)
- `t_m` = machining time per component (s)
- `t_ct` = tool changing time (s)
- `C_t` = cost of providing a sharp tool ($)
- `N_t` = number of tools used for the batch
- `N_b` = batch size

**Cost breakdown (4 terms):**
1. **Nonproductive cost** = `M * t_l` (constant, independent of cutting speed)
2. **Machining cost** = `M * t_m` (decreases as speed increases)
3. **Tool changing cost** = `M * (N_t/N_b) * t_ct` (increases as speed increases)
4. **Tool cost** = `(N_t/N_b) * C_t` (increases as speed increases)

### Taylor Tool-Life Equation

```
Eq. (6.3):  v/v_r = (t_r/t)^n
```

where:
- `v` = cutting speed
- `t` = tool life
- `v_r` = reference cutting speed
- `t_r` = measured tool life at speed v_r
- `n` = Taylor exponent (constant)

Rearranged:

```
Eq. (6.4):  t = t_r * (v_r / v)^(1/n)
```

Traditional English form:

```
Eq. (6.5):  v * t^n = C
```

where `v` in ft/min, `t` in minutes, `C` = cutting speed for 1 min of tool life (ft/min).

### Taylor Exponent Values

| Tool Material | Taylor exponent n | (1-n)/n factor |
|---------------|------------------|----------------|
| High-speed steel | ~0.125 | 7 |
| Carbide | 0.25 < n < 0.3 | 3 |
| Oxide or ceramic | 0.5 < n < 0.7 | 1 |

### Reference Cutting Speed Chart (Figure 6.2)

Approximate cutting speeds `v_r` when tool life `t_r = 60 s`, for various tool and work materials (from the log-log chart on p.180):

| Work Material | Tensile Strength (MN/m^2) | HSS v_r (m/s) | Carbide v_r (m/s) | Ceramic v_r (m/s) |
|---------------|--------------------------|---------------|-------------------|-------------------|
| Aluminum alloys | ~200 | 0.2-0.4 | 2-4 | -- |
| Brass | ~400 | 0.6-1.0 | 4-8 | -- |
| Cast steel | ~500 | 0.4-0.8 | 2-5 | -- |
| Cold-drawn steel, cast iron, bronze | ~600 | 0.3-0.6 | 2-4 | 8-15 |
| Iron forgings | ~700-900 | 0.5-1.5 | 3-8 | 10-30 |
| Heat-treated steels | ~1000-1500 | 0.8-4.0 | 5-20 | 20-80 |

Conversion: `197*v_r / C = (60/t_r)^n` (Eq. 6.7, for converting published C values to SI v_r)

### Number of Tools Used

```
Eq. (6.8):  N_t / N_b = t_m / t = (t_m / t_r) * (v / v_r)^(1/n)
```

### Machining Time

```
Eq. (6.9):  t_m = K / v
```

where `K` = constant for the particular operation. For cylindrical turning:
`K = (pi * d_w * l_w) / f`

- `d_w` = diameter of workpiece
- `l_w` = length to be turned
- `f` = feed

### Production Cost as Function of Speed

Substituting Eqs. (6.8) and (6.9) into (6.2):

```
Eq. (6.10):  C_pr = M*t_l + M*K*v^(-1) + (K / (v_r^(1/n) * t_r)) * (M*t_ct + C_t) * v^((1-n)/n)
```

### Optimum Cutting Speed for Minimum Cost

Differentiate Eq. (6.10) w.r.t. v and set to zero:

```
Eq. (6.11):  v_c = v_r * (n/(1-n) * M*t_r / (M*t_ct + C_t))^n
```

**Key insight:** The optimum cutting speed for minimum cost is **independent of batch size** and nonproductive times.

### Optimum Cutting Speed for Minimum Production Time

Average production time per component:

```
Eq. (6.12):  t_pr = t_l + t_m + (N_t/N_b) * t_ct
```

Differentiating and solving:

```
Eq. (6.13):  v_p = v_r * (n/(1-n) * t_r/t_ct)^n
```

**Comparison:** Eqs. (6.11) and (6.13) yield different optimum speeds. Minimum cost and minimum production time conditions are NOT the same.

---

## 6.4 Tool Life for Minimum Cost and Minimum Production Time (p.182-183)

### Optimum Tool Life for Minimum Cost

```
Eq. (6.14):  t_c = (1-n)/n * (t_ct + C_t/M)
```

### Optimum Tool Life for Minimum Production Time

```
Eq. (6.15):  t_p = (1-n)/n * t_ct
```

### Practical Approximations by Tool Material

The factor `(1-n)/n`:
- HSS: ~7
- Carbide: ~3
- Oxide/ceramic: ~1

**High-speed steel:**
```
Eq. (6.16):  t_c = 7 * (t_ct + C_t/M)
Eq. (6.17):  t_p = 7 * t_ct
```

**Carbide:**
```
Eq. (6.18):  t_c = 3 * (t_ct + C_t/M)
Eq. (6.19):  t_p = 3 * t_ct
```

**Oxide or ceramic:**
```
Eq. (6.20):  t_c = t_ct + C_t/M
Eq. (6.21):  t_p = t_ct
```

### Corresponding Optimum Cutting Speeds

Once optimum tool life is known:

```
Eq. (6.22):  v_c = v_r * (t_r / t_c)^n      (minimum cost)
Eq. (6.23):  v_p = v_r * (t_r / t_p)^n      (minimum production time)
```

---

## 6.5 Estimation of Factors Needed to Determine Optimum Conditions (p.184-185)

### Machine and Operator Rate M

```
Eq. (6.24):  M = W_o + (percent operator overhead / 100) * W_o
                 + M_t + (percent machine overhead / 100) * M_t
```

Where:
- `W_o` = operator's wage rate ($/s)
- `M_t` = machine depreciation rate ($/s)

**Operator overhead:** 100% to 300% (includes benefits, facilities, administration)
**Machine overhead:** includes power, servicing, location costs

### Machine Depreciation Rate

```
Eq. (6.25):  M_t = initial cost of machine / (working hours per year * amortization period)
```

Amortization period: typically 2-10 years depending on machine type and tax depreciation rates.

### Cost of Providing a Sharp Tool

**For regrindable tools:**
```
Eq. (6.26):  C_t = cost of grinding + cost of tool / average number of regrinds possible
```

Note: Although a tool might theoretically be reground 20 times, in practice the actual number is often less than half the theoretical number (tools get damaged/chipped).

**For disposable-insert tools:**
```
Eq. (6.27):  C_t = cost of insert / avg cutting edges used per insert
                  + cost of holder / (cutting edges used during life of holder)
```

### Tool-Changing Time

**For disposable-insert tools:**
```
Eq. (6.28):  t_ct = [time to index * (avg edges used per insert - 1) + time to replace insert]
                    / avg cutting edges used per insert
```

### Reference Cutting Speed

`v_r` for a particular tool life `t_r` depends on tool material, tool shape, work material, and cutting conditions. Values of `C` (cutting speed for 1 min of tool life) are tabulated in machining handbooks. A rough guide is presented in Figure 6.2.

---

## 6.6 Example of a Constant-Cutting-Speed Operation (p.185-188)

### Problem Setup

Rough-turning steel shafts to 76 mm diameter for 300 mm length at feed 0.25 mm.

**Given data:**
- Brazed-type carbide tool
- Taylor constants: n = 0.25, v_r = 4.064 m/s (C = 800 ft/min) when t_r = 60 s
- Machine initial cost: $10,800, amortized over 5 years
- Operator's wage: $0.0015/s ($5.40/hr)
- Operator and machine overheads: 100% each
- Tool-changing and resetting time: t_ct = 300 s
- Cost of regrinding: $2.00
- Tool cost: $6.00, reground 10 times average
- Nonproductive time per component: t_l = 120 s

### Step-by-Step Calculation

**1. Machine and operator rate M:**
```
M_t = 10,800 / (7.2 x 10^6 s x 5) = $0.0003/s
M = 0.0003 + 0.0003 + 0.0015 + 0.0015 = $0.0036/s
```

**2. Cost of providing a sharp tool C_t:**
```
C_t = $2.00 + $6.00/10 = $2.60
```

**3. Tool-changing time:**
```
t_ct = 300 s
```

**4. Optimum tool life for minimum cost (Eq. 6.18, carbide):**
```
t_c = 3 * (300 + 2.6 x 10^3 / 3.6) = 3 * (300 + 722) = 3070 s (51.2 min)
```

Wait -- re-reading: `t_c = 3(t_ct + C_t/M) = 3(300 + 2600/3.6) = 3(300 + 722.2) = 3067 s`

Actually from the text: `t_c = 3(300 + (2.6 x 10^3)/3.6) = 3.07 ks (51.2 min)`

**5. Cutting speed for minimum cost (Eq. 6.22):**
```
v_c = 4.064 * (60/3070)^0.25 = 1.52 m/s (299 ft/min)
```

**6. For minimum production time (Eq. 6.19):**
```
t_p = 3 * t_ct = 900 s
v_p = 4.064 * (60/900)^0.25 = 2.065 m/s (407 ft/min)
```

### Results for Minimum Cost

```
Machining time: t_m = (pi * 76e-3 * 300e-3) / (1.52 * 0.25e-3) = 189 s (3.15 min)
Tool life: 3070 s --> each tool produces 16 components
N_t/N_b = 0.0625

Nonproductive cost    = M * t_l           = 3.6e-3 * 120     = $0.432
Machining cost        = M * t_m           = 3.6e-3 * 189     = $0.68
Tool cost             = (N_t/N_b)*(M*t_ct + C_t) = 0.0625*(3.6e-3*300 + 2.6) = $0.23

TOTAL COST per component C_pr = $1.34
```

### Results for Minimum Production Time

```
Machining time: t_m = 139.1 s (2.32 min)
Production cost: C_pr = $1.55

Nonproductive time  = 120 s
Machining time      = 189 s (min cost) vs 139 s (min time)
Tool changing time  = 18.75 s (min cost) vs ~similar

Total production time: 328 s (5.5 min) for min cost
                      vs 309 s (5.15 min) for min time
```

### Economic Comparison

| Metric | Min Cost | Min Time |
|--------|----------|----------|
| Production cost ($/part) | $1.34 | $1.55 |
| Production time (s/part) | 328 | 309 |
| Cost increase | -- | +15.7% |
| Time reduction | -- | -5.8% |

**Practical insight:** Using minimum production time rather than minimum cost resulted in only 5.8% time reduction but 15.7% cost increase. Minimum cost is usually preferable unless demand is very high.

**Profit comparison over 1 year (7.2 x 10^6 s):**
- At $1.75/component selling price:
  - Minimum cost: profit = $9,000
  - Minimum time: profit = $4,660
- Minimum cost conditions clearly preferable unless selling price is very high

---

## 6.7 Machining at Maximum Efficiency (p.188-190)

When neither pure minimum cost nor minimum time is optimal, **maximum rate of profit** can be used as the criterion.

### Rate of Profit

```
Eq. (6.29):  P_r = (S - C_pr) / t_pr
```

Where `S` = selling price (amount received per component).

### Optimum Tool Life for Maximum Efficiency (Maximum Profit Rate)

Substituting cost and time equations and differentiating:

```
Eq. (6.31):  t_ef = (1-n)/n * (t_l + t_ct*C_t/S + C_t*K / (n*S*v_r) * (t_r/t_ef)^(1/n))
```

This equation can only be solved by **numerical iteration**. A simple method:
1. Assume initial `t_ef` equal to 6.5 s* for carbide or 2.5 s* for HSS
2. Substitute into the right side of Eq. (6.31)
3. Get new `t_ef`, repeat until convergence

**Key insight:** The condition for maximum efficiency is **independent of the machine rate M**. This is extremely practical because M is the hardest constant to estimate accurately (due to uncertainty in overheads and amortization periods).

### Relationship Between the Three Optima

From Figure 6.4 (rate of profit vs cutting speed for various selling prices S):

- When profit is zero, maximum efficiency condition equals minimum cost condition
- Unless profit is very high, the maximum profit condition lies close to the minimum cost condition
- Maximum efficiency always lies **between** minimum cost and minimum production time
- The three conditions converge as Taylor exponent n approaches 1 (ceramics)

### Figure 6.4 Parameters

Typical turning operation: M = $0.00334/s, C_t = $2.60, t_ct = 300 s, n = 0.25, t_r = 60 s, K = 328 m, t_l = 1 s, v_r = 12.2 m/s.

Shows rate of profit curves for S = $1.20 to $2.20 per component.

---

## 6.8 Facing Operations (p.191-194)

In facing operations, constant spindle speed gives **variable cutting speed** (speed changes linearly with radius). This changes the optimization.

### Tool Wear Model for Facing

```
Eq. (6.32):  (VB)_b / (VB)_w = t_m / t
```

Where:
- `(VB)_b` = flank wear-land width increase per component
- `(VB)_w` = maximum wear-land width when tool must be reground
- `t_m` = machining time per component
- `t` = tool life

```
Eq. (6.33):  (VB)_m / (d(VB)/dt') = t_r * (v_r / v)^(1/n)
```

### Instantaneous Cutting Speed in Facing

```
Eq. (6.34):  v = 2*pi*n_s*r
```

Where `n_s` = rotational frequency, `r` = instantaneous radius.

```
Eq. (6.35):  r = r_o - n_s*f*t'
```

Where `r_o` = outside radius, `f` = feed, `t'` = time.

### Key Facing Equations

After integration:

```
Eq. (6.38):  (VB)_b/(VB)_w = t_m/t = N_t/N_b = (2*pi*n_s/v_r)^(1/n) * n / (f*n_s*t_r*(n+1)) * (r_o^((n+1)/n) - r_i^((n+1)/n))
```

Machining time:
```
Eq. (6.39):  t_m = (r_o - r_i) / (n_s * f)
```

### Optimum Spindle Speed for Facing (Minimum Cost)

```
Eq. (6.40):  n_c = v_r / (2*pi*r_o) * ((1+n)/(1-n) * M*t_r / (M*t_ct + C_t) * 1 / (1 - a_r^((n+1)/n)))^n
```

Where `a_r = r_i / r_o` (ratio of inner to outer radius).

### Tool Life for Facing (Minimum Cost)

```
Eq. (6.41):  t_c = (1-n)/n * (t_ct + C_t/M)
```

**Same as for constant-speed operations!** The optimum tool life is identical.

### Optimum Spindle Speed Relation

```
Eq. (6.42):  n_s,c,p,ef = v_c,p,ef / (2*pi*r_o) * [(1 + 1/n) * (1-a_r) / (1 - a_r^((n+1)/n))]^n
```

Where `v_c,p,ef` = cutting speed for constant-speed operation corresponding to the same tool life.

As `a_r` approaches 1 (thin ring), `n_s` approaches `v / (2*pi*r_o)` (converges to constant-speed case).

Figure 6.7 shows the correction factor `2*pi*r_o*n_s / v_c` vs `a_r` for n = 0.125, 0.25, 0.5. The correction ranges from 1.0 to about 1.8 depending on n and a_r.

---

## 6.9 Operations with Interrupted Cuts (p.194-195)

All milling, shaping, and planing operations involve intermittent cutting.

**Key principle:** The tool life expressions (t_c, t_p, t_ef) still hold, but represent the time the tool is **actually cutting**. The cutting speed must be corrected for the engagement proportion Q.

```
Eq. (6.43):  v_c,p,ef = v_r * (t_r / (Q * t_c,p,ef))^n
```

### Engagement Proportion Q for Different Operations

**Slab milling (Fig. 6.8a):**
```
Eq. (6.44):  Q = theta/(2*pi) = 1/4 + 1/(2*pi) * arcsin(2*a_e/d_t - 1)
```
Where `a_e` = working engagement, `d_t` = tool diameter.

**Side milling (Fig. 6.8b):**
```
Eq. (6.45):  Q = theta/(2*pi) = 1/4 + 1/(2*pi) * arcsin(2*a_e/d_t - 1)
```

**Face milling (Fig. 6.8c):**
```
Eq. (6.46):  Q = theta/pi = 1/pi * arcsin(a_e/d_t)
```

(unless `a_e >= d_t`, when Q = 0.5)

---

## 6.10 Economics of Various Tool Materials and Tool Designs (p.195-199)

### Three Economic Comparisons

#### Comparison 1: HSS vs Brazed Carbide (Rough Turning) -- Table 6.1

| Parameter | HSS | Brazed Carbide |
|-----------|-----|----------------|
| Q (engagement proportion) | 1.0 | 1.0 |
| M ($/s) | 0.0028 | 0.0028 |
| C_t ($) | 0.30 | 2.10 |
| t_ct (s) | 240 | 240 |
| n | 0.125 | 0.25 |
| t_c (ks) | 2.43 | 2.97 |
| v_r at t_r=60s (m/s) | 0.508 | 2.73 |
| v_c (m/s) | 0.32 | 1.03 |
| K (m) | 200 | 200 |
| t_m = K/v_c (s) | 625 | 194 |
| Components per tool | 4 | 15 |
| t_l (s) | 300 | 300 |
| Tool changing time/component (s) | 60 | 16 |
| Nonproductive cost ($) | 0.84 | 0.84 |
| Tool cost/component ($) | 0.243 | 0.185 |
| Machining cost/component ($) | 1.75 | 0.543 |
| **Total production time (s)** | **985** | **510** |
| **Total cost per component ($)** | **2.83** | **1.57** |

**Insight:** Although optimum tool life is similar for both, production time with HSS is roughly **twice** that of carbide. Carbide tool costs 7x more per sharp edge but reduces total production cost by 44%.

#### Comparison 2: Brazed Carbide vs Disposable Carbide vs Disposable Ceramic (Finish Turning) -- Table 6.2

| Parameter | Brazed Carbide | Disposable Carbide | Disposable Ceramic |
|-----------|---------------|-------------------|-------------------|
| Q | 1.0 | 1.0 | 1.0 |
| M ($/s) | 0.003 | 0.003 | 0.003 |
| C_t ($) | 2.00 | 0.25 | 0.40 |
| t_ct (s) | 240 | 60 | 60 |
| n | 0.25 | 0.25 | 0.50 |
| t_c (ks) | 2.72 | 0.43 | 0.193 |
| v_r at 60s (m/s) | 6 | 6 | 50 |
| v_c (m/s) | 2.35 | 3.73 | 28.3 |
| K (m) | 1000 | 1000 | 1000 |
| t_m (s) | 432 | 273 | 35.9 |
| Components per tool | 6 | 1 | 5 |
| t_l (s) | 240 | 240 | 240 |
| Tool changing time/component (s) | 40 | 60 | 12 |
| Nonproductive cost ($) | 0.72 | 0.72 | 0.72 |
| Tool cost/component ($) | 0.453 | 0.43 | 0.116 |
| Machining cost/component ($) | 1.296 | 0.819 | 0.108 |
| **Total production time (s)** | **712** | **573** | **288** |
| **Total cost per component ($)** | **2.47** | **1.97** | **0.94** |

**Insights:**
- Disposable-insert carbide vs brazed carbide (same material): **19% less time, 20% less cost** -- primarily due to lower tool-changing time and lower sharp-tool cost
- Disposable ceramic: dramatically lower cost ($0.94 vs $2.47) due to much higher cutting speeds, but requires machine tools designed for high-speed operation
- The introduction of disposable-insert tools is "one of the most important developments in the machining process"

#### Comparison 3: Milling vs Shaping (Flat Surface 150x80mm) -- Table 6.3

| Parameter | Milling | Shaping |
|-----------|---------|---------|
| Q | 0.14 | 0.75 |
| M ($/s) | 0.004 | 0.0025 |
| C_t ($) | 20.00 | 0.50 |
| t_ct (s) | 600 | 120 |
| n | 0.125 | 0.125 |
| t_c (ks) | 39.2 | 2.24 |
| v_r (m/s) | 1.0 | 1.0 |
| v_c (m/s) | 0.57 | 0.66 |
| t_m (s) | 140.4 | 186.4 |
| Components per tool | 279 | 12 |
| t_l (s) | 120 | 120 |
| Tool changing time/component (s) | 2 | 10 |
| Nonproductive cost ($) | 0.48 | 0.300 |
| Tool cost/component ($) | 0.08 | 0.067 |
| Machining cost/component ($) | 0.562 | 0.466 |
| **Total production time (s)** | **262.4** | **316.4** |
| **Total cost per component ($)** | **2.12** | **0.833** |

**Insights:**
- Shaping is cheaper for simple flat surfaces ($0.83 vs $2.12) due to much lower tool costs and machine rate
- Milling is faster (262 vs 316 s) due to higher material removal rate
- Milling tool costs result in a long tool life (279 components per tool) since "ganged" cutters produce large batches per sharpening
- Shaping not economic for complex shapes or large batches -- it's generally only for very small batches

---

## 6.11 Machinability Data Systems (p.200)

Two types:

### 6.11.1 Data Base Systems
- Incorporate large databases of experimental data from laboratory and workshop experience
- Accessed to determine cutting parameters for specific tool-work combinations
- Include cost information as well as cutting parameters

### 6.11.2 Mathematical Model Systems
- Go further than databases: store machinability data, then determine Taylor equation constants
- Use economic/production rate equations from this chapter to compute optimum feeds and speeds
- Automated optimization for specific operations

---

## Key Formulas Summary (Quick Reference)

### Core Cost Equation
```
C_pr = M*t_l + M*K/v + (K/(v_r^(1/n) * t_r)) * (M*t_ct + C_t) * v^((1-n)/n)
```

### Optimum Tool Life
| Criterion | Formula |
|-----------|---------|
| Minimum cost | t_c = (1-n)/n * (t_ct + C_t/M) |
| Minimum time | t_p = (1-n)/n * t_ct |
| Maximum efficiency | Solve iteratively via Eq. (6.31) |

### Optimum Cutting Speed
```
v_opt = v_r * (t_r / t_opt)^n
```

### Practical Tool Life Rules of Thumb

| Tool Material | n | Min Cost Tool Life | Min Time Tool Life |
|---------------|---|-------------------|-------------------|
| HSS | 0.125 | 7*(t_ct + C_t/M) | 7*t_ct |
| Carbide | 0.25 | 3*(t_ct + C_t/M) | 3*t_ct |
| Ceramic | 0.5-0.7 | t_ct + C_t/M | t_ct |

### Typical Shop Floor Values (from examples)

| Parameter | Typical Range |
|-----------|---------------|
| Machine + operator rate M | $0.0025-0.004/s ($9-14.40/hr) |
| Tool changing time (brazed) | 240-300 s |
| Tool changing time (disposable insert) | 60 s |
| Cost of sharp brazed tool C_t | $2.00-2.60 |
| Cost of sharp disposable insert C_t | $0.25-0.50 |
| Nonproductive time t_l | 120-300 s |
| Operator overhead | 100-300% |
| Machine overhead | ~100% |
| Machine amortization | 2-10 years |
| Operator wage (1990s USD) | $5.40/hr |

---

## Key Practical Insights for Cost Estimation

1. **Feed first, speed second:** Always maximize feed before optimizing cutting speed. Feed has less effect on tool life than speed does.

2. **The (1-n)/n rule:** This single factor determines how tool life scales with tool material. HSS needs 7x longer tool life than ceramics for the same cost optimum.

3. **Minimum cost != Minimum time:** Using minimum-time conditions instead of minimum-cost typically saves only 5-6% time but increases cost by 15-16%. Almost always prefer minimum cost.

4. **Maximum efficiency is independent of M:** The rate-of-profit optimum doesn't depend on machine rate -- enormously practical since M is the hardest parameter to estimate.

5. **Disposable inserts are game-changers:** Switching from brazed to disposable carbide (same material) cuts cost by 20% and time by 19%, primarily through reduced tool-changing time.

6. **Tool cost is often the smallest component:** In most operations, nonproductive time and machining time dominate. Tool cost per component is typically $0.08-0.45.

7. **Batch size doesn't affect optimum speed:** The optimum cutting speed (Eq. 6.11) is independent of batch size N_b and nonproductive time t_l. This simplifies optimization significantly.

8. **For facing operations:** The optimum tool life is identical to constant-speed operations. Only the spindle speed calculation differs (correction factor depends on inner/outer radius ratio).

9. **Interrupted cuts (milling):** Use the same tool-life formulas but multiply by engagement proportion Q when calculating cutting speed. Q ranges from 0.14 (shallow slab milling) to 0.75 (shaping).

10. **Cost breakdown hierarchy (typical):** Machining cost > Nonproductive cost > Tool cost. Reducing machining time (via higher speeds with better tooling) has the greatest impact.

---

## References (from Chapter 6)

1. Taylor, F. W.: On the art of cutting metals, *Trans. ASME*, vol. 28, p. 31, 1906.
2. Partons, N. R., ed.: *N.C. Machinability Data Systems*, SME, Dearborn, MI, 1971.
3. Pressman, R. S., and J. E. Williams: *Numerical Control and Computer Aided Manufacturing*, Wiley, New York, 1977.
4. Groover, M. P., and E. W. Zimmers: *CAD/CAM*, Prentice-Hall, Englewood Cliffs, NJ, 1984.
