---
slug: bibliography
title: Bibliography and Reference Index
keywords: bibliography, references, Sandvik, Kennametal, Machinery's Handbook, Boothroyd, DFMA, CMTI, BIS, DINOv2, ColPali, Qwen, Pactum, CADDi, Taylor tool life, cutting data, cost models, Indian manufacturing
sources: BIBLIOGRAPHY-SOURCES.md
updated: 2026-04-04
---

# Bibliography and Reference Index

Concise index of sources used to build Newton-Metre's cost estimation engine, organized by category. Priority acquisition list and status included.

## 1. Cutting Data and Machining Physics

| Source | Key Data | Status |
|--------|----------|--------|
| **Machinery's Handbook** (30th Ed, Industrial Press, 2016) | 50+ material cutting speed tables (HSS + carbide), Kp power constants for 30+ materials, Taylor V*T^n=C, Gilbert's economic cutting speed, IT grade tolerances by process, surface roughness by process, total cost formula CTOT | **Extracted** |
| **Sandvik Coromant Training Handbook** (2017) | kc1 specific cutting force values for 9 materials, power formula Pc=(vc*ap*fn*kc)/(60*10^3), tool life factors, insert selection rules | **Extracted** |
| **Kennametal NOVO** | Unit power constants for 16 AISI material grades, carbide grade compositions, grooving/parting speeds for all ISO groups, machinability factors | **Extracted** |
| **Walter Titex Drilling/Threading** (2009) | Drilling time = depth/(f*n), tapping time = 2*depth/(pitch*n), 20+ material groups with Vc and f by drill diameter, core hole formulas | **Extracted** |
| **Fundamentals of CNC Machining** (Autodesk/Titans) | RPM = (SFM*3.82)/Dia, milling speeds for 6 materials, stepover/stepdown rules, tap/drill charts | **Extracted** |
| **Metal Cutting Principles** (M.C. Shaw, 2005) | Theoretical foundation: cutting temperatures, chip formation, tool wear mechanisms, machining economics | Not read |
| **Metal Cutting Theory and Practice** (Stephenson & Agapiou, 2016) | Ch.13: Machining Economics and Optimization. Cost-per-part formulas, optimal speed derivation | Not read |
| **ASM Vol. 16 -- Machining** (2020) | Speed/feed tables for 100+ material grades | Not obtained |

## 2. Cost Models and Estimation Methods

| Source | Key Data | Status |
|--------|----------|--------|
| **DFMA** (Boothroyd, Dewhurst & Knight, 3rd ed, 2011) | Foundation of ALL process cost models. Part cost = Material + (Process Time * Rate) + (Tooling/Volume) + Secondary. 200K+ data points in commercial software. Chapters 8-10: machining economics gold standard | Not read |
| **Estimating and Costing for Metal Manufacturing** (Creese & Adithan, 1992) | THE most directly relevant book. Chapter-by-chapter cost formulas for machining, casting, welding, forging. Generalized metal cutting economics model in appendix | Not read |
| **Realistic Cost Estimating for Manufacturing** (Lembersky/SME, 3rd ed, 2016) | Practitioner handbook since 1968. Process-by-process costing: machining, casting, stamping, forging, welding, plastics, finishing | Not read |
| **Manufacturing Engineering and Technology** (Kalpakjian & Schmid, 8th ed, 2020) | Process capability charts, tolerance-cost relationships, Taylor equation, Gilbert's optimal speed | Not read |
| **Cost Estimation: Methods and Tools** (Mislick & Nussbaum, 2015) | CER development, regression, learning curves, parametric methodology | Referenced |

## 3. Indian Manufacturing Data

| Source | Key Data | Status |
|--------|----------|--------|
| **CMTI Machine Hour Rate Guide** (CMTI Bangalore) | Indian-specific machine rates per Indian tax rules. #1 Indian-specific resource | Not obtained |
| **BIS Standards** (Bureau of Indian Standards) | IS 2062 (structural steel), IS 1570 Part 2 & 4 (alloy steels). BIS-to-ISO grade cross-references | **Extracted** |
| **Totem Master Catalogue 2025** (Forbes Precision) | Cutting speeds by ISO material group, Indian tool data | **Extracted** |
| **Manufacturing Science** (Ghosh & Mallik, 2nd ed, 2010) | THE Indian textbook (IIT/NIT standard, GATE exam). Casting, forming, machining, joining | Not read |
| **Manufacturing Technology Vol 1 & 2** (P.N. Rao, 5th ed, 2019) | Indian author, used across Indian engineering colleges | Not read |
| **MSME Annual Report** (Govt. of India) | Power costs, labour rates, MSME classification | Partially extracted |
| **SIAM Auto Industry Report** | 31M vehicles produced, 43L PV sold, regional hub mapping for component demand | Extracted |

## 4. Process-Specific References

### Sheet Metal
| Source | Key Data |
|--------|----------|
| **Sheet Metal Forming: Fundamentals** (Altan & Tekkaya, 2012) | Blank size, K-factor, tonnage, springback |
| **Handbook of Die Design** (Suchy, 2006) | Die cost as f(complexity), die life, tryout costs |

### Casting and Forging
| Source | Key Data |
|--------|----------|
| **Casting Design and Performance** (ASM, 2009) | Yields: sand 50-70%, investment 60-80%, die 30-50% |
| **Forging** (Altan, Ngaile & Shen, 2005) | Force formulas, die life (5K-50K), flash weight |
| Sand casting cost framework (Chougule & Ravi, IIT Bombay, 2006) | Feature-based, Indian context |

