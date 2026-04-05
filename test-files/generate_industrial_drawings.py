"""Generate realistic Indian industrial manufacturing part DXF drawings.

Parts chosen from Defense / Aerospace / Automotive sectors:
  1. crankpin_journal.dxf    — EN8 steel turned shaft, automotive
  2. defense_bracket.dxf    — EN19 steel milled bracket, defense
  3. hydraulic_piston.dxf   — EN24 steel hydraulic piston, industrial
  4. spindle_nose.dxf       — EN24 steel machine tool spindle nose
  5. turbine_disc_spacer.dxf — Inconel 718 aerospace spacer

Ground truth embedded in each drawing via title block + dimension callouts.
Run: python test-files/generate_industrial_drawings.py
"""

from pathlib import Path
import ezdxf
from ezdxf.enums import TextEntityAlignment

OUT = Path(__file__).parent / "dxf"
OUT.mkdir(exist_ok=True)


def _add_dim(msp, x1, y1, x2, y2, dim_y, override=None):
    """Add a horizontal linear dimension."""
    try:
        d = msp.add_linear_dim(
            base=(x1, dim_y),
            p1=(x1, y1),
            p2=(x2, y2),
            angle=0,
        )
        d.render()
    except Exception:
        pass  # tolerate ezdxf version differences


def _add_label(msp, x, y, text, height=2.5):
    msp.add_text(text, dxfattribs={"insert": (x, y), "height": height})


# ─────────────────────────────────────────────────────────────────────────────
# 1. Crankpin Journal — EN8 Steel, Ø55mm, L=90mm, automotive
# ─────────────────────────────────────────────────────────────────────────────
def make_crankpin_journal():
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()

    # Turned profile (half-section, symmetric about X-axis)
    # OD=55mm (r=27.5), shoulders at D40 (r=20), L=90
    points = [
        (0, 20), (0, 27.5), (90, 27.5), (90, 20),  # main journal OD=55
    ]
    msp.add_lwpolyline([(0, -20), (0, -27.5), (90, -27.5), (90, -20), (90, 0), (0, 0)],
                       close=False)
    msp.add_lwpolyline([(0, 0), (0, 27.5), (90, 27.5), (90, 0)], close=False)

    # Centreline
    msp.add_line((0, 0), (100, 0))

    # Oil hole: D8mm at centre
    msp.add_circle((45, 0), 4)
    _add_label(msp, 43, 5, "D8 OIL HOLE")

    # Fillet R2 at shoulders (symbolic)
    msp.add_arc((0, 25), 2, 90, 180)
    msp.add_arc((90, 25), 2, 0, 90)

    # Keyway 14x5mm at left end
    msp.add_lwpolyline([(3, 20), (3, 25), (17, 25), (17, 20)], close=True)
    _add_label(msp, 4, 22, "14x5 KEYWAY")

    # Dimensions
    msp.add_linear_dim(base=(45, 35), p1=(0, 0), p2=(90, 0), angle=0).render()  # L=90
    msp.add_linear_dim(base=(-15, 15), p1=(0, 0), p2=(0, 27.5), angle=90).render()  # R=27.5

    # Tolerance callout
    _add_label(msp, 30, 30, "Ø55h6 (+0.000/-0.019)")
    _add_label(msp, 2, -8, "TOTAL LENGTH = 90mm")

    # Title block
    _add_label(msp, 0, -40, "DRAWING: Crankpin Journal — Automotive Crank Assembly")
    _add_label(msp, 0, -46, "MATERIAL: EN8 Steel (IS 080M40)")
    _add_label(msp, 0, -52, "HEAT TREATMENT: Induction Hardened 58-62 HRC")
    _add_label(msp, 0, -58, "SURFACE FINISH: Ra 0.4 on journal dia, Ra 1.6 on faces")
    _add_label(msp, 0, -64, "TOLERANCE: ±0.02 general, h6 on journal Ø55")
    _add_label(msp, 0, -70, "QTY: 6 per engine")
    _add_label(msp, 0, -76, "DRG NO: CJ-3001-Rev2")

    # GD&T
    _add_label(msp, 50, 22, "⌭ 0.005 A")   # cylindricity
    _add_label(msp, 50, 19, "↗ 0.010 A")   # circular runout

    doc.saveas(OUT / "crankpin_journal.dxf")
    print("  crankpin_journal.dxf saved  [OD=55mm, L=90mm, EN8]")


