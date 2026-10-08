Paste this whole file into your agent (or @-mention it). Team 3, unit U15 (your part).

# TEAM-3 · U15 — Integration tests on the real pipeline

Evidence + demo phase (T0+4h to T0+5h). Depends on U10 on `main` (`git pull origin main` first). Branch `team-3/work`. During the Integrate phase you also support U10: use `PROMPT-FIX-integration.md` for any failure.

## Read first

- `AGENTS.md`
- `TEAMS/CONTRACTS.md`: sections 1.4, 2.3, 2.6
- `TEAMS/TEAM-3-antigravity-classical/DETAILS-for-the-agent.md`
- Plan `docs/plans/2026-10-08-2115-feat-quantum-portfolio-optimiser-plan.md`: section "U15", "Verification Contract" (honesty gates), U8 and U9 test scenarios

## Process

Plan first, list the exact test cases and files, and stop for review before editing. Edit only owned paths.

## Goal

Prove on real pipeline output that metrics, frontier and verdict are consistent and honest, and fix any defect in your area.

## Owned paths / Do not touch

- Owned: `backend/qportfolio/classical/`, `backend/qportfolio/{metrics.py,frontier.py,verdict.py}`, `backend/tests/{test_classical,test_metrics}.py`.
- Do not touch: everything else. Report defects in other areas to the owner.

## Files (exact)

- Edits inside your owned paths; new test cases in `backend/tests/test_metrics.py` and `backend/tests/test_classical.py` only.

## Approach

1. Run `pipeline.run` on several requests (use `contracts/api-examples/run_request.json` as the base): varied K, sector cap on and off, target return set, holdings entered, `variant` standard and xy, QAOA with no feasible sample (force it by passing penalties of 0 in a test helper if the pipeline allows, otherwise use a hand-built `Sample` list).
2. Assert on the real results: every solver is feasible per `Problem.evaluate`; `qaoa.metrics.p_random` equals 1/`landscape.n_feasible`; the frontier discrete points include the brute-force optimum or a point it dominates; frontier markers match the solver table values.
3. Run the banned-phrase check over `verdict.headline` and every line of `verdict.details` for all of these results.
4. Fix any defect in `classical/`, `metrics.py`, `frontier.py`, `verdict.py`.

## Interfaces

- Provide: unchanged (section 1.4).
- Consume: `pipeline.run` (section 1.5) and the `RunResult` shape (section 2.6).

## Test scenarios

- [ ] Each request above yields a result whose verdict level matches the numbers (`matched`, `near`, `worse`, `no-feasible`).
- [ ] No verdict text contains "advantage", "outperforms classical" or "quantum speedup".
- [ ] Brute force remains under 2 s for 16 assets, K=8.

## Verify

```
cd backend; uv run pytest tests/test_metrics.py tests/test_classical.py -q; uv run pytest -q
```

## Done checklist

- [ ] New integration cases pass; full suite green.
- [ ] No files outside owned paths changed.
- [ ] Committed and pushed to `team-3/work`; 3-line summary printed (Wahab opens the PR and merges).

## When finished

1. Run the verify command above.
2. If it fails, fix it only inside your owned paths and run it again (up to 3 tries). If it still fails, stop and print the error.
3. When it passes: `git add -A`, then `git commit -m "team-3: U15 <short summary>"`.
4. Then `git push -u origin team-3/work`. Never force-push. Never push to `main`.
5. Print a 3-line summary: what was built, the test result, and any known gap.
6. If git reports a conflict or asks for a login, stop and say so. Do not resolve it; Wahab does.
