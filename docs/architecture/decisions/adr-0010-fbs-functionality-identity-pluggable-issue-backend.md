---
title: FBS Functionality Identity — Pluggable Issue-Tracker Backend for spec-functional-breakdown-structure and plan-delivery-roadmap
status: draft
owner: Victor Hueni
last_reviewed: 2026-08-13
review_interval: 180d
---

# FBS Functionality Identity — Pluggable Issue-Tracker Backend for spec-functional-breakdown-structure and plan-delivery-roadmap

Date: 2026-08-13

## Context and Problem Statement

`spec-functional-breakdown-structure` mints `C-N.M.FXX` functionality identifiers by hand into
Markdown — one row per functionality, grouped under a `C-N.M` capability section. That identity
scheme has the same shape as the open-items `OI-NNNN` scheme ADR-0002 replaced: a hand-minted,
markdown-only ID doing a job an issue tracker does natively (monotonic, free, closure-by-reference
unfakeable, filterable/groupable via a Project view).

A downstream project (`swiss-aos-drug-reimbursement-model`) has already proven this in practice,
independently of this ADR: its Recovery/Codex MVP roadmap (`RE-NN` epics, hand-authored in
Markdown this same day) was seeded into 139 GitHub Issues — 15 epics, 124 functionalities, native
sub-issue hierarchy, a `Capability` Project field dual-stored as a `Capability: C-N.M` body line —
with the functionality's identity being its GitHub issue number, not a minted ID. Every
cross-reference between functionalities was rewritten to a native `#N` link. The seeding script and
its two-pass reference-resolution design (create first, patch cross-references once every target
exists) are the reference implementation this ADR generalises into the kit skills, the same way
ADR-0002 generalised from a specific need into `util-open-items`'s backend abstraction.

The question this ADR settles: **should `spec-functional-breakdown-structure` (and, downstream,
`plan-delivery-roadmap`) gain a pluggable issue-tracker backend for functionality identity, the
same shape ADR-0002 already validated for open items — and if so, what does the primitive mapping
and config surface look like?**

This ADR is scoped to the **functionality-identity layer** (`C-N.M.FXX` rows / their replacement).
It does **not** touch capability identity (`C-N.M`) — capabilities remain markdown-authored in the
capability map. A downstream project's own ADR-0050 already reasoned through why: capabilities are
a small, curated, slow-changing taxonomy edited by a human; functionalities are the high-volume,
work-item-shaped layer a tracker is built for. That boundary is reused here, not re-litigated.

## Decision Drivers

- **Reuse the validated pattern, don't re-derive it.** ADR-0002/ADR-0003 already worked out the
  hard parts for this exact shape of decision (pluggable backend, GitHub first, decline to
  generalise as a forced default) and paid for the portability lessons (Issue Types are org-level →
  `type:` label fallback; ledger `owner` ≠ GitHub login; label/Project bootstrap needed). Re-doing
  that discovery for a second skill family would be paying the same cost twice.
- **Don't invent a second config surface.** `backend.yml` (colocated with the domain it governs,
  per `docs/project-control/open-items/backend.yml`'s own placement) is the established shape. The
  functionality-tracker declaration gets its own colocated file with the same schema — not a merged
  multi-domain config file, and not a differently-shaped one.
- **Preserve domain-agnostic portability** — the same founding-premise driver ADR-0002/ADR-0003
  already applied: the kit scaffolds into non-GitHub and offline projects, so `markdown` stays the
  universal default; `github` is opt-in per project.
- **Capabilities stay out of scope.** Whatever this ADR decides for functionality identity must not
  require or imply moving `C-N.M` capability identity into the tracker.
- **The reference implementation already exists and is real.** Design the primitive mapping to
  match what the downstream project's script actually built and verified (139/139 issues, 0
  hierarchy mismatches, 0 dual-storage mismatches, idempotent re-run proven), not a fresh design
  from first principles.

## Considered Options

1. **Pluggable backend, `github` first, `spec-functional-breakdown-structure`-scoped `backend.yml`
   (chosen).** The skill gains a `backend:` setting (`markdown` | `github`), mirroring
   `util-open-items`'s exactly. `markdown` keeps today's hand-minted `C-N.M.FXX` behaviour
   unchanged. `github` creates an issue per functionality (and per epic, via
   `plan-delivery-roadmap`) and adopts the returned issue number as identity.
2. **Hardcode GitHub, no abstraction.** Simplest to build; breaks the kit's domain-agnostic premise
   the same way ADR-0002's Option 2 would have for open items. Rejected for the same reason.
