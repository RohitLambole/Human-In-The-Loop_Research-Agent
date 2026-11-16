CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS threads (
    thread_id UUID PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(32) NOT NULL DEFAULT 'running'
);

CREATE INDEX IF NOT EXISTS ix_threads_user_id ON threads (user_id);
CREATE INDEX IF NOT EXISTS ix_threads_user_created ON threads (user_id, created_at DESC);
