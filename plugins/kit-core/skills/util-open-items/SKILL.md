---
name: util-open-items
license: MIT
description: "Maintain the repo-wide living ledger of unresolved governance work at `docs/project-control/open-items/open-items.md`. Use this skill to file open items directly into the central ledger, triage incoming rows, close or drop items with a tracker ref, archive terminal rows at the end of a review cycle, and produce status reports. Triggers on: log open item, file open item, sync open items, triage open items, close open item, drop open item, archive open items, open-items report, roll up open items, OI-NNNN, central ledger, docs/project-control/open-items."
user-invocable: true
metadata:
  category: "infrastructure"
  complexity: "medium"
  version: "2.1.0"
  status: active
  last_reviewed: 2026-07-20
  review_interval: 180d
  impact: "medium"
---

# util-open-items — Open Items Ledger Operator

Operate the central control plane for unresolved governance work. This skill is the only
sanctioned writer of the central ledger — `docs/project-control/open-items/open-items.md`
under the `markdown` backend, or GitHub Issues under `github` (the repo's issue tracker
*is* the ledger — no marker label, kit ADR-0009). Every
other skill that identifies unresolved work chains to this skill to file it **directly**:
there is no per-artefact local section to author first
([ADR-0005](../docs/architecture/decisions/adr-0005-open-items-ledger-sole-authoring-surface.md)).

The canonical contract — section name, schema, taxonomy, lifecycle, central-plane rules —
lives in the `metamodel` skill's `references/open-items-governance.md`. This skill
is the operating manual that turns the contract into repeatable mechanics. When the rule
and this file diverge, the rule wins; this skill must then be reconciled.

---

## Backends

The central plane is a **serialization** of the §4 model (governance §5.3). This skill
operates one of two backends:

- **`markdown`** (default) — the living ledger at
  `docs/project-control/open-items/open-items.md` plus `archive/`. Mints `OI-NNNN`.
- **`github`** — GitHub Issues; the whole tracker is the ledger, read out through the
  ADR-0009 label axes (`type:` / `priority:` / `size:` / readiness / `state:`) via
  filtered queries. Identity is the issue number `#N`; `OI-NNNN` is retired.

**Declaration.** A project selects its backend in
`docs/project-control/open-items/backend.yml`; absent ⇒ `markdown`:

```yaml
backend: github          # markdown (default) | github
repo: owner/name         # github only — where the issues live
```

**What stays the same regardless of backend:** filing is always direct (Invariant I4) — only
what `sync` *writes to* changes. The abstract model, taxonomy, lifecycle, and provenance
composite are identical (governance §4/§5.3).

**One backend per project.** Never both. Moving between them is a one-way
`markdown → github` migration (Mode 7, `OI-0031`), never a live two-way sync.

**Operational github mapping.** Before operating the `github` backend, read
[`references/github-backend.md`](references/github-backend.md) — the normative slug
contract, serialization (§2, §2a type mapping, §2b execution layer), identity
translation, status decomposition, and invariants I1–I5. The human authoring surface is
the per-type issue forms (`templates/form-{bug,feature,task,docs,tech-debt}.yml`); the
skill's own filings go through `gh` with the same section headings.

**github adoption checklist** (per project, one-time — order matters):

