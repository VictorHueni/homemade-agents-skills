---
title: Open-Items github Backend — Label-Based Agent-Execution Serialization
status: active
owner: Victor Hueni
last_reviewed: 2026-07-20
review_interval: 180d
---

# Open-Items github Backend — Label-Based Agent-Execution Serialization

Date: 2026-07-20

## Context and Problem Statement

[ADR-0002](adr-0002-open-items-pluggable-backend-github-issues.md) mapped the open-items
§4 model onto GitHub primitives, assigning `priority` to a **Project (v2) single-select
field** and the `in-progress`/`blocked` halves of `status` to a **Project Status field**.
In fourteen months of operating the backend on this repo, that Project was never created:
`priority` exists only as body text (`### Priority`), and `in-progress`/`blocked` are not
represented at all. Nothing — human or agent — can filter or sort the live queue by
priority without parsing issue bodies.

Meanwhile the backlog's primary *executor* is becoming coding agents
([research 0001](../research/0001-open-items-agent-execution-setup.md),
[research 0002](../research/0002-github-issue-creation-best-practices.md)). Agents need:

- a **queryable** priority/effort surface (one `gh issue list --label` call, not body parsing);
- a **trust signal** separating issues an agent can safely take from issues needing a human
  decision — the strongest published pattern is a triage state machine whose
  `ready-for-agent` column is kept trustworthy (research 0001 §3.4);
- **agent-ready content fields** — code pointers and machine-checkable acceptance criteria
  measurably double agent PR merge rates (77.1% vs 45.9%, research 0001 §3.3).

This ADR settles: **where do `priority`, execution metadata (`size`, readiness), and the
`in-progress`/`blocked` status decomposition live in the `github` backend?**

This ADR **extends ADR-0002** (it amends its serialization table); it does not supersede
it. The abstract model — §2 taxonomy, §3 lifecycle, §4 canonical columns, §5.3 invariants
I1–I5 — is unchanged. The `markdown` backend is untouched. Plan-0003 tracks the
implementation.

## Decision Drivers

- **Agent queryability.** The execution surface must be readable/writable in one `gh`/API
  call by an agent with repo scope — no GraphQL Project mutations, no body parsing.
- **Personal-repo portability** (ADR-0003 driver). Projects v2 fields and native Issue
  Types are org-grade; labels work identically on personal repos.
- **One write surface per fact.** The unwired-Project experience showed that a second
  metadata home (Project fields) beside the issue itself invites drift; labels live *on*
  the issue.
- **Trustworthy delegation queue.** `ready-for-agent` must be a guarantee, not a mood —
  it needs an enforceable precondition.
- **Evidence over convention** (ADR-0002 driver, unchanged): closure stays
  structurally evidenced; the new layer must not weaken it.

## Considered Options

