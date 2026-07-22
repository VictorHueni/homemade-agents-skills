---
type: rule
---

# Git & tool-use discipline

## Never `git commit --amend`

Always create a new commit. Amending rewrites a hash you may have already recorded elsewhere (progress logs, PR descriptions, follow-up commits) and creates self-inconsistent history.

If a pre-commit hook fails, the commit did NOT happen — the previous commit is unchanged. Fix the issue, re-stage, and create a NEW commit. Do not `--amend` to "fold the fix in."

Exception: only if the user explicitly asks for `--amend` in the same conversation.

## Commit & PR scope vocabulary — capability, not work-item number

The scope in a Conventional Commit (`type(scope): …`) and in a squash-merged **PR title** should name **what the change advances in product terms**, drawn from the project's own vocabulary — never an internal work-item / plan number.

**Resolution order (first match wins):**

1. **Declared scope** — if the plan or task being executed declares a `Commit scope:` (e.g. in an implementation plan's Delivery Rules), use it verbatim.
2. **Capability / product vocabulary** — else, if the project has a capability map or FBS, use a **product slug** (`P-NN` → e.g. `billing`) or **capability slug** (`C-N.M` → e.g. `search`). These read as plain language in the changelog and let a stakeholder release note (`com-release-note`) attribute the change to a capability near-mechanically.
3. **Area / module** — else infer from the changed files (`auth`, `api`, `infra`, `deps`) — the sensible default for repos with no capability map.

**Never put a bare work-item / plan number in the scope** (`feat(0121): …`). It is opaque to a non-technical reader, un-attributable to a capability without a lookup, and pollutes the automated changelog. Keep the plan / increment reference in a **`Refs:` trailer** instead:

```text
feat(billing): word-level diff on plan terms

Refs: Plan-0042 increment 03
```

**Why it matters (the whole chain):** a squash-merge uses the PR title as the commit subject, so the PR-title scope is what the automated changelog groups by — and what the curated release note is built from. A capability scope makes both legible; a work-item number makes both opaque. This is why `agent-ralph-loop`, `dev-git-commit`, `dev-pr`, and `plan-implementation` all resolve the scope the same way. Mechanical enforcement (a generated scope-enum + PR-title gate) is tracked separately; **this rule is the authoring convention every skill follows.**

## `Edit` tool: `replace_all=True` matches the whole `old_string`, not the inner substring

`replace_all=True` replaces every literal occurrence of the exact `old_string` you provided. If `old_string` is multi-line or contains surrounding context, occurrences of the inner substring with *different* surroundings will silently survive.

After any wide-pattern `replace_all`, follow up with:

```bash
git grep -n "<inner_string>" <dir>/
```

If grep still finds the string, those are the occurrences where the wider pattern did not match. Run targeted single-occurrence Edits for them. The grep takes 5 seconds; skipping it means the next test discovers the miss for you with a less helpful error.

**Heuristic for `old_string` width:**

- **Narrow `old_string`** (just the inner substring) + grep follow-up → safer default. Risk: over-replacement if the inner string is non-unique.
- **Wide `old_string`** (with surrounding context) → only when disambiguation is required. Risk: silent misses when surrounding context varies.

Anti-pattern: assuming a multi-line `replace_all` Edit "got everything" without verification.
