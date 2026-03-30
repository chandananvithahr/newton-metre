# Costimize — Testing Strategy & Plan

> Unit tests, integration tests, and E2E test plan.
> Last updated: 2026-03-30

---

## 1. Current State

### 1.1 Existing Test Coverage

| Test File | Tests | What It Covers |
|-----------|-------|---------------|
| `test_config.py` | 2 | Config loading, material/process data integrity |
| `test_mechanical_engine.py` | 19 | MRR calculations, process times, cost formulas, Sandvik kc1, Taylor tool life |
| `test_sheet_metal_engine.py` | 28 | Laser cutting speeds, bending tonnage, nesting, material costs, integration |
| `test_surface_treatment.py` | 19 | 40+ surface treatment processes, area-based costing, H.E. baking |
| `test_heat_treatment.py` | 12 | 15 heat treatment processes, weight-based costing |
| `test_extractors.py` | 6 | Vision extraction, process detection, BOM parsing |
| `test_pcb_engine.py` | 5 | PCB assembly cost model |
| `test_cable_engine.py` | 3 | Cable assembly labour model |
| `test_component_scraper.py` | 3 | DigiKey/Mouser price scraping |
| `test_material_scraper.py` | 3 | Metal material price lookup |
| `test_history.py` | 5 | PO parsing, matching, deduplication |
| `test_validation.py` | 29 | Comparator, arbitrator, interactive, orchestrator |
| `test_similarity.py` | 32 | Embedder, ranker, indexer, searcher |
| **Total** | **164** | |

### 1.2 Gaps Identified

| Area | Current Coverage | Gap |
|------|-----------------|-----|
| **Backend API routes** | 0 tests | No route-level integration tests |
| **Auth flow** | 0 tests | JWT validation, middleware untested |
| **Budget tracking** | 0 tests | cost_tracker.py untested |
| **Frontend components** | 0 tests | No React component tests |
| **E2E workflows** | 0 tests | No end-to-end browser tests |
| **Error paths** | Minimal | Happy paths mostly, few error cases |
| **Edge cases** | Partial | Missing: zero quantity, negative dims, empty processes |

---

## 2. Testing Architecture

### 2.1 Test Pyramid

```
        /\
       /  \       E2E Tests (Playwright)
      /    \      - Full user workflows
     /------\     - 5-10 critical paths
    /        \
   / Integr.  \   Integration Tests (pytest + httpx)
  /   Tests    \  - API routes with mocked AI
 /              \ - Database operations
/                \- Auth flow
/------------------\
/                    \ Unit Tests (pytest)
/   Unit Tests        \ - Cost engines (physics math)
/                      \ - Validators, parsers
/________________________\ - Pure functions
                           164 existing + new
```

### 2.2 Test Organization

```
costimize-v2/tests/
├── unit/                          # Pure function tests (no I/O)
│   ├── test_config.py
│   ├── test_mechanical_engine.py
│   ├── test_sheet_metal_engine.py
│   ├── test_surface_treatment.py
│   ├── test_heat_treatment.py
│   ├── test_pcb_engine.py
│   ├── test_cable_engine.py
│   ├── test_validation.py
│   ├── test_similarity.py
│   └── test_history.py
│
├── integration/                   # API + database tests
│   ├── test_extract_routes.py     # NEW
│   ├── test_estimate_routes.py    # NEW
│   ├── test_auth_flow.py          # NEW
│   ├── test_budget_tracking.py    # NEW
│   ├── test_rfq_routes.py         # NEW
│   └── test_similarity_routes.py  # NEW
│
├── fixtures/                      # Test data
│   ├── sample_drawing.png
│   ├── sample_bom.csv
│   ├── sample_rfq.pdf
│   └── mock_responses.py         # Predefined AI responses
│
└── conftest.py                    # Shared fixtures, test client

frontend/
├── __tests__/                     # NEW: Frontend tests
│   ├── components/
│   │   ├── Toast.test.tsx
│   │   ├── CostBreakdownTable.test.tsx
│   │   └── CopyValue.test.tsx
│   ├── lib/
│   │   ├── api.test.ts
│   │   └── supabase.test.ts
│   └── pages/
│       ├── login.test.tsx
│       └── dashboard.test.tsx
│
├── e2e/                           # NEW: E2E tests (Playwright)
│   ├── auth.spec.ts
│   ├── estimate-workflow.spec.ts
│   ├── dashboard.spec.ts
│   ├── rfq-workflow.spec.ts
│   └── similarity.spec.ts
│
├── jest.config.ts                 # NEW
├── playwright.config.ts           # NEW
└── package.json                   # Add: vitest, @testing-library/react, playwright
```

