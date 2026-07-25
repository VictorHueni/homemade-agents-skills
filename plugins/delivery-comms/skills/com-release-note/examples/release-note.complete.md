---
type: Release Notes
title: "Slotwise v2.0.0 — Self-service scheduling, end to end"
description: "Stakeholder release note for v2.0.0: patients manage their own appointments from booking to rebooking, clinics see demand a week ahead, and the v1 API is retired."
tags: [release-notes, "v2.0.0"]
timestamp: "2026-07-25T00:00:00Z"
status: active
owner: "Victor Hueni"
last_reviewed: "2026-07-25"
review_interval: 90d
---

# v2.0.0: Self-service scheduling, end to end (2026-04-02 to 2026-07-25)

> _The first release where a patient can complete a whole appointment lifecycle without calling the clinic. It also retires the v1 API, so integration partners have work to do before 1 September._

## What's new

**P1 · Slotwise Patient Portal**

- C1.1 Booking: Patients can book a first appointment themselves, choosing from live availability instead of requesting a callback. Average time to a confirmed slot fell from two days to four minutes in the pilot clinics. (0148)
- C1.2 Slot rebooking: A missed or unwanted appointment can be moved by the patient in a couple of taps, with confirmation by mail and SMS. (0141)
- C1.4 Cancellations: Cancelling releases the slot to the waitlist immediately, so the time is offered to someone else the same hour rather than the next working day. (0150)
- C1.3 Reminders: Reminder timing adapts to how each patient has responded in the past, so people who confirm late are nudged earlier. (0137)

**P2 · Slotwise Clinic Console**

- C2.1 Schedule overview: Coordinators see tomorrow's schedule ranked by no-show risk, so the bookings worth a phone call are at the top of the list. (0139)
- C2.4 Waitlist: Freed slots are offered to waitlisted patients automatically; the first acceptance takes the slot and everyone else is stood down politely. (0141)
- C2.6 Capacity planning: A seven-day demand forecast shows where next week is over- or under-booked, early enough to move staff. (0152)

**P3 · Partner Integrations**

- C3.2 Scheduling API: The new `/api/v2` subscription feed pushes slot changes to partner systems as they happen, replacing the polling model that could be up to fifteen minutes stale. (0145)
- C3.3 Audit export: Practice managers can export a full appointment audit trail for a date range without raising a support ticket. (0149)

## Fixes and improvements

- C2.4 Waitlist: Double bookings no longer happen when two coordinators accept the same freed slot at the same moment. (0144)
- C1.3 Reminders: Reminders are no longer sent twice when a patient updates their phone number between confirmation and appointment. (0137)
- C1.2 Slot rebooking: Rebooking across a daylight-saving change now keeps the time the patient actually chose. (0143)
- C3.3 Audit export: Exports covering more than 5,000 appointments complete instead of timing out. (0149)

## Platform and engineering

- CI/CD and Deployment: Portal, console and API now ship as one release train, cutting the release window from a full day to under two hours. (0135)
- Data and Pipeline: Availability sync moved to change-data-capture; slot data is at most five minutes stale, down from a nightly batch. (0138)
- Observability: Booking and rebooking journeys are traced end to end, so a failed booking can be diagnosed from a single appointment reference. (0146)
- Quality Assurance: The full self-service journey runs as an automated test on every merge, alongside a load test at three times peak booking volume. (0147)
- Architecture and Domain: Scheduling logic was consolidated into one service, removing the duplicate slot rules that caused the double-booking defects. (0144)
- Security: Session tokens rotate on privilege change, and penetration-test findings PT-7 and PT-11 are closed. (0142)

## Breaking changes

- Scheduling API v1 retired: The `/api/v1/slots` polling endpoint is switched off. Partner systems must move to the `/api/v2/slots` subscription feed before 2026-09-01; integration contacts were notified on 2026-07-01 and a migration guide is published. (0145)
- Appointment identifiers: Appointment references change from sequential numbers to opaque identifiers. Systems storing references keep working, but anything deriving order or volume from them must stop doing so. (0151)
- Reminder webhooks: The `reminder.sent` webhook now fires once per appointment rather than once per channel. Partners counting deliveries should count channel entries in the payload instead. (0137)

---

**Full Changelog**: v1.4.0...v2.0.0
