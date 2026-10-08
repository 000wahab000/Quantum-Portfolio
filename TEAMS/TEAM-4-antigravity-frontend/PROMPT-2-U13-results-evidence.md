Paste this whole file into your agent (or @-mention it). Team 4, unit U13.

# TEAM-4 · U13 — Frontend results views, charts, evidence page

Integrate phase (T0+2.5h to T0+4h). Depends on U12 on your branch or `main`. Branch `team-4/work`.

## Read first

- `AGENTS.md`
- `TEAMS/CONTRACTS.md`: section 2.3 (`Sample`), section 2.6 (`RunResult`: `solvers`, `qaoa`, `frontier`, `benchmarks`, `verdict`, `recommended`, no-feasible rule), section 2.7 (`Study`)
- `TEAMS/TEAM-4-antigravity-frontend/DETAILS-for-the-agent.md`
- `TEAMS/TEAM-4-antigravity-frontend/DESIGN.md` (chart series colours, histogram colours, contrast rules)
- Plan `docs/plans/2026-10-08-2115-feat-quantum-portfolio-optimiser-plan.md`: R9, R15, R16, R17, R20, R21, R22, F2, section "U13. Frontend results views, charts, evidence page"
- `contracts/api-examples/job_done.json`, `studies_index.json`, `study_depth.json`

## Process

Plan first, list the exact files, and stop for review before editing. Edit only `frontend/`.

## Goal

Show the result and the evidence clearly to a non-quantum user.

## Owned paths / Do not touch

- Owned: `frontend/`.
- Do not touch: everything outside `frontend/`. No new dependencies (Recharts 3 only for charts).

## Files (exact)

- `frontend/src/components/PortfolioTable.tsx`, `MetricCards.tsx`, `SolverTable.tsx`, `FrontierChart.tsx`, `ConvergenceChart.tsx`, `BitstringHistogram.tsx`, `HonestyPanel.tsx`, `OutOfSample.tsx`, `StudyChart.tsx`
- `frontend/src/lib/chartColors.ts` (series and histogram colours from DESIGN.md, defined once)
- `frontend/src/pages/Evidence.tsx`; wire the result views into `frontend/src/pages/Optimise.tsx`

## Approach

1. Recharts 3 throughout; wrap each chart in `ResponsiveContainer` inside a parent with an explicit height. Do not copy Recharts 2 snippets blindly (removed props such as `activeIndex`); follow the 3.x docs and confirm with `npm run build`.
2. `FrontierChart`: scatter plot with x = annualised risk (volatility) and y = annualised return. Continuous line from `frontier.continuous`, discrete points greyed out, each solver as a labelled marker at its `volatility` / `exp_return`; solvers with null numbers are listed beneath instead of plotted.
3. `BitstringHistogram`: top 20 `qaoa.samples` by `prob`, coloured optimal / feasible / infeasible, with a legend that explains each; the bitstring is asset order, x0 first.
4. `HonestyPanel`: verdict level badge, `headline`, `details`, plus a "P(opt) vs random guess" line from `qaoa.metrics.p_opt` and `p_random`, and `feasible_rate`; when `qaoa.noise` is set, show ideal vs noisy metrics and transpiled depth / two-qubit gates. Neutral wording only; never "advantage", "beats", "outperforms".
5. `PortfolioTable`: rows (ticker, name, sector, weight, shares, price, value), `invested`, `cash_left`. Default to the solver in `result.recommended` with a selector for the others. If a QAOA solver has `selection: null`, show "QAOA found no feasible portfolio" with its `feasible_rate`; nothing else breaks.
6. `MetricCards`: expected return, volatility and variance, objective, transaction cost for the selected solver. `SolverTable`: every solver (objective, `exp_return`, `volatility`, feasible, `runtime_s`; for QAOA also `approx_ratio`, `p_opt`, `feasible_rate`). `OutOfSample`: each solver's `oos` and the `benchmarks.nifty50` block, labelled with the test window dates. `ConvergenceChart`: `qaoa.convergence` (iteration vs energy).
7. `Evidence.tsx`: `GET /api/studies`, then `GET /api/studies/{id}` per study. `StudyChart` renders any number of `series` generically with `x_label` / `y_label`, optional `yerr` error bars, and shows the instance details (`n_assets`, `k`, `q`, `seeds`, `shots`), `generated_at`, `wall_time_s`, `notes` and data dates.
8. Chart colours come only from DESIGN.md: one fixed colour per series in every chart and in the frontier (QAOA standard, QAOA XY, brute force, relaxation, simulated annealing, NIFTY 50 dashed); histogram optimal / feasible / infeasible as DESIGN.md says, with a legend in words. Define the series colours once in `frontend/src/lib/chartColors.ts`, never inline hex per chart. Error text uses #FF8A8A on #541A2E, never red text on navy; colour is never the only signal (add a label or icon).
9. Mobile: tables inside an `overflow-x-auto` wrapper (never the page), charts keep a minimum height, no horizontal page scroll at 375 px. Format annualised decimals as percentages (0.12 -> 12%).

## Interfaces

- Provide: none to other teams.
- Consume: section 2.6 `RunResult` via `GET /api/runs/{job_id}` (`state: "done"`), section 2.7 `Study` via `/api/studies`. Use the mock examples with `VITE_USE_MOCKS=1` until TEAM-2's API and TEAM-1's pipeline are merged.

## Test scenarios (build plus manual)

- [ ] `npm run build` passes.
- [ ] Manual with `job_done.json`: every R20 element is visible (portfolio table, return/variance/objective, frontier with all solvers, convergence curve, bitstring histogram with feasible states marked, honesty panel), and solver markers on the frontier match the solver table values.
- [ ] Manual with an example where QAOA has `selection: null` (edit a copy of `job_done.json` locally in the mock): the UI shows "QAOA found no feasible portfolio" and nothing breaks.
- [ ] Manual: each study in `studies_index.json` renders with axis labels, and the instance details show seeds and dates.
- [ ] Manual at 375 px: no horizontal scroll.

## Verify

```
cd frontend; npm run build
$env:VITE_USE_MOCKS="1"; npm run dev
```

Then run against the real API: start the backend (`cd backend; uv run uvicorn qportfolio.api.main:app --reload --reload-dir qportfolio --port 8000`) and `cd frontend; npm run dev`.

## Done checklist

- [ ] Build passes; manual checks pass on desktop and phone width.
- [ ] Every number on screen comes from the payload (no hard-coded values).
- [ ] No "advantage" wording; neutral and negative verdicts render fine.
- [ ] Committed and pushed to `team-4/work`; 3-line summary printed (Wahab opens the PR and merges).

## When finished

1. Run the verify command above.
2. If it fails, fix it only inside your owned paths and run it again (up to 3 tries). If it still fails, stop and print the error.
3. When it passes: `git add -A`, then `git commit -m "team-4: U13 <short summary>"`.
4. Then `git push -u origin team-4/work`. Never force-push. Never push to `main`.
5. Print a 3-line summary: what was built, the test result, and any known gap.
6. If git reports a conflict or asks for a login, stop and say so. Do not resolve it; Wahab does.
