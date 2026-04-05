"""Tests for the sheet metal cost engine — laser cutting, bending, material."""
from engines.sheet_metal.material_db import (
    get_sheet_material, list_sheet_material_names,
    calculate_blank_weight_kg, estimate_utilization_pct,
)
from engines.sheet_metal.cutting_db import (
    get_laser_speed_m_per_min, get_pierce_time_sec,
    estimate_laser_cutting_time_min, estimate_laser_cutting_cost,
)
from engines.sheet_metal.bending_db import (
    calculate_bending_tonnage, select_press_brake_size,
    estimate_bending_time_min, estimate_bending_cost,
    calculate_bend_allowance,
    get_min_bend_radius_mm, get_springback_deg, check_bend_radius,
    MIN_BEND_RADIUS_FACTOR, SPRINGBACK_DEG,
)
from engines.sheet_metal.cost_engine import (
    calculate_sheet_metal_cost, SheetMetalCostBreakdown,
    HARDWARE_RATES,
)
import math
import pytest


# --- Material DB ---

def test_list_sheet_materials():
    names = list_sheet_material_names()
    assert len(names) >= 8
    assert "Mild Steel CR" in names
    assert "Stainless Steel 304" in names


def test_get_sheet_material():
    mat = get_sheet_material("Mild Steel CR")
    assert mat.density_kg_per_m3 == 7850
    assert mat.price_per_kg_inr == 65
    assert mat.uts_mpa == 450


def test_unknown_material_raises():
    with pytest.raises(ValueError):
        get_sheet_material("Unobtanium")


def test_blank_weight_calculation():
    """200×300×2mm mild steel blank."""
    weight = calculate_blank_weight_kg(300, 200, 2, 7850)
    expected = 0.3 * 0.2 * 0.002 * 7850  # 0.942 kg
    assert abs(weight - expected) < 0.001


def test_utilization_rectangular():
    """Rectangular parts should give >80% utilization."""
    util = estimate_utilization_pct(200, 100, 2500, 1250)
    assert util > 80


def test_utilization_large_part():
    """Part larger than sheet → fallback 75%."""
    util = estimate_utilization_pct(3000, 2000, 2500, 1250)
    assert util == 75.0


# --- Laser Cutting ---

def test_laser_speed_mild_steel_3mm():
    speed = get_laser_speed_m_per_min("Mild Steel CR", 3)
    assert speed == 10  # exact lookup


def test_laser_speed_interpolation():
    """4mm should interpolate between 3mm (10) and 5mm (5)."""
    speed = get_laser_speed_m_per_min("Mild Steel CR", 4)
    assert 5 < speed < 10


def test_laser_speed_stainless_slower():
    """Stainless should be slower than mild steel at same thickness."""
    ms = get_laser_speed_m_per_min("Mild Steel CR", 2)
    ss = get_laser_speed_m_per_min("Stainless Steel 304", 2)
    assert ss < ms


def test_laser_speed_unknown_material():
    with pytest.raises(ValueError):
        get_laser_speed_m_per_min("Titanium", 1)


def test_pierce_time_scales_with_thickness():
    t1 = get_pierce_time_sec("Mild Steel CR", 1)
    t5 = get_pierce_time_sec("Mild Steel CR", 5)
    assert t5 > t1 * 2  # thicker → much longer pierce


def test_pierce_time_ss_longer():
    """Stainless pierce takes 1.5x longer."""
    ms = get_pierce_time_sec("Mild Steel CR", 3)
    ss = get_pierce_time_sec("Stainless Steel 304", 3)
    assert abs(ss / ms - 1.5) < 0.01


def test_cutting_time_positive():
    time = estimate_laser_cutting_time_min("Mild Steel CR", 2, 1000, 4)
    assert time > 0
    assert time < 5  # 1m perimeter in 2mm MS should be fast


def test_cutting_cost_positive():
    cost = estimate_laser_cutting_cost("Mild Steel CR", 2, 1000, 4)
    assert cost > 0


# --- Bending ---

def test_bending_tonnage_mild_steel():
    """2mm × 500mm bend in MS (UTS=450) should need ~5-15 tons."""
    tonnage = calculate_bending_tonnage(450, 2, 500)
    assert 1 < tonnage < 20


def test_bending_tonnage_thicker_is_more():
    t2 = calculate_bending_tonnage(450, 2, 500)
    t5 = calculate_bending_tonnage(450, 5, 500)
    # With V=8T, tonnage = UTS×T²×L/(8T×1000) = UTS×T×L/8000 → linear in T
    # So 5mm should be ~2.5× the 2mm value
    assert t5 > t2 * 2