3. **Status quo — keep hand-minting `C-N.M.FXX`.** No new work, but the reference implementation
   already proves the tracker does the job better (free monotonic ID, native hierarchy,
   unfakeable closure), and a real project has already migrated past this scheme once (the
   downstream project's ADR-0050/0051 pair retired `C-N.M.FXX` for exactly this reason). Rejected —
   the kit would be behind a project already using it.
4. **GitHub Issues become the universal default for FBS.** Rejected on the same grounds ADR-0003
   already settled for open items: hard-requires GitHub + `gh` auth + network for every project,
   breaking non-GitHub and offline projects. Not re-litigated here — ADR-0003's reasoning transfers
   directly.

## Decision Outcome

Chosen option: **Option 1 — pluggable backend, `github` implemented first, opt-in per project.**

This decision is coupled to ADR-0002/ADR-0003's already-settled shape, not a fresh design: `github`
stays opt-in (ADR-0003's conclusion applies here without re-derivation — the same portability
constraint, the same evidence), and the backend abstraction exists so a project can adopt `github`
for functionality identity without the kit acquiring a hard GitHub dependency.

### Config surface

New file, `docs/product-specs/backend.yml` (colocated with the FBS/roadmap artefacts it governs,
mirroring `docs/project-control/open-items/backend.yml`'s own placement convention exactly):

```yaml
# Functionality-tracker backend declaration (spec-functional-breakdown-structure,
# plan-delivery-roadmap). Read by both skills. Absent file => markdown (default).
backend: github
repo: <owner>/<repo>
project: <Project v2 number>   # optional — required only if epics/functionalities get Project-fielded
```

Same three fields as the open-items `backend.yml`, same absent-file-means-markdown default. A
project running both `open-items` and FBS on `github` declares two files (one per domain) — this
mirrors the domain-scoped-file convention rather than merging domains into one config, per the
decision driver above.

### GitHub primitive mapping (when `backend: github`)

| FBS model field | GitHub primitive |
| :--- | :--- |
| `C-N.M.FXX` (functionality ID) | Issue number `#N` (native; `C-N.M.FXX` minting retired in this backend) |
| Epic (delivery-roadmap grouping) | Parent issue, `type:epic` label |
| Functionality | Native sub-issue of its epic (`addSubIssue`), `type:functionality` label |
| `C-N.M` (capability link) | **Dual-stored**: a Project `Capability` single-select field **and** a `Capability: C-N.M` line in the issue body — same dual-storage rationale ADR-0051 already gave for a downstream project's tracker config (Actions' `GITHUB_TOKEN` cannot hold `read:project`, so any CI assertion needs the body line as a token-free fallback) |
| Status (⬜/🔄/✅) | Project `Status` single-select field |
| Cross-functionality reference (a functionality's description mentioning another) | Native `#N` link — resolved via a two-pass create-then-patch, exactly as the reference implementation does: unresolvable-at-creation-time references (the target doesn't exist yet) go in as plain text and get patched once the target exists |
| Idempotency | A hidden HTML comment marker (`<!-- <skill>-seed: <manifest-key> -->`) in every issue body; re-runs match on the marker and create only what's missing — never re-scanned for cross-reference resolution (a caught bug in the reference implementation: the marker literally spells out its own ID and must be excluded from reference-resolution scanning, not just from rendering) |

### Tooling consequences

- **`spec-functional-breakdown-structure`** (kit skill) gains a mode that reads `backend.yml`, and
  when `backend: github`, creates an issue per functionality instead of minting `C-N.M.FXX` into
  Markdown, adopting the returned number as identity. `markdown` mode is unchanged.
- **`plan-delivery-roadmap`** (kit skill) gains the inverse capability: read existing functionality
  issues from the configured backend and *propose* an epic grouping over them, rather than the
  markdown-authored-then-migrated flow this ADR's reference implementation used. This is a genuine
  workflow inversion — functionalities are born in the backend, epics are proposed over an existing
  inventory — not just a new output format for the same input.
- **`util-epic-estimate`** is *not* a kit skill (it is project-local to the downstream project that
  produced the reference implementation) and is therefore out of this ADR's scope. It is noted as a
  downstream consequence: any project adopting the `github` backend for FBS will eventually want its
  own estimation tooling to read the backend directly rather than parse a Markdown roadmap document.
  That rework happens in the consuming project, not the kit.
- `docs/product-specs/spec-functional-breakdown-structure`-family reference docs need a `github`
  backend section analogous to `util-open-items/references/github-backend.md`.

### Data model & interoperability

- **Schema-interoperable always; instance-interoperable once, one-way** — the same posture
  ADR-0002 took. A `markdown → github` migration is sanctioned at adoption time; bidirectional or
  concurrent sync is not (two live writers over two ID spaces is the dual-source-of-truth
  anti-pattern ADR-0002 already named).
- **The crossing is lossy by design**, same as `OI-NNNN → #N`: `C-N.M.FXX` retires in favour of
  `#N`. A migration must emit a `C-N.M.FXX → #N` map so historical citations remain decodable — the
  reference implementation's `07-issue-map.yaml` is the concrete shape this takes.
- Portability gaps ADR-0002's dogfooding already found (Issue Types are org-level → `type:` label
  fallback; ledger `owner` ≠ GitHub login → mapping; label/Project bootstrap needed) apply here
  without needing re-discovery — build the `github` backend mode with these already fixed, not as a
  second round of the same findings.

