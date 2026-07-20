---
type: Implementation Plan
title: Plan-0003 — Open-Items Agent-Execution Layer (github backend v2)
description: Evolve the github open-items backend with an agent-execution layer — queryable priority/size/readiness labels, an agent-ready issue form, creation-time automation, triage v2 with a staleness policy, a delegation skill, and the kit-repo backfill — per research 0001/0002 (Option A).
tags: [open-items, github-backend, agent-execution, governance, tech-debt]
timestamp: 2026-07-20T12:00:00Z
status: draft
owner: Victor Hueni
last_reviewed: 2026-07-20
review_interval: 30d
---

# Implementation Plan: Open-Items Agent-Execution Layer

## Summary

This plan implements **Option A** from
[research 0001](../../../architecture/research/0001-open-items-agent-execution-setup.md)
(setup analysis) and
[research 0002](../../../architecture/research/0002-github-issue-creation-best-practices.md)
(issue-creation best practices): keep GitHub Issues as the per-project open-items backend
and add the **agent-execution layer** the current serialization lacks, so coding agents can
query the backlog, be pointed at issues, self-select from a trusted queue, and be dispatched
by automation.

What it fixes (live audit of 2026-07-20):

1. `priority` is trapped in issue bodies — not filterable by humans or agents.
2. No `size` signal and no readiness signal (`ready-for-agent` vs `needs-human`).
3. The Project (v2) fields ADR-0002 mapped `priority`/`status` onto were never wired up;
   labels replace them (cheaper, agent-queryable, personal-repo-safe).
4. The issue form lacks the agent-ready fields that measurably drive agent PR merge rates
   (code pointers, acceptance criteria with a runnable check, out-of-scope).
5. ~17 of 29 open items are stale June-migrated backlog rows sitting undifferentiated in
   the live queue.

The abstract governance model (taxonomy, lifecycle, provenance, evidence-gated closure,
Invariants I1–I5) is **unchanged**. All changes land in the `github` serialization layer
and are additive under §4's "skills MAY add informational columns" clause. The `markdown`
backend is untouched.

No PRD exists; the two research notes are the source artefacts. `0003` continues the
exec-plan sequence.

**Revision (2026-07-20, after increment 06 —
[ADR-0009](../../../architecture/decisions/adr-0009-standard-issue-vocabulary-github-backend.md)):**
the operator rejected the `open-item` marker + governance-derived type vocabulary as
exotic ("everything is an open item; fit what GitHub Issues is created for"). Decisions:
type axis becomes the standard 5-value set (`bug`/`feature`/`task`/`docs`/`tech-debt` —
the `decision` type was dropped same-day after conformance research 0003: decision work
is a `task` whose deliverable is the ADR/decision record, governance §2 mapping in the backend reference §2a), the marker label is
dropped (the tracker is the ledger), and intake is one form per type. Increments 04–06
were reworked in place (all unmerged); increments 07–13 read with the amended
vocabulary — notably: `sync` applies mapped `type:` labels, the backfill (09–10) also
remaps old type labels and strips `open-item`, and the delegation queue is
`is:open label:ready-for-agent`.

Principles:

1. One increment equals one coherent change set.
2. Every increment has an explicit test gate.
3. Contract before mechanics: the ADR and normative backend reference (M1) gate every
   later increment.
4. Labels are bootstrapped before any surface that names them (forms silently skip
   nonexistent labels).
5. Backfill and triage of live issues are **operator-gated**: dry-run first, human
   approval before any label write or closure on existing issues.
6. The `ready-for-agent` label is trustworthy by construction — an issue may only carry it
   if acceptance criteria and code pointers are present.

**Overall Status:** in-progress
**Current Increment:** 07

## Increment Plan

### Increment 01: ADR-0008 — Label-Based Agent-Execution Serialization (extends ADR-0002)

**Status:** done

Scope:

1. Record the serialization amendment: `priority` → `priority:p0..p3` label (Project
   single-select retired unwired); `status` decomposition for `in-progress`/`blocked` →
   `state:in-progress`/`state:blocked` labels (Project Status field retired unwired);
   issue open/closed + close-reason unchanged.
2. Record the two new **optional execution slugs** added after the canonical §4 set:
   `size` (`size:S|M|L` label) and `readiness` (`needs-triage` | `ready-for-agent` |
   `needs-human` labels) — orthogonal to lifecycle `status`, never a replacement for it.
