# V1 Public Launch — Design Spec

**Date:** 2026-03-29
**Deadline:** 2026-04-14 (16 days)
**Event:** YC Startup School India + Vibecon (Apr 15-16-18)

---

## 1. What We're Building

A public web app where procurement teams upload mechanical engineering drawings and get line-by-line should-cost breakdowns in INR. Plus a similarity search feature to find visually similar parts from history.

### Core Value Proposition

"Upload a drawing. Get the real cost. Negotiate with confidence."

---

## 2. Scope

### In v1

- Landing page (public, no login)
- Email signup/login (name, email, company, sourcing country)
- Mechanical cost estimation (upload drawing → AI extract → physics engine → breakdown)
- Drawing similarity search (upload 2+ drawings → find matches)
- Summary table with expandable full breakdown
- Estimate history (dashboard)
- PDF download of estimate
- User analytics (who signed up, what they estimated)
- Validation pipeline (runs silently, shows confidence badge)
- $20/day API cost cap monitoring

### Not in v1

- Sheet metal / PCB / cable engines (v1.1 after event)
- Payments / billing
- Team accounts
- Admin dashboard
- Custom domain (deploy to Vercel free URL)
- Google OAuth (email/password only)

---

## 3. Architecture

```
Frontend (Vercel, free)          Backend (Railway, $5/mo)         Database (Supabase, free)
┌─────────────────┐             ┌─────────────────┐             ┌─────────────────┐
│   Next.js App   │────API───▶  │   FastAPI        │────SQL───▶  │   Supabase      │
│                 │             │                  │             │                 │
│ - Landing page  │             │ - /api/extract   │             │ Auth:           │
│ - Auth (Supa)   │             │ - /api/estimate  │             │ - users table   │
│ - Dashboard     │             │ - /api/similar   │             │                 │
│ - Estimate flow │             │ - /api/estimates │             │ Tables:         │
│ - Similar parts │             │ - /api/usage     │             │ - profiles      │
│ - UI via Stitch │             │                  │             │ - estimates     │
│                 │             │ Python engines:  │             │ - drawings      │
│                 │             │ - mechanical/*   │             │ - usage_log     │
│                 │             │ - similarity/*   │             │                 │
│                 │             │ - validation/*   │             │ Storage:        │
│                 │             │ - extractors/*   │             │ - drawings bucket│
└─────────────────┘             └─────────────────┘             └─────────────────┘
```

### Key Decisions

- Python engines stay exactly as they are — zero rewrite
- FastAPI is a thin API wrapper around existing engines
- Next.js handles UI + auth via Supabase client SDK
- Supabase replaces JSON file storage
- Uploaded drawings stored in Supabase Storage (free 1GB)
- UI built with Stitch (design system + component generation)

---

## 4. Database Schema (Supabase)

### profiles

Extends Supabase auth.users:

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | FK to auth.users |
| full_name | text | Required at signup |
| email | text | From auth |
| company | text | Required at signup |
| sourcing_country | text | Dropdown at signup |
| created_at | timestamptz | Auto |

### estimates

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | PK |
| user_id | uuid | FK to profiles |
| part_type | text | 'mechanical' for v1 |
| drawing_url | text | Supabase Storage path |
| extracted_data | jsonb | AI-extracted dimensions/processes |
| cost_breakdown | jsonb | Full engine output (frozen dataclass → JSON) |
| total_cost | decimal | Summary total in INR |
| confidence_tier | text | HIGH/MEDIUM/LOW/INSUFFICIENT |
| currency | text | 'INR' default |
| created_at | timestamptz | Auto |

### drawings (for similarity search)

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | PK |
| user_id | uuid | FK to profiles |
| file_url | text | Supabase Storage path |
| embedding | vector(256) | For similarity search |
| metadata | jsonb | Material, dimensions, processes |
| created_at | timestamptz | Auto |

### usage_log (analytics)

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | PK |
| user_id | uuid | FK to profiles |
| action | text | 'estimate', 'similarity', 'signup', 'login' |
| api_cost_usd | decimal | Estimated API cost for this action |
| details | jsonb | Part type, file name, etc. |
| created_at | timestamptz | Auto |

---

## 5. API Endpoints (FastAPI)

### POST /api/extract

Upload drawing → AI extracts dimensions + processes.

- **Input:** multipart file (PDF/image)
- **Output:** `{ dimensions: {...}, processes: [...], material: "..." }`
- **Calls:** OpenAI GPT-4o (primary) → Gemini (fallback)
- **Est. cost:** $0.01-0.03 per call

### POST /api/estimate

Extracted data → cost breakdown.

- **Input:** `{ extracted_data: {...}, quantity: 1 }`
- **Output:** `{ summary: {...}, breakdown: [...], total: 2672, confidence: "HIGH" }`
- **Calls:** mechanical cost engine + validation pipeline (Gemini)
- **Est. cost:** $0.005-0.01 per call (Gemini validation)

### POST /api/similarity/embed

Upload drawing → generate embedding.

- **Input:** multipart file (PDF/image)
- **Output:** `{ drawing_id: "...", embedding: [...] }`
- **Calls:** Gemini API for embedding

### POST /api/similarity/search

Find similar drawings.

