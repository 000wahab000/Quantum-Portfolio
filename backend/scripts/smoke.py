"""Environment smoke test for the Qiskit QAOA portfolio optimiser stack.

Run:  uv run python smoke.py
Each check prints PASS/FAIL + wall time.  Checks share a few module-level
artefacts (optimised QAOA parameters) so they stay independent-ish but fast.
"""
from __future__ import annotations

import sys
import time
import traceback
from collections import Counter
from itertools import combinations
from pathlib import Path

import numpy as np

# WINDOWS GOTCHA: when stdout is piped/redirected Python uses cp1252, and QAOAAnsatz parameter names
# are 'β[0]', 'γ[0]' -> UnicodeEncodeError on print.  Force UTF-8 (or set PYTHONUTF8=1).
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

RESULTS: list[tuple[str, bool, float, str]] = []
SHARED: dict = {}


def check(name: str):
    """Decorator: run fn immediately, record PASS/FAIL + timing, never raise."""

    def deco(fn):
        t0 = time.perf_counter()
        try:
            note = fn() or ""
            ok = True
        except Exception:  # noqa: BLE001
            note = traceback.format_exc()
            ok = False
        dt = time.perf_counter() - t0
        RESULTS.append((name, ok, dt, note))
        print(f"[{'PASS' if ok else 'FAIL'}] {name}  ({dt:.2f}s)")
        if note:
            print("      " + str(note).strip().replace("\n", "\n      "))
        sys.stdout.flush()
        return fn

    return deco


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def make_ising(n: int, seed: int = 1):
    """Random Ising Hamiltonian: ZZ couplings (dense-ish) + Z fields."""
    from qiskit.quantum_info import SparsePauliOp

    rng = np.random.default_rng(seed)
    terms = []
    for i, j in combinations(range(n), 2):
        if rng.random() < 0.7:
            terms.append(("ZZ", [i, j], float(rng.normal())))
    for i in range(n):
        terms.append(("Z", [i], float(rng.normal())))
    return SparsePauliOp.from_sparse_list(terms, num_qubits=n)


def exact_min(H) -> tuple[float, str]:
    """Brute-force ground energy + bitstring (qiskit little-endian string)."""
    n = H.num_qubits
    diag = np.real(np.diag(H.to_matrix()))
    idx = int(np.argmin(diag))
    return float(diag[idx]), format(idx, f"0{n}b")


def top_counts(counts: dict[str, int], k: int = 5):
    return sorted(counts.items(), key=lambda kv: -kv[1])[:k]


def dicke_circuit(n: int, k: int):
    """Deterministic Dicke state |D^n_k> (Baertschi & Eidenbenz 2019), O(nk) gates."""
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import RYGate

    def gate_i(qc, m):
        qc.cx(m - 2, m - 1)
        qc.cry(2 * np.arccos(np.sqrt(1 / m)), m - 1, m - 2)
        qc.cx(m - 2, m - 1)

    def gate_ii(qc, m, l):
        qc.cx(m - l - 1, m - 1)
        theta = 2 * np.arccos(np.sqrt(l / m))
        qc.append(RYGate(theta).control(2), [m - 1, m - l, m - l - 1])
        qc.cx(m - l - 1, m - 1)

    def scs(qc, m, kk):
        gate_i(qc, m)
        for l in range(2, kk + 1):
            gate_ii(qc, m, l)

    qc = QuantumCircuit(n, name=f"Dicke({n},{k})")
    qc.x(range(n - k, n))
    for m in range(n, k, -1):
        scs(qc, m, k)
    for m in range(k, 1, -1):
        scs(qc, m, m - 1)
    return qc


def dicke_statevector(n: int, k: int):
    from qiskit.quantum_info import Statevector

    amp = np.zeros(2**n, dtype=complex)
    for idx in range(2**n):
        if bin(idx).count("1") == k:
            amp[idx] = 1.0
    amp /= np.linalg.norm(amp)
    return Statevector(amp)


def flatten(circ):
    """Decompose until no composite QAOA / PauliEvolution blocks remain.

    PERF + COMPAT: StatevectorEstimator on the raw QAOAAnsatz (PauliEvolutionGate) is ~25x slower
    (scipy sparse expm per call) and Aer primitives reject it ('unknown instruction: QAOA').
    """
    for _ in range(6):
        names = set(circ.count_ops())
        if not names & {"QAOA", "PauliEvolution"}:
            break
        circ = circ.decompose()
    return circ


