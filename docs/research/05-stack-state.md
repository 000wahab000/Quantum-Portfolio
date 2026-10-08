# Research: Stack state as of 2026-10-08

Sources: PyPI/npm metadata plus official docs, collected by the research agent. These are **untested pins**; Unit 0 of the plan verifies them by actually installing.

## Qiskit ecosystem (important)
| Package | Latest | Status | Use? |
|---|---|---|---|
| qiskit | 2.5.2 | active, py>=3.10 | **yes**: `QAOAAnsatz`, `StatevectorSampler/Estimator`, `SparsePauliOp`, `generate_preset_pass_manager` |
| qiskit-aer | 0.17.2 | active (last release 2025-09) | **yes**: `AerSimulator(noise_model=NoiseModel.from_backend(fake))` |
| qiskit-ibm-runtime | 0.50.0 | active, needs qiskit>=2.3 | **yes**: `fake_provider` (FakeSherbrooke/Brisbane 127q, FakeTorino 133q, FakeFez 156q, FakeGuadalupeV2 16q, FakeCairoV2 27q); optional hardware via SamplerV2 |
| qiskit-optimization | 0.7.0 | **archived 2026-07-12**, supports qiskit 2.x on paper, ships `minimum_eigensolvers.QAOA`, `WarmStartQAOAOptimizer` | optional, as a cross-check only |
| qiskit-algorithms | 0.4.0 | unsupported by IBM | **no** |
| qiskit-finance | 0.4.1 | unsupported since 2023, pre-Qiskit-2 | **no**: write our own data layer |

**Decision driver:** build QAOA as `QAOAAnsatz` + V2 primitives + our own `scipy.optimize` loop. This is IBM's current tutorial pattern. It gives full control over the mixer (XY), the initial state (Dicke or warm start), the convergence callback and the initial points, and it avoids depending on archived code.

V1 primitives (`Sampler`, `Estimator`, `BackendSampler`), BackendV1 and the V1 fake backends are **removed** in Qiskit 2.x. Map bitstrings with `apply_layout` after transpiling. Bind parameters by `Parameter` object.

## Data
- **yfinance 1.7.0:** 429 rate limits are a known problem. Make one batched `yf.download`, cache to Parquet, and check in a fixture CSV. `auto_adjust=True` is the default, so use `Close`.
- **Stooq via pandas-datareader:** broken (needs an API key since 2026-03).
- **Alpha Vantage free tier:** 25 requests/day, so not viable for a multi-ticker universe.

## Classical
- **cvxpy 1.9.3** (py>=3.11) ships OSQP, Clarabel, SCS and HiGHS.
  - It solves the continuous QP relaxation for free (convex because Σ is PSD).
  - MIQP needs `pyscipopt` (SCIP, open source).
  - Brute force is exact up to n≈20.

## Frontend
- **Core:** React 19.3, Vite 8.3 (Node ≥20.19/22.12; we have Node 24), Tailwind 4.3 with `@tailwindcss/vite` (`@import "tailwindcss";`, no config file needed).
- **Charts:** Recharts 3.10. For the bitstring histogram and frontier, Plotly (`react-plotly.js` 4.1 + plotly.js 4.1, Node ≥22) is heavier. Prefer Recharts throughout unless a chart needs Plotly.

## Backend
- **API:** FastAPI (latest ~0.143, py>=3.10).
- **Long jobs:** a background job plus progress polling or SSE, so the UI can show live convergence.

## Local machine
Python 3.13.14, Node 24.18, npm 12, uv 0.11.29, gh 2.98.