- **Input:** `{ drawing_id: "...", top_k: 5 }`
- **Output:** `{ matches: [{ drawing_id, score, metadata, estimate_summary }] }`

### GET /api/estimates

User's estimate history.

- **Input:** auth token (header)
- **Output:** `{ estimates: [...] }`

### GET /api/usage

Usage stats for current user.

- **Input:** auth token (header)
- **Output:** `{ total_estimates: 12, total_similarity: 3, joined: "2026-04-15" }`

### GET /api/admin/usage (internal only)

Daily API cost tracking.

- **Output:** `{ today_cost_usd: 4.20, estimates_today: 105, signups_today: 23 }`

---

## 6. User Flow

```
1. User lands on /                    → sees landing page
2. Clicks "Try it free"              → /login (signup form)
3. Fills: name, email, pw, company,  → account created
   sourcing country
4. Redirected to /dashboard          → welcome + two cards
5. Clicks "New Estimate"             → /estimate/new
6. Uploads drawing (drag & drop)     → loading: "AI analyzing..."
7. AI extracts dims + processes      → shows extracted data for review
8. Clicks "Calculate Cost"           → loading: "Calculating..."
9. Summary table appears             → total + key line items + confidence badge
10. Clicks "Expand full breakdown"   → all sub-lines visible
11. Clicks "Download PDF"            → PDF generated client-side
12. Estimate auto-saved to history   → visible on /dashboard

Similarity flow:
1. From /dashboard clicks "Similar Parts"  → /similar
2. Uploads 2+ drawings                     → embeddings generated
3. Sees similarity matrix                  → scores + matched historical costs
```

---

## 7. User Asks: Sourcing Country

At signup, user selects sourcing country. This affects:

- Currency display (INR for India, USD for others)
- Labour rates in cost engine (Indian rates vs adjusted international rates)
- Material prices (Indian market vs global)

For v1: **India only** (INR pricing, Indian rates). Country field collected for future use but doesn't change calculations yet. This is honest — the engine is built on Indian manufacturing data.

---

## 8. Cost Control

### $20/day API budget

| API | Cost per call | Calls per estimate | Cost per estimate |
|-----|--------------|-------------------|-------------------|
| GPT-4o vision | $0.01-0.03 | 1 | $0.03 |
| Gemini validation | $0.005-0.01 | 1 | $0.01 |
| **Total per estimate** | | | **~$0.04** |

$20/day = ~500 estimates/day. More than enough for event traffic.

### Monitoring

- usage_log table tracks every API call cost
- /api/admin/usage endpoint shows running daily total
- Alert (email or log) if daily cost exceeds $15 (75% threshold)
- Hard stop at $20 — return "Service temporarily at capacity" message

---

## 9. Landing Page Content

### Hero

**Headline:** "Know the real cost before you negotiate."
**Subhead:** "AI-powered should-cost breakdowns for mechanical parts. Line by line. Physics-based. Accurate to +/-10%."
**CTA:** "Try it free"

### How it works

1. Upload your engineering drawing (PDF or image)
2. AI extracts dimensions, tolerances, and processes
3. Get a line-by-line should-cost breakdown in seconds

### Who it's for

- Procurement teams negotiating with suppliers
- Defense, aerospace, and automotive manufacturers
- Anyone buying custom machined parts

### Trust signals

(To be crafted during landing page design — not needed in spec)

---

## 10. Tech Stack Summary

| Layer | Technology | Cost |
|-------|-----------|------|
| Frontend | Next.js on Vercel | Free |
| UI Components | Stitch | Free |
| Backend | FastAPI on Railway | $5/mo |
| Database | Supabase (Postgres) | Free tier |
| Auth | Supabase Auth | Free tier |
| File Storage | Supabase Storage | Free (1GB) |
| AI Vision | OpenAI GPT-4o | ~$0.03/call |
| AI Validation | Google Gemini | ~$0.01/call |
| AI Embeddings | Google Gemini | ~$0.005/call |
| PDF Generation | Client-side (jsPDF or react-pdf) | Free |

**Total fixed cost: $5/month**
**Variable cost: ~$0.04 per estimate**

---

## 11. What's NOT in v1 (Explicitly Deferred)

| Feature | When |
|---------|------|
| Sheet metal engine | v1.1 (week after event) |
| PCB engine | v1.2 |
| Cable engine | v1.2 |
| Payments/billing | After free tier users hit limits |
| Custom domain | After validation at event |
| Google OAuth | v1.1 |
| Team accounts | v2 |
| Admin dashboard | v1.1 (basic Supabase dashboard for now) |
| International rates | v2 (India only for now) |
| DXF/STEP upload | v2 |

---

## 12. Risk Assessment

| Risk | Mitigation |
|------|-----------|
| 16 days too tight | Mechanical only, UI from Stitch, engines unchanged |
| API costs spike | $20/day hard cap with monitoring |
| AI extraction fails on bad drawings | Show "couldn't extract" with manual input fallback |
| Supabase free tier limits | 500MB DB, 1GB storage, 50K auth users — more than enough |
| Railway downtime | Free tier has cold starts; upgrade to $5 plan for always-on |
| Demo at event fails | Have 2-3 pre-run estimates cached as fallback demo |
