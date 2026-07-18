---
name: plan-implementation
description: "Create a small-step, testable implementation roadmap from a PRD or feature request. Use when asked to create an implementation plan, write a roadmap, or plan this feature following the project's atomic increment standard."
version: "1.0.0"
status: active
last_reviewed: 2026-05-22
review_interval: 180d
user-invocable: true
allow_implicit_invocation: true
impact: "low"
metadata:
  category: "planning"
  complexity: "high"
---

# Implementation Planner

This skill guides you through creating a high-quality, structured implementation plan based on the project's standard for atomic increments and test-gated milestones.

## Workflow

1. **Deconstruct Requirement:** Read the PRD or feature request. Identify the core architectural components and the order of operations.
2. **Define Summary:** State the purpose, reference the source PRD, and list the guiding principles (e.g., isolation, small steps, test gates).
3. **Draft Increments:** Break the implementation into small, coherent increments. Each increment MUST be a standalone changeset with a test gate.
4. **Define Delivery Rules:** Include project-wide constraints (e.g., "one increment per commit", "no live API keys"), and **declare the `Commit scope:`** — resolve it from the source PRD's product/capability (`P-NN` → product slug, `C-N.M` → capability slug) so the ralph loop and `dev-git-commit` emit a capability scope, not the plan number. See [Commit & PR scope vocabulary](../../rules/git-and-tools.md).
5. **Group into Milestones:** Create a table grouping increments into logical, standalone delivery chunks.
6. **Save the Plan:** Save the completed plan to `docs/plans/active/{NNNN}_exec_{slug}.md`. The `{NNNN}` MUST match the ID of the corresponding PRD.

## Output

- **Format:** Markdown (`.md`)
- **Location:** `docs/plans/active/`
- **Filename:** `{NNNN}_exec_{slug}.md` (e.g., 0001_exec_onboard-agent.md)
- Open every generated file with the standard artefact frontmatter (OKF-superset block — set `type` to this artefact's `okf_type` display name from `rules/artefact-types-registry.md`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`). Run `git config user.name` for `owner`. Set `status: draft` on initial scaffold. Default `review_interval: 30d`. Full schema: `rules/artefact-frontmatter.md`.
- When a PRD exists for this plan, add a `prd:` field to the frontmatter: `prd: docs/product-specs/prds/prd-NNNN-{feature}.md`. This is the machine-readable link used by `agent-ralph-loop` to locate the PRD at its canonical location without requiring a workspace copy. Omit the field if the plan has no associated PRD.

## Implementation Plan Template

Use the following Markdown structure exactly:

```markdown
# Implementation Plan: [Feature Name]

## Summary

[High-level context and reference to the PRD]

Principles:

1. One increment equals one coherent change set.
2. Every increment has an explicit test gate.
3. [Project-specific principle]

**Overall Status:** pending
**Current Increment:** --

## Increment Plan

### Increment XX: [Descriptive Title]

**Status:** pending

Scope:

1. [Actionable item]
2. [Actionable item]

Primary files:

1. [File path]
2. [File path]

Test gate:

1. [Command to verify success]

Exit criteria:

1. [Outcome 1]
2. [Outcome 2]

[Repeat for each increment...]

## Delivery Rules

1. One increment per commit.
2. **Commit scope:** `[capability/product slug]` — the scope every increment's commit uses, derived from the PRD's product/capability (`P-NN` → product slug, or `C-N.M` → capability slug). The ralph loop and `dev-git-commit` read this; the plan + increment ref goes in a `Refs: Plan-NNNN increment XX` trailer, **never** the scope. See [Commit & PR scope vocabulary](../../rules/git-and-tools.md).
3. Each increment must be independently runnable and reversible.
4. [Other standard rules...]

## Milestone Chunks (Standalone Delivery Groups)

| Milestone      | Increments    | Status  | Coherent Outcome | Standalone Test Gate   | Exit Criteria      | Commit Guidance |
| :------------- | :------------ | :------ | :--------------- | :--------------------- | :----------------- | :-------------- |
| [M-ID]: [Name] | [Start]-[End] | pending | [Description]    | [Verification command] | [Success criteria] | [Commit style]  |
```

## Guiding Principles for Planning

- **Atomic Changes:** An increment should be small enough to review easily but large enough to provide value or a foundation.
- **Test-Driven Gates:** Every increment must have a `Test gate`. If no logic is added, use a `smoke test` or `import test`.
- **Deterministic Outcomes:** Exit criteria must be objective and verifiable.
- **Sequential Flow:** Order increments to minimize rework and respect dependencies.
- **Ralph Loop Ready:** Status fields on every increment and milestone enable autonomous execution via the `agent-ralph-loop` skill. Use `**Status:** pending | in-progress | done` to track progress.

## File Open Items to the central ledger

Implementation plans frequently carry actionable unresolved work surfaced while
breaking the PRD down into increments — deferred decisions an ADR must close,
doc-gaps to fill before a specific increment can start, follow-up execution
items that should not block the plan but must not be lost, tech-debt items
explicitly deferred. File each directly to the central ledger via
`util-open-items` — there is no local section to author first
([ADR-0005](https://github.com/VictorHueni/homemade-claude-kit/blob/main/docs/architecture/decisions/adr-0005-open-items-ledger-sole-authoring-surface.md)).
Cite the plan as `Source artefact` with `Source anchor` + `Source heading`
pointing back to the originating increment — e.g. `#increment-03` +
"Increment 03: Normalize Existing Artefact Templates" (per
[`rules/open-items-governance.md`](https://github.com/VictorHueni/homemade-claude-kit/blob/main/rules/open-items-governance.md)).

- **File nothing when there's nothing to file.** A plan whose unresolved work
  is fully captured by the increment list itself needs no filing at all.
  Scaffold `_TODO_` placeholders inside an increment scope or test gate are
  NOT open items and MUST NOT be filed to the ledger.
- **File as state changes.** When the Ralph Loop or a manual editor closes,
  reassigns, or discovers new unresolved work, use `util-open-items` (`close`
  / `drop` / `sync`) so the ledger reflects the current plan state.

Invoke as: "File the open item for `docs/plans/active/[NNNN]_exec_[feature-name].md`
increment `<NN>` via the util-open-items skill."
