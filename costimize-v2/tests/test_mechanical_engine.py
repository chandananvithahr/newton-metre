"""Tests for the mechanical cost engine — physics-based MRR calculations."""
from engines.mechanical.cost_engine import (
    calculate_mechanical_cost,
    apply_gdt_surcharges,
    MechanicalCostBreakdown,
)
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

def test_milled_part_uses_rectangular_billet():
    """Prismatic part (width×height) must use rectangular billet, not circumscribed cylinder.

    Cylinder overestimates by ~27% vs billet for a 100×80mm part.
    Verify milled material_cost < cylindrical approximation would give.
    """
    import math
    milled = calculate_mechanical_cost(
        dimensions={"width_mm": 100, "height_mm": 80, "length_mm": 50},
        material_name="EN8 Steel",
        selected_processes=["milling_face"],
        quantity=10,
    )
    # Build what the OLD circumscribed-cylinder method would have given:
    # od_circumscribed = sqrt(100² + 80²) ≈ 128.06mm
    # volume = π × (128.06/2 + 5)² × (50+10) / 1e9
    od_circ = math.sqrt(100**2 + 80**2)
    from config import MACHINING_ALLOWANCE_DIA_MM, MACHINING_ALLOWANCE_LEN_MM, MATERIAL_WASTAGE_PCT
    from engines.mechanical.material_db import get_material
    mat = get_material("EN8 Steel")
    bar_od_m = (od_circ + MACHINING_ALLOWANCE_DIA_MM) / 1000
    bar_len_m = (50 + MACHINING_ALLOWANCE_LEN_MM) / 1000
    vol_cylinder = math.pi * (bar_od_m / 2) ** 2 * bar_len_m
    weight_cylinder = vol_cylinder * mat.density_kg_per_m3 * (1 + MATERIAL_WASTAGE_PCT / 100)
    old_material_cost = weight_cylinder * mat.price_per_kg_inr

    # New rectangular billet must be cheaper
    assert milled.material_cost < old_material_cost, (
        f"Billet cost {milled.material_cost:.2f} should be < cylinder cost {old_material_cost:.2f}"
    )
    # And the saving should be meaningful (at least 15%)
    saving_pct = (old_material_cost - milled.material_cost) / old_material_cost * 100
    assert saving_pct > 15, f"Expected >15% saving, got {saving_pct:.1f}%"


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


# ── GD&T surcharge tests ──────────────────────────────────────────────────────

class TestGdtSurcharges:
    DIMS = {"outer_diameter_mm": 50.0, "length_mm": 120.0}

    def test_no_gdt_no_change(self):
        cost, insp, procs = apply_gdt_surcharges(1000.0, [], ["turning"], 100)
        assert cost == 1000.0
        assert insp == 0.0
        assert procs == ["turning"]

    def test_single_symbol_applies_multiplier(self):
        # perpendicularity → multiplier 1.30
        cost, _, _ = apply_gdt_surcharges(1000.0, ["perpendicularity"], ["turning"], 100)
        assert abs(cost - 1300.0) < 0.01

    def test_max_multiplier_not_compounded(self):
        # circular_runout=1.35, perpendicularity=1.30 → max is 1.35, not 1.35*1.30
        cost, _, _ = apply_gdt_surcharges(1000.0, ["circular_runout", "perpendicularity"], ["turning"], 100)
        assert abs(cost - 1350.0) < 0.01

    def test_adds_implied_process(self):
        # perpendicularity implies grinding_surface
        _, _, procs = apply_gdt_surcharges(1000.0, ["perpendicularity"], ["turning"], 100)
        assert "grinding_surface" in procs

    def test_no_duplicate_process(self):
        # grinding_surface already in list — should not be added twice
        _, _, procs = apply_gdt_surcharges(1000.0, ["perpendicularity"], ["turning", "grinding_surface"], 100)
        assert procs.count("grinding_surface") == 1

    def test_inspection_amortized_over_quantity(self):
        # qty=100: sample=10, cost_per_unit = (inspection_cost * 10) / 100
        _, insp_100, _ = apply_gdt_surcharges(1000.0, ["true_position"], ["turning"], 100)
        _, insp_10, _ = apply_gdt_surcharges(1000.0, ["true_position"], ["turning"], 10)
        # true_position inspection_inr = 400
        # qty=100: sample=max(3,10)=10, per_unit = 400*10/100 = 40
        assert abs(insp_100 - 40.0) < 0.01
        # qty=10: sample=max(3,1)=3, per_unit = 400*3/10 = 120
        assert abs(insp_10 - 120.0) < 0.01

    def test_gdt_raises_full_cost(self):
        base = calculate_mechanical_cost(
            self.DIMS, "EN8 Steel", ["turning", "facing"], quantity=100
        )
        with_gdt = calculate_mechanical_cost(
            self.DIMS, "EN8 Steel", ["turning", "facing"], quantity=100,
            gdt_symbols=["circular_runout", "perpendicularity"],
        )
        # Cost must increase with GD&T
        assert with_gdt.unit_cost > base.unit_cost

    def test_gdt_increase_within_bounds(self):
        base = calculate_mechanical_cost(
            self.DIMS, "EN8 Steel", ["turning", "facing"], quantity=100
        )
        with_gdt = calculate_mechanical_cost(
            self.DIMS, "EN8 Steel", ["turning", "facing"], quantity=100,
            gdt_symbols=["circular_runout", "perpendicularity"],
        )
        pct_increase = (with_gdt.unit_cost / base.unit_cost - 1) * 100
        # For qty=100, typical GD&T surcharge: 10–60% increase
        assert 5 < pct_increase < 100

    def test_unknown_gdt_symbol_ignored(self):
        # Should not raise, just skip unknown symbols
        cost, insp, _ = apply_gdt_surcharges(1000.0, ["unknown_symbol"], ["turning"], 100)
        assert cost == 1000.0
        assert insp == 0.0

    def test_profile_of_surface_highest_multiplier(self):
        # profile_of_surface has the highest multiplier (1.60)
        cost, _, _ = apply_gdt_surcharges(1000.0, ["profile_of_surface"], ["milling_face"], 50)
        assert abs(cost - 1600.0) < 0.01


