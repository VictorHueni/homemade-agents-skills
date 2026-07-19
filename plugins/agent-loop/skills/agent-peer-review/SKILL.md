---
name: agent-peer-review
description: "Critically review PRDs and implementation plans to identify gaps, blind spots, contradictions, and delivery risks before coding begins. Use when asked to review product docs, technical specs, implementation plans, migration/deletion plans, acceptance criteria, or rollout strategy; produce ranked findings by severity (critical, major, normal, low) with concrete remediation and exact document updates."
version: "1.1.0"
status: active
last_reviewed: 2026-07-04
review_interval: 180d
user-invocable: true
allow_implicit_invocation: true
impact: "low"
metadata:
  category: "agent"
  complexity: "high"
---

# Peer Reviewer

## Objective

Deliver a high-signal peer review for planning artifacts before implementation starts.
Prioritize defects and execution risks, not writing style.

## Inputs

Provide:

1. Target document path(s) to review.
2. Optional related references (code, schema, migration files, linked docs).
3. Optional review focus (for example: data contracts, testability, rollout risk).

## Workflow

1. Read the target doc end-to-end and build a requirement map:

   - goals, non-goals, acceptance criteria, dependencies, constraints, open questions.

2. Cross-check internal consistency:

   - detect contradictions between goals, acceptance criteria, and technical approach.

3. Validate feasibility against implementation reality:

   - compare required behavior with existing CLI, contracts, DB schema, and test patterns.

4. Run risk lenses:

   - scope boundaries, backward compatibility, data integrity, observability, testability, delivery sequencing, migration/deletion safety.

5. Produce findings ranked by severity with concrete remediation and PRD/plan update instructions.

## Severity Rubric

Use exactly these labels:

1. `critical`: Release-blocking contradiction or missing requirement that can cause wrong behavior, data loss/corruption, severe security/compliance risk, or invalid scope.
2. `major`: High-impact gap likely to cause rework, failed delivery, or materially incorrect/ambiguous implementation.
3. `normal`: Important clarity/testability/operability issue that should be fixed for reliable execution but is not release-blocking.
4. `low`: Improvement for precision, maintainability, or readability with limited delivery risk.

## Review Lenses

Use all lenses, then emphasize the highest-risk areas:

1. Problem framing: Is the problem measurable and tied to user/business outcomes?
2. Scope boundaries: Are non-goals explicit and enforceable?
3. Requirements quality: Are acceptance criteria verifiable, unambiguous, and complete?
4. Data/contracts: Are schemas, stage identities, keys, and invariants defined correctly?
5. Failure behavior: Are error handling, edge cases, and exit semantics explicit?
6. Compatibility/migration: Are deletion and replacement plans gated and reversible?
7. Testing strategy: Are test gates realistic, sufficient, and aligned to risk?
8. Operational readiness: Are observability, metrics, and rollout safeguards specified?
9. Sequencing: Is implementation order coherent and dependency-safe?

## Output Format

A peer review is a **working record, not a spine `docs/` artefact** — the `agent-*` family mints no IDs and writes no catalogued `docs/` documents (it orchestrates *how the agent builds*, not *what the product is*). So the review does **not** carry the OKF artefact-frontmatter block: no registered `type`, no `review_interval`, no the `metamodel` skill's `references/artefact-types-registry.yaml` lookup. Registering a `peer_review` type would miscategorise a transient review as a first-class artefact and force it into the audit's spine.

Default output location: `var/reports/<feature>/` (a feature-named subfolder, per the skill-output convention) — e.g. `var/reports/<feature>/<target-slug>-peer-review.md`. This path is outside `docs/`, so the `metamodel` skill's Audit mode never sweeps it, which is correct: a review is regenerable and not part of the knowledge graph.

Open with a **light plain-markdown header** (no YAML frontmatter block): an H1 title, then a one-line metadata line — target reviewed (path), date, reviewer (`git config user.name`), and the one-line verdict.

If the caller explicitly wants the review colocated with the artefact it reviews (e.g. next to a plan under `docs/exec-plans/`), honour that placement but keep the same light header — it stays a record, never a catalogued doc.

Produce findings first, sorted by severity descending. Include:

1. `Severity`
2. `Issue`
3. `Evidence` with file path and line reference
4. `Recommendation`
5. `How to update PRD/plan` with section-level patch guidance

Then include:

1. `Open questions/assumptions` (only if unresolved decisions remain)
2. `Optional short summary` (after findings)

If no findings exist, state that explicitly and list residual risks or testing gaps.

## PRD Update Guidance Pattern

For each finding, propose document edits that are directly actionable:

1. section to modify (for example: "US-003 Acceptance Criteria")
2. exact change type (`add`, `replace`, `clarify`, `defer`, `gate`)
3. specific text direction (what requirement to add/change and why)

## Implementation Plan Add-On

When reviewing implementation plans, additionally verify:

1. each increment is atomic and independently testable
2. each increment has a deterministic test gate
3. dependency ordering is explicit
4. rollback/remediation paths exist for risky increments
5. file ownership and touch-points are scoped to reduce regression risk

## Ralph Loop Readiness

When reviewing plans intended for autonomous execution via `agent-ralph-loop`, additionally verify:

1. Every increment has a `**Status:** pending` field.
2. The plan header includes `**Overall Status:**` and `**Current Increment:**` fields.
3. The milestone table includes a `Status` column.
4. Test gates contain executable commands (not prose descriptions).
5. The corresponding PRD has `- [ ]` checkboxes on all acceptance criteria.
6. The PRD has `**Status:**` fields on each user story.
7. Increments are ordered so that each can be implemented independently of later ones.

If any of these are missing, flag as `major` severity — the plan cannot be executed autonomously without them.

Do not implement code in this skill; review and planning quality is the deliverable.
