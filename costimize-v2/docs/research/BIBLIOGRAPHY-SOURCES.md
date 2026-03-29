# Bibliography — Books, Papers & Sources for Cost Estimation
## Compiled March 29, 2026 (Updated: deep sweep of professors, papers, repos)

---

# PRIORITY ACQUISITION LIST (Top 12)

| # | Source | Why It's Priority | Get From | Est. Cost |
|---|--------|-------------------|----------|-----------|
| 1 | **Boothroyd — DFMA** (3rd ed, 2011) | Foundation of ALL process cost models. This IS the book your product automates | Amazon | ~Rs 8,000 |
| 2 | **Creese & Adithan — Estimating and Costing for Metal Manufacturing** (1992) | THE most directly relevant book. Chapter-by-chapter cost formulas for machining, casting, welding, forging. Generalized metal cutting economics model in appendix | Amazon/Routledge | ~Rs 6,000 |
| 3 | **Stephenson & Agapiou — Metal Cutting Theory and Practice** (3rd ed, 2016) | Chapter 13: Machining Economics and Optimization. Cost-per-part formulas, optimal speed derivation | Amazon | ~Rs 10,000 |
| 4 | **Kalpakjian & Schmid — Manufacturing Engineering and Technology** (8th ed, 2020) | Process capability charts, tolerance-cost relationships, 8 sections covering all processes | Amazon | ~Rs 5,000 |
| 5 | **Lembersky — Realistic Cost Estimating for Manufacturing** (3rd ed, SME, 2016) | Practitioner handbook since 1968. Process-by-process costing: machining, casting, stamping, forging, welding, plastics, finishing | SME | ~Rs 8,000 |
| 6 | **Lincoln Electric Procedure Handbook** (14th ed) | FREE. Welding cost bible. Cost per meter of weld by joint type | lincolnelectric.com | FREE |
| 7 | **ASM Vol. 16 — Machining** (2020) | Speed/feed tables for 100+ material grades | ASM International | ~Rs 15,000 |
| 8 | **Halevi & Weill — Principles of Process Planning** (1995) | THE CAPP book. 16 chapters: drawing → process selection → speed selection → machine selection → tool selection → costing. Full PDF available online | Springer / archive | FREE-ish |
| 9 | **Altan — Sheet Metal Forming** (2012) | Sheet metal physics + cost models. Blank size, tonnage, springback | Amazon | ~Rs 12,000 |
| 10 | **CMTI Machine Hour Rate Guide** | Indian-specific machine rates from Central Manufacturing Technology Institute, Bangalore | cmti-india.net | ~Rs 2,000 |
| 11 | **Shaw — Metal Cutting Principles** (2nd ed, 2005) | THE theoretical foundation. Cutting temperatures, chip formation, tool wear mechanisms, machining economics | Oxford UP | ~Rs 5,000 |
| 12 | **Ghosh & Mallik — Manufacturing Science** (2nd ed, 2010) | THE Indian textbook. Metal cutting, casting, forming, welding. Used at IITs. GATE/ESE standard | East-West Press | ~Rs 800 |

---

# BOOKS BY CATEGORY

## Metal Cutting Theory (The Big 5 — Professors' Books)

> **Key insight from research**: The "physics first, ML later" strategy is validated by a 2024 Taylor & Francis review ("Physics-based and data-driven hybrid modeling in manufacturing") which found hybrid models outperform pure ML with better transparency at lower computational cost.

