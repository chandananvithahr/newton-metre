-- RFQ templates for automated RFQ construction.

CREATE TABLE IF NOT EXISTS rfq_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL,
    name TEXT NOT NULL,
    subject_template TEXT NOT NULL DEFAULT 'Request for Quotation — {part_description}',
    body_template TEXT NOT NULL DEFAULT '',
    terms_template TEXT NOT NULL DEFAULT '',
    fields JSONB NOT NULL DEFAULT '[]',   -- custom fields: [{name, type, required}]
    is_default BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_rfq_templates_company ON rfq_templates(company_id);

ALTER TABLE rfq_templates ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Company isolation on rfq_templates"
    ON rfq_templates FOR ALL
    USING (company_id::text = auth.uid()::text OR auth.role() = 'service_role');

-- Seed a default template
INSERT INTO rfq_templates (company_id, name, subject_template, body_template, terms_template, is_default)
VALUES (
    '00000000-0000-0000-0000-000000000000',
    'Default Manufacturing RFQ',
    'RFQ: {part_description} — {material} — Qty {quantity}',
    E'Dear {supplier_name},\n\nWe invite you to submit a quotation for the following:\n\n**Part:** {part_description}\n**Material:** {material}\n**Quantity:** {quantity} units\n**Key Dimensions:** {dimensions_summary}\n**Processes Required:** {processes_summary}\n**Tolerances:** {tolerance_notes}\n\nPlease provide:\n1. Unit price (INR)\n2. Tooling charges (if any)\n3. Delivery timeline\n4. MOQ (if different from quantity above)\n5. Payment terms\n\nQuotation validity: 30 days minimum.\n\nDrawing attached for reference.\n\nRegards,\n{sender_name}\n{company_name}',
    E'Standard Terms:\n- Delivery: Ex-works\n- Payment: 30 days from invoice\n- Quality: As per drawing specifications\n- Inspection: At our facility before acceptance',
    true
);