def test_press_brake_selection():
    assert select_press_brake_size(30) == "small"
    assert select_press_brake_size(75) == "medium"
    assert select_press_brake_size(150) == "large"
    assert select_press_brake_size(400) == "heavy"


def test_bending_time_scales_with_count():
    t2 = estimate_bending_time_min(2)
    t6 = estimate_bending_time_min(6)
    assert abs(t6 / t2 - 3) < 0.1


def test_bending_cost_returns_tuple():
    cycle, setup = estimate_bending_cost(
        uts_mpa=450, thickness_mm=2, bend_length_mm=500,
        n_bends=4, quantity=100,
    )
    assert cycle > 0
    assert setup > 0
    assert setup < cycle  # setup amortized over 100 should be small


def test_bend_allowance():
    """90° bend, 2mm radius, 1mm sheet, K=0.42 → BA ≈ π/2 × (2 + 0.42)."""
    ba = calculate_bend_allowance(90, 2.0, 1.0, 0.42)
    expected = (math.pi / 2) * (2.0 + 0.42 * 1.0)
    assert abs(ba - expected) < 0.001


# --- Full Cost Engine ---

def test_basic_sheet_metal_cost():
    """Simple flat laser-cut part in 2mm MS."""
    result = calculate_sheet_metal_cost(
        material_name="Mild Steel CR",
        thickness_mm=2,
        part_length_mm=300,
        part_width_mm=200,
        cutting_length_mm=1000,
        pierce_count=5,
        quantity=100,
    )
    assert isinstance(result, SheetMetalCostBreakdown)
    assert result.quantity == 100
    assert result.material_cost > 0
    assert result.cutting_cost > 0
    assert result.unit_cost > 0
    assert result.order_cost == round(result.unit_cost * 100, 2)


def test_cost_with_bending():
    """Part with 4 bends should cost more than flat part."""
    flat = calculate_sheet_metal_cost(
        material_name="Mild Steel CR", thickness_mm=2,
        part_length_mm=300, part_width_mm=200,
        cutting_length_mm=1000, pierce_count=5, quantity=100,
    )
    bent = calculate_sheet_metal_cost(
        material_name="Mild Steel CR", thickness_mm=2,
        part_length_mm=300, part_width_mm=200,
        cutting_length_mm=1000, pierce_count=5,
        n_bends=4, bend_complexity="simple", quantity=100,
    )
    assert bent.unit_cost > flat.unit_cost
    assert bent.bending_cost > 0


def test_cost_with_welding():
    result = calculate_sheet_metal_cost(
        material_name="Mild Steel CR", thickness_mm=2,
        part_length_mm=300, part_width_mm=200,
        cutting_length_mm=1000, pierce_count=5,
        weld_type="mig", weld_length_mm=500, quantity=100,
    )
    assert result.welding_cost > 0


def test_cost_with_finish():
    no_finish = calculate_sheet_metal_cost(
        material_name="Mild Steel CR", thickness_mm=2,
        part_length_mm=300, part_width_mm=200,
        cutting_length_mm=1000, pierce_count=5, quantity=100,
    )
    powder = calculate_sheet_metal_cost(
        material_name="Mild Steel CR", thickness_mm=2,
        part_length_mm=300, part_width_mm=200,
        cutting_length_mm=1000, pierce_count=5,
        finish_type="powder_coating", quantity=100,
    )
    assert powder.unit_cost > no_finish.unit_cost
    assert powder.finish_cost > 0


def test_stainless_costs_more():
    """SS304 should cost significantly more than MS for same part."""
    ms = calculate_sheet_metal_cost(
        material_name="Mild Steel CR", thickness_mm=2,
        part_length_mm=300, part_width_mm=200,
        cutting_length_mm=1000, pierce_count=5, quantity=100,
    )
    ss = calculate_sheet_metal_cost(
        material_name="Stainless Steel 304", thickness_mm=2,
        part_length_mm=300, part_width_mm=200,
        cutting_length_mm=1000, pierce_count=5, quantity=100,
    )
    assert ss.unit_cost > ms.unit_cost * 1.5


def test_higher_quantity_reduces_setup():
    q10 = calculate_sheet_metal_cost(
        material_name="Mild Steel CR", thickness_mm=2,
        part_length_mm=300, part_width_mm=200,
        cutting_length_mm=1000, pierce_count=5, quantity=10,
    )
    q1000 = calculate_sheet_metal_cost(
        material_name="Mild Steel CR", thickness_mm=2,
        part_length_mm=300, part_width_mm=200,
        cutting_length_mm=1000, pierce_count=5, quantity=1000,
    )
    assert q10.total_setup_cost > q1000.total_setup_cost


