# GitHub Repositories Survey for Manufacturing Cost Estimation

> Surveyed March 29, 2026. 130+ repositories across 11 categories relevant to Costimize's AI-powered should-cost estimation tool.
> Updated: deep sweep added 40+ new repos from agent search + 4 Kaggle datasets across all tiers.

---

## Table of Contents

1. [Cost Estimation / Should-Cost](#1-cost-estimation--should-cost)
2. [Process Planning (CAPP)](#2-process-planning-capp)
3. [Machining Calculations & CNC Tools](#3-machining-calculations--cnc-tools)
4. [Engineering Drawing Analysis](#4-engineering-drawing-analysis)
5. [Material Databases](#5-material-databases)
6. [Manufacturing Process Databases & Knowledge](#6-manufacturing-process-databases--knowledge)
7. [ML for Manufacturing](#7-ml-for-manufacturing)
8. [Specific Process Calculators](#8-specific-process-calculators)
9. [CAD Kernels & Parametric Modeling](#9-cad-kernels--parametric-modeling)
10. [Curated Lists & Awesome Repos](#10-curated-lists--awesome-repos)

---

## 1. Cost Estimation / Should-Cost

> **Reality check:** There is no mature open-source should-cost tool. This is our opportunity.

| # | Repository | Stars | Language | Updated | Description | Relevance to Costimize |
|---|-----------|-------|----------|---------|-------------|----------------------|
| 1 | [Rutwik1000/Manufacturing-Cost-Estimation-Based-On-Deep-Learning](https://github.com/Rutwik1000/Manufacturing-Cost-Estimation-Based-On-Deep-Learning) | 5 | Python | 2025-09 | DL-based machining cost estimation with computer vision (SSDNet, PyTorch) | **HIGH** -- Direct competitor approach. Uses CV to read drawings and estimate cost. Study their model architecture |
| 2 | [clarks2022/Engineering-Design-Analysis-AI-App-for-Manufacturing](https://github.com/clarks2022/Engineering-Design-Analysis-AI-App-for-Manufacturing-) | 3 | -- | 2026-01 | Web platform for blueprint analysis, cost estimation, manufacturability | **HIGH** -- Very similar product concept. Review their approach to manufacturability assessment |
| 3 | [ahmadsalamifar/CostWise](https://github.com/ahmadsalamifar/CostWise) | 0 | JavaScript | 2026-02 | Web app for manufacturing cost estimation, recursive BOM management, online price updates | **HIGH** -- BOM management + price scraping, same pattern as our PCB/cable engines |
| 4 | [AlexandroBoldi/Industrial-Costing-Kernel](https://github.com/AlexandroBoldi/Industrial-Costing-Kernel) | 0 | -- | 2026-02 | Deterministic core for 2D manufacturing cost estimation with geometric traceability | **MEDIUM** -- Geometric-based costing approach, worth reviewing methodology |
| 5 | [rayaan95958/COST-ESTIMATION-TOOL-SANSERA](https://github.com/rayaan95958/COST-ESTIMATION-TOOL-SANSERA) | 0 | Python | 2025-03 | Cost estimation tool for aeronautical parts at Sansera Engineering | **MEDIUM** -- Indian aero manufacturer, directly relevant domain |
| 6 | [Top-Technologies/cost_estimation](https://github.com/Top-Technologies/cost_estimation) | 0 | Python | 2026-03 | Manual manufacturing cost estimation module | **LOW** -- Basic module, but recently active |
| 7 | [Taylor-C-Powell/Molecule_Builder](https://github.com/Taylor-C-Powell/Molecule_Builder) | 7 | Python | 2026-03 | Retrosynthesis, process engineering, cost estimation (chemical manufacturing) | **LOW** -- Different domain but interesting process-to-cost methodology |

#### Deep Sweep Additions (March 29 PM)

| # | Repository | Stars | Language | Description | Relevance to Costimize |
|---|-----------|-------|----------|-------------|----------------------|
| 93 | [kentavv/pymachining](https://github.com/kentavv/pymachining) | 5 | Python | Python machining calculations: `specific_cutting_force()`, MRR, feeds/speeds | **CRITICAL** -- Has actual cutting data & physics models. Most directly relevant library found |
| 94 | [Ownraza1214/mechforge](https://github.com/Ownraza1214/mechforge) | 0 | Python | Mechanical engineering package: `taylor_tool_life()`, `material_removal_rate()`, kc1=2000 default | **HIGH** -- Code-level overlap with our engine (Taylor + MRR + kc1) |
| 95 | [costiqtemp/costiq](https://github.com/costiqtemp/costiq) | 1 | Python | Laser cutting speed DB by material/thickness, blank-vs-laser process selector, test suite | **CRITICAL** -- Very close to our sheet metal engine. Suspiciously similar name to "costimize" |
| 96 | [rudloffl/sheet-metal-cost-calculator](https://github.com/rudloffl/sheet-metal-cost-calculator) | 5 | Jupyter | Predicts sheet metal part cost from DXF files | **HIGH** -- DXF-based sheet metal cost model, directly relevant |
| 97 | [jwerthen/Werco-ERP-MES](https://github.com/jwerthen/Werco-ERP-MES) | 0 | TypeScript | Manufacturing ERP with `get_laser_cutting_speed()`, laser speeds by gauge/material | **MEDIUM** -- Has laser cutting speed DB in quote calculator endpoint |
| 98 | [Gbspro/LaserCost-Pro](https://github.com/Gbspro/LaserCost-Pro) | 1 | TypeScript | CNC Laser Cost Calculator: DXF parsing, auto geometry (cut length, net area, scrap), Gemini AI quotes | **HIGH** -- DXF + laser cost + AI quotes. Directly comparable to our sheet metal flow |
| 99 | [abh21jay/EX-WORKS_PREDICTION](https://github.com/abh21jay/EX-WORKS_PREDICTION) | 0 | Python | ML machining cost predictor: `machining_cost = predicted_machining_time * 375.71` | **MEDIUM** -- Simple ML rate-based approach |
| 100 | [libracore/amf](https://github.com/libracore/amf) | 2 | Python | Manufacturing ERP with `machining_cost_per_minute = HOURLY_RATE / 60.0`, time-based costing | **MEDIUM** -- Rate-based machining cost model in production ERP |
| 101 | [emclab/jobshop_quotex](https://github.com/emclab/jobshop_quotex) | 0 | Ruby | Job shop quotation system: grinding_cost, heat_treat_cost, machining_cost, material_cost fields | **MEDIUM** -- Actual quotation system with cost breakdown matching ours |
| 102 | [xsession/r3ditor](https://github.com/xsession/r3ditor) | 0 | Rust | Complete CAM cost engine: `taylor_tool_life()`, `material_removal_rate()`, kc1.1, `machining_cost_cents` | **CRITICAL** -- Taylor + MRR + kc1.1 + cost all in one module. Best reference implementation |
| 103 | [DavidMaco/Supplier_Selection_Project](https://github.com/DavidMaco/Supplier_Selection_Project) | 0 | Python | Procurement analytics: should-cost modelling, Monte Carlo simulation, supplier scorecards. Streamlit + MySQL | **HIGH** -- Has should-cost module in same tech stack (Streamlit) |
| 104 | [shameel0505/CNC-Cost-Estimation-ACE](https://github.com/shameel0505/CNC-Cost-Estimation-ACE) | N/A | N/A | Data-driven CNC machining cost prediction using ML | **HIGH** -- ML-based CNC cost prediction, directly relevant |
| 105 | [ktruongme/Manufacturing-Cost-Estimation](https://github.com/ktruongme/Manufacturing-Cost-Estimation) | N/A | N/A | Airbus technical test: data science approach to manufacturing cost estimation | **HIGH** -- Enterprise approach to cost estimation via data science |
| 106 | [Jinal1996/Procurement-Cost-Analysis](https://github.com/Jinal1996/Procurement-Cost-Analysis) | 0 | N/A | Cost modeling, regression analysis, bottom-up cost estimation for procurement | **MEDIUM** -- Academic procurement cost analysis |
| 107 | [sidin-exos/exos-ux-replica](https://github.com/sidin-exos/exos-ux-replica) | N/A | TypeScript | Procurement tool with `should_cost_components` field, Kraljic matrix, supplier concentration | **MEDIUM** -- Shows procurement SaaS data model |

**Key finding:** The market is wide open. No repo above 10 stars does what we do. `costiqtemp/costiq` and `xsession/r3ditor` are the closest to production-grade cost engines but neither is complete. `kentavv/pymachining` has the best Python cutting data library.

---

## 2. Process Planning (CAPP)

| # | Repository | Stars | Language | Updated | Description | Relevance to Costimize |
|---|-----------|-------|----------|---------|-------------|----------------------|
| 8 | [nrjsingh1/CAPP_system](https://github.com/nrjsingh1/CAPP_system) | 7 | Python | 2024-11 | Computer Aided Process Planning system | **HIGH** -- Reference implementation for process sequence generation |
| 9 | [Hassan23121999/CAPP-Benchmarking-Tool](https://github.com/Hassan23121999/CAPP-Benchmarking-Tool) | 0 | Python | 2024-05 | Benchmarking tool for CAPP systems (accuracy, speed, interoperability) | **MEDIUM** -- Useful for validating our process detection against CAPP standards |
| 10 | [Lord-Turmoil/CAPP](https://github.com/Lord-Turmoil/CAPP) | 0 | C# | 2024-04 | Simple CAPP implementation | **LOW** -- Academic exercise but shows basic CAPP logic |
| 11 | [hanshiyingbing/numcraft](https://github.com/hanshiyingbing/numcraft) | 21 | Python | 2026-03 | Multi-Agent system for intelligent G-Code generation using LangGraph | **HIGH** -- AI agent approach to CNC process planning. Very relevant architecture pattern |

#### Deep Sweep Additions

| # | Repository | Stars | Language | Description | Relevance to Costimize |
|---|-----------|-------|----------|-------------|----------------------|
| 119 | [AJAY-P-37/MachineLearning-based-CAPP-Web](https://github.com/AJAY-P-37/MachineLearning-based-CAPP-Web) | 1 | Python | ML-based CAPP system in web UI (final year project) | **MEDIUM** -- ML approach to process planning |
| 120 | [connorkapoor/Palmetto](https://github.com/connorkapoor/Palmetto) | 19 | C++ | DFM workbench using LLMs + Attributed Adjacency Graphs for manufacturing algorithms | **HIGH** -- Most innovative approach found. LLM + AAG for DFM |

**Key finding:** CAPP is mostly trapped in academic papers, not code. numcraft (2026) shows LLM-agent approach. Palmetto (19 stars) shows the LLM + graph approach to DFM — worth studying.

---

## 3. Machining Calculations & CNC Tools

### G-Code Simulators

| # | Repository | Stars | Language | Updated | Description | Relevance to Costimize |
|---|-----------|-------|----------|---------|-------------|----------------------|
| 12 | [CauldronDevelopmentLLC/CAMotics](https://github.com/CauldronDevelopmentLLC/CAMotics) | 712 | C++ | 2026-03 | Open-source 3-axis CNC G-Code simulator (formerly OpenSCAM) | **MEDIUM** -- Understand toolpath simulation for time estimation validation |
| 13 | [filipecaixeta/cncwebsim](https://github.com/filipecaixeta/cncwebsim) | 93 | JavaScript | 2026-03 | Web-based CNC simulator (milling + lathe + 3D printer) | **LOW** -- Web CNC sim, could inspire UI for machining visualization |
| 14 | [Monksc/cncsim](https://github.com/Monksc/cncsim) | 14 | Rust | 2026-03 | Simulates G-Code from CNC router, converts to STL/PNG | **LOW** |
| 15 | [NCalu/NCviewer](https://github.com/NCalu/NCviewer) | 12 | HTML | 2026-01 | Online G-Code viewer and CNC simulator | **LOW** |

### Feeds & Speeds Calculators

| # | Repository | Stars | Language | Updated | Description | Relevance to Costimize |
|---|-----------|-------|----------|---------|-------------|----------------------|
| 16 | [dubstar-04/FeedsAndSpeeds](https://github.com/dubstar-04/FeedsAndSpeeds) | -- | Python | -- | FreeCAD CAM addon for feeds and speeds | **HIGH** -- Reference for cutting parameter calculation logic |
| 17 | [brturn/feeds-and-speeds](https://github.com/brturn/feeds-and-speeds) | -- | -- | -- | Optimizing feeds & speeds calculator for CNC milling with min/max ranges | **HIGH** -- Optimization approach to cutting params, relevant to our physics engine |
| 18 | [Cael-Verd/Machining-Calculators](https://github.com/Cael-Verd/Machining-Calculators) | -- | Python | -- | Python calculators for CNC machining (RPM, feedrate, MRR) | **HIGH** -- Direct Python reference for our cutting_data.py calculations |
| 19 | [bhowiebkr/CNC-ToolHub](https://github.com/bhowiebkr/Speeds-And-Feeds) | -- | -- | -- | Tool management app with feeds/speeds database | **MEDIUM** -- Tool library data structure reference |
| 20 | [cheltenhamhackspace/CncHelper](https://github.com/cheltenhamhackspace/CncHelper) | -- | -- | -- | Lightweight web app for CNC speeds and feeds | **LOW** |

### CNC Controllers & Firmware (Context)

| # | Repository | Stars | Language | Updated | Description | Relevance to Costimize |
|---|-----------|-------|----------|---------|-------------|----------------------|
| 21 | [grbl/grbl](https://github.com/grbl/grbl) | 6,131 | C | 2026-03 | The original open-source G-Code parser and CNC controller for Arduino | **LOW** -- Not directly useful but defines G-code standard we parse |
| 22 | [LinuxCNC/linuxcnc](https://github.com/LinuxCNC/linuxcnc) | 2,227 | Python | 2026-03 | Full CNC machine controller (mills, lathes, 3D printers, laser cutters) | **LOW** -- Industry-standard CNC controller, context for machine parameters |
| 23 | [burnshall-ui/vibeCNC](https://github.com/burnshall-ui/vibeCNC) | 3 | Python | 2026-02 | Fanuc-style CNC lathe simulator with AI-powered G-Code assistance (Claude + Ollama) | **MEDIUM** -- AI + CNC integration, interesting for future AI-assisted process planning |

#### Deep Sweep: CNC Tools & CAM

| # | Repository | Stars | Language | Description | Relevance to Costimize |
|---|-----------|-------|----------|-------------|----------------------|
| 121 | [nraynaud/webgcode](https://github.com/nraynaud/webgcode) | 415 | JavaScript | Online G-Code simulator with STM32 controller | **LOW** -- G-code parsing/visualization |
| 122 | [Heeks/heekscnc](https://github.com/Heeks/heekscnc) | 103 | C++ | HeeksCNC CAM with CuttingRate data (Brinell hardness to max MRR mapping) | **HIGH** -- Has cutting rate DB mapping material hardness to MRR |
| 123 | [dorisoy/Dorisoy.CNC-Simulator](https://github.com/dorisoy/Dorisoy.CNC-Simulator) | 21 | C# | .NET 8.0 CNC simulator with material removal, tool management | **LOW** |
| 124 | [Frikallo/NWSS-CNC](https://github.com/Frikallo/NWSS-CNC) | 11 | C++ | Open source 2D CNC CAM software | **LOW** |
| 125 | [bjstark07/CNC-Cycle-Time-Optimizer](https://github.com/bjstark07/CNC-Cycle-Time-Optimizer) | 0 | JavaScript | G-code upload, cycle time calculation, optimization | **HIGH** -- Has cycle time estimation from G-code |

### Cutting Force & Physics

| # | Repository | Stars | Language | Updated | Description | Relevance to Costimize |
|---|-----------|-------|----------|---------|-------------|----------------------|
| 24 | [Omkar-Kushare/Merchant-Theory-Formula](https://github.com/Omkar-Kushare/Merchant-Theory-Formula) | 0 | Python | 2026-02 | Merchant's Theory calculator: cutting forces, shear angle, friction, power | **HIGH** -- Directly validates our cutting_data.py physics formulas |

#### Deep Sweep: kc1 / Kienzle Implementations

Multiple repos implement the same Kienzle kc1.1 formula: `kc = kc11 * (hm/h0)^-mc * Kg * Kw`. Cross-validate our Sandvik kc1 values against these sources.

| # | Repository | Stars | Language | Description | Relevance to Costimize |
|---|-----------|-------|----------|-------------|----------------------|
| 108 | [KASUYASU/cutsim](https://github.com/KASUYASU/cutsim) | 40 | C++ | Cutting simulation with DEFAULT_SPECIFIC_CUTTING_FORCE=2000, power coefficient calcs | **HIGH** -- Cutting force simulation with material removal and power |
| 109 | [roslane07/conditions-coupe-app](https://github.com/roslane07/conditions-coupe-app) | 0 | Python | Cutting conditions calculator with `calculate_specific_cutting_force(kc1, hm, mc)` | **MEDIUM** -- kc1 cutting force calculation |
| 110 | [McMuff86/nc_feedrate](https://github.com/McMuff86/nc_feedrate) | 0 | Python | NC feedrate calculator with `calculate_specific_cutting_force(kc_1_1, hm, mc)` | **MEDIUM** -- Kienzle kc1.1 formula implementation |
| 111 | [TheMrFish3D/JustTheChip](https://github.com/TheMrFish3D/JustTheChip) | 0 | JavaScript | CNC Feeds & Speeds calculator with KC1 coefficients per material in constants.js | **HIGH** -- Material-specific KC1 database |
| 112 | [Cygnus-X2/milling_tools](https://github.com/Cygnus-X2/milling_tools) | 0 | JavaScript | Milling calculator with `specificCuttingForceKc = kc1_1 / (middleChipThickness ** mc)` | **MEDIUM** -- Kienzle formula implementation |
| 113 | [acornel5/Bayesian-stability-and-cutting-force](https://github.com/acornel5/Bayesian-stability-and-cutting-force) | 2 | MATLAB | Bayesian stability and cutting force modelling with uncertainty quantification | **MEDIUM** -- Research-grade cutting force model |
| 114 | [boothg599/FreeCAD-CAM-Addons](https://github.com/boothg599/FreeCAD-CAM-Addons) | 1 | Python | FreeCAD CAM experimental workbench with GPU-accelerated force kernel: kc=1200.0 (Al default) | **MEDIUM** -- GPU cutting force simulation for FreeCAD |
| 115 | [spanner888/CamScripts](https://github.com/spanner888/CamScripts) | 3 | Python | FreeCAD CAM scripts reading `UnitCuttingForce` from material props, complete Kienzle formula | **HIGH** -- Complete kc correction formula with all factors (Kg, Kw) |
| 116 | [LibreEngineer/LuaCAM](https://github.com/LibreEngineer/LuaCAM) | 3 | C | CAM library with material data referencing machiningdoctor.com kc1 values | **MEDIUM** -- Material cutting data structure |
| 117 | [ThomasVanRiel/OpenMachiningTechnology](https://github.com/ThomasVanRiel/OpenMachiningTechnology) | 0 | N/A | Documentation with Kronenberg plots, kc11=1680 N/mm² example, cutting data visualization | **LOW** -- Machining technology reference |
| 118 | [RhodosBerger/Krystal-stack-platform-framework](https://github.com/RhodosBerger/Krystal-stack-platform-framework) | 1 | Python | CNC copilot with synthetic data research, process planning, material-specific kc values | **MEDIUM** -- Has synthetic CNC data generation |

**Key finding:** The Kienzle kc1.1 formula is the de facto standard across all open-source machining tools. FreeCAD's `Machinability.yml` in a 30K-star project references machiningdoctor.com — worth cross-validating against our Sandvik kc1 data.

---

## 4. Engineering Drawing Analysis

### Drawing OCR & Extraction

| # | Repository | Stars | Language | Updated | Description | Relevance to Costimize |
|---|-----------|-------|----------|---------|-------------|----------------------|
| 25 | [W24-Service-GmbH/werk24-python](https://github.com/W24-Service-GmbH/werk24-python) | 85 | Python | 2026-03 | Commercial API for automated processing of technical drawings (dimensions, GD&T, tolerances, materials) | **CRITICAL** -- The gold standard for drawing extraction. 95%+ accuracy. Commercial but Python SDK is open. Study their API response structure |
| 26 | [Bakkopi/engineering-drawing-extractor](https://github.com/Bakkopi/engineering-drawing-extractor) | 75 | Python | 2026-03 | Automated data extraction from engineering blueprint images (OCR + OpenCV) | **HIGH** -- Open-source alternative to Werk24. Uses Tesseract + OpenCV for table/text extraction |
| 27 | [javvi51/eDOCr](https://github.com/javvi51/eDOCr) | -- | Python | -- | Packaged OCR system for mechanical engineering drawings (keras-ocr based) | **HIGH** -- Purpose-built ML OCR for engineering drawings, research paper backed |
| 28 | [saurabhkovoor/EngineeringDrawingAndTextExtraction](https://github.com/saurabhkovoor/EngineeringDrawingAndTextExtraction) | -- | Python | -- | Extraction of drawing regions and tabulated text from engineering drawings | **MEDIUM** -- Tesseract-based, simpler approach |
| 29 | [atharvayeole2023ainds-boop/Dimension_Extractor](https://github.com/atharvayeole2023ainds-boop/Dimension_Extractor) | 0 | Python | 2026-01 | Engineering drawing dimension extraction using OCR | **MEDIUM** -- Recent, focused on dimensions specifically |

### DXF/CAD File Parsing

| # | Repository | Stars | Language | Updated | Description | Relevance to Costimize |
|---|-----------|-------|----------|---------|-------------|----------------------|
| 30 | [mozman/ezdxf](https://github.com/mozman/ezdxf) | 1,244 | Python | 2026-03 | Python interface to DXF files (read/write/modify) | **CRITICAL** -- The standard Python DXF library. Essential for our DXF extraction pipeline |
| 31 | [jparedesDS/extract-data-dxf](https://github.com/jparedesDS/extract-data-dxf) | 19 | Python | 2026-03 | Extract entity data from DXF files for technical drawing analysis | **HIGH** -- Practical example of DXF entity extraction, directly applicable |
| 32 | [MadScrewdriver/qsketchmetric](https://github.com/MadScrewdriver/qsketchmetric) | 28 | Python | 2026-02 | 2D parametric DXF rendering CAD engine | **MEDIUM** -- Parametric DXF generation, useful for understanding DXF structure |
| 33 | [anjanadev96/STEPfileparser](https://github.com/anjanadev96/STEPfileparser) | -- | Python | -- | Converts STEP files to JSON with surface/hole info via pythonOCC | **HIGH** -- Exactly what we need for STEP parsing pipeline |

### STEP File Feature Detection

| # | Repository | Stars | Language | Updated | Description | Relevance to Costimize |
|---|-----------|-------|----------|---------|-------------|----------------------|
| 34 | [sguerin13/cad-feature-detection](https://github.com/sguerin13/cad-feature-detection) | 27 | Python | 2026-03 | Converts STEP files to Three.js via pythonOCC, detects manufacturing features with UV-Net | **CRITICAL** -- The closest thing to what we need: STEP -> feature detection -> manufacturing context. FastAPI + React frontend |
| 35 | [BrepMaster/CAD-Model-Classification-System](https://github.com/BrepMaster/CAD-Model-Classification-System) | 5 | Python | 2025-11 | PyQt5 + PythonOCC platform for STEP model classification using UV-Net | **HIGH** -- Full desktop app for CAD classification |
| 36 | [BrepMaster/3D-CAD-Analysis-System](https://github.com/BrepMaster/3D-CAD-Analysis-System) | 2 | Python | 2025-09 | STEP model classification AND segmentation using UV-Net + PyQt5 | **HIGH** -- Adds segmentation (face-level labeling) to classification |
| 37 | [zstar239/STEP-Thread-Hole-Inspection-Tool](https://github.com/zstar239/STEP-Thread-Hole-Inspection-Tool) | 1 | Python | 2026-02 | Auto-detects cylindrical thread holes in STEP files via PythonOCC | **HIGH** -- Specific feature detection (holes/threads) from STEP, directly useful for process detection |

#### Deep Sweep: STEP/Drawing Processing

| # | Repository | Stars | Language | Description | Relevance to Costimize |
|---|-----------|-------|----------|-------------|----------------------|
| 129 | [IfcOpenShell/step-file-parser](https://github.com/IfcOpenShell/step-file-parser) | 30 | Python | Pure Python ISO 10303-21 STEP file parser | **HIGH** -- Pure Python STEP parser for our STEP roadmap |
| 130 | [EltiganiHamad/Engineering-Drawing-Extraction](https://github.com/EltiganiHamad/Engineering-Drawing-Extraction) | N/A | Python | Image segmentation on engineering drawings to separate tabulated data from diagrams | **MEDIUM** -- Drawing extraction via image processing |
| 131 | [advaithh21/STEP-file-feature-recognition](https://github.com/advaithh21/STEP-file-feature-recognition) | N/A | N/A | STEP file feature recognition | **MEDIUM** -- Feature recognition from STEP |
| 132 | [DonSqualo/cascade-rs](https://github.com/DonSqualo/cascade-rs) | 2 | Rust | Pure Rust CAD kernel aiming for OpenCASCADE parity | **LOW** -- Future Rust-based STEP processing |

---

## 5. Material Databases

| # | Repository | Stars | Language | Updated | Description | Relevance to Costimize |
|---|-----------|-------|----------|---------|-------------|----------------------|
| 38 | [materialsproject/pymatgen](https://github.com/materialsproject/pymatgen) | 1,842 | Python | 2026-03 | Python Materials Genomics -- powers the Materials Project. Crystal structures, electronic structure, phase diagrams | **MEDIUM** -- Overkill for our needs (atomic-level), but the Materials Project API could source material property data |
| 39 | [hackingmaterials/matminer](https://github.com/hackingmaterials/matminer) | 578 | Python | 2026-03 | Materials data mining -- featurizers for compositions, structures. Connects to 40+ databases | **MEDIUM** -- Could generate material feature vectors for ML cost prediction models |
| 40 | [materialsproject/pymatgen-db](https://github.com/materialsproject/pymatgen-db) | 51 | Python | 2025-12 | MongoDB database addon for pymatgen -- Materials Project-style data management | **LOW** -- Database pattern reference |
| 41 | [ncfrey/resources](https://github.com/ncfrey/resources) | -- | -- | -- | Curated list of open-source materials informatics resources | **MEDIUM** -- Meta-list of materials databases and tools |

**Key finding:** pymatgen/matminer are materials science tools (crystal-level properties). For engineering materials (steel grades, aluminum alloys), we still need our own curated database. No open-source "engineering material property + cost" database exists.

---

## 6. Manufacturing Process Databases & Knowledge

| # | Repository | Stars | Language | Updated | Description | Relevance to Costimize |
|---|-----------|-------|----------|---------|-------------|----------------------|
| 42 | [slightlynybbled/tol-stack](https://github.com/slightlynybbled/tol-stack) | -- | Python | -- | Python tolerance stack-up analysis using Monte Carlo simulation | **MEDIUM** -- Relevant for tolerance-cost relationship modeling |
| 43 | [EinmalmitProfis/Statistical-Tolerance-Analysis-and-Synthesis-with-Python](https://github.com/EinmalmitProfis/Statistical-Tolerance-Analysis-and-Synthesis-with-Python) | -- | Python | -- | Statistical tolerance analysis, peer-reviewed paper implementation | **MEDIUM** -- Formal tolerance analysis approach |
| 44 | [CiphracoreSystems/kfactor](https://github.com/CiphracoreSystems/kfactor) | 0 | HTML | 2025-08 | Sheet metal K-factor and bend allowance calculator | **HIGH** -- Directly relevant to our sheet metal cost engine |
| 45 | [jonathanwvd/awesome-industrial-datasets](https://github.com/jonathanwvd/awesome-industrial-datasets) | -- | -- | -- | Curated collection of public industrial datasets | **MEDIUM** -- Source of training data for ML cost models |

**Key finding:** No open-source manufacturing process capability database exists. This is a moat opportunity -- build and open-source a process-tolerance-cost mapping database.

---

## 7. ML for Manufacturing

### Feature Recognition (B-Rep / Graph Neural Networks)

| # | Repository | Stars | Language | Updated | Description | Relevance to Costimize |
|---|-----------|-------|----------|---------|-------------|----------------------|
| 46 | [AutodeskAILab/UV-Net](https://github.com/AutodeskAILab/UV-Net) | ~133 | Python | -- | UV-Net: Learning from Boundary Representations (CVPR 2021). CNN on UV-grids from B-Rep faces/edges | **CRITICAL** -- State-of-the-art for learning geometry from STEP/B-Rep files. Foundation for any ML-based feature detection on CAD |
| 47 | [AutodeskAILab/BRepNet](https://github.com/AutodeskAILab/BRepNet) | ~56 | Python | -- | Topological message passing on solid models. Face segmentation for machining features | **CRITICAL** -- Directly classifies B-Rep faces into machining feature types. The backbone for our future STEP-based process detection |
| 48 | [whjdark/AAGNet](https://github.com/whjdark/AAGNet) | 122 | Python | 2026-03 | Attributed Adjacency Graph for automatic machining feature recognition from B-Rep | **CRITICAL** -- Best open-source machining feature recognition. 122 stars, actively maintained. Preserves topological + geometric + extended attributes |
| 49 | [zhangshuming0668/BrepMFR](https://github.com/zhangshuming0668/BrepMFR) | 64 | Python | 2026-03 | Enhanced machining feature recognition with deep learning and domain adaptation | **HIGH** -- Domain adaptation approach = generalizes better to real-world parts |
| 50 | [AndrewColligan/CADNet](https://github.com/AndrewColligan/CADNet) | 44 | -- | 2026-02 | Graph representation of 3D CAD models for machining feature recognition (PyTorch Geometric) | **HIGH** -- Academic paper code, graph neural network approach |
| 51 | [Seamus113/TGnet](https://github.com/Seamus113/TGnet) | 4 | Python | 2026-01 | Graph Neural + Transformer for multi-task machining feature recognition in B-Rep | **MEDIUM** -- Newest approach combining GNN + Transformer |
| 52 | [Davidlequnchen/VLM-CADFeatureRecognition](https://github.com/Davidlequnchen/VLM-CADFeatureRecognition) | 55 | Jupyter | 2026-03 | Manufacturing feature recognition using Vision-Language Models (VLMs) | **CRITICAL** -- VLM approach to feature recognition = our exact approach (using GPT-4o). Study their prompts and methodology |
| 53 | [zhenshihaowanlee/Self-supervised-BRep-learning-for-CAD](https://github.com/zhenshihaowanlee/Self-supervised-BRep-learning-for-CAD) | -- | -- | -- | Self-supervised representation learning for CAD models | **MEDIUM** -- Pre-training approach for B-Rep understanding |

#### Deep Sweep: ML for Manufacturing Cost & Tool Wear

| # | Repository | Stars | Language | Description | Relevance to Costimize |
|---|-----------|-------|----------|-------------|----------------------|
| 126 | [kidozh/keras_detect_tool_wear](https://github.com/kidozh/keras_detect_tool_wear) | N/A | Python | Tool wear prediction by residual CNN | **MEDIUM** -- ML for tool wear, relevant to tooling cost model |
| 127 | [kidozh/phm10-tool-wear-prediction](https://github.com/kidozh/phm10-tool-wear-prediction) | N/A | Python | PHM tool wear prediction revisit | **MEDIUM** -- Academic tool wear prediction |
| 128 | [abp15/aperion_local_agent](https://github.com/abp15/aperion_local_agent) | 0 | N/A | AI cost estimation for apparel: CNN + MobileNetV2 vector search for historical evidence retrieval | **HIGH** -- Dual-path architecture (prediction + similarity search) validates our estimate + historical PO comparison flow |

### Datasets

| # | Repository | Stars | Language | Updated | Description | Relevance to Costimize |
|---|-----------|-------|----------|---------|-------------|----------------------|
| 54 | [hducg/MFCAD](https://github.com/hducg/MFCAD) | 45 | Python | 2026-03 | Dataset of 15,488 3D CAD models with machining feature labels (STEP format) | **CRITICAL** -- The benchmark dataset for machining feature recognition. Generated with PythonOCC. Use for training/evaluation |
| 55 | [hducg/MFCAD_GNN](https://github.com/hducg/MFCAD_GNN) | 2 | Python | 2023-01 | GNN implementation on MFCAD dataset | **MEDIUM** |
| 56 | [LEO-SHAO020104/MFCAD-](https://github.com/LEO-SHAO020104/MFCAD-) | -- | -- | -- | MFCAD++ dataset (59,665 samples, extended version with more feature types) | **HIGH** -- Larger dataset version with more machining features |

---

## 8. Specific Process Calculators

### Sheet Metal: Nesting & Cutting

| # | Repository | Stars | Language | Updated | Description | Relevance to Costimize |
|---|-----------|-------|----------|---------|-------------|----------------------|
| 57 | [Jack000/SVGnest](https://github.com/Jack000/SVGnest) | 2,516 | JavaScript | 2026-03 | Open-source vector nesting using genetic algorithm + No-Fit Polygon | **HIGH** -- Gold standard for 2D nesting. Could integrate for sheet metal material utilization estimation |
| 58 | [Jack000/Deepnest](https://github.com/Jack000/Deepnest) | 1,073 | JavaScript | 2026-03 | Desktop nesting app for laser/plasma cutters. Based on SVGnest with C speed-critical code | **HIGH** -- Production-grade nesting with common-line merging |
| 59 | [deepnest-next/deepnest](https://github.com/deepnest-next/deepnest) | 143 | JavaScript | 2026-03 | Community fork of Deepnest, actively maintained | **MEDIUM** -- More active development than original |
| 60 | [VovaStelmashchuk/nest2D](https://github.com/VovaStelmashchuk/nest2D) | -- | Rust | -- | Nesting library migrated to Rust for performance | **LOW** |
| 61 | [phossystems/FuseNest](https://github.com/phossystems/FuseNest) | 36 | JavaScript | 2026-03 | Fusion360 add-in for nesting based on SVGnest | **LOW** |

### Welding & FEA

| # | Repository | Stars | Language | Updated | Description | Relevance to Costimize |
|---|-----------|-------|----------|---------|-------------|----------------------|
| 62 | [parallelworks/welding-model](https://github.com/parallelworks/welding-model) | -- | -- | -- | Thermomechanical welding simulation using CalculiX FEA solver | **LOW** -- More simulation than cost estimation |
| 63 | [CastillonMiguel/phasefieldx](https://github.com/CastillonMiguel/phasefieldx) | -- | Python | -- | Phase-field modeling framework (fracture, solidification) on FEniCSx | **LOW** -- Casting solidification simulation, academic |
| 64 | [slukiceng/CalcForge](https://github.com/slukiceng/CalcForge) | -- | Python | -- | Open-source Python engineering calculators (structural, mechanical, electrical) | **MEDIUM** -- Reference for engineering calculation patterns |

---

## 9. CAD Kernels & Parametric Modeling

> These are the foundational tools for our STEP parsing and 3D analysis pipeline.

| # | Repository | Stars | Language | Updated | Description | Relevance to Costimize |
|---|-----------|-------|----------|---------|-------------|----------------------|
| 65 | [FreeCAD/FreeCAD](https://github.com/FreeCAD/FreeCAD) | 29,847 | C++ | 2026-03 | Open-source parametric 3D CAD with CAM workbench | **MEDIUM** -- Reference for CAM toolpath generation and machining parameters |
| 66 | [CadQuery/cadquery](https://github.com/CadQuery/cadquery) | 4,710 | Python | 2026-03 | Python parametric CAD scripting based on OCCT (reads/writes STEP, DXF, STL) | **HIGH** -- Python STEP/DXF manipulation. Could use for programmatic part analysis |
| 67 | [Open-Cascade-SAS/OCCT](https://github.com/Open-Cascade-SAS/OCCT) | 2,275 | C++ | 2026-03 | Open CASCADE Technology -- the open-source 3D geometry kernel (STEP/IGES/BREP native) | **HIGH** -- The engine behind pythonocc, cadquery, FreeCAD. Understand its capabilities |
| 68 | [tpaviot/pythonocc-core](https://github.com/tpaviot/pythonocc-core) | 1,852 | SWIG | 2026-03 | Python bindings for OpenCASCADE -- full 3D CAD/CAM/CAE in Python | **CRITICAL** -- Our primary tool for STEP file analysis. All feature detection repos use this |
| 69 | [gumyr/build123d](https://github.com/gumyr/build123d) | 1,519 | Python | 2026-03 | Modern Python CAD library built on OpenCASCADE (cleaner API than CadQuery) | **MEDIUM** -- Nicer API than raw pythonocc for creating/analyzing geometry |
| 70 | [SolidCode/SolidPython](https://github.com/SolidCode/SolidPython) | 1,242 | Python | 2026-03 | Python frontend for OpenSCAD | **LOW** -- OpenSCAD based, less useful for manufacturing analysis |
| 71 | [partcad/partcad](https://github.com/partcad/partcad) | 442 | Python | 2026-03 | Package manager for CAD parts -- digital thread / TDP standard | **MEDIUM** -- Interesting for part library / reuse patterns |
| 72 | [Irev-Dev/curated-code-cad](https://github.com/Irev-Dev/curated-code-cad) | 311 | Python | 2026-03 | Curated list of code-CAD projects (CadQuery, OpenSCAD, build123d, etc.) | **MEDIUM** -- Meta-list of all programmatic CAD tools |
| 73 | [dubstar-04/TurningAddon](https://github.com/dubstar-04/TurningAddon) | -- | Python | -- | FreeCAD CNC turning addon | **MEDIUM** -- Turning-specific toolpath logic |
| 74 | [voneiden/ocp-freecad-cam](https://github.com/voneiden/ocp-freecad-cam) | -- | Python | -- | CAM for CadQuery/Build123d via FreeCAD Path workbench | **MEDIUM** -- Bridges parametric Python CAD to toolpath generation |

---

## 10. Curated Lists & Awesome Repos

| # | Repository | Stars | Language | Description | Relevance to Costimize |
|---|-----------|-------|----------|-------------|----------------------|
| 75 | [m2n037/awesome-mecheng](https://github.com/m2n037/awesome-mecheng) | 1,494 | -- | Curated mechanical engineering resources (software, databases, calculators, courses) | **HIGH** -- Master reference list. Contains links to FEA tools, material databases, calculators |
| 76 | [mhatalski/awesome-cnc](https://github.com/mhatalski/awesome-cnc) | 62 | -- | Curated CNC resources (software, hardware, learning) | **HIGH** -- CNC-specific tools and references |
| 77 | [Phreak87/Awesome-CNC](https://github.com/Phreak87/Awesome-CNC) | 23 | -- | CAD/CAM/CAE/FEM software list | **MEDIUM** -- Broader scope including CAE/FEM |
| 78 | [awesomelistsio/awesome-mechanical-engineering](https://github.com/awesomelistsio/awesome-mechanical-engineering) | -- | -- | Tools, platforms, resources for mechanical engineering | **MEDIUM** |
| 79 | [CadQuery/awesome-cadquery](https://github.com/CadQuery/awesome-cadquery) | -- | -- | CadQuery code and resources | **MEDIUM** |

---

## Priority Matrix

### Tier 1: Study Immediately (build or integrate)

These repos directly impact what we're building right now.

| Repo | Why | Action |
|------|-----|--------|
| **pythonocc-core** (1,852 stars) | Our STEP parsing engine | Already in our roadmap. Install and build STEP pipeline |
| **ezdxf** (1,244 stars) | Our DXF parsing engine | Already using/planned. Validate against extract-data-dxf examples |
| **AAGNet** (122 stars) | Best machining feature recognition | Study for future ML-based feature detection from STEP files |
| **UV-Net** (~133 stars) | Foundation for B-Rep learning | Pre-train on MFCAD dataset, use for feature embeddings |
| **VLM-CADFeatureRecognition** (55 stars) | VLM approach = our approach | Study prompts and methodology for GPT-4o feature extraction |
| **werk24-python** (85 stars) | API response structure for drawing extraction | Study their JSON schema as target for our extraction output |
| **MFCAD dataset** (45 stars) | Training/benchmark data | Download for evaluation of our process detection accuracy |
| **cad-feature-detection** (27 stars) | STEP -> UV-Net -> features app | Reference architecture for our STEP analysis pipeline |
| **kentavv/pymachining** (5 stars) | Python kc1, MRR, feeds/speeds library | Cross-validate our cutting_data.py against their formulas |
| **costiqtemp/costiq** (1 star) | Laser cutting speed DB + process selection | Compare sheet metal engine approaches |
| **xsession/r3ditor** (0 stars) | Complete CAM cost engine (Rust) | Best reference for Taylor + MRR + kc1 + cost in one module |
| **connorkapoor/Palmetto** (19 stars) | LLM + AAG for DFM | Study novel approach to AI-driven manufacturability |

### Tier 2: Port or Adapt (next 1-3 months)

| Repo | Why | Action |
|------|-----|--------|
| **SVGnest** (2,516 stars) | Sheet metal nesting for material utilization | Port nesting algorithm for sheet metal cost estimation |
| **engineering-drawing-extractor** (75 stars) | Open-source drawing extraction | Compare against our GPT-4o extraction; use as fallback |
| **IfcOpenShell/step-file-parser** (30 stars) | Pure Python STEP parser | Evaluate for STEP file support roadmap |
| **Heeks/heekscnc** (103 stars) | Brinell hardness → MRR mapping | Cross-reference cutting rate data |
| **rudloffl/sheet-metal-cost-calculator** (5 stars) | DXF-based sheet metal cost | Compare methodology with our sheet metal engine |
| **DavidMaco/Supplier_Selection_Project** | Should-cost + Monte Carlo in Streamlit | Study procurement analytics module |
| **abp15/aperion_local_agent** | Dual-path: prediction + similarity search | Validates our estimate + historical PO comparison architecture |
| **BrepMFR** (64 stars) | Enhanced feature recognition | Second-gen approach with domain adaptation |
| **CadQuery** (4,710 stars) | Cleaner STEP manipulation API | Consider using alongside/instead of raw pythonocc |
| **Machining-Calculators** | Python CNC calc reference | Validate our cutting_data.py formulas against these |
| **FeedsAndSpeeds** | Cutting parameter logic | Cross-reference with our Sandvik-based parameters |
| **numcraft** (21 stars) | Multi-agent G-Code generation | Architecture reference for AI-agent process planning |

### Tier 3: Reference & Learning

| Repo | Why |
|------|-----|
| **FreeCAD** (29,847 stars) | CAM workbench source for machining parameter reference |
| **CAMotics** (712 stars) | G-Code simulation for time estimation validation |
| **matminer** (578 stars) | Materials featurization for future ML models |
| **awesome-mecheng** (1,494 stars) | Master reference for mech eng resources |
| **tol-stack** | Tolerance analysis for tolerance-cost modeling |
| **kfactor** | Sheet metal bend allowance calculations |

---

## Gap Analysis: What Does NOT Exist on GitHub

These are opportunities where nothing adequate exists in open source:

1. **Should-cost estimation tool** -- No mature open-source alternative to aPriori. This is our core product.
2. **Engineering material cost database** -- pymatgen is atomic-level. No database maps steel/aluminum grades to market prices + machinability + density for manufacturing.
3. **Process-tolerance-cost mapping** -- No database links manufacturing processes to achievable tolerances and associated cost multipliers.
4. **Indian manufacturing rate database** -- No open data source for Indian job shop rates (machine hour rates, labour rates, overhead factors).
5. **Drawing-to-cost pipeline** -- No end-to-end system takes a 2D drawing PDF and outputs a should-cost breakdown. We are building this.
6. **BOM-to-cost with price scraping** -- CostWise is the only attempt, at 0 stars. Our PCB/cable engines are more complete.
7. **Historical PO matching for cost intelligence** -- No repo does this. Our PO parser + matcher is novel.

---

## Technology Stack Validation

Our current stack choices are validated by this survey:

| Our Choice | Validated By |
|-----------|-------------|
| **OpenAI GPT-4o for vision** | VLM-CADFeatureRecognition (55 stars) uses VLMs for feature recognition |
| **PythonOCC for STEP** | Every serious CAD ML repo (UV-Net, BRepNet, AAGNet, MFCAD) uses it |
| **Physics-based MRR/cutting data** | FeedsAndSpeeds, Machining-Calculators, Merchant-Theory all validate physics approach |
| **JSON for data storage** | CostWise, partcad, and most lightweight tools use JSON |
| **ezdxf for DXF** | 1,244 stars, the undisputed standard |
| **Streamlit for MVP** | Multiple engineering tools use Streamlit (though we're moving to Next.js) |

---

## 11. Deep Sweep Overflow (March 29 PM)

> Repos 80-92 from the initial sweep. 40+ additional repos from agent search have been merged into sections 1-9 above (repos 93-132).

### Manufacturing Cost & Process Planning

| # | Repository | Stars | Language | Description | Relevance |
|---|-----------|-------|----------|-------------|-----------|
| 80 | [dimasthoriq/cnc-machining-time-estimation](https://github.com/dimasthoriq/cnc-machining-time-estimation) | ~1 | Python | Neural network for CNC milling time estimation. Published Procedia CIRP 2024 | **HIGH** -- ML cycle time estimation |
| 81 | [czhao33/Manufacturing-Process-Selection](https://github.com/czhao33/Manufacturing-Process-Selection-Using-Knowledge-Learned-from-Design-and-Manufacturing-Data) | 5 | -- | Process selection using knowledge from design data | **HIGH** -- automated process selection |
| 82 | [federicocoppa75/MachineSimulation.NET](https://github.com/federicocoppa75/MachineSimulation.NET) | 30 | C# | CNC machining simulation with 3D visualization | **MEDIUM** |
| 83 | [harsh1702/Optimization-of-MRR-in-milling](https://github.com/harsh1702/Optimization-of-MRR-in-milling) | 2 | MATLAB | MRR optimization for thin-walled structures | **MEDIUM** |
| 84 | [boschresearch/CNC_Machining](https://github.com/boschresearch/CNC_Machining) | ~5 | -- | Bosch Research CNC process monitoring dataset | **HIGH** -- industrial dataset |
| 85 | [Mraut97/CNC_Machining_Calculator](https://github.com/Mraut97/CNC_Machining_Calculator) | 0 | HTML | Shop floor CNC calculator | **LOW** |
| 86 | [zibozzb/FeatureNet](https://github.com/zibozzb/FeatureNet) | ~10 | Python | FeatureNet: 3D CNN for 24 machining features | **HIGH** |
| 87 | [kavinpuri/Manufacturing-Process-Advisor](https://github.com/kavinpuri/Manufacturing-Process-Advisor) | 0 | -- | Automated process selection for sheet metal | **MEDIUM** |

### Feature Recognition (2025 additions)

| # | Repository | Stars | Description | Relevance |
|---|-----------|-------|-------------|-----------|
| 88 | BRepFormer (arXiv:2504.07378) | -- | Transformer-based B-Rep feature recognition, 93.16% on MFTRCAD (+3.28pp SOTA) | **CRITICAL** -- newest SOTA for feature recognition |

### Datasets (Kaggle + GitHub)

| # | Source | Description | Relevance |
|---|--------|-------------|-----------|
| 89 | [Kaggle: CNC Turning Roughness & Wear](https://www.kaggle.com/datasets/adorigueto/cnc-turning-roughness-forces-and-tool-wear) | AISI H13 turning: forces, roughness, wear | **HIGH** |
| 90 | [Kaggle: CNC Mill Tool Wear](https://www.kaggle.com/datasets/shasun/tool-wear-detection-in-cnc-mill) | Milling tool wear detection | **HIGH** |
| 91 | [Kaggle: Milling Tool Wear & RUL](https://www.kaggle.com/datasets/programmer3/milling-tool-wear-and-rul-dataset) | Remaining useful life prediction | **MEDIUM** |
| 92 | [makinarocks/awesome-industrial-machine-datasets](https://github.com/makinarocks/awesome-industrial-machine-datasets) | Curated industrial machine datasets | **HIGH** -- meta-list |

---

### Key Findings from Deep Sweep

1. **No open-source should-cost tool exists at scale.** Confirmed again. `costiqtemp/costiq` and `xsession/r3ditor` are closest but neither is production-grade.
2. **Kienzle kc1.1 is the de facto standard.** Found in 8+ repos: pymachining, mechforge, r3ditor, CamScripts, nc_feedrate, milling_tools, JustTheChip, FreeCAD. Our Sandvik kc1 data should be cross-validated against these.
3. **FreeCAD's Machinability.yml** in a 30K-star project is the most authoritative open-source kc1 data source (references machiningdoctor.com).
4. **Dual-path architecture validated.** `abp15/aperion_local_agent` uses CNN prediction + similarity search for historical evidence — mirrors our planned estimate + PO comparison flow.
5. **ML gap confirmed.** Tool wear prediction has 20+ repos, surface roughness has several, but cost prediction from drawings has near-zero ML implementations. Our physics-first + ML-correction strategy is differentiated.

---

*Survey conducted March 29, 2026. 132 repos catalogued. Searched via GitHub API (search_repositories), GitHub Topics, web search, and agent-driven deep sweep across curated awesome-lists and keyword combinations.*
