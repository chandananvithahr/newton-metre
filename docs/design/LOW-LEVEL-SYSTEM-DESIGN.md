# Costimize — Low-Level System Design

> Detailed component design, class structures, algorithms, and data contracts.
> Last updated: 2026-03-30

---

## 1. Database Schema

### 1.1 Entity-Relationship Diagram

```
auth.users (Supabase built-in)
    |
    | 1:1
    v
profiles
    |
    | 1:N
    +-------+----------+----------+
    |       |          |          |
    v       v          v          v
estimates  drawings  usage_log  validated_estimates
```

### 1.2 Table Definitions

#### `profiles`
```sql
CREATE TABLE public.profiles (
  id          UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name   TEXT,
  company     TEXT,
  created_at  TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "users read own profile"
  ON profiles FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "users update own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id);
```

#### `estimates`
```sql
CREATE TABLE public.estimates (
  id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id             UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  part_type           TEXT NOT NULL,  -- "mechanical" | "sheet_metal" | "pcb" | "cable" | "assembly"
  material_name       TEXT,
  dimensions          JSONB,
  suggested_processes TEXT[],
  process_breakdown   JSONB NOT NULL,  -- array of process cost lines
  total_cost          FLOAT NOT NULL,
  confidence_tier     TEXT,            -- "high" | "medium" | "low" | "insufficient"
  quantity            INT NOT NULL DEFAULT 1,
  currency            TEXT NOT NULL DEFAULT 'INR',
  created_at          TIMESTAMPTZ DEFAULT now(),
  updated_at          TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_estimates_user_id ON estimates(user_id);
CREATE INDEX idx_estimates_created_at ON estimates(created_at DESC);

ALTER TABLE estimates ENABLE ROW LEVEL SECURITY;

CREATE POLICY "users read own estimates"
  ON estimates FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "service role inserts estimates"
  ON estimates FOR INSERT
  WITH CHECK (true);  -- backend uses service role key
```

#### `drawings`
```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE public.drawings (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  file_url    TEXT,
  embedding   VECTOR(256),
  metadata    JSONB,  -- { filename, material, processes, dimensions }
  created_at  TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_drawings_user_id ON drawings(user_id);
CREATE INDEX idx_drawings_embedding ON drawings
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

ALTER TABLE drawings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "users read own drawings"
  ON drawings FOR SELECT
  USING (auth.uid() = user_id);
```

#### `usage_log`
```sql
CREATE TABLE public.usage_log (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL REFERENCES profiles(id),
  action      TEXT NOT NULL,     -- "extract" | "estimate" | "similarity_embed" | etc.
  cost_usd    FLOAT NOT NULL,
  metadata    JSONB,             -- { filename, part_type, etc. }
  created_at  TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_usage_log_user_date ON usage_log(user_id, created_at);
CREATE INDEX idx_usage_log_date ON usage_log(created_at);

ALTER TABLE usage_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "users read own logs"
  ON usage_log FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "service role inserts logs"
  ON usage_log FOR INSERT
  WITH CHECK (true);
```

#### `validated_estimates` (ML training data)
```sql
CREATE TABLE public.validated_estimates (
  id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id             UUID NOT NULL REFERENCES profiles(id),
  physics_cost        FLOAT NOT NULL,
  ai_cost             FLOAT NOT NULL,
  delta_pct           FLOAT NOT NULL,
  final_cost          FLOAT,          -- user-confirmed actual cost
  metadata            JSONB,          -- { material, processes, dimensions }
  created_at          TIMESTAMPTZ DEFAULT now()
);
```

---

## 2. Backend Module Design

### 2.1 API Layer (`api/`)

#### `main.py` — Application Factory

