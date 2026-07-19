---
name: util-toolkit-doctor
description: "Audit and repair the Claude Code setup health — chezmoi state, dotfiles + homemade-claude-kit repo sync, and ~/.claude/ symlink integrity. Auto-fixes safe drift but stops on uncommitted local changes. Use when the user asks to check, audit, sync, repair, doctor, or initialize their Claude setup, dotfiles, kit repo, skills, or commands installation."
allowed-tools: Bash(chezmoi *) Bash(git *) Bash(ls *) Bash(readlink *) Bash(stat *) Bash(test *) Bash(cat *) Bash(~/projects/homemade-claude-kit/util-toolkit-doctor/scripts/gather-state.sh) Bash(~/projects/homemade-claude-kit/install.sh*)
status: active
last_reviewed: 2026-05-29
version: "1.0.0"
user-invocable: true
impact: "low"
---

# util-toolkit-doctor

Diagnose and (safely) repair the health of Victor's Claude Code setup.

## Step 1 — Always run the diagnostic first

```bash
~/projects/homemade-claude-kit/util-toolkit-doctor/scripts/gather-state.sh
```

The script is read-only. It checks:

- **Prerequisites**: `chezmoi`, `git`, `gh`, SSH auth to `github.com`
- **Dotfiles repo** (`~/.local/share/chezmoi`): existence, remote, working tree clean, ahead/behind origin
- **Chezmoi deployed-vs-source drift**: `chezmoi status` output
- **Kit repo** (`~/projects/homemade-claude-kit`): same checks as dotfiles
- **Symlink health**: every entry under `~/.claude/skills/` and `~/.claude/commands/` must be a symlink resolving into `~/projects/homemade-claude-kit/`

## Step 2 — Detect mode

- **Init mode**: dotfiles repo line says `NOT INITIALIZED`. Machine is fresh — go to "Init mode" below.
- **Audit mode**: dotfiles repo exists. Walk findings and apply the auto-fix policy.

## Step 3 — Apply auto-fix policy

### ✓ Safe to auto-fix without asking

| Finding | Fix |
|---------|-----|
| Symlink drift in `~/.claude/skills/` or `~/.claude/commands/` (real dirs, broken symlinks, wrong-target symlinks) | `~/projects/homemade-claude-kit/install.sh` |
| Kit repo missing AND dotfiles healthy | `chezmoi apply` (triggers the on-change hook to clone the kit) |
| Either repo **clean** AND **behind origin** with **0 commits ahead** | `git -C <repo> pull --ff-only` |
| Chezmoi has only deployed-state drift (`chezmoi status` shows changes) AND source is clean | `chezmoi apply` |

After any auto-fix, re-run the diagnostic and confirm the issue is gone before reporting.

### ✗ STOP and propose-confirm — NEVER auto-fix

| Finding | Action |
|---------|--------|
| **Uncommitted local changes** in dotfiles or kit repo | Show `git status --short` + `git diff --stat`. Propose: (a) `/commit` then push, (b) stash, (c) discard (require explicit "yes discard"). Wait for the user. |
| **Local commits ahead of origin** in either repo | Propose `git push`. Don't push without confirmation — pushing is a shared-state action. |
| **Diverged branches** (both ahead and behind) | Propose `git pull --rebase` (preferred) or merge. Ask which. Never force-push. |
| **Missing prerequisites** (`chezmoi`, `git`, `gh`) | Tell the user how to install on their platform. Do not attempt to install yourself. |
| **SSH to github.com fails** | Tell the user to run `gh auth login` or set up an SSH key. Do not generate keys yourself. |

## Init mode (uninitialized machine)

1. Verify prereqs (chezmoi, git, gh, ssh) are present and SSH auth works
2. If anything is missing, STOP and tell the user how to install it
3. Show the user the bootstrap command and ask to confirm:
   ```bash
   chezmoi init --apply git@github.com:VictorHueni/dotfiles.git
   ```
4. After confirmation, run it
5. Re-run the diagnostic — verify dotfiles repo, kit repo, and symlinks all came up
6. Report

## Reporting style

After all auto-fixes (and any blocking findings), give a short scannable report. Example:

```
Setup health: ⚠ 2 issues fixed, 1 needs your input

✓ dotfiles: clean, in sync with origin
⚠ kit: was 2 commits behind → pulled (ff-only) ✓
⚠ ~/.claude/skills/: 3 real dirs converted to symlinks ✓
✗ kit has uncommitted changes in commands/draft.md — please choose:
    1. /commit and push
    2. stash
    3. discard (destructive)
```

Keep it terse. No walls of text. Lead with the overall verdict.

## Hard rules

- **Never** force-push, `reset --hard`, or `clean -f` automatically
- **Never** delete files outside `~/.claude/skills/`, `~/.claude/commands/`, or known-drift artifacts under those dirs
- **Never** modify the kit repo or dotfiles repo working trees without confirmation
- The diagnostic script is read-only — running it has zero side effects, so always run it again after a fix to confirm
- When in doubt, surface the finding and ask
