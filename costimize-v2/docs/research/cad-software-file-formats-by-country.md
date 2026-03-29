# CAD Software & File Formats by Country: Research for Format Support Prioritization

**Date:** 2026-03-28
**Purpose:** Inform which file formats Costimize should support for should-cost estimation
**Focus:** What formats do procurement teams ACTUALLY send to suppliers?

---

## Executive Summary: What to Support First

**Priority 1 (Must-have for launch):**
- **PDF** -- the universal drawing format. Every procurement team sends PDFs. This IS the contractual document.
- **STEP (.stp/.step)** -- the universal 3D exchange format. Industry standard for geometry sharing.

**Priority 2 (High value, covers 80%+ of use cases):**
- **DXF** -- 2D drawing exchange, dominant for sheet metal/laser cutting
- **DWG** -- AutoCAD native, massive install base especially in India

**Priority 3 (Future differentiation):**
- **SLDPRT/SLDASM** -- SolidWorks native (13-14% global market share, dominant in SME manufacturing)
- **IGES (.igs/.iges)** -- legacy 3D exchange, still sent by older shops
- **X_T/.x_b** -- Parasolid kernel format (shared by SolidWorks, Siemens NX, Solid Edge)

**Priority 4 (Enterprise/niche):**
- Native formats: CATIA (.CATPart), Creo (.prt), Siemens NX (.prt)
- Chinese formats: CAXA native, ZW3D native

---

## 1. Global CAD Software Market Share

### Overall Market (2025)

| Software | Market Share | Users | Primary Use |
|----------|-------------|-------|-------------|
| AutoCAD (Autodesk) | ~37-39% | 10.7M+ | 2D drafting, general purpose |
| SolidWorks (Dassault) | ~12-14% | 4.6M | Mechanical design, SME manufacturing |
| CATIA (Dassault) | ~5-8% | -- | Automotive, aerospace, complex surfaces |
| Siemens NX | ~5-7% | -- | Automotive, aerospace, shipbuilding |
| Creo/Pro-E (PTC) | ~4-6% | -- | Large enterprises, defense |
| Fusion 360 (Autodesk) | Growing fast | -- | SME, startups, hobbyist-to-pro |
| Inventor (Autodesk) | ~3-4% | -- | Manufacturing, mechanical |

**Sources:** 6sense CAD market share data; Enlyft AutoCAD vs SolidWorks comparison; Grand View Research 3D CAD market report.

### Regional CAD Market Size (2025, Asia-Pacific)

| Country | Market Size (USD) | APAC Share | CAGR |
|---------|------------------|------------|------|
| China | $2,194M | 31.2% | 7.8% |
| Japan | -- | 16.1% | -- |
| India | $1,103M | 14.25% | 7.9% |
| South Korea | -- | 11.5% | -- |
| Taiwan | -- | 1.53% | -- |
| SE Asia (aggregate) | -- | 7.05% | -- |

**Source:** Cognitive Market Research, CAD Software Market Report 2026.

---

## 2. CAD Software by Country

### India (Primary Target Market)

**Dominant software:**
- **AutoCAD** -- by far the most widely used. Ubiquitous in 2D drafting. Many small shops use it (or pirated copies/free alternatives).
- **SolidWorks** -- growing rapidly, ~3 of 10 manufacturing companies use it. Popular in mechanical design and product development.
- **CATIA** -- used in automotive (Tata Motors, Mahindra) and aerospace (HAL, DRDO). Majorly used for complex surfacing.
- **Creo/Pro-E** -- used in larger enterprises. Legacy install base.

**SME/Job Shop reality:**
- Many small manufacturers still work from **2D PDF printouts**. They may not have any CAD software.
- AutoCAD piracy has been historically widespread (documented in Autodesk vs Deshmukh, 2011 Indian court case).
- Free alternatives gaining traction: FreeCAD, LibreCAD for basic 2D work.
- Fusion 360 adoption growing due to low cost and integrated CAD/CAM.
- **Bureau of Indian Standards (BIS) SP 46:2003** governs engineering drawing practices.

**What Indian job shops RECEIVE from customers:**
- **PDF drawings** -- the overwhelming majority. Printed or emailed. This is the baseline.
- **DWG/DXF** -- from customers who use AutoCAD. Common for sheet metal.
- **STEP files** -- from more sophisticated OEMs and design houses.
- **Native SolidWorks files** -- from companies using SolidWorks.
- Many small job shops work from **hand-drawn sketches** or **WhatsApp photos of drawings**.

