"""Surface treatment and plating process database — 40+ processes.

Area-based costing (₹/sq.dm) from Indian job shop rates.
Sources: IndiaMART, finishing.com, Indian plating shop quotes.
MIL-spec references for defense/aerospace processes.
"""
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class SurfaceTreatment:
    name: str
    rate_per_sq_dm: float       # ₹/sq.dm
    min_batch_charge: float     # ₹ minimum per batch
    category: str               # electroplating, anodizing, conversion, spray, paint, vapor, mechanical
    applicable_materials: tuple[str, ...]  # substrate types
    mil_spec: str               # MIL/AMS spec reference (or "")
    industry: str               # "all", "defense", "aerospace", "auto", "defense+aerospace"
    thickness_um: tuple[float, float]  # typical min-max in microns
    needs_he_baking: bool       # hydrogen embrittlement baking for high-strength steel


SURFACE_TREATMENTS: dict[str, SurfaceTreatment] = {
    # --- Electroplating ---
    "zinc_clear": SurfaceTreatment(
        "Zinc Plating (Clear)", 5, 800, "electroplating",
        ("steel", "cast_iron"), "ASTM B633", "all", (5, 25), True,
    ),
    "zinc_yellow": SurfaceTreatment(
        "Zinc Plating (Yellow Passivation)", 6, 800, "electroplating",
        ("steel", "cast_iron"), "ASTM B633", "all", (5, 25), True,
    ),
    "zinc_black": SurfaceTreatment(
        "Zinc Plating (Black Passivation)", 7, 800, "electroplating",
        ("steel", "cast_iron"), "ASTM B633", "defense+aerospace", (5, 25), True,
    ),
    "nickel_bright": SurfaceTreatment(
        "Nickel Plating (Bright)", 12, 1500, "electroplating",
        ("steel", "copper", "brass"), "ASTM B689", "all", (10, 40), True,
    ),
    "nickel_electroless": SurfaceTreatment(
        "Electroless Nickel (EN)", 18, 3000, "electroplating",
        ("steel", "aluminum", "copper", "cast_iron"), "MIL-C-26074/AMS 2404", "defense+aerospace", (12, 75), False,
    ),
    "chrome_hard": SurfaceTreatment(
        "Hard Chrome Plating", 15, 3000, "electroplating",
        ("steel", "cast_iron", "stainless"), "MIL-STD-1501/AMS 2406", "defense+aerospace", (25, 250), True,
    ),
    "chrome_decorative": SurfaceTreatment(
        "Decorative Chrome (Ni+Cr)", 22, 2000, "electroplating",
        ("steel", "copper", "brass"), "ASTM B456", "auto", (0.25, 1.0), True,
    ),
    "cadmium": SurfaceTreatment(
        "Cadmium Plating", 25, 5000, "electroplating",
        ("steel",), "QQ-P-416/AMS 2400", "defense+aerospace", (5, 25), True,
    ),
    "copper_plate": SurfaceTreatment(
        "Copper Plating", 8, 1000, "electroplating",
        ("steel", "cast_iron"), "MIL-C-14550", "all", (5, 50), True,
    ),
    "tin": SurfaceTreatment(
        "Tin Plating", 8, 1000, "electroplating",
        ("steel", "copper", "brass"), "MIL-T-10727/ASTM B545", "all", (5, 30), True,
    ),
    "silver": SurfaceTreatment(
        "Silver Plating", 50, 5000, "electroplating",
        ("copper", "brass", "steel"), "QQ-S-365/AMS 2410", "defense+aerospace", (5, 25), True,
    ),
    "gold": SurfaceTreatment(
        "Gold Plating", 150, 10000, "electroplating",
        ("copper", "brass", "steel"), "MIL-G-45204", "defense+aerospace", (0.5, 5), True,
    ),

    # --- Anodizing (Aluminum only) ---
    "anodize_type_i": SurfaceTreatment(
        "Anodize Type I (Chromic Acid)", 12, 2000, "anodizing",
        ("aluminum",), "MIL-A-8625 Type I", "aerospace", (2, 7), False,
    ),
    "anodize_type_ii_clear": SurfaceTreatment(
        "Anodize Type II (Sulfuric, Clear)", 8, 1500, "anodizing",
        ("aluminum",), "MIL-A-8625 Type II", "all", (5, 25), False,
    ),
    "anodize_type_ii_color": SurfaceTreatment(
        "Anodize Type II (Color)", 12, 1500, "anodizing",
        ("aluminum",), "MIL-A-8625 Type II", "all", (5, 25), False,
    ),
    "anodize_type_iii": SurfaceTreatment(
        "Anodize Type III (Hard Anodize)", 22, 3000, "anodizing",
        ("aluminum",), "MIL-A-8625 Type III", "defense+aerospace", (25, 75), False,
    ),
    "anodize_ptfe": SurfaceTreatment(
        "Anodize + PTFE Infusion", 35, 4000, "anodizing",
        ("aluminum",), "MIL-A-8625 Type III + PTFE", "defense+aerospace", (25, 75), False,
    ),

    # --- Chemical Conversion ---
    "chromate_conversion": SurfaceTreatment(
        "Chromate Conversion (Alodine)", 4, 500, "conversion",
        ("aluminum",), "MIL-DTL-5541/MIL-C-5541", "aerospace", (0.025, 1.0), False,
    ),
    "phosphate_zinc": SurfaceTreatment(
        "Zinc Phosphating", 3, 500, "conversion",
        ("steel",), "MIL-DTL-16232", "defense", (5, 15), False,
    ),
    "phosphate_manganese": SurfaceTreatment(
        "Manganese Phosphating (Parkerizing)", 5, 600, "conversion",
        ("steel",), "MIL-DTL-16232 Type M", "defense", (5, 25), False,
    ),
    "phosphate_iron": SurfaceTreatment(
        "Iron Phosphating", 2, 400, "conversion",
        ("steel",), "TT-C-490", "auto", (1, 3), False,
    ),
    "black_oxide_hot": SurfaceTreatment(
        "Black Oxide (Hot)", 3, 500, "conversion",
        ("steel",), "MIL-DTL-13924", "defense", (0.5, 2.5), False,
    ),
    "black_oxide_cold": SurfaceTreatment(
        "Black Oxide (Cold)", 2, 300, "conversion",
        ("steel",), "", "all", (0.5, 1.0), False,
    ),
    "passivation_nitric": SurfaceTreatment(
        "Passivation (Nitric Acid)", 4, 600, "conversion",
        ("stainless",), "ASTM A967/AMS 2700", "all", (0, 0), False,
    ),
    "passivation_citric": SurfaceTreatment(
        "Passivation (Citric Acid)", 5, 600, "conversion",
        ("stainless",), "ASTM A967", "all", (0, 0), False,
    ),

    # --- Thermal/Spray Coatings ---
    "hvof": SurfaceTreatment(
        "HVOF Coating", 150, 10000, "spray",
        ("steel", "stainless", "aluminum"), "AMS 2447", "aerospace", (100, 500), False,
    ),
    "plasma_spray": SurfaceTreatment(
        "Plasma Spray", 100, 8000, "spray",
        ("steel", "stainless"), "AMS 2437", "aerospace", (100, 1000), False,
    ),
    "flame_spray": SurfaceTreatment(
        "Flame Spray", 60, 5000, "spray",
        ("steel",), "", "all", (100, 500), False,
    ),

    # --- Paint/Organic ---
    "powder_coat_standard": SurfaceTreatment(
        "Powder Coating (Standard)", 8, 800, "paint",
        ("steel", "aluminum"), "", "all", (60, 100), False,
    ),
    "powder_coat_premium": SurfaceTreatment(
        "Powder Coating (Premium/Epoxy)", 12, 1000, "paint",
        ("steel", "aluminum"), "", "auto", (60, 120), False,
    ),
    "ecoat": SurfaceTreatment(
        "E-Coat (Cathodic)", 6, 1500, "paint",
        ("steel",), "", "auto", (15, 35), False,
    ),
    "wet_paint_2coat": SurfaceTreatment(
        "Wet Paint (Primer + Topcoat)", 15, 500, "paint",
        ("steel", "aluminum"), "", "all", (40, 80), False,
    ),
    "carc": SurfaceTreatment(
        "CARC (Military Paint)", 50, 8000, "paint",
        ("steel", "aluminum"), "MIL-DTL-53072/MIL-DTL-64159", "defense", (50, 100), False,
    ),

    # --- Vapor Deposition ---
    "pvd": SurfaceTreatment(
        "PVD Coating", 80, 8000, "vapor",
        ("steel", "stainless", "aluminum"), "", "aerospace", (1, 5), False,
    ),
    "cvd": SurfaceTreatment(
        "CVD Coating", 120, 10000, "vapor",
        ("steel",), "", "aerospace", (5, 20), False,
    ),
    "dlc": SurfaceTreatment(
        "DLC (Diamond-Like Carbon)", 150, 15000, "vapor",
        ("steel", "stainless"), "", "auto", (1, 4), False,
    ),

    # --- Mechanical Surface ---
    "shot_peening": SurfaceTreatment(
        "Shot Peening", 5, 1000, "mechanical",
        ("steel", "aluminum", "stainless"), "AMS 2430/MIL-S-13165", "defense+aerospace", (0, 0), False,
    ),
    "shot_blasting": SurfaceTreatment(
        "Shot Blasting", 3, 500, "mechanical",
        ("steel", "cast_iron"), "", "all", (0, 0), False,
    ),
    "electropolishing": SurfaceTreatment(
        "Electropolishing", 12, 2000, "mechanical",
        ("stainless",), "ASTM B912", "aerospace", (0, 0), False,
    ),
    "tumble_deburring": SurfaceTreatment(
        "Tumble/Vibratory Deburring", 3, 500, "mechanical",
        ("steel", "aluminum", "brass", "copper"), "", "all", (0, 0), False,
    ),
}

