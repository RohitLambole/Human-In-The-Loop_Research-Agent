# ResearchOS

ResearchOS is an evidence-driven, resumable multi-agent research platform. This repository is being built phase-by-phase from the ResearchOS v2 plan. The current scaffold implements **Phase 0 only**; graph execution and HITL are intentionally not implemented yet.

## Current status

- [ ] Phase 0: verification in progress; real Supabase JWT validation remains outstanding. See [the Phase 0 verification record](PHASE0_VERIFICATION.md).
- [ ] Phase 1: linear research graph and SSE progress events
- [ ] Phase 2: PostgreSQL checkpointer and HITL review-node pattern
- [ ] Phases 3–8: RAG, verification, source triage, frontend, observability and hardening

## Prerequisites

- Python 3.11+
- Docker Desktop / Docker Engine with Compose
- A Supabase project for real access tokens (local API tests override the auth dependency)

## Start PostgreSQL

From the repository root:

```bash
docker compose up -d postgres
docker compose ps
```

The database image includes pgvector. The SQL bootstrap creates the extension and `threads` ownership table on the first initialization of the named volume.

The container is published on host port `5434` (container port `5432`) to avoid a local Windows PostgreSQL service that already owns port `5432`. Keep the local `DATABASE_URL` on port `5434`.

## Run the API

```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Copy the root `.env.example` to `.env`, set `SUPABASE_URL`, then start the API:

```bash
uvicorn app.main:app --reload
```

Health check: `GET http://localhost:8000/health`.

Protected routes require `Authorization: Bearer <Supabase access token>`. The API validates issuer, audience, expiry and signature. Asymmetric Supabase signing keys are resolved from the project's JWKS endpoint; the optional `SUPABASE_JWT_SECRET` supports legacy HS256 projects.

## Phase 0 API surface

- `POST /sessions` — create an owned session record
- `GET /sessions` — list only the authenticated user's sessions
- `GET /sessions/{thread_id}/state` — read session status (graph state arrives in Phase 1)
- `GET /sessions/{thread_id}/stream` — ownership-protected placeholder; implemented in Phase 1
- `POST /sessions/{thread_id}/resume` — ownership-protected placeholder; implemented in Phase 2

Every route that accepts a `thread_id` uses the shared `get_owned_thread` dependency. Non-owned and unknown IDs both return 404 to prevent thread enumeration.

## Tests and lint

From `backend/`:

```bash
pytest -q
ruff check .
```

The ownership tests use SQLite in-memory and override authentication with two deterministic test identities. They do not require Docker or a live Supabase project.

## Phase discipline

Tests define each phase's exit criteria before implementation. Do not add the frontend or advanced agents before the Phase 1 graph and Phase 2 HITL idempotency checks pass. Keep graph state slim: IDs and control fields in state, bulk evidence and documents in PostgreSQL.
