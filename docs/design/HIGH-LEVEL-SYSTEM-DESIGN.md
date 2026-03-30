# Costimize — High-Level System Design

> AI-powered should-cost intelligence for manufacturing procurement.
> Last updated: 2026-03-30

---

## 1. System Overview

Costimize provides line-by-line should-cost breakdowns for manufactured parts. Procurement teams upload engineering drawings and receive physics-based cost estimates calibrated for Indian manufacturing economics.

### Core Value Proposition

Procurement teams negotiate with suppliers but lack independent cost data. Costimize calculates what a part *should* cost using physics-based manufacturing models (cycle times, material removal rates, tool life equations), giving buyers evidence-backed negotiation data.

### Supported Part Types

| Type | Engine | Accuracy |
|------|--------|----------|
| CNC Turned/Milled (Mechanical) | Physics-based (Sandvik, Taylor) | +-5-10% |
| Sheet Metal | Laser + bending models | +-10-15% |
| PCB Assembly | BOM + fab + assembly rates | +-10% |
| Cable Assembly | Wire/connector labour model | +-15% |

---

## 2. Architecture Diagram

```
                                     +-----------+
                                     |  Supabase |
                                     |  (Postgres |
                                     |  + Auth    |
                                     |  + pgvector)|
                                     +-----+-----+
                                           |
                                           | RLS-protected queries
                                           |
    +----------------+              +------+-------+              +------------------+
    |                |   REST API   |              |   AI APIs    |                  |
    |   Next.js      +------------->+   FastAPI    +------------->+  OpenAI GPT-4o   |
    |   Frontend     |   (JWT auth) |   Backend    |              |  (Vision)        |
    |   (Vercel)     +<-------------+   (Railway)  +<------------>+                  |
    |                |   JSON resp  |              |              +------------------+
    +-------+--------+              +------+-------+
            |                              |              +------------------+
            |                              +------------->+  Google Gemini   |
            |                              |   AI APIs    |  (Validation +   |
      +-----+------+                      |              |   Embeddings)    |
      |  Supabase  |                      |              +------------------+
      |  JS Client |                      |
      |  (Auth)    |               +------+-------+
      +------------+               |  Cost Engines |
                                   |  (Python)     |
                                   |  - Mechanical |
                                   |  - Sheet Metal|
                                   |  - PCB        |
                                   |  - Cable      |
                                   +--------------+
```

### Component Responsibilities

| Component | Technology | Responsibility |
|-----------|-----------|----------------|
| **Frontend** | Next.js 15 + Tailwind CSS 4 | UI, auth flow, file uploads, result display |
| **Backend API** | FastAPI (Python 3.11) | Request validation, routing, auth verification, budget tracking |
| **Cost Engines** | Python (pure) | Physics-based cost calculations, no external dependencies |
| **Validation Pipeline** | Python + Gemini API | Cross-check physics vs AI estimate, confidence scoring |
| **Similarity Engine** | Python + pgvector | Drawing embeddings, vector search, multi-signal ranking |
| **Database** | Supabase (Postgres) | Users, estimates, drawings, usage logs, embeddings |
| **AI Vision** | OpenAI GPT-4o + Gemini | Drawing dimension extraction, process detection |

---

## 3. Data Flow

### 3.1 Primary Flow: Drawing to Cost Estimate

```
User uploads drawing (PDF/image)
    |
    v
[Frontend] POST /api/extract (multipart file + JWT)
    |
    v
[Backend] Auth check -> Budget check -> Rate limit
    |
    v
[Vision Extractor] GPT-4o analyzes drawing
    |                  |
    | (success)        | (fail)
    v                  v
  Return extracted   [Gemini fallback]
  dimensions +         |
  material +           v
  processes          Return extracted data
    |
    v
[Frontend] User reviews & edits extracted data
    |
    v
[Frontend] POST /api/estimate (extracted_data + quantity)
    |
    v
[Backend] Auth check -> Budget check -> Material resolution
    |
    +-------+--------+
    |                 |
    v                 v
[Physics Engine]   [Gemini Estimator]
  (deterministic)    (independent AI check)
    |                 |
    +-------+---------+
            |
            v
    [Validation Orchestrator]
      Compare delta %
        |
        +-- <= 3%  --> HIGH confidence   --> return physics result
        +-- 3-7%   --> MEDIUM confidence --> return physics + note
        +-- 7-15%  --> LOW confidence    --> run AI arbitrator
        +-- > 15%  --> INSUFFICIENT      --> interactive questions
            |
            v
    [Save to Supabase: estimates table]
    [Log usage: usage_log table]
    [Save training data: validated_estimates table]
            |
            v
    Return full cost breakdown to frontend
```

### 3.2 RFQ Processing Flow

```
User uploads RFQ PDF
    |
    v
[PDF Classifier] Identify document type (RFQ, drawing, spec, contract)
    |
    v
[RFQ Extractor] GPT-4o extracts line items (part#, desc, qty, material)
    |
    v
[Frontend] User reviews extracted line items
    |
    v
[Backend] For each line item:
    +-- resolve material
    +-- detect processes
    +-- run mechanical cost engine
    +-- assign confidence tier
    |
    v
Return aggregated cost breakdown per item + total order cost
```