# Hydrogen embrittlement baking cost (₹/kg)
HE_BAKING_RATE_PER_KG = 15.0


def get_surface_treatment(process_id: str) -> SurfaceTreatment:
    if process_id not in SURFACE_TREATMENTS:
        raise ValueError(
            f"Unknown surface treatment: {process_id}. "
            f"Available: {list(SURFACE_TREATMENTS.keys())}"
        )
    return SURFACE_TREATMENTS[process_id]


def list_surface_treatments(
    category: str | None = None,
    industry: str | None = None,
) -> list[str]:
    """List available treatments, optionally filtered by category or industry."""
    results = []
    for pid, st in SURFACE_TREATMENTS.items():
        if category and st.category != category:
            continue
        if industry and industry not in st.industry and st.industry != "all":
            continue
        results.append(pid)
    return results


def estimate_surface_area_sq_dm(
    od_mm: float = 0,
    length_mm: float = 0,
    width_mm: float = 0,
    height_mm: float = 0,
    complexity_factor: float = 1.2,
) -> float:
    """Estimate treatable surface area in sq.dm.

    For cylindrical parts: pi * D * L (outer surface).
    For rectangular parts: 2*(L*W + L*H + W*H).
    Complexity factor accounts for features (holes, grooves, etc.).
    """
    if od_mm > 0 and length_mm > 0:
        # Cylindrical: outer surface + two end faces
        area_mm2 = (math.pi * od_mm * length_mm
                     + 2 * math.pi * (od_mm / 2) ** 2)
    elif length_mm > 0 and width_mm > 0:
        h = height_mm if height_mm > 0 else 1.0  # minimum 1mm for flat parts
        area_mm2 = 2 * (length_mm * width_mm + length_mm * h + width_mm * h)
    else:
        return 0.0

    area_sq_dm = (area_mm2 / 1e4) * complexity_factor  # 1 sq.dm = 100cm² = 10000mm²
    return area_sq_dm