| Book | Author | Year | What It Uniquely Provides | Status |
|------|--------|------|---------------------------|--------|
| **Metal Cutting Principles** | M.C. Shaw (Arizona State) | 2005 (2nd ed) | THE standard textbook. Physics of chip formation, cutting temperatures, shear angle theory, tool wear mechanisms, machining economics. "The standard textbook on metal-cutting" — American Machinist | **NOT READ** |
| **Metal Cutting** | E.M. Trent & P.K. Wright | 2000 (4th ed) | Metallurgical approach: seizure at tool-chip interface, diffusion wear, temperature distribution. Deep on WHY tools fail, not just WHEN | **NOT READ** |
| **Metal Cutting Mechanics** | Viktor P. Astakhov | 1998 | Challenges Merchant theory. Defines cutting as "purposeful fracture." Power = plastic deformation + tool-chip friction + tool-workpiece friction + new surface formation. Most advanced theoretical treatment | **NOT READ** |
| **Tribology of Metal Cutting** | Viktor P. Astakhov | 2006 | Friction and wear at tool interfaces. Critical for tool life prediction accuracy | **NOT READ** |
| **Metal Cutting Theory and Practice** | Stephenson & Agapiou (GM/Chrysler) | 2016 (3rd ed) | Ch.13: Machining Economics and Optimization. Industry practitioners' perspective. Cost-per-part optimization | **NOT READ** |

**Why these matter for our engine**: Our physics model uses simplified Merchant-type chip thickness correction (mc=0.25). Shaw and Astakhov would give us better power prediction models. Trent/Wright would improve tool wear prediction beyond simple Taylor V-T^n. Stephenson's Ch.13 has the most practical cost optimization formulas.

## Machining Economics & Cost Estimation

| Book | Author | Year | Key Data |
|------|--------|------|----------|
| **Estimating and Costing for Metal Manufacturing** | Creese & Adithan | 1992 | Generalized metal cutting economics model (appendix), process-by-process costing, overhead analysis, break-even. THE cost estimation textbook |
| **Realistic Cost Estimating for Manufacturing** (3rd ed) | Lembersky / SME | 2016 | Practitioner handbook. Machining, casting, stamping, forging, welding, plastics, finishing, electronics. End-of-chapter problems |
| **Cost Estimation: Methods and Tools** | Mislick & Nussbaum | 2015 | CER development, regression, learning curves, parametric methodology |
| **Production Economics** | Desai & Mital | 2017 | Costing of casting, forging, turning, milling, welding. Academic + MBA perspective |
| **Cost Analysis for Engineers and Scientists** | Tayyari | 2018 | 35+ years of teaching engineering economy and cost analysis |
| **Fundamentals of Machining and Machine Tools** | Boothroyd & Knight | 2005 | Chapters 8-10: machining economics gold standard |
| **DFMA — Product Design for Manufacture & Assembly** | Boothroyd, Dewhurst & Knight | 2011 | Cost models for machining, sheet metal, die casting, forging. 200K+ data points in commercial software |

## Manufacturing Processes (General Textbooks)

| Book | Author | Year | What It Uniquely Provides | Status |
|------|--------|------|---------------------------|--------|
| **Manufacturing Engineering and Technology** (8th ed) | Kalpakjian & Schmid | 2020 | THE comprehensive textbook. 8 sections: casting, forming, machining, joining, surface, microelectronics, MEMS, nano. Economics chapter. Taylor equation, Gilbert's optimal speed | **NOT READ** |
| **Fundamentals of Modern Manufacturing** (7th ed) | M.P. Groover | 2019 | Materials + processes + systems. Cycle time and cost analysis. Broader scope than Kalpakjian (includes electronics, AM) | **NOT READ** |
| **Manufacturing Science** (2nd ed) | Amitabha Ghosh & A.K. Mallik | 2010 | THE Indian textbook for IIT/NIT. Casting, forming, machining, joining, unconventional processes. Used for GATE exam | **NOT READ** |
| **Manufacturing Technology Vol 1 & 2** | P.N. Rao (IIT Delhi → Univ. of Northern Iowa) | 2019 (5th ed) | Indian author, used across Indian engineering colleges. Vol 1: Foundry, forming, welding. Vol 2: Metal cutting and machine tools. GATE questions included | **NOT READ** |
| Machinery's Handbook (30th ed) | Industrial Press | 2016 | **ALREADY EXTRACTED** — 50+ material tables, Kp, Taylor, tolerances |
| CNC Fundamentals | Autodesk/Titans | - | **ALREADY EXTRACTED** — SFM tables, feed rules |
| Walter Drilling/Threading | Walter Titex | 2009 | **ALREADY EXTRACTED** — 20+ material groups |
| Sandvik Training Handbook | Sandvik Coromant | 2017 | **ALREADY EXTRACTED** — kc1 values, power formulas, tool life |

