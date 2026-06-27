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

## Columns

- `type` — the snake_case identifier.
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

## Maintenance coupling

| What changed | Update |
|---|---|
| New type, or a change to its id_format / path / layout / skill / interval | this file (the type's row) |
| A type's semantics | the minting `SKILL.md` `## Canonical definition` |
| Build order / dependencies / ER | [`metamodel.md`](metamodel.md) |
