# TEAM-1 — Quantum core and integrator

Tool: Claude Code (`claude --permission-mode plan`). Coding subagents on Sonnet, research subagents on Haiku.

## Mission

Build the genuine quantum part and glue everything together. Deliver one QUBO from a pluggable constraint registry with tuned penalties (R5-R7), our own QAOA loop with standard and XY mixers whose best feasible sampled bitstring is the answer (R10-R12, R15 inputs), the fake-backend noise re-run (R13), the pipeline that returns a contract-valid `RunResult` (integration of R1-R20), and the precomputed evidence studies (R12, R13, R21). You also own the frozen contracts and merge every team's branch.

## Your units

| U-ID | Title | When | Depends on |
|---|---|---|---|
| U1 | Scaffold + frozen contracts + example payloads | Prework | — |
| U2 | Shared agent rules + team briefs (this documentation; done) | Prework | U1 spec |
| U5 | QUBO builder, constraint registry, penalties, Ising | Build (T0 to T0+2.5h) | U1 |
| U6 | QAOA engine (standard + XY), optimisers, init points | Build | U5 |
| U7 | Noise runner (fake backend) | Integrate (T0+2.5h to T0+4h) | U6 |
| U10 | Pipeline orchestrator | Integrate | U3-U9 |
| U14 | Evidence studies script + checked-in results | Evidence + demo (T0+4h to T0+5h) | U6, U7, U8, U9 |
| U15 | Integration, offline demo hardening, README (you lead) | Evidence + demo | U10-U14 |

## Owned paths

- `backend/qportfolio/{contracts.py,problem.py,pipeline.py,__init__.py}`
- `backend/qportfolio/qubo/` (`constraints.py`, `builder.py`, `penalty.py`, `ising.py`)
- `backend/qportfolio/quantum/` (`ansatz.py`, `optimizers.py`, `init_points.py`, `qaoa.py`, `noise.py`)
- `backend/scripts/{smoke.py,run_studies.py}`, `backend/data/studies/`
- `backend/tests/{test_contracts,test_problem,test_qubo,test_qaoa,test_noise,test_pipeline}.py`
- `contracts/`, `backend/pyproject.toml`, `backend/uv.lock`, `backend/.python-version`, `.gitignore`, `README.md`, `AGENTS.md`, `CLAUDE.md`, `docs/`

## Do not touch

- `backend/qportfolio/{data,api}/`, `backend/scripts/fetch_snapshot.py`, `backend/data/{nifty50.csv,snapshot/}` (TEAM-2).
- `backend/qportfolio/classical/`, `backend/qportfolio/{metrics,frontier,verdict}.py` (TEAM-3).
- `frontend/` (TEAM-4).
- Integration fix in another team's area: hand the owner the exact fix (their `99-integration-fix.md`). Patch it yourself only if the owner is unavailable, in a separate commit titled `fix(team-N): ...`, and tell them in chat.

## Interfaces you provide

- CONTRACTS.md §1.1: `Problem`, `Evaluation`, `Problem.evaluate` in `backend/qportfolio/problem.py` (ready at T0; TEAM-3 builds on it).
- `backend/qportfolio/contracts.py` (pydantic models mirroring §2 one-to-one) and `contracts/api-examples/*.json` (TEAM-4 mocks, TEAM-2 test fixtures).
- §1.3: `build_qubo`, `Qubo.energy`, `Qubo.energies_all`, `tune_penalties`, `qaoa_solve`, `noisy_solve`.
- §1.5: `pipeline.run(request, on_progress, cancel) -> RunResult` (stub returns the example until U10), and `Cancelled`.
- §2.7: `backend/data/studies/{depth,optimizer,init,mixer,noise}.json` (TEAM-2 serves them at `/api/studies`).
- `docs/teams/CONTRACTS.md` itself. Only you change it.

## Interfaces you consume

- §1.2 (TEAM-2, used in U10 and U14): `build_market`, `Market.subset`, `prescreen`, `linear_costs`, `to_shares`, `out_of_sample`, plus `benchmark_oos(market)` for `benchmarks.nifty50`.
- §1.4 (TEAM-3, used in U10 and U14): `brute_force` (returns `Landscape`), `relaxation`, `annealing`, `qaoa_metrics`, `frontier`, `verdict`.
- Until TEAM-2/3 merge: test your units on hand-built `Problem` instances (no `data/` dependency). U10 starts only when U3, U4, U8, U9 are merged to `main`.

## Setup (do once)

```
cd "D:\wahab stuff\wahab code\Quantum-Portfolio"
claude --worktree team-1 --permission-mode plan     # or: claude --permission-mode plan, then git checkout -b team-1/<topic>
$env:PYTHONUTF8="1"
cd backend; uv python pin 3.13; uv sync             # first sync ~10 min
uv run pytest -q; uv run python scripts/smoke.py    # both must pass before you start
```

- Inside Claude: plan mode (Shift+Tab) before edits; `/ponytail` for coding, `/caveman` for terse output.
- Drive each unit with `/compound-engineering:ce-work` on the plan unit (for example "execute U5 of docs/plans/2026-10-08-2115-feat-quantum-portfolio-optimiser-plan.md"). Dispatch coding subagents with model sonnet and research subagents with model haiku.

## Prompts (run in order)

Claude Code: type `@docs/teams/prompts/TEAM-1/02-U5-qubo.md` (or any file below) and send. Antigravity users type `@` and pick the file. Each file is self-contained.

