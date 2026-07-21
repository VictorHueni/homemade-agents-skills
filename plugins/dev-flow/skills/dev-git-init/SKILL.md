---
type: skill
name: dev-git-init
description: 'Scaffold the deterministic git enforcement stack for a Node or Python project — husky/pre-commit hooks, commitlint/commitizen with Conventional Commits, gitleaks, .gitignore + .gitattributes + .editorconfig, CONTRIBUTING.md, GitHub PR template + CODEOWNERS + 3 issue templates, CI workflows, scripts/setup-branch-protection.sh, Dependabot config; on squash-merge strategies also a PR-title lint check, squash-title setting, and a capability scope-enum. Two modes: audit (read-only) and scaffold (3-question Q&A: stack · branching strategy · reviewer model). Uniformly skip-if-exists. Emits install + branch-protection commands; never executes them. Post-scaffold prompt asks whether to record decisions as an ADR via arch-adr. Triggers on: scaffold git, git init, set up git hooks, install husky, install commitlint, install commitizen, set up commit conventions, PR title lint, commit scope enum, branch protection, git workflow setup, dev workflow setup, repo conventions, scaffold contributing, scaffold dependabot.'
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
- **Dependency freshness:** a `.github/dependabot.yml` is always scaffolded (a base slot). It is the freshness mechanism that makes pinning safe — pin actions/dependencies for immutability, Dependabot to keep the pins current. Neither works alone; a stale pin with no watcher is strictly worse than a floating tag.

**Three choices preserved** (genuinely vary across projects):

- **Q1 — Stack + package manager:** pnpm / npm / yarn (Node) · pip-family / uv (Python) (5 options — the package manager pins the exact Dependabot ecosystem; see §Q1 → Dependabot ecosystem)
- **Q2 — Branching strategy + merge mode:** trunk-based + squash / GitLab Flow / GitFlow (3 options)
- **Q3 — Reviewer model:** solo founder admin-bypass / mutual peer / CODEOWNERS-driven (3 options — **no default; operator must make an explicit governance choice**)

**Merge-hygiene layer (conditional — derived from Q2, no extra question).** When Q2 **squash-merges** (option A trunk-based + squash, or option B squash-to-main on release), a squash-merge makes the **PR title** the commit subject that actually lands — and the local `commit-msg` hook never sees it. So the skill additionally scaffolds a **PR-title lint** CI check (reusing the *same* commitlint/commitizen vocabulary — never a second type-list like `amannn/action-semantic-pull-request`), emits the `squash_merge_commit_title = PR_TITLE` repo setting, and — when a capability map / FBS is present — generates a **capability scope-enum** (product/capability slugs + `platform, infra, ci, deps, chore`) wired into both the commit-msg hook and the PR-title lint, with a drift-gate. Full rationale, arming order, and the `cross-cutting` label override live in [`references/scope-enforcement.md`](references/scope-enforcement.md). This layer is inert for GitFlow-only (Q2=C, merge-commits) and degrades to free area/module scopes when there is no capability map.

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
| 15 | `.github/dependabot.yml` | (file) | Both (language ecosystem differs per Q1; `docker` / `docker-compose` blocks emitted only when detected) |
| 16 *(conditional — Q2 squash-merge)* | PR-title lint workflow | `.github/workflows/pr-title-lint.yml` | Both (Node runs commitlint, Python runs `cz check`) |
| 17 *(conditional — capability map/FBS present)* | Capability scope-enum bundle | `scripts/gen-commit-scopes.py` + `.commit-scopes.json` + `.github/workflows/scope-enum-drift.yml` + the `scope-enum` line wired into the slot-4 commit-linter config | Both |

**17 logical slots — 15 base + 2 conditional.** Node projects fill slots 1–3 with husky; Python fills the same 3 slots with `.pre-commit-config.yaml`. Slots 16–17 apply only when their condition holds (see below); everything else is the same across stacks.

**Conditional-slot rules:**
- **Slot 16 (PR-title lint)** is scaffolded only when **Q2 squash-merges** (option A or B). For GitFlow (Q2=C) it is **N/A** — a merge-commit repo lints every branch commit, so the PR title is not the landed subject.
- **Slot 17 (scope-enum bundle)** is scaffolded only when a capability map (`docs/business/03a-capability-map.md`) or FBS (`docs/product-specs/07a-fbs.md`) exists. Absent both, it is **N/A** and scopes fall back to free area/module names (`auth`, `api`, `infra`, `deps`).
- Slot 17's `scope-enum` line only lands if the slot-4 commit-linter config was *also* scaffolded this run (skip-if-exists means a pre-existing config is untouched — the closing report then tells the operator to add the line manually).