1. **Bootstrap the 17-label vocabulary first**:
   `scripts/bootstrap_labels.sh --repo OWNER/NAME --apply` (idempotent; MUST precede the
   forms — GitHub silently skips `labels:` entries that don't exist).
2. **Install the intake surface**: copy `templates/form-<type>.yml` →
   `.github/ISSUE_TEMPLATE/{1-bug,2-feature,3-task,4-docs,5-tech-debt}.yml` (numeric
   prefixes = chooser order), `templates/issue-template.config.yml` →
   `.github/ISSUE_TEMPLATE/config.yml`, and `templates/issue-form-labeler.workflow.yml` →
   `.github/workflows/issue-form-labeler.yml`.
3. **Ensure the repo's `CLAUDE.md` carries a verification-commands section**
   (build/test/lint invocations) — the single biggest measured driver of agent success on
   delegated issues (research 0001 §3.3).
4. Add `docs/project-control/open-items/backend.yml` with `backend: github` + `repo`.

---

## When to invoke

Invoke `util-open-items` whenever:

- Unresolved work is identified while producing or updating any artefact → run `sync` to
  file it directly, citing that artefact as `Source artefact`.
- Governance or kit-development work with no artefact home is identified → run `sync` as a
  central-only row (governance §5.2).
- A row needs review for priority, owner, or de-duplication against the ledger → run
  `triage`.
- An open item has been resolved by a PR / ADR / plan increment / runbook / audit
  report → run `close` (or `drop` if abandoned).
- A review cycle ends and terminal rows are eligible for archival → run `archive`.
- Someone wants a snapshot of governance health → run `report`.

Do NOT invoke this skill to mutate `_TODO_` scaffold placeholders in artefact bodies —
those are scaffold debt, audited by the `metamodel` skill's Audit mode Check 8, and are not open items.

---

## Modes

This skill exposes seven modes — six steady-state operations plus a one-time `migrate`
cutover (Mode 7, `markdown → github`). Each mode reads or writes
`docs/project-control/open-items/open-items.md` and respects the lifecycle in
the `metamodel` skill's `references/open-items-governance.md` §3.

### Mode 1 — `sync`

File a new open item directly into the central ledger. ("Sync" now means "commit this item
to the ledger" — the name is retained for continuity with existing trigger phrasing and
callers; there is no local table left to reconcile against, per
[ADR-0005](../docs/architecture/decisions/adr-0005-open-items-ledger-sole-authoring-surface.md).)

Input:

- The item's fields: `Type`, `Summary`, `Source artefact` (a relative repo path, or the
  central-only scope marker per governance §5.2), `Source anchor`, `Source heading`,
  `Resolution path`, `Priority`, `Size` (S/M/L, github backend), `Owner`,
  `Due / Review date`; optionally `References`, `Acceptance criteria`, `Out of scope`
  (the agent-execution fields — recommended at filing, required later for
  `ready-for-agent` promotion). `Status` defaults to `open`; `Tracker ref` defaults to
  `_TBD_`. Readiness always starts `needs-triage` — `sync` NEVER applies
  `ready-for-agent` (triage-owned, ADR-0008 §3).

Process:

1. **Validate the fields.** `Type` must be one of the four taxonomy values. `Source anchor`
   and `Source heading` are supplied together, or both left empty for a central-only row.
2. **De-duplicate AND check dependencies before creating.** Identity is the triple
   `(Source artefact, Source anchor, Summary fingerprint)` (see De-duplication policy
   below) — search the ledger table, or `gh issue list --search` under `github`, before
   creating. Under `github`, also search for **related or dependent** open issues (same
   files, same subsystem, blocking work): link them in the body (`Relates to #N` /
   `Blocked by #N`) instead of duplicating context. Filing without this search is a
   contract violation — it is why the forms carry no duplicate-search checkbox.
3. **Assign the ID.** `markdown` backend: mint the next monotonic `OI-NNNN` (max across
   `open-items.md` plus every `archive/*.md`, plus one — never recycle). `github` backend:
   `gh issue create`; the resulting issue number `#N` **is** the ID — no `OI-NNNN` is
   minted.
4. **Write the row.** `markdown`: append to `open-items.md` using the §4 schema.
   `github`: `gh issue create` with the labels applied **atomically at creation** —
   `--label "type:<mapped>,priority:<p0..p3>,size:<S|M|L>,needs-triage"` (governance
   `Type` mapped per `references/github-backend.md` §2a: doc-gap→docs,
   decision-gap→task, execution-item→task, tech-debt→tech-debt) — body using the form's
   `### <slug label>` section headings (provenance, `Resolution path`, `References`,
   `Acceptance criteria`, `Out of scope`), assignee = `owner`, milestone = review date
   when one exists.
5. **Report** the assigned `OI-NNNN` or issue number back to the caller.

Refuse to sync if:

- `Type` is not one of `doc-gap`, `decision-gap`, `execution-item`, `tech-debt`.
- The row is filed already `closed`/`dropped` with `Tracker ref: _TBD_` — §3 requires a
  non-`_TBD_` tracker ref before reaching a terminal state.
- A duplicate is found and the caller's intent is unclear — surface the existing
  `OI-NNNN`/issue number and ask the operator to reference it directly, or use `triage`/
  `drop` to merge explicitly, instead of silently creating a second row.
- The caller asks for `ready-for-agent` at filing time — promotion is triage-owned; file
  as `needs-triage` and let `triage` (or the operator) promote.

