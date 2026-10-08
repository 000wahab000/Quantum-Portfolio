Paste this whole file into your agent (or @-mention it). Team 2, unit U4.

# TEAM-2 · U4 — Pre-screen, costs, allocation, out-of-sample

Build phase (T0 to T0+2.5h). Depends on U1 and U3 (U3 merged, or on your branch). Branch `team-2/screen-costs`.

## Read first

- `AGENTS.md`
- `docs/teams/CONTRACTS.md`: section 1.2 (`prescreen`, `linear_costs`, `to_shares`, `out_of_sample`), section 2.4 (`ScreenInfo`), section 2.6 (`portfolio` and `oos` blocks)
- `docs/teams/TEAM-2.md`
- Plan `docs/plans/2026-10-08-2115-feat-quantum-portfolio-optimiser-plan.md`: KTD5, KTD11, section "U4. Pre-screen, costs, allocation, out-of-sample", AE1, AE3
- `docs/research/06-nifty50-costs.md` (cost model, risk-free rate)

## Process

Plan first, list the exact files, and stop for review before editing. Edit only owned paths. Test-first.

## Goal

Supply the declared pre-screen, the cost terms for the QUBO, whole-share portfolios and held-out scoring.

## Owned paths / Do not touch

- Owned: `backend/qportfolio/data/`, `backend/qportfolio/api/`, `backend/scripts/fetch_snapshot.py`, `backend/data/nifty50.csv`, `backend/data/snapshot/`, `backend/tests/{test_data,test_screen_costs,test_api}.py`.
- Do not touch: `contracts.py`, `problem.py`, `pipeline.py`, `qubo/`, `quantum/`, `classical/`, `metrics.py`, `frontier.py`, `verdict.py`, `contracts/`, `pyproject.toml`, `uv.lock`, `docs/`, `AGENTS.md`, `CLAUDE.md`, `frontend/`.

## Files (exact)

- `backend/qportfolio/data/screen.py`, `costs.py`, `allocate.py`, `evaluate.py`
- `backend/tests/test_screen_costs.py`

## Approach

1. `prescreen`: rank by estimation-window Sharpe (mu_i - rf)/sqrt(Sigma_ii). With a sector cap keep at most cap+1 per sector. Keep N = qubit_budget - slack bits, where slack bits = ceil(log2(cap+1)) per sector that still has more kept candidates than cap (an upper-bound estimate; reduce N until assets + slack <= budget). If the universe already fits, `applied=false`, `kept=[]`, `dropped=[]`. Raise a plain-language error if N < k. The `rule` text names the metric, the estimation window dates, rf, the per-sector limit and the qubit split, in the style of CONTRACTS 2.4.
2. `linear_costs`: tc(x) = lin.x + const as a fraction of capital. A buy costs C_BUY/K. A held position that is dropped costs C_SELL * its holding weight h_i. So lin_i = C_BUY/K for a non-held asset, lin_i = -C_SELL*h_i for a held one, const = sum of C_SELL*h_i over held. Top-ups of kept positions are free; state this in the docstring. `holdings_weights` are fractions of capital (the pipeline converts share counts).
3. `to_shares`: per-pick budget = capital/K; shares = floor(budget/price) at estimation-end prices; rows carry ticker, name, sector, weight (1/K), shares, price, value; `invested` = sum of values; `cash_left` = capital - invested.
4. `out_of_sample`: buy-and-hold equal-weight over the test window (no rebalancing); annualised return, volatility, Sharpe against rf, max drawdown (<= 0). `benchmark_oos(market, rf=RF)` does the same for `market.benchmark_test_returns` (^NSEI).

## Interfaces

- Provide (section 1.2): `prescreen(market, k, qubit_budget, sector_cap, rf=RF) -> ScreenInfo`; `linear_costs(tickers, k, holdings_weights) -> (lin, const)`; `to_shares(tickers, prices, capital, selection) -> portfolio block`; `out_of_sample(market, selection, rf=RF) -> oos block`; extra `benchmark_oos(market, rf=RF)`. `selection` is a list of tickers (as in `SolverResult.selection`); check `contracts.py` for exact types.
- Consume: `Market` and constants from U3 (`backend/qportfolio/data/risk.py`).

## Test scenarios

- [ ] AE1: 50 tickers, K=10, budget 16, no caps -> keeps 16 tickers, each kept Sharpe >= the best dropped Sharpe, `rule` text names the metric and the window.
- [ ] Sector cap 2 -> no more than 3 kept tickers from any one sector.
- [ ] AE3: holdings in A and B; a selection keeping A and B has lower tc than one swapping both out.
- [ ] No holdings -> tc equals the sum of buy costs over the selection.
- [ ] Capital 1,000,000, K=5, known prices -> shares are floors of 200000/price and `cash_left` = capital - invested >= 0.
- [ ] A price above the per-asset budget -> shares 0 and value 0 (the row stays; shares=0 is the flag), no crash.
- [ ] Synthetic series that doubles -> out-of-sample annualised return computed correctly and max drawdown is 0.

## Verify

```
cd backend; uv run pytest tests/test_screen_costs.py -q; uv run pytest -q
```

The screen output for the default request matches the shape of `contracts/api-examples/screen.json`.

## Done checklist

- [ ] All scenarios above exist as pytest tests and pass; full suite green.
- [ ] Only estimation-window data feeds the screen (no look-ahead).
- [ ] Committed on branch `team-2/screen-costs`, PR to `main`; summary posted.
