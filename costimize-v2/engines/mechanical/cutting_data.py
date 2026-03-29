"""Cutting parameter database — physics-based speeds, feeds, and constants.

Sources:
- Sandvik Coromant Training Handbook 2017 (kc1 specific cutting force, power formulas,
  tool life correction factors, hardness compensation — THE primary source)
- Machinery's Handbook 30th Ed (turning/milling speeds, Kp power constants, Taylor tool life)
- Walter Titex Handbook 2009 (drilling speeds/feeds by material group)
- Fundamentals of CNC Machining (SFM tables, feed/speed relationships)
- Machining Fundamentals, Walker (HSS/carbide speed ratios, process sequences)
- Stephenson & Agapiou, Metal Cutting Theory & Practice 3rd Ed (specific cutting energy,
  Taylor constants, empirical force models, machining economics, surface finish formulas)
- Ghosh & Mallik, Manufacturing Science 2nd Ed (specific cutting energy Uc, milling force
  coefficients, Taylor constants, machining economics — Indian textbook)
- P.N. Rao, Manufacturing Technology Vol 2 (cutting force constants, milling power constants,
  Taylor data for AISI 4140, process accuracy — Indian textbook)

Cross-validated against:
- xsession/r3ditor CAM engine (Kienzle kc1.1, Taylor constants for 6 CNC materials)
- kentavv/pymachining (specific cutting energy, machinability ratings for 60+ materials)
- Kennametal unit power constants (16 AISI materials — see KENNAMETAL-DATA-EXTRACTION.md)
- FreeCAD Machinability.yml (kc1 references from machiningdoctor.com)
- Stephenson Table 2.1 us values (converted to kc1, consistent with Sandvik after
  chip-thickness correction — see STEPHENSON-DATA-EXTRACTION.md §22)
- Ghosh & Mallik Table 4.4 Uc values (steel 1400, CI 1100, Al 400-700 — matches our kc1)

All values are for CARBIDE tooling (standard in Indian CNC job shops).
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class TurningParams:
    """Cutting parameters for turning/facing/boring operations."""
    vc_rough: float   # cutting speed, roughing (m/min)
    vc_finish: float  # cutting speed, finishing (m/min)
    f_rough: float    # feed rate, roughing (mm/rev)
    f_finish: float   # feed rate, finishing (mm/rev)
    ap_rough: float   # depth of cut, roughing (mm)
    ap_finish: float  # depth of cut, finishing (mm)


@dataclass(frozen=True)
class MillingParams:
    """Cutting parameters for face/slot/pocket milling."""
    vc_rough: float       # cutting speed, roughing (m/min)
    vc_finish: float      # cutting speed, finishing (m/min)
    fz_rough: float       # feed per tooth, roughing (mm/tooth)
    fz_finish: float      # feed per tooth, finishing (mm/tooth)
    ap_rough: float       # axial depth, roughing (mm)
    ap_finish: float      # axial depth, finishing (mm)
    ae_ratio_rough: float # radial engagement ratio (ae/D), roughing
    ae_ratio_finish: float


@dataclass(frozen=True)
class DrillingParams:
    """Cutting parameters for drilling operations."""
    vc: float        # cutting speed (m/min) — for ~10mm carbide drill
    f_per_rev: float # feed per revolution (mm/rev)


@dataclass(frozen=True)
class GrindingParams:
    """Cutting parameters for grinding operations."""
    wheel_speed: float       # wheel peripheral speed (m/s)
    infeed_rough: float      # depth per pass, roughing (mm)
    infeed_finish: float     # depth per pass, finishing (mm)
    traverse_rate: float     # table traverse (m/min)
    sparkout_passes: int     # number of zero-infeed passes


@dataclass(frozen=True)
class MaterialCuttingData:
    """Complete cutting data for one material."""
    turning: TurningParams
    milling: MillingParams
    drilling: DrillingParams
    grinding: GrindingParams
    kp: float       # specific cutting power (kW per cm³/min) — Machinery's Handbook
    taylor_n: float # Taylor tool life exponent (carbide ≈ 0.25)
    taylor_c: float # Taylor constant C in V×T^n = C (m/min)
    # Sandvik kc1 data — specific cutting force at 1mm chip thickness (N/mm²)
    kc1: float      # specific cutting force (N/mm²) — Sandvik Training Handbook
    mc: float       # chip thickness exponent for kc correction (typically 0.25)
    # Extended Taylor exponents (Stephenson Eq.9.9: V×T^n × f^a × d^b = Kt)
    # speed has 5-6× more impact on tool life than feed (Stephenson p.763)
    taylor_a: float = 0.77   # feed exponent (HSS baseline, carbide similar)
    taylor_b: float = 0.37   # DOC exponent (50% DOC increase → ~15% life reduction)
    # Shear stress of work material (N/mm²) — for force calculations
    # Sources: Ghosh & Mallik Table 4.4 Uc, P.N. Rao Table 2.16 tau
    shear_stress: float = 400.0


# ---------------------------------------------------------------------------
# Standard tool geometry assumptions (Indian CNC job shop defaults)
# ---------------------------------------------------------------------------
FACE_MILL_DIA_MM = 63.0     # 63mm face mill insert cutter
FACE_MILL_TEETH = 6
ENDMILL_DIA_MM = 16.0       # 16mm carbide endmill
ENDMILL_TEETH = 4
CARBIDE_EDGE_COST_INR = 12.5  # ₹50 insert / 4 edges = ₹12.5 per cutting edge
MACHINE_EFFICIENCY = 0.80     # 80% spindle utilization (rapid moves, measurement, etc.)
NON_CUT_TIME_FACTOR = 1.40   # 40% overhead: rapid traverse, tool change, measurement, load/unload
# Based on Boothroyd Ch6 data: nonproductive time is 50-60% of cycle time in production,
# but our engine already includes setup time separately, so 40% covers per-part non-cutting only.
# Process-specific adjustments applied in process_db.py where needed.

# ---------------------------------------------------------------------------
# Kienzle correction factors for cutting force (from CamScripts + Stephenson)
# kc = kc1 × (1/h)^mc × Kg × Kw × Ksp × Kvc
# Source: spanner888/CamScripts, Europa-Lehrmittel Tabellenbuch Zerspantechnik 5th Ed
# ---------------------------------------------------------------------------
KW_SHARP = 1.0     # tool wear factor — sharp tool
KW_WORN = 1.3      # tool wear factor — moderately worn (typical production)
KW_HEAVY = 1.5     # tool wear factor — heavy wear (conservative estimate)
KW_DEFAULT = 1.1   # default: slightly worn, realistic for production

# Chip compression factor by operation (Ksp)
KSP_TURNING = 1.0
KSP_MILLING = 1.2   # higher due to interrupted cut
KSP_PARTING = 1.3    # constrained chip flow
KSP_DRILLING = 1.1   # moderate compression in hole

# Speed correction factor by tool material (Kvc)
KVC_CARBIDE = 1.0    # reference
KVC_HSS = 1.2        # higher specific force at lower speeds
KVC_CERAMIC = 0.85   # lower at high speeds

# ---------------------------------------------------------------------------
# Surface finish constants (Stephenson Eq.10.9-10.10, Ghosh & Mallik Eq.4.77)
# Ra_geometric = 0.0321 × f² / rn  (μm, f in mm/rev, rn in mm)
# Actual Ra = Ra_geometric × material_factor (1.0–2.4)
# ---------------------------------------------------------------------------
DEFAULT_NOSE_RADIUS_MM = 0.8  # standard CNMG/WNMG insert nose radius

# Actual/geometric Ra ratio by material (Stephenson Fig.10.13, at ~120 m/min)
RA_CORRECTION_FACTOR: dict[str, float] = {
    "Aluminum 6061": 1.15,
    "Mild Steel IS2062": 1.20,
    "Stainless Steel 304": 1.30,
    "Brass IS319": 1.15,
    "EN8 Steel": 1.25,
    "EN24 Steel": 1.30,
    "Copper": 1.15,
    "Cast Iron": 1.40,
    "Titanium Grade 5": 1.35,
}

# Surface roughness achievable by process (Ghosh & Mallik Table 4.17, μm Ra)
PROCESS_RA_RANGE: dict[str, tuple[float, float]] = {
    "turning": (0.05, 21.0),
    "facing": (0.05, 21.0),
    "boring": (0.05, 21.0),
    "milling_face": (0.25, 25.0),
    "milling_slot": (0.25, 25.0),
    "milling_pocket": (0.25, 25.0),
    "drilling": (0.375, 12.5),
    "reaming": (0.5, 6.25),
    "grinding_cylindrical": (0.025, 6.25),
    "grinding_surface": (0.025, 6.25),
}

# Process accuracy achievable (P.N. Rao Vol 2 Table 3.1, ±μm)
PROCESS_ACCURACY_UM: dict[str, float] = {
    "turning": 25.0,
    "facing": 25.0,
    "boring": 25.0,
    "milling_face": 25.0,
    "milling_slot": 12.0,
    "milling_pocket": 25.0,
    "drilling": 125.0,
    "reaming": 12.0,
    "grinding_cylindrical": 6.0,
    "grinding_surface": 6.0,
}

# ---------------------------------------------------------------------------
# Force ratios for cutting force decomposition (Stephenson Ch.6 p.400)
# Rough turning: Ft : Fa : Fr = 4 : 2 : 1
# ---------------------------------------------------------------------------
FORCE_RATIO_TURNING_ROUGH = (4.0, 2.0, 1.0)   # tangential : axial : radial
FORCE_RATIO_TURNING_FINISH = (4.0, 1.5, 1.5)  # finishing: radial increases

# ---------------------------------------------------------------------------
# Milling specific energy (Ghosh & Mallik Table 4.14, J/mm³ = N/mm²)
# Useful for power estimation in milling operations
# ---------------------------------------------------------------------------
MILLING_SPECIFIC_ENERGY: dict[str, float] = {
    "Aluminum 6061": 0.8,       # Al: 0.6-1.0
    "Mild Steel IS2062": 3.5,   # Steel BHN 100: 3.5
    "Stainless Steel 304": 4.5, # higher hardness steel range
    "Brass IS319": 1.25,        # Bronze: 1.0-1.5
    "EN8 Steel": 4.0,           # Steel ~BHN 200
    "EN24 Steel": 5.0,          # Steel ~BHN 300-400
    "Copper": 1.5,              # copper alloys range
    "Cast Iron": 2.5,           # CI: 1.5-3.5
    "Titanium Grade 5": 4.5,    # similar to hard steel
}

# Milling force coefficients A and k (Ghosh & Mallik Table 4.13)
# Fc = A × t1^k (tangential force per unit width, N/mm)
MILLING_FORCE_COEFFICIENTS: dict[str, tuple[float, float]] = {
    "Mild Steel IS2062": (900.0, 0.88),
    "EN8 Steel": (1100.0, 1.06),      # alloy steel
    "EN24 Steel": (1100.0, 1.06),
    "Cast Iron": (500.0, 0.70),
    "Brass IS319": (300.0, 0.45),
    "Aluminum 6061": (250.0, 0.40),    # estimated from bronze/Al range
    "Copper": (400.0, 0.55),           # estimated
    "Stainless Steel 304": (1000.0, 1.00),  # between mild and alloy steel
    "Titanium Grade 5": (1100.0, 1.06),     # similar to alloy steel
}


# ---------------------------------------------------------------------------
# Per-material cutting parameters
# ---------------------------------------------------------------------------
CUTTING_DATA: dict[str, MaterialCuttingData] = {
    "Aluminum 6061": MaterialCuttingData(
        turning=TurningParams(
            vc_rough=400, vc_finish=500,
            f_rough=0.30, f_finish=0.10,
            ap_rough=2.0, ap_finish=0.3,
        ),
        milling=MillingParams(
            vc_rough=350, vc_finish=450,
            fz_rough=0.15, fz_finish=0.08,
            ap_rough=3.0, ap_finish=0.5,
            ae_ratio_rough=0.70, ae_ratio_finish=0.30,
        ),
        drilling=DrillingParams(vc=120, f_per_rev=0.20),
        grinding=GrindingParams(
            wheel_speed=30, infeed_rough=0.02, infeed_finish=0.005,
            traverse_rate=1.5, sparkout_passes=2,
        ),
        kp=0.25, taylor_n=0.27, taylor_c=600,
        kc1=700, mc=0.25,
        # Cross-validated: Sandvik=600, r3ditor=800, Ghosh & Mallik Uc=400-700,
        # Stephenson us=0.012-0.022 kW/cm³/min. 700 is median for wrought Al.
        shear_stress=207.0,  # Al 6061-T6 shear yield (Stephenson, Ghosh & Mallik)
    ),
    "Mild Steel IS2062": MaterialCuttingData(
        turning=TurningParams(
            vc_rough=180, vc_finish=220,
            f_rough=0.25, f_finish=0.10,
            ap_rough=2.0, ap_finish=0.3,
        ),
        milling=MillingParams(
            vc_rough=160, vc_finish=200,
            fz_rough=0.15, fz_finish=0.08,
            ap_rough=2.5, ap_finish=0.4,
            ae_ratio_rough=0.65, ae_ratio_finish=0.25,
        ),
        drilling=DrillingParams(vc=80, f_per_rev=0.18),
        grinding=GrindingParams(
            wheel_speed=30, infeed_rough=0.02, infeed_finish=0.005,
            traverse_rate=1.2, sparkout_passes=3,
        ),
        kp=0.74, taylor_n=0.23, taylor_c=300,
        kc1=1650, mc=0.25,
        # Cross-validated: Sandvik P1.2=1700, r3ditor 1018=1700,
        # Ghosh & Mallik Uc=1400 (BHN 85-200), Stephenson us=0.05-0.066.
        # 1650 correct for IS2062 E250 (~1018 equivalent).
        shear_stress=400.0,  # C25 steel tau=588 (Rao), but IS2062 is lower C → ~400
    ),
    "Stainless Steel 304": MaterialCuttingData(
        turning=TurningParams(
            vc_rough=120, vc_finish=160,
            f_rough=0.20, f_finish=0.08,
            ap_rough=1.5, ap_finish=0.25,
        ),
        milling=MillingParams(
            vc_rough=100, vc_finish=140,
            fz_rough=0.12, fz_finish=0.06,
            ap_rough=2.0, ap_finish=0.3,
            ae_ratio_rough=0.55, ae_ratio_finish=0.20,
        ),
        drilling=DrillingParams(vc=50, f_per_rev=0.12),
        grinding=GrindingParams(
            wheel_speed=25, infeed_rough=0.015, infeed_finish=0.003,
            traverse_rate=0.8, sparkout_passes=4,
        ),
        kp=0.78, taylor_n=0.22, taylor_c=200,
        kc1=2050, mc=0.25,
        # Cross-validated: Sandvik M2=2100, r3ditor=2100,
        # Stephenson us=0.055-0.09. Austenitic SS = most difficult stainless.
        shear_stress=500.0,  # austenitic SS, high work hardening
    ),
    "Brass IS319": MaterialCuttingData(
        turning=TurningParams(
            vc_rough=280, vc_finish=350,
            f_rough=0.25, f_finish=0.10,
            ap_rough=2.0, ap_finish=0.3,
        ),
        milling=MillingParams(
            vc_rough=250, vc_finish=320,
            fz_rough=0.15, fz_finish=0.08,
            ap_rough=2.5, ap_finish=0.4,
            ae_ratio_rough=0.65, ae_ratio_finish=0.25,
        ),
        drilling=DrillingParams(vc=100, f_per_rev=0.18),
        grinding=GrindingParams(
            wheel_speed=28, infeed_rough=0.02, infeed_finish=0.005,
            traverse_rate=1.5, sparkout_passes=2,
        ),
        kp=0.40, taylor_n=0.25, taylor_c=600,
        kc1=750, mc=0.25,
        # Cross-validated: Ghosh & Mallik Uc=560-830 for brass. 750 in range.
        shear_stress=180.0,  # free-cutting brass
    ),
    "EN8 Steel": MaterialCuttingData(
        turning=TurningParams(
            vc_rough=150, vc_finish=200,
            f_rough=0.25, f_finish=0.10,
            ap_rough=2.0, ap_finish=0.3,
        ),
        milling=MillingParams(
            vc_rough=130, vc_finish=180,
            fz_rough=0.12, fz_finish=0.07,
            ap_rough=2.0, ap_finish=0.3,
            ae_ratio_rough=0.60, ae_ratio_finish=0.25,
        ),
        drilling=DrillingParams(vc=70, f_per_rev=0.15),
        grinding=GrindingParams(
            wheel_speed=30, infeed_rough=0.02, infeed_finish=0.005,
            traverse_rate=1.0, sparkout_passes=3,
        ),
        kp=0.74, taylor_n=0.23, taylor_c=280,
        kc1=1700, mc=0.25,
        # EN8 = 45C8 = AISI 1045. Ghosh & Mallik: C45 tau=706 N/mm².
        # Stephenson: steel 0<Rc<45 us=0.065-0.09.
        shear_stress=706.0,  # C45 steel (Ghosh & Mallik Table 2.16 / P.N. Rao)
    ),
    "EN24 Steel": MaterialCuttingData(
        turning=TurningParams(
            vc_rough=100, vc_finish=140,
            f_rough=0.20, f_finish=0.08,
            ap_rough=1.5, ap_finish=0.25,
        ),
        milling=MillingParams(
            vc_rough=90, vc_finish=120,
            fz_rough=0.10, fz_finish=0.06,
            ap_rough=1.5, ap_finish=0.3,
            ae_ratio_rough=0.50, ae_ratio_finish=0.20,
        ),
        drilling=DrillingParams(vc=50, f_per_rev=0.12),
        grinding=GrindingParams(
            wheel_speed=28, infeed_rough=0.015, infeed_finish=0.003,
            traverse_rate=0.8, sparkout_passes=4,
        ),
        kp=0.82, taylor_n=0.22, taylor_c=200,
        kc1=1900, mc=0.25,
        # EN24 = 40NiCrMo6 = AISI 4340. P.N. Rao: AISI 4140 V*T^0.22=475.
        # EN24 is harder than 4140 → lower C. 200 is correct.
        # Ghosh & Mallik: low alloy steel tau=715 N/mm².
        shear_stress=715.0,  # low alloy steel (Ghosh & Mallik Table 2.16)
    ),
    "Copper": MaterialCuttingData(
        turning=TurningParams(
            vc_rough=200, vc_finish=280,
            f_rough=0.25, f_finish=0.10,
            ap_rough=2.0, ap_finish=0.3,
        ),
        milling=MillingParams(
            vc_rough=180, vc_finish=250,
            fz_rough=0.15, fz_finish=0.08,
            ap_rough=2.5, ap_finish=0.4,
            ae_ratio_rough=0.65, ae_ratio_finish=0.25,
        ),
        drilling=DrillingParams(vc=90, f_per_rev=0.18),
        grinding=GrindingParams(
            wheel_speed=28, infeed_rough=0.02, infeed_finish=0.005,
            traverse_rate=1.2, sparkout_passes=2,
        ),
        kp=0.35, taylor_n=0.25, taylor_c=500,
        kc1=800, mc=0.25,
        # Ghosh & Mallik Uc=900-1260 for copper alloys (higher than brass).
        # Stephenson: copper alloys RB<80 us=0.027-0.04. Pure Cu is gummy/difficult.
        shear_stress=250.0,  # pure copper, highly ductile
    ),
    "Cast Iron": MaterialCuttingData(
        turning=TurningParams(
            vc_rough=120, vc_finish=160,
            f_rough=0.25, f_finish=0.10,
            ap_rough=2.0, ap_finish=0.3,
        ),
        milling=MillingParams(
            vc_rough=110, vc_finish=150,
            fz_rough=0.15, fz_finish=0.08,
            ap_rough=2.5, ap_finish=0.4,
            ae_ratio_rough=0.65, ae_ratio_finish=0.25,
        ),
        drilling=DrillingParams(vc=70, f_per_rev=0.18),
        grinding=GrindingParams(
            wheel_speed=30, infeed_rough=0.02, infeed_finish=0.005,
            traverse_rate=1.2, sparkout_passes=3,
        ),
        kp=0.55, taylor_n=0.25, taylor_c=250,
        kc1=1100, mc=0.25,
        # Cross-validated: Ghosh & Mallik Uc=1100-1600 for CI, Stephenson us=0.044-0.08.
        # 1100 correct for gray CI class 30. P.N. Rao: tau=392 for CI.
        shear_stress=392.0,  # gray cast iron (Ghosh & Mallik / P.N. Rao Table 2.16)
    ),
    "Titanium Grade 5": MaterialCuttingData(
        turning=TurningParams(
            vc_rough=45, vc_finish=65,
            f_rough=0.15, f_finish=0.06,
            ap_rough=1.0, ap_finish=0.2,
        ),
        milling=MillingParams(
            vc_rough=40, vc_finish=55,
            fz_rough=0.08, fz_finish=0.04,
            ap_rough=1.0, ap_finish=0.2,
            ae_ratio_rough=0.40, ae_ratio_finish=0.15,
        ),
        drilling=DrillingParams(vc=25, f_per_rev=0.08),
        grinding=GrindingParams(
            wheel_speed=20, infeed_rough=0.010, infeed_finish=0.002,
            traverse_rate=0.5, sparkout_passes=5,
        ),
        kp=0.65, taylor_n=0.17, taylor_c=100,
        kc1=1420, mc=0.23,
        # Cross-validated: Sandvik S4=1500, r3ditor=1500,
        # Stephenson us=0.053-0.066. Ti is notoriously difficult.
        shear_stress=550.0,  # Ti-6Al-4V shear yield
    ),
}


# ---------------------------------------------------------------------------
# Machinability ratings (AISI 1212 = 1.00 baseline)
# Source: Carbide Depot / Machinery's Handbook, cross-validated with pymachining
# Higher = easier to machine. Used for fallback speed scaling.
# ---------------------------------------------------------------------------
MACHINABILITY_RATINGS: dict[str, float] = {
    # Carbon steels
    "1015": 0.72, "1018": 0.78, "1020": 0.72, "1030": 0.70,
    "1040": 0.64, "1045": 0.57, "1050": 0.54, "1095": 0.42,
    "1117": 0.91, "1137": 0.72, "1141": 0.70, "1144": 0.76,
    "1212": 1.00, "1213": 1.36, "12L14": 1.70, "1215": 1.36,
    # Alloy steels
    "4130": 0.72, "4140": 0.66, "4150": 0.60, "4340": 0.57,
    "4620": 0.66, "8620": 0.66, "52100": 0.40, "6150": 0.60,
    # Stainless steels
    "302": 0.45, "303": 0.78, "304": 0.45, "316": 0.45,
    "321": 0.36, "347": 0.36, "410": 0.54, "416": 1.10,
    "420": 0.45, "430": 0.54, "431": 0.45, "440A": 0.45,
    "15-5PH": 0.48, "17-4PH": 0.48, "A286": 0.33,
    # Tool steels
    "A-2": 0.42, "D-2": 0.27, "D-3": 0.27, "M-2": 0.39, "O-1": 0.42,
    # Cast iron (ASTM class)
    "CI-20": 0.73, "CI-25": 0.55, "CI-30": 0.48, "CI-35": 0.48,
    "CI-40": 0.48, "CI-45": 0.36, "CI-50": 0.36,
    # Aluminum and copper
    "Al-cold-drawn": 3.60, "Al-cast": 4.50, "Al-die-cast": 0.76,
    "Mg-cold-drawn": 4.80, "Brass-free-cutting": 1.00, "Copper": 0.60,
    # Indian grades (mapped to AISI equivalents)
    "IS2062-E250": 0.72, "IS2062-E350": 0.66, "IS2062-E450": 0.57,
    "EN8": 0.57, "EN19": 0.57, "EN24": 0.42, "EN31": 0.40,
    "EN36": 0.51, "EN47": 0.54,
}


def get_cutting_data(material_name: str | None = None,
                     machinability: float = 0.5) -> MaterialCuttingData:
    """Get cutting parameters for a material.

    If material_name is provided and found in CUTTING_DATA, returns exact data.
    Otherwise, derives approximate data by scaling from a mild steel baseline
    using the machinability factor (0-1, higher = easier to machine).
    """
    if material_name and material_name in CUTTING_DATA:
        return CUTTING_DATA[material_name]

    # Fallback: scale from mild steel baseline using machinability
    # machinability=1.0 → aluminum-like speeds; 0.25 → titanium-like
    base = CUTTING_DATA["Mild Steel IS2062"]
    scale = max(machinability, 0.15) / 0.6  # normalize to mild steel's 0.6

    return MaterialCuttingData(
        turning=TurningParams(
            vc_rough=base.turning.vc_rough * scale,
            vc_finish=base.turning.vc_finish * scale,
            f_rough=base.turning.f_rough * min(scale, 1.2),
            f_finish=base.turning.f_finish,
            ap_rough=base.turning.ap_rough * min(scale, 1.2),
            ap_finish=base.turning.ap_finish,
        ),
        milling=MillingParams(
            vc_rough=base.milling.vc_rough * scale,
            vc_finish=base.milling.vc_finish * scale,
            fz_rough=base.milling.fz_rough * min(scale, 1.2),
            fz_finish=base.milling.fz_finish,
            ap_rough=base.milling.ap_rough * min(scale, 1.2),
            ap_finish=base.milling.ap_finish,
            ae_ratio_rough=base.milling.ae_ratio_rough,
            ae_ratio_finish=base.milling.ae_ratio_finish,
        ),
        drilling=DrillingParams(
            vc=base.drilling.vc * scale,
            f_per_rev=base.drilling.f_per_rev * min(scale, 1.2),
        ),
        grinding=base.grinding,  # grinding params are less material-sensitive
        kp=base.kp / max(scale, 0.3),  # harder materials need more power
        taylor_n=0.25,
        taylor_c=base.taylor_c * scale,
        kc1=base.kc1 / max(scale, 0.3),  # higher for harder materials
        mc=0.25,
    )


def calculate_tool_life_min(vc: float, taylor_n: float, taylor_c: float) -> float:
    """Taylor tool life equation: V × T^n = C → T = (C/V)^(1/n).

    Returns tool life in minutes. Clamped to [1, 300] for sanity.
    """
    if vc <= 0 or taylor_c <= 0:
        return 60.0
    ratio = taylor_c / vc
    tool_life = ratio ** (1.0 / taylor_n)
    return max(1.0, min(tool_life, 300.0))


def calculate_tool_cost_per_min(vc: float, taylor_n: float,
                                taylor_c: float) -> float:
    """Tool wear cost per minute of cutting (₹/min).

    Based on Taylor tool life and carbide insert edge cost.
    """
    tool_life = calculate_tool_life_min(vc, taylor_n, taylor_c)
    return CARBIDE_EDGE_COST_INR / tool_life


def calculate_cutting_power_kw(mrr_cm3_per_min: float, kp: float) -> float:
    """Actual cutting power from MRR and specific cutting force.

    P (kW) = Kp × MRR (cm³/min)
    Divide by machine efficiency to get spindle power required.
    """
    return kp * mrr_cm3_per_min / MACHINE_EFFICIENCY


def calculate_sandvik_power_kw(vc: float, ap: float, fn: float,
                               kc1: float, mc: float,
                               kapr: float = 95.0,
                               gamma0: float = 6.0) -> float:
    """Sandvik power formula for turning (more precise than Kp×MRR).

    Pc = (vc × ap × fn × kc) / (60 × 10³)  [kW]
    kc = kc1 × (1/hm)^mc × (1 - gamma0/100)
    hm = fn × sin(KAPR)

    Args:
        vc: cutting speed (m/min)
        ap: depth of cut (mm)
        fn: feed per revolution (mm/rev)
        kc1: specific cutting force at 1mm chip thickness (N/mm²)
        mc: chip thickness exponent (typically 0.25)
        kapr: entering angle (degrees), default 95°
        gamma0: effective rake angle (degrees), default 6°

    Returns:
        Net cutting power in kW.
    """
    import math
    hm = fn * math.sin(math.radians(kapr))
    if hm <= 0:
        return 0.0
    kc = kc1 * (1.0 / hm) ** mc * (1.0 - gamma0 / 100.0)
    return (vc * ap * fn * kc) / (60 * 1e3)


def estimate_surface_roughness_um(feed_mm_per_rev: float,
                                  nose_radius_mm: float = DEFAULT_NOSE_RADIUS_MM,
                                  material_name: str | None = None) -> float:
    """Estimate achievable surface roughness Ra (μm).

    Rmax = f² / (8 × rn)  [mm]  (Ghosh & Mallik Eq.4.77, Stephenson Eq.10.9)
    Ra ≈ Rmax / 4  [mm]  →  Ra_μm = f² × 1000 / (32 × rn)
    Ra_actual = Ra_geometric × material_correction_factor

    Sources: Stephenson & Agapiou p.583-585, Ghosh & Mallik p.271
    """
    if feed_mm_per_rev <= 0 or nose_radius_mm <= 0:
        return 0.0
    ra_geo_um = feed_mm_per_rev**2 * 1000.0 / (32.0 * nose_radius_mm)
    correction = RA_CORRECTION_FACTOR.get(material_name or "", 1.25)
    return ra_geo_um * correction


def calculate_corrected_kc(kc1: float, mc: float, chip_thickness_mm: float,
                           rake_angle_deg: float = 6.0,
                           kw: float = KW_DEFAULT,
                           ksp: float = KSP_TURNING) -> float:
    """Kienzle-corrected specific cutting force (N/mm²).

    kc = kc1 × (1/h)^mc × (1 - γ₀/100) × Kw × Ksp

    Sources:
    - Sandvik power formula (base kc1 × chip thickness correction)
    - CamScripts/Europa-Lehrmittel (Kw, Ksp correction factors)
    - Stephenson Ch.6 (force coefficient validation)
    """
    if chip_thickness_mm <= 0:
        return kc1
    kc = kc1 * (1.0 / chip_thickness_mm) ** mc
    kc *= (1.0 - rake_angle_deg / 100.0)  # rake angle correction
    kc *= kw   # tool wear correction
    kc *= ksp  # chip compression correction
    return kc


# Sandvik tool life correction factors (base = 15 min)
# Multiply recommended Vc by this factor to achieve target tool life
TOOL_LIFE_CORRECTION: dict[int, float] = {
    10: 1.11,
    15: 1.00,  # base
    20: 0.93,
    25: 0.88,
    30: 0.84,
    45: 0.75,
    60: 0.70,
}
