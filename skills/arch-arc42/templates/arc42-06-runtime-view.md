---
type: Architecture Documentation
title: "{{project_name}} — Runtime View (arc42 §6)"
description: "{{One-sentence summary of this arc42 section}}"
tags: []
timestamp: "{{YYYY-MM-DDThh:mm:ssZ}}"
status: draft
owner: {{owner}}
last_reviewed: {{today}}
review_interval: 180d
---

# 6. Runtime View

> "The runtime view describes the concrete behavior and interactions of the system's building blocks in form of scenarios." — arc42 §6

Each scenario below shows how the system's building blocks collaborate to fulfil a specific use case. The **prose and the scenario identity (`SCN-NN`) are owned by `arch-arc42`**; the figure is *pulled* from a generator via the declared-dependency comment (see ADR-0004). For the static structure, see [§5 Building Block View](./05-building-blocks.md). For aggregate-internal state machines, see [`docs/domain/07b-models/`](../../domain/07b-models/).

**Figure source — pick per the §6 boundary rule:**

- **C4 dynamic view** (`arch-c4 runtime`, rendered to `../c4/views/`) — for cross-container flows tied to the C4 model.
- **UML sequence** (`arch-uml sequence`, rendered to `../diagrams/views/`) — for intra-component / algorithmic detail richer than the C4 model carries (`alt`/`par`/`loop`).

---

<!-- One §6.x block per scenario. Authored via `arch-arc42 runtime` mode. -->

## 6.1 {{scenario_title}} (`SCN-01`)

**Motivation:** _TODO_ — one sentence explaining why this scenario is architecturally significant (e.g. "Shows the end-to-end claim submission flow, highlighting the async handoff to the insurer integration service").

**Participants:** _TODO_ — list `CON-NN` containers (and any `P-NN` actors or external `SYS-NN`) involved.

<!-- arch-figure scenario=SCN-01 realises=UC-NN source=arch-c4 path=../c4/views/runtime-SCN-01-{{scenario_slug}}.svg -->
<!-- UML alternative: source=arch-uml path=../diagrams/views/seq-NN-{{scenario_slug}}.svg -->
![{{scenario_slug}}](../c4/views/runtime-SCN-01-{{scenario_slug}}.svg)

### Step table

| Step | From | To | Message / action | Notes |
|---|---|---|---|---|
| 1 | _TODO_ | _TODO_ | _TODO_ | _TODO_ |

(One row per annotated step in the Structurizr dynamic view. Numbering must match the DSL `"step"` property values.)

### Error / alternative flows

_TODO_ — describe what happens when step N fails. Skip if error handling is trivial (caller receives HTTP 5xx, retries handled by client). Document when the error path involves a saga rollback, compensating transaction, dead-letter queue, or circuit breaker.

---

## Cross-references

| Linked artefact | Relationship |
|---|---|
| [`docs/architecture/arc42/05-building-blocks.md`](./05-building-blocks.md) | Static structure of the `CON-NN` containers appearing in scenarios |
| [`docs/architecture/c4/views/`](../c4/views/) | C4 **dynamic** view SVGs (`arch-c4 runtime`) — figure source for cross-container scenarios |
| [`docs/architecture/diagrams/views/`](../diagrams/views/) | UML **sequence** SVGs (`arch-uml sequence`) — figure source for intra-component / algorithmic detail |
| [`docs/domain/07b-models/`](../../domain/07b-models/) | Aggregate lifecycle state machines — do NOT duplicate here |
| [`docs/architecture/arc42/07-deployment.md`](./07-deployment.md) | Where the containers here actually run |
| [`docs/business/04-value-streams.md`](../../business/04-value-streams.md) | Value stream stages that motivated the scenario selection |
| [`docs/architecture/decisions/`](../decisions/) | ADRs governing async patterns, retry policies, saga patterns visible in scenarios |

## Open Items

| OI-ID | Type | Summary | Source anchor | Source heading | Resolution path | Priority | Status | Owner | Due / Review date | Tracker ref |
| :---- | :--- | :------ | :------------ | :------------- | :-------------- | :------- | :----- | :---- | :---------------- | :---------- |

_None at present._
