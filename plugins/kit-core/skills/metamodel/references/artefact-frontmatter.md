# Artefact Frontmatter Convention

Every markdown file produced by a kit skill under `docs/` must open with this YAML frontmatter block.

**OKF baseline (2026-07-01).** This schema is a backward-compatible **superset of Google Cloud's [Open Knowledge Format (OKF) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)**. The six OKF fields (`type`, `title`, `description`, `resource`, `tags`, `timestamp`) come first; the kit's lifecycle fields (`status`, `owner`, `last_reviewed`, `review_interval`, and the supersession pair) follow as OKF *extension* fields — OKF requires consumers to accept unknown fields, so they never break conformance. The result: any `docs/` tree the kit produces is a conformant OKF bundle, ingestible by OKF consumers (Google Knowledge Catalog, the OKF graph visualiser, OKF-speaking agents), while keeping every richer metamodel guarantee. Scope note: this applies to the artefacts the kit **generates**; making the kit's own `skills/` + `rules/` an OKF bundle is deferred (issue #53).

**Exemption — README, index, and log files.**

- Any file literally named `README.md` (case-sensitive) at any depth under `docs/` is exempt. READMEs are tool-, folder-, or vendor-level navigation aids whose lifecycle does not match the artefact review cadence. Adding artefact frontmatter to a README implies strategic content it does not carry and forces a noisy `review_interval`. Examples that stay frontmatter-free: a notebook's runtime `analysis/README.md`, a vendored package's `README.md`, a folder-level "what lives here" `README.md`.
- `index.md` and `log.md` are **OKF reserved files** (see §Reserved files below) — they are directory-navigation / history aids, **not** artefact concept documents, and are exempt from the artefact frontmatter block. The **root** `docs/index.md` is the sole exception: it carries a minimal frontmatter block containing only `okf_version` (see below).