```python
# Responsibilities:
# 1. Create FastAPI app with metadata
# 2. Configure CORS from ALLOWED_ORIGINS env var
# 3. Mount all route modules
# 4. Global exception handler (500 -> generic message)

app = FastAPI(
    title="Costimize API",
    docs_url="/docs" if ENVIRONMENT != "production" else None,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(extract_router, prefix="/api")
app.include_router(estimate_router, prefix="/api")
app.include_router(assembly_router, prefix="/api")
app.include_router(estimates_router, prefix="/api")
app.include_router(similarity_router, prefix="/api")
app.include_router(rfq_router, prefix="/api")
app.include_router(material_router, prefix="/api")
app.include_router(usage_router, prefix="/api")
```

#### `deps.py` — Dependency Injection

```python
# Two Supabase clients:
# 1. anon_client  -> for RLS-scoped queries (user's JWT)
# 2. admin_client -> for service-role operations (logging, admin)

def get_supabase_anon() -> Client:
    """Client with anon key for RLS-protected queries."""
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def get_supabase_admin() -> Client:
    """Client with service role key for admin operations."""
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

async def get_current_user(
    authorization: str = Header(...)
) -> dict:
    """
    Extract and validate JWT from Authorization header.
    Returns: { "id": uuid, "email": str }
    Raises: HTTPException(401) if invalid
    """
    token = authorization.replace("Bearer ", "")
    user = supabase_admin.auth.get_user(token)
    if not user:
        raise HTTPException(401, "Invalid token")
    return {"id": user.user.id, "email": user.user.email}
```

#### `cost_tracker.py` — Budget Enforcement

```python
GLOBAL_DAILY_BUDGET_USD = 2.00
USER_48H_BUDGET_USD = 0.50

COST_PER_ACTION = {
    "extract": 0.002,
    "extract_multi": 0.005,
    "estimate": 0.01,
    "assembly_estimate": 0.01,
    "similarity_embed": 0.005,
    "similarity_search": 0.005,
    "rfq_extract": 0.01,
    "rfq_estimate_item": 0.01,
}

def check_budget() -> bool:
    """Check global daily budget. Returns True if under budget."""
    today_cost = supabase.rpc("sum_today_cost").execute()
    return today_cost.data < GLOBAL_DAILY_BUDGET_USD

def check_user_budget(user_id: str) -> bool:
    """Check per-user 48h budget."""
    cutoff = datetime.utcnow() - timedelta(hours=48)
    user_cost = (
        supabase.table("usage_log")
        .select("cost_usd")
        .eq("user_id", user_id)
        .gte("created_at", cutoff.isoformat())
        .execute()
    )
    total = sum(r["cost_usd"] for r in user_cost.data)
    return total < USER_48H_BUDGET_USD

def log_usage(user_id: str, action: str, metadata: dict = None):
    """Insert usage record with calculated cost."""
    cost = COST_PER_ACTION.get(action, 0.01)
    supabase.table("usage_log").insert({
        "user_id": user_id,
        "action": action,
        "cost_usd": cost,
        "metadata": metadata or {},
    }).execute()
```

#### `schemas.py` — Pydantic Models

```python
# -- Request Models --

class Dimensions(BaseModel):
    outer_diameter_mm: float | None = None
    inner_diameter_mm: float | None = None
    length_mm: float | None = None
    width_mm: float | None = None
    height_mm: float | None = None
    hole_diameter_mm: float | None = None
    hole_count: int | None = None
    thread_count: int | None = None
    thread_length_mm: float | None = None
    groove_count: int | None = None
    surface_area_cm2: float | None = None

class Tolerances(BaseModel):
    has_tight_tolerances: bool = False
    tightest_tolerance_mm: float | None = None

class ExtractedData(BaseModel):
    dimensions: Dimensions
    material: str | None = None
    material_confidence: str = "medium"
    tolerances: Tolerances = Tolerances()
    suggested_processes: list[str] = []
    confidence: str = "medium"
    notes: str = ""

class EstimateRequest(BaseModel):
    extracted_data: ExtractedData
    quantity: int = 1

class AssemblyComponent(BaseModel):
    name: str
    extracted_data: ExtractedData

class AssemblyEstimateRequest(BaseModel):
    components: list[AssemblyComponent]
    joining_method: str  # "mig_welding" | "tig_welding" | etc.
    num_joints: int
    quantity: int = 1

# -- Response Models --

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
```

