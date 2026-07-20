---
okf_version: "0.1"
---

# Documentation Stack — homemade-claude-kit

> **Scaffolded:** 2026-07-20 · **Last refreshed:** 2026-07-20
>
> Run the Scaffold mode Mode 3 to refresh status.
> Run the Audit mode Mode 2 for a full progress snapshot.
>
> This is the OKF bundle root `index.md` (reserved file — no artefact frontmatter).

> **Note on this repo.** `homemade-claude-kit` is the skill kit itself, not a product built
> through its own full business-strategy spine — it carries a **`VISION.md`** (its north
> star as a harness-agnostic toolkit) but no personas, BMC, or capability map of its own, so
> Steps 1–10 below remain legitimately ⬜. What this repo actually dogfoods is the
> **open-items governance system** (`docs/project-control/open-items/`, github backend) and
> the **use-case registry** (`docs/product-specs/use-cases/`, 11 UCs). Its Architecture
> Decision Records (9) and research notes (3) are also live and current.

---

## Stack progress

Status key: ✅ Done · 🔄 In progress (scaffold exists, needs filling) · ⬜ Not started

| Step | Artefact | Skill | Status | Canonical path | Last modified |
|---|---|---|---|---|---|
| 0 | Product Vision | `business-vision` | ✅ | [`docs/VISION.md`](VISION.md) | 2026-07-20 |
| 1 | Personas | `business-persona` | ⬜ | [`docs/business/01a-personas.md`](business/01a-personas.md) | — |
| 2 | Business Model Canvas | `business-model-canvas` | ⬜ | [`docs/business/02a-bmc.md`](business/02a-bmc.md) | — |
| 2b | Bounded Context Map | `domain-bounded-context` | ⬜ | [`docs/domain/02b-bounded-contexts.md`](domain/02b-bounded-contexts.md) | — |
| 2c | Domain Glossary | `domain-glossary` | ⬜ | [`docs/domain/02c-glossary.md`](domain/02c-glossary.md) | — |
| 3 | Capability Map | `business-capability-map` | ⬜ | [`docs/business/03a-capability-map.md`](business/03a-capability-map.md) | — |
| 4 | Value Streams | `business-value-stream` | ⬜ | [`docs/business/04a-value-streams.md`](business/04a-value-streams.md) | — |
| 4.5 | Business Objectives | `business-objective` | ⬜ | [`docs/business/04b-objectives.md`](business/04b-objectives.md) | — |
| 5 | Business Processes | `business-process` | ⬜ | [`docs/business/05a-processes/`](business/05a-processes/) | — |
| 6 | Quantitative Models | `business-quantitative-model` | ⬜ | [`docs/business/06a-models/`](business/06a-models/) | — |
| 7 | Functional Breakdown Structure | `spec-functional-breakdown-structure` | ⬜ | [`docs/product-specs/07a-fbs.md`](product-specs/07a-fbs.md) | — |
| 7b | Domain Model | `domain-model` | ⬜ | [`docs/domain/07b-models/`](domain/07b-models/) | — |
| 8 | Delivery Roadmap | `plan-delivery-roadmap` | ⬜ | [`docs/plans/delivery-roadmap.md`](plans/delivery-roadmap.md) | — |
| 9 | Quality Attributes | `spec-quality-attributes` | ⬜ | [`docs/product-specs/09a-quality-attributes.md`](product-specs/09a-quality-attributes.md) | — |
| 9.5 | Use Cases | `spec-use-case` | ✅ | [`docs/product-specs/use-cases/`](product-specs/use-cases/) (11 UCs, index in-folder) | 2026-07-20 |
| 10 | PRDs | `spec-prd` | ⬜ | [`docs/product-specs/prds/`](product-specs/prds/) | — |
| 11 | Implementation Plans | `plan-implementation` | ✅ | [`docs/plans/active/`](plans/active/) (3 plans: 0001, 0002, 0003, folder-per-plan with co-located `progress.txt`) | 2026-07-20 |

**Summary:** ✅ 3 / 🔄 0 / ⬜ 13 of 16 artefact steps

