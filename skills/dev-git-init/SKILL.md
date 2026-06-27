---
name: dev-git-init
description: 'Scaffold the deterministic git enforcement stack for a Node or Python project — husky/pre-commit hooks, commitlint/commitizen with Conventional Commits, gitleaks, .gitignore + .gitattributes + .editorconfig, CONTRIBUTING.md, GitHub PR template + CODEOWNERS + 3 issue templates, CI workflows, scripts/setup-branch-protection.sh. Two modes: audit (read-only) and scaffold (3-question Q&A: stack · branching strategy · reviewer model). Uniformly skip-if-exists. Emits install + branch-protection commands; never executes them. Post-scaffold prompt asks whether to record decisions as an ADR via arch-adr. Triggers on: scaffold git, git init, set up git hooks, install husky, install commitlint, install commitizen, install pre-commit, set up commit conventions, set up PR template, set up CODEOWNERS, branch protection, git workflow setup, dev workflow setup, repo conventions, scaffold contributing.'
version: "2.0.0"
status: active
last_reviewed: 2026-05-28
review_interval: 180d
user-invocable: true
allow_implicit_invocation: true
impact: "medium"
metadata:
  category: "infrastructure"
  complexity: "medium"
---

# Git Enforcement Stack Scaffolder

## Overview

`dev-git-init` provisions the **deterministic git enforcement stack** for a Node or Python project — the layered set of client-side hooks, server-side checks, and convention files that make every contributor (human or AI) produce compliant commits, branches, and PRs without having to remember the rules. It is the one-shot scaffolder that lands before the project's first real commit.

**Two-layer model the skill assumes** (per industry standard pre-AI tooling):

- **Client-side hooks** = fast, bypassable feedback (husky / pre-commit / commitlint / commitizen / gitleaks pre-commit)
- **Server-side checks** = authoritative, unbypassable truth (GitHub Actions + branch protection)

Both layers exist; the AI-skill layer is purely a *compliance helper* on top — it does not replace enforcement.

**Opinionated defaults** (v2.0.0). Most prior choice-points have been replaced by sensible defaults that match the patterns the skill is designed for:

