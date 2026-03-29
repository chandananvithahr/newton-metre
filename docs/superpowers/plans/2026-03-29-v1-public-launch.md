# V1 Public Launch — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a public web app (FastAPI + Next.js + Supabase) for mechanical should-cost estimation + similarity search by April 14.

**Architecture:** FastAPI wraps existing Python engines as API endpoints. Next.js frontend (UI via Stitch) handles auth and pages. Supabase provides auth, database, and file storage. Python engines are untouched.

**Tech Stack:** Python 3.11+, FastAPI, Next.js 14+, Supabase (Auth + Postgres + Storage), Vercel, Railway

---

## File Structure

### Backend (new: `costimize-v2/api/`)

| File | Responsibility |
|------|---------------|
| `api/__init__.py` | Package init |
| `api/main.py` | FastAPI app, CORS, lifespan |
| `api/deps.py` | Supabase client, auth dependency, cost tracker |
| `api/routes/extract.py` | POST /api/extract — drawing upload + AI extraction |
| `api/routes/estimate.py` | POST /api/estimate — cost calculation + validation |
| `api/routes/similarity.py` | POST /api/similarity/embed + /api/similarity/search |
| `api/routes/estimates.py` | GET /api/estimates — user history |
| `api/routes/usage.py` | GET /api/usage + GET /api/admin/usage |
| `api/schemas.py` | Pydantic request/response models |
| `api/cost_tracker.py` | Daily API cost tracking + $20 cap enforcement |
| `tests/test_api.py` | API endpoint tests |

### Frontend (new: `frontend/`)

| File | Responsibility |
|------|---------------|
| `frontend/package.json` | Next.js + dependencies |
| `frontend/.env.local` | NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY, NEXT_PUBLIC_API_URL |
| `frontend/src/lib/supabase.ts` | Supabase client singleton |
| `frontend/src/lib/api.ts` | Typed API client for FastAPI backend |
| `frontend/src/middleware.ts` | Auth redirect (protect /dashboard, /estimate, /similar) |
| `frontend/src/app/layout.tsx` | Root layout |
| `frontend/src/app/page.tsx` | Landing page |
| `frontend/src/app/login/page.tsx` | Signup + login form |
| `frontend/src/app/dashboard/page.tsx` | Dashboard with estimate history |
| `frontend/src/app/estimate/new/page.tsx` | Upload → extract → calculate flow |
| `frontend/src/app/estimate/[id]/page.tsx` | View saved estimate |
| `frontend/src/app/similar/page.tsx` | Similarity search |

### Supabase (migrations)

| File | Responsibility |
|------|---------------|
| `supabase/migrations/001_profiles.sql` | profiles table + RLS |
| `supabase/migrations/002_estimates.sql` | estimates table + RLS |
| `supabase/migrations/003_drawings.sql` | drawings table + RLS |
| `supabase/migrations/004_usage_log.sql` | usage_log table + RLS |

### Deployment

| File | Responsibility |
|------|---------------|
| `costimize-v2/Dockerfile` | FastAPI container for Railway |
| `costimize-v2/api/requirements.txt` | API-specific dependencies (fastapi, uvicorn, supabase, python-multipart) |
| `frontend/vercel.json` | Vercel config (rewrites, env) |

---

## Task 1: Supabase Setup + Database Schema

**Files:**
- Create: `supabase/migrations/001_profiles.sql`
- Create: `supabase/migrations/002_estimates.sql`
- Create: `supabase/migrations/003_drawings.sql`
- Create: `supabase/migrations/004_usage_log.sql`

**Prerequisite:** User must create a Supabase project at supabase.com and provide the project URL + anon key + service role key.

- [ ] **Step 1: Create Supabase project**

