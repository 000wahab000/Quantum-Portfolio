# AGENTS.md

Always-on rules for every agent in this repo (Google Antigravity and Claude Code). Read fully before editing anything. If a rule here conflicts with a chat instruction, stop and ask.

## Project

Quantum Portfolio Optimiser: our PS-03 entry for Qiskit Fall Fest 2026 (team 4 GOATS). A FastAPI backend turns NIFTY 50 prices into one QUBO of stock picks (risk-weighted variance minus return, plus pluggable constraint terms) and solves it with our own QAOA loop on Qiskit 2.5 V2 primitives and with three classical baselines (brute force, relaxation + rounding, simulated annealing). A React app shows the portfolio, efficient frontier, convergence, sampled bitstrings, noise effect, out-of-sample scores and an honest verdict. Four teams build in parallel against frozen interfaces.

- Plan (requirements R1-R22, decisions KTD1-KTD16, units U1-U15, Verification Contract, Definition of Done): [docs/plans/2026-10-08-2115-feat-quantum-portfolio-optimiser-plan.md](docs/plans/2026-10-08-2115-feat-quantum-portfolio-optimiser-plan.md)
- Frozen interfaces (Python and HTTP): [docs/teams/CONTRACTS.md](docs/teams/CONTRACTS.md)
- Team briefs: [TEAM-1](docs/teams/TEAM-1.md) (quantum core + integrator), [TEAM-2](docs/teams/TEAM-2.md) (data + API), [TEAM-3](docs/teams/TEAM-3.md) (classical + metrics), [TEAM-4](docs/teams/TEAM-4.md) (frontend)
- Problem statement (product authority): [docs/research/00-problem-statement.md](docs/research/00-problem-statement.md)
- Verified versions and working patterns: [docs/research/08-env-spike.md](docs/research/08-env-spike.md)

## Ownership (edit only your team's paths)

| Path | Team |
|---|---|
| `backend/qportfolio/{contracts.py,problem.py,pipeline.py}`, `backend/qportfolio/__init__.py` | TEAM-1 (Claude Code) |
| `backend/qportfolio/qubo/`, `backend/qportfolio/quantum/` | TEAM-1 |
| `backend/scripts/{smoke.py,run_studies.py}`, `backend/data/studies/` | TEAM-1 |
| `contracts/` (example payloads) | TEAM-1 |
| `backend/pyproject.toml`, `backend/uv.lock`, `backend/.python-version`, `.gitignore`, `README.md` | TEAM-1 |
| `AGENTS.md`, `CLAUDE.md`, `docs/` | TEAM-1 |
| `backend/qportfolio/data/`, `backend/qportfolio/api/` | TEAM-2 (Antigravity) |
| `backend/scripts/fetch_snapshot.py`, `backend/data/nifty50.csv`, `backend/data/snapshot/` | TEAM-2 |
| `backend/qportfolio/classical/`, `backend/qportfolio/{metrics.py,frontier.py,verdict.py}` | TEAM-3 (Antigravity) |
| `frontend/` | TEAM-4 (Antigravity) |

- Tests: each team owns the test files named in its units. TEAM-1: `test_contracts.py`, `test_problem.py`, `test_qubo.py`, `test_qaoa.py`, `test_noise.py`, `test_pipeline.py`. TEAM-2: `test_data.py`, `test_screen_costs.py`, `test_api.py`. TEAM-3: `test_classical.py`, `test_metrics.py`. All in `backend/tests/`.
- Each package's `__init__.py` belongs to that package's team. Any shared file not listed above belongs to TEAM-1.
- Need a change in someone else's path? Ask the owner in team chat. Do not "just fix it".

## Golden rules

1. Edit only the paths your team owns.
2. `docs/teams/CONTRACTS.md` is frozen. Only TEAM-1 changes it. If it looks wrong or incomplete, keep building against the current version and ask TEAM-1 in chat. Do not work around it silently.
3. No new dependencies (Python or npm) without TEAM-1. The only approved frontend stack is React 19, Vite 8, TypeScript, Tailwind 4 with `@tailwindcss/vite`, Recharts 3 (KTD14).
4. PS-03 honesty rules (automated gates exist; see Verification Contract in the plan):
   - Never solve classically and wrap the answer in a circuit. QAOA's portfolio is the best feasible bitstring sampled from the optimised circuit.
   - Never inject the known optimum, or any classical solution, as an initial state. The only warm start is `interp` from QAOA's own depth p-1 parameters, labelled wherever it appears.
   - No future data in estimation. Only the estimation window feeds mu, Sigma, the pre-screen and estimation-end prices.
   - Never claim quantum advantage. Neutral or negative findings are fine. Banned in any verdict or UI text: "advantage", "outperforms classical", "quantum speedup".
   - Never silently repair infeasible QAOA samples. No feasible sample means `selection: null`, shown as such.
   - `Problem.evaluate` is the only feasibility judge and the only objective evaluator. Never re-implement either.