1. **Labels for priority + execution layer; Project fields retired (chosen).**
2. **Wire the Projects v2 fields as originally mapped.** Best read-out UX, but a second
   write surface with a permanent label↔field sync tax, org-grade assumptions, and a
   heavier agent round-trip (GraphQL). Deferred as an optional read-out layer on top of
   labels — filed as [#73](https://github.com/VictorHueni/homemade-claude-kit/issues/73).
3. **Status quo** (priority in body text). Zero work, but unqueryable — fails the
   primary driver.

## Decision Outcome

Chosen option: **Option 1 — labels are the serialization home for `priority`, the
`in-progress`/`blocked` status decomposition, and the new optional execution slugs.**

### 1. Amended serialization (supersedes the corresponding ADR-0002 rows)

| Canonical slug | Old home (ADR-0002) | New home |
| :--- | :--- | :--- |
| `priority` | Project single-select field (never wired) | `priority:p0..p3` label |
| `status` = `in-progress` / `blocked` | Project Status field (never wired) | `state:in-progress` / `state:blocked` label |
| `status` = `open` / `closed` / `dropped` | Issue state + close reason | unchanged |

Priority domain mapping (canonical value ↔ label): `critical`↔`priority:p0`,
`high`↔`priority:p1`, `medium`↔`priority:p2`, `low`↔`priority:p3`.

### 2. New optional execution slugs (additive per governance §4)

Two slugs join the canonical set as **optional, execution-layer** fields, sanctioned by
§4's "skills MAY add informational columns after `Tracker ref`":

- **`size`** — one-PR effort bound: `size:S | size:M | size:L` label. Supplied by the
  filer (form dropdown / `sync` input).
- **`readiness`** — delegation trust state: `needs-triage | ready-for-agent | needs-human`
  label. **Orthogonal to lifecycle `status`** — it qualifies an `open` item, never
  replaces §3. `needs-triage` is the creation default (form-applied and `sync`-applied);
  the other two are **triage-owned**: only a triage pass (or an operator) promotes or
  routes. Filing agents never self-promote.

Three new **form/body content fields** (Issue Form ids = canonical slugs, Invariant I1):
`references` (code pointers: files, symbols, prior PRs, patterns to imitate),
`acceptance_criteria` (observable pass/fail checklist ending in a runnable verification
command), `out_of_scope` (optional). These serialize in the issue body as `### <label>`
sections, like the existing provenance fields.

### 3. The readiness contract

`ready-for-agent` is a guarantee with an enforceable precondition:

> An issue MAY carry `ready-for-agent` only if its `acceptance_criteria` and `references`
> sections are non-empty and its `size` is set.

Promotion happens only via triage (`util-open-items` triage v2, or the delegation skill's
`validate` mode proposing — operator approves). The metamodel Audit mode verifies the
invariant report-only (Plan-0003 increment 08). Demotion (drift found later) is likewise
a cited, proposal-first action.

Axis exclusivity: an issue carries **at most one label per axis** (`type:`, `priority:`,
`size:`, readiness, `state:`). When work starts (`take`), `state:in-progress` replaces the
readiness label; the closing flow removes readiness/`state:` labels at terminal state
(leftovers on closed issues are audit hygiene findings, not drift).

### 4. Canonical label vocabulary (17 labels, six axes)

At most 4–5 labels ever apply to one issue (marker + type + priority + size + one
workflow label). Bootstrap is idempotent (`gh label create --force`, Plan-0003
increment 04) and normalizes colors/descriptions on re-run.

| Axis | Label | Color | Description |
| :--- | :--- | :--- | :--- |
| marker | `open-item` | `5319E7` | Governance open item (backend contract marker) |
| type | `type:doc-gap` | `C5DEF5` | Missing information to research/write |
| type | `type:decision-gap` | `1D76DB` | Decision required before downstream work |
| type | `type:execution-item` | `0052CC` | Concrete follow-up work to schedule |
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

This exceeds the folk "~15 total" heuristic by two; the operative limit from the research
is **labels per issue** (2–4 recommended; we cap at 5), and every axis here is queryable
metadata, not free-form tagging. Plan-0003's increment-01 gate is amended accordingly.

### 5. Title convention

The `[OI] ` title prefix is **dropped**. The `open-item` label carries the signal; no
tooling greps titles (the rust-`[ICE]:` niche does not apply). Titles are short,
specific, searchable — symptom statements for gaps, imperative outcomes for
execution/debt items. Existing issue titles are left as-is (no retro-rename churn); the
form template and `sync` stop emitting the prefix.

### 6. Where validation actually lives

Issue Form `validations.required` gates **only the web UI**. Issues filed by
`util-open-items` via `gh`/API bypass the form entirely, so the skill's refusal rules
(valid `type`, no terminal state without `tracker_ref` — now plus: no `ready-for-agent`
without the §3 precondition) remain the authoritative gate. The form is a convenience
mirror of the contract, not its enforcement.

### Positive Consequences

- Priority/size/readiness become one-call queryable for agents and humans
  (`gh issue list --label open-item,ready-for-agent`); body parsing retired.
- Works identically on personal repos — no org, no Project, no extra scopes.
- The delegation queue has an enforceable trust invariant, audit-checkable.
- `in-progress`/`blocked` are finally represented (the ADR-0002 mapping's unwired gap).
- One write surface: every fact about an issue lives on the issue.

### Negative Consequences

- No board/table read-out; filtered lists must suffice until
  [#73](https://github.com/VictorHueni/homemade-claude-kit/issues/73) (Projects v2 layer)
  is triggered.
- Labels are flat strings — axis exclusivity is convention + audit, not schema-enforced.
- 17 repo labels to bootstrap and keep normalized (mitigated: idempotent script).
- Existing issues need a one-time backfill (Plan-0003 increments 09–10).

## Deferred questions (filed as open items)

- [#72](https://github.com/VictorHueni/homemade-claude-kit/issues/72) — free GitHub org
  for native Issue Types / org issue fields across the portfolio.
- [#73](https://github.com/VictorHueni/homemade-claude-kit/issues/73) — Projects v2
  read-out layer (Option B) on top of labels.
- [#74](https://github.com/VictorHueni/homemade-claude-kit/issues/74) — Backlog.md as
  successor to the `markdown` backend for non-GitHub projects.

## Open Items

None beyond the three filed above.
