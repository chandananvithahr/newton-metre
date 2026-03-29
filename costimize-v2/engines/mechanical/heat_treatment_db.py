"""Heat treatment process database — 15+ processes with Indian rates.

Weight-based costing (₹/kg) from Indian job shop rates.
Covers through-hardening, case-hardening, annealing, tempering, and specialty processes.
"""
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class HeatTreatment:
    name: str
    rate_per_kg: float              # ₹/kg (primary costing unit)
    min_batch_charge: float         # ₹ minimum per batch
    cycle_time_hr: tuple[float, float]  # typical min-max hours
    temperature_c: tuple[int, int]  # typical temp range °C
    applicable_materials: tuple[str, ...]
    mil_spec: str
    industry: str                   # "all", "defense", "aerospace", "auto"


HEAT_TREATMENTS: dict[str, HeatTreatment] = {
    # --- Through Hardening ---
    "through_hardening": HeatTreatment(
        "Through Hardening (Quench + Temper)", 25, 1500,
        (2, 6), (800, 870), ("steel",), "AMS 2759", "all",
    ),
    "tempering": HeatTreatment(
        "Tempering", 15, 800,
        (1, 4), (150, 650), ("steel",), "AMS 2759", "all",
    ),
    "annealing": HeatTreatment(
        "Annealing (Full)", 18, 1000,
        (3, 8), (750, 900), ("steel",), "", "all",
    ),
    "normalizing": HeatTreatment(
        "Normalizing", 18, 1000,
        (2, 4), (850, 920), ("steel",), "", "all",
    ),
    "stress_relief": HeatTreatment(
        "Stress Relieving", 15, 800,
        (1, 4), (550, 650), ("steel", "aluminum", "stainless"), "AMS 2759", "all",
    ),

    # --- Case Hardening ---
    "carburizing": HeatTreatment(
        "Carburizing (Gas)", 35, 2500,
        (4, 20), (870, 940), ("steel",),
        "AMS 2759/7", "defense+aerospace",
    ),
    "carbonitriding": HeatTreatment(
        "Carbonitriding", 30, 2000,
        (2, 6), (820, 870), ("steel",), "", "auto",
    ),
    "nitriding_gas": HeatTreatment(
        "Nitriding (Gas)", 45, 3000,
        (20, 70), (500, 570), ("steel",),
        "AMS 2759/10", "defense+aerospace",
    ),
    "nitriding_ion": HeatTreatment(
        "Nitriding (Ion/Plasma)", 55, 4000,
        (10, 40), (400, 580), ("steel", "stainless"),
        "AMS 2759/12", "defense+aerospace",
    ),
    "induction_hardening": HeatTreatment(
        "Induction Hardening", 20, 800,
        (0.01, 0.1), (850, 1000), ("steel",), "", "auto",
    ),

    # --- Aluminum/Ti Heat Treatment ---
    "solution_aging_al": HeatTreatment(
        "Solution Treatment + Aging (Al)", 30, 1500,
        (4, 12), (460, 540), ("aluminum",),
        "AMS 2770/2771", "aerospace",
    ),
    "solution_aging_ti": HeatTreatment(
        "Solution Treatment + Aging (Ti)", 80, 5000,
        (2, 8), (900, 1050), ("titanium",),
        "AMS 2801", "aerospace",
    ),
    "precipitation_hardening": HeatTreatment(
        "Precipitation Hardening (17-4PH, Inconel)", 50, 3000,
        (4, 8), (480, 620), ("stainless", "nickel_alloy"),
        "AMS 2759/3", "aerospace",
    ),

    # --- Specialty ---
    "cryogenic": HeatTreatment(
        "Cryogenic Treatment (-196°C)", 40, 2000,
        (24, 48), (-196, -196), ("steel",), "", "defense",
    ),
    "vacuum_hardening": HeatTreatment(
        "Vacuum Hardening", 60, 5000,
        (3, 8), (1000, 1100), ("steel", "stainless"),
        "AMS 2759/5", "aerospace",
    ),
}


def get_heat_treatment(process_id: str) -> HeatTreatment:
    if process_id not in HEAT_TREATMENTS:
        raise ValueError(
            f"Unknown heat treatment: {process_id}. "
            f"Available: {list(HEAT_TREATMENTS.keys())}"
        )
    return HEAT_TREATMENTS[process_id]


def list_heat_treatments(industry: str | None = None) -> list[str]:
    results = []
    for pid, ht in HEAT_TREATMENTS.items():
        if industry and industry not in ht.industry and ht.industry != "all":
            continue
        results.append(pid)
    return results


def calculate_heat_treatment_cost(
    process_id: str,
    part_weight_kg: float,
    quantity: int = 1,
) -> float:
    """Calculate heat treatment cost per unit in ₹.

    Primarily weight-based (₹/kg), with minimum batch charge.
    """
    ht = get_heat_treatment(process_id)
    base_cost = part_weight_kg * ht.rate_per_kg
    min_per_unit = ht.min_batch_charge / quantity
    return max(base_cost, min_per_unit)