### China

**Dominant software:**
- **CAXA** -- China's largest domestic CAD vendor. Brand awareness >50% among Chinese manufacturers. Largest market share in China's CAD/CAM software market.
- **ZW3D/ZWCAD** -- domestic alternative, 1.4M+ users in 90+ countries. Growing as cost-effective AutoCAD alternative.
- **AutoCAD** -- still widely used, especially for 2D.
- **SolidWorks** -- popular in SME manufacturing.
- **CATIA / NX** -- used by automotive OEMs (SAIC, BYD, etc.) and aerospace.

**Notable:** China is actively promoting domestic CAD software (CAXA, ZWCAD) as part of technology self-sufficiency. Government procurement increasingly favors domestic vendors.

**Formats received by Chinese shops:**
- PDF, DWG, DXF dominate
- STEP for 3D parts
- CAXA native format within domestic supply chains

### USA

**Dominant software:**
- **SolidWorks** -- most popular for mechanical design in SMEs
- **AutoCAD** -- ubiquitous for 2D and general drafting
- **Siemens NX** -- automotive (GM, Ford), aerospace (Boeing)
- **CATIA** -- aerospace (Lockheed Martin), automotive
- **Creo** -- defense, heavy machinery
- **Fusion 360** -- startups, maker economy, small shops
- **Onshape** -- cloud-native, gaining traction

**What US shops receive:**
- **STEP + PDF** is the gold standard for RFQs
- Online platforms (Xometry, Protolabs, Hubs) accept: STEP, STP, SLDPRT, STL, DXF, IPT, X_T, CATPART, PRT, SAT, 3MF, JT
- STEP is overwhelmingly preferred for instant quoting

### Germany

**Dominant software:**
- **Siemens NX** -- home market advantage. Dominant in automotive (BMW, Mercedes-Benz, VW) and industrial machinery.
- **CATIA** -- used in automotive and aerospace alongside NX.
- **SolidWorks** -- popular in Mittelstand (SME manufacturers).
- **AutoCAD** -- 2D drafting.
- **Inventor** -- used in mechanical engineering firms.

**Notable:** Germany's Spanflug (now part of Xometry) built a CNC quoting platform that accepts STEP files as the primary format.

### Japan

**Dominant software:**
- **Fujitsu iCAD SX** -- high market share in machinery and production equipment design. Japan-specific.
- **CATIA** -- used by Toyota, Nikon, Mitsubishi for automotive and precision engineering.
- **Siemens NX** -- used in some automotive and heavy manufacturing.
- **AutoCAD** -- 2D drafting still very common.
- **SolidWorks** -- growing adoption.

**Notable:** Japan's manufacturing culture is heavily production-engineering focused. Many companies were slow to adopt 3D CAD and still rely heavily on 2D drawings. The industry phrase is "CAM/CAD" rather than "CAD/CAM" -- manufacturing drives the design process.

### South Korea

**Dominant software:**
- **Siemens NX + Teamcenter** -- massive adoption. Hyundai Shipbuilding group signed a 10,000-user deal with Siemens for NX-based ship design CAD.
- **CATIA** -- automotive (Hyundai Motor, Kia).
- **AutoCAD Mechanical** -- Hyundai Heavy Industries Offshore division uses ~200 licenses.
- **SolidWorks** -- SME segment.

### Taiwan

**Dominant software:**
- **SolidWorks** -- widely used in electronics and mechanical components manufacturing.
- **AutoCAD** -- 2D drafting for PCB-related mechanical design.
- **Siemens NX / CATIA** -- used by larger enterprises.

**Notable:** Taiwan's manufacturing is heavily electronics-focused (TSMC, Foxconn). EDA tools (Cadence, Synopsys) dominate semiconductor design, not mechanical CAD. For mechanical enclosures and components, SolidWorks and AutoCAD are standard.

### Vietnam

**Dominant software:**
- **AutoCAD** -- most widely used due to familiarity and availability.
- **Autodesk Inventor** -- some companies transitioning from 2D to 3D.
- **ZWCAD** -- adopted by manufacturing companies as a lower-cost alternative to AutoCAD.

