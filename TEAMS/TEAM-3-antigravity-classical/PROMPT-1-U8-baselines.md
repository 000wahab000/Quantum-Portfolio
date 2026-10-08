Paste this whole file into your agent (or @-mention it). Team 3, unit U8.

# TEAM-3 · U8 — Classical baselines

Build phase (T0 to T0+2.5h). Depends on U1 (`Problem` and `evaluate`). Uses `Qubo` from U5 for simulated annealing once it lands. `git pull origin main` first; branch `team-3/work`.

## Read first

- `AGENTS.md`
- `TEAMS/CONTRACTS.md`: section 1.1 (`Problem`, `Evaluation`), section 1.3 (`Qubo` fields), section 1.4 (`brute_force`, `relaxation`, `annealing`, `Landscape`), section 2.6 (`solvers[]` entry, `details` per solver)
- `TEAMS/TEAM-3-antigravity-classical/DETAILS-for-the-agent.md`
- Plan `docs/plans/2026-10-08-2115-feat-quantum-portfolio-optimiser-plan.md`: KTD2, KTD12, section "U8. Classical baselines"
- `docs/research/04-arxiv-2207.10555.md` (5-asset fixture), `docs/research/08-env-spike.md` (cvxpy `psd_wrap`)

## Process

Plan first, list the exact files, and stop for review before editing. Edit only owned paths. Test-first.

## Goal

Run three classical solvers on the same `Problem` and QUBO as QAOA, with honest, declared methods. Brute force also produces the landscape that QAOA metrics use.

## Owned paths / Do not touch

- Owned: `backend/qportfolio/classical/` (`__init__.py`, `brute_force.py`, `relaxation.py`, `annealing.py`), `backend/qportfolio/{metrics.py,frontier.py,verdict.py}`, `backend/tests/{test_classical,test_metrics}.py`.
- Do not touch: `contracts.py`, `problem.py`, `pipeline.py`, `qubo/`, `quantum/`, `data/`, `api/`, `contracts/`, `pyproject.toml`, `uv.lock`, `docs/`, `TEAMS/`, `AGENTS.md`, `CLAUDE.md`, `frontend/`. Never edit `Problem.evaluate`.

## Files (exact)

- `backend/qportfolio/classical/__init__.py`, `brute_force.py`, `relaxation.py`, `annealing.py`
- `backend/tests/test_classical.py`

## Approach

1. `brute_force(problem)`: enumerate `itertools.combinations(range(n), K)`. Feasibility and objective of each subset come from `Problem.evaluate` (never re-implement it); a vectorised numpy objective is allowed only as a speed-up, with a test asserting it equals `Problem.evaluate` on sampled subsets. Return a `SolverResult` plus a `Landscape` over feasible selections only (`selections` (F, n) 0/1, `objectives`, `returns`, `variances`, `f_min`, `f_max`, `f_mean`, `optimum`). Set `approx_ratio=1.0` as in the examples.
2. `relaxation(problem)`: CVXPY with `cp.quad_form(x, cp.psd_wrap(Sigma))`; minimise q*x'Sigma x/K^2 - (1-q)*(mu'x/K - (cost_lin.x + cost_const)); constraints 0 <= x <= 1, sum x = K, sector cap per sector (sum <= cap) and target return when set. Round by top-K of the relaxed `x` (ties by index). Report `details = {"relaxed_x": [...], "rounding": "top-K by relaxed value"}`. Evaluate the rounded set with `Problem.evaluate`; if infeasible, report it as infeasible. No hidden repair.
3. `annealing(problem, qubo, seed=7, sweeps=2000)`: single-flip Metropolis on the QUBO energy over all variables (assets then slack), geometric temperature schedule, `numpy.random.default_rng(seed)`. Track the best state; decode the asset bits, evaluate with `Problem.evaluate`; report infeasible as infeasible. `details = {"seed": seed, "sweeps": sweeps}`. An incremental energy delta is fine if a test confirms it against `Qubo.energy`.
4. All three return `SolverResult` with `solver` id (`brute_force`, `relaxation`, `annealing`), `label`, `kind="classical"`, `selection` (tickers), `bitstring` (asset order, x0 first), `objective`, `exp_return`, `volatility` (= sqrt(variance)), `variance`, `txn_cost`, `feasible`, `violations`, `runtime_s` (`time.perf_counter()`, > 0). Leave `portfolio` and `oos` unset: the pipeline fills them.
5. Until U5 lands, build a throwaway stub with the `Qubo` fields (Q, c, const, n_assets, n_slack, labels, penalties; cardinality penalty only) inside `backend/tests/test_classical.py`. After `git pull origin main` with U5 merged, switch the SA tests to `build_qubo`.

## Interfaces

- Provide (section 1.4): `brute_force(problem) -> (SolverResult, Landscape)`, `relaxation(problem) -> SolverResult`, `annealing(problem, qubo, seed=7, sweeps=2000) -> SolverResult`.
- Consume: section 1.1 `Problem`, `Problem.evaluate`; section 1.3 `Qubo` (SA only); types `SolverResult`, `Landscape` from `contracts.py` (ask TEAM-1 if one is missing; never define your own).

## Test scenarios

- [ ] Brandhofer 5-asset fixture (q = 1/3, B = 2): brute force finds {LIN, VNA} with F_min ~ -0.22608, F_max ~ 0.08191 and F_mean ~ -0.08986 (data in `docs/research/04-arxiv-2207.10555.md`). If the fixture values are not transcribed, use a hand-checked 4-asset case.
- [ ] Brute force respects sector caps: no returned selection violates them, and the landscape counts only feasible selections.
- [ ] On a convex instance, the relaxation's rounded selection is feasible and its objective is >= the brute-force optimum.
- [ ] SA with a fixed seed reaches the brute-force optimum on a 10-asset, K=5 instance in at least 8 of 10 seeds. If it does not, the test records the rate and the honest result (do not tune the test to pass).
- [ ] All three return `runtime_s > 0` and identical `objective` values for identical selections.
- [ ] The vectorised objective (if used) equals `Problem.evaluate` on sampled subsets.

## Verify

```
cd backend; uv run pytest tests/test_classical.py -q; uv run pytest -q
```

Brute force on 16 assets with K=8 (12,870 subsets) runs in under 2 s.

## Done checklist

- [ ] All scenarios above exist as pytest tests and pass; full suite green.
- [ ] No feasibility logic outside `Problem.evaluate`; no repair of infeasible results.
- [ ] No banned APIs (AGENTS.md `git grep`), no qiskit imports in `classical/`.
- [ ] Committed and pushed to `team-3/work`; 3-line summary printed (Wahab opens the PR and merges).

## When finished

1. Run the verify command above.
2. If it fails, fix it only inside your owned paths and run it again (up to 3 tries). If it still fails, stop and print the error.
3. When it passes: `git add -A`, then `git commit -m "team-3: U8 <short summary>"`.
4. Then `git push -u origin team-3/work`. Never force-push. Never push to `main`.
5. Print a 3-line summary: what was built, the test result, and any known gap.
6. If git reports a conflict or asks for a login, stop and say so. Do not resolve it; Wahab does.