| Prompt file | Unit | When to run |
|---|---|---|
| [01-U1-scaffold-contracts.md](prompts/TEAM-1/01-U1-scaffold-contracts.md) | U1 | Prework, only if not already on `main` |
| [02-U5-qubo.md](prompts/TEAM-1/02-U5-qubo.md) | U5 | T0 (first unit) |
| [03-U6-qaoa.md](prompts/TEAM-1/03-U6-qaoa.md) | U6 | After U5 |
| [04-U7-noise.md](prompts/TEAM-1/04-U7-noise.md) | U7 | After U6, T0+2.5h |
| [05-U10-pipeline.md](prompts/TEAM-1/05-U10-pipeline.md) | U10 | After U3, U4, U8, U9 are merged |
| [06-U14-studies.md](prompts/TEAM-1/06-U14-studies.md) | U14 | After U7 and U10; start the long run early |
| [07-U15-integration.md](prompts/TEAM-1/07-U15-integration.md) | U15 | T0+4h |
| [99-integration-fix.md](prompts/TEAM-1/99-integration-fix.md) | any | When an integration failure appears |

## How to verify

```
cd backend; uv run pytest -q                           # all tests
uv run pytest tests/test_qubo.py tests/test_qaoa.py tests/test_noise.py tests/test_pipeline.py -q
uv run python scripts/smoke.py
cd ..; git grep -nE "qiskit\.algorithms|qiskit_algorithms|qiskit_finance|qiskit_optimization|import Aer|QuantumInstance|BackendSampler|BackendEstimator|applymap|execute\(" -- backend
```

- U5: 12-asset QUBO with caps and a target return builds in under 1 s including tuning.
- U6: 10-asset p=3, 150 iterations, in under 20 s. U7: noisy 10-asset run in under 60 s. U10: default request in under 60 s.
- Manual: with the API up, `POST /api/runs` with `contracts/api-examples/run_request.json` and poll until `done`; the result matches `job_done.json` in shape.

## Definition of done

- [ ] U5, U6, U7, U10, U14 tests exist for every scenario in their prompt files and pass; `uv run pytest -q` is green on `main`.
- [ ] Honesty gates green: penalty argmin (U5), no look-ahead (U3), no-repair (U6), banned-phrase verdict (U9).
- [ ] `contracts.py` parses every file in `contracts/api-examples/` (`test_contracts.py`); CONTRACTS.md, `contracts.py` and the examples agree.
- [ ] `backend/data/studies/{depth,optimizer,init,mixer,noise}.json` committed and rendered on the Evidence page.
- [ ] Offline demo runs twice with Wi-Fi off; phone check done; README lets a judge run the demo.
- [ ] No banned APIs (git grep clean), no abandoned experiment code or stray files in the diff.
- [ ] Every team branch merged, each handoff note posted.

## Handoff

- Branch `team-1/<topic>`, PR to `main`. You are the merger: self-merge only after `uv run pytest -q` passes.
- Post in team chat: units done, test result line, contract changes (if any), known gaps.

## Integrator duties

- Merge order: U1 first, then each TEAM branch as soon as its tests pass (TEAM-3 and TEAM-2 early, TEAM-4 when `npm run build` passes). Ask owners to rebase on `main` after each merge.
- After every merge, run the full Verification Contract (backend tests, smoke, `/api/health`, `npm run build`). Revert the merge if it breaks `main`.
- Own contract changes: edit CONTRACTS.md, `contracts.py` and `contracts/api-examples/` in one commit and announce it. Record two small additions agreed in the briefs: `benchmark_oos(market, rf=RF)` in §1.2, and that `RunRequest.holdings` (share counts) is converted to weights by the pipeline before `linear_costs`.
- Known fix: the example verdict text in CONTRACTS.md §2.6 says "no speed advantage is claimed", which contains the banned word "advantage" (U9 banned-phrase test). Reword it there and in `contracts/api-examples/job_done.json` (for example "no speed benefit is claimed at this size").
- Run U15: demo rehearsal offline, phone check, README.
- You can run `/compound-engineering:ce-work` on the plan unit by unit with Sonnet subagents; keep research on Haiku.
- Cut order if late (plan Risks): U14 study breadth, then XY in the live UI, then the noise toggle in the live UI.

## Pitfalls

- Flatten the ansatz before `StatevectorEstimator` (about 10 ms vs 270 ms per eval); never pass a raw `QAOAAnsatz` to Aer.
- Noisy estimator needs the transpiled circuit and `H.apply_layout(isa.layout)`; otherwise the observable acts on the wrong qubits.
- Bitstring reversal: Qiskit counts are little-endian. Reverse once, in `quantum/`, then drop slack bits. Test it with a known string.
- Penalty double-count: `Q_ij + Q_ji` must total 2A per pair. Keep the penalty-only argmin test (K in {2, 3, 5}) green.
- XY variant: no cardinality term in H (constant inside the Dicke subspace); slack qubits get an X mixer. Expect about 4x the CX count of standard; report degradation, do not hide it.
- Hamiltonian is normalised by max |coefficient|; keep the scale and report unscaled energies.
- `interp` uses only QAOA's own depth p-1 optimum. No classical solution ever enters the circuit or the initial point.
- Set `PYTHONUTF8=1`; seed everything (SPSA, random init, samplers) so tests are deterministic.
