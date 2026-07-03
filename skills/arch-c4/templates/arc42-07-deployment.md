---
type: Architecture Documentation
title: "{{project_name}} — Deployment View (arc42 §7)"
description: "{{One-sentence summary of this arc42 section}}"
tags: []
timestamp: "{{YYYY-MM-DDThh:mm:ssZ}}"
status: draft
owner: {{owner}}
last_reviewed: {{today}}
review_interval: 180d
---

# 7. Deployment View

> "The deployment view describes the technical infrastructure used to execute your system, with infrastructure elements like geographical locations, environments, computers, processors, channels and net topologies … and the mapping of (software) building blocks to those infrastructure elements." — arc42 §7

Each environment (Production / Staging / Development / …) is documented as its own subsection — environments differ in instance counts, node sizes, and regions, so a single combined view would obscure the differences.

## 7.1 Infrastructure overview

_(Narrative — owned by `arch-arc42`.)_ _TODO_ — one paragraph naming each environment documented below and the primary infrastructure approach (e.g. "Single-cloud AWS with EKS for application containers, RDS for managed Postgres, MSK for Kafka. Production is multi-AZ within eu-west-1; Staging is single-AZ.").

Each appended §7.x environment block carries a generated block — the deployment diagram + the building-block→infrastructure mapping table — fenced by `<!-- arch-c4:start key=deployment-<env> -->` … `<!-- arch-c4:end key=deployment-<env> -->`. The Motivation and Quality/Performance narrative sit OUTSIDE the markers and are owned by `arch-arc42`. See ADR-0004.

<!-- §7.x environment subsections appended below by `arch-c4 deployment <env>` runs -->

_No environments documented yet. Run `arch-c4 deployment production` to document the primary environment._

## Cross-references

| Linked artefact | Relationship |
|---|---|
| [`docs/architecture/decisions/`](../decisions/) | Infrastructure ADRs (hosting choice, runtime platform, database provisioning, region strategy) — referenced in Motivation paragraphs below |
| [`docs/architecture/arc42/05-building-blocks.md`](./05-building-blocks.md) | The containers (`CON-NN`) deployed below |
| [`docs/product-specs/09a-quality-attributes.md`](../../product-specs/09a-quality-attributes.md) | Quality requirements (`QA-XXNN`) — the Quality/Performance Features subsection here explains *how* the deployment achieves them |
| [`docs/ops/runbooks/`](../../ops/runbooks/) | Operational procedures that depend on this deployment structure |
