Paste this whole file into your agent (or @-mention it). Team 2, unit U11.

# TEAM-2 · U11 — API + job runner + studies endpoint

Integrate phase (T0+2.5h to T0+4h). Depends on U1 (stub `pipeline.run`) to build; U10 for real results. Branch `team-2/api`.

## Read first

- `AGENTS.md`
- `docs/teams/CONTRACTS.md`: section 1.5 (`pipeline.run`, `Cancelled`), all of section 2 (2.1 to 2.7)
- `docs/teams/TEAM-2.md`
- Plan `docs/plans/2026-10-08-2115-feat-quantum-portfolio-optimiser-plan.md`: KTD13, section "U11. API + job runner + studies endpoint", AE5
- `contracts/api-examples/*.json` (fixtures)

## Process

Plan first, list the exact files, and stop for review before editing. Edit only owned paths. Build against the stub `pipeline.run` in `backend/qportfolio/pipeline.py`; never edit that file.

## Goal

Serve the contract over HTTP with background jobs, polling and cancel.

## Owned paths / Do not touch

- Owned: `backend/qportfolio/api/`, `backend/qportfolio/data/`, `backend/tests/test_api.py` (plus the other TEAM-2 paths).
- Do not touch: `contracts.py`, `problem.py`, `pipeline.py`, `qubo/`, `quantum/`, `classical/`, `metrics.py`, `frontier.py`, `verdict.py`, `contracts/`, `backend/data/studies/`, `pyproject.toml`, `uv.lock`, `docs/`, `frontend/`.

## Files (exact)

- `backend/qportfolio/api/__init__.py`, `main.py`, `jobs.py`, `studies.py`
- `backend/tests/test_api.py`

## Approach

1. `main.py`: FastAPI app with exactly the routes of CONTRACTS section 2 (paths, bodies, status codes):
   - `GET /api/health` -> `{"ok": true, "version": "0.1.0"}`
   - `GET /api/universe` (assets plus `as_of` and `source` from `load_prices`, `excluded_reason` for excluded tickers)
   - `POST /api/screen` (RunRequest -> `build_market` -> `prescreen` -> ScreenInfo)
   - `POST /api/runs` (202, `{"job_id"}`), `GET /api/runs/{job_id}`, `DELETE /api/runs/{job_id}`
   - `GET /api/studies`, `GET /api/studies/{id}`
   - Error body `{"detail": "plain-language message"}`. CORS allows `http://localhost:5173` and `http://127.0.0.1:5173`. Validate with the pydantic models in `contracts.py` (RunRequest limits per section 2.2).
2. `jobs.py`: in-memory dict guarded by a `threading.Lock` plus `ThreadPoolExecutor(max_workers=1)`. Each job has a `threading.Event` cancel flag passed to `pipeline.run`, an `on_progress` that updates `progress`, `stage` and appends convergence points, and `elapsed_s`. States: `queued`, `running`, `done`, `error`, `cancelled`. `DELETE` sets the flag and returns JobStatus with `state: "cancelled"` (works for queued and running jobs); a pipeline raising `Cancelled` leaves the state `cancelled` with no result.
3. Errors: a pipeline exception sets `state=error` with a plain-language `error` string (no traceback, no file paths); log the full traceback server-side with `logging.exception`. Unknown job id -> 404.
4. `studies.py`: read `backend/data/studies/*.json` (id = file stem; title and summary from the content); empty or missing dir -> `[]`; unknown id -> 404. Resolve the dir from `__file__`.

## Interfaces

- Provide (section 2): all routes above, with shapes 2.1, 2.4, 2.5, 2.6, 2.7. TEAM-4 consumes them.
- Consume: section 1.5 `pipeline.run(request, on_progress, cancel)` and `Cancelled`; section 1.2 `load_universe`, `load_prices`, `build_market`, `prescreen`; `backend/data/studies/*.json` (TEAM-1, U14; may be empty until then).

## Test scenarios (`fastapi.testclient.TestClient`; monkeypatch the pipeline with a slow fake for cancel)

- [ ] `POST /api/runs` returns a `job_id`; polling reaches `done` with a result that validates (stub pipeline).
- [ ] `DELETE /api/runs/{id}` while running moves state to `cancelled` within 2 s.
- [ ] A pipeline exception gives `state=error` and an `error` string with no traceback.
- [ ] Unknown job id returns 404.
- [ ] `GET /api/universe` returns 50 assets with sectors.
- [ ] `GET /api/studies` lists each JSON file; `GET /api/studies/{id}` returns its content; unknown id returns 404 (use a temp dir with a copy of `contracts/api-examples/study_depth.json`).
- [ ] `POST /api/screen` with 30 tickers returns `kept` and `dropped` lists whose total is 30.

## Verify

```
cd backend; uv run pytest tests/test_api.py -q; uv run pytest -q
uv run uvicorn qportfolio.api.main:app --reload --reload-dir qportfolio --port 8000
```

`GET http://localhost:8000/api/health` returns ok; the frontend's real-API mode (`npm run dev` in `frontend/`) works against it.

## Done checklist

- [ ] All scenarios above exist as pytest tests and pass; full suite green.
- [ ] Routes and JSON shapes match CONTRACTS section 2 exactly; no traceback ever reaches a client.
- [ ] When U10 merges, `test_api.py` still passes unchanged against the real pipeline (or only the fixture changes).
- [ ] Committed on branch `team-2/api`, PR to `main`; summary posted.