### Welding
| Source | Key Data |
|--------|----------|
| **Lincoln Electric Procedure Handbook** (14th ed) | FREE. Cost/meter by joint type, deposition rates. Welding cost bible |
| **AWS Welding Handbook Vol. 1** (2001) | Weld economics, operator factor by process |

### Heat and Surface Treatment
| Source | Key Data |
|--------|----------|
| **ASM Vol. 4 -- Heat Treating** (1991+) | Every process: cycle time, furnace, atmosphere |
| **Metal Finishing Guidebook** (Products Finishing, annual) | Bath chemistry costs, plating time, coverage |

### Process Planning
| Source | Key Data |
|--------|----------|
| **Principles of Process Planning** (Halevi & Weill, 1995) | THE CAPP book. 16 chapters: drawing interpretation through costing. Full PDF available online |

## 5. AI/ML Papers

### Vision and Embedding Models
| Paper | Year | Key Finding |
|-------|------|-------------|
| **DINOv2** (Meta) | 2023 | Self-supervised ViT-B/14, 768-dim. 64% visual similarity accuracy (2.3x better than CLIP's 28%) |
| **ColPali** (Faysse et al.) | 2024 | Page-image retrieval beats OCR+text pipelines |
| **ColFlor** | 2025 | 174M params, 17x smaller than ColPali, 1.8% quality drop. Fits 8GB for defense on-prem |
| **SigLIP 2** (Google) | 2025 | Multi-task pretraining, beats CLIP at all scales |
| **Matryoshka Representation Learning** | 2022/2024 | 14x smaller embeddings at same accuracy. 768-dim retains 99.5% of 3072-dim quality |

### Engineering Drawing Extraction
| Paper | Year | Key Finding |
|-------|------|-------------|
| Fine-tuning VLM for drawing extraction (arXiv:2411.03707) | 2024 | Florence-2 on 400 drawings: +52% F1, -43% hallucination vs GPT-4o |
| Hybrid VLF for 2D drawing parsing (arXiv:2506.17374) | 2025 | YOLOv11-obb + VLM on 1,367 annotated drawings |
| **Qwen2.5-VL-7B** | 2025 | 95.7 DocVQA, 864 OCRBench -- beats GPT-4o on document understanding |

### Manufacturing Cost ML
| Paper | Year | Key Finding |
|-------|------|-------------|
| ML cost from 2D drawings (arXiv:2508.12440) | 2025 | XGBoost on 13,684 DWG files, 200 features, MAPE 3.91-18.51% |
| Explainable AI for cost (arXiv:2010.14824) | 2020 | 3D CNN + 3D Grad-CAM on 1,006 voxelized parts |
| Physics-ML hybrid review (Taylor & Francis) | 2024 | ML correction on physics requires less data than end-to-end ML |
| **ARKNESS** (arXiv:2506.13026) | 2025 | KG + 3B Llama = GPT-4o accuracy on 155 machining questions |
| **CAPP-GPT** (TechRxiv 1297057) | 2025 | Custom encoder-decoder for process planning from CAD B-Rep |
| **BRepFormer** (arXiv:2504.07378) | 2025 | 93.16% feature recognition accuracy on MFTRCAD |

### Feature Recognition
| Paper/Dataset | Key Data |
|---------------|----------|
| **MFCAD++** (Colligan, 2022) | 59,655 labeled STEP models for feature recognition training |
| **ABC Dataset** | 1,000,000 STEP models from Onshape for geometric embedding pre-training |
| **AAGNet** (Wu, 2024) | Open-source B-Rep feature recognition + MFInstSeg (60K STEP files) |

## 6. Business and Competitive Intelligence

| Source | Key Data |
|--------|----------|
| **CADDi** ($1.4B valuation, 28 patents) | Proprietary deep learning shape recognition on millions of Japanese drawings. SaaS $50K-$200K/year per customer |
| **aPriori** | Pure physics-based, 440+ process models, 87 regional cost libraries. $150K+/year. Requires 3D CAD only |
| **Pactum AI** | Hybrid rule+LLM negotiation. Walmart: 2,000+ suppliers, 3% savings, 35 days payment term extension |
| **IndustrialMind.ai** | Ex-Tesla founders, $1.2M pre-seed, deploying with Siemens |
| McKinsey procurement studies | Similar part search yields 10-25% cost reduction |
| Aberdeen Group | 60% of "new" parts are near-identical to existing designs |

## 7. Online Tools and Databases

| Resource | URL | Use |
|----------|-----|-----|
| Sandvik CoroPlus Tool Guide | sandvik.coromant.com/toolguide | Real-time Vc/fz for any tool+material |
| Kennametal NOVO | novo.kennametal.com | Tool selection + cutting data |
| MTConnect Standard | mtconnect.org | Open-source CNC data collection protocol |
| CustomPartNet | custompartnet.com | Process cost estimators (basic reference) |
| IndiaMART / TradeIndia | Online | Real-time Indian material and component pricing |

## 8. Key Open-Source Tools

| Tool | Use in Newton-Metre |
|------|---------------------|
| **ezdxf** (1,244 stars) | DXF parsing -- dimension extraction, tolerance info, layer data |
| **PythonOCC** / CadQuery | STEP file parsing -- B-Rep analysis, feature detection |
| **vLLM** | Self-hosted inference server for fine-tuned models |
| **pgvector** | Vector similarity search on Supabase Postgres |
| **FlashRank** | Lightweight open-source re-ranking |