> **Migration note (INDEX.md → index.md).** The kit previously produced an uppercase `INDEX.md` navigation hub that *required* artefact frontmatter. As of the OKF baseline, that hub is the lowercase OKF-reserved **`index.md`** (frontmatter-free, except the root's `okf_version`). Its rich nav content (the ✅/🔄/⬜ stack-progress table) lives in the file **body**. the `metamodel` skill's Scaffold mode produces `index.md`; any legacy `INDEX.md` is migrated with `git mv INDEX.md index.md` + frontmatter strip.

```yaml
---
type: <canonical OKF display name — the artefact's okf_type from rules/artefact-types-registry.md>
title: <human-readable title of this specific document instance>
description: <one-sentence summary of what this document instance is>
resource: <URI of the underlying asset this documents — omit the line when there is none>
tags: [<tag>, <tag>]
timestamp: <ISO 8601 datetime of last change, e.g. 2026-07-01T14:30:00Z>
status: draft
owner: <git config user.name>
last_reviewed: YYYY-MM-DD
review_interval: Nd
---
```

**Always present:** `type`, `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`. `resource` is present **only when the artefact documents an external addressable asset** (a service endpoint, a dataset, a repo) — most strategic artefacts have none, so the line is omitted (OKF marks `resource` recommended, not required). Two further fields appear only on a lifecycle event — never in an initial scaffold:

| Field | When it appears |
|---|---|
| `superseded_by` | Added when `status` switches to `superseded`. Points to the replacement. |
| `supersedes` | Added only on documents created specifically to replace another. Points to what was replaced. |

---

## Reserved files (OKF)

Per OKF v0.1, two filenames are reserved across every directory of a bundle. The kit adopts them as the standard for `docs/` and its subfolders.

| File | Purpose | Frontmatter |
|---|---|---|
| `index.md` | Optional per-directory listing enabling **progressive disclosure** as an agent walks the tree. Body is free-form (the kit uses it for the folder's nav hub / stack-progress table). | **None**, except the **root** `docs/index.md`, which carries only `okf_version: "0.1"`. |
| `log.md` | Optional chronological change history for a directory. | None. |

- **Every folder under `docs/` may carry an `index.md`** (and optionally a `log.md`). At minimum the bundle root `docs/index.md` exists (produced by the `metamodel` skill's Scaffold mode).
- **Version declaration:** only the root `docs/index.md` declares the bundle's target OKF version:

```yaml
---
okf_version: "0.1"
---
# <Project> — documentation index
… stack-progress table + navigation …
```

- All other `.md` files under `docs/` (except `README.md`) are **concept documents** and MUST carry the full artefact frontmatter block above.

---

## Field rules

**`type`** — the artefact's canonical **OKF display name**: the `okf_type` value from the [OKF `type` display names](artefact-types-registry.md#okf-type-display-names) table (`Product Vision`, `Persona`, `Business Capability`, `Product Requirements Document`, …). This is OKF's **only required field**, and per OKF idiom it is a human-readable Title-Case string that doubles as the consumer-facing presentation label. **Emit the registry's value verbatim — never invent, translate, or re-case it.** It must be non-empty and match a registered `okf_type`; a value not in the registry is tolerated by OKF consumers but flagged by the audit.
- ✅ `type: Product Requirements Document`
- ✅ `type: Persona`
- ❌ `type: prd` (snake_case internal key — not the OKF display value)
- ❌ empty / missing (breaks OKF conformance)

**`title`** — instance title, not the artefact type name.
- ✅ `"Payment Bounded Context Map"`
- ✅ `"PRD-0003 — Bulk Invoice Export"`
- ❌ `"Bounded Context Map"` (generic type — says nothing about the project)

**`description`** — a single sentence summarising this document instance. Human- and agent-facing; OKF consumers use it for listing/preview. Keep it specific to the instance, not the type.

**`resource`** — a URI uniquely identifying the underlying asset the document describes, when one exists (e.g. a deployed endpoint for an interface contract, a dataset URL). **Omit the line entirely when the artefact has no external asset** — do not emit an empty or placeholder value.

**`tags`** — a YAML list of categorisation strings (free-form; e.g. the bounded context slug, the epic id, a domain keyword). Used by OKF consumers for filtering. May be an empty list `[]` on scaffold.

**`timestamp`** — ISO 8601 datetime of the **last change** to the file (e.g. `2026-07-01T14:30:00Z`). Distinct from `last_reviewed` (last human *review*): `timestamp` bumps on every edit; `last_reviewed` bumps only on a review. Set both on meaningful edits.

**`status`** — one of four values:
- `draft` — being written; not yet authoritative; set this on every initial scaffold
- `active` — current and authoritative; decisions may be based on it
- `superseded` — replaced by another document; `superseded_by` is required
- `deprecated` — no longer relevant; kept for history only

**`owner`** — run `git config user.name` at creation time. Update when ownership changes.

**`last_reviewed`** — today's date in `YYYY-MM-DD`. Update on every meaningful review or edit, not just structural changes.

**`review_interval`** — cadence for staleness checks. Skill-specific defaults below; override per file when the project warrants it.

**`superseded_by`** — added to a document the moment its `status` switches to `superseded`. Relative path to the replacement. Never present on `draft`, `active`, or `deprecated` documents.

**`supersedes`** — added only to a document that was created specifically to replace another. Relative path to what it replaced. Absent on documents that were not written as a replacement for a prior document.

```yaml
# the document being retired:
status: superseded
superseded_by: docs/domain/bounded-contexts-v2.md

# the replacement document (only if it was written to replace the above):
supersedes: docs/domain/02b-bounded-contexts.md
```

---

## Default review intervals by artefact

| Interval | Artefacts |
|---|---|
| `30d` | PRDs · Implementation plans |
| `60d` | Delivery roadmap · Business objectives · Quality attributes |
| `90d` | Value streams · Processes · BMC · Competitive landscape · FBS · Ideas · Runbooks · RCAs · Architecture research |
| `180d` | Vision · Personas · Capability map · Bounded contexts · Glossary · Domain model · ADRs |

**ADR note:** the `## Status` body section is removed from MADR files — frontmatter `status` is the single source of truth. Supersession fields and audit details live in `arch-adr/references/madr-templates.md`.

---

## Cross-linking (OKF graph)

Concept documents link to each other with ordinary markdown links, which OKF treats as **relationship assertions** that turn the directory into a knowledge graph. The kit's [cross-doc linking rule](metamodel.md) (`[ID + name](relative/path.md#anchor)`) is the conformant, ID-stable form of this — keep using it. OKF consumers tolerate broken links, but the audit still verifies them.