Go to supabase.com → New Project → note down:
- Project URL (e.g., https://xxxxx.supabase.co)
- Anon key (public)
- Service role key (secret, for backend only)

- [ ] **Step 2: Create profiles table migration**

Create file `supabase/migrations/001_profiles.sql`:

```sql
-- profiles table — extends Supabase auth.users
create table public.profiles (
    id uuid references auth.users(id) on delete cascade primary key,
    full_name text not null,
    email text not null,
    company text not null,
    sourcing_country text not null default 'India',
    created_at timestamptz not null default now()
);

-- Enable RLS
alter table public.profiles enable row level security;

-- Users can read/update their own profile
create policy "Users can view own profile"
    on public.profiles for select
    using (auth.uid() = id);

create policy "Users can update own profile"
    on public.profiles for update
    using (auth.uid() = id);

create policy "Users can insert own profile"
    on public.profiles for insert
    with check (auth.uid() = id);

-- Auto-create profile on signup via trigger
create or replace function public.handle_new_user()
returns trigger as $$
begin
    insert into public.profiles (id, full_name, email, company, sourcing_country)
    values (
        new.id,
        coalesce(new.raw_user_meta_data->>'full_name', ''),
        new.email,
        coalesce(new.raw_user_meta_data->>'company', ''),
        coalesce(new.raw_user_meta_data->>'sourcing_country', 'India')
    );
    return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
    after insert on auth.users
    for each row execute function public.handle_new_user();
```

- [ ] **Step 3: Create estimates table migration**

Create file `supabase/migrations/002_estimates.sql`:

```sql
create table public.estimates (
    id uuid default gen_random_uuid() primary key,
    user_id uuid references public.profiles(id) on delete cascade not null,
    part_type text not null default 'mechanical',
    drawing_url text,
    extracted_data jsonb,
    cost_breakdown jsonb not null,
    total_cost decimal not null,
    confidence_tier text,
    currency text not null default 'INR',
    created_at timestamptz not null default now()
);

alter table public.estimates enable row level security;

create policy "Users can view own estimates"
    on public.estimates for select
    using (auth.uid() = user_id);

create policy "Users can insert own estimates"
    on public.estimates for insert
    with check (auth.uid() = user_id);

create index idx_estimates_user_id on public.estimates(user_id);
create index idx_estimates_created_at on public.estimates(created_at desc);
```

- [ ] **Step 4: Create drawings table migration**

Create file `supabase/migrations/003_drawings.sql`:

```sql
-- Enable pgvector extension for similarity search
create extension if not exists vector;

create table public.drawings (
    id uuid default gen_random_uuid() primary key,
    user_id uuid references public.profiles(id) on delete cascade not null,
    file_url text not null,
    embedding vector(256),
    metadata jsonb,
    created_at timestamptz not null default now()
);

alter table public.drawings enable row level security;

create policy "Users can view own drawings"
    on public.drawings for select
    using (auth.uid() = user_id);

create policy "Users can insert own drawings"
    on public.drawings for insert
    with check (auth.uid() = user_id);

create index idx_drawings_user_id on public.drawings(user_id);
```

- [ ] **Step 5: Create usage_log table migration**

Create file `supabase/migrations/004_usage_log.sql`:

```sql
create table public.usage_log (
    id uuid default gen_random_uuid() primary key,
    user_id uuid references public.profiles(id) on delete set null,
    action text not null,
    api_cost_usd decimal not null default 0,
    details jsonb,
    created_at timestamptz not null default now()
);

alter table public.usage_log enable row level security;

-- Users can view own usage
create policy "Users can view own usage"
    on public.usage_log for select
    using (auth.uid() = user_id);

-- Backend inserts via service role key (bypasses RLS)
-- No insert policy needed for regular users

create index idx_usage_log_user_id on public.usage_log(user_id);
create index idx_usage_log_created_at on public.usage_log(created_at desc);
```

- [ ] **Step 6: Create Supabase Storage bucket**

In Supabase dashboard → Storage → New Bucket:
- Name: `drawings`
- Public: No
- File size limit: 10MB
- Allowed MIME types: `image/png, image/jpeg, application/pdf`

Add RLS policy: users can upload to their own folder (`user_id/filename`).

- [ ] **Step 7: Run migrations**

In Supabase dashboard → SQL Editor → paste each migration file and run in order (001 → 004).

- [ ] **Step 8: Commit**

```bash
git add supabase/
git commit -m "feat: add Supabase database schema migrations"
```

---

## Task 2: FastAPI Backend — Core Setup + Dependencies

**Files:**
- Create: `costimize-v2/api/__init__.py`
- Create: `costimize-v2/api/main.py`
- Create: `costimize-v2/api/deps.py`
- Create: `costimize-v2/api/schemas.py`
- Create: `costimize-v2/api/cost_tracker.py`
- Create: `costimize-v2/api/requirements.txt`

- [ ] **Step 1: Create API requirements**

Create file `costimize-v2/api/requirements.txt`:

```
fastapi==0.115.0
uvicorn[standard]==0.30.0
python-multipart==0.0.9
supabase==2.9.1
pydantic==2.9.0
python-dotenv==1.0.1
```

- [ ] **Step 2: Install dependencies**

Run: `cd costimize-v2 && pip install -r api/requirements.txt`

- [ ] **Step 3: Create Pydantic schemas**

Create file `costimize-v2/api/schemas.py`:

```python
"""Request/response models for the API."""
from pydantic import BaseModel


class ExtractionResponse(BaseModel):
    dimensions: dict
    material: str | None
    tolerances: dict
    suggested_processes: list[str]
    confidence: str
    notes: str


class EstimateRequest(BaseModel):
    extracted_data: dict
    quantity: int = 1


class ProcessLine(BaseModel):
    process_id: str
    process_name: str
    time_min: float
    machine_cost: float
    setup_cost_per_unit: float
    tooling_cost: float
    labour_cost: float
    power_cost: float


class EstimateResponse(BaseModel):
    material_name: str
    material_cost: float
    process_lines: list[ProcessLine]
    total_machining_cost: float
    total_setup_cost: float
    total_tooling_cost: float
    total_labour_cost: float
    total_power_cost: float
    subtotal: float
    overhead: float
    profit: float
    unit_cost: float
    order_cost: float
    quantity: int
    confidence_tier: str | None
    currency: str = "INR"


class SimilarityEmbedResponse(BaseModel):
    drawing_id: str
    message: str


class SimilarityMatch(BaseModel):
    drawing_id: str
    score: float
    metadata: dict


class SimilaritySearchResponse(BaseModel):
    matches: list[SimilarityMatch]


class UsageResponse(BaseModel):
    total_estimates: int
    total_similarity: int
    joined: str


class AdminUsageResponse(BaseModel):
    today_cost_usd: float
    estimates_today: int
    signups_today: int


class EstimateHistoryItem(BaseModel):
    id: str
    part_type: str
    total_cost: float
    confidence_tier: str | None
    currency: str
    created_at: str
```

- [ ] **Step 4: Create dependencies module**

Create file `costimize-v2/api/deps.py`:

```python
"""Shared dependencies — Supabase client, auth, cost tracking."""
import os
from functools import lru_cache

from dotenv import load_dotenv
from fastapi import Header, HTTPException
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
SUPABASE_ANON_KEY = os.environ["SUPABASE_ANON_KEY"]


@lru_cache()
def get_supabase_admin() -> Client:
    """Service role client — bypasses RLS. For backend writes only."""
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def get_supabase_client() -> Client:
    """Anon client — respects RLS. For user-scoped queries."""
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


async def get_current_user_id(authorization: str = Header(...)) -> str:
    """Extract user ID from Supabase JWT in Authorization header.

    Header format: 'Bearer <jwt_token>'
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = authorization.split(" ", 1)[1]
    client = get_supabase_client()

    try:
        user_response = client.auth.get_user(token)
        if user_response and user_response.user:
            return user_response.user.id
    except Exception:
        pass

    raise HTTPException(status_code=401, detail="Invalid or expired token")
```

- [ ] **Step 5: Create cost tracker**

Create file `costimize-v2/api/cost_tracker.py`:

```python
"""Daily API cost tracking with $20/day hard cap."""
from datetime import date

from api.deps import get_supabase_admin

DAILY_BUDGET_USD = 20.0
ALERT_THRESHOLD_USD = 15.0


def get_daily_cost() -> float:
    """Get total API cost for today in USD."""
    sb = get_supabase_admin()
    today = date.today().isoformat()
    result = sb.table("usage_log") \
        .select("api_cost_usd") \
        .gte("created_at", f"{today}T00:00:00Z") \
        .execute()
    return sum(row["api_cost_usd"] for row in result.data) if result.data else 0.0


def check_budget() -> bool:
    """Returns True if under budget, False if over."""
    return get_daily_cost() < DAILY_BUDGET_USD


def log_usage(user_id: str, action: str, api_cost_usd: float, details: dict | None = None) -> None:
    """Log an API usage event."""
    sb = get_supabase_admin()
    sb.table("usage_log").insert({
        "user_id": user_id,
        "action": action,
        "api_cost_usd": api_cost_usd,
        "details": details or {},
    }).execute()
```

- [ ] **Step 6: Create FastAPI main app**

Create file `costimize-v2/api/__init__.py`:

```python
```

Create file `costimize-v2/api/main.py`:

```python
"""FastAPI app — thin wrapper around existing Python cost engines."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import extract, estimate, similarity, estimates, usage

app = FastAPI(
    title="Costimize API",
    description="Should-cost intelligence for mechanical parts",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(extract.router, prefix="/api")
app.include_router(estimate.router, prefix="/api")
app.include_router(similarity.router, prefix="/api")
app.include_router(estimates.router, prefix="/api")
app.include_router(usage.router, prefix="/api")


@app.get("/api/health")
async def health():
    return {"status": "ok"}
```

- [ ] **Step 7: Commit**

```bash
git add costimize-v2/api/
git commit -m "feat: add FastAPI core setup with schemas, deps, cost tracker"
```

---

## Task 3: FastAPI Routes — Extract + Estimate

**Files:**
- Create: `costimize-v2/api/routes/__init__.py`
- Create: `costimize-v2/api/routes/extract.py`
- Create: `costimize-v2/api/routes/estimate.py`

- [ ] **Step 1: Create routes package**

Create file `costimize-v2/api/routes/__init__.py`:

```python
```

- [ ] **Step 2: Create extract route**

Create file `costimize-v2/api/routes/extract.py`:

```python
"""POST /api/extract — upload drawing, AI extracts dimensions + processes."""
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from api.deps import get_current_user_id
from api.cost_tracker import check_budget, log_usage
from api.schemas import ExtractionResponse

router = APIRouter()


@router.post("/extract", response_model=ExtractionResponse)
async def extract_drawing(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
):
    if not check_budget():
        raise HTTPException(status_code=429, detail="Service temporarily at capacity. Please try again tomorrow.")

    image_bytes = await file.read()
    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Maximum 10MB.")

    try:
        from extractors.vision import analyze_drawing
        result = analyze_drawing(image_bytes, file.filename or "drawing.png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze drawing: {str(e)}")

    log_usage(user_id, "extract", 0.03, {"filename": file.filename})

    return ExtractionResponse(
        dimensions=result.get("dimensions", {}),
        material=result.get("material"),
        tolerances=result.get("tolerances", {}),
        suggested_processes=result.get("suggested_processes", []),
        confidence=result.get("confidence", "low"),
        notes=result.get("notes", ""),
    )
```

- [ ] **Step 3: Create estimate route**

Create file `costimize-v2/api/routes/estimate.py`:

```python
"""POST /api/estimate — run physics engine + validation, return cost breakdown."""
import dataclasses

from fastapi import APIRouter, Depends, HTTPException

from api.deps import get_current_user_id, get_supabase_admin
from api.cost_tracker import check_budget, log_usage
from api.schemas import EstimateRequest, EstimateResponse

router = APIRouter()


@router.post("/estimate", response_model=EstimateResponse)
async def create_estimate(
    body: EstimateRequest,
    user_id: str = Depends(get_current_user_id),
):
    if not check_budget():
        raise HTTPException(status_code=429, detail="Service temporarily at capacity. Please try again tomorrow.")

    extracted = body.extracted_data
    dims = extracted.get("dimensions", {})
    material = extracted.get("material", "Mild Steel")
    processes = extracted.get("suggested_processes", ["turning"])
    has_tight = extracted.get("tolerances", {}).get("has_tight_tolerances", False)

    try:
        from engines.validation.orchestrator import orchestrate
        result = orchestrate(
            image_bytes=None,
            dimensions=dims,
            material_name=material,
            selected_processes=processes,
            quantity=body.quantity,
            has_tight_tolerances=has_tight,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cost calculation failed: {str(e)}")

    breakdown = result.physics_result
    confidence = result.confidence_tier.value if result.confidence_tier else None

    process_lines = [
        {
            "process_id": pl.process_id,
            "process_name": pl.process_name,
            "time_min": pl.time_min,
            "machine_cost": pl.machine_cost,
            "setup_cost_per_unit": pl.setup_cost_per_unit,
            "tooling_cost": pl.tooling_cost,
            "labour_cost": pl.labour_cost,
            "power_cost": pl.power_cost,
        }
        for pl in breakdown.process_lines
    ]

    # Save to Supabase
    sb = get_supabase_admin()
    sb.table("estimates").insert({
        "user_id": user_id,
        "part_type": "mechanical",
        "extracted_data": extracted,
        "cost_breakdown": {
            "material_name": breakdown.material_name,
            "material_cost": breakdown.material_cost,
            "process_lines": process_lines,
            "total_machining_cost": breakdown.total_machining_cost,
            "total_setup_cost": breakdown.total_setup_cost,
            "total_tooling_cost": breakdown.total_tooling_cost,
            "total_labour_cost": breakdown.total_labour_cost,
            "total_power_cost": breakdown.total_power_cost,
            "subtotal": breakdown.subtotal,
            "overhead": breakdown.overhead,
            "profit": breakdown.profit,
        },
        "total_cost": breakdown.unit_cost,
        "confidence_tier": confidence,
    }).execute()

    log_usage(user_id, "estimate", 0.01, {"material": material, "processes": processes})

    return EstimateResponse(
        material_name=breakdown.material_name,
        material_cost=breakdown.material_cost,
        process_lines=process_lines,
        total_machining_cost=breakdown.total_machining_cost,
        total_setup_cost=breakdown.total_setup_cost,
        total_tooling_cost=breakdown.total_tooling_cost,
        total_labour_cost=breakdown.total_labour_cost,
        total_power_cost=breakdown.total_power_cost,
        subtotal=breakdown.subtotal,
        overhead=breakdown.overhead,
        profit=breakdown.profit,
        unit_cost=breakdown.unit_cost,
        order_cost=breakdown.order_cost,
        quantity=breakdown.quantity,
        confidence_tier=confidence,
    )
```

- [ ] **Step 4: Write test for extract + estimate endpoints**

Create file `costimize-v2/tests/test_api.py`:

```python
"""Tests for FastAPI endpoints."""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

# Mock deps before importing app
with patch("api.deps.get_current_user_id", return_value="test-user-123"):
    from api.main import app

client = TestClient(app)


def auth_headers():
    return {"Authorization": "Bearer test-token"}


@patch("api.deps.get_current_user_id", return_value="test-user-123")
@patch("api.cost_tracker.check_budget", return_value=True)
@patch("api.cost_tracker.log_usage")
@patch("extractors.vision.analyze_drawing")
def test_extract_returns_dimensions(mock_analyze, mock_log, mock_budget, mock_auth):
    mock_analyze.return_value = {
        "dimensions": {"outer_diameter_mm": 50, "length_mm": 100},
        "material": "Aluminum 6061",
        "tolerances": {"has_tight_tolerances": False},
        "suggested_processes": ["turning", "facing"],
        "confidence": "high",
        "notes": "",
    }
    response = client.post(
        "/api/extract",
        files={"file": ("test.png", b"fake-image-bytes", "image/png")},
        headers=auth_headers(),
    )
    assert response.status_code == 200
    data = response.json()
    assert data["dimensions"]["outer_diameter_mm"] == 50
    assert data["material"] == "Aluminum 6061"


@patch("api.deps.get_current_user_id", return_value="test-user-123")
@patch("api.cost_tracker.check_budget", return_value=False)
def test_extract_rejects_over_budget(mock_budget, mock_auth):
    response = client.post(
        "/api/extract",
        files={"file": ("test.png", b"fake", "image/png")},
        headers=auth_headers(),
    )
    assert response.status_code == 429


@patch("api.deps.get_current_user_id", return_value="test-user-123")
@patch("api.cost_tracker.check_budget", return_value=True)
@patch("api.cost_tracker.log_usage")
@patch("api.deps.get_supabase_admin")
@patch("engines.validation.orchestrator.orchestrate")
def test_estimate_returns_breakdown(mock_orch, mock_sb, mock_log, mock_budget, mock_auth):
    from engines.mechanical.cost_engine import MechanicalCostBreakdown, ProcessCostLine
    from engines.validation.comparator import ConfidenceTier

    mock_orch.return_value = MagicMock(
        physics_result=MechanicalCostBreakdown(
            material_name="Mild Steel",
            raw_weight_kg=0.5,
            wastage_weight_kg=0.075,
            material_cost=50.0,
            process_lines=(
                ProcessCostLine("turning", "CNC Turning", 5.0, 66.7, 20.0, 5.0, 20.8, 2.0),
            ),
            total_machining_cost=66.7,
            total_setup_cost=20.0,
            total_tooling_cost=5.0,
            total_labour_cost=20.8,
            total_power_cost=2.0,
            subtotal=164.5,
            overhead=24.7,
            profit=37.8,
            unit_cost=227.0,
            order_cost=227.0,
            quantity=1,
        ),
        confidence_tier=ConfidenceTier.HIGH,
    )
    mock_sb.return_value.table.return_value.insert.return_value.execute.return_value = None

    response = client.post(
        "/api/estimate",
        json={
            "extracted_data": {
                "dimensions": {"outer_diameter_mm": 50, "length_mm": 100},
                "material": "Mild Steel",
                "suggested_processes": ["turning"],
                "tolerances": {"has_tight_tolerances": False},
            },
            "quantity": 1,
        },
        headers=auth_headers(),
    )
    assert response.status_code == 200
    data = response.json()
    assert data["unit_cost"] == 227.0
    assert data["confidence_tier"] == "HIGH"
```

- [ ] **Step 5: Run tests**

Run: `cd costimize-v2 && python -m pytest tests/test_api.py -v`
Expected: 3 tests PASS

- [ ] **Step 6: Commit**

```bash
git add costimize-v2/api/routes/ costimize-v2/tests/test_api.py
git commit -m "feat: add extract and estimate API routes with tests"
```

---

## Task 4: FastAPI Routes — Similarity, History, Usage

**Files:**
- Create: `costimize-v2/api/routes/similarity.py`
- Create: `costimize-v2/api/routes/estimates.py`
- Create: `costimize-v2/api/routes/usage.py`

- [ ] **Step 1: Create similarity routes**

Create file `costimize-v2/api/routes/similarity.py`:

```python
"""Similarity search routes — embed drawings + find matches."""
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from api.deps import get_current_user_id, get_supabase_admin
from api.cost_tracker import check_budget, log_usage
from api.schemas import SimilarityEmbedResponse, SimilaritySearchResponse, SimilarityMatch

router = APIRouter()


@router.post("/similarity/embed", response_model=SimilarityEmbedResponse)
async def embed_drawing(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
):
    if not check_budget():
        raise HTTPException(status_code=429, detail="Service temporarily at capacity.")

    image_bytes = await file.read()
    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Maximum 10MB.")

    try:
        from engines.similarity.preprocessor import preprocess_drawing
        from engines.similarity.embedder import DrawingEmbedder

        processed = preprocess_drawing(image_bytes, file.filename or "drawing.png")
        embedder = DrawingEmbedder()
        embedding = embedder.embed(processed.clean_image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to embed drawing: {str(e)}")

    # Store in Supabase
    sb = get_supabase_admin()
    result = sb.table("drawings").insert({
        "user_id": user_id,
        "file_url": file.filename,
        "embedding": embedding.tolist(),
        "metadata": {"filename": file.filename},
    }).execute()

    drawing_id = result.data[0]["id"] if result.data else "unknown"

    # Upload file to storage
    sb.storage.from_("drawings").upload(
        f"{user_id}/{drawing_id}.pdf",
        image_bytes,
    )

    log_usage(user_id, "similarity_embed", 0.005, {"filename": file.filename})

    return SimilarityEmbedResponse(
        drawing_id=drawing_id,
        message="Drawing embedded successfully",
    )


@router.post("/similarity/search", response_model=SimilaritySearchResponse)
async def search_similar(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
):
    if not check_budget():
        raise HTTPException(status_code=429, detail="Service temporarily at capacity.")

    image_bytes = await file.read()

    try:
        from engines.similarity.preprocessor import preprocess_drawing
        from engines.similarity.embedder import DrawingEmbedder

        processed = preprocess_drawing(image_bytes, file.filename or "drawing.png")
        embedder = DrawingEmbedder()
        query_embedding = embedder.embed(processed.clean_image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process drawing: {str(e)}")

    # Search in Supabase using pgvector
    sb = get_supabase_admin()
    result = sb.rpc("match_drawings", {
        "query_embedding": query_embedding.tolist(),
        "match_threshold": 0.5,
        "match_count": 5,
        "p_user_id": user_id,
    }).execute()

    matches = [
        SimilarityMatch(
            drawing_id=row["id"],
            score=row["similarity"],
            metadata=row.get("metadata", {}),
        )
        for row in (result.data or [])
    ]

    log_usage(user_id, "similarity_search", 0.005, {"matches_found": len(matches)})

    return SimilaritySearchResponse(matches=matches)
```

- [ ] **Step 2: Add pgvector similarity function migration**

Create file `supabase/migrations/005_similarity_function.sql`:

```sql
-- Vector similarity search function for pgvector
create or replace function match_drawings(
    query_embedding vector(256),
    match_threshold float,
    match_count int,
    p_user_id uuid
)
returns table (
    id uuid,
    file_url text,
    metadata jsonb,
    similarity float
)
language sql stable
as $$
    select
        d.id,
        d.file_url,
        d.metadata,
        1 - (d.embedding <=> query_embedding) as similarity
    from drawings d
    where d.user_id = p_user_id
        and 1 - (d.embedding <=> query_embedding) > match_threshold
    order by d.embedding <=> query_embedding
    limit match_count;
$$;
```

- [ ] **Step 3: Create estimates history route**

Create file `costimize-v2/api/routes/estimates.py`:

```python
"""GET /api/estimates — user's estimate history."""
from fastapi import APIRouter, Depends

from api.deps import get_current_user_id, get_supabase_admin
from api.schemas import EstimateHistoryItem

router = APIRouter()


@router.get("/estimates", response_model=list[EstimateHistoryItem])
async def list_estimates(
    user_id: str = Depends(get_current_user_id),
):
    sb = get_supabase_admin()
    result = sb.table("estimates") \
        .select("id, part_type, total_cost, confidence_tier, currency, created_at") \
        .eq("user_id", user_id) \
        .order("created_at", desc=True) \
        .limit(50) \
        .execute()

    return [
        EstimateHistoryItem(
            id=str(row["id"]),
            part_type=row["part_type"],
            total_cost=float(row["total_cost"]),
            confidence_tier=row.get("confidence_tier"),
            currency=row["currency"],
            created_at=row["created_at"],
        )
        for row in (result.data or [])
    ]


@router.get("/estimates/{estimate_id}")
async def get_estimate(
    estimate_id: str,
    user_id: str = Depends(get_current_user_id),
):
    sb = get_supabase_admin()
    result = sb.table("estimates") \
        .select("*") \
        .eq("id", estimate_id) \
        .eq("user_id", user_id) \
        .single() \
        .execute()

    if not result.data:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Estimate not found")

    return result.data
```

- [ ] **Step 4: Create usage route**

Create file `costimize-v2/api/routes/usage.py`:

```python
"""GET /api/usage — user stats. GET /api/admin/usage — daily cost tracking."""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException

from api.deps import get_current_user_id, get_supabase_admin
from api.schemas import UsageResponse, AdminUsageResponse

router = APIRouter()

ADMIN_SECRET = "costimize-admin-2026"  # Replace with env var in production


@router.get("/usage", response_model=UsageResponse)
async def get_user_usage(
    user_id: str = Depends(get_current_user_id),
):
    sb = get_supabase_admin()

    # Get profile for join date
    profile = sb.table("profiles") \
        .select("created_at") \
        .eq("id", user_id) \
        .single() \
        .execute()

    # Count estimates
    estimates = sb.table("estimates") \
        .select("id", count="exact") \
        .eq("user_id", user_id) \
        .execute()

    # Count similarity searches
    similarity = sb.table("usage_log") \
        .select("id", count="exact") \
        .eq("user_id", user_id) \
        .in_("action", ["similarity_embed", "similarity_search"]) \
        .execute()

    return UsageResponse(
        total_estimates=estimates.count or 0,
        total_similarity=similarity.count or 0,
        joined=profile.data["created_at"] if profile.data else "",
    )


@router.get("/admin/usage", response_model=AdminUsageResponse)
async def get_admin_usage(secret: str = ""):
    if secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Forbidden")

    sb = get_supabase_admin()
    today = date.today().isoformat()

    # Today's API cost
    cost_result = sb.table("usage_log") \
        .select("api_cost_usd") \
        .gte("created_at", f"{today}T00:00:00Z") \
        .execute()
    today_cost = sum(r["api_cost_usd"] for r in (cost_result.data or []))

    # Today's estimates
    est_result = sb.table("usage_log") \
        .select("id", count="exact") \
        .eq("action", "estimate") \
        .gte("created_at", f"{today}T00:00:00Z") \
        .execute()

    # Today's signups
    signup_result = sb.table("profiles") \
        .select("id", count="exact") \
        .gte("created_at", f"{today}T00:00:00Z") \
        .execute()

    return AdminUsageResponse(
        today_cost_usd=today_cost,
        estimates_today=est_result.count or 0,
        signups_today=signup_result.count or 0,
    )
```

- [ ] **Step 5: Run all tests**

Run: `cd costimize-v2 && python -m pytest tests/ -v`
Expected: All existing 161 tests + new API tests pass

- [ ] **Step 6: Commit**

```bash
git add costimize-v2/api/routes/ supabase/migrations/005_similarity_function.sql
git commit -m "feat: add similarity, history, and usage API routes"
```

---

## Task 5: FastAPI Dockerfile + Local Run

**Files:**
- Create: `costimize-v2/Dockerfile`
- Modify: `costimize-v2/.env` (add Supabase vars)

- [ ] **Step 1: Create Dockerfile**

Create file `costimize-v2/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/requirements.txt api/requirements.txt
RUN pip install --no-cache-dir -r api/requirements.txt

COPY . .

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- [ ] **Step 2: Add Supabase env vars to .env**

Add to `costimize-v2/.env`:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

- [ ] **Step 3: Test local run**

Run: `cd costimize-v2 && PYTHONPATH=. uvicorn api.main:app --reload --port 8000`
Expected: Server starts at http://localhost:8000
Test: `curl http://localhost:8000/api/health` → `{"status":"ok"}`

- [ ] **Step 4: Commit**

```bash
git add costimize-v2/Dockerfile
git commit -m "feat: add Dockerfile for Railway deployment"
```

---

## Task 6: Next.js Frontend — Project Setup

**Files:**
- Create: `frontend/` (via create-next-app)
- Create: `frontend/.env.local`
- Create: `frontend/src/lib/supabase.ts`
- Create: `frontend/src/lib/api.ts`

- [ ] **Step 1: Create Next.js project**

Run:
```bash
cd C:/Users/chand/costimize-mvp
npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --no-import-alias
```

- [ ] **Step 2: Install Supabase client**

Run:
```bash
cd frontend
npm install @supabase/supabase-js @supabase/ssr
```

- [ ] **Step 3: Create environment file**

Create file `frontend/.env.local`:

```
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

- [ ] **Step 4: Create Supabase client**

Create file `frontend/src/lib/supabase.ts`:

```typescript
import { createBrowserClient } from "@supabase/ssr";

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  );
}
```

- [ ] **Step 5: Create typed API client**

Create file `frontend/src/lib/api.ts`:

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getAuthHeaders(): Promise<HeadersInit> {
  const { createClient } = await import("./supabase");
  const supabase = createClient();
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (!session?.access_token) {
    throw new Error("Not authenticated");
  }

  return {
    Authorization: `Bearer ${session.access_token}`,
  };
}

export async function extractDrawing(file: File) {
  const headers = await getAuthHeaders();
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_URL}/api/extract`, {
    method: "POST",
    headers,
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Extraction failed");
  }

  return res.json();
}

