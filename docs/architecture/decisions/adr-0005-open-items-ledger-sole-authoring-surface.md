---
type: Architecture Decision Record
title: Central Open-Items Ledger as Sole Authoring Surface (Retire Per-Artefact Local Sections)
description: Retires the per-artefact local `## Open Items` section; the central ledger (whichever backend a project runs) becomes the only place open items are authored, ending the local-section-then-sync workflow.
tags: [open-items, governance]
timestamp: 2026-07-03T00:00:00Z
status: active
owner: Victor Hueni
last_reviewed: 2026-07-03
review_interval: 180d
---

# Central Open-Items Ledger as Sole Authoring Surface (Retire Per-Artefact Local Sections)

Date: 2026-07-03

## Context and Problem Statement

[`rules/open-items-governance.md`](open-items-governance.md) currently mandates a two-surface
design: every artefact that can carry unresolved work exposes a document-level `## Open Items`
table as the **authoring surface** (§1, §4); `util-open-items` Mode 1 (`sync`) then reads that
table, deduplicates against the ledger, mints an `OI-NNNN` ID (or, under the `github` backend,
opens an issue), and writes the consolidated row into the **central ledger** — the
"read-out" (§5). Every doc-producing skill's conformance checklist (§8) requires it to write
local rows first and chain to `util-open-items` afterward, and ~14 output templates
(`arch-arc42`, `arch-c4`, `spec-use-case`, `dev-stack-guide`, `dev-getting-started`,
`ux-design-system`) scaffold the bare local table into every generated artefact.

This sits on top of, and does not reopen, two prior decisions on the *backend* the central
ledger uses: [ADR-0002](adr-0002-open-items-pluggable-backend-github-issues.md) made the
backend pluggable (`markdown` | `github`) and put the kit repo's own ledger on `github`;
[ADR-0003](adr-0003-github-backend-stays-opt-in.md) declined to make `github` the universal
default for scaffolded projects, keeping `markdown` as the portable default. Neither ADR
addressed whether a *local* authoring surface should exist at all — both assumed the §1/§4/§5
two-surface design as given. This ADR narrows that assumption; it leaves the backend choice
made by ADR-0002/ADR-0003 untouched.