---

## 3. Unit Test Plan

### 3.1 Existing Tests — No Changes Needed

The 164 existing tests cover the core physics engines well. They test:
- Material lookup and pricing
- Process time calculations (MRR-based)
- Cutting parameter formulas (Sandvik kc1, Taylor)
- Cost aggregation (material + machining + overhead + profit)
- Sheet metal models (laser, bending, nesting)
- Validation pipeline (comparator, orchestrator)
- Similarity search (embedder, ranker)

### 3.2 New Unit Tests

#### `test_cost_tracker.py` (NEW — 8 tests)

```python
# Tests for api/cost_tracker.py

def test_cost_lookup_known_action():
    """COST_PER_ACTION["extract"] should return 0.002"""

def test_cost_lookup_unknown_action():
    """Unknown action should return default 0.01"""

def test_check_budget_under_limit():
    """When today's total < $2.00, should return True"""

def test_check_budget_over_limit():
    """When today's total >= $2.00, should return False"""

def test_check_user_budget_under_limit():
    """When user's 48h total < $0.50, should return True"""

def test_check_user_budget_over_limit():
    """When user's 48h total >= $0.50, should return False"""

def test_log_usage_inserts_record():
    """log_usage should insert a row into usage_log"""

def test_log_usage_correct_cost():
    """Inserted cost should match COST_PER_ACTION"""
```

#### `test_schemas.py` (NEW — 6 tests)

```python
# Tests for api/schemas.py Pydantic models

def test_dimensions_all_optional():
    """Dimensions() with no args should not raise"""

def test_estimate_request_default_quantity():
    """EstimateRequest with only extracted_data should default quantity=1"""

def test_estimate_request_rejects_zero_quantity():
    """quantity=0 should raise validation error"""

def test_assembly_request_requires_components():
    """AssemblyEstimateRequest with empty components should fail"""

def test_process_line_immutable():
    """ProcessLine should be a frozen/immutable model"""

def test_extracted_data_roundtrip():
    """ExtractedData -> dict -> ExtractedData should be identical"""
```

#### `test_edge_cases.py` (NEW — 12 tests)

```python
# Edge cases for cost engines

def test_mechanical_zero_quantity():
    """quantity=0 should raise or return 0 order_cost"""

def test_mechanical_negative_diameter():
    """Negative diameter should raise ValueError"""

def test_mechanical_no_processes():
    """Empty process list should still return material cost"""

def test_mechanical_unknown_material():
    """Unknown material should fall back to default or raise"""

def test_sheet_metal_zero_thickness():
    """thickness=0 should not cause division by zero"""

def test_sheet_metal_huge_part():
    """Part larger than sheet should report >100% utilization"""

def test_drilling_zero_holes():
    """hole_count=0 should return 0 drilling time"""

def test_turning_very_small_part():
    """1mm diameter part should not underflow"""

def test_turning_very_large_part():
    """1000mm diameter part should be handled"""

def test_taylor_tool_life_extreme_speed():
    """Very high cutting speed should give very short tool life"""

def test_power_calculation_zero_feed():
    """Feed=0 should not cause math error"""

def test_nesting_tiny_part_on_large_sheet():
    """Very small parts should have high utilization"""
```

---

## 4. Integration Test Plan

### 4.1 API Route Tests

```python
# tests/integration/conftest.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

@pytest.fixture
def client():
    """Test client with mocked auth."""
    from api.main import app
    return TestClient(app)

@pytest.fixture
def auth_headers():
    """Mock JWT auth headers."""
    return {"Authorization": "Bearer test-jwt-token"}

@pytest.fixture
def mock_auth():
    """Patch get_current_user to return test user."""
    with patch("api.deps.get_current_user") as mock:
        mock.return_value = {"id": "test-user-123", "email": "test@test.com"}
        yield mock
```

#### `test_extract_routes.py` (NEW — 10 tests)