**Notable:** Vietnam's manufacturing sector is growing rapidly but still heavily 2D-oriented. Many shops work from PDF drawings sent by foreign customers (Japanese, Korean, US companies outsourcing).

### Mexico

**Dominant software:**
- **SolidWorks** -- popular in automotive supply chain (serving US OEMs).
- **AutoCAD** -- ubiquitous for 2D.
- **CATIA / NX** -- in automotive tier-1 suppliers following OEM requirements.

**Notable:** Mexico's manufacturing is heavily integrated with US supply chains. Formats follow US practices (STEP + PDF).

### Turkey

**Dominant software:**
- **AutoCAD** -- widely used for 2D drafting.
- **SolidWorks** -- growing adoption in machinery manufacturing.
- **ZWCAD** -- adopted by some manufacturers as cost-effective alternative.

---

## 3. Native File Formats by CAD Software

| CAD Software | 3D Native | 2D Native | Assembly | Kernel |
|-------------|-----------|-----------|----------|--------|
| AutoCAD | .dwg | .dwg, .dxf | N/A | ShapeManager |
| SolidWorks | .sldprt | .slddrw | .sldasm | Parasolid |
| CATIA V5/V6 | .CATPart | .CATDrawing | .CATProduct | CGM |
| Siemens NX | .prt | .prt | .prt | Parasolid |
| Creo/Pro-E | .prt | .drw | .asm | Granite |
| Fusion 360 | .f3d | -- | .f3d | -- (cloud) |
| Inventor | .ipt | .idw, .dwg | .iam | ShapeManager |
| FreeCAD | .FCStd | -- | .FCStd | OpenCascade |
| CAXA | .exb (2D), proprietary 3D | .exb | -- | ACIS |
| ZWCAD/ZW3D | .dwg (2D), .z3 (3D) | .dwg | .z3 | Overdrive |
| Solid Edge | .par | .dft | .asm | Parasolid |
| Onshape | Cloud-only | Cloud-only | Cloud-only | Parasolid |

### Universal Exchange Formats

| Format | Extension | Type | Standard | Notes |
|--------|-----------|------|----------|-------|
| STEP | .stp, .step | 3D solid | ISO 10303 | Gold standard for 3D exchange. Keeps exact geometry. No feature history. |
| IGES | .igs, .iges | 3D surface | ANSI Y14.26M | Legacy predecessor to STEP. Still used. Surface-only (no solids). |
| Parasolid | .x_t, .x_b | 3D solid | Siemens | Shared kernel for SolidWorks, NX, Solid Edge. Excellent fidelity. |
| DXF | .dxf | 2D | Autodesk (open) | Universal 2D exchange. Nearly all CAD can read/write. |
| DWG | .dwg | 2D/3D | Autodesk (proprietary) | AutoCAD native. De facto standard for 2D. |
| STL | .stl | 3D mesh | -- | 3D printing only. No dimensions/tolerances. Useless for cost estimation. |
| PDF | .pdf | Document | ISO 32000 | Universal for drawings with dimensions, GD&T, notes. THE contractual document. |
| 3D PDF | .pdf | 3D in doc | PRC/U3D | Embeds 3D model in PDF. Rare but growing. |
| JT | .jt | 3D | Siemens/ISO 14306 | Lightweight 3D visualization. Used in automotive PLM. |
| QIF | .qif | 3D + PMI | ANSI/DMSC | Quality information. Emerging standard. |
| 3MF | .3mf | 3D mesh | 3MF Consortium | Modern STL replacement. Gaining adoption. |

---

## 4. What Procurement Teams ACTUALLY Send for Quoting

### The Universal Truth

**PDF is king.** Across every country, every company size, every industry -- the 2D PDF engineering drawing is the most commonly sent format for quoting. This is because:

1. **Everyone can open it** -- no CAD software needed
2. **It's the legal/contractual document** -- tolerances, GD&T, notes, material callouts
3. **It can be printed** -- shop floor workers read paper drawings
4. **It's hard to modify** -- reduces accidental changes

### Format Hierarchy by Sophistication

| Sender Type | What They Send | Format |
|-------------|---------------|--------|
| Large OEM (auto, aero) | 3D model + 2D drawing | STEP + PDF (or native CAD) |
| Mid-size manufacturer | 2D drawing, sometimes 3D | PDF, maybe DXF/STEP |
| Small company / startup | 2D drawing | PDF, sometimes DXF |
| Indian SME procurement | 2D drawing | PDF (email/WhatsApp) |
| Online quoting platform | 3D model required | STEP (primary) |
| Sheet metal / laser | 2D flat pattern | DXF |
| PCB / cable assembly | Bill of Materials | Excel/CSV + PDF |