**Slot 15 (Dependabot config) is a base slot** — always scaffolded, every repo benefits. It always emits a `github-actions` block (dir `/`, weekly, one grouped PR) plus the language ecosystem from Q1 (`npm` / `pip` / `uv`, dir `/`, monthly, 7-day cooldown, minor+patch grouped); `docker` and/or `docker-compose` blocks are appended **only when a `Dockerfile` / compose file is detected** (never emit empty blocks). `target-branch` is the integration branch derived from Q2. See §`.github/dependabot.yml`, §Q1 → Dependabot ecosystem, and [`references/dependabot-config.md`](references/dependabot-config.md).

What the skill does **NOT** write:
- `lint-staged` config (Node) or per-language lint runners — varies too much within each ecosystem; deferred to follow-up per-stack skills
- A second PR-title type-list Action like `amannn/action-semantic-pull-request` — the PR-title lint (slot 16) reuses the **same** commitlint/commitizen config as the commit-msg hook, so there is one vocabulary and nothing to hand-sync
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
#   - .github/dependabot.yml = slot 15 (base — always)
#   - .github/workflows/pr-title-lint.yml = slot 16 (conditional — Q2 squash-merge)
#   - scripts/gen-commit-scopes.py + .commit-scopes.json + scope-enum-drift.yml = slot 17 (conditional — capability map/FBS)
#   Loop checks ~24 paths; audit denominator is 15 base + up to 2 conditional slots.
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
  scripts/setup-branch-protection.sh \
  .github/dependabot.yml \
  .github/workflows/pr-title-lint.yml \
  scripts/gen-commit-scopes.py .commit-scopes.json .github/workflows/scope-enum-drift.yml; do
  [ -e "$f" ] && echo "✅ $f" || echo "⬜ $f"
done

# Conditions that decide whether slots 16–17 are applicable (vs N/A):
[ -f docs/business/03a-capability-map.md ] || [ -f docs/product-specs/07a-fbs.md ] \
  && echo "capability map / FBS present → slot 17 applies" \
  || echo "no capability map / FBS → slot 17 N/A (area/module scopes)"

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

**Counting convention for the audit report below:** the denominator is **15 base slots + up to 2 conditional slots (16–17)**, one per row in the §Output catalogue. Each grouped row counts as one slot regardless of how many files it expands to (issue templates = 3 files / 1 slot; workflows = 4 files / 1 slot; commitlint config variants count toward the single commit-linter slot; the scope-enum bundle = 3+ files / 1 slot). Mark a slot as **in place** when at least one file in the family exists. For slots 1–3 the rule is: if `.pre-commit-config.yaml` exists (Python), it fills all three; otherwise check each `.husky/*` file (Node). Slot 15 (`.github/dependabot.yml`) is base — always counted. **Conditional slots** are reported as **N/A** (not counted in the denominator) when their condition does not hold: slot 16 is N/A unless the repo squash-merges; slot 17 is N/A unless a capability map / FBS exists. The invariant is: **in-place + missing + N/A = 17**.

### Step 2 — report

Report format (in-place + missing + N/A must always sum to 17):

```
## Audit — git enforcement stack

**Stack detected:** Node + pnpm (pnpm-lock.yaml present)
**Default branch:** main (assumed; override via --default-branch if wrong)
**Platform:** github.com (<owner>/<repo>)
**Merge mode (from CONTRIBUTING.md / assumed Q2):** squash-merge → slot 16 applies
**Capability map / FBS:** present → slot 17 applies

**In place (6 of 17):**
- ✅ .gitignore
- ✅ CONTRIBUTING.md
- ✅ .github/PULL_REQUEST_TEMPLATE.md
- ✅ .github/CODEOWNERS
- ✅ .github/ISSUE_TEMPLATE/{bug, feature, docs}.md  (1 slot — 3 files)
- ✅ scripts/setup-branch-protection.sh

**Missing (11 of 17):**
- ⬜ .husky/commit-msg
- ⬜ .husky/pre-commit
- ⬜ .husky/pre-push
- ⬜ commitlint.config.*  (1 slot — any variant)
- ⬜ .gitleaks.toml
- ⬜ .gitattributes
- ⬜ .editorconfig
- ⬜ .github/workflows/{lint-build, typecheck, test, gitleaks}.yml  (1 slot — 4 files)
- ⬜ .github/dependabot.yml  (slot 15 — base)
- ⬜ .github/workflows/pr-title-lint.yml  (slot 16 — squash-merge repo)
- ⬜ scope-enum bundle: gen-commit-scopes.py + .commit-scopes.json + scope-enum-drift.yml  (slot 17 — 3 files)

**N/A (0 of 17):**  (slots 16–17 both applicable here)

**Next action:** run `scaffold` mode to fill the missing 11 components.
The 6 in-place components will be skipped automatically (manual rm + re-run to overwrite).
```