5. Keep code minimal ("ponytail"): the smallest change that fully works. No speculative abstractions, flags, config layers or helper modules. Reuse before writing. Delete dead code and experiments before committing.
6. Every non-trivial function gets a small pytest (frontend: `npm run build` plus the manual checks in your brief). Tests are deterministic (fixed seeds) and make no network calls (patch them).
7. Never read, print or commit `.env` or any secret.
8. Create files only at the exact paths your brief names. Never "make a new X" where it could overwrite an existing file. Never delete directories.
9. Keep token cost low: read only the plan sections for your unit (by U-ID and KTD-ID), not the whole repo. Do not paste large outputs into chat.

## Banned and stale APIs

- Packages: `qiskit.algorithms`, `qiskit_algorithms`, `qiskit_finance`, `qiskit_optimization` (none in the solver path; KTD1).
- Qiskit idioms: `from qiskit import Aer`, `execute(`, `QuantumInstance`, V1 `Sampler` / `Estimator` / `BackendSampler` / `BackendEstimator`, `qiskit_ibm_runtime.SamplerV2` / `EstimatorV2` (deprecated in 0.50).
- Passing a raw `QAOAAnsatz` to Aer fails (`unknown instruction: QAOA`). Flatten (decompose) or transpile first.
- pandas-2 idioms on pandas 3: `applymap`, chained assignment, `fillna(method=...)`.
- Allowed Qiskit/Aer/yfinance/cvxpy patterns: only those in `backend/scripts/smoke.py` and `docs/research/08-env-spike.md`. If you need another pattern, ask TEAM-1.
- Self-check before committing (from repo root): `git grep -nE "qiskit\.algorithms|qiskit_algorithms|qiskit_finance|qiskit_optimization|import Aer|QuantumInstance|BackendSampler|BackendEstimator|applymap|execute\(" -- backend` must print nothing.

## Conventions

- Python 3.13 via uv (`uv python pin 3.13`, otherwise uv silently picks 3.14). pandas 3, numpy 2, pydantic 2.
- JSON keys are `snake_case`. Tickers are yfinance tickers (`TCS.NS`). Dates are ISO `YYYY-MM-DD`. Money is INR.
- Returns and volatility are annualised decimals (0.12 = 12%). mu and Sigma are annualised (x252) from daily log returns of the estimation window.
- Bitstring convention: strings in JSON are asset order, x0 first (leftmost). Qiskit counts are little-endian (qubit 0 is the rightmost character), so reverse them inside `backend/qportfolio/quantum/` before anything leaves it. QUBO variable order: assets first, then slack bits.
- Constants: `RF = 0.0557`, `C_BUY = 0.001187`, `C_SELL = 0.001037`.
- Windows: estimation 2023-10-01 to 2025-09-30, test 2025-10-01 to 2026-09-30 (`DEFAULT_WINDOWS`).
- Qubit cap is 16 variables (assets + slack). Every stochastic function takes a seed (default 7).
- `backend/qportfolio/data/` is the Python package; `backend/data/` holds files (CSV, parquet, JSON). Do not mix them up. Resolve file paths relative to `__file__`, never the current directory.

## Commands

| Task | Command |
|---|---|
| Install backend | `cd backend; uv sync` |
| Backend tests (must pass before any merge) | `cd backend; uv run pytest -q` |
| One test file | `cd backend; uv run pytest tests/test_<area>.py -q` |
| Stack smoke | `cd backend; uv run python scripts/smoke.py` |
| API | `cd backend; uv run uvicorn qportfolio.api.main:app --reload --reload-dir qportfolio --port 8000` then `GET http://localhost:8000/api/health` |
| Install frontend | `cd frontend; npm install` |
| Frontend dev | `cd frontend; npm run dev` (proxies `/api` to `:8000`) |
| Frontend on mocks (PowerShell) | `cd frontend; $env:VITE_USE_MOCKS="1"; npm run dev` (bash: `VITE_USE_MOCKS=1 npm run dev`) |
| Frontend build (must pass, no type errors) | `cd frontend; npm run build` |

## Windows notes

- Set `PYTHONUTF8=1` in every shell (PowerShell: `$env:PYTHONUTF8="1"`). Otherwise printing beta/gamma names crashes under cp1252.
- The repo path has spaces (`D:\wahab stuff\wahab code\Quantum-Portfolio`). Quote every path. Scripts resolve paths from their own file.
- First `uv sync` takes about 10 minutes (scipy, pyarrow). Later syncs are instant from the uv cache.
- `uvicorn --reload` needs `--reload-dir qportfolio`, otherwise `.venv` changes cause reload loops.
- No symlinks (they need admin on Windows).

## Git rules

- Branch per task: `team-N/<short-topic>` (for example `team-2/data-layer`).
- Run `git pull origin main` before starting each task. Commit small and often. Commit before every agent run so a bad run is one `git restore` away.
- Never force-push. Never rewrite shared history.
- Never commit `.env`, `.venv`, `node_modules`, `backend/data/cache/`.
- Open a PR to `main`. TEAM-1 merges after `uv run pytest -q` (backend) or `npm run build` (frontend) passes. Do not merge your own PR.

## Agent safety (Antigravity)

- Artifact review policy: Request review. Terminal: Request Review. Windows sandbox mode ON. Non-workspace file access OFF.
- Never use Turbo or Always proceed. Users have reported directory wipes and `.env` leaks.
- Stop at the plan for approval, then review each diff per file before accepting.
- Never delete directories. Never read or print `.env` or secrets. Name exact file paths when asking an agent to create files.
- Commit before each agent run.