# --------------------------------------------------------------------------
# (a) noiseless QAOA with V2 primitives
# --------------------------------------------------------------------------
@check("a. noiseless QAOA: QAOAAnsatz + StatevectorEstimator/COBYLA + StatevectorSampler")
def check_a():
    from qiskit.circuit.library import QAOAAnsatz
    from qiskit.primitives import StatevectorEstimator, StatevectorSampler
    from scipy.optimize import minimize

    n, reps = 6, 2
    H = make_ising(n)
    ansatz = QAOAAnsatz(cost_operator=H, reps=reps)
    est = StatevectorEstimator()
    hist: list[float] = []
    flat = flatten(ansatz)  # ~10 ms/eval instead of ~270 ms/eval for the raw ansatz
    t0 = time.perf_counter(); est.run([(ansatz, H, np.zeros(ansatz.num_parameters))]).result(); t_raw = time.perf_counter() - t0
    t0 = time.perf_counter(); est.run([(flat, H, np.zeros(ansatz.num_parameters))]).result(); t_flat = time.perf_counter() - t0

    def cost(x):
        pub = (flat, H, x)
        val = float(est.run([pub]).result()[0].data.evs)
        hist.append(val)
        return val

    rng = np.random.default_rng(0)
    x0 = rng.uniform(0, np.pi, ansatz.num_parameters)
    res = minimize(cost, x0, method="COBYLA", options={"maxiter": 60})
    e_exact, b_exact = exact_min(H)

    meas = ansatz.copy()
    meas.measure_all()  # adds classical register named "meas"
    bound = meas.assign_parameters(res.x)
    sampler = StatevectorSampler(default_shots=2048, seed=7)
    result = sampler.run([bound]).result()
    pub_res = result[0]
    reg_names = list(pub_res.data.keys())  # -> ['meas']
    counts = pub_res.data.meas.get_counts()
    assert sum(counts.values()) == 2048
    SHARED["a_x"] = res.x
    SHARED["a_H"] = H
    SHARED["a_ansatz"] = ansatz
    top = top_counts(counts)
    return (
        f"1 estimator eval: raw QAOAAnsatz {1000*t_raw:.0f} ms vs flatten(ansatz) {1000*t_flat:.0f} ms; flat ops={dict(flat.count_ops())}\n"
        f"num_parameters={ansatz.num_parameters}  params={[p.name for p in ansatz.parameters]}\n"
        f"COBYLA nfev={res.nfev}  E_start={hist[0]:.4f}  E_opt={res.fun:.4f}  E_exact_min={e_exact:.4f} ({b_exact})\n"
        f"classical registers on data bin: {reg_names}\n"
        f"top-5 bitstrings: {top}"
    )