When a conditional slot does not apply, report it under **N/A** instead of Missing, e.g. for a GitFlow (Q2=C) repo with no capability map:

```
**N/A (2 of 17):**
- ▫️ .github/workflows/pr-title-lint.yml  (slot 16 — repo is not squash-merge)
- ▫️ scope-enum bundle  (slot 17 — no capability map / FBS)
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
1. Stack + package manager? (pins the exact Dependabot ecosystem — see the map below)
   A. pnpm (Node) — recommended for new Node projects
   B. npm (Node)
   C. yarn (Node)
   D. Python, pip-family (pip / pip-tools / poetry / setuptools — requirements.txt or pyproject.toml resolved by pip)
   E. Python, uv (pyproject.toml + uv.lock)

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

#### Q1 → Dependabot ecosystem

Q1 captures the package manager precisely so slot 15's language ecosystem is exact. The Node managers all map to Dependabot's single `npm` ecosystem (which covers `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml`); Python splits into the two Dependabot Python ecosystems — `pip` (requirements/pyproject resolved by pip, pip-tools, poetry, setuptools) and `uv` (its own ecosystem, reads `pyproject.toml` + `uv.lock`):

| Q1 | Package manager | Dependabot `package-ecosystem` |
|---|---|---|
| A | pnpm (Node) | `npm` |
| B | npm (Node) | `npm` |
| C | yarn (Node) | `npm` |
| D | Python, pip-family | `pip` |
| E | Python, uv | `uv` |

**D and E differ ONLY at slot 15.** For every other slot they are the same "Python" path — both use `.pre-commit-config.yaml` (slots 1–3), the `pyproject.toml [tool.commitizen]` linter (slot 4), the Python `.gitignore`, and the Python CI-workflow variants. The pip-vs-uv split exists purely to name the Dependabot ecosystem correctly; wherever a template says "Python" or "Q1 = D/E", treat D and E identically.

**Q2 also drives the merge-hygiene layer — no extra question.** If the answer is **2A or 2B (squash-merge)**, the scaffold list gains slot 16 (`pr-title-lint.yml`) and the closing report emits the `squash_merge_commit_title = PR_TITLE` command; if a capability map / FBS is also detected (Step 1) it gains slot 17 (the scope-enum bundle). If the answer is **2C (GitFlow, merge-commits)**, both are skipped as N/A — read [`references/scope-enforcement.md`](references/scope-enforcement.md) for why.

### Step 1 — detect existing project state

Run the audit detection from §Mode: audit Step 1. Capture the list of files that already exist — those will be silently skipped in Step 3.

Also capture:
- **Owner for CODEOWNERS catch-all:** `gh repo view --json owner -q .owner.login 2>/dev/null || git config user.name`
- **Repo full name:** `gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null` or parse from `git remote get-url origin`
- **Whether an ADR for git branching strategy already exists:** `grep -l -i "branching strategy\|merge mode" docs/architecture/decisions/adr-*.md 2>/dev/null` — if it returns a match, the post-scaffold ADR prompt (Step 4) will be skipped and the closing report will note the existing ADR.
- **Capability map / FBS (drives slot 17):** `[ -f docs/business/03a-capability-map.md ] || [ -f docs/product-specs/07a-fbs.md ]` — if either exists, slot 17 (scope-enum bundle) applies; otherwise it is N/A and CONTRIBUTING.md documents area/module scopes.
- **Squash-merge (drives slots 16–17):** derived from Q2 (2A/2B = squash → slots apply; 2C = merge-commit → N/A). No detection needed — the operator's Q2 answer is authoritative.
- **Dockerfile / compose presence (drives slot 15's optional blocks):** `find . -iname 'Dockerfile' -not -path '*/node_modules/*' -not -path '*/.git/*' | head -1` and `find . \( -iname 'docker-compose*.y*ml' -o -iname 'compose.y*ml' \) -not -path '*/node_modules/*' -not -path '*/.git/*' | head -1`. A Dockerfile hit → append a `docker` block to `dependabot.yml`; a compose hit → append a `docker-compose` block. No hit → omit that block entirely (never emit an empty ecosystem). Direct the block's `directory:` at `/` unless the detected file sits in a subdir, in which case use that subdir.
- **Integration branch (drives slot 15's `target-branch`):** derived from Q2 — the same integration-branch concept `dev-release-init` reads. **2A (trunk-based)** → `main` (default branch == integration branch); **2B (GitLab Flow, develop integration)** or **2C (GitFlow)** → the promotion/integration branch (e.g. `develop`). If a promotion flow is chosen but the integration branch name is unknown, confirm it with the operator rather than inventing one. This value substitutes `{{integration_branch}}` in the template.

### Step 2 — confirm scope

Echo back the scoped plan with the answer summary at the top:

```
## Plan