### Industry-Specific Patterns

**CNC Machining (most relevant for Costimize):**
- Best practice: STEP (.stp) + PDF drawing
- The STEP provides geometry for CAM programming
- The PDF provides tolerances, surface finish, material, notes
- Many shops quote from PDF alone, especially for simpler parts
- Some shops can quote from STEP alone for basic geometries

**Sheet Metal:**
- DXF is the dominant format (flat pattern for laser/waterjet)
- PDF for bend notes, tolerances
- STEP for 3D reference

**PCB Assembly:**
- Gerber files for bare board fabrication
- BOM in Excel/CSV for component sourcing
- Pick-and-place file for assembly
- PDF for assembly drawings

**Cable Assembly:**
- BOM in Excel/CSV
- PDF drawing for routing and connector pinout

### What Online Manufacturing Platforms Accept

| Platform | Primary Format | All Accepted Formats |
|----------|---------------|---------------------|
| Xometry | STEP | STEP, STP, SLDPRT, STL, DXF, IPT, X_T, X_B, 3DXML, CATPART, PRT, SAT, 3MF, JT |
| Protolabs/Hubs | STEP | STEP, SLDPRT, IPT, X_T, CATPART, SAT (no STL for CNC) |
| eMachineShop | Multiple | STEP, DXF, DWG, STL |
| Spanflug (Germany) | STEP | STEP + PDF |
| Komacut | STEP | STEP + PDF drawing |

---

## 5. Recommendations for Costimize

### Immediate Priority (Launch MVP)

**Support PDF first.** Rationale:
- 100% of procurement teams can produce PDFs
- Indian SME job shops primarily receive PDFs
- You already have AI vision extraction working on PDFs (GPT-4o / Gemini)
- PDF is the contractual document with tolerances and GD&T
- Lowest barrier to adoption

### Phase 2 (After launch)

**Add STEP file support.** Rationale:
- Universal 3D exchange format
- Required by all online manufacturing platforms
- Enables automated geometry extraction (no AI vision needed)
- Gives precise dimensions, volumes, surface areas
- Every CAD tool can export STEP

**Add DXF support.** Rationale:
- Essential for sheet metal quoting
- Universal 2D exchange format
- Programmatic parsing (no AI needed for geometry)
- Huge volume of sheet metal work in Indian manufacturing

### Phase 3 (Differentiation)

**Add native SolidWorks (.sldprt) support.** Rationale:
- 14% global market share, dominant in SME manufacturing
- Feature tree gives manufacturing intent (not just geometry)
- Shows you're serious about engineering workflows
- Can extract material, mass, volume directly

**Add DWG support.** Rationale:
- AutoCAD has 37% market share
- Dominant in India specifically
- Many legacy drawings exist only as DWG

### Not Worth Supporting (for now)

- **STL** -- mesh format, no dimensions or tolerances. Useless for cost estimation.
- **Native CATIA/NX/Creo** -- enterprise formats requiring expensive SDKs. These companies send STEP externally.
- **CAXA native (.exb)** -- relevant only for Chinese domestic market.
- **3D PDF** -- still rare, complex to parse.
- **IGES** -- legacy, largely replaced by STEP. Low priority.

---

## Sources

