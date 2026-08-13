# FBS — GitHub Backend Reference

Operational reference for the `github` backend of `spec-functional-breakdown-structure`.
This file travels with the skill (symlinked into `~/.claude/skills/`), so it is available to
every project that selects the backend **without ever being copied into a project's
`docs/`**.

## Authority boundary

- **`adr-0010`** (in the consuming repo's `docs/architecture/decisions/`, e.g. the kit) owns
  the decision — why a pluggable backend, why `github` first, why capabilities stay out of
  scope. Read it for rationale; this file does not repeat it.
- **This reference owns the `github` serialization** — how the FBS functionality model maps
  onto GitHub primitives, the cross-reference resolution mechanics, and the identity
  translation.
- **`SKILL.md` §Backends and §Mode 3** own the authoring-time procedure — when this mapping
  gets invoked and by what steps. Where this file and `SKILL.md` diverge, `SKILL.md` wins on
  procedure; this file wins on the wire format.
- **Capability identity (`C-N.M`) is out of scope everywhere.** Per `adr-0010`, capabilities
  stay markdown-authored in the BC Map regardless of backend — this file maps
  *functionalities* only.

## Scope

The `github` backend is **opt-in** per project via `docs/product-specs/backend.yml`;
`markdown` stays the universal default (same portability posture `adr-0003` established for
`util-open-items`, reused here rather than re-derived). Declaration:

```yaml
# docs/product-specs/backend.yml — absent file => markdown (default)
backend: github
repo: <owner>/<repo>
project: <Project v2 number>   # optional — required only for the Status field mapping
```

Same three fields, same absent-file-means-markdown default as
`docs/project-control/open-items/backend.yml`. A project running both `open-items` and FBS
on `github` declares two files, one per domain — domain-scoped config, not a merged one.

---

## 1. Canonical field slugs (functionality scope)

| Slug | FBS model field | Domain |
| :--- | :--- | :--- |
| `functionality_id` | `C-N.M.FXX` (markdown) / issue number (github) | identity (realized per backend — §3) |
| `capability_id` | `C-N.M` | always markdown-authored; never migrates |
| `name` | Functionality name | system-perspective phrasing, per `SKILL.md`'s granularity discipline |
| `status` | ✅ Shipped / 🔄 Planned / ⬜ Backlog | see §2 |
| `vs_stage` | `VS-N.M` (optional) | unaffected by backend — stays a plain reference in the issue body when present |

There is no separate "epic" slug in the FBS model itself — epic grouping is
`plan-delivery-roadmap`'s concern, added over an existing functionality inventory (see
`adr-0010` §Tooling consequences). This backend creates functionality issues standalone;
parenting them under an epic issue happens later, when `plan-delivery-roadmap` runs.

## 2. GitHub serialization

