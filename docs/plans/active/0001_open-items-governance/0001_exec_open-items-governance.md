---
title: Plan-0001 — Open Items Governance
status: draft
owner: Victor Hueni
last_reviewed: 2026-05-25
review_interval: 30d
---

# Implementation Plan: Open Items Governance

## Summary

This plan implements a repo-native governance model for unresolved work across generated artefacts. The target state is: each artefact uses a standardized document-level `## Open Items` section with one canonical schema; a central living ledger exists under `project-control/open-items/`; a dedicated skill maintains that ledger; and `util-metamodel-audit` verifies compliance and sync health. `util-docs-audit` remains generic and is not extended into stack-specific open-item governance.

Source: feature request discussed on 2026-05-25. No upstream PRD exists yet; `0001` is a provisional feature-request ID and should be reused by the future PRD if one is created.

Principles:

1. One increment equals one coherent change set.
2. Every increment has an explicit test gate.
3. Standardize local artefact sections before building central sync logic.
4. Keep the central tracker as the living system of record; keep audits report-only.
5. Distinguish scaffold placeholders from actionable unresolved work.
6. Normalize schema and lifecycle rules across artefacts without exceptions in section placement.

**Overall Status:** done
**Current Increment:** _all increments complete_

## Increment Plan

### Increment 01: Define the Open Items Contract

**Status:** done

Scope:

1. Add a canonical governance spec describing heading name, column schema, item taxonomy, lifecycle states, and repo-level source-of-truth rules.
2. Define the difference between inline `_TODO_` placeholders and actionable open items.
3. Define how each open-item row preserves source location in the central ledger using both a short source anchor and its full heading text.
4. Define the canonical control-plane path `project-control/open-items/` and explain why it is separate from product backlog artefacts.

Primary files:

1. `rules/open-items-governance.md`
2. `rules/metamodel.md`
3. `README.md`

Test gate:

1. `test -f docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md`
2. `rg -n "## Open Items|document-level|Source anchor|Source heading|project-control/open-items|doc-gap|decision-gap|execution-item|tech-debt" rules/open-items-governance.md rules/metamodel.md README.md`

Exit criteria:

1. A single canonical `Open Items` contract exists in the repo.
2. The contract defines section name, source-location fields, table columns, item types, and status lifecycle unambiguously.

### Increment 02: Scaffold the Central Control Plane

**Status:** done

Scope:

1. Create the `project-control/open-items/` folder with a README that defines purpose, lifecycle, and operator guidance.
2. Create the initial living ledger file with the canonical table schema, source-location provenance fields, and placeholder guidance.
3. Add an archive convention for historical snapshots or closed-item rollups without confusing the live ledger.

Primary files:

1. `project-control/open-items/README.md`
2. `project-control/open-items/open-items.md`
3. `project-control/open-items/archive/.gitkeep`

Test gate:

1. `test -d project-control/open-items`
2. `test -f project-control/open-items/open-items.md`
3. `rg -n "OI-ID|Type|Summary|Source artefact|Source anchor|Source heading|Resolution path|Priority|Status|Owner|Due / Review date" project-control/open-items/README.md project-control/open-items/open-items.md`

Exit criteria:

1. The central ledger exists and is readable without referring back to the skill discussion.
2. The live ledger and archive intent are clearly separated.

### Increment 03: Normalize Existing Artefact Templates With Real Open-Item Sections

**Status:** done

Scope:

1. Rename existing dedicated sections such as `Open / TODO`, `Open TODOs`, and `Open questions ...` to the canonical document-level `## Open Items`.
2. Convert those sections to the canonical table schema while preserving artefact-specific context in adjacent sections.
3. Refactor `arch-research` so question-level unresolved notes move into one document-level `## Open Items` section, with each row carrying both `Source anchor` and `Source heading`.
4. Update skill instructions so generated artefacts consolidate actionable unresolved items in one canonical document-level `## Open Items` section.
5. Remove placeholder-only open-item requirements from `business-process`; only actionable unresolved work belongs in `Open Items`.
6. In `business-research/references/template.md`, cover every embedded variant that has an unresolved-work section today: interview template, interview synthesis, and research synthesis.
7. In `business-workshop/references/template.md`, cover every embedded variant that has an unresolved-work section today, including workshop synthesis and any other variant that currently carries such a section.
8. Treat `spec-prd` as a first adopter of the contract even though it is not a migration from an older heading.

Primary files:

1. `arch-research/references/template.md`
2. `business-process/references/template.md`
3. `business-research/references/template.md`
4. `business-workshop/references/template.md`
5. `arch-research/references/discipline.md`
6. `business-process/references/logic-and-sequence.md`
7. `util-metamodel-audit/references/check-catalogue.md`
8. `arch-research/SKILL.md`
9. `business-process/SKILL.md`
10. `business-research/SKILL.md`
11. `business-workshop/SKILL.md`
12. `spec-prd/SKILL.md`

Test gate:

1. `rg -n "^## Open Items" arch-research business-process business-research business-workshop spec-prd`
2. `rg -n "OI-ID|Resolution path|Due / Review date|Tracker ref" arch-research business-process business-research business-workshop spec-prd`
3. `rg -n "Source anchor|Source heading|Tracker ref" arch-research business-process business-research business-workshop spec-prd`
4. `! rg -n "## 11\\. Open TODOs|### Open / TODO|## Open questions remaining|## Open questions for next workshop / research wave|## Open questions for next interview|^### Open Items" arch-research business-process business-research business-workshop`
5. `! rg -n "Open / TODO|Open TODOs" arch-research/references/discipline.md business-process/references/logic-and-sequence.md util-metamodel-audit/references/check-catalogue.md`

Exit criteria:

1. The currently implemented open-item sections share one heading and one schema at document level.
2. `arch-research` explicitly consolidates question-level unresolved notes into one document-level `## Open Items` section, preserving per-question provenance via `Source anchor` and `Source heading`.
3. `business-process` no longer requires placeholder-only scaffold rows in `Open Items`.
4. The affected skills explicitly instruct the model to consolidate actionable unresolved items into canonical document-level `Open Items` sections and keep tracker provenance.

### Increment 04: Resolve Stale `§Open Issues` References and Decide Coverage for Other Business Artefacts

**Status:** done

Scope:

1. Replace stale discipline-doc references to `§Open Issues` with the canonical `Open Items` wording.
2. Decide whether business-model-canvas, business-capability-map, business-value-stream, and spec-functional-breakdown-structure gain explicit `Open Items` sections in their templates or rely on changelog-only handling.
3. Record that `business-competitive-landscape` remains changelog-only for now and is not part of the formal `Open Items` rollout in this increment.
4. Apply those decisions consistently across discipline docs, templates, and skill guidance.

Primary files:

1. `business-model-canvas/references/canvas-discipline.md`
2. `business-capability-map/references/capability-discipline.md`
3. `business-value-stream/references/value-stream-discipline.md`
4. `spec-functional-breakdown-structure/references/fbs-discipline.md`
5. `business-model-canvas/references/template.md`
6. `business-capability-map/references/template.md`
7. `business-value-stream/references/template.md`
8. `spec-functional-breakdown-structure/references/template.md`
9. `business-competitive-landscape/references/landscape-discipline.md`

Test gate:

1. `! rg -n "§Open Issues|Open Issues" business-model-canvas business-capability-map business-value-stream spec-functional-breakdown-structure`
2. `rg -n "Open Items|Changelog" business-model-canvas/references/template.md business-capability-map/references/template.md business-value-stream/references/template.md spec-functional-breakdown-structure/references/template.md business-competitive-landscape/references/landscape-discipline.md`

Exit criteria:

1. No stale `§Open Issues` wording remains in the targeted artefacts.
2. Each targeted artefact has an explicit and documented stance on unresolved-item capture.
3. `business-competitive-landscape` explicitly remains changelog-only for now.

### Increment 05: Create the `util-open-items` Skill

**Status:** done

Scope:

1. Add a dedicated utility skill for syncing, triaging, closing, and reporting open items.
2. Define the ledger update rules, ID assignment rules, de-duplication policy, source-location provenance rules, and closure semantics.
3. Define how synced rows preserve both `Source anchor` and `Source heading` from the source document.
4. Add references or templates needed for a predictable operating model.

Primary files:

1. `util-open-items/SKILL.md`
2. `util-open-items/references/template.md`
3. `util-open-items/references/triage-rules.md`

Test gate:

1. `test -f util-open-items/SKILL.md`
2. `rg -n "sync|triage|close|report|OI-ID|Source anchor|Source heading|## Open Items|project-control/open-items/open-items.md" util-open-items/SKILL.md util-open-items/references/template.md util-open-items/references/triage-rules.md`

Exit criteria:

1. A dedicated skill exists for maintaining the living ledger.
2. The skill can be invoked without relying on tribal knowledge from this conversation.

### Increment 06: Chain Open-Item Sync Into Artefact-Producing Skills

**Status:** done

Scope:

1. Update artefact-producing skills that can emit unresolved work to include a final `Sync Open Items` step.
2. Ensure the chaining language distinguishes between local artefact consolidation and central-ledger sync.
3. Ensure the chaining language states that sync preserves `Source anchor` and `Source heading` for each row.
4. Limit chaining to relevant skills rather than every skill in the repo.

Primary files:

1. `arch-research/SKILL.md`
2. `business-process/SKILL.md`
3. `business-research/SKILL.md`
4. `business-workshop/SKILL.md`
5. `spec-prd/SKILL.md`
6. `spec-implementation-plan/SKILL.md`
7. `ops-runbook/SKILL.md`

Test gate:

1. `rg -n "Sync Open Items|util-open-items|project-control/open-items" arch-research/SKILL.md business-process/SKILL.md business-research/SKILL.md business-workshop/SKILL.md spec-prd/SKILL.md spec-implementation-plan/SKILL.md ops-runbook/SKILL.md`

Exit criteria:

1. Relevant artefact-producing skills instruct the agent to sync open items after generation or update.
2. The chaining language is consistent enough to support future automation.

### Increment 07: Extend `util-metamodel-audit` With Open-Item Governance Checks

**Status:** done

Scope:

1. Add stack-aware checks for open-item section compliance, schema compliance, tracker sync coverage, stale open items, source-location provenance, and closure drift.
2. Extend the audit template and check catalogue to report those findings clearly.
3. Keep the audit report-only; do not let it mutate the central ledger or source artefacts.

Primary files:

1. `util-metamodel-audit/SKILL.md`
2. `util-metamodel-audit/references/template.md`
3. `util-metamodel-audit/references/check-catalogue.md`
4. `util-metamodel-audit/references/methodology-references.md`

Test gate:

1. `rg -n "Open item|tracker sync|schema compliance|closure drift|project-control/open-items" util-metamodel-audit/SKILL.md util-metamodel-audit/references/template.md util-metamodel-audit/references/check-catalogue.md`
2. `rg -n "report-only|never modifies|No auto-fix" util-metamodel-audit/SKILL.md`

Exit criteria:

1. The metamodel audit can detect governance drift between artefacts and the central ledger.
2. The report remains clearly separated from the living control plane.

### Increment 08: Clarify `util-docs-audit` Boundaries and Run a Repo Pilot

**Status:** done

Scope:

1. Add a small boundary note so `util-docs-audit` remains focused on generic doc rot, not stack governance.
2. Run a pilot pass across this repo’s skills and templates using the new contract.
3. Capture any rollout gaps discovered during the pilot in the central ledger or a follow-up report.

Primary files:

1. `util-docs-audit/SKILL.md`
2. `project-control/open-items/open-items.md`
3. `var/reports/metamodel-audit/`

Test gate:

1. `rg -n "generic|stale|outdated|dead docs" util-docs-audit/SKILL.md`
2. `rg -n "not a stack-governance tracker|util-metamodel-audit|util-open-items" util-docs-audit/SKILL.md`
3. `test -d var/reports/metamodel-audit || true`

Exit criteria:

1. The boundary between docs audit, open-item ledger, and metamodel audit is explicit.
2. A first-pass rollout path exists for validating the governance model on this repo.

## Delivery Rules

1. One increment per commit.
2. Each increment must be independently runnable and reversible.
3. Do not let audit skills mutate source artefacts or the living ledger.
4. Do not treat scaffold `_TODO_` placeholders as ledger-worthy open items; placeholder-only open-item rows should not be scaffolded.
5. Keep naming, table columns, and lifecycle states identical across artefacts once standardized.
6. Prefer additive migrations with explicit wording changes over silent semantic reinterpretation.
7. Preserve the distinction between product delivery backlog, documentation completeness, and operational governance work.

## Milestone Chunks (Standalone Delivery Groups)

| Milestone | Increments | Status | Coherent Outcome | Standalone Test Gate | Exit Criteria | Commit Guidance |
| :------------- | :------------ | :------ | :--------------- | :--------------------- | :----------------- | :-------------- |
| M1: Contract and Control Plane | 01-02 | done | Canonical open-items rules exist and a central ledger is scaffolded | `rg -n "Open Items|project-control/open-items" rules/open-items-governance.md rules/metamodel.md project-control/open-items/README.md project-control/open-items/open-items.md` | Governance contract and live ledger both exist | `docs(governance): define open-items contract and control plane` |
| M2: Artefact Normalization | 03-04 | done | Existing templates and discipline docs use one unresolved-work vocabulary and one canonical document-level schema | `rg -n "^## Open Items" arch-research business-process business-research business-workshop business-model-canvas business-capability-map business-value-stream spec-functional-breakdown-structure spec-prd` | No stale `Open Issues` wording remains in targeted artefacts, normalized sections preserve tracker provenance, and `business-process` no longer scaffolds placeholder-only rows | `docs(skills): normalize open-items sections across artefacts` |
| M3: Ledger Automation | 05-06 | done | Dedicated maintenance skill exists and relevant artefact skills chain to it | `rg -n "util-open-items|Sync Open Items|project-control/open-items/open-items.md" util-open-items arch-research business-process business-research business-workshop spec-prd spec-implementation-plan ops-runbook` | Central sync behavior is documented and reusable | `feat(skills): add open-items tracker and chaining flow` |
| M4: Audit and Pilot | 07-08 | done | Stack audit covers governance drift and docs audit boundaries stay clean | `rg -n "tracker sync|schema compliance|closure drift|util-open-items|not a stack-governance tracker" util-metamodel-audit util-docs-audit` | Governance can be audited end-to-end without blurring tool responsibilities | `feat(audit): add open-items governance checks and rollout guardrails` |
