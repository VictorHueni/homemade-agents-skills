# Release automation — the two axes, the eight lessons, and the release ritual

Loaded on demand by `dev-release-init`. This is the *why* behind every file the skill generates and every check it runs. The skill scaffolds a [release-please](https://github.com/googleapis/release-please) pipeline; the tool is deliberately named tool-neutrally because the axes and lessons below survive a swap to any conventional-commit release automator.

The skill **consumes** the clean commit/PR history that `dev-git-init` guarantees (Conventional Commits on every landed subject) and **produces** the automated technical changelog + tags that `com-release-note` later curates into a stakeholder narrative:

```
dev-git-init      → commit/PR/merge contract        (the clean history)
dev-release-init  → release automation (THIS)        (SemVer + CHANGELOG + tags)
com-release-note  → stakeholder narrative            (curates the changelog)
```

---

## Axis 1 — Branch mode (read from dev-git-init, do not re-ask)

Where release-please runs and what its `target-branch` is depends entirely on the project's branching strategy — the decision `dev-git-init` already captured. Detect it (see SKILL §Detecting Axis 1); ask only if no signal exists.

| Branch mode | When | Config | Promotion |
|---|---|---|---|
| **integration-branch-targeted** | The repo has a promotion flow: `feature → <integration> → main` (e.g. an integration branch such as `develop` or a pre-prod branch), with build-once promotion (the artifact is built from the integration branch and promoted, never rebuilt for main). | `on: push: branches: [<integration>]`, action `target-branch: <integration>` | Release commits (version bump, CHANGELOG, tag) flow to `main` through the normal promotion — no back-merge, no divergence. |
| **main-targeted** | Simple GitHub flow: `feature → main`, deploy from `main`. | `on: push: branches: [main]`, action `target-branch: main` | None — `main` is the release branch. |

**Why integration-branch-targeting beats main-targeting when a promotion flow exists** (generalise into the post-scaffold ADR): with build-once promotion the production artifact is built *before* any main-side release could be cut, so a version bump committed to `main` can never be inside the shipped image — main-targeted versioning is structurally always one release behind in the artifact. Targeting the integration branch dissolves three defects at once:

1. **Version divergence** — version files + `CHANGELOG.md` would otherwise go stale on the integration branch (bumps land only on main, and there is no main→integration back-flow).
2. **Artifact off-by-one** — the promoted image's baked-in version is permanently one release behind (built pre-release).
3. **Untestable first fire** — `main`-only triggers (`schedule:`, `workflow_run`, dispatch registration) arm only at the next promotion; a push-triggered integration-branch workflow runs from the pushed ref immediately.

For a repo with **no** promotion flow, main-targeting is correct and simpler — do not impose an integration branch that does not exist.

---

## Axis 2 — Version-source strategy (12-factor; detect stack + ask app-vs-library)

What *is* the release identity? This sets `release-type` and, critically, `extra-files` — which fails **silently** when wrong (lesson 4).

| Version source | When | `release-type` | `extra-files` / manifests |
|---|---|---|---|
| **deployed-app-not-published** | The project is a deployed application, not a published package. Its release identity is the **git tag + GitHub Release + `version.txt`**, not any language manifest. | `simple` (maintains `version.txt`) | Language manifests are **frozen** and excluded from `extra-files` (see lesson 8). Optionally track a UI manifest (`package.json` `$.version`) that tolerates a lagging lockfile — but never a manifest coupled to a checked-in lockfile. |
| **published-package** | The project is a library/package published to a registry (npm, PyPI, crates.io, …). The **manifest version IS the release identity**. | `node` / `python` / `rust` / … per the ecosystem | The manifest is the source of truth; release-type reads and writes it directly. Add `extra-files` only for *additional* places the version is echoed (a constant, a docs badge). |

**Detecting the stack:** presence of `package.json` (node), `pyproject.toml` (python), `Cargo.toml` (rust), `go.mod` (go), etc. The stack narrows the *candidate* `release-type`; the **app-vs-library question** decides between `simple` (deployed app) and the ecosystem type (published package). Always ask — the file layout alone cannot tell a deployed Node service from a published npm library.

---

## The eight hard-won lessons (each becomes a guardrail or an audit check)

### 1. `include-component-in-tag: false` is mandatory

Without it, release-please tags as `<component>-vX.Y.Z` and, finding no prior tag in the bare `vX.Y.Z` form, falls back to walking the **entire** commit history into one giant first-release changelog. Set it `false` for a single-package repo so tags are plain `vX.Y.Z`. **Audit check:** config present, key present, value exactly `false`.

### 2. An anchor tag must exist before the first fire

release-please walks commits back to the most recent tag it recognises. With **zero** tags the first run digests all history into a meaningless mega-PR. `seed` mode creates the *minimal* anchor: one `vX.Y.Z` tag on the current tip (matching the seeded manifest/version), so the first real release PR is scoped to post-anchor commits only. **Audit check:** at least one `vX.Y.Z` tag exists and matches the manifest version. (Retro version archaeology — reconstructing many historical tags — is explicitly out of scope; `seed` does the anchor only.)

### 3. The release PR gets no CI → admin-merge, documented

release-please opens the release PR with the default `GITHUB_TOKEN`. GitHub does not trigger workflow runs from `GITHUB_TOKEN` pushes (a deliberate recursion guard), so the release PR receives **no required-status-check runs** and cannot satisfy branch protection the normal way. It is **admin-merged**, exactly like a promotion PR. This is safe by construction: every underlying change was gate-validated when its own feature PR merged. Do **not** "fix" this with a PAT to give the PR its own CI — that is unjustified token surface. **Guardrail:** the workflow uses `GITHUB_TOKEN` (never a PAT); the release-ritual runbook documents admin-merge as step 1.

### 4. `extra-files` fails silently → the `verify` dry-run is mandatory

A wrong `extra-files` path or `jsonpath` does not error — release-please simply does not bump that file, and you discover it a release later. `verify` mode runs `release-please release-pr --dry-run` and inspects the proposed changes to confirm (a) a clean `vX.Y.Z` tag scoped to post-anchor commits, and (b) every intended version file appears in the bump set. Run it after scaffold and after any `extra-files` edit.

### 5. Squash-merge uses the PR title → depends on dev-git-init's PR-title lint

On a squash-merge repo the landed commit subject is the **PR title**, which the local commit-msg hook never sees. release-please parses that landed subject and builds the changelog from it. So the PR title must be lint-guarded — which is `dev-git-init`'s PR-title-lint check + the `squash_merge_commit_title = PR_TITLE` setting (Workstream A). `dev-release-init` **detects and requires** this hygiene layer; it never duplicates it. **Audit first-check:** is the PR-title lint workflow + `PR_TITLE` squash setting present? If not → offer to run `dev-git-init` (detect + offer, not a hard block).

### 6. Arming order — the PR-title check must report before branch protection can require it

(Inherited from `dev-git-init`.) A status check cannot be registered as **required** until it has reported at least once on a real PR; GitHub rejects an unseen context. So the branch-protection re-apply that adds the release-relevant contexts is a **follow-up** step, emitted after the first PR reports — never assumed to register on first apply.

### 7. "Allow GitHub Actions to create and approve pull requests" must be enabled

release-please cannot open its standing release PR unless this repo setting is on. With it off, the action builds the release branch + commit and then fails with *"GitHub Actions is not permitted to create or approve pull requests."* — no PR. **Emit** (never run) the command, and keep the read-only default token policy intact (this toggle is orthogonal to `default_workflow_permissions`):

```bash
# Enable Actions-can-create-PRs while preserving the read-only default token policy.
gh api -X PUT repos/{owner}/{repo}/actions/permissions/workflow \
  -f default_workflow_permissions=read \
  -F can_approve_pull_request_reviews=true
```

If the setting later resets, re-run the failed release-please workflow after re-enabling — the release branch it already created is reused.

### 8. Lockfile coupling → freeze language manifests for deployed apps

Bumping a language manifest that a checked-in lockfile records the project's own version into (e.g. a Python `pyproject.toml` whose version is mirrored in a resolver lockfile) **desyncs the lockfile on every release** and fails a lock-file-sync gate — for zero benefit on a non-published app. So for the **deployed-app** strategy (axis 2): keep the release identity in the git tag + `version.txt`, exclude the lockfile-coupled manifest from `extra-files`, and freeze it at a placeholder version. A UI manifest whose lockfile tolerates a lagging root version *may* still be tracked. Dynamic versioning (deriving the manifest version from git at build time) is rejected for the same reason — it makes the lockfile record a churning `dev+g<sha>` version.

---

## The release ritual (generalise into a runbook / CONTRIBUTING section)

The merge of the release PR is **step 1 of a release session**, never a standalone act — a merged-but-unpromoted release PR leaves tags/GitHub Releases ahead of what is deployed. For a promotion-flow (integration-branch-targeted) repo:

1. **Merge the standing release PR** (admin-merge — it carries no required checks; lesson 3). This finalises `CHANGELOG.md`, bumps the version source(s), tags `vX.Y.Z`, publishes the GitHub Release, and — being an integration-branch push — triggers the build of the release artifact.
2. **Wait for the integration-branch build + any post-merge validation to go green.**
3. **Promote** integration → `main` (the version files + changelog flow along with it — no back-merge).
4. **Deploy** by promoting the already-built, already-tagged artifact (build-once — no rebuild).

For a main-targeted repo, steps 3–4 collapse: merging the release PR on `main` cuts the release and the deploy runs from `main`.

**Discipline contract:** treat "merge release PR" as the opening move of a promotion session so tags never sit ahead of production for long.

---

## Out of scope (advisory only — emit guidance, do not scaffold)

- **Retro version archaeology** — reconstructing a full historical tag sequence is a bespoke one-time migration per repo. `seed` does the minimal anchor only.
- **Observability version injection** — surfacing the running version in the app (a health endpoint field, a UI footer, a build-arg baked into the image). Emit the guidance — *inject the version at build time from the tag / `version.txt` (12-factor Factor III: config in the environment), do not compile it into a committed manifest* — but do not scaffold app-specific wiring.