export async function createEstimate(extractedData: Record<string, unknown>, quantity = 1) {
  const headers = await getAuthHeaders();

  const res = await fetch(`${API_URL}/api/estimate`, {
    method: "POST",
    headers: { ...headers, "Content-Type": "application/json" },
    body: JSON.stringify({ extracted_data: extractedData, quantity }),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Estimation failed");
  }

  return res.json();
}

export async function getEstimates() {
  const headers = await getAuthHeaders();

  const res = await fetch(`${API_URL}/api/estimates`, { headers });

  if (!res.ok) throw new Error("Failed to fetch estimates");
  return res.json();
}

export async function getEstimate(id: string) {
  const headers = await getAuthHeaders();

  const res = await fetch(`${API_URL}/api/estimates/${id}`, { headers });

  if (!res.ok) throw new Error("Failed to fetch estimate");
  return res.json();
}

export async function getUsage() {
  const headers = await getAuthHeaders();

  const res = await fetch(`${API_URL}/api/usage`, { headers });

  if (!res.ok) throw new Error("Failed to fetch usage");
  return res.json();
}

export async function searchSimilar(file: File) {
  const headers = await getAuthHeaders();
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_URL}/api/similarity/search`, {
    method: "POST",
    headers,
    body: formData,
  });

  if (!res.ok) throw new Error("Similarity search failed");
  return res.json();
}

export async function embedDrawing(file: File) {
  const headers = await getAuthHeaders();
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_URL}/api/similarity/embed`, {
    method: "POST",
    headers,
    body: formData,
  });

  if (!res.ok) throw new Error("Embedding failed");
  return res.json();
}
```

- [ ] **Step 6: Create auth middleware**

Create file `frontend/src/middleware.ts`:

```typescript
import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";