### 2.2 Cost Engines

#### Mechanical Engine — Core Algorithm

```python
# engines/mechanical/cost_engine.py

@dataclass(frozen=True)
class ProcessCostLine:
    process_id: str
    process_name: str
    time_min: float
    machine_cost: float
    setup_cost_per_unit: float
    tooling_cost: float
    labour_cost: float
    power_cost: float

@dataclass(frozen=True)
class MechanicalCostBreakdown:
    material_name: str
    material_cost: float
    process_lines: tuple[ProcessCostLine, ...]
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

def calculate_mechanical_cost(
    dimensions: dict,
    material: str,
    processes: list[str],
    quantity: int = 1,
    tolerances: dict | None = None,
) -> MechanicalCostBreakdown:
    """
    Main entry point for mechanical cost estimation.

    Algorithm:
    1. Resolve material -> get density, price, machinability index
    2. Calculate part volume from dimensions
    3. Calculate raw weight (with 15% wastage factor)
    4. material_cost = raw_weight_kg * price_per_kg
    5. For each process:
       a. Get cutting parameters (speed, feed, depth)
       b. Calculate cutting time via MRR or geometry
       c. machine_cost = time_min * machine_rate / 60
       d. setup_cost = setup_time / quantity * rate / 60
       e. tooling_cost = tool_wear_cost * time_min
       f. labour_cost = time_min * LABOUR_RATE / 60
       g. power_cost = power_kw * time_min * POWER_RATE / 60
    6. If tight tolerances: apply 30% surcharge
    7. subtotal = material + sum(process costs)
    8. overhead = subtotal * 0.15
    9. profit = (subtotal + overhead) * 0.20
    10. unit_cost = subtotal + overhead + profit
    """
```

#### Process Time Estimation

```python
# engines/mechanical/process_db.py

PROCESS_DB = {
    "turning": {
        "name": "CNC Turning",
        "machine_rate": 800,     # INR/hr
        "setup_time_min": 30,
        "power_kw": 7.5,
        "time_fn": estimate_turning_time,
    },
    "milling_face": {
        "name": "Face Milling",
        "machine_rate": 1000,
        "setup_time_min": 45,
        "power_kw": 11.0,
        "time_fn": estimate_milling_time,
    },
    "drilling": {
        "name": "Drilling",
        "machine_rate": 600,
        "setup_time_min": 15,
        "power_kw": 3.5,
        "time_fn": estimate_drilling_time,
    },
    # ... 18 total processes
}

def estimate_turning_time(dims: dict, machinability: float) -> float:
    """
    CNC turning time based on Material Removal Rate.

    Formula:
      volume_to_remove = pi/4 * (OD^2 - ID^2) * L * excess_factor
      MRR = vc * feed * depth_of_cut  (cm3/min)
      time_min = volume / MRR

    Where:
      vc = base_cutting_speed * machinability_index (m/min)
      feed = 0.2 mm/rev (typical finishing)
      depth_of_cut = 2.0 mm (per pass)
    """

def estimate_drilling_time(dims: dict, machinability: float) -> float:
    """
    Drilling time per hole.

    Formula:
      time_per_hole = hole_depth / (feed_rate * rpm)
      total_time = time_per_hole * hole_count + approach_time * hole_count

    Where:
      rpm = (vc * 1000) / (pi * hole_diameter)
      feed_rate = 0.15 mm/rev
    """
```

#### Cutting Data — Physics Constants