### Mode 2 — `triage` (v2)

Walk every `open` and `in-progress` row/issue and propose owner, priority,
de-duplication, **readiness**, and **staleness** changes. Triage is proposal-only: it
never mutates silently; every disposition is applied only after operator approval.

Process:

1. Cluster rows by `Source artefact` and by `Resolution path` to surface duplicates.
2. Flag rows with `Owner: _TBD_` older than 14 days as triage-needed.
3. Flag rows with `Priority: critical` or `high` and no `Tracker ref` movement as
   escalation candidates.
4. **Readiness routing (github backend).** For each `needs-triage` issue, propose one of:
   - **Promote to `ready-for-agent`** — ONLY when the readiness precondition holds
     (non-empty `Acceptance criteria` + `References`, `size:` set — ADR-0008 §3). For
     near-misses, draft the missing brief (proposed acceptance criteria + code pointers)
     as part of the proposal so approval is one edit away.
   - **Route to `needs-human`** — valid item, but requires a human decision or work an
     agent cannot verify.
   - **Keep `needs-triage`** with a stated reason (rare; e.g. blocked on info).
   Also flag drift: `ready-for-agent` issues that no longer pass the precondition →
   propose demotion, citing the failed criterion.
5. **Staleness policy.** Rows/issues with no movement (no label change, comment, or
   linked activity) for 90 days (configurable per invocation) → propose `drop`
   (`not planned` + one-line rationale). Bankruptcy happens item-by-item with an audit
   trail, never as a bulk purge.
6. Output a triage report — a per-item **disposition table**
   (`# | title | current | proposed | rationale / draft brief`) — in-memory or written to
   `var/reports/open-items/triage-YYYY-MM-DD.md` if the operator requests a file. After
   operator approval, apply the accepted dispositions (label changes via `gh`; drops via
   Mode 4 so closure evidence rules hold).

### Mode 3 — `close`

Move a single row to terminal state `closed`.

Input: `OI-NNNN`, `Tracker ref` (PR / ADR / plan increment / runbook / audit report URL),
optional closure-date override (default: today).

Process:

1. Verify the row exists in `open-items.md` and is in state `open`, `in-progress`, or
   `blocked`.
2. Verify `Tracker ref` is a non-`_TBD_` value — §3 requires it.
3. Update the ledger row: `Status: closed`, `Tracker ref: <value>`,
   `Due / Review date: <closure-date>`.
4. Leave the row on the live ledger for one review cycle (default 30 days) before it
   becomes archive-eligible.

### Mode 4 — `drop`

Same mechanics as `close` but the terminal state is `dropped`.

Required extra input: a rationale sentence in `Resolution path` explaining why the item is
abandoned (e.g. "Superseded by ADR-0007"). `Tracker ref` still required — typically the
discussion link (PR comment, ADR rejection, meeting note).

### Mode 5 — `archive`

Move eligible terminal rows out of the live ledger into a time-bucketed snapshot.

Process:

1. Identify rows in `open-items.md` with `Status: closed` or `Status: dropped` whose
   `Due / Review date` is older than 30 days (configurable per invocation).
2. Move those rows into `docs/project-control/open-items/archive/<YYYY-Q[1-4]>.md`, creating
   the bucket file with the canonical 12-column ledger schema if it does not already
   exist.
3. Remove the rows from `open-items.md` only after they have been written to the archive
   file. Never silently delete — the move is the audit trail.
4. Update §Status snapshot in `open-items.md` to reflect the new totals.

### Mode 6 — `report`

Produce a governance-health snapshot.

Output sections:

- **Counts.** `open` / `in-progress` / `blocked` / `closed` / `dropped` totals.
- **By type.** Distribution across `doc-gap`, `decision-gap`, `execution-item`,
  `tech-debt`.
- **Oldest open items.** Top-N by age.
- **Stale closure candidates.** Rows in `closed` / `dropped` older than 30 days (i.e.
  archive-eligible — feeds Mode 5).
- **Coverage map.** Distribution of ledger rows by `Source artefact`, so an operator can see
  which artefacts currently have open governance work and which have none.

Write to `var/reports/open-items/report-YYYY-MM-DD.md`. Never mutates the ledger.

### Mode 7 — `migrate` (markdown → github, one-way)

One-time cutover of a project from the `markdown` backend to `github`. Enforces Invariant I2
(governance §5.3): one-way only, emits the `OI-NNNN → #N` map, never a reverse or concurrent
sync.

