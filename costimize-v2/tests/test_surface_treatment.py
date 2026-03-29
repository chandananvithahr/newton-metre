"""Tests for the expanded surface treatment database — 40+ processes."""
import pytest
from engines.mechanical.surface_treatment_db import (
    get_surface_treatment,
    list_surface_treatments,
    estimate_surface_area_sq_dm,
    calculate_surface_treatment_cost,
    SURFACE_TREATMENTS,
    SurfaceTreatment,
)


def test_all_treatments_have_positive_rates():
    for pid, st in SURFACE_TREATMENTS.items():
        assert st.rate_per_sq_dm > 0, f"{pid} has zero rate"
        assert st.min_batch_charge > 0, f"{pid} has zero min charge"


def test_treatment_count():
    """Should have 40+ surface treatments."""
    assert len(SURFACE_TREATMENTS) >= 40


def test_get_known_treatment():
    st = get_surface_treatment("zinc_clear")
    assert st.name == "Zinc Plating (Clear)"
    assert st.rate_per_sq_dm == 5
    assert st.category == "electroplating"


def test_get_unknown_raises():
    with pytest.raises(ValueError):
        get_surface_treatment("unicorn_coating")


def test_list_all():
    all_treatments = list_surface_treatments()
    assert len(all_treatments) >= 40


def test_list_by_category():
    plating = list_surface_treatments(category="electroplating")
    assert "zinc_clear" in plating
    assert "anodize_type_ii_clear" not in plating

    anodizing = list_surface_treatments(category="anodizing")
    assert "anodize_type_ii_clear" in anodizing
    assert len(anodizing) >= 4


def test_list_by_industry():
    defense = list_surface_treatments(industry="defense")
    assert "cadmium" in defense
    assert "carc" in defense

    aerospace = list_surface_treatments(industry="aerospace")
    assert "anodize_type_i" in aerospace
    assert "hvof" in aerospace


def test_surface_area_cylinder():
    """50mm OD × 100mm length cylinder."""
    area = estimate_surface_area_sq_dm(od_mm=50, length_mm=100, complexity_factor=1.0)
    # pi * 50 * 100 + 2 * pi * 25^2 = 15708 + 3927 = 19635 mm² ≈ 1.96 sq.dm
    assert 1.5 < area < 2.5


def test_surface_area_rectangular():
    """200×100×50mm box."""
    area = estimate_surface_area_sq_dm(
        length_mm=200, width_mm=100, height_mm=50, complexity_factor=1.0,
    )
    # 2*(200*100 + 200*50 + 100*50) = 2*(20000+10000+5000) = 70000 mm² = 7.0 sq.dm
    assert 6.5 < area < 7.5


def test_surface_area_with_complexity():
    base = estimate_surface_area_sq_dm(od_mm=50, length_mm=100, complexity_factor=1.0)
    complex_ = estimate_surface_area_sq_dm(od_mm=50, length_mm=100, complexity_factor=1.5)
    assert complex_ == pytest.approx(base * 1.5, rel=0.01)


def test_cost_basic():
    cost = calculate_surface_treatment_cost("zinc_clear", surface_area_sq_dm=5.0, quantity=100)
    assert cost > 0
    assert cost == 5.0 * 5  # 5 sq.dm × ₹5/sq.dm = ₹25


def test_cost_min_batch_charge():
    """Single piece should hit minimum batch charge."""
    cost = calculate_surface_treatment_cost("nickel_electroless", surface_area_sq_dm=1.0, quantity=1)
    # 1 sq.dm × ₹18 = ₹18, but min charge is ₹3000
    assert cost == 3000


def test_cost_scales_with_area():
    cost_small = calculate_surface_treatment_cost("chrome_hard", surface_area_sq_dm=2.0, quantity=100)
    cost_large = calculate_surface_treatment_cost("chrome_hard", surface_area_sq_dm=10.0, quantity=100)
    assert cost_large > cost_small * 3


def test_he_baking_adds_cost():
    """High-strength steel + electroplating should add baking cost."""
    no_bake = calculate_surface_treatment_cost(
        "zinc_clear", surface_area_sq_dm=5.0, quantity=100,
        part_weight_kg=2.0, is_high_strength_steel=False,
    )
    with_bake = calculate_surface_treatment_cost(
        "zinc_clear", surface_area_sq_dm=5.0, quantity=100,
        part_weight_kg=2.0, is_high_strength_steel=True,
    )
    assert with_bake > no_bake
    assert with_bake - no_bake == pytest.approx(2.0 * 15, rel=0.01)  # 2kg × ₹15/kg


def test_anodizing_no_he_baking():
    """Anodizing should NOT add H.E. baking even for high-strength parts."""
    cost = calculate_surface_treatment_cost(
        "anodize_type_ii_clear", surface_area_sq_dm=5.0, quantity=100,
        part_weight_kg=2.0, is_high_strength_steel=True,
    )
    base = 5.0 * 8  # 5 sq.dm × ₹8/sq.dm
    assert cost == base  # no baking added


def test_masking_surcharge():
    base = calculate_surface_treatment_cost("chrome_hard", surface_area_sq_dm=5.0, quantity=100)
    masked = calculate_surface_treatment_cost(
        "chrome_hard", surface_area_sq_dm=5.0, quantity=100, masking_pct=50,
    )
    assert masked > base


def test_expensive_treatments_cost_more():
    """Gold plating should cost more than zinc plating for same area."""
    zinc = calculate_surface_treatment_cost("zinc_clear", surface_area_sq_dm=5.0, quantity=100)
    gold = calculate_surface_treatment_cost("gold", surface_area_sq_dm=5.0, quantity=100)
    assert gold > zinc * 10


def test_defense_processes_exist():
    """Defense-critical processes must be present."""
    for pid in ["cadmium", "phosphate_manganese", "black_oxide_hot", "carc", "passivation_nitric"]:
        st = get_surface_treatment(pid)
        assert "defense" in st.industry or st.industry == "all"


def test_aerospace_processes_exist():
    for pid in ["anodize_type_i", "chromate_conversion", "hvof", "pvd", "electropolishing"]:
        st = get_surface_treatment(pid)
        assert "aerospace" in st.industry or st.industry == "all"