# --------------------------------------------------------------------------
# (b) noisy Aer with a fake backend noise model
# --------------------------------------------------------------------------
@check("b. noisy Aer: NoiseModel.from_backend(fake) + transpile + SamplerV2/EstimatorV2")
def check_b():
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import NoiseModel
    from qiskit_aer.primitives import EstimatorV2 as AerEstimatorV2
    from qiskit_aer.primitives import SamplerV2 as AerSamplerV2
    import qiskit_ibm_runtime.fake_provider as fp

    H = SHARED.get("a_H") or make_ising(6)
    ansatz = SHARED.get("a_ansatz")
    if ansatz is None:
        from qiskit.circuit.library import QAOAAnsatz

        ansatz = QAOAAnsatz(cost_operator=H, reps=2)
    x = SHARED.get("a_x", np.full(ansatz.num_parameters, 0.3))

    notes = []
    fake = None
    for name in ("FakeGuadalupeV2", "FakeSherbrooke"):
        t0 = time.perf_counter()
        try:
            fake = getattr(fp, name)()
            notes.append(f"fake backend {name}: OK, {fake.num_qubits}q, built in {time.perf_counter()-t0:.2f}s")
            break
        except Exception as e:  # noqa: BLE001
            notes.append(f"fake backend {name}: FAILED {type(e).__name__}: {e}")
    assert fake is not None, "\n".join(notes)

    t0 = time.perf_counter()
    nm = NoiseModel.from_backend(fake)
    notes.append(f"NoiseModel.from_backend: {time.perf_counter()-t0:.2f}s, basis_gates={nm.basis_gates}")

    # --- AerSimulator.from_backend
    t0 = time.perf_counter()
    sim_fb = AerSimulator.from_backend(fake)
    notes.append(f"AerSimulator.from_backend(fake): OK ({time.perf_counter()-t0:.2f}s) num_qubits={sim_fb.num_qubits}")
    # --- explicit noise model on an Aer backend
    sim_nm = AerSimulator(noise_model=nm)

    meas = ansatz.copy()
    meas.measure_all()
    bound_logical = meas.assign_parameters(x)

    for opt in (1, 3):
        t0 = time.perf_counter()
        pm = generate_preset_pass_manager(optimization_level=opt, backend=fake)
        isa = pm.run(bound_logical)
        t_tr = time.perf_counter() - t0
        ops = isa.count_ops()
        notes.append(
            f"opt={opt}: transpile {t_tr:.2f}s depth={isa.depth()} 2q={sum(v for k,v in ops.items() if k in ('cz','ecr','cx'))} "
            f"ops={dict(ops)} layout_physical={isa.layout.final_index_layout() if isa.layout else None}"
        )
        t0 = time.perf_counter()
        counts = sim_fb.run(isa, shots=2048).result().get_counts()
        notes.append(f"  AerSimulator.from_backend.run: {time.perf_counter()-t0:.2f}s top5={top_counts(counts)}")
        t0 = time.perf_counter()
        counts2 = sim_nm.run(isa, shots=2048).result().get_counts()
        notes.append(f"  AerSimulator(noise_model=nm).run: {time.perf_counter()-t0:.2f}s top5={top_counts(counts2)}")

    # --- Aer SamplerV2 with noise via options (use the opt=3 isa circuit)
    t0 = time.perf_counter()
    aer_sampler = AerSamplerV2(
        default_shots=2048,
        seed=7,
        options={"backend_options": {"noise_model": nm}},
    )
    sres = aer_sampler.run([isa]).result()
    scounts = sres[0].data.meas.get_counts()
    notes.append(
        f"qiskit_aer.primitives.SamplerV2(default_shots=2048, seed=7, options={{'backend_options': {{'noise_model': nm}}}}): "
        f"OK {time.perf_counter()-t0:.2f}s total={sum(scounts.values())} top5={top_counts(scounts)}"
    )

    # --- noisy expectation: EstimatorV2 with noise model; H must be mapped to physical layout
    pm = generate_preset_pass_manager(optimization_level=1, backend=fake)
    isa_noMeas = pm.run(ansatz)  # no measurements for the estimator
    H_isa = H.apply_layout(isa_noMeas.layout)
    t0 = time.perf_counter()
    aer_est = AerEstimatorV2(options={"backend_options": {"noise_model": nm}})
    e_noisy = float(aer_est.run([(isa_noMeas, H_isa, x)]).result()[0].data.evs)
    from qiskit.primitives import StatevectorEstimator

    e_ideal = float(StatevectorEstimator().run([(ansatz, H, x)]).result()[0].data.evs)
    notes.append(
        f"qiskit_aer.primitives.EstimatorV2(options={{'backend_options': {{'noise_model': nm}}}}) + H.apply_layout(isa.layout): "
        f"E_noisy={e_noisy:.4f} vs E_ideal={e_ideal:.4f} ({time.perf_counter()-t0:.2f}s)"
    )

    # --- from_backend shortcuts (noise taken from the fake backend automatically)
    t0 = time.perf_counter()
    s2 = AerSamplerV2.from_backend(fake, default_shots=2048, seed=7).run([isa]).result()[0].data.meas.get_counts()
    notes.append(f"AerSamplerV2.from_backend(fake, default_shots=2048, seed=7): OK {time.perf_counter()-t0:.2f}s top3={top_counts(s2, 3)}")
    t0 = time.perf_counter()
    e2 = float(AerEstimatorV2.from_backend(fake).run([(isa_noMeas, H_isa, x)]).result()[0].data.evs)
    notes.append(f"AerEstimatorV2.from_backend(fake): E={e2:.4f} {time.perf_counter()-t0:.2f}s")
    # --- shot-noise estimator option
    e3 = float(
        AerEstimatorV2(options={"default_precision": 0.02, "backend_options": {"noise_model": nm}})
        .run([(isa_noMeas, H_isa, x)]).result()[0].data.evs
    )
    notes.append(f"AerEstimatorV2(options default_precision=0.02, noise_model): E={e3:.4f}")
    # --- expected failure: un-transpiled QAOAAnsatz into an Aer primitive
    try:
        AerEstimatorV2().run([(ansatz, H, x)]).result()
        notes.append("raw QAOAAnsatz in AerEstimatorV2: unexpectedly worked")
    except Exception as e:  # noqa: BLE001
        notes.append(f"raw QAOAAnsatz in AerEstimatorV2 -> {type(e).__name__}: {e}  (so always transpile/decompose first)")

    # --- fake backend direct .run (V2 fake backends delegate to Aer when installed)
    t0 = time.perf_counter()
    try:
        c3 = fake.run(isa, shots=512).result().get_counts()
        notes.append(f"fake.run(isa, shots=512): OK {time.perf_counter()-t0:.2f}s top3={top_counts(c3, 3)}")
    except Exception as e:  # noqa: BLE001
        notes.append(f"fake.run FAILED {type(e).__name__}: {e}")

    # --- runtime SamplerV2 / EstimatorV2 in local-testing mode (mode=fake backend)
    try:
        from qiskit_ibm_runtime import EstimatorV2 as RtEstimator
        from qiskit_ibm_runtime import SamplerV2 as RtSampler

        t0 = time.perf_counter()
        rt_s = RtSampler(mode=fake)
        rc = rt_s.run([isa], shots=1024).result()[0].data.meas.get_counts()
        notes.append(f"qiskit_ibm_runtime.SamplerV2(mode=fake) local mode: OK {time.perf_counter()-t0:.2f}s top3={top_counts(rc, 3)}")
        t0 = time.perf_counter()
        rt_e = RtEstimator(mode=fake)
        ev = float(rt_e.run([(isa_noMeas, H_isa, x)]).result()[0].data.evs)
        notes.append(f"qiskit_ibm_runtime.EstimatorV2(mode=fake) local mode: E={ev:.4f} {time.perf_counter()-t0:.2f}s")
    except Exception as e:  # noqa: BLE001
        notes.append(f"runtime local mode FAILED {type(e).__name__}: {e}")
    try:
        from qiskit_ibm_runtime.executor_sampler import Sampler as ExSampler

        t0 = time.perf_counter()
        rc = ExSampler(mode=fake).run([isa], shots=1024).result()[0].data.meas.get_counts()
        notes.append(f"qiskit_ibm_runtime.executor_sampler.Sampler(mode=fake): OK {time.perf_counter()-t0:.2f}s top3={top_counts(rc, 3)}")
    except Exception as e:  # noqa: BLE001
        notes.append(f"executor_sampler.Sampler(mode=fake) FAILED {type(e).__name__}: {str(e)[:300]}")

    return "\n".join(notes)


