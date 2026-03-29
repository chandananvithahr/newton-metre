"""Process database — physics-based time estimation for manufacturing processes.

Uses Material Removal Rate (MRR) calculations with real cutting parameters
from Machinery's Handbook, Walter drilling handbook, and CNC Fundamentals.

Key formulas:
  Turning MRR:  Vc × 1000 × f × ap  (mm³/min)
  Milling MRR:  ae × ap × Vf         (mm³/min)  where Vf = fz × z × n
  Drilling time: depth / (f × n)      (min)      where n = Vc×1000 / (π×d)
  Tapping time:  2 × depth / (pitch × n) (min)   (in + out stroke)
  Power:         Kp × MRR             (kW)
  Tool life:     V × T^n = C          (Taylor equation)
"""
import json
import math
from pathlib import Path
from dataclasses import dataclass
from config import MACHINE_RATES, SETUP_TIMES, POWER_CONSUMPTION, TOOLING_COST_PER_UNIT
from engines.mechanical.cutting_data import (
    get_cutting_data,
    MaterialCuttingData,
    NON_CUT_TIME_FACTOR,
    FACE_MILL_DIA_MM,
    FACE_MILL_TEETH,
    ENDMILL_DIA_MM,
    ENDMILL_TEETH,
)


DATA_FILE = Path(__file__).parent.parent.parent / "data" / "processes.json"

# Machining allowances (mm) — must match config.py
_ALLOWANCE_DIA = 3.0   # diameter allowance
_ALLOWANCE_LEN = 5.0   # length allowance
_FACING_DEPTH = 2.5    # material removed per face (mm)


@dataclass(frozen=True)
class ProcessInfo:
    id: str
    name: str
    category: str
    description: str
    machine_rate: float
    setup_time_min: float
    power_kw: float
    tooling_cost_per_unit: float


def load_processes() -> dict[str, ProcessInfo]:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    result = {}
    for p in data["processes"]:
        pid = p["id"]
        result[pid] = ProcessInfo(
            id=pid,
            name=p["name"],
            category=p["category"],
            description=p["description"],
            machine_rate=MACHINE_RATES.get(pid, 800),
            setup_time_min=SETUP_TIMES.get(pid, 30),
            power_kw=POWER_CONSUMPTION.get(pid, 5),
            tooling_cost_per_unit=TOOLING_COST_PER_UNIT.get(pid, 5),
        )
    return result


def list_process_names() -> list[tuple[str, str]]:
    processes = load_processes()
    return [(pid, p.name) for pid, p in processes.items()]


# ---------------------------------------------------------------------------
# MRR-based time estimation helpers
# ---------------------------------------------------------------------------

def _turning_mrr(vc: float, f: float, ap: float) -> float:
    """MRR for turning (mm³/min) = Vc(m/min) × 1000 × f(mm/rev) × ap(mm)."""
    return vc * 1000 * f * ap


def _milling_mrr(vc: float, fz: float, z: int, d_tool: float,
                 ae: float, ap: float) -> float:
    """MRR for milling (mm³/min) = ae × ap × Vf, where Vf = fz × z × n."""
    n = (vc * 1000) / (math.pi * d_tool) if d_tool > 0 else 1
    vf = fz * z * n  # table feed (mm/min)
    return ae * ap * vf


def _drilling_time_per_hole(vc: float, f: float, diameter: float,
                            depth: float) -> float:
    """Drilling time (min) = depth / (f × n), where n = Vc×1000 / (π×d)."""
    if diameter <= 0:
        return 0.5
    n = (vc * 1000) / (math.pi * diameter)
    feed_rate = f * n  # mm/min
    if feed_rate <= 0:
        return 1.0
    return depth / feed_rate


# ---------------------------------------------------------------------------
# Main estimation function
# ---------------------------------------------------------------------------