export async function middleware(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) =>
            request.cookies.set(name, value),
          );
          supabaseResponse = NextResponse.next({ request });
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options),
          );
        },
      },
    },
  );

  const {
    data: { user },
  } = await supabase.auth.getUser();

  const protectedPaths = ["/dashboard", "/estimate", "/similar"];
  const isProtected = protectedPaths.some((p) =>
    request.nextUrl.pathname.startsWith(p),
  );

  if (isProtected && !user) {
    const url = request.nextUrl.clone();
    url.pathname = "/login";
    return NextResponse.redirect(url);
  }

  if (request.nextUrl.pathname === "/login" && user) {
    const url = request.nextUrl.clone();
    url.pathname = "/dashboard";
    return NextResponse.redirect(url);
  }

  return supabaseResponse;
}

export const config = {
  matcher: ["/dashboard/:path*", "/estimate/:path*", "/similar/:path*", "/login"],
};
```

- [ ] **Step 7: Commit**

```bash
git add frontend/
git commit -m "feat: add Next.js frontend with Supabase auth and API client"
```

---

## Task 7: Next.js Pages — Login + Dashboard

**Files:**
- Create: `frontend/src/app/login/page.tsx`
- Modify: `frontend/src/app/page.tsx` (landing page)
- Create: `frontend/src/app/dashboard/page.tsx`

UI for these pages will be generated via Stitch. The code below provides the functional structure — Stitch will style it.

- [ ] **Step 1: Create login page**

Create file `frontend/src/app/login/page.tsx`:

```tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase";