## Process Planning (CAPP)

| Book | Author | Year | What It Uniquely Provides | Status |
|------|--------|------|---------------------------|--------|
| **Principles of Process Planning: A Logical Approach** | Halevi & Weill | 1995 | THE CAPP textbook. 16 chapters covering full pipeline: drawing interpretation → dimensioning → process selection → cutting speed selection → machine selection → tool selection. Full PDF found online | **NOT READ — PDF available** |
| **Setup Planning for Machining** | U.S. Dixit (IIT Guwahati) | 2015 | Setup planning algorithms. Directly relevant to our setup time estimation. 118 journal papers by author | **NOT READ** |
| **Computer-Aided Manufacturing** | Chang, Wysk & Wang | 2006 | Variant vs generative CAPP, process selection rules, operation sequencing algorithms | Referenced but not read |
| **Machining and CNC Technology** | Fitzpatrick | 2019 | CNC cycle time estimation, G-code analysis | Not read |

## Sheet Metal

| Book | Author | Year | Key Data |
|------|--------|------|----------|
| **Sheet Metal Forming: Fundamentals** | Altan & Tekkaya | 2012 | Blank size, K-factor, tonnage, springback |
| **Sheet Metal Forming Processes & Die Design** | Boljanovic | 2014 | Die cost estimation, strip layout, press selection |
| **Handbook of Die Design** | Suchy | 2006 | Die cost as f(complexity), die life, tryout costs |

## Casting

| Book | Author | Year | Key Data |
|------|--------|------|----------|
| **Casting Design and Performance** | ASM International | 2009 | Yields: sand 50-70%, investment 60-80%, die 30-50% |
| **Investment Casting** | Beeley | 2008 | Shell cost/layer, furnace cycles, wax injection |
| **Die Casting Engineering** | Andresen | 2005 | Die life (100K-1M shots), machine tonnage, cycle time |

## Forging

| Book | Author | Year | Key Data |
|------|--------|------|----------|
| **Forging** | Altan, Ngaile & Shen | 2005 | Force formulas, die life (5K-50K), flash weight |
| **ASM Vol. 14A: Metalworking — Bulk Forming** | ASM | 2005 | Forging temps, die materials, heating energy |

## Welding

| Book | Author | Year | Key Data |
|------|--------|------|----------|
| **Lincoln Electric Procedure Handbook** | Lincoln Electric | Latest | FREE. Cost/meter by joint type, deposition rates |
| **Welding Principles and Applications** | Jeffus | 2020 | Deposition rates kg/hr, electrode consumption |
| **AWS Welding Handbook Vol. 1** | AWS | 2001 | Weld economics, operator factor by process |

## Heat & Surface Treatment

| Book | Author | Year | Key Data |
|------|--------|------|----------|
| **ASM Vol. 4: Heat Treating** | ASM | 1991+ | Every process: cycle time, furnace, atmosphere |
| **Metal Finishing Guidebook** | Products Finishing | Annual | Bath chemistry costs, plating time, coverage |
| **Surface Treatment of Aluminium** | Wernick et al. | 2001 | Anodizing cost per sq dm by type |

## Composites & Additive

