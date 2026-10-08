# Research: Qiskit Finance tutorial 01 (Portfolio Optimization)

Source: https://qiskit-community.github.io/qiskit-finance/tutorials/01_portfolio_optimization.html. The rendered page targets qiskit 1.0.1, qiskit_finance 0.4.1, qiskit_algorithms 0.3.0, qiskit_optimization 0.6.1 and qiskit_aer 0.13.3. It uses **V1 primitives** and is outdated for Qiskit 2.x.

## Formulation
min_{x∈{0,1}^n}  q·xᵀΣx − μᵀx   s.t. 1ᵀx = B

- q is the risk factor and B is the budget, i.e. the cardinality K.
- The equality constraint becomes a soft penalty (1ᵀx − B)² inside `MinimumEigenOptimizer` via `QuadraticProgramToQubo`.
- The printed tables show infeasible states (Hamming weight ≠ B) still carrying probability mass. The penalty is soft.

## API (tutorial-era)
```python
from qiskit_finance.applications.optimization import PortfolioOptimization  # (expected_returns, covariances, risk_factor, budget, bounds=None)
from qiskit_finance.data_providers import RandomDataProvider, YahooDataProvider
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import NumPyMinimumEigensolver, QAOA, SamplingVQE
from qiskit_algorithms.optimizers import COBYLA
from qiskit_aer.primitives import Sampler   # V1, removed in Qiskit 2.x era
```
- `PortfolioOptimization(...).to_quadratic_program()` returns a QuadraticProgram with 1 linear equality constraint.
- `.interpret(result)` returns the selected indices. `.portfolio_expected_value(result)` and `.portfolio_variance(result)` are also available.

Tutorial settings: n=4, q=0.5, B=2, QAOA reps=3, COBYLA maxiter=250, seed 1234. All solvers find `[1,0,0,1]`.

## Bitstring decoding gotcha
Qiskit bitstrings are little-endian. Reverse the key string so that x_0 is the leftmost element: `x = [int(c) for c in reversed(key)]`.

## Take-aways for our build
- Reuse `PortfolioOptimization` only as a **cross-check** of our own QP builder. We need extra constraints (sectors, lots, costs), so we build the `QuadraticProgram` ourselves.
- `result.x` (the best sample found) is not the same as the most-probable state. Report both, plus P(optimal).
- Port the tutorial to the V2 primitives (StatevectorSampler / Aer SamplerV2). Verify against the version-state report.
