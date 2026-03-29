"""Material database — loads materials.json, provides lookup by name.

Mechanical properties added from:
- Ghosh & Mallik, Manufacturing Science 2nd Ed (UTS, shear stress, hardness)
- P.N. Rao, Manufacturing Technology Vol 1 (IS-AISI grade mapping, Indian steel grades)
- Stephenson & Agapiou, Metal Cutting Theory & Practice 3rd Ed (machinability data)
"""
import json
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Material:
    name: str
    price_per_kg_inr: float
    density_kg_per_m3: float
    machinability: float  # 0.0 to 1.0, higher = easier to machine
    uts_mpa: float = 0.0        # ultimate tensile strength (MPa)
    yield_mpa: float = 0.0      # yield strength (MPa)
    hardness_bhn: float = 0.0   # Brinell hardness number
    elongation_pct: float = 0.0 # elongation at break (%)
    aisi_equivalent: str = ""   # AISI/SAE equivalent grade


DATA_FILE = Path(__file__).parent.parent.parent / "data" / "materials.json"


# Mechanical properties by material name.
# Sources: Ghosh & Mallik (UTS, hardness), P.N. Rao Vol 1 (IS grade mapping),
# Machinery's Handbook (yield, elongation), Stephenson (machinability).
# IS-AISI mapping from P.N. Rao Table 2.7.
_MECHANICAL_PROPERTIES: dict[str, dict] = {
    "Aluminum 6061": {
        "uts_mpa": 310, "yield_mpa": 276, "hardness_bhn": 95,
        "elongation_pct": 17.0, "aisi_equivalent": "6061-T6",
    },
    "Mild Steel IS2062": {
        "uts_mpa": 410, "yield_mpa": 250, "hardness_bhn": 120,
        "elongation_pct": 23.0, "aisi_equivalent": "AISI 1018",
        # IS 2062 E250 → AISI 1018/1020 (P.N. Rao Table 2.7)
    },
    "Stainless Steel 304": {
        "uts_mpa": 515, "yield_mpa": 205, "hardness_bhn": 170,
        "elongation_pct": 40.0, "aisi_equivalent": "AISI 304",
    },
    "Brass IS319": {
        "uts_mpa": 360, "yield_mpa": 125, "hardness_bhn": 80,
        "elongation_pct": 35.0, "aisi_equivalent": "CuZn39Pb3",
    },
    "EN8 Steel": {
        "uts_mpa": 600, "yield_mpa": 350, "hardness_bhn": 180,
        "elongation_pct": 16.0, "aisi_equivalent": "AISI 1045",
        # EN8 = 45C8 = C45 (P.N. Rao Table 2.7)
    },
    "EN24 Steel": {
        "uts_mpa": 850, "yield_mpa": 680, "hardness_bhn": 260,
        "elongation_pct": 12.0, "aisi_equivalent": "AISI 4340",
        # EN24 = 40NiCrMo6 (P.N. Rao Table 2.7)
    },
    "Copper": {
        "uts_mpa": 220, "yield_mpa": 70, "hardness_bhn": 45,
        "elongation_pct": 45.0, "aisi_equivalent": "C11000",
    },
    "Cast Iron": {
        "uts_mpa": 250, "yield_mpa": 0, "hardness_bhn": 200,
        "elongation_pct": 1.0, "aisi_equivalent": "ASTM A48 Class 30",
        # Ghosh & Mallik: CI brittle, elongation ~1-2%, breaks ~200-300 N/mm²
    },
    "Titanium Grade 5": {
        "uts_mpa": 950, "yield_mpa": 880, "hardness_bhn": 334,
        "elongation_pct": 14.0, "aisi_equivalent": "Ti-6Al-4V",
    },
}


def load_materials() -> dict[str, Material]:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    result = {}
    for m in data["materials"]:
        name = m["name"]
        props = _MECHANICAL_PROPERTIES.get(name, {})
        result[name] = Material(
            name=name,
            price_per_kg_inr=m["price_per_kg_inr"],
            density_kg_per_m3=m["density_kg_per_m3"],
            machinability=m.get("machinability", 0.5),
            uts_mpa=props.get("uts_mpa", 0.0),
            yield_mpa=props.get("yield_mpa", 0.0),
            hardness_bhn=props.get("hardness_bhn", 0.0),
            elongation_pct=props.get("elongation_pct", 0.0),
            aisi_equivalent=props.get("aisi_equivalent", ""),
        )
    return result


def get_material(name: str) -> Material:
    materials = load_materials()
    if name not in materials:
        available = ", ".join(materials.keys())
        raise ValueError(f"Material '{name}' not found. Available: {available}")
    return materials[name]


def list_material_names() -> list[str]:
    return list(load_materials().keys())