**Answers:** Q1=A (pnpm), Q2=A (trunk-based + squash), Q3=solo founder + admin bypass

**Will scaffold (9 missing slots):**
- .husky/commit-msg, .husky/pre-commit, .husky/pre-push
- commitlint.config.js
- .gitleaks.toml
- .gitattributes
- .editorconfig
- .github/workflows/{lint-build, typecheck, test, gitleaks}.yml
- .github/dependabot.yml (slot 15 — base; github-actions + npm ecosystem, target-branch: main)

**Will skip (6 already exist — manual rm + re-run to overwrite):**
- .gitignore, CONTRIBUTING.md, .github/PULL_REQUEST_TEMPLATE.md, .github/CODEOWNERS,
  .github/ISSUE_TEMPLATE/{bug, feature, docs}.md, scripts/setup-branch-protection.sh

**Also scaffold (conditional):**
- [Q2=A/B squash] .github/workflows/pr-title-lint.yml (slot 16)
- [capability map/FBS present] scripts/gen-commit-scopes.py + .commit-scopes.json + .github/workflows/scope-enum-drift.yml + commitlint scope-enum line (slot 17)

**Will emit (not execute):**
- pnpm install command for husky + commitlint + gitleaks
- `./scripts/setup-branch-protection.sh` instruction (run after first CI workflow)
- [Q2=A/B squash] `gh api ... squash_merge_commit_title=PR_TITLE` + PR-title-lint arming-order note
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

**Slot 15 (Dependabot config)** — always (base slot): write `.github/dependabot.yml` from the §`.github/dependabot.yml` template. Substitute `{{lang_ecosystem}}` per the Q1 → Dependabot ecosystem map (`npm` / `pip` / `uv`) and `{{integration_branch}}` per the Q2-derived integration branch. Append the `docker` block only if a Dockerfile was detected, and the `docker-compose` block only if a compose file was detected (Step 1) — never emit an empty ecosystem. Skip-if-exists like every file.

**Slot 16 (PR-title lint)** — when Q2 squash-merges: write `.github/workflows/pr-title-lint.yml` (Node or Python variant per Q1). Skip entirely for Q2=C.

**Slot 17 (scope-enum bundle)** — when a capability map / FBS was detected in Step 1:
1. Copy the generator into the target repo: `cp ~/.claude/skills/dev-git-init/scripts/gen-commit-scopes.py scripts/gen-commit-scopes.py` (skip-if-exists like every file).
2. Generate the committed enum: `python3 scripts/gen-commit-scopes.py --out .commit-scopes.json`. If it exits 2 (no sources readable after all), abort slot 17 and fall back to area/module scopes.
3. Write `.github/workflows/scope-enum-drift.yml`.
4. Wire the `scope-enum` line into the slot-4 commit-linter config **only if that config was scaffolded this same run** (a pre-existing `commitlint.config.js` is skip-if-exists, so the closing report instead tells the operator to add the line by hand).