**The problem:** the local-authoring step has already lapsed on the kit repo, without anyone
deciding to drop it, and without the drift it should have caused. Issues
[#53](https://github.com/VictorHueni/homemade-claude-kit/issues/53),
[#54](https://github.com/VictorHueni/homemade-claude-kit/issues/54),
[#57](https://github.com/VictorHueni/homemade-claude-kit/issues/57), and
[#58](https://github.com/VictorHueni/homemade-claude-kit/issues/58) were filed directly as
GitHub issues, each carrying the full provenance triple (`Source artefact` / `Source anchor` /
`Source heading`) in the issue body — but none of their cited source files
(`rules/artefact-types-registry.md`, `rules/metamodel-reference.md`,
`var/reports/okf-compliance/okf-compliance-analysis.md`) carry a corresponding local
`## Open Items` row. There is no reconciliation drift to report because the local step was
skipped entirely, and the outcome — a fully provenance-complete central row — was
indistinguishable from doing it "the codified way." That is evidence the local step is
redundant once the central surface (an Issue Form, or a directly-edited ledger table) already
demands the same provenance fields at filing time.

## Decision Drivers

- Eliminate dual-authoring-surface bookkeeping: writing a local row and then syncing it is
  pure overhead when the central surface captures the same fields in one step.
- Match observed practice instead of maintaining a codified step nobody follows on the kit
  repo itself.
- Shrink `util-open-items` Mode 1 and the local-section presence/schema/provenance-drift
  checks in `util-metamodel-audit` — machinery that exists only to support the local step.
- Preserve provenance and traceability: the change must not weaken the
  `Source artefact` / `Source anchor` / `Source heading` discipline, only relocate the moment
  it is captured — from "in the artefact, pre-sync" to "at the central ledger, at filing time."
- Stay scoped to the authoring-surface question; do not reopen ADR-0002's backend-pluggability
  decision or ADR-0003's opt-in-`github` stance.

## Considered Options

- **Central-ledger-only.** Retire the local `## Open Items` section everywhere; the central
  ledger (whichever backend a project runs) is the sole authoring surface. (Chosen.)
- **Status quo.** Keep the local section mandatory in every artefact-producing skill; the
  central ledger stays a synced read-out per the existing §1/§4/§5/§8 contract.
- **Optional / best-effort local section.** Skills may still write a local row if convenient,
  but it is no longer mandatory or audited; the central ledger is the enforced source of
  truth regardless.
- **Thin backlink only.** Drop the full local table, but require artefacts to carry a one-line
  pointer back to their central rows (e.g. `Open items: #57, #58`) for inline discoverability.

## Decision Outcome

Chosen option: **central-ledger-only**, because it matches the kit's own dogfooded practice
with no loss of provenance — the provenance triple is asserted at central-filing time either
way — and it removes a governance layer (local-table schema compliance, sync reconciliation,
ID deduplication) that has already proven unnecessary in operation. The status quo option is
rejected precisely because it is not actually being followed. The optional/best-effort option
is rejected as a false middle ground: an unaudited, non-mandatory local section is strictly
worse than no section — it invites half-populated tables that look authoritative but aren't,
with no check to catch the difference. The thin-backlink option is rejected as a *mandate*
(discussed under Negative Consequences below) but is not prohibited — a skill may still choose
to add such a pointer as a documentation nicety.

This decision extends the authoring-surface half of ADR-0002; it does not supersede
ADR-0002 or ADR-0003, whose backend-pluggability and opt-in-`github` outcomes stand unchanged.

### Positive Consequences

- One authoring surface per project, matching how the kit repo already operates.
- `util-open-items` Mode 1 (`sync`) collapses from "reconcile local table against ledger,
  dedupe, mint ID, write back" to direct ledger/issue authoring — materially less mechanism.
- `util-metamodel-audit`'s local-section-presence, schema-compliance, and provenance-drift
  checks (§7) simplify to a single question: does the central row's provenance point at a
  real file/anchor? There is no second surface to drift against.
- ~14 output templates and ~18 `SKILL.md` conformance instructions shrink — no bare table
  skeleton to scaffold, no "write locally then chain to `util-open-items`" step to maintain.
- Removes an entire class of findings `util-metamodel-audit` currently has to check for:
  malformed local tables, nested `### Open Items` headings, local/ledger ID mismatches.

### Negative Consequences

- **Inline discoverability is lost.** A reader of an artefact no longer sees its pending open
  items co-located in the document; they must separately check the central ledger/issue
  tracker. No backlink is mandated to mitigate this — a skill may add a one-line pointer
  voluntarily, but it is not part of this decision.
- Provenance capture now depends entirely on whoever files the central row supplying an
  accurate `Source artefact` / `Source anchor` / `Source heading` at that moment, without the
  benefit of editing directly next to the heading being referenced (slightly higher risk of a
  stale or approximate anchor compared to authoring in place).
- §9's `_central-only_` provenance form (governance work with no artefact home) was
  documented as the *exception* to artefact-sourced rows; under this decision it becomes the
  default shape for provenance capture generally (still distinguishing "has a source artefact"
  from "central-only"), which requires rewriting §9's framing, not just its scope.
- Non-trivial follow-through: `rules/open-items-governance.md` §1/§4/§8/§9,
  `util-open-items/SKILL.md` Mode 1, `util-metamodel-audit`'s check catalogue, ~14 templates,
  and ~18 `SKILL.md` files all need updating. This ADR records the decision only — the
  execution is tracked separately (see Open Items below) and picked up as its own
  implementation plan.

## Pros and Cons of the Options

### Central-ledger-only

Retire the local table everywhere; author directly into whichever central surface a project
runs (markdown ledger or GitHub Issues).

#### Positive

- Matches observed practice on the kit repo with zero migration needed for the rows already
  filed that way.
- Removes the sync/reconciliation/dedup mechanism and the local-section audit surface.

#### Negative

- Loses inline, co-located discoverability of pending work inside the artefact itself.
- Concentrates provenance-quality risk on the central-filing step, with no local edit-in-place
  cross-check.

### Status quo (local section + sync)

Keep §1/§4/§5/§8 as specified: local table is the authoring surface, central ledger is the
synced read-out.

#### Positive

- Inline discoverability preserved — pending work is visible right in the artefact.
- Provenance is captured at the moment of noticing the gap, next to the heading it references.

#### Negative

- Already demonstrably not followed on the kit repo (issues #53/#54/#57/#58) — codifies a step
  that adds process cost without adding compliance.
- Full sync/reconciliation/ID-mint machinery in `util-open-items` Mode 1 and the matching
  audit checks in `util-metamodel-audit` must be built and kept correct for every backend.

### Optional / best-effort local section

Local table stays available but not mandatory or audited; central ledger is enforced as the
sole source of truth regardless.

#### Positive

- Skills that want inline visibility can still have it, with no audit burden.

#### Negative

- An unaudited "convention" is worse than no convention — a stale or half-filled local table
  looks authoritative to a reader but isn't, and nothing flags the mismatch.
- Does not actually simplify `util-open-items` or the audit relative to central-ledger-only —
  both would still need to *tolerate* a local section that might or might not be accurate.

## Open Items

None here — per this very decision, follow-up work is tracked at the central ledger, not
in this ADR. The four execution items that implement this decision were filed as
[#60](https://github.com/VictorHueni/homemade-claude-kit/issues/60),
[#61](https://github.com/VictorHueni/homemade-claude-kit/issues/61),
[#62](https://github.com/VictorHueni/homemade-claude-kit/issues/62), and
[#63](https://github.com/VictorHueni/homemade-claude-kit/issues/63), and closed once this
branch merges.