```python
def test_extract_requires_auth(client):
    """POST /api/extract without JWT should return 401"""

def test_extract_rejects_large_file(client, mock_auth, auth_headers):
    """File > 10MB should return 413"""

def test_extract_rejects_invalid_type(client, mock_auth, auth_headers):
    """Non-image/PDF file should return 400"""

def test_extract_returns_dimensions(client, mock_auth, auth_headers, mock_vision):
    """Valid drawing should return structured dimensions"""

def test_extract_handles_vision_failure(client, mock_auth, auth_headers):
    """If GPT-4o + Gemini both fail, should return 500 with message"""

def test_extract_logs_usage(client, mock_auth, auth_headers, mock_vision):
    """Successful extraction should insert usage_log record"""

def test_extract_respects_budget(client, mock_auth, auth_headers):
    """If budget exceeded, should return 403"""

def test_extract_rate_limited(client, mock_auth, auth_headers):
    """11th request in 1 minute should return 429"""

def test_extract_multi_requires_2_files(client, mock_auth, auth_headers):
    """Single file to /extract/multi should return 400"""

def test_extract_multi_max_5_files(client, mock_auth, auth_headers):
    """6 files to /extract/multi should return 400"""
```

#### `test_estimate_routes.py` (NEW — 12 tests)

```python
def test_estimate_requires_auth(client):
    """POST /api/estimate without JWT should return 401"""

def test_estimate_valid_request(client, mock_auth, auth_headers):
    """Valid extracted data + quantity should return cost breakdown"""

def test_estimate_saves_to_database(client, mock_auth, auth_headers, mock_supabase):
    """Successful estimate should be inserted into estimates table"""

def test_estimate_resolves_material_alias(client, mock_auth, auth_headers):
    """'EN8' should resolve to 'EN8 Steel'"""

def test_estimate_unknown_material_fallback(client, mock_auth, auth_headers):
    """Unknown material should use Mild Steel as default"""

def test_estimate_applies_tolerance_surcharge(client, mock_auth, auth_headers):
    """Tight tolerances (<0.05mm) should add 30% surcharge"""

def test_estimate_quantity_affects_setup_cost(client, mock_auth, auth_headers):
    """Higher quantity should reduce setup cost per unit"""

def test_estimate_returns_confidence_tier(client, mock_auth, auth_headers):
    """Response should include confidence_tier field"""

def test_estimate_logs_usage(client, mock_auth, auth_headers):
    """Should log cost to usage_log"""

def test_estimate_respects_user_budget(client, mock_auth, auth_headers):
    """Over-budget user should get 403"""

def test_assembly_estimate_valid(client, mock_auth, auth_headers):
    """Valid assembly request should return component + joining costs"""

def test_assembly_estimate_joining_methods(client, mock_auth, auth_headers):
    """All 6 joining methods should calculate without error"""
```

#### `test_rfq_routes.py` (NEW — 6 tests)

```python
def test_rfq_extract_requires_auth(client):
    """POST /api/rfq/extract without JWT should return 401"""

def test_rfq_extract_valid_pdf(client, mock_auth, auth_headers, mock_vision):
    """Valid RFQ PDF should return line items"""

def test_rfq_extract_classifies_document(client, mock_auth, auth_headers, mock_vision):
    """Should identify document_type (rfq, drawing, spec, etc.)"""

def test_rfq_estimate_all_items(client, mock_auth, auth_headers):
    """Should return cost for each line item + total"""

def test_rfq_estimate_handles_failed_items(client, mock_auth, auth_headers):
    """Failed items should have error field set, not crash entire request"""

def test_rfq_extract_rejects_non_pdf(client, mock_auth, auth_headers):
    """Non-PDF file should return 400"""
```

#### `test_similarity_routes.py` (NEW — 6 tests)

```python
def test_similarity_embed_requires_auth(client):
    """POST /api/similarity/embed without JWT should return 401"""

def test_similarity_embed_returns_id(client, mock_auth, auth_headers, mock_embedder):
    """Should return drawing_id UUID"""

def test_similarity_search_returns_matches(client, mock_auth, auth_headers, mock_searcher):
    """Should return ranked matches with scores"""

def test_similarity_search_user_scoped(client, mock_auth, auth_headers, mock_searcher):
    """User should only see their own drawings"""

def test_similarity_search_min_2_drawings(client, mock_auth, auth_headers):
    """Search with 0 existing drawings should return empty"""

def test_similarity_logs_usage(client, mock_auth, auth_headers, mock_embedder):
    """Both embed and search should log usage"""
```

---

## 5. Frontend Test Plan

### 5.1 Setup