Make scripts executable: `chmod +x .husky/* scripts/*.sh scripts/*.py` after writing.

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
- ✅ .github/dependabot.yml (github-actions weekly + <npm|pip|uv> monthly w/ 7-day cooldown; target-branch: <integration-branch>; [+ docker / docker-compose blocks when a Dockerfile / compose file was detected])
[If Q2 squash-merges:]
- ✅ .github/workflows/pr-title-lint.yml (required check — same vocabulary as the commit-msg hook)
[If capability map / FBS present:]
- ✅ scripts/gen-commit-scopes.py (scope-enum generator)
- ✅ .commit-scopes.json (<N> scopes derived + fixed buckets)
- ✅ .github/workflows/scope-enum-drift.yml (regen-and-diff gate)
- ✅ commitlint.config.js scope-enum wired (or: manual line noted below)

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

   git add .husky/ commitlint.config.js .gitleaks.toml .editorconfig .gitattributes .github/workflows/ .github/dependabot.yml
   git commit -m "chore(repo): scaffold git enforcement stack via dev-git-init"

4. Push and open the first PR to trigger CI workflows (so status check names register with GitHub).

4a. Dependabot arming (no command to run — a timing note): GitHub reads
    `.github/dependabot.yml` from the DEFAULT branch only. On a trunk-based repo
    (default branch == integration branch) it arms as soon as this scaffold lands
    on the default branch. On a promotion flow it arms only after the next
    integration→main promotion — NOT on the merge into the integration branch.
    Confirm the config is live under Insights → Dependency graph → Dependabot.

5. Apply branch protection (once workflows have run at least once):

   ./scripts/setup-branch-protection.sh

[If Q2 squash-merges — emit, do NOT run:]
5a. Set the squash subject to the linted PR title (sibling of branch protection —
    a remote setting; the operator runs it deliberately):

   gh api -X PATCH repos/<owner>/<repo> \
     -f squash_merge_commit_title=PR_TITLE \
     -f squash_merge_commit_message=PR_BODY

5b. Arming order for the PR-title lint required check (0137 lesson): the check
    must REPORT on a PR before it can be registered as required. So:
      (1) merge this scaffold,
      (2) open one PR → `PR Title Lint` (and `scope-enum-drift`) run and report,
      (3) add "PR Title Lint" to the required contexts in
          scripts/setup-branch-protection.sh, then re-run it.
    Do not expect step 5 to register a check GitHub has never seen.

[If capability map / FBS present — the scope-enum is live:]
5c. If commitlint.config.js already existed (skip-if-exists), add the scope-enum
    line by hand so the allowlist is enforced:
      'scope-enum': [2, 'always', require('./.commit-scopes.json').scopes],
    Regenerate after any capability-map change:
      python3 scripts/gen-commit-scopes.py --out .commit-scopes.json
    The `cross-cutting` PR label bypasses the scope check for genuine
    multi-capability PRs. See references/scope-enforcement.md.

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

### `.pre-commit-config.yaml` *(Python only — Q1 = D/E)*

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

A narrative document covering: TL;DR · branching strategy per Q2 · branch naming table · Conventional Commits (minimal 7-type set) · **commit + PR-title scope vocabulary** (capability/product slugs from `.commit-scopes.json`, or free area/module names when there is no enum — see `rules/git-and-tools.md` §"Commit & PR scope vocabulary") · PR workflow · CI gates (lint-build, typecheck, test, gitleaks; **+ PR Title Lint + scope-enum-drift when Q2 squash-merges**) · reviewer's checklist · review model per Q3 · local pre-flight · AI-assisted dev habits · branch protection rules per Q3 · conventions-change process. Length target: ~200 lines. Per-Q substitution:

- **Q2 squash-merge (A/B)** → add a "PR titles are commits" note: the PR title is linted (`PR Title Lint`) and becomes the squash subject (`squash_merge_commit_title = PR_TITLE`); its scope must be in `.commit-scopes.json` (or use the `cross-cutting` label). **Q2=C (GitFlow)** → omit this note; the merge-commit lints branch commits instead.
- **Scope-enum present** → document the allowlist + regen command; **absent** → document that scopes are free area/module names (`auth`, `api`, `infra`, `deps`).

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

### `.github/dependabot.yml` *(slot 15 — base, always scaffolded)*

The dependency-freshness config. Always emits the `github-actions` block plus the language ecosystem from Q1; the `docker` / `docker-compose` blocks are appended **only when detected** (Step 1) — never emit an empty ecosystem. Substitute `{{lang_ecosystem}}` (`npm` / `pip` / `uv`, per §Q1 → Dependabot ecosystem) and `{{integration_branch}}` (per the Q2-derived integration branch). Full rationale — arming gotcha, ecosystem map, group/cooldown policy, integration-branch resolution — lives in [`references/dependabot-config.md`](references/dependabot-config.md).