def test_tight_tolerance_surcharge():
    base = calculate_sheet_metal_cost(
        material_name="Mild Steel CR", thickness_mm=2,
        part_length_mm=300, part_width_mm=200,
        cutting_length_mm=1000, pierce_count=5, quantity=100,
    )
    tight = calculate_sheet_metal_cost(
        material_name="Mild Steel CR", thickness_mm=2,
        part_length_mm=300, part_width_mm=200,
        cutting_length_mm=1000, pierce_count=5, quantity=100,
        has_tight_tolerances=True,
    )
    assert tight.cutting_cost > base.cutting_cost


def test_thicker_material_slower_cutting():
    """5mm should cost more to cut than 2mm (same perimeter)."""
    thin = calculate_sheet_metal_cost(
        material_name="Mild Steel CR", thickness_mm=2,
        part_length_mm=300, part_width_mm=200,
        cutting_length_mm=1000, pierce_count=5, quantity=100,
    )
    thick = calculate_sheet_metal_cost(
        material_name="Mild Steel CR", thickness_mm=5,
        part_length_mm=300, part_width_mm=200,
        cutting_length_mm=1000, pierce_count=5, quantity=100,
    )
    assert thick.cutting_cost > thin.cutting_cost * 2


# --- Bend Radius Validation (Phase 3B) ---

def test_min_bend_radius_mild_steel():
    """2mm MS → min radius = 0.8 × 2 = 1.6mm."""
    r = get_min_bend_radius_mm("Mild Steel CR", 2.0)
    assert abs(r - 1.6) < 0.01


def test_min_bend_radius_stainless():
    """2mm SS304 → min radius = 1.0 × 2 = 2.0mm."""
    r = get_min_bend_radius_mm("Stainless Steel 304", 2.0)
    assert abs(r - 2.0) < 0.01


def test_min_bend_radius_aluminum():
    """3mm Al 5052 → min radius = 0.5 × 3 = 1.5mm."""
    r = get_min_bend_radius_mm("Aluminum 5052", 3.0)
    assert abs(r - 1.5) < 0.01


def test_springback_values():
    assert get_springback_deg("Mild Steel CR") == 2.0
    assert get_springback_deg("Stainless Steel 304") == 3.0
    assert get_springback_deg("Aluminum 5052") == 1.0
    assert get_springback_deg("Copper") == 0.5


def test_springback_default_unknown():
    """Unknown material should get default 2.0°."""
    assert get_springback_deg("Unobtanium") == 2.0


def test_check_bend_radius_ok():
    """2mm MS with 2.0mm radius (above 1.6mm min) → no surcharge."""
    below, mult = check_bend_radius("Mild Steel CR", 2.0, 2.0)
    assert not below
    assert mult == 1.0


def test_check_bend_radius_below_min():
    """2mm MS with 1.0mm radius (below 1.6mm min) → 20% surcharge."""
    below, mult = check_bend_radius("Mild Steel CR", 2.0, 1.0)
    assert below
    assert abs(mult - 1.20) < 0.01


def test_check_bend_radius_none():
    """None radius → no surcharge (standard assumed)."""
    below, mult = check_bend_radius("Mild Steel CR", 2.0, None)
    assert not below
    assert mult == 1.0


def test_all_materials_have_bend_data():
    """Every sheet material should have min bend radius and springback entries."""
    from engines.sheet_metal.material_db import SHEET_MATERIALS
    for name in SHEET_MATERIALS:
        assert name in MIN_BEND_RADIUS_FACTOR, f"Missing min bend radius for {name}"
        assert name in SPRINGBACK_DEG, f"Missing springback for {name}"


def test_cost_with_tight_bend_radius():
    """Part with below-min bend radius should cost more than standard."""
    standard = calculate_sheet_metal_cost(
        material_name="Mild Steel CR", thickness_mm=2,
        part_length_mm=300, part_width_mm=200,
        cutting_length_mm=1000, pierce_count=5,
        n_bends=4, bend_radius_mm=2.0, quantity=100,
    )
    tight = calculate_sheet_metal_cost(
        material_name="Mild Steel CR", thickness_mm=2,
        part_length_mm=300, part_width_mm=200,
        cutting_length_mm=1000, pierce_count=5,
        n_bends=4, bend_radius_mm=0.5, quantity=100,  # well below 1.6mm min
    )
    assert tight.bending_cost > standard.bending_cost
    assert tight.unit_cost > standard.unit_cost