```bash
# Install test dependencies
cd frontend
npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom
npm install -D @playwright/test
npx playwright install
```

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./tests/setup.ts'],
    globals: true,
  },
  resolve: {
    alias: {
      '@': './src',
    },
  },
})
```

### 5.2 Component Tests

#### `Toast.test.tsx` (6 tests)

```typescript
describe("ToastProvider", () => {
  it("renders children")
  it("shows toast when triggered")
  it("auto-dismisses after timeout")
  it("supports success variant")
  it("supports error variant")
  it("handles multiple toasts")
})
```

#### `CostBreakdownTable.test.tsx` (4 tests)

```typescript
describe("CostBreakdownTable", () => {
  it("renders all 10 cost lines")
  it("displays correct total")
  it("copies value to clipboard on click")
  it("shows toast after copy")
})
```

#### `api.test.ts` (8 tests)

```typescript
describe("API client", () => {
  it("includes auth header in requests")
  it("throws 'Not authenticated' when no session")
  it("parses error detail from response")
  it("handles network errors gracefully")
  it("extractDrawing sends multipart form data")
  it("createEstimate sends JSON body")
  it("getEstimates returns array")
  it("getMaterialPrice returns price object")
})
```

---

## 6. E2E Test Plan (Playwright)

### 6.1 Critical User Flows

#### Flow 1: Sign Up + First Estimate

```typescript
// e2e/estimate-workflow.spec.ts

test("new user can sign up and create first estimate", async ({ page }) => {
  // 1. Go to /login
  await page.goto("/login")

  // 2. Sign up with test email
  await page.fill('[name="email"]', 'e2e-test@example.com')
  await page.fill('[name="password"]', 'TestPassword123!')
  await page.click('button:has-text("Sign up")')

  // 3. Redirected to /dashboard
  await expect(page).toHaveURL(/\/dashboard/)
  await expect(page.locator("h1")).toContainText("COST INTELLIGENCE")

  // 4. Click "Analyse a Part"
  await page.click('button:has-text("Analyse a Part")')
  await expect(page).toHaveURL(/\/estimate\/new/)

  // 5. Select "Single Part"
  await page.click('button:has-text("Single Part")')

  // 6. Upload test drawing
  await page.setInputFiles('input[type="file"]', 'e2e/fixtures/test-drawing.png')

  // 7. Wait for extraction
  await page.waitForSelector('text=Review', { timeout: 30000 })

  // 8. Confirm extraction and calculate
  await page.fill('[name="quantity"]', '100')
  await page.click('button:has-text("Calculate")')

  // 9. Wait for result
  await page.waitForSelector('text=Should cost', { timeout: 15000 })

  // 10. Verify cost breakdown is visible
  await expect(page.locator('text=Material')).toBeVisible()
  await expect(page.locator('text=INR')).toBeVisible()
})
```

#### Flow 2: Dashboard Data Display

```typescript
// e2e/dashboard.spec.ts

test("dashboard shows estimates and stats", async ({ page }) => {
  // Login
  await loginAsTestUser(page)

  // Navigate to dashboard
  await page.goto("/dashboard")

  // Verify metric cards
  await expect(page.locator('text=Analyses Run')).toBeVisible()
  await expect(page.locator('text=Parts Matched')).toBeVisible()

  // Verify recent analyses section
  await expect(page.locator('text=RECENT ANALYSES')).toBeVisible()
})
```

#### Flow 3: Auth Protection

```typescript
// e2e/auth.spec.ts

test("unauthenticated user redirected to login", async ({ page }) => {
  await page.goto("/dashboard")
  await expect(page).toHaveURL(/\/login/)
})

test("authenticated user redirected from login to dashboard", async ({ page }) => {
  await loginAsTestUser(page)
  await page.goto("/login")
  await expect(page).toHaveURL(/\/dashboard/)
})

test("logout clears session", async ({ page }) => {
  await loginAsTestUser(page)
  await page.goto("/dashboard")
  await page.click('button[title="Log out"]')
  await expect(page).toHaveURL("/")
})
```

#### Flow 4: RFQ Workflow

```typescript
// e2e/rfq-workflow.spec.ts

test("user can extract and estimate RFQ", async ({ page }) => {
  await loginAsTestUser(page)
  await page.goto("/rfq/new")

  // Upload RFQ PDF
  await page.setInputFiles('input[type="file"]', 'e2e/fixtures/sample-rfq.pdf')

  // Wait for extraction
  await page.waitForSelector('text=Line Items', { timeout: 30000 })

  // Verify line items appear
  await expect(page.locator('table tbody tr')).toHaveCount({ minimum: 1 })

  // Click estimate all
  await page.click('button:has-text("Estimate")')

  // Wait for results
  await page.waitForSelector('text=Total', { timeout: 30000 })
})
```

#### Flow 5: Similarity Search

```typescript
// e2e/similarity.spec.ts

