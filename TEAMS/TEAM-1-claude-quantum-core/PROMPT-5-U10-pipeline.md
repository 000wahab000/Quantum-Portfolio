Paste this whole file into your agent (or @-mention it). Team 1, unit U10.

# TEAM-1 · U10 — Pipeline orchestrator

Integrate phase (T0+2.5h to T0+4h). Start only when U3, U4, U8, U9 are merged to `main` (`git pull origin main` first) and U5, U6 are done.

## Read first

- `AGENTS.md`
- `TEAMS/CONTRACTS.md`: all of section 1 (1.1 to 1.5), sections 2.2, 2.4, 2.5, 2.6
- `TEAMS/TEAM-1-claude-quantum-core/START-HERE.md`
- Plan `docs/plans/2026-10-08-2115-feat-quantum-portfolio-optimiser-plan.md`: KTD5, KTD10, section "U10. Pipeline orchestrator", AE1, AE2, AE5

## Process

Plan first, list the exact files, and stop for review before editing. Edit only owned paths.

## Goal

Run one `RunRequest` end to end, report progress, and return a `RunResult` that validates against `backend/qportfolio/contracts.py`.

## Owned paths / Do not touch

- Owned: `backend/qportfolio/pipeline.py`, `backend/tests/test_pipeline.py`.
- Do not touch: `data/`, `api/`, `classical/`, `metrics.py`, `frontier.py`, `verdict.py`, `frontend/`. If a teammate's function misbehaves, send the owner the failing call (use their `PROMPT-FIX-integration.md` prompt).

## Files (exact)

- `backend/qportfolio/pipeline.py` (replaces the stub; keep `Cancelled`)
- `backend/tests/test_pipeline.py`

## Approach

1. `build_market` -> `prescreen` if the universe exceeds the cap (pass `qubit_budget = qubit_cap`, minus 3 when `target_return` is set, because the 3-bit return slack is not visible to `prescreen`) -> `Market.subset(kept)` -> convert `RunRequest.holdings` (share counts) to weights with `est_end_prices` -> `linear_costs` -> `Problem` -> `build_qubo` with `tune_penalties`.
2. Run `brute_force` (gives the `Landscape`), `relaxation`, `annealing`, then `qaoa_solve` in the requested variant (`noisy_solve` when `settings.noise`).
3. `qaoa_metrics`, then per solver `to_shares` and `out_of_sample`, then `frontier`, `benchmarks.nifty50` from `benchmark_oos(market)` (TEAM-2), `verdict`. Set `recommended` to the feasible solver with the lowest objective (one-line rule, comment it).
4. Progress fractions: data 0.05, screen 0.1, qubo 0.15, classical 0.3, qaoa 0.3 to 0.9, wrap-up 1.0. `cancel` is checked between stages and inside QAOA; raise `Cancelled`, return no partial result.
5. A QAOA with no feasible sample is reported with `selection: null` (no repair); the verdict level is `no-feasible`.

## Interfaces

- Provide (section 1.5): `run(request, on_progress=None, cancel=None) -> RunResult`; `on_progress(fraction, stage, convergence_point | None)`; `Cancelled`.
- Consume: section 1.2 `build_market`, `Market.subset`, `prescreen`, `linear_costs`, `to_shares`, `out_of_sample`, `benchmark_oos`; section 1.3 `build_qubo`, `tune_penalties`, `qaoa_solve`, `noisy_solve`; section 1.4 `brute_force`, `relaxation`, `annealing`, `qaoa_metrics`, `frontier`, `verdict`; section 1.1 `Problem`.

## Test scenarios

- [ ] Default `contracts/api-examples/run_request.json` produces a `RunResult` that validates; every solver has a `portfolio` and an `oos` block.
- [ ] AE1: a request with all 50 tickers sets `screen.applied=true` and every solver's selection is a subset of `screen.kept`.
- [ ] `on_progress` fractions are monotonically non-decreasing and end at 1.0.
- [ ] A cancel mid-QAOA raises `Cancelled` and returns no partial result.
- [ ] AE3: with holdings in the request, the transaction cost appears in the objective breakdown.

## Verify

```
cd backend; uv run pytest tests/test_pipeline.py -q; uv run pytest -q
```

The default request finishes in under 60 s (about 10 assets, p <= 3, no noise, QAOA plus all baselines).

## Done checklist

- [ ] All scenarios above exist as pytest tests and pass; full suite green.
- [ ] `POST /api/runs` with the example request (TEAM-2's API) reaches `done` against the real pipeline.
- [ ] Committed and pushed to `team-1/work`; 3-line summary printed (Wahab opens the PR and merges).

## When finished

1. Run the verify command above.
2. If it fails, fix it only inside your owned paths and run it again (up to 3 tries). If it still fails, stop and print the error.
3. When it passes: `git add -A`, then `git commit -m "team-1: U10 <short summary>"`.
4. Then `git push -u origin team-1/work`. Never force-push. Never push to `main`.
5. Print a 3-line summary: what was built, the test result, and any known gap.
6. If git reports a conflict or asks for a login, stop and say so. Do not resolve it; Wahab does.