def estimate_process_time_min(
    process_id: str,
    dimensions: dict,
    machinability: float = 0.5,
    material_name: str | None = None,
) -> float:
    """Estimate machining time in minutes using MRR-based physics.

    Args:
        process_id: Process identifier (e.g., "turning", "drilling").
        dimensions: Part dimensions from drawing extraction.
        machinability: 0-1 scale (fallback if material_name not provided).
        material_name: Exact material name for cutting data lookup.

    Returns:
        Estimated cycle time in minutes (including non-cutting overhead).
    """
    cd = get_cutting_data(material_name, machinability)

    od = dimensions.get("outer_diameter_mm", 50)
    id_mm = dimensions.get("inner_diameter_mm", 0)
    length = dimensions.get("length_mm", 100)
    width = dimensions.get("width_mm", 50)
    height = dimensions.get("height_mm", 30)
    hole_dia = dimensions.get("hole_diameter_mm", 8)
    hole_count = dimensions.get("hole_count", 1)
    hole_depth = dimensions.get("hole_depth_mm", 0) or length * 0.5
    thread_length = dimensions.get("thread_length_mm", 20)
    thread_count = dimensions.get("thread_count", 1)
    thread_pitch = dimensions.get("thread_pitch_mm", 1.5)
    groove_count = dimensions.get("groove_count", 1)
    surface_area = dimensions.get("surface_area_cm2", 100)
    pocket_depth = dimensions.get("pocket_depth_mm", 0) or height * 0.5
    slot_width = dimensions.get("slot_width_mm", 0) or 10.0
    slot_depth = dimensions.get("slot_depth_mm", 0) or 8.0

    t = cd.turning
    m = cd.milling
    d = cd.drilling
    g = cd.grinding

    if process_id == "turning":
        return _estimate_turning(od, length, t)

    elif process_id == "facing":
        return _estimate_facing(od, t)

    elif process_id == "boring":
        return _estimate_boring(id_mm, length, t)

    elif process_id == "milling_face":
        return _estimate_face_milling(length, width, m)

    elif process_id == "milling_slot":
        return _estimate_slot_milling(length, slot_width, slot_depth, m)

    elif process_id == "milling_pocket":
        return _estimate_pocket_milling(length, width, pocket_depth, m)

    elif process_id == "drilling":
        return _estimate_drilling(hole_dia, hole_depth, hole_count, d)

    elif process_id == "reaming":
        return _estimate_reaming(hole_dia, hole_depth, hole_count, d)

    elif process_id == "tapping":
        return _estimate_tapping(hole_dia, thread_length, thread_pitch,
                                 thread_count, d)

    elif process_id == "threading":
        return _estimate_threading(od, thread_length, thread_pitch,
                                   thread_count, t)

    elif process_id == "grinding_cylindrical":
        return _estimate_cylindrical_grinding(od, length, g)

    elif process_id == "grinding_surface":
        return _estimate_surface_grinding(length, width, g)

    elif process_id == "knurling":
        return _estimate_knurling(od, length, t)

    elif process_id == "broaching":
        return _estimate_broaching(length)

    elif process_id == "heat_treatment":
        weight_proxy = od * od * length / 1e6
        return max(5.0, weight_proxy * 10)

    elif process_id.startswith("surface_treatment"):
        return max(2.0, surface_area / 50)

    else:
        return 5.0


# ---------------------------------------------------------------------------
# Per-process physics estimators
# ---------------------------------------------------------------------------

def _estimate_turning(od: float, length: float, t) -> float:
    """Turning: remove machining allowance from OD over full length.

    Roughing pass removes bulk (allowance/2 per side), finishing pass cleans up.
    """
    stock_od = od + _ALLOWANCE_DIA
    # Roughing: stock_od → od + 2*ap_finish (leave finishing stock)
    rough_start_r = stock_od / 2
    rough_end_r = od / 2 + t.ap_finish
    rough_depth = rough_start_r - rough_end_r

    rough_time = 0.0
    if rough_depth > 0:
        n_rough_passes = max(1, math.ceil(rough_depth / t.ap_rough))
        actual_ap = rough_depth / n_rough_passes
        rough_vol = math.pi * (rough_start_r**2 - rough_end_r**2) * length
        rough_mrr = _turning_mrr(t.vc_rough, t.f_rough, actual_ap)
        rough_time = rough_vol / max(rough_mrr, 1)

    # Finishing: remove last ap_finish per side
    finish_start_r = od / 2 + t.ap_finish
    finish_end_r = od / 2
    finish_vol = math.pi * (finish_start_r**2 - finish_end_r**2) * length
    finish_mrr = _turning_mrr(t.vc_finish, t.f_finish, t.ap_finish)
    finish_time = finish_vol / max(finish_mrr, 1)

    return (rough_time + finish_time) * NON_CUT_TIME_FACTOR


def _estimate_facing(od: float, t) -> float:
    """Facing: remove material from one end face."""
    face_radius = (od + _ALLOWANCE_DIA) / 2
    volume = math.pi * face_radius**2 * _FACING_DEPTH
    mrr = _turning_mrr(t.vc_rough, t.f_rough, t.ap_rough)
    cut_time = volume / max(mrr, 1)
    # Typically face both ends → 2x, but user selects per-operation
    return cut_time * NON_CUT_TIME_FACTOR