### Positive Consequences

- Native, monotonic, never-recycled functionality ID for free; no `C-N.M.FXX` minting in this
  backend.
- Native sub-issue hierarchy replaces a markdown table's implicit epic→functionality grouping with
  a structurally-enforced one.
- A Project view is a materially better read-out than a static Markdown FBS table, same argument
  ADR-0002 made for open items.
- The reference implementation is not hypothetical — it is measured, verified evidence (139/139
  issues reconciled, 0 hierarchy mismatches, 0 dual-storage mismatches, idempotency proven live)
  from a real adoption, the same "dogfood before generalising" discipline ADR-0002/ADR-0003 already
  modelled.

### Negative Consequences

- A second functionality-identity backend to build and maintain in
  `spec-functional-breakdown-structure`, on top of the two `util-open-items` already carries.
- For the `github` backend, FBS authoring now requires `gh` auth and network access — the
  functionality inventory's history leaves the repo and is no longer air-gapped-auditable, same
  trade-off ADR-0002 already accepted for open items.
- `plan-delivery-roadmap`'s workflow inversion (propose epics over an existing backend inventory,
  rather than author-then-migrate) is a larger design change than a thin backend wrapper — it is not
  free to build even with the reference implementation as a guide.
- Two capability-linking mechanisms now exist in parallel across the kit's skill families (this
  ADR's dual-storage pattern and ADR-0051's, in different repos) — acceptable because they describe
  the same underlying constraint (`GITHUB_TOKEN` cannot hold `read:project`), but a future reader
  needs to know both exist.

## Open Items

| Item | Resolution path | Priority |
| :--- | :--- | :--- |
| Add `backend:` setting + `github` mode to `spec-functional-breakdown-structure` (create-issue, adopt-ID, idempotency-marker, two-pass reference resolution) | Implement per the primitive mapping above; port the reference implementation's caught marker-scanning bug fix (exclude the trailer from reference resolution) as a starting correctness constraint, not something to rediscover | high |
| Add the workflow-inversion mode to `plan-delivery-roadmap` (read backend functionality issues, propose an epic grouping) | Design as its own increment — larger than the FBS-side backend wrapper | high |
| Author `docs/product-specs/backend.yml`'s schema doc + a `github-backend.md` reference for `spec-functional-breakdown-structure`, mirroring `util-open-items/references/github-backend.md` | Write alongside the skill implementation | medium |
| Build a one-way `markdown C-N.M.FXX → github #N` migration mode, emitting the ID map | Mirror `util-open-items`'s Mode 7 migration design | medium |
| Update `rules/open-items-governance.md`-equivalent FBS governance doc (if one exists / gets created) to describe the two-backend model | Follow ADR-0002's own tooling-consequences precedent | low |
| **Deferred, own future ADR:** should `util-epic-estimate`'s *mechanism* (read functionality/epic issues from a backend, combine with role-rate calibration, produce a dual-track estimate) move to the kit, with calibration supplied per-project rather than baked in? | Blocked on this ADR's own Open Items landing first (the estimator needs the GitHub-issue shape to exist before it can be redesigned to read it). Also blocked on `util-codebase-valuation`'s own status — `util-epic-estimate` depends on its output, and that skill is *also* project-local for the same calibration-specificity reason; moving one without resolving the other creates a kit skill depending on a project-local skill. Needs a calibration-injection design (mechanism in the kit, Swiss rates / measured founder velocity / any project's own numbers supplied as project-local config) before a move is even well-formed — not a file move. Raised 2026-08-13, not decided | deferred |
