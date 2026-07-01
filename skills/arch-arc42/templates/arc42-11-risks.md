---
type: Architecture Documentation
title: "{{project_name}} — Risks and Technical Debt (arc42 §11)"
description: "{{One-sentence summary of this arc42 section}}"
tags: []
timestamp: "{{YYYY-MM-DDThh:mm:ssZ}}"
status: draft
owner: {{owner}}
last_reviewed: {{today}}
review_interval: 90d
---

# 11. Risks and Technical Debt

> "A list of identified technical risks or technical debts, ordered by priority. Risk management is project management for grown-ups." — arc42 §11 / Tim Lister

Architectural-scope risks and deliberate technical shortcuts that require an architect's attention. Ordered by severity descending. Operational risks (infrastructure failure, DR) belong in ops runbooks.

## 11.1 Active Risks

| ID | Type | Summary | Probability | Impact | Severity | Mitigation | Contingency | Status | Owner | ADR / QA ref |
|---|---|---|---|---|---|---|---|---|---|---|
| RSK-01 | `architectural` | _TODO_ | medium | high | high | _TODO_ | _TODO_ | open | _TBD_ | _TBD_ |

**Type values:** `architectural` · `technical-debt` · `dependency` · `security`  
**Probability / Impact:** `low` · `medium` · `high` · `critical`  
**Severity:** derived — see `references/arc42-section-11.md` for the scoring rule  
**Status:** `open` · `mitigated` · `materialised` · `closed` · `accepted`

### RSK-01 — [Risk title]

**Summary:** _TODO_

**Mitigation:** _TODO_ (what reduces the probability or impact of the risk)

**Contingency:** _TODO_ (what we do if the risk materialises — rollback plan, incident runbook pointer, etc.)

**Acceptance rationale:** _(only if status = `accepted`)_ _TODO_

---

## 11.2 Technical Debt

Technical debt items are `technical-debt` risks where the shortcut is deliberate and the remediation path is known but not yet scheduled.

| ID | Summary | Affected area | Severity | Remediation path | Due / target | Status |
|---|---|---|---|---|---|---|
| RSK-XX | _TODO_ | _TODO_ | medium | _TODO_ | _TBD_ | open |

---

## 11.3 Closed / Accepted Risks

Risks that have been resolved (status = `closed`) or deliberately accepted (status = `accepted`) are moved here after one review cycle.

_None yet._

---

## Cross-references

| Linked artefact | Relationship |
|---|---|
| [`docs/architecture/decisions/`](../decisions/) | ADRs that introduced or mitigated risks |
| [`docs/product-specs/09a-quality-attributes.md`](../../product-specs/09a-quality-attributes.md) | Low-confidence `QA-XXNN` items that may signal architectural risk |
| [`docs/architecture/arc42/08-cross-cutting-concepts.md`](./08-cross-cutting-concepts.md) | Incomplete CC-NN concepts often surface as active risks |
| [`docs/ops/runbooks/`](../../ops/runbooks/) | Operational risks and DR procedures (out of scope for §11) |

## Open Items

| OI-ID | Type | Summary | Source anchor | Source heading | Resolution path | Priority | Status | Owner | Due / Review date | Tracker ref |
| :---- | :--- | :------ | :------------ | :------------- | :-------------- | :------- | :----- | :---- | :---------------- | :---------- |

_None at present._
