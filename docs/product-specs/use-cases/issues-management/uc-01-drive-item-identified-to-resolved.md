---
type: Use Case
title: "UC-01 — Drive an item from identified to resolved"
description: "The summary-level map: how one unit of unresolved work travels from identification through filing, triage, and execution to an evidenced closure — the kite under which the other use cases sit."
tags: [open-items, lifecycle, summary, github-backend]
timestamp: "2026-07-20T15:30:00Z"
status: draft
owner: "Victor Hueni"
last_reviewed: "2026-07-20"
review_interval: 180d
---

# UC-01 — Drive an item from identified to resolved

> Casual format (Cockburn). Promote to fully-dressed without re-numbering when the goal earns it. Methodology: kit `spec-use-case/references/methodology.md`.

| **Scope** | system | **Level** | summary ☁ | **Primary Actor** | Operator | **Realises** | _TBD_ (lifecycle normative in `docs/project-control/open-items/README.md` §readiness state machine) |
|---|---|---|---|---|---|---|---|

**Main scenario.** A unit of unresolved work is identified — by the Operator noticing
it, or by an agent mid-task — and enters the tracker: the Operator files it through
the per-type forms (UC-02) or an agent files it through the sync contract (UC-03);
either way it arrives classified (type, priority, size) and awaiting triage. A triage
pass (UC-04) then gives it exactly one deliberate disposition: promoted to the
delegation queue with a complete brief (`ready-for-agent`), routed to a human
decision (`needs-human`), or dropped as stale with a recorded rationale. Queued items
get executed — the Operator delegates one directly, or an agent self-selects the next
(UC-07) — and the execution (UC-06) carries the item through claim, implementation,
and verification to a reviewed, merged change that closes it with structural
evidence. Between sessions, the Operator periodically re-verifies that the queue's
guarantee still holds (UC-08). When it succeeds, the item is closed with evidence of
why, the tracker state matches reality at every intermediate step, and nothing was
ever deleted without a trace — the full state machine is drawn in
`docs/project-control/open-items/README.md`.

**Alternate paths.**

- Triage routes the item to `needs-human` → it waits on a human decision; once
  decided, it re-enters triage for promotion or is dropped deliberately.
- The item shows no movement for the staleness window (default 90 days) → triage
  proposes dropping it, closed as not planned with the rationale recorded —
  item-by-item bankruptcy, never a bulk purge.
- The item turns out to duplicate an existing one → the deduplication flow (UC-05)
  merges its context onto the canonical issue and closes it as "Duplicate of #N".
- Queue verification (UC-08) finds the item's brief has drifted → it is demoted back
  to `needs-triage`, citing the failed criterion, and re-enters triage.
- Execution blocks on an external dependency → the item carries `state:blocked` with
  the blocker recorded, and resumes when the dependency clears.
- The item pre-dates the tracker (a legacy list) → it enters via the conversion flow
  (UC-10) instead of fresh filing — or is deliberately left behind there.