def calculate_surface_treatment_cost(
    process_id: str,
    surface_area_sq_dm: float,
    quantity: int = 1,
    part_weight_kg: float = 0,
    is_high_strength_steel: bool = False,
    masking_pct: float = 0,
) -> float:
    """Calculate surface treatment cost per unit in ₹.

    Args:
        process_id: Key from SURFACE_TREATMENTS.
        surface_area_sq_dm: Treatable surface area per part.
        quantity: Batch size (for minimum charge amortization).
        part_weight_kg: Part weight (for H.E. baking calculation).
        is_high_strength_steel: True if >31 HRC and electroplated.
        masking_pct: % of area requiring masking (adds 10-25% cost).
    """
    st = get_surface_treatment(process_id)

    base_cost = surface_area_sq_dm * st.rate_per_sq_dm

    # Minimum batch charge amortized
    min_charge_per_unit = st.min_batch_charge / quantity
    base_cost = max(base_cost, min_charge_per_unit)

    # Masking surcharge
    if masking_pct > 0:
        masking_factor = 1.0 + (masking_pct / 100) * 0.20  # 20% of masking area ratio
        base_cost *= masking_factor

    # Hydrogen embrittlement baking (electroplating on high-strength steel)
    he_cost = 0.0
    if (is_high_strength_steel and st.needs_he_baking
            and st.category == "electroplating" and part_weight_kg > 0):
        he_cost = part_weight_kg * HE_BAKING_RATE_PER_KG

    return base_cost + he_cost
