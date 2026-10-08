Paste this whole file into your agent (or @-mention it). Team 1, integration fix.

# TEAM-1 · Integration fix (template)

Fill in the two placeholders, then paste.

## Failure

Integration with TEAM-X failed with: `<paste the error, failing test name and command>`.

## Read first

- `AGENTS.md`
- `TEAMS/CONTRACTS.md` section `<section, for example §1.4 or §2.6>`
- `TEAMS/TEAM-1-claude-quantum-core/START-HERE.md` (your owned paths)
- The failing test and the file named in the error

## Process

Plan first, list files, and stop for review before editing. Edit only owned paths.

## Owned paths / Do not touch

- Owned: `backend/qportfolio/{contracts.py,problem.py,pipeline.py}`, `qubo/`, `quantum/`, `backend/scripts/{smoke.py,run_studies.py}`, `backend/data/studies/`, `contracts/`, `docs/`, `TEAMS/`, your tests.
- Do not touch: `data/`, `api/`, `classical/`, `metrics.py`, `frontier.py`, `verdict.py`, `frontend/`.

## Approach

1. Reproduce the failure with the exact command; find the root cause (our code, their code, or the contract).
2. If the contract is wrong or incomplete: propose the change to `CONTRACTS.md`, `contracts.py` and `contracts/api-examples/` together, apply it, and announce it in team chat. Otherwise fix only inside TEAM-1 paths.
3. If the bug is in another team's area, write the exact fix request for the owner and stop.
4. Add or adjust one test that reproduces it.

## Verify

```
cd backend; uv run pytest -q
```

## Done checklist

- [ ] Root cause stated in one sentence.
- [ ] Test reproduces the failure and now passes; full suite green.
- [ ] Contract changes (if any) announced in team chat.

## When finished

1. Run the verify command above.
2. If it fails, fix it only inside your owned paths and run it again (up to 3 tries). If it still fails, stop and print the error.
3. When it passes: `git add -A`, then `git commit -m "team-1: fix <short summary>"`.
4. Then `git push -u origin team-1/work`. Never force-push. Never push to `main`.
5. Print a 3-line summary: what was built, the test result, and any known gap.
6. If git reports a conflict or asks for a login, stop and say so. Do not resolve it; Wahab does.
