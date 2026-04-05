"""Request/response models for the API."""
from pydantic import BaseModel


class ExtractionResponse(BaseModel):
    dimensions: dict
    material: str | None
    material_confidence: str  # "high" | "medium" | "low" — separate from overall drawing confidence
    tolerances: dict
    suggested_processes: list[str]
    gdt_symbols: list[str] = []  # GD&T symbol names detected in the drawing
    confidence: str
    notes: str


class MaterialPriceResponse(BaseModel):
    name: str
    price_inr: float
    source: str  # "database" | "cache" | "estimated"


class EstimateRequest(BaseModel):
    extracted_data: dict
    quantity: int = 1
    supplier_quote: float | None = None  # actual quote from supplier, for calibration tracking
    gdt_symbols: list[str] = []  # GD&T symbols from extraction, used for per-symbol cost surcharges
    surface_treatment_id: str | None = None  # specific treatment from surface_treatment_db (e.g. "zinc_clear")
    heat_treatment_id: str | None = None     # specific treatment from heat_treatment_db (e.g. "through_hardening")
    machine_tier: str = "cnc_3axis"  # conventional, cnc_2axis, cnc_3axis, cnc_5axis, hmc


class ProcessLine(BaseModel):
    process_id: str
    process_name: str
    time_min: float
    machine_cost: float
    setup_cost_per_unit: float
    tooling_cost: float
    labour_cost: float
    power_cost: float


class EstimateResponse(BaseModel):
    material_name: str
    material_cost: float
    process_lines: list[ProcessLine]
    total_machining_cost: float
    total_setup_cost: float
    total_tooling_cost: float
    total_labour_cost: float
    total_power_cost: float
    surface_treatment_cost: float = 0.0
    heat_treatment_cost: float = 0.0
    machine_tier: str = "cnc_3axis"
    subtotal: float
    overhead: float
    profit: float
    unit_cost: float
    unit_cost_low: float
    unit_cost_high: float
    uncertainty_pct: int
    order_cost: float
    quantity: int
    confidence_tier: str | None
    currency: str = "INR"


class SimilarityEmbedResponse(BaseModel):
    drawing_id: str
    message: str


class SimilarityMatch(BaseModel):
    drawing_id: str
    score: float
    metadata: dict


class SimilaritySearchResponse(BaseModel):
    matches: list[SimilarityMatch]


class UsageResponse(BaseModel):
    total_estimates: int
    total_similarity: int
    joined: str


class AdminUsageResponse(BaseModel):
    today_cost_usd: float
    estimates_today: int
    signups_today: int


class EstimateHistoryItem(BaseModel):
    id: str
    part_type: str
    total_cost: float
    confidence_tier: str | None
    currency: str
    created_at: str


# --- Assembly estimate ---

class AssemblyComponentInput(BaseModel):
    name: str
    extracted_data: dict


class AssemblyEstimateRequest(BaseModel):
    components: list[AssemblyComponentInput]
    joining_method: str
    num_joints: int
    quantity: int = 1


class ComponentCostResult(BaseModel):
    name: str
    material_name: str
    material_cost: float
    machining_cost: float
    setup_cost: float
    tooling_cost: float
    labour_cost: float
    power_cost: float
    subtotal: float
    unit_cost: float


class AssemblyEstimateResponse(BaseModel):
    components: list[ComponentCostResult]
    joining_cost: float
    joining_method_label: str
    joining_material_cost: float
    joining_machine_cost: float
    joining_labour_cost: float
    assembly_subtotal: float
    overhead: float
    profit: float
    unit_cost: float
    order_cost: float
    quantity: int
    currency: str = "INR"


# --- RFQ extraction and estimation ---

class RFQLineItemResult(BaseModel):
    line_number: int
    part_number: str | None
    description: str
    quantity: int
    material: str | None
    delivery_weeks: int | None
    dimensions: dict
    suggested_processes: list[str]
    unit_price_expected: float | None
    notes: str | None


class RFQExtractResponse(BaseModel):
    rfq_number: str | None
    customer: str | None
    date: str | None
    document_type: str  # rfq | drawing | contract | spec_sheet | other
    line_items: list[RFQLineItemResult]
    confidence: str
    page_count: int


class RFQLineItemEstimate(BaseModel):
    line_number: int
    part_number: str | None
    description: str
    quantity: int
    material: str | None
    unit_cost: float
    order_cost: float
    confidence_tier: str | None
    error: str | None = None  # set if estimation failed for this line


class RFQEstimateRequest(BaseModel):
    line_items: list[RFQLineItemResult]


class RFQEstimateResponse(BaseModel):
    line_items: list[RFQLineItemEstimate]
    total_order_cost: float
    currency: str = "INR"
