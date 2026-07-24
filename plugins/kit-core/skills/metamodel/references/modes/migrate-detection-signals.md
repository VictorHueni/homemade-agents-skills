# Detection Signals — the Migrate mode

Internal Claude reference. Never copied to projects. Update this file when the metamodel gains new artefacts.

The three-tier detection system. A finding requires ≥2 tiers to agree before being reported with a fix block. Single-tier matches are flagged Low confidence.

**Registry derivation (read first).** The "Canonical path" values in the tables below are
informational snapshots — the **authoritative** canonical path and ID format for every
artefact type is its entry in this skill's `references/artefact-types-registry.yaml`. At
run time: (1) resolve each detected type's destination by parsing the registry, never by
trusting the column; (2) additionally derive a baseline Tier-1 signal for EVERY registry
entry from its `default_path` filename pattern and `id_format` — so a newly registered
artefact type is detected even before a curated heuristic row exists here. The curated
rows below add fuzzy-name intelligence (synonyms, legacy names) the registry cannot carry.

---

## §Filename patterns (Tier 1 — High signal)

A file whose name matches one of these patterns is likely the artefact type listed.

| Filename pattern (glob) | Likely artefact type | Canonical skill | Canonical path |
|---|---|---|---|
| `INDEX.md` (any depth under `docs/`) | Legacy bundle/folder index | the Scaffold mode | Rename to `index.md` (OKF reserved file); strip artefact frontmatter; root keeps only `okf_version` — see `okf-index-rename` in `path-migration-v2.md` |
| `*_prd_*.md` or `*-prd-*.md` | PRD | `spec-prd` | `docs/product-specs/prds/prd-NNNN-{slug}.md` |
| `uc-[0-9][0-9]-*.md` or `*use-case*.md` | Use case | `spec-use-case` | `docs/product-specs/use-cases/uc-NN-{slug}.md` |
| `[0-9][0-9][0-9][0-9]-*.md` or `[0-9][0-9][0-9][0-9]_*.md` in a decisions-like folder | ADR | `arch-adr` | `docs/architecture/decisions/adr-NNNN-{topic}.md` |
| `*-adr-*.md` (redundant adr in name) | ADR naming issue | `arch-adr` | Rename: remove `-adr` from filename |
| `*runbook*.md` | Runbook | `ops-runbook` | `docs/ops/runbooks/{slug}.md` |
| `*-rca*.md` or `*-incident*.md` or `*-postmortem*.md` | Bug RCA | `ops-bug-rca` | `docs/ops/rcas/{date}-{slug}.md` |
| `*-process.md` or `*-workflow.md` | Business process | `business-process` | `docs/business/05a-processes/proc-NN-{slug}.md` |
| `*persona*.md` or `*personas*.md` | Personas | `business-persona` | `docs/business/01a-personas.md` |
| `*capability-map*.md` or `*capabilities*.md` | Capability map | `business-capability-map` | `docs/business/03a-capability-map.md` |
| `*value-stream*.md` or `*value-streams*.md` | Value streams | `business-value-stream` | `docs/business/04a-value-streams.md` |
| `*business-model-canvas*.md` or `*lean-canvas*.md` or `*bmc*.md` | BMC / Lean Canvas | `business-model-canvas` | `docs/business/02a-bmc.md or docs/business/02a-lean-canvas.md` |
| `*glossary*.md` | Domain glossary | `domain-glossary` | `docs/domain/02c-glossary.md` |
| `*information-model*.md` or `*domain-model*.md` or `*canonical*model*.md` | Domain model | `domain-model` | `docs/domain/07b-models/{bc-slug}.md` |
| `*bounded-context*.md` or `*context-map*.md` | Bounded context | `domain-bounded-context` | `docs/domain/02b-bounded-contexts.md` + `docs/domain/02b-context-map.md` |
| `FBS.md` or `*functional-breakdown*.md` | FBS | `spec-functional-breakdown-structure` | `docs/product-specs/07a-fbs.md` |
| `*quality-attributes*.md` or `*nfr*.md` or `*non-functional*.md` | Quality attributes | `spec-quality-attributes` | `docs/product-specs/09a-quality-attributes.md` |
| `*delivery-roadmap*.md` or `*epic-catalogue*.md` or `*epic-catalog*.md` | Delivery roadmap | `plan-delivery-roadmap` | `docs/plans/delivery-roadmap.md` |
| `*competitive-landscape*.md` or `*competitor*.md` | Competitive landscape | `business-competitive-landscape` | `docs/business/01b-competitive-landscape/` |
| `*quant-model*.md` or `*tam-*.md` or `*savings-model*.md` | Quantitative model | `business-quantitative-model` | `docs/business/06a-models/qm-NN-{topic}.md` |
| `VISION.md` or `*vision*.md` or `*north-star*.md` | Product vision | `business-vision` | `docs/VISION.md` (singleton at docs root) |
| `*objectives*.md` or `*okr*.md` or `*key-results*.md` | Business objectives | `business-objective` | `docs/business/04b-objectives.md` |
| `*interface-contract*.md` or `*service-contract*.md` or `*api-contract*.md` or `*api-surface*.md` (outside `docs/architecture/interfaces/`) | Service contract | `arch-service-contract` | `docs/architecture/interfaces/{bc-slug}.md` |
| `*cli-contract*.md` or `*cli-surface*.md` (outside `docs/architecture/interfaces/`) | CLI contract | `arch-cli-contract` | `docs/architecture/interfaces/cli-{slug}.md` |
| `getting-started.md` outside `docs/dev-guides/` | Getting started guide | `dev-getting-started` | `docs/dev-guides/getting-started.md` |
| `*-research.md` under a `dev-guides/` folder but not at `docs/dev-guides/research/` | Stack guide research scratch | `dev-stack-guide` | `docs/dev-guides/research/{tech-slug}-research.md` |
| `IDEA-[0-9][0-9][0-9][0-9]-*.md` or `*idea*.md` outside canonical | Discovery idea | `discovery-idea` | `docs/discovery/ideation/IDEA-NNNN-{slug}.md` |
| `interview-*.md` or `research-synthesis-*.md` or `research-plan-*.md` outside canonical | Discovery research | `discovery-research` | `docs/discovery/interviews/` |
| `workshop-*.md` or `workshop-synthesis-*.md` outside canonical | Discovery workshop | `discovery-workshop` | `docs/discovery/workshops/` |
| `*release-note*.md` or `*release-notes*.md` (outside `docs/communication/release-notes/`; NOT root `CHANGELOG.md`) | Release notes | `com-release-note` | `docs/communication/release-notes/{slug}.md` (or an existing `docs/release-notes/`) |
| `workspace.dsl` (Structurizr DSL) anywhere | C4 workspace | `arch-structurizr` | `docs/architecture/c4/workspace.dsl` |
| `*.dsl` outside `docs/architecture/c4/` that contains `workspace "..."` | Misplaced Structurizr DSL | `arch-structurizr` | `docs/architecture/c4/workspace.dsl` |
| `render.sh` containing `structurizr/structurizr` reference outside `docs/architecture/c4/` | Misplaced render pipeline | `arch-structurizr` | `docs/architecture/c4/render.sh` |
| `03-context.md`, `05-building-blocks.md`, `06-runtime-view.md`, `07-deployment.md` outside `docs/architecture/arc42/` | arc42 diagram sections | `arch-c4` | `docs/architecture/arc42/{03,05,06,07}-*.md` |
| `02-constraints.md`, `04-solution-strategy.md`, `08-cross-cutting-concepts.md`, `11-risks.md` outside `docs/architecture/arc42/` | arc42 narrative sections | `arch-arc42` | `docs/architecture/arc42/{02,04,08,11}-*.md` |
| `*context*.md` or `*system-context*.md` containing `arc42 §3` reference, outside canonical | arc42 §3 misplaced | `arch-c4` | `docs/architecture/arc42/03-context.md` |
| `*building-blocks*.md` or `*building_block*.md` containing `arc42 §5` reference, outside canonical | arc42 §5 misplaced | `arch-c4` | `docs/architecture/arc42/05-building-blocks.md` |
| `*runtime-view*.md` or `*runtime*.md` containing `arc42 §6` or `SCN-` reference, outside canonical | arc42 §6 misplaced | `arch-c4` | `docs/architecture/arc42/06-runtime-view.md` |
| `*deployment-view*.md` or `*deployment*.md` containing `arc42 §7` reference, outside canonical | arc42 §7 misplaced | `arch-c4` | `docs/architecture/arc42/07-deployment.md` |
| `*cross-cutting*.md` or `*cross_cutting*.md` containing `CC-` ID or `arc42 §8` reference, outside canonical | arc42 §8 misplaced | `arch-arc42` | `docs/architecture/arc42/08-cross-cutting-concepts.md` |
| `*risks*.md` or `*risk-register*.md` containing `RSK-` ID or `arc42 §11` reference, outside canonical | arc42 §11 misplaced | `arch-arc42` | `docs/architecture/arc42/11-risks.md` |

