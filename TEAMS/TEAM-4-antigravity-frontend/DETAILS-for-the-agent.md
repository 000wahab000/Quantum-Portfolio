# TEAM-4 DETAILS for the agent: Frontend

Teammates do not need to read this file. The prompt files tell the agent to read it. Human steps are in `START-HERE.md`.

Tool: Google Antigravity (Planning mode, Request review).

Read `TEAMS/TEAM-4-antigravity-frontend/DESIGN.md` (colour palette, shapes, contrast rules) before PROMPT-1. Every colour in the app comes from it.

## Mission

Build the web app a non-quantum investor can actually use: choose stocks and rules, run, watch live progress, and read the result next to the efficient frontier, the classical solvers, the sampled bitstrings, the honesty verdict and the evidence studies, on desktop and at phone width. Delivers the UI side of R9, R15-R22. You work against mocks from T0, so you never wait for the backend.

## Your units

| U-ID | Title | When | Depends on |
|---|---|---|---|
| U12 | Frontend shell, form, mocks, API client | Build (T0 to T0+2.5h) | U1 examples |
| U13 | Frontend results views, charts, evidence page | Integrate (T0+2.5h to T0+4h) | U12 |
| U15 (your part) | Mobile polish and real-API check | Evidence + demo (T0+4h to T0+5h) | U10-U14 |

## Owned paths

- `frontend/` (everything inside it): `package.json`, `vite.config.ts`, `index.html`, `src/{main.tsx,App.tsx,index.css}`, `src/api/`, `src/components/`, `src/pages/`, `src/mocks/`, `src/lib/`.

## Do not touch

- Everything outside `frontend/`: `backend/` (TEAM-1/2/3), `contracts/`, `docs/`, `TEAMS/`, `AGENTS.md`, `CLAUDE.md` (TEAM-1). Read `contracts/api-examples/` only.
- No dependencies beyond React 19, Vite 8, TypeScript, Tailwind 4 with `@tailwindcss/vite`, Recharts 3 (KTD14). Anything else (router, UI kit, state library) needs TEAM-1's approval.
- Need a contract change or a field that is missing from the examples? Ask TEAM-1 in chat.

## Interfaces you provide

- None to other teams. The deliverable is the app: `npm run build` must pass on `main`.

## Interfaces you consume

- HTTP API, CONTRACTS.md §2 (served by TEAM-2): `GET /api/health`, `GET /api/universe` (§2.1), `POST /api/screen` (§2.4), `POST /api/runs`, `GET /api/runs/{job_id}` (§2.5, poll every 500 ms), `DELETE /api/runs/{job_id}`, `GET /api/studies`, `GET /api/studies/{id}` (§2.7).
- Types: RunRequest §2.2, Sample §2.3, JobStatus §2.5, RunResult §2.6 (`solvers`, `qaoa`, `frontier`, `benchmarks`, `verdict`, `recommended`), Study §2.7. `src/api/types.ts` mirrors them by hand.
- While waiting for TEAM-2/TEAM-1: run with mocks, `VITE_USE_MOCKS=1`, which replay `contracts/api-examples/{universe,run_request,screen,job_running,job_done,job_error,studies_index,study_depth}.json`. The Vite dev server proxies `/api` to `:8000` in real mode.

## How to verify

```
cd frontend; npm run build                 # no type errors
$env:VITE_USE_MOCKS="1"; npm run dev       # manual checks on mocks
npm run dev                                # real mode, with uvicorn on :8000
```

- Mock mode: submit shows progress, live convergence and Cancel, then results; Cancel returns to idle.
- `job_done.json`: every R20 element visible; frontier markers match the solver table. A QAOA `selection: null` case shows "QAOA found no feasible portfolio".
- Evidence page: each study renders with axis labels, seeds, dates.
- Phone width (375 px device toolbar, then a real phone over LAN with `npm run dev -- --host`): no horizontal scroll, inputs labelled.
- API down in real mode: plain-language error with a Retry button.

## Definition of done

- [ ] `npm run build` passes with no type errors on `main`.
- [ ] U12 and U13 manual checks pass on desktop and at 375 px.
- [ ] Every R20 element is visible: portfolio table, return/variance/objective, efficient frontier with all solvers, convergence curve, bitstring distribution with feasible states marked, honesty panel.
- [ ] Evidence page shows depth, optimiser, init, mixer and noise studies with instance details.
- [ ] Quantum terms have plain-language tooltips; no "advantage" wording anywhere; QAOA `selection: null` is handled.
- [ ] No new dependencies, no files outside `frontend/`.
- [ ] Committed and pushed to `team-4/work`; 3-line summary printed (Wahab merges).

## Handoff

- One branch only: `team-4/work`. The agent commits and pushes it at the end of every prompt (see "When finished" in each prompt file). Never push to `main`, never force-push.
- Wahab (TEAM-1) opens the pull requests, merges and resolves conflicts. If `git pull origin main` reports a conflict, stop, do not resolve it, and tell the user to message Wahab.
- Final message of every prompt: a 3-line summary (what was built, test result, known gaps).

## Pitfalls

- Tailwind v4: `@import "tailwindcss";` in `src/index.css` and the `@tailwindcss/vite` plugin. There is no `tailwind.config.js`, no `postcss.config.js`, and no `@tailwind base/components/utilities`.
- Recharts 3 differs from 2: do not paste v2 snippets (removed props such as `activeIndex`); wrap charts in `ResponsiveContainer` inside a parent with an explicit height or they render at zero height.
- Mobile 375 px: no horizontal page scroll. Put wide tables in an `overflow-x-auto` wrapper, stack the layout below `lg:`, make tap targets at least 44 px.
- Never show "advantage", "beats classical" or "speedup" wording. Verdict text comes from the backend; render it as is. A neutral or negative verdict is a normal result.
- QAOA can have `selection: null` (no feasible sample): show "QAOA found no feasible portfolio" plus `feasible_rate`; guard every access to `selection`, `bitstring` and the numeric fields.
- Polling: clear the interval on unmount, done, error and cancel; never leave two pollers running. Keep the UI responsive during long noisy runs.
- `VITE_USE_MOCKS` on PowerShell: `$env:VITE_USE_MOCKS="1"; npm run dev` (the bash form `VITE_USE_MOCKS=1 npm run dev` fails). If Vite blocks `../contracts/api-examples` imports, set `server.fs.allow: ['..']`.
- Annualised returns and volatility are decimals (0.12 = 12%). Display as percentages, and never hard-code numbers: everything on screen comes from the payload.
