Paste this whole file into your agent (or @-mention it). Team 1, unit U1.

# TEAM-1 · U1 — Scaffold + frozen contracts + example payloads

Prework (before T0). Skip this prompt if `backend/pyproject.toml` and `backend/qportfolio/contracts.py` are already on `main`.

## Read first

- `AGENTS.md` (all)
- `TEAMS/CONTRACTS.md` (all; you implement it one-to-one)
- `TEAMS/TEAM-1-claude-quantum-core/START-HERE.md`
- Plan `docs/plans/2026-10-08-2115-feat-quantum-portfolio-optimiser-plan.md`: section "U1. Scaffold + frozen contracts + example payloads", KTD2, KTD11, KTD15
- `docs/research/08-env-spike.md` (pins, gotchas), `docs/research/06-nifty50-costs.md` (constituents, sectors)

## Process

Plan first, list the exact files, and stop for review before editing. Edit only owned paths.

## Goal

Give every team a runnable skeleton and the exact interfaces before the event, so all four teams can work in parallel from T0.

## Owned paths / Do not touch

- Owned: everything in this prompt's file list below (repo root files, `backend/` scaffold, `contracts/`).
- Exception: create `backend/data/nifty50.csv` once as the initial file; TEAM-2 owns it afterwards.
- Do not touch: `frontend/`, and do not implement anything inside `data/`, `api/`, `classical/`, `qubo/`, `quantum/` beyond an empty `__init__.py`.

## Files (exact)

- `backend/pyproject.toml`, `backend/uv.lock`, `backend/.python-version`, `.gitignore`
- `backend/qportfolio/__init__.py`, `contracts.py`, `problem.py`
- `backend/qportfolio/pipeline.py`: a stub whose `run(request, on_progress=None, cancel=None)` returns the example `RunResult`; also defines `Cancelled`
- Empty packages with `__init__.py`: `backend/qportfolio/{data,qubo,quantum,classical,api}/`
- `backend/scripts/smoke.py` (copy from the spike), `backend/data/nifty50.csv` (from `docs/research/06-nifty50-costs.md`)
- `contracts/api-examples/{universe,run_request,screen,job_running,job_done,job_error,studies_index,study_depth}.json`
- `backend/tests/test_contracts.py`, `backend/tests/test_problem.py`

## Approach

1. `cd backend; uv init` (adapt to the existing layout), `uv python pin 3.13`, then add the verified pins: qiskit 2.5.2, qiskit-aer 0.17.2, qiskit-ibm-runtime 0.50.0, cvxpy 1.9.3, yfinance 1.7.0, pandas 3.0.6, numpy 2.5.3, scipy 1.18.1, pyarrow 25.0.1, fastapi 0.143.0, uvicorn 0.54.0, pydantic 2.14.0. Dev: pytest 9.1.1, httpx2 2.13.1. `.gitignore`: `.env`, `.venv/`, `node_modules/`, `backend/data/cache/`, `__pycache__/`, `.pytest_cache/`, `dist/`.
2. `contracts.py`: pydantic models mirroring `TEAMS/CONTRACTS.md` section 2 one-to-one (RunRequest with the 2.2 validation limits, Sample, ScreenInfo, JobStatus, RunResult with SolverResult/QaoaBlock/Verdict/Frontier, Study, Universe). Also the shared result types used in section 1 (SolverResult, Landscape, QaoaMetrics, Verdict, Sample). Pick field names exactly as in the JSON.
3. `problem.py`: the `Problem` and `Evaluation` dataclasses of section 1.1 and the exact `evaluate(x)`: objective F(x) = q*x'Sigma x/K^2 - (1-q)*(mu'x/K - tc(x)), tc(x) = cost_lin.x + cost_const, plus feasibility and violation strings (cardinality, sector cap, target return) in the formats of section 1.1. TEAM-3 depends on this from T0.
4. Hand-write realistic example JSON for a 10-asset, K=5 instance. The numbers must be internally consistent (volatility = sqrt(variance), weights sum to 1, shares x price = value, cash_left = capital - invested, frontier points consistent with solver points). The verdict text must not contain the banned phrases "advantage", "outperforms classical", "quantum speedup" (use the wording now in CONTRACTS.md section 2.6, "no speed benefit is claimed at this size", in `job_done.json`; do not edit CONTRACTS.md).
5. `smoke.py` from the spike; `pipeline.py` stub loads `contracts/api-examples/job_done.json`'s `result` via `__file__`-relative path.

## Interfaces

- Provide: section 1.1 (`Problem`, `Evaluation`, `evaluate`), section 1.5 stub (`run`, `Cancelled`), all section 2 models in `contracts.py`, example payloads.
- Consume: nothing.

## Test scenarios

- [ ] Every file in `contracts/api-examples/` parses into its pydantic model without error.
- [ ] 4-asset `Problem`, K=2, no other constraints: `evaluate` equals the hand computation q*x'Sigma x/K^2 - (1-q)*mu'x/K.
- [ ] A selection of K+1 assets returns `feasible=false` with a cardinality violation.
- [ ] Sector cap 1 with two picks in the same sector returns `feasible=false` and names the sector.
- [ ] Target return above the selection's net return returns `feasible=false` with a target-return violation.
- [ ] The stub `pipeline.run` returns a `RunResult` that validates.

## Verify

```
cd backend; uv sync; uv run pytest -q; uv run python scripts/smoke.py
```

## Done checklist

- [ ] `uv run pytest -q` and `smoke.py` pass; `uv.lock` committed.
- [ ] Examples are consistent and contain no banned phrases.
- [ ] CONTRACTS.md, `contracts.py` and the examples agree.
- [ ] Committed and pushed to `team-1/work`; Wahab merges it to `main` before anyone else clones, then everyone runs `git pull origin main`.

## When finished

1. Run the verify command above.
2. If it fails, fix it only inside your owned paths and run it again (up to 3 tries). If it still fails, stop and print the error.
3. When it passes: `git add -A`, then `git commit -m "team-1: U1 <short summary>"`.
4. Then `git push -u origin team-1/work`. Never force-push. Never push to `main`.
5. Print a 3-line summary: what was built, the test result, and any known gap.
6. If git reports a conflict or asks for a login, stop and say so. Do not resolve it; Wahab does.
