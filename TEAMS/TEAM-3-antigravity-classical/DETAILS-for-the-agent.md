# TEAM-3 DETAILS for the agent: Classical baselines and metrics

Teammates do not need to read this file. The prompt files tell the agent to read it. Human steps are in `START-HERE.md`.

Tool: Google Antigravity (Planning mode, Request review).

## Mission

Give QAOA an honest opponent and an honest judge. Deliver exact brute force with the full feasible landscape, a CVXPY relaxation with rounding and seeded simulated annealing, all on the same `Problem` and QUBO as QAOA (R14), plus the metrics, frontier data and rule-based verdict that say plainly how QAOA compared, including neutral or negative outcomes (R15, R16, frontier part of R20). You never re-implement feasibility: `Problem.evaluate` is the only judge.

## Your units

| U-ID | Title | When | Depends on |
|---|---|---|---|
| U8 | Classical baselines | Build (T0 to T0+2.5h) | U1 (U5 for SA's real QUBO) |
| U9 | Metrics, frontier, verdict | Build | U1, U8 |
| U10 support | Fix metrics/baselines defects found in integration | Integrate (T0+2.5h to T0+4h) | U10 |
| U15 (your part) | Integration tests on the real pipeline | Evidence + demo (T0+4h to T0+5h) | U10 |

## Owned paths

- `backend/qportfolio/classical/` (`__init__.py`, `brute_force.py`, `relaxation.py`, `annealing.py`)
- `backend/qportfolio/{metrics.py,frontier.py,verdict.py}`
- `backend/tests/{test_classical,test_metrics}.py`

## Do not touch

- `backend/qportfolio/{contracts.py,problem.py,pipeline.py}`, `qubo/`, `quantum/`, `backend/scripts/`, `backend/data/studies/`, `contracts/`, `backend/pyproject.toml`, `backend/uv.lock`, `docs/`, `TEAMS/`, `AGENTS.md`, `CLAUDE.md` (TEAM-1).
- `backend/qportfolio/{data,api}/`, `backend/scripts/fetch_snapshot.py`, `backend/data/{nifty50.csv,snapshot/}` (TEAM-2).
- `frontend/` (TEAM-4).
- Never edit `Problem.evaluate`. Need a new dependency, a contract change, or a type missing from `contracts.py`? Ask TEAM-1 in chat.

## Interfaces you provide

- CONTRACTS.md §1.4:
  - `brute_force(problem) -> (SolverResult, Landscape)`
  - `relaxation(problem) -> SolverResult`
  - `annealing(problem, qubo, seed=7, sweeps=2000) -> SolverResult`
  - `qaoa_metrics(samples, landscape) -> QaoaMetrics`
  - `frontier(market_subset, landscape) -> Frontier` (shape in §2.6 `frontier`)
  - `verdict(solvers, landscape, qaoa) -> Verdict` (shape in §2.6 `verdict`)
- `Landscape` is consumed by TEAM-1's QAOA engine (U6) and studies (U14).

## Interfaces you consume

- §1.1 `Problem` and `Problem.evaluate` (ready at T0 from U1) for every objective and feasibility check.
- §1.3 `Qubo` for `annealing` (arrives with U5). Until then use a throwaway stub QUBO with the `Qubo` fields in `backend/tests/test_classical.py` (not in `qubo/`); switch to `build_qubo` after `git pull origin main`.
- §1.2 `Market.subset` shape (`tickers`, `sectors`, `mu`, `sigma`) for `frontier`. Until U3 lands, use a minimal stub object in the test file.
- Types `SolverResult`, `Landscape`, `Sample`, `QaoaMetrics`, `Frontier`, `Verdict` from `backend/qportfolio/contracts.py`. If one is missing, ask TEAM-1; do not define your own.
- Example payloads in `contracts/api-examples/` (read-only) for field names and shapes.

## How to verify

```
cd backend; uv run pytest tests/test_classical.py tests/test_metrics.py -q
uv run pytest -q
```

- Brute force on 16 assets with K=8 (12,870 subsets) runs in under 2 s.
- Banned phrases ("advantage", "outperforms classical", "quantum speedup") never appear in any verdict text (test over all four levels).
- Manual: call `brute_force` on the example instance and compare its optimum with `contracts/api-examples/job_done.json` shape (fields present, `volatility` = sqrt(`variance`)).

## Definition of done

- [ ] U8 and U9 test scenarios exist as pytest tests and pass; `uv run pytest -q` is green.
- [ ] Brandhofer fixture (or the hand-checked 4-asset case) matches; SA reach-optimum rate recorded honestly.
- [ ] Banned-phrase verdict test green (honesty gate).
- [ ] No feasibility logic outside `Problem.evaluate`; no repair of infeasible results.
- [ ] No banned APIs, no new dependencies, no files outside owned paths.
- [ ] Committed and pushed to `team-3/work`; 3-line summary printed (Wahab merges).

## Handoff

- One branch only: `team-3/work`. The agent commits and pushes it at the end of every prompt (see "When finished" in each prompt file). Never push to `main`, never force-push.
- Wahab (TEAM-1) opens the pull requests, merges and resolves conflicts. If `git pull origin main` reports a conflict, stop, do not resolve it, and tell the user to message Wahab.
- Final message of every prompt: a 3-line summary (what was built, test result, known gaps).

## Pitfalls

- Never re-implement feasibility or the objective: call `Problem.evaluate`. A vectorised shortcut needs a test proving it equals `Problem.evaluate`.
- CVXPY needs `cp.quad_form(x, cp.psd_wrap(Sigma))`; the default solver (OSQP) is fine. A rounded relaxation may be infeasible: report it, do not repair it.
- Verdict wording: no "advantage", "outperforms classical", "quantum speedup". Follow the wording style of the sample in CONTRACTS §2.6 ("no speed benefit is claimed at this size").
- Landscape holds feasible selections only. `f_min`/`f_max` for the approximation ratio are feasible-only. Mark ties for the optimum with a 1e-9 tolerance.
- QUBO variable order is assets first, then slack: SA must decode `x[:n_assets]` and evaluate exactly; slack bits never become tickers.
- Bitstrings you return are asset order, x0 first. No qiskit imports are needed in `classical/`.
- Seed everything (SA uses `numpy.random.default_rng(seed)`); tests must be deterministic and fast.
- Do not tune SA or its test to hide a miss. A neutral or negative result is valid evidence.
