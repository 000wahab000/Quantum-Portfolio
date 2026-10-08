Paste this whole file into your agent (or @-mention it). Team 1, unit U6.

# TEAM-1 · U6 — QAOA engine (standard + XY), optimisers, init points

Build phase (T0 to T0+2.5h). Depends on U5.

## Read first

- `AGENTS.md`
- `TEAMS/CONTRACTS.md`: section 1.3 (`qaoa_solve`), section 2.2 (`qaoa` settings), section 2.3 (`Sample`), section 2.6 (`qaoa` block, `details.most_probable`, no-feasible rule)
- `TEAMS/TEAM-1-claude-quantum-core/START-HERE.md`, `docs/research/08-env-spike.md`, `backend/scripts/smoke.py`
- Plan `docs/plans/2026-10-08-2115-feat-quantum-portfolio-optimiser-plan.md`: KTD1, KTD6, KTD7, KTD8, KTD9, section "U6. QAOA engine (standard + XY), optimisers, init points"

## Process

Plan first, list the exact files, and stop for review before editing. Edit only owned paths.

## Goal

Optimise and sample QAOA circuits and return samples, convergence and the inputs for metrics. The answer comes from the circuit; no classical solution enters it.

## Owned paths / Do not touch

- Owned: `backend/qportfolio/quantum/` (except `noise.py`, which is U7), `backend/tests/test_qaoa.py`.
- Do not touch: `data/`, `api/`, `classical/`, `metrics.py`, `frontier.py`, `verdict.py`, `frontend/`.

## Files (exact)

- `backend/qportfolio/quantum/__init__.py`, `ansatz.py`, `optimizers.py`, `init_points.py`, `qaoa.py`
- `backend/tests/test_qaoa.py`

## Approach

1. `ansatz.build` returns a flattened `QAOAAnsatz` (decompose until no `QAOA`/`PauliEvolution` ops remain). Standard: |+> start, default mixer. XY: deterministic Dicke(n_assets, K) start (Bartschi-Eidenbenz), ring mixer of `XXPlusYYGate(2*beta, 0)` on asset qubits passed as the `mixer_operator` circuit, X mixer on slack qubits, no cardinality term in H (constant inside the subspace).
2. `optimizers.py`: `cobyla`, `nelder_mead` (scipy) and `spsa` (own seeded ~30-line implementation, deterministic). All share the callback `(iter, energy, params)` and return the history.
3. `init_points.py`: `random` (seeded uniform), `ramp` (TQA-style linear), `interp(prev_params)` (INTERP from depth p-1; the declared warm start; uses only QAOA's own parameters).
4. `qaoa.solve`: minimise <H> with `StatevectorEstimator`; call `on_progress(fraction, stage, {"iter","energy"})` per evaluation; honour `cancel` (raise `Cancelled` within one more evaluation); sample the final circuit with `StatevectorSampler(default_shots, seed)`; reverse Qiskit little-endian bitstrings so x0 is first and drop slack bits; evaluate unique selections with `Problem.evaluate`; answer = best feasible selection, otherwise `selection=None`, `bitstring=None`, `feasible=False`; always report `feasible_rate` and `details.most_probable`. Never repair infeasible samples.
5. Samples (`Sample` list), convergence and circuit stats (qubits, reps, depth, two-qubit gates, optimizer, init, seed) must reach the pipeline for `RunResult.qaoa`: carry them on the returned object. If a field is missing from `contracts.py`, update `contracts.py`, `CONTRACTS.md` and `contracts/api-examples/` together. Mark `Sample.optimal` when `landscape` is given. `approx_ratio` and `p_opt` come from TEAM-3's `qaoa_metrics` in the pipeline.

## Interfaces

- Provide (section 1.3): `qaoa_solve(problem, qubo, settings: QaoaSettings, on_progress=None, cancel=None, landscape=None) -> SolverResult`; `QaoaSettings` fields = RunRequest.qaoa (variant, reps, optimizer, init, shots, maxiter, noise, seed).
- Consume: section 1.1 `Problem.evaluate`; section 1.3 `build_qubo`, `ising.to_sparse_pauli` (U5); `Cancelled` from `pipeline.py` (section 1.5).
- Patterns: only those in `backend/scripts/smoke.py` (checks a and c) and `docs/research/08-env-spike.md`. No `qiskit_algorithms`, `qiskit_optimization`, V1 primitives, or raw `QAOAAnsatz` into Aer.

## Test scenarios

- [ ] 6-asset K=3, p=2 COBYLA, seed fixed: expected approximation ratio > 0.7 and the brute-force optimum is sampled at least once in 4096 shots.
- [ ] XY variant, noiseless: every sampled asset bitstring has Hamming weight K.
- [ ] Decoding: a bitstring ending in "01" (qubit 0 = 1) maps to asset 0 selected.
- [ ] No-repair (AE2): penalties forced to 0 so samples are mostly infeasible -> `selection=None`, `feasible=False`, `feasible_rate` reported, nothing repaired.
- [ ] Cancel flag set after 3 iterations -> `solve` stops within one more evaluation and raises `Cancelled`.
- [ ] `interp` from p=1 parameters gives 2 gamma and 2 beta values; its p=2 start energy is at or below the p=1 optimum.
- [ ] SPSA with a fixed seed is deterministic across two runs.

## Verify

```
cd backend; uv run pytest tests/test_qaoa.py -q; uv run pytest -q
```

A 10-asset p=3 run with 150 iterations finishes in under 20 s.

## Done checklist

- [ ] All scenarios above exist as pytest tests and pass; full suite green.
- [ ] The no-repair test stays green (honesty gate).
- [ ] AGENTS.md banned-API `git grep` prints nothing.
- [ ] Committed and pushed to `team-1/work`; 3-line summary printed (Wahab opens the PR and merges).

## When finished

1. Run the verify command above.
2. If it fails, fix it only inside your owned paths and run it again (up to 3 tries). If it still fails, stop and print the error.
3. When it passes: `git add -A`, then `git commit -m "team-1: U6 <short summary>"`.
4. Then `git push -u origin team-1/work`. Never force-push. Never push to `main`.
5. Print a 3-line summary: what was built, the test result, and any known gap.
6. If git reports a conflict or asks for a login, stop and say so. Do not resolve it; Wahab does.
