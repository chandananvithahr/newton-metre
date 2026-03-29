# Surface Treatment & Plating Process Database

> Comprehensive reference for Indian job shop surface treatment cost estimation.
> Target sectors: Defense, Aerospace, Automobile.
> All rates in INR unless noted. Rates reflect 2025-2026 Indian job shop pricing.

---

## Table of Contents

1. [Pre-Treatment Requirements](#1-pre-treatment-requirements)
2. [Electroplating Processes](#2-electroplating-processes)
3. [Anodizing Processes](#3-anodizing-processes)
4. [Chemical Conversion Coatings](#4-chemical-conversion-coatings)
5. [Thermal / Spray Coatings](#5-thermal--spray-coatings)
6. [Paint / Organic Coatings](#6-paint--organic-coatings)
7. [Vapor Deposition Coatings](#7-vapor-deposition-coatings)
8. [Mechanical Surface Treatments](#8-mechanical-surface-treatments)
9. [Cross-Cutting Cost Factors](#9-cross-cutting-cost-factors)
10. [Integration with Costimize Engine](#10-integration-with-costimize-engine)

---

## 1. Pre-Treatment Requirements

Every surface treatment requires proper pre-treatment. The cost of pre-treatment is typically 15-30% of the total finishing cost and is often the difference between a coating that lasts and one that fails.

### Standard Pre-Treatment Sequence

| Step | Process | Purpose | Time (min) | Cost Impact |
|------|---------|---------|-----------|-------------|
| 1 | Solvent degrease | Remove oils, cutting fluids | 5-15 | Included in bath cost |
| 2 | Alkaline clean (soak/electro) | Remove residual grease | 10-20 | Included |
| 3 | Water rinse (2x) | Remove cleaning chemicals | 2-5 | Included |
| 4 | Acid pickle / etch | Remove scale, oxide, activate surface | 5-30 | ₹2-5/sq.dm additional for heavy scale |
| 5 | Water rinse (2x) | Remove acid | 2-5 | Included |
| 6 | Activation dip | Final surface activation | 1-3 | Included |

### Masking Costs

| Masking Type | Cost Range | Notes |
|-------------|-----------|-------|
| Simple tape masking | ₹5-15/piece | Threads, bores |
| Wax / lacquer masking | ₹10-30/piece | Complex geometries |
| Custom silicone plugs | ₹50-200/piece (reusable) | Precision bores, first article cost higher |
| Fixture/jig masking | ₹500-5,000 one-time jig cost | High-volume production |

**Rule of thumb:** Masking adds 10-25% to per-piece surface treatment cost for typical machined parts.

---

## 2. Electroplating Processes

### 2.1 Zinc Plating

**Function:** Sacrificial corrosion protection (zinc corrodes before the base metal).

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Steel, cast iron, copper alloys |
| **Thickness range** | 5-25 um (typ. 8-12 um for general, 20-25 um for severe environments) |
| **Process time** | 20-45 min per rack (depends on thickness) |
| **Passivation types** | Clear (blue-white), Yellow (iridescent), Black, Olive drab |

#### Indian Job Shop Rates

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per kg | ₹18-35/kg | Small fasteners, bulk barrel plating |
| Per sq.dm | ₹3-8/sq.dm | Rack plating, larger parts |
| Per sq.inch | ₹0.50-1.50/sq.in | Quoted by some shops |
| Minimum batch | ₹500-1,500 | Typical minimum order charge |

**Passivation surcharges:**
- Clear (trivalent Cr): Base rate (included)
- Yellow chromate (hex Cr): +15-20% (being phased out under RoHS)
- Black passivation: +20-30%
- Olive drab: +25-35% (military spec)

#### Specifications

| Spec | Description | Industry |
|------|-------------|----------|
| ASTM B633 | Zinc plating on iron/steel | General |
| IS 1573 | Indian Standard for zinc electroplating | All India |
| QQ-Z-325 | Federal spec, zinc plating | US Defense |
| MIL-DTL-12898 | Zinc plating, barrel/rack | Defense |

#### Cost Drivers
- Hex chrome passivation requires CPCB compliance (ETP cost adds ₹2-5/kg)
- Trivalent chrome passivation slightly more expensive chemicals but lower ETP cost
- Barrel plating (small parts) is 30-50% cheaper than rack plating
- Yellow/black passivation chemicals cost more than clear

---

### 2.2 Nickel Plating

**Function:** Corrosion resistance, wear resistance, appearance (bright finish), undercoat for chrome.

#### 2.2.1 Bright Nickel (Electrolytic)

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Steel, copper, brass, zinc die-cast |
| **Thickness range** | 10-40 um (typ. 15-25 um) |
| **Process time** | 30-60 min per rack |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per kg | ₹90-150/kg | Bulk parts |
| Per sq.dm | ₹8-15/sq.dm | Rack plating |
| Per sq.inch | ₹1.25-3.00/sq.in | Small precision parts |
| Minimum batch | ₹1,000-2,500 | |

#### 2.2.2 Dull/Matte Nickel (Electrolytic)

Same rates as bright nickel. Used as undercoat or where matte finish required. Slightly cheaper chemicals (no brightener additives).

#### 2.2.3 Electroless Nickel (EN/ENP)

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Almost any metal, some plastics (with activation) |
| **Thickness range** | 5-75 um (typ. 10-25 um) |
| **Process time** | 1-4 hours (deposition rate ~10-20 um/hr) |
| **Hardness** | 48-52 HRC as-plated, 68-72 HRC after heat treat (320C) |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.dm | ₹12-25/sq.dm | Higher than electrolytic due to chemical cost |
| Per sq.inch | ₹1.40-2.50/sq.in | Chennai/Pune rates confirmed |
| Per kg | ₹150-300/kg | Complex parts priced by weight |
| Minimum batch | ₹2,000-5,000 | Chemical bath is expensive to maintain |

**Why EN costs more:** Chemical bath is auto-catalytic (no external current), gives perfectly uniform thickness even in blind holes and complex geometries. Bath chemicals (sodium hypophosphite, nickel sulfate) are expensive and deplete with use.

#### Specifications

| Spec | Description | Industry |
|------|-------------|----------|
| AMS 2404 | Electroless nickel plating | Aerospace |
| AMS 2405 | EN, low phosphorus | Aerospace (high hardness) |
| MIL-C-26074 | EN plating, military | Defense |
| ASTM B733 | EN plating, general | All |
| IS 10602 | Indian Standard, nickel plating | General |

#### Cost Drivers
- Electroless nickel is 2-3x cost of electrolytic nickel
- Bath life and turnover rate (typically 5-8 metal turnovers)
- Low-phosphorus EN (for solderability) costs ~20% more than mid-phos
- Thickness uniformity requirement drives EN over electrolytic for precision parts

---

### 2.3 Chrome Plating

#### 2.3.1 Hard Chrome

**Function:** Extreme wear resistance, low friction, corrosion resistance for hydraulic cylinders, piston rods, molds, tooling.

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Steel, stainless steel, cast iron, copper alloys |
| **Thickness range** | 20-500 um (typ. 25-75 um for wear, up to 250 um for build-up) |
| **Hardness** | 65-70 HRC |
| **Process time** | 1-8 hours (deposition rate ~25 um/hr) |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.inch | ₹0.12-4.00/sq.in | Wide range based on thickness |
| Per sq.dm | ₹8-25/sq.dm | Standard thickness (25-50 um) |
| Per kg | ₹300/kg | Quoted by some Pune shops |
| Per sq.ft | ₹2,500/sq.ft | Heavy industrial parts |
| Minimum batch | ₹2,000-5,000 | |

#### 2.3.2 Decorative Chrome

**Function:** Bright mirror finish over nickel undercoat. Thin layer for appearance only.

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Steel, copper, brass, zinc die-cast (over nickel undercoat) |
| **Thickness range** | 0.25-1.0 um (very thin, over 15-25 um nickel) |
| **Process time** | 5-15 min (chrome layer only, nickel undercoat adds 30-60 min) |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.inch | ₹2.50-5.00/sq.in | Nickel + chrome combined |
| Per sq.dm | ₹15-30/sq.dm | Combined process |
| Per kg | ₹100-150/kg | Automotive parts, handles |
| Minimum batch | ₹1,500-3,000 | |

#### Specifications

| Spec | Description | Industry |
|------|-------------|----------|
| AMS 2406 | Hard chrome plating | Aerospace |
| AMS 2460 | Hard chrome, ground finish | Aerospace |
| QQ-C-320 | Chrome plating (decorative) | Federal |
| MIL-STD-1501 | Hard chrome plating, military | Defense |
| IS 2040 | Indian Standard, chrome plating | General |

#### Cost Drivers
- Hex chrome (Cr6+) is a known carcinogen; CPCB compliance adds significant ETP cost
- Trivalent chrome (Cr3+) is gaining traction but process is harder to control
- Thick deposits (>100 um) require grinding after plating (add grinding cost)
- Environmental compliance is the single largest cost driver (30-40% of total)
- REACH restrictions in EU pushing alternatives (HVOF, EN); Indian defense still uses hex chrome

---

### 2.4 Cadmium Plating

**Function:** Superior corrosion protection, excellent lubricity, galvanic compatibility with aluminum, low electrical resistance. The gold standard for aerospace fasteners and landing gear.

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Steel, stainless steel, copper alloys |
| **Thickness range** | 5-25 um (typ. 8-13 um per QQ-P-416) |
| **Process time** | 15-40 min per rack |
| **Toxicity** | HIGHLY TOXIC -- restricted substance, phasing out globally |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.dm | ₹15-35/sq.dm | Premium due to toxicity/compliance |
| Per piece (fastener) | ₹3-15/piece | Aerospace fasteners |
| Minimum batch | ₹3,000-8,000 | Few shops left; long lead times |

#### Specifications

| Spec | Description | Industry |
|------|-------------|----------|
| QQ-P-416 (Type I, II) | Cadmium plating, federal | Defense/Aerospace |
| AMS-QQ-P-416 | Cadmium plating | Aerospace |
| MIL-DTL-12898 | Cadmium plating, military | Defense |
| LPS-03-002 | Low hydrogen embrittlement cadmium | Aerospace |

#### Cost Drivers
- Very few CPCB-approved cadmium plating shops remaining in India
- Hazardous waste disposal cost is highest of any plating process
- Hydrogen embrittlement baking mandatory (see Section 9)
- Being replaced by zinc-nickel alloy plating in many applications
- Lead time: 2-4 weeks typical (limited suppliers)

---

### 2.5 Copper Plating

**Function:** Undercoat for nickel/chrome, heat conductivity, solderability, EMI shielding.

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Steel, zinc die-cast, plastics (with activation) |
| **Thickness range** | 5-30 um (typ. 10-20 um as undercoat) |
| **Process time** | 15-40 min |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.dm | ₹5-12/sq.dm | |
| Per kg | ₹60-120/kg | |
| Minimum batch | ₹800-1,500 | |

#### Specifications

| Spec | Description |
|------|-------------|
| AMS 2418 | Copper plating (cyanide) |
| AMS 2451 | Copper plating (acid sulfate) |
| MIL-C-14550 | Copper plating, military |

#### Cost Drivers
- Cyanide copper (better adhesion) requires stricter CPCB compliance than acid copper
- Usually combined with subsequent nickel/chrome -- total system cost matters more

---

### 2.6 Tin Plating

**Function:** Solderability, corrosion resistance, food contact safety, low contact resistance.

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Steel, copper, brass |
| **Thickness range** | 5-30 um (typ. 8-15 um) |
| **Process time** | 15-30 min |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per kg | ₹90-150/kg | Confirmed IndiaMART range |
| Per sq.dm | ₹5-12/sq.dm | |
| Minimum batch | ₹800-1,500 | |

#### Specifications

| Spec | Description |
|------|-------------|
| ASTM B545 | Tin plating |
| MIL-T-10727 | Tin plating, military |
| AMS 2408 | Tin plating, aerospace |

---

### 2.7 Silver Plating

**Function:** Highest electrical/thermal conductivity of any metal, anti-galling for threaded fasteners, high-frequency RF/microwave components.

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Copper, brass, steel, stainless steel |
| **Thickness range** | 5-50 um (typ. 10-25 um for electrical, 50 um for anti-galling) |
| **Process time** | 20-60 min |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.dm | ₹25-80/sq.dm | Depends heavily on thickness and silver price |
| Per piece (connector) | ₹15-100/piece | Electronics connectors |
| Minimum batch | ₹3,000-8,000 | Silver chemical cost is high |

#### Specifications

| Spec | Description | Industry |
|------|-------------|----------|
| QQ-S-365 | Silver plating, federal | Defense |
| AMS 2410 | Silver plating | Aerospace |
| AMS 2411 | Silver plating, high purity | Aerospace |
| MIL-DTL-46089 | Silver plating, military | Defense |

#### Cost Drivers
- Silver commodity price fluctuates (₹85,000-95,000/kg in 2025-2026)
- Precious metal recovery from spent bath is critical
- Anti-tarnish coating (chromate or lacquer) adds ₹2-5/sq.dm
- Cyanide-based bath dominant; compliance cost significant

---

### 2.8 Gold Plating

**Function:** Corrosion resistance, low contact resistance, solderability, wire bonding for ICs.

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Copper, nickel (undercoat), kovar, beryllium copper |
| **Thickness range** | 0.5-5.0 um (typ. 1.0-2.5 um for connectors, 0.05-0.5 um for flash) |
| **Process time** | 5-30 min |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.dm | ₹50-300/sq.dm | Driven entirely by gold price and thickness |
| Per piece (connector) | ₹10-200/piece | Wide range by size |
| Minimum batch | ₹5,000-15,000 | Precious metal bath |

**Gold price reference:** ₹7,800-8,500/gram (2025-2026). Even thin deposits are expensive.

#### Specifications

| Spec | Description | Industry |
|------|-------------|----------|
| MIL-G-45204 | Gold plating, military/aerospace | Defense/Aerospace |
| AMS 2422 | Gold plating | Aerospace |
| ASTM B488 | Gold plating, general | Electronics |

#### Cost Drivers
- Gold commodity price is the dominant factor
- Selective plating (masking) to minimize gold usage is critical
- Nickel undercoat (2-5 um) required -- adds to total cost
- Gold thickness specification tolerance is tight (+/-10%)

---

### 2.9 Rhodium Plating

**Function:** Extreme hardness, tarnish resistance, high reflectivity. Used on precision optical components, electrical contacts, jewelry.

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Nickel (undercoat), silver, gold, platinum group metals |
| **Thickness range** | 0.25-2.5 um (very thin deposits) |
| **Process time** | 5-20 min |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per gram (metal) | ₹20-22/gram | IndiaMART confirmed |
| Per piece (jewelry) | ₹50-500/piece | Depends on size |
| Per sq.dm | ₹80-400/sq.dm | Industrial components |
| Minimum batch | ₹5,000-10,000 | |

**Rhodium price reference:** ~₹400,000-500,000/troy oz (extremely volatile). Most expensive plating metal.

#### Specifications

| Spec | Description |
|------|-------------|
| AMS 2413 | Rhodium plating |
| ASTM B634 | Rhodium plating |

---

## 3. Anodizing Processes

Anodizing is an electrolytic process that grows a protective oxide layer INTO the aluminum surface (not deposited on top). Only applicable to aluminum and titanium alloys.

### 3.1 Type I -- Chromic Acid Anodizing

**Function:** Thin, soft oxide for aerospace structural parts. Minimal dimensional change. Best fatigue life retention.

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Aluminum alloys (2xxx, 5xxx, 6xxx, 7xxx series) |
| **Thickness range** | 0.5-7.5 um (typ. 2.5-5.0 um) |
| **Process time** | 30-60 min |
| **Dimensional change** | ~50% penetration into surface, ~50% growth |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.dm | ₹8-18/sq.dm | Limited availability in India |
| Per piece (small) | ₹50-200/piece | Aerospace parts |
| Minimum batch | ₹2,000-5,000 | |

#### Specifications

| Spec | Description | Industry |
|------|-------------|----------|
| MIL-A-8625 Type I | Chromic acid anodizing | Aerospace/Defense |
| MIL-A-8625 Type IB | Non-chromic acid substitute | Aerospace |

#### Cost Drivers
- Uses hexavalent chromium (CPCB restricted)
- Very few qualified shops in India (Bangalore, Hyderabad clusters)
- Being replaced by Type IB (non-chromic) or Type II (sulfuric) where possible
- Aerospace qualification (Nadcap) adds significant overhead
- Lead time: 1-3 weeks

---

### 3.2 Type II -- Sulfuric Acid Anodizing

**Function:** General-purpose corrosion protection and paint adhesion base. Most common anodizing process.

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Aluminum alloys (all series, best on 5xxx/6xxx) |
| **Thickness range** | 5-25 um (typ. 10-18 um) |
| **Process time** | 20-60 min (depends on thickness) |
| **Dimensional change** | ~67% penetration, ~33% growth |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.dm | ₹5-12/sq.dm | Most competitive pricing |
| Per piece (small-medium) | ₹20-150/piece | |
| Per kg | ₹80-200/kg | Some shops price by weight |
| Minimum batch | ₹1,000-2,500 | |

**Bangalore reference:** 3 components (64x62x75mm) anodized for Rs. 150/set (confirmed quote).

#### Specifications

| Spec | Description | Industry |
|------|-------------|----------|
| MIL-A-8625 Type II, Class 1 | Clear anodize | Aerospace/Defense |
| MIL-A-8625 Type II, Class 2 | Dyed (colored) anodize | Aerospace/Defense |
| IS 6005 | Indian Standard, anodizing | General |
| AMS 2471 | Sulfuric acid anodizing | Aerospace |

---

### 3.3 Type III -- Hard Anodizing

**Function:** Extreme wear resistance, electrical insulation, thermal barrier. Replaces hard chrome in many applications.

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Aluminum alloys (best on 6061, 7075; poor on high-Si casting alloys) |
| **Thickness range** | 25-100 um (typ. 50-75 um) |
| **Hardness** | 60-70 HRC equivalent |
| **Process time** | 1-4 hours |
| **Dimensional change** | ~50% penetration, ~50% growth |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.dm | ₹12-35/sq.dm | 2-3x cost of Type II |
| Per piece | ₹100-500/piece | Depends on size |
| Minimum batch | ₹2,500-5,000 | |

**International reference:** $2.30-3.70/sq.ft (~₹190-310/sq.ft) for MIL-spec Type III.

#### Specifications

| Spec | Description | Industry |
|------|-------------|----------|
| MIL-A-8625 Type III | Hard anodizing | Aerospace/Defense |
| AMS 2469 | Hard anodize, sealed | Aerospace |
| MIL-A-8625 Type III, Class 1 | Non-dyed hard anodize | Defense |

#### Cost Drivers
- Requires refrigerated electrolyte (0-5 deg C) -- high energy cost
- Slow deposition rate means long tank time
- Fixturing/racking is critical -- poor contact = burn marks
- MIL-spec testing (salt spray, hardness, thickness) adds 20-30% to cost
- True MIL-spec Type III can be 10x cost of non-spec Type II

---

### 3.4 Color Anodizing

Type II anodize with organic or inorganic dyes added during the porous oxide stage before sealing.

| Parameter | Value |
|-----------|-------|
| **Colors available** | Black, red, blue, green, gold, purple, orange |
| **Surcharge over clear** | +20-40% for standard colors, +50-80% for custom/matched colors |
| **UV stability** | Organic dyes fade; inorganic (black, gold) most stable |

| Pricing Basis | Rate Range |
|--------------|-----------|
| Per sq.dm | ₹8-18/sq.dm (standard black), ₹12-25/sq.dm (custom color) |

#### Specifications
- MIL-A-8625 Type II, Class 2 (dyed)

---

### 3.5 PTFE-Infused Anodizing

Hard anodize with PTFE (Teflon) particles co-deposited or infused into porous oxide before sealing.

| Parameter | Value |
|-----------|-------|
| **Function** | Low friction + wear resistance (COF ~0.15 vs 0.4 for plain hard anodize) |
| **Applicable materials** | Aluminum alloys |
| **Thickness range** | 25-50 um |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.dm | ₹20-50/sq.dm | Premium over standard hard anodize |
| Minimum batch | ₹5,000-10,000 | Specialized process |

**Proprietary brands:** Tufram, Magnaplate (licensed processes -- limited India availability).

---

## 4. Chemical Conversion Coatings

### 4.1 Chromate Conversion (Alodine/Iridite)

**Function:** Corrosion protection on aluminum without dimensional change. Excellent paint adhesion primer. Electrically conductive (unlike anodize).

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Aluminum alloys, zinc, cadmium, magnesium |
| **Thickness range** | 0.025-1.0 um (essentially zero dimensional change) |
| **Process time** | 1-5 min immersion |
| **Conductivity** | Conductive (key advantage over anodize) |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.dm | ₹2-6/sq.dm | Very cheap process |
| Per piece (small) | ₹5-25/piece | |
| Per batch (dip tank) | ₹500-1,500/batch | Most economical for bulk |
| Minimum batch | ₹500-1,000 | |

#### Specifications

| Spec | Description | Industry |
|------|-------------|----------|
| MIL-DTL-5541 Type I | Hex chrome (gold/iridescent) | Defense/Aerospace |
| MIL-DTL-5541 Type II | Non-hex chrome (clear) -- RoHS compliant | Aerospace |
| AMS 2473 | Chromate conversion | Aerospace |
| AMS 2474 | Non-chromate conversion | Aerospace |

#### Cost Drivers
- Type I (hex chrome) is cheapest but environmentally restricted
- Type II (trivalent/non-chrome) is 30-50% more expensive (newer chemistry)
- Touch-up pens available for field repair (Alodine 1132)
- Shelf life of coating: 7 days before painting (per MIL-DTL-5541)

---

### 4.2 Phosphating

**Function:** Corrosion inhibitor, paint adhesion base, anti-galling for sliding surfaces, break-in lubricant.

#### 4.2.1 Zinc Phosphate

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Steel, cast iron |
| **Thickness range** | 5-15 um (coating weight 4-10 g/sq.m) |
| **Process time** | 5-15 min |
| **Use case** | Pre-paint treatment (most common in automobile) |

| Pricing Basis | Rate Range |
|--------------|-----------|
| Per sq.dm | ₹1.5-4/sq.dm |
| Per kg | ₹12-25/kg |
| Per batch (spray/dip) | ₹300-800/batch |

#### 4.2.2 Manganese Phosphate (Parkerizing)

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Steel, cast iron |
| **Thickness range** | 10-25 um (coating weight 10-30 g/sq.m) |
| **Process time** | 15-30 min at 95-100 deg C |
| **Use case** | Military firearms, gears, engine cylinders. Anti-galling, oil retention |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.dm | ₹3-8/sq.dm | |
| Per kg | ₹20-40/kg | |
| Per piece (gear/weapon) | ₹30-150/piece | |
| Minimum batch | ₹800-2,000 | |

#### 4.2.3 Iron Phosphate

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Steel |
| **Thickness range** | 0.5-1.5 um (lightest phosphate) |
| **Process time** | 3-5 min (spray application) |
| **Use case** | Pre-paint treatment, lowest cost phosphate |

| Pricing Basis | Rate Range |
|--------------|-----------|
| Per sq.dm | ₹1-2.5/sq.dm |
| Per batch (spray) | ₹200-500/batch |

#### Specifications (All Phosphating)

| Spec | Description | Industry |
|------|-------------|----------|
| MIL-DTL-16232 | Phosphate coating, military | Defense |
| TT-C-490 | Zinc phosphate coating | Federal |
| IS 6005 | Indian Standard, phosphate coating | General |
| DOD-P-16232 | Manganese phosphate | Defense (firearms) |

---

### 4.3 Black Oxide

**Function:** Mild corrosion resistance (with oil), appearance (uniform black), dimensional stability (no build-up).

#### 4.3.1 Hot Black Oxide

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Steel, stainless steel, copper |
| **Thickness range** | 0.5-2.5 um (magnetite Fe3O4 conversion) |
| **Process time** | 15-30 min at 140-150 deg C (hot alkaline bath) |
| **Corrosion resistance** | Poor alone; must be oiled or waxed |

| Pricing Basis | Rate Range |
|--------------|-----------|
| Per kg | ₹15-30/kg |
| Per sq.dm | ₹2-5/sq.dm |
| Minimum batch | ₹500-1,200 |

#### 4.3.2 Cold Black Oxide

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Steel |
| **Thickness range** | Deposited film (~1 um, not true conversion) |
| **Process time** | 5-10 min at room temperature |
| **Corrosion resistance** | Lower than hot process |

| Pricing Basis | Rate Range |
|--------------|-----------|
| Per kg | ₹10-20/kg |
| Per sq.dm | ₹1.5-3.5/sq.dm |

#### Specifications

| Spec | Description |
|------|-------------|
| MIL-DTL-13924 | Black oxide, military (Class 1: hot, Class 4: cold) |
| AMS 2485 | Black oxide, aerospace |

---

### 4.4 Passivation (Stainless Steel)

**Function:** Removes free iron from stainless steel surface, restores/enhances chromium oxide passive layer. NOT a coating -- it is surface chemistry restoration.

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | All stainless steel grades (300 series, 400 series, PH grades) |
| **Thickness range** | No measurable thickness change |
| **Process time** | 20-60 min immersion |

#### 4.4.1 Nitric Acid Passivation

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.dm | ₹2-6/sq.dm | Traditional method |
| Per kg | ₹15-35/kg | |
| Per batch | ₹500-1,500/batch | |

#### 4.4.2 Citric Acid Passivation

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.dm | ₹2.5-7/sq.dm | Slightly more expensive chemical but safer |
| Per kg | ₹18-40/kg | |

**Citric acid advantages:** Non-hazardous waste, no NOx fumes, RoHS compliant. Increasingly preferred.

#### Specifications

| Spec | Description | Industry |
|------|-------------|----------|
| ASTM A967 | Passivation of stainless steel | General |
| AMS 2700 | Passivation, aerospace | Aerospace |
| QQ-P-35 | Passivation, federal | Defense |
| ASTM A380 | Cleaning/descaling stainless | General |

---

## 5. Thermal / Spray Coatings

### 5.1 HVOF (High Velocity Oxy-Fuel)

**Function:** Extremely dense, hard coatings for wear/corrosion. Replaces hard chrome in many aerospace applications.

| Parameter | Value |
|-----------|-------|
| **Applicable materials (substrate)** | Steel, stainless steel, nickel alloys, titanium |
| **Coating materials** | WC-Co, WC-CoCr, Cr3C2-NiCr, Inconel, Stellite |
| **Thickness range** | 50-500 um (typ. 100-300 um) |
| **Hardness** | 1100-1400 Hv (WC-Co) |
| **Bond strength** | >70 MPa |
| **Process time** | 30 min - 4 hours (depends on area and thickness) |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.dm | ₹80-300/sq.dm | Depends on coating material |
| Per sq.meter | ₹8,000-30,000/sq.m | Large area parts |
| Per piece (shaft sleeve) | ₹2,000-15,000/piece | Landing gear, hydraulic rods |
| Minimum batch | ₹5,000-15,000 | Setup is expensive |

**Indian service providers:** Plasmatron (Mumbai), Plasma Spray India (Bangalore), Alloy Thermal Spray (Pune/Mumbai).

#### Specifications

| Spec | Description | Industry |
|------|-------------|----------|
| AMS 2447 | HVOF coating | Aerospace |
| AMS 2448 | WC-Co HVOF | Aerospace |
| MIL-STD-1687 | Thermal spray requirements | Defense |

#### Cost Drivers
- Powder material cost is dominant (WC-Co powder: ₹8,000-15,000/kg)
- Deposition efficiency: only 40-60% of powder bonds to part (rest is overspray)
- Post-spray grinding/lapping required for precision parts
- Equipment cost is very high (~₹1-3 Cr per HVOF gun system)
- Few qualified shops in India (Pune, Mumbai, Bangalore, Hyderabad clusters)

---

### 5.2 Plasma Spray

**Function:** Versatile coating for thermal barriers, wear resistance, electrical insulation.

| Parameter | Value |
|-----------|-------|
| **Applicable materials (substrate)** | Most metals and some ceramics |
| **Coating materials** | Al2O3, ZrO2-Y2O3 (TBC), Cr2O3, NiCrAlY, Metco 447 |
| **Thickness range** | 50-1000 um (typ. 100-500 um) |
| **Bond strength** | 20-40 MPa (lower than HVOF) |
| **Process time** | 30 min - 4 hours |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.dm | ₹50-200/sq.dm | |
| Per sq.meter | ₹5,000-20,000/sq.m | |
| Minimum batch | ₹5,000-10,000 | |

#### Specifications

| Spec | Description | Industry |
|------|-------------|----------|
| AMS 2437 | Plasma spray coating | Aerospace |
| AMS 2447 | Thermal spray | Aerospace |

---

### 5.3 Flame Spray

**Function:** Lower-cost thermal spray for corrosion protection and dimensional restoration.

| Parameter | Value |
|-----------|-------|
| **Coating materials** | Zinc, aluminum, stainless steel wires; NiCr, bronze |
| **Thickness range** | 100-2000 um |
| **Bond strength** | 10-30 MPa (lowest of spray methods) |
| **Process time** | 15 min - 2 hours |

| Pricing Basis | Rate Range |
|--------------|-----------|
| Per sq.dm | ₹30-100/sq.dm |
| Per sq.meter | ₹3,000-10,000/sq.m |
| Minimum batch | ₹3,000-8,000 |

---

### 5.4 Cold Spray

**Function:** Low-temperature deposition (no melting). Ideal for oxygen-sensitive materials (titanium, aluminum). Dimensional restoration without heat-affected zone.

| Parameter | Value |
|-----------|-------|
| **Coating materials** | Cu, Al, Ti, Ta, Ni, Inconel |
| **Thickness range** | 100-5000 um (can build up thick deposits) |
| **Process time** | Variable -- depends on build-up volume |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per piece | ₹5,000-50,000/piece | Highly specialized |
| Minimum batch | ₹10,000-25,000 | Very few providers in India |

**Note:** Cold spray is still emerging in India. Limited to defense R&D labs (DMRL Hyderabad, NAL Bangalore) and a few private facilities.

---

### 5.5 Thermal Barrier Coatings (TBC)

**Function:** Insulate turbine blades/combustion components from extreme heat. Multi-layer system: metallic bond coat + ceramic top coat.

| Parameter | Value |
|-----------|-------|
| **System** | MCrAlY bond coat (100-150 um) + YSZ top coat (250-500 um) |
| **Operating temperature** | Up to 1200 deg C |
| **Process** | Plasma spray or EB-PVD (for turbine blades) |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per blade (turbine) | ₹5,000-50,000/blade | Depends on size |
| Per sq.dm | ₹150-500/sq.dm | Complete TBC system |
| Minimum batch | ₹15,000-50,000 | |

**Note:** TBC application is essentially limited to HAL (Bangalore), GTRE (Bangalore), and a handful of Nadcap-certified private shops in India.

---

## 6. Paint / Organic Coatings

### 6.1 Powder Coating

**Function:** Durable, thick finish for corrosion protection and appearance. No solvents (environmentally friendly).

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Steel, aluminum, cast iron (any conductive substrate) |
| **Thickness range** | 40-120 um (typ. 60-80 um) |
| **Process** | Electrostatic spray + oven cure (180-200 deg C, 10-20 min) |

#### Powder Types

| Type | Properties | Cost Factor |
|------|-----------|-------------|
| Epoxy | Best corrosion, poor UV | 1.0x (base) |
| Polyester | Good UV, good corrosion | 1.1x |
| Hybrid (epoxy-polyester) | Balanced indoor/outdoor | 1.05x |
| Polyurethane | Premium UV + chemical resistance | 1.5x |
| Fluoropolymer (PVDF) | Architectural, 20-year warranty | 2.5x |

#### Indian Job Shop Rates

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.m (material only) | ₹26-50/sq.m | Powder cost at 60-80 um |
| Per sq.ft (service) | ₹15-50/sq.ft | IndiaMART range (includes labor) |
| Per kg (of part) | ₹25-60/kg | Small/medium parts |
| Per piece (furniture/frame) | ₹50-500/piece | |
| Minimum batch | ₹500-1,500 | |

#### Specifications

| Spec | Description | Industry |
|------|-------------|----------|
| IS 14927 | Indian Standard, powder coating | General |
| ASTM D3451 | Powder coating testing | General |

#### Cost Drivers
- Powder recovery (booth efficiency): 60-95% with reclaim
- Oven size limits part size
- Pre-treatment (zinc phosphate or iron phosphate) is mandatory -- adds ₹5-15/sq.m
- Color change = booth cleaning time (single-color lines are cheapest)

---

### 6.2 E-Coat (Cathodic Electrodeposition)

**Function:** Uniform thin coating in every recess, crevice, and tube interior. Primary primer for automotive bodies.

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Steel, aluminum, zinc (conductive substrates) |
| **Thickness range** | 15-35 um (self-limiting, very uniform) |
| **Process** | Electrophoretic dip (cathodic), 200 deg C bake |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.ft | ₹15-50/sq.ft | IndiaMART confirmed |
| Per sq.m | ₹160-540/sq.m | |
| Per kg | ₹20-50/kg | Automotive components |
| Minimum batch | ₹1,000-3,000 | |

#### Specifications

| Spec | Description |
|------|-------------|
| IS 14928 | Indian Standard, cathodic electrocoating |

#### Cost Drivers
- Capital-intensive (dip tanks, power supply, ultrafiltration, DI water system)
- Bath chemistry maintenance is ongoing cost
- Best economics at high volume (auto OEM, not job shop)
- Job shop e-coat is available but limited (mainly Mumbai, Pune, Chennai clusters)

---

### 6.3 Wet Paint (Primer + Topcoat Systems)

**Function:** Versatile coating system for any substrate, any environment. Multi-coat systems for maximum protection.

#### Common Systems

| System | Layers | Total DFT | Use Case |
|--------|--------|----------|----------|
| Primer + enamel | 2 coats | 50-80 um | General industrial |
| Primer + PU topcoat | 2 coats | 60-100 um | Outdoor equipment |
| Zinc-rich primer + epoxy MIO + PU topcoat | 3 coats | 200-350 um | Marine, heavy industrial |
| Wash primer + epoxy primer + topcoat | 3 coats | 100-150 um | Aerospace structural |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.m (2-coat) | ₹150-400/sq.m | Includes material + labor |
| Per sq.m (3-coat marine) | ₹400-1,000/sq.m | |
| Per kg (small parts) | ₹30-80/kg | |
| Minimum batch | ₹500-2,000 | |

---

### 6.4 CARC (Chemical Agent Resistant Coating)

**Function:** Military topcoat that can be decontaminated of chemical warfare agents (mustard gas, nerve agents) without coating damage.

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Steel, aluminum (over primer) |
| **System** | CARC primer (MIL-DTL-53022) + CARC topcoat (MIL-DTL-64159) |
| **Total DFT** | 50-100 um (primer 25-50 um + topcoat 25-50 um) |
| **Colors** | OD Green 383, Desert Tan 686A, Woodland camouflage |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.m | ₹500-1,500/sq.m | Specialized military paint |
| Per vehicle (combat) | ₹50,000-200,000/vehicle | Full CARC system |
| Minimum batch | ₹5,000-15,000 | |

#### Specifications

| Spec | Description |
|------|-------------|
| MIL-DTL-53022 | CARC primer |
| MIL-DTL-64159 | CARC topcoat (water-reducible) |
| MIL-DTL-53039 | CARC touch-up |

#### Cost Drivers
- Restricted material (isocyanate hardener requires safety controls)
- Application requires HVLP or airless spray in controlled environment
- Multi-color camouflage patterns require masking (labor-intensive)
- Limited to defense-certified painters in India

---

### 6.5 Primer Systems

| Primer Type | Function | Spec | Rate (₹/sq.m) |
|-------------|---------|------|---------------|
| Zinc chromate primer | Corrosion inhibitor for aluminum | MIL-PRF-23377 | ₹80-150/sq.m |
| Epoxy primer (2-pack) | General purpose, excellent adhesion | MIL-PRF-23377 Type I | ₹100-200/sq.m |
| Wash primer (etch primer) | Thin adhesion promoter for bare metal | MIL-DTL-15328 | ₹50-100/sq.m |
| Zinc-rich primer | Sacrificial protection for steel | SSPC Paint 20 | ₹120-250/sq.m |
| Epoxy MIO (micaceous iron oxide) | Barrier coat, intermediate | IS 2074 | ₹100-200/sq.m |

---

## 7. Vapor Deposition Coatings

### 7.1 PVD (Physical Vapor Deposition)

**Function:** Extremely thin, hard coatings for wear resistance, low friction, decorative finishes.

| Parameter | Value |
|-----------|-------|
| **Applicable materials (substrate)** | Steel, stainless steel, titanium, carbide, ceramics |
| **Coating types** | TiN (gold), TiCN (blue-gray), TiAlN (violet), CrN (silver), ZrN (brass) |
| **Thickness range** | 1-5 um |
| **Hardness** | 2000-3500 Hv |
| **Process temperature** | 200-500 deg C |
| **Process time** | 2-8 hours per batch |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per piece (cutting tool) | ₹20-200/piece | High volume |
| Per piece (component) | ₹100-2,000/piece | Depends on size |
| Per batch | ₹5,000-25,000/batch | Chamber size dependent |
| Minimum batch | ₹5,000-10,000 | |

**PVD is typically 2-3x cost of conventional plating/nitriding.**

#### Specifications

| Spec | Description |
|------|-------------|
| VDI 3198 | PVD coating adhesion test |

**Indian providers:** ARKA PVD (multiple locations), Oerlikon Balzers (Pune), IHI Ionbond (Pune).

#### Cost Drivers
- Capital equipment cost (₹5-15 Cr per PVD chamber)
- Batch process = chamber utilization is key to per-piece cost
- Masking is difficult (vacuum environment)
- Pre-treatment (ultra-clean surface) is critical

---

### 7.2 CVD (Chemical Vapor Deposition)

**Function:** Thicker, harder coatings than PVD. Conformal coating of complex geometries.

| Parameter | Value |
|-----------|-------|
| **Coating types** | TiC, TiN, Al2O3, diamond (polycrystalline) |
| **Thickness range** | 5-20 um |
| **Hardness** | 2500-10,000 Hv (diamond) |
| **Process temperature** | 800-1100 deg C (limits substrate choices) |
| **Process time** | 4-12 hours per batch |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per piece (cutting insert) | ₹30-300/piece | |
| Per batch | ₹10,000-50,000/batch | |
| Minimum batch | ₹10,000-20,000 | |

#### Cost Drivers
- High temperature limits to HSS and cemented carbide substrates
- Cannot coat finished/hardened steel (tempering would occur)
- Longer cycle time than PVD
- Very limited job shop availability in India (primarily captive lines at tool manufacturers)

---

### 7.3 DLC (Diamond-Like Carbon)

**Function:** Ultra-low friction (COF 0.05-0.15), high hardness, chemical inertness. Ideal for sliding components, medical devices, engine parts.

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Steel, stainless steel, titanium, aluminum (with interlayer) |
| **Thickness range** | 1-5 um |
| **Hardness** | 2000-8000 Hv (depending on sp3 content) |
| **Process temperature** | 80-250 deg C |
| **Friction coefficient** | 0.05-0.15 |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per piece (piston ring) | ₹50-500/piece | High-volume automotive |
| Per piece (component) | ₹200-5,000/piece | |
| Per batch | ₹10,000-50,000/batch | |
| Minimum batch | ₹10,000-25,000 | |

**DLC is ~3-5x cost of standard PVD coatings.**

#### Specifications

| Spec | Description |
|------|-------------|
| VDI 2840 | Classification of DLC coatings |
| ISO 26443 | DLC coating characterization |

---

## 8. Mechanical Surface Treatments

### 8.1 Shot Peening

**Function:** Introduces compressive residual stress to increase fatigue life. Mandatory for aerospace springs, gears, turbine blades.

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Steel, stainless steel, titanium, aluminum |
| **Media** | Steel shot (S110-S780), ceramic beads, glass beads |
| **Intensity** | 0.004A-0.024A Almen (per AMS 2430) |
| **Coverage** | 100-200% per AMS 2430 |
| **Process time** | 5-30 min per batch |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per kg | ₹15-40/kg | Bulk parts |
| Per piece (gear/spring) | ₹10-100/piece | |
| Per batch | ₹500-3,000/batch | |
| Minimum batch | ₹500-1,500 | |

#### Specifications

| Spec | Description | Industry |
|------|-------------|----------|
| AMS 2430 | Shot peening | Aerospace |
| AMS-S-13165 | Shot peening, controlled | Aerospace |
| MIL-S-13165 | Shot peening, military | Defense |

---

### 8.2 Shot Blasting / Sandblasting

**Function:** Surface cleaning, scale removal, surface profile for paint/coating adhesion.

| Parameter | Value |
|-----------|-------|
| **Media** | Steel grit (G25-G80), aluminum oxide (36-120 mesh), garnet |
| **Surface profile** | Sa 2.5 to Sa 3 (per ISO 8501) |
| **Process time** | 5-30 min per piece (depends on size) |

| Pricing Basis | Rate Range |
|--------------|-----------|
| Per kg | ₹5-15/kg |
| Per sq.m | ₹50-150/sq.m |
| Per piece | ₹20-200/piece |
| Minimum batch | ₹300-800 |

---

### 8.3 Bead Blasting

**Function:** Uniform matte/satin finish, cosmetic surface preparation. Gentler than sandblasting.

| Parameter | Value |
|-----------|-------|
| **Media** | Glass beads (60-325 mesh) |
| **Surface finish** | 0.8-3.2 Ra um |
| **Process time** | 5-20 min per piece |

| Pricing Basis | Rate Range |
|--------------|-----------|
| Per piece (small-medium) | ₹10-100/piece |
| Per sq.dm | ₹3-8/sq.dm |
| Minimum batch | ₹300-800 |

---

### 8.4 Electropolishing

**Function:** Electrolytic material removal to produce mirror finish, remove micro-burrs, passivate surface. Reverse of electroplating.

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Stainless steel (primary), aluminum, copper, titanium |
| **Material removal** | 10-50 um |
| **Surface finish** | 0.1-0.4 Ra um achievable |
| **Process time** | 5-30 min |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per sq.dm | ₹8-20/sq.dm | |
| Per piece (pharmaceutical/food) | ₹50-500/piece | |
| Minimum batch | ₹1,500-4,000 | |

#### Specifications

| Spec | Description |
|------|-------------|
| ASTM B912 | Electropolishing of stainless steel |
| ASME BPE | Bioprocessing equipment (pharma) |

---

### 8.5 Tumble / Vibratory Deburring

**Function:** Mass finishing for deburring, edge radiusing, surface smoothing, cleaning.

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | All metals, plastics |
| **Media** | Ceramic (aggressive), plastic (gentle), steel (burnishing) |
| **Process time** | 30 min - 8 hours (depends on finish required) |

| Pricing Basis | Rate Range |
|--------------|-----------|
| Per kg | ₹8-25/kg |
| Per piece (small) | ₹2-15/piece |
| Per batch (drum/tub load) | ₹500-2,000/batch |
| Minimum batch | ₹300-800 |

---

### 8.6 Burnishing (Roller/Ball)

**Function:** Cold-working the surface to produce a mirror finish, compressive stress, and improved fatigue life. No material removal.

| Parameter | Value |
|-----------|-------|
| **Applicable materials** | Steel, stainless steel, aluminum, brass |
| **Surface finish** | 0.05-0.4 Ra um |
| **Process time** | Same as turning (done on lathe/mill) |

| Pricing Basis | Rate Range | Notes |
|--------------|-----------|-------|
| Per piece | ₹20-200/piece | Tool-based, priced as machining operation |
| Per linear meter (bore/OD) | ₹50-200/m | |

**Note:** Burnishing is typically quoted as a machining operation, not a surface treatment.

---

## 9. Cross-Cutting Cost Factors

### 9.1 Hydrogen Embrittlement Relief (Baking)

**CRITICAL for high-strength steel parts (>1000 MPa / >31 HRC) that undergo any acid cleaning, pickling, or electroplating.**

| Parameter | Value |
|-----------|-------|
| **Temperature** | 190 +/- 14 deg C (375 +/- 25 deg F) |
| **Time** | 3-23 hours (depends on spec and steel strength) |
| **Timing** | MUST begin within 1-4 hours of plating (per AMS 2759) |

| Steel Strength | Baking Time | Standard |
|---------------|------------|---------|
| 1000-1200 MPa | 3 hours minimum | AMS 2759 |
| 1200-1400 MPa | 8 hours minimum | AMS 2759 |
| >1400 MPa | 12-23 hours minimum | AMS 2759/AMS 2406 |

| Pricing | Rate |
|---------|------|
| Per batch (oven load) | ₹500-2,000 |
| Per kg | ₹10-25/kg |

**Processes that require H.E. baking:** All electroplating (zinc, cadmium, chrome, nickel), acid pickling, phosphating (acid-based). NOT required for: anodizing (aluminum), passivation (stainless steel), powder coating.

#### Specifications

| Spec | Description |
|------|-------------|
| AMS 2759/9 | Hydrogen embrittlement relief for steel |
| ASTM F519 | Testing for hydrogen embrittlement |
| ASTM B849 | Pre-plating stress relief |
| ASTM B850 | Post-plating H.E. relief |

---

### 9.2 Batch Size Economics

| Batch Size | Price Impact | Notes |
|-----------|-------------|-------|
| 1-5 pieces | 100% (base rate + minimum charge applies) | Prototyping |
| 6-25 pieces | 70-85% | Small batch |
| 26-100 pieces | 50-65% | Medium batch |
| 101-500 pieces | 40-55% | Standard production |
| 500+ pieces | 30-45% | Volume pricing |
| 5000+ pieces | 25-35% | Mass production (barrel plating eligible) |

**Minimum batch charges (typical):**
- Simple processes (zinc, black oxide): ₹500-1,500
- Medium processes (nickel, chrome, anodize): ₹1,500-5,000
- Complex processes (cadmium, silver, gold, HVOF): ₹5,000-25,000

---

### 9.3 Lead Times (Indian Job Shops)

| Process Category | Standard Lead Time | Rush Surcharge |
|-----------------|-------------------|----------------|
| Zinc/black oxide/phosphating | 2-5 days | +25-50% for same-day |
| Nickel/chrome (electrolytic) | 3-7 days | +30-50% |
| Hard chrome | 5-10 days | +40-60% |
| Anodizing (Type II) | 3-7 days | +25-50% |
| Hard anodizing (Type III) | 5-12 days | +40-60% |
| Electroless nickel | 5-10 days | +30-50% |
| Cadmium plating | 10-20 days | Limited rush availability |
| Precious metal (Ag/Au) | 7-15 days | +50-75% |
| HVOF/plasma spray | 7-15 days | +50-100% |
| PVD/DLC | 7-15 days | +50-75% |
| Powder coating | 2-5 days | +25-40% |
| Wet paint (multi-coat) | 3-10 days | +30-50% |
| CARC (military) | 10-21 days | Limited |

---

### 9.4 Environmental Regulations (India)

#### CPCB (Central Pollution Control Board) Requirements

All electroplating shops must comply with:
- **Consent to Establish (CTE)** and **Consent to Operate (CTO)** from State Pollution Control Board (SPCB)
- **Effluent Treatment Plant (ETP)** mandatory for all plating shops
- **Hazardous Waste Authorization** under Hazardous and Other Wastes (Management and Transboundary Movement) Rules, 2016 (amended 2024)

#### Effluent Limits (Selected)

| Parameter | Discharge Limit |
|-----------|----------------|
| Hexavalent chromium (Cr6+) | 0.1 mg/L |
| Total chromium | 2.0 mg/L |
| Nickel | 3.0 mg/L |
| Zinc | 5.0 mg/L |
| Cadmium | 0.1 mg/L |
| Cyanide | 0.2 mg/L |
| pH | 6.0-9.0 |

#### Cost Impact of Environmental Compliance

| Item | Estimated Cost |
|------|---------------|
| ETP installation (small shop) | ₹5-15 lakh |
| ETP operation (monthly) | ₹15,000-50,000/month |
| Hazardous waste disposal (sludge) | ₹8,000-15,000/ton |
| SPCB annual renewal | ₹5,000-25,000/year |
| Environmental compensation (violation) | ₹1-50 lakh |

**These costs are embedded in plating rates.** Shops that cut corners on ETP offer lower rates but face shutdown risk. Prefer CPCB-compliant shops for defense/aerospace work.

---

### 9.5 RoHS/REACH Compliance Impact

| Restricted Substance | Affected Processes | Compliant Alternative | Cost Impact |
|---------------------|-------------------|---------------------|-------------|
| Hexavalent chromium (Cr6+) | Chrome plating, chromate conversion, zinc yellow passivation | Trivalent chrome, non-chrome conversion | +20-50% |
| Cadmium | Cadmium plating | Zinc-nickel alloy plating | +30-60% |
| Lead | Tin-lead solder plate | Pure tin or tin-silver | +10-20% |

**Note:** Indian defense procurement (DRDO, OFB, DPSUs) does NOT mandate RoHS compliance as of 2025-2026. However, export-oriented defense production and commercial aerospace (Boeing, Airbus supply chain) require full RoHS/REACH compliance.

---

## 10. Integration with Costimize Engine

### Current State (config.py)

The existing config.py has three surface treatment categories:
```
surface_treatment_plating:   ₹400/hr
surface_treatment_anodizing: ₹450/hr
surface_treatment_painting:  ₹300/hr
```

### Recommended Expansion

Replace the three generic categories with granular process-specific rates. The cost model should shift from time-based (₹/hr) to area-based (₹/sq.dm) since surface treatments are fundamentally area-driven, not time-driven.

#### Proposed Rate Structure (₹/sq.dm, median job shop rates)

```python
SURFACE_TREATMENT_RATES = {
    # --- Electroplating ---
    "zinc_clear": 5,          # ₹/sq.dm
    "zinc_yellow": 6,
    "zinc_black": 7,
    "nickel_bright": 12,
    "nickel_electroless": 18,
    "chrome_hard": 15,
    "chrome_decorative": 22,   # includes nickel undercoat
    "cadmium": 25,
    "copper": 8,
    "tin": 8,
    "silver": 50,
    "gold": 150,              # highly variable with gold price
    "rhodium": 200,

    # --- Anodizing ---
    "anodize_type_i": 12,
    "anodize_type_ii_clear": 8,
    "anodize_type_ii_color": 12,
    "anodize_type_iii": 22,
    "anodize_ptfe": 35,

    # --- Chemical Conversion ---
    "chromate_conversion": 4,
    "phosphate_zinc": 3,
    "phosphate_manganese": 5,
    "phosphate_iron": 2,
    "black_oxide_hot": 3,
    "black_oxide_cold": 2,
    "passivation_nitric": 4,
    "passivation_citric": 5,

    # --- Thermal Spray ---
    "hvof": 150,
    "plasma_spray": 100,
    "flame_spray": 60,
    "cold_spray": 250,        # limited availability

    # --- Paint/Organic ---
    "powder_coat_standard": 8,    # per sq.dm
    "powder_coat_premium": 12,
    "ecoat": 6,
    "wet_paint_2coat": 15,
    "wet_paint_3coat": 25,
    "carc": 50,

    # --- Vapor Deposition ---
    "pvd": 80,                # per sq.dm (or per-piece model)
    "cvd": 120,
    "dlc": 150,

    # --- Mechanical ---
    "shot_peening": 5,
    "shot_blasting": 3,
    "bead_blasting": 5,
    "electropolishing": 12,
    "tumble_deburring": 3,    # per sq.dm equivalent
    "burnishing": 8,
}

# Minimum batch charges (₹)
SURFACE_TREATMENT_MIN_CHARGE = {
    "zinc_clear": 800,
    "nickel_bright": 1500,
    "nickel_electroless": 3000,
    "chrome_hard": 3000,
    "cadmium": 5000,
    "silver": 5000,
    "gold": 10000,
    "anodize_type_ii_clear": 1500,
    "anodize_type_iii": 3000,
    "hvof": 10000,
    "pvd": 8000,
    "dlc": 15000,
    "powder_coat_standard": 800,
    "carc": 8000,
}

# H.E. baking cost (₹/kg, added to plating cost for high-strength steel)
HE_BAKING_RATE_PER_KG = 15
```

#### Surface Area Estimation

The cost engine needs surface area. For machined parts:
- **Cylinder OD:** pi * D * L
- **Cylinder bore:** pi * d * depth
- **Flat face:** pi/4 * D^2 (or L * W for rectangular)
- **Complex:** Use a complexity factor (1.2-2.0x simple envelope area)

#### Cost Formula

```
surface_treatment_cost = max(
    surface_area_sq_dm * rate_per_sq_dm * batch_factor,
    minimum_batch_charge / quantity
) + masking_cost + he_baking_cost
```

Where:
- `batch_factor` = lookup from batch size table (Section 9.2)
- `masking_cost` = 10-25% of base treatment cost (if masking required)
- `he_baking_cost` = HE_BAKING_RATE_PER_KG * part_weight_kg (only for steel >31 HRC + electroplating)

---

## Sources

- [IndiaMART Zinc Plating](https://dir.indiamart.com/impcat/zinc-plating.html)
- [IndiaMART Nickel Plating Services](https://dir.indiamart.com/impcat/nickel-plating-services.html)
- [IndiaMART Electroless Nickel Plating](https://dir.indiamart.com/impcat/electroless-nickel-plating.html)
- [IndiaMART Hard Chrome Plating](https://dir.indiamart.com/impcat/hard-chrome-plating.html)
- [IndiaMART HVOF Coating Services](https://dir.indiamart.com/impcat/hvof-coating-services.html)
- [IndiaMART Electro Coating Services](https://dir.indiamart.com/impcat/electro-coating-services.html)
- [Metal Finish and Design - Rates](https://www.metalfinishanddesign.in/rates.html)
- [AK Finishing Technologies - EN Plating](https://www.akfinishingtechnologies.in/electroless-nickel-plating-service.html)
- [ASP Ultra Coating - Plating Services](https://www.aspultracoating.com/plating-services.html)
- [Finishing.com - Cost Forums](https://www.finishing.com/429/81.shtml)
- [Finishing.com - Powder Coating India](https://www.finishing.com/524/55.shtml)
- [DCMSME - Hard Chrome Plating Profile](https://www.dcmsme.gov.in/old/publications/pmryprof/chemical/ch15.pdf)
- [Anodizing Association - MIL-A-8625](https://www.anodizing.org/military-specification-mil-a-8625/)
- [SAF - Military Spec Anodizing](https://www.saf.com/how-to-specify/military-specification-anodizing-mil-a-8625/)
- [Sharrett's Plating - Defense Plating](https://www.sharrettsplating.com/industries/defense-plating/)
- [Sharrett's Plating - Electroless Nickel Cost](https://www.sharrettsplating.com/blog/electroless-nickel-plating-cost/)
- [Sharrett's Plating - H.E. and Electroplating](https://www.sharrettsplating.com/blog/hydrogen-embrittlement-electroplating-what-you-need-to-know/)
- [ENS Technology - Cadmium Plating](https://www.enstechnology.com/mil-spec/fed-qq-p-416f)
- [Omega Research - H.E. Best Practices](https://omegaresearchinc.com/hydrogen-embrittlement-processing-best-practices-for-aerospace-safety/)
- [Erie Plating - Baking for H.E.](https://erieplating.com/finish/baking-for-hydrogen-embrittlement)
- [ARKA PVD Coating India](https://arkapvdcoating.com/ultimate-guide-pvd-coating-industrial-components-india/)
- [VaporTech - PVD Coating Costs](https://blog.vaportech.com/how-much-does-pvd-coating-cost)
- [Plasmatron India - Thermal Spray](https://plasmatronindia.com/)
- [Plasma Spray India](https://www.plasmaspray.co.in/)
- [CPCB - Effluent Emission Standards](https://cpcb.nic.in/effluent-emission/)
- [Netsol Water - CPCB Guidelines for Electroplating ETP](https://www.netsolwater.com/cpcb-guidelines-for-electroplating-industry-effluent-treatment-plants.php?blog=4184)
- [EnterClimate - Electroplating Pollution Control](https://enterclimate.com/blog/environmental-pollutants-in-the-electroplating-anodizing-industry/)
- [ChemResearch - Cadmium Plating Aerospace](https://chemresearchco.com/cadmium-plating-for-aerospace-and-defense/)
- [Scribd - Complete Market Report Electroplating India](https://www.scribd.com/document/681991022/Complete-market-report-on-electroplating-nickel-chrome-India)
