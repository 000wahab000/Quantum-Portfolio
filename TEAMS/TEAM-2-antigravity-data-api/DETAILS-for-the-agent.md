# TEAM-2 DETAILS for the agent: Data layer and API

Teammates do not need to read this file. The prompt files tell the agent to read it. Human steps are in `START-HERE.md`.

Tool: Google Antigravity (Planning mode, Request review).

## Mission

Turn NIFTY 50 prices into a leak-free `Market`, supply the declared pre-screen, cost terms, whole-share allocation and out-of-sample scoring, then serve the whole contract over HTTP with background jobs. Delivers R1-R4, R8, R9, R17 and the transaction-cost inputs of R6, plus the serving side of R18, R19, R21. The one thing that must never break: nothing after the estimation end date may influence mu, Sigma, the screen or any solver (AE4).

## Your units

| U-ID | Title | When | Depends on |
|---|---|---|---|
| U3 | Data layer: universe, prices, windows, mu/Sigma | Build (T0 to T0+2.5h) | U1 |
| U4 | Pre-screen, costs, allocation, out-of-sample | Build | U1, U3 |
| U11 | API + job runner + studies endpoint | Integrate (T0+2.5h to T0+4h) | U1 (stub pipeline), U10 |
| U15 (your part) | Offline and demo checks | Evidence + demo (T0+4h to T0+5h) | U10-U14 |

## Owned paths

- `backend/qportfolio/data/` (`__init__.py`, `universe.py`, `prices.py`, `risk.py`, `screen.py`, `costs.py`, `allocate.py`, `evaluate.py`)
- `backend/qportfolio/api/` (`__init__.py`, `main.py`, `jobs.py`, `studies.py`)
- `backend/scripts/fetch_snapshot.py`, `backend/data/nifty50.csv`, `backend/data/snapshot/` (committed parquet)
- `backend/tests/{test_data,test_screen_costs,test_api}.py`
- `backend/data/cache/` is runtime-only and gitignored. Never commit it.

## Do not touch

- `backend/qportfolio/{contracts.py,problem.py,pipeline.py}`, `qubo/`, `quantum/`, `backend/scripts/{smoke.py,run_studies.py}`, `backend/data/studies/`, `contracts/`, `backend/pyproject.toml`, `backend/uv.lock`, `docs/`, `TEAMS/`, `AGENTS.md`, `CLAUDE.md` (TEAM-1).
- `backend/qportfolio/classical/`, `metrics.py`, `frontier.py`, `verdict.py` (TEAM-3).
- `frontend/` (TEAM-4).
- Need a new dependency, a contract change, or a field missing from `contracts.py`? Ask TEAM-1 in chat.

## Interfaces you provide

- CONTRACTS.md §1.2 (everything in `backend/qportfolio/data/`): `load_universe`, `load_prices`, `build_market`, `Market.subset`, `prescreen`, `linear_costs`, `to_shares`, `out_of_sample`. Constants `RF`, `C_BUY`, `C_SELL`, `DEFAULT_WINDOWS`.
- Also export `benchmark_oos(market, rf=RF)` from `data/evaluate.py` (same metrics for `^NSEI`; the pipeline uses it for `benchmarks.nifty50`). It is listed in TEAMS/CONTRACTS.md §1.2.
- `Market` is consumed by TEAM-1's pipeline and TEAM-3's `frontier(market_subset, landscape)`: keep `tickers`, `sectors`, `mu`, `sigma` in the same order everywhere.
- §2 HTTP API, all routes: `GET /api/health`, `GET /api/universe` (§2.1), `POST /api/screen` (§2.4), `POST /api/runs`, `GET /api/runs/{job_id}` (§2.5), `DELETE /api/runs/{job_id}`, `GET /api/studies`, `GET /api/studies/{id}` (§2.7). TEAM-4 consumes these.

## Interfaces you consume

- `backend/qportfolio/contracts.py` pydantic models for §2.2 RunRequest, §2.4 ScreenInfo, §2.5 JobStatus, §2.6 portfolio/oos blocks, §2.7 Study.
- §1.5 `pipeline.run(request, on_progress, cancel) -> RunResult` and `Cancelled`. A stub returns the example result until U10 merges; build U11 against the stub and change nothing when U10 lands.
- `contracts/api-examples/*.json` as test fixtures (read-only).
- `backend/data/studies/*.json` (written by TEAM-1 in U14). Until then the dir may be empty: `GET /api/studies` returns `[]`; tests use a temp dir with a copy of `contracts/api-examples/study_depth.json`.

## How to verify

```
cd backend; uv run pytest tests/test_data.py tests/test_screen_costs.py tests/test_api.py -q
uv run pytest -q
uv run uvicorn qportfolio.api.main:app --reload --reload-dir qportfolio --port 8000
```

- `GET http://localhost:8000/api/health` returns `{"ok": true, "version": "0.1.0"}`; `GET /api/universe` returns 50 assets with sectors and `source`/`as_of`.
- `build_market` on all 50 tickers takes under 2 s from the snapshot.
- Manual (U15): Wi-Fi off, default run through the API reaches `done`; the universe call still reports `source: "snapshot"`.

## Definition of done

- [ ] U3, U4, U11 test scenarios exist as pytest tests and pass; `uv run pytest -q` is green.
- [ ] AE4 look-ahead test and AE6 offline test are green.
- [ ] `backend/data/snapshot/prices.parquet` committed (50 tickers plus `^NSEI`, 2023-09-01 to 2026-10-07); `backend/data/cache/` not committed.
- [ ] Screen output matches `contracts/api-examples/screen.json` in shape; all `/api` routes match CONTRACTS §2 and `test_api.py` passes against the stub and later the real pipeline.
- [ ] No banned APIs (AGENTS.md git grep clean), no new dependencies, no files outside owned paths.
- [ ] Committed and pushed to `team-2/work`; 3-line summary printed (Wahab merges).

## Handoff

- One branch only: `team-2/work`. The agent commits and pushes it at the end of every prompt (see "When finished" in each prompt file). Never push to `main`, never force-push.
- Wahab (TEAM-1) opens the pull requests, merges and resolves conflicts. If `git pull origin main` reports a conflict, stop, do not resolve it, and tell the user to message Wahab.
- Final message of every prompt: a 3-line summary (what was built, test result, known gaps).

## Pitfalls

- yfinance returns MultiIndex columns `(Price, Ticker)` with tickers in alphabetical order: reorder with `df["Close"][tickers]`. `end` is exclusive (pass 2026-10-08 to include 2026-10-07). The index is tz-naive. Use `auto_adjust=True`.
- `TMPV.NS` breaks on the 2025-10-14 demerger and is excluded by default; check other ticker traps in `docs/research/06-nifty50-costs.md`.
- Look-ahead: slice by date first, compute after. Nothing after the estimation end may touch mu, Sigma, the screen or `est_end_prices`. Keep the randomise-the-future test (AE4) green.
- pandas 3: no `applymap`, no chained assignment, no `fillna(method=...)`. Use `.ffill(limit=3)` and `.loc`.
- Keep `tickers`, `sectors`, `mu`, `sigma`, `est_end_prices` in one consistent order; `Market.subset` must preserve it.
- Tests never touch the network: patch `yf.download`. The snapshot is the truth in tests.
- `ThreadPoolExecutor(max_workers=1)`: a second run queues. Never return a traceback to the client; log it server-side.
- `qportfolio/data/` is a Python package; `backend/data/` holds files. Resolve file paths from `__file__`, and quote the repo path (it has spaces).