**ADR naming redundancy rule:** if a file is already in `docs/architecture/decisions/` and its name contains `-adr-` (e.g. `0003-adr-clean-architecture.md`), flag as Tier 1 naming issue. Proposed fix: `git mv 0003-adr-clean-architecture.md 0003-clean-architecture.md`. The `-adr-` prefix is redundant since the folder already signals the type.

**PRD location rule:** canonical location is `docs/product-specs/prds/prd-NNNN-{slug}.md`. PRDs found flat under `docs/product-specs/` (not in `prds/` subfolder) should be moved.

---

## §Folder name patterns (Tier 2 — Medium signal)

A folder whose name matches one of these patterns, AND is not already at the canonical path, is likely misplaced.

| Folder name pattern | Likely artefact type | Canonical path | Detection command |
|---|---|---|---|
| `runbooks/` or `runbook/` | `ops-runbook` | `docs/ops/runbooks/` | `find docs -type d -iname "runbook*" \| grep -v "docs/ops/runbooks"` |
| `bugs/` or `bug-reports/` or `rcas/` or `incidents/` | `ops-bug-rca` | `docs/ops/rcas/` | `find docs -type d -iname "bug*" -o -type d -iname "rca*" -o -type d -iname "incident*" \| grep -v "docs/ops"` |
| `workshop*/` or `workshops/` | `discovery-workshop` | `docs/discovery/workshops/` | `find docs -type d -iname "workshop*" \| grep -v "docs/discovery/workshops"` |
| `interview*/` or `interviews/` | `discovery-research` | `docs/discovery/interviews/` | `find docs -type d -iname "interview*" \| grep -v "docs/discovery/interviews"` |
| `objectives/` or `okr/` or `okrs/` | `business-objective` | `docs/business/04b-objectives.md` (flat — no subfolder in v2) | `find docs/business -type d -iname "objective*" -o -type d -iname "okr*"` |
| `personas/` or `persona/` | `business-persona` | `docs/business/01a-personas.md` (flat — no subfolder in v2) | `find docs/business -type d -iname "persona*"` |
| `capabilities/` or `capability-map/` | `business-capability-map` | `docs/business/03a-capability-map.md` (flat — no subfolder in v2) | `find docs/business -type d -iname "capabilit*"` |
| `value-streams/` or `journeys/` or `customer-journeys/` | `business-value-stream` | `docs/business/04a-value-streams.md` (flat — no subfolder in v2) | `find docs/business -type d -iname "value-stream*" -o -type d -iname "journey*"` |
| `processes/` or `workflows/` | `business-process` | `docs/business/05a-processes/` | `find docs -type d -iname "process*" -o -type d -iname "workflow*" \| grep -v "docs/business/05a-processes"` |
| `decisions/` or `adrs/` or `adr/` | `arch-adr` | `docs/architecture/decisions/` | `find docs -type d -iname "decision*" -o -type d -iname "adr*" \| grep -v "docs/architecture/decisions"` |
| `interfaces/` or `api-surface/` or `api-contracts/` or `service-contracts/` (not at `docs/architecture/interfaces/`) | Interface / CLI contracts | `docs/architecture/interfaces/` | `find docs -type d \( -iname "interface*" -o -iname "api-surface*" -o -iname "api-contract*" -o -iname "service-contract*" \) \| grep -v "docs/architecture/interfaces"` |
| `glossary/` or `ubiquitous-language/` or `vocabulary/` | `domain-glossary` | `docs/domain/02c-glossary.md` (flat — no subfolder in v2) | `find docs/domain -type d -iname "glossar*" -o -type d -iname "ubiquitous*"` |
| `models/` containing `*model*.md` files | `business-quantitative-model` or `domain-model` | `docs/business/06a-models/` or `docs/domain/` | Confirm with Tier 1 + Tier 3 |
| `ideas/` or `proposals/` or `ideation/` | `discovery-idea` | `docs/discovery/ideation/` | `find docs -type d \( -iname "idea*" -o -iname "proposal*" -o -iname "ideation*" \) \| grep -v "docs/discovery/ideation"` |
| `business/discovery/` (legacy — discovery promoted to top-level) | `discovery-*` family | `docs/discovery/` | `find docs/business -type d -iname "discovery"` |
| `dev-guides/` or `developer-guides/` or `stack-guides/` not at `docs/dev-guides/` | Developer guides | `dev-stack-guide` / `dev-getting-started` | `find docs -type d \( -iname "dev-guide*" -o -iname "developer-guide*" -o -iname "stack-guide*" \) \| grep -v "docs/dev-guides"` |
| `c4/` or `structurizr/` not at `docs/architecture/c4/` | C4 workspace foundation | `arch-structurizr` | `find docs -type d \( -iname "c4" -o -iname "structurizr" \) \| grep -v "docs/architecture/c4"` |
| `arc42/` not at `docs/architecture/arc42/` | arc42 markdown sections | `arch-c4` | `find docs -type d -iname "arc42" \| grep -v "docs/architecture/arc42"` |
| `release-notes/` or `release-note/` not at `docs/communication/release-notes/` | `com-release-note` | `docs/communication/release-notes/` (an existing top-level `docs/release-notes/` is honoured, not flagged) | `find docs -type d -iname "release-note*" \| grep -vE "docs/communication/release-notes\|docs/release-notes"` |

