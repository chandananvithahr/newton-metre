"""
Generate 3 realistic engineering drawing PDFs for Costimize demo.
Parts: turned shaft, sheet metal bracket, milled housing block.
"""

from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
import math

W, H = landscape(A3)

# ── Colour palette ────────────────────────────────────────────────────────────
BLACK   = colors.black
BLUE    = HexColor("#1a3a6b")
GREY    = HexColor("#cccccc")
LGREY   = HexColor("#f2f2f2")
DKGREY  = HexColor("#555555")


def title_block(c, part_no, part_name, material, scale, revision,
                drawn_by="C.N.", checked_by="A.K.", approved_by="R.M.",
                company="AI.Procurve / Costimize Demo",
                dwg_no=None, sheet="1 of 1"):
    """Draw a standard title block in the bottom-right corner."""
    bx = W - 180*mm
    by = 0
    bw = 180*mm
    bh = 50*mm

    c.setLineWidth(0.5)
    c.setFillColor(LGREY)
    c.rect(bx, by, bw, bh, fill=1, stroke=0)

    # border
    c.setStrokeColor(BLACK)
    c.setLineWidth(0.8)
    c.rect(bx, by, bw, bh, fill=0, stroke=1)

    # divider lines
    col1 = bx + 55*mm
    col2 = bx + 110*mm
    col3 = bx + 145*mm

    row4 = by + 38*mm
    row3 = by + 28*mm
    row2 = by + 18*mm
    row1 = by + 9*mm

    for x in [col1, col2, col3]:
        c.line(x, by, x, by+bh)
    for y in [row1, row2, row3, row4]:
        c.line(bx, y, bx+bw, y)

    def cell(x, y, w, h, label, value, label_size=5, value_size=8):
        c.setFont("Helvetica", label_size)
        c.setFillColor(DKGREY)
        c.drawString(x+1*mm, y+h-4*mm, label)
        c.setFont("Helvetica-Bold", value_size)
        c.setFillColor(BLACK)
        c.drawString(x+1*mm, y+1*mm, value)

    # Row 4 — part name spans full width
    c.setFillColor(BLUE)
    c.rect(bx, row4, bw, bh-row4+by, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.white)
    c.drawCentredString(bx + bw/2, row4 + (bh-row4)/2 - 2*mm, part_name)
    c.setFont("Helvetica", 7)
    c.drawCentredString(bx + bw/2, row4 + 2*mm, company)

    # Row 3
    cell(bx,   row3, col1-bx,    row4-row3, "PART NO.", part_no)
    cell(col1, row3, col2-col1,  row4-row3, "MATERIAL", material)
    cell(col2, row3, col3-col2,  row4-row3, "SCALE", scale)
    cell(col3, row3, bx+bw-col3, row4-row3, "REV.", revision)

    # Row 2
    cell(bx,   row2, col1-bx,    row3-row2, "DRAWN BY", drawn_by)
    cell(col1, row2, col2-col1,  row3-row2, "CHECKED", checked_by)
    cell(col2, row2, col3-col2,  row3-row2, "APPROVED", approved_by)
    cell(col3, row2, bx+bw-col3, row3-row2, "DWG NO.", dwg_no or part_no)

    # Row 1
    cell(bx,   row1, col1-bx,    row2-row1, "DATE", "30-03-2026")
    cell(col1, row1, col2-col1,  row2-row1, "SHEET", sheet)
    cell(col2, row1, col3-col2,  row2-row1, "PROJECTION", "1st Angle ⊕")
    cell(col3, row1, bx+bw-col3, row2-row1, "UNIT", "mm")

    # Row 0
    cell(bx, by, bw, row1-by, "NOTES",
         "ALL DIMENSIONS IN mm  |  GENERAL TOL: ±0.1  |  SURFACE FINISH: Ra 3.2 UNLESS NOTED")


