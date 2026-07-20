---
type: Use Case
title: "UC-02 — File an issue via the tracker forms"
description: "The operator files a new item through the per-type intake forms, which classify it at birth: type label and needs-triage applied on submit, priority and size mirrored to labels by automation."
tags: [open-items, filing, issue-forms, github-backend]
timestamp: "2026-07-20T15:30:00Z"
status: draft
owner: "Victor Hueni"
last_reviewed: "2026-07-20"
review_interval: 180d
---

# UC-02 — File an issue via the tracker forms

> Casual format (Cockburn). Promote to fully-dressed without re-numbering when the goal earns it. Methodology: kit `spec-use-case/references/methodology.md`.

| **Scope** | system | **Level** | user-goal 🌊 | **Primary Actor** | Operator | **Realises** | _TBD_ (contract lives in `util-open-items/references/github-backend.md` §2; forms in `util-open-items/templates/`) |
|---|---|---|---|---|---|---|---|

**Main scenario.** The Operator has a new item to record and opens the tracker's
intake chooser, which offers one form per kind of work — bug, feature, task, docs,
tech-debt, in that order. They pick the form matching the item; it asks for the
substance first — the fields that kind of work requires (reproduction steps for a
bug, problem and motivation for a feature, what's missing and where for docs) plus
the shared execution fields (references, acceptance criteria, out of scope) where
they apply — and the shared priority and size ratings last. On submission the issue
arrives already classified: the form statically applies its `type:` label and
`needs-triage`, and the labeler automation mirrors the priority and size answers to
their `priority:`/`size:` labels. The item is now queryable by labels alone,
correctly shaped for triage (UC-04), and guaranteed not to enter the delegation
queue until a triage pass promotes it.

**Alternate paths.**

- The Operator tries to open a blank issue → the intake surface disallows it
  (blank issues disabled); every filing goes through a typed form so no issue is born
  unclassified.
- The label vocabulary was never bootstrapped on the repo → the tracker **silently
  skips** the form's label entries and the issue arrives unlabelled — the hazard that
  is exactly why bootstrap-labels-first is step 1 of the adoption checklist (UC-09).
- The tracker's duplicate suggestions surface an existing similar issue while the
  title is being typed → the Operator abandons the filing and adds their context to
  the existing issue instead.
- The Operator later edits the priority or size answer in the issue body → the
  labeler automation re-mirrors the dropdown values to the labels, keeping body and
  labels consistent.
- The item needs fields no form carries (pure governance provenance edge cases) →
  file through the sync contract (UC-03) instead; forms and sync produce the same
  body sections either way.
