Paste this whole file into your agent (or @-mention it). Team 3, integration fix.

# TEAM-3 · Integration fix (template)

Fill in the failure and the section, then paste.

## Failure

Integration with TEAM-X failed with: `<paste the error, failing test name and command>`.

## Read first

- `AGENTS.md`
- `TEAMS/CONTRACTS.md` section `<section, for example §1.4 or §2.6>`
- `TEAMS/TEAM-3-antigravity-classical/DETAILS-for-the-agent.md` (your owned paths)
- The failing test and the file named in the error

## Process

Plan first, list files, and stop for review before editing. Edit only owned paths.

## Owned paths / Do not touch

- Owned: `backend/qportfolio/classical/`, `backend/qportfolio/{metrics.py,frontier.py,verdict.py}`, `backend/tests/{test_classical,test_metrics}.py`.
- Do not touch: `contracts.py`, `problem.py`, `pipeline.py`, `qubo/`, `quantum/`, `data/`, `api/`, `contracts/`, `docs/`, `TEAMS/`, `frontend/`.

## Approach

1. Reproduce the failure with the exact command; find the root cause.
2. Fix only inside TEAM-3 owned paths. Never re-implement feasibility (use `Problem.evaluate`). If the contract is wrong or a field is missing, stop and tell the team what to ask TEAM-1.
3. If the bug is in another team's area, write the exact request for the owner and stop.
4. Add or adjust one test that reproduces it.

## Verify

```
cd backend; uv run pytest -q
```

## Done checklist

- [ ] Root cause stated in one sentence.
- [ ] Test reproduces the failure and now passes; full suite green.
- [ ] Result posted in team chat.

## When finished

1. Run the verify command above.
2. If it fails, fix it only inside your owned paths and run it again (up to 3 tries). If it still fails, stop and print the error.
3. When it passes: `git add -A`, then `git commit -m "team-3: fix <short summary>"`.
4. Then `git push -u origin team-3/work`. Never force-push. Never push to `main`.
5. Print a 3-line summary: what was built, the test result, and any known gap.
6. If git reports a conflict or asks for a login, stop and say so. Do not resolve it; Wahab does.