# --------------------------------------------------------------------------
# (c) XY-mixer QAOA with Dicke initial state (cardinality-constrained)
# --------------------------------------------------------------------------
@check("c. XY-mixer QAOA + Dicke init (n=6,k=3): all samples have Hamming weight k")
def check_c():
    from qiskit import QuantumCircuit
    from qiskit.circuit import Parameter
    from qiskit.circuit.library import QAOAAnsatz, StatePreparation, XXPlusYYGate
    from qiskit.primitives import StatevectorEstimator, StatevectorSampler
    from qiskit.quantum_info import Statevector, SparsePauliOp, state_fidelity
    from scipy.optimize import minimize

    n, k, reps = 6, 3, 2
    H = make_ising(n, seed=3)
    notes = []

    # --- Dicke prep option 1: deterministic O(nk) circuit
    dk = dicke_circuit(n, k)
    fid = state_fidelity(Statevector(dk), dicke_statevector(n, k))
    notes.append(f"deterministic Dicke circuit: fidelity vs ideal = {fid:.12f}, size={dk.size()}, depth={dk.depth()}")
    assert fid > 1 - 1e-9, "deterministic Dicke circuit incorrect"

    # --- Dicke prep option 2: StatePreparation of the uniform weight-k superposition
    sp = QuantumCircuit(n, name="DickeSP")
    sp.append(StatePreparation(dicke_statevector(n, k).data), range(n))
    fid2 = state_fidelity(Statevector(sp), dicke_statevector(n, k))
    notes.append(f"StatePreparation Dicke: fidelity = {fid2:.12f}")

    # --- Mixer variant 1: parameterised QuantumCircuit of XXPlusYYGate on a ring.
    # Ring pairs ordered (even layer)(odd layer)(closing pair); pairs inside a layer commute.
    beta = Parameter("beta_xy")
    pairs = [(0, 1), (2, 3), (4, 5), (1, 2), (3, 4), (5, 0)]
    mix = QuantumCircuit(n, name="XYring")
    for (i, j) in pairs:
        mix.append(XXPlusYYGate(2 * beta, 0.0), [i, j])

    ans_circ = QAOAAnsatz(cost_operator=H, reps=reps, initial_state=dk, mixer_operator=mix)
    notes.append(
        f"QAOAAnsatz(mixer_operator=QuantumCircuit): num_parameters={ans_circ.num_parameters} "
        f"{[p.name for p in ans_circ.parameters]}"
    )

    # --- Mixer variant 2: operator (sum of (XX+YY)/2) -> PauliEvolutionGate (Lie-Trotter)
    terms = []
    for (i, j) in pairs:
        terms.append(("XX", [i, j], 0.5))
        terms.append(("YY", [i, j], 0.5))
    Hm = SparsePauliOp.from_sparse_list(terms, num_qubits=n)
    ans_op = QAOAAnsatz(cost_operator=H, reps=reps, initial_state=dk, mixer_operator=Hm)
    notes.append(
        f"QAOAAnsatz(mixer_operator=SparsePauliOp): num_parameters={ans_op.num_parameters} "
        f"{[p.name for p in ans_op.parameters]}"
    )

    est = StatevectorEstimator()
    for label, ans in (("circuit-mixer", ans_circ), ("operator-mixer", ans_op)):
        flat = flatten(ans)
        notes.append(f"{label}: flattened ops={dict(flat.count_ops())}")

        def cost(x, flat=flat):
            return float(est.run([(flat, H, x)]).result()[0].data.evs)

        x0 = np.random.default_rng(1).uniform(0, np.pi, ans.num_parameters)
        res = minimize(cost, x0, method="COBYLA", options={"maxiter": 60})
        meas = ans.copy()
        meas.measure_all()
        counts = (
            StatevectorSampler(default_shots=4096, seed=7).run([meas.assign_parameters(res.x)]).result()[0].data.meas.get_counts()
        )
        weights = Counter()
        for bs, c in counts.items():
            weights[bs.count("1")] += c
        assert set(weights) == {k}, f"{label}: Hamming weights seen {dict(weights)}"
        # exact feasible optimum
        diag = np.real(np.diag(H.to_matrix()))
        feas = [(diag[i], format(i, f"0{n}b")) for i in range(2**n) if bin(i).count("1") == k]
        e_feas = min(feas)[0]
        notes.append(
            f"{label}: COBYLA nfev={res.nfev} E_opt={res.fun:.4f} (exact feasible min {e_feas:.4f}); "
            f"weights={dict(weights)}; top5={top_counts(counts)}"
        )
        SHARED[f"c_{label}"] = (ans, res.x)

    # transpile-ability of the XY ansatz (PauliEvolutionGate + XXPlusYYGate + Dicke) for a fake backend
    try:
        from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
        import qiskit_ibm_runtime.fake_provider as fp

        fake = fp.FakeGuadalupeV2()
        for label in ("circuit-mixer", "operator-mixer"):
            ans, x = SHARED[f"c_{label}"]
            m = ans.copy()
            m.measure_all()
            isa = generate_preset_pass_manager(optimization_level=1, backend=fake).run(m.assign_parameters(x))
            notes.append(f"{label}: transpiled to Guadalupe: depth={isa.depth()} ops={dict(isa.count_ops())}")
    except Exception as e:  # noqa: BLE001
        notes.append(f"transpile of XY ansatz FAILED {type(e).__name__}: {e}")
    return "\n".join(notes)