**Preconditions:** the github adoption checklist (§Backends) is done — form installed, Issue
labels bootstrapped, `gh` authenticated against the target repo. The `markdown`
ledger `open-items.md` is the source.

**Driver:** [`scripts/migrate_markdown_to_github.py`](scripts/migrate_markdown_to_github.py)
— stdlib + `gh`, **dry-run by default**.

```text
# 1. Dry-run — prints planned issues + the OI-NNNN→#N map + ref-rewrite diff, mutates nothing
python3 scripts/migrate_markdown_to_github.py --repo OWNER/NAME --assignee-map victor=LOGIN

# 2. Apply — create issues, write the map, rewrite OI-NNNN back-references across docs/
python3 scripts/migrate_markdown_to_github.py --repo OWNER/NAME --assignee-map victor=LOGIN --apply
```

**Portability (auto-detected — works on personal repos):**

- **Types are labels** (ADR-0009): the script maps ledger types per §2a
  (doc-gap→`type:docs`, decision-gap→`type:task`, execution-item→`type:task`,
  tech-debt→`type:tech-debt`) and bootstraps the full 17-label vocabulary via
  `scripts/bootstrap_labels.sh` semantics (the label table is parsed from that script at
  runtime — single source of truth).
- **`owner` → GitHub login.** Ledger owners rarely equal a GitHub login. Pass
  `--assignee-map LEDGER_OWNER=LOGIN` (repeatable). `_TBD_` and unmapped owners get **no
  assignee** (warned), never a failing `--assignee`.
- The ADR-0009 label vocabulary is created idempotently (`gh label create --force` via
  the bootstrap script); no marker label exists.

**Per live ledger row:**

1. De-dups by summary + provenance (`gh issue list --search`) — re-runs are idempotent.
2. `gh issue create` — `summary`→title, `type`→**`type:` label per the §2a mapping**,
   provenance + `resolution_path`→form-structured body, mapped `owner`→assignee.
3. Lifecycle: `open` stays open; `in-progress`/`blocked` stay open with the matching
   `state:` label applied (§3c decomposition — logged); `closed`→close `completed`;
   `dropped`→close `not planned` (original `tracker_ref` preserved as a comment).
4. Records `OI-NNNN → #N`, writing the map to
   `docs/project-control/open-items/migration-map.md` (the persisted I2 artefact).
5. Rewrites every `OI-NNNN` back-reference under `--docs` (OI-ID cells + prose) to `#N`.

**Operator finish (not automated — verify first):**

1. Eyeball the issues + label queries (`gh issue list --label needs-triage`); the
   `state:` labels for `in-progress`/`blocked` rows are applied by the script (logged).
2. Move `open-items.md` into `archive/` as a frozen, dated snapshot — never silent-delete (§6).
3. Set `backend.yml: github`. From here `sync` / `close` / etc. operate the github backend.

**Rollback** (before step 2–3): the migration is one-way, so undo = delete the created issues
and `git checkout` the ref rewrites while the markdown ledger is still authoritative.

`archive/*.md` history stays as frozen markdown (optionally backfilled as closed issues
later). The script logs any label it could not set so you can finish via the GitHub UI.

---

## Backend behaviour per mode (`github`)

Under `backend: github`, the six modes keep their contract but retarget GitHub via `gh`.
Fields are supplied directly by the calling skill; only the write target changes. See
[`references/github-backend.md`](references/github-backend.md) for the full field mapping.

| Mode | `github` behaviour |
| :--- | :--- |
| `sync` | `gh issue create` — `summary` → title (no prefix), labels applied atomically (`type:<mapped>` per §2a, `priority:p0..p3`, `size:`, `needs-triage`), provenance + `resolution_path` + agent-execution fields → `### <slug>` body sections, assignee = `owner`. Report the resulting `#N` back to the caller. Before creating: de-dup by `(source_artefact, source_anchor, summary)` AND search related/dependent issues via `gh issue list --search`, linking them in the body. |
| `triage` | `gh issue list` + label queries to cluster duplicates, flag `_TBD_` assignees and stale high-priority items, propose readiness routing (promote/route/demote per the ADR-0008 §3 precondition, drafting missing briefs) and 90-day staleness drops. Proposal only — apply after operator approval. |
| `close` | `gh issue close --reason completed`; remove readiness/`state:` labels. The closing reference (`Closes #N` / linked PR) **is** the `tracker_ref` — evidence is structurally enforced, so the §3 `_TBD_` guard cannot be violated. |
| `drop` | `gh issue close --reason "not planned"`; record the rationale as an issue comment (the `Resolution path` analog); remove readiness/`state:` labels. |
| `archive` | No-op. Closed issues are the archive (searchable indefinitely); there is no `archive/` file. |
| `report` | Render from label queries (`gh issue list --label …`) instead of the markdown ledger — counts by `type:`/`priority:`/readiness axis, delegation-queue depth (`is:open label:ready-for-agent`), stale candidates. May still emit a `var/reports/open-items/report-YYYY-MM-DD.md` snapshot. |