```python
# engines/mechanical/cutting_data.py

# Sandvik kc1 values (N/mm2) — specific cutting force
# Source: Sandvik Coromant General Turning Catalogue
KC1_VALUES = {
    "EN8 Steel":        1800,
    "Mild Steel":       1500,
    "Stainless Steel":  2000,
    "Aluminum 6061":     700,
    "Aluminum 7075":     800,
    "Cast Iron":        1100,
    "Brass":             750,
    "Copper":            850,
    "Titanium Grade 5": 1400,
}

# Taylor tool life equation: V * T^n = C
# V = cutting speed (m/min), T = tool life (min)
TAYLOR_CONSTANTS = {
    "EN8 Steel":        {"n": 0.25, "C": 250},
    "Mild Steel":       {"n": 0.25, "C": 300},
    "Stainless Steel":  {"n": 0.20, "C": 180},
    "Aluminum 6061":    {"n": 0.40, "C": 600},
    "Titanium Grade 5": {"n": 0.15, "C": 100},
    # ...
}

def calculate_power(
    vc: float,      # cutting speed, m/min
    ap: float,      # depth of cut, mm
    fn: float,      # feed per rev, mm/rev
    kc1: float,     # specific cutting force, N/mm2
) -> float:
    """
    Cutting power (kW).
    Formula: Pc = (vc * ap * fn * kc) / (60 * 1000)
    Where kc = kc1 * (fn)^(-0.14)  (Sandvik correction for feed)
    """
    kc = kc1 * (fn ** -0.14)
    return (vc * ap * fn * kc) / (60 * 1000)

def calculate_tool_life(vc: float, material: str) -> float:
    """
    Tool life in minutes using Taylor equation.
    T = (C / V) ^ (1/n)
    """
    params = TAYLOR_CONSTANTS[material]
    return (params["C"] / vc) ** (1 / params["n"])
```

### 2.3 Validation Pipeline

#### Orchestrator — Parallel Execution

```python
# engines/validation/orchestrator.py

from concurrent.futures import ThreadPoolExecutor, as_completed

class ValidationOrchestrator:
    """
    Runs physics engine and Gemini AI in parallel,
    compares results, assigns confidence tier.
    """

    def validate_estimate(
        self,
        extracted_data: dict,
        quantity: int,
        drawing_bytes: bytes | None = None,
    ) -> ValidatedResult:
        """
        Main entry point.

        Execution flow:
        1. Submit physics engine and Gemini to thread pool
        2. Wait for both results
        3. Compare: delta_pct = |physics - ai| / max(physics, ai) * 100
        4. Route by confidence tier:
           - HIGH (<=3%): return physics, tier="high"
           - MEDIUM (3-7%): return physics, tier="medium"
           - LOW (7-15%): run arbitrator, return reconciled
           - INSUFFICIENT (>15%): return physics with warning
        5. Save to training data
        """
        with ThreadPoolExecutor(max_workers=2) as executor:
            physics_future = executor.submit(
                calculate_mechanical_cost,
                extracted_data["dimensions"],
                extracted_data["material"],
                extracted_data["suggested_processes"],
                quantity,
            )
            ai_future = executor.submit(
                estimate_with_gemini,
                extracted_data,
                drawing_bytes,
            )

            physics_result = physics_future.result(timeout=30)
            ai_result = ai_future.result(timeout=30)

        return self._compare_and_route(physics_result, ai_result)
```

#### Comparator — Confidence Tiers

```python
# engines/validation/comparator.py

from enum import Enum

class ConfidenceTier(str, Enum):
    HIGH = "high"              # delta <= 3%
    MEDIUM = "medium"          # 3% < delta <= 7%
    LOW = "low"                # 7% < delta <= 15%
    INSUFFICIENT = "insufficient"  # delta > 15%

def compare_estimates(
    physics_cost: float,
    ai_cost: float,
) -> tuple[ConfidenceTier, float]:
    """
    Compare two independent estimates and assign confidence.

    Returns: (tier, delta_percentage)
    """
    if physics_cost <= 0 or ai_cost <= 0:
        return ConfidenceTier.INSUFFICIENT, 100.0

    delta_pct = abs(physics_cost - ai_cost) / max(physics_cost, ai_cost) * 100

    if delta_pct <= 3.0:
        return ConfidenceTier.HIGH, delta_pct
    elif delta_pct <= 7.0:
        return ConfidenceTier.MEDIUM, delta_pct
    elif delta_pct <= 15.0:
        return ConfidenceTier.LOW, delta_pct
    else:
        return ConfidenceTier.INSUFFICIENT, delta_pct
```