**Base template (always — `github-actions` + language ecosystem):**

```yaml
# Dependabot dependency-freshness config.
#
# WHY: pinned actions and locked dependencies never float, so a scheduled bump
# PR is the only thing that moves them. Dependabot is the freshness mechanism
# that makes pinning safe — pin for immutability, Dependabot to keep the pins
# current. A stale pin with no watcher is strictly worse than a floating tag.
#
# ARMING GOTCHA: GitHub reads this file from the DEFAULT branch only. On a
# promotion flow (feature -> integration branch -> main), the config therefore
# arms on the next integration->main promotion, NOT on the merge into the
# integration branch. On a trunk-based repo (default branch == integration
# branch == main) it arms immediately.
#
# target-branch: Dependabot opens its PRs against the integration branch so
# they get the same CI gate as any other PR. Resolved from the branching model
# (Q2): `main` for trunk-based; the integration branch for a promotion flow.

version: 2
updates:
  # Pinned actions never float, so a scheduled bump is the only way they move —
  # weekly, no cooldown, one grouped PR (all update-types) to keep noise low.
  - package-ecosystem: "github-actions"
    directory: "/"
    target-branch: "{{integration_branch}}"
    open-pull-requests-limit: 5
    schedule:
      interval: "weekly"
    groups:
      actions-all:
        patterns:
          - "*"

  # Language dependencies: monthly cadence, 7-day cooldown (a supply-chain
  # detection buffer on fresh releases), minor+patch grouped into one PR;
  # majors intentionally fall OUTSIDE the group and arrive as individual PRs so
  # a breaking bump is reviewed on its own. {{lang_ecosystem}} = npm | pip | uv.
  - package-ecosystem: "{{lang_ecosystem}}"
    directory: "/"
    target-branch: "{{integration_branch}}"
    open-pull-requests-limit: 5
    schedule:
      interval: "monthly"
    cooldown:
      default-days: 7
    groups:
      minor-patch:
        update-types:
          - "minor"
          - "patch"
```

**Docker block — append ONLY when a `Dockerfile` was detected:**

```yaml
  # Dockerfile base images. The `docker` ecosystem parses Dockerfiles only.
  - package-ecosystem: "docker"
    directory: "/"
    target-branch: "{{integration_branch}}"
    open-pull-requests-limit: 5
    schedule:
      interval: "weekly"
    groups:
      docker-all:
        patterns:
          - "*"
```

**Compose block — append ONLY when a `docker-compose*.yml` / `compose.yml` was detected:**

```yaml
  # Compose-pinned images. Compose files have their own `docker-compose`
  # ecosystem — the `docker` ecosystem above does NOT parse them.
  - package-ecosystem: "docker-compose"
    directory: "/"
    target-branch: "{{integration_branch}}"
    open-pull-requests-limit: 5
    schedule:
      interval: "weekly"
    groups:
      compose-all:
        patterns:
          - "*"
```

Set each block's `directory:` to `/` unless the detected file lives in a subdirectory, in which case point it there.

### `.github/workflows/pr-title-lint.yml` *(slot 16 — only when Q2 squash-merges)*

Validates the PR title against the **same** Conventional-Commits vocabulary as the local commit-msg hook — because a squash-merge makes the PR title the landed commit subject the hook never sees. The title is passed via `env:` (never inline `${{ }}` in `run:`) for template-injection hardening. `name: PR Title Lint` is the stable branch-protection context — keep it stable.

> Actions are shown with floating tags to match this skill's other workflow templates; if your repo policy requires SHA-pinning, pin each `uses:` to a full commit SHA.

**Node variant** (reuses `commitlint.config.js`, including its `scope-enum`):

```yaml
name: PR Title Lint
on:
  pull_request:
    types: [opened, edited, synchronize, reopened]
    branches: [{{default_branch}}]

permissions:
  contents: read

jobs:
  pr-title:
    name: PR Title Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version-file: '.nvmrc'
      - run: npm install --no-save @commitlint/cli @commitlint/config-conventional
      - name: Validate PR title (commitlint — same config as commit-msg hook)
        env:
          PR_TITLE: ${{ github.event.pull_request.title }}
        run: printf '%s' "$PR_TITLE" | npx --no -- commitlint
```

**Python variant** (reuses `pyproject.toml [tool.commitizen]`):

