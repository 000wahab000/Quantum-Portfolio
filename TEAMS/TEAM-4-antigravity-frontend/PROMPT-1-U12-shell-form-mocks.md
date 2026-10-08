Paste this whole file into your agent (or @-mention it). Team 4, unit U12.

# TEAM-4 · U12 — Frontend shell, form, mocks, API client

Build phase (T0 to T0+2.5h). Depends on the U1 example payloads in `contracts/api-examples/` (`git pull origin main` first). Branch `team-4/work`.

## Read first

- `AGENTS.md`
- `TEAMS/CONTRACTS.md`: section 2 table (routes), 2.1 Universe, 2.2 RunRequest (validation limits), 2.4 ScreenInfo, 2.5 JobStatus, 2.6 RunResult (for `types.ts`)
- `TEAMS/TEAM-4-antigravity-frontend/DETAILS-for-the-agent.md`
- `TEAMS/TEAM-4-antigravity-frontend/DESIGN.md` (the colour palette and shapes; every colour you use comes from it)
- Plan `docs/plans/2026-10-08-2115-feat-quantum-portfolio-optimiser-plan.md`: KTD14, R18, R19, R22, F1, AE5, section "U12. Frontend shell, form, mocks, API client"
- `contracts/api-examples/*.json` (all eight files)

## Process

Plan first, list the exact files, and stop for review before editing. Edit only `frontend/`.

## Goal

A usable, responsive input flow that works against mocks from T0 and against the real API later.

## Owned paths / Do not touch

- Owned: `frontend/` (everything inside it).
- Do not touch: everything outside `frontend/` (`backend/`, `contracts/`, `docs/`, `TEAMS/`, `AGENTS.md`, `CLAUDE.md`). Read `contracts/api-examples/` only. No dependencies beyond React 19, Vite 8, TypeScript, Tailwind 4 with `@tailwindcss/vite`, and Recharts 3.

## Files (exact)

- `frontend/package.json`, `vite.config.ts`, `index.html`, `src/index.css` (plus the tsconfig files the scaffold generates)
- `frontend/src/main.tsx`, `src/App.tsx`
- `frontend/src/api/types.ts`, `client.ts`, `mock.ts`
- `frontend/src/pages/Optimise.tsx`, `Evidence.tsx`, `Method.tsx`
- `frontend/src/components/UniversePicker.tsx`, `ConstraintsForm.tsx`, `AdvancedQaoa.tsx`, `ScreenPreview.tsx`, `RunProgress.tsx`, `DataBanner.tsx`, `Glossary.tsx`

## Approach

