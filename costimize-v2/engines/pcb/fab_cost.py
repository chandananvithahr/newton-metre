# costimize-v2/engines/pcb/fab_cost.py
"""PCB bare board fabrication cost model — rule-based pricing for Indian PCB fabs."""


def estimate_pcb_fab_cost(
    board_length_mm: float,
    board_width_mm: float,
    layers: int,
    quantity: int,
    surface_finish: str = "HASL",
) -> float:
    area_cm2 = (board_length_mm * board_width_mm) / 100  # mm² to cm²

    layer_rates = {
        1: 0.8,
        2: 1.2,
        4: 2.5,
        6: 4.0,
        8: 6.0,
    }
    closest_layers = min(layer_rates.keys(), key=lambda x: abs(x - layers))
    base_rate = layer_rates[closest_layers]

    finish_multiplier = {
        "HASL": 1.0,
        "Lead-free HASL": 1.05,
        "ENIG": 1.3,
        "OSP": 0.95,
        "Immersion Tin": 1.15,
        "Immersion Silver": 1.2,
    }
    multiplier = finish_multiplier.get(surface_finish, 1.0)

    if quantity >= 1000:
        qty_factor = 0.6
    elif quantity >= 500:
        qty_factor = 0.7
    elif quantity >= 100:
        qty_factor = 0.8
    elif quantity >= 50:
        qty_factor = 0.9
    else:
        qty_factor = 1.0

    per_board = max(5.0, area_cm2 * base_rate * multiplier * qty_factor)
    return round(per_board, 2)
