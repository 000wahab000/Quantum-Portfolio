# TEAMS: find your folder

Teammates: open your folder, open START-HERE.md, and copy-paste each box in order. That's all.

Open your folder → START-HERE.md → follow it top to bottom.

| Folder | Who | Tool | What you build | First prompt |
|---|---|---|---|---|
| [TEAM-1-claude-quantum-core](TEAM-1-claude-quantum-core/START-HERE.md) | Wahab (integrator) | Claude Code | QUBO, QAOA, noise, pipeline, evidence studies; owns the contracts; merges everything | [PROMPT-2-U5-qubo](TEAM-1-claude-quantum-core/PROMPT-2-U5-qubo.md) (U1 first if not on `main`) |
| [TEAM-2-antigravity-data-api](TEAM-2-antigravity-data-api/START-HERE.md) | Teammate 2 | Google Antigravity | Market data with no look-ahead, stock pre-screen, costs, whole shares, the web API | [PROMPT-1-U3-data-layer](TEAM-2-antigravity-data-api/PROMPT-1-U3-data-layer.md) |
| [TEAM-3-antigravity-classical](TEAM-3-antigravity-classical/START-HERE.md) | Teammate 3 | Google Antigravity | Classical baselines, scoring of QAOA, efficient frontier, honest verdict | [PROMPT-1-U8-baselines](TEAM-3-antigravity-classical/PROMPT-1-U8-baselines.md) |
| [TEAM-4-antigravity-frontend](TEAM-4-antigravity-frontend/START-HERE.md) | Teammate 4 | Google Antigravity | The web app: form, live run, results, evidence page, phone layout | [PROMPT-1-U12-shell-form-mocks](TEAM-4-antigravity-frontend/PROMPT-1-U12-shell-form-mocks.md) |

## Phase timeline (T0 = event start)

| Phase | When | TEAM-1 | TEAM-2 | TEAM-3 | TEAM-4 |
|---|---|---|---|---|---|
| Prework | before T0 | U1 scaffold + contracts, U2 rules + briefs | install, clone | install, clone | install, clone |
| Build | T0 to T0+2.5h | U5 QUBO, U6 QAOA | U3 data, U4 screen/costs/OOS | U8 baselines, U9 metrics | U12 shell + form on mocks |
| Integrate | T0+2.5h to T0+4h | U10 pipeline, U7 noise | U11 API + jobs | support U10, fix metrics | U13 results + evidence views |
| Evidence + demo | T0+4h to T0+5h | U14 studies, U15 integration | U15 offline/demo checks | U15 tests | U15 mobile polish |
| Offline phase | after online | XY polish, stretch items | stretch items | stretch items | stretch items |

Shared files: [CONTRACTS.md](CONTRACTS.md) (frozen interfaces, only TEAM-1 changes it), [AGENTS.md](../AGENTS.md) (rules the agents read), [plan](../docs/plans/2026-10-08-2115-feat-quantum-portfolio-optimiser-plan.md). Anything unclear: ask Wahab.
