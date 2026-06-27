---
name: dev-ralph-loop
description: "Execute an implementation plan autonomously using the Ralph Loop protocol. Iterates through increments one at a time: implement, test, commit, repeat. Use when asked to 'run the ralph loop', 'execute this plan', or 'start autonomous execution'."
version: '1.0.0'
user-invocable: true
allow_implicit_invocation: false
impact: 'high'
metadata:
  category: 'execution'
  complexity: 'high'
status: active
last_reviewed: 2026-05-29
---

# Ralph Loop Runner

## Overview

The Ralph Loop is an autonomous execution protocol that drives an implementation plan from start to finish. Each iteration implements one increment, validates it against its test gate, commits the change, and advances to the next increment.

The loop follows the principle: **Perceive → Implement → Validate → Commit → Repeat**.

A fresh agent instance handles each iteration, ensuring clean context and preventing drift. The loop terminates when all increments reach `**Status:** done`.

## Prerequisites

Before starting the Ralph Loop:

1. **Execution plan exists** in `docs/plans/active/` with `**Status:** pending` on every increment.
2. **Optional PRD exists** in `docs/product-specs/` if you want the loop to track acceptance criteria during execution.
3. **Peer review recommended** — run `spec-peer-review` on the execution plan and PRD if both exist.
4. **Test infrastructure works** — verify the project's test commands run successfully.

## Workspace Setup Protocol

Before the first iteration, prepare the workspace:

1. **Create workspace directory**: `docs/plans/active/NNNN_feature-name/`
2. **Move exec plan into workspace**: Move `docs/plans/active/NNNN_exec_feature-name.md` into the workspace directory. The exec plan's `prd:` frontmatter field (if present) points to the PRD at its canonical location — no copy needed.
3. **Create progress log**: `docs/plans/active/NNNN_feature-name/progress.txt`
4. **Create feature branch**: `git checkout -b ralph/NNNN-feature-name`

Workspace structure after setup:

```text
docs/plans/active/NNNN_feature-name/
  NNNN_exec_feature-name.md     # Execution plan (prd: frontmatter field links to canonical PRD)
  progress.txt                  # Iteration log
```

## Iteration Protocol

Each iteration follows this exact sequence:

1. **Read workspace**: Load the exec plan and find the next `**Status:** pending` increment.
2. **Set status**: Change that increment's status from `pending` to `in-progress`. Update `**Current Increment:**` in the plan header.
3. **Implement**: Execute the increment's scope items. Follow the primary files list.
4. **Run test gate**: Execute every command listed in the increment's test gate section.
5. **Pottery wheel**: If any test gate fails, fix the issue and re-run. Maximum 3 retries per increment.
6. **Verify exit criteria**: Confirm every statement in the increment's exit criteria section holds. If a criterion is not met, treat it as a test gate failure and re-enter the pottery wheel.
7. **Mark done**: Change the increment's status from `in-progress` to `done`.
8. **Update PRD if present**: Check off any acceptance criteria (`- [ ]` → `- [x]`) satisfied by this increment. Update each user story's `**Status:**` (`pending` → `in-progress` if some criteria are now checked; `in-progress` → `done` if all criteria for that story are checked). After updating user stories, update the top-level PRD `**Status:**`: set to `in-progress` on the first increment that checks any criterion; set to `complete` when all user story statuses are `done`.
9. **Commit**: Stage and commit with the convention below.
10. **Log progress**: Append an entry to `progress.txt`.
11. **Exit or continue**: If more `pending` increments remain and running interactively, continue to step 1. If running via `ralph.sh`, exit with `RALPH_COMPLETE` signal so the script can spawn a fresh agent.

## Marking Convention

Status values for increments:

- `**Status:** pending` — not yet started
- `**Status:** in-progress` — currently being implemented
- `**Status:** done` — implemented and test gate passed

Status values for milestones (in the Milestone Chunks table):

- `pending` — no increments in this milestone are done
- `in-progress` — at least one increment is done, others remain
- `done` — all increments in this milestone are done

Overall plan status:

- `**Overall Status:** pending` — no work started
- `**Overall Status:** in-progress` — at least one increment done
- `**Overall Status:** done` — all increments done

Optional PRD user story status:

- `**Status:** pending` — not started
- `**Status:** in-progress` — some acceptance criteria checked
- `**Status:** done` — all acceptance criteria checked

## Progress Log Format

Each entry in `progress.txt` follows this format:

```text
## Iteration N
- Increment: XX — [Title]
- Status: done | blocked
- Files changed: [list]
- Test gate: passed | failed (retry M)
- Learnings: [any notable observations]
- Commit: [hash]
- Timestamp: [ISO 8601]
```

## Commit Convention

Use conventional commits with the plan ID as scope:

```text
feat|fix|refactor(NNNN): increment XX — [title]
```

Examples:

- `feat(0001): increment 01 — create database schema`
- `fix(0001): increment 03 — fix validation edge case`
- `refactor(0001): increment 05 — extract shared utilities`

## Completion Detection

The loop is complete when:

1. No increments have `**Status:** pending` or `**Status:** in-progress` in the exec plan.
2. All milestone statuses in the table are `done`.
3. `**Overall Status:**` is set to `done`.

## Archival Protocol

When all increments are done:

1. **Move exec plan**: Move from workspace to `docs/plans/completed/`.
2. **Delete progress log**: Remove `progress.txt`.
3. **Remove workspace**: Delete the empty `NNNN_feature-name/` directory.
4. **Optional**: Invoke `git-dev-pr` to open a pull request for the feature branch.

## Error Recovery

### Blocked increment

If an increment cannot be completed after 3 pottery-wheel retries:

1. Set its status to `**Status:** blocked`.
2. Log the blocker in `progress.txt` with details.
3. Stop the loop — do not skip increments (they may have dependencies).
4. Notify the user with the blocker details.

### Crash recovery

If the agent or script crashes mid-iteration:

1. Check `git status` and `git log` to determine what was committed.
2. Read `progress.txt` to find the last completed iteration.
3. Find the first `**Status:** pending` or `**Status:** in-progress` increment.
4. If an increment is `in-progress` but not committed, reset it to `pending` and restart.

### Max retries

- Per-increment pottery wheel: 3 attempts maximum.
- Per-loop max iterations: configurable via `ralph.sh --max-iterations` (default: 50).

## PRD Modes

`ralph.sh` supports three PRD modes:

- `auto` (default) — if the exec plan's frontmatter contains a `prd:` field pointing to an existing file, the agent reads and updates it; otherwise the loop runs plan-only.
- `--with-prd` — require a `prd:` field in the exec plan frontmatter pointing to an existing file; fail fast if absent or unresolvable.
- `--without-prd` — ignore any `prd:` field and run using only the execution plan and progress log.
