"""Tests for the mechanical cost engine — physics-based MRR calculations."""
from engines.mechanical.cost_engine import calculate_mechanical_cost, MechanicalCostBreakdown
from engines.mechanical.material_db import get_material, list_material_names
from engines.mechanical.process_db import estimate_process_time_min, load_processes
from engines.mechanical.cutting_data import (
    get_cutting_data,
    calculate_tool_life_min,
    calculate_tool_cost_per_min,
    calculate_sandvik_power_kw,
    CUTTING_DATA,
    TOOL_LIFE_CORRECTION,
)


# --- Material DB tests (unchanged) ---

def test_load_materials():
    names = list_material_names()
    assert len(names) >= 6
    assert "EN8 Steel" in names


def test_get_material_returns_correct_data():
    mat = get_material("EN8 Steel")
    assert mat.price_per_kg_inr == 75
    assert mat.density_kg_per_m3 == 7850


# --- Process DB tests ---

def test_load_processes():
    procs = load_processes()
    assert "turning" in procs
    assert "drilling" in procs
    assert procs["turning"].machine_rate == 800


def test_estimate_turning_time():
    """Turning 60mm OD × 100mm length in EN8-like material → 1-5 min."""
    dims = {"outer_diameter_mm": 60, "length_mm": 100}
    time_min = estimate_process_time_min("turning", dims, machinability=0.55)
    assert time_min > 0
    assert 0.5 < time_min < 8.0  # physics-based gives tighter range


def test_estimate_turning_with_material_name():
    """Using exact material name gives physics-based time."""
    dims = {"outer_diameter_mm": 60, "length_mm": 100}
    time_en8 = estimate_process_time_min("turning", dims, material_name="EN8 Steel")
    time_al = estimate_process_time_min("turning", dims, material_name="Aluminum 6061")
    time_ti = estimate_process_time_min("turning", dims, material_name="Titanium Grade 5")
    # Aluminum should be fastest, titanium slowest
    assert time_al < time_en8 < time_ti


def test_estimate_drilling_time_scales_with_hole_count():
    dims1 = {"hole_diameter_mm": 8, "length_mm": 50, "hole_count": 1}
    dims4 = {"hole_diameter_mm": 8, "length_mm": 50, "hole_count": 4}
    t1 = estimate_process_time_min("drilling", dims1, machinability=0.6)
    t4 = estimate_process_time_min("drilling", dims4, machinability=0.6)
    # 4 holes should take ~4x the time of 1 hole
    assert 3.5 < (t4 / t1) < 4.5


def test_estimate_milling_pocket_slower_than_face():
    """Pocket milling takes longer than face milling for same area."""
    dims = {"length_mm": 100, "width_mm": 50, "height_mm": 20}
    t_face = estimate_process_time_min("milling_face", dims, material_name="EN8 Steel")
    t_pocket = estimate_process_time_min("milling_pocket", dims, material_name="EN8 Steel")
    assert t_pocket > t_face


# --- Cutting data tests ---

def test_cutting_data_all_materials_present():
    """Every material in materials.json should have cutting data."""
    names = list_material_names()
    for name in names:
        cd = get_cutting_data(name)
        assert cd.turning.vc_rough > 0
        assert cd.kp > 0


def test_cutting_data_fallback_from_machinability():
    """Unknown material falls back to machinability-scaled data."""
    cd = get_cutting_data(material_name=None, machinability=0.8)
    assert cd.turning.vc_rough > 0
    # Higher machinability → higher cutting speed
    cd_low = get_cutting_data(material_name=None, machinability=0.3)
    assert cd.turning.vc_rough > cd_low.turning.vc_rough


def test_taylor_tool_life():
    """Taylor: T = (C/V)^(1/n). EN8 at 150 m/min should give 20-100 min."""
    en8 = CUTTING_DATA["EN8 Steel"]
    tool_life = calculate_tool_life_min(
        vc=en8.turning.vc_rough,
        taylor_n=en8.taylor_n,
        taylor_c=en8.taylor_c,
    )
    assert 10 < tool_life < 200