def notes_box(c, notes, x, y, w=90*mm):
    """Draw a notes box."""
    lh = 5*mm
    bh = (len(notes) + 1) * lh + 4*mm
    c.setStrokeColor(BLACK)
    c.setLineWidth(0.5)
    c.setFillColor(LGREY)
    c.rect(x, y - bh, w, bh, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(BLACK)
    c.drawString(x + 2*mm, y - lh, "NOTES:")
    c.setFont("Helvetica", 6.5)
    for i, note in enumerate(notes):
        c.drawString(x + 2*mm, y - lh*(i+2) - 1*mm, note)


def border(c):
    """Draw sheet border and corner marks."""
    m = 10*mm
    c.setStrokeColor(BLACK)
    c.setLineWidth(1.2)
    c.rect(m, m, W - 2*m, H - 2*m, fill=0, stroke=1)
    # tick marks
    c.setLineWidth(0.4)
    for frac in [0.25, 0.5, 0.75]:
        c.line(0, H*frac, m, H*frac)
        c.line(W-m, H*frac, W, H*frac)
        c.line(W*frac, 0, W*frac, m)
        c.line(W*frac, H-m, W*frac, H)


def dim_horizontal(c, x1, y, x2, text, above=True, offset=8*mm):
    """Draw horizontal dimension line with text."""
    dy = offset if above else -offset
    ext = 3*mm
    c.setStrokeColor(BLACK)
    c.setLineWidth(0.35)
    # extension lines
    c.line(x1, y, x1, y + dy + (ext if above else -ext))
    c.line(x2, y, x2, y + dy + (ext if above else -ext))
    # dim line with arrows
    yd = y + dy
    c.line(x1, yd, x2, yd)
    _arrowhead(c, x1, yd, "left")
    _arrowhead(c, x2, yd, "right")
    c.setFont("Helvetica", 6)
    c.setFillColor(BLACK)
    c.drawCentredString((x1+x2)/2, yd + 1.5*mm if above else yd - 4*mm, text)


def dim_vertical(c, x, y1, y2, text, right=True, offset=8*mm):
    """Draw vertical dimension line with text."""
    dx = offset if right else -offset
    ext = 3*mm
    c.setStrokeColor(BLACK)
    c.setLineWidth(0.35)
    c.line(x, y1, x + dx + (ext if right else -ext), y1)
    c.line(x, y2, x + dx + (ext if right else -ext), y2)
    xd = x + dx
    c.line(xd, y1, xd, y2)
    _arrowhead(c, xd, y1, "down")
    _arrowhead(c, xd, y2, "up")
    c.setFont("Helvetica", 6)
    c.setFillColor(BLACK)
    c.saveState()
    c.translate(xd + (2.5*mm if right else -5*mm), (y1+y2)/2)
    c.rotate(90)
    c.drawCentredString(0, 0, text)
    c.restoreState()


def _arrowhead(c, x, y, direction, size=2.5*mm):
    p = c.beginPath()
    if direction == "left":
        p.moveTo(x, y)
        p.lineTo(x + size, y + size*0.4)
        p.lineTo(x + size, y - size*0.4)
    elif direction == "right":
        p.moveTo(x, y)
        p.lineTo(x - size, y + size*0.4)
        p.lineTo(x - size, y - size*0.4)
    elif direction == "up":
        p.moveTo(x, y)
        p.lineTo(x - size*0.4, y - size)
        p.lineTo(x + size*0.4, y - size)
    elif direction == "down":
        p.moveTo(x, y)
        p.lineTo(x - size*0.4, y + size)
        p.lineTo(x + size*0.4, y + size)
    p.close()
    c.setFillColor(BLACK)
    c.drawPath(p, fill=1, stroke=0)


def centre_line(c, x1, y1, x2, y2):
    """Draw a centre line (dash-dot pattern)."""
    c.setStrokeColor(DKGREY)
    c.setLineWidth(0.3)
    c.setDash([8, 2, 2, 2])
    c.line(x1, y1, x2, y2)
    c.setDash([])


def hidden_line(c, x1, y1, x2, y2):
    c.setStrokeColor(BLACK)
    c.setLineWidth(0.35)
    c.setDash([4, 2])
    c.line(x1, y1, x2, y2)
    c.setDash([])


def solid(c):
    c.setStrokeColor(BLACK)
    c.setLineWidth(0.7)
    c.setDash([])


# ═══════════════════════════════════════════════════════════════════════════════
# DRAWING 1 — TURNED SHAFT (CNC Turning, EN8 Steel)
# ═══════════════════════════════════════════════════════════════════════════════

def draw_turned_shaft(filename):
    c = canvas.Canvas(filename, pagesize=landscape(A3))

    border(c)
    title_block(c,
                part_no="CPT-001-A",
                part_name="STEPPED SHAFT — CNC TURNED",
                material="EN8 / IS 1570 Gr.C45 STEEL",
                scale="1:2",
                revision="A",
                dwg_no="AIP-CPT-001")

    # ── Front view (orthographic) — stepped shaft ────────────────────────────
    # Shaft segments (left to right):
    # Seg A: Ø20 × 30mm  (thread end M20×1.5)
    # Seg B: Ø30 × 10mm  (shoulder)
    # Seg C: Ø40 × 80mm  (main body)
    # Seg D: Ø30 × 10mm  (shoulder)
    # Seg E: Ø25 × 40mm  (keyway end)
    # Total length = 170mm

    ox = 55*mm          # origin X (left end of shaft)
    oy = H/2 + 20*mm    # centre line Y
    sc = 2.0            # scale factor (1:2 drawing)

    def sx(v): return ox + v/sc * mm
    def sy(v): return oy + v/sc * mm

    # Centre line
    centre_line(c, ox - 10*mm, oy, sx(185), oy)

    # Segment boundaries (mm from left)
    segs = [
        (0,   30,  20),   # A: M20 thread stub
        (30,  40,  30),   # B: shoulder
        (40, 120,  40),   # C: main body
        (120, 130, 30),   # D: shoulder
        (130, 170, 25),   # E: keyway end
    ]

    solid(c)
    for x1, x2, dia in segs:
        r = dia / 2
        # top line
        c.line(sx(x1), sy(r), sx(x2), sy(r))
        # bottom line
        c.line(sx(x1), sy(-r), sx(x2), sy(-r))

    # Vertical shoulder lines
    transitions = [
        (0,  20, 20),    # left face, seg A top/bot
        (30, 20, 30),
        (30, 30, 20),
        (40, 30, 40),    # left shoulder
        (40, 40, 30),
        (120, 40, 30),   # right shoulder
        (120, 30, 40),
        (130, 30, 25),
        (130, 25, 30),
        (170, 25, 25),   # right face
    ]
    for xpos, r1, r2 in transitions:
        c.line(sx(xpos), sy(r1/2), sx(xpos), sy(-r1/2))
        if r1 != r2:
            c.line(sx(xpos), sy(r2/2), sx(xpos), sy(-r2/2))

    # Left face full vertical line
    c.line(sx(0), sy(10), sx(0), sy(-10))
    # Right face full vertical line
    c.line(sx(170), sy(12.5), sx(170), sy(-12.5))

    # ── Thread annotation on seg A ─────
    c.setFont("Helvetica", 6.5)
    c.setFillColor(BLACK)
    c.drawCentredString(sx(15), sy(14), "M20×1.5-6g")

    # ── Keyway on seg E (hidden lines + annotation) ────
    kw = 8   # keyway width mm
    kd = 4   # keyway depth mm
    hidden_line(c, sx(130), sy(-kw/2), sx(170), sy(-kw/2))
    hidden_line(c, sx(130), sy(kw/2),  sx(170), sy(kw/2))
    c.setFont("Helvetica", 6)
    c.setFillColor(DKGREY)
    c.drawCentredString(sx(150), sy(-16), "KEYWAY 8×4 DIN 6885-A")

    # ── Dimensions ────────────────────────────────────────────────────────────
    dim_dy = 18*mm   # above centre

    # Overall length
    dim_horizontal(c, sx(0), oy + sy(20)-oy, sx(170),
                   "170", above=True, offset=22*mm)

    # Seg A length
    dim_horizontal(c, sx(0), oy, sx(30), "30", above=False, offset=12*mm)

    # Seg C length (main body)
    dim_horizontal(c, sx(40), oy, sx(120), "80", above=False, offset=12*mm)

    # Seg E length
    dim_horizontal(c, sx(130), oy, sx(170), "40", above=False, offset=12*mm)

    # Dia annotations (leaders)
    c.setFont("Helvetica", 7)
    c.setFillColor(BLACK)
    # Ø40 main body
    c.drawString(sx(75), sy(24), "Ø40 h6")
    c.setLineWidth(0.3)
    c.line(sx(80), sy(23), sx(80), sy(20))

    # Ø30 shoulder
    c.drawString(sx(31), sy(19), "Ø30")
    c.line(sx(35), sy(18), sx(35), sy(15))

    # Ø25 end
    c.drawString(sx(148), sy(16), "Ø25 h7")
    c.line(sx(155), sy(15), sx(155), sy(12.5))

    # ── Tolerance / Surface finish callouts ───────────────────────────────────
    c.setFont("Helvetica", 6.5)
    c.setFillColor(DKGREY)
    c.drawString(sx(75), sy(-26), "Ra 1.6 ▽▽")
    c.drawString(sx(148), sy(-19), "Ra 0.8 ▽▽▽")

    # ── Section view circle on end ────────────────────────────────────────────
    ev_cx = sx(190)
    ev_cy = oy
    c.setStrokeColor(BLACK)
    c.setLineWidth(0.7)
    c.circle(ev_cx, ev_cy, 40/2/sc*mm, stroke=1, fill=0)   # Ø40
    centre_line(c, ev_cx - 16*mm, ev_cy, ev_cx + 16*mm, ev_cy)
    centre_line(c, ev_cx, ev_cy - 16*mm, ev_cx, ev_cy + 16*mm)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(ev_cx, ev_cy - 16*mm - 5*mm, "END VIEW — A")

    # ── Hardness / heat treatment callout box ────────────────────────────────
    notes_box(c, [
        "1. MATERIAL: EN8 (IS 1570 Part 3, C45) — NORMALIZED",
        "2. HEAT TREATMENT: INDUCTION HARDENED @ Ø40 JOURNAL — 52-56 HRC",
        "3. SURFACE FINISH: Ra 1.6 ON JOURNALS, Ra 3.2 ON SHOULDERS",
        "4. THREAD: M20×1.5 — 6g TOLERANCE PER IS 4218",
        "5. KEYWAY: 8×4 DIN 6885-A — BROACHED AFTER HARDENING",
        "6. CHAMFER ALL SHARP EDGES 0.5×45° UNLESS NOTED",
        "7. REMOVE ALL BURRS, CLEAN WITH COMPRESSED AIR BEFORE INSPECTION",
    ], 13*mm, H - 15*mm, w=120*mm)

    c.save()
    print(f"  OK {filename}")


# ═══════════════════════════════════════════════════════════════════════════════
# DRAWING 2 — SHEET METAL BRACKET (IS 2062 Mild Steel, 3mm)
# ═══════════════════════════════════════════════════════════════════════════════

def draw_sheet_metal_bracket(filename):
    c = canvas.Canvas(filename, pagesize=landscape(A3))

    border(c)
    title_block(c,
                part_no="CPT-002-A",
                part_name="MOUNTING BRACKET — SHEET METAL",
                material="IS 2062 GR.A MS SHEET t=3mm",
                scale="1:2",
                revision="A",
                dwg_no="AIP-CPT-002")

    sc = 2.0
    ox = 40*mm
    oy = H/2 - 10*mm

    def sx(v): return ox + v/sc * mm
    def sy(v): return oy + v/sc * mm

    # ── Front view (unfolded flat pattern) ────────────────────────────────────
    # Overall: 200mm wide × 120mm tall (flange down 40mm, web 80mm)
    # Web: 200×80, Flange: 200×40 bent 90° down
    # Holes: 4× Ø10mm on web (50mm from edges, 25mm from top)
    #        2× Ø14mm slots on flange for mounting

    solid(c)

    # Outer rectangle (flat pattern)
    c.rect(sx(0), sy(0), 200/sc*mm, 120/sc*mm, fill=0, stroke=1)

    # Bend line (dash)
    c.setDash([6, 2])
    c.setStrokeColor(BLUE)
    c.setLineWidth(0.5)
    c.line(sx(0), sy(80), sx(200), sy(80))
    c.setDash([])
    c.setStrokeColor(BLACK)

    # Bend annotation
    c.setFont("Helvetica", 6.5)
    c.setFillColor(BLUE)
    c.drawString(sx(105), sy(82), "BEND LINE — 90° DOWN, R4 INSIDE")
    c.setFillColor(BLACK)

    # Holes on web: 4× Ø10mm at (50, 95), (150, 95), (50, 60), (150, 60) — wait, web is y=80 to y=120
    web_holes = [(40, 100), (160, 100), (40, 85), (160, 85)]
    for hx, hy in web_holes:
        c.circle(sx(hx), sy(hy), 5/sc*mm, stroke=1, fill=0)
        centre_line(c, sx(hx)-5*mm, sy(hy), sx(hx)+5*mm, sy(hy))
        centre_line(c, sx(hx), sy(hy)-5*mm, sx(hx), sy(hy)+5*mm)

    # Slots on flange: 2× 30×14 slots at (60, 20), (140, 20) — y=0 to y=80 is flange
    flange_slots = [(60, 25), (140, 25)]
    for sx2, sy2 in flange_slots:
        c.roundRect(sx(sx2-15), sy(sy2-7), 30/sc*mm, 14/sc*mm, 7/sc*mm,
                    stroke=1, fill=0)

    # ── Dimensions ────────────────────────────────────────────────────────────
    # Width
    dim_horizontal(c, sx(0), sy(120), sx(200), "200", above=True, offset=12*mm)
    # Web height
    dim_vertical(c, sx(200), sy(80), sy(120), "40", right=True, offset=10*mm)
    # Flange height
    dim_vertical(c, sx(200), sy(0), sy(80), "80", right=True, offset=18*mm)
    # Hole pitch horiz
    dim_horizontal(c, sx(40), sy(100), sx(160), "120", above=True, offset=8*mm)
    # Hole pitch vert
    dim_vertical(c, sx(0), sy(85), sy(100), "15", right=False, offset=8*mm)
    # Edge to first hole
    dim_horizontal(c, sx(0), sy(85), sx(40), "40", above=False, offset=6*mm)

    # ── Side / isometric sketch ───────────────────────────────────────────────
    # Simple L-shape side view showing 90° bend
    lx = sx(225)
    ly = sy(40)
    t = 3/sc*mm

    solid(c)
    # Web (horizontal top)
    c.line(lx, ly + 40*mm, lx + 40*mm, ly + 40*mm)          # top
    c.line(lx, ly + 40*mm, lx, ly + 40*mm - t)               # left
    c.line(lx + 40*mm, ly + 40*mm, lx + 40*mm, ly + 40*mm - t)  # right
    c.line(lx, ly + 40*mm - t, lx + t, ly + 40*mm - t)
    # Bend corner
    c.line(lx + t, ly + 40*mm - t, lx + t, ly)
    c.line(lx, ly + 40*mm - t, lx, ly)
    # Flange (vertical down)
    c.line(lx, ly, lx + 20*mm, ly)                           # bottom
    c.line(lx + 20*mm, ly, lx + 20*mm, ly + t)
    c.line(lx + t, ly + t, lx + 20*mm, ly + t)
    c.line(lx + t, ly, lx + t, ly + t)

    # 90° angle mark
    c.setLineWidth(0.35)
    c.arc(lx - 3*mm, ly + 40*mm - t - 3*mm, lx + 3*mm, ly + 40*mm - t + 3*mm,
          0, -90)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(lx + 3*mm, ly + 40*mm - t - 5*mm, "90°")

    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(BLACK)
    c.drawCentredString(lx + 20*mm, ly - 6*mm, "SIDE VIEW — B")

    # ── Weld / finish callouts ────────────────────────────────────────────────
    notes_box(c, [
        "1. MATERIAL: IS 2062 GR.A MILD STEEL, t=3mm HOT ROLLED",
        "2. LASER CUT (FIBER 3kW) — CUTTING TOLERANCE ±0.2mm",
        "3. DEBURR ALL EDGES — MAX BURR HEIGHT 0.1mm",
        "4. BEND: 90° ± 0.5° — INSIDE RADIUS R4mm (K-FACTOR 0.4)",
        "5. HOLES: 4× Ø10 ±0.2  |  SLOTS: 2× 30×14 ±0.2",
        "6. SURFACE TREATMENT: POWDER COAT RAL 7035 LIGHT GREY, 60-80µm DFT",
        "7. FLATNESS: WEB ≤0.3mm PER 100mm  |  PERPENDICULARITY ≤0.5mm",
    ], 13*mm, H - 15*mm, w=120*mm)

    c.save()
    print(f"  OK {filename}")


# ═══════════════════════════════════════════════════════════════════════════════
# DRAWING 3 — MILLED HOUSING BLOCK (Al 6061-T6)
# ═══════════════════════════════════════════════════════════════════════════════

def draw_milled_housing(filename):
    c = canvas.Canvas(filename, pagesize=landscape(A3))

    border(c)
    title_block(c,
                part_no="CPT-003-A",
                part_name="SENSOR HOUSING BLOCK — CNC MILLED",
                material="ALUMINIUM 6061-T6 (IS 736 HR30)",
                scale="1:1",
                revision="A",
                dwg_no="AIP-CPT-003")

    sc = 1.0
    ox = 35*mm
    oy = H/2 - 5*mm

    def sx(v): return ox + v/sc * mm
    def sy(v): return oy + v/sc * mm

    # ── Front view ────────────────────────────────────────────────────────────
    # Block: 80×60mm
    # Central pocket: 50×30mm, 15mm deep (shown as hidden rect)
    # 4× M6 boss holes at corners (Ø8 counterbore, Ø6 thru)
    # 1× Ø12 thru hole for sensor port (centre)

    bw = 80
    bh = 60

    solid(c)
    c.rect(sx(0), sy(0), bw*mm, bh*mm, fill=0, stroke=1)

    # Central pocket (hidden — dashed)
    pw = 50; ph = 30
    px = (bw-pw)/2; py = (bh-ph)/2
    hidden_line(c, sx(px), sy(py), sx(px+pw), sy(py))
    hidden_line(c, sx(px), sy(py+ph), sx(px+pw), sy(py+ph))
    hidden_line(c, sx(px), sy(py), sx(px), sy(py+ph))
    hidden_line(c, sx(px+pw), sy(py), sx(px+pw), sy(py+ph))

    # Centre lines for pocket
    centre_line(c, sx(px-3), sy(bh/2), sx(px+pw+3), sy(bh/2))
    centre_line(c, sx(bw/2), sy(py-3), sx(bw/2), sy(py+ph+3))

    # Central sensor bore Ø12
    c.setStrokeColor(BLACK)
    c.setLineWidth(0.7)
    c.circle(sx(bw/2), sy(bh/2), 6*mm, stroke=1, fill=0)

    # Boss holes 4 corners (Ø8 cbore Ø6 thru)
    corners = [(10, 10), (70, 10), (10, 50), (70, 50)]
    for cx2, cy2 in corners:
        c.setLineWidth(0.7)
        c.circle(sx(cx2), sy(cy2), 4*mm, stroke=1, fill=0)   # Ø8 cbore
        c.setLineWidth(0.35)
        c.setDash([3, 1.5])
        c.circle(sx(cx2), sy(cy2), 3*mm, stroke=1, fill=0)   # Ø6 thru
        c.setDash([])
        centre_line(c, sx(cx2)-5*mm, sy(cy2), sx(cx2)+5*mm, sy(cy2))
        centre_line(c, sx(cx2), sy(cy2)-5*mm, sx(cx2), sy(cy2)+5*mm)

    # ── Side view (right) ──────────────────────────────────────────────────────
    lx = sx(95)
    ly = sy(0)
    solid(c)
    depth = 40

    c.rect(lx, ly, depth*mm, bh*mm, fill=0, stroke=1)
    # Pocket depth shown as hidden
    hidden_line(c, lx, ly + py*mm, lx + 15*mm, ly + py*mm)
    hidden_line(c, lx, ly + (py+ph)*mm, lx + 15*mm, ly + (py+ph)*mm)
    hidden_line(c, lx + 15*mm, ly + py*mm, lx + 15*mm, ly + (py+ph)*mm)
    # Sensor bore (hidden circle)
    c.setStrokeColor(BLACK)
    c.setLineWidth(0.35)
    c.setDash([3, 1.5])
    c.line(lx + 20*mm, ly + (bh/2-6)*mm, lx + depth*mm, ly + (bh/2-6)*mm)
    c.line(lx + 20*mm, ly + (bh/2+6)*mm, lx + depth*mm, ly + (bh/2+6)*mm)
    c.setDash([])

    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(lx + depth*mm/2, ly - 6*mm, "SIDE VIEW — C")

    # ── Top view ───────────────────────────────────────────────────────────────
    tx = sx(0)
    ty = sy(75)
    solid(c)
    c.rect(tx, ty, bw*mm, depth*mm, fill=0, stroke=1)
    # Pocket outline (hidden)
    hidden_line(c, tx + px*mm, ty, tx + px*mm, ty + 15*mm)
    hidden_line(c, tx + (px+pw)*mm, ty, tx + (px+pw)*mm, ty + 15*mm)
    hidden_line(c, tx + px*mm, ty + 15*mm, tx + (px+pw)*mm, ty + 15*mm)

    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(tx + bw*mm/2, ty + depth*mm + 5*mm, "TOP VIEW — D")

    # ── Dimensions ────────────────────────────────────────────────────────────
    dim_horizontal(c, sx(0), sy(0), sx(80), "80", above=False, offset=12*mm)
    dim_vertical(c, sx(0), sy(0), sy(60), "60", right=False, offset=12*mm)
    dim_vertical(c, sx(95+40), sy(0), sy(60), "60", right=True, offset=8*mm)

    # Pocket dims
    dim_horizontal(c, sx(px), sy(py), sx(px+pw), "50", above=False, offset=6*mm)
    dim_vertical(c, sx(px), sy(py), sy(py+ph), "30", right=False, offset=6*mm)

    # Corner hole pitch
    dim_horizontal(c, sx(10), sy(10), sx(70), "60", above=False, offset=8*mm)
    dim_vertical(c, sx(70), sy(10), sy(50), "40", right=True, offset=6*mm)

    # ── Hole table ────────────────────────────────────────────────────────────
    htx = sx(145)
    hty = sy(60)
    c.setStrokeColor(BLACK)
    c.setLineWidth(0.5)
    rows = [
        ("REF", "QTY", "SIZE", "DESCRIPTION"),
        ("H1",  "1",   "Ø12 THRU", "SENSOR PORT — REAMED H7"),
        ("H2",  "4",   "Ø8 × 5dp CBORE", "M6 MOUNTING — CBORE Ø8×5"),
        ("H3",  "4",   "M6 THRU", "M6×1.0 TAPPED — 12mm DEPTH"),
    ]
    row_h = 7*mm
    col_ws = [10*mm, 10*mm, 35*mm, 55*mm]
    tw = sum(col_ws)

    for ri, row in enumerate(rows):
        ry = hty - ri * row_h
        if ri == 0:
            c.setFillColor(BLUE)
            c.rect(htx, ry - row_h, tw, row_h, fill=1, stroke=1)
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 6)
        else:
            c.setFillColor(LGREY if ri % 2 == 0 else colors.white)
            c.rect(htx, ry - row_h, tw, row_h, fill=1, stroke=1)
            c.setFillColor(BLACK)
            c.setFont("Helvetica", 6)
        cx2 = htx
        for ci, (cell_text, cw) in enumerate(zip(row, col_ws)):
            c.drawString(cx2 + 1.5*mm, ry - row_h + 2*mm, cell_text)
            cx2 += cw

    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(BLACK)
    c.drawString(htx, hty + 3*mm, "HOLE SCHEDULE")

    # ── GD&T frame on sensor bore ─────────────────────────────────────────────
    gx = sx(bw/2) + 8*mm
    gy = sy(bh/2) + 3*mm
    c.setLineWidth(0.5)
    c.setFont("Helvetica", 6.5)
    c.rect(gx, gy, 8*mm, 5*mm, fill=0, stroke=1)
    c.line(gx + 8*mm, gy, gx + 8*mm + 3*mm, gy + 2.5*mm)
    c.drawString(gx + 1*mm, gy + 1*mm, "⌀0.05 | A")
    c.line(sx(bw/2) + 5*mm, sy(bh/2) + 3*mm, gx, gy + 2.5*mm)

    notes_box(c, [
        "1. MATERIAL: AA 6061-T6 ALUMINIUM (IS 736 HR30) — BILLET",
        "2. ALL MACHINING ON 3-AXIS VMC — HAAS VF-2",
        "3. SENSOR PORT Ø12H7: BORE + REAM — CYLINDRICITY ⌀0.05 REF A",
        "4. POCKET: 50×30×15mm DEPTH — FLOOR FLATNESS ≤0.05mm",
        "5. M6 TAPPED HOLES: 12mm MIN ENGAGEMENT — THREAD GAUGE GO/NO-GO",
        "6. SURFACE FINISH: Ra 1.6 ON BORE, Ra 3.2 ALL OTHER MACHINED FACES",
        "7. ANODISE: TYPE II CLEAR (MIL-A-8625 TYPE II), 10-15µm",
        "8. DEBURR ALL EDGES — BREAK SHARP CORNERS 0.3×45° MAX",
    ], 13*mm, H - 15*mm, w=130*mm)

    c.save()
    print(f"  OK {filename}")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    out = os.path.dirname(os.path.abspath(__file__))

    print("Generating demo engineering drawings...")
    draw_turned_shaft(    os.path.join(out, "CPT-001-A_turned_shaft.pdf"))
    draw_sheet_metal_bracket(os.path.join(out, "CPT-002-A_sheet_metal_bracket.pdf"))
    draw_milled_housing(  os.path.join(out, "CPT-003-A_milled_housing.pdf"))
    print("Done. 3 drawings saved to demo-drawings/")