# ─────────────────────────────────────────────────────────────────────────────
# 2. Defense Mounting Bracket — EN19 Steel, 180x120x25mm, milled
# ─────────────────────────────────────────────────────────────────────────────
def make_defense_bracket():
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()

    # Outer profile 180x120
    msp.add_lwpolyline([(0, 0), (180, 0), (180, 120), (0, 120)], close=True)

    # Central pocket 80x50 at (50, 35)
    msp.add_lwpolyline([(50, 35), (130, 35), (130, 85), (50, 85)], close=True)
    _add_label(msp, 55, 55, "POCKET 80x50x15 DEEP")

    # 4x M10 through-holes on corners, PCD 160x100
    holes = [(10, 10), (170, 10), (10, 110), (170, 110)]
    for cx, cy in holes:
        msp.add_circle((cx, cy), 5)

    # 2x M16 mounting holes at 90x60
    mount_holes = [(40, 60), (140, 60)]
    for cx, cy in mount_holes:
        msp.add_circle((cx, cy), 8)
    _add_label(msp, 35, 52, "2xM16 THRU")

    # Slot 30x12 at bottom
    msp.add_lwpolyline([(75, 5), (105, 5), (105, 17), (75, 17)], close=True)
    _add_label(msp, 76, 9, "SLOT 30x12")

    # Dimensions
    msp.add_linear_dim(base=(90, -15), p1=(0, 0), p2=(180, 0), angle=0).render()
    msp.add_linear_dim(base=(-15, 60), p1=(0, 0), p2=(0, 120), angle=90).render()

    # Title block
    _add_label(msp, 0, -20, "DRAWING: Defense Equipment Mounting Bracket")
    _add_label(msp, 0, -26, "MATERIAL: EN19 Steel (4140) — Hardened & Tempered 28-32 HRC")
    _add_label(msp, 0, -32, "DIMENSIONS: 180 x 120 x 25 mm")
    _add_label(msp, 0, -38, "SURFACE: Hard Chrome Plating 20-25 micron")
    _add_label(msp, 0, -44, "TOLERANCE: ±0.05 unless noted")
    _add_label(msp, 0, -50, "DRG NO: DMB-4502-A")

    # GD&T
    _add_label(msp, 90, 125, "⊥ 0.05 A")   # perpendicularity
    _add_label(msp, 120, 125, "□ 0.02")    # flatness

    doc.saveas(OUT / "defense_bracket.dxf")
    print("  defense_bracket.dxf saved  [180x120x25, EN19, hard chrome]")