# --------------------------------------------------------------------------
# (d) cvxpy
# --------------------------------------------------------------------------
@check("d. cvxpy: min q x'Sx - mu'x  s.t. sum(x)=3, 0<=x<=1 (n=8)")
def check_d():
    import cvxpy as cp

    n, q = 8, 0.5
    rng = np.random.default_rng(0)
    A = rng.normal(size=(n, n))
    Sigma = A @ A.T / n + 1e-3 * np.eye(n)
    mu = rng.normal(0.1, 0.05, n)
    x = cp.Variable(n)
    prob = cp.Problem(
        cp.Minimize(q * cp.quad_form(x, cp.psd_wrap(Sigma)) - mu @ x),
        [cp.sum(x) == 3, x >= 0, x <= 1],
    )
    prob.solve()
    return (
        f"cvxpy {cp.__version__}; status={prob.status}; solver_stats.solver_name={prob.solver_stats.solver_name}; "
        f"obj={prob.value:.5f}; x={np.round(x.value, 3).tolist()}; sum={x.value.sum():.4f}\n"
        f"installed_solvers={cp.installed_solvers()}"
    )


# --------------------------------------------------------------------------
# (e) yfinance
# --------------------------------------------------------------------------
@check("e. yfinance: download 4 NSE tickers, inspect columns, parquet round-trip")
def check_e():
    import pandas as pd
    import yfinance as yf

    tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]
    df = yf.download(tickers, start="2023-01-01", end="2025-12-31", auto_adjust=True, progress=False)
    notes = [
        f"yfinance {yf.__version__}",
        f"shape={df.shape}",
        f"columns type={type(df.columns).__name__} nlevels={df.columns.nlevels} level0={list(df.columns.get_level_values(0).unique())} "
        f"level1={list(df.columns.get_level_values(1).unique())}",
        f"index: {df.index.min()} -> {df.index.max()} tz={df.index.tz} dtype={df.index.dtype}",
        f"NaN count total={int(df.isna().sum().sum())}",
    ]
    assert not df.empty, "empty frame returned (rate limit / network?)\n" + "\n".join(notes)
    close = df["Close"]  # DataFrame: columns = tickers
    notes.append(f"df['Close'] shape={close.shape} cols={list(close.columns)} NaN={int(close.isna().sum().sum())}")
    rets = np.log(close).diff().dropna()
    notes.append(f"log-returns shape={rets.shape}; annualised mu={ (rets.mean()*252).round(3).to_dict() }")
    p = Path("prices.parquet")
    close.to_parquet(p)
    back = pd.read_parquet(p)
    assert back.shape == close.shape and np.allclose(back.values, close.values, equal_nan=True)
    notes.append(f"parquet round-trip OK: {p} ({p.stat().st_size} bytes), index dtype after read={back.index.dtype}")
    # raw MultiIndex frame also round-trips?
    try:
        df.to_parquet("prices_multiindex.parquet")
        back2 = pd.read_parquet("prices_multiindex.parquet")
        notes.append(f"MultiIndex-columns parquet round-trip: OK, columns type={type(back2.columns).__name__}")
    except Exception as e:  # noqa: BLE001
        notes.append(f"MultiIndex-columns parquet round-trip FAILED: {type(e).__name__}: {e}")
    return "\n".join(notes)