export default function LoginPage() {
  const router = useRouter();
  const [isSignUp, setIsSignUp] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [company, setCompany] = useState("");
  const [country, setCountry] = useState("India");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const countries = [
    "India", "China", "Vietnam", "Thailand", "Taiwan",
    "South Korea", "Japan", "Germany", "USA", "UK", "Other",
  ];

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    const supabase = createClient();

    if (isSignUp) {
      const { error: signUpError } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: {
            full_name: fullName,
            company,
            sourcing_country: country,
          },
        },
      });
      if (signUpError) {
        setError(signUpError.message);
        setLoading(false);
        return;
      }
    } else {
      const { error: signInError } = await supabase.auth.signInWithPassword({
        email,
        password,
      });
      if (signInError) {
        setError(signInError.message);
        setLoading(false);
        return;
      }
    }

    router.push("/dashboard");
  }

  return (
    <div>
      <h1>{isSignUp ? "Create Account" : "Log In"}</h1>
      <form onSubmit={handleSubmit}>
        {isSignUp && (
          <>
            <input
              type="text"
              placeholder="Full Name"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              required
            />
            <input
              type="text"
              placeholder="Company Name"
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              required
            />
            <select value={country} onChange={(e) => setCountry(e.target.value)}>
              {countries.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </>
        )}
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={6}
        />
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit" disabled={loading}>
          {loading ? "Please wait..." : isSignUp ? "Sign Up" : "Log In"}
        </button>
      </form>
      <button onClick={() => setIsSignUp(!isSignUp)}>
        {isSignUp ? "Already have an account? Log in" : "Need an account? Sign up"}
      </button>
    </div>
  );
}
```

- [ ] **Step 2: Create dashboard page**

Create file `frontend/src/app/dashboard/page.tsx`:

```tsx
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getEstimates, getUsage } from "@/lib/api";

