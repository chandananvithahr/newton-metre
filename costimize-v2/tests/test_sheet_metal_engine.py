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
)
from engines.sheet_metal.cost_engine import (
    calculate_sheet_metal_cost, SheetMetalCostBreakdown,
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