def test_springback_in_bending_description():
    """Bending line description should mention springback."""
    result = calculate_sheet_metal_cost(
        material_name="Stainless Steel 304", thickness_mm=2,
        part_length_mm=300, part_width_mm=200,
        cutting_length_mm=1000, pierce_count=5,
        n_bends=4, quantity=100,
    )
    bend_lines = [l for l in result.lines if l.item == "Bending"]
    assert len(bend_lines) == 1
    assert "springback 3.0°" in bend_lines[0].description


# --- Hardware Inserts (Phase 3C) ---

def test_hardware_rates_exist():
    """All four hardware types should be defined."""
    assert "pem_nut" in HARDWARE_RATES
    assert "pem_stud" in HARDWARE_RATES
    assert "rivnut" in HARDWARE_RATES
    assert "standoff" in HARDWARE_RATES


def test_cost_with_hardware_inserts():
    """Part with hardware inserts should cost more."""
    no_hw = calculate_sheet_metal_cost(
        material_name="Mild Steel CR", thickness_mm=2,
        part_length_mm=300, part_width_mm=200,
        cutting_length_mm=1000, pierce_count=5, quantity=100,
    )
    with_hw = calculate_sheet_metal_cost(
        material_name="Mild Steel CR", thickness_mm=2,
        part_length_mm=300, part_width_mm=200,
        cutting_length_mm=1000, pierce_count=5,
        hardware_items=[
            {"type": "pem_nut", "quantity": 4},
            {"type": "rivnut", "quantity": 2},
        ],
        quantity=100,
    )
    assert with_hw.hardware_cost > 0
    assert with_hw.unit_cost > no_hw.unit_cost
    assert no_hw.hardware_cost == 0


def test_hardware_cost_calculation():
    """Verify hardware cost math: 4 pem_nut (₹8 each + 0.3min) + 2 rivnut (₹6 each + 0.5min)."""
    result = calculate_sheet_metal_cost(
        material_name="Mild Steel CR", thickness_mm=2,
        part_length_mm=300, part_width_mm=200,
        cutting_length_mm=1000, pierce_count=5,
        hardware_items=[
            {"type": "pem_nut", "quantity": 4},
            {"type": "rivnut", "quantity": 2},
        ],
        quantity=1,
    )
    # Material: 4×8 + 2×6 = 44
    # Time: 4×0.3 + 2×0.5 = 2.2 min → (2.2/60) × 600 = 22
    # Total: 44 + 22 = 66
    assert abs(result.hardware_cost - 66.0) < 0.1


def test_hardware_in_line_items():
    """Hardware inserts should appear as a line item."""
    result = calculate_sheet_metal_cost(
        material_name="Mild Steel CR", thickness_mm=2,
        part_length_mm=300, part_width_mm=200,
        cutting_length_mm=1000, pierce_count=5,
        hardware_items=[{"type": "standoff", "quantity": 6}],
        quantity=100,
    )
    hw_lines = [l for l in result.lines if l.item == "Hardware Inserts"]
    assert len(hw_lines) == 1
    assert "6× standoff" in hw_lines[0].description


def test_unknown_hardware_type_ignored():
    """Unknown hardware types should be silently skipped."""
    result = calculate_sheet_metal_cost(
        material_name="Mild Steel CR", thickness_mm=2,
        part_length_mm=300, part_width_mm=200,
        cutting_length_mm=1000, pierce_count=5,
        hardware_items=[{"type": "unknown_widget", "quantity": 10}],
        quantity=100,
    )
    assert result.hardware_cost == 0


# --- Assembly ZIP extraction (Phase 3A) ---

_has_api_env = True
try:
    from api.routes.extract import _extract_single_file, _result_to_response
except (KeyError, ImportError):
    _has_api_env = False


@pytest.mark.skipif(not _has_api_env, reason="API env vars not set")
def test_extract_single_file_refactor():
    """Verify _extract_single_file is importable and callable."""
    assert callable(_extract_single_file)
    assert callable(_result_to_response)


@pytest.mark.skipif(not _has_api_env, reason="API env vars not set")
def test_result_to_response_basic():
    """_result_to_response should convert a dict to ExtractionResponse."""
    result = {
        "dimensions": {"od": 50, "length": 100},
        "material": "Mild Steel",
        "confidence": "high",
        "tolerances": {},
        "suggested_processes": ["turning"],
        "gdt_symbols": [],
        "notes": "Test",
    }
    resp = _result_to_response(result)
    assert resp.material == "Mild Steel"
    assert resp.confidence == "high"
    assert resp.material_confidence == "high"


@pytest.mark.skipif(not _has_api_env, reason="API env vars not set")
def test_result_to_response_no_material():
    """No material → material_confidence should be 'low'."""
    result = {"dimensions": {}, "confidence": "medium"}
    resp = _result_to_response(result)
    assert resp.material is None
    assert resp.material_confidence == "low"
