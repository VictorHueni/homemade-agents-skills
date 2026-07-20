---
description: Audit an execution plan against Ralph Loop requirements and emit the bash command to run it
argument-hint: <path-to-exec-plan-or-workspace>
---

Audit the execution plan at `$ARGUMENTS` against the Ralph Loop Runner requirements, then prepare the bash command to execute it.

If `$ARGUMENTS` is empty, list all workspaces under `docs/plans/active/` and ask which one to audit before proceeding.

If `$ARGUMENTS` points to an `*_exec_*.md` file, resolve the workspace as its parent directory. If it points to a directory, treat it as the workspace.

## Audit checklist

Read the plan and its workspace, then verify each item. Report PASS / FAIL / WARN with a one-line reason per item.

### Workspace structure
1. Workspace dir exists at `docs/plans/active/NNNN_feature-name/`
2. Exec plan file matches `*_exec_*.md` inside the workspace (not at the parent level)
3. If the exec plan frontmatter contains a `prd:` field, the referenced file exists at that path (relative to git root) — FAIL if field is present but file is missing; if field is absent, extract the NNNN prefix from the exec plan filename and check whether `docs/product-specs/prds/prd-NNNN-*.md` exists — WARN if a matching PRD is found but not linked ("PRD found at `<path>` but not linked via prd: frontmatter field")
4. `progress.txt` exists in the workspace

### Plan header
5. Plan has `**Overall Status:**` field (pending | in-progress | done)
6. Plan has `**Current Increment:**` field
7. Plan has a Summary section
8. Plan has a Milestone Chunks table (optional but recommended — WARN if missing)

### Per-increment checks (for every increment in the plan)
9. Has `**Status:**` field (pending | in-progress | done | blocked)
10. Has a Scope section with numbered items
11. Has a Primary files list
12. Has a Test gate section with runnable commands (not TBD, not pseudo, no `...`)
13. Has Exit criteria
14. Test gate commands reference real files/tools — spot-check: do the paths exist under the primary files list?

### Git state
15. Current branch is `ralph/NNNN-feature-name` (or warn if on another branch)
16. Working tree is clean (or warn with a short summary of dirty files)
17. Feature branch exists and is checked out

### Ralph readiness
18. At least one increment has `**Status:** pending` (otherwise the loop has nothing to do)
19. No increment has `**Status:** blocked` (would halt the loop immediately)
20. If the exec plan frontmatter has a `prd:` field, the referenced PRD has user stories with acceptance criteria that map to increments in the plan

## Output format

1. **Audit report** — one line per check, grouped by section, with PASS / FAIL / WARN and a short reason.
2. **Blockers** — any FAILs that would prevent the loop from running. If any exist, STOP and do not emit the command.
3. **Warnings** — non-blocking issues the user should know about before starting.
4. **Ready-to-run command** — if no blockers, emit a single bash oneliner in a fenced code block:

    ```bash
    cd <repo-root-or-worktree-path> && ~/.claude/skills/agent-ralph-loop/scripts/ralph.sh <workspace-dir> --max-iterations <N>
    ```

   Rules for building the command:
   - `<repo-root-or-worktree-path>` — resolve via `git rev-parse --show-toplevel` from the current working directory.
   - `<workspace-dir>` — path to the workspace relative to the repo root.
   - `<N>` — number of pending increments plus a buffer of 3.
   - Add `--with-prd` if the exec plan frontmatter has a `prd:` field pointing to an existing file.
   - Add `--without-prd` only if the user should explicitly skip PRD tracking (otherwise the default auto-detect is fine).
   - Do NOT add `--with-push` unless the user asked for it.

5. **Next steps** — one short paragraph: advise running the command in a detached terminal, and mention that it uses `--dangerously-skip-permissions` internally so each agent can edit/commit without prompts.

## Rules

- Do NOT modify the plan, the PRD, or `progress.txt` during the audit — this is read-only.
- Do NOT run the Ralph Loop yourself — only emit the command for the user to run.
- Do NOT spawn agents — do the audit inline using Read, Grep, Glob, and Bash.
- Keep the report concise — one line per check, no long explanations unless it's a FAIL.