---

## §Content signals (Tier 3 — Confirmation, first 50 lines only)

Read only `head -50 {file}`. Check for these high-signal headings. A content signal alone = Low confidence; combined with Tier 1 or 2 = High confidence.

| Heading pattern (grep -iE) | Artefact type confirmed |
|---|---|
| `## Porter.s Five Forces` or `## Five Forces` | `business-competitive-landscape` |
| `## Persona Backlog` or `## Cooper Persona` | `business-persona` |
| `## §8 KPI` or `^## KPIs` with `## §3 Actors` nearby | `business-process` |
| `## L0 axis` or `## Capability Index` or `## Global overview` | `business-capability-map` |
| `## Value Stream Catalogue` or `## Catalogue` with `VS-[0-9]` nearby | `business-value-stream` |
| `## Aggregate catalogue` or `## Domain event catalogue` | `domain-model` |
| `## Subdomain catalogue` or `## Bounded Context` with `BC-[0-9]` | `domain-bounded-context` |
| `## Implicit assumptions` or `§5\.2` or `## Scenario Matrix` | `business-quantitative-model` |
| `§0 Architecture Traceability` or `## Acceptance criteria` with `PRD-[0-9]` | `spec-prd` |
| `\*\*Status:\*\*.*Accepted` or `\*\*Status:\*\*.*Deprecated` with `## Context` | `arch-adr` |
| `## Customer Segments` or `## Value Propositions` with `## Revenue Streams` | `business-model-canvas` |
| `## Ubiquitous Language` or `GT-[0-9][0-9]` pattern | `domain-glossary` |
| `✅\|🔄\|⬜` in functionality table rows | `spec-functional-breakdown-structure` |
| `QA-[A-Z]{2}[0-9]{2}` pattern | `spec-quality-attributes` |
| `E-[0-9][0-9].*epic` | `plan-delivery-roadmap` |
| `## The Elevator Pitch` or `## North Star Metric` heading | `business-vision` |
| `OBJ-[0-9][0-9]` pattern or `KR-[0-9][0-9]\.[0-9]` pattern | `business-objective` |
| `## Objective.*Epic traceability` | `business-objective` |
| `## Main Success Scenario` with `## Extensions` nearby, or `Primary Actor` + `Level` header fields, or `UC-NN` pattern | `spec-use-case` (use case) |
| `## §0 Traceability` with `BC-NN.CTR-NN` or `CTR-NN` pattern | `arch-service-contract` (service / interface contract) |
| `## §2 Command catalogue` or `## §7 Error contract` with `CMD-NN` pattern | `arch-cli-contract` (CLI contract) |
| `## Stack identity` with `verified-for:` in frontmatter | `dev-stack-guide` (stack developer guide) |
| `## Clone & bootstrap` or `## Running locally` with `## Coding agent setup` | `dev-getting-started` (project getting-started guide) |
| `workspace "..."` followed by `model {` and `views {` blocks in a `.dsl` file | `arch-structurizr` (Structurizr DSL workspace) |
| `# 3. Context and Scope` with `arc42 §3` reference or `## 3.1 Business Context` / `## 3.2 Technical Context` | `arch-c4` (arc42 §3 markdown) |
| `# 5. Building Block View` with `arc42 §5` reference or `## 5.1 Whitebox Overall System` + `Domain aggregates implemented` column | `arch-c4` (arc42 §5 markdown) |
| `# 7. Deployment View` with `arc42 §7` reference or `Mapping of building blocks to infrastructure` heading | `arch-c4` (arc42 §7 markdown) |
| `SYS-[0-9]{2}`, `CON-[0-9]{2}`, `CMP-[0-9]{2}`, or `DN-[0-9]{2}` patterns in markdown | `arch-c4` (C4 IDs minted) |
| `## v[0-9]+\.[0-9]+\.[0-9]+` heading with `## What.s new` nearby, or `type: Release Notes` in frontmatter | `com-release-note` (release notes) |

