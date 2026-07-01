---
type: Architecture Documentation
title: "{{project_name}} — Architecture Constraints (arc42 §2)"
description: "{{One-sentence summary of this arc42 section}}"
tags: []
timestamp: "{{YYYY-MM-DDThh:mm:ssZ}}"
status: draft
owner: {{owner}}
last_reviewed: {{today}}
review_interval: 180d
---

# 2. Architecture Constraints

> "Any requirement that constrains software architects in their freedom of design and implementation decisions." — arc42 §2

These constraints are non-negotiable within the current project scope. Each row cites its source so the rationale is auditable. Hard constraints cannot be traded off; soft constraints are marked `negotiable` and may be revisited in future ADR deliberations.

## 2.1 Technical Constraints

| ID | Constraint | Source | Negotiable? | ADR ref |
|---|---|---|---|---|
| CST-01 | _TODO_ | _TODO_ | no | _TBD_ |

(One row per technical mandate — mandated languages, frameworks, platforms, tools, APIs. Source = contract, org policy, or existing ADR number.)

## 2.2 Organizational Constraints

| ID | Constraint | Source | Negotiable? | ADR ref |
|---|---|---|---|---|
| CST-XX | _TODO_ | _TODO_ | no | _TBD_ |

(One row per organizational constraint — team size limits, timeline, budget, vendor, DPA requirement, partner SLA.)

## 2.3 Legal and Regulatory Constraints

| ID | Constraint | Regulation / Standard | Negotiable? | ADR ref |
|---|---|---|---|---|
| CST-XX | _TODO_ | _TODO_ | no | _TBD_ |

(One row per legal / regulatory constraint — GDPR, PCI DSS, HIPAA, SOC 2, etc. Cite the specific article or control where possible.)

## Cross-references

| Linked artefact | Relationship |
|---|---|
| [`docs/architecture/decisions/`](../decisions/) | ADRs that record the architectural response to each constraint |
| [`docs/product-specs/09a-quality-attributes.md`](../../product-specs/09a-quality-attributes.md) | Quality targets derived from regulatory constraints (QA-XXNN) |
| [`docs/architecture/arc42/04-solution-strategy.md`](./04-solution-strategy.md) | How constraints shaped the solution strategy |

## Open Items

| OI-ID | Type | Summary | Source anchor | Source heading | Resolution path | Priority | Status | Owner | Due / Review date | Tracker ref |
| :---- | :--- | :------ | :------------ | :------------- | :-------------- | :------- | :----- | :---- | :---------------- | :---------- |

_None at present._
