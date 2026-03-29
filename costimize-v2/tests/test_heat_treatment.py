"""Tests for the heat treatment process database."""
import pytest
from engines.mechanical.heat_treatment_db import (
    get_heat_treatment,
    list_heat_treatments,
    calculate_heat_treatment_cost,
    HEAT_TREATMENTS,
)


def test_treatment_count():
    assert len(HEAT_TREATMENTS) >= 15


def test_all_have_positive_rates():
    for pid, ht in HEAT_TREATMENTS.items():
        assert ht.rate_per_kg > 0, f"{pid} has zero rate"
        assert ht.min_batch_charge > 0, f"{pid} has zero min charge"


def test_get_known_treatment():
    ht = get_heat_treatment("through_hardening")
    assert ht.rate_per_kg == 25
    assert "steel" in ht.applicable_materials


def test_get_unknown_raises():
    with pytest.raises(ValueError):
        get_heat_treatment("magic_heat")


def test_list_all():
    all_ht = list_heat_treatments()
    assert len(all_ht) >= 15


def test_list_by_industry():
    defense = list_heat_treatments(industry="defense")
    assert "cryogenic" in defense

    aerospace = list_heat_treatments(industry="aerospace")
    assert "vacuum_hardening" in aerospace
    assert "solution_aging_ti" in aerospace


def test_cost_basic():
    """2kg part, through hardening at ₹25/kg = ₹50."""
    cost = calculate_heat_treatment_cost("through_hardening", 2.0, quantity=100)
    assert cost == 50.0


def test_cost_min_batch():
    """Light part (0.1kg) → ₹2.5, but min charge ₹1500 for qty=1."""
    cost = calculate_heat_treatment_cost("through_hardening", 0.1, quantity=1)
    assert cost == 1500


def test_nitriding_more_expensive():
    """Nitriding should cost more per kg than simple tempering."""
    temper = calculate_heat_treatment_cost("tempering", 5.0, quantity=100)
    nitride = calculate_heat_treatment_cost("nitriding_gas", 5.0, quantity=100)
    assert nitride > temper * 2


def test_vacuum_hardening_premium():
    """Vacuum hardening should be most expensive standard process."""
    vacuum = calculate_heat_treatment_cost("vacuum_hardening", 5.0, quantity=100)
    through = calculate_heat_treatment_cost("through_hardening", 5.0, quantity=100)
    assert vacuum > through * 2


def test_induction_hardening_cheap():
    """Induction is fast and cheap per kg."""
    induction = calculate_heat_treatment_cost("induction_hardening", 5.0, quantity=100)
    carburize = calculate_heat_treatment_cost("carburizing", 5.0, quantity=100)
    assert induction < carburize


def test_quantity_amortizes_min_charge():
    q1 = calculate_heat_treatment_cost("carburizing", 0.5, quantity=1)
    q100 = calculate_heat_treatment_cost("carburizing", 0.5, quantity=100)
    assert q1 > q100  # min charge dominates at qty=1
