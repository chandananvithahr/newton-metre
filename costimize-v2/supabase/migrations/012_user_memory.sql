-- 012_user_memory.sql
-- Mem0-style user memory layer for the chat agent.
-- Extracts preferences and patterns from conversations,
-- injects them into future sessions so the agent "remembers" the user.

CREATE TABLE IF NOT EXISTS user_memory (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL,
    key         TEXT NOT NULL,          -- e.g. "preferred_material", "typical_batch_size"
    value       TEXT NOT NULL,          -- e.g. "EN8 steel", "500 units"
    confidence  SMALLINT DEFAULT 2,     -- 1=low, 2=medium, 3=high (increases with repetition)
    source      TEXT,                   -- "chat_extraction" or "explicit"
    updated_at  TIMESTAMPTZ DEFAULT now(),
    UNIQUE (user_id, key)               -- one value per key per user (upsert pattern)
);

-- Index for fast per-user lookup
CREATE INDEX IF NOT EXISTS user_memory_user_id_idx ON user_memory (user_id);

-- RLS: users can only read their own memory; service role can write
ALTER TABLE user_memory ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users read own memory"
    ON user_memory FOR SELECT
    USING (auth.uid() = user_id);

-- Service role bypasses RLS (used by backend API)
