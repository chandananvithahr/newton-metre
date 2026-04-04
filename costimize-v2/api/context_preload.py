"""CAG context preloader — loads operational constants once at startup.

Karpathy CAG pattern: preload static knowledge (rates, materials, processes)
into a cached string injected into every chat system prompt. Zero retrieval
latency — the agent always "knows" the numbers.

Unlike wiki_loader (which routes query-specific knowledge), this is always-on
operational data the agent needs for every manufacturing cost question.
"""

import json
import logging
from pathlib import Path
from functools import lru_cache

logger = logging.getLogger("costimize")

DATA_DIR = Path(__file__).parent.parent / "data"


@lru_cache(maxsize=1)
def get_operational_context() -> str:
    """Return formatted operational constants for the system prompt.

    Cached forever (lru_cache) — loaded once, reused on every request.
    """
    sections = []

    # 1. Machine rates + labour
    sections.append(_format_rates())

    # 2. Materials reference
    sections.append(_format_materials())

    # 3. Processes reference
    sections.append(_format_processes())

    context = "\n\n".join(s for s in sections if s)
    logger.info("Operational context loaded: ~%d tokens", len(context) // 4)
    return context


def _format_rates() -> str:
    """Format machine rates, setup times, and base constants."""
    try:
        # Import config constants directly
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        import config as cfg

        lines = [
            "=== LIVE OPERATIONAL RATES (₹, Indian Manufacturing) ===",
            "",
            "**Base Rates:**",
            f"- Labour: ₹{cfg.LABOUR_RATE}/hr",
            f"- Power: ₹{cfg.POWER_RATE}/kWh",
            f"- Material wastage: {cfg.MATERIAL_WASTAGE_PCT}%",
            f"- Tight tolerance surcharge (<±0.05mm): +{cfg.TIGHT_TOLERANCE_SURCHARGE_PCT}%",
            f"- Overhead: {cfg.OVERHEAD_PCT}%  |  Profit margin: {cfg.PROFIT_PCT}%",
            f"- Shop floor efficiency vs catalog: {int(cfg.SHOP_FLOOR_EFFICIENCY * 100)}%",
            "",
            "**Machine Hour Rates (₹/hr):**",
        ]
        for process, rate in cfg.MACHINE_RATES.items():
            setup = cfg.SETUP_TIMES.get(process, 0)
            tooling = cfg.TOOLING_COST_PER_UNIT.get(process, 0)
            lines.append(
                f"- {process.replace('_', ' ').title()}: ₹{rate}/hr | setup {setup}min | tooling ₹{tooling}/unit"
            )

        lines += [
            "",
            "**PCB Assembly:**",
            f"- SMD: ₹{cfg.SMD_RATE_PER_PAD}/pad | THT: ₹{cfg.THT_RATE_PER_PIN}/pin",
            f"- Stencil: ₹{cfg.STENCIL_COST} amortized | Test: ₹{cfg.TEST_RATE_PER_BOARD}/board",
            "",
            "**Cable Assembly:**",
            f"- Labour: ₹{cfg.CABLE_LABOUR_RATE}/hr | Wire: {cfg.CABLE_TIME_PER_WIRE_MIN}min/wire",
            f"- Connector: {cfg.CABLE_TIME_PER_CONNECTOR_MIN}min each | Sleeving: {cfg.CABLE_TIME_SLEEVING_MIN}min",
        ]
        return "\n".join(lines)
    except Exception as e:
        logger.warning("Failed to load rates from config: %s", e)
        return ""


def _format_materials() -> str:
    """Format material prices and properties."""
    try:
        mat_file = DATA_DIR / "materials.json"
        if not mat_file.exists():
            return ""

        data = json.loads(mat_file.read_text())
        materials = data.get("materials", [])

        lines = ["**Material Prices & Properties (current, INR):**"]
        for m in materials:
            lines.append(
                f"- {m['name']}: ₹{m['price_per_kg_inr']}/kg | "
                f"density {m['density_kg_per_m3']} kg/m³ | "
                f"machinability {int(m['machinability'] * 100)}%"
            )
        return "\n".join(lines)
    except Exception as e:
        logger.warning("Failed to load materials.json: %s", e)
        return ""


def _format_processes() -> str:
    """Format available processes."""
    try:
        proc_file = DATA_DIR / "processes.json"
        if not proc_file.exists():
            return ""

        data = json.loads(proc_file.read_text())
        processes = data.get("processes", [])

        # Group by category
        by_cat: dict[str, list] = {}
        for p in processes:
            cat = p.get("category", "other")
            by_cat.setdefault(cat, []).append(p)

        lines = ["**Available Processes:**"]
        for cat, procs in by_cat.items():
            names = ", ".join(p["name"] for p in procs)
            lines.append(f"- {cat.title()}: {names}")
        return "\n".join(lines)
    except Exception as e:
        logger.warning("Failed to load processes.json: %s", e)
        return ""
