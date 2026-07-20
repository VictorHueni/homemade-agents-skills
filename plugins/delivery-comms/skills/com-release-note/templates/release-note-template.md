---
type: Release Notes
title: "{Product} v{X.Y.Z} — {one-line theme}"
description: "Stakeholder release note for v{X.Y.Z}: {what this release delivers, in one sentence a non-technical reader understands}."
tags: [release-notes, "v{X.Y.Z}"]
timestamp: "{ISO 8601 datetime, e.g. 2026-07-18T00:00:00Z}"
status: draft
owner: "{git config user.name}"
last_reviewed: "{YYYY-MM-DD}"
review_interval: 90d
---

<!--
  TEMPLATE — do not fill in place. Copy to the project (Scaffold mode), then Curate mode
  populates it. Every {curly placeholder} and _TODO_ is a slot to replace. Rules of this artefact:
    - Plain language, benefit-first. Write for an insurer / manager / investor, not a developer.
    - NO em dashes in the title or any heading (use a colon for `label: description`).
    - Scope honesty: Tier 1 describes only what a non-technical reader can see or act on.
      Operator-only / internal / staging-only work belongs in Tier 2 (or an earlier release).
    - Do NOT invent features that are not in the changelog / evidence bundle.
    - Private audit-trail IDs (plan numbers, PRD IDs) go in small parens: (0137).
  Delete this comment block when the note is finalised.
-->

# v{X.Y.Z}: {one-line theme} ({date or date-range})

> _{Optional one-sentence framing: what changed for the reader this release, or a retro/disclaimer note.}_

## What's new

<!-- Tier 1 — Product capabilities. One block per Product that shipped user-facing work.
     Structure mirrors the FBS product-scoped view: Product -> Business Capability -> Functionality.
     Use the FBS (docs/product-specs/07a-fbs.md), NOT the domain-scoped capability map IDs
     (the two numbering schemes collide). Empty products/capabilities simply don't render. -->

**P{n} · {Product name}**

- C{n}.{m} {Capability name}: {what shipped, in plain language and benefit-first}. ({plan/PRD id})
- C{n}.{m} {Capability name}: {what shipped}. ({plan/PRD id})

**P{n} · {Product name}**

- C{n}.{m} {Capability name}: {what shipped}. ({plan/PRD id})

## Platform and engineering

<!-- Tier 2 — work with no product-capability home (infra, CI/CD, refactors, tooling, perf,
     security). DEFAULT generic buckets below. **Redefine these per project** to your own stable
     set the first time you curate a note, then keep them fixed release-to-release so the reader
     learns the shape. Delete any bucket with nothing to report this release. -->

- CI/CD and Deployment: {what changed}. ({plan id})
- Data and Pipeline: {what changed}. ({plan id})
- Observability: {what changed}. ({plan id})
- Quality Assurance: {what changed}. ({plan id})
- Architecture and Domain: {what changed}. ({plan id})
- Security: {what changed}. ({plan id})

## Breaking changes

<!-- Only if any. Plain-language impact + what the reader must do. Delete the section if none. -->

- {what breaks, who it affects, the action required}.

---

**Full Changelog**: v{PREV}...v{X.Y.Z}