3. Record the readiness contract: `ready-for-agent` requires non-empty
   `acceptance_criteria` + `references` form fields; `needs-triage` is the default at
   creation; promotion happens only via triage.
4. Record the form-validation gap: `gh`/API-filed issues bypass form `required:`
   validations — `util-open-items` refusal rules remain the real gate.
5. Record the title decision: drop the `[OI] ` prefix (the `open-item` label carries the
   signal; nothing greps titles).
6. Record deferred questions as filed open items (see §File Open Items): free GitHub org
   for native issue types/fields; Projects v2 board layer (Option B); Backlog.md as
   markdown-backend successor for non-GitHub projects.

Primary files:

1. `docs/architecture/decisions/adr-0008-open-items-agent-execution-labels.md`

Test gate:

1. `test -f docs/architecture/decisions/adr-0008-open-items-agent-execution-labels.md`
2. `rg -n "priority:p|ready-for-agent|size:|extends ADR-0002" docs/architecture/decisions/adr-0008-open-items-agent-execution-labels.md`

Exit criteria:

1. The full label vocabulary is enumerated with exact names and colors (17 labels across
   six axes; ≤5 applied per issue — amended from the original "≤15 total" heuristic at
   ADR time: the research's operative limit is per-issue count, and every axis is
   queryable metadata, not free-form tagging).
2. The serialization is specified precisely enough that increments 02–09 need no further
   design decisions.

### Increment 02: Normative Backend Reference Update (`github-backend.md`)

**Status:** done

Scope:

1. Rewrite §2 serialization table per ADR-0008: `priority` home = label; `status`
   decomposition (§3c) via `state:` labels; add `size` + `readiness` rows as optional
   slugs.
2. Add a "§ Execution layer" section: label vocabulary, readiness contract, the
   creation-default (`needs-triage`), and the promotion rule.
3. Update the field-partition note: authoring-time fields gain `references`,
   `acceptance_criteria`, `out_of_scope`, `size` (form); `readiness` is triage-owned,
   never set by the filer.
4. Invariants I1–I5 restated unchanged; new slugs added to the I1 slug list as optional.

Primary files:

1. `plugins/kit-core/skills/util-open-items/references/github-backend.md`

Test gate:

1. `rg -n "size|readiness|state:in-progress|acceptance_criteria" plugins/kit-core/skills/util-open-items/references/github-backend.md`
2. `rg -n "Project single-select" plugins/kit-core/skills/util-open-items/references/github-backend.md` returns no live-mapping hit (only historical note, if any).

Exit criteria:

1. The slug map is the single place a reader (or the audit) needs to interpret any label
   on an open-item issue.

### Increment 03: Governance Rule Touch (metamodel reference)

**Status:** done

Scope:

1. In the `metamodel` skill's `references/open-items-governance.md` §5.3, add one short
   paragraph: backends MAY carry optional execution-layer slugs (`size`, `readiness`)
   after the canonical set, serialized per the backend reference; readiness is orthogonal
   to lifecycle `status`.
2. No change to §2 taxonomy, §3 lifecycle, §4 canonical columns.

Primary files:

1. `plugins/kit-core/skills/metamodel/references/open-items-governance.md`

Test gate:

1. `rg -n "execution-layer|readiness" plugins/kit-core/skills/metamodel/references/open-items-governance.md`

Exit criteria:

1. The rule sanctions the new slugs without restating backend mechanics (schema stays
   single-sourced in the backend reference).

### Increment 04: Label Bootstrap Script

**Status:** done

Scope:

1. Add `scripts/bootstrap_labels.sh` to `util-open-items` — idempotent
   `gh label create --force` for the full ADR-0008 vocabulary: `open-item`,
   `type:{doc-gap,decision-gap,execution-item,tech-debt}`, `priority:{p0,p1,p2,p3}`,
   `size:{S,M,L}`, `needs-triage`, `ready-for-agent`, `needs-human`,
   `state:{in-progress,blocked}` — with fixed colors and descriptions.
