-- Negotiation memory — episodic + semantic + message audit trail.
-- Per-company isolation via company_id on all tables.

-- Episodic: individual negotiation outcomes
CREATE TABLE IF NOT EXISTS negotiation_episodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL,
    supplier_id UUID REFERENCES suppliers(id),
    workflow_id UUID REFERENCES agent_workflows(id),
    part_family TEXT,
    initial_quote DECIMAL(12, 2),
    should_cost DECIMAL(12, 2),
    target_price DECIMAL(12, 2),
    final_price DECIMAL(12, 2),
    rounds INTEGER DEFAULT 0,
    arguments_used JSONB DEFAULT '[]',     -- [{argument, effectiveness: 1-5}]
    arguments_failed JSONB DEFAULT '[]',
    concessions_made JSONB DEFAULT '[]',   -- [{what, value}]
    outcome TEXT DEFAULT 'pending',        -- 'accepted', 'rejected', 'expired', 'pending'
    duration_days INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_neg_episodes_company ON negotiation_episodes(company_id);
CREATE INDEX idx_neg_episodes_supplier ON negotiation_episodes(supplier_id);
CREATE INDEX idx_neg_episodes_part ON negotiation_episodes(part_family);

ALTER TABLE negotiation_episodes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Company isolation on episodes"
    ON negotiation_episodes FOR ALL
    USING (company_id::text = auth.uid()::text OR auth.role() = 'service_role');

-- Semantic: supplier intelligence patterns
CREATE TABLE IF NOT EXISTS supplier_intelligence (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL,
    supplier_id UUID REFERENCES suppliers(id),
    pattern_type TEXT NOT NULL,            -- 'price_inflation', 'response_time', 'quality_trend', etc.
    pattern_data JSONB NOT NULL DEFAULT '{}',
    evidence_count INTEGER DEFAULT 1,
    last_updated TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_supplier_intel_company ON supplier_intelligence(company_id);
CREATE INDEX idx_supplier_intel_supplier ON supplier_intelligence(supplier_id);

ALTER TABLE supplier_intelligence ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Company isolation on intelligence"
    ON supplier_intelligence FOR ALL
    USING (company_id::text = auth.uid()::text OR auth.role() = 'service_role');

-- Message audit trail
CREATE TABLE IF NOT EXISTS negotiation_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    episode_id UUID NOT NULL REFERENCES negotiation_episodes(id) ON DELETE CASCADE,
    direction TEXT NOT NULL,               -- 'outbound' | 'inbound'
    channel TEXT DEFAULT 'email',          -- 'email', 'call', 'meeting'
    content TEXT NOT NULL,
    sentiment TEXT,                        -- 'positive', 'neutral', 'negative'
    extracted_terms JSONB DEFAULT '{}',    -- prices, dates, conditions mentioned
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_neg_messages_episode ON negotiation_messages(episode_id);

ALTER TABLE negotiation_messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service role full access on messages"
    ON negotiation_messages FOR ALL
    USING (auth.role() = 'service_role');
