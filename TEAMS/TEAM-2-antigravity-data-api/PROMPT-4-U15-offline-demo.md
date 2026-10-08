Paste this whole file into your agent (or @-mention it). Team 2, unit U15 (your part).

# TEAM-2 · U15 — Offline and demo checks

Evidence + demo phase (T0+4h to T0+5h). Depends on U10 to U14 being on `main` (`git pull origin main` first). Branch `team-2/work`.

## Read first

- `AGENTS.md`
- `TEAMS/CONTRACTS.md`: section 2.1 (`source`, `as_of`), section 1.2 (`load_prices`)
- `TEAMS/TEAM-2-antigravity-data-api/DETAILS-for-the-agent.md`
- Plan `docs/plans/2026-10-08-2115-feat-quantum-portfolio-optimiser-plan.md`: section "U15. Integration, offline demo hardening, README", AE6

## Process

Plan first, list the steps and files, and stop for review before editing. Edit only owned paths.

## Goal

The demo works with the network off, and from a phone on the same Wi-Fi.

## Owned paths / Do not touch

- Owned: `backend/qportfolio/data/`, `backend/qportfolio/api/`, `backend/scripts/fetch_snapshot.py`, `backend/data/{nifty50.csv,snapshot/}`, TEAM-2 tests.
- Do not touch: everything owned by TEAM-1, TEAM-3 or TEAM-4. Report their bugs to the owner instead.

## Files (exact)

- Fixes inside `backend/qportfolio/data/` and `backend/qportfolio/api/` and their tests only; no new files unless a test needs one.

## Approach

1. Wi-Fi off (or `yf.download` patched to fail): start uvicorn; `GET /api/universe` must show `source: "snapshot"` and the snapshot `as_of` date.
2. `POST /api/runs` with `contracts/api-examples/run_request.json` must reach `done`; nothing may call the network at import or startup.
3. `backend/data/cache/` is created on demand and ignored by git.
4. Bind uvicorn to `0.0.0.0` (`--host 0.0.0.0`) and confirm a phone on the same Wi-Fi can load the app through the Vite proxy; the first run after a restart must not time out.
5. Fix any failure inside TEAM-2 paths, with a test where practical.

## Interfaces

- Provide: the offline-capable data layer and API (section 1.2, section 2).
- Consume: the real `pipeline.run` (U10) through the API.

## Test scenarios

- [ ] AE6: with the network off, `/api/universe` reports `source: "snapshot"` and the correct `as_of`.
- [ ] The default run reaches `done` offline, twice in a row without a restart.
- [ ] Startup with no cache directory present works.

## Verify

```
cd backend; uv run pytest -q
uv run uvicorn qportfolio.api.main:app --reload --reload-dir qportfolio --port 8000 --host 0.0.0.0
```

## Done checklist

- [ ] Offline run passes twice; phone check done.
- [ ] Full suite green; no files outside owned paths changed.
- [ ] Committed and pushed to `team-2/work`; 3-line summary printed (Wahab opens the PR and merges).

## When finished

1. Run the verify command above.
2. If it fails, fix it only inside your owned paths and run it again (up to 3 tries). If it still fails, stop and print the error.
3. When it passes: `git add -A`, then `git commit -m "team-2: U15 <short summary>"`.
4. Then `git push -u origin team-2/work`. Never force-push. Never push to `main`.
5. Print a 3-line summary: what was built, the test result, and any known gap.
6. If git reports a conflict or asks for a login, stop and say so. Do not resolve it; Wahab does.