**Next step:** this repo does not run its full business-strategy spine (see note above) — Step 0 (Vision) is now live, but Steps 1–10 are deliberately skipped for a toolkit rather than a product. The live work surfaces are `docs/VISION.md`, the open-items ledger, and the use-case registry.

---

## What this repo actually runs (not on the linear spine)

| Artefact | Location | Status |
|---|---|---|
| Open-items ledger (github backend) | [`docs/project-control/open-items/`](project-control/open-items/) | ✅ live — 32 open issues on `VictorHueni/homemade-claude-kit`, ADR-0008/0009 label vocabulary |
| Use-case registry | [`docs/product-specs/use-cases/`](product-specs/use-cases/) | ✅ 11 UCs (UC-01..UC-11) |
| Implementation plans | [`docs/plans/active/`](plans/active/) | ✅ 3 active plans (migrated from the legacy `docs/exec-plans/` path 2026-07-20 — `var/reports/metamodel-migration/migration-2026-07-20.md`) |
| Architecture Decision Records | [`docs/architecture/decisions/`](architecture/decisions/) | ✅ 9 ADRs |
| Architecture Research notes | [`docs/architecture/research/`](architecture/research/) | ✅ 3 notes |

---

## Supporting artefacts (run as needed — not in the linear build order)

| Artefact | Skill | Path |
|---|---|---|
| Architecture Decision Records | `arch-adr` | `docs/architecture/decisions/adr-NNNN-{slug}.md` |
| Architecture Research | `arch-research` | `docs/architecture/research/{NNNN}-{slug}.md` |
| Competitive Landscape | `business-competitive-landscape` | `docs/business/01b-competitive-landscape/` |
| Discovery Research | `discovery-research` | `docs/discovery/interviews/` |
| Discovery Workshops | `discovery-workshop` | `docs/discovery/workshops/` |
| Ops Runbooks | `ops-runbook` | `docs/ops/runbooks/{slug}.md` |
| Bug RCAs | `ops-bug-rca` | `docs/ops/rcas/{date}-{slug}.md` |
| Pre-formal Ideas | `discovery-idea` | `docs/discovery/ideation/IDEA-NNNN-{slug}.md` |
| Slide Decks | `com-slide-deck` | `docs/communication/slides/{slug}/` |
| PRD / Plan reviews | `agent-peer-review` | — (interactive, no persistent artefact) |

---

## Audit

| Tool | Purpose | Cadence |
|---|---|---|
| the Audit mode Mode 1 | Full 18-check health audit | Monthly (active) / Quarterly (maintenance) |
| the Audit mode Mode 2 | Progress snapshot | Before sprint planning |
| the Audit mode Mode 4 | Freshness check | Before research waves or presentations |
| the Scaffold mode Mode 3 | Refresh this index.md | After completing any stack step |

---

## ID conventions at a glance

| ID format | Artefact | Owning file |
|---|---|---|
| `P-NN` | Persona | `01a-personas.md` |
| `C-N.M` | Capability | `03a-capability-map.md` |
| `VS-N.M` | Value-stream stage | `04a-value-streams.md` |
| `OBJ-NN` · `KR-NN.M` | Objective · Key Result | `04b-objectives.md` |
| `BC-NN` | Bounded Context | `02b-bounded-contexts.md` |
| `BC-NN.GT-NN` | Glossary Term | `02c-glossary.md` |
| `BC-NN.AGG-NN` · `BC-NN.ENT-NN` | Aggregate · Entity | `07b-models/{bc-slug}.md` |
| `C-N.M.FXX` | Functionality | `07a-fbs.md` |
| `E-NN` | Epic | `delivery-roadmap.md` |
| `QA-XXNN` | Quality Attribute | `09a-quality-attributes.md` |
| `PRD-NNNN` | PRD | `prds/prd-NNNN-{slug}.md` |
| `ADR-NNNN` | Architecture Decision | `architecture/decisions/adr-NNNN-{slug}.md` |
| `UC-NN` | Use Case | `use-cases/uc-NN-{slug}.md` |
