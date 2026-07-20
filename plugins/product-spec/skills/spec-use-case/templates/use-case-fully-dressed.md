---
type: Use Case
title: "UC-{{NN}} — {{Use case goal as a short verb phrase}}"
description: "{{One-sentence summary of the actor goal this use case satisfies}}"
tags: []
timestamp: "{{YYYY-MM-DDThh:mm:ssZ}}"
status: draft
owner: "{{git config user.name}}"
last_reviewed: "{{YYYY-MM-DD}}"
review_interval: 180d
---

# UC-{{NN}} — {{Use case goal as a short verb phrase}}

> Methodology: see the kit's [`spec-use-case/references/methodology.md`](../../../) (Cockburn fully-dressed format). Do not restate the method here.

| Field | Value |
|---|---|
| **Scope** | {{enterprise \| system \| subsystem}} — {{what "the system" is here}} |
| **Level** | {{user-goal 🌊 \| summary ☁🪁 \| subfunction 🐟🦪}} |
| **Primary Actor** | {{P-NN persona, or actor role}} |
| **Supporting Actors** | {{external systems/services the system calls — or "none"}} |
| **Realises** | {{FBS functionality IDs e.g. C-N.M.F03 — or _TBD_}} |

## Stakeholders and Interests

- **{{Stakeholder}}** — {{the interest the system must protect}}
- **{{Stakeholder}}** — {{interest}}

## Preconditions

- {{What must be true before this use case can start}}

## Guarantees

- **Minimal guarantees** (hold even on failure): {{e.g. no state change without an audit record}}
- **Success guarantees** (hold when the goal is achieved): {{e.g. the order is recorded and the actor is notified}}

## Trigger

{{What starts the use case.}}

## Main Success Scenario

1. {{Actor}} {{verb}} {{object}}.
2. The system {{verb}} {{object}}.
3. {{… 3–9 steps, active voice, alternating actor / system, who-has-the-ball always clear …}}
4. The system {{records the result / notifies the actor}}.

## Extensions

_For each main step, capture every condition that diverges from success. Label `<step><letter>`; start with the condition, then the handling steps._

- **1a.** {{Condition at step 1}}:
  - **1a1.** {{Handling step}}
- **2a.** {{Condition at step 2}}:
  - **2a1.** {{Handling step}}
  - **2a2.** {{… resume at step N, or fail with minimal guarantee …}}

## Technology and Data Variations

- {{Step N}}: {{variations in how the data arrives or the channel used — optional}}

## Related Information

- {{Frequency, performance notes, links to PRD-NNNN, domain events, value-stream stage VS-N.M — optional}}

## Use-Case 2.0 Slices

_Populated by the `slice` mode. The basic flow is the first slice; each alternative flow becomes a further slice. Every slice needs a test case._

| Slice | Narrative | Test case(s) | Status |
|---|---|---|---|
| UC-{{NN}}.S1 | Basic flow (main success scenario) | {{test ref}} | ⬜ |