1. Scaffold from the repo root (`frontend/` does not exist yet): `npm create vite@latest frontend -- --template react-ts`, then `cd frontend; npm install; npm install recharts tailwindcss @tailwindcss/vite`. Check versions: react 19, vite 8, recharts 3, tailwindcss 4.
2. Tailwind v4: `@import "tailwindcss";` at the top of `src/index.css`, the `tailwindcss()` plugin from `@tailwindcss/vite` in `vite.config.ts`. No `tailwind.config.js`, no `postcss.config.js`. Right after the import, declare every token of DESIGN.md in `src/index.css` with `@theme { --color-ink: #161E2F; --color-panel: #242F49; ... }` (all nine tokens), then use classes such as `bg-ink`, `bg-panel`, `text-peach`, `border-line`. Set the page background to `ink`, text to `text`, and build the header with the hero gradient from DESIGN.md. Use rounded-2xl cards, the soft shadow and the 16px mobile gutter from DESIGN.md. No other colours.
3. `vite.config.ts`: proxy `/api` to `http://localhost:8000`. If Vite refuses to serve `../contracts/api-examples/*.json`, set `server.fs.allow: ['..']`.
4. `types.ts` mirrors CONTRACTS section 2 by hand (Universe, RunRequest, ScreenInfo, JobStatus, RunResult, SolverResult, Sample, Study). Check it against the example JSON.
5. `client.ts` exposes `getUniverse`, `postScreen`, `startRun`, `getRun`, `cancelRun`, `listStudies`, `getStudy` and switches to `mock.ts` when `import.meta.env.VITE_USE_MOCKS === "1"`. The mock replays `contracts/api-examples/*.json` (for example `import.meta.glob('../../../contracts/api-examples/*.json', { eager: true })`) and simulates progress over about 5 s using `job_running.json` then `job_done.json`; cancel returns state `cancelled`; a way to trigger `job_error.json` (for example a special k) to test errors.
6. Run flow: `POST /api/runs` -> `job_id` -> poll `GET /api/runs/{id}` every 500 ms until `done`, `error` or `cancelled` (clear the timer on unmount, done and cancel); Cancel button calls `DELETE`.
7. Layout: form on the left and results on the right on desktop (`lg:` and up), stacked on mobile. Tabs for Optimise / Evidence / Method via simple state or hash (no router dependency).
8. Form: `UniversePicker` (all 50 or pick; search; excluded tickers disabled with `excluded_reason`), `ConstraintsForm` (risk appetite 0 to 1, K 2 to 15, sector cap off/number, target return off/%, capital, optional holdings as ticker -> shares), `AdvancedQaoa` collapsed (variant, reps 1 to 5, optimizer COBYLA/SPSA/NELDER_MEAD, init random/ramp/interp with interp labelled as the warm start, shots 256 to 20000, maxiter, noise toggle, seed; defaults from `run_request.json`), `ScreenPreview` (when the universe exceeds the qubit cap: call `POST /api/screen` and show the rule, kept, dropped, qubit split), `RunProgress` (progress bar, stage text, live convergence line from `JobStatus.convergence`, Cancel), `DataBanner` (`source`, `as_of`, estimation and test window dates, survivorship note), `Glossary` (plain-language tooltips for QAOA, QUBO, qubit, mixer, depth p, shots, approximation ratio, P(opt), warm start, noise model; work on tap and keyboard).
9. Client-side validation mirrors section 2.2 limits. A down API shows a plain-language error with a Retry button; an `error` job shows its `error` string. `Method.tsx` is static plain-language text on the formulation, QAOA, baselines, honesty rules and limitations (never claim advantage). `Optimise.tsx` leaves a clearly marked slot for the U13 result views.

## Interfaces

- Provide: none to other teams (UI only).
- Consume (HTTP, section 2): `GET /api/universe`, `POST /api/screen`, `POST /api/runs`, `GET /api/runs/{job_id}`, `DELETE /api/runs/{job_id}`, `GET /api/studies`, `GET /api/studies/{id}`. Until TEAM-2's API is up, use mocks with `VITE_USE_MOCKS=1`.

## Test scenarios (build plus manual)

- [ ] `npm run build` passes with no type errors.
- [ ] Manual, mock mode: submitting shows progress, the live convergence line and Cancel, then the finished state. Cancel returns to an idle state.
- [ ] Manual at 375 px width: no horizontal scroll; all inputs reachable and labelled.
- [ ] Manual, real mode with the API down: a plain-language error with a Retry button; nothing crashes.
- [ ] Manual: invalid input (k = 1, shots = 100) is blocked with a clear message.

## Verify

```
cd frontend; npm install; npm run build
$env:VITE_USE_MOCKS="1"; npm run dev
```

Open the printed URL; use the browser device toolbar at 375 px.

## Done checklist

- [ ] Build passes; manual checks pass on desktop and phone width.
- [ ] No dependency outside the approved list; no files outside `frontend/` changed.
- [ ] No "advantage" wording anywhere in the UI copy.
- [ ] Committed and pushed to `team-4/work`; 3-line summary printed (Wahab opens the PR and merges).

## When finished

1. Run the verify command above.
2. If it fails, fix it only inside your owned paths and run it again (up to 3 tries). If it still fails, stop and print the error.
3. When it passes: `git add -A`, then `git commit -m "team-4: U12 <short summary>"`.
4. Then `git push -u origin team-4/work`. Never force-push. Never push to `main`.
5. Print a 3-line summary: what was built, the test result, and any known gap.
6. If git reports a conflict or asks for a login, stop and say so. Do not resolve it; Wahab does.