def _estimate_boring(inner_dia: float, length: float, t) -> float:
    """Boring: enlarge existing hole to final ID."""
    if inner_dia <= 0:
        return 1.0 * NON_CUT_TIME_FACTOR

    # Assume pre-drilled pilot is 80% of final bore dia
    pilot_dia = inner_dia * 0.8
    bore_depth = length * 0.8

    start_r = inner_dia / 2
    pilot_r = pilot_dia / 2
    volume = math.pi * (start_r**2 - pilot_r**2) * bore_depth
    # Boring uses lower feed/speed than OD turning (reduced rigidity)
    mrr = _turning_mrr(t.vc_rough * 0.7, t.f_rough * 0.8, t.ap_rough * 0.7)
    return (volume / max(mrr, 1)) * NON_CUT_TIME_FACTOR


def _estimate_face_milling(length: float, width: float, m) -> float:
    """Face milling with indexable face mill cutter."""
    # Roughing pass
    ae = FACE_MILL_DIA_MM * m.ae_ratio_rough
    rough_mrr = _milling_mrr(
        m.vc_rough, m.fz_rough, FACE_MILL_TEETH, FACE_MILL_DIA_MM,
        ae, m.ap_rough,
    )
    # Number of passes across width
    n_stepover = max(1, math.ceil(width / ae))
    rough_vol = length * width * m.ap_rough
    rough_time = rough_vol / max(rough_mrr, 1) * (n_stepover / max(n_stepover, 1))

    # Finishing pass (light cut)
    ae_fin = FACE_MILL_DIA_MM * m.ae_ratio_finish
    finish_mrr = _milling_mrr(
        m.vc_finish, m.fz_finish, FACE_MILL_TEETH, FACE_MILL_DIA_MM,
        ae_fin, m.ap_finish,
    )
    finish_vol = length * width * m.ap_finish
    finish_time = finish_vol / max(finish_mrr, 1)

    return (rough_time + finish_time) * NON_CUT_TIME_FACTOR


def _estimate_slot_milling(length: float, slot_width: float,
                           slot_depth: float, m) -> float:
    """Slot milling: full-width engagement with endmill."""
    tool_dia = min(ENDMILL_DIA_MM, slot_width)
    ae = tool_dia  # full slot = 100% engagement

    n_depth_passes = max(1, math.ceil(slot_depth / m.ap_rough))
    actual_ap = slot_depth / n_depth_passes

    mrr = _milling_mrr(
        m.vc_rough * 0.7,  # reduce speed for full engagement
        m.fz_rough * 0.7,
        ENDMILL_TEETH, tool_dia, ae, actual_ap,
    )
    volume = slot_width * slot_depth * length
    return (volume / max(mrr, 1)) * NON_CUT_TIME_FACTOR


def _estimate_pocket_milling(length: float, width: float,
                             pocket_depth: float, m) -> float:
    """Pocket milling with endmill — multiple depth + stepover passes."""
    ae = ENDMILL_DIA_MM * m.ae_ratio_rough

    n_depth_passes = max(1, math.ceil(pocket_depth / m.ap_rough))
    actual_ap = pocket_depth / n_depth_passes

    rough_mrr = _milling_mrr(
        m.vc_rough, m.fz_rough, ENDMILL_TEETH, ENDMILL_DIA_MM,
        ae, actual_ap,
    )
    volume = length * width * pocket_depth
    rough_time = volume / max(rough_mrr, 1)

    # Finishing walls + floor (perimeter × depth + floor area × ap_finish)
    perimeter = 2 * (length + width)
    wall_vol = perimeter * pocket_depth * m.ap_finish
    floor_vol = length * width * m.ap_finish
    finish_vol = wall_vol + floor_vol

    ae_fin = ENDMILL_DIA_MM * m.ae_ratio_finish
    finish_mrr = _milling_mrr(
        m.vc_finish, m.fz_finish, ENDMILL_TEETH, ENDMILL_DIA_MM,
        ae_fin, m.ap_finish,
    )
    finish_time = finish_vol / max(finish_mrr, 1)

    return (rough_time + finish_time) * NON_CUT_TIME_FACTOR


def _estimate_drilling(hole_dia: float, hole_depth: float,
                       hole_count: int, d) -> float:
    """Drilling using MRR-based time per hole."""
    time_per = _drilling_time_per_hole(d.vc, d.f_per_rev, hole_dia, hole_depth)
    # Add rapid + pecking overhead for deep holes (depth > 3×dia)
    peck_factor = 1.0 + max(0, (hole_depth / max(hole_dia, 1) - 3) * 0.1)
    return time_per * hole_count * peck_factor * NON_CUT_TIME_FACTOR


