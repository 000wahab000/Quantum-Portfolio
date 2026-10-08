# PS-03: Portfolio Optimisation using Quantum Computing

Part of VESIT's Qiskit Fall Fest 2026. The training is given during the official sessions. The problem statement below is copied verbatim as the team received it. **It is the product authority:** where it conflicts with the POC, the PS wins.

## Background
Pick 10 stocks out of 50. Respect sector caps, lot sizes and transaction costs. Maximise return for the risk you are willing to take. Every stock is a yes-or-no decision, which means 2^50 possible portfolios, and no analyst can check them all by hand.

This is the shape of the problem that QAOA was designed for. Yet anyone can wrap a circuit around a classical solver and call the result quantum. The real problem is making the formulation faithful, the quantum part genuine, and the comparison with classical methods honest, from raw prices to a portfolio and back.

## Problem Statement
Build a portfolio optimiser in Qiskit that takes a market dataset to a selected portfolio: formulated as a QUBO, solved with QAOA, constrained by real investment rules, and benchmarked against classical solvers. It must work across different universe sizes and constraint sets, and be wrapped in a clear, interactive web interface that a non-quantum user can actually use.

## Objective
1. **Data & risk model:** Pull historical daily prices from a free API or open-source dataset (e.g. Yahoo Finance via yfinance, Alpha Vantage free tier, Stooq, or public Kaggle datasets). Compute returns, expected returns (mu) and the covariance matrix (Sigma). Handle missing data, document the lookback window, and keep estimation and test periods separate so there is no look-ahead bias.
2. **QAOA solver:** Solve the selection problem with QAOA. Study the effect of circuit depth, compare at least two classical optimisers, and compare at least two initial-point strategies (e.g. random vs. warm start). The quantum circuit must genuinely produce the answer.
3. **Constraints:** At least two constraint types beyond cardinality, e.g. sector caps, min/max weight via binary lot encoding, target return, or transaction cost. Adding a new constraint must not mean rewriting the solver.
4. **Classical baselines:** Exact brute force for small universes, a classical relaxation with rounding, and one heuristic (greedy or simulated annealing). Baselines get the same data and constraints.
5. **Noise & hardware realism:** Re-run the best configuration under a noise model from a fake backend and report the degradation. A run on real IBM hardware is optional, and if done, must include job IDs.
6. **Interactive UI/UX:** A polished web app is a core deliverable, not an afterthought. Users pick assets and set risk appetite, portfolio size and constraints, run the optimiser, and watch results update. Show the selected portfolio with return, variance and objective value against the efficient frontier and the classical solutions, plus convergence curves and the sampled bitstring distribution. Handle loading, errors and long-running quantum jobs gracefully, and make it usable on mobile.

## Allowed Tools and Rules
1. **Quantum stack:** Qiskit and its extension libraries: Qiskit Optimization, Qiskit Finance, Qiskit Algorithms, Qiskit Machine Learning, Qiskit Aer for simulation, and Qiskit IBM Runtime for fake backends and optional hardware.
2. **Classical & frontend stack:**
   - Python: NumPy, SciPy, pandas, scikit-learn, CVXPY, with FastAPI or Flask to serve the Qiskit backend.
   - Frontend: React with Vite, Tailwind CSS (or similar), and a charting library such as Recharts, D3 or Plotly.
   - No paid or closed-source solver for the core optimisation.
3. **Data:** Free APIs or open-source datasets only. The organisers do not supply data. Cache what you fetch so the app still works if the API is down or rate-limited.
4. **Hardware:** Real-device runs are optional and subject to your IBM Quantum plan quota and queue times.
5. **Not allowed:**
   - Solving classically and wrapping the answer in a circuit.
   - Injecting the known optimal bitstring as an undeclared initial state.
   - Using future data in estimation.
   - Claiming quantum advantage without evidence.

   Neutral or negative findings are welcome if the evidence is rigorous.
