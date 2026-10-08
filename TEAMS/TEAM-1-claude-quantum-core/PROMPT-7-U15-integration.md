Paste this whole file into your agent (or @-mention it). Team 1, unit U15 (you lead).

# TEAM-1 · U15 — Integration, offline demo hardening, README

Evidence + demo phase (T0+4h to T0+5h). Depends on U10 to U14. All teams contribute fixes in their own areas.

## Read first

- `AGENTS.md`
- `TEAMS/CONTRACTS.md` (sections 1 and 2)
- `TEAMS/TEAM-1-claude-quantum-core/START-HERE.md` (Integrator duties)
- Plan `docs/plans/2026-10-08-2115-feat-quantum-portfolio-optimiser-plan.md`: section "U15. Integration, offline demo hardening, README", "Verification Contract", "Definition of Done", AE6

## Process

Plan first, list the steps and files, and stop for review before editing. Edit only owned paths; route fixes in other teams' areas to their owners with the owner's `PROMPT-FIX-integration.md` prompt.

## Goal

One command per side starts the demo, and it works offline.

## Owned paths / Do not touch

- Owned: `README.md`, fixes in TEAM-1 paths, merging.
- Do not touch: other teams' files (see their briefs). Patch them only if the owner is unavailable, in a separate commit `fix(team-N): ...`, and tell them.

## Files (exact)

- `README.md` (new) and fixes across owned paths.

## Approach

1. On `main`, run the full Verification Contract: `cd backend; uv sync; uv run pytest -q; uv run python scripts/smoke.py`; start uvicorn and `GET /api/health`; `cd frontend; npm install; npm run build`.
2. Confirm the honesty gates are green (penalty argmin U5, no look-ahead U3, no-repair U6, banned-phrase verdict U9) and the AGENTS.md banned-API `git grep` prints nothing.
3. Offline rehearsal with Wi-Fi off: the default run completes and the banner shows the snapshot date. Run it twice in a row without a restart.
4. Phone check over LAN: `uvicorn ... --host 0.0.0.0`, `npm run dev -- --host`, open the laptop IP on the phone, cancel during a noisy run.
5. README: setup, run, method, honesty rules, limitations (survivorship bias, equal weights, n <= 16, link to the evidence page and research notes).

## Interfaces

- Provide: the working demo; README.
- Consume: everything (CONTRACTS.md sections 1 and 2).

## Test scenarios

- [ ] AE6: with Wi-Fi off, the default run completes and the banner shows the snapshot date.
- [ ] Demo script runs end to end twice in a row with no restart.
- [ ] Noise run can be cancelled and the app stays responsive (AE5); phone width has no horizontal scroll.

## Verify

```
cd backend; uv run pytest -q; uv run python scripts/smoke.py
cd ..\frontend; npm run build
```

## Done checklist

- [ ] Full Verification Contract green on `main`.
- [ ] Every R1 to R22 visible in the app or on the Evidence page.
- [ ] README lets a judge run the demo; no stray files or abandoned experiments in the diff.
- [ ] Each team's brief done-list ticked and handoff notes posted.

## When finished

1. Run the verify command above.
2. If it fails, fix it only inside your owned paths and run it again (up to 3 tries). If it still fails, stop and print the error.
3. When it passes: `git add -A`, then `git commit -m "team-1: U15 <short summary>"`.
4. Then `git push -u origin team-1/work`. Never force-push. Never push to `main`.
5. Print a 3-line summary: what was built, the test result, and any known gap.
6. If git reports a conflict or asks for a login, stop and say so. Do not resolve it; Wahab does.