def _estimate_reaming(hole_dia: float, hole_depth: float,
                      hole_count: int, d) -> float:
    """Reaming: slower than drilling, higher precision.

    Vc ≈ 50% of drilling, feed ≈ 150% of drilling.
    """
    time_per = _drilling_time_per_hole(
        d.vc * 0.5, d.f_per_rev * 1.5, hole_dia, hole_depth,
    )
    return time_per * hole_count * NON_CUT_TIME_FACTOR


def _estimate_tapping(hole_dia: float, thread_length: float,
                      thread_pitch: float, thread_count: int, d) -> float:
    """Tapping time = 2 × depth / (pitch × n) — in-stroke + out-stroke.

    Tapping Vc is typically 10-20 m/min (much slower than drilling).
    """
    vc_tap = min(d.vc * 0.2, 20)  # tapping speed, capped at 20 m/min
    if hole_dia <= 0 or thread_pitch <= 0:
        return 0.5 * thread_count
    n = (vc_tap * 1000) / (math.pi * hole_dia)
    pitch_feed = thread_pitch * n  # mm/min (synchronized feed)
    time_per = 2 * thread_length / max(pitch_feed, 1)  # in + out
    return time_per * thread_count * NON_CUT_TIME_FACTOR


def _estimate_threading(od: float, thread_length: float,
                        thread_pitch: float, thread_count: int, t) -> float:
    """External threading on lathe — multiple passes at decreasing depth.

    Typically 4-8 spring passes. Thread depth ≈ 0.65 × pitch.
    """
    if thread_pitch <= 0:
        return 1.0 * thread_count

    thread_depth = 0.65 * thread_pitch
    n_passes = max(4, math.ceil(thread_depth / 0.1))  # ~0.1mm per pass

    # RPM limited by threading speed (lower than turning)
    vc_thread = t.vc_rough * 0.4
    n_rpm = (vc_thread * 1000) / (math.pi * od) if od > 0 else 500
    time_per_pass = thread_length / (thread_pitch * n_rpm)
    # Factor of 2 for return stroke
    total = time_per_pass * n_passes * 2 * thread_count
    return total * NON_CUT_TIME_FACTOR


def _estimate_cylindrical_grinding(od: float, length: float, g) -> float:
    """Cylindrical grinding: traverse grinding with infeed per pass.

    Stock to remove ≈ 0.2mm on diameter (0.1mm per side after turning).
    """
    stock_per_side = 0.10  # mm
    n_rough = max(1, math.ceil(stock_per_side * 0.8 / g.infeed_rough))
    n_finish = max(1, math.ceil(stock_per_side * 0.2 / g.infeed_finish))

    # Time per pass = length / traverse_rate (converted mm to m)
    time_per_pass = (length / 1000) / max(g.traverse_rate, 0.1)
    sparkout_time = time_per_pass * g.sparkout_passes

    return ((n_rough + n_finish) * time_per_pass + sparkout_time) * NON_CUT_TIME_FACTOR


def _estimate_surface_grinding(length: float, width: float, g) -> float:
    """Surface grinding: crossfeed across width, traverse along length.

    Stock to remove ≈ 0.15mm total.
    """
    stock = 0.15  # mm total
    n_rough = max(1, math.ceil(stock * 0.7 / g.infeed_rough))
    n_finish = max(1, math.ceil(stock * 0.3 / g.infeed_finish))

    crossfeed_step = 5.0  # mm per traverse pass
    n_crossfeed = max(1, math.ceil(width / crossfeed_step))
    time_per_depth = n_crossfeed * (length / 1000) / max(g.traverse_rate, 0.1)
    sparkout_time = time_per_depth * g.sparkout_passes

    return ((n_rough + n_finish) * time_per_depth + sparkout_time) * NON_CUT_TIME_FACTOR


def _estimate_knurling(od: float, length: float, t) -> float:
    """Knurling: single slow pass with forming tool."""
    if od <= 0:
        return 1.0
    # Knurling feed ≈ 0.5 mm/rev, slow RPM
    knurl_vc = 20  # m/min (very slow)
    n_rpm = (knurl_vc * 1000) / (math.pi * od)
    feed_rate = 0.5 * n_rpm  # mm/min
    return (length / max(feed_rate, 1)) * NON_CUT_TIME_FACTOR


def _estimate_broaching(length: float) -> float:
    """Broaching: relatively fixed time per stroke.

    Cutting speed 3-10 m/min, stroke = 1.5× feature length.
    """
    stroke = length * 1.5
    broach_speed = 6000  # mm/min (6 m/min)
    cut_time = stroke / broach_speed
    return_time = stroke / (broach_speed * 3)  # fast return
    return (cut_time + return_time) * NON_CUT_TIME_FACTOR * 2  # safety factor
