---
type: Use Case
title: "UC-04 — Triage the backlog"
description: "The operator, assisted by an agent, converts untriaged issues into a trustworthy queue: promotions with complete briefs, human-routing, and deliberate staleness drops — every disposition operator-approved."
tags: [open-items, triage, readiness, github-backend]
timestamp: "2026-07-20T15:00:00Z"
status: draft
owner: "Victor Hueni"
last_reviewed: "2026-07-20"
review_interval: 180d
---

# UC-04 — Triage the backlog

> Methodology: see the kit's `spec-use-case/references/methodology.md` (Cockburn fully-dressed format). Do not restate the method here.

| Field | Value |
|---|---|
| **Scope** | system — the backlog-execution system (github open-items backend + `util-open-items` triage v2) |
| **Level** | user-goal 🌊 |
| **Primary Actor** | Operator (the human maintainer — triage authority) |
| **Supporting Actors** | Coding Agent (analysis assistant); GitHub (issue tracker) |
| **Realises** | _TBD_ (contract lives in `util-open-items/SKILL.md` Mode 2) |

## Stakeholders and Interests

- **Operator** — a backlog they can trust: every `ready-for-agent` item is genuinely
  delegable, stale items don't silently rot, and no mutation happens behind their back.
- **Coding Agents** — a delegation queue whose guarantee holds, so `take`/`next` never
  need human judgment to decide whether an item is safe.
- **Future maintainers** — dropped items carry a recorded rationale, never silent
  deletion.

## Preconditions

- The repo runs the `github` backend with the ADR-0009 label vocabulary bootstrapped.
- At least the readiness axis is in use (`needs-triage` applied at creation).

## Guarantees

- **Minimal guarantees** (hold even if the session is abandoned): no label change and no
  closure has been applied without the Operator's explicit approval; every applied
  closure carries a rationale and evidence; the tracker is never left half-mutated
  without a report of what was and wasn't applied.
- **Success guarantees**: every open issue carries exactly one deliberate readiness
  disposition (`ready-for-agent` with a complete brief, `needs-human`, or a recorded
  keep-reason); stale items are resolved deliberately (dropped with rationale or
  consciously kept); the delegation queue passes the readiness precondition end-to-end.

## Trigger

The Operator requests a triage pass — on cadence, after a batch of filings, or when the
audit/queue-verification flags drift.

## Main Success Scenario

1. The Operator requests triage of the backlog.
2. The system gathers every open issue awaiting triage (plus, on request, the whole open
   set) and clusters related and potentially duplicate items.
3. For each item, the system assesses readiness (**include UC-11**) and, for near-misses,
   drafts the missing brief (proposed acceptance criteria + references) from the issue
   text and the codebase.
4. The system proposes one disposition per item — promote to `ready-for-agent` (brief
   complete), route to `needs-human`, keep as `needs-triage` with a stated reason, or
   drop as stale (no movement past the staleness window, default 90 days) — presented as
   a disposition table with per-item rationale.
5. The Operator reviews the table: amends dispositions, rejects some, accepts the rest.
6. The Operator approves the amended table.
7. The system applies exactly the approved dispositions: readiness label changes, drafted
   briefs written into promoted issues, priority corrections, and stale drops closed
   with their rationale recorded.
8. The system reports the resulting queue state: counts per axis, delegation-queue
   depth, and anything it could not apply.

## Extensions

- **2a.** Nothing awaits triage:
  - **2a1.** The system reports the clean state and the current queue depth; use case
    ends successfully.
- **2b.** A duplicate cluster is found:
  - **2b1.** The system flags the pair(s) for the deduplication flow (UC-05) instead of
    proposing a readiness disposition for the duplicates; triage of the canonical item
    proceeds normally.
- **3a.** An item is malformed (priority/size unreadable from labels or body):
  - **3a1.** The system proposes a default (`priority:p2`) plus an explicit flag so the
    Operator confirms or corrects it in step 5.
- **3b.** An item's brief cannot be drafted (the goal itself is unclear):
  - **3b1.** The system proposes `needs-human` with the open questions listed on the
    issue.
- **4a.** An item hit the staleness window but shows signs of continued relevance
  (recent references from other issues/PRs):
  - **4a1.** The system proposes *keep* with the evidence, not drop; the staleness clock
    restarts from the operator's decision, which is recorded on the issue.
- **5a.** The Operator rejects a proposed promotion:
  - **5a1.** The item stays `needs-triage`; the rejection reason is recorded so the next
    pass does not re-propose it unchanged.
- **5b.** The Operator amends a drafted brief:
  - **5b1.** The amended brief is what gets written in step 7 — the system never
    overwrites operator text with its own.
- **7a.** Applying a disposition fails (the issue changed since the proposal — new
  labels, closed meanwhile):
  - **7a1.** The system skips that item, completes the rest, and lists the skipped items
    in the step-8 report with a re-run suggestion.
- **7b.** A drop's closure cannot record its rationale (write failure):
  - **7b1.** The item is left open and reported — an unevidenced closure is never
    performed.

## Technology and Data Variations

- Step 2: "awaiting triage" is the `needs-triage` label query; the full-set variant adds
  `ready-for-agent` drift checking (overlaps UC-08, which runs it standalone).
- Step 7: label changes and closures go through the tracker API (`gh`); drops use the
  close-as-not-planned primitive so evidence is structural.

## Related Information

- Contract: `util-open-items/SKILL.md` Mode 2 (triage v2); readiness precondition:
  kit ADR-0008 §3; staleness policy rationale (item-by-item bankruptcy beats bulk
  purges): research 0001 §3.4.
- Cadence guidance: short and regular (10–15 min) beats rare and heroic; the disposition
  table is the whole interface — the Operator never needs to open each issue.

## Use-Case 2.0 Slices

| Slice | Narrative | Test case(s) | Status |
|---|---|---|---|
| UC-04.S1 | Basic flow: untriaged set → approved dispositions applied | Plan-0003 increment 11 (kit-repo triage session) | ⬜ |
| UC-04.S2 | Near-miss promotion with drafted brief (3, 5b) | One issue promoted with an operator-amended brief | ⬜ |
| UC-04.S3 | Staleness drop with rationale (4, 7) | One stale item closed `not planned` + rationale comment | ⬜ |
| UC-04.S4 | Conflict safety (7a): changed issue is skipped and reported | Simulated mid-session issue edit | ⬜ |