Refusal conditions from `sync` (invalid `Type`, terminal status filed with a `_TBD_`
tracker) apply unchanged — validated before any `gh` call.

---

## ID assignment

**`markdown` backend only.** Under `github`, identity is the issue number `#N` (native,
monotonic, never recycled) and no `OI-NNNN` is minted — skip this section.

Canonical IDs are `OI-NNNN` (four-digit zero-padded, monotonic).

- The next ID is computed by scanning every row in `open-items.md` AND every
  `archive/*.md` file for the highest `OI-NNNN` value, then incrementing by one.
- Every row is filed once, directly, with its canonical ID — there is no pre-sync
  placeholder stage to reconcile.
- IDs are never recycled. A `dropped` row's ID stays with that row forever, including
  after it moves to `archive/`.

---

## Source-location provenance

Every filed ledger row preserves three coordinates back to its origin:

| Field             | Where it comes from                                                          |
| :---------------- | :--------------------------------------------------------------------------- |
| `Source artefact` | Relative repo path to the source document (e.g. `docs/business/04a-value-streams.md`). |
| `Source anchor`   | Short fragment identifier supplied at filing time (e.g. `#stage-onboarding`, `#q3`). |
| `Source heading`  | Full heading text the anchor resolves to (e.g. `Stage 2: Onboarding`).        |

The pair `(Source anchor, Source heading)` is the provenance contract from
the `metamodel` skill's `references/open-items-governance.md` §4. Both halves are
required because:

- The anchor is the stable jump target — surviving heading edits.
- The heading is the readable context — surviving anchor renames.

Governance-only items (raised directly at the central plane with no artefact home) carry
`_central-only_` in `Source heading`, an empty `Source anchor`, and an empty
`Source artefact`. the `metamodel` skill's Audit mode does not flag these as orphans (per the README
in `docs/project-control/open-items/`).

---

## De-duplication policy

A row is considered a duplicate of an existing ledger row when ALL of the following match:

1. `Source artefact` is identical (path, post-rename normalisation).
2. `Source anchor` is identical OR `Source heading` is identical (one half of the
   provenance pair is enough — heading changes alone are not duplicates).
3. `Summary` shares ≥80% lexical overlap (case-insensitive, whitespace-normalised) with
   the existing row OR explicitly references the same `Resolution path`.

When `sync` detects a duplicate:

- No new row is created. Report the existing `OI-NNNN`/issue number back to the caller so
  they reference it directly instead.
- If the caller insists a second row is genuinely distinct, file it and let `triage` flag
  the pair for manual review; if it turns out to be a true duplicate, `drop` the newer one
  with rationale `Duplicate of OI-NNNN`.

---

## Closure semantics

Closure is event-driven, not date-driven:

- A row becomes `closed` only when a real tracker reference exists (PR merged, ADR
  written, plan increment shipped, runbook published, audit report acted on).
- A row becomes `dropped` only when an explicit decision exists not to act (recorded in
  `Resolution path`, with the discussion link in `Tracker ref`).
- Reaching a `Due / Review date` without a tracker ref does NOT auto-close the row — it
  surfaces in `triage` as an escalation candidate.
- Closed and dropped rows stay on the live ledger for one review cycle (default 30 days)
  so they remain visible in retrospectives. After that, `archive` moves them out.

The 30-day linger period is intentional: it is the difference between "we resolved this
item" and "we have forgotten about it". Retrospectives, post-mortems, and quarterly
audits use the linger period to scan recent resolutions for patterns.

---

## Operator-facing examples

**File an open item identified while authoring an arch-research note:**

