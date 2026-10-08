# Research: Environment spike (verified on team laptop, Windows 11, 2026-10-08)

**Verdict:** the full stack installs from wheels and all six smoke checks pass on CPython 3.13.14, and also on 3.14.6. The spike code is in `backend/scripts/smoke.py` (copied from the spike).

## Verified versions
| Package | Version |
|---|---|
| qiskit | 2.5.2 |
| qiskit-aer | 0.17.2 |
| qiskit-ibm-runtime | 0.50.0 |
| cvxpy | 1.9.3 (solvers: CLARABEL, SCS, SCIPY, HIGHS, OSQP) |
| yfinance | 1.7.0 |
| pandas | 3.0.6 |
| numpy | 2.5.3 |
| scipy | 1.18.1 |
| pyarrow | 25.0.1 |
| fastapi | 0.143.0 |
| uvicorn | 0.54.0 |
| pydantic | 2.14.0 |
| pytest | 9.1.1 |
| httpx2 | 2.13.1 (dev; needed by starlette TestClient) |

`qiskit-optimization` 0.7.0 also resolves cleanly, but we don't depend on it.

## Patterns that work
- **Counts (V2):**
  - Get counts with `qc.measure_all()`, then `StatevectorSampler(default_shots=N, seed=s).run([bound]).result()[0].data.meas.get_counts()`.
  - Qubit 0 is the **rightmost** character of the bitstring.
- **Expectation loop:** run `StatevectorEstimator` on a **flattened** ansatz. Decompose until no `QAOA` or `PauliEvolution` ops remain. This takes ~10 ms per eval, against ~270 ms raw.
- **Noise:**
  - Use `FakeGuadalupeV2` (16q). Building `NoiseModel.from_backend` takes 0.9 s.
  - Transpile with `generate_preset_pass_manager(optimization_level=1|3, backend=fake)`.
  - Sampler: `qiskit_aer.primitives.SamplerV2(default_shots, seed, options={"backend_options": {"noise_model": nm}})`.
  - Estimator: `EstimatorV2(options={"backend_options": {"noise_model": nm}})` with `H.apply_layout(isa.layout)`.
  - A 2048-shot noisy run takes 0.3–0.5 s.
  - FakeSherbrooke (127q) also works but is ~10× slower.
- **XY mixer:**
  - Pass `QAOAAnsatz(cost_operator=H, reps, initial_state=dicke_circuit(n,k), mixer_operator=<circuit of XXPlusYYGate(2β,0) on ring pairs>)`.
  - All samples keep Hamming weight k when noiseless.
  - The deterministic Bärtschi–Eidenbenz Dicke circuit has fidelity 1.0.
  - Cost on Guadalupe at n=6: ~285 CX for XY versus ~70 CX for standard QAOA. This is why XY degrades more under noise.
- **cvxpy:** `cp.quad_form(x, cp.psd_wrap(Sigma))`. The default solver is OSQP.
- **yfinance:**
  - `yf.download(...)` returns MultiIndex columns `(Price, Ticker)`.
  - Tickers come back **alphabetically**, so reorder with `df["Close"][tickers]`.
  - `end` is exclusive, and the index is tz-naive.

## Gotchas
1. Run `uv python pin 3.13`. Otherwise uv silently picks 3.14.
2. First install takes ~10 min (scipy and pyarrow downloads). After that, the uv cache makes it instant.
3. Set `PYTHONUTF8=1`, or reconfigure stdout to UTF-8. Otherwise printing β/γ parameter names crashes under cp1252.
4. Never pass a raw `QAOAAnsatz` to the Aer primitives. It fails with `AerError: 'unknown instruction: QAOA'`. Decompose or transpile first.
5. Run `uvicorn --reload` with `--reload-dir app`. Otherwise `.venv` changes trigger reload loops.
6. `qiskit_ibm_runtime.SamplerV2`/`EstimatorV2` are deprecated in 0.50. Local Aer avoids them.
7. The repo path contains spaces (`D:\wahab stuff\...`). This is untested, so quote paths in scripts.