#### Arbitrator — AI Resolution

```python
# engines/validation/arbitrator.py

def arbitrate_estimate(
    physics_breakdown: MechanicalCostBreakdown,
    ai_estimate: float,
    extracted_data: dict,
) -> ArbitrationResult:
    """
    For LOW confidence tier (7-15% delta).
    Gemini analyzes both estimates line-by-line
    and returns a reconciled cost with reasoning.

    Prompt structure:
    - Physics breakdown (every cost line)
    - AI total estimate
    - Material + dimension context
    - Ask: "Which estimate is more accurate and why?
            What specific cost lines need adjustment?"

    Returns:
      reconciled_cost: float
      reasoning: str
      adjusted_lines: list[str]
      confidence_bump: bool  (true if arbitration resolved)
    """
```

### 2.4 Vision Extraction

```python
# extractors/vision.py

async def analyze_drawing(
    file_bytes: bytes,
    filename: str,
) -> ExtractionResult:
    """
    Extract technical specifications from engineering drawing.

    Strategy:
    1. Try OpenAI GPT-4o Vision (primary)
    2. If fails: try Google Gemini 1.5 Flash (fallback)
    3. If both fail: return partial result with low confidence

    GPT-4o prompt:
    - System: "You are an expert manufacturing engineer..."
    - User: [image] + "Extract: material, dimensions (OD, ID, length,
      width, height, holes, threads), tolerances, surface finish,
      manufacturing processes needed."
    - Response format: structured JSON matching Dimensions schema

    Post-processing:
    - Validate dimension ranges (reject absurd values)
    - Cross-check material vs processes (e.g., aluminum + hardening = warning)
    - Assign confidence: high (all fields), medium (partial), low (few fields)
    """

# extractors/process_detector.py

def detect_processes(
    dimensions: dict,
    material: str,
    notes: str = "",
) -> list[str]:
    """
    Detect manufacturing processes from part geometry.

    Rule-based logic:
    - Has outer_diameter + length -> "turning"
    - Has holes -> "drilling"
    - Has threads -> "threading"
    - Has grooves -> "grooving"
    - Has flat surfaces + width -> "milling_face"
    - Has tight tolerances -> "grinding"
    - Surface finish noted -> "surface_treatment"

    AI augmentation:
    - If confidence < medium, ask Gemini to verify process list
    - Gemini can add processes the rules miss (e.g., "gear hobbing")
    """
```

### 2.5 Similarity Engine

```python
# engines/similarity/embedder.py

EMBEDDING_DIM = 256

class EmbeddingStrategy(str, Enum):
    GEMINI_API = "gemini_api"      # Default: Gemini text embedding
    IMAGE_HASH = "image_hash"      # Fallback: perceptual hash
    DINOV2 = "dinov2"              # Future: DINOv2 model

def embed_drawing(
    image_bytes: bytes,
    strategy: EmbeddingStrategy = EmbeddingStrategy.GEMINI_API,
) -> list[float]:
    """
    Convert drawing image to 256-dimensional vector.

    Gemini strategy:
    1. Send image to Gemini with prompt:
       "Describe this engineering drawing: material, shape,
        dimensions, features, manufacturing processes"
    2. Embed the text description using Gemini text embedding
    3. Truncate/pad to 256 dimensions

    Image hash strategy (fallback):
    1. Resize image to 16x16 grayscale
    2. Compute perceptual hash (pHash)
    3. Expand to 256-dim float vector

    Returns: list[float] of length 256
    """

# engines/similarity/ranker.py

RANKING_WEIGHTS = {
    "visual": 0.50,      # Vector cosine similarity
    "material": 0.20,    # Exact or fuzzy material match
    "dimension": 0.20,   # Proximity of key dimensions
    "process": 0.10,     # Overlap of suggested processes
}

def rank_matches(
    query_metadata: dict,
    candidates: list[dict],  # from pgvector search
) -> list[RankedMatch]:
    """
    Multi-signal ranking.

    For each candidate:
    1. visual_score = 1 - cosine_distance (from pgvector)
    2. material_score = 1.0 if exact match, 0.5 if same family, 0.0 otherwise
    3. dimension_score = 1 - normalized_dimension_delta
    4. process_score = |intersection| / |union| (Jaccard)

    final_score = sum(weight * signal for each signal)

    Sort by final_score descending, return top 10.
    """
```

