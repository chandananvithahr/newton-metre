# Similarity Search Technology Deep Dive

> Research date: 2026-04-02
> Status: Comprehensive multi-agent research across 8 parallel investigations
> Purpose: Define the technology strategy for Newton-Metre's similarity search + "company brain" vision

---

## Table of Contents

1. [Current State Assessment](#1-current-state-assessment)
2. [How Google Does It](#2-how-google-does-it)
3. [AI Embedding Models Landscape](#3-ai-embedding-models-landscape)
4. [Vector Databases & ANN Algorithms](#4-vector-databases--ann-algorithms)
5. [RAG, GraphRAG & Knowledge Graphs](#5-rag-graphrag--knowledge-graphs)
6. [ColPali & Late-Interaction Models](#6-colpali--late-interaction-models)
7. [Key Research Papers](#7-key-research-papers)
8. [GitHub Repos Catalog](#8-github-repos-catalog)
9. [The "Company Brain" Market](#9-the-company-brain-market)
10. [Infrastructure & Costs at Every Scale](#10-infrastructure--costs-at-every-scale)
11. [ROI Analysis: Is It Worth It?](#11-roi-analysis-is-it-worth-it)
12. [Build vs Buy](#12-build-vs-buy)
13. [Recommended Architecture](#13-recommended-architecture)
14. [Phased Upgrade Roadmap](#14-phased-upgrade-roadmap)

---

## 1. Current State Assessment

### What We Have

The similarity search lives in `costimize-v2/engines/similarity/` with 5 modules:

| Module | What It Does |
|--------|-------------|
| `preprocessor.py` | Converts PDF/DXF/PNG/JPG → clean 224x224 RGB image + 300x300 thumbnail |
| `embedder.py` | 3 strategies: Gemini API text-hash (default), image hash (fallback), DINOv2 (future) |
| `indexer.py` | FAISS IndexFlatIP or numpy brute-force, JSON metadata sidecar |
| `ranker.py` | 4-signal weighted: 0.5 visual + 0.2 material + 0.2 dimension + 0.1 process |
| `searcher.py` | Orchestrates: ingest → embed → store → search → rank → return top 5 |

Production API: Supabase pgvector via `match_drawings` RPC. Rate-limited 15/min, $0.50/48h budget cap.

### Critical Gaps

1. **No real vision embedding.** The Gemini strategy sends drawing to Gemini Flash, gets a 50-word text description, then hashes character trigrams into 256 bins using MD5. This is fundamentally lossy — two visually similar drawings with different text descriptions hash to different vectors. Two different drawings with similar words hash together. The quality ceiling is the text-to-vector hashing, not Gemini's vision.

2. **256-dim is undersized.** With MD5 hashing to 256 bins, collisions are frequent. The trigram hashing is a crude bag-of-characters model that doesn't capture word order or semantic meaning.

3. **DINOv2 not wired in.** It produces 768-dim vectors (incompatible with EMBEDDING_DIM=256), exists as standalone function only, not in the auto-selection chain.

4. **No true multimodal embedding.** Neither CLIP, Gemini's embedding API, nor any vision model is called. The Gemini strategy uses text generation + hashing as a proxy.

5. **Dimension scoring too narrow.** Only OD and length compared — misses width, height, thickness, wall thickness, bend count (critical for sheet metal).

6. **No feedback loop.** No mechanism to collect user feedback on search result relevance.

7. **Two incompatible storage paths.** Local FAISS/numpy vs production pgvector — improvements to one don't affect the other.

8. **No STEP file support** in preprocessor.

---

## 2. How Google Does It

### Google's Visual Search Pipeline (Lens / Image Search)

1. **Preprocessing** — image adjusted for lighting, orientation, quality
2. **Feature extraction** — Vision Transformers (ViTs) convert images to high-dim embedding vectors
3. **Embedding indexing** — stored in massive distributed index built on ScaNN
4. **ANN retrieval** — approximate nearest neighbor search across billions of vectors
5. **Re-ranking** — cross-encoder models re-rank top candidates

### Google ScaNN (Scalable Nearest Neighbors)

- **Paper:** "Accelerating Large-Scale Inference with Anisotropic Vector Quantization" (ICML 2020)
- **Repo:** [google-research/scann](https://github.com/google-research/google-research/tree/master/scann)
- **Core innovation:** Anisotropic Vector Quantization (AVQ) — penalizes quantization error parallel to the original vector more heavily than perpendicular error, aligning quantization with the downstream MIPS objective
- **3-stage pipeline:** Partition (k-means) → Quantize (AVQ) → Re-rank (exact distances)
- **SOAR upgrade (2024):** Orthogonality-Amplified Residuals for multi-cluster assignment. Won Big-ANN 2023. Libraries approaching ScaNN's speed need 10x memory and 50x indexing time.
- **When to use:** 100K to billions of vectors. Overkill for <10K.

### Google's Embedding Models

| Model | Modality | Dimensions | Pricing | Best For |
|-------|----------|------------|---------|----------|
| **Gemini Embedding 2** | Text + Image + Video + Audio + PDF | 3072 (MRL: truncatable to 768) | $0.20/M tokens | Unified multimodal search |
| **text-embedding-005** | Text only | 768 | ~$0.025/M tokens | Text semantic search |
| **SigLIP 2** | Image + Text (open-source) | 384-1152 | Free (self-hosted) | Fine-tunable visual similarity |

**Gemini Embedding 2 key facts:**
- First natively multimodal embedding model (all modalities from scratch)
- MTEB English score: 68.32 (top spot by 5+ points)
- Matryoshka: 768 dims retains 99.5% of quality vs 3072
- Embeds PDFs directly (up to 6 pages) — perfect for drawings
- 10x more expensive than OpenAI text-embedding-3-small

### Vertex AI Vector Search (Managed ScaNN)

- Minimum $68/month for a single node
- Handles billions of vectors
- **Verdict:** Massive overkill for us. pgvector handles our scale comfortably.

### Key Insight

> Google's similarity stack is optimized for consumer-scale problems (billions of product images). For engineering drawing similarity, **the bottleneck is not the ANN algorithm — it is the quality of the embeddings.** A fine-tuned SigLIP 2 on 500-1000 manufacturing drawings would outperform any off-the-shelf Google model with brute-force cosine similarity.

---

## 3. AI Embedding Models Landscape

### Foundation Models Comparison (April 2026)

| Model | Org | Dim | Type | Key Strength |
|-------|-----|-----|------|--------------|
| **DINOv3** | Meta | 1024 (7B params) | Self-supervised vision | SOTA visual features, 88.4% ImageNet |
| **DINOv2** | Meta | 768 (ViT-B/14) | Self-supervised vision | Best zero-shot visual similarity |
| **SigLIP2** | Google | 384-1152 | Vision-language contrastive | Multilingual, text+image retrieval |
| **CLIP** | OpenAI | 512-768 | Vision-language contrastive | Text-image alignment, zero-shot |
| **C-RADIOv4** | NVIDIA | Unified | Distilled (SigLIP2+DINOv3+SAM3) | Single model, all tasks |
| **Florence-2** | Microsoft | Variable | Vision-language | Diverse visual tasks |

### Head-to-Head: DINOv2 vs CLIP

- DINOv2-ViT-B14: **64% accuracy** on challenging visual similarity
- CLIP: **28.45%** on the same task
- **DINOv2 wins dramatically for pure visual (structural/geometric) similarity** — trained on self-supervised objectives capturing shape, texture, spatial composition
- CLIP wins for text-to-image search ("find cylindrical parts with threads")

### Domain-Specific: Engineering Drawing Embeddings

**GC-CAD** (arxiv:2406.08863) — Self-supervised GNN for Mechanical CAD Retrieval:
- Operates directly on STEP file B-Rep graph structure
- 100x efficiency improvement over baselines
- Relevant when we add STEP support

**CADDi's approach (patented):**
- Proprietary geometric shape analysis (28 patents)
- Our image-based approach is explicitly non-conflicting

### Recommendation for Newton-Metre

| Phase | Model | Why |
|-------|-------|-----|
| **Now** | Gemini Embedding 2 (768-dim) | Real learned embeddings, embeds PDFs directly, same API cost |
| **Next** | DINOv2-ViT-B/14 (768-dim) | 2.3x better visual similarity than CLIP, works on 8GB RAM CPU |
| **Later** | Fine-tuned DINOv2 on our drawings | Contrastive learning on 200-500 drawing pairs, $5-15 on cloud GPU |
| **Future** | GC-CAD GNN for STEP files | 5th ranking signal when STEP support ships |

---

## 4. Vector Databases & ANN Algorithms

### Vector Database Comparison

| Database | Stars | Language | Best For | License |
|----------|-------|----------|----------|---------|
| **FAISS** (Meta) | ~33K | C++/Python | Raw speed, GPU, in-process | MIT |
| **Milvus** | 43.6K | Go/C++ | Billions of vectors | Apache 2.0 |
| **Qdrant** | 30K | Rust | Filtered search + vectors | Apache 2.0 |
| **pgvector** | 20.6K | C (PG ext) | Already-on-Postgres teams | PostgreSQL |
| **Weaviate** | 15.9K | Go | Built-in vectorizers | BSD-3 |
| **ChromaDB** | ~17K | Python | Prototyping | Apache 2.0 |
| **Pinecone** | Managed | — | Zero-ops managed | Proprietary |

### ANN Algorithm Comparison

| Algorithm | Speed | Memory | Recall | Best For |
|-----------|-------|--------|--------|----------|
| **HNSW** | Fastest queries | High (2-3x) | 95-99% | Production, <10M vectors |
| **IVF-PQ** | Fast | Very low (4-8x compression) | 90-95% | Billions, memory-constrained |
| **ScaNN** (Google) | Very fast | Medium | 95%+ | High-throughput serving |
| **ANNOY** (Spotify) | Medium | Low | 85-95% | Read-heavy, static indexes |

### pgvector Performance (Our Stack)

- pgvector 0.7.0+: **30x faster** HNSW index builds
- pgvectorscale: **471 QPS at 99% recall** on 50M vectors (11.4x better than Qdrant at same recall)
- **For our scale (<10K drawings): pgvector HNSW is more than sufficient**
- Scaling limit: at 50M vectors with HNSW, need ~1TB RAM

### Verdict

**Do NOT migrate off pgvector.** At <100K drawings for years, pgvector HNSW on Supabase is sufficient. Adding another database is unnecessary complexity. Migrate to Milvus only if we hit 50M+ vectors.

---

## 5. RAG, GraphRAG & Knowledge Graphs

### Standard RAG for Similarity

For our use case (finding similar drawings), the retrieval step IS the similarity search. RAG adds generation on top: "here are 5 similar parts, here's how they differ in cost."

**Hybrid Search (Critical Upgrade):**
Combine dense vectors (semantic) + sparse BM25 (exact match):
- Dense: "turned aluminum shaft" matches "CNC lathe machined AL6061 spindle"
- Sparse: part numbers, material grades like "IS 2062 E250", tolerance "±0.05mm"

**Implementation:** Add PostgreSQL `tsvector` on part descriptions + material names + part numbers. Combine scores with Reciprocal Rank Fusion (RRF): `score = Σ 1/(k + rank_i)` where k=60.

**Re-ranking (High ROI):**
Two-stage: fast bi-encoder (top 100) → expensive cross-encoder re-rank (top 10):
- **BAAI/bge-reranker-v2-m3** — open-source, self-hostable, multilingual
- **Cohere Rerank v3.5** — $1/1000 queries, best commercial option
- **FlashRank** — lightweight, open-source, resource-constrained environments
- **ColBERT v2** — late interaction, pre-computes token embeddings, fast yet accurate

### GraphRAG (Microsoft)

**Repo:** `microsoft/graphrag` (15K+ stars)

Architecture: Entity extraction → Knowledge graph → Leiden community detection → Community summaries → Two search modes (local + global)

**When GraphRAG beats standard RAG:**
- Synthesizing across many documents ("What materials are most common across 500 historical quotes?")
- Relationships matter (part → material → supplier → cost history)
- Thematic/global questions, not specific lookups

**When to skip GraphRAG:**
- Simple lookups ("Find parts similar to this drawing") ← OUR PRIMARY USE CASE
- Small corpus (<100 documents)
- Real-time latency matters
- **Cost:** Indexing 1000 docs = $50-200 in LLM calls. Too expensive for startup.

### LightRAG (Better Alternative)

**Repo:** `HKUDS/LightRAG` (20K+ stars)
- **70% cheaper** to index than Microsoft GraphRAG
- **Incremental updates** — add docs without full re-index
- Dual-level retrieval: entities + themes
- Supports Neo4j or NetworkX backends

### Knowledge Graph for Manufacturing

Schema that would power graph-aware similarity:

```
(Part) -[:MADE_FROM]-> (Material)
(Part) -[:USES_PROCESS]-> (Process)
(Part) -[:HAS_FEATURE]-> (Feature)  // hole, slot, pocket, thread
(Part) -[:HAS_TOLERANCE]-> (Tolerance)
(Part) -[:COSTS]-> (CostBreakdown)
(Part) -[:SIMILAR_TO {score}]-> (Part)
(Part) -[:FROM_SUPPLIER]-> (Supplier)
(Feature) -[:REQUIRES_PROCESS]-> (Process)
(Tolerance) -[:AFFECTS_COST {multiplier}]-> (Process)
```

**Practical approach:** Use PostgreSQL relational modeling (not Neo4j) for part → material → process → feature relationships. Add graph-aware boosting to ranking. We can build explicit similarity edges from user feedback over time.

### Agentic RAG for Similarity Search

The pattern for our use case:
1. User uploads drawing
2. Agent extracts: material, dimensions, features, processes, tolerances (existing extraction)
3. Agent decides strategy: clear metadata → hybrid search; ambiguous → clarifying questions; few results → relax constraints progressively
4. Agent re-ranks considering query context
5. Agent generates comparison summary

**This is essentially what our validation orchestrator already does for cost estimation.** Same pattern applies to similarity.

### Multimodal RAG: ColPali

See [Section 6](#6-colpali--late-interaction-models) for full coverage. The short version: ColPali embeds document page images directly (no OCR, no parsing) and is SOTA on ViDoRe benchmark. Highly relevant for engineering drawings.

---

## 6. ColPali & Late-Interaction Models

### What ColPali Is

**Paper:** "ColPali: Efficient Document Retrieval with Vision Language Models" (NeurIPS 2024)
**Repo:** [illuin-tech/colpali](https://github.com/illuin-tech/colpali) (2,586 stars)

A PaliGemma-3B VLM produces ColBERT-style multi-vector embeddings directly from page images:
1. SigLIP vision encoder splits page into patches
2. Gemma-2B language model contextualizes patches
3. Each patch projected to 128-dim vector (~1024 vectors per page)
4. Late interaction (MaxSim) matches query token vectors against page patch vectors

**Why it matters for engineering drawings:**
- No OCR needed, no parsing needed
- Works on scanned drawings, hand-drawn sketches, photos of parts
- Patch-level matching localizes which PART of a drawing matches the query
- Handles mixed text+diagram pages natively
- GD&T symbols, dimension callouts, geometry captured simultaneously

### ColPali Variants

| Model | Size | Key Feature | Relevance |
|-------|------|-------------|-----------|
| **ColPali** | 3B (PaliGemma) | Original | Good baseline |
| **ColQwen2** | Qwen2-VL | Better multilingual + resolution | Better for Indian docs |
| **ColSmol** | 256M | Edge deployment | Fits 8GB RAM for defense on-prem |
| **ColFlor** | 174M | 17x smaller, 5.25x faster, 1.8% drop | Best for our self-hosted target |
| **Nemotron ColEmbed V2** | 4B/8B | NVIDIA, NDCG@10 63.42 on ViDoRe V3 | Highest quality |

### Practical Concern

ColPali produces ~1024 vectors per page (128-dim each). For 10K drawings = ~10M vectors. Solutions:
- Use PLAID (ColBERT's efficient indexing)
- Pre-filter with single-vector model → re-rank with ColPali
- Use **fast-plaid** (LightOn, 230 stars) for efficient multi-vector search

### Key Repos for ColPali

| Repo | Stars | What |
|------|-------|------|
| `illuin-tech/colpali` | 2,586 | Core models (ColPali, ColQwen2, ColSmol) |
| `AnswerDotAI/byaldi` | 846 | Simple wrapper, deploy in 5 lines |
| `tonywu71/colpali-cookbooks` | 356 | Fine-tuning recipes for specific domains |
| `lightonai/fast-plaid` | 230 | High-perf engine for multi-vector search |
| `s-emanuilov/litepali` | 122 | Minimal, efficient deployment |
| `fangzhensheng/vembed-factory` | 28 | Unified trainer: LoRA + Matryoshka on 24GB GPU |

---

## 7. Key Research Papers

### Highest Priority for Newton-Metre

| # | Paper | Year | Key Finding | Relevance |
|---|-------|------|-------------|-----------|
| 1 | **ColPali** (Faysse et al.) | 2024 | Page-image retrieval beats OCR+text pipelines | Replace Gemini text-hash with visual embeddings |
| 2 | **ColFlor** | 2025 | 174M params, 17x smaller than ColPali | Fits 8GB self-hosted defense target |
| 3 | **GC-CAD** | 2024 | Self-supervised GNN for CAD B-Rep retrieval, 100x efficiency | STEP file similarity when we add support |
| 4 | **ARKNESS** | 2025 | KG + 3B Llama matches GPT-4o on machining | Enhance validation arbitrator with KG reasoning |
| 5 | **ML Cost from 2D Drawings** (arXiv 2508.12440) | 2025 | MAPE 3.91-18.51% from 2D drawings via ML | Direct benchmark comparison for our physics approach |
| 6 | **DAT: Dynamic Alpha Tuning** | 2025 | Per-query dynamic weighting of retrieval signals | Replace our fixed 4-signal weights with learned weights |
| 7 | **CSR (Beyond Matryoshka)** | 2025 | Adaptive-dim embeddings without retraining, beats MRL | Post-hoc sparsification of embeddings |
| 8 | **Geometric DL for CAD Survey** | 2024 | Maps entire landscape of CAD ML methods | Essential reference |

### Vision & Embedding Papers

| Paper | Year | Key Finding |
|-------|------|-------------|
| **SigLIP 2** | 2025 | Multi-task pretraining, beats CLIP at all scales |
| **DINOv3** | 2026 | 7B params, 88.4% ImageNet, but needs serious GPU |
| **DINOv2 Meets Text** (CVPR 2025) | 2025 | DINOv2 leads classification but drops in retrieval vs CLIP |
| **Talking to DINO** (ICCV 2025) | 2025 | Bridges DINOv2 with language via InfoNCE |
| **C-RADIOv4** (NVIDIA) | 2026 | Unified SigLIP2+DINOv3+SAM3, commercial license |
| **Matryoshka Representation Learning** | 2022/2024 | 14x smaller embeddings at same accuracy |

### Manufacturing & CAD Papers

| Paper | Year | Key Finding |
|-------|------|-------------|
| **BRepNet** (Autodesk, ICCV 2021) | 2021 | GNN on B-Rep topology for segmentation/classification |
| **UV-Net** (Autodesk, CVPR 2021) | 2021 | CNN on UV-grids of CAD faces |
| **UVStyle-Net** (Autodesk, ICCV 2021) | 2021 | Unsupervised B-Rep similarity |
| **CAPP-GPT** | 2024 | LLM-based process planning from B-Rep |
| **From Drawings to Decisions** | 2025 | YOLOv11-obb + VLM for engineering drawing parsing |
| **Automated Parsing of Eng. Drawings** | 2025 | Donut (Swin-B + BART) for drawing parsing without OCR |
| **A2Z-10M+ Dataset** | 2026 | 10M annotations for 1M ABC CAD models |
| **Manufacturing Process Selection via GNN** | 2025 | GNN-based process selection from geometry |

### RAG & Retrieval Papers

| Paper | Year | Key Finding |
|-------|------|-------------|
| **GraphRAG** (Microsoft) | 2024 | Community summaries enable global questions |
| **LightRAG** | 2024 | 70% cheaper than GraphRAG, incremental updates |
| **RAPTOR** (Stanford) | 2024 | Recursive summary tree beats flat RAG |
| **Self-RAG** | 2023 | Model learns when to retrieve, reduces hallucination |
| **CRAG (Corrective RAG)** | 2024 | Evaluator classifies results, retries if poor |
| **Late Chunking** (Jina AI) | 2024 | Embed full doc first, then chunk — preserves context |
| **SPLADE v3** | 2024 | Neural sparse retrieval, 29% better than BM25 |
| **Document GraphRAG for Manufacturing** | 2025 | KG-enhanced RAG for manufacturing QA |

---

## 8. GitHub Repos Catalog

### Tier 1: Directly Relevant to Manufacturing Drawing Similarity

| Repo | Stars | Tech | Relevance |
|------|-------|------|-----------|
| **illuin-tech/colpali** | 2,586 | ColBERT-style visual doc retrieval | VERY HIGH — drawing page embeddings |
| **AutodeskAILab/BRepNet** | 220 | GNN on B-Rep topology | HIGH — STEP file similarity |
| **AutodeskAILab/UV-Net** | 183 | CNN on B-Rep UV-grids | HIGH — CAD face embeddings |
| **AutodeskAILab/UVStyle-Net** | 31 | Unsupervised B-Rep similarity | VERY HIGH — explicit similarity |
| **AutodeskAILab/Fusion360GalleryDataset** | 644 | 8,625 CAD models with labels | HIGH — training data |
| **W24-Service-GmbH/werk24-python** | 85 | Drawing processing API | HIGH — competitor reference |
| **rundiwu/DeepCAD** | 719 | Generative CAD latent space | MEDIUM — latent space for search |
| **hducg/MFCAD** | 45 | Machining feature CAD dataset | HIGH — training data |

### Tier 2: ColPali Ecosystem

| Repo | Stars | Purpose |
|------|-------|---------|
| **AnswerDotAI/byaldi** | 846 | Simple ColPali wrapper |
| **morphik-org/morphik-core** | 3,556 | ColPali-powered doc search |
| **tonywu71/colpali-cookbooks** | 356 | Fine-tuning recipes |
| **lightonai/fast-plaid** | 230 | High-perf multi-vector search |
| **s-emanuilov/litepali** | 122 | Lightweight deployment |
| **fangzhensheng/vembed-factory** | 28 | LoRA trainer for ColPali on 24GB GPU |

### Tier 3: Vision Foundation Models

| Repo | Stars | Purpose |
|------|-------|---------|
| **facebookresearch/faiss** | 39,599 | Vector similarity search (already using) |
| **mlfoundations/open_clip** | 13,634 | Open-source CLIP, fine-tunable |
| **facebookresearch/dinov2** | 12,634 | Self-supervised ViT (on roadmap) |
| **google-research/big_vision** | 3,405 | SigLIP / ViT official code |
| **NVlabs/RADIO** | — | C-RADIOv4 unified backbone |

### Tier 4: Vector Databases

| Repo | Stars | When to Use |
|------|-------|-------------|
| **milvus-io/milvus** | 43,591 | >50M vectors |
| **qdrant/qdrant** | 30,014 | Complex filtering + vectors |
| **pgvector/pgvector** | 20,606 | Already on Postgres (US NOW) |
| **weaviate/weaviate** | 15,946 | Built-in vectorizers |

### Tier 5: Document Intelligence

| Repo | Stars | Purpose |
|------|-------|---------|
| **docling-project/docling** | 56,982 | PDF/DOCX to structured output (IBM) |
| **michaelfeil/infinity** | 2,742 | High-throughput CLIP/ColPali serving |
| **VikParuchuri/marker** | ~18K | PDF to markdown, preserves tables |

### Tier 6: GraphRAG

| Repo | Stars | Purpose |
|------|-------|---------|
| **HKUDS/LightRAG** | ~20K | Lightweight GraphRAG (prefer over MS) |
| **microsoft/graphrag** | ~15K | Full GraphRAG (expensive) |
| **gusye1234/nano-graphrag** | ~2K | Minimal GraphRAG for learning |

---

## 9. The "Company Brain" Market

### Who Is Doing It

| Company | Focus | Valuation | Approach |
|---------|-------|-----------|----------|
| **CADDi** | Manufacturing drawing similarity | $1.4B+ | Proprietary CNN, 28 patents, Japan-first |
| **Glean** | Enterprise AI search | $7.2B | Horizontal, connects 12+ platforms |
| **OpenAI Company Knowledge** | Enterprise AI brain | Part of ChatGPT Enterprise | GPT-5 powered, connects Slack/Drive/etc. |
| **Guru** | Knowledge management | Acquired by Canva | "Secure company brain" |
| **ContextClue** | Manufacturing doc intelligence | Startup | Transforms unstructured mfg docs to KG |
| **Peppr AI** (YC) | Engineering knowledge capture | Startup | Captures tribal knowledge from workflows |
| **Palantir** | Enterprise data platform | $250B+ | Government + enterprise, custom |

### Market Size

- AI-driven knowledge management: **$7.66B in 2025, projected $51.36B by 2030** (46.7% CAGR)
- Broader KM software: **$23.2B in 2025, projected $74.2B by 2034**
- Vector database market: **$1.73B in 2024, projected $10.6B by 2032**
- Manufacturing-specific TAM: **$2.5B-$25B** (bottom-up from 250K manufacturers globally)

### Newton-Metre's Unique Angle

- **OpenAI Company Knowledge** = horizontal (Slack, email, docs) — knows nothing about drawings
- **CADDi** = drawing similarity + parts consolidation — but NO should-cost estimation
- **aPriori** = should-cost estimation — but requires 3D CAD, doesn't do similarity
- **Newton-Metre** = should-cost + similarity + company memory from 2D drawings = **unique combination, no one else does all three**

### The "Company Brain" Difference vs Simple Search

1. **Semantic understanding** — meaning-based, not keyword
2. **Cross-format** — drawings + PDFs + spreadsheets + ERP data simultaneously
3. **Institutional memory** — captures tribal knowledge from retiring workforce
4. **Contextual intelligence** — "find a similar part but cheaper" is analysis, not search
5. **Active suggestions** — "you designed a similar part 3 years ago, here's what it cost"

---

## 10. Infrastructure & Costs at Every Scale

### Vector Storage Math

| Vectors | Dimensions | Raw Size | With HNSW (3-4x) | With Metadata |
|---------|-----------|----------|-------------------|---------------|
| 10,000 | 768 | 29 MB | ~90-120 MB | ~150 MB |
| 1,000,000 | 768 | 2.9 GB | ~9-12 GB | ~15 GB |
| 100,000,000 | 768 | 290 GB | ~900 GB-1.2 TB | ~1.5 TB |
| 1,000,000,000 | 768 | 2.87 TB | ~9-12 TB | ~15 TB |

### Cost Breakdown by Scale

#### Tier 1: Startup (10K docs) — Newton-Metre Today

| Component | Monthly | Annual |
|-----------|---------|--------|
| Embedding generation (Gemini API) | ~$0-1 | ~$5 |
| Vector DB (pgvector on Supabase) | $0-25 | $0-300 |
| Raw document storage | $1-5 | $12-60 |
| Compute | $5-20 | $60-240 |
| **Total** | **$30-70** | **$400-850** |

#### Tier 2: Mid-Size Manufacturer (1M docs)

| Component | Monthly | Annual |
|-----------|---------|--------|
| Embedding generation (self-hosted) | — | $200-500 (one-time) |
| Vector DB (Milvus/Qdrant, 1 node) | $200-500 | $2,400-6,000 |
| Storage (S3, ~1 TB) | $23 | $276 |
| Compute (2x GPU inference) | $500-1,500 | $6,000-18,000 |
| **Total** | **$800-2,200** | **$10K-27K** |

#### Tier 3: Large Enterprise (100M docs)

| Component | Monthly | Annual |
|-----------|---------|--------|
| Embedding generation (GPU cluster) | — | $5K-15K (one-time) |
| Vector DB (Milvus cluster, 8-16 nodes) | $8K-20K | $96K-240K |
| Compute (8x GPU inference) | $5K-15K | $60K-180K |
| DevOps/SRE (2-3 engineers) | $30K-50K | $360K-600K |
| **Total** | **$47K-90K** | **$560K-1.1M** |

#### Tier 4: Fortune 500 (1B+ docs, Petabyte)

| Component | Monthly | Annual |
|-----------|---------|--------|
| Embedding generation (32x A100) | — | $15K-30K (one-time) |
| Vector DB (Milvus, 50-100 nodes) | $50K-150K | $600K-1.8M |
| Storage (S3, 1+ PB) | $21.5K | $258K |
| GPU inference (16-32 GPUs) | $20K-60K | $240K-720K |
| Engineering team (5-8 people) | $80K-150K | $960K-1.8M |
| Security/compliance | $10K-30K | $120K-360K |
| **Total** | **$190K-430K** | **$2.3M-5.4M** |

### Summary

| Scale | Documents | Annual Cost | Monthly |
|-------|-----------|-------------|---------|
| **Startup** | 10K | $400-850 | $30-70 |
| **Mid-size** | 1M | $10K-27K | $800-2,200 |
| **Enterprise** | 100M | $560K-1.1M | $47K-90K |
| **Fortune 500** | 1B+ | $2.3M-5.4M | $190K-430K |

**Infrastructure scales gracefully.** We don't need to build for petabyte on day one. pgvector on Supabase handles our first 1,000+ customers at 10K docs each.

---

## 11. ROI Analysis: Is It Worth It?

### What Competitors Charge

| Company | Pricing |
|---------|---------|
| **CADDi** | Custom enterprise, not disclosed. Customers: Hitachi, Kawasaki, Subaru |
| **aPriori** | $100K-$500K+/year per contract |
| **Glean** | ~$50/user/month + $15 AI add-on. Min 100 seats = $78K/year |
| **Guru** | $25/user/month |

### Documented ROI from Similar Parts & Duplicate Elimination

The research is **unambiguous — this is high-ROI:**

- **60% of part numbers** in a typical mfg database are duplicates or obsolete (Deloitte)
- Failing to consolidate costs **10-15% premium** on procurement spend
- Each redundant part adds **$4,500-$7,500/year** in inventory carrying
- AI procurement analysis: **$1.2M in duplicate spending** uncovered (case study)
- Engineers spend **up to 30% of work hours** redesigning instead of reusing
- CADDi: search reduced from **hours to seconds**, **1.5-2.1x faster quotations**

### ROI Calculation for a Mid-Size Manufacturer

Assumptions: $50M annual procurement, 200 engineers at $80K avg

| Savings Source | Conservative | Aggressive |
|----------------|-------------|-----------|
| Procurement cost reduction (5-15%) | $2.5M | $7.5M |
| Engineering time savings (10-30%) | $800K | $2.4M |
| Inventory carrying reduction | $500K | $2M |
| Supplier negotiation leverage | $500K | $2M |
| **Total annual savings** | **$4.3M** | **$13.9M** |
| System cost (Tier 2-3) | $30K-$1.1M | $30K-$1.1M |
| **ROI** | **4x-140x** | **13x-460x** |

> A $50M-procurement manufacturer spending $100K/year on similarity saves $4.3M minimum — **43x return**.

### Is the "Company Brain" Worth Building?

**Definitively yes.** The combination of:
1. Massive proven ROI (10-40x+)
2. Growing market ($7.66B → $51.36B by 2030)
3. No existing tool combines should-cost + similarity + company memory
4. CADDi proved $1.4B valuation with similarity alone

---

## 12. Build vs Buy

### For Newton-Metre (Startup): BUILD

We're already building the core technology. At 10K docs, infrastructure is negligible ($30-70/month). The engineering team IS the product.

### For a Mid-Size Manufacturer (Customer): BUY US

Buy CADDi for drawing similarity only. Buy Newton-Metre for should-cost + similarity + company memory.

### Build In-House Team Requirement

| Scale | Team Size | Infrastructure | Total Annual |
|-------|-----------|---------------|-------------|
| 10K docs | 1-2 FTEs | $500-1K | $150K-300K |
| 1M docs | 3-4 FTEs | $10K-27K | $310K-527K |
| 100M docs | 5-8 FTEs | $200K-500K | $700K-1.3M |
| 1B+ docs | 8-12 FTEs | $1.3M-3.6M | $2.1M-5.1M |

---

## 13. Recommended Architecture

### Target Architecture (Phased)

```
┌─────────────────────────────────────────────────────────┐
│                    SIMILARITY SEARCH v2                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────┐   ┌──────────────┐   ┌─────────────────┐  │
│  │ INGEST   │   │  EMBED       │   │  STORE          │  │
│  │          │   │              │   │                 │  │
│  │ PDF ─────┼──▶│ Gemini Emb 2 │──▶│ pgvector HNSW   │  │
│  │ DXF ─────┤   │ (768-dim)    │   │ (Supabase)      │  │
│  │ STEP ────┤   │              │   │                 │  │
│  │ Image ───┘   │ + DINOv2     │   │ + tsvector      │  │
│  │              │   (visual)    │   │   (BM25 text)   │  │
│  │  Metadata    │              │   │                 │  │
│  │  extraction  │ + ColFlor    │   │ + metadata      │  │
│  │  (GPT-4o/   │   (on-prem)   │   │   tables        │  │
│  │   Gemini)    │              │   │                 │  │
│  └──────────┘   └──────────────┘   └─────────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────────┐│
│  │                    SEARCH                             ││
│  │                                                      ││
│  │  Query ──▶ Embed ──▶ Hybrid Retrieval (top 100)     ││
│  │                      (vector + BM25 + filters)       ││
│  │                           │                          ││
│  │                    Cross-encoder Re-rank (top 10)    ││
│  │                    (BGE-reranker-v2-m3)              ││
│  │                           │                          ││
│  │                    Multi-signal Ranking               ││
│  │                    (visual + material + dims +        ││
│  │                     process + tolerance + finish)     ││
│  │                           │                          ││
│  │                    Results + Cost Intelligence        ││
│  └──────────────────────────────────────────────────────┘│
│                                                          │
│  ┌──────────────────────────────────────────────────────┐│
│  │                 COMPANY BRAIN (Phase 2)               ││
│  │                                                      ││
│  │  Knowledge Graph (PostgreSQL relational)             ││
│  │  Part → Material → Process → Feature → Cost          ││
│  │  + Supplier → History → Trends                       ││
│  │                                                      ││
│  │  LightRAG for cross-document intelligence            ││
│  │  "What's our average cost for turned AL parts?"      ││
│  │                                                      ││
│  │  Feedback loop: user confirms/rejects matches        ││
│  │  → builds explicit similarity graph over time         ││
│  └──────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

---

## 14. Phased Upgrade Roadmap

### Phase 1: Quick Wins (1-2 days)

**Replace Gemini text-hash with real embeddings.**

Option A (API, zero infra): Switch to Gemini Embedding 2 (768-dim, embeds PDFs directly).
Option B (free, self-hosted): Use Gemini's existing vision to generate descriptions, then embed with `text-embedding-005` instead of character trigram hashing.

Impact: Dramatically better vector quality at same cost. Bump EMBEDDING_DIM to 768.

**Add BM25 text search.** Add PostgreSQL `tsvector` on part descriptions, material names, part numbers. Combine with vector search via RRF. Catches exact-match cases embeddings miss.

### Phase 2: Major Quality Jump (3-5 days)

**Add DINOv2-ViT-B/14 as primary visual embedder.** 768-dim vectors, works on CPU (4-5GB RAM, slow but functional). Dramatically better pure visual similarity than any text-based approach.

**Expand dimension scoring.** Add width, height, thickness, wall_thickness, bend_count, cutting_perimeter to ranker. Critical for sheet metal parts.

**Add tolerance + surface finish signals.** 6-signal ranking instead of 4.

**Add cross-encoder re-ranker.** BGE-reranker-v2-m3 (open-source) or FlashRank (lightweight) as second stage after vector retrieval.

### Phase 3: Defense-Ready (1-2 weeks)

**Fine-tune DINOv2 on our drawing corpus.** Contrastive learning (triplet loss) on 200-500 drawing pairs. LoRA fine-tuning = $5-15 on cloud GPU. Proprietary embedding model = genuine moat.

**Add ColFlor/ColSmol for on-premise.** 174M/256M params, fits 8GB RAM. For defense clients who won't use cloud APIs.

**Structured metadata filtering.** Pre-filter by material family, part type, dimension range before vector search. Prevents nonsensical matches.

### Phase 4: Company Brain (2-4 weeks)

**Build relational knowledge graph in PostgreSQL.** Part → material → process → feature → cost → supplier relationships. Graph-aware ranking boosts.

**Add feedback loop.** Users confirm/reject matches → builds explicit similarity edges → improves ranking over time.

**LightRAG for portfolio intelligence.** Cross-document questions: "What's our average cost for turned aluminum parts?" "Which supplier is cheapest for sheet metal?"

### Phase 5: Multi-Format (when STEP support ships)

**GC-CAD GNN embeddings for STEP files.** 5th ranking signal. Cross-modal: upload STEP, find similar 2D drawings.

**BRepNet/UV-Net for 3D similarity.** Train on Fusion360GalleryDataset + MFCAD for manufacturing-specific features.

### What NOT to Do

- Do NOT migrate off pgvector (sufficient for years at our scale)
- Do NOT add another database (ChromaDB, Milvus) — unnecessary complexity
- Do NOT use DINOv3 (7B model needs serious GPU)
- Do NOT use full Microsoft GraphRAG (too expensive to index for startup)
- Do NOT build custom ANN algorithms (HNSW is battle-tested)
- Do NOT jump to Neo4j (PostgreSQL relational modeling is sufficient for our KG)

---

## Sources

### Google Technology
- [ScaNN: Efficient Vector Similarity Search](https://research.google/blog/announcing-scann-efficient-vector-similarity-search/)
- [SOAR: Improved Indexing for ANN](https://arxiv.org/html/2404.00774v1)
- [Gemini Embedding 2](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-embedding-2/)
- [SigLIP 2](https://arxiv.org/pdf/2502.14786)
- [Vertex AI Vector Search](https://docs.cloud.google.com/vertex-ai/docs/vector-search/overview)

### Embedding Models
- [DINOv2](https://github.com/facebookresearch/dinov2) | [DINOv3](https://arxiv.org/html/2508.10104v1)
- [OpenCLIP](https://github.com/mlfoundations/open_clip)
- [C-RADIOv4 (NVIDIA)](https://huggingface.co/nvidia/C-RADIOv4-H)
- [CLIP vs DINOv2 comparison](https://medium.com/aimonks/clip-vs-dinov2-in-image-similarity-6fa5aa7ed8c6)
- [GC-CAD: Self-supervised GNN for CAD](https://arxiv.org/abs/2406.08863)

### ColPali & Document Retrieval
- [ColPali paper](https://arxiv.org/abs/2407.01449) | [GitHub](https://github.com/illuin-tech/colpali)
- [ColFlor](https://huggingface.co/blog/ahmed-masry/colflor)
- [Nemotron ColEmbed V2](https://arxiv.org/abs/2602.03992)
- [Byaldi wrapper](https://github.com/AnswerDotAI/byaldi)
- [fast-plaid](https://github.com/lightonai/fast-plaid)

### RAG & GraphRAG
- [Microsoft GraphRAG](https://github.com/microsoft/graphrag)
- [LightRAG](https://github.com/HKUDS/LightRAG)
- [Self-RAG](https://arxiv.org/abs/2310.11511) | [CRAG](https://arxiv.org/abs/2401.15884)
- [DAT: Dynamic Alpha Tuning](https://arxiv.org/abs/2503.23013)
- [Document GraphRAG for Manufacturing](https://www.mdpi.com/2079-9292/14/11/2102)
- [ARKNESS: KG + LLM for Manufacturing](https://arxiv.org/html/2506.13026v1)

### Vector Databases
- [pgvector](https://github.com/pgvector/pgvector) | [FAISS](https://github.com/facebookresearch/faiss)
- [Milvus](https://github.com/milvus-io/milvus) | [Qdrant](https://github.com/qdrant/qdrant)
- [ann-benchmarks](https://github.com/erikbern/ann-benchmarks)

### Manufacturing & CAD
- [BRepNet](https://github.com/AutodeskAILab/BRepNet) | [UV-Net](https://github.com/AutodeskAILab/UV-Net)
- [Fusion360 Gallery Dataset](https://github.com/AutodeskAILab/Fusion360GalleryDataset)
- [MFCAD](https://github.com/hducg/MFCAD) | [DeepCAD](https://github.com/rundiwu/DeepCAD)
- [ML Cost from 2D Drawings](https://arxiv.org/html/2508.12440v1)
- [CAPP-GPT](https://www.sciencedirect.com/science/article/pii/S221384632400066X)
- [Geometric DL for CAD Survey](https://arxiv.org/abs/2402.17695)

### Market & ROI
- [CADDi raises $38M](https://us.caddi.com/resources/news/caddi-raises-38m-series-c-extension-led-by-atomico)
- [AI Knowledge Management Market ($51.36B by 2030)](https://www.researchandmarkets.com/reports/6103462)
- [Duplicate parts cost 10-15% premium](https://3dsman.com/manufacturing-efficiency-duplicate-parts/)
- [AI procurement 25% cost reduction](https://www.businessplusai.com/blog/how-ai-reduced-procurement-costs-by-25-in-6-months-a-data-driven-case-study)
- [aPriori Carrier case study](https://www.apriori.com/resources/case-study/carrier-apriori-saving-millions-annually-with-apriori/)
- [Glean pricing ($7.2B valuation)](https://www.glean.com/pricing-guide)
- [OpenAI Company Knowledge](https://openai.com/index/introducing-company-knowledge/)

### Document Intelligence
- [Docling (IBM, 57K stars)](https://github.com/docling-project/docling)
- [Marker (PDF→markdown)](https://github.com/VikParuchuri/marker)
- [Infinity (embedding serving)](https://github.com/michaelfeil/infinity)

### Contrastive Learning & Fine-tuning
- [Matryoshka Representation Learning](https://arxiv.org/abs/2205.13147)
- [CSR: Beyond Matryoshka](https://arxiv.org/abs/2503.01776)
- [Contrastive Learning Guide](https://encord.com/blog/guide-to-contrastive-learning/)
- [DINOv2 fine-tuning](https://github.com/xuwangyin/dinov2-finetune)
- [Sentence-Transformers losses](https://sbert.net/docs/package_reference/sentence_transformer/losses.html)

### OCR Models
- [GLM-OCR (Zhipu AI)](https://github.com/zai-org/GLM-OCR) | [HuggingFace](https://huggingface.co/zai-org/GLM-OCR) | [Paper](https://arxiv.org/abs/2603.10910)
- [GOT-OCR2.0](https://github.com/Ucas-HaoranWei/GOT-OCR2.0)
- [Drawing-OCR-Extractor (GLM-OCR for engineering drawings)](https://github.com/quydo144/Drawing-OCR-Extractor)
- [OCR Benchmark comparison](https://github.com/andyhuo520/ocr_benchmark)

---

## 15. GLM-OCR: Cheap Pre-Processing Layer

> Added 2026-04-02. Researched as a potential cost-reduction layer for the extraction pipeline.

### What It Is

GLM-OCR is a 0.9B parameter OCR model by Zhipu AI (ChatGLM family). Released 2026-02-02. Purpose-built for document OCR with CogViT visual encoder (0.4B) + GLM language decoder (0.5B).

### Key Specs

| Spec | Value |
|------|-------|
| Parameters | 0.9B |
| VRAM | ~2-4GB inference |
| GGUF size | 950MB (Q8_0) |
| Speed | 1.86 pages/sec (PDF) |
| GitHub stars | 5,344 |
| HF downloads | 4.47M/month |
| License | MIT (weights), Apache 2.0 (code) |
| API cost | **$0.03/M tokens** (1/100th of GPT-4o) |

### Benchmarks

| Benchmark | GLM-OCR | Context |
|-----------|---------|---------|
| OmniDocBench V1.5 | 94.62 | #1 at launch |
| Text recognition | 96.1 | Strong |
| Table recognition (TEDS) | 91.8 | Good for title blocks |
| Formula recognition (CDM) | 94.9 | Handles math notation |
| olmOCR-bench | 75.2 | Weaker on old scans (37.6) |

### 2026 OCR Competitive Landscape

| Model | Size | Avg Elo | Notes |
|-------|------|---------|-------|
| Gemini 3 Pro | Large | 1210.7 | Best overall, cloud API |
| dots.mocr (RedNote) | 1.7B | 1124.7 | Open source, strongest open |
| dots.ocr | 1.7B | 1086.2 | Predecessor |
| HuanyuanOCR (Tencent) | — | 984.2 | Cloud only |
| PaddleOCR-VL-1.5 (Baidu) | 0.9B | 920.5 | Strong structured parsing |
| GLM-OCR (Zhipu) | 0.9B | 892.5 | Cheapest API, MIT license |

### Engineering Drawing Assessment

**Good at:** General text (96.1%), dimension values, title block extraction (table-like), material callouts ("IS 2062", "AISI 304"), tolerance notation ("0.05 ± 0.02").

**Risky/Unknown:** GD&T symbols (perpendicularity, concentricity, Ra/Rz), complex engineering layouts, structured JSON output for engineering parameters. No engineering drawing benchmarks exist.

**NOT a replacement for GPT-4o/Gemini** for core extraction. 0.9B vs 200B+ capacity gap too large for engineering context understanding.

### Two-Stage Architecture for Newton-Metre

Use GLM-OCR as a cheap pre-processing layer to cut AI costs 50-80%:

```
Drawing image
    │
    ▼
GLM-OCR (local, 950MB, ~free)
    → raw text extraction
    → title block OCR (drawing #, rev, material)
    → dimension value extraction
    │
    ▼
Gemini Flash (cloud, $0.002/drawing)
    → structured engineering interpretation
    → GD&T symbol understanding
    → process detection
    → JSON output
```

**Real-world validation:** `quydo144/Drawing-OCR-Extractor` already uses GLM-OCR via Ollama for engineering drawing title block extraction → Gemini for normalization. Confirms the two-stage approach works.

### Where to Use in Our Pipeline

| Use Case | GLM-OCR? | Why |
|----------|----------|-----|
| Title block OCR (drawing #, rev, material) | **Yes** | Table-like, text-heavy, proven |
| RFQ document parsing | **Yes** | Documents not drawings, $0.03/M tokens |
| Contract/spec text extraction | **Yes** | Huge cost savings vs GPT-4o |
| Pre-processing text for Gemini | **Yes** | Extract text cheap, reason expensive |
| On-prem defense deployment | **Yes** | 950MB, any 4GB GPU laptop |
| GD&T symbol extraction | **No** | Use GPT-4o/Gemini |
| Dimension + tolerance interpretation | **No** | Needs engineering context |
| Process detection from drawing | **No** | Needs VLM reasoning |

### Deployment Options

- **Cloud API:** `open.bigmodel.cn` — $0.03/M tokens
- **Ollama:** `ollama run glm-ocr` — local, 950MB
- **vLLM:** >=0.17.0, self-hosted serving
- **llama.cpp:** GGUF quantized, any CPU/GPU
- **HuggingFace Transformers:** Direct Python integration

### Impact on AI Cost Budget

Current per-estimate cost: ~$0.002 (Gemini Flash for full extraction).

With GLM-OCR pre-processing:
- GLM-OCR extracts all text: ~$0.0003 (local = free, or API = $0.03/M tokens)
- Gemini Flash interprets structured data from text (not image): ~$0.0005 (text-only = cheaper than vision)
- **Estimated savings: 60-75% on per-estimate AI cost**
- At scale (1000 estimates/day): saves ~$1-2/day → ~$40-60/month

For RFQ/contract parsing (heavier documents): savings are larger since documents are multi-page.