test("user can search for similar parts", async ({ page }) => {
  await loginAsTestUser(page)
  await page.goto("/similar")

  // Upload 2 drawings
  await page.setInputFiles('input[type="file"]', [
    'e2e/fixtures/drawing-1.png',
    'e2e/fixtures/drawing-2.png',
  ])

  // Wait for results
  await page.waitForSelector('text=similarity', { timeout: 30000 })
})
```

---

## 7. Test Commands

```bash
# Backend unit tests (existing)
cd costimize-v2
python -m pytest tests/ -v

# Backend unit tests (fast, no AI mocks)
python -m pytest tests/ -v -m "not slow"

# Backend integration tests (new)
python -m pytest tests/integration/ -v

# All backend tests
python -m pytest tests/ -v --tb=short

# Coverage report
python -m pytest tests/ --cov=engines --cov=api --cov-report=html

# Frontend component tests
cd frontend
npx vitest run

# Frontend tests in watch mode
npx vitest

# E2E tests (requires running dev servers)
npx playwright test

# E2E with browser visible
npx playwright test --headed

# Single E2E test
npx playwright test e2e/estimate-workflow.spec.ts
```

---

## 8. CI/CD Test Pipeline

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [master]
  pull_request:
    branches: [master]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: |
          cd costimize-v2
          pip install -r requirements.txt
          pip install -r api/requirements.txt
          pip install pytest pytest-cov
      - run: |
          cd costimize-v2
          python -m pytest tests/ -v --tb=short
      - run: |
          cd costimize-v2
          python -m pytest tests/ --cov=engines --cov=api --cov-report=xml
      - uses: codecov/codecov-action@v4
        with:
          file: costimize-v2/coverage.xml

  frontend-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - run: |
          cd frontend
          npm ci
          npx next build
      # Frontend component tests (when added):
      # - run: cd frontend && npx vitest run

  # E2E tests (when added):
  # e2e-tests:
  #   needs: [backend-tests, frontend-build]
  #   runs-on: ubuntu-latest
  #   steps:
  #     - Start backend + frontend
  #     - npx playwright test
```

---

## 9. Test Coverage Targets

| Area | Current | Target | Priority |
|------|---------|--------|----------|
| Mechanical engine | ~85% | 90% | Maintain |
| Sheet metal engine | ~80% | 85% | Maintain |
| Validation pipeline | ~75% | 85% | Improve |
| Similarity engine | ~70% | 80% | Improve |
| API routes | 0% | 80% | **High** |
| Budget tracking | 0% | 90% | **High** |
| Auth flow | 0% | 70% | **Medium** |
| Frontend components | 0% | 60% | **Medium** |
| E2E critical paths | 0% | 5 flows | **Medium** |

### Priority Order for New Tests

1. **API route integration tests** — highest risk, no coverage
2. **Budget tracking unit tests** — money-related, must be correct
3. **Edge case unit tests** — prevent production crashes
4. **Frontend API client tests** — error handling matters
5. **E2E estimate workflow** — core user flow
6. **E2E auth flow** — security-critical
7. **Frontend component tests** — nice to have
8. **Remaining E2E flows** — nice to have

---

## 10. Test Data Management

### Backend Fixtures

```python
# tests/fixtures/mock_responses.py

MOCK_EXTRACTION_RESULT = {
    "dimensions": {
        "outer_diameter_mm": 50,
        "length_mm": 100,
        "hole_count": 4,
        "hole_diameter_mm": 8,
        "thread_count": 2,
    },
    "material": "EN8 Steel",
    "material_confidence": "high",
    "tolerances": {
        "has_tight_tolerances": False,
    },
    "suggested_processes": ["turning", "drilling", "threading"],
    "confidence": "high",
    "notes": "Standard shaft with through-holes and threads",
}

MOCK_GEMINI_ESTIMATE = {
    "total_cost": 720.0,
    "breakdown": {
        "material": 230,
        "machining": 280,
        "overhead": 110,
        "profit": 100,
    },
}
```

### E2E Fixtures

- `e2e/fixtures/test-drawing.png` — Simple CNC shaft drawing
- `e2e/fixtures/sample-rfq.pdf` — 3-line-item RFQ
- `e2e/fixtures/drawing-1.png` — For similarity search
- `e2e/fixtures/drawing-2.png` — For similarity search

### Test User

```typescript
// e2e/helpers.ts
const TEST_USER = {
  email: "e2e-test@costimize.dev",
  password: "E2eTestPassword123!",
}

async function loginAsTestUser(page: Page) {
  await page.goto("/login")
  await page.fill('[name="email"]', TEST_USER.email)
  await page.fill('[name="password"]', TEST_USER.password)
  await page.click('button:has-text("Sign in")')
  await page.waitForURL(/\/dashboard/)
}
```