| Book | Author | Year | Key Data |
|------|--------|------|----------|
| **Composites Manufacturing** | Mazumdar | 2002 | Layup rates, autoclave costs, material waste |
| **Wohlers Report** | Wohlers Associates | Annual | AM machine hour rates, build time, material cost |
| **Additive Manufacturing Technologies** | Gibson, Rosen & Stucker | 2021 | Build time models, support waste, post-processing |

## Defense/Aerospace Specific

| Book | Author | Year | Key Data |
|------|--------|------|----------|
| **Aerospace Manufacturing Processes** | Saha | 2016 | NADCAP, cost multipliers (1.5-3x commercial) |
| AS9100 Rev D | SAE International | 2016 | Compliance adds 15-25% overhead |

## Indian Manufacturing Specific

| Source | Publisher | Key Data | Status |
|--------|-----------|----------|--------|
| **Manufacturing Science** | Ghosh & Mallik | THE Indian textbook, IIT standard | NOT READ |
| **Manufacturing Technology Vol 1 & 2** | P.N. Rao | Indian author, engineering college standard | NOT READ |
| **CMTI Machine Hour Rate Guide** | CMTI Bangalore | Indian-specific rates per Indian tax rules | Not obtained |
| **IMTMA Handbook** | IMTMA | Machine hour rates, utilization, regional costs | Not obtained |
| **CII Manufacturing Report** | CII | Cost benchmarking across sectors | Not obtained |
| **MSME Annual Report** | Govt. of India | Power costs, labour rates, MSME classification | Partially extracted |
| **BIS Standards** | Bureau of Indian Standards | IS 2062, IS 1570 Part 2 & 4 | **EXTRACTED** |
| **Totem Master Catalogue 2025** | Forbes Precision | Cutting speeds by ISO group, Indian tool data | **EXTRACTED** |
| IndiaMART / TradeIndia | Online | Real-time Indian material & component pricing | Available |

---

# KEY PAPERS

## Machining Cost Estimation

| Paper | Authors | Year | Finding | Status |
|-------|---------|------|---------|--------|
| Comprehensive review of cost estimation for machining | Yildiz et al. | 2020 | Reviews 50+ machining cost models | Referenced |
| ML-based cost estimation for machined parts | Ning et al. | 2024 | ML on features -> cost, compares with parametric | Referenced |
| Feature-based cost estimation review | Ben-Arieh & Qian | 2003 | Foundation for feature->cost mapping | Referenced |
| Systematic review of cost estimation techniques | Niazi, Dai & Balabani | 2006 | Taxonomy of 200+ papers into 4 methods | Referenced |
| **DXF geometric features + XGBoost -> 3.91% MAPE** | arXiv:2508.12440 | 2025 | **MOST RELEVANT** — 200 features from 13,684 DWG drawings, SHAP explainability, proves 2D drawing -> cost works | Referenced |
| Explainable AI for manufacturing cost estimation | Yoo & Kang (arXiv:2010.14824) | 2021 | 3D Grad-CAM shows WHICH features drive cost in CNC parts | Referenced |
| **Manufacturing cost from deep learning** | Ning et al. | 2020 | ResearchGate: DL-based machining cost from process data | **NEW** |
| **ML for costing sheet metals** | Springer 2024 | 2024 | ML approach specifically for sheet metal costing | **NEW** |
| **AI in cost estimation systematic review** | Various | 2024 | 39 papers 2016-2024; ANNs = 26.33% of studies; hybrid models best | **NEW** |

## Vision-Language Models for Engineering Drawings (2024-2025)

| Paper | Year | Finding | Status |
|-------|------|---------|--------|
| **From Drawings to Decisions: Hybrid VLF for 2D Drawing Parsing** | 2025 (arXiv:2506.17374) | Rotation-aware detector + lightweight VLM. 1,367 annotated mechanical drawings. Structured outputs for cost estimation | **NEW** |
| **Fine-Tuning VLM for Engineering Drawing Extraction** | 2024 (arXiv:2411.03707) | Florence-2 fine-tuned for GD&T. 52.4% F1 improvement over closed-source models | **NEW** |
| **Evaluating VLMs for Engineering Design** | 2025 (Springer AI Review) | Full design-to-manufacturing pipeline evaluation of VLMs | **NEW** |