---

## 3. Frontend Component Design

### 3.1 Page Components

#### `/estimate/new/page.tsx` — State Machine

```typescript
// Step types
type Step =
  | "type"                // Choose single vs assembly
  | "upload"              // File upload
  | "extracting"          // Loading (AI extraction)
  | "review"              // Edit extracted data
  | "calculating"         // Loading (cost calculation)
  | "result"              // Display breakdown
  | "assembly-upload"     // Assembly: add components
  | "assembly-extracting" // Assembly: extracting component
  | "assembly-review"     // Assembly: review all components
  | "assembly-joining"    // Assembly: select joining method
  | "assembly-result"     // Assembly: display result

// State
interface EstimateState {
  step: Step
  partType: "single" | "assembly"
  file: File | null
  extractedData: ExtractedData | null
  quantity: number
  result: EstimateResponse | null
  error: string
  // Assembly-specific
  components: AssemblyComponent[]
  joiningMethod: string
  numJoints: number
  assemblyResult: AssemblyEstimateResponse | null
}

// Transitions
// type -> upload (user selects "single")
// type -> assembly-upload (user selects "assembly")
// upload -> extracting (file selected, call extractDrawing())
// extracting -> review (extraction complete)
// extracting -> upload (extraction failed, show error)
// review -> calculating (user confirms, call createEstimate())
// calculating -> result (estimate complete)
// result -> upload (user clicks "new estimate")
```

#### `/dashboard/page.tsx` — Data Loading

```typescript
// On mount:
// 1. Fetch estimates + usage in parallel
// 2. If 401: redirect to /login
// 3. If error: show error banner
// 4. Render: metric cards + intelligence feed + summary

// Data dependencies:
// - estimates: Estimate[] (from GET /api/estimates)
// - usage: Usage (from GET /api/usage)
// - latestEstimate: derived from estimates[0]
```

### 3.2 API Client (`src/lib/api.ts`)

```typescript
// Base configuration
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

// Auth header injection
async function getAuthHeaders(): Promise<Record<string, string>> {
  const supabase = createClient()
  const { data: { session } } = await supabase.auth.getSession()
  if (!session?.access_token) throw new Error("Not authenticated")
  return {
    Authorization: `Bearer ${session.access_token}`,
  }
}

// Error extraction
function parseErrorResponse(data: unknown): string {
  if (typeof data === "object" && data && "detail" in data) {
    return String((data as { detail: string }).detail)
  }
  return "An unexpected error occurred"
}

// Safe fetch wrapper
async function safeFetch(url: string, options: RequestInit): Promise<Response> {
  try {
    return await fetch(url, options)
  } catch {
    throw new Error("Network error — check your connection")
  }
}

// Example endpoint
export async function extractDrawing(file: File): Promise<ExtractedData> {
  const headers = await getAuthHeaders()
  const formData = new FormData()
  formData.append("file", file)

  const res = await safeFetch(`${API_URL}/api/extract`, {
    method: "POST",
    headers,
    body: formData,
  })

  if (!res.ok) {
    const data = await res.json()
    throw new Error(parseErrorResponse(data))
  }

  return res.json()
}
```

### 3.3 Middleware (`src/middleware.ts`)