---

## §Outside metamodel scope patterns

Folders/files that are valid project docs but have NO equivalent metamodel artefact. Flag as Info — no action needed, no fix block.

| Pattern | Why outside scope |
|---|---|
| `docs/developer/` or `docs/dev-guide/` or `docs/contributing/` | Developer guides — not a metamodel artefact |
| `docs/design/` or `docs/ui/` | Legacy design-system / UX location — the `ux-` category now owns `docs/ux/` (in metamodel); treat as a `docs/design/` → `docs/ux/` rename |
| `docs/ci-cd/` or `docs/deployment/` or `docs/infra/` | CI/CD and infra docs — not in metamodel |
| `docs/data/` (excluding glossary/info-model files) | Data engineering docs — not in metamodel (glossary/info-model are DDD candidates) |
| `docs/codebase/` or `docs/valuation/` | Business/financial analysis — not in metamodel |
| `docs/pipeline*/` or `docs/pipeline steps/` | Pipeline technical guides — not in metamodel |
| `docs/developer/` | Developer onboarding — not in metamodel |
| Files with `.pptx`, `.html`, `.pdf` | Binary/presentation formats — not text artefacts in the metamodel |

---

## §DDD migration candidate signals

Files that predate the domain- skill layer but contain content that belongs in `docs/domain/`. These get §4 treatment (Warning, no git mv fix block — the domain skill must process them first).

| Signal | Likely destination | Skill to run |
|---|---|---|
| File named `*glossary*.md` not at `docs/domain/02c-glossary.md` | `docs/domain/02c-glossary.md` | `domain-glossary` Mode 2 (seed from existing) |
| File named `*information-model*.md` or `*canonical*model*.md` or `*domain-model*.md` outside `docs/domain/` | `docs/domain/07b-models/{bc-slug}.md` | `domain-model` Mode 2 (fill from existing) |
| File named `*entity*.md` or `*entities*.md` or `*aggregate*.md` | `docs/domain/07b-models/{bc-slug}.md` | `domain-model` Mode 2 |
| File named `*bounded-context*.md` not at `docs/domain/02b-bounded-contexts.md` | `docs/domain/02b-bounded-contexts.md` | `domain-bounded-context` Mode 3 (fill) |
| Content signal: `## Ubiquitous Language` or `GT-[0-9]` IDs anywhere | `docs/domain/02c-glossary.md` | `domain-glossary` Mode 3 (enrich) |

**DDD candidate note:** do NOT emit `git mv` for DDD candidates. The domain skill (domain-glossary, domain-model) should be invoked first to scaffold the target doc at the correct path — it reads the existing content and imports it. Moving first would leave the domain skill with nothing to import.
