# Research: Shared agent setup for Antigravity + Claude Code (2026-10-08)

## Shared instruction files
- **Single source of truth: root `AGENTS.md`.**
  - Antigravity reads it as an always-on workspace rule (IDE, 2.0 app and `agy` CLI).
  - Do not also add `GEMINI.md`. Precedence between the two is undocumented.
- **`CLAUDE.md` = `@AGENTS.md` plus a few Claude-only lines.** Claude Code skips AGENTS.md whenever a CLAUDE.md exists, so the import is required. Do not use a symlink: they fail on Windows without admin or Developer Mode.
- **Skip `.agents/workflows/`.** Workflows are sunset on 2026-10-19.
- **Skip `.agents/skills/`.** Claude doesn't read that path.
- **`.agents/rules/*.md` only for glob-scoped rules.** Each needs valid `trigger:` frontmatter, otherwise the rule is silently dropped.
- **Per-team brief:** `docs/teams/TEAM-N.md`. Plain markdown, readable by both tools.

## Per-team settings
- **Antigravity:**
  - Artifact review policy: **Request review** (halts before plans and diffs).
  - Terminal: **Request Review**.
  - Windows "Enable Sandbox Mode (Preview)": ON.
  - Non-workspace file access: OFF.
  - Start each task in a **New worktree** if you're comfortable with git; otherwise work Local and commit before every run.
  - Never use **Turbo** or **Always proceed**. Users have reported directory wipes and `.env` leaks.
- **Claude Code:** `claude --worktree team-1 --permission-mode plan`, or plan mode via Shift+Tab.

## Kickoff prompt pattern (both tools)
"Read AGENTS.md and docs/teams/TEAM-N.md. Plan first and list target files. Do not edit outside your Owned paths. Run `<verify cmd>`. Stop at the plan for approval."
- Antigravity: attach the files with `@`.
- Claude Code: use `@docs/teams/TEAM-N.md`.

## Prompting tips (Antigravity official CLI best practices)
- Split each task into three phases: explore → plan → execute.
- Name the exact target files and the verification command.
- Name exact new paths. Users report that "make new" can overwrite existing files.
- Review diffs per file, and commit before each run.

## Sources
- https://antigravity.google/docs/rules
- https://antigravity.google/docs/migration/workflows-to-skills
- https://antigravity.google/docs/artifact-review/
- https://antigravity.google/docs/permissions
- https://antigravity.google/docs/agent-settings
- https://antigravity.google/docs/cli/best-practices
- https://code.claude.com/docs/en/memory
