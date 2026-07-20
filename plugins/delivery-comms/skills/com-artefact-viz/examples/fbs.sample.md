---
title: Example Platform — Functional Breakdown Structure
status: draft
owner: example
last_reviewed: 2026-05-29
review_interval: 60d
---

<!-- doc-version: 1.0 | created: 2026-05-29 -->

# Example Platform — Functional Breakdown Structure

Functionality registry for the example platform.

---

## Status legend

| Symbol | Meaning |
|---|---|
| ✅ | **Shipped** |
| 🔄 | **Planned** |
| ⬜ | **Backlog** |

---

## L0 axis declaration

**Chosen axis:** Capability domain *(inherited from BC Map)*

**L0 items:**
- **C1** — Customer Management
- **C2** — Service Delivery

---

## Global overview

```
Example Platform
│
├── C1 · Customer Management
│   ├── C1.1 · Identity & Access  (functionalities: 2 ✅ · 1 🔄 · 0 ⬜)
│   └── C1.2 · Account Lifecycle  (functionalities: 1 ✅ · 1 🔄 · 1 ⬜)
│
└── C2 · Service Delivery
    └── C2.1 · Order Capture  (functionalities: 0 ✅ · 1 🔄 · 2 ⬜)
```

---

## C1 · Customer Management

### C1.1 · Identity & Access

*Authenticate and authorise every actor.*

**BC Map:** [C1.1](../../business/03a-capability-map.md#c11)

| ID | Functionality | Status | VS stage |
|---|---|---|---|
| C1.1.F01 | Email + password login | ✅ | VS-1.1 |
| C1.1.F02 | SSO via OIDC | ✅ | VS-1.1 |
| C1.1.F03 | Role-based access control | 🔄 | _TODO_ |

---

### C1.2 · Account Lifecycle

*Onboard, maintain, and offboard accounts.*

| ID | Functionality | Status | VS stage |
|---|---|---|---|
| C1.2.F01 | Self-serve sign-up | ✅ | VS-1.2 |
| C1.2.F02 | Account suspension | 🔄 | VS-1.3 |
| C1.2.F03 | Data export on offboard | ⬜ | _TODO_ |

---

## C2 · Service Delivery

### C2.1 · Order Capture

*Capture and validate service orders.*

| ID | Functionality | Status | VS stage |
|---|---|---|---|
| C2.1.F01 | Guided order form | 🔄 | VS-2.1 |
| C2.1.F02 | Bulk order import | ⬜ | _TODO_ |
| C2.1.F03 | Order validation rules | ⬜ | VS-2.1 |
