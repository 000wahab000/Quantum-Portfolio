Paste this whole file into your agent (or @-mention it). Team 4, unit U15 (your part).

# TEAM-4 · U15 — Mobile polish and real-API check

Evidence + demo phase (T0+4h to T0+5h). Depends on U10 to U14 on `main` (`git pull origin main` first). Branch `team-4/work`.

## Read first

- `AGENTS.md`
- `TEAMS/CONTRACTS.md`: section 2 (routes and shapes)
- `TEAMS/TEAM-4-antigravity-frontend/DETAILS-for-the-agent.md`
- `TEAMS/TEAM-4-antigravity-frontend/DESIGN.md` (contrast rules)
- Plan `docs/plans/2026-10-08-2115-feat-quantum-portfolio-optimiser-plan.md`: R22, AE5, AE6, section "U15"

## Process

Plan first, list the screens and files, and stop for review before editing. Edit only `frontend/`.

## Goal

The demo is comfortable on a phone and works against the real backend, including the offline banner and cancel.

## Owned paths / Do not touch

- Owned: `frontend/`.
- Do not touch: everything outside `frontend/`. Report backend or contract problems to TEAM-1/2/3.

## Files (exact)

- Edits inside `frontend/src/` only (components, pages, `index.css`).

## Approach

1. Real-API pass: `npm run dev -- --host` against uvicorn on `:8000`; run the default request, a request with all 50 stocks (screen preview first), a request with sector cap and target return, and a noisy run you cancel.
2. Phone pass at 375 px and on a real phone over the LAN: no horizontal page scroll, inputs labelled, tap targets at least 44 px, Glossary tooltips work on tap, charts readable, sticky Cancel visible during runs.
3. Offline pass: with Wi-Fi off, the DataBanner shows `source: snapshot` and the `as_of` date, and the run completes.
4. Error states: API down, job `error`, QAOA `selection: null`, empty studies list: each shows a plain-language message.
5. Remove leftover console logs, unused components and dead code.

## Interfaces

- Provide: none.
- Consume: all of section 2 against the real API.

## Test scenarios (manual)

- [ ] Default run, all-50 run with screen preview, capped run, noisy run with cancel: all behave.
- [ ] 375 px: no horizontal scroll on Optimise, Evidence and Method.
- [ ] Offline: banner shows the snapshot date (AE6); cancel keeps the app responsive (AE5).
- [ ] `npm run build` passes with no type errors.

## Verify

```
cd frontend; npm run build
npm run dev -- --host
```

## Done checklist

- [ ] All manual checks pass on desktop and phone.
- [ ] No files outside `frontend/` changed; no new dependencies.
- [ ] Committed and pushed to `team-4/work`; 3-line summary printed (Wahab opens the PR and merges).

## When finished

1. Run the verify command above.
2. If it fails, fix it only inside your owned paths and run it again (up to 3 tries). If it still fails, stop and print the error.
3. When it passes: `git add -A`, then `git commit -m "team-4: U15 <short summary>"`.
4. Then `git push -u origin team-4/work`. Never force-push. Never push to `main`.
5. Print a 3-line summary: what was built, the test result, and any known gap.
6. If git reports a conflict or asks for a login, stop and say so. Do not resolve it; Wahab does.
