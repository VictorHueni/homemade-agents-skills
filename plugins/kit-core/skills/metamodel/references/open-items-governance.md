# Open Items Governance

The kit captures unresolved work across many artefact types — research questions, missing
decisions, follow-up implementation items, deferred refactors. Without a single contract
those captures drift in schema, lifecycle vocabulary, and provenance completeness, making it
impossible to audit governance health or roll up live open work across the stack.

This rule is the **single source of truth** for that contract. Every skill that emits
unresolved work and every audit that verifies it must conform to the schema and lifecycle
defined here. `util-docs-audit` stays generic (file-level rot) and is out of scope;
stack-aware governance lives in the `metamodel` skill's Audit mode and the dedicated `util-open-items`
skill.

---

## 1. Authoring surface: the central ledger only

Every open item — whatever artefact it concerns, or none at all — is authored **directly
into the central ledger**: the living markdown table at
`docs/project-control/open-items/open-items.md`, or a GitHub Issue labelled `open-item`,
per whichever backend the project selects (`backend.yml`, §5.3). There is no per-artefact
local section to expose, populate, or keep in sync — the ledger (or issue tracker) is the
only surface a skill or contributor writes to.

**Why no local section ([ADR-0005](https://github.com/VictorHueni/homemade-claude-kit/blob/main/docs/architecture/decisions/adr-0005-open-items-ledger-sole-authoring-surface.md)).**
An earlier version of this contract required every artefact to expose a document-level
`## Open Items` table as an authoring surface, synced into the ledger by `util-open-items`.
That local step had already gone unfollowed in practice — new items were being filed
straight to the ledger with full provenance and no local-row counterpart — because filing
directly is strictly less work for the same result: the ledger/Issue Form already demands
the same provenance fields (§4) at creation time. ADR-0005 retired the local step to match
observed practice.

A skill MAY still add a single-line backlink in a generated artefact (e.g.
`Open items: #57, #58`) so a reader can find related ledger rows without leaving the
document. This is optional per skill and is never a table — a full local table is the
retired pattern this rule no longer sanctions. Any leftover local `## Open Items` table
found in a swept artefact is a stale relic of the prior contract; delete it.

---

## 2. Item taxonomy

Every row in an `## Open Items` table is exactly one of four types:

| Type            | Meaning                                                                                                         | Typical resolution path                                  |
| :-------------- | :-------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------- |
| `doc-gap`       | Information that should live in this artefact is missing and needs to be researched or written.                  | Update the artefact in place.                            |
| `decision-gap`  | A decision is required (often architectural) before downstream work can proceed.                                | Write or update an ADR, then close the row.              |
| `execution-item`| Concrete follow-up work that does not change the artefact itself but must be scheduled.                          | Open a PRD / implementation plan increment / runbook.    |
| `tech-debt`     | Known structural shortcut that must be paid back later; not a defect, but a deliberate deferral.                | Open a refactor PRD or schedule into a maintenance epic. |

The type field is mandatory on every row. A row that does not fit one of the four types
either belongs elsewhere (product backlog, defect tracker) or has been mis-classified.

### Open items are NOT scaffold placeholders

Inline `_TODO_` placeholders inside an artefact body (a stub heading, an unfinished
sentence, a missing diagram) are **not** open items. They are scaffold debt: they signal an
incomplete first draft of the document itself. `_TODO_` density is measured by
the `metamodel` skill's Audit mode Check 8 and is reported separately.

Open items capture **work that remains after the artefact is internally complete** —
unanswered questions, deferred decisions, follow-ups, debt. Skills must not file
placeholder-only rows to the central ledger just to have something to point at; filing
nothing is the correct state when no actionable unresolved work exists yet.

---

## 3. Lifecycle states

Each row uses one of the following statuses, in this lifecycle order:

| Status        | Meaning                                                                                  |
| :------------ | :--------------------------------------------------------------------------------------- |
| `open`        | Identified, not yet being worked on.                                                      |
| `in-progress` | Actively being resolved (assigned, on the active work plan).                              |
| `blocked`     | Cannot progress without an external dependency (decision, evidence, third party).         |
| `closed`      | Resolved. Kept in the row for one review cycle, then archived per §6.                     |
| `dropped`     | Decided not to act on this item. Rationale recorded in `Resolution path`.                 |

Closure must be evidenced: a `Tracker ref` (link to PR, ADR, plan increment, or audit
report) is required to move a row to `closed` or `dropped`.

---

## 4. Table schema

Every open item is captured with one canonical set of fields, whatever the backend. Under
the `markdown` backend these are literal table columns in `open-items.md`; under `github`
they are the Issue Form fields (see §5.3 and `util-open-items/references/github-backend.md`
for the field-to-form mapping). Column order and headings, where a literal table is used,
are fixed:

```markdown
| OI-ID  | Type           | Summary                       | Source artefact                                | Source anchor | Source heading                          | Resolution path                                  | Priority | Status      | Owner   | Due / Review date | Tracker ref       |
| :----- | :------------- | :---------------------------- | :---------------------------------------------- | :------------- | :-------------------------------------- | :----------------------------------------------- | :------- | :---------- | :------ | :---------------- | :---------------- |
| OI-001 | decision-gap   | Auth model for partner API    | `docs/architecture/research/0003-token-auth.md` | #q3            | Q3 — How do partners authenticate?      | Open ADR on token strategy                       | high     | open        | victor  | 2026-06-15        | _TBD_             |
```

**Column rules:**

- `OI-ID` — assigned at filing time: the next monotonic `OI-NNNN` under the `markdown`
  backend, or the native issue number `#N` under `github`. There is no pre-sync placeholder
  stage — a row is filed once, directly, with its canonical ID.
- `Type` — exactly one of the four taxonomy values from §2.
- `Summary` — one-sentence statement of the open item. Self-contained: a reader should
  understand the row without opening the source artefact, since there is no local row
  co-located with it.
- `Source artefact` — relative repo path to the artefact this item concerns (e.g.
  `docs/architecture/research/0003-token-auth.md`), or the central-only scope marker per
  §5.2 when the item has no artefact home.
- `Source anchor` — short fragment identifier (e.g. `#q3`, `#stage-onboarding`, `#vp-2`,
  `#cs-1`) inside the source artefact. Provides a precise jump target and is the stable
  half of the provenance pair.
- `Source heading` — the full heading text the anchor resolves to (e.g.
  `Q3 — How do partners authenticate?`, `Stage 2: Onboarding`, `VP-2: Self-serve setup`).
  Provides human-readable context that survives anchor renames and is the readable half of
  the provenance pair.
- `Resolution path` — what closing this row looks like in practice (e.g. "Open ADR on token
  strategy", "Schedule into refactor epic E-07").
- `Priority` — `low` | `medium` | `high` | `critical`.
- `Status` — lifecycle value from §3.
- `Owner` — person accountable. Use `_TBD_` if no owner is yet assigned.
- `Due / Review date` — ISO 8601. For `closed` / `dropped` rows this is the closure date.
- `Tracker ref` — link to the resolving PR, ADR, plan increment, runbook, or audit report.
  Use `_TBD_` while the row is still `open`; required to leave `open` for a terminal state.

Skills MAY add additional informational columns *after* `Tracker ref`. They MUST NOT remove
or reorder the canonical columns.

---

## 5. Central control plane

The repo-level living ledger lives under:

```text
docs/project-control/open-items/
```

This path is **under `docs/` for unified navigation** (every persistent artefact in the
repo lives somewhere under `docs/`, so contributors only have to remember one root) but
**named `project-control/` because it is an operational control plane, not a product
spec**. The folder name is the load-bearing signal: anything under
`docs/project-control/` is a live, continuously-changing system of record — closer to a
runbook or an internal tracker than to a PRD, an ADR, or a domain model. Audits and
linters that operate on product-spec artefacts (PRDs, FBS, ADRs, domain models, etc.)
either match by file pattern or by deeper folder (`docs/product-specs/`, `docs/domain/`,
`docs/architecture/`) and therefore do **not** sweep `docs/project-control/`.

Why it is separate from product backlog artefacts (PRDs, delivery roadmap, FBS):

- The delivery roadmap (`E-NN` epics) plans **what we build next** at product scope. Open
  items capture **governance-level unresolved work** across every kind of artefact, only
  some of which results in built features.
- PRDs and implementation plans are commitment artefacts. Open items can include items that
  may never become commitments (e.g. dropped research questions).
- The FBS tracks **functionality status** in shipped or in-flight features. Open items can
  include doc gaps and decision gaps that never appear as functionalities.

Source-of-truth rule: **the central ledger is the only authoring surface (§1).** A skill
files a row directly via `util-open-items`, which assigns the canonical `OI-NNNN` ID (or, on
`github`, the row is the issue itself) and records `Source anchor` and `Source heading` at
filing time so the ledger can navigate back into the source artefact without relying on
tribal knowledge.

Each ledger row points back to its source via three coordinates:

- The relative path to the source artefact (e.g. `docs/architecture/research/0003-token-auth.md`).
- The `Source anchor` (e.g. `#q3`).
- The `Source heading` (e.g. `Q3 — How do partners authenticate?`).

If a source artefact is renamed, the central ledger row is updated; if a heading is
renamed, the `Source heading` field is updated while the anchor remains stable, or the
anchor is updated and the new heading recorded.

### 5.1 Ledger column layout

The ledger uses exactly the §4 canonical columns — `Source artefact` is a baseline §4 field,
not a ledger-only addition (an artefact of the pre-ADR-0005 contract, when the ledger added
this column on top of a slimmer local-section schema):

```
OI-ID | Type | Summary | Source artefact | Source anchor | Source heading | Resolution path | Priority | Status | Owner | Due / Review date | Tracker ref
```

Skills MAY add additional informational columns after `Tracker ref` per §4; no other
deviation is sanctioned.

### 5.2 Central-only rows (governance work with no source artefact)

Most rows cite a `Source artefact` — the specific document the item concerns. Some
governance work is raised with **no artefact home at all** — e.g. kit-development items (per
§9), or repo-wide decisions not owned by any single document. These **central-only** rows are
valid and use this provenance form:

- `Source heading` = `_central-only_`
- `Source anchor` = empty
- `Source artefact` = the owning folder/skill or scope marker (e.g. `ops-terraform-exoscale/`),
  or `(cross-cutting)` when no single location applies.

the `metamodel` skill's Audit mode MUST NOT flag central-only rows as orphaned or as provenance-drift
findings. All other §4 column rules (valid `Type`, lifecycle `Status`, `_TBD_`-until-terminal
`Tracker ref`, ISO date) apply unchanged.

### 5.3 Pluggable backend

The central plane is a **serialization** of the §4 model, not the model itself. The default
and only universally-required backend is **`markdown`** — the living ledger of §5 plus the
archive of §6. A project MAY select an alternative backend (for example, an issue tracker)
for the consolidated read-out. Whatever the backend, these invariants hold:

- **Backend-independent model.** The §4 schema is the one logical model; each backend is a
  serialization of it. The field **slugs** (the stable lower-snake keys behind each §4
  column) — not column headers or UI labels — are the binding contract every backend
  conforms to. The audit reads any backend through that single slug map.
- **Authoring surface is backend-invariant.** Every backend is filed into directly (§1);
  only *what* gets written — a ledger row or an issue — changes with the backend. Switching
  backends never introduces or removes an authoring step.
- **One backend per project.** Backends are never run concurrently — two live writers over
  two identity spaces reintroduce the dual-source-of-truth this contract exists to prevent.
  Moving between backends is a **one-way migration** performed once, and MUST emit an
  identity map so back-references survive the identifier re-mint.
- **Evidence-gated closure holds.** A terminal `Status` still requires a non-`_TBD_`
  `Tracker ref`, whether the backend enforces it natively or the operator validates it.
- **Provenance is preserved.** Every backend stores the full provenance composite
  (`Source artefact` + `Source anchor` + `Source heading`) under the canonical slugs, so
  central-only and artefact-originated items are distinguishable in any backend.

A worked two-backend mapping (the kit's own `markdown` ledger plus an issue-tracker backend)
is maintained as the reference model that operator tooling and the audit conform to; see
§10.

---

## 6. Archive and snapshots

Closed and dropped items remain on the active central ledger for one review cycle (default:
30 days). After that they are moved to:

```text
docs/project-control/open-items/archive/
```

Archive files are time-bucketed snapshots (e.g. `2026-Q2.md`) or per-resolution rollups.
The live ledger never silently deletes rows — archival is explicit and dated.

---

## 7. Audit and tooling boundaries

| Tool                          | Responsibility                                                                                              |
| :---------------------------- | :---------------------------------------------------------------------------------------------------------- |
| `util-docs-audit`             | Generic file-level rot (stale, outdated, dead). **Not** an open-items governance tracker.                   |
| `util-open-items`             | Maintains the central plane — sync, triage, close, archive, report — honouring the configured backend (§5.3). Living ledger CRUD.         |
| the `metamodel` skill's Audit mode        | Report-only. Verifies central-ledger/issue rows conform to the §4 schema, that `Source artefact` / `Source anchor` resolve to a real file/heading, and that closure evidence is present — reading whichever backend is configured via the canonical field slugs (§5.3). Never mutates the ledger. |

the `metamodel` skill's Audit mode is the only place that flags governance drift on the central ledger
(schema compliance, dangling provenance, closure evidence). It must not mutate the ledger;
remediation is always operator-driven via `util-open-items`.

---

## 8. Skill conformance checklist

When a skill emits or governs unresolved work **about the artefacts it produces** (under a
project's `docs/`), its `SKILL.md` instructions must:

1. File the item directly with `util-open-items` the moment it is identified — no local
   heading, table, or scaffold to populate first (§1).
2. Cite the column schema in §4 by reference (link to this rule) — never restate it inline.
3. Distinguish `_TODO_` scaffold placeholders from real `doc-gap` / `decision-gap` /
   `execution-item` / `tech-debt` rows; only the latter are open items.
4. Supply `Source artefact` + `Source anchor` + `Source heading` on every row that concerns a
   specific sub-section of the artefact (questions, stages, blocks, processes) it is
   producing.

Output templates carry no Open Items scaffold of any kind — there is nothing for a template
to include (§1).

---

## 9. Scope boundary — skill folders are tooling, not artefacts

The `## Open Items` contract governs **project artefacts** (PRDs, ADRs, domain models,
research notes, and the like) — the documents a skill *produces* under a project's `docs/`.
It does **not** apply to the skill definitions themselves.

A skill folder (`<skill>/SKILL.md` and its `references/`, `templates/`, `scripts/`) is
tooling, not a governed artefact. It **MUST NOT** carry its own open-items tracking of any
kind, and ledger rows about the skill's own development MUST NOT cite the skill folder as a
`Source artefact` — that field names a project artefact under `docs/`, and the skill folder
is not one. Genuine kit-dev items are central-only rows instead (below).

Follow-up work on a skill — new modes, extra checks, deferred refinements — is **real
governance work on the kit itself**, so the kit dogfoods this very contract: such items live
in the kit's own central ledger at `docs/project-control/open-items/open-items.md` (§5), as
central-only rows (`Source heading: _central-only_`, empty `Source anchor`). They do **not**
live in the skill folder. The same ledger also holds the kit's candidate-skill backlog and
structural-decision items (the former `BACKLOG.md`, merged in); shipped-skill history is
recorded under `docs/project-control/open-items/archive/`. A skill's `SKILL.md` may carry at most a short
**"Follow-up work"** pointer to the ledger; it never carries the canonical `## Open Items`
table.

**Skills do not restate the schema.** A skill whose process may surface unresolved work does
**not** embed the canonical table, an example row, or a §4 column recital in its `SKILL.md`.
It names the fields it needs to supply (type, summary, provenance, resolution path) and
points at this rule for the mechanics — the schema lives here and in
`util-open-items/references/template.md`, never duplicated into a skill folder or an output
template (§1, §8).

Restated:

- Items a skill identifies **about the artefacts it produces** → filed directly to the
  central ledger per §1–§8, citing that artefact as `Source artefact`.
- Items about the **skill's own evolution** → the kit's `docs/project-control/open-items/`
  ledger, as central-only rows, never inside the skill folder.

---

## 10. See also

- `rules/metamodel.md` — strategic-architecture build order; references this contract.
- `util-open-items/references/github-backend.md` — the operator skill's worked backend-mapping reference (canonical field slugs, identity translation, status decomposition); the §5.3 worked example. Travels with the skill — never copied into a project's `docs/`.
- `docs/project-control/open-items/open-items.md` — the kit's own ledger: kit-dev open items (per §9) **and** the merged skill backlog (candidate skills + structural decisions). Shipped history under `archive/`.
- `util-open-items/SKILL.md` — operating manual for the living ledger.
- `the `metamodel` skill's `references/modes/audit-check-catalogue.md`` — exact audit checks for governance
  drift, schema compliance, and provenance.
