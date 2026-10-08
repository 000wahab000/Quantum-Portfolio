Paste this whole file into your agent (or @-mention it). Team 1, unit U7.

# TEAM-1 · U7 — Noise runner (fake backend)

Integrate phase (T0+2.5h to T0+4h). Depends on U6. You can run this while waiting for TEAM-2/3 merges before U10.

## Read first

- `AGENTS.md`
- `TEAMS/CONTRACTS.md`: section 1.3 (`noisy_solve`), section 2.6 (`qaoa.noise` block)
- `TEAMS/TEAM-1-claude-quantum-core/START-HERE.md`, `docs/research/08-env-spike.md` (Noise, gotchas 4 and 6)
- Plan `docs/plans/2026-10-08-2115-feat-quantum-portfolio-optimiser-plan.md`: KTD10, section "U7. Noise runner (fake backend)"

## Process

Plan first, list the exact files, and stop for review before editing. Edit only owned paths.

## Goal

Re-run a configuration under FakeGuadalupeV2 noise and report degradation against the ideal run.

## Owned paths / Do not touch

- Owned: `backend/qportfolio/quantum/noise.py`, `backend/tests/test_noise.py`.
- Do not touch: `data/`, `api/`, `classical/`, `metrics.py`, `frontier.py`, `verdict.py`, `frontend/`.

## Files (exact)

- `backend/qportfolio/quantum/noise.py`
- `backend/tests/test_noise.py`

## Approach

1. Build `NoiseModel.from_backend(FakeGuadalupeV2())` and `generate_preset_pass_manager(optimization_level=1, backend=fake)` once; cache them.
2. `sample_noisy(params)`: ideal parameters, noisy sampling with `qiskit_aer.primitives.SamplerV2(default_shots, seed, options={"backend_options": {"noise_model": nm}})` on the transpiled circuit.
3. `optimise_noisy`: `qiskit_aer.primitives.EstimatorV2(options={"backend_options": {"noise_model": nm}})`, `H.apply_layout(isa.layout)`, transpiled circuit.
4. Return the same metric set as the ideal run plus transpiled depth and two-qubit gate count (maps to `qaoa.noise` = `{backend, ideal, noisy, transpiled}`). Never pass a raw `QAOAAnsatz` to Aer.

## Interfaces

- Provide (section 1.3): `noisy_solve(problem, qubo, settings, params=None, on_progress=None, cancel=None) -> NoiseReport`.
- Consume: `qaoa_solve` and the ansatz builder from U6, `Problem.evaluate` (section 1.1).

## Test scenarios

- [ ] 6-asset instance: noisy feasible rate and P(opt) are each <= ideal + 0.05; the report contains both ideal and noisy.
- [ ] A noisy run on 16 variables completes and the transpiled circuit uses no more than 16 physical qubits.
- [ ] Depth > 0 and two-qubit gates > 0; XY shows more two-qubit gates than standard on the same instance.

## Verify

```
cd backend; uv run pytest tests/test_noise.py -q; uv run pytest -q
```

The noisy 10-asset run finishes in under 60 s.

## Done checklist

- [ ] All scenarios above exist as pytest tests and pass; full suite green.
- [ ] Cancel works during a noisy optimisation (flag checked per evaluation).
- [ ] Committed and pushed to `team-1/work`; 3-line summary printed (Wahab opens the PR and merges).

## When finished

1. Run the verify command above.
2. If it fails, fix it only inside your owned paths and run it again (up to 3 tries). If it still fails, stop and print the error.
3. When it passes: `git add -A`, then `git commit -m "team-1: U7 <short summary>"`.
4. Then `git push -u origin team-1/work`. Never force-push. Never push to `main`.
5. Print a 3-line summary: what was built, the test result, and any known gap.
6. If git reports a conflict or asks for a login, stop and say so. Do not resolve it; Wahab does.