```yaml
name: PR Title Lint
on:
  pull_request:
    types: [opened, edited, synchronize, reopened]
    branches: [{{default_branch}}]

permissions:
  contents: read

jobs:
  pr-title:
    name: PR Title Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4   # for root pyproject.toml [tool.commitizen]
      - name: Validate PR title (commitizen — same config as commit-msg hook)
        # Pin commitizen to match the .pre-commit-config.yaml commit-msg hook rev.
        env:
          PR_TITLE: ${{ github.event.pull_request.title }}
        run: pipx run --spec commitizen==3.20.0 cz check --message "$PR_TITLE"
```

**Advisory scope-enum step** *(append to the job above — only scaffolded when slot 17 is active)*. Warns (does not fail) when the title's scope is outside `.commit-scopes.json`; bypassed by the `cross-cutting` label. To harden to blocking once the vocabulary settles, swap `::warning::` for `::error::` and add `exit 1`.

```yaml
      - name: Advisory — PR-title scope in capability enum
        if: ${{ hashFiles('.commit-scopes.json') != '' && !contains(github.event.pull_request.labels.*.name, 'cross-cutting') }}
        env:
          PR_TITLE: ${{ github.event.pull_request.title }}
        run: |
          python3 - <<'PY'
          import json, os, re, sys
          title = os.environ["PR_TITLE"]
          m = re.match(r"^[a-z]+(?:\(([^)]+)\))?!?:", title)
          scope = m.group(1) if m and m.group(1) else None
          allowed = set(json.load(open(".commit-scopes.json"))["scopes"])
          if scope and scope not in allowed:
              print(f"::warning::scope '{scope}' is not in .commit-scopes.json "
                    f"({sorted(allowed)}). Use a capability scope or add the "
                    f"'cross-cutting' label. See references/scope-enforcement.md.")
          PY
```

### `.github/workflows/scope-enum-drift.yml` *(slot 17 — only when a capability map / FBS exists)*

Re-runs the generator and diffs against the committed `.commit-scopes.json` — the same regen-and-diff pattern as an `openapi.bundled.yaml` / `requirements.lock` drift-gate. Fails when the capability map / FBS changed without a regen.

```yaml
name: scope-enum-drift
on:
  pull_request:
    branches: [{{default_branch}}]
  push:
    branches: [{{default_branch}}]

permissions:
  contents: read

jobs:
  scope-enum-drift:
    name: scope-enum-drift
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - name: Regenerate scope-enum and diff against committed copy
        run: |
          python3 scripts/gen-commit-scopes.py --out .commit-scopes.generated.json
          if ! diff -u .commit-scopes.json .commit-scopes.generated.json; then
            echo "::error::.commit-scopes.json is stale — the capability map / FBS changed."
            echo "Run: python3 scripts/gen-commit-scopes.py --out .commit-scopes.json  and commit."
            exit 1
          fi
```

### `scripts/gen-commit-scopes.py` *(slot 17 generator — bundled with the skill)*

Not inlined here — the canonical script ships at `~/.claude/skills/dev-git-init/scripts/gen-commit-scopes.py`. Step 3 copies it into the target repo's `scripts/`. It reads `docs/business/03a-capability-map.md` + `docs/product-specs/07a-fbs.md` (both optional), derives a slug per product and per L0 capability domain, appends the fixed buckets `platform, infra, ci, deps, chore`, and writes byte-stable JSON. Exit 2 = no sources → degrade to area/module scopes.

### `commitlint.config.js` scope-enum wiring *(slot 17 — Node, added to the slot-4 config)*

When slot 17 is active **and** `commitlint.config.js` is scaffolded this run, add one rule so the allowlist is enforced natively on both the commit-msg hook and the PR-title lint:

```js
    'scope-enum': [2, 'always', require('./.commit-scopes.json').scopes],
```

