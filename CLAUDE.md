@AGENTS.md

# Claude Code only

- TEAM-1 runs in Claude Code. Start with `claude --permission-mode plan` (or `claude --worktree team-1 --permission-mode plan`) and plan before any edit.
- Use `/ponytail` for coding and `/caveman` for terse output.
- Dispatch coding subagents with model `sonnet` and research subagents with model `haiku`. Keep token cost low: read only the plan sections for the unit at hand.
- Drive work from the units in `docs/plans/2026-10-08-2115-feat-quantum-portfolio-optimiser-plan.md` with `/compound-engineering:ce-work`.
- You own `TEAMS/CONTRACTS.md`. Change it together with `backend/qportfolio/contracts.py` and `contracts/api-examples/` in one commit, then announce it in team chat.