### 3.3 Similarity Search Flow

```
User uploads 2+ drawings
    |
    v
[Preprocessor] Normalize image (resize, grayscale, clean)
    |
    v
[Embedder] Generate 256-dim vector
    |   Strategy priority:
    |   1. Gemini API text embedding (default, 0 RAM)
    |   2. Image perceptual hash (fallback, 0 deps)
    |   3. DINOv2 (future, GPU required)
    |
    v
[pgvector] Cosine similarity search against user's drawing index
    |
    v
[Ranker] 4-signal weighted score:
    0.50 visual similarity (vector distance)
    0.20 material match
    0.20 dimension proximity
    0.10 process overlap
    |
    v
Return ranked matches with scores + metadata
```

---

## 4. Authentication & Authorization

### Auth Architecture

```
[Browser]
    |
    +-- Supabase JS SDK (client-side auth)
    |     - signUp(email, password)
    |     - signInWithPassword(email, password)
    |     - getSession() -> JWT token
    |
    +-- Next.js Middleware
    |     - Checks Supabase session on protected routes
    |     - Redirects unauthenticated users to /login
    |
    +-- API calls with JWT
          - Authorization: Bearer {supabase_jwt}
          |
          v
    [FastAPI Backend]
          - deps.py: get_current_user()
          - Validates JWT with Supabase service role key
          - Extracts user_id for RLS queries
```

### Protected Routes

| Route | Protection |
|-------|-----------|
| `/dashboard` | Middleware redirect |
| `/estimate/*` | Middleware redirect |
| `/similar` | Middleware redirect |
| `/rfq/*` | Middleware redirect |
| `POST /api/*` | JWT validation in backend |

### Row-Level Security

All database queries go through Supabase with the user's JWT. RLS policies ensure:
- Users can only read/write their own estimates
- Users can only search their own drawing embeddings
- Usage logs are user-scoped (admin has global read)

---

## 5. API Design

### Endpoint Summary

| Method | Path | Purpose | Rate Limit | Cost |
|--------|------|---------|------------|------|
| `POST` | `/api/extract` | Extract from single drawing | 10/min | $0.002 |
| `POST` | `/api/extract/multi` | Extract from multi-sheet drawing | 5/min | $0.005 |
| `POST` | `/api/estimate` | Calculate should-cost | 20/min | $0.01 |
| `POST` | `/api/estimate/assembly` | Assembly cost estimate | 10/min | $0.01 |
| `GET` | `/api/estimates` | List user's estimates | 30/min | free |
| `GET` | `/api/estimates/{id}` | Get estimate detail | 30/min | free |
| `POST` | `/api/similarity/embed` | Embed a drawing | 15/min | $0.005 |
| `POST` | `/api/similarity/search` | Find similar drawings | 15/min | $0.005 |
| `POST` | `/api/rfq/extract` | Extract RFQ line items | 5/min | $0.01 |
| `POST` | `/api/rfq/estimate` | Bulk estimate RFQ items | 5/min | $0.01/item |
| `GET` | `/api/material-price` | Get material INR price | 30/min | free |
| `GET` | `/api/usage` | User usage stats | 30/min | free |
| `GET` | `/api/health` | Health check | unlimited | free |

### Error Handling Strategy

```
All errors return:
{
  "detail": "Human-readable error message"
}

HTTP status codes:
  400 - Bad request (invalid input, missing fields)
  401 - Unauthorized (missing/invalid JWT)
  403 - Forbidden (budget exceeded, rate limit)
  404 - Not found (estimate doesn't exist)
  413 - File too large (> 10MB drawings, > 20MB RFQ)
  422 - Validation error (Pydantic model mismatch)
  429 - Rate limited
  500 - Internal server error (logged, generic message to client)
```

---

## 6. Budget & Rate Limiting

### Cost Control Architecture

```
Every AI-consuming endpoint:
    |
    v
[1. Rate Limiter] slowapi: X req/min per IP
    |
    v
[2. Auth Check] Validate JWT, extract user_id
    |
    v
[3. Global Budget] SELECT SUM(cost) FROM usage_log WHERE date = today
    |                  If > $2.00/day -> 403 "Budget exceeded"
    v
[4. User Budget] SELECT SUM(cost) FROM usage_log WHERE user_id AND last 48h
    |                  If > $0.50 -> 403 "User budget exceeded"
    v
[5. Execute Request]
    |
    v
[6. Log Usage] INSERT INTO usage_log (user_id, action, cost_usd, metadata)
```

### Budget Limits

| Scope | Limit | Window | Rationale |
|-------|-------|--------|-----------|
| Global | $2.00 | 24 hours | Prevent runaway API costs |
| Per user | $0.50 | 48 hours | Fair usage, prevent abuse |

---

## 7. Deployment Architecture

### Production Infrastructure

