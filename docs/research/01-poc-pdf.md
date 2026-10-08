# Research: Team POC (4 GOATS, PS-03), summary

Source: `D:\FinTech_PS-3_4 Goats_Wahab_Shaikh.pdf` (3 pages: 2 with content, 1 blank). This is a proposal and contains no experimental results.

## What the POC commits to
- **Universe:** NIFTY 50 pool. The example 10-stock universe is RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK, HINDUNILVR, ITC, SUNPHARMA, LT, BHARTIARTL. One qubit per stock gives 10 qubits.
- **Data:** yfinance daily prices, cached locally, with missing-data handling. Estimation and test windows are kept separate to avoid look-ahead bias. The lookback window is "documented" but its length is not given.
- **Model:** mu and Sigma estimated over the estimation window. Objective: maximise return minus risk, with a risk-aversion parameter.
- **Constraints:**
  - Cardinality sum x_i = K is enforced **exactly** by a Dicke-state initial state plus an XY mixer.
  - Sector caps, minimum target return and an Indian transaction-cost model are pluggable QUBO penalty terms.
- **QAOA:**
  - Depth p = 1..5.
  - Optimisers: COBYLA vs SPSA.
  - Initial points: random vs warm start.
  - Decoding: rank the sampled bitstrings and filter out those below the target return.
- **Baselines ("Quantum Honesty Panel"):**
  - Brute force (2^10 = 1024 portfolios).
  - CVXPY relaxation, then rounding, then local search.
  - Simulated annealing.
  - Tabu search.
  - All baselines get the same data, constraints and budgets. Results are reported as mean ± CI over seeds for approximation ratio, P(optimum), feasibility and time-to-target. An auto verdict includes neutral outcomes.
- **Noise:** re-run the best configuration under an Aer noise model built from a fake IBM backend. No real hardware.
- **UI:**
  - Investor inputs: K, risk aversion, constraints.
  - Ranked portfolio menu built from the top QAOA bitstrings.
  - Consensus heatmap: which solvers pick which stock, grouped by sector, with caps marked.
  - Recommended portfolio: return, volatility and Sharpe, plotted against the efficient frontier.
- **Stack:** Python, yfinance, pandas, NumPy, SciPy, Qiskit (+ Finance, Algorithms, ML), Aer, CVXPY, FastAPI, React + Vite, Recharts or Plotly.

## Gaps the build must close
1. **Weights are missing.** Binary selection does not give portfolio weights. Decide an explicit scheme: equal weight, or lot-encoded weights. The PS also asks for "min/max weight via binary lot encoding".
2. **XY mixer vs sector caps.** The XY mixer preserves only the Hamming weight. Sector caps remain soft penalties, so feasibility depends on the penalty weights. Report a feasibility ratio.
3. **Target return is applied twice.** It is both a penalty and a post-filter. Choose one authoritative mechanism; the post-filter is only a display ranking.
4. **Transaction cost has no reference point.** It needs a reference holding: either the current portfolio or the costs of entering from cash.
5. **Undefined numbers.** Lookback length, split ratio, R_f, seed count, CI method, budget units and verdict thresholds are not given and must be fixed and documented.
6. **No rigour items.** No survivorship-bias note, no adjusted-price policy, no shrinkage estimator, and no out-of-sample evaluation are stated.
7. **Advantage claims.** At n = 10, brute force is trivial, so the project cannot claim a quantum advantage. Frame the outcome honestly as a benchmark.
