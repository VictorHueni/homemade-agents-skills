---
title: Example Platform — Delivery Roadmap
status: draft
owner: example
last_reviewed: 2026-05-29
review_interval: 60d
---

<!-- doc-version: 1.0 | created: 2026-05-29 -->

# Example Platform — Delivery Roadmap

Dual-purpose delivery plan + product roadmap.

---

## Walking Skeleton — MVP

**Hypothesis to validate:** A customer can place and receive one order end-to-end without manual support.
**Value stream delivered end-to-end:** VS-2 · Order to Delivery — Pain: Critical

| Epic | MVP functionalities | Deferred to Phase 1 |
|---|---|---|
| E-01 | C1.1.F01 · C1.2.F01 | SSO, RBAC |
| E-02 | C2.1.F01 | Bulk import |

**After MVP ships, P-01 can:**
1. Create an account and log in
2. Place a single validated order
3. Receive delivery confirmation

**After MVP ships, P-01 cannot yet:**
- Import orders in bulk → Phase 1 (E-02 complete)
- Use SSO → Phase 1 (E-01 complete)

---

## Phase Plan

| Phase | Epics | Value streams fully operational | Goal |
|---|---|---|---|
| **MVP** | E-01 (partial), E-02 (partial) | VS-2 (thin slice) | P-01 completes one order end-to-end. |
| **Phase 1** | E-01, E-02 complete | VS-1 · VS-2 | P-01 onboards and orders without workarounds. |
| **Phase 2** | E-03 | VS-3 | Operators bill and observe the platform. |

---

## Epic Table

| ID | Epic name | VS anchor | Pain | Personas | Capabilities | FBS rows | Phase | PRD | Status |
|---|---|---|---|---|---|---|---|---|---|
| E-01 | Account Onboarding | VS-1.2 | Critical | P-01 | C1.1, C1.2 | 6 | MVP | _TODO_ | 🔄 |
| E-02 | Order Capture | VS-2.1 | High | P-01 | C2.1 | 3 | MVP | _TODO_ | 🔄 |
| E-03 | Operations & Billing | VS-3.1 | Medium | P-02 | C3.1, C3.2 | 4 | Phase 2 | _TODO_ | ⬜ |

---

## Epics

### E-01 · Account Onboarding

**Value statement:** When this epic ships, P-01 can create and manage an account unaided.
**VS anchor:** VS-1.2 · Account Lifecycle — Pain: Critical
**Phase:** MVP

**FBS scope:**

| ID | Functionality | Status |
|---|---|---|
| C1.1.F01 | Email + password login | ✅ |
| C1.2.F01 | Self-serve sign-up | ✅ |
| C1.1.F03 | Role-based access control | 🔄 |

---

### E-02 · Order Capture

**Value statement:** When this epic ships, P-01 can place a validated order.
**VS anchor:** VS-2.1 · Order Capture — Pain: High
**Phase:** MVP

**FBS scope:**

| ID | Functionality | Status |
|---|---|---|
| C2.1.F01 | Guided order form | 🔄 |
| C2.1.F03 | Order validation rules | ⬜ |

---

### E-03 · Operations & Billing

**Value statement:** When this epic ships, P-02 can monitor and bill usage.
**VS anchor:** VS-3.1 · Billing — Pain: Medium
**Phase:** Phase 2

**FBS scope:**

| ID | Functionality | Status |
|---|---|---|
| C3.2.F01 | Usage metering | ⬜ |
