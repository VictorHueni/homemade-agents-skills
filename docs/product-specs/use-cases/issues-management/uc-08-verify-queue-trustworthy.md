---
type: Use Case
title: "UC-08 — Verify the queue is trustworthy"
description: "The operator re-verifies the delegation queue between sessions: every ready-for-agent issue is re-assessed against the readiness precondition, failures become cited demotion proposals, and structural drift is reported — never silently fixed."
tags: [open-items, queue-verification, drift, github-backend]
timestamp: "2026-07-20T15:30:00Z"
status: draft
owner: "Victor Hueni"
last_reviewed: "2026-07-20"
review_interval: 180d
---

# UC-08 — Verify the queue is trustworthy

> Casual format (Cockburn). Promote to fully-dressed without re-numbering when the goal earns it. Methodology: kit `spec-use-case/references/methodology.md`.

| **Scope** | system | **Level** | user-goal 🌊 | **Primary Actor** | Operator | **Realises** | _TBD_ (contracts live in `agent-issue-loop/SKILL.md` Family A, `validate --queue`; audit checks 18h/18i in the `metamodel` skill's audit catalogue) |
|---|---|---|---|---|---|---|---|

**Main scenario.** Between working sessions — on cadence, or before delegating a
batch — the Operator checks that the delegation queue's guarantee still holds: that
every issue labelled `ready-for-agent` genuinely passes the readiness precondition.
They run the queue-wide validation (`validate --queue`), which re-assesses each
queued issue (**include UC-11**) — criteria still runnable, references still
resolving, size still set, brief still self-contained — and, complementarily or
instead, the metamodel audit's open-items structural checks (18h trustworthy queue,
18i axis exclusivity) over the whole tracker. Every failure comes back as a
**demotion proposal citing the failed criterion** — never an applied change: both
the validation and the audit are report-only. The Operator reviews the findings and
approves the demotions worth applying (dropping failed issues back to
`needs-triage`, where triage — UC-04 — will rebuild their briefs). When it succeeds,
the Operator knows the queue can be trusted blindly again: any agent's next
self-selection (UC-07) draws from verified stock.

**Alternate paths.**

- The queue is clean → the report says so with the current queue depth; nothing to
  approve, and the verification cost was minutes.
- The Operator approves some or all demotion proposals → the labels are changed only
  then, each demotion carrying its cited criterion, so the demoted issues re-enter
  triage with a diagnosis attached rather than a bare rejection.
- The audit finds an axis-exclusivity violation (two labels on one axis, or
  readiness/state leftovers on closed issues) → reported as a structural finding
  with the offending labels named; fixing it is a deliberate operator or triage
  action, since report-only tools never mutate.
- A queued issue is mid-execution (`state:in-progress` replaced its readiness
  label) → it is simply not in the queue query anymore; verification concerns only
  what is still offered for taking.
