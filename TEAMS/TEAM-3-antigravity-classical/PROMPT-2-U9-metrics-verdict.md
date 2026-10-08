Paste this whole file into your agent (or @-mention it). Team 3, unit U9.

# TEAM-3 · U9 — Metrics, frontier, verdict

Build phase (T0 to T0+2.5h). Depends on U1 and U8 (`Landscape`). `git pull origin main` first; branch `team-3/work`.

## Read first

- `AGENTS.md`
- `TEAMS/CONTRACTS.md`: section 1.4 (`qaoa_metrics`, `frontier`, `verdict`, `Sample`), section 2.3 (`Sample`), section 2.6 (`qaoa.metrics`, `frontier`, `verdict`, banned-phrase note)
- `TEAMS/TEAM-3-antigravity-classical/DETAILS-for-the-agent.md`
- Plan `docs/plans/2026-10-08-2115-feat-quantum-portfolio-optimiser-plan.md`: KTD6, section "U9. Metrics, frontier, verdict", AE2
- `docs/research/04-arxiv-2207.10555.md` (approximation ratio, Eq. 8)

## Process

Plan first, list the exact files, and stop for review before editing. Edit only owned paths. Test-first.

## Goal

Compute the honest comparison numbers, the frontier data and the plain-language verdict.

## Owned paths / Do not touch

- Owned: `backend/qportfolio/classical/`, `backend/qportfolio/{metrics.py,frontier.py,verdict.py}`, `backend/tests/{test_classical,test_metrics}.py`.
- Do not touch: `contracts.py`, `problem.py`, `pipeline.py`, `qubo/`, `quantum/`, `data/`, `api/`, `contracts/`, `pyproject.toml`, `uv.lock`, `docs/`, `TEAMS/`, `AGENTS.md`, `CLAUDE.md`, `frontend/`.

## Files (exact)

- `backend/qportfolio/metrics.py`, `frontier.py`, `verdict.py`
- `backend/tests/test_metrics.py`

## Approach

1. `qaoa_metrics(samples, landscape) -> QaoaMetrics`:
   - `approx_ratio` = expected value over samples of r, weighted by `prob`; for a feasible sample r = (f_max - F)/(f_max - f_min) using the landscape's feasible-only f_min and f_max (guard zero range); r = 0 for infeasible samples (Brandhofer Eq. 8).
   - `p_opt` = total probability of optimal samples (compare with `landscape.optimum`, tolerance 1e-9 for ties).
   - `p_random` = 1/|feasible| (number of feasible selections in the landscape).
   - `feasible_rate` = total probability of feasible samples.
   - `top_samples` = top 20 by probability, each annotated `feasible` and `optimal`.
2. `frontier(market_subset, landscape) -> Frontier`:
   - `continuous`: long-only mean-variance frontier, a CVXPY sweep of 25 return targets (minimise x'Sigma x with `cp.psd_wrap`, sum x = 1, x >= 0, mu'x >= target), as `{risk, ret}` with risk = sqrt(variance).
   - `discrete`: K-of-n equal-weight Pareto points from the landscape (non-dominated in risk/return), each with its `selection` tickers (from `market_subset.tickers`).
3. `verdict(solvers, landscape, qaoa) -> Verdict` (rule-based): level `matched` (QAOA best objective equals the exact optimum), `near` (relative gap <= 1%), `worse`, or `no-feasible` (QAOA found no feasible sample). Gap = (F_qaoa - F_opt)/max(|F_opt|, 1e-12). Always add:
   - the P(opt) versus random-guess line (for example "It sampled the exact optimum with probability 8.3%, 17x more often than a random guess (0.48%).");
   - a runtime comparison sentence (classical solved this n-stock instance exactly in X s);
   - a size disclaimer (simulated, n <= 16 qubits; says nothing about larger instances).
   Never use the banned phrases "advantage", "outperforms classical", "quantum speedup" (case-insensitive). The sample wording in CONTRACTS 2.6 ("no speed benefit is claimed at this size") is the style to follow. Handle `qaoa=None` without crashing (ask TEAM-1 which level the contract wants).
4. Until U3 lands, stub a minimal market object (`tickers`, `sectors`, `mu`, `sigma`) inside the test file.

## Interfaces

- Provide (section 1.4): `qaoa_metrics(samples, landscape) -> QaoaMetrics`, `frontier(market_subset, landscape) -> Frontier`, `verdict(solvers, landscape, qaoa) -> Verdict`.
- Consume: `Landscape`, `Sample`, `SolverResult` types (U1 `contracts.py`); `Landscape` from `brute_force` (U8); `Market.subset` shape from section 1.2 (`tickers`, `sectors`, `mu`, `sigma`).

## Test scenarios

- [ ] All samples on the optimum -> `approx_ratio` = 1 and `p_opt` = 1.
- [ ] All samples infeasible -> `approx_ratio` = 0, `feasible_rate` = 0 and the verdict level is `no-feasible`.
- [ ] Approx ratio uses feasible-only f_min and f_max: on a hand-built landscape the computed r matches the hand-computed value.
- [ ] Verdict text for any input (all four levels, `qaoa=None`) contains none of the banned phrases.
- [ ] Every point on the discrete Pareto frontier is non-dominated.
- [ ] Every continuous frontier point has weights summing to 1, each >= 0 (assert on an internal helper that returns the weights).

## Verify

```
cd backend; uv run pytest tests/test_metrics.py -q; uv run pytest -q
```

## Done checklist

- [ ] All scenarios above exist as pytest tests and pass; full suite green.
- [ ] Banned-phrase verdict test (honesty gate) is green.
- [ ] No banned APIs; no new dependencies.
- [ ] Committed and pushed to `team-3/work`; 3-line summary printed (Wahab opens the PR and merges).

## When finished

1. Run the verify command above.
2. If it fails, fix it only inside your owned paths and run it again (up to 3 tries). If it still fails, stop and print the error.
3. When it passes: `git add -A`, then `git commit -m "team-3: U9 <short summary>"`.
4. Then `git push -u origin team-3/work`. Never force-push. Never push to `main`.
5. Print a 3-line summary: what was built, the test result, and any known gap.
6. If git reports a conflict or asks for a login, stop and say so. Do not resolve it; Wahab does.
