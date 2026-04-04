-- Sprint 5: Upgrade similarity search RPCs to return text_description + richer metadata
-- Also recreate the RPCs to ensure they include the text_description column

-- Drop old functions first (return type changed — can't just CREATE OR REPLACE)
DROP FUNCTION IF EXISTS match_drawings(vector, double precision, integer, uuid);
DROP FUNCTION IF EXISTS match_drawings_hybrid(vector, text, integer, uuid, double precision, double precision);

-- Recreate match_drawings with text_description
CREATE OR REPLACE FUNCTION match_drawings(
  query_embedding vector(768),
  match_threshold float DEFAULT 0.3,
  match_count int DEFAULT 10,
  p_user_id uuid DEFAULT NULL
)
RETURNS TABLE (
  id uuid,
  similarity float,
  metadata jsonb,
  text_description text
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    d.id,
    1 - (d.embedding <=> query_embedding) AS similarity,
    d.metadata,
    d.text_description
  FROM drawings d
  WHERE
    (p_user_id IS NULL OR d.user_id = p_user_id)
    AND 1 - (d.embedding <=> query_embedding) > match_threshold
  ORDER BY d.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

-- Drop and recreate match_drawings_hybrid to include text_description
CREATE OR REPLACE FUNCTION match_drawings_hybrid(
  query_embedding vector(768),
  query_text text DEFAULT '',
  match_count int DEFAULT 10,
  p_user_id uuid DEFAULT NULL,
  vector_weight float DEFAULT 0.7,
  text_weight float DEFAULT 0.3
)
RETURNS TABLE (
  id uuid,
  similarity float,
  metadata jsonb,
  text_description text
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    d.id,
    (
      vector_weight * (1 - (d.embedding <=> query_embedding)) +
      text_weight * COALESCE(
        ts_rank_cd(
          to_tsvector('english', COALESCE(d.text_description, '')),
          plainto_tsquery('english', query_text)
        ),
        0
      )
    ) AS similarity,
    d.metadata,
    d.text_description
  FROM drawings d
  WHERE
    (p_user_id IS NULL OR d.user_id = p_user_id)
  ORDER BY similarity DESC
  LIMIT match_count;
END;
$$;

-- Add GIN index for BM25 text search if not exists
CREATE INDEX IF NOT EXISTS idx_drawings_text_search
ON drawings USING gin(to_tsvector('english', COALESCE(text_description, '')));
