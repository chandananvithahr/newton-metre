"""Request/response models for the API."""
from pydantic import BaseModel


class ExtractionResponse(BaseModel):
    dimensions: dict
    material: str | None
    material_confidence: str  # "high" | "medium" | "low" — separate from overall drawing confidence
    tolerances: dict
    suggested_processes: list[str]
    confidence: str
    notes: str


class MaterialPriceResponse(BaseModel):
    name: str
    price_inr: float
    source: str  # "database" | "cache" | "estimated"


class EstimateRequest(BaseModel):
    extracted_data: dict
    quantity: int = 1


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
    subtotal: float
    overhead: float
    profit: float
    unit_cost: float
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
