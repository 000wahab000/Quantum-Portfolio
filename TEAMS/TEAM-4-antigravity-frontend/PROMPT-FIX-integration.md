Paste this whole file into your agent (or @-mention it). Team 4, integration fix.

# TEAM-4 · Integration fix (template)

Fill in the failure and the section, then paste.

## Failure

Integration with TEAM-X failed with: `<paste the error, screenshot description, request/response and steps>`.

## Read first

- `AGENTS.md`
- `TEAMS/CONTRACTS.md` section `<section, for example §2.5 or §2.6>`
- `TEAMS/TEAM-4-antigravity-frontend/DETAILS-for-the-agent.md` (your owned paths)
- The matching file in `contracts/api-examples/` and the failing component

## Process

Plan first, list files, and stop for review before editing. Edit only `frontend/`.

## Owned paths / Do not touch

- Owned: `frontend/`.
- Do not touch: everything outside `frontend/`.

## Approach

1. Reproduce with the exact request. Compare the real response with the example JSON and with `frontend/src/api/types.ts`.
2. If the backend response deviates from CONTRACTS.md, stop and report the exact difference to the owner (TEAM-2 for HTTP, TEAM-1 for contract changes). If `types.ts` or a component deviates, fix it in `frontend/`.
3. Make the UI tolerant of the case (missing optional fields, `null` numbers) with a plain-language message instead of a crash.

## Verify

```
cd frontend; npm run build
```

Then repeat the failing steps manually in mock mode and real mode.

## Done checklist

- [ ] Root cause stated in one sentence.
- [ ] Failing steps now pass in both modes; build passes.
- [ ] Result posted in team chat.

## When finished

1. Run the verify command above.
2. If it fails, fix it only inside your owned paths and run it again (up to 3 tries). If it still fails, stop and print the error.
3. When it passes: `git add -A`, then `git commit -m "team-4: fix <short summary>"`.
4. Then `git push -u origin team-4/work`. Never force-push. Never push to `main`.
5. Print a 3-line summary: what was built, the test result, and any known gap.
6. If git reports a conflict or asks for a login, stop and say so. Do not resolve it; Wahab does.