## Physics-Based & Hybrid Models

| Paper | Year | Finding | Status |
|-------|------|---------|--------|
| **Physics-based and data-driven hybrid modeling in manufacturing** | 2024 (Taylor & Francis) | Hybrid physics+ML outperforms pure ML. Validates our "physics first, ML later" strategy | **NEW — key validation** |
| **Physics-based models for machining performance — critical review** | 2024 (ScienceDirect) | Reviews dynamic, tribological, thermo-mechanical interactions. Identifies gaps | **NEW** |
| **Milling parameter optimization via deep RL considering cost** | 2022 (J. Manufacturing Processes) | Deep RL optimizes milling params with cost as objective. 9-12% improvement | **NEW** |
| **Feature-Based and Process-Based Manufacturing Cost Estimation** | 2022 (MDPI Machines) | Feature+process estimation yields highest accuracy; requires accurate feature ID | **NEW** |

## LLM + Manufacturing (2024-2026 — Emerging Field)

| Paper | Authors | Year | Finding | Status |
|-------|---------|------|---------|--------|
| **ARKNESS — KG + LLM for CNC** | arXiv:2506.13026 | 2025 | **ALREADY READ** — 3B Llama + KG = GPT-4o accuracy for CNC process planning | Extracted |
| **CAPP-GPT — process planning from B-Rep** | 2025 | 2025 | **ALREADY READ** — feature->process mapping, hierarchical transformer | Extracted |
| **Large Language Models for Manufacturing** | arXiv:2410.21418 | 2024 | Survey: GPT-4V for manufacturing education, coding automation, robot control. Transformative potential across manufacturing | **NEW — read** |
| **LLM-based CAPP under Industry 5.0** | Tandfonline | 2025 | LLM transforms user descriptions into manufacturing task flows. Adaptive process management | **NEW** |
| **LLM-enabled Machining Process KG** | ScienceDirect | 2025 | Auto-constructs machining knowledge graphs. 48.6% faster, 46.4% cheaper than manual. DL + LLM integration | **NEW** |
| **LLMs for High-Level CAPP** | ScienceDirect | 2026 | >99% accuracy for process chain generation with only 5% training data. Distributed manufacturing | **NEW — most recent** |

## Feature Recognition & B-Rep Analysis

| Paper | Authors | Year | Finding | Status |
|-------|---------|------|---------|--------|
| AAGNet — B-Rep feature recognition | Wu et al. | 2024 | Open-source + 60K STEP dataset | Referenced |
| **BRepFormer — Transformer-based B-Rep** | arXiv:2504.07378 | 2025 | Transformer for B-Rep feature recognition. 93.16% on MFTRCAD, +3.28pp over previous SOTA | **NEW** |
| MFCAD++ | Colligan | 2022 | 59,665 labeled STEP files | Referenced |
| BrepMFR — Enhanced with domain adaptation | Zhangshuming | 2024 | Domain adaptation for cross-domain feature recognition | Referenced |
| ChatCNC — multi-agent RAG | Jeon | 2025 | 93.3% accuracy CNC monitoring | Referenced |

## Digital Twins for Machining

| Paper | Year | Finding | Status |
|-------|------|---------|--------|
| **DT + AI in Machining: Bibliometric Analysis** | 2024 | Comprehensive review of digital twin + AI for machining response prediction | **NEW** |
| **DT-driven machining quality characterization** | 2025 | Multi-scale quality characterization, current status and challenges | **NEW** |
| **Neural network cycle time prediction via DT** | 2025 | 90% accuracy for federate and cycle time prediction | **NEW** |
| **Hybrid mechanism-data CNC feed system DT** | 2025 | Error reduction from 0.0576mm to 0.0121mm via adaptive parameter updating | **NEW** |

