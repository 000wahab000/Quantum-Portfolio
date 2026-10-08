Paste this whole file into your agent (or @-mention it). Team 1, unit U14.

# TEAM-1 · U14 — Evidence studies script + checked-in results

Evidence + demo phase (T0+4h to T0+5h). Depends on U6, U7, U8, U9 (and U3 for `build_market`).

## Read first

- `AGENTS.md`
- `TEAMS/CONTRACTS.md`: section 1.2 (`build_market`, `Market.subset`), 1.3, 1.4 (`brute_force`, `qaoa_metrics`), section 2.7 (`Study`)
- `TEAMS/TEAM-1-claude-quantum-core/START-HERE.md`
- Plan `docs/plans/2026-10-08-2115-feat-quantum-portfolio-optimiser-plan.md`: KTD7, KTD8, KTD10, KTD12, KTD16, section "U14. Evidence studies script + checked-in results"

## Process

Plan first, list the exact files, and stop for review before editing. Edit only owned paths. The full run takes a long time: start it early, in the background, and commit the JSON as each study finishes.

## Goal

Produce the depth, optimiser, init, mixer and noise evidence that PS-03 asks for, reproducibly.

## Owned paths / Do not touch

- Owned: `backend/scripts/run_studies.py`, `backend/data/studies/`.
- Do not touch: `data/`, `api/`, `classical/`, `metrics.py`, `frontier.py`, `verdict.py`, `frontend/`.

## Files (exact)

- `backend/scripts/run_studies.py`
- `backend/data/studies/depth.json`, `optimizer.json`, `init.json`, `mixer.json`, `noise.json`

## Approach

1. 10 fixed-seed random 10-asset, K=5 instances drawn from the estimation window (`build_market` + `Market.subset`), seeds 1 to 10, q=0.5, shots 4096. Brute force gives each instance's `Landscape` and `qaoa_metrics` gives approximation ratio and P(opt).
2. Studies:
   - depth: p = 1 to 5 x {standard, XY}; mean and std of (1 - approximation ratio) and P(opt).
   - optimizer: COBYLA vs SPSA vs NELDER_MEAD at p=3.
   - init: random vs ramp vs interp (interp is the declared warm start; label it in `notes`).
   - mixer: standard vs XY at the best depth from the depth study (declare the choice in `description`).
   - noise: best configuration, ideal vs noisy, for both mixers; report ideal parameters sampled noisy and noisy-optimised.
3. Write each file in the `Study` shape of section 2.7 (`id`, `title`, `description`, `x_label`, `y_label`, `series[].points[]` with `x`, `y`, `yerr`, `instance` with seeds, `notes`, `generated_at`, `wall_time_s`). Skip studies whose file already exists (resume).
4. Options: `--quick` (2 instances, p <= 2) and `--out DIR` (default `backend/data/studies`). `--quick` must not overwrite committed full results, so point it at a temp dir.

## Interfaces

- Provide (section 2.7): `backend/data/studies/{depth,optimizer,init,mixer,noise}.json`, served by TEAM-2's `/api/studies`.
- Consume: `qaoa_solve`, `noisy_solve` (section 1.3); `brute_force`, `qaoa_metrics` (section 1.4); `build_market`, `Market.subset` (section 1.2).

## Test scenarios

- [ ] `--quick` runs in under 2 minutes and writes schema-valid JSON for every study (validate each file with the `Study` model in `contracts.py`).
- [ ] Re-running skips studies already written.
- [ ] Full study files are committed and render on the Evidence page (TEAM-4).

## Verify

```
cd backend; uv run python scripts/run_studies.py --quick --out "$env:TEMP\qp_studies"
uv run python scripts/run_studies.py          # full run, long
uv run pytest -q
```

## Done checklist

- [ ] Five study JSON files committed, each with instance, seeds and wall time.
- [ ] `GET /api/studies` lists them; the Evidence page renders all five.
- [ ] Committed and pushed to `team-1/work`; 3-line summary printed (Wahab opens the PR and merges).

## When finished

1. Run the verify command above.
2. If it fails, fix it only inside your owned paths and run it again (up to 3 tries). If it still fails, stop and print the error.
3. When it passes: `git add -A`, then `git commit -m "team-1: U14 <short summary>"`.
4. Then `git push -u origin team-1/work`. Never force-push. Never push to `main`.
5. Print a 3-line summary: what was built, the test result, and any known gap.
6. If git reports a conflict or asks for a login, stop and say so. Do not resolve it; Wahab does.
