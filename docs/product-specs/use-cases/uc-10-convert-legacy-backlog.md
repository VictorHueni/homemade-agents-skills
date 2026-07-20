---
type: Use Case
title: "UC-10 — Convert a legacy backlog"
description: "The operator, agent-assisted, converts a pre-existing backlog — an ad-hoc TODO list or a structured markdown ledger — into tracker issues: deliberate item-by-item bankruptcy, survivors filed through the contract, the source frozen, nothing deleted."
tags: [open-items, migration, backlog-conversion, github-backend]
timestamp: "2026-07-20T15:30:00Z"
status: draft
owner: "Victor Hueni"
last_reviewed: "2026-07-20"
review_interval: 180d
---

# UC-10 — Convert a legacy backlog

> Methodology: see the kit's `spec-use-case/references/methodology.md` (Cockburn fully-dressed format). Do not restate the method here.

| Field | Value |
|---|---|
| **Scope** | system — the backlog-execution system (github open-items backend + `util-open-items` sync / Mode 7) |
| **Level** | user-goal 🌊 |
| **Primary Actor** | Operator (the human maintainer — agent-assisted, approval authority) |
| **Supporting Actors** | Coding Agent (analysis + filing assistant); GitHub (issue tracker) |
| **Realises** | _TBD_ (contracts live in `util-open-items/SKILL.md` Mode 7 + the convert-and-triage guidance in `docs/project-control/open-items/README.md`) |

## Stakeholders and Interests

- **Operator** — the new backlog contains only items still worth doing, each in the
  normalized shape agents and triage can operate on; the old list stops being a
  parallel source of truth the day the conversion lands.
- **Future maintainers** — the original source survives as a frozen, dated archive
  with a pointer forward; any historical item can be traced to its issue or to a
  recorded don't-migrate decision. Nothing is silently deleted.
- **Coding Agents** — post-conversion, one backend and one ID space: every surviving
  item is a labelled issue; no stale `OI-NNNN` back-reference points into the void.

## Preconditions

- The github backend adoption checklist (UC-09) is complete on the target repo:
  labels bootstrapped, intake surface installed, verification commands documented.
- A legacy backlog exists — an ad-hoc markdown TODO list, or a structured
  `markdown`-backend ledger — and the Operator can edit the repo and write the tracker.

## Guarantees

- **Minimal guarantees** (hold even if the session is abandoned mid-way): the source
  document is never deleted or truncated — at worst it is still fully authoritative;
  no item is filed without the Operator's approval; re-running the conversion never
  creates duplicates of already-filed items; for ledger sources, no back-reference is
  rewritten before its identity mapping is persisted.
- **Success guarantees**: every source item has exactly one recorded fate — a filed
  issue (created through the filing contract, labelled, `needs-triage`) or an
  approved don't-migrate decision; the source is frozen as a dated archive carrying a
  pointer to the issues; for ledger sources, the `OI-NNNN → #N` map is persisted,
  back-references are rewritten, and `backend.yml` declares `github`. The tracker is
  now the only live backlog.

## Trigger

The Operator adopts the github backend on a repo that already has a backlog, and
decides to convert it rather than let two sources of truth coexist.

## Main Success Scenario

1. The Operator points the Coding Agent at the legacy source and asks for a
   conversion.
2. The agent classifies the source — an ad-hoc, free-form TODO list, or a structured
   `markdown`-backend ledger — which fixes the conversion route (extensions 2a / 2b
   carry the route-specific mechanics).
3. The agent walks every source item and produces a per-item conversion proposal for
   the Operator: what would be filed (normalized), or why the item should not migrate.
4. The Operator reviews the proposal batch — amending, rejecting, and approving item
   fates deliberately; the conversion is the backlog's bankruptcy moment, and only a
   fraction of an old list surviving is success, not loss.
5. The agent files the approved survivors into the tracker through the filing
   contract (**include UC-03** — duplicate/dependency search, atomic labels,
   `needs-triage`), recording each item's resulting issue number.
6. The agent freezes the source as a dated archive carrying a pointer to the issues —
   the file moves out of the live path but is never deleted.
7. The Operator spot-checks the result (label queries, a sampled item or two) and
   confirms the tracker is now the only live backlog.

## Extensions

- **1a.** The adoption checklist is incomplete (labels not bootstrapped, no
  `backend.yml` plan):
  - **1a1.** The agent refuses to convert and routes the Operator through UC-09
    first — filing into a repo without the vocabulary silently loses labels.
