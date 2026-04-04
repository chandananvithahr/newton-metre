---
slug: similarity-search
title: Similarity Search and the Company Brain
keywords: similarity search, company brain, DINOv2, ColFlor, pgvector, embeddings, hybrid search, BM25, re-ranking, FlashRank, drawing similarity, CADDi, part reuse, knowledge management, visual similarity, role presets
sources: SIMILARITY-SEARCH-DEEP-DIVE.md, COMPANY-WIDE-SIMILARITY-SEARCH.md
updated: 2026-04-04
---

# Similarity Search and the Company Brain

Similarity search turns a company's drawing history into a searchable asset. Instead of searching by part number or text description, users upload a drawing and find visually and functionally similar parts from the entire corporate archive -- linked to cost history, supplier data, and quality records. This is the foundation of Newton-Metre's "Company Brain" concept.

## The Business Case

The market for AI-driven knowledge management is $7.66B in 2025, projected to reach $51.36B by 2030 (46.7% CAGR). CADDi proved the category at $1.4B valuation with similarity search alone.

**ROI for a $50M-procurement manufacturer:** Conservative savings of $4.3M/year from procurement cost reduction, engineering time savings, inventory carrying reduction, and negotiation leverage -- against a system cost of ~$100K/year. That is a 43x return.

**Key statistics:**
- 60% of part numbers in a typical manufacturing database are duplicates or obsolete (Deloitte)
- 70-80% of new designs are variants of existing parts (Boothroyd/DFMA, PTC research)
- Engineers spend 6 hours on average searching for every new part
- Each redundant part adds $4,500-$7,500/year in inventory carrying costs
- Introducing one new part costs ~$15,000 NPV (PTC research)

## 7+ Departments Served

Similarity search is not a single-department feature. It serves the entire manufacturing organization.

**Design Engineering:** "Does this already exist?" Avoids $15K new-part introduction. A global airplane manufacturer standardized brackets, eliminated 850 part numbers, saved $1.42M on brackets alone.

**Procurement:** Vendor rationalization, make-vs-buy decisions, demand aggregation across plants, alternate MPN discovery. The 70/30 insight: 70% of procurement spend is off-the-shelf MPN-based items where similarity search finds alternates and builds supplier matrices.

**Quality Assurance:** 25-30% of quality issues in Indian auto manufacturing are repeat failures. Similarity search surfaces past NCRs for similar parts, supplier quality history, and FAI plans from similar components.

**Sales:** Quick quoting from historical similar parts closes 15-20% more deals. Verbal-to-part matching bridges the conversation-to-quotation gap.

**Logistics:** Inventory deduplication catches what text-based ERP misses. One Tata Motors supplier audit found ~18% duplicate SKUs representing INR 12Cr in locked working capital.

**Import/Export:** India's customs tariff has 11,000+ HS codes. Similarity search surfaces past import classifications for similar parts, capturing FTA benefits (Indian manufacturers utilize only 25-30% of available FTA benefits).

**Marketing:** Data-backed capability statements ("we have manufactured 340+ turned aerospace-grade titanium components with tolerances under 0.02mm") generated directly from the indexed archive.

## Current Architecture

The similarity search lives in `engines/similarity/` with 5 modules:
- **preprocessor.py** -- converts PDF/DXF/PNG/JPG to clean 224x224 RGB image + thumbnail
- **embedder.py** -- 3 strategies: Gemini API text-hash (default), image hash (fallback), DINOv2 (future)
- **indexer.py** -- FAISS IndexFlatIP or numpy brute-force, JSON metadata sidecar
- **ranker.py** -- 4-signal weighted ranking: 0.5 visual + 0.2 material + 0.2 dimension + 0.1 process
- **searcher.py** -- orchestrates ingest, embed, store, search, rank, return top 5

Production API uses Supabase pgvector via `match_drawings` RPC, rate-limited at 15/min with $0.50/48h per-user budget cap.

**Critical gap:** The current Gemini strategy sends a drawing to Gemini Flash, gets a 50-word text description, then hashes character trigrams into 256 bins using MD5. This is fundamentally lossy -- two visually similar drawings with different text descriptions hash to different vectors.

## Target Architecture

### Embedding Models

| Phase | Model | Why |
|-------|-------|-----|
| Now | Gemini Embedding 2 (768-dim) | Real learned embeddings, embeds PDFs directly (up to 6 pages), Matryoshka (truncatable) |
| Next | DINOv2-ViT-B/14 (768-dim) | 2.3x better visual similarity than CLIP (64% vs 28% accuracy), runs on 8GB RAM CPU |
| Later | Fine-tuned DINOv2 | Contrastive learning on 200-500 drawing pairs, $5-15 on cloud GPU |
| Future | GC-CAD GNN | Self-supervised GNN for STEP file B-Rep retrieval, 100x efficiency |

For on-prem defense deployment: ColFlor (174M params) is 17x smaller than ColPali with only 1.8% quality drop, fits 8GB RAM.

### Hybrid Search

Combine dense vectors (semantic) with sparse BM25 (exact match):
- Dense: "turned aluminum shaft" matches "CNC lathe machined AL6061 spindle"
- Sparse: part numbers, material grades like "IS 2062 E250", tolerance "±0.05mm"

Implementation: PostgreSQL `tsvector` on part descriptions + material names + part numbers. Combine scores with Reciprocal Rank Fusion (RRF): `score = sum(1/(k + rank_i))` where k=60.

### 6-Signal Ranking

Upgrade from 4 signals to 6: visual similarity + material match + dimension proximity + process match + tolerance class + surface finish. Dynamic alpha tuning (DAT) can learn per-query weights instead of fixed weights.

### Re-Ranking

Two-stage retrieval: fast bi-encoder retrieves top 100, then expensive cross-encoder re-ranks to top 10. Options:
- FlashRank -- lightweight, open-source, resource-constrained environments
- BAAI/bge-reranker-v2-m3 -- open-source, self-hostable, multilingual
- ColBERT v2 -- late interaction, pre-computes token embeddings

### Role Presets

Different departments weight ranking signals differently:
- Designer: visual-heavy (shape and geometry matter most)
- Procurement: material-heavy (cost and supplier matter most)
- QA: process-heavy (manufacturing method and tolerances matter most)

## Infrastructure Scaling

pgvector on Supabase is sufficient until 50M+ vectors. At our scale (<10K drawings for years), pgvector HNSW delivers 471 QPS at 99% recall with pgvectorscale. No need for a separate vector database.

| Scale | Documents | Annual Cost |
|-------|-----------|-------------|
| Startup (10K) | Today | $400-850 |
| Mid-size (1M) | Future | $10K-27K |
| Enterprise (100M) | Far future | $560K-1.1M |

## Product Rules

- Similarity search is hard-separated from cost estimation (cost estimation never feeds the similarity index)
- Session-scoped for free users (nothing persisted after session)
- Enterprise tier gets persistent index via explicit opt-in
- Minimum 2 drawings required for similarity
- If user deletes history, data is gone (defense clients are paranoid about data)

## Competitive Position

**No competitor does all three:** should-cost + similarity + institutional memory from 2D drawings.

- CADDi ($1.4B): similarity search only, no should-cost estimation
- aPriori: should-cost only, requires 3D CAD, no similarity
- Glean ($7.2B): horizontal enterprise search, knows nothing about engineering drawings
- PLM systems: search by metadata only, not visual similarity, cost $1,200-2,500/user/year
