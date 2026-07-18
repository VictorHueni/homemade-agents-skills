# PR-title lint + squash-title + capability scope-enum — enforcement guidance

Loaded on demand by `dev-git-init` when the branching strategy squash-merges and/or a capability map / FBS is present. This is the mechanical enforcement backstop under the authoring convention in `rules/git-and-tools.md` §"Commit & PR scope vocabulary" — that rule is the source of truth for *why* a scope names a capability and never a work-item number. Do **not** restate it here; this file covers only the *how*.

## Why PR-title lint is not optional on a squash-merge repo

A squash-merge collapses a branch to a single commit whose **subject is the PR title**. The local `commit-msg` hook (commitlint / commitizen) only ever sees the *branch* commits — never the squash subject. So on a squash-merge repo the PR title is the one commit that actually lands on the default branch, and it is completely unguarded unless a CI check lints it. It is also exactly what a release-automation tool parses and what the changelog groups by. Hence: when Q2 squash-merges (trunk-based + squash, or GitLab-Flow squash-to-main), the PR-title lint is a **required** check, not a nicety.

The old SKILL deferral ("commitlint on commits + reviewer's checklist covers the PR title at MVP") is false for squash-merge and is removed.

## One vocabulary, both surfaces — per stack

The PR-title check reuses the **same** config as the local commit-msg hook so there is a single type/scope vocabulary and zero drift. Never introduce a second type list (this is why `amannn/action-semantic-pull-request` is rejected — it is a parallel type-list to hand-sync):

| Stack | commit-msg hook | PR-title lint reuses |
|---|---|---|
| Node | `commitlint --edit` (reads `commitlint.config.js`) | `echo "$PR_TITLE" \| npx --no -- commitlint` — same config file, incl. `scope-enum` |
| Python | commitizen `commit-msg` hook (reads `pyproject.toml [tool.commitizen]`) | `cz check --message "$PR_TITLE"` — same config |

**Injection hardening (zizmor):** the PR title is attacker-influenced. Always pass it through an `env:` binding (`PR_TITLE: ${{ github.event.pull_request.title }}`) and reference `"$PR_TITLE"` in `run:` — never interpolate `${{ github.event.pull_request.title }}` directly inside a `run:` block.

## Arming order (the 0137 lesson)

A status check cannot be registered as **required** in branch protection until it has **reported at least once** on a real PR. GitHub rejects a required-check context it has never seen. Therefore:

1. Merge the scaffold (workflow files land on the default branch).
2. Open one PR → the `PR Title Lint` (and drift-gate) checks run and report.
3. *Then* run `scripts/setup-branch-protection.sh` to add the now-known contexts to `required_status_checks`.

Do not assume the branch-protection script can register the check on first apply — emit it as a **follow-up** step and document this order. The stable job name (`name: PR Title Lint`) is the context string branch protection matches on; keep it stable.

## `squash_merge_commit_title = PR_TITLE` (merge-strategy setting)

Without this repo setting a **multi-commit** PR squashes using GitHub's default title (the first commit's subject or "PR-title (#N)"), which the PR-title lint never validated — defeating the whole point. Set it so the squash subject is exactly the linted PR title. Emitted, never executed (same emit-not-run discipline as branch protection):

```bash
gh api -X PATCH repos/{owner}/{repo} \
  -f squash_merge_commit_title=PR_TITLE \
  -f squash_merge_commit_message=PR_BODY
```

Only relevant when Q2 squash-merges. It is a sibling of branch protection — a remote side effect with no undo risk but real behavioural consequence, so the operator runs it deliberately.

## Capability scope-enum — generate → check → drift-gate

Three pieces, all owned here because `dev-git-init` owns both surfaces the enum is checked on (the commit-msg hook and the PR-title lint).

### Generate

