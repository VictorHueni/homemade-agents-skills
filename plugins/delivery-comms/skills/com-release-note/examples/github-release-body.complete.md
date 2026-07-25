## Self-service scheduling, end to end

Patients can now book, rebook and cancel appointments themselves without calling the clinic, and coordinators get a week of demand forecast plus no-show risk on tomorrow's schedule. This release also retires the v1 scheduling API.

**Highlights**

- Patient Portal: Book, rebook and cancel in a couple of taps, with the freed slot offered to the waitlist the same hour.
- Clinic Console: Tomorrow's schedule ranked by no-show risk, and a seven-day demand forecast early enough to move staff.
- Partner Integrations: The new `/api/v2` subscription feed pushes slot changes as they happen instead of polling.
- Platform: Portal, console and API ship as one release train, cutting the release window from a day to under two hours.

⚠️ **Breaking:** `/api/v1/slots` is switched off. Partners must move to `/api/v2/slots` before **2026-09-01**. Appointment references become opaque identifiers, and `reminder.sent` now fires once per appointment rather than once per channel.

📄 **Full release note:** [v2.0.0-self-service-scheduling](../blob/v2.0.0/docs/communication/release-notes/v2.0.0-self-service-scheduling.md)

**Full Changelog**: https://github.com/VictorHueni/slotwise/compare/v1.4.0...v2.0.0