# ─────────────────────────────────────────────────────────────────────────────
# 3. Hydraulic Piston — EN24 Steel, Ø65mm, L=140mm, O-ring grooves
# ─────────────────────────────────────────────────────────────────────────────
def make_hydraulic_piston():
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()

    # Piston body OD=65 (r=32.5), L=140
    msp.add_line((0, 0), (140, 0))       # centreline
    msp.add_line((0, 32.5), (140, 32.5))   # top profile
    msp.add_line((0, -32.5), (140, -32.5)) # bottom profile
    msp.add_line((0, -32.5), (0, 32.5))    # left face
    msp.add_line((140, -32.5), (140, 32.5)) # right face

    # Rod end bore Ø30mm (r=15) at left
    msp.add_circle((15, 0), 15)
    _add_label(msp, 10, 17, "Ø30H7")

    # O-ring grooves: 2 grooves at x=40 and x=90, 4mm wide, 3mm deep
    for gx in [40, 90]:
        msp.add_lwpolyline([(gx, 29.5), (gx+4, 29.5), (gx+4, 32.5), (gx, 32.5)], close=True)
        msp.add_lwpolyline([(gx, -29.5), (gx+4, -29.5), (gx+4, -32.5), (gx, -32.5)], close=True)
    _add_label(msp, 38, 26, "2x O-RING GROOVE\n4mm W x 3mm DEEP")

    # M20x1.5 thread at right end, 25mm long
    msp.add_text("M20x1.5 - 6g  25 DEEP", dxfattribs={"insert": (112, 20), "height": 2.5})

    # Dimensions
    msp.add_linear_dim(base=(70, 45), p1=(0, 0), p2=(140, 0), angle=0).render()
    msp.add_linear_dim(base=(-15, 16), p1=(0, 0), p2=(0, 32.5), angle=90).render()

    # Title block
    _add_label(msp, 0, -50, "DRAWING: Hydraulic Piston — Double-Acting Cylinder")
    _add_label(msp, 0, -56, "MATERIAL: EN24 Steel (817M40) — QT Condition")
    _add_label(msp, 0, -62, "DIMENSIONS: OD Ø65mm, Bore Ø30mm, Length 140mm")
    _add_label(msp, 0, -68, "SURFACE: Hard Chrome 50 micron on Ø65 — Ground Ra 0.2")
    _add_label(msp, 0, -74, "TOLERANCE: Ø65f7 on OD, Ø30H7 on bore")
    _add_label(msp, 0, -80, "PRESSURE RATING: 350 bar (5000 psi)")
    _add_label(msp, 0, -86, "DRG NO: HYD-P6501-R3")

    # GD&T
    _add_label(msp, 60, 36, "⌭ 0.005 A")
    _add_label(msp, 60, 33, "○ 0.003 A")

    doc.saveas(OUT / "hydraulic_piston.dxf")
    print("  hydraulic_piston.dxf saved  [OD=65mm, L=140mm, EN24, hard chrome]")


# ─────────────────────────────────────────────────────────────────────────────
# 4. Machine Tool Spindle Nose — EN24 Steel, Ø100mm, L=95mm, precision
# ─────────────────────────────────────────────────────────────────────────────
def make_spindle_nose():
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()

    # Stepped profile: Ø100 main, Ø80 journal, Ø60 taper
    msp.add_line((0, 0), (95, 0))   # centreline

    # Ø100 flange (0-15mm)
    msp.add_line((0, 50), (15, 50))
    msp.add_line((0, -50), (15, -50))
    msp.add_line((0, -50), (0, 50))

    # Ø80 journal (15-60mm)
    msp.add_line((15, 40), (60, 40))
    msp.add_line((15, -40), (60, -40))
    msp.add_line((15, 40), (15, 50))
    msp.add_line((15, -40), (15, -50))

    # Ø60 nose taper (60-95mm) — tapered 7:24
    msp.add_line((60, 40), (60, 30))
    msp.add_line((60, -40), (60, -30))
    msp.add_line((60, 30), (95, 23))   # 7:24 taper
    msp.add_line((60, -30), (95, -23))
    msp.add_line((95, 23), (95, -23))

    # Center bore Ø35mm (r=17.5)
    msp.add_circle((10, 0), 17.5)
    _add_label(msp, 6, 19, "Ø35H6")

    # 4x M12 bolt holes on Ø80 PCD on flange face
    for angle_deg in [45, 135, 225, 315]:
        import math
        cx = 7.5 + 40 * math.cos(math.radians(angle_deg))
        cy = 40 * math.sin(math.radians(angle_deg))
        msp.add_circle((cx, cy), 6)
    _add_label(msp, -5, 55, "4xM12 EQ.SP. ON Ø80 PCD")

    # Dimensions
    msp.add_linear_dim(base=(47, 60), p1=(0, 0), p2=(95, 0), angle=0).render()
    msp.add_linear_dim(base=(-15, 25), p1=(0, 0), p2=(0, 50), angle=90).render()

    # Title block
    _add_label(msp, 0, -30, "DRAWING: Lathe Spindle Nose — Precision CNC Machine Tool")
    _add_label(msp, 0, -36, "MATERIAL: EN24 Steel (817M40) — Case Hardened 60-62 HRC")
    _add_label(msp, 0, -42, "DIMENSIONS: Ø100mm flange, Ø80mm journal, 7:24 taper, L=95mm")
    _add_label(msp, 0, -48, "SURFACE: Ground Ra 0.2 on journal, lapped Ra 0.1 on taper")
    _add_label(msp, 0, -54, "TOLERANCE: p5 on journal Ø80, H6 on bore Ø35")
    _add_label(msp, 0, -60, "DRG NO: SPL-100-7/24")

    _add_label(msp, 20, 44, "⊥ 0.003 A")
    _add_label(msp, 20, 41, "↗ 0.002 A")

    doc.saveas(OUT / "spindle_nose.dxf")
    print("  spindle_nose.dxf saved  [OD=100mm, L=95mm, EN24, 7:24 taper]")


