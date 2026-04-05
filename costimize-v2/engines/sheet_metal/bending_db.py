"""Press brake bending calculations — tonnage, time, and cost.

Formulas from The Fabricator, Sandvik, and Indian job shop data.
"""
import math
from dataclasses import dataclass


# Minimum bend radius as multiplier of thickness (R_min = factor × T)
# Source: Machinery's Handbook + Indian shop data
MIN_BEND_RADIUS_FACTOR: dict[str, float] = {
    "Mild Steel CR":       0.8,
    "Mild Steel HR":       0.8,
    "Stainless Steel 304": 1.0,
    "Stainless Steel 316": 1.0,
    "Aluminum 5052":       0.5,
    "Aluminum 6061":       0.5,
    "Galvanized Steel":    0.8,
    "Copper":              0.3,
    "Brass":               0.3,
}

# Springback angle correction (degrees to overbend)
# Applied to compensate elastic recovery after bending
SPRINGBACK_DEG: dict[str, float] = {
    "Mild Steel CR":       2.0,
    "Mild Steel HR":       2.0,
    "Stainless Steel 304": 3.0,
    "Stainless Steel 316": 3.0,
    "Aluminum 5052":       1.0,
    "Aluminum 6061":       1.5,
    "Galvanized Steel":    2.0,
    "Copper":              0.5,
    "Brass":               0.5,
}

# Surcharge when requested radius is below minimum
BELOW_MIN_RADIUS_SURCHARGE = 0.20  # 20%


def get_min_bend_radius_mm(material_name: str, thickness_mm: float) -> float:
    """Minimum inside bend radius in mm for a given material and thickness."""
    factor = MIN_BEND_RADIUS_FACTOR.get(material_name, 0.8)  # default = mild steel
    return factor * thickness_mm


def get_springback_deg(material_name: str) -> float:
    """Springback angle correction in degrees."""
    return SPRINGBACK_DEG.get(material_name, 2.0)


def check_bend_radius(
    material_name: str,
    thickness_mm: float,
    requested_radius_mm: float | None,
) -> tuple[bool, float]:
    """Check if requested bend radius meets minimum.

    Returns (is_below_minimum, surcharge_multiplier).
    surcharge_multiplier is 1.0 if OK, 1.0 + BELOW_MIN_RADIUS_SURCHARGE if below minimum.
    If requested_radius_mm is None, assumes standard radius (no surcharge).
    """
    if requested_radius_mm is None:
        return False, 1.0
    min_r = get_min_bend_radius_mm(material_name, thickness_mm)
    if requested_radius_mm < min_r:
        return True, 1.0 + BELOW_MIN_RADIUS_SURCHARGE
    return False, 1.0


# Die opening rule of thumb: V = 8 × T
_DIE_OPENING_FACTOR = 8

# Time per bend (seconds) by complexity
BEND_TIMES_SEC: dict[str, float] = {
    "simple": 10,       # single straight 90-degree bend
    "standard": 12,     # 2-3 bends, same tool
    "complex": 25,      # tool change needed
    "hemming": 20,      # two-step: acute + close
    "z_bend": 32,       # requires repositioning
}

# Setup times (minutes)
BEND_SETUP_FIRST_MIN = 20      # first setup (tool install)
BEND_TOOL_CHANGE_MIN = 8       # per additional tool change

# Machine rates (₹/hr) by tonnage
PRESS_BRAKE_RATES: dict[str, float] = {
    "small":  600,      # manual ≤50T
    "medium": 900,      # CNC 50-100T
    "large":  1200,     # CNC 100-250T
    "heavy":  1800,     # CNC 250-600T
}


def calculate_bending_tonnage(
    uts_mpa: float,
    thickness_mm: float,
    bend_length_mm: float,
    die_opening_mm: float | None = None,
) -> float:
    """Bending force in metric tons (kN / 9.81).

    Formula: F(kN) = (UTS × T² × L) / (V × 1000)
    where UTS in N/mm², T in mm, L in mm, V in mm.
    """
    if die_opening_mm is None:
        die_opening_mm = _DIE_OPENING_FACTOR * thickness_mm

    force_kn = (uts_mpa * thickness_mm ** 2 * bend_length_mm) / (die_opening_mm * 1000)
    return force_kn / 9.81  # convert kN to metric tons


def select_press_brake_size(tonnage: float) -> str:
    """Select press brake size category based on required tonnage."""
    if tonnage <= 50:
        return "small"
    if tonnage <= 100:
        return "medium"
    if tonnage <= 250:
        return "large"
    return "heavy"


def estimate_bending_time_min(
    n_bends: int,
    n_tool_changes: int = 0,
    bend_complexity: str = "simple",
) -> float:
    """Total bending time in minutes (setup + cycle).

    Does NOT include setup — that is amortized separately.
    """
    time_per_bend_sec = BEND_TIMES_SEC.get(bend_complexity, BEND_TIMES_SEC["simple"])
    cycle_time_min = (n_bends * time_per_bend_sec) / 60
    tool_change_min = n_tool_changes * BEND_TOOL_CHANGE_MIN
    return cycle_time_min + tool_change_min


def estimate_bending_cost(
    uts_mpa: float,
    thickness_mm: float,
    bend_length_mm: float,
    n_bends: int,
    n_tool_changes: int = 0,
    bend_complexity: str = "simple",
    quantity: int = 1,
) -> tuple[float, float]:
    """Bending cost per unit in ₹.

    Returns (cycle_cost_per_unit, setup_cost_per_unit).
    """
    tonnage = calculate_bending_tonnage(uts_mpa, thickness_mm, bend_length_mm)
    size = select_press_brake_size(tonnage)
    rate = PRESS_BRAKE_RATES[size]

    cycle_time_min = estimate_bending_time_min(n_bends, n_tool_changes, bend_complexity)
    cycle_cost = (cycle_time_min / 60) * rate

    setup_time_min = BEND_SETUP_FIRST_MIN + n_tool_changes * BEND_TOOL_CHANGE_MIN
    setup_cost_per_unit = ((setup_time_min / 60) * rate) / quantity

    return cycle_cost, setup_cost_per_unit


def calculate_bend_allowance(
    angle_deg: float, radius_mm: float, thickness_mm: float, k_factor: float,
) -> float:
    """Bend allowance in mm.

    BA = angle_rad × (R + K × T)
    """
    angle_rad = math.radians(angle_deg)
    return angle_rad * (radius_mm + k_factor * thickness_mm)
