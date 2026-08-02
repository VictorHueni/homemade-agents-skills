---
name: dev-pr
description: "Use this skill when asked to create a pull request (PR). It ensures all PRs follow the repository's established templates and standards. Triggers on: create PR, open PR, pull request, draft PR."
allowed-tools: Bash(git status *) Bash(git diff *) Bash(git log *) Bash(git push *) Bash(gh repo view *) Bash(gh pr create *)
version: "1.1.0"
status: active
last_reviewed: 2026-06-07
user-invocable: true
impact: "low"
---

# Pull Request Creator

This skill guides the creation of high-quality Pull Requests that adhere to the
repository's standards.

## Types (required)

Minimal 7-type Conventional Commits set — the canonical default across all projects:

| Type       | Description                         |
| ---------- | ----------------------------------- |
| `feat`     | New feature                         |
| `fix`      | Bug fix                             |
| `docs`     | Documentation only                  |
| `chore`    | Routine tasks, maintenance, deps     |
| `refactor` | Code change (no bug fix or feature) |
| `test`     | Adding or correcting tests          |
| `perf`     | Performance improvement             |

If the project's `commitlint.config.js` (or equivalent) defines a different type-enum, use that instead — read the file first and defer to it.

## Scopes (optional)

Infer the scope from the change — do not use a hardcoded list. **Prefer the project's capability / product vocabulary** (a capability-map or FBS slug) when it has one; else the changed area (`auth`, `api`, `infra`, `deps`). **Never a bare work-item / plan number** — keep any plan/increment ref in the PR body, not the title. Omit the scope if the change genuinely spans multiple areas. Because a squash-merge makes the **PR title** the commit subject the automated changelog groups by, this scope is the one that flows into the changelog and the curated release note — see [Commit & PR scope vocabulary](../../rules/git-and-tools.md).

## Summary Rules

- Use imperative present tense: "Add" not "Added"
- Capitalize first letter
- No period at the end
- No ticket IDs in the title (link issues in the PR body instead)

## Workflow

1. **Detect base branch** — read `CONTRIBUTING.md` or `.github/` conventions to find the integration branch (commonly `staging` or `main`). Fall back to `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`.

2. **Check current state**:
   ```bash
   git status
   git diff --stat
   git log origin/<base-branch>..HEAD --oneline
   ```

3. **Analyze changes** to determine type, scope, and summary.

4. **Push branch if needed**:
   ```bash
   git push -u origin HEAD
   ```

5. **Read the PR template** — check `.github/PULL_REQUEST_TEMPLATE.md` (or `.github/pull_request_template.md`). If multiple templates exist under `.github/PULL_REQUEST_TEMPLATE/`, ask the user which to use.

6. **Draft description** that strictly follows the template structure:
   - Keep every heading from the template
   - Mark checklist items `[x]` only if actually completed; leave `[ ]` otherwise
   - Fill sections with clear, concise content

7. **Create PR** — write the body to a temp file to avoid shell escaping issues:
   ```bash
   gh pr create --title "type(scope): succinct description" --body-file <temp_file> --base <base-branch>
   rm <temp_file>
   ```

## Principles

- **Compliance**: Never ignore the PR template. It exists for a reason.
- **Completeness**: Fill out all relevant sections.
- **Accuracy**: Don't check boxes for tasks you haven't done.

## Examples

```
feat(auth): Add magic-link login flow
fix(api): Resolve tenant isolation leak in schedule query
docs(adr-0012): Record staging environment strategy decision
chore(deps): Bump @supabase/ssr to 0.6
refactor(infra): Extract deploy script into reusable function
test(rls): Add smoke test for cross-tenant data isolation
perf(schedule): Cache tenant claim lookup per statement
```

Breaking change (exclamation before colon):
```
feat(api)!: Remove deprecated v1 schedule endpoints
```

## Validation

The PR title must match this pattern:
```
^(feat|fix|docs|chore|refactor|test|perf)(\([a-zA-Z0-9._-]+\))?!?: [A-Z].+[^.]$
```

Key validation rules:
- Type must be one of the 7 allowed types (or the project's commitlint type-enum if it differs)
- Scope is optional; if present, use parentheses and keep it short
- Breaking change exclamation mark goes before the colon
- Summary starts with a capital letter and has no trailing period