def test_tool_cost_per_min_positive():
    en8 = CUTTING_DATA["EN8 Steel"]
    cost = calculate_tool_cost_per_min(
        vc=en8.turning.vc_rough,
        taylor_n=en8.taylor_n,
        taylor_c=en8.taylor_c,
    )
    assert cost > 0
    assert cost < 5.0  # should be well under ₹5/min


# --- Cost engine integration tests ---

def test_calculate_mechanical_cost_basic():
    result = calculate_mechanical_cost(
        dimensions={"outer_diameter_mm": 60, "length_mm": 100},
        material_name="EN8 Steel",
        selected_processes=["turning", "facing", "drilling"],
        quantity=100,
    )
    assert isinstance(result, MechanicalCostBreakdown)
    assert result.quantity == 100
    assert result.material_cost > 0
    assert len(result.process_lines) == 3
    assert result.unit_cost > 0
    assert result.order_cost == round(result.unit_cost * 100, 2)


def test_tight_tolerance_increases_cost():
    base = calculate_mechanical_cost(
        dimensions={"outer_diameter_mm": 60, "length_mm": 100},
        material_name="EN8 Steel",
        selected_processes=["turning"],
        quantity=100,
        has_tight_tolerances=False,
    )
    tight = calculate_mechanical_cost(
        dimensions={"outer_diameter_mm": 60, "length_mm": 100},
        material_name="EN8 Steel",
        selected_processes=["turning"],
        quantity=100,
        has_tight_tolerances=True,
    )
    assert tight.total_machining_cost > base.total_machining_cost


def test_higher_quantity_reduces_setup_cost_per_unit():
    q10 = calculate_mechanical_cost(
        dimensions={"outer_diameter_mm": 60, "length_mm": 100},
        material_name="EN8 Steel",
        selected_processes=["turning"],
        quantity=10,
    )
    q1000 = calculate_mechanical_cost(
        dimensions={"outer_diameter_mm": 60, "length_mm": 100},
        material_name="EN8 Steel",
        selected_processes=["turning"],
        quantity=1000,
    )
    assert q10.total_setup_cost > q1000.total_setup_cost


def test_tooling_cost_from_taylor():
    """Tooling cost should be physics-based (not flat rate) for machining."""
    result = calculate_mechanical_cost(
        dimensions={"outer_diameter_mm": 60, "length_mm": 100},
        material_name="EN8 Steel",
        selected_processes=["turning"],
        quantity=100,
    )
    turning_line = result.process_lines[0]
    assert turning_line.tooling_cost > 0
    # Should be proportional to cutting time, not a flat number
    assert turning_line.tooling_cost < 5.0  # well under old flat ₹8


def test_sandvik_power_formula():
    """Sandvik power: Pc = (vc * ap * fn * kc) / (60 * 10^3)."""
    # EN8 Steel: kc1=1700, turning at vc=150, ap=2, fn=0.25
    power = calculate_sandvik_power_kw(
        vc=150, ap=2.0, fn=0.25, kc1=1700, mc=0.25,
    )
    assert 1.0 < power < 20.0  # reasonable range for a lathe cut


def test_sandvik_kc1_values_present():
    """All materials should have Sandvik kc1 values."""
    for name, data in CUTTING_DATA.items():
        assert data.kc1 > 0, f"{name} missing kc1"
        assert data.mc > 0, f"{name} missing mc"


def test_tool_life_correction_factors():
    """Sandvik tool life correction table should be monotonically decreasing."""
    factors = [TOOL_LIFE_CORRECTION[t] for t in sorted(TOOL_LIFE_CORRECTION)]
    for i in range(1, len(factors)):
        assert factors[i] <= factors[i - 1]


def test_harder_material_costs_more():
    """Titanium should cost significantly more than mild steel for same part."""
    ms = calculate_mechanical_cost(
        dimensions={"outer_diameter_mm": 60, "length_mm": 100},
        material_name="Mild Steel IS2062",
        selected_processes=["turning", "drilling"],
        quantity=100,
    )
    ti = calculate_mechanical_cost(
        dimensions={"outer_diameter_mm": 60, "length_mm": 100},
        material_name="Titanium Grade 5",
        selected_processes=["turning", "drilling"],
        quantity=100,
    )
    # Titanium: higher material cost + slower machining + more tool wear
    assert ti.unit_cost > ms.unit_cost * 2