```text
util-open-items sync --source-artefact docs/architecture/research/0003-token-auth.md \
  --source-anchor "#q3" --source-heading "Q3 — How do partners authenticate?" \
  --type decision-gap --summary "Auth model for partner API" \
  --resolution-path "Open ADR on token strategy" --priority high --size S
# github backend: files as type:task (decision-gap maps per §2a) + priority:p1 + size:S
#                 + needs-triage, after the duplicate/dependency search
# → mints OI-NNNN (or opens a GitHub issue),
#   appends the row directly to docs/project-control/open-items/open-items.md
#   (or files it as an issue under the github backend).
```

**Close a resolved decision gap:**

```text
util-open-items close OI-0007 --tracker-ref https://github.com/.../pull/142
# → updates the ledger row to Status: closed.
```

**End-of-quarter archive sweep:**

```text
util-open-items archive --older-than 30d
# → moves eligible closed/dropped rows into archive/2026-Q2.md,
#   refreshes the §Status snapshot block in open-items.md.
```

**Governance health report:**

```text
util-open-items report
# → writes var/reports/open-items/report-2026-05-25.md with counts,
#   type distribution, oldest open items, and coverage map.
```

---

## Output paths

| Path                                                          | Owner                                  |
| :------------------------------------------------------------ | :------------------------------------- |
| `docs/project-control/open-items/open-items.md`                    | This skill (sync / close / drop / archive). |
| `docs/project-control/open-items/archive/<YYYY-Q[1-4]>.md`         | This skill (archive only).             |
| `var/reports/open-items/triage-YYYY-MM-DD.md`                 | This skill (triage report).            |
| `var/reports/open-items/report-YYYY-MM-DD.md`                 | This skill (report mode).              |

The `open-items.md` / `archive/` paths above apply to the **`markdown` backend**. Under
**`github`**, those central writes go to GitHub Issues + labels instead (via `gh`) —
this skill writes no repo file at all in that case.

This skill MUST NOT write to any other path. In particular it MUST NOT mutate
the `metamodel` skill's Audit mode reports (those are produced by a separate report-only skill) and
MUST NOT touch any artefact body — there is no local section for it to write back to
(ADR-0005). A producing skill MAY add its own optional backlink to an artefact it generates
(governance §1), but `util-open-items` itself never edits artefact content.

---

## Reference files

- [`references/template.md`](references/template.md) — canonical ledger table skeleton and
  worked sync example (`markdown` backend).
- [`references/triage-rules.md`](references/triage-rules.md) — operator playbook for
  triage mode (de-duplication, priority escalation, owner assignment).
- [`references/github-backend.md`](references/github-backend.md) — normative `github`-backend
  mapping: slug contract, serialization, identity translation, status decomposition,
  invariants I1–I5.
- `templates/form-{bug,feature,task,docs,tech-debt}.yml` — the per-type GitHub Issue
  Forms (human authoring surface for the `github` backend); installed as
  `1-bug` … `5-tech-debt` per the adoption checklist.
- [`templates/issue-template.config.yml`](templates/issue-template.config.yml) +
  [`templates/issue-form-labeler.workflow.yml`](templates/issue-form-labeler.workflow.yml)
  — intake config (no blank issues) and the Priority/Size → label mirror workflow.
- [`scripts/bootstrap_labels.sh`](scripts/bootstrap_labels.sh) — idempotent 17-label
  vocabulary bootstrap (adoption step 1; dry-run by default).
- [`scripts/backfill_execution_labels.py`](scripts/backfill_execution_labels.py) — one-time
  backfill for repos on the github backend pre-ADR-0009 (old type labels remapped per §2a,
  body-parsed `priority:` labels, `needs-triage` default, marker stripped; dry-run by
  default, offline `--selftest`).
- [`scripts/migrate_markdown_to_github.py`](scripts/migrate_markdown_to_github.py) — the
  one-way `markdown → github` migration driver for Mode 7 (dry-run by default; emits the
  `OI-NNNN → #N` map and rewrites back-references).

---

## See also

- the `metamodel` skill's `references/open-items-governance.md` — canonical
  contract; the rule wins on every conflict.
- [`docs/project-control/open-items/README.md`](../docs/project-control/open-items/README.md) —
  operator orientation for the central control plane.
- `the `metamodel` skill's `references/modes/audit-check-catalogue.md`` — governance-drift audit (report
  only; never mutates).