# ─────────────────────────────────────────────────────────────────────────────
# 5. Turbine Disc Spacer — Inconel 718, Ø220mm, L=40mm, aerospace
# ─────────────────────────────────────────────────────────────────────────────
def make_turbine_disc_spacer():
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()

    # Annular disc: OD=220mm (r=110), ID=90mm (r=45), thickness=40mm
    msp.add_circle((0, 0), 110)   # OD
    msp.add_circle((0, 0), 45)    # ID bore

    # 12x Ø12mm cooling holes on Ø170 PCD
    import math
    for i in range(12):
        angle = math.radians(i * 30)
        cx = 85 * math.cos(angle)
        cy = 85 * math.sin(angle)
        msp.add_circle((cx, cy), 6)
    _add_label(msp, -30, 90, "12x Ø12 EQ.SP. ON Ø170 PCD")

    # 6x M8 blind tapped holes (Ø160 PCD, alternating with coolant holes)
    for i in range(6):
        angle = math.radians(i * 60 + 15)
        cx = 80 * math.cos(angle)
        cy = 80 * math.sin(angle)
        msp.add_circle((cx, cy), 4)
    _add_label(msp, 50, 85, "6xM8x15 DEEP EQ.SP.")

    # Slot/keyway on ID
    msp.add_lwpolyline([(-4, 45), (4, 45), (4, 58), (-4, 58)], close=True)
    _add_label(msp, -20, 55, "8x7 KEYWAY")

    # Dimensions
    msp.add_linear_dim(base=(0, 130), p1=(-110, 0), p2=(110, 0), angle=0).render()  # OD
    msp.add_linear_dim(base=(0, 120), p1=(-45, 0), p2=(45, 0), angle=0).render()    # ID

    # Title block
    _add_label(msp, -110, -130, "DRAWING: Turbine Disc Spacer — Aero Engine Stage 3")
    _add_label(msp, -110, -138, "MATERIAL: Inconel 718 (AMS 5663) — Solution Annealed + Aged")
    _add_label(msp, -110, -146, "DIMENSIONS: OD Ø220mm, ID Ø90mm, Thickness 40mm")
    _add_label(msp, -110, -154, "SURFACE: Shot peened, EDM holes, no burrs")
    _add_label(msp, -110, -162, "TOLERANCE: OD H6, ID H7, hole position ±0.05")
    _add_label(msp, -110, -170, "INSPECTION: 100% CMM, FPI (Fluorescent Penetrant)")
    _add_label(msp, -110, -178, "DRG NO: TDS-220-GEN3-IN718")

    _add_label(msp, 80, 115, "⌖ Ø0.05 A B")
    _add_label(msp, 80, 110, "⊥ 0.02 A")

    doc.saveas(OUT / "turbine_disc_spacer.dxf")
    print("  turbine_disc_spacer.dxf saved  [OD=220mm, ID=90mm, Inconel 718]")


if __name__ == "__main__":
    print("Generating real-industry DXF drawings...")
    make_crankpin_journal()
    make_defense_bracket()
    make_hydraulic_piston()
    make_spindle_nose()
    make_turbine_disc_spacer()
    print(f"Done. Files in {OUT}/")
