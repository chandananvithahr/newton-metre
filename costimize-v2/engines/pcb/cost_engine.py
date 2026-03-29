# costimize-v2/engines/pcb/cost_engine.py
"""PCB assembly cost engine — components + fabrication + assembly + testing."""

from dataclasses import dataclass
from config import SMD_RATE_PER_PAD, THT_RATE_PER_PIN, STENCIL_COST, TEST_RATE_PER_BOARD, OVERHEAD_PCT, PROFIT_PCT
from engines.pcb.fab_cost import estimate_pcb_fab_cost


@dataclass(frozen=True)
class ComponentCostLine:
    mpn: str
    description: str
    quantity: int
    unit_price: float
    line_total: float
    source: str


@dataclass(frozen=True)
class PcbCostBreakdown:
    component_lines: tuple[ComponentCostLine, ...]
    total_components_cost: float
    board_fab_cost: float
    smd_pads: int
    smd_cost: float
    tht_pins: int
    tht_cost: float
    stencil_cost_per_board: float
    total_assembly_cost: float
    test_cost: float
    subtotal: float
    overhead: float
    profit: float
    unit_cost: float
    order_cost: float
    quantity: int


def calculate_pcb_cost(
    component_prices: list[dict],
    board_length_mm: float,
    board_width_mm: float,
    layers: int,
    quantity: int,
    smd_pads: int,
    tht_pins: int,
    surface_finish: str = "HASL",
) -> PcbCostBreakdown:
    comp_lines = []
    for cp in component_prices:
        unit_price = cp.get("unit_price", 0)
        qty = cp.get("quantity", 1)
        comp_lines.append(ComponentCostLine(
            mpn=cp.get("mpn", ""),
            description=cp.get("description", ""),
            quantity=qty,
            unit_price=round(unit_price, 2),
            line_total=round(unit_price * qty, 2),
            source=cp.get("source", "manual"),
        ))
    total_comp = sum(c.line_total for c in comp_lines)

    board_fab = estimate_pcb_fab_cost(board_length_mm, board_width_mm, layers, quantity, surface_finish)

    smd_cost = smd_pads * SMD_RATE_PER_PAD
    tht_cost = tht_pins * THT_RATE_PER_PIN
    stencil_per_board = STENCIL_COST / max(quantity, 1)
    total_assembly = smd_cost + tht_cost + stencil_per_board

    test_cost = TEST_RATE_PER_BOARD

    subtotal = total_comp + board_fab + total_assembly + test_cost
    overhead = subtotal * (OVERHEAD_PCT / 100)
    profit = (subtotal + overhead) * (PROFIT_PCT / 100)
    unit_cost = subtotal + overhead + profit
    order_cost = round(round(unit_cost, 2) * quantity, 2)

    return PcbCostBreakdown(
        component_lines=tuple(comp_lines),
        total_components_cost=round(total_comp, 2),
        board_fab_cost=round(board_fab, 2),
        smd_pads=smd_pads,
        smd_cost=round(smd_cost, 2),
        tht_pins=tht_pins,
        tht_cost=round(tht_cost, 2),
        stencil_cost_per_board=round(stencil_per_board, 2),
        total_assembly_cost=round(total_assembly, 2),
        test_cost=round(test_cost, 2),
        subtotal=round(subtotal, 2),
        overhead=round(overhead, 2),
        profit=round(profit, 2),
        unit_cost=round(unit_cost, 2),
        order_cost=order_cost,
        quantity=quantity,
    )
