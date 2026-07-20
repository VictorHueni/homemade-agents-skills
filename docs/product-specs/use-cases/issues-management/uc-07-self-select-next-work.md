---
type: Use Case
title: "UC-07 — Self-select the next work item"
description: "A coding agent picks its own next issue from the delegation queue by a deterministic rule — highest priority, then smallest size, then oldest — and executes it; an empty queue is reported, never worked around."
tags: [open-items, delegation-queue, self-selection, github-backend]
timestamp: "2026-07-20T15:30:00Z"
status: draft
owner: "Victor Hueni"
last_reviewed: "2026-07-20"
review_interval: 180d
---

# UC-07 — Self-select the next work item

> Casual format (Cockburn). Promote to fully-dressed without re-numbering when the goal earns it. Methodology: kit `spec-use-case/references/methodology.md`.

| **Scope** | system | **Level** | user-goal 🌊 | **Primary Actor** | Coding Agent | **Realises** | _TBD_ (contract lives in `agent-issue-loop/SKILL.md` Family C, `next`) |
|---|---|---|---|---|---|---|---|

**Main scenario.** The Coding Agent is told to work "the next ready issue" with no
specific number. It queries the delegation queue — the open issues carrying
`ready-for-agent` (`is:open label:ready-for-agent`) — and picks deterministically:
highest priority first (p0 → p3), ties broken by smallest size (S → M → L), final
ties by oldest issue. Because the queue's label is a guarantee (every queued issue
has passed the readiness precondition), the pick needs no human judgment. The agent
then executes the picked issue end-to-end (**include UC-06**): gate, claim,
implement, verify, and a review submission that closes it on merge. One invocation,
one issue — when it finishes, it reports and stops rather than chaining into a second
pick unasked. When it succeeds, the most valuable smallest ready item is in review or
merged, and the queue is one shorter.

**Alternate paths.**

- The queue is empty → the agent reports exactly that and suggests the remedies —
  a queue verification (`validate --queue`) or a triage session (UC-04) to promote
  near-misses. It **never** lowers the bar by picking from `needs-triage` or
  `needs-human`; an empty queue is information, not an obstacle.
- Several issues tie on priority, size, and age bracket → oldest wins outright; the
  rule leaves no discretionary pick, so two agents given the same queue make the
  same choice.
- The pick fails its execution gate (drift since promotion — UC-06 extension 2b) →
  the agent proposes demotion for it and may take the next pick down the same
  ordering, reporting both actions.
- The top pick is `size:L` → it is still legal to take, but the agent flags that
  splitting before delegation was the recommended route and proceeds only if the
  brief truly bounds one coherent change.
