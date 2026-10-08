# Research: Reference repo Ayomide05/Quantum-Portfolio-Optimization

Source: https://github.com/Ayomide05/Quantum-Portfolio-Optimization. I read it through `gh api`. Nothing was cloned or executed.

## Verdict: use it as a cautionary example, not a template
- **No Qiskit, no QAOA, no circuits, no UI, no API.** The "quantum" solver is D-Wave `neal` simulated annealing, a classical method, with a hand-written classical annealer as fallback.
- **Synthetic data.** 50 anonymised assets from a hackathon workbook. Σ is synthetic (sector-block correlations times volatilities derived from market cap) and **not symmetric** (max asymmetry 0.025). There is no price history, no lookback window and no train/test split.
- **The headline "+71% Sharpe" is an artifact.**
  - It compares classical **equal-weight** metrics against quantum **SLSQP-optimised** metrics.
  - Like-for-like, the two are tied: classical optimised Sharpe 4.84 vs quantum 4.85.

## Bugs worth learning from
1. **Cardinality penalty is double-counted.**
   - The code writes `2P` into both `Q_ij` and `Q_ji`, which gives `4P` per pair. The energy minimum then lands at k=8 instead of the target 15.
   - Correct form for `P·(Σx − N)²` in `xᵀQx + cᵀx` with symmetric Q: `c += P(1 − 2N)`, `Q += P(J − I)`.
   - **Our test:** assert that `argmin` over k of the penalty-only energy equals K.
2. **Sector cap is not in the QUBO.** It is a weak soft term (5 per pair, against ~4000 for cardinality), and the hard cap is applied only in post-processing. The QUBO alone therefore does not encode the stated constraints.
3. **Post-processing "repair" does most of the work.** The raw solver output (~8 assets) is greedily filled up to 15. **Our rule:** report raw sampler output separately from any repaired output. Repair must be declared, and must be applied identically to every solver.
4. **Unseeded RNGs, and a temperature typo** (`temperatue`) that leaves the classical SA as a random walk.
5. **Ising conversion is off by a factor of 2.** `J = Q_ij/4` is wrong for the `xᵀQx` convention. **Our rule:** use Qiskit's own `QuadraticProgram.to_ising()` (or the converters) and verify by brute force that `E_ising(z) = E_qubo(x) + const`.
6. **Artifact hygiene.** One JSON file is truncated, the README names files that don't exist, `applymap` is gone in pandas 3, and `allow_pickle=True` is used for no reason.

## Ideas worth keeping
- **Turnover / transaction cost as a linear term.** With previous holdings `x_prev`, `|x − x_prev| = x(1 − 2·x_prev) + x_prev` for binaries. That makes the cost linear: `c_i += τ·tc_i·(1 − 2·x_prev_i)`. Make τ large enough to matter.
- **Seed with classical heuristics.** Maps to a *declared* warm-start QAOA (Egger et al. 2021: relaxed solution → biased initial state and mixer).
- **Drift monitor.** Mahalanobis distance `sqrt(dᵀ(Σ+εI)⁻¹d)` as a rebalance trigger. Optional nice-to-have.

## Scale note
At 50 assets, QAOA needs ~50 qubits, which is beyond statevector simulation. Our plan is a two-stage approach:
1. **Classical pre-screen.** Narrow 50 down to n_q ≤ ~16 candidates with a documented, solver-agnostic rule, applied identically to all baselines.
2. **QAOA on the reduced universe.**

Brute force is exact up to n ≈ 20 (C(20,10) = 184,756). Above that, use CVXPY + an open-source MIQP solver, or flag the reference as "best known".
