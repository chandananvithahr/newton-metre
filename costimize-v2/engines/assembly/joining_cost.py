"""Joining cost models for assembly estimates.

Covers permanent and temporary joining methods used in Indian job shops:
- Welding: MIG, TIG, Spot
- Mechanical fasteners: Bolting, Riveting
- Interference: Press Fit

Rates sourced from CMTI Machine Hour Rate Guide and Indian shop floor benchmarks.
"""
from dataclasses import dataclass

OVERHEAD_RATE = 0.15
PROFIT_RATE = 0.20

# Each entry: machine_rate_per_hr (₹), labour_rate_per_hr (₹),
#             time_per_joint_min, material_per_joint (₹)
JOINING_METHODS: dict[str, dict] = {
    "mig_welding": {
        "label": "MIG Welding",
        "machine_rate_per_hr": 800,
        "labour_rate_per_hr": 250,
        "time_per_joint_min": 3.0,
        "material_per_joint": 12.0,  # wire + shielding gas consumables
    },
    "tig_welding": {
        "label": "TIG Welding",
        "machine_rate_per_hr": 1200,
        "labour_rate_per_hr": 250,
        "time_per_joint_min": 5.0,
        "material_per_joint": 20.0,  # filler rod + argon
    },
    "spot_welding": {
        "label": "Spot Welding",
        "machine_rate_per_hr": 600,
        "labour_rate_per_hr": 250,
        "time_per_joint_min": 0.5,
        "material_per_joint": 0.0,
    },
    "bolting": {
        "label": "Bolting (Nut & Bolt)",
        "machine_rate_per_hr": 0,
        "labour_rate_per_hr": 250,
        "time_per_joint_min": 2.0,
        "material_per_joint": 18.0,  # bolt + nut + washer (M8 avg)
    },
    "riveting": {
        "label": "Riveting",
        "machine_rate_per_hr": 0,
        "labour_rate_per_hr": 250,
        "time_per_joint_min": 1.0,
        "material_per_joint": 8.0,
    },
    "press_fit": {
        "label": "Press Fit / Interference Fit",
        "machine_rate_per_hr": 500,
        "labour_rate_per_hr": 250,
        "time_per_joint_min": 10.0,
        "material_per_joint": 0.0,
    },
    "brazing_torch": {
        "label": "Torch Brazing",
        "machine_rate_per_hr": 300,
        "labour_rate_per_hr": 250,
        "time_per_joint_min": 4.0,
        "material_per_joint": 40.0,  # silver/copper filler rod + flux
    },
    "brazing_furnace": {
        "label": "Furnace Brazing",
        "machine_rate_per_hr": 800,
        "labour_rate_per_hr": 250,
        "time_per_joint_min": 8.0,
        "material_per_joint": 25.0,  # pre-placed filler, less waste
    },
    "laser_welding": {
        "label": "Laser Welding",
        "machine_rate_per_hr": 2500,
        "labour_rate_per_hr": 250,
        "time_per_joint_min": 1.5,
        "material_per_joint": 5.0,  # filler wire (optional)
    },
    "resistance_seam": {
        "label": "Resistance Seam Welding",
        "machine_rate_per_hr": 900,
        "labour_rate_per_hr": 250,
        "time_per_joint_min": 0.3,
        "material_per_joint": 2.0,  # electrode wear
    },
}


@dataclass(frozen=True)
class JoiningCostResult:
    method: str
    method_label: str
    num_joints: int
    material_cost: float
    machine_cost: float
    labour_cost: float
    total_joining_cost: float  # sum of above, before overhead/profit


def calculate_joining_cost(method: str, num_joints: int) -> JoiningCostResult:
    """Calculate joining cost for one assembly unit (all joints).

    Overhead and profit are applied at the assembly level, not here.
    """
    if method not in JOINING_METHODS:
        raise ValueError(
            f"Unknown joining method '{method}'. "
            f"Allowed: {', '.join(JOINING_METHODS)}"
        )
    if num_joints < 1:
        raise ValueError("num_joints must be at least 1.")

    p = JOINING_METHODS[method]
    time_hr = (p["time_per_joint_min"] * num_joints) / 60.0
    material_cost = round(p["material_per_joint"] * num_joints, 2)
    machine_cost = round(p["machine_rate_per_hr"] * time_hr, 2)
    labour_cost = round(p["labour_rate_per_hr"] * time_hr, 2)
    total = round(material_cost + machine_cost + labour_cost, 2)

    return JoiningCostResult(
        method=method,
        method_label=p["label"],
        num_joints=num_joints,
        material_cost=material_cost,
        machine_cost=machine_cost,
        labour_cost=labour_cost,
        total_joining_cost=total,
    )


def list_joining_methods() -> list[dict]:
    return [{"id": k, "label": v["label"]} for k, v in JOINING_METHODS.items()]