## Sheet Metal

| Paper | Authors | Year | Finding |
|-------|---------|------|---------|
| Cost estimation for sheet metal using features | Verlinden et al. | 2008 | Feature->operation->cost for sheet metal |
| Laser cutting cost parametric model | Eltawahni et al. | 2013 | Gas consumption, nozzle wear, lens life |
| Nesting optimization review | Bennell & Oliveira | 2008 | Material utilization algorithms |

## Casting & Forging

| Paper | Authors | Year | Finding |
|-------|---------|------|---------|
| Sand casting cost framework | Chougule & Ravi (IIT Bombay) | 2006 | Feature-based, INDIAN context |
| Die life in hot forging | Gronostajski et al. | 2014 | Die cost = 15-30% of forging cost |
| Forging cost parametric model | Behrens et al. | 2018 | Die amortization + material + energy |

## Welding

| Paper | Authors | Year | Finding |
|-------|---------|------|---------|
| Cost estimation for welded structures | Klansek & Kravanja | 2006 | Geometry->time->cost model |

## Additive Manufacturing

| Paper | Authors | Year | Finding |
|-------|---------|------|---------|
| AM cost estimation systematic review | Costabile et al. | 2021 | Reviews 40+ AM cost models |
| CFRP cost model for AFP | Schubel | 2012 | Aerospace composite costs |

## Aerospace Specific

| Paper | Authors | Year | Finding |
|-------|---------|------|---------|
| Cost estimation in aerospace review | Layer et al. | 2002 | Learning curves, complexity factors |
| Parametric cost for aerospace composites | Curran et al. | 2006 | Qualification + certification costs |

---

# NEW GITHUB REPOS (Found in March 29 deep sweep)

These are repos NOT in our original 79-repo GITHUB-REPOS-SURVEY.md:

## Manufacturing Cost & Process Planning

