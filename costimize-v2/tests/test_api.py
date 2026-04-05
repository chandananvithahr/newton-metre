"""Tests for FastAPI endpoints."""
import os

# Dummy JWT-format keys needed before api.deps imports (module-level os.environ reads)
_DUMMY_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0In0.test"
os.environ.setdefault("SUPABASE_URL", "http://localhost:54321")
os.environ.setdefault("SUPABASE_SERVICE_ROLE_KEY", _DUMMY_JWT)
os.environ.setdefault("SUPABASE_ANON_KEY", _DUMMY_JWT)

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from api.deps import get_current_user_id
from api.main import app


async def _mock_user_id() -> str:
    return "test-user-123"


app.dependency_overrides[get_current_user_id] = _mock_user_id


def auth_headers():
    return {"Authorization": "Bearer test-token"}


@patch("api.routes.extract.check_budget", return_value=True)
@patch("api.routes.extract.log_usage")
@patch("extractors.vision.analyze_drawing")
def test_extract_returns_dimensions(mock_analyze, mock_log, mock_budget):
    client = TestClient(app)
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
    assert data["suggested_processes"] == ["turning", "facing"]
    assert data["confidence"] == "high"


@patch("api.routes.extract.check_budget", return_value=False)
def test_extract_rejects_over_budget(mock_budget):
    client = TestClient(app)
    response = client.post(
        "/api/extract",
        files={"file": ("test.png", b"fake", "image/png")},
        headers=auth_headers(),
    )
    assert response.status_code == 429


@patch("api.routes.estimate.check_budget", return_value=True)
@patch("api.routes.estimate.log_usage")
@patch("api.routes.estimate.get_supabase_admin")
@patch("engines.validation.orchestrator.orchestrate")
def test_estimate_returns_breakdown(mock_orch, mock_sb, mock_log, mock_budget):
    client = TestClient(app)
    from engines.mechanical.cost_engine import (
        MechanicalCostBreakdown,
        ProcessCostLine,
    )
    from engines.validation.comparator import ConfidenceTier

    mock_orch.return_value = MagicMock(
        physics_result=MechanicalCostBreakdown(
            material_name="Mild Steel IS2062",
            raw_weight_kg=0.5,
            wastage_weight_kg=0.075,
            material_cost=50.0,
            process_lines=(
                ProcessCostLine(
                    "turning", "CNC Turning", 5.0, 66.7, 20.0, 5.0, 20.8, 2.0
                ),
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
            unit_cost_low=204,
            unit_cost_high=250,
            uncertainty_pct=10,
            order_cost=227.0,
            quantity=1,
        ),
        confidence_tier=ConfidenceTier.HIGH,
    )
    mock_sb.return_value.table.return_value.insert.return_value.execute.return_value = (
        None
    )

    response = client.post(
        "/api/estimate",
        json={
            "extracted_data": {
                "dimensions": {"outer_diameter_mm": 50, "length_mm": 100},
                "material": "Mild Steel IS2062",
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
    assert data["confidence_tier"] == "high"
    assert data["currency"] == "INR"
    assert len(data["process_lines"]) == 1
    assert data["process_lines"][0]["process_name"] == "CNC Turning"
