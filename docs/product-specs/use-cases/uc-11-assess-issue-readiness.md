---
type: Use Case
title: "UC-11 — Assess an issue's readiness"
description: "The reused readiness check: one issue is assessed against the four-part delegation precondition, yielding pass with an extracted verification command or fail with exact gaps and a drafted brief."
tags: [open-items, readiness, validation, github-backend]
timestamp: "2026-07-20T15:30:00Z"
status: draft
owner: "Victor Hueni"
last_reviewed: "2026-07-20"
review_interval: 180d
---

# UC-11 — Assess an issue's readiness

> Methodology: see the kit's `spec-use-case/references/methodology.md` (Cockburn fully-dressed format). Do not restate the method here.

| Field | Value |
|---|---|
| **Scope** | system — the backlog-execution system (github open-items backend + `agent-issue-loop` Family A) |
| **Level** | subfunction 🐟 — the readiness step reused by UC-04 (triage), UC-06 (execute gate), and UC-08 (queue verification); its standalone face is `agent-issue-loop validate` |
| **Primary Actor** | (reused step) — the including use case's actor: a Coding Agent or a triage/verification session |
| **Supporting Actors** | GitHub (issue tracker); the repository (reference resolution) |
| **Realises** | _TBD_ (contract lives in `agent-issue-loop/SKILL.md` Family A; precondition normative in kit ADR-0008 §3) |

## Stakeholders and Interests

- **Coding Agents** — `ready-for-agent` is a guarantee, not a mood: a passing
  assessment means the issue can be taken without human judgment.
- **Operator** — failures name the exact gap, and near-misses arrive with a drafted
  brief, so fixing an issue is one approval away, not a research task.

## Preconditions

- The issue exists and its title, body, and labels are readable; the repository named
  by its references is readable.

## Guarantees

- **Minimal guarantees**: the assessment never mutates anything — no label change, no
  comment, no edit; drafting a brief is analysis, not mutation.
- **Success guarantees**: the caller receives an unambiguous verdict — **pass** with
  the verification command extracted, or **fail** with the exact failed criteria and,
  for near-misses, a drafted brief ready to apply.

## Trigger

An including use case reaches its readiness step (UC-04 step 3, UC-06 step 2, UC-08
per queue item), or an operator invokes the check standalone on one issue.

## Main Success Scenario

1. The caller presents one issue for assessment.
2. The system checks the four-part precondition: (i) non-empty acceptance criteria of
   observable pass/fail items ending in a runnable check; (ii) non-empty references
   that resolve to real locations in the codebase; (iii) a size label; (iv) a
   self-contained title and body that depend on no context the agent cannot reach.
3. The system extracts the verification command from the acceptance criteria.
4. The system returns **pass** to the caller, with the extracted verification command
   as the issue's definition of done.

## Extensions

- **2a.** One or more references do not resolve (file moved, symbol renamed, link
  dead):
  - **2a1.** The system returns **fail**, citing each unresolved reference; where the
    codebase suggests an obvious new location, the drafted brief proposes the
    corrected pointer.
- **2b.** Acceptance criteria are present but do not end in a check the agent can run
  (aspirational prose, no command):
  - **2b1.** The system returns **fail** on criterion (i) and drafts a runnable
    verification command inferred from the issue text and the repo's verification
    conventions, as part of the brief.
- **2c.** Any other criterion fails but the goal is clear (a near-miss):
  - **2c1.** The system returns **fail** with the exact gaps and a **drafted brief** —
    proposed acceptance criteria and references inferred from the issue and the
    codebase — ready for a triage pass or the operator to apply. Applying it is never
    this subfunction's call.
- **2d.** The goal itself is unclear — no brief can honestly be drafted:
  - **2d1.** The system returns **fail** and proposes routing the issue to
    `needs-human`, listing the open questions a human must answer first.

## Technology and Data Variations

- Step 1: standalone invocation is `agent-issue-loop validate #N`; the queue-wide
  sweep (UC-08) runs the same assessment per issue over
  `is:open label:ready-for-agent`.
- Step 2: criteria and references are read from the issue's canonical body sections
  (`### Acceptance criteria`, `### References`); size from the `size:` label — no
  free-form body parsing.

## Related Information

- Contract: `agent-issue-loop/SKILL.md` Family A; the precondition is normative in
  kit ADR-0008 §3 and summarized in `docs/project-control/open-items/README.md`
  (readiness state machine).
- Action budget: read-only, proposals only — promotion and demotion belong to triage
  (UC-04) or the operator, never to the assessment itself.

## Use-Case 2.0 Slices

| Slice | Narrative | Test case(s) | Status |
|---|---|---|---|
| UC-11.S1 | Pass: all four criteria hold, verification command extracted | `validate` on a known-good issue | ⬜ |
| UC-11.S2 | Near-miss fail (2b/2c): exact gaps + drafted brief | `validate` on an issue missing a runnable check | ⬜ |
| UC-11.S3 | Unclear goal (2d): needs-human proposal with open questions | `validate` on a vague issue | ⬜ |
