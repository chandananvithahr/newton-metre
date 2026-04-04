-- Agent workflow tables for the multi-agent procurement system.
-- Three tables: workflows (top-level), checkpoints (per-agent state), audit_log (cost tracking).

-- ============================================================
-- agent_workflows — top-level workflow tracking
-- ============================================================
CREATE TABLE IF NOT EXISTS agent_workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id),
    company_id UUID,
    workflow_type TEXT NOT NULL,           -- 'rfq', 'negotiate', 'full_procurement', etc.
    execution_mode TEXT NOT NULL DEFAULT 'hitl',  -- 'auto', 'hitl', 'manual'
    state TEXT NOT NULL DEFAULT 'created', -- WorkflowState enum values
    inputs JSONB NOT NULL DEFAULT '{}',
    outputs JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX idx_agent_workflows_user ON agent_workflows(user_id);
CREATE INDEX idx_agent_workflows_state ON agent_workflows(state);
CREATE INDEX idx_agent_workflows_type ON agent_workflows(workflow_type);

-- RLS: users see only their own workflows
ALTER TABLE agent_workflows ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own workflows"
    ON agent_workflows FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create own workflows"
    ON agent_workflows FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Service role can do everything (backend writes)
CREATE POLICY "Service role full access on workflows"
    ON agent_workflows FOR ALL
    USING (auth.role() = 'service_role');


-- ============================================================
-- agent_checkpoints — per-agent state snapshots for resume
-- ============================================================
CREATE TABLE IF NOT EXISTS agent_checkpoints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID NOT NULL REFERENCES agent_workflows(id) ON DELETE CASCADE,
    agent_name TEXT NOT NULL,
    state TEXT NOT NULL,
    context JSONB NOT NULL DEFAULT '{}',
    approval_required BOOLEAN NOT NULL DEFAULT false,
    approved_by UUID REFERENCES auth.users(id),
    approved_at TIMESTAMPTZ,
    modifications JSONB,                   -- human edits applied on approval
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_agent_checkpoints_workflow ON agent_checkpoints(workflow_id);
CREATE INDEX idx_agent_checkpoints_pending ON agent_checkpoints(workflow_id)
    WHERE approval_required = true AND approved_by IS NULL;

ALTER TABLE agent_checkpoints ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service role full access on checkpoints"
    ON agent_checkpoints FOR ALL
    USING (auth.role() = 'service_role');

CREATE POLICY "Users can view own checkpoints"
    ON agent_checkpoints FOR SELECT
    USING (
        workflow_id IN (
            SELECT id FROM agent_workflows WHERE user_id = auth.uid()
        )
    );


-- ============================================================
-- agent_audit_log — tracks every agent execution for cost/debug
-- ============================================================
CREATE TABLE IF NOT EXISTS agent_audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID NOT NULL REFERENCES agent_workflows(id) ON DELETE CASCADE,
    agent_name TEXT NOT NULL,
    action TEXT NOT NULL,                  -- 'executed', 'validation_failed', etc.
    details JSONB NOT NULL DEFAULT '{}',
    llm_calls INTEGER NOT NULL DEFAULT 0,
    cost_usd DECIMAL(10, 6) NOT NULL DEFAULT 0,
    duration_ms INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_agent_audit_workflow ON agent_audit_log(workflow_id);
CREATE INDEX idx_agent_audit_agent ON agent_audit_log(agent_name);

ALTER TABLE agent_audit_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service role full access on audit_log"
    ON agent_audit_log FOR ALL
    USING (auth.role() = 'service_role');

CREATE POLICY "Users can view own audit logs"
    ON agent_audit_log FOR SELECT
    USING (
        workflow_id IN (
            SELECT id FROM agent_workflows WHERE user_id = auth.uid()
        )
    );