# --------------------------------------------------------------------------
# (f) FastAPI / uvicorn
# --------------------------------------------------------------------------
@check("f. fastapi + uvicorn import, TestClient request")
def check_f():
    import fastapi
    import uvicorn
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    app = FastAPI()

    @app.get("/ping")
    def ping():
        return {"ok": True}

    r = TestClient(app).get("/ping")
    assert r.status_code == 200 and r.json() == {"ok": True}
    return f"fastapi {fastapi.__version__}; uvicorn {uvicorn.__version__}; TestClient GET /ping -> {r.json()}"


# --------------------------------------------------------------------------
print("\n=== SUMMARY ===")
print(f"python {sys.version.split()[0]} on {sys.platform}")
try:
    import importlib.metadata as md

    for pkg in (
        "qiskit", "qiskit-aer", "qiskit-ibm-runtime", "cvxpy", "yfinance", "pandas",
        "pyarrow", "scipy", "numpy", "fastapi", "uvicorn", "pytest",
    ):
        print(f"  {pkg:20s} {md.version(pkg)}")
except Exception:  # noqa: BLE001
    traceback.print_exc()
for name, ok, dt, _ in RESULTS:
    print(f"  {'PASS' if ok else 'FAIL'}  {dt:7.2f}s  {name}")
sys.exit(0 if all(r[1] for r in RESULTS) else 1)
