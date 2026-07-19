---
description: Audit every local/remote branch and worktree for merge status, then emit ready-to-run cleanup commands for what's safe to delete
argument-hint: [--no-fetch]
---

Audit the current repository's branches (local + remote) and worktrees, classify each as merged or not, and propose cleanup — never delete anything yourself.

If `$ARGUMENTS` contains `--no-fetch`, skip the fetch step and work off whatever remote-tracking refs are already present. Otherwise run `git fetch --all --prune` first (safe, non-destructive — only updates remote-tracking refs and prunes stale ones).

## Step 1 — Discover integration branches

Detect which of these exist (local or remote) in this repo, in this order of likelihood: `main`, `master`, `staging`, `develop`. These are the **protected branches** — never propose deleting them or their worktrees, and never treat them as "candidates" in the tables below. Every protected branch that exists becomes a merge target checked in Step 3.

Most repos following this convention have exactly two: a long-lived integration branch (`staging`/`develop`) that every feature branch PRs into, and a trunk (`main`/`master`) that the integration branch periodically merges into. Feature branches normally never merge directly into the trunk — so if a non-protected branch turns out to be merged into `main`/`master` but NOT into `staging`/`develop`, flag that explicitly as an anomaly in the report (it means history bypassed the normal flow — worth a one-line note, not a blocker).

## Step 2 — Enumerate branches and worktrees

- Local branches: `git for-each-ref refs/heads --format='%(refname:short) %(objectname) %(upstream:short)'`
- Remote branches: `git for-each-ref refs/remotes --format='%(refname:short) %(objectname)'` (exclude `origin/HEAD`)
- Worktrees: `git worktree list --porcelain` — parse `worktree <path>`, `HEAD <sha>`, and `branch refs/heads/<name>` (or note `detached` when there's no branch line)

Merge each branch's local and remote-tracking entries into one row per branch name (e.g. `feat/x` local + `origin/feat/x` remote = one row, noting both exist).

## Step 3 — Classify merge status per branch

For every non-protected branch, against every protected branch detected in Step 1:

1. **Ancestor check** (fast, no network): `git merge-base --is-ancestor <branch> <protected-branch>` (prefer the remote-tracking ref, e.g. `origin/staging`, if it exists; fall back to the local ref otherwise).
2. **Squash/rebase-merge fallback** — ancestor check misses PRs merged with squash or rebase, since the commit SHA never lands on the target branch. If step 1 says "not merged" AND `gh` is installed AND this repo has a GitHub remote (`git remote get-url origin` matches `github.com`): run `gh pr list --head <branch-name> --state merged --json number,baseRefName,mergedAt --limit 5` and check if any merged PR's `baseRefName` matches the protected branch. If found, mark merged via that PR number instead of a plain ancestor match.
3. If `gh` is unavailable or there's no GitHub remote, skip step 2 silently but add one caveat line to the final report noting that squash-merged branches may show as "not merged" and should be spot-checked manually.
4. Also check (informationally, not a blocker either way) whether there's an **open** PR for the branch (`gh pr list --head <branch-name> --state open`) — worth surfacing so the user doesn't delete something mid-review.

A branch's overall verdict is **merged** if it's merged (by either method) into *any* protected branch that exists in this repo; otherwise **not merged**.

## Step 4 — Classify worktrees

For each worktree from Step 2 (excluding the main/primary worktree — the one at the repo root, which can never be `git worktree remove`d):

- Cross-reference its branch against the Step 3 verdict.
- If the worktree is on a **protected branch** → never delete, note why.
- If the worktree is **detached HEAD** → can't use the branch-merge table; instead check `git merge-base --is-ancestor <sha> <protected-branch>` directly against each protected branch. Flag as needing manual judgement if inconclusive.
- If the worktree's working tree is dirty (`git -C <path> status --porcelain` is non-empty) → regardless of merge status, mark **do not delete without review** (uncommitted work would be lost) and show a short summary of what's dirty.
- Otherwise: **safe to delete** only if the branch verdict from Step 3 is **merged** and the tree is clean. **Not merged → never safe to delete**, no matter how old or apparently-abandoned it looks — that's the whole point of this audit.

## Output format

1. **Branch table** — one row per branch (protected branches excluded): `Branch | Local/Remote/Both | Merged→<target1> | Merged→<target2>... | Open PR? | Worktree (path or "none")`.
2. **Worktree table** — one row per non-primary worktree: `Path | Branch (or "detached @ <sha>") | Clean/Dirty | Verdict (safe to delete / keep — reason)`.
3. **Anomalies** — anything that bypassed the normal flow (merged to trunk but not to the integration branch), branches with no worktree that are already merged (candidates for a plain branch delete, no worktree involved), stale remote branches with a deleted upstream tracking ref (`git branch -vv` shows `: gone`).
4. **Caveats** — note if `gh` was unavailable/no GitHub remote (squash-merge blind spot per Step 3.3).
5. **Ready-to-run cleanup commands** — two clearly separated fenced `bash` blocks, for the user to review and run themselves (never execute these):

   ```bash
   # Local cleanup — worktrees + local branches confirmed merged and clean
   git worktree remove <path>
   git branch -d <branch>
   ```

   ```bash
   # Remote cleanup — deletes branches on origin (shared state — review carefully before running)
   git push origin --delete <branch>
   ```

   Only emit a line for a branch/worktree that passed Step 3/4 as merged (and, for worktrees, clean). Never emit a line for anything not-merged, dirty, protected, or with an open PR still pending review. If nothing qualifies for a block, omit that block entirely rather than emitting an empty one.

## Rules

- This is a read-only audit. Do NOT run `git worktree remove`, `git branch -d`/`-D`, `git push --delete`, or any other mutating command yourself — only print them for the user to run.
- Do NOT spawn agents — do the audit inline using Bash, Read, and Grep.
- Keep the report concise: tables over prose, one line of explanation only where the verdict isn't obvious (dirty tree, anomaly, missing `gh`).
