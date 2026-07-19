---
name: dev-release-init
description: 'Scaffold a release-please SemVer + changelog automation pipeline for a project whose commit hygiene dev-git-init guarantees. Generates release-please-config.json (mandatory include-component-in-tag:false, changelog-sections, extra-files), the manifest + version.txt, and the release-please.yml workflow. Two axes drive it: branch mode (integration-branch-targeted vs main-targeted — read from dev-git-init, never re-asked) and version-source (deployed-app with version.txt as truth + frozen manifests vs published-package with manifest identity). Four modes: audit (gap report; first checks for dev-git-init''s PR-title-lint + squash-title layer, offers to run it), scaffold (Q&A; emits but never runs the gh / tag / branch-protection commands), verify (dry-run to catch silent extra-files failures), seed (minimal anchor tag). Bakes in eight hard-won release lessons as guardrails. Triggers on: release automation, release-please, set up releases, versioning pipeline, changelog automation, cut releases, dev-release-init.'
version: "1.0.0"
status: active
last_reviewed: 2026-07-18
review_interval: 180d
user-invocable: true
allow_implicit_invocation: true
impact: "low"
metadata:
  category: "infrastructure"
  complexity: "medium"
---

# Release Automation Scaffolder

## Overview

`dev-release-init` provisions a **consistent release automation pipeline** — [release-please](https://github.com/googleapis/release-please) config + manifest + workflow — for a project that already produces clean Conventional-Commit history. It cuts SemVer versions, generates the technical `CHANGELOG.md`, tags `vX.Y.Z`, and publishes GitHub Releases, all off the commit history `dev-git-init` guarantees.

It sits in the middle of a three-skill chain and touches only the release layer:

```
dev-git-init      → commit/PR/merge contract        (the clean history — Workstream A)
dev-release-init  → release automation (THIS)        (SemVer + CHANGELOG + tags)
com-release-note  → stakeholder narrative            (curates the changelog)
```

The tool is named **tool-neutrally** (`dev-release-init`, not `dev-release-please-init`) so it survives a swap to any conventional-commit release automator. Deep rationale for every axis, lesson, and file lives in [`references/release-lessons.md`](references/release-lessons.md) — read it before scaffolding.

**Two design axes drive everything generated** (detailed in the reference; summarised here):

- **Axis 1 — Branch mode.** *integration-branch-targeted* (release-please targets an integration branch such as `develop`/pre-prod, promote to `main`) vs *main-targeted* (simple GitHub flow). **Read this from `dev-git-init`'s branching-strategy decision — do not re-ask** (§Detecting the axes).
- **Axis 2 — Version-source strategy (12-factor).** *deployed-app-not-published* (git tag + `version.txt` is truth, `release-type: simple`, language manifests frozen because bumping them desyncs lockfiles) vs *published-package* (the manifest version IS the release identity; `release-type: node`/`python`/…). **Detect the stack, then ask app-vs-library** — this sets `extra-files`, which fails *silently* when wrong.

**Scope discipline (mirrors `dev-git-init`):**
- This skill **writes files** — it does NOT run `gh`, create git tags, apply branch protection, or change repo settings. It **emits** those commands for the operator to run deliberately.
- It is **uniformly skip-if-exists**: every existing file is preserved untouched. To replace one, delete it and re-run.
- It **detects and requires** `dev-git-init`'s PR-title-lint + squash-title hygiene layer; it never duplicates it and never touches commit scopes.

---

## Output catalogue

**All files are skip-if-exists.** To overwrite, delete the file and re-run scaffold. No `--force` flag.

| # | Slot | File | Notes |
|---|---|---|---|
| 1 | Release config | `release-please-config.json` | `include-component-in-tag: false` (mandatory) + `changelog-sections` + `extra-files` (from Axis 2) |
| 2 | Release manifest | `.release-please-manifest.json` | Seeded at the anchor version (`{ ".": "X.Y.Z" }`) |
| 3 *(conditional — Axis 2 = deployed-app)* | Version file | `version.txt` | The release identity for `release-type: simple`. **N/A for published-package** (the manifest is the identity) |
| 4 | Workflow | `.github/workflows/release-please.yml` | `on: push` to the release branch, `target-branch`, `GITHUB_TOKEN`, `permissions: contents+PRs+issues write`, concurrency group |

**4 logical slots — 3 base + 1 conditional (slot 3).** Slot 3 is `version.txt`, present only for the **deployed-app** version-source (it is what `release-type: simple` maintains); for a **published-package** it is N/A because the language manifest carries the version.

**Emitted, never executed** (closing report):
- **Anchor tag** (`seed` mode) — the minimal `git tag vX.Y.Z` so the first fire does not walk all history (lesson 2).
- **Actions-can-create-PRs** repo setting (lesson 7) — release-please cannot open its PR without it.
- **`squash_merge_commit_title = PR_TITLE`** — only if `dev-git-init` (Workstream A) has not already set it.
- **Branch-protection re-apply** — a follow-up step, after the first PR reports (arming order, lesson 6).

What the skill does **NOT** write:
- The `CHANGELOG.md` itself — release-please generates it on the first release PR.
- Any language manifest (`package.json`, `pyproject.toml`, …) — it reads/freezes them, never creates them.
- ADRs directly — the post-scaffold prompt invokes `arch-adr`.
- Retro historical tags, or app-specific version-injection wiring — both out of scope (advisory only; see the reference).

---

## Modes

| Mode | Purpose | Side effects |
|---|---|---|
| `audit` | Read-only: detect existing setup + the `dev-git-init` prerequisite; report gaps against the lesson checklist | None — report only |
| `scaffold` | Q&A on the 2 axes + stack → generate config + manifest + version file + workflow | Writes files; never overwrites existing ones; emits (never runs) the outward commands |
| `verify` | Dry-run `release-please release-pr --dry-run` to confirm a clean `vX.Y.Z` tag scoped to post-anchor commits + every intended `extra-files` bump (catches the silent failure) | None — read-only dry run |
| `seed` | Emit the **minimal anchor tag** command so the first fire is scoped, not full-history | None — emits the `git tag` command; operator runs it |

---

## Detecting the axes

### Axis 1 — branch mode (read from `dev-git-init`, do not re-ask)

Resolve in this order; ask the operator only if all signals are silent:

```bash
# 1. An ADR captured the branching strategy (dev-git-init's post-scaffold ADR):
grep -l -i "branching strategy\|merge mode\|integration branch" \
  docs/architecture/decisions/adr-*.md 2>/dev/null

# 2. An integration branch exists on the remote (promotion flow present):
git branch -a 2>/dev/null | grep -Ei 'origin/(develop|staging|integration|preprod|pre-prod)'

# 3. CONTRIBUTING.md documents the strategy (dev-git-init writes this):
grep -Ei 'trunk-based|gitlab flow|gitflow|integration branch|promote' CONTRIBUTING.md 2>/dev/null
```

- Integration branch found (signal 2) or an ADR/CONTRIBUTING naming a promotion flow → **integration-branch-targeted**; the branch from signal 2 is the `target-branch`.
- Only `main`, no promotion flow → **main-targeted** (`target-branch: main`).
- No signal at all → ask: *"Does this repo promote through an integration branch (feature → <integration> → main), or deploy straight from main?"* Do not invent an integration branch that does not exist.

### Axis 2 — version source (detect stack, then ask app-vs-library)

```bash
# Stack detection (narrows the candidate release-type):
[ -f package.json ]   && echo "node"
[ -f pyproject.toml ] && echo "python"
[ -f Cargo.toml ]     && echo "rust"
[ -f go.mod ]         && echo "go"
```

Then ask the one question the file layout cannot answer: **"Is this a deployed application (not published to a package registry), or a published library/package?"**

- **Deployed app** → `release-type: simple`; `version.txt` is the truth; language manifests **frozen** and excluded from `extra-files` (lesson 8). A UI manifest whose lockfile tolerates a lagging root version *may* be tracked.
- **Published package** → `release-type: node`/`python`/`rust`/… per the stack; the manifest IS the identity; `version.txt` is N/A.

---

## Mode: `audit` (read-only)

### Step 1 — the prerequisite check (first, always)

The release changelog is only as clean as the commit subjects that land. On a squash-merge repo that means the **PR title** (lesson 5) — guarded by `dev-git-init`'s PR-title lint + the `squash_merge_commit_title = PR_TITLE` setting.

```bash
# dev-git-init's hygiene layer present?
[ -f .github/workflows/pr-title-lint.yml ] && echo "✅ PR-title lint present" || echo "⬜ PR-title lint MISSING"
gh api repos/{owner}/{repo} --jq '.squash_merge_commit_title' 2>/dev/null   # want: PR_TITLE
```

**Detect + offer, not a hard block.** If the layer is missing (and the repo squash-merges), the report's first finding is: *"Workstream A hygiene layer absent — run `dev-git-init` (audit then scaffold) first so the landed PR titles release-please parses are lint-guarded. Want me to invoke it?"* On a merge-commit repo (every branch commit is linted) the PR-title layer is N/A — note it and continue.

### Step 2 — detect existing release setup

```bash
for f in \
  release-please-config.json \
  .release-please-manifest.json \
  version.txt \
  .github/workflows/release-please.yml; do
  [ -e "$f" ] && echo "✅ $f" || echo "⬜ $f"
done

# Lesson guardrails on an existing config:
if [ -f release-please-config.json ]; then
  grep -q '"include-component-in-tag": *false' release-please-config.json \
    && echo "✅ include-component-in-tag:false (lesson 1)" \
    || echo "⚠ include-component-in-tag NOT false — giant-changelog risk (lesson 1)"
fi

# Anchor tag exists and matches the manifest version? (lesson 2)
git tag --list 'v*' 2>/dev/null | tail -1
```

Resolve Axis 1 + Axis 2 (§Detecting the axes) so the report states the detected branch mode + version source.

### Step 3 — report

```
## Audit — release automation

**Prerequisite (dev-git-init hygiene):** ✅ PR-title lint + PR_TITLE squash setting present
  (or: ⬜ MISSING → offer to run dev-git-init first)
**Branch mode (Axis 1):** integration-branch-targeted → target-branch: develop
**Version source (Axis 2):** deployed-app → release-type: simple, version.txt is truth

**In place (N of 4):**
- ✅ release-please-config.json  (include-component-in-tag:false ✅)
- ...

**Missing (N of 4):**
- ⬜ .github/workflows/release-please.yml
- ...

**Guardrail findings:**
- ⚠ No vX.Y.Z anchor tag — first fire will digest all history (lesson 2). Run `seed`.
- ⚠ extra-files unverified — run `verify` to catch a silent bump failure (lesson 4).

**Next action:** run `scaffold` to fill the missing slots, then `seed`, then `verify`.
```

Report slot 3 (`version.txt`) as **N/A** when Axis 2 = published-package (`in-place + missing + N/A = 4`). End audit mode.

---

## Mode: `scaffold` (interactive Q&A)

### Step 0 — resolve the axes

1. Run the **prerequisite check** (audit Step 1). If the hygiene layer is missing on a squash-merge repo, **offer** to run `dev-git-init` first — do not hard-block; the operator may proceed knowingly.
2. Resolve **Axis 1** (§Detecting the axes) — read from `dev-git-init`, ask only if silent.
3. Resolve **Axis 2** — detect the stack, ask app-vs-library.
4. Ask the **anchor version** (default `0.1.0` for a pre-1.0 app; the operator may pick the real current version).

Echo the resolved axes back before writing anything.

### Step 1 — detect existing files + capture substitutions

Run audit Step 2. Capture:
- Files that already exist (skipped silently in Step 3).
- **Repo full name:** `gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null` or parse `git remote get-url origin`.
- **Whether `squash_merge_commit_title` is already `PR_TITLE`** (drives whether the closing report emits that command — skip it if Workstream A already set it).
- **Whether a release-versioning ADR already exists:** `grep -l -i "release-please\|release versioning\|release automation" docs/architecture/decisions/adr-*.md 2>/dev/null` — if found, the post-scaffold ADR prompt is skipped.

### Step 2 — confirm scope

Echo the plan: resolved axes, the slots that will be written vs skipped, the anchor version, and the commands that will be **emitted (not run)**. Wait for `y`. Stop on `n`.

### Step 3 — write files

For each missing slot, copy the template from `templates/` and substitute placeholders. **Idempotency is uniform** — file exists → skip silently; to overwrite, the operator deletes it and re-runs.

**`release-please-config.json`** (`templates/release-please-config.json`) — substitute:
- `{{release_type}}` → `simple` (deployed-app) or `node`/`python`/`rust`/… (published-package).
- `{{extra_files}}` → the version-echo targets:
  - **deployed-app:** empty `[]` for a backend-only app (version.txt is maintained by `release-type: simple` — do NOT list it in extra-files). Add a UI manifest only if one exists and its lockfile tolerates a lagging version, e.g.
    `{ "type": "json", "path": "frontend/package.json", "jsonpath": "$.version" }`.
    **Never** list a language manifest coupled to a checked-in lockfile (lesson 8).
  - **published-package:** usually empty (the manifest is handled by `release-type`); add entries only for *additional* echoes (a version constant, a docs badge).

**`.release-please-manifest.json`** (`templates/release-please-manifest.json`) — substitute `{{anchor_version}}`.

**`version.txt`** (`templates/version.txt`) — substitute `{{anchor_version}}`. **Skip this slot entirely for published-package.**

**`.github/workflows/release-please.yml`** (`templates/release-please.yml`) — substitute `{{integration_branch}}` with the Axis-1 target branch (the integration branch, or `main` for main-targeted). If the repo policy requires SHA-pinned actions, note in the closing report that `@v4` must be pinned to a full commit SHA.

### Step 4 — post-scaffold ADR prompt

After writing, ask whether to record the release-versioning decision as an ADR (generalising the reference implementation's ADR). This invokes `arch-adr` to create `docs/architecture/decisions/adr-XXXX-release-versioning-strategy.md`, documenting **Axis 1** (why the branch mode — dissolves version divergence / artifact off-by-one / untestable first fire when a promotion flow exists) and **Axis 2** (why the version source — the 12-factor / lockfile-coupling rationale). **Skip the prompt** if Step 1 found an existing release-versioning ADR (note it instead). Recommended: yes.

### Step 5 — closing report

List scaffolded vs skipped slots, then the **emit-not-run** command block and next steps:

```
## Scaffolded
- ✅ release-please-config.json (release-type: <..>, include-component-in-tag:false)
- ✅ .release-please-manifest.json (anchor <X.Y.Z>)
- ✅ version.txt (<X.Y.Z>)            [deployed-app only]
- ✅ .github/workflows/release-please.yml (target-branch: <branch>)

## Next steps (operator runs — the skill does not execute these)

1. Commit the scaffold:
   git add release-please-config.json .release-please-manifest.json version.txt \
     .github/workflows/release-please.yml
   git commit -m "ci(release): scaffold release automation via dev-release-init"

2. Seed the anchor tag BEFORE the workflow first fires (lesson 2 — run `seed` mode or):
   git tag v<X.Y.Z> <commit-on-release-branch> && git push origin v<X.Y.Z>

3. Enable "Allow GitHub Actions to create and approve pull requests" (lesson 7 —
   release-please cannot open its PR without it; preserves the read-only default token):
   gh api -X PUT repos/<owner>/<repo>/actions/permissions/workflow \
     -f default_workflow_permissions=read -F can_approve_pull_request_reviews=true

[Only if Workstream A has not already set it:]
4. Set the squash subject to the linted PR title (lesson 5):
   gh api -X PATCH repos/<owner>/<repo> \
     -f squash_merge_commit_title=PR_TITLE -f squash_merge_commit_message=PR_BODY

5. Push the release branch → release-please opens the standing release PR.
   Run `verify` (dry-run) first to confirm the tag + extra-files bumps (lesson 4).

6. When ready to release: merge the standing release PR. It carries NO required
   checks (GITHUB_TOKEN opens it → no CI; lesson 3) so admin-merge it, as step 1 of
   a release session (see the release ritual in references/release-lessons.md).

[If a required check should gate later — arming order, lesson 6:]
7. Register any new required contexts in branch protection only AFTER they have
   reported on one PR, then re-run scripts/setup-branch-protection.sh.

[If Step 4 = yes:]
8. Record the decision as an ADR:
   arch-adr create "ADR-XXXX — Release Versioning Strategy"
   Seed with: Axis 1 = <branch mode> · Axis 2 = <version source>.
```

Also emit the **release-ritual runbook** pointer: suggest capturing the admin-merge → build → promote → deploy flow via `ops-runbook` (or a CONTRIBUTING.md section), generalised from the reference in `references/release-lessons.md` §The release ritual.

End scaffold mode.

---

## Mode: `verify` (dry-run — catches the silent `extra-files` failure)

`extra-files` fails **silently** (lesson 4): a wrong path/jsonpath simply does not bump, discovered a release too late. Run a dry run and inspect the proposed changes:

```bash
# npx (Node) or the release-please CLI; reads the scaffolded config + manifest.
npx release-please release-pr \
  --dry-run \
  --token="$(gh auth token)" \
  --repo-url="$(gh repo view --json nameWithOwner -q .nameWithOwner)" \
  --target-branch=<integration_branch> \
  --config-file=release-please-config.json \
  --manifest-file=.release-please-manifest.json
```

Confirm from the output:
1. A single clean `vX.Y.Z` tag is proposed (not `<component>-vX.Y.Z` → lesson 1 regression).
2. The version delta is scoped to **post-anchor** commits (not a full-history dump → lesson 2).
3. **Every** file you intended to bump appears in the proposed changes — including each `extra-files` target. A file missing here is the silent failure; fix its path/jsonpath in the config and re-run.

Report the three checks as pass/fail. `verify` runs no mutation — it is a dry run only.

---

## Mode: `seed` (minimal anchor tag only)

The first release-please run walks commits back to the newest recognised tag; with **zero** tags it digests all history into one meaningless mega-PR (lesson 2). `seed` emits the **minimal** anchor — one tag on the current release-branch tip, matching the seeded manifest/version:

```bash
# Emitted, never executed. Run on the release branch (integration branch or main).
git tag v{{anchor_version}}    # e.g. v0.1.0 — the version in .release-please-manifest.json
git push origin v{{anchor_version}}
```

This is **not** retro archaeology — reconstructing a full historical tag sequence is a bespoke one-time migration, out of scope forever. `seed` establishes exactly one anchor so the first real release PR is scoped to post-anchor work. End seed mode.

---

## Anti-patterns

1. **Omitting `include-component-in-tag: false`.** Without it, tags become `<component>-vX.Y.Z`, no prior tag matches, and release-please dumps the entire history into one giant first changelog (lesson 1).
2. **Firing before an anchor tag exists.** Zero tags → full-history mega-PR. Always `seed` first (lesson 2).
3. **Giving the release PR its own CI via a PAT.** The release PR carries no checks by design (`GITHUB_TOKEN` recursion guard); admin-merge it. A PAT is unjustified token surface (lesson 3).
4. **Trusting `extra-files` without a dry run.** It fails silently. `verify` is mandatory after scaffold and after any `extra-files` edit (lesson 4).
5. **Duplicating `dev-git-init`'s PR-title lint / scope enum.** This skill *detects and requires* Workstream A; it never re-scaffolds the hygiene layer and never touches commit scopes (lesson 5).
6. **Bumping a lockfile-coupled language manifest for a deployed app.** It desyncs the lockfile every release for no benefit. Freeze the manifest; keep the identity in the tag + `version.txt` (lesson 8).
7. **Running the `gh api` / `git tag` / branch-protection commands.** All are remote or history side effects — emit them, never execute (same discipline as `dev-git-init`).
8. **Registering a required check before it has reported.** GitHub rejects an unseen context; the branch-protection re-apply is a follow-up step (arming order, lesson 6).
9. **Silently overwriting an existing config/workflow.** Every file is skip-if-exists. To replace one, the operator deletes it and re-runs. No `--force`.
10. **Re-asking Axis 1.** The branch mode is `dev-git-init`'s decision — read it from the ADR / integration branch / CONTRIBUTING; ask only when every signal is silent.
11. **Scaffolding retro tags or version-injection wiring.** Both are advisory-only / out of scope; `seed` does the minimal anchor, and version injection is emitted as guidance, not code.

---

## Checklist

**Scaffold mode:**

- [ ] Prerequisite check run; missing hygiene layer → offered `dev-git-init` (not hard-blocked)
- [ ] Axis 1 resolved from `dev-git-init` (ADR / integration branch / CONTRIBUTING); asked only if silent
- [ ] Axis 2 resolved: stack detected + app-vs-library asked
- [ ] Anchor version captured
- [ ] Scope confirmed with the operator before any write
- [ ] `include-component-in-tag: false` present in the written config
- [ ] `extra-files` matches Axis 2 (no lockfile-coupled manifest for a deployed app)
- [ ] `version.txt` written iff deployed-app; skipped for published-package
- [ ] Workflow `target-branch` + `on: push` branch match Axis 1
- [ ] Emit-not-run block includes: anchor tag, Actions-can-create-PRs, squash setting (iff not already set), branch-protection follow-up
- [ ] Post-scaffold ADR prompt asked (unless an existing release-versioning ADR was found)
- [ ] Release-ritual runbook pointer emitted

**Audit mode:**

- [ ] Prerequisite (PR-title lint + `PR_TITLE`) checked first
- [ ] All 4 slots checked; slot 3 reported N/A for published-package
- [ ] Axis 1 + Axis 2 detected and stated
- [ ] Lesson guardrails checked (include-component-in-tag, anchor tag, extra-files unverified)
- [ ] in-place + missing + N/A = 4; next action given

---

## Relations to other skills

- **Depends on `dev-git-init`** (Workstream A): consumes the clean Conventional-Commit history + PR-title-lint + `squash_merge_commit_title = PR_TITLE` it guarantees. `audit`/`scaffold` **detect and require** that layer (offer to run it if absent) but never duplicate it and never touch commit scopes.
- **Feeds `com-release-note`:** produces the `CHANGELOG.md` + tags + GitHub Releases that `com-release-note` curates into a stakeholder narrative. `dev-release-init` owns the *technical* release automation; `com-release-note` owns the *communication* layer.
- **Invokes `arch-adr`** via the Step 4 post-scaffold prompt (operator runs separately): records the Axis 1 + Axis 2 decisions as a release-versioning ADR.
- **Invokes `ops-runbook`** (suggested, operator runs separately): captures the release ritual (admin-merge → build → promote → deploy) as an operator runbook, or a CONTRIBUTING.md section.
- **Independent of `dev-git-commit`, `dev-pr`, `dev-git-worktree`, `agent-ralph-loop`** — they operate alongside the release pipeline without depending on its scaffolding state.
- **Detected by the `metamodel` skill's Audit mode** indirectly — the optional ADR (if created via Step 4) is checked for frontmatter validity and ID conventions.

## Follow-up work

Open items about this skill's own evolution go to the kit's central ledger (`docs/project-control/open-items/`) per the `metamodel` skill's `references/open-items-governance.md`, never in a local section here.

## See also

- [`references/release-lessons.md`](references/release-lessons.md) — the two axes, the eight lessons, the release ritual, out-of-scope guidance
- `templates/release-please-config.json` · `templates/release-please-manifest.json` · `templates/version.txt` · `templates/release-please.yml` — the generated file bodies
- `dev-git-init` — the prerequisite commit/PR/merge hygiene contract (Workstream A)
- `com-release-note` — the downstream stakeholder-narrative curator