| # | Repository | Stars | Language | Description | Relevance |
|---|-----------|-------|----------|-------------|-----------|
| 80 | [dimasthoriq/cnc-machining-time-estimation](https://github.com/dimasthoriq/cnc-machining-time-estimation) | ~1 | Python | Neural network for CNC milling time estimation. Published at Procedia CIRP 2024 | **HIGH** — ML approach to cycle time, our exact problem |
| 81 | [czhao33/Manufacturing-Process-Selection](https://github.com/czhao33/Manufacturing-Process-Selection-Using-Knowledge-Learned-from-Design-and-Manufacturing-Data) | 5 | — | Process selection using knowledge learned from design data | **HIGH** — automated process selection, our roadmap |
| 82 | [federicocoppa75/MachineSimulation.NET](https://github.com/federicocoppa75/MachineSimulation.NET) | 30 | C# | CNC machining simulation with 3D visualization | **MEDIUM** — time estimation validation |
| 83 | [harsh1702/Optimization-of-MRR-in-milling](https://github.com/harsh1702/Optimization-of-MRR-in-milling) | 2 | MATLAB | MRR optimization for thin-walled structures | **MEDIUM** — physics model reference |
| 84 | [boschresearch/CNC_Machining](https://github.com/boschresearch/CNC_Machining) | ~5 | — | Bosch Research: CNC process monitoring dataset | **HIGH** — industrial dataset from Bosch |
| 85 | [Mraut97/CNC_Machining_Calculator](https://github.com/Mraut97/CNC_Machining_Calculator) | 0 | HTML | Shop floor CNC calculator (RPM, feed, MRR, power) | **LOW** — basic but validates our formulas |
| 86 | [zibozzb/FeatureNet](https://github.com/zibozzb/FeatureNet) | ~10 | Python | FeatureNet implementation: 3D CNN for 24 machining features | **HIGH** — deep learning feature recognition |
| 87 | [kavinpuri/Manufacturing-Process-Advisor](https://github.com/kavinpuri/Manufacturing-Process-Advisor) | 0 | — | Automated process selection for sheet metal parts | **MEDIUM** — niche but directly relevant |

## Datasets

| # | Repository/Source | Description | Relevance |
|---|------------------|-------------|-----------|
| 88 | [Kaggle: CNC Turning Roughness & Tool Wear](https://www.kaggle.com/datasets/adorigueto/cnc-turning-roughness-forces-and-tool-wear) | AISI H13 steel turning: forces, roughness, wear data | **HIGH** — tool wear validation |
| 89 | [Kaggle: CNC Mill Tool Wear](https://www.kaggle.com/datasets/shasun/tool-wear-detection-in-cnc-mill) | Milling tool wear detection dataset | **HIGH** — ML training data |
| 90 | [Kaggle: Milling Tool Wear & RUL](https://www.kaggle.com/datasets/programmer3/milling-tool-wear-and-rul-dataset) | Remaining useful life prediction | **MEDIUM** — future ML feature |
| 91 | [makinarocks/awesome-industrial-machine-datasets](https://github.com/makinarocks/awesome-industrial-machine-datasets) | Curated list of industrial machine datasets | **HIGH** — meta-list for ML training data |

---

# OPEN-SOURCE TOOLS ON GITHUB

| Repo | What It Does | Why Relevant |
|------|-------------|-------------|
| **PythonOCC** (pythonocc-core) | Full B-Rep analysis in Python | STEP feature extraction — our roadmap |
| **CadQuery / Build123d** | Python CAD kernel, STEP parsing | Alternative to PythonOCC |
| **FreeCAD** | Open-source CAD + cost addons | Study feature recognition code |
| **OpenMDAO** | NASA optimization framework | Parametric cost modeling |
| **ezdxf** | DXF parsing in Python | ALREADY USING — dimension extraction |

---

# ONLINE RESOURCES

| Resource | URL | What It Provides |
|----------|-----|-----------------|
| Sandvik CoroPlus Tool Guide | sandvik.coromant.com/toolguide | Real-time Vc/fz for any tool+material |
| Kennametal NOVO | novo.kennametal.com | Tool selection + cutting data |
| Iscar Machining Calculator | iscar.com | Online machining calculator |
| Mitcalc | mitcalc.com | Engineering calculation sheets |
| CustomPartNet | custompartnet.com | Process cost estimators (basic) |
| aPriori eLearning | apriori.com | Should-cost methodology resources |
| Halevi & Weill PDF | alvarestech.com | Full "Principles of Process Planning" book online |
| MTConnect Standard | mtconnect.org | Open-source CNC data collection protocol. Real-time cycle times, spindle loads, feeds |
| STEP-NC (ISO 14649) | iso.org | Feature-based machining standard. Bi-directional CAD-CAPP-CAM-CNC data flow |
| NIST AMS 100-61 | nist.gov | "Economics of Digital Twins" — $37.9B annual impact, ABC methodology |

---

# OPEN DATASETS FOR ML PHASE

| Dataset | Source | What It Contains | Relevance |
|---------|--------|-----------------|-----------|
| **Purdue Cutting Sound** | GitHub: purduelamm/mt_cutting_dataset | CNC milling cutting sound, lab + industry | Tool wear / chatter detection |
| **Bosch CNC_Machining** | GitHub: boschresearch/CNC_Machining | Vibration data, 2kHz, 6 timeframes over 2 years | Process monitoring |
| **QIT-CEMC** (2024) | Nature Scientific Data | Ti6Al4V end milling, 68 samples, ~5M rows each | Tool wear lifecycle |
| **CNC Turning Forces/Wear** | Kaggle: adorigueto | AISI H13 turning: forces, roughness, wear | Tool life validation |
| **CNC Mill Tool Wear** | Kaggle: shasun | Michigan data. 18 experiments, wax blocks | ML benchmark |
| **Milling Tool Wear & RUL** | Kaggle: programmer3 | Remaining useful life prediction data | Future ML feature |
| **Manufacturing Cost** | Kaggle: vinicius150987 | Actual manufacturing cost data | **RARE** — cost dataset |
| **MFInstSeg** | GitHub: whjdark/AAGNet | 60,000+ STEP files with machining feature labels | Feature recognition training |
| **MFCAD++** | GitHub: hducg | 59,665 labeled STEP files | Feature recognition benchmark |
| **awesome-industrial-datasets** | GitHub: makinarocks | Curated meta-list of industrial ML datasets | Discovery |

---

# WHAT TO READ NEXT (Priority Order)

Based on gaps in our engine and what's freely available:

1. **Halevi & Weill** — Full PDF available. THE process planning reference. Will improve our process detection and sequencing logic.
2. **Ghosh & Mallik** — Rs 800 on Amazon India. Indian context, IIT standard, will give us Indian-relevant formulas and examples.
3. **P.N. Rao Vol 2** — Rs 500 on Amazon India. Metal cutting from Indian perspective, GATE-level problems useful for validation.
4. **Creese & Adithan** — The generalized metal cutting economics model in the appendix is exactly what we need.
5. **Shaw — Metal Cutting Principles** — Available on multiple PDF sites. Deepest theoretical treatment of chip formation and cutting temperatures.
6. **Stephenson Ch.13** — Machining economics optimization. Industry practitioners' cost-per-part formulas.
7. **Kalpakjian** — Process capability charts and tolerance-cost data we don't have yet.
8. **arXiv:2410.21418** — "Large Language Models for Manufacturing" survey (2024). Free on arxiv. Maps our exact approach.

---

# CADDI PATENT SOURCES

| Source | URL | What It Provides |
|--------|-----|-----------------|
| CADDi Drawer Patent Portfolio | https://caddi.com/info/20231116/ | Patent announcement + portfolio overview |
| CADDi x Plethora Patent Acquisition | https://caddi.com/press/20220720/ | Plethora auto-DFM/quote/CAM patents acquired Jul 2022 |
| CADDi Drawing Image Search | https://us.caddi.com/resources/insights/drawing-image-search | Similarity search product architecture description |
| CADDi Product Overview | https://us.caddi.com/product-overview | Full product capabilities + feature list |
| Fortune — CADDi $470M Valuation | https://fortune.com/2025/03/27/japanese-ai-startup-caddi-venture-capital-funding-atomico-supply-chain-optimization/ | Series C extension details, Atomico investment, $1B revenue target |
| CADDi Tech Blog — Engineering Culture | https://caddi.tech/2024/12/25/100000 | Engineering team size (150→300), Golang/Python stack, Kaggle Grandmasters |
| CADDi Functions Overview | https://caddi.com/en/functions/ | Drawer feature set: OCR, shape search, annotation management |

### Key Patents

| Patent # | Jurisdiction | Title |
|----------|-------------|-------|
| JP 7372697 | Japan | Similar drawing search device, method, and program |
| JP 7377565 | Japan | Drawing search device, database construction device, search system |
| EP 4546196A1 | Europe | Similar drawing retrieval by shape features |
| WO 2026004458A1 | PCT/International | Advanced similar drawing retrieval |
| JP 2023100170A | Japan | Drawing search via title column attributes |
| JP 2024113144A | Japan | Raster-to-vector with dimension recognition |
| WO 2026004078A1 | PCT/International | Component table extraction |
| WO 2026022945A1 | PCT/International | Drawing annotation management |

> Full analysis: [CADDI-PATENTS-DEEP-DIVE.md](../../../docs/research/CADDI-PATENTS-DEEP-DIVE.md)

---

*Bibliography updated March 29, 2026 after deep sweep of professors' books, recent papers, GitHub repos, and CADDi patent portfolio.*