- **Default branch:** assumed `main`. Override only if needed.
- **Commit types:** always the minimal 7 (`feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `perf`). Teams wanting `style/build/ci/revert` edit `commitlint.config.js` post-scaffold.
- **CI workflows:** always scaffolded. Opt-out is `rm -rf .github/workflows`.
- **`.gitignore` on conflict:** skip-if-exists like every other file. Operator manually merges missing patterns.
- **No `--force` mode:** to overwrite an existing file, `rm` it and re-run.

**Three choices preserved** (genuinely vary across projects):

- **Q1 — Stack:** pnpm / npm / yarn / Python (4 options)
- **Q2 — Branching strategy + merge mode:** trunk-based + squash / GitLab Flow / GitFlow (3 options)
- **Q3 — Reviewer model:** solo founder admin-bypass / mutual peer / CODEOWNERS-driven (3 options — **no default; operator must make an explicit governance choice**)

**Scope discipline:**
- This skill **writes files** — it does NOT install dependencies (`pnpm add ...`, `pip install ...`), execute hooks, or apply remote configuration (branch protection on GitHub). It emits commands for the operator to run.
- It is **uniformly skip-if-exists**: every existing file is preserved untouched. To replace one, delete it and re-run.
- It produces no `.claude/*.yaml` config file. The scaffolded standard files (`commitlint.config.js` / commitizen `pyproject.toml` section, `.husky/` or `.pre-commit-config.yaml`, `CONTRIBUTING.md`, `.github/*`) ARE the source of truth that downstream skills (`dev-git-commit`, `dev-pr`) read.

---

## Output catalogue

**All files are skip-if-exists.** To overwrite, delete the file and re-run scaffold. No `--force` flag.

| # | Slot | Files (1 slot = these files) | Stack-specific |
|---|---|---|---|
| 1 | `.husky/commit-msg` *(Node only)* | `.husky/commit-msg` | Node — Python uses `.pre-commit-config.yaml` instead |
| 2 | `.husky/pre-commit` *(Node only)* | `.husky/pre-commit` | Node — see above |
| 3 | `.husky/pre-push` *(Node only)* | `.husky/pre-push` | Node — see above |
| 1–3 (Python) | `.pre-commit-config.yaml` *(Python only)* | `.pre-commit-config.yaml` | Python — replaces the 3 husky slots |
| 4 | Commit linter config | Node: `commitlint.config.js` · Python: `pyproject.toml` `[tool.commitizen]` section appended | Both |
| 5 | `.gitleaks.toml` | `.gitleaks.toml` | Both |
| 6 | `.gitignore` | `.gitignore` | Both (stack-appropriate base) |
| 7 | `.gitattributes` | `.gitattributes` | Both |
| 8 | `.editorconfig` | `.editorconfig` | Both |
| 9 | `CONTRIBUTING.md` | `CONTRIBUTING.md` | Both (text varies per Q2 + Q3) |
| 10 | `.github/PULL_REQUEST_TEMPLATE.md` | (file) | Both |
| 11 | `.github/CODEOWNERS` | (file) | Both |
| 12 | `.github/ISSUE_TEMPLATE/*` | `bug.md` + `feature.md` + `docs.md` (3 files) | Both |
| 13 | `.github/workflows/*` | `lint-build.yml` + `typecheck.yml` + `test.yml` + `gitleaks.yml` (4 files) | Both (runtime + commands differ) |
| 14 | `scripts/setup-branch-protection.sh` | (file) | Both |

**14 logical slots.** Node projects fill slots 1–3 with husky; Python fills the same 3 slots with `.pre-commit-config.yaml`. Everything else is the same across stacks.

What the skill does **NOT** write:
- `lint-staged` config (Node) or per-language lint runners — varies too much within each ecosystem; deferred to follow-up per-stack skills
- PR title enforcement Action like `amannn/action-semantic-pull-request` — commitlint/commitizen on commits + reviewer's checklist on PR title covers it at MVP
- ADRs directly — closing report invokes `arch-adr` via the post-scaffold prompt
- `package.json` / `pyproject.toml` script entries — operator adds via the emitted install command
- `.claude/*.yaml` config — classical configs above ARE the source of truth

---

## Modes

| Mode | Purpose | Side effects |
|---|---|---|
| `audit` | Read-only check: which stack components are in place vs missing | None — report only |
| `scaffold` | 3-question Q&A → generate the stack | Writes files; never overwrites existing ones |

---

## Mode: `audit` (read-only)

Run first whenever the project already has any of the stack components.

### Step 1 — detect existing files

```bash
# Run from project root.
# NOTE on slot counting (see §Counting convention below the loop):
#   - .husky/* (Node) or .pre-commit-config.yaml (Python) = slots 1–3 (one stack populates them)
#   - commitlint.config.{js,mjs} / .commitlintrc.{yaml,json} (Node) OR pyproject.toml [tool.commitizen] (Python) = 1 slot (any one variant)
#   - .github/ISSUE_TEMPLATE/{bug,feature,docs}.md = 1 slot (3 files)
#   - .github/workflows/{lint-build,typecheck,test,gitleaks}.yml = 1 slot (4 files)
#   Loop checks ~20 paths; audit denominator is 14 logical slots.
for f in \
  .husky/commit-msg .husky/pre-commit .husky/pre-push \
  .pre-commit-config.yaml \
  commitlint.config.js commitlint.config.mjs .commitlintrc.yaml .commitlintrc.json \
  .gitleaks.toml \
  .gitignore .gitattributes .editorconfig \
  CONTRIBUTING.md \
  .github/PULL_REQUEST_TEMPLATE.md \
  .github/CODEOWNERS \
  .github/ISSUE_TEMPLATE/bug.md .github/ISSUE_TEMPLATE/feature.md .github/ISSUE_TEMPLATE/docs.md \
  .github/workflows/lint-build.yml .github/workflows/typecheck.yml .github/workflows/test.yml .github/workflows/gitleaks.yml \
  scripts/setup-branch-protection.sh; do
  [ -e "$f" ] && echo "✅ $f" || echo "⬜ $f"
done

# Also check pyproject.toml for [tool.commitizen] section (Python path)
[ -f pyproject.toml ] && grep -q '^\[tool\.commitizen\]' pyproject.toml \
  && echo "✅ pyproject.toml [tool.commitizen]" \
  || echo "⬜ pyproject.toml [tool.commitizen]"
```

Also detect:
- **Stack:** presence of `package.json` (Node) · `pyproject.toml` (Python). **If neither matches, classify as `none / docs-only`** — hook-based pieces cannot run without an app. Recommend either deferring the scaffold or running it after `pnpm init` / `python -m venv && touch pyproject.toml`.
- **Package manager (Node only):** presence of `pnpm-lock.yaml` / `yarn.lock` / `package-lock.json`
- **Default branch:** assumed `main`. Operator may override via Q-skip with `--default-branch <name>` flag. Detection is intentionally not chained — assumption is cheaper, override is one flag.
- **Repo platform:** `git remote get-url origin` (github.com / gitlab.com / bitbucket.org)

**Counting convention for the audit report below:** the denominator is **14 logical slots**, one per row in the §Output catalogue. Each grouped row counts as one slot regardless of how many files it expands to (issue templates = 3 files / 1 slot; workflows = 4 files / 1 slot; commitlint config variants count toward the single commit-linter slot). Mark a slot as **in place** when at least one file in the family exists. For slots 1–3 the rule is: if `.pre-commit-config.yaml` exists (Python), it fills all three; otherwise check each `.husky/*` file (Node).

### Step 2 — report

Report format (in-place count + missing count must always sum to 14):

```
## Audit — git enforcement stack

**Stack detected:** Node + pnpm (pnpm-lock.yaml present)
**Default branch:** main (assumed; override via --default-branch if wrong)
**Platform:** github.com (<owner>/<repo>)

**In place (6 of 14):**
- ✅ .gitignore
- ✅ CONTRIBUTING.md
- ✅ .github/PULL_REQUEST_TEMPLATE.md
- ✅ .github/CODEOWNERS
- ✅ .github/ISSUE_TEMPLATE/{bug, feature, docs}.md  (1 slot — 3 files)
- ✅ scripts/setup-branch-protection.sh

**Missing (8 of 14):**
- ⬜ .husky/commit-msg
- ⬜ .husky/pre-commit
- ⬜ .husky/pre-push
- ⬜ commitlint.config.*  (1 slot — any variant)
- ⬜ .gitleaks.toml
- ⬜ .gitattributes
- ⬜ .editorconfig
- ⬜ .github/workflows/{lint-build, typecheck, test, gitleaks}.yml  (1 slot — 4 files)

**Next action:** run `scaffold` mode to fill the missing 8 components.
The 6 in-place components will be skipped automatically (manual rm + re-run to overwrite).
```

**Docs-only project variant** — when stack detection returns `none / docs-only`, the **Next action** changes:

```
**Next action:** stack is docs-only — hook-based pieces (husky/pre-commit + commitlint/commitizen)
cannot run without an app first. Two paths:
  (1) Defer scaffold until the app is scaffolded (recommended).
  (2) Run `pnpm init` (or `touch pyproject.toml`) first to seed a minimal app,
      then re-run dev-git-init scaffold.
The scaffold WILL run on a docs-only repo but the hook layer will be inert until
an app exists and the install command is executed.
```

End audit mode.

---

## Mode: `scaffold` (interactive Q&A)

### Step 0 — ask the question set

Three questions upfront. User responds like `1A, 2A, 3` — and for Q3 you MUST wait for an explicit answer (there is no default).

```
1. Stack?
   A. pnpm (Node) — recommended for new Node projects
   B. npm (Node)
   C. yarn (Node)
   D. python + pre-commit framework

2. Branching strategy + merge mode?
   A. Trunk-based + squash-merge — recommended for solo + small teams + continuous deploy
   B. GitLab Flow with develop integration branch + squash to main on release cadence
   C. GitFlow (develop + release/* + hotfix/*)

3. Reviewer model? (no default — make an explicit governance choice)
   - Solo founder, admin bypass for self-merge — required-review off; you self-merge via `gh pr merge --admin`
   - Mutual peer review — every PR needs 1 approval from any team member
   - CODEOWNERS-driven — required approval from owners of the changed paths
```

If the operator declines to answer Q3 or asks for a recommendation, **do not pick on their behalf** — re-explain the governance trade-off and re-ask. Q3 is the one decision that has too much downstream consequence (branch protection rules, PR auto-assignment, founder admin-bypass policy) to default.

### Step 1 — detect existing project state

Run the audit detection from §Mode: audit Step 1. Capture the list of files that already exist — those will be silently skipped in Step 3.

Also capture:
- **Owner for CODEOWNERS catch-all:** `gh repo view --json owner -q .owner.login 2>/dev/null || git config user.name`
- **Repo full name:** `gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null` or parse from `git remote get-url origin`
- **Whether an ADR for git branching strategy already exists:** `grep -l -i "branching strategy\|merge mode" docs/architecture/decisions/adr-*.md 2>/dev/null` — if it returns a match, the post-scaffold ADR prompt (Step 4) will be skipped and the closing report will note the existing ADR.

### Step 2 — confirm scope

Echo back the scoped plan with the answer summary at the top:

```
## Plan

**Answers:** Q1=A (pnpm), Q2=A (trunk-based + squash), Q3=solo founder + admin bypass

**Will scaffold (8 missing slots):**
- .husky/commit-msg, .husky/pre-commit, .husky/pre-push
- commitlint.config.js
- .gitleaks.toml
- .gitattributes
- .editorconfig
- .github/workflows/{lint-build, typecheck, test, gitleaks}.yml

**Will skip (6 already exist — manual rm + re-run to overwrite):**
- .gitignore, CONTRIBUTING.md, .github/PULL_REQUEST_TEMPLATE.md, .github/CODEOWNERS,
  .github/ISSUE_TEMPLATE/{bug, feature, docs}.md, scripts/setup-branch-protection.sh

**Will emit (not execute):**
- pnpm install command for husky + commitlint + gitleaks
- `./scripts/setup-branch-protection.sh` instruction (run after first CI workflow)
- Post-scaffold ADR prompt (skipped — `adr-0010-git-branching-strategy-and-merge-mode.md` already exists)

Proceed? (y/n)
```

Wait for confirmation. Stop on `n`.

### Step 3 — write files

For each file in the scoped scaffold list, write the appropriate template from §File templates below, substituting per-answer values.

**Idempotency (uniform — applies to every file):**
- File exists → **skip silently**
- File doesn't exist + parent dir doesn't exist → create dir + file
- File doesn't exist + parent dir exists → create file
- **To overwrite an existing file:** the operator deletes it and re-runs. No `--force` flag exists.

Make scripts executable: `chmod +x .husky/* scripts/*.sh` after writing.

### Step 4 — post-scaffold ADR prompt

After all files are written, ask the operator:

```
Scaffold complete. Want me to record the branching strategy (Q2) + reviewer
model (Q3) decisions as an ADR for revisitability?

This invokes the arch-adr skill to create:
  docs/architecture/decisions/adr-XXXX-git-branching-strategy-and-merge-mode.md

The ADR will document:
  - Q2 = <chosen> as the canonical decision with triggers to revisit
  - Q3 = <chosen> as the reviewer model
  - Cross-references to CONTRIBUTING.md and the branch-protection script

Recommended: yes — makes the decision revisitable rather than silent convention.

(y/n)
```

**Skip this prompt entirely** if Step 1 detected an existing branching-strategy ADR (the existence check from `grep -l ... docs/architecture/decisions/adr-*.md`). In that case the closing report mentions the existing ADR and suggests amending it if the scaffold's Q2/Q3 answers differ from the existing ADR's choices.

On `y`: the closing report's Next-steps section adds an explicit `arch-adr create ...` instruction with the Q2 + Q3 values to seed the ADR.

On `n`: the closing report omits the ADR step.

### Step 5 — closing report

```
## Scaffolded
- ✅ .husky/commit-msg (calls commitlint)
- ✅ .husky/pre-commit (calls gitleaks)
- ✅ .husky/pre-push (placeholder for heavy checks)
- ✅ commitlint.config.js (Conventional Commits + minimal 7-type set)
- ✅ .gitleaks.toml (default + project allowlist scaffold)
- ✅ .gitattributes (LF line endings, binary marking)
- ✅ .editorconfig (2-space indent, UTF-8, LF, trim trailing whitespace)
- ✅ .github/workflows/lint-build.yml
- ✅ .github/workflows/typecheck.yml
- ✅ .github/workflows/test.yml
- ✅ .github/workflows/gitleaks.yml (full-history scan)

## Skipped (already present — manual rm + re-run to overwrite)
- .gitignore
- CONTRIBUTING.md
- .github/PULL_REQUEST_TEMPLATE.md
- .github/CODEOWNERS
- .github/ISSUE_TEMPLATE/{bug, feature, docs}.md
- scripts/setup-branch-protection.sh

## Next steps

1. Install dependencies (operator runs — skill does not execute):

   # Node:
   pnpm add -D husky @commitlint/cli @commitlint/config-conventional
   pnpm exec husky init
   # Python:
   pip install pre-commit commitizen
   pre-commit install --hook-type commit-msg --hook-type pre-commit
   # gitleaks (both stacks): install via OS package manager
   brew install gitleaks   # macOS
   scoop install gitleaks  # Windows
   apt install gitleaks    # Debian/Ubuntu

2. Verify hooks fire:

   echo "test commit" > .git/COMMIT_EDITMSG && pnpm exec commitlint --edit  # should reject
   echo "feat: test commit" > .git/COMMIT_EDITMSG && pnpm exec commitlint --edit  # should pass

3. Commit the scaffold:

   git add .husky/ commitlint.config.js .gitleaks.toml .editorconfig .gitattributes .github/workflows/
   git commit -m "chore(repo): scaffold git enforcement stack via dev-git-init"

4. Push and open the first PR to trigger CI workflows (so status check names register with GitHub).

5. Apply branch protection (once workflows have run at least once):

   ./scripts/setup-branch-protection.sh

[If Step 4 = yes:]
6. Record the branching decisions as an ADR:

   Run the arch-adr skill:
     arch-adr create "ADR-XXXX — Git Branching Strategy and Merge Mode"

   Seed with: Q2 = <chosen branching strategy> · Q3 = <chosen reviewer model>.
   Include the triggers to revisit (team > 3 contributors, scheduled release
   cadence, multi-PR launch coordination, etc.) so the deferral of any
   alternative is documented rather than silent.

[If Step 4 was skipped because an ADR already exists:]
6. An existing ADR was detected:
     docs/architecture/decisions/adr-XXXX-...md
   If the Q2/Q3 answers above differ from what that ADR documents, amend the
   ADR (don't create a duplicate). Otherwise, no action needed.
```

End scaffold mode.

---

## File templates

The templates below are inline for self-contained execution. Substitute placeholders per the Q&A answers.

### `.husky/commit-msg` *(Node only — Q1 = A/B/C)*

```sh
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx --no -- commitlint --edit "$1"
```

`chmod +x .husky/commit-msg`.

### `.husky/pre-commit` *(Node only)*

```sh
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

if command -v gitleaks >/dev/null 2>&1; then
  gitleaks protect --staged --no-banner --redact
else
  echo "⚠ gitleaks not installed — skipping secret scan. Install via your OS package manager."
fi
```

`chmod +x .husky/pre-commit`.

### `.husky/pre-push` *(Node only)*

```sh
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Heavy pre-push checks. Uncomment as the project gains the corresponding scripts.
# pnpm typecheck
# pnpm test
```

`chmod +x .husky/pre-push`.

### `.pre-commit-config.yaml` *(Python only — Q1 = D)*

```yaml
# https://pre-commit.com
# Install hooks: pre-commit install --hook-type commit-msg --hook-type pre-commit
repos:
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.20.0
    hooks:
      - id: commitizen
        stages: [commit-msg]

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.4
    hooks:
      - id: gitleaks
        stages: [pre-commit]
```

### `commitlint.config.js` *(Node — minimal 7-type set, always)*

```js
/** @type {import('@commitlint/types').UserConfig} */
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', ['feat', 'fix', 'docs', 'chore', 'refactor', 'test', 'perf']],
    'subject-case': [2, 'always', 'lower-case'],
    'subject-max-length': [2, 'always', 72],
    'body-max-line-length': [2, 'always', 72],
    'header-max-length': [2, 'always', 100],
  },
};
```

### `pyproject.toml [tool.commitizen]` *(Python — minimal 7-type set, always)*

Append (or merge) the following block in `pyproject.toml`:

```toml
[tool.commitizen]
name = "cz_conventional_commits"
version = "0.1.0"
tag_format = "v$version"
# Restrict to the minimal 7-type set
[tool.commitizen.customize]
example = "feat(scope): short subject"
schema = "<type>(<scope>): <subject>"
schema_pattern = "^(feat|fix|docs|chore|refactor|test|perf)(\\(.+\\))?: .{1,72}$"
```

(If `pyproject.toml` already has a `[tool.commitizen]` section, skip per the skip-if-exists rule.)

### `.gitleaks.toml`

```toml
# gitleaks config — extends the default ruleset.
# Add per-project allowlist entries below as false positives surface.

