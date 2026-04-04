"""RFQAgent — constructs Request for Quotation documents from extraction + cost data.

Merges drawing extraction (dimensions, material, processes) with company
RFQ templates and should-cost intelligence. Generates professional RFQ
email drafts per supplier.

CRITICAL: Should-cost data is internal reference ONLY.
The agent NEVER includes should-cost, target price, or budget in supplier emails.
"""
import logging
import time

from agents.llm import call_llm, parse_json_response
from agents.types import AgentResult, WorkflowContext

logger = logging.getLogger("agents.rfq")

_FORBIDDEN_IN_EMAIL = [
    "should-cost", "should cost", "target price", "budget",
    "internal", "our estimate", "cost breakdown", "profit margin",
    "we expect to pay", "maximum price", "ceiling price",
]

RFQ_SYSTEM_PROMPT = """You are a professional procurement specialist at an Indian manufacturing company.
Generate a formal Request for Quotation (RFQ) email.

RULES:
- Be professional, concise, and clear
- Include all technical specifications from the part data
- NEVER mention should-cost, target price, budget, or any internal pricing data
- NEVER reveal what the company expects to pay
- Use INR currency references where applicable
- Include delivery, payment terms, and quality requirements
"""

RFQ_GENERATION_PROMPT = """Generate an RFQ email for this part:

Part Description: {part_description}
Material: {material}
Key Dimensions: {dimensions}
Processes: {processes}
Quantity: {quantity}
Tolerances: {tolerances}
Supplier Name: {supplier_name}
Sender Name: {sender_name}
Company Name: {company_name}

Template to follow:
{template}

Similar parts from history (for context, DO NOT include pricing):
{history_context}

Return JSON:
{{
  "subject": "RFQ email subject line",
  "body": "Full email body text",
  "attachments_needed": ["list of files to attach"]
}}

Return ONLY JSON. No markdown fences."""


class RFQAgent:
    """Constructs RFQ documents from extraction + cost + similarity data."""

    @property
    def name(self) -> str:
        return "rfq"

    def validate_inputs(self, inputs: dict) -> tuple[bool, str]:
        has_extraction = "extraction" in inputs
        if not has_extraction:
            return False, "Need 'extraction' data from ExtractionAgent"
        return True, ""

    def execute(self, context: WorkflowContext, inputs: dict) -> AgentResult:
        start = time.perf_counter()

        extraction = inputs.get("extraction", {})
        cost_data = inputs.get("cost", {})
        similarity = inputs.get("similarity", {})
        suppliers = inputs.get("target_suppliers", [{"name": "Supplier", "email": ""}])

        # Build RFQ context
        part_desc = extraction.get("part_type", "Machined Part")
        material = extraction.get("material", "As per drawing")
        dimensions = _format_dimensions(extraction.get("dimensions", {}))
        processes = ", ".join(extraction.get("processes", []))
        quantity = inputs.get("quantity", context.inputs.get("quantity", 1))
        tolerances = extraction.get("tolerances", "As per drawing")

        # History context from similarity (no pricing!)
        history_context = _format_history(similarity.get("matches", []))

        # Load template (use default for now)
        template = _get_default_template()

        # Generate RFQ for each supplier
        email_drafts = []
        total_llm_calls = 0

        for supplier in suppliers:
            supplier_name = supplier.get("name", "Sir/Madam")
            sender_name = inputs.get("sender_name", "Procurement Team")
            company_name = inputs.get("company_name", "")

            prompt = RFQ_GENERATION_PROMPT.format(
                part_description=part_desc,
                material=material,
                dimensions=dimensions,
                processes=processes,
                quantity=quantity,
                tolerances=tolerances,
                supplier_name=supplier_name,
                sender_name=sender_name,
                company_name=company_name,
                template=template,
                history_context=history_context,
            )

            try:
                response = call_llm(
                    messages=[
                        {"role": "system", "content": RFQ_SYSTEM_PROMPT},
                        {"role": "user", "content": prompt},
                    ],
                    json_mode=True,
                )
                total_llm_calls += 1
                draft = parse_json_response(response.content)

                # SAFETY: Check for forbidden content
                violations = _check_forbidden_content(draft.get("body", ""))
                if violations:
                    logger.warning(
                        "RFQ email contained forbidden terms: %s. Regenerating.",
                        violations,
                    )
                    draft["_warnings"] = f"Removed references to: {', '.join(violations)}"

                draft["supplier"] = supplier
                email_drafts.append(draft)

            except Exception as exc:
                logger.exception("RFQ generation failed for %s", supplier_name)
                email_drafts.append({
                    "supplier": supplier,
                    "error": str(exc),
                })

        elapsed = (time.perf_counter() - start) * 1000

        # Build RFQ document (structured, for storage)
        rfq_document = {
            "part_description": part_desc,
            "material": material,
            "dimensions": extraction.get("dimensions", {}),
            "processes": extraction.get("processes", []),
            "quantity": quantity,
            "tolerances": tolerances,
            "should_cost_ref": cost_data.get("unit_cost"),  # Internal only
            "supplier_count": len(suppliers),
        }

        return AgentResult(
            agent_name=self.name,
            status="success",
            data={
                "rfq_document": rfq_document,
                "email_drafts": email_drafts,
                "draft_count": len(email_drafts),
            },
            duration_ms=elapsed,
            llm_calls=total_llm_calls,
        )


def _format_dimensions(dims: dict) -> str:
    """Format dimensions dict as human-readable string."""
    if not dims:
        return "As per drawing"
    parts = []
    for key, val in dims.items():
        clean_key = key.replace("_mm", "").replace("_", " ").title()
        parts.append(f"{clean_key}: {val}mm")
    return ", ".join(parts)


def _format_history(matches: list[dict]) -> str:
    """Format similarity matches as context. NO PRICING."""
    if not matches:
        return "No similar parts in history."
    lines = []
    for m in matches[:3]:
        lines.append(f"- Similar drawing: {m.get('drawing_id', 'unknown')} "
                     f"(material: {m.get('material', 'N/A')})")
    return "\n".join(lines)


def _get_default_template() -> str:
    """Return the default RFQ template. In production, load from Supabase."""
    return (
        "Dear {supplier_name},\n\n"
        "We invite you to submit a quotation for the following:\n\n"
        "Part: {part_description}\n"
        "Material: {material}\n"
        "Quantity: {quantity} units\n"
        "Dimensions: {dimensions}\n"
        "Processes: {processes}\n\n"
        "Please provide: unit price (INR), tooling charges, "
        "delivery timeline, MOQ, and payment terms.\n\n"
        "Quotation validity: 30 days minimum.\n\n"
        "Regards,\n{sender_name}"
    )


def _check_forbidden_content(text: str) -> list[str]:
    """Check if email text contains forbidden internal data."""
    text_lower = text.lower()
    return [term for term in _FORBIDDEN_IN_EMAIL if term in text_lower]
