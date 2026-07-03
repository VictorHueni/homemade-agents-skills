---
title: Example Platform — Business Capability Map
status: draft
owner: example
last_reviewed: 2026-05-29
review_interval: 90d
---

<!-- doc-version: 1.0 | created: 2026-05-29 -->

# Example Platform — Business Capability Map

Strategic "what" layer for the example platform.

---

## L0 axis declaration

**Chosen axis:** Capability domain

**Rationale:** Domains map cleanly onto the platform's value streams.

**L0 items:**

- **C1** — Customer Management
- **C2** — Service Delivery
- **C3** — Platform Operations

---

## Global overview

```
Example Platform
│
├── C1 · Customer Management
│   ├── C1.1 · Identity & Access
│   ├── C1.2 · Account Lifecycle
│   └── C1.3 · Engagement
│
├── C2 · Service Delivery
│   ├── C2.1 · Order Capture
│   ├── C2.2 · Fulfilment
│   │   ├── C2.2.1 · Scheduling
│   │   └── C2.2.2 · Dispatch
│   └── C2.3 · Quality Assurance
│
└── C3 · Platform Operations
    ├── C3.1 · Observability
    └── C3.2 · Billing
```

---

## Capability index

| ID | Name | L0 parent | Strategic Importance | One-line definition |
|---|---|---|---|---|
| C1.1 | Identity & Access | C1 · Customer Management | Necessary | Authenticate and authorise every actor. |
| C1.2 | Account Lifecycle | C1 · Customer Management | Differentiator | Onboard, maintain, and offboard accounts. |
| C1.3 | Engagement | C1 · Customer Management | Commodity | Notify and re-engage customers. |
| C2.1 | Order Capture | C2 · Service Delivery | Differentiator | Capture and validate service orders. |
| C2.2 | Fulfilment | C2 · Service Delivery | Differentiator | Schedule and execute committed work. |
| C2.3 | Quality Assurance | C2 · Service Delivery | Necessary | Verify delivered work meets the contract. |
| C3.1 | Observability | C3 · Platform Operations | Necessary | Monitor health and trace incidents. |
| C3.2 | Billing | C3 · Platform Operations | Commodity | Meter usage and issue invoices. |