[allowlist]
description = "Project-specific allowlist"
paths = [
  # '''docs/business/06a-models/.*\.md''',  # example: documentation containing fake API keys
]
regexes = [
  # '''AKIA[0-9A-Z]{16}''',  # example: a specific known-safe pattern
]
```

### `.gitignore`

Per Q1 stack, write the appropriate ignore set.

**Node template:**

```
# Node
node_modules/
.pnpm-store/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build
.next/
out/
build/
dist/

# Environment
.env
.env.local
.env.*.local
!.env.example

# Editor
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

**Python template:**

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/

# Virtual envs
.venv/
venv/
.python-version

# Build
build/
dist/

# Environment
.env
.env.local

# Editor / OS
.vscode/
.idea/
.DS_Store
```

### `.gitattributes` (stack-agnostic)

```
# Normalize line endings on checkout to LF
* text=auto eol=lf

# Specific text types
*.md     text
*.json   text
*.yml    text
*.yaml   text
*.sh     text eol=lf
*.py     text
*.js     text
*.ts     text
*.tsx    text
*.css    text

# Binary types
*.png    binary
*.jpg    binary
*.jpeg   binary
*.gif    binary
*.svg    text
*.ico    binary
*.pdf    binary
*.zip    binary
*.gz     binary
```

### `.editorconfig`

```
# https://editorconfig.org
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 2
insert_final_newline = true
trim_trailing_whitespace = true
max_line_length = 100

