Paste this whole file into your agent (or @-mention it). Team 1, unit U5.

# TEAM-1 · U5 — QUBO builder, constraint registry, penalties, Ising

Build phase (T0 to T0+2.5h). Depends on U1.

## Read first

- `AGENTS.md`
- `docs/teams/CONTRACTS.md`: section 1.1 (`Problem`, `Evaluation`), section 1.3 (`build_qubo`, `Qubo`, `tune_penalties`)
- `docs/teams/TEAM-1.md`
- Plan `docs/plans/2026-10-08-2115-feat-quantum-portfolio-optimiser-plan.md`: KTD2, KTD3, KTD4, KTD5, section "U5. QUBO builder, constraint registry, penalties, Ising"
- `docs/research/02-reference-repo.md` (the penalty double-count bug to guard against)

## Process

Plan first, list the exact files, and stop for review before editing. Edit only owned paths. Test-first: the energy-equivalence tests must exist before QAOA consumes this.

## Goal

Build one faithful QUBO from a `Problem` using pluggable constraints, tuned penalties and an Ising form for QAOA.

## Owned paths / Do not touch

- Owned: `backend/qportfolio/qubo/`, `backend/tests/test_qubo.py`.
- Do not touch: `data/`, `api/`, `classical/`, `metrics.py`, `frontier.py`, `verdict.py`, `frontend/`, `docs/teams/CONTRACTS.md` (change it only together with `contracts.py` if a real gap appears).

## Files (exact)

- `backend/qportfolio/qubo/__init__.py` (exports `build_qubo`, `tune_penalties`, `Qubo`)
- `backend/qportfolio/qubo/constraints.py`, `builder.py`, `penalty.py`, `ising.py`
- `backend/tests/test_qubo.py`

## Approach

1. Registry maps a name to a term object. `equality` term gives a quadratic penalty (cardinality A*(sum x - K)^2; Q_ij + Q_ji must total 2A per pair). `inequality` term a.x <= b gives slack bits. `objective` term gives a linear or quadratic addition. A new constraint is a new registry entry; solvers are untouched.
2. Objective F(x) = q*x'Sigma x/K^2 - (1-q)*(mu'x/K - tc(x)), with tc(x) = cost_lin.x + cost_const as an objective term.
3. Slack bits: sector cap sum_{i in s} x_i <= cap uses ceil(log2(cap+1)) bits, only for sectors with more candidates than cap. Target return mu'x/K - tc(x) >= R uses a 3-bit discretised slack.
4. Variable labels: assets first, then slack. If total variables exceed 16, raise a clear error naming the count (KTD5).
5. `penalty.tune`: brute force over all 2^m states (m <= 16). Doubling schedule starting at 0.5x the objective spread. Pick the smallest weight such that the minimum infeasible energy >= (F_min + F_mean_feasible)/2 (Brandhofer Eq. 11). Feasibility is always re-checked exactly with `Problem.evaluate`.
6. `ising.to_sparse_pauli` maps x = (1 - Z)/2 and returns the `SparsePauliOp`, the constant offset and the normalisation scale (Hamiltonian normalised by max |coefficient|; keep the scale so energies can be reported unscaled). Document the return shape in the docstring.

## Interfaces

- Provide (section 1.3): `build_qubo(problem, penalties=None) -> Qubo(Q, c, const, n_assets, n_slack, labels, penalties)`, `Qubo.energy(bits)`, `Qubo.energies_all()`, `tune_penalties(problem) -> dict[str, float]`, `ising.to_sparse_pauli`.
- Consume (section 1.1): `Problem`, `Problem.evaluate`. TEAM-3's `annealing(problem, qubo, ...)` and U6 consume what you build.

## Test scenarios

- [ ] Penalty-only energy (mu = Sigma = 0): the argmin over all bitstrings has exactly K ones, for K in {2, 3, 5}.
- [ ] Random 6-asset problem: E_ising(z) + offset == E_qubo(x) for all 64 bitstrings, within 1e-9.
- [ ] For every feasible selection with optimal slack, the QUBO energy equals the `Problem.evaluate` objective, within 1e-9.
- [ ] Tuned penalty makes every infeasible state >= (F_min + F_mean)/2.
- [ ] Registering a dummy entry (for example "exclude ticker X") builds successfully with no solver change.
- [ ] A sector cap only produces slack bits for sectors with more candidates than the cap.
- [ ] More than 16 total variables raises a clear error naming the count.

## Verify

```
cd backend; uv run pytest tests/test_qubo.py -q; uv run pytest -q
```

Building a 12-asset QUBO with caps and a target return takes under 1 s including tuning.

## Done checklist

- [ ] All scenarios above exist as pytest tests and pass; full suite green.
- [ ] No banned APIs (AGENTS.md `git grep`).
- [ ] Branch `team-1/qubo`, committed, PR to `main`; summary posted (files, test output, known gaps).
