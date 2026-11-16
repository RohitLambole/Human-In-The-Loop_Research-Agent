# Phase 0 verification record

Verified on 2026-11-16. Phase 0 remains active: real Supabase JWT authentication has not yet been verified against a configured Supabase project.

## Confirmed

- Docker Compose PostgreSQL is healthy and published as `localhost:5434 -> container:5432`.
- Windows Python connects through both `asyncpg` and SQLAlchemy.
- PostgreSQL 16.16 is reachable; pgvector is version 0.8.7.
- The `threads` table exists with `thread_id`, `user_id`, `created_at`, and `status` columns.
- A live Uvicorn server returns `200 {"status":"ok"}` from `/health`.
- `pytest -q` passes: 5 tests in 0.08s.
- `ruff check .` passes.
- Ownership tests cover owner read access and deny a second user access to state, stream, and resume routes with 404.

## Resolved database routing issue

Windows had a native `postgresql-x64-18` service listening on port 5432 while Docker Desktop also advertised the ResearchOS mapping on that port. The Python connection reached the competing service, explaining the authentication failure and absence of a corresponding Docker PostgreSQL log entry.

The Compose host mapping and local database URLs now use port 5434. Only the Compose container was replaced to apply the binding; the named PostgreSQL volume was preserved. The local `.env` also had a malformed `DATABASE_URL` line that merged in `SUPABASE_URL`; it is now split into separate settings.

## Remaining exit criterion

- [ ] Configure a real `SUPABASE_URL` and, if needed, `SUPABASE_JWT_SECRET` in `.env`.
- [ ] Use a real Supabase access token to verify that a valid token is accepted and invalid, expired, wrong-audience, and malformed tokens are rejected.

The unit tests deliberately override authentication with deterministic users, so they do not establish real Supabase connectivity. Do not start Phase 1 until this final criterion is recorded as passed.

## Security follow-up

The development database password has appeared in local configuration and conversation history. Before any shared environment or deployment, rotate it to a unique value, update `.env`, and keep `.env` untracked.