[*.py]
indent_size = 4

[*.md]
trim_trailing_whitespace = false
max_line_length = off

[Makefile]
indent_style = tab
```

### `CONTRIBUTING.md`

A narrative document covering: TL;DR · branching strategy per Q2 · branch naming table · Conventional Commits (minimal 7-type set) · PR workflow · CI gates (lint-build, typecheck, test, gitleaks) · reviewer's checklist · review model per Q3 · local pre-flight · AI-assisted dev habits · branch protection rules per Q3 · conventions-change process. Length target: ~200 lines. Per-Q substitution:

- **Q2 = A** → trunk-based + squash; one long-lived branch (`main`); branch lifetime < 1 day
- **Q2 = B** → trunk-based-ish with `develop` integration; squash to `main` on release cadence
- **Q2 = C** → full GitFlow with `develop`, `release/*`, `hotfix/*`; merge-commits to `develop`, squash to `main` on release

- **Q3 = solo + admin bypass** → "Founder reviews all PRs; founder uses `gh pr merge --admin` to self-merge"; branch protection rules section explicitly notes "Do not allow bypassing the above settings" stays UNCHECKED
- **Q3 = mutual peer** → "Every PR needs 1 approval from any team member"; "Do not allow bypassing" UNCHECKED at start (small team), CHECKED once trust established
- **Q3 = CODEOWNERS-driven** → "Required approval from CODEOWNERS of the changed paths"; "Require review from Code Owners" enabled; "Do not allow bypassing" CHECKED

### `.github/PULL_REQUEST_TEMPLATE.md`

```markdown
<!--
Auto-loaded on every PR. Fill every section; delete sections that genuinely don't
apply (don't leave empty placeholders). See CONTRIBUTING.md for the full workflow.
-->

## Summary

<!-- 1–3 sentences. What does this PR change? -->

## Why

<!-- Link the upstream artefact: issue #, ADR-NNNN, PRD-NNNN, or a business reason. -->

Closes #
References:

## What's NOT in this PR

<!--
Anti-scope-creep checkpoint. List anything a reviewer might expect to see here that
you intentionally deferred. If nothing, write "Nothing — fully scoped."
-->

## Pre-flight (tick before requesting review)

- [ ] Ran local pre-flight commands — all green
- [ ] Verified every external API call exists in current vendor docs
- [ ] No secrets, no PII, no `.env` content in the diff
- [ ] Self-reviewed the diff in the GitHub UI before requesting review

## Reviewer attention

<!-- Anything specific to look at? Edge cases? A section you're less sure about? -->

## Test plan

<!-- How did you verify this works? What scenarios did you exercise? -->
```

### `.github/CODEOWNERS`

```
# CODEOWNERS — first-match-wins; later patterns override earlier ones.
# Catch-all routes every PR to the owner.

*    @{{owner}}
```

Substitute `{{owner}}` with the detected GitHub username. For Q3 = CODEOWNERS-driven, prepend a comment noting that path-specific owners should be added as the team grows; the catch-all is the floor, not the ceiling.

### `.github/ISSUE_TEMPLATE/bug.md`

```markdown
---
name: Bug report
about: Something is broken or behaving unexpectedly
title: "fix: "
labels: bug
---

## What happened

## What you expected

## Steps to reproduce

1. 
2. 
3. 

## Environment

- Browser / device:
- URL or page:
- Timestamp:

## Screenshots / logs
```

### `.github/ISSUE_TEMPLATE/feature.md`

```markdown
---
name: Feature request
about: A new capability or improvement
title: "feat: "
labels: feature
---

## What user need does this serve

## What does success look like

## Acceptance criteria

- [ ] 
- [ ] 

## Linked artefacts

- PRD:
- ADR:
- Related issue: #
```

### `.github/ISSUE_TEMPLATE/docs.md`

```markdown
---
name: Documentation
about: A doc is missing, wrong, or unclear
title: "docs: "
labels: documentation
---

## What's wrong / missing

## What should it say
```

### `.github/workflows/lint-build.yml` (per Q1 stack)

**Node template:**

```yaml
name: lint-build
on:
  pull_request:
    branches: [{{default_branch}}]
  push:
    branches: [{{default_branch}}]

jobs:
  lint-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3   # omit for npm/yarn
        with:
          version: latest
      - uses: actions/setup-node@v4
        with:
          node-version-file: '.nvmrc'
          cache: pnpm                 # 'npm' or 'yarn' as appropriate
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm build
```

**Python template:**

```yaml
name: lint-build
on:
  pull_request:
    branches: [{{default_branch}}]
  push:
    branches: [{{default_branch}}]

jobs:
  lint-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version-file: pyproject.toml
      - run: pip install -e .[dev]
      - run: ruff check .
      - run: python -m build
```

Substitute `{{default_branch}}` per detected/assumed value (default `main`).

### `.github/workflows/typecheck.yml`

**Node:** runs `pnpm typecheck` (project-defined; typically `tsc --noEmit`).
**Python:** runs `mypy .` or `pyright`.

(Structure mirrors `lint-build.yml` with the relevant runtime setup.)

### `.github/workflows/test.yml`

**Node:** runs `pnpm test`.
**Python:** runs `pytest`.

(Structure mirrors `lint-build.yml`.)

### `.github/workflows/gitleaks.yml`

```yaml
name: gitleaks
on:
  pull_request:
    branches: [{{default_branch}}]
  push:
    branches: [{{default_branch}}]

jobs:
  gitleaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### `scripts/setup-branch-protection.sh`

```bash
#!/usr/bin/env bash
# Idempotent — re-run anytime to re-apply branch protection rules.
# Pre-requisites:
#   - gh CLI installed and authenticated with admin scope on the repo
#   - First PR has run at least once so required status check names exist
#
# Usage:
#   ./scripts/setup-branch-protection.sh                       # detects repo + uses main
#   ./scripts/setup-branch-protection.sh owner/repo            # explicit repo
#   ./scripts/setup-branch-protection.sh owner/repo branch     # explicit branch

set -euo pipefail

REPO="${1:-$(gh repo view --json nameWithOwner -q .nameWithOwner)}"
BRANCH="${2:-{{default_branch}}}"

echo "Applying branch protection to ${REPO}:${BRANCH} ..."

gh api "repos/${REPO}/branches/${BRANCH}/protection" -X PUT --input - <<'JSON'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["lint-build", "typecheck", "test", "gitleaks"]
  },
  "enforce_admins": {{enforce_admins}},
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": {{require_code_owner_reviews}}
  },
  "restrictions": null,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_conversation_resolution": true
}
JSON

echo "✅ Branch protection applied. Verify in the GitHub UI:"
echo "   https://github.com/${REPO}/settings/branches"
```

Per-Q3 substitution:

| Q3 | `enforce_admins` | `require_code_owner_reviews` |
|---|---|---|
| Solo founder + admin bypass | `false` | `true` |
| Mutual peer | `false` | `false` |
| CODEOWNERS-driven | `true` | `true` |

`chmod +x scripts/setup-branch-protection.sh`.

---

## Stack-specific install commands (closing report)

| Q1 | Install command |
|---|---|
| pnpm (Node) | `pnpm add -D husky @commitlint/cli @commitlint/config-conventional && pnpm exec husky init` |
| npm (Node) | `npm install -D husky @commitlint/cli @commitlint/config-conventional && npx husky init` |
| yarn (Node) | `yarn add -D husky @commitlint/cli @commitlint/config-conventional && yarn husky init` |
| Python | `pip install pre-commit commitizen && pre-commit install --hook-type commit-msg --hook-type pre-commit` |

gitleaks for all: `brew install gitleaks` (macOS) · `scoop install gitleaks` (Windows) · `apt install gitleaks` (Debian/Ubuntu) · or download a binary release from https://github.com/gitleaks/gitleaks/releases

---

## Anti-patterns

1. **Silently overwriting existing files.** Every file is skip-if-exists. To replace one, the operator deletes it and re-runs. No `--force` flag — explicit > magic.
2. **Running installers.** The skill is a scaffolder, not an installer. Emit `pnpm add -D ...` for the operator; do not invoke it.
3. **Applying branch protection from the skill.** Branch protection is a remote side effect with lockout risk. Write the script; do not run it.
4. **Generating `.claude/dev-skills.yaml`.** The classical configs ARE the source of truth. Do not mint a parallel schema.
5. **Hardcoding project-specific scopes** in templates. Templates are domain-agnostic; operators add project-specific content in their CONTRIBUTING.md after scaffolding.
6. **Skipping the audit step on existing projects.** Always detect what's present before scaffolding. The Step 2 scope-confirmation prevents surprises.
7. **Defaulting Q3 (reviewer model).** This is the one decision with too much downstream consequence (branch protection rules, founder admin-bypass policy) to default. If the operator declines to answer, re-explain the trade-off and re-ask. Do not pick on their behalf.
8. **Creating duplicate ADRs.** Step 1 detects an existing branching-strategy ADR via grep; the post-scaffold ADR prompt (Step 4) is skipped if one exists. The closing report notes the existing ADR and suggests amending it instead.
9. **Forgetting `chmod +x` on `.husky/*` and `scripts/*.sh`.** Hooks won't fire if not executable. Step 3 must explicitly set the executable bit on scripts.

---

## Checklist

**Scaffold mode:**

- [ ] 3 questions asked; Q3 answered explicitly (no default applied)
- [ ] Step 1 detected stack + default branch + existing files + existing branching-strategy ADR (if any)
- [ ] Step 2 scope summary echoed with answers + scaffold list + skip list; operator confirmed
- [ ] Every written file exists at its target path; existing files skipped silently
- [ ] All `.husky/*` and `.sh` files are executable (`chmod +x` applied)
- [ ] Step 4 ADR prompt asked (unless skipped per existing-ADR detection)
- [ ] Closing report lists scaffolded vs skipped + emits install command for the chosen Q1 stack + conditional ADR step per Step 4 answer

**Audit mode:**

- [ ] Detection loop run; all 14 logical slots checked
- [ ] Stack + default branch + repo platform detected; docs-only branch handled if no stack
- [ ] Report shows in-place / missing split summing to 14
- [ ] Next-action recommendation given

---

## Relations to other skills

- **Consumed by `dev-git-commit`** (post-rewrite): reads `commitlint.config.js` (Node) / `pyproject.toml [tool.commitizen]` (Python) for type/scope rules; `.husky/commit-msg` or `.pre-commit-config.yaml` to know what's about to run; project script files for pre-flight commands; `CONTRIBUTING.md` for narrative fallback
- **Consumed by `dev-pr`** (post-rewrite): reads `commitlint.config.js` / commitizen schema for PR title format; `.github/PULL_REQUEST_TEMPLATE.md` for body skeleton; `.github/CODEOWNERS` for reviewer acknowledgement; `docs/architecture/decisions/adr-*.md` glob for auto-linking ADR references
- **Invokes `arch-adr`** via the Step 4 post-scaffold prompt (operator runs separately): records the Q2 + Q3 decisions as an ADR for revisitability
- **Independent of `dev-git-worktree`, `agent-ralph-loop`, `dev-stack-guide`** — they operate alongside the enforcement stack without depending on its scaffolding state
- **Detected by `util-metamodel-audit`** indirectly — the optional ADR (if created via Step 4 prompt) is checked for frontmatter validity and ID conventions