- [6sense - SolidWorks Market Share](https://6sense.com/tech/cad-software/solidworks-market-share)
- [Enlyft - AutoCAD vs SolidWorks Market Share](https://enlyft.com/resources/autocad-vs-solidworks-worldwide-market-share-compared)
- [Cognitive Market Research - CAD Software Market Report](https://www.cognitivemarketresearch.com/cad-software-market-report)
- [BOEN Rapid - File Formats for CNC Machining Quotes](https://blog.boenrapid.com/what-file-formats-are-required-for-cnc-machining-quotes)
- [Komacut - CNC Machining Drawing Guidelines](https://www.komacut.com/blog/cnc-machining-drawing-guidelines/)
- [Xometry - Preparing DXF Files](https://www.xometry.com/resources/sheet/preparing-dxf-files/)
- [Xometry Pro - File Formats for Manufacturing](https://xometry.pro/en/articles/file-formats-manufacturing/)
- [GaugeHow - CAD File Types Explained](https://gaugehow.com/cad/cad-file-types)
- [Capvidia - Top Neutral 3D CAD File Formats](https://www.capvidia.com/blog/top-neutral-3d-cad-file-formats)
- [3D-Tool - CAD Formats and Versions](https://www.3d-tool.com/en-cad-viewer-formats.htm)
- [Wevolver - Understanding CAD File Types](https://www.wevolver.com/article/understanding-cad-file-types-a-comprehensive-guide-for-digital-design-and-hardware-engineers)
- [ManufactureNow India - Top CAD/CAM for Manufacturing SMEs](https://www.manufacturenow.in/blogs/cad-cam-software-for-manufacturing)
- [Quora - SolidWorks vs Creo in India](https://www.quora.com/Which-CAD-software-is-mostly-preferred-in-India-SolidWorks-or-Creo)
- [SolidWorks Supplier Guide India - Linz Technologies](https://www.linztechnologies.in/post/solidworks-supplier-guide-where-businesses-can-buy-cad-software)
- [CADENAS - CAXA as China's Most Important CAD Manufacturer](https://www.cadenas.de/en/news/chinas-most-important-cad-software-manufacturer-caxa-relies-on-cadenas-partcommunity)
- [FirstMold - 10 Most Used CNC Software in Chinese Plants](https://firstmold.com/guides/cnc-software/)
- [ZWSOFT - About](https://www.zwsoft.com/about/)
- [Design News - In Japan it's CAM/CAD](https://www.designnews.com/design-software/in-japan-it-s-cam-cad-not-cad-cam)
- [Fujitsu iCAD SX](https://www.fujitsu.com/global/solutions/industry/manufacturing/monozukuri/productline-fjicad-sx/)
- [Siemens - Hyundai Heavy Industries Digital Shipyard](https://plm.automation.siemens.com/global/en/our-story/customers/hyundai-heavy-industries-shipbuilding/16002)
- [Engineering.com - Siemens Win in Shipbuilding](https://www.engineering.com/siemens-strikes-gold-again-in-cad-and-plm-with-a-big-win-in-shipbuilding/)
- [Protolabs Network/Hubs - Uploading CAD Files](https://www.hubs.com/help-center/ordering-custom-parts/1-uploading-parts/uploading-cad-files/)
- [Xometry Community - Accepted File Types](https://community.xometry.com/kb/articles/643-what-file-types-does-xometry-accept)
- [CNCPor - Quoting from 2D Drawings Only](https://cncpor.com/can-cnc-machining-be-quoted-from-2d-drawings-only/)
- [Protolabs Network - How to Prepare Technical Drawing](https://www.hubs.com/knowledge-base/how-prepare-technical-drawing-cnc-machining/)
- [Dragon Metal - Production-Ready Drawings for Offshore Manufacturing](https://dragonmetal.com.au/blog/production-ready-drawings-for-offshore-manufacturing-how-to-prepare-and-avoid-costly-errors/)
- [OpenBOM - Sharing CAD Derivatives with Suppliers](https://www.openbom.com/blog/3-reasons-openbom-helps-to-streamline-cad-files-derivatives-pdf-step-dxf-sharing-with-your-supplier)
- [RCO Engineering - Most Used CAD Software in Manufacturing](https://www.rcoeng.com/blog/most-used-cad-software)
- [New System Vietnam - Comparison of CAD Software in Manufacturing](https://newsystemvietnam.com/en/comparison-of-cad-software-in-the-manufacturing-industry)
- [CADDi - Procurement RFQ Process](https://us.caddi.com/resources/insights/request-for-quotation)
- [Grand View Research - 3D CAD Software Market](https://www.grandviewresearch.com/industry-analysis/3d-cad-software-market)
- [Autodesk - Korean Manufacturer Implementation](https://investors.autodesk.com/news-releases/news-release-details/korean-manufacturer-implements-powerful-autodesk-design-and)
- [CAD Interop - Creo Data Interoperability](https://www.cadinterop.com/en/formats/cad-systems/creo.html)
- [PTC - Creo File Types Overview](https://support.ptc.com/help/creo/ced_modeling/r20.6.0.0/en/ced_modeling/OSDM_Main/Files_Types.html)