- **2a.** The source is an **ad-hoc markdown TODO list** (the common starting state):
  - **2a1.** For each list item the agent proposes either a **normalized issue
    draft** — type, priority, size, a self-contained summary, and code pointers
    recovered from the repo — or **"don't migrate: stale / vague / superseded"**
    with the reason stated.
  - **2a2.** The Operator approves the batch (step 4); survivors are filed via the
    UC-03 contract (step 5); the list is frozen as a dated archive with a pointer to
    the issues (step 6). Bulk-importing every line verbatim is never on the table.
- **2b.** The source is a **structured `markdown`-backend ledger**:
  - **2b1.** The agent runs the one-way migration tooling (Mode 7) in **dry-run
    first**: the Operator reviews the planned issues, the `OI-NNNN → #N` identity
    map, and the back-reference rewrite diff before anything mutates.
  - **2b2.** On approval, the migration applies: issues are created with the mapped
    type labels and lifecycle decomposition, the identity map is persisted to the
    project's control plane, and every `OI-NNNN` back-reference across the docs tree
    is rewritten to its `#N`.
  - **2b3.** The Operator freezes the ledger into the archive and flips
    `backend.yml` to `github` — from that moment every mode of the open-items
    contract operates the tracker. Resume at step 7.
- **4a.** The Operator rejects a proposed issue draft (item not worth carrying
  forward):
  - **4a1.** The item is not filed; its don't-migrate fate and reason are recorded in
    the conversion report, so the frozen source plus the report account for every
    item.
- **5a.** Filing detects that a survivor duplicates an issue already live on the
  tracker:
  - **5a1.** Per the filing contract, nothing new is created; the existing issue
    number is recorded as the item's fate. This is also what makes an interrupted
    conversion safely re-runnable.
- **5b.** A tracker write fails mid-batch:
  - **5b1.** The agent stops filing, reports which items landed and which did not,
    and leaves the source authoritative until the batch completes on a re-run —
    the freeze (step 6) never happens around a half-filed batch.
- **6a.** Anyone proposes deleting the source instead of freezing it:
  - **6a1.** Refused. The frozen, dated archive with its forward pointer *is* the
    audit trail; deletion would orphan every historical reference and hide the
    don't-migrate decisions.

## Technology and Data Variations

- Step 2: route (2a) is judgment work — an agent-assisted convert-and-triage session;
  route (2b) is mechanized by `scripts/migrate_markdown_to_github.py` (dry-run by
  default, `--apply` to execute, `--assignee-map` for owner → login translation).
- Step 5: filings go through `util-open-items sync`; the Mode 7 script embeds the
  same serialization (§2a type mapping, form-structured bodies, status decomposition).
- Step 6: the identity map persists at
  `docs/project-control/open-items/migration-map.md`; frozen sources live under
  `docs/project-control/open-items/archive/`.

## Related Information

- Contracts: `util-open-items/SKILL.md` Mode 7 (`migrate`) and §Backends;
  invariants I2 (one-way, once, persisted map) in
  `util-open-items/references/github-backend.md` §3b; operator guidance:
  `docs/project-control/open-items/README.md` §Adopting on another repo.
- Design stance: migration is the **deliberate bankruptcy moment** — item-by-item
  with an audit trail, never a bulk purge and never a bulk import (research 0001
  §3.4). Expect and want only a fraction of an old list to survive.
- This repo's own 2026-06 conversion (29 issues, migration-map.md) is the worked
  example of route 2b.

## Use-Case 2.0 Slices

| Slice | Narrative | Test case(s) | Status |
|---|---|---|---|
| UC-10.S1 | Ad-hoc route (2a): TODO list → approved drafts filed, list frozen with pointer | One sample list converted end-to-end on a scratch repo | ⬜ |
| UC-10.S2 | Ledger route (2b): dry-run reviewed → apply → map persisted, refs rewritten, backend flipped | Mode 7 script run against a fixture ledger | ⬜ |
| UC-10.S3 | Bankruptcy discipline (4a): don't-migrate fates recorded, nothing filed for them | Conversion report accounts for every source item | ⬜ |
| UC-10.S4 | Safety (5a/5b/6a): re-run idempotence, half-batch stop, source never deleted | Interrupted conversion re-run; assert no duplicates, source intact | ⬜ |