```typescript
// Pattern: Check Supabase session, redirect if needed
export async function middleware(request: NextRequest) {
  const supabase = createServerClient(/* cookies */)
  const { data: { user } } = await supabase.auth.getUser()

  const isProtected = ["/dashboard", "/estimate", "/similar", "/rfq"]
    .some(p => request.nextUrl.pathname.startsWith(p))

  if (isProtected && !user) {
    return NextResponse.redirect(new URL("/login", request.url))
  }

  if (request.nextUrl.pathname === "/login" && user) {
    return NextResponse.redirect(new URL("/dashboard", request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ["/dashboard/:path*", "/estimate/:path*", "/similar/:path*", "/rfq/:path*", "/login"],
}
```

---

## 4. Key Algorithms

### 4.1 Material Volume Calculation

```python
def calculate_volume_cm3(dims: dict) -> float:
    """
    Calculate part volume from dimensions.

    For cylindrical parts (OD present):
      V = pi/4 * (OD^2 - ID^2) * L
      (convert mm to cm: / 1000)

    For prismatic parts (width + height present):
      V = L * W * H
      (convert mm to cm)

    For complex parts:
      V = surface_area_cm2 * estimated_thickness
    """
```

### 4.2 Nesting Utilization (Sheet Metal)

```python
def calculate_nesting_utilization(
    part_width_mm: float,
    part_length_mm: float,
    sheet_width_mm: float = 1220,   # Standard Indian 4x8 ft
    sheet_length_mm: float = 2440,
) -> float:
    """
    Rectangular part nesting on standard sheet.

    Try both orientations:
    1. parts_x = floor(sheet_width / part_width)
       parts_y = floor(sheet_length / part_length)
    2. parts_x = floor(sheet_width / part_length)
       parts_y = floor(sheet_length / part_width)

    utilization = max(orientation1, orientation2) * part_area / sheet_area
    Returns: float (0.0 to 1.0)
    """
```

### 4.3 Laser Cutting Speed Interpolation

```python
# engines/sheet_metal/cutting_db.py

# 3kW fiber laser speeds (mm/min) by material group x thickness
LASER_SPEEDS = {
    "mild_steel": {
        1.0: 8000, 2.0: 4500, 3.0: 3200, 4.0: 2400,
        5.0: 1800, 6.0: 1400, 8.0: 900, 10.0: 600, 12.0: 400,
    },
    "stainless_steel": {
        1.0: 6000, 2.0: 3200, 3.0: 2200, 4.0: 1600,
        5.0: 1200, 6.0: 900, 8.0: 500, 10.0: 350, 12.0: 200,
    },
    # ... 6 material groups total
}

def get_cutting_speed(material_group: str, thickness_mm: float) -> float:
    """
    Interpolate cutting speed for non-standard thicknesses.

    1. Find bracketing thicknesses in table
    2. Linear interpolation between them
    3. If below minimum: return max speed
    4. If above maximum: return min speed with 20% safety factor
    """
```

### 4.4 Bending Tonnage Formula

```python
def calculate_bend_force(
    material_uts_mpa: float,  # Ultimate tensile strength
    thickness_mm: float,
    bend_length_mm: float,
    v_die_opening_mm: float,
) -> float:
    """
    Press brake bending force.

    Formula (air bending):
      F = (UTS * T^2 * L) / (V * 1000)

    Where:
      F = force in tonnes
      UTS = ultimate tensile strength (MPa)
      T = thickness (mm)
      L = bend length (mm)
      V = V-die opening (mm), typically 8 * thickness
    """
    if v_die_opening_mm <= 0:
        v_die_opening_mm = 8 * thickness_mm
    return (material_uts_mpa * thickness_mm**2 * bend_length_mm) / (v_die_opening_mm * 1000)
```

---

## 5. Error Handling Patterns

### Backend

