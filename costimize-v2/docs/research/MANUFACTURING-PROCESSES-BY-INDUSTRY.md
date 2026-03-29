# Manufacturing Processes: Defense, Aerospace & Automobile Industries

> Comprehensive reference for AI.Procurve (Costimize) should-cost estimation engine.
> Covers all major manufacturing processes organized by industry and process category.
> Research date: March 29, 2026

---

## Table of Contents

1. [Process Category Reference](#1-process-category-reference)
2. [Aerospace Industry](#2-aerospace-industry)
3. [Defense Industry](#3-defense-industry)
4. [Automobile Industry](#4-automobile-industry)
5. [Cross-Industry Comparison Matrix](#5-cross-industry-comparison-matrix)
6. [Regulatory Standards Summary](#6-regulatory-standards-summary)

---

## 1. Process Category Reference

### 1.1 Subtractive (Machining)

| Process | Description | Typical Tolerance | Surface Finish (Ra) | Typical Materials |
|---------|-------------|-------------------|---------------------|-------------------|
| CNC Turning | Cylindrical material removal on lathe, OD/ID profiles | +/-0.01-0.025 mm | 0.8-3.2 um | All metals, plastics |
| CNC Milling (3/4/5-axis) | Flat, contour, pocket, slot cutting on mill | +/-0.01-0.05 mm | 0.8-3.2 um | All metals, composites |
| Drilling | Hole creation with twist/gun drills | +/-0.05-0.1 mm | 1.6-6.3 um | All metals |
| Boring | Enlarging/finishing existing holes on lathe or mill | +/-0.01-0.025 mm | 0.8-1.6 um | All metals |
| Grinding (cylindrical/surface/centerless) | Precision material removal with abrasive wheel | +/-0.005-0.01 mm | 0.1-0.8 um | Hardened steels, ceramics |
| Honing | Internal bore finishing with abrasive stones | +/-0.005 mm | 0.05-0.4 um | Cylinder bores, gears |
| Lapping | Ultra-precision flat/spherical surface finishing | +/-0.001-0.005 mm | 0.01-0.1 um | Gauge blocks, optical flats |
| Wire EDM | Electrically charged wire cuts conductive materials | +/-0.005-0.01 mm | 0.2-1.6 um | Hardened steels, Ti, Inconel |
| Sinker EDM | Shaped electrode erodes complex cavities | +/-0.01-0.025 mm | 0.4-3.2 um | Hardened tool steels, carbides |
| ECM (Electrochemical Machining) | Reverse electroplating dissolves material, no thermal damage | +/-0.025-0.05 mm | 0.1-0.8 um | Ni superalloys, Ti, hardened steels |
| Broaching | Single-pass creation of keyways, splines, gear teeth | +/-0.01-0.025 mm | 0.4-1.6 um | Steels, Ti, Ni alloys |
| Gear Cutting (hobbing/shaping/shaving) | Generating or form-cutting gear tooth profiles | +/-0.01-0.025 mm (AGMA 10-12) | 0.4-1.6 um | Alloy steels, stainless |

### 1.2 Sheet Metal

| Process | Description | Typical Tolerance | Materials | Thickness Range |
|---------|-------------|-------------------|-----------|-----------------|
| Laser Cutting | Focused laser beam melts/vaporizes material along path | +/-0.05-0.1 mm | Steel, Al, Ti, SS | 0.5-25 mm |
| Plasma Cutting | Ionized gas arc cuts conductive materials | +/-0.5-1.5 mm | Carbon steel, SS, Al | 3-50 mm |
| Waterjet Cutting | High-pressure water + abrasive cuts any material, no HAZ | +/-0.05-0.1 mm | Any (metals, composites, ceramics) | 0.5-200 mm |
| Punching/Blanking | Punch/die creates holes and profiles in sheet | +/-0.05-0.1 mm | Steel, Al, Cu, brass | 0.5-6 mm |
| Press Brake Bending | V-die/punch bends sheet along linear axis | +/-0.1-0.5 mm, +/-0.5 deg | Steel, Al, SS, Ti | 0.5-20 mm |
| Deep Drawing | Punch draws sheet into cup/box shape through die | +/-0.1-0.25 mm | Steel, Al, Cu, brass | 0.3-6 mm |
| Stamping (progressive/transfer) | High-speed punch press forms complex shapes from coil | +/-0.05-0.1 mm | Steel, Al, Cu | 0.3-6 mm |
| Metal Spinning | Mandrel + roller forms axisymmetric shapes from disc | +/-0.1-0.5 mm | Al, steel, Cu, Ti | 0.5-12 mm |
| Hydroforming (tube/sheet) | High-pressure fluid forms complex hollow shapes | +/-0.1-0.25 mm | Al, steel, SS, Ti | 0.5-10 mm |
| Roll Forming | Continuous bending of strip through roller stations | +/-0.1-0.25 mm | Steel, Al, SS | 0.3-6 mm |
| Stretch Forming | Sheet stretched over form block, minimal springback | +/-0.25-1.0 mm | Al, Ti, SS | 0.5-6 mm |

### 1.3 Forming / Forging

| Process | Description | Typical Tolerance | Materials | Size Range |
|---------|-------------|-------------------|-----------|------------|
| Open Die Forging | Flat dies compress billet, operator controls shape | +/-1-5 mm | Carbon/alloy steels, Ti, Ni alloys | Up to 150 tonnes |
| Closed Die Forging (impression) | Shaped dies form near-net-shape parts | +/-0.5-2 mm | Steels, Al, Ti, Ni superalloys | 0.1 kg - 500 kg |
| Ring Rolling | Radial-axial rolling of seamless rings | +/-0.5-2 mm | Steels, Ti, Ni superalloys | 100mm - 8m diameter |
| Isothermal Forging | Dies heated to workpiece temp, uniform deformation | +/-0.25-0.5 mm | Ti-6Al-4V, Ni superalloys | Up to 50 kg |
| Superplastic Forming (SPF) | Gas pressure forms sheet at superplastic temperature | +/-0.25-0.5 mm | Ti-6Al-4V, Al-Li, Inconel | Large panels |
| Powder Metallurgy (PM) | Compaction + sintering of metal powder, near-net-shape | +/-0.05-0.1 mm | Iron, steel, Cu, SS, Ti | 0.01-10 kg |
| Metal Injection Molding (MIM) | Injection molding of fine metal powder + binder | +/-0.03-0.05 mm | SS, Ti, tool steels, W, Co | 0.1-250 g |
| Extrusion (hot/cold) | Material forced through shaped die | +/-0.1-0.5 mm | Al, Cu, steel, Ti | Profiles up to 500mm |
| Swaging | Radial forging reduces diameter of tubes/bars | +/-0.05-0.1 mm | Steel, Ti, W, Mo | 5-150 mm dia |
| Cold Heading/Forming | High-speed forming of fasteners from wire | +/-0.025-0.05 mm | Steel, SS, Al, Cu | M1-M30 fasteners |

### 1.4 Casting

| Process | Description | Typical Tolerance | Surface Finish (Ra) | Materials |
|---------|-------------|-------------------|---------------------|-----------|
| Sand Casting | Molten metal poured into sand mold | +/-0.4-1.6 mm/100mm (CT11-13) | 6.3-25 um | Iron, steel, Al, Cu, Ni alloys |
| Investment Casting (lost wax) | Wax pattern, ceramic shell, precision casting | +/-0.1-0.5 mm (CT5-8) | 1.6-6.3 um | Ni superalloys, Ti, SS, Co-Cr |
| Die Casting - HPDC | High pressure injection into steel die | +/-0.05-0.3 mm (CT4-7) | 0.8-3.2 um | Al, Zn, Mg |
| Die Casting - Gravity | Gravity-fed metal into permanent mold | +/-0.2-0.5 mm (CT6-9) | 3.2-6.3 um | Al, Cu, Mg |
| Die Casting - Low Pressure | Low pressure pushes metal up into mold | +/-0.1-0.4 mm (CT5-8) | 1.6-6.3 um | Al alloys |
| Centrifugal Casting | Spinning mold, centrifugal force distributes metal | +/-0.1-0.5% radial (CT3-8) | 3-8 um | Steel, Ni alloys, Cu, Ti |
| Single Crystal Casting | Bridgman process + grain selector for SC blades | +/-0.1-0.25 mm | 3.2-6.3 um | Ni superalloys (CMSX-4, PWA 1484) |
| Vacuum Casting | Investment casting under vacuum, prevents oxidation | +/-0.1-0.5 mm | 1.6-6.3 um | Ti, Ni superalloys, reactive alloys |

### 1.5 Joining

| Process | Description | Typical Applications | Materials |
|---------|-------------|---------------------|-----------|
| TIG Welding (GTAW) | Gas tungsten arc, highest quality, manual/automated | Aerospace structures, thin sheets, root passes | Ti, Al, SS, Ni alloys |
| MIG/MAG Welding (GMAW) | Gas metal arc, high deposition rate | Automotive BIW, structural steel | Steel, Al, SS |
| Stick Welding (SMAW) | Shielded metal arc, field/maintenance welding | Defense field repair, structural | Carbon/alloy steels |
| Resistance Spot Welding (RSW) | Current through clamped sheets creates spot nugget | Automotive BIW (4000-6000 spots/car) | Steel, Al sheets |
| Friction Stir Welding (FSW) | Rotating tool plasticizes and joins without melting | Aerospace Al structures, rocket tanks | Al alloys, Cu, Mg |
| Electron Beam Welding (EBW) | High-energy electron beam in vacuum | Jet engine components, gears, Ti structures | Ti, Ni superalloys, refractory metals |
| Laser Welding (LBW) | Focused laser beam, deep penetration, low distortion | Automotive panels, battery housings, gear assemblies | Steel, Al, Ti, dissimilar metals |
| Brazing | Filler metal flows by capillary action above 450C | Heat exchangers, turbine components, carbide tooling | Cu, Ag, Ni-based fillers on SS, Ni alloys |
| Soldering | Filler metal below 450C | Electronics, PCB assembly | Sn-Pb, Sn-Ag-Cu (lead-free) |
| Riveting (solid/blind) | Mechanical fastening with permanent pin | Aircraft skins (100,000+ per aircraft), structural | Al, Ti, steel, Monel |
| Adhesive Bonding | Structural adhesives (epoxy, polyurethane, acrylic) | Composite joints, aerospace panels, automotive | Composites, Al, steel |
| Friction Welding (rotary/linear) | Rotational or linear friction generates joining heat | Drive shafts, valves, bi-metallic joints | Steel, Ti, Al, dissimilar metals |
| Diffusion Bonding | Solid-state joining under heat and pressure | SPF/DB Ti panels, heat exchangers | Ti, Ni superalloys |

### 1.6 Surface Treatment

| Process | Description | Coating Thickness | Purpose | Materials |
|---------|-------------|-------------------|---------|-----------|
| Anodizing (Type II, sulfuric) | Electrochemical oxide layer on Al | 5-25 um | Corrosion resistance, color | Aluminum alloys |
| Hard Anodizing (Type III) | Dense, hard oxide on Al | 25-75 um | Wear + corrosion resistance | Aluminum alloys |
| Chrome Plating (hard) | Electrodeposited chromium | 20-100 um | Wear, corrosion, low friction | Steel, Cu, Al (with undercoat) |
| Electroless Nickel Plating | Autocatalytic Ni-P deposition | 5-75 um | Uniform coating, corrosion, wear | All metals |
| Zinc Plating + Chromate | Electrodeposited Zn + passivation | 5-25 um | Corrosion protection (sacrificial) | Steel, iron |
| Cadmium Plating | Electrodeposited Cd (restricted, defense use) | 5-25 um | Corrosion, lubricity, galvanic compatibility | Steel (aerospace/defense) |
| Phosphating (Mn/Zn) | Chemical conversion coating | 5-25 um | Paint adhesion, corrosion, break-in wear | Steel, iron |
| Passivation (citric/nitric acid) | Chemical treatment removes free iron | <1 um | Corrosion resistance (stainless) | Stainless steels |
| Black Oxide | Chemical conversion to Fe3O4 | 1-2 um | Appearance, minimal corrosion, anti-glare | Steel, iron, SS |
| Powder Coating | Electrostatic spray + heat cure | 50-150 um | Corrosion, appearance, UV resistance | Steel, Al, castings |
| Wet Painting (primer/topcoat) | Spray/dip liquid paint | 25-75 um per coat | Corrosion, appearance, camouflage | All metals |
| HVOF Thermal Spray | High velocity oxy-fuel sprays WC/Co, Cr3C2 | 50-500 um | Extreme wear, hard chrome replacement | Landing gear, hydraulic rods |
| Plasma Spray | Plasma arc sprays ceramic/metal powder | 100-1000 um | Thermal barrier (TBC), wear | Turbine blades, combustion liners |
| PVD Coating | Physical vapor deposition in vacuum | 1-5 um | Hardness, low friction, wear (TiN, TiAlN, DLC) | Cutting tools, bearings, gears |
| CVD Coating | Chemical vapor deposition at high temp | 5-20 um | Hardness, high-temp protection (TiC, Al2O3) | Cutting tools, turbine components |
| Shot Peening | High-velocity media impacts surface | N/A (compressive stress layer) | Fatigue life improvement, stress relief | Steel, Ti, Al, Ni alloys |
| Electropolishing | Reverse electroplating dissolves surface peaks | Removes 10-50 um | Smooth, bright finish, passivation | SS, Ti, Ni alloys |

### 1.7 Heat Treatment

| Process | Description | Typical Temp Range | Purpose | Materials |
|---------|-------------|-------------------|---------|-----------|
| Hardening (quench) | Austenitize + rapid quench to form martensite | 750-900C | Maximum hardness | Carbon/alloy steels |
| Tempering | Reheat after hardening to relieve stress | 150-650C | Toughness, reduce brittleness | Hardened steels |
| Annealing (full) | Heat above Ac3, slow cool in furnace | 700-950C | Softening, relieve stress, improve machinability | Steels, Cu, Al |
| Normalizing | Heat above Ac3, air cool | 800-950C | Uniform grain, moderate hardness | Carbon/alloy steels |
| Stress Relieving | Below transformation temp, slow cool | 550-650C | Relieve residual stress from welding/machining | All steels |
| Carburizing (gas/vacuum/pack) | Carbon diffusion into surface | 850-950C | Hard case, tough core (0.5-2.0mm depth) | Low-carbon steels (8620, 9310) |
| Nitriding (gas/ion/salt bath) | Nitrogen diffusion into surface | 480-580C | Surface hardness, wear, fatigue (no quench needed) | Alloy steels, Ti, SS |
| Carbonitriding | C + N diffusion simultaneously | 700-900C | Thin hard case on small parts | Low-carbon steels |
| Induction Hardening | Localized heating via electromagnetic field + quench | Surface only to 900C+ | Selective surface hardening | Medium-carbon steels |
| Cryogenic Treatment | Sub-zero treatment after hardening | -80C to -196C | Convert retained austenite, dimensional stability | Tool steels, bearing steels |
| Solution Treatment + Aging | Dissolve precipitates, then age to precipitate | 480-560C (Al), 950-1050C (Ti) | Strength via precipitation hardening | Al (2xxx, 6xxx, 7xxx), Ti-6Al-4V |
| Precipitation Hardening | Age after solution treatment | 480-620C | High strength + corrosion resistance | 17-4PH SS, Inconel 718, Waspaloy |
| Vacuum Heat Treatment | All HT operations under vacuum/inert atmosphere | Varies | No oxidation/decarburization, bright finish | Ti, Ni superalloys, tool steels |

### 1.8 Composites & Additive Manufacturing

| Process | Description | Typical Tolerance | Materials | Applications |
|---------|-------------|-------------------|-----------|-------------|
| Hand Layup | Manual placement of prepreg/dry fabric | +/-0.5-1.0 mm | CFRP, GFRP, aramid | Low-volume aerospace panels, repairs |
| Automated Fiber Placement (AFP) | Robotic head places narrow tows on complex surfaces | +/-0.25-0.5 mm | CFRP, GFRP prepreg tows | Fuselage barrels, wing skins |
| Automated Tape Laying (ATL) | Robotic head lays wide prepreg tape on flat/gentle contours | +/-0.25-0.5 mm | CFRP/GFRP wide prepreg tape | Large flat panels, wing skins |
| Autoclave Curing | Pressurized oven cures prepreg under vacuum + pressure | +/-0.1-0.25 mm thickness | CFRP, GFRP prepreg | Primary structure, flight-critical parts |
| Out-of-Autoclave (OOA/VBO) | Vacuum-bag-only cure in standard oven | +/-0.25-0.5 mm thickness | OOA prepregs | Secondary structure, cost-sensitive |
| RTM (Resin Transfer Molding) | Dry fiber preform in closed mold, resin injected under pressure | +/-0.1-0.25 mm | CFRP, GFRP + epoxy/BMI resin | Complex 3D shapes, fan blades |
| VARTM (Vacuum-Assisted RTM) | Vacuum draws resin into dry preform under single-sided mold | +/-0.25-0.5 mm | GFRP, CFRP + epoxy/vinyl ester | Large structures, boat hulls, wind blades |
| Filament Winding | Continuous fiber wound on rotating mandrel | +/-0.1-0.25 mm | CFRP, GFRP, aramid | Pressure vessels, rocket motor cases, tubes |
| Compression Molding (SMC/BMC) | Heated matched dies compress sheet/bulk molding compound | +/-0.1-0.25 mm | SMC, BMC (chopped glass + polyester) | Automotive body panels, covers |
| DMLS/SLM (Laser Powder Bed Fusion) | Laser selectively melts metal powder layer by layer (30-50 um) | +/-0.05-0.1 mm | Ti-6Al-4V, Inconel 718/625, Al, SS, CoCr | Turbine fuel nozzles, brackets, implants |
| EBM (Electron Beam Melting) | Electron beam melts powder in vacuum | +/-0.1-0.2 mm | Ti-6Al-4V, CoCr, Inconel | Orthopedic implants, turbine blades |
| WAAM (Wire Arc Additive Mfg) | Wire-feed arc welding builds large near-net-shape parts | +/-0.5-2.0 mm | Ti, Al, steel, Ni alloys, tantalum | Large aerospace structural preforms |
| Binder Jetting | Binder deposited on powder bed, then sintered | +/-0.1-0.2 mm | SS, tool steel, Inconel, Cu | Tooling, short-run production parts |
| DED (Directed Energy Deposition) | Laser/electron beam melts powder/wire feed | +/-0.25-0.5 mm | Ti, Ni alloys, steel | Repair, large part build-up, cladding |

### 1.9 Inspection / Testing

| Method | Description | Detects | Standards |
|--------|-------------|---------|-----------|
| CMM (Coordinate Measuring Machine) | Contact/non-contact 3D dimensional measurement | Dimensional deviations from CAD | ISO 10360, ASME B89.4.1 |
| Surface Roughness Testing (profilometer) | Stylus/optical measurement of surface profile | Ra, Rz, Rq surface finish values | ISO 4287, ASME B46.1 |
| Hardness Testing (Rockwell/Vickers/Brinell) | Indenter measures resistance to penetration | Material hardness (HRC, HV, HB) | ASTM E18, E92, E10 |
| UT - Ultrasonic Testing | High-frequency sound waves detect internal defects | Cracks, voids, inclusions, delaminations | ASTM E164, E2375; ISO 17640 |
| MPI - Magnetic Particle Inspection | Magnetic flux leakage + iron particles detect surface defects | Surface/near-surface cracks in ferromagnetic materials | ASTM E1444, E709; ISO 17638 |
| DPI/LPI - Dye Penetrant Inspection | Liquid penetrant wicks into surface cracks, developer reveals | Surface-breaking cracks in any non-porous material | ASTM E1417, E165; ISO 3452 |
| RT - Radiographic Testing | X-ray/gamma ray reveals internal structure | Internal voids, porosity, inclusions, cracks | ASTM E94, E1742; ISO 17636 |
| ET - Eddy Current Testing | Electromagnetic induction detects conductivity changes | Surface/subsurface cracks, corrosion, coating thickness | ASTM E376, E2884; ISO 15549 |
| Pressure/Leak Testing | Hydrostatic or pneumatic pressure verifies seal integrity | Leaks, burst strength, proof pressure | ASME BPVC, MIL-STD-1246 |
| Salt Spray Testing | Accelerated corrosion testing in salt fog chamber | Corrosion resistance of coatings/treatments | ASTM B117, ISO 9227 |
| Tensile/Fatigue Testing | Mechanical testing of material properties | Yield/ultimate strength, elongation, fatigue life | ASTM E8, E466; ISO 6892 |
| CT Scanning (Industrial) | X-ray computed tomography for 3D internal visualization | Internal geometry, porosity, assembly verification | ASTM E1695, VDI/VDE 2630 |
| Phased Array UT (PAUT) | Multi-element UT probe for detailed volumetric scanning | Complex geometry internal defects | ASTM E2491, ISO 13588 |

---

## 2. Aerospace Industry

### 2.1 Most-Used Processes

**Primary Manufacturing:**
- 5-axis CNC milling (structural components, monolithic ribs, spars, bulkheads)
- CNC turning (engine shafts, landing gear components, fasteners)
- Investment casting / single crystal casting (turbine blades, vanes, combustion liners)
- Closed die forging (landing gear, engine discs, fan blades)
- Ring rolling (engine casings, bearing races)
- Sheet metal forming: stretch forming, hydroforming (fuselage skins, wing panels)
- Composite layup: AFP/ATL + autoclave cure (fuselage barrels, wing skins, empennage)
- RTM (fan blades -- e.g., LEAP engine CFRP fan blades)
- Filament winding (pressure vessels, rocket motor cases)

**Joining:**
- Riveting (100,000+ rivets per commercial aircraft fuselage)
- Friction stir welding (Al fuel tanks, wing panels -- SpaceX, Airbus)
- Electron beam welding (Ti structures, engine components -- vacuum environment)
- TIG welding (Ti and Ni alloy assemblies)
- Diffusion bonding + SPF (Ti sandwich panels)
- Adhesive bonding (composite-to-composite, composite-to-metal secondary bonds)

**Surface Treatment:**
- Hard anodizing (Al components)
- Cadmium plating (legacy, being replaced by IVD Al or Zn-Ni)
- HVOF thermal spray (landing gear -- replacing hard chrome per AMS 2448)
- Plasma spray TBC (turbine blades -- yttria-stabilized zirconia)
- PVD coatings (bearings, gears -- DLC, WC/C)
- Shot peening (all fatigue-critical components -- SAE AMS-2432)
- Electroless nickel plating
- Chromic acid anodize (being replaced due to REACH)

**Heat Treatment:**
- Solution treatment + aging (Al 7075-T6, 2024-T3; Ti-6Al-4V)
- Precipitation hardening (Inconel 718, 17-4PH SS, Waspaloy)
- Vacuum heat treatment (Ti and Ni superalloy components)
- Stress relieving (post-weld, post-machining)
- Carburizing (gear teeth -- AMS 2759/7)
- Nitriding (Ti components for wear resistance)

**Additive Manufacturing:**
- DMLS/SLM (fuel nozzles -- GE LEAP has 19 AM fuel nozzles per engine)
- EBM (Ti structural brackets, orthopedic)
- DED/WAAM (large Ti preforms, repair of high-value components)

### 2.2 Specialized Processes (Aerospace-Specific)

| Process | Why Aerospace-Specific | Example Component |
|---------|----------------------|-------------------|
| Single crystal investment casting | Only way to achieve creep resistance at >1400C | Turbine blades (CMSX-4, PWA 1484) |
| Superplastic forming / diffusion bonding (SPF/DB) | Ti-6Al-4V sandwich panels, impossible by other means | Wing leading edges, engine nacelles |
| Isothermal forging | Tight tolerances in Ti/Ni superalloys with narrow forging windows | Turbine discs, compressor discs |
| Friction stir welding (Al alloys) | No melting = no porosity, ideal for pressure-tight Al joints | Fuel tanks, fuselage barrels |
| Autoclave composite curing | Maximum fiber volume fraction (60%+), lowest void content (<1%) | Primary structure (fuselage, wings) |
| Electron beam welding | Deep penetration in vacuum, no contamination of Ti/Ni alloys | Engine cases, Ti structures |
| HVOF WC/Co thermal spray | Replacing hard chrome on landing gear (AMS 2447/2448) | Landing gear actuator rods |
| Electrochemical machining (ECM) | Stress-free machining of Ni superalloy turbine blade cooling holes | Turbine blade film cooling holes |
| Chemical milling (chem-mill) | Controlled acid etching removes material from large thin panels | Fuselage skin panels (weight reduction) |
| Abrasive waterjet trimming | Cuts composites without delamination, no thermal damage | CFRP panel trimming |

### 2.3 Typical Materials

| Material | Alloys | Applications |
|----------|--------|-------------|
| Aluminum | 2024-T3, 7075-T6, 7050-T7451, 2219, Al-Li (2195, 2050) | Fuselage skins, wing ribs, spars, bulkheads |
| Titanium | Ti-6Al-4V, Ti-6Al-2Sn-4Zr-2Mo, Ti-5553, Ti-6246 | Fan blades, landing gear, bulkheads, fasteners |
| Nickel superalloys | Inconel 718, 625, Waspaloy, Rene 88, CMSX-4, PWA 1484 | Turbine blades/discs, combustion liners, exhaust |
| Stainless steel | 17-4PH, 15-5PH, Custom 450, A286, AM355 | Fasteners, hydraulic fittings, bearings |
| High-strength steel | 300M, 4340, Aermet 100, Custom 465 | Landing gear, actuators, flap tracks |
| CFRP (carbon fiber) | T800/M21, IM7/8552, AS4/3501-6 | Fuselage barrels, wing skins, empennage |
| Ceramic Matrix Composites (CMC) | SiC/SiC, oxide-oxide | Turbine shrouds, combustor liners (GE LEAP, GE9X) |

### 2.4 Tolerance Requirements

| Component Type | Dimensional Tolerance | Surface Finish | Position/Profile |
|---------------|----------------------|----------------|-----------------|
| Turbine blades | +/-0.025-0.05 mm | Ra 0.4-1.6 um | Profile +/-0.05 mm |
| Landing gear | +/-0.01-0.025 mm on bearing surfaces | Ra 0.2-0.8 um | True position +/-0.025 mm |
| Engine shafts | +/-0.005-0.01 mm on journals | Ra 0.1-0.4 um | Concentricity 0.01 mm TIR |
| Structural machined parts | +/-0.05-0.1 mm general, +/-0.01 mm critical | Ra 1.6-3.2 um | Profile +/-0.1 mm |
| Fuselage skins (machined) | +/-0.1-0.25 mm thickness | Ra 1.6-3.2 um | Contour +/-0.5 mm |
| Composite panels | +/-0.1-0.25 mm thickness | N/A (tooled surface) | Profile +/-0.5-1.0 mm |

### 2.5 Regulatory Standards

| Standard | Scope |
|----------|-------|
| AS9100 (Rev D) / IA9100 | Quality management system for aviation, space, defense (builds on ISO 9001) |
| Nadcap | Special process accreditation: heat treat, welding, NDT, surface treatment, composites, chemical processing |
| AMS (Aerospace Material Specifications) | Material and process specs (SAE International): AMS 2759 (heat treat), AMS 2447/2448 (HVOF), AMS 2432 (shot peening), AMS 2750 (pyrometry) |
| AWS D17.1 | Fusion welding for aerospace applications |
| AWS D17.2 | Resistance welding for aerospace |
| AWS D17.3 | Friction stir welding of Al for aerospace |
| ASTM E1444/E165/E164 | NDT methods (MPI, DPI, UT) |
| NAS 410 / EN 4179 | NDT personnel qualification |
| FAR Part 21 | Airworthiness certification (FAA) |
| EASA Part 21 | Airworthiness certification (European) |
| NIST SP 800-171 / CMMC | Cybersecurity for defense supply chain |

---

## 3. Defense Industry

### 3.1 Most-Used Processes

**Primary Manufacturing:**
- CNC milling (weapon housings, missile components, optics mounts, avionics chassis)
- CNC turning (barrels, shafts, ammunition components, projectile bodies)
- Closed die forging (gun receivers, barrel blanks, armor-piercing penetrators)
- Cold hammer forging (gun barrels -- button rifling, cold hammer forging for rifled bores)
- Deep hole drilling/gun drilling (barrel bores)
- Sand casting (large vehicle hulls, turret components, engine blocks)
- Investment casting (missile fins, guidance components, small arms parts)
- Die casting (aluminum housings, electronic enclosures)
- Sheet metal forming: laser cutting, press brake bending (vehicle armor panels, enclosures)
- Stamping (ammunition casings, small hardware)
- Powder metallurgy (tungsten penetrators, copper rotating bands, sintered bearings)

**Joining:**
- MIG/MAG welding (armored vehicle hulls -- RHA steel, Al 5083/7039)
- TIG welding (high-quality structural joints, Ti assemblies)
- Stick welding (field repair, expeditionary manufacturing)
- Friction stir welding (Al armor panels -- reducing weight)
- Electron beam welding (gun components, high-strength joints)
- Brazing (ammunition primers, electronics, heat exchangers)
- Riveting (aircraft, lightweight vehicle structures)

**Surface Treatment:**
- Hard chrome plating (gun barrels, hydraulic actuators)
- Cadmium plating (fasteners, connectors -- MIL-STD-870)
- Phosphating / Parkerizing (weapons, vehicle components -- MIL-DTL-16232)
- Black oxide (small arms components)
- CARC painting (Chemical Agent Resistant Coating -- MIL-DTL-64159)
- Zinc plating (hardware, fasteners)
- Anodizing (Al enclosures, optics housings)
- Ion nitriding (Ti armament components, gun barrels)

**Heat Treatment:**
- Through-hardening + tempering (barrel steels 4150, 4340)
- Carburizing (gears, drive components)
- Induction hardening (selective hardening of critical surfaces)
- Cryogenic treatment (barrel steels for dimensional stability and wear)
- Solution treatment + aging (Al 7075, Ti-6Al-4V armor)
- Nitriding (gun barrels for erosion resistance)

**Additive Manufacturing:**
- DMLS/SLM (rapid prototyping, short-run missile/drone components)
- WAAM (expeditionary repair, large structural preforms)
- Binder jetting (tooling, casting patterns)

### 3.2 Specialized Processes (Defense-Specific)

| Process | Why Defense-Specific | Example Component |
|---------|---------------------|-------------------|
| Cold hammer forging (barrel) | Creates rifling while forging barrel to near-net-shape | Rifle/cannon barrels (M4, M240) |
| Rotary forging (projectiles) | Forms aerodynamic projectile shapes at high rate | Artillery shells, mortar rounds |
| RHA/armor steel welding | Specialized procedures for welding rolled homogeneous armor | IFV/APC hulls (M2 Bradley, Stryker) |
| CARC painting | Chemical agent resistant coating, infrared signature reduction | All military vehicles (MIL-DTL-64159) |
| Parkerizing (Mn phosphate) | Corrosion + wear protection for weapons per MIL-DTL-16232 | M16/M4 receivers, small arms |
| Depleted uranium machining | Specialized containment and tooling for DU penetrators | M829 APFSDS tank rounds |
| Explosive forming | Shock wave forms large armor panels from high-strength alloys | Vehicle armor plates |
| Autofrettage | Internal pressure exceeds yield, creates compressive residual stress | Gun barrels (extends fatigue life 3-5x) |
| Electroforming | Electrodeposits metal to form precision thin-wall shapes | Radar waveguides, RF components |

### 3.3 Typical Materials

| Material | Alloys | Applications |
|----------|--------|-------------|
| Armor steel | RHA (MIL-DTL-12560), HHA (MIL-DTL-46100), UHH | Vehicle hulls, ballistic protection |
| Armor aluminum | 5083-H131, 7039-T64, 2519-T87 (MIL-DTL-46027) | Lightweight vehicle armor |
| Gun steels | 4150, 4340, Stellite 6 (liner), Cr-Mo-V barrel steels | Barrels, receivers, bolts |
| Tungsten alloys | W-Ni-Fe, W-Ni-Co (sintered), depleted uranium | Kinetic energy penetrators, counterweights |
| Titanium | Ti-6Al-4V, Ti-6Al-4V ELI | Armor, structural, hypersonic vehicles |
| Nickel superalloys | Inconel 718, 625, Waspaloy | Jet engines, missile components |
| Copper alloys | CuBe, CuCrZr, Cu-Ni | Rotating bands, electronics, RF connectors |
| Composite armor | Ceramic + UHMWPE (Dyneema), ceramic + aramid (Kevlar) | Body armor, vehicle applique armor |
| Energetic materials | RDX, HMX, PBXN-110, IMX-101 (insensitive munitions) | Warheads, explosive fills |

### 3.4 Tolerance Requirements

| Component Type | Dimensional Tolerance | Surface Finish | Notes |
|---------------|----------------------|----------------|-------|
| Gun barrels (bore) | +/-0.005-0.01 mm | Ra 0.2-0.8 um | Rifling geometry critical |
| Projectile bodies | +/-0.01-0.025 mm | Ra 0.8-1.6 um | Aerodynamic profile critical |
| Optics mounts | +/-0.005-0.01 mm | Ra 0.4-0.8 um | Alignment critical |
| Missile guidance | +/-0.01-0.025 mm | Ra 0.8-1.6 um | Precision assemblies |
| Vehicle structural | +/-0.25-1.0 mm | Ra 3.2-6.3 um | Weldment tolerances |
| Ammunition casings | +/-0.025-0.05 mm | Ra 0.8-3.2 um | Chamber fit critical |
| Electronics enclosures | +/-0.05-0.1 mm | Ra 1.6-3.2 um | EMI shielding fit |

### 3.5 Regulatory Standards

| Standard | Scope |
|----------|-------|
| MIL-STD-11991B | General standard for parts, materials, and processes (master DoD standard) |
| MIL-STD-186F | Protective finishes (zinc, cadmium, etc.) |
| MIL-STD-1916 | Acceptance sampling |
| MIL-DTL-12560 | Rolled homogeneous armor (RHA) steel plate |
| MIL-DTL-46100 | High-hardness armor (HHA) steel plate |
| MIL-DTL-32332 | Transparent armor (glass/polycarbonate) |
| MIL-DTL-16232 | Phosphate coating (Parkerizing) |
| MIL-DTL-64159 | CARC painting system |
| MIL-S-23284 | Steel forgings for military applications |
| MIL-Q-9858 (legacy) / AS9100 | Quality program requirements (legacy replaced by AS9100 for many programs) |
| MIL-STD-810 | Environmental testing (shock, vibration, temperature, humidity, altitude) |
| MIL-STD-461 | EMI/EMC requirements for electronic subsystems |
| MIL-STD-1246 | Cleanliness levels for fluid systems |
| DFARS 252.225-7014 | Specialty metals clause (domestic sourcing) |
| ITAR (22 CFR 120-130) | International Traffic in Arms Regulations (export control) |
| CMMC (Cybersecurity Maturity Model) | Cybersecurity requirements for defense contractors |

---

## 4. Automobile Industry

### 4.1 Most-Used Processes

The automotive manufacturing flow follows the "Big Four" stages: **Stamping -> Welding (BIW) -> Painting -> Final Assembly**, with upstream component manufacturing feeding into these.

**Primary Manufacturing:**
- Progressive/transfer die stamping (body panels: doors, hoods, fenders, roof -- 200-1500 ton presses)
- Mega/giga casting - HPDC (large structural castings -- Tesla Model Y rear underbody, 6000-9000 ton press)
- Die casting - HPDC (engine blocks, transmission cases, structural nodes)
- Die casting - gravity/low pressure (Al cylinder heads, suspension knuckles)
- Sand casting (engine blocks - legacy, large components)
- Closed die forging (crankshafts, connecting rods, steering knuckles, axle shafts)
- Powder metallurgy (connecting rods, gears, valve seats, camshaft lobes -- 50% of all PM goes to automotive)
- Cold heading (fasteners, studs, nuts -- billions per year per OEM)
- CNC turning (crankshafts, camshafts, axle shafts, transmission shafts)
- CNC milling (engine heads, transmission cases -- post-casting machining)
- Grinding (crankshaft journals, camshaft lobes, gear teeth)
- Honing (cylinder bores -- critical for oil retention and ring seal)
- Broaching (keyways in transmission gears, spline profiles)
- Gear cutting: hobbing + shaving/grinding (transmission gears)
- Roll forming (structural members, bumper beams, door beams)
- Hydroforming (exhaust manifolds, structural rails, chassis members)
- Extrusion (Al structural profiles for EV platforms)
- Injection molding (interior trim, bumper fascia, dashboards -- plastic)
- Compression molding - SMC/BMC (body panels, underbody shields)

**Joining:**
- Resistance spot welding (4000-6000 spots per BIW -- primary joining method)
- Laser welding (roof-to-side panel, tailored blanks, battery housings)
- MIG/MAG welding (chassis subframes, suspension, exhaust systems)
- Laser brazing (visible seams -- roof joints, trunk lids)
- Adhesive bonding (windshield, composite/Al panels, anti-flutter)
- Self-pierce riveting (SPR) (Al-to-steel mixed material BIW)
- Flow drill screwing (FDS) (mixed material joining)
- Clinching (mechanical interlocking of sheet metal)
- Friction element welding (multi-material EV bodies)
- Projection welding (nuts, studs welded to panels)

**Surface Treatment / Painting:**
- E-coat (electrodeposition primer -- full BIW immersion, 18-25 um, corrosion protection)
- Phosphating (zinc phosphate pre-treatment before E-coat)
- Primer surfacer (smooths imperfections before basecoat)
- Basecoat/clearcoat (appearance, UV protection, durability)
- Powder coating (underbody, chassis components)
- Zinc/zinc-nickel plating (fasteners, brackets)
- Zinc flake coating (Geomet/Dacromet -- high-corrosion fasteners)
- Galvanizing (hot-dip or electrogalvanized body sheet)
- Anodizing (Al trim, EV battery enclosures)

**Heat Treatment:**
- Carburizing (transmission gears, differential gears)
- Induction hardening (crankshaft journals, camshaft lobes, CV joint components)
- Through-hardening + tempering (springs, fasteners)
- Solution treatment + aging (Al castings -- T6 condition)
- Austempering (connecting rods -- ADI, austempered ductile iron)
- Press hardening / hot stamping (boron steel B-pillar, door beams -- 1500+ MPa)

### 4.2 Specialized Processes (Automotive-Specific)

| Process | Why Automotive-Specific | Example Component |
|---------|------------------------|-------------------|
| Progressive die stamping | Ultra-high-speed (30-60 strokes/min) for million+ volume | Body panels, brackets |
| Mega/giga casting (HPDC 6000-9000T) | Single-piece structural castings replace 70+ stamped/welded parts | Tesla rear underbody, subframes |
| Press hardening (hot stamping) | Boron steel heated to 900C, formed + quenched in die to 1500 MPa | B-pillars, door beams, bumper beams |
| Resistance spot welding (robotic) | 4000-6000 spots per BIW at 1-2 sec/spot, fully robotic | Body-in-White assembly |
| Tailored blank laser welding | Different thickness/grade sheets welded before stamping | Door inners, floor pans |
| Self-pierce riveting (SPR) | Joins Al-to-steel without pre-drilling, critical for mixed-material BIW | Jaguar/Land Rover Al bodies, Ford F-150 |
| Honing (cylinder bore) | Plateau honing creates oil-retention crosshatch pattern | Engine cylinder bores |
| Powder metallurgy (PM) | Near-net-shape, high volume (100K+/month), 50% of global PM market | Connecting rods, gears, valve seats |
| Automated BIW painting (E-coat + 3-wet) | Full dip + robotic spray in 30m+ paint booth, 40-60 JPH | Entire vehicle body |
| Laser brazing | Visible seam joining with smooth finish, no grinding needed | Roof-to-side joints |

### 4.3 Typical Materials

| Material | Grades | Applications |
|----------|--------|-------------|
| Mild steel | DC04, DC06, IF steel | Body panels (inner), brackets |
| HSLA steel | HSLA 340-550 | Structural reinforcements, rails |
| DP/TRIP/CP steels | DP 590-980, TRIP 780, CP 1000 | Structural, energy absorption |
| Press hardening steel | 22MnB5 (Usibor 1500) | B-pillars, bumper beams, door beams |
| Aluminum | 5xxx (5182, 5754), 6xxx (6016, 6111), 7xxx (7075) | Closures, BIW panels, structural |
| Cast aluminum | A356 (AlSi7Mg), A380 (AlSi9Cu3), AlSi10MnMg | Engine blocks, structural castings |
| Cast iron | Grey iron (GJL-250), CGI (GJV-450), ADI | Engine blocks (legacy), brake rotors |
| Magnesium | AZ91D, AM60B | Steering columns, instrument panels, seat frames |
| Carbon fiber | SMC, CFRP prepreg | Roof panels (BMW 7-Series), structural (supercars) |
| Engineering plastics | PA6/PA66 (GF), PBT, PP, ABS, PC/ABS | Interior trim, bumpers, covers |

### 4.4 Tolerance Requirements

| Component Type | Dimensional Tolerance | Surface Finish | Notes |
|---------------|----------------------|----------------|-------|
| Stamped body panels | +/-0.2-0.5 mm | Class A surface (paint-ready) | Gap/flush +/-0.5 mm for closures |
| Engine block (cast + machined) | +/-0.01-0.025 mm (bore) | Ra 0.4-1.6 um (deck/bore) | Bore cylindricity 0.005 mm |
| Crankshaft | +/-0.005-0.01 mm (journals) | Ra 0.1-0.4 um | Runout 0.01 mm TIR |
| Transmission gears | +/-0.01-0.025 mm, AGMA 10-12 | Ra 0.2-0.8 um | Profile/lead/pitch critical |
| Cylinder bore (honed) | +/-0.005-0.01 mm diameter | Ra 0.2-0.8 um plateau | Crosshatch angle 40-50 deg |
| Die castings (structural) | +/-0.1-0.3 mm | Ra 1.6-6.3 um | Draft angles 1-3 deg |
| Forged crankshaft | +/-0.25-0.5 mm (as-forged), +/-0.005 mm (machined) | Ra 0.2-0.4 um (journals) | Flash line within 0.5 mm |

### 4.5 Regulatory Standards

| Standard | Scope |
|----------|-------|
| IATF 16949 | Quality management system for automotive (builds on ISO 9001 + AIAG requirements) |
| APQP (Advanced Product Quality Planning) | Product development process framework |
| PPAP (Production Part Approval Process) | Supplier part approval before production |
| FMEA (AIAG/VDA) | Failure mode and effects analysis |
| SPC (Statistical Process Control) | Process capability monitoring (Cpk >= 1.33 standard, >= 1.67 safety-critical) |
| MSA (Measurement Systems Analysis) | Gauge R&R studies |
| ISO 6892 | Tensile testing |
| ISO 4287 / ASME B46.1 | Surface roughness measurement |
| SAE J standards | Material and process specs (J434 -- ADI, J403 -- steel composition) |
| VDA 6.3 | Process audit standard (German OEM requirement) |
| CQI-9 | Special process: heat treat assessment |
| CQI-11 | Special process: plating assessment |
| CQI-12 | Special process: coating assessment |
| CQI-15 | Special process: welding assessment |
| CQI-27 | Special process: casting assessment |
| UN ECE regulations / FMVSS | Vehicle safety standards (crash, emissions) |
| Euro NCAP / IIHS | Crash testing and safety ratings |

---

## 5. Cross-Industry Comparison Matrix

### 5.1 Process Usage by Industry

| Process | Aerospace | Defense | Automobile |
|---------|-----------|---------|------------|
| **SUBTRACTIVE** | | | |
| 5-axis CNC milling | Primary | Heavy | Moderate (post-cast machining) |
| CNC turning | Heavy | Heavy | Heavy |
| Grinding (precision) | Heavy | Heavy | Heavy (crank/cam/gear) |
| Honing | Moderate | Moderate (barrels) | Primary (cylinder bores) |
| Lapping | Specialized | Specialized | Rare |
| Wire EDM | Heavy | Moderate | Moderate (tooling) |
| Sinker EDM | Heavy | Moderate | Heavy (die/mold making) |
| ECM | Specialized (turbine) | Rare | Rare |
| Broaching | Moderate | Moderate | Heavy (gears) |
| Gear cutting | Moderate | Moderate | Primary |
| **SHEET METAL** | | | |
| Laser cutting | Heavy | Heavy | Heavy |
| Plasma cutting | Moderate | Heavy | Moderate |
| Waterjet cutting | Heavy (composites) | Heavy | Moderate |
| Press brake bending | Moderate | Heavy | Moderate |
| Progressive stamping | Rare | Moderate | Primary (highest volume) |
| Deep drawing | Moderate | Moderate | Heavy |
| Hydroforming | Moderate | Moderate | Heavy (exhaust, chassis) |
| Stretch forming | Primary (skins) | Moderate | Rare |
| Roll forming | Moderate | Moderate | Heavy |
| **FORMING/FORGING** | | | |
| Closed die forging | Primary (Ti, Ni) | Heavy | Primary (steel) |
| Open die forging | Heavy (large parts) | Moderate | Moderate |
| Ring rolling | Primary (engine casings) | Moderate | Moderate (bearings) |
| Isothermal forging | Primary (Ti/Ni) | Rare | Rare |
| Superplastic forming | Specialized | Rare | Rare |
| Powder metallurgy | Moderate | Heavy (W penetrators) | Primary (50% of PM market) |
| MIM | Moderate | Moderate | Moderate |
| Cold heading | Moderate | Heavy (ammo) | Primary (fasteners) |
| Press hardening (hot stamp) | Rare | Rare | Primary (UHSS body) |
| **CASTING** | | | |
| Sand casting | Moderate | Heavy | Heavy (legacy engine blocks) |
| Investment casting | Primary (turbine) | Heavy (missile/guidance) | Moderate (turbo housings) |
| Single crystal casting | Primary (turbine blades) | N/A | N/A |
| HPDC | Moderate | Moderate | Primary (giga-casting trend) |
| Gravity/LP die casting | Moderate | Moderate | Primary (heads, knuckles) |
| Centrifugal casting | Specialized (rings, pipes) | Specialized | Rare |
| **JOINING** | | | |
| TIG welding | Primary | Heavy | Moderate |
| MIG/MAG welding | Moderate | Primary (vehicle hulls) | Heavy (chassis, exhaust) |
| Resistance spot welding | Rare | Rare | Primary (4000-6000/BIW) |
| Friction stir welding | Specialized (Al) | Specialized (Al armor) | Emerging (EV) |
| Electron beam welding | Primary (Ti, Ni) | Moderate | Rare |
| Laser welding | Heavy | Moderate | Primary (BIW, tailored blanks) |
| Brazing | Heavy | Heavy | Moderate |
| Riveting | Primary (100K+/aircraft) | Heavy | Moderate (SPR for mixed mat'l) |
| Adhesive bonding | Heavy | Heavy | Heavy (BIW, glass) |
| Diffusion bonding | Specialized (Ti SPF/DB) | Rare | Rare |
| **SURFACE TREATMENT** | | | |
| Anodizing | Primary | Heavy | Moderate (Al parts) |
| Hard chrome plating | Heavy (replacing w/ HVOF) | Primary (barrels) | Heavy (hydraulics) |
| HVOF thermal spray | Primary (landing gear) | Moderate | Moderate |
| Plasma spray TBC | Primary (turbine) | Rare | Rare |
| PVD/CVD coating | Heavy | Moderate | Heavy (tooling) |
| Shot peening | Primary (all fatigue-critical) | Heavy | Heavy (springs, gears) |
| Cadmium plating | Heavy (being phased out) | Primary | Banned (EU) |
| Phosphating | Moderate | Primary (Parkerizing) | Primary (pre-E-coat) |
| E-coat | Rare | Moderate | Primary (every BIW) |
| Powder coating | Moderate | Heavy | Heavy |
| **HEAT TREATMENT** | | | |
| Solution treatment + aging | Primary (Al, Ti, Ni) | Heavy | Heavy (Al castings) |
| Carburizing | Heavy (gears) | Heavy | Primary (trans gears) |
| Nitriding | Heavy (Ti, steels) | Heavy (barrels) | Moderate |
| Induction hardening | Moderate | Moderate | Primary (crank, cam) |
| Vacuum heat treatment | Primary | Moderate | Moderate |
| Cryogenic treatment | Moderate | Heavy (barrels) | Moderate |
| Press hardening (in-die quench) | N/A | N/A | Primary (B-pillars) |
| **COMPOSITES & ADDITIVE** | | | |
| AFP/ATL + autoclave | Primary | Heavy (missiles, UAVs) | Rare (supercars only) |
| RTM | Heavy (fan blades) | Heavy | Emerging (body panels) |
| Filament winding | Primary (pressure vessels) | Primary (motor cases) | Rare |
| DMLS/SLM | Primary (fuel nozzles) | Heavy (prototyping) | Emerging (prototyping) |
| EBM | Moderate | Moderate | Rare |
| WAAM | Emerging (Ti preforms) | Emerging (repair) | Rare |
| SMC/BMC compression molding | Rare | Moderate | Heavy (body panels) |
| **INSPECTION** | | | |
| CMM | Primary | Primary | Primary |
| UT/PAUT | Primary | Primary | Heavy |
| RT (radiography) | Primary (every weld) | Primary | Moderate |
| MPI | Primary | Primary | Heavy |
| DPI/LPI | Primary | Primary | Moderate |
| CT scanning | Heavy | Heavy | Emerging (castings) |
| Salt spray testing | Heavy | Primary | Primary |

### 5.2 Volume vs. Precision Comparison

| Dimension | Aerospace | Defense | Automobile |
|-----------|-----------|---------|------------|
| **Production volume** | 1-1,000 units/year | 100-100,000 units/year | 100,000-1,000,000+ units/year |
| **Tightest tolerance** | +/-0.001 mm (lapping) | +/-0.005 mm (optics, barrels) | +/-0.005 mm (crankshafts) |
| **Typical tolerance** | +/-0.01-0.05 mm | +/-0.025-0.1 mm | +/-0.01-0.5 mm (varies by part) |
| **Cost priority** | Performance/safety first | Performance/reliability first | Cost/volume first |
| **Cycle time priority** | Low (months-long processes OK) | Medium (days-weeks) | Critical (seconds per operation) |
| **Material waste tolerance** | Accepts high buy-to-fly ratio (10:1-20:1 for Ti) | Moderate | Minimal (cost-driven) |
| **Traceability** | Full per-part (serial # cradle-to-grave) | Full per-lot, per-part for critical | Lot-based, per-part for safety-critical |
| **NDT extent** | 100% of flight-critical parts | 100% of weapon-critical parts | Sample-based (AQL), 100% for safety-critical |

---

## 6. Regulatory Standards Summary

### 6.1 Quality Management Systems

| Industry | Primary QMS | Basis | Key Addition |
|----------|-------------|-------|-------------|
| Aerospace | AS9100D / IA9100 | ISO 9001:2015 | Configuration management, counterfeit parts prevention, zero tolerance for defects |
| Defense | AS9100D + CMMC + MIL-STD-11991B | ISO 9001:2015 + MIL-STDs | ITAR compliance, cybersecurity, domestic sourcing (DFARS) |
| Automobile | IATF 16949 | ISO 9001:2015 | APQP, PPAP, SPC (Cpk >= 1.33), FMEA |

### 6.2 Special Process Standards Comparison

| Process | Aerospace | Defense | Automobile |
|---------|-----------|---------|------------|
| Heat Treatment | Nadcap HT, AMS 2750 (pyrometry), AMS 2759 | MIL-H-6875, AMS 2759 | CQI-9 |
| Welding | Nadcap WLD, AWS D17.1/D17.2/D17.3 | MIL-STD-1595, AWS D17.1 | CQI-15, AWS D8.x |
| Surface Treatment | Nadcap, AMS 2447/2448, MIL-A-8625 (anodize) | MIL-STD-186, MIL-DTL-16232 | CQI-11, CQI-12 |
| NDT | Nadcap NDT, NAS 410 / EN 4179 | MIL-STD-2132, NAS 410 | CQI-spec, ASTM standards |
| Casting | Nadcap, AMS specs | MIL-C-xxxx series | CQI-27 |
| Composites | Nadcap Composites | MIL-HDBK-17 (CMH-17) | N/A (limited use) |

### 6.3 Material and Process Specification Families

| Specification Family | Issuing Body | Industry | Examples |
|---------------------|-------------|----------|----------|
| AMS (Aerospace Material Specification) | SAE International | Aerospace/Defense | AMS 2759 (heat treat), AMS 2432 (shot peening), AMS 5643 (17-4PH) |
| MIL-STD / MIL-DTL / MIL-PRF | US DoD | Defense | MIL-STD-186 (finishes), MIL-DTL-12560 (armor plate) |
| ASTM | ASTM International | All | ASTM A36 (structural steel), ASTM B209 (Al sheet), ASTM E8 (tensile test) |
| ISO | ISO | All (international) | ISO 2768 (general tolerances), ISO 8062 (casting tolerances) |
| AWS D-series | American Welding Society | All | AWS D17.1 (aerospace fusion weld), AWS D1.1 (structural steel weld) |
| SAE J-series | SAE International | Automotive | SAE J403 (steel chemical composition), SAE J434 (ADI) |
| AIAG standards | Automotive Industry Action Group | Automotive | APQP, PPAP, FMEA, MSA, SPC |
| CQI series | AIAG | Automotive | CQI-9 (heat treat), CQI-11 (plating), CQI-15 (welding), CQI-27 (casting) |
| VDA standards | Verband der Automobilindustrie | Automotive (German) | VDA 6.3 (process audit), VDA 6.5 (product audit) |

---

## Sources

- [Aerospace Manufacturing Strategies 2025 & Beyond](https://www.orcalean.com/article/aerospace-manufacturing-strategies:-how-to-improve-performance-in-2025-and-2026)
- [Top 6 Aerospace Component Manufacturing Processes](https://www.tuofa-cncmachining.com/tuofa-blog/aerospace-component-manufacturing-processes.html)
- [Defense Standardization Program](https://www.dsp.dla.mil/Specs-Standards/)
- [EverySpec - Military Standards](https://everyspec.com/)
- [Precision Machining for Military/Defense - Greno Industries](https://www.greno.com/news/precision-machining-specifications-military-defense-industries)
- [Automotive Manufacturing Process - Mitsubishi Manufacturing](https://www.mitsubishimanufacturing.com/automotive-manufacturing-process-explained/)
- [Toyota Virtual Plant Tour - Stamping](https://global.toyota/en/company/plant-tours/stamping/index.html)
- [Nadcap Accreditation - PRI](https://www.p-r-i.org/nadcap/accreditation)
- [Nadcap Requirements for Aerospace Steel Processing - MD Metals](https://www.mdmetals.com/2026/03/07/nadcap-requirements-aerospace-steel-processing/)
- [Nadcap Heat Treating Standards - Advanced Welding](https://blog.theperfectweld.com/nadcap-heat-treating)
- [Gun Barrel Manufacturing - DSIAC](https://dsiac.dtic.mil/technical-inquiries/notable/gun-barrel-manufacturing/)
- [Military Fabrication Guide - NAMF](https://www.namf.com/military-fabrication/)
- [Firearms and Defense Forging - Cornell Forge](https://www.cornellforge.com/markets/firearms-and-defense/)
- [Composites Manufacturing - Aerospace Engineering Blog](https://aerospaceengineeringblog.com/composite-manufacturing/)
- [Composite Manufacturing Methods - Explore Composites](https://explorecomposites.com/articles/design-for-composites/basics-manufacturing-methods/)
- [Metal Additive Manufacturing in Aerospace - ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0264127521005633)
- [Metal 3D Printing Technologies 2026 - UnionFab](https://www.unionfab.com/blog/2026/02/metal-3d-printing-technologies)
- [Metal 3D Printing in Aerospace - Skygens](https://www.skygens.com/the-ultimate-guide-to-metal-3d-printing-aerospace/)
- [Investment Casting for Turbine Blades - Allied Casting](https://alliedcasting.com/investment-casting-for-turbine-blades/)
- [Rolls-Royce Single Crystal Casting - The Engineer](https://www.theengineer.co.uk/content/in-depth/jewel-in-the-crown-rolls-royce-s-single-crystal-turbine-blade-casting-foundry)
- [Friction Stir Welding for Aerospace - Fraunhofer IWS](https://www.iws.fraunhofer.de/en/technologyfields/cutting-and-joining/component-design-and-special-technologies/special-joining-technologies/products_projects/friction_stir_welding_aerospace_applications.html)
- [Electron Beam Welding Aerospace - PTR Precision](https://www.ptreb.com/electron-beam-welding-applications/aerospace-welding)
- [AWS D17.3 FSW Specification](https://pubs.aws.org/p/2212/d173d173m2021-amd1-specification-for-friction-stir-welding-of-aluminum-alloys-for-aerospace-applications)
- [NDT in Aerospace - ASNT](https://www.asnt.org/what-is-nondestructive-testing/industries/aerospace)
- [Aerospace NDT Explained - Aerospace Testing International](https://www.aerospacetestinginternational.com/features/aerospace-ndt-explained.html)
- [PVD Coatings Replacing Hard Chrome - Advanced Manufacturing](https://www.advancedmanufacturing.org/industries/aerospace-defense/pvd-coatings-as-replacement-for-hard-chrome-on-components/article_d030176c-5256-11ef-9b29-378e1ef08714.html)
- [HVOF Coating of Landing Gears - Progressive Surface](https://www.progressivesurface.com/thermal-spraying-videos/hvof-coating-of-landing-gears/)
- [Shot Peening Aerospace Standards - Superior Shot Peening](https://superiorshotpeening.com/news/aerospace-thermal-coatings-longevity)
- [Defense Heat Treating - Thermal Modification Technologies](https://thermalmodtech.com/industries-served/defense-heat-treating/)
- [Ion Nitriding of Titanium - AHT Corp](https://www.ahtcorp.com/articles/blog/ion-nitriding-of-titanium-aerospace-armament-applications/)
- [Hydroforming for Military/Defense - FluidForming Americas](https://www.ffamericas.com/industries/military-defense)
- [Superplastic Forming - Argonne National Lab](https://publications.anl.gov/anlpubs/2008/01/60753.pdf)
- [AS9100 vs IATF 16949 - BPR Hub](https://www.bprhub.com/blogs/as9100-vs-iatf-16949)
- [ISO 9001 in 2026 - Quality Magazine](https://www.qualitymag.com/articles/99324-iso-9001-in-2026-whats-changingand-how-as9100-ia9100-iatf-16949-nist-and-cmmc-fit-together)
- [Automotive Die Casting Tolerances - NADCA](https://www.kineticdiecasting.com/NADCA-Product-Standards-for-Die-Casting.pdf)
- [Aerospace Castings - Frigate Manufacturing](https://frigate.ai/casting/aerospace-castings-materials-and-manufacturing-processes/)
- [Casting Tolerances ISO 8062 - DeZe Technology](https://casting-china.org/casting-tolerances/)
- [Powder Metallurgy in Automotive - IQS Directory](https://www.iqsdirectory.com/articles/powder-metal-parts/powder-metallurgy.html)
