---
type: Architecture Documentation
title: "{{project_name}} — Solution Strategy (arc42 §4)"
description: "{{One-sentence summary of this arc42 section}}"
tags: []
timestamp: "{{YYYY-MM-DDThh:mm:ssZ}}"
status: draft
owner: {{owner}}
last_reviewed: {{today}}
review_interval: 180d
---

# 4. Solution Strategy

> "A short summary of the fundamental decisions and solution strategies, that shape system architecture." — arc42 §4

This section is a navigation aid. One-line summaries link to ADRs and quality attributes; full rationale lives in those artefacts.

## 4.1 Technology Decisions

| Decision | Summary | ADR ref |
|---|---|---|
| _TODO_ | _TODO_ | ADR-NNNN |

(One row per key technology choice — language, framework, database, messaging system, cloud provider. Keep the summary to one sentence; the ADR has the detail.)

## 4.2 Top-Level Decomposition

_TODO_ — one paragraph describing how the system is decomposed at the highest level: microservices / modular monolith / serverless / hybrid, and the rationale. Reference the bounded context map (`docs/domain/02b-bounded-contexts.md`) and the building block view (`docs/architecture/arc42/05-building-blocks.md`) if they exist.

## 4.3 Quality Goal → Architectural Tactic Mapping

| Quality goal | QA-XXNN | Architectural tactic | ADR ref |
|---|---|---|---|
| _TODO_ | _TODO_ | _TODO_ | ADR-NNNN |

(One row per top-priority quality attribute. Tactic = the architectural mechanism that delivers the quality goal, e.g. "stateless containers + HPA", "hexagonal architecture + domain isolation", "circuit breaker + retry with exponential backoff".)

## 4.4 Key Organizational Decisions

_TODO_ — brief notes on organizational decisions with architectural impact: development process, outsourcing, open-source vs buy, cross-team ownership. Keep to bullet points; no more than 5.

## Cross-references

| Linked artefact | Relationship |
|---|---|
| [`docs/architecture/decisions/`](../decisions/) | Full rationale for each technology decision listed above |
| [`docs/product-specs/09a-quality-attributes.md`](../../product-specs/09a-quality-attributes.md) | Quality attributes (`QA-XXNN`) whose tactics are mapped in §4.3 |
| [`docs/domain/02b-bounded-contexts.md`](../../domain/02b-bounded-contexts.md) | Decomposition basis — BC-NN boundaries that drove the service split |
| [`docs/architecture/arc42/02-constraints.md`](./02-constraints.md) | Constraints that narrowed the solution space |
| [`docs/architecture/arc42/05-building-blocks.md`](./05-building-blocks.md) | Detailed structural realisation of the decomposition described above |

## Open Items

| OI-ID | Type | Summary | Source anchor | Source heading | Resolution path | Priority | Status | Owner | Due / Review date | Tracker ref |
| :---- | :--- | :------ | :------------ | :------------- | :-------------- | :------- | :----- | :---- | :---------------- | :---------- |

_None at present._