`scripts/gen-commit-scopes.py` (pure stdlib, read-only) reads the capability map (`docs/business/03a-capability-map.md`) and FBS (`docs/product-specs/07a-fbs.md`) and derives the allowlist. **Scope altitude is the capability, not the product:** every capability maps to one product in the FBS, so a capability scope encodes Product → Capability (the subject line then carries the functionality) — the full hierarchy — whereas a product-only scope would skip the capability floor. Product slugs are emitted too (for genuinely cross-capability product work), and the fixed buckets `platform, infra, ci, deps, chore` are appended. Output is a byte-stable `.commit-scopes.json`:

```json
{ "scopes": ["billing", "checkout", "search", "platform", "infra", "ci", "deps", "chore"], "sources": ["docs/business/03a-capability-map.md"] }
```

Slug derivation: kebab-case of the name, connective stopwords dropped, a leading product-family word common to every product name stripped (so "Acme Billing" → `billing`).

**Short capability slugs — the `scope:` alias.** A verbose capability name would produce an unusable slug (`prior-authorization-clinical-decision-support`, 45 chars). Declare a short alias *in that capability's block* in the capability map and the generator emits the alias instead:

```
### C6.1 · Prior Authorization / Clinical Decision Support
scope: prior-auth
```

→ emits `prior-auth`. This is **author-once and drift-gated** — the alias lives in the capability map (the source of truth), never in the emitted JSON. When a capability has no alias and its slug exceeds ~20 chars, the generator prints a stderr **warning** suggesting one; the enum is still written (a long slug is usable, just awkward to type), so the warning is a nudge, not a failure. The optional per-capability `scope:` field is a `business-capability-map` convention — see that skill for where it lives in a capability block.

### Check

- **Node:** `commitlint.config.js` gains `'scope-enum': [2, 'always', require('./.commit-scopes.json').scopes]`. This enforces the allowlist natively on **both** the commit-msg hook and the PR-title lint (both run commitlint). `feat(billing): …` ✅ · `feat(0121): …` ❌ (not in enum).
- **Python:** commitizen's `cz_conventional_commits` does not enforce a scope allowlist, so the PR-title-lint workflow adds a small **advisory** scope step (pure `python3`, reads `.commit-scopes.json`) after the blocking format check. It warns (does not fail) when the title's scope is outside the enum.
- **`cross-cutting` label override:** a PR labelled `cross-cutting` bypasses the scope check (not the format check) — for the legitimate multi-capability PR that no single scope describes. The label is the escape hatch that keeps the check advisory-friendly.

### Drift-gate

`.github/workflows/scope-enum-drift.yml` re-runs the generator in CI and diffs against the committed `.commit-scopes.json`; it fails when the capability map / FBS changed without a regen — the same pattern as an `openapi.bundled.yaml` or `requirements.lock` drift-gate. Fix on failure: run `python3 scripts/gen-commit-scopes.py --out .commit-scopes.json` and commit.

### Advisory-first posture

Start advisory (nudge + `cross-cutting` override); harden to blocking only if work-item numbers keep leaking into scopes. On Node the native `scope-enum` is already blocking on the commit-msg hook — if that proves too strict early on, downgrade the rule level from `2` (error) to `1` (warning) in `commitlint.config.js` until the vocabulary settles. Never try to enforce that a scope is "meaningful" — only "in the allowlist" is mechanically enforceable.

## Graceful degradation — no capability map / FBS

When neither `docs/business/03a-capability-map.md` nor `docs/product-specs/07a-fbs.md` exists, the generator exits 2 and writes nothing. In that case `dev-git-init`:

- does **not** create `.commit-scopes.json`, the drift-gate workflow, or the commitlint `scope-enum` line;
- still scaffolds `pr-title-lint.yml` (format check only) when Q2 squash-merges;
- documents in `CONTRIBUTING.md` that scopes are free **area/module** names inferred from changed paths (`auth`, `api`, `infra`, `deps`) — the sensible default for a repo with no capability map.

Re-run `dev-git-init` (or just the generator) later once a capability map exists to add the enum.
