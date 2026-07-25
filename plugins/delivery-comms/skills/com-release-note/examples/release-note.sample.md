---
type: Release Notes
title: "Slotwise v1.4.0 — Rebooking without phone calls"
description: "Stakeholder release note for v1.4.0: patients can now rebook missed slots themselves, and clinics see no-show risk before it happens."
tags: [release-notes, "v1.4.0"]
timestamp: "2026-07-18T00:00:00Z"
status: active
owner: "Victor Hueni"
last_reviewed: "2026-07-18"
review_interval: 90d
---

# v1.4.0: Rebooking without phone calls (2026-06-02 to 2026-07-18)

> _This release moves slot rebooking from the clinic's front desk to the patient's own hands, and gives coordinators early warning on likely no-shows._

## What's new

**P1 · Slotwise Patient Portal**

- C1.2 Slot rebooking: Patients who miss an appointment can now pick a replacement slot themselves from live availability, instead of calling the clinic. Confirmations go out by mail and SMS. (0141)
- C1.3 Reminders: Reminder timing now adapts to each patient's past response behaviour, so late confirmers get an earlier nudge. (0137)

**P2 · Slotwise Clinic Console**

- C2.1 Schedule overview: Coordinators see a no-show risk badge on tomorrow's schedule, ranked so the riskiest bookings sit on top. (0139)
- C2.4 Waitlist: Freed slots are offered to the waitlist automatically; the first acceptance wins the slot and everyone else is stood down politely. (0141)

## Platform and engineering

- CI/CD and Deployment: Release pipeline now ships the portal and console together, halving the release window. (0135)
- Data and Pipeline: Nightly availability sync moved to change-data-capture; slot data is now at most 5 minutes stale. (0138)
- Quality Assurance: End-to-end rebooking journey is covered by an automated test that runs on every merge. (0141)
- Security: Session tokens rotate on privilege change; penetration-test finding PT-7 closed. (0142)

## Breaking changes

- The legacy `/api/v1/slots` polling endpoint is retired. Integrations must move to the `/api/v2/slots` subscription feed before 2026-09-01; clinic IT contacts were notified on 2026-07-01.

---

**Full Changelog**: v1.3.0...v1.4.0
