---
title: Standard Issue Vocabulary for the github Backend (Amends ADR-0008)
status: active
owner: Victor Hueni
last_reviewed: 2026-07-20
review_interval: 180d
---

# Standard Issue Vocabulary for the github Backend (Amends ADR-0008)

Date: 2026-07-20

## Context and Problem Statement

[ADR-0008](adr-0008-open-items-agent-execution-labels.md) serialized the open-items model
onto labels, carrying the governance heritage forward unchanged: an `open-item` marker
label plus the governance §2 taxonomy as type labels (`type:doc-gap`,
`type:decision-gap`, `type:execution-item`, `type:tech-debt`).

That vocabulary made sense when the ledger was a separate control plane *beside* a normal
issue tracker. It stops making sense when the tracker **is** the whole backlog — the
operator's declared model: *"everything is an open item basically."* Then:

- The marker label is redundant: it only distinguishes open items from other issues, and
  there are no other issues. It is pure noise on every issue and in every query.
- The governance-derived type names are **exotic** where the platform, community label
  norms, and agent tooling (Copilot, triage bots, coding agents — all trained on normal
  repos) expect `bug` / `feature` / `docs` (research 0002 §1, §4).
- Real repos have bugs and features; the governance taxonomy explicitly scoped them out
  ("belongs elsewhere — product backlog, defect tracker"), but on GitHub the defect
  tracker is the same tracker. One repo would end up speaking two vocabularies.
- A single form with a type dropdown cannot require different fields per type (no
  conditional validation) — but a **bug** needs required reproduction steps while a
  **decision** needs context/options (research 0002 §2, §4).

## Decision Drivers

- **Fit the platform, don't be exotic** — operator's explicit direction; matches research
  0002's convergent practice (standard vocabulary, per-scenario templates, prefixed label
  groups).
- **One tracker, one vocabulary** — bugs, features, and governance items share the
  execution layer (priority/size/readiness) instead of living in parallel systems.
- **Tailored intake validation** — per-type forms are the sanctioned workaround for
  forms' lack of conditional fields.
- **Preserve the governance model** — §2 taxonomy, provenance, evidence-gated closure
  stay intact at the abstract level; only the github serialization changes.

## Considered Options

1. **Standard 6-type vocabulary, marker dropped, one form per type (chosen).**
2. **Keep ADR-0008 as decided.** Consistent with the ledger heritage, but exotic on a
   real tracker and unable to host bugs/features natively.
3. **Hybrid: keep `open-item` on governance-filed issues only.** Preserves audit scoping
   precision but keeps one exotic label and two classes of issue. Rejected: the audit can
   scope by the presence of provenance sections instead.

## Decision Outcome

Chosen option: **Option 1.** This ADR amends ADR-0008 §4 (vocabulary) and §the marker;
everything else in ADR-0008 — label-based serialization, execution slugs, readiness
contract, title convention, validation home — stands unchanged.

### 1. Type axis: five standard values

`type:bug` · `type:feature` · `type:task` · `type:docs` · `type:tech-debt`

The `type:` prefix stays (prefixed label groups are recognized practice and what axis
exclusivity + the audit key on); the *values* are standard dev vocabulary.

**Same-day amendment (operator review + conformance research 0003): no `decision`
type.** A "decision needed" item is a **task** whose deliverable is the decision record
("research X, write ADR-NNNN"); decisions with no codebase home are logged outside the
tracker. This matches observed practice — no surveyed mainstream repo ships a decision
template; decisions live in ADRs/RFCs, not in an issue type. `decision-gap` therefore
maps to `type:task` (§2) and the vocabulary is 17 labels (§5).

### 2. Governance mapping (abstract model unchanged)

The governance §2 taxonomy maps into the serialization:

