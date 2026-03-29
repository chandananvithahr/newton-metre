"""Laser cutting speed database and time estimation.

Data from Sandvik, LaserSpecHub, OEM compiled data.
Reference machine: 3kW fiber laser (most common in Indian job shops).
"""
import math
from dataclasses import dataclass


# Laser cutting speeds at 3kW fiber laser (m/min)
# Keys: material group → thickness_mm → speed_m_per_min
LASER_SPEEDS_3KW: dict[str, dict[float, float]] = {
    "mild_steel": {
        1: 35, 2: 20, 3: 10, 5: 5, 8: 2.5, 10: 1.8, 12: 1.2, 15: 0.8, 20: 0.4,
    },
    "stainless_steel": {
        1: 28, 2: 16, 3: 8, 5: 4, 8: 2, 10: 1.5, 12: 1.0, 15: 0.6,
    },
    "aluminum": {
        1: 25, 2: 13, 3: 7, 5: 3.5, 8: 1.8, 10: 1.2, 12: 0.8,
    },
    "galvanized_steel": {
        1: 33, 2: 18, 3: 9, 5: 4.5, 8: 2.3, 10: 1.6, 12: 1.1,
    },
    "copper": {1: 15, 2: 8, 3: 4, 5: 2},
    "brass": {1: 18, 2: 10, 3: 5, 5: 2.5, 8: 1.2},
}

# Map full material names → speed table keys
_MATERIAL_TO_GROUP: dict[str, str] = {
    "Mild Steel CR": "mild_steel",
    "Mild Steel HR": "mild_steel",
    "Stainless Steel 304": "stainless_steel",
    "Stainless Steel 316": "stainless_steel",
    "Aluminum 5052": "aluminum",
    "Aluminum 6061": "aluminum",
    "Galvanized Steel": "galvanized_steel",
    "Copper": "copper",
    "Brass": "brass",
}

# Pierce times at 3kW (seconds) by thickness
_PIERCE_TIMES_3KW: dict[float, float] = {
    1: 0.3, 2: 0.5, 3: 0.8, 5: 1.5, 8: 3.0, 10: 5.0, 12: 8.0, 15: 12.0,
}

# Stainless steel pierce time multiplier
_SS_PIERCE_MULT = 1.5
_AL_PIERCE_MULT = 1.2

# Machine rates (₹/hr)
LASER_MACHINE_RATE = 2500       # 3kW fiber laser (Indian average)
LASER_GAS_COST_PER_HR = 150    # N2 average
LASER_POWER_KW = 12            # total power draw including chiller


def get_laser_speed_m_per_min(
    material_name: str, thickness_mm: float,
) -> float:
    """Look up cutting speed, interpolating between known thicknesses.

    Returns speed in m/min. Raises ValueError if material or thickness
    is outside the data range.
    """
    group = _MATERIAL_TO_GROUP.get(material_name)
    if group is None:
        raise ValueError(f"No laser cutting data for {material_name}")

    speeds = LASER_SPEEDS_3KW[group]
    thicknesses = sorted(speeds.keys())

    if thickness_mm <= 0:
        raise ValueError("Thickness must be positive")

    # Exact match
    if thickness_mm in speeds:
        return speeds[thickness_mm]

    # Clamp to range
    if thickness_mm < thicknesses[0]:
        return speeds[thicknesses[0]]
    if thickness_mm > thicknesses[-1]:
        raise ValueError(
            f"Thickness {thickness_mm}mm exceeds max {thicknesses[-1]}mm "
            f"for {material_name} at 3kW"
        )

    # Linear interpolation between two nearest thicknesses
    for i in range(len(thicknesses) - 1):
        t_lo, t_hi = thicknesses[i], thicknesses[i + 1]
        if t_lo <= thickness_mm <= t_hi:
            v_lo, v_hi = speeds[t_lo], speeds[t_hi]
            frac = (thickness_mm - t_lo) / (t_hi - t_lo)
            return v_lo + frac * (v_hi - v_lo)

    return speeds[thicknesses[-1]]  # fallback


def get_pierce_time_sec(material_name: str, thickness_mm: float) -> float:
    """Pierce time in seconds for a single pierce point."""
    thicknesses = sorted(_PIERCE_TIMES_3KW.keys())

    # Find nearest
    if thickness_mm <= thicknesses[0]:
        base = _PIERCE_TIMES_3KW[thicknesses[0]]
    elif thickness_mm >= thicknesses[-1]:
        base = _PIERCE_TIMES_3KW[thicknesses[-1]]
    elif thickness_mm in _PIERCE_TIMES_3KW:
        base = _PIERCE_TIMES_3KW[thickness_mm]
    else:
        # Interpolate
        for i in range(len(thicknesses) - 1):
            t_lo, t_hi = thicknesses[i], thicknesses[i + 1]
            if t_lo <= thickness_mm <= t_hi:
                v_lo, v_hi = _PIERCE_TIMES_3KW[t_lo], _PIERCE_TIMES_3KW[t_hi]
                frac = (thickness_mm - t_lo) / (t_hi - t_lo)
                base = v_lo + frac * (v_hi - v_lo)
                break
        else:
            base = 1.0

    # Material multiplier
    group = _MATERIAL_TO_GROUP.get(material_name, "mild_steel")
    if group == "stainless_steel":
        return base * _SS_PIERCE_MULT
    if group == "aluminum":
        return base * _AL_PIERCE_MULT
    return base


def estimate_laser_cutting_time_min(
    material_name: str,
    thickness_mm: float,
    cutting_length_mm: float,
    pierce_count: int,
) -> float:
    """Total laser cutting time in minutes.

    Includes cutting traverse + pierce times + non-productive time (15%).
    """
    speed_m_min = get_laser_speed_m_per_min(material_name, thickness_mm)
    cutting_length_m = cutting_length_mm / 1000

    cut_time_min = cutting_length_m / speed_m_min
    pierce_time_min = (pierce_count * get_pierce_time_sec(material_name, thickness_mm)) / 60

    # 15% non-productive: head positioning, acceleration/deceleration
    return (cut_time_min + pierce_time_min) * 1.15


def estimate_laser_cutting_cost(
    material_name: str,
    thickness_mm: float,
    cutting_length_mm: float,
    pierce_count: int,
) -> float:
    """Laser cutting cost in ₹ for a single part."""
    time_min = estimate_laser_cutting_time_min(
        material_name, thickness_mm, cutting_length_mm, pierce_count,
    )
    time_hr = time_min / 60
    machine_cost = time_hr * LASER_MACHINE_RATE
    gas_cost = time_hr * LASER_GAS_COST_PER_HR
    return machine_cost + gas_cost
