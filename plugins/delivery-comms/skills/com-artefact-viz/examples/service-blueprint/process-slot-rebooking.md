<!-- doc-version: 1.0 | created: 2026-01-01 -->

# Slot Release & Rebooking

**Audience:** internal technical reference.

**Type:** Descriptive operator-grade reference.

---

## 1. What this process is

**Slot Release & Rebooking** is the coordination loop that frees a booked slot a
requester can no longer use and reassigns it to someone else before it is lost.

**Scope:** starts when a requester confirms they will release a slot; ends when
the slot has been reattributed and all parties notified.

---

## 2. Triggers — what starts this process

| Trigger | Source | Frequency | Decision criteria |
|---|---|---|---|
| Requester signals a release | Requesting User | per-case | Slot is in the future and still held |

---

## 3. Actors — roles + responsibilities

| Actor | Role in this process | Authority | Decision rights | Statutory / contractual basis |
|---|---|---|---|---|
| Requesting User | Releases the slot they can no longer use | Self-service | Release / keep | Terms of use |
| Coordinator | Validates the release and the rebooking | Operational | Approve rebooking | Internal SOP |
| Operations Analyst | Reconciles freed capacity, audits the loop | Operational | Flag anomalies | Internal SOP |
| Scheduling Platform | Detects the freed slot and fans out availability | Automated | — | — |

---

## 4. Data Stores — systems and registries involved

| System | Owner | Read by | Written by | Authoritative for | Format / API |
|---|---|---|---|---|---|
| Scheduling Platform | Operations | All actors | Coordinator, Platform | Slot state | REST API |
| Capacity Ledger | Operations | Operations Analyst | Scheduling Platform | Freed-capacity history | Internal |

---

## 5. Data Objects — what flows through the process

| Object | Created by | Consumed by | Format | Required fields | Standards reference |
|---|---|---|---|---|---|
| Release confirmation | Requesting User | Coordinator | App form | Slot ID, reason | — |
| Slot-open event | Scheduling Platform | Operations Analyst | Event | Slot ID, timestamp | — |
| Availability broadcast | Scheduling Platform | Requesting User | Email / SMS | Slot ID, window | — |
| Rebooking confirmation | Coordinator | Requesting User | Email | Slot ID, new holder | — |

---

## 6. Activities — step-by-step walkthrough

### 6.1 Requesting User's flow

1. **Open the slot** — locate the held slot in the app.
2. **Confirm release** — submit the release confirmation with a reason.
3. **Receive availability broadcast** — see the slot offered out (if re-requesting).
4. **Receive rebooking confirmation** — get notified the slot was reassigned.

### 6.2 Coordinator's flow

1. **Review release** — open the release confirmation.
2. **Validate freed slot** — check the slot is genuinely free.
3. **Approve broadcast** — let the platform fan out availability.
4. **Confirm rebooking** — validate the new holder and send confirmation.

### 6.3 Operations Analyst's flow

1. **Ingest slot-open event** — record the freed slot in the ledger.
2. **Reconcile capacity** — match freed capacity to demand.
3. **Audit the loop** — flag slots that were freed but never reattributed.

### 6.4 Scheduling Platform's flow

1. **Mark slot open** — flip the slot to available on release.
2. **Emit slot-open event** — notify backstage of the freed slot.
3. **Broadcast availability** — fan out the availability broadcast.
4. **Reassign slot** — bind the slot to the new holder.

---

## 9. What's broken today — pain points

| Pain point | Who experiences it | Where in the process | Impact |
|---|---|---|---|
| Manual validation is slow | Coordinator | §6.2 Validate freed slot | Slots expire before rebooking |
| No visibility into freed capacity | Requesting User | §6.1 Receive availability broadcast | Missed rebooking windows |