```python
# Route-level: catch specific exceptions
@router.post("/api/extract")
async def extract_drawing(file: UploadFile, user=Depends(get_current_user)):
    # Validate file size
    if file.size > 10 * 1024 * 1024:
        raise HTTPException(413, "File too large (max 10MB)")

    # Validate file type
    allowed = {"image/png", "image/jpeg", "application/pdf", "image/tiff", "image/webp"}
    if file.content_type not in allowed:
        raise HTTPException(400, f"Unsupported file type: {file.content_type}")

    # Budget check
    if not check_budget():
        raise HTTPException(403, "Daily budget exceeded. Try again tomorrow.")
    if not check_user_budget(user["id"]):
        raise HTTPException(403, "Usage limit reached. Try again in 48 hours.")

    # Extract
    try:
        result = await analyze_drawing(await file.read(), file.filename)
    except openai.RateLimitError:
        raise HTTPException(429, "AI service busy. Please retry in a few seconds.")
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise HTTPException(500, "Failed to analyze drawing. Please try again.")

    log_usage(user["id"], "extract", {"filename": file.filename})
    return result
```

### Frontend

```typescript
// Component-level: try-catch with user-friendly messages
async function handleExtract() {
  setStep("extracting")
  setError("")
  try {
    const data = await extractDrawing(file!)
    setExtractedData(data)
    setStep("review")
  } catch (e) {
    const msg = e instanceof Error ? e.message : "Extraction failed"
    setError(msg)
    setStep("upload")  // go back to upload step
  }
}
```

---

## 6. Configuration Constants

```python
# config.py — Single source of truth

# Machine rates (INR/hr)
MACHINE_RATES = {
    "turning": 800,
    "milling_face": 1000,
    "milling_end": 1000,
    "drilling": 600,
    "boring": 700,
    "reaming": 700,
    "threading": 700,
    "tapping": 600,
    "grooving": 700,
    "parting": 700,
    "knurling": 600,
    "grinding_cylindrical": 1200,
    "grinding_surface": 1200,
    "grinding_internal": 1500,
    "broaching": 1000,
    "honing": 1500,
    "lapping": 1500,
    "gear_hobbing": 1200,
}

# Setup times (minutes per batch)
SETUP_TIMES = {
    "turning": 30, "milling_face": 45, "drilling": 15,
    "boring": 30, "threading": 20, "grinding_cylindrical": 60,
    # ...
}

# Power consumption (kW per process)
POWER_CONSUMPTION = {
    "turning": 7.5, "milling_face": 11.0, "drilling": 3.5,
    # ...
}

# Global constants
LABOUR_RATE = 250          # INR/hr
POWER_RATE = 8             # INR/kWh
MATERIAL_WASTAGE_PCT = 15  # % raw material wasted
OVERHEAD_PCT = 15          # % overhead on subtotal
PROFIT_MARGIN_PCT = 20     # % profit on (subtotal + overhead)
TIGHT_TOLERANCE_SURCHARGE = 0.30  # 30% surcharge for < +-0.05mm

# PCB constants
SMD_RATE_PER_PAD = 1.50    # INR
THT_RATE_PER_PIN = 3.00    # INR
STENCIL_COST = 2500        # INR (amortized over quantity)
TEST_RATE_PER_BOARD = 25   # INR

# Cable constants
CABLE_LABOUR_RATE = 200    # INR/hr
WIRE_TIME_MIN = 2.0        # min per wire
CONNECTOR_TIME_MIN = 0.5   # min per connector
```

---

## 7. File Size & Complexity Guide

| File | Lines | Complexity | Notes |
|------|-------|-----------|-------|
| `estimate/new/page.tsx` | ~350 | High | 11-step state machine, largest frontend component |
| `api/schemas.py` | ~200 | Medium | 80+ Pydantic models, well-structured |
| `engines/mechanical/cost_engine.py` | ~200 | High | Core physics calculations |
| `engines/validation/orchestrator.py` | ~150 | High | Parallel execution, routing logic |
| `engines/mechanical/cutting_data.py` | ~150 | Medium | Constants + formulas |
| `api/routes/estimate.py` | ~150 | Medium | Material resolution, validation |
| `config.py` | ~130 | Low | Constants only |
| `src/lib/api.ts` | ~250 | Medium | All API calls, error handling |
| `src/app/page.tsx` | ~390 | Low | Static landing page markup |
| `src/app/dashboard/page.tsx` | ~490 | Medium | Data loading + rendering |