```
+------------------+        +------------------+        +------------------+
|                  |        |                  |        |                  |
|   GitHub         |        |    Vercel        |        |    Railway       |
|   (costimize-mvp)|------->|    (Frontend)    |------->|    (Backend)     |
|                  | push   |                  | API    |                  |
|   master branch  |        |  Next.js 15      |        |  FastAPI + Uvicorn|
|                  |        |  CDN + Edge      |        |  Docker container |
+------------------+        +--------+---------+        +--------+---------+
                                     |                           |
                                     |                           |
                                     v                           v
                            +------------------+        +------------------+
                            |                  |        |                  |
                            |   Supabase       |        |   OpenAI API     |
                            |   (Postgres +    |        |   Gemini API     |
                            |    Auth +        |        |                  |
                            |    pgvector)     |        +------------------+
                            |                  |
                            +------------------+
```

### Environment Separation

| Environment | Frontend | Backend | Database |
|-------------|----------|---------|----------|
| Local dev | localhost:3000 | localhost:8000 | Supabase (cloud) |
| Production | Vercel CDN | Railway container | Supabase (cloud) |

### CI/CD Pipeline

```
git push to master
    |
    +----> Vercel auto-deploy (frontend)
    |        - npm install
    |        - npx next build
    |        - Deploy to edge
    |
    +----> GitHub Actions (tests)
             - pip install requirements
             - pytest tests/ -q
```

### Manual Backend Deploy

The backend deploys from a separate clean directory (`~/costimize-deploy`, ~705KB) to Railway. This is intentional — the monorepo contains research docs, PDFs, and test fixtures that shouldn't be in the production image.

---

## 8. Scalability Considerations

### Current Scale (MVP)

- Single Vercel deployment (auto-scaling)
- Single Railway container (256MB RAM, 0.5 vCPU)
- Supabase free tier (500MB storage, 2GB bandwidth)
- AI API budget: $2/day

### Growth Bottlenecks

| Bottleneck | Current | Solution Path |
|------------|---------|--------------|
| AI API cost | $2/day cap | Self-hosted VLM (Qwen2.5-VL-7B) |
| Similarity search | pgvector brute-force | FAISS index, DINOv2 local embeddings |
| Concurrent extractions | Single container | Railway horizontal scaling |
| Drawing storage | Supabase Blob | S3-compatible storage |

### Phase Roadmap

```
Phase 1 (NOW): Cloud APIs + physics engines
Phase 2: ML correction factors from validated estimates
Phase 3: Self-hosted VLM (defense clients, no cloud APIs)
Phase 4: Agentic procurement workflows (company memory, auto-negotiation)
```

---

## 9. Security Architecture

### Defense in Depth

```
Layer 1: Network
    - Vercel edge (DDoS protection, TLS termination)
    - Railway container (private network)
    - CORS: only frontend origin allowed

Layer 2: Application
    - Content Security Policy (CSP)
    - HSTS with preload
    - X-Frame-Options: DENY
    - Rate limiting (slowapi)

Layer 3: Authentication
    - Supabase Auth (bcrypt passwords)
    - JWT tokens (short-lived)
    - Middleware route protection

Layer 4: Authorization
    - Row-Level Security (Supabase RLS)
    - Service role key only on backend
    - Anon key on frontend (limited permissions)

Layer 5: Data
    - No secrets in code (env vars only)
    - .env.local in .gitignore
    - Budget caps prevent cost abuse
```

### Threat Model

| Threat | Mitigation |
|--------|-----------|
| API key leakage | Env vars, .gitignore, service role only on backend |
| Budget abuse | Per-user $0.50/48h cap, global $2/day cap |
| Drawing data leak | RLS: users see only own data |
| XSS | React JSX escaping, CSP headers |
| CSRF | Supabase managed tokens |
| DDoS | Vercel edge protection, rate limiting |

---

## 10. Monitoring & Observability

### Current

| Tool | What It Tracks |
|------|---------------|
| Vercel Analytics | Page views, Core Web Vitals |
| usage_log table | Every AI API call with cost |
| Railway logs | Backend request/error logs |
| `/api/admin/usage` | Daily cost, estimate count, signups |

### Future

- Structured logging (JSON) with request IDs
- Error tracking (Sentry)
- Cost dashboard (Grafana or custom)
- Latency monitoring per endpoint

---

## 11. Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Physics-first, ML later | Physics engines are primary | Day-one accuracy without training data |
| Supabase over self-hosted Postgres | Managed auth + pgvector + RLS | Faster shipping, free tier sufficient |
| Separate deploy directories | Monorepo dev, clean deploy | Keep 200MB+ research PDFs out of Docker |
| Frozen dataclasses for results | Immutable cost breakdowns | Prevents accidental mutation, audit trail |
| Gemini for validation (not OpenAI) | Parallel independent check | Different model avoids systematic bias |
| Indian rates hardcoded | config.py constants | Accuracy for target market, updatable per-city later |
| 256-dim embeddings | Sufficient for similarity | Gemini text hash + perceptual hash both fit |
| AI fallback chain | OpenAI -> Gemini | Redundancy for vision extraction |