# ── GD&T + extraction pipeline integration ───────────────────────────────────

class TestGdtExtractorIntegration:
    def test_gdt_from_text_unicode_symbol(self):
        from extractors.cad_converter import _extract_gdt_from_texts
        result = _extract_gdt_from_texts(["perpendicularity 0.02 A"])
        assert "perpendicularity" in result

    def test_gdt_from_text_empty(self):
        from extractors.cad_converter import _extract_gdt_from_texts
        result = _extract_gdt_from_texts(["STEPPED SHAFT", "Material: EN8"])
        assert result == []

    def test_gdt_multiple_symbols(self):
        from extractors.cad_converter import _extract_gdt_from_texts
        result = _extract_gdt_from_texts([
            "runout tolerance 0.03",
            "flatness 0.01",
            "true position 0.05 A B",
        ])
        assert "circular_runout" in result
        assert "flatness" in result
        assert "true_position" in result

    def test_gdt_deduplication(self):
        from extractors.cad_converter import _extract_gdt_from_texts
        # Same symbol appears twice — should only appear once in output
        result = _extract_gdt_from_texts(["flatness 0.01", "flatness required per print"])
        assert result.count("flatness") == 1


# ── Edge case & correctness tests ───────────────────────────────────────────

class TestEdgeCases:
    """Stress-tests for edge cases, boundary conditions, and physics sanity."""

    def test_tiny_part_has_minimum_cycle_time(self):
        """A 6x10mm shaft must not compute sub-second machining time."""
        result = calculate_mechanical_cost(
            dimensions={"outer_diameter_mm": 6, "length_mm": 10},
            material_name="EN8 Steel",
            selected_processes=["turning"],
            quantity=100,
        )
        # MIN_CYCLE_TIME_MIN = 0.5 (30 seconds)
        assert result.process_lines[0].time_min >= 0.5
        assert result.unit_cost > 10  # must be at least a few rupees

    def test_zero_hole_count_drilling_skipped(self):
        """Drilling with hole_count=0 should not appear in process lines."""
        result = calculate_mechanical_cost(
            dimensions={"outer_diameter_mm": 60, "length_mm": 100, "hole_count": 0},
            material_name="EN8 Steel",
            selected_processes=["turning", "drilling"],
            quantity=100,
        )
        process_ids = [p.process_id for p in result.process_lines]
        assert "turning" in process_ids
        assert "drilling" not in process_ids

    def test_prismatic_error_message_not_od(self):
        """Prismatic with zero height should mention width/height, not OD."""
        import pytest
        with pytest.raises(ValueError, match="width.*height|Width.*Height|W=.*H="):
            calculate_mechanical_cost(
                dimensions={"width_mm": 100, "height_mm": 0, "length_mm": 50},
                material_name="EN8 Steel",
                selected_processes=["milling_face"],
                quantity=10,
            )

    def test_gdt_prismatic_remaps_to_surface_grinding(self):
        """Circularity on a milled part should add grinding_surface, not cylindrical."""
        _, _, procs = apply_gdt_surcharges(
            1000.0, ["circularity"], ["milling_face"], 100, is_prismatic=True,
        )
        assert "grinding_surface" in procs
        assert "grinding_cylindrical" not in procs

    def test_gdt_rotational_keeps_cylindrical_grinding(self):
        """Circularity on a turned part should add grinding_cylindrical."""
        _, _, procs = apply_gdt_surcharges(
            1000.0, ["circularity"], ["turning"], 100, is_prismatic=False,
        )
        assert "grinding_cylindrical" in procs

    def test_heat_treatment_minimum_45_min(self):
        """Even a tiny part needs minimum 45 min in furnace."""
        from engines.mechanical.process_db import estimate_process_time_min
        t = estimate_process_time_min(
            "heat_treatment", {"outer_diameter_mm": 10, "length_mm": 20},
        )
        assert t >= 45.0

    def test_heat_treatment_scales_with_section(self):
        """Larger cross-section needs longer soak time."""
        from engines.mechanical.process_db import estimate_process_time_min
        t_small = estimate_process_time_min(
            "heat_treatment", {"outer_diameter_mm": 25, "length_mm": 50},
        )
        t_large = estimate_process_time_min(
            "heat_treatment", {"outer_diameter_mm": 200, "length_mm": 500},
        )
        assert t_large > t_small * 2

    def test_drilling_through_hole_uses_full_depth(self):
        """Without explicit hole_depth, drilling should use min(height, length)."""
        from engines.mechanical.process_db import estimate_process_time_min
        # Plate: height=20, length=200 -> drill depth = min(20, 200) = 20mm
        t_plate = estimate_process_time_min("drilling", {
            "width_mm": 100, "height_mm": 20, "length_mm": 200,
            "hole_diameter_mm": 10, "hole_count": 1,
        }, material_name="EN8 Steel")
        # Same but explicit 20mm depth — should match closely
        t_explicit = estimate_process_time_min("drilling", {
            "width_mm": 100, "height_mm": 20, "length_mm": 200,
            "hole_diameter_mm": 10, "hole_count": 1, "hole_depth_mm": 20,
        }, material_name="EN8 Steel")
        assert abs(t_plate - t_explicit) < 0.01

    def test_quantity_1_setup_dominates(self):
        """At qty=1, setup cost should be >30% of unit cost."""
        result = calculate_mechanical_cost(
            dimensions={"outer_diameter_mm": 30, "length_mm": 50},
            material_name="Aluminum 6061",
            selected_processes=["turning", "drilling"],
            quantity=1,
        )
        setup_pct = result.total_setup_cost / result.unit_cost * 100
        assert setup_pct > 30, f"Setup only {setup_pct:.0f}% at qty=1"

    def test_cost_monotonic_with_size(self):
        """Larger part must cost more (same material, same process)."""
        small = calculate_mechanical_cost(
            dimensions={"outer_diameter_mm": 30, "length_mm": 50},
            material_name="EN8 Steel",
            selected_processes=["turning"],
            quantity=100,
        )
        large = calculate_mechanical_cost(
            dimensions={"outer_diameter_mm": 100, "length_mm": 300},
            material_name="EN8 Steel",
            selected_processes=["turning"],
            quantity=100,
        )
        assert large.unit_cost > small.unit_cost * 2
        assert large.material_cost > small.material_cost

    def test_cost_monotonic_with_material_hardness(self):
        """Harder material must cost more for same geometry."""
        al = calculate_mechanical_cost(
            dimensions={"outer_diameter_mm": 50, "length_mm": 80},
            material_name="Aluminum 6061",
            selected_processes=["turning"],
            quantity=100,
        )
        ss = calculate_mechanical_cost(
            dimensions={"outer_diameter_mm": 50, "length_mm": 80},
            material_name="Stainless Steel 304",
            selected_processes=["turning"],
            quantity=100,
        )
        ti = calculate_mechanical_cost(
            dimensions={"outer_diameter_mm": 50, "length_mm": 80},
            material_name="Titanium Grade 5",
            selected_processes=["turning"],
            quantity=100,
        )
        assert al.unit_cost < ss.unit_cost < ti.unit_cost

    def test_process_order_independence(self):
        """Same processes in different order should give same total cost."""
        procs_a = ["turning", "drilling", "facing"]
        procs_b = ["facing", "turning", "drilling"]
        dims = {"outer_diameter_mm": 60, "length_mm": 100}
        a = calculate_mechanical_cost(dims, "EN8 Steel", procs_a, quantity=50)
        b = calculate_mechanical_cost(dims, "EN8 Steel", procs_b, quantity=50)
        assert abs(a.unit_cost - b.unit_cost) < 0.01

    def test_all_15_materials_produce_valid_cost(self):
        """Every material in the database should produce a valid estimate."""
        from engines.mechanical.material_db import list_material_names
        for mat in list_material_names():
            result = calculate_mechanical_cost(
                dimensions={"outer_diameter_mm": 50, "length_mm": 80},
                material_name=mat,
                selected_processes=["turning"],
                quantity=100,
            )
            assert result.unit_cost > 0, f"{mat}: zero unit cost"
            assert result.material_cost > 0, f"{mat}: zero material cost"

    def test_all_25_processes_produce_valid_time(self):
        """Every machining process should produce > 0 time for reasonable dims."""
        from engines.mechanical.process_db import estimate_process_time_min, load_processes
        all_procs = load_processes()
        dims = {
            "outer_diameter_mm": 60, "inner_diameter_mm": 20,
            "length_mm": 100, "width_mm": 80, "height_mm": 30,
            "hole_diameter_mm": 10, "hole_count": 4,
            "thread_count": 2, "thread_length_mm": 20,
            "groove_count": 2, "surface_area_cm2": 200,
        }
        for pid in all_procs:
            t = estimate_process_time_min(pid, dims, material_name="EN8 Steel")
            assert t > 0, f"Process {pid} returned zero time"

    def test_milled_pocket_slower_than_face(self):
        """Pocket milling takes longer than face milling for same footprint."""
        from engines.mechanical.process_db import estimate_process_time_min
        dims = {"length_mm": 100, "width_mm": 50, "height_mm": 20}
        t_face = estimate_process_time_min("milling_face", dims, material_name="EN8 Steel")
        t_pocket = estimate_process_time_min("milling_pocket", dims, material_name="EN8 Steel")
        assert t_pocket > t_face

    def test_boring_requires_inner_diameter(self):
        """Boring with id_mm=0 should return minimum time, not crash."""
        from engines.mechanical.process_db import estimate_process_time_min
        t = estimate_process_time_min(
            "boring", {"outer_diameter_mm": 60, "length_mm": 100, "inner_diameter_mm": 0},
            material_name="EN8 Steel",
        )
        assert t > 0

    def test_unknown_process_in_cost_engine_skipped(self):
        """Unknown process ID should be silently skipped."""
        result = calculate_mechanical_cost(
            dimensions={"outer_diameter_mm": 60, "length_mm": 100},
            material_name="EN8 Steel",
            selected_processes=["turning", "fantasy_process", "drilling"],
            quantity=100,
        )
        process_ids = [p.process_id for p in result.process_lines]
        assert "fantasy_process" not in process_ids
        assert "turning" in process_ids

    def test_inner_diameter_larger_than_outer_raises(self):
        """Bore larger than OD should raise ValueError."""
        import pytest
        with pytest.raises(ValueError, match="Inner diameter"):
            calculate_mechanical_cost(
                dimensions={"outer_diameter_mm": 30, "inner_diameter_mm": 50, "length_mm": 100},
                material_name="EN8 Steel",
                selected_processes=["turning"],
                quantity=100,
            )

    def test_prismatic_material_cheaper_than_cylindrical_equivalent(self):
        """Rectangular billet must be cheaper than circumscribed cylinder."""
        import math
        r = calculate_mechanical_cost(
            dimensions={"width_mm": 100, "height_mm": 50, "length_mm": 80},
            material_name="EN8 Steel",
            selected_processes=["milling_face"],
            quantity=100,
        )
        # Cylinder that circumscribes 100x50 = od=111.8mm
        od_circ = math.sqrt(100**2 + 50**2)
        r_cyl = calculate_mechanical_cost(
            dimensions={"outer_diameter_mm": od_circ, "length_mm": 80},
            material_name="EN8 Steel",
            selected_processes=["milling_face"],
            quantity=100,
        )
        assert r.material_cost < r_cyl.material_cost
