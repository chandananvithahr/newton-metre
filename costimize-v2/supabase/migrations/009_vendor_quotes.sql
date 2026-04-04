-- Vendor quotes and comparison results.

CREATE TABLE IF NOT EXISTS vendor_quotes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID REFERENCES agent_workflows(id) ON DELETE CASCADE,
    supplier_id UUID REFERENCES suppliers(id),
    raw_file_path TEXT,
    raw_format TEXT,                       -- 'pdf', 'excel', 'email', 'manual'
    extracted_data JSONB DEFAULT '{}',
    normalized_lines JSONB DEFAULT '[]',   -- [{description, unit_price, qty, total, ...}]
    total_quoted DECIMAL(12, 2),
    currency TEXT DEFAULT 'INR',
    delivery_weeks INTEGER,
    payment_terms TEXT,
    validity_days INTEGER DEFAULT 30,
    received_at TIMESTAMPTZ DEFAULT now(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_vendor_quotes_workflow ON vendor_quotes(workflow_id);
CREATE INDEX idx_vendor_quotes_supplier ON vendor_quotes(supplier_id);

ALTER TABLE vendor_quotes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service role full access on quotes"
    ON vendor_quotes FOR ALL
    USING (auth.role() = 'service_role');

-- Quote comparisons
CREATE TABLE IF NOT EXISTS quote_comparisons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID REFERENCES agent_workflows(id) ON DELETE CASCADE,
    comparison_data JSONB NOT NULL DEFAULT '{}',
    best_quote_id UUID REFERENCES vendor_quotes(id),
    savings_vs_should_cost DECIMAL(12, 2),
    savings_pct DECIMAL(5, 2),
    recommendation TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE quote_comparisons ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service role full access on comparisons"
    ON quote_comparisons FOR ALL
    USING (auth.role() = 'service_role');