| Governance §2 | Serialized as |
| :--- | :--- |
| `doc-gap` | `type:docs` |
| `decision-gap` | `type:task` (the task's deliverable is the decision record — ADR or logged decision) |
| `execution-item` | `type:task` |
| `tech-debt` | `type:tech-debt` |

`type:bug` and `type:feature` are **tracker-native** types with no governance
counterpart — they are ordinary dev work, not governance items, and never sync to a
`markdown`-backend ledger. Structural checks (axis exclusivity, readiness contract) apply
to every issue; provenance checks apply only to issues carrying provenance sections.

### 3. Marker label dropped

`open-item` is retired. The backend contract "GitHub Issues labelled `open-item`" becomes
"**the repo's issue tracker**" — `backend.yml` still declares the backend; the tracker
boundary is the ledger boundary. The delegation queue query becomes
`is:open label:ready-for-agent`.

### 4. One issue form per type

Five forms (`1-bug` / `2-feature` / `3-task` / `4-docs` / `5-tech-debt` — numeric
prefixes control the template-chooser order, GitHub's documented mechanism), each:

- auto-applies its `type:` label and `needs-triage` (statically — no mirroring needed for
  type anymore);
- shares the `priority` and `size` dropdowns (still mirrored to labels by the labeler
  workflow, which loses its type mapping and `open-item` scope guard);
- carries **tailored required fields**: bug → description + reproduction (environment
  optional, `render: shell`); feature → problem/motivation; task → description;
  docs → what's missing/where; tech-debt → current state + impact — substance fields
  first, the shared Priority/Size dropdowns last (conformance research 0003: no
  mainstream form leads with metadata);
- keeps the canonical-slug fields where they apply: `references`,
  `acceptance_criteria`, `out_of_scope` on executable types; the provenance triple +
  `resolution_path` (optional) on the governance-mapped types (task/docs/tech-debt).
  Field `id:` ≡ slug (Invariant I1) throughout;
- omits the conventional duplicate-search checkbox **by design**: issues are filed by
  the operator or by agents whose contract requires a duplicate/dependency search
  before creation; the checkbox is added the day a repo takes external filers (noted
  in each form header).

### 5. Amended vocabulary (17 labels, five axes)

Marker axis removed (−1); type axis becomes five standard values (+1 net: `bug` and
`feature` added, the four governance names replaced, no `decision` per the §1
amendment). Priority, size, readiness, state axes unchanged from ADR-0008 §4.

| Axis | Label | Color | Description |
| :--- | :--- | :--- | :--- |
| type | `type:bug` | `D73A4A` | Something is broken |
| type | `type:feature` | `A2EEEF` | New user-facing capability |
| type | `type:task` | `1D76DB` | Concrete work item — not a feature, not broken (incl. decision work → ADR) |
| type | `type:docs` | `C5DEF5` | Documentation missing, wrong, or unclear |
| type | `type:tech-debt` | `023B95` | Deliberate structural shortcut to pay back |
| priority | `priority:p0` | `B60205` | Critical — drop everything |
| priority | `priority:p1` | `D93F0B` | High — this cycle |
| priority | `priority:p2` | `FBCA04` | Medium — scheduled |
| priority | `priority:p3` | `FEF2C0` | Low — opportunistic |
| size | `size:S` | `EDEDED` | Small — hours, single-file scale |
| size | `size:M` | `BFBFBF` | Medium — a focused day, few files |
| size | `size:L` | `878787` | Large — consider splitting before delegation |
| readiness | `needs-triage` | `D4C5F9` | Untriaged — not yet routed (creation default) |
| readiness | `ready-for-agent` | `0E8A16` | Brief complete — an agent may take this |
| readiness | `needs-human` | `F9D0C4` | Valid, but requires a human decision/work |
| state | `state:in-progress` | `006B75` | Actively being worked (replaces readiness label) |
| state | `state:blocked` | `000000` | Blocked on an external dependency |

### Positive Consequences

- The tracker reads like every other GitHub repo — native for humans, community norms,
  and agent tooling; no private vocabulary to explain.
- Bugs and features become first-class citizens of the same backlog and execution layer.
- Per-type forms give per-type required fields (repro for bugs, context for decisions).
- One less label per issue and simpler queries (no marker).

### Negative Consequences

- The existing issues (the 29 migrated + #72–#74) carry the old marker + type labels;
  the Plan-0003 backfill (increments 09–10) must additionally remap
  `type:doc-gap`→`type:docs` etc. and strip `open-item`.
- The audit loses the marker as a cheap population selector; it scopes provenance checks
  by section presence instead.
- Five forms to maintain instead of one (mitigated: shared blocks, template copies in the
  skill).
- Plan-0003 increments 04–06, already built, are reworked in place (all unmerged — no
  released surface breaks).

## Deferred / unchanged

- ADR-0008's readiness contract, execution slugs, title rule, and validation-home note
  stand unchanged.
- Native Issue Types (org-level) remain a possible future upgrade
  ([#72](https://github.com/VictorHueni/homemade-claude-kit/issues/72)) — the 5-value
  standard vocabulary maps cleanly onto them if the portfolio moves to an org.

## Open Items

None beyond the backfill scope amendment recorded in Plan-0003.
