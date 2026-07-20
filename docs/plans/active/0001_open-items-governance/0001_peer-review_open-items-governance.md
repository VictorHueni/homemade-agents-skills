---
title: Peer Review — Plan-0001 Open Items Governance
status: draft
owner: Victor Hueni
last_reviewed: 2026-05-25
review_interval: 30d
---

# Peer Review: Open Items Governance

## Findings

No active plan-level findings remain after the plan patch on 2026-05-25. The previously identified findings are now resolved at specification level, with a few implementation risks still worth watching during Increment 03.

### resolved major — `arch-research` contract shape is now explicit

**Severity:** major

**Issue:** The earlier ambiguity is resolved. The plan now explicitly requires a document-level `## Open Items` section across artefacts and explicitly states that `arch-research` will consolidate question-level unresolved notes into that section while preserving provenance via `Source anchor` and `Source heading`.

**Evidence:**
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:13`
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:39`
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:91`
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:93`
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:117`
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:125`
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:126`

**Implementation risk to watch:** Increment 03 still needs a clean migration rule for how per-question notes are rewritten into the consolidated doc-level table so no question-specific nuance is lost.

### resolved major — Increment 03 scope now includes the missing support files

**Severity:** major

**Issue:** The under-scoping problem is resolved. Increment 03 now includes the discipline and audit support files that would otherwise preserve or reintroduce the old vocabulary.

**Evidence:**
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:100`
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:106`
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:107`
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:108`
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:121`

**Implementation risk to watch:** the future edit should keep the audit expectations in `util-metamodel-audit/references/check-catalogue.md` aligned with the new headings, otherwise the migration can still drift at enforcement time.

### resolved major — `business-process` placeholder policy is now coherent at plan level

**Severity:** major

**Issue:** The previous contradiction is resolved at specification level. The plan now says placeholder-only open-item rows should not be scaffolded, and Increment 03 explicitly removes placeholder-only requirements from `business-process`.

**Evidence:**
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:23`
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:95`
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:127`
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:257`

**Implementation risk to watch:** the repo still needs the actual template and skill edits so no latent `≥3 TODOs on first scaffold` instruction survives in `business-process`.

### resolved normal — embedded template variant coverage is now explicit

**Severity:** normal

**Issue:** The plan now explicitly names the embedded `business-research` and `business-workshop` variants that must be covered by Increment 03, so "file touched" is no longer enough to claim completion.

**Evidence:**
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:96`
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:97`
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:120`

**Implementation risk to watch:** the workshop wording still leaves room for a hidden variant if another unresolved-work section exists in the same file. The implementer should verify there are no additional headings beyond the ones currently identified.

### resolved normal — `spec-prd` is now explicitly treated as a first adopter

**Severity:** normal

**Issue:** The ambiguity is resolved. The plan now explicitly says `spec-prd` stays in Increment 03 as a first adopter rather than pretending it is a migration from an existing heading.

**Evidence:**
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:98`

**Implementation risk to watch:** none beyond ordinary delivery risk; this is now a deliberate scope choice, not a spec defect.

### resolved low — `business-competitive-landscape` now has an explicit stance

**Severity:** low

**Issue:** The coverage ambiguity is resolved. The plan now explicitly records that `business-competitive-landscape` remains changelog-only for now and is out of the formal `Open Items` rollout for this increment.

**Evidence:**
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:138`
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:151`
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:156`
- `docs/plans/active/0001_open-items-governance/0001_exec_open-items-governance.md:162`

## Open Questions / Assumptions

1. The plan-level contract is now coherent; remaining work is implementation precision, not scope definition.
2. Increment 03 completion should still mean both template/skill edits and supporting discipline/audit updates, not just visible heading renames.
3. I still treat files that only contain generic `_TODO_` placeholders as out of scope unless they explicitly govern unresolved-work capture or audit behavior.

## Optional Short Summary

The earlier review findings have been resolved at plan level. The remaining work is execution quality: migrate `arch-research` into a single doc-level table without losing per-question provenance, remove `business-process` placeholder-only rows in practice, and keep discipline/audit support files aligned with the new contract so old headings do not re-enter the repo.