2. `--repo OWNER/NAME` flag; dry-run default, `--apply` to execute (mirrors the
   migration script's convention).

Primary files:

1. `plugins/kit-core/skills/util-open-items/scripts/bootstrap_labels.sh`

Test gate:

1. `bash plugins/kit-core/skills/util-open-items/scripts/bootstrap_labels.sh --repo VictorHueni/homemade-claude-kit` (dry-run) prints the full vocabulary and exits 0 without mutating.

Exit criteria:

1. Re-running with `--apply` twice is a no-op the second time (idempotent).
2. Label count ≤ 15 excluding pre-existing repo labels.

### Increment 05: Issue Form v2

**Status:** done

Scope:

1. Update the canonical form template (`templates/open-item.form.yml`) and this repo's
   installed copy (`.github/ISSUE_TEMPLATE/open-item.yml`):
   - Add `size` dropdown (S/M/L, required).
   - Add `references` textarea — code pointers: files, symbols, prior PRs, patterns to
     imitate (required for `execution-item`/`tech-debt` per guidance text; forms cannot
     conditionally require).
   - Add `acceptance_criteria` textarea — observable pass/fail checklist ending in a
     runnable verification command (guidance text per research 0002 §4).
   - Add `out_of_scope` textarea (optional).
   - Drop the `[OI] ` title prefix.
   - Keep `type` + `priority` dropdowns (labeler action maps them — increment 06).
2. Field `id:` keys = canonical slugs (Invariant I1): `size`, `references`,
   `acceptance_criteria`, `out_of_scope`.
3. Form `labels:` gains `needs-triage` (bootstrap in increment 04 guarantees existence).

Primary files:

1. `plugins/kit-core/skills/util-open-items/templates/open-item.form.yml`
2. `.github/ISSUE_TEMPLATE/open-item.yml`

Test gate:

1. `python3 -c "import yaml,sys; yaml.safe_load(open('.github/ISSUE_TEMPLATE/open-item.yml'))"` exits 0.
2. `rg -n "id: (size|references|acceptance_criteria|out_of_scope)" .github/ISSUE_TEMPLATE/open-item.yml` shows all four.
3. `diff` between template and installed copy shows only the documented deltas (project-specific `labels:`/comments).

Exit criteria:

1. A form-filed issue renders `### <label>` sections parseable by the increment-06
   labeler and the audit slug map.

### Increment 06: Creation-Time Automation (labeler + config.yml)

**Status:** done

Scope:

1. Add `.github/workflows/issue-form-labeler.yml` (filename renamed post-ADR-0009) — on
   `issues: [opened, edited]`: parse the form's `### Priority` / `### Size` sections and
   apply the matching `priority:` / `size:` labels (Advanced Issue Labeler action or an
   equivalent `gh`-scripted step — decide in-increment, record choice in the workflow
   header). Type labels are form-static per ADR-0009.
2. Add `.github/ISSUE_TEMPLATE/config.yml` — `blank_issues_enabled: false`; no
   contact_links yet (solo repo).
3. Template copies of both files land in `util-open-items/templates/` for adopting repos.

Primary files:

1. `.github/workflows/issue-form-labeler.yml`
2. `.github/ISSUE_TEMPLATE/config.yml`
3. `plugins/kit-core/skills/util-open-items/templates/` (copies)

Test gate:

1. YAML parse of both files exits 0.
2. `rg -n "issues" .github/workflows/issue-form-labeler.yml` confirms the trigger; a
   manual test issue (filed after increment 04+05 land) arrives with correct labels.

Exit criteria:

1. A web-UI-filed open item needs zero manual label edits to be triage-ready.

### Increment 07: `util-open-items` SKILL.md v2.1 — sync labels + triage v2

**Status:** pending

Scope:

1. **Mode 1 `sync` (github):** `gh issue create` applies labels atomically
   (`--label type:<mapped>,priority:<p>,size:<s>,needs-triage` — governance type mapped
   per backend reference §2a); body uses form
   section headings; refusal rules unchanged and restated as the API-path gate
   (ADR-0008 §4).
2. **Mode 2 `triage` v2:** adds the readiness duties — propose promotions to
   `ready-for-agent` (only when acceptance criteria + references are present; draft them
   as part of the proposal when missing), routing to `needs-human`, and staleness
   dispositions (default policy: no movement in 90 days → propose `drop` as
   `not planned` with rationale). Proposal-only, never mutates without operator approval
   (unchanged principle).
3. **Backends section / adoption checklist rewrite:** step order = (1) bootstrap labels
   (increment 04 script), (2) install form v2 + config.yml + labeler workflow,
   (3) write `backend.yml`. The Project (v2) step is removed (moved to the filed
   Option B open item). Add the requirement that adopting repos carry a CLAUDE.md
   verification-commands section (the measured agent-success lever, research 0001 §3.3).
4. Backend behaviour table updated (priority/size/readiness columns; `archive` still
   no-op).
5. Version bump to 2.1.0.

Primary files:

1. `plugins/kit-core/skills/util-open-items/SKILL.md`

Test gate:

1. `rg -n "ready-for-agent|bootstrap_labels|90 days|2.1.0" plugins/kit-core/skills/util-open-items/SKILL.md`

Exit criteria:

1. An operator can adopt the backend on a fresh repo from the checklist alone.
2. Triage v2's proposal output format is specified (per-issue disposition table).

### Increment 08: Audit Mode Conformance

**Status:** pending

Scope:

1. Update the `metamodel` skill's Audit mode github check path
   (`references/modes/audit-check-catalogue.md`): read `priority` (and `size`,
   `readiness`, `state:`) from labels via the updated slug map, not from body text.
2. New check: any `ready-for-agent` issue has non-empty `acceptance_criteria` and
   `references` sections (the trustworthy-queue invariant, report-only).
3. New check: no issue carries more than one label from the same axis (one `priority:`,
   one `size:`, one readiness label).

Primary files:

1. `plugins/kit-core/skills/metamodel/references/modes/audit-check-catalogue.md`

Test gate:

1. `rg -n "ready-for-agent|one label per axis|labels" plugins/kit-core/skills/metamodel/references/modes/audit-check-catalogue.md`

Exit criteria:

1. Audit reads the whole execution layer through labels; no body-parsing for priority
   remains in the catalogue.

### Increment 09: Migration Script v2 + Backfill Helper

**Status:** pending

Scope:

1. `migrate_markdown_to_github.py`: bootstrap the full ADR-0008 vocabulary (reuse
   increment-04 script or inline equivalent); set `priority:` + `needs-triage` labels at
   issue creation; map ledger `in-progress`/`blocked` rows to `state:` labels instead of
   the retired "set Project Status manually" log line.
2. New `scripts/backfill_execution_labels.py` — for repos already on the github backend:
   parse each open issue's `### Priority` body section → apply `priority:` label; apply
   `needs-triage` where no readiness label exists; **remap old type labels to the
   ADR-0009 vocabulary** (`type:doc-gap`→`type:docs`, `type:decision-gap`→`type:task`,
   `type:execution-item`→`type:task`; `type:tech-debt` unchanged) and **strip the retired
   `open-item` marker** (using it first as the population selector, then removing it).
   Dry-run default, `--apply`, idempotent.

Primary files:

1. `plugins/kit-core/skills/util-open-items/scripts/migrate_markdown_to_github.py`
2. `plugins/kit-core/skills/util-open-items/scripts/backfill_execution_labels.py`

Test gate:

1. `python3 -m py_compile` on both scripts.
2. Backfill dry-run against `VictorHueni/homemade-claude-kit` lists all 29 open items
   with their derived labels and exits 0 without mutating.

Exit criteria:

1. Backfill dry-run output matches a hand-checked sample (≥5 issues).
2. Second `--apply` run reports zero changes (idempotent).

### Increment 10: Kit-Repo Backfill (operator-gated)

**Status:** pending

Scope:

1. Run increment-04 bootstrap `--apply` on `VictorHueni/homemade-claude-kit`.
2. Run increment-09 backfill dry-run; operator reviews the full plan; then `--apply`.
3. Verify: every open issue carries exactly one ADR-0009 `type:` label, exactly one
   `priority:` label, and `needs-triage`; the retired `open-item` marker and old type
   labels are gone (backfill uses the marker as population selector, then strips it and
   deletes the retired labels from the repo).

Primary files: none (operational; run log linked in progress.txt).

Test gate:

1. `gh issue list --state open --json labels` shows no issue missing a `type:`/`priority:`
   label, none with a readiness label other than `needs-triage`, and zero occurrences of
   `open-item` / `type:doc-gap` / `type:decision-gap` / `type:execution-item`.

Exit criteria:

1. All 29 (± drift) open items are label-complete; zero issues were closed or edited
   beyond labels.

### Increment 11: Kit-Repo Triage Session (operator-gated)

**Status:** pending

Scope:

1. Run triage v2 (increment 07) over the backfilled queue: per-issue disposition
   proposal — promote (`ready-for-agent`, drafting acceptance criteria + references into
   the issue body), route (`needs-human`), or drop stale (`not planned` + rationale
   comment; candidates: the ~17 June-migrated candidate-skill rows).
2. Operator approves/amends the disposition table; apply approved actions.
3. Write the session report to `var/reports/open-items/triage-2026-MM-DD.md` (gitignored
   path convention unchanged — link summary in progress.txt).

Primary files: none (operational).

Test gate:

1. Post-session: `gh issue list --label needs-triage --state open` is empty; every
   `ready-for-agent` issue passes the increment-08 audit check.

Exit criteria:

1. The live queue contains only deliberately-kept items, each `ready-for-agent` or
   `needs-human`; dropped items are closed `not planned` with rationale, never deleted.

### Increment 12: Delegation Skill — `agent-issue-loop` (three mode families)

**Status:** pending

Scope:

1. New skill in the `agent-loop` plugin (working name `agent-issue-loop`; confirm against
   `rules/skill-creation-sync.md` naming at build time). Three mode families:

   **A. Readiness validation (read + propose; no implementation):**
   - `validate #N` — assess one issue against the `ready-for-agent` contract
     (self-contained summary, `references` present and resolving to real files/symbols,
     `acceptance_criteria` observable and ending in a runnable check, one-PR `size`,
     no reliance on context an agent cannot reach — research 0002 §4/§7). Output a
     pass/fail report with the exact gaps, and for near-misses a **drafted brief**
     (proposed criteria + references) ready to paste into the issue.
   - `validate --queue` — run the same assessment over every issue currently labelled
     `ready-for-agent` and flag any that no longer pass (drift check; keeps the queue
     trustworthy between triage sessions). Proposal-only: promotion/demotion label
     changes are applied only with operator approval, and demotion proposals cite the
     failed criterion.

   **B. Duplication control & merge (write, operator-gated):**
   - `dedupe` — scan open issues, cluster candidates using the skill's
     established identity triple (`source_artefact`, `source_anchor`, summary
     fingerprint) plus semantic similarity of summary/resolution-path; output a
     duplicate-pairs proposal table (canonical issue, duplicate, evidence, merge plan).
   - On operator approval, execute each merge: append the duplicate's unique
     information (provenance, context, links) as a comment on the canonical issue;
     cross-reference both; close the duplicate via the `util-open-items` `drop`
     semantics (`not planned`, rationale `Duplicate of #N`) so closure evidence rules
     hold. Never auto-merges without approval; never deletes content.

   **C. Implementation & verification (write):**
   - `take #N` — refuse unless the issue passes the mode-A validation (cite what's
     missing); set `state:in-progress`; plan → implement → verify against the issue's
     own acceptance-criteria checks → PR with `Closes #N`; on merge the label lifecycle
     ends naturally with the issue.
   - `next` — query `is:open label:ready-for-agent`, pick highest `priority:`
     (tie-break: smallest `size:`), then run `take`.

2. Action-budget contract in the skill (per research 0002 §7), per mode family:
   validation mutates nothing without approval; dedupe touches only the approved pairs
   and always closes with a rationale; take/next touch only the taken issue, never
   promote issues to `ready-for-agent`, never file new issues without running the
   duplicate search, one issue per invocation.
3. Boundary with `util-open-items`: triage v2 (increment 07) remains the owner of
   readiness *promotion* during triage sessions; `validate` is the per-issue /
   between-sessions check, and `dedupe` executes what triage-style clustering only
   proposes — both route closures through the `drop` contract rather than raw
   `gh issue close`.
4. Register in the plugin's `plugin.json` / marketplace set.

Primary files:

1. `plugins/agent-loop/skills/agent-issue-loop/SKILL.md` (path per plugin layout)
2. `.claude-plugin/marketplace.json` (if set membership files require it)

Test gate:

1. Skill frontmatter parses; `rg -n "validate|dedupe|take|ready-for-agent|Closes #|refuse" .../agent-issue-loop/SKILL.md` shows all mode families.
2. `validate` dry-run on one known-good and one known-incomplete issue produces the
   expected pass and gap report.
3. `dedupe` dry-run against the post-increment-11 queue outputs a proposal table (empty
   is acceptable) without mutating.
4. Dry-run `next` against the post-increment-11 queue selects the expected top issue.

Exit criteria:

1. `take` on a `needs-human` issue refuses with the missing-precondition message.
2. `validate --queue` demotion proposals cite the failed criterion for each flagged issue.
3. One approved `dedupe` merge (or a documented empty run) executed with the duplicate
   closed as `not planned` + rationale.
4. One full `take → PR` round-trip executed on a real `ready-for-agent` issue.

### Increment 13: Rollout Guide + README Refresh

**Status:** pending

Scope:

1. Update `docs/project-control/open-items/README.md`: label vocabulary quick-reference,
   the readiness state machine, links to ADR-0008 and the two research notes.
2. Add a short "adopting on a new repo" walkthrough (checklist pointer) and the
   convert-and-triage guidance for ad-hoc markdown lists (research 0001 §5 population 3:
   agent-assisted normalize → file survivors → freeze source as archive; migration is the
   bankruptcy moment — don't bulk-import).
3. Note the optional `@claude` GitHub Action as the triggered-automation flow (document,
   don't install — per-repo choice).

Primary files:

1. `docs/project-control/open-items/README.md`

Test gate:

1. `rg -n "ready-for-agent|adopting|bankruptcy|bootstrap_labels" docs/project-control/open-items/README.md`

Exit criteria:

1. A future operator (or agent) can execute a full adoption or conversion on another
   repo from this README plus the SKILL.md checklist, without reading the research notes.

## Delivery Rules

1. One increment per commit.
2. **Commit scope:** `open-items` — increments reference `Refs: Plan-0003 increment NN`
   in the trailer, never in the scope.
3. Each increment must be independently runnable and reversible; scripts are dry-run by
   default and idempotent under `--apply`.
4. Increments 10 and 11 mutate live issues and are **operator-gated**: dry-run output must
   be reviewed and approved before `--apply`; closures are always `not planned` +
   rationale, never deletion.
5. Labels are created before any file that names them ships (04 before 05/06).
6. The `markdown` backend and Invariants I1–I5 must hold unchanged at every increment;
   any pressure to break them stops the plan and goes back to ADR.

## Milestone Chunks (Standalone Delivery Groups)

| Milestone | Increments | Status | Coherent Outcome | Standalone Test Gate | Exit Criteria | Commit Guidance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| M1: Contract | 01–03 | done | Serialization amendment decided and normative docs conform | rg checks on ADR-0008 + backend ref + governance rule | Label vocabulary + slugs fully specified; no design decisions left downstream | `docs(open-items): ...` |
| M2: Intake surface | 04–06 | done | New issues arrive label-complete and agent-parseable | Test issue filed via form arrives fully labelled | Zero manual label edits needed on a fresh filing | `feat(open-items): ...` |
| M3: Tooling conformance | 07–09 | pending | Skill, audit, and scripts operate the new layer | Script dry-runs + rg checks | Adoption checklist self-sufficient; backfill validated dry-run | `feat(open-items): ...` |
| M4: Kit-repo rollout | 10–11 | pending | Live queue backfilled and triaged; `ready-for-agent` trustworthy | `gh issue list` label assertions | No `needs-triage` remains; stale items dropped with rationale | operational commits + progress.txt log |
| M5: Delegation + rollout | 12–13 | pending | Agents can validate readiness, dedupe/merge, and take/select issues; other repos can adopt | Dry-run `validate --queue` + `dedupe` + `next`, one real `take → PR` round-trip | One issue driven to merged PR by the skill; queue passes validate with zero unproposed drift | `feat(agent-loop): ...` / `docs(open-items): ...` |

## File Open Items to the central ledger

Filed at plan creation (github backend, per ADR-0005 direct filing):

1. `decision-gap` — Decide whether to move the project portfolio into a free GitHub org
   for native issue types + org issue fields (Source: this plan, `#increment-01-adr-0008`).
2. `execution-item` — Add the Projects v2 board read-out layer (research 0001 Option B)
   once label volume or a second triager justifies it (Source: this plan,
   `#increment-07`).
3. `decision-gap` — Evaluate Backlog.md as the successor to the `markdown` backend for
   non-GitHub / offline projects (Source: this plan, `#increment-13`).
