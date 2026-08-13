# Delivery Roadmap — GitHub Backend Reference (epic-side mapping)

Operational reference for the `github` backend of `plan-delivery-roadmap`. This file travels
with the skill (symlinked into `~/.claude/skills/`), so it is available to every project that
selects the backend **without ever being copied into a project's `docs/`**.

## Authority boundary

- **`adr-0010`** (in the consuming repo's `docs/architecture/decisions/`, e.g. the kit) owns
  the decision — why this is a genuine workflow inversion, not a thin wrapper.
- **`spec-functional-breakdown-structure/references/github-backend.md`** owns the
  **functionality-side** mapping (the inventory this skill reads). Read it first — this file
  assumes it.
- **This reference owns the epic-side mapping only**: how a proposed grouping over an
  existing functionality inventory becomes an epic issue, and the sub-issue relationship that
  replaces a hand-authored FBS-scope table.
- **`SKILL.md` §Backends and §Mode 2** own the authoring-time procedure. Where this file and
  `SKILL.md` diverge, `SKILL.md` wins on procedure; this file wins on wire format.

## Scope

Same `docs/product-specs/backend.yml` that `spec-functional-breakdown-structure` reads — one
config file, one domain, two skills. `github` is opt-in per project; `markdown` stays the
default (same portability posture `adr-0003`/`adr-0010` already established, reused here
rather than re-derived).

---

## 1. Canonical field slugs (epic scope)

| Slug | Roadmap model field | Domain |
| :--- | :--- | :--- |
| `epic_id` | `E-NN` (markdown) / issue number (github) | identity — realized per backend, §2 |
| `name` | Epic name | value-oriented phrasing, per `SKILL.md` Step 2 |
| `vs_anchor` | `VS-N.M` | unaffected by backend — read from `docs/business/04a-value-streams.md`, which stays markdown regardless of FBS backend (out of `adr-0010`'s scope) |
| `fbs_scope` | The member functionality issues | native sub-issue set, §2 |
| `phase` | Phase 1/2/3 tag | **not mapped** — see §5, a known gap |
| `differentiator` (★) | Differentiator anchor marker | **not mapped** — see §5, a known gap |
| `status` | Epic-level roll-up | not automatically derived in this increment — operator sets it if a `project` Status field exists |

## 2. GitHub serialization

| Canonical slug | GitHub home | Mechanism |
| :--- | :--- | :--- |
| `epic_id` | Issue **number** `#N` | native; `E-NN` minting retired in this backend, mirroring `C-N.M.FXX`'s retirement on the functionality side |
| `name` | Issue **title** | plain epic name, no ID prefix |
| `fbs_scope` | Native **sub-issues** | each member functionality issue is attached via `addSubIssue` (GraphQL — the `gh` CLI has no sub-issue subcommand as of this mapping; use `gh api graphql` the same way Project custom-field creation needed the GraphQL API directly when the CLI only exposed a subset) |
| `type:epic` label | Issue label | marks the issue as roadmap-governed, mirroring `type:functionality` on the FBS side |
| Capability rollup | **Not stored on the epic issue.** An epic can span multiple capabilities (Step 1 heuristic #2 explicitly allows a setup epic to cross `C1`+`C2`); each member functionality already carries its own `Capability:` line (dual-stored per the FBS reference) — read that off the members, don't duplicate it on the epic. | |

Everything the current `markdown`-mode §Epic Table / §Per-epic §FBS-scope table renders is a
**read-out** of this graph (epic issue → its sub-issues → each sub-issue's `Capability:` /
`VS stage:` lines) under `backend: github`, not a hand-authored table — see `SKILL.md` §Mode
2 Step 6.

---

## 3. Workflow inversion — what's mechanical vs what needs the operator

Mode 2 reads an **existing** functionality inventory and proposes groupings, rather than
enumerating functionalities freshly the way Mode 1 does from a markdown FBS. Not every
grouping heuristic in `SKILL.md` §Step 1/§Step 3 has a GitHub primitive to read from:

| Heuristic | Backend availability | github-mode behaviour |
| :--- | :--- | :--- |
| VS stage affinity | `VS stage:` body line, when the functionality issue carries one (optional per the FBS mapping) | mechanical, when present; functionalities with no `VS stage:` line behave like the markdown mode's `—` case |
| Capability domain coherence | `Capability:` body line (dual-stored, always present) | mechanical |
| Differentiator anchoring (★) | **no primitive** | propose groupings without it, then ask the operator which functionalities are differentiators before finalising — do not invent a label unprompted (see §5) |
| Phase boundary | **no primitive** | same as above — surfaced as an explicit operator decision per proposed epic, not inferred |
| Sizing check (5–25 rows) | issue count per proposed group | mechanical |

Pain-index ordering (Step 3) is **unaffected** — it reads `docs/business/04a-value-streams.md`
directly, which stays markdown regardless of the FBS backend (out of `adr-0010`'s scope).
Personas likewise read from `docs/business/01a-personas.md` unchanged.

## 4. Creating the epic

1. `gh issue create --repo <repo> --title "<name>" --label type:epic` — capture the returned
   issue number.
2. For each member functionality issue, resolve both issues' GraphQL node IDs
   (`gh api graphql` query on `repository.issue(number:).id`) and call the `addSubIssue`
   mutation with the epic as parent.
3. If `project` is set in `backend.yml`, add the epic issue to that Project (no dedicated
   epic-level field beyond `Status`, set manually — see §1).

No idempotency marker is defined for epics in this increment: epic creation is an
operator-confirmed, one-shot proposal step (not a re-run batch import like the functionality
side), so accidental duplication is a review-time concern, not a re-run concern. Revisit if a
future increment adds a batch epic-migration mode.

---

## 5. Known gap — phase and differentiator have no GitHub primitive

Neither is invented here. The markdown-mode heuristics that key off "phase tag (Phase
1/2/3)" and "★ marker" (`SKILL.md` Step 1) assume per-functionality FBS columns that, on
inspection, the current `spec-functional-breakdown-structure` template does not actually
carry either (its functionality table is `ID | Functionality | Status | VS stage` — no Phase
or ★ column) — this is a pre-existing gap in the `markdown` backend, not something this
increment introduces or is scoped to fix. Under `github`, the gap is simply more visible: Mode
2 surfaces phase and differentiator as explicit questions to the operator at proposal time
rather than silently reading a column that was never reliably populated. A future increment —
candidate labels `phase:1|2|3` and `differentiator` on functionality issues — would need its
own design pass (which level owns the signal, when it's set, how it interacts with the FBS
side's idempotency marker) and is not decided by this reference.

---

## 6. Invariants

- **I1** — `type:epic` label ≡ this backend's epic marker; `adr-0010`'s primitive mapping is
  the single source both `SKILL.md` and any future migration script bind to.
- **I2** — Epic membership is expressed structurally (sub-issues), never by a hand-typed list
  in a body — the same "closure/relationship is native, not re-typed" posture
  `util-open-items` applies to `tracker_ref`.
- **I3** — Capability is never duplicated onto the epic issue; it is read off member
  functionality issues, single source per functionality (§2).
- **I4** — Phase and differentiator are operator-confirmed at proposal time in this
  increment, never silently inferred or defaulted (§5).

---

## See also

- `spec-functional-breakdown-structure/references/github-backend.md` — the functionality-side
  mapping this file assumes as its input inventory.
- `adr-0010` (in a consuming repo's `docs/architecture/decisions/`, e.g. the kit) — the
  decision this mapping implements.
- `SKILL.md` §Backends, §Mode 2 — the authoring-time procedure that invokes this mapping.