(Python commitizen has no native scope-enum; the allowlist there is the workflow's advisory step above.)

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

# Add "PR Title Lint" and "scope-enum-drift" to contexts below ONLY after those
# checks have reported on at least one PR (see references/scope-enforcement.md
# §Arming order) — GitHub rejects a required context it has never seen.
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
10. **Adding `amannn/action-semantic-pull-request` (a second type-list).** The PR-title lint reuses the *same* commitlint/commitizen config as the commit-msg hook — one vocabulary, no drift. A second Action means two type lists to hand-sync.
11. **Interpolating the PR title inline in `run:`.** `${{ github.event.pull_request.title }}` inside a `run:` block is a template-injection hole. Always bind it to `env: PR_TITLE:` and reference `"$PR_TITLE"`.
12. **Running the `gh api` squash-title or branch-protection commands.** Both are remote side effects — emit them, never execute (same discipline as branch protection).
13. **Registering the PR-title check as required before it has reported.** GitHub rejects an unseen context. Merge → open one PR so it reports → then add it to branch protection.
14. **Hand-editing `.commit-scopes.json`.** It is generated; the drift-gate will fail. Change capability names in the source doc and regenerate instead.
15. **Hard-blocking scope from day one, or enforcing "meaningful" scope.** Start advisory with the `cross-cutting` override; only "in the allowlist" is mechanically enforceable, and only harden to blocking once work-item numbers stop leaking.

---

## Checklist

**Scaffold mode:**

- [ ] 3 questions asked; Q3 answered explicitly (no default applied)
- [ ] Step 1 detected stack + default branch + existing files + existing branching-strategy ADR (if any)
- [ ] Step 2 scope summary echoed with answers + scaffold list + skip list; operator confirmed
- [ ] Every written file exists at its target path; existing files skipped silently
- [ ] All `.husky/*`, `.sh`, and `.py` files are executable (`chmod +x` applied)
- [ ] Slot 15 (`.github/dependabot.yml`) scaffolded (base — always); `{{lang_ecosystem}}` set per Q1, `{{integration_branch}}` per Q2; docker/docker-compose blocks appended only when detected
- [ ] Slot 16 (`pr-title-lint.yml`) scaffolded iff Q2 squash-merges; PR title bound via `env:`, not inline
- [ ] Slot 17 (generator + `.commit-scopes.json` + drift-gate + scope-enum wiring) scaffolded iff a capability map / FBS exists; generator exit 2 handled as graceful fallback
- [ ] Step 4 ADR prompt asked (unless skipped per existing-ADR detection)
- [ ] Closing report lists scaffolded vs skipped + emits install command for the chosen Q1 stack + (if Q2 squash) the `squash_merge_commit_title=PR_TITLE` command + arming-order note + conditional ADR step per Step 4 answer

**Audit mode:**

- [ ] Detection loop run; all 15 base + up to 2 conditional slots checked
- [ ] Stack + default branch + repo platform + capability-map/FBS presence detected; docs-only branch handled if no stack
- [ ] Report shows in-place / missing / N/A split summing to 17
- [ ] Next-action recommendation given

---

## Relations to other skills

- **Consumed by `dev-git-commit`** (post-rewrite): reads `commitlint.config.js` (Node) / `pyproject.toml [tool.commitizen]` (Python) for type/scope rules; `.husky/commit-msg` or `.pre-commit-config.yaml` to know what's about to run; project script files for pre-flight commands; `CONTRIBUTING.md` for narrative fallback
- **Consumed by `dev-pr`** (post-rewrite): reads `commitlint.config.js` / commitizen schema for PR title format; `.github/PULL_REQUEST_TEMPLATE.md` for body skeleton; `.github/CODEOWNERS` for reviewer acknowledgement; `docs/architecture/decisions/adr-*.md` glob for auto-linking ADR references
- **Invokes `arch-adr`** via the Step 4 post-scaffold prompt (operator runs separately): records the Q2 + Q3 decisions as an ADR for revisitability
- **Enables `dev-release-init`** (release automation) **and `com-release-note`** (stakeholder narrative): the PR-title lint + `squash_merge_commit_title=PR_TITLE` + capability scope-enum guarantee every squash-merge lands a clean, capability-scoped Conventional Commit — the clean history those skills parse to group and attribute changelog entries. `dev-git-init` owns the commit/PR/merge hygiene contract; the release skills consume it and never touch scopes. Setting up releases next? → `dev-release-init` reads this skill's branching-strategy decision + PR-title-lint layer directly.
- **Implements `rules/git-and-tools.md` §"Commit & PR scope vocabulary"** as mechanical enforcement — that rule is the authoring convention (`dev-git-commit`, `dev-pr`, `plan-implementation`, `agent-ralph-loop` all follow it); this skill's scope-enum + PR-title gate are the backstop.
- **Independent of `dev-git-worktree`, `agent-ralph-loop`, `dev-stack-guide`** — they operate alongside the enforcement stack without depending on its scaffolding state
- **Detected by the `metamodel` skill's Audit mode** indirectly — the optional ADR (if created via Step 4 prompt) is checked for frontmatter validity and ID conventions