| Canonical slug | GitHub home | Mechanism |
| :--- | :--- | :--- |
| `functionality_id` | Issue **number** `#N` | native; `C-N.M.FXX` minting retired in this backend |
| `name` | Issue **title** | plain functionality name, no ID prefix |
| `capability_id` | **Dual-stored**: a Project `Capability` single-select field (when `project` is configured) **and** a `Capability: C-N.M` line in the issue body — same dual-storage rationale `adr-0051` already gave a downstream project's tracker config (`GITHUB_TOKEN` in Actions cannot hold `read:project`, so any CI assertion needs the body line as a token-free fallback) | `type:functionality` label marks the issue as FBS-governed |
| `status` | Project `Status` single-select field, when `project` is configured; otherwise the issue's open/closed state only distinguishes ✅ from {🔄, ⬜} — a project with no `project:` set cannot represent the 🔄/⬜ distinction and should note that limitation to the user | |
| `vs_stage` | Plain text line in the issue body (`VS stage: VS-N.M`) — no dedicated GitHub primitive; informational only | |
| Cross-functionality reference (a functionality's description mentioning another) | Native `#N` link | resolved via a two-pass create-then-patch — §3 |
| Idempotency | A hidden HTML comment marker in every issue body | §4 |

---

## 3. Cross-reference resolution (two-pass)

Mode 3 typically authors several functionalities in one batch (a capability's full row set,
or a targeted addition). Any functionality description that mentions another functionality
by name may reference a sibling created in the **same** batch, whose issue number doesn't
exist yet at the point the referencing issue is created. Resolve in two passes, exactly as
the reference implementation this backend generalises does:

1. **Pass 1 — create.** For every functionality in the batch, create its issue with the
   resolved content it already has (its own description, capability line, marker) and leave
   any not-yet-resolvable reference as **plain text** (the functionality's name, not a link).
2. **Pass 2 — patch.** Once every issue in the batch exists, re-scan each created issue's
   plain-text references against the batch's name→`#N` map and `gh issue edit --body` the
   resolved links in.

**Caught bug, ported as a starting constraint — do not rediscover it:** the hidden
idempotency marker (§4) itself spells out the functionality's own identity. Pass 2's
reference-resolution scan must exclude the marker from the text it scans, or it flags the
marker's own content as an unresolved reference and attempts to "resolve" it. Compose the
body as two distinct parts — resolved-content and marker trailer — and scan only the former.

## 4. Idempotency marker

Every functionality issue's body carries a hidden HTML comment marker:

```text
<!-- fbs-seed: C-N.M:<functionality-slug> -->
```

`<functionality-slug>` is a stable kebab-case slug derived from the functionality name at
authoring time (github-backend functionalities have no pre-existing `C-N.M.FXX` to key off
— the marker key is capability + slug, not a minted ID). Before creating an issue, search for
an existing one carrying the same marker (`gh issue list --repo <repo> --search "<marker
text>" --state all`); if found, treat the functionality as already present and skip creation
(re-running Mode 3 against an already-populated capability must not duplicate issues).

---

## 5. Interoperability

### 5a. Identity translation

| | `markdown` | `github` |
| :--- | :--- | :--- |
| identity | `C-N.M.FXX` (minted, capability-scoped counter) | `#N` (issue number) |
| ID space | independent | independent |

Migration is **`markdown → github` only**, one-way, performed once at adoption — mirroring
`util-open-items`'s Invariant I2. A migration mode emitting a persisted `C-N.M.FXX → #N` map
(mirroring the reference implementation's `07-issue-map.yaml`) is `adr-0010`'s Open Items
table, a separate increment from this backend's interactive create path — not yet built.

### 5b. Capability identity never migrates

`capability_id` (`C-N.M`) has no github-backend counterpart to migrate to — it is dual-stored
*by reference* (§2), never re-identified. A project on `backend: github` for functionalities
still authors and edits capabilities in the BC Map / FBS markdown structure exactly as today.

### 5c. Open question — the FBS markdown document under `backend: github`

Not resolved by this reference or by `adr-0010`: whether `FBS.md`'s per-capability
functionality table stays a hand-authored artefact, becomes a regenerated read-out queried
from the tracker (mirroring `util-open-items`'s `report` mode), or is dropped in favour of a
direct tracker view once `backend: github` is active. `SKILL.md`'s Mode 3 currently creates
the github issue and adopts its number as identity; it does not yet change what (if anything)
Mode 3 writes back into `FBS.md`'s functionality table. Flag this to the user rather than
silently picking one — the reference implementation's downstream project resolved it by
retiring the markdown FBS entirely, but that is a project-level choice, not a backend
requirement.

---

## 6. Invariants

- **I1** — `type:functionality` label ≡ this backend's functionality marker; `adr-0010`'s
  primitive mapping (§2 here) is the single source both `SKILL.md` and any future migration
  script bind to.
- **I2** — Migration is one-way (`markdown → github`), once, with a persisted ID map; never
  concurrent. One backend per project.
- **I3** — Capability identity is never migrated or re-minted; it is dual-stored by reference
  only (§5b).
- **I4** — The idempotency marker (§4) is excluded from cross-reference scanning (§3) — the
  caught bug this backend ships already fixed, not as a rediscoverable defect.
- **I5** — Filing is direct in both backends: switching backends never introduces or removes
  an authoring step, only where Mode 3 writes to (same posture as `util-open-items`'s I4).

---

## See also

- `adr-0010` (in a consuming repo's `docs/architecture/decisions/`, e.g. the kit) — the
  decision this mapping implements.
- `util-open-items/references/github-backend.md` — the sibling reference this file mirrors
  in shape; read it for the fuller worked example of a slug-map / serialization /
  invariants split, since FBS's model is narrower.
- `SKILL.md` §Backends, §Mode 3 — the authoring-time procedure that invokes this mapping.
