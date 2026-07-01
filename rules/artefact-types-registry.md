---
paths:
  - "docs/**"
  - "rules/artefact-types-registry.md"
---

# Artefact Types Registry

The canonical registry of every artefact type the kit mints and its structural facts —
one row per type. Build order, dependencies, and the ER live in
[`metamodel.md`](metamodel.md); per-type semantics live in each minting skill's `SKILL.md`
`## Canonical definition` section.

**OKF `type` source (2026-07-01).** Every generated artefact carries a **`type:` frontmatter
field** — the required field of
[Open Knowledge Format (OKF) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md).
Per OKF idiom the value is a **human-readable display name** (Title Case), because `type`
doubles as the consumer-facing presentation label. These display names are **defined here, not
inferred by the LLM** — the [OKF `type` display names](#okf-type-display-names) table below is
the single source of truth. The snake_case `type` column in the registry remains the internal
stable key (row identity, audit lookup, folder logic); the `okf_type` display value is what a
skill writes into `type:` (full frontmatter schema in
[`artefact-frontmatter.md`](artefact-frontmatter.md), an OKF superset). Adding or renaming a
type means updating **both** the row's snake_case key and its `okf_type` display value, which
changes the emitted `type:` and the audit's accepted enum.

## Columns

- `type` — the snake_case identifier (internal stable key: row identity, audit lookup, folder logic).
- `okf_type` — the Title-Case **display name** written into the artefact's `type:` frontmatter field (OKF-idiomatic). Defined canonically in the [OKF `type` display names](#okf-type-display-names) table, not in the row below.
- `minting skill` — the skill that produces the type.
- `id_format` — the business-ID regex (`—` when the type mints no ID).
- `layout` — `single-collection` (many instances in one file), `one-per-artefact` (one file
  per instance), or `inherits-from-parent` (file binding inherited from `parent`).
- `default_path` — canonical output location template.
- `review_interval` — staleness cadence (`30d` / `60d` / `90d` / `180d`).
- `frontmatter_conditionals` — per-type frontmatter fields beyond the universal
  `supersedes` / `superseded_by` pair (`—` when none).
- `property_schema_ref` — the property-model reference (`_TBD_` until defined).

## Registry

| type | minting skill | id_format | layout | default_path | review_interval | frontmatter_conditionals | property_schema_ref |
|---|---|---|---|---|---|---|---|
| `vision` | `business-vision` | — | one-per-artefact | `docs/VISION.md` | `180d` | — | _TBD_ |
| `persona` | `business-persona` | `P-\d{2}` | single-collection | `docs/business/01a-personas.md` | `180d` | — | _TBD_ |
| `canvas` | `business-model-canvas` | — | one-per-artefact | `docs/business/02a-{slug}.md` | `90d` | — | _TBD_ |
| `bmc_block` | `business-model-canvas` | `[A-Z]{2}-\d+` | inherits-from-parent (`canvas`) | _(inherits `canvas`)_ | `90d` | — | _TBD_ |
| `capability` | `business-capability-map` | `C\d+(\.\d+){0,2}` | single-collection | `docs/business/03a-capability-map.md` | `180d` | — | _TBD_ |
| `value_stream` | `business-value-stream` | `VS-\d+` | single-collection | `docs/business/04a-value-streams.md` | `90d` | — | _TBD_ |
| `vs_stage` | `business-value-stream` | `VS-\d+\.\d+` | inherits-from-parent (`value_stream`) | _(inherits `value_stream`)_ | `90d` | — | _TBD_ |
| `objective` | `business-objective` | `OBJ-\d{2}` | single-collection | `docs/business/04b-objectives.md` | `60d` | — | _TBD_ |
| `key_result` | `business-objective` | `KR-\d{2}\.\d+` | inherits-from-parent (`objective`) | _(inherits `objective`)_ | `60d` | — | _TBD_ |
| `process` | `business-process` | — | one-per-artefact | `docs/business/05a-processes/proc-{nn}-{slug}.md` | `90d` | — | _TBD_ |
| `quantitative_model` | `business-quantitative-model` | — | one-per-artefact | `docs/business/06a-models/qm-{nn}-{topic}.md` | `90d` | — | _TBD_ |
| `competitor` | `business-competitive-landscape` | `CO-\d{2}` | one-per-artefact | `docs/business/01b-competitive-landscape/{slug}.md` | `90d` | — | _TBD_ |
| `bounded_context` | `domain-bounded-context` | `BC-\d{2}` | single-collection | `docs/domain/02b-bounded-contexts.md` | `180d` | — | _TBD_ |
| `glossary_term` | `domain-glossary` | `BC-\d{2}\.GT-\d{2}` | single-collection | `docs/domain/02c-glossary.md` | `180d` | — | _TBD_ |
| `fbs_functionality` | `spec-functional-breakdown-structure` | `C\d+\.\d+\.F\d{2}` | single-collection | `docs/product-specs/07a-fbs.md` | `90d` | — | _TBD_ |
| `domain_model` | `domain-model` | — | one-per-artefact | `docs/domain/07b-models/{bc-slug}.md` | `180d` | — | _TBD_ |
| `aggregate` | `domain-model` | `BC-\d{2}\.AGG-\d{2}` | inherits-from-parent (`domain_model`) | _(inherits `domain_model`)_ | `180d` | — | _TBD_ |
| `entity` | `domain-model` | `BC-\d{2}\.ENT-\d{2}` | inherits-from-parent (`domain_model`) | _(inherits `domain_model`)_ | `180d` | — | _TBD_ |
| `value_object` | `domain-model` | `BC-\d{2}\.VO-\d{2}` | inherits-from-parent (`domain_model`) | _(inherits `domain_model`)_ | `180d` | — | _TBD_ |
| `domain_event` | `domain-model` | `BC-\d{2}\.EVT-\d{2}` | inherits-from-parent (`domain_model`) | _(inherits `domain_model`)_ | `180d` | — | _TBD_ |
| `interface_contract` | `arch-service-contract` | `(BC-\d{2}\.)?CTR-\d{2}` | one-per-artefact | `docs/architecture/interfaces/{bc-slug}.md` | `90d` | — | _TBD_ |
| `epic` | `plan-delivery-roadmap` | `E-\d{2}` | single-collection | `docs/plans/delivery-roadmap.md` | `60d` | — | _TBD_ |
| `cli_surface` | `arch-cli-contract` | `(BC-\d{2}\.)?CLI-\d{2}` | one-per-artefact | `docs/architecture/interfaces/cli-{slug}.md` | `90d` | — | _TBD_ |
| `cli_command` | `arch-cli-contract` | `(BC-\d{2}\.)?CLI-\d{2}\.CMD-\d{2}` | inherits-from-parent (`cli_surface`) | _(inherits `cli_surface`)_ | `90d` | — | _TBD_ |
| `quality_attribute` | `spec-quality-attributes` | `QA-[A-Z]{2}\d{2}` | single-collection | `docs/product-specs/09a-quality-attributes.md` | `60d` | — | _TBD_ |
| `use_case` | `spec-use-case` | `UC-\d{2}` | one-per-artefact | `docs/product-specs/use-cases/uc-{nn}-{slug}.md` | `60d` | — | _TBD_ |
| `prd` | `spec-prd` | `PRD-\d{4}` | one-per-artefact | `docs/product-specs/prds/prd-{nnnn}-{feature}.md` | `30d` | — | _TBD_ |
| `implementation_plan` | `plan-implementation` | `Plan-\d{4}` | one-per-artefact | `docs/plans/active/{nnnn}_exec_{slug}.md` | `30d` | — | _TBD_ |
| `adr` | `arch-adr` | `ADR-\d{4}` | one-per-artefact | `docs/architecture/decisions/adr-{nnnn}-{slug}.md` | `180d` | `supersedes`, `superseded_by` | _TBD_ |
| `research` | `arch-research` | `Research-\d{4}` | one-per-artefact | `docs/architecture/research/{nnnn}-{slug}.md` | `90d` | — | _TBD_ |
| `idea` | `discovery-idea` | `IDEA-\d{4}` | one-per-artefact | `docs/discovery/ideation/IDEA-{nnnn}-{slug}.md` | `90d` | `graduates_to` | _TBD_ |
| `runbook` | `ops-runbook` | — | one-per-artefact | `docs/ops/runbooks/{slug}.md` | `90d` | — | _TBD_ |
| `bug_rca` | `ops-bug-rca` | — | one-per-artefact | `docs/ops/rcas/{date}-{slug}.md` | `90d` | — | _TBD_ |
| `stack_guide` | `dev-stack-guide` | — | one-per-artefact | `docs/dev-guides/{tech-slug}.md` | `90d` | — | _TBD_ |
| `getting_started` | `dev-getting-started` | — | one-per-artefact | `docs/dev-guides/getting-started.md` | `180d` | — | _TBD_ |
| `research_note` | `discovery-research` | — | one-per-artefact | `docs/discovery/interviews/{slug}.md` | `90d` | — | _TBD_ |
| `workshop_note` | `discovery-workshop` | — | one-per-artefact | `docs/discovery/workshops/{slug}.md` | `90d` | — | _TBD_ |
| `design_system` | `ux-design-system` | — | one-per-artefact | `docs/ux/design-system.md` | `180d` | — | _TBD_ |
| `arc42_section` | `arch-arc42` | — | one-per-artefact | `docs/architecture/arc42/{nn}-{slug}.md` | `180d` | — | _TBD_ |

> **Supporting doc-types (2026-07-01).** The rows above `runbook`…`arc42_section` are doc-producing skills that mint **no business ID** (`id_format` `—`) but write `docs/**` markdown that OKF requires to carry a `type`. They were added to the registry when the OKF baseline made `type` mandatory for every concept document. They are not steps in the linear build order (see `metamodel.md` supporting-skills list). **`arc42_section` (KISS):** all eight arc42 section files share the one display name `Architecture Documentation`, disambiguated by the section number in their `title` (and by the `CST-NN`/`SCN-NN`/`CC-NN`/`RSK-NN` sub-IDs they mint); `arch-arc42` owns the frontmatter even for §3/§5/§7 where `arch-c4` fills the DSL-derived tables (ADR-0004).

## OKF `type` display names

Canonical, metamodel-defined mapping from each registry key to the exact string a skill writes
into the artefact's `type:` frontmatter field. **Skills emit the `okf_type` value verbatim —
never invent, translate, or re-case it.** The audit validates the emitted `type:` against this
column. For a `single-collection` file (many instances in one file), the file carries the
singular `okf_type` of the instances it holds (e.g. `01a-personas.md` → `type: Persona`); this
is revisited if per-instance explosion ships (issue #54).

| registry key (`type`) | emitted `type:` (`okf_type`) |
|---|---|
| `vision` | `Product Vision` |
| `persona` | `Persona` |
| `canvas` | `Business Model Canvas` |
| `bmc_block` | `Business Model Canvas Block` |
| `capability` | `Business Capability` |
| `value_stream` | `Value Stream` |
| `vs_stage` | `Value Stream Stage` |
| `objective` | `Business Objective` |
| `key_result` | `Key Result` |
| `process` | `Business Process` |
| `quantitative_model` | `Quantitative Model` |
| `competitor` | `Competitor Profile` |
| `bounded_context` | `Bounded Context` |
| `glossary_term` | `Glossary Term` |
| `fbs_functionality` | `Functionality` |
| `domain_model` | `Domain Model` |
| `aggregate` | `Aggregate` |
| `entity` | `Entity` |
| `value_object` | `Value Object` |
| `domain_event` | `Domain Event` |
| `interface_contract` | `Interface Contract` |
| `epic` | `Epic` |
| `cli_surface` | `CLI Surface Contract` |
| `cli_command` | `CLI Command` |
| `quality_attribute` | `Quality Attribute` |
| `use_case` | `Use Case` |
| `prd` | `Product Requirements Document` |
| `implementation_plan` | `Implementation Plan` |
| `adr` | `Architecture Decision Record` |
| `research` | `Architecture Research Note` |
| `idea` | `Idea` |
| `runbook` | `Runbook` |
| `bug_rca` | `Bug RCA` |
| `stack_guide` | `Stack Guide` |
| `getting_started` | `Getting Started Guide` |
| `research_note` | `Research Note` |
| `workshop_note` | `Workshop Note` |
| `design_system` | `Design System` |
| `arc42_section` | `Architecture Documentation` |

## Maintenance coupling

| What changed | Update |
|---|---|
| New type, or a change to its id_format / path / layout / skill / interval | this file (the type's row) |
| New type, or a change to its `okf_type` display name | this file — the [OKF `type` display names](#okf-type-display-names) table + `util-metamodel-audit` Check 17 `type` enum |
| A type's semantics | the minting `SKILL.md` `## Canonical definition` |
| Build order / dependencies / ER | [`metamodel.md`](metamodel.md) |