interface Estimate {
  id: string;
  part_type: string;
  total_cost: number;
  confidence_tier: string | null;
  currency: string;
  created_at: string;
}

interface Usage {
  total_estimates: number;
  total_similarity: number;
  joined: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const [estimates, setEstimates] = useState<Estimate[]>([]);
  const [usage, setUsage] = useState<Usage | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [est, usg] = await Promise.all([getEstimates(), getUsage()]);
        setEstimates(est);
        setUsage(usg);
      } catch {
        // Auth might have expired
      }
      setLoading(false);
    }
    load();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1>Dashboard</h1>

      {usage && (
        <div>
          <p>{usage.total_estimates} estimates completed</p>
          <p>{usage.total_similarity} similarity searches</p>
        </div>
      )}

      <div>
        <button onClick={() => router.push("/estimate/new")}>
          New Estimate
        </button>
        <button onClick={() => router.push("/similar")}>
          Similar Parts
        </button>
      </div>

      <h2>Recent Estimates</h2>
      {estimates.length === 0 ? (
        <p>No estimates yet. Upload your first drawing.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Type</th>
              <th>Total Cost</th>
              <th>Confidence</th>
            </tr>
          </thead>
          <tbody>
            {estimates.map((est) => (
              <tr
                key={est.id}
                onClick={() => router.push(`/estimate/${est.id}`)}
                style={{ cursor: "pointer" }}
              >
                <td>{new Date(est.created_at).toLocaleDateString()}</td>
                <td>{est.part_type}</td>
                <td>{est.currency} {est.total_cost.toLocaleString()}</td>
                <td>{est.confidence_tier || "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
```

- [ ] **Step 3: Update landing page**

Replace `frontend/src/app/page.tsx`:

```tsx
import Link from "next/link";

export default function LandingPage() {
  return (
    <div>
      <section>
        <h1>Know the real cost before you negotiate.</h1>
        <p>
          AI-powered should-cost breakdowns for mechanical parts.
          Line by line. Physics-based. Accurate to +/-10%.
        </p>
        <Link href="/login">Try it free</Link>
      </section>

      <section>
        <h2>How it works</h2>
        <ol>
          <li>Upload your engineering drawing (PDF or image)</li>
          <li>AI extracts dimensions, tolerances, and processes</li>
          <li>Get a line-by-line should-cost breakdown in seconds</li>
        </ol>
      </section>

      <section>
        <h2>Built for procurement teams</h2>
        <ul>
          <li>Defense, aerospace, and automotive manufacturers</li>
          <li>Anyone buying custom machined parts</li>
          <li>Negotiating with suppliers on proprietary parts</li>
        </ul>
      </section>

      <footer>
        <Link href="/login">Get started free</Link>
      </footer>
    </div>
  );
}
```

- [ ] **Step 4: Run dev server and verify**

Run: `cd frontend && npm run dev`
Expected: http://localhost:3000 shows landing page, /login shows form, /dashboard redirects to /login

- [ ] **Step 5: Commit**

```bash
git add frontend/src/
git commit -m "feat: add login, dashboard, and landing pages"
```

---

## Task 8: Next.js Pages — Estimate Flow + View

**Files:**
- Create: `frontend/src/app/estimate/new/page.tsx`
- Create: `frontend/src/app/estimate/[id]/page.tsx`

- [ ] **Step 1: Create new estimate page**

Create file `frontend/src/app/estimate/new/page.tsx`:

```tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { extractDrawing, createEstimate } from "@/lib/api";

type Step = "upload" | "extracting" | "review" | "calculating" | "result";

interface ProcessLine {
  process_id: string;
  process_name: string;
  time_min: number;
  machine_cost: number;
  setup_cost_per_unit: number;
  tooling_cost: number;
  labour_cost: number;
  power_cost: number;
}

interface EstimateResult {
  material_name: string;
  material_cost: number;
  process_lines: ProcessLine[];
  total_machining_cost: number;
  total_setup_cost: number;
  total_tooling_cost: number;
  total_labour_cost: number;
  total_power_cost: number;
  subtotal: number;
  overhead: number;
  profit: number;
  unit_cost: number;
  order_cost: number;
  quantity: number;
  confidence_tier: string | null;
  currency: string;
}

export default function NewEstimatePage() {
  const router = useRouter();
  const [step, setStep] = useState<Step>("upload");
  const [file, setFile] = useState<File | null>(null);
  const [extractedData, setExtractedData] = useState<Record<string, unknown> | null>(null);
  const [result, setResult] = useState<EstimateResult | null>(null);
  const [quantity, setQuantity] = useState(1);
  const [error, setError] = useState("");
  const [expanded, setExpanded] = useState(false);

  async function handleUpload() {
    if (!file) return;
    setError("");
    setStep("extracting");

    try {
      const data = await extractDrawing(file);
      setExtractedData(data);
      setStep("review");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Extraction failed");
      setStep("upload");
    }
  }

  async function handleCalculate() {
    if (!extractedData) return;
    setError("");
    setStep("calculating");

    try {
      const est = await createEstimate(extractedData, quantity);
      setResult(est);
      setStep("result");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Calculation failed");
      setStep("review");
    }
  }

  if (step === "upload") {
    return (
      <div>
        <h1>New Estimate</h1>
        <p>Upload an engineering drawing to get a should-cost breakdown.</p>
        <input
          type="file"
          accept=".pdf,.png,.jpg,.jpeg"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
        <div>
          <label>Quantity: </label>
          <input
            type="number"
            min={1}
            value={quantity}
            onChange={(e) => setQuantity(parseInt(e.target.value) || 1)}
          />
        </div>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button onClick={handleUpload} disabled={!file}>
          Analyze Drawing
        </button>
      </div>
    );
  }

  if (step === "extracting") {
    return (
      <div>
        <h1>Analyzing Drawing...</h1>
        <p>AI is extracting dimensions, tolerances, and processes.</p>
      </div>
    );
  }

  if (step === "review" && extractedData) {
    return (
      <div>
        <h1>Review Extracted Data</h1>
        <table>
          <tbody>
            {Object.entries(extractedData.dimensions as Record<string, unknown> || {}).map(
              ([key, val]) =>
                val != null && (
                  <tr key={key}>
                    <td>{key.replace(/_/g, " ")}</td>
                    <td>{String(val)}</td>
                  </tr>
                ),
            )}
          </tbody>
        </table>
        <p>Material: {String(extractedData.material || "Not detected")}</p>
        <p>Processes: {(extractedData.suggested_processes as string[] || []).join(", ")}</p>
        <p>AI Confidence: {String(extractedData.confidence || "—")}</p>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button onClick={handleCalculate}>Calculate Cost</button>
        <button onClick={() => setStep("upload")}>Re-upload</button>
      </div>
    );
  }

  if (step === "calculating") {
    return (
      <div>
        <h1>Calculating Cost...</h1>
        <p>Physics engine computing line-by-line breakdown.</p>
      </div>
    );
  }

  if (step === "result" && result) {
    return (
      <div>
        <h1>Should-Cost Estimate</h1>
        {result.confidence_tier && (
          <span>Confidence: {result.confidence_tier}</span>
        )}

        <table>
          <thead>
            <tr>
              <th>Cost Component</th>
              <th>Amount ({result.currency})</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Material ({result.material_name})</td>
              <td>{result.material_cost.toLocaleString("en-IN", { maximumFractionDigits: 0 })}</td>
            </tr>
            <tr>
              <td>Machining</td>
              <td>{result.total_machining_cost.toLocaleString("en-IN", { maximumFractionDigits: 0 })}</td>
            </tr>
            <tr>
              <td>Setup & Tooling</td>
              <td>{(result.total_setup_cost + result.total_tooling_cost).toLocaleString("en-IN", { maximumFractionDigits: 0 })}</td>
            </tr>
            <tr>
              <td>Labour</td>
              <td>{result.total_labour_cost.toLocaleString("en-IN", { maximumFractionDigits: 0 })}</td>
            </tr>
            <tr>
              <td>Power</td>
              <td>{result.total_power_cost.toLocaleString("en-IN", { maximumFractionDigits: 0 })}</td>
            </tr>
            <tr>
              <td>Overhead ({Math.round((result.overhead / result.subtotal) * 100)}%)</td>
              <td>{result.overhead.toLocaleString("en-IN", { maximumFractionDigits: 0 })}</td>
            </tr>
            <tr>
              <td>Profit ({Math.round((result.profit / result.subtotal) * 100)}%)</td>
              <td>{result.profit.toLocaleString("en-IN", { maximumFractionDigits: 0 })}</td>
            </tr>
            <tr style={{ fontWeight: "bold" }}>
              <td>TOTAL (per unit)</td>
              <td>{result.currency} {result.unit_cost.toLocaleString("en-IN", { maximumFractionDigits: 0 })}</td>
            </tr>
            {result.quantity > 1 && (
              <tr style={{ fontWeight: "bold" }}>
                <td>ORDER TOTAL ({result.quantity} units)</td>
                <td>{result.currency} {result.order_cost.toLocaleString("en-IN", { maximumFractionDigits: 0 })}</td>
              </tr>
            )}
          </tbody>
        </table>

        <button onClick={() => setExpanded(!expanded)}>
          {expanded ? "Hide" : "Show"} Full Breakdown
        </button>

        {expanded && (
          <table>
            <thead>
              <tr>
                <th>Process</th>
                <th>Time (min)</th>
                <th>Machine</th>
                <th>Setup</th>
                <th>Tooling</th>
                <th>Labour</th>
                <th>Power</th>
              </tr>
            </thead>
            <tbody>
              {result.process_lines.map((pl) => (
                <tr key={pl.process_id}>
                  <td>{pl.process_name}</td>
                  <td>{pl.time_min.toFixed(1)}</td>
                  <td>{pl.machine_cost.toFixed(0)}</td>
                  <td>{pl.setup_cost_per_unit.toFixed(0)}</td>
                  <td>{pl.tooling_cost.toFixed(0)}</td>
                  <td>{pl.labour_cost.toFixed(0)}</td>
                  <td>{pl.power_cost.toFixed(0)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        <div>
          <button onClick={() => router.push("/dashboard")}>Back to Dashboard</button>
          <button onClick={() => setStep("upload")}>New Estimate</button>
        </div>
      </div>
    );
  }

  return null;
}
```

- [ ] **Step 2: Create view estimate page**

Create file `frontend/src/app/estimate/[id]/page.tsx`:

```tsx
"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { getEstimate } from "@/lib/api";

export default function ViewEstimatePage() {
  const { id } = useParams();
  const router = useRouter();
  const [data, setData] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const est = await getEstimate(id as string);
        setData(est);
      } catch {
        router.push("/dashboard");
      }
      setLoading(false);
    }
    load();
  }, [id, router]);

  if (loading) return <div>Loading...</div>;
  if (!data) return <div>Estimate not found.</div>;

  const breakdown = data.cost_breakdown as Record<string, unknown>;

  return (
    <div>
      <h1>Estimate Details</h1>
      <p>Created: {new Date(data.created_at as string).toLocaleString()}</p>
      <p>Total: {data.currency as string} {Number(data.total_cost).toLocaleString("en-IN")}</p>
      <p>Confidence: {(data.confidence_tier as string) || "—"}</p>

      <h2>Breakdown</h2>
      <pre>{JSON.stringify(breakdown, null, 2)}</pre>

      <button onClick={() => router.push("/dashboard")}>Back to Dashboard</button>
    </div>
  );
}
```

- [ ] **Step 3: Run dev server and test flow**

Run: `cd frontend && npm run dev`
Navigate: /estimate/new → upload a file → verify extraction → calculate → see results

- [ ] **Step 4: Commit**

```bash
git add frontend/src/app/estimate/
git commit -m "feat: add estimate creation and viewing pages"
```

---

## Task 9: Next.js — Similarity Search Page

**Files:**
- Create: `frontend/src/app/similar/page.tsx`

- [ ] **Step 1: Create similarity page**

Create file `frontend/src/app/similar/page.tsx`:

```tsx
"use client";

import { useState } from "react";
import { embedDrawing, searchSimilar } from "@/lib/api";

interface Match {
  drawing_id: string;
  score: number;
  metadata: Record<string, unknown>;
}

export default function SimilarPartsPage() {
  const [files, setFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState<"upload" | "results">("upload");
  const [matches, setMatches] = useState<Match[]>([]);
  const [error, setError] = useState("");

  async function handleSearch() {
    if (files.length < 2) {
      setError("Upload at least 2 drawings to compare.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      // Embed all drawings first
      for (const file of files) {
        await embedDrawing(file);
      }

      // Search using the first drawing as query
      const result = await searchSimilar(files[0]);
      setMatches(result.matches);
      setStep("results");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Search failed");
    }

    setLoading(false);
  }

  if (step === "upload") {
    return (
      <div>
        <h1>Similar Parts Search</h1>
        <p>Upload 2 or more engineering drawings to find similar parts and compare costs.</p>

        <input
          type="file"
          accept=".pdf,.png,.jpg,.jpeg"
          multiple
          onChange={(e) => setFiles(Array.from(e.target.files || []))}
        />

        {files.length > 0 && (
          <p>{files.length} file(s) selected: {files.map((f) => f.name).join(", ")}</p>
        )}

        {error && <p style={{ color: "red" }}>{error}</p>}

        <button onClick={handleSearch} disabled={loading || files.length < 2}>
          {loading ? "Processing..." : "Find Similar Parts"}
        </button>
      </div>
    );
  }

  return (
    <div>
      <h1>Similarity Results</h1>

      {matches.length === 0 ? (
        <p>No similar parts found. Upload more drawings to build your library.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Drawing</th>
              <th>Similarity Score</th>
              <th>Details</th>
            </tr>
          </thead>
          <tbody>
            {matches.map((m) => (
              <tr key={m.drawing_id}>
                <td>{(m.metadata.filename as string) || m.drawing_id}</td>
                <td>{(m.score * 100).toFixed(1)}%</td>
                <td>{JSON.stringify(m.metadata)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <button onClick={() => { setStep("upload"); setMatches([]); setFiles([]); }}>
        New Search
      </button>
    </div>
  );
}
```

- [ ] **Step 2: Verify similarity flow**

Run: `cd frontend && npm run dev`
Navigate: /similar → upload 2+ files → verify embed + search works

- [ ] **Step 3: Commit**

```bash
git add frontend/src/app/similar/
git commit -m "feat: add similarity search page"
```

---

## Task 10: Stitch UI Design

**Files:**
- Modify: All frontend pages (styling via Stitch)

- [ ] **Step 1: Use Stitch to create design system**

Use the Stitch MCP tool to create a design system for the app:
- Colors: professional blue/white, one accent
- Typography: Inter or Geist
- Components: buttons, cards, tables, forms, badges
- Responsive: desktop-first

- [ ] **Step 2: Apply Stitch design to all pages**

Use Stitch to generate styled versions of:
- Landing page (`/`)
- Login/signup (`/login`)
- Dashboard (`/dashboard`)
- New estimate (`/estimate/new`)
- View estimate (`/estimate/[id]`)
- Similar parts (`/similar`)

- [ ] **Step 3: Verify all pages look professional**

Run: `cd frontend && npm run dev`
Check every page visually. Should look like a real product, not a hackathon project.

- [ ] **Step 4: Commit**

```bash
git add frontend/
git commit -m "feat: apply Stitch design system to all pages"
```

---

## Task 11: End-to-End Testing

**Files:**
- Modify: `costimize-v2/tests/test_api.py` (add more tests)

- [ ] **Step 1: Run all Python engine tests**

Run: `cd costimize-v2 && python -m pytest tests/ -v`
Expected: All 161 existing tests + new API tests pass

- [ ] **Step 2: Run FastAPI locally and test full flow**

Terminal 1: `cd costimize-v2 && PYTHONPATH=. uvicorn api.main:app --reload --port 8000`
Terminal 2: `cd frontend && npm run dev`

Manual test checklist:
- [ ] Landing page loads at http://localhost:3000
- [ ] Click "Try it free" → goes to /login
- [ ] Sign up with email/password/name/company/country
- [ ] Redirected to /dashboard
- [ ] Click "New Estimate"
- [ ] Upload a drawing (PDF or image)
- [ ] AI extracts dimensions (verify values look reasonable)
- [ ] Click "Calculate Cost"
- [ ] Summary table shows with correct INR formatting
- [ ] Expand full breakdown → see per-process details
- [ ] Go back to dashboard → see estimate in history
- [ ] Click estimate → view saved details
- [ ] Go to Similar Parts → upload 2 drawings → see results
- [ ] Log out → verify /dashboard redirects to /login

- [ ] **Step 3: Check Supabase dashboard**

Verify in Supabase:
- [ ] Profile created for new user
- [ ] Estimate saved in estimates table
- [ ] Usage logged in usage_log table
- [ ] Drawings saved in drawings table

- [ ] **Step 4: Commit**

```bash
git add costimize-v2/tests/
git commit -m "test: verify end-to-end flow with manual + automated tests"
```

---

## Task 12: Deploy to Vercel + Railway

**Files:**
- Create: `frontend/vercel.json`
- Modify: `costimize-v2/.env` (production values)

- [ ] **Step 1: Deploy FastAPI to Railway**

1. Go to railway.com → sign up → New Project → Deploy from GitHub repo
2. Set root directory: `costimize-v2`
3. Railway auto-detects Dockerfile
4. Add environment variables:
   - `OPENAI_API_KEY`
   - `GEMINI_API_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
5. Deploy → note the public URL (e.g., `https://costimize-api-production.up.railway.app`)

- [ ] **Step 2: Deploy frontend to Vercel**

1. Go to vercel.com → sign up → Import Git Repository
2. Set root directory: `frontend`
3. Add environment variables:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `NEXT_PUBLIC_API_URL` = Railway URL from step 1
4. Deploy → note the public URL (e.g., `https://costimize.vercel.app`)

- [ ] **Step 3: Update CORS in FastAPI**

Add the Vercel production URL to CORS origins in `costimize-v2/api/main.py`:

```python
allow_origins=[
    "http://localhost:3000",
    "https://*.vercel.app",
    "https://costimize.vercel.app",  # add exact production URL
],
```

- [ ] **Step 4: Redeploy and verify production**

Run through the same manual test checklist from Task 11 on the production URLs.

- [ ] **Step 5: Commit**

```bash
git add frontend/vercel.json costimize-v2/api/main.py
git commit -m "feat: deploy to Vercel + Railway, configure production CORS"
```

---

## Task 13: Pre-Event Polish

- [ ] **Step 1: Prepare demo drawings**

Have 2-3 engineering drawings ready:
- One simple turning part (shaft/pin)
- One complex multi-process part (housing with holes + threads)
- Test both on production to cache results

- [ ] **Step 2: Check mobile responsiveness**

Open production URL on phone. Key pages should be usable (dashboard, results table).

- [ ] **Step 3: Verify $20/day cost cap**

Hit `/api/admin/usage?secret=costimize-admin-2026` on production. Verify cost tracking works.

- [ ] **Step 4: Prepare fallback**

If live demo fails at event:
- Screenshot 2-3 completed estimates
- Record a 30-second screen recording of the full flow
- Have them on your phone

- [ ] **Step 5: Final commit**

```bash
git add -A
git commit -m "chore: pre-event polish and demo preparation"
```
