---
type: Use Case
title: "UC-06 — Execute a delegated issue"
description: "A coding agent takes a ready-for-agent issue through gate, claim, implement, verify, and pull request, closing it with structural evidence."
tags: [open-items, agent-execution, delegation, github-backend]
timestamp: "2026-07-20T15:00:00Z"
status: draft
owner: "Victor Hueni"
last_reviewed: "2026-07-20"
review_interval: 180d
---

# UC-06 — Execute a delegated issue

> Methodology: see the kit's `spec-use-case/references/methodology.md` (Cockburn fully-dressed format). Do not restate the method here.

| Field | Value |
|---|---|
| **Scope** | system — the backlog-execution system (github open-items backend + `agent-issue-loop` / `util-open-items`) |
| **Level** | user-goal 🌊 |
| **Primary Actor** | Coding Agent (LLM-driven session, e.g. Claude Code) |
| **Supporting Actors** | GitHub (issue tracker + PR API); the Operator as reviewer |
| **Realises** | _TBD_ (no FBS for the kit; contract lives in `agent-issue-loop/SKILL.md` Family C) |

## Stakeholders and Interests

- **Operator** — no unreviewed or unverified change reaches the mainline; the review
  workload stays proportionate (small, evidenced PRs, not slop floods).
- **Future maintainers** — every closed issue carries structural evidence (the merged
  change) explaining *why* it closed.
- **Other agents / future sessions** — the tracker state always reflects reality, so the
  delegation queue and `state:` labels can be trusted blindly.

## Preconditions

- The repo runs the `github` open-items backend (labels bootstrapped, ADR-0009 vocabulary).
- The issue exists and the agent can read/write the tracker and the repository.
- The repo documents its verification commands (build/test/lint) in `CLAUDE.md`.

## Guarantees

- **Minimal guarantees** (hold even on failure): no change reaches the mainline without
  review; the issue's labels reflect its true state at all times (in-progress, blocked,
  or readiness restored); no issue is closed without evidence; any finding produced
  before stopping is recorded on the issue, not lost.
- **Success guarantees**: the issue is closed by a **merged, reviewed change** that
  satisfies the issue's own acceptance criteria; the verification commands pass; the
  `state:` label is cleared; nothing outside the issue's scope was modified.

## Trigger

The Operator directs the agent at a specific issue ("take #N"), or the self-selection
use case (UC-07) picks it, or — variation — a tracker automation assigns/mentions the
agent on the issue.

## Main Success Scenario

1. The Coding Agent receives the goal of resolving issue #N.
2. The agent assesses the issue's readiness (**include UC-11**) and confirms it is
   labelled `ready-for-agent`.
3. The agent claims the issue: it replaces the readiness label with `state:in-progress`
   and records itself as the worker.
4. The agent studies every location named in the issue's References, honours the
   Out-of-scope boundary, and restates the acceptance criteria as its definition of done.
5. The agent implements the smallest coherent change that satisfies the criteria, on an
   isolated line of work (its own branch).
6. The agent verifies the change: the issue's own verification command(s) and the repo's
   standard verification commands all pass.
7. The agent submits the change for review, citing the acceptance-criteria checklist as
   evidence and linking the submission so that acceptance closes the issue (`Closes #N`).
8. The Operator reviews and merges; the tracker closes the issue with the merged change
   as evidence, and the `state:` label is removed.

## Extensions

- **2a.** The issue is not labelled `ready-for-agent` (it is `needs-triage` or
  `needs-human`):
  - **2a1.** The agent refuses, citing the missing precondition and pointing at the
    route to fix it (a triage session, or `validate` with its drafted brief).
  - **2a2.** Use case ends; minimal guarantees hold (nothing was touched).
- **2b.** The issue is labelled `ready-for-agent` but fails the readiness assessment
  (drift — e.g. criteria were edited away):
  - **2b1.** The agent refuses as in 2a and additionally proposes demotion to
    `needs-triage`, citing the failed criterion.
- **3a.** The tracker is unreachable or the claim cannot be recorded:
  - **3a1.** The agent stops before touching any code and reports the outage.
- **4a.** A referenced location no longer exists (file moved/renamed):
  - **4a1.** The agent attempts to re-resolve it from the codebase.
  - **4a2.** If ambiguous, it records the discrepancy on the issue, restores
    `needs-triage`, and stops.
- **4b.** Fulfilling the criteria would require crossing the Out-of-scope boundary:
  - **4b1.** The agent stops implementing, records the conflict on the issue, applies
    `needs-human`, and reports.
- **5a.** The work turns out larger than the issue's size bound (not one coherent PR):
  - **5a1.** The agent stops, records a proposed split on the issue, restores the
    readiness label, and suggests filing the split via the filing contract (UC-03).
- **5b.** The agent discovers adjacent work mid-implementation (an unrelated bug, a
  refactor opportunity):
  - **5b1.** It files a separate issue via the filing contract (duplicate/dependency
    search included) and continues — it never silently absorbs scope.
- **6a.** Verification fails and cannot be brought to pass within the criteria:
  - **6a1.** The agent reverts to a safe state, records the findings and failing output
    on the issue, restores the readiness label, and reports.
- **6b.** The criteria themselves prove wrong or unverifiable (e.g. the check cannot run
  in any available environment):
  - **6b1.** The agent records why, proposes corrected criteria, applies `needs-human`,
    and stops without opening a PR.
- **7a.** An equivalent change is already in review (duplicate work detected late):
  - **7a1.** The agent links the existing review on the issue, abandons its branch, and
    restores the issue to its pre-claim state.
- **8a.** The Operator's review requests changes:
  - **8a1.** The agent iterates on the same branch, re-verifies (step 6), and resubmits;
    repeat until merged or abandoned.
- **8b.** An external dependency blocks completion (a decision, a third-party fix):
  - **8b1.** The agent replaces `state:in-progress` with `state:blocked`, records the
    blocker on the issue, and stops. Resumption re-enters at step 4.

## Technology and Data Variations

- Step 1: the goal may arrive via direct instruction, queue self-selection (UC-07), or
  tracker automation (`@claude` mention / assignment) — the behaviour from step 2 on is
  identical regardless of trigger channel.
- Step 7: "submission for review" is a pull request on GitHub; on other hosts the
  equivalent merge-request primitive.

## Related Information

- Contract: `agent-issue-loop/SKILL.md` Family C; label semantics:
  `util-open-items/references/github-backend.md` §2b; readiness precondition: kit
  ADR-0008 §3; evidence-gated closure: governance §3.
- The one-issue-per-invocation action budget and the never-self-promote rule are the
  system's defenses against review-flood and queue corruption (research 0001 §3.5).

## Use-Case 2.0 Slices

| Slice | Narrative | Test case(s) | Status |
|---|---|---|---|
| UC-06.S1 | Basic flow: ready issue → merged PR closes it | Plan-0003 increment M5 gate: one real `take → PR` round-trip | ⬜ |
| UC-06.S2 | Refusal path (2a/2b): non-ready issue is refused with cited precondition | `take` on a `needs-human` issue refuses | ⬜ |
| UC-06.S3 | Failure discipline (6a): failing verification restores the queue state | Simulated failing check → label restored + findings comment | ⬜ |
| UC-06.S4 | Blocked handover (8b): blocker recorded, `state:blocked` applied | Simulated blocked take | ⬜ |
