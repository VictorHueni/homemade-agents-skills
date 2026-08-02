---
name: metamodel
license: MIT
description: "Canonical metamodel of the strategic-architecture documentation stack: the 19-artefact build order, the artefact-type registry (ID formats, canonical paths, review intervals, OKF type names), the artefact frontmatter schema, and open-items governance — plus the stack lifecycle as modes: Audit (health check), Scaffold (canonical folder tree + CLAUDE.md wiring), Migrate (bring existing docs onto the metamodel). Every doc-producing kit skill reads this skill's references; consult it directly for stack-level work. Triggers on: build the documentation stack, do the strategic docs, start the project documentation, documentation plan, build order, what artefact comes next, where does an artefact live, which ID format, artefact frontmatter, docs folder structure, audit my docs stack, metamodel audit, artefact stack health, scaffold the docs folder, docs folder setup, migrate my docs, docs migration report."
version: "1.0.0"
status: active
last_reviewed: 2026-07-19
review_interval: 180d
user-invocable: true
impact: "medium"
metadata:
  category: "metamodel"
  complexity: "high"
---

# The Metamodel — Strategic Architecture Stack

The **imperative core** of the kit's documentation system: what artefacts the `business-*` /
`domain-*` / `spec-*` / `plan-*` / `arch-*` skills produce, the **order** to build them, and
how the agent drives that work. This skill is the kit's single distribution point for the
metamodel — every doc-producing skill resolves structural facts through it (by skill name:
"the `metamodel` skill's `references/<file>`"; in flat installs it is a sibling directory).

> **Provenance — generated projection (future).** The structural and relational metamodel is
> canonically owned by the **clew** repo (clew ADR-0008): `docs/metamodel/` there is the
> authority; this skill's structural references are the interim hand-authored projection,
> to be emitted by `clew metamodel export` (Phase 4). Do not author new artefact types here
> first — author clew-side, then sync. Per-type *semantics* (what a good persona is,
> methodology, anti-patterns) stay with each minting skill's `## Canonical definition`.

## Reference files (load on demand)

| File | Contents |
|---|---|
| [`references/metamodel-reference.md`](references/metamodel-reference.md) | The heavy companion: supporting-skill catalogue, dependency DAG, ER model, per-step process + output verification, cross-doc ID conventions, canonical path tree, maintenance coupling |
| [`references/artefact-types-registry.yaml`](references/artefact-types-registry.yaml) | Structural registry — one entry per artefact type: `id_format` regex, layout, `default_path`, `review_interval`, `okf_type` display name, slug contract. Parse it (`python3 -c "import yaml; …"`), don't eyeball it |
| [`references/artefact-frontmatter.md`](references/artefact-frontmatter.md) | The OKF-superset frontmatter block every generated `docs/**` artefact opens with |
| [`references/open-items-governance.md`](references/open-items-governance.md) | Cross-cutting open-items contract: central ledger, item taxonomy, provenance fields |

When the user says *"build the documentation stack"*, *"do the strategic docs"*, *"start the
project documentation"*, or *"follow the architecture plan"* — this skill is the authoritative
reference for **what to build, in what order, and where to put it**.

## Modes (lifecycle operations)

Beyond the default **Reference** use (answering stack-level questions, guiding build-order
work), this skill owns three lifecycle modes. Pick by intent; each mode's full procedure is
its file under `references/modes/`:

| Mode | Intent signals | Procedure | What it does |
|---|---|---|---|
| **Audit** | "audit my docs stack", "artefact stack health", "metamodel audit", "governance drift" | [`references/modes/audit.md`](references/modes/audit.md) (+ [`audit-check-catalogue.md`](references/modes/audit-check-catalogue.md), [`audit-report-template.md`](references/modes/audit-report-template.md)) | Report-only health check of a project's docs stack — 19 checks derived from the registry: placement, IDs, links, dependencies, frontmatter, open-items governance |
| **Scaffold** | "scaffold the docs folder", "set up the documentation tree", "docs folder setup" | [`references/modes/scaffold.md`](references/modes/scaffold.md) (+ [`scaffold-folder-catalogue.md`](references/modes/scaffold-folder-catalogue.md), [`scaffold-index-template.md`](references/modes/scaffold-index-template.md)) | Creates the canonical `docs/` tree + root `index.md`; the Wire step writes `CLAUDE.md` (the reason this skill carries `impact: medium`) |
| **Migrate** | "migrate my docs", "bring existing docs onto the metamodel", "docs migration report" | [`references/modes/migrate.md`](references/modes/migrate.md) (+ [`migrate-detection-signals.md`](references/modes/migrate-detection-signals.md), [`migrate-path-migration-v2.md`](references/modes/migrate-path-migration-v2.md)) | Report-first migration of an existing docs tree onto the canonical layout — three-tier detection, ≥2-tier agreement before proposing moves |

All three modes parse `references/artefact-types-registry.yaml` at run time for structural
facts — none carries its own copy. Their long-term future is thin wrappers over the clew CLI
(`clew audit` / `clew init` / `clew migrate`), per clew ADR-0008.

---

## The build-order spine — 19 artefacts

| # | Artefact | Skill | Mints |
|---|---|---|---|
| 0 | **Product Vision** (why — the north star) | `business-vision` | — |
| 1 | **Personas** (who) | `business-persona` | `P-NN` |
| 2 | **Business Model Canvas** (commercial wrapper) | `business-model-canvas` | — |
| 3 | **Business Capability Map** (what abilities) | `business-capability-map` | `C-N.M` |
| 2b | **Bounded Context Map** (domain boundaries) | `domain-bounded-context` | `BC-NN` |
| 2c | **Domain Glossary** (ubiquitous language per BC) | `domain-glossary` | `BC-NN.GT-NN` |
| 4 | **Value Streams** (how value flows) | `business-value-stream` | `VS-N.M` |
| 4.5 | **Business Objectives** (strategic intent) | `business-objective` | `OBJ-NN` · `KR-NN.M` |
| 5 | **Business Processes** (operational how) | `business-process` | — |
| 6 | **Quantitative models** (numbers) | `business-quantitative-model` | — |
| 7 | **Functional Breakdown Structure** (functionality registry) | `spec-functional-breakdown-structure` | `C-N.M.FXX` |
| 7b | **Domain Model** (entities · aggregates · VOs · events per BC) | `domain-model` | `BC-NN.AGG/ENT/VO/EVT-NN` |
| 7c | **Interface Contract** (external API surface) | `arch-service-contract` | `BC-NN.CTR-NN` |
| 8 | **Delivery Roadmap** (Plan by Feature) | `plan-delivery-roadmap` | `E-NN` |
| 8.5 | **CLI Surface Contract** (only when the product ships a CLI) | `arch-cli-contract` | `CLI-NN.CMD-NN` |
| 9 | **Quality Attributes** (how well — NFRs) | `spec-quality-attributes` | `QA-XXNN` |
| 9.5 | **Use Cases** (actor↔system scenarios) | `spec-use-case` | `UC-NN` |
| 10 | **PRDs** (feature specs — Build by Feature) | `spec-prd` | `PRD-NNNN` · `PRD-NNNN.US-NN` |
| 11 | **Implementation plans** (atomic increments) | `plan-implementation` | `Plan-NNNN` |

> The number is build order, not a strict linear chain — several artefacts are parallelisable
> (see the DAG in [`references/metamodel-reference.md`](references/metamodel-reference.md)).
> Prerequisites, process, and output-verification for each step are in the companion's
> § Recommended build order. Supporting skills not on the spine (`arch-adr`,
> `arch-c4`/`arch-arc42`/`arch-uml`, `discovery-*`, `agent-*`, `ux-design-system`, `com-*`,
> `ops-*`, `util-*`) are catalogued in the companion's § Supporting skills.

**Hub rule:** the Capability Map (`C-N.M`) is the hub — most artefacts soft-link to it by ID.
An arrow `A → B` means *B soft-links to A by ID*; B can be scaffolded before A exists
(placeholder `_TODO_`), filled when A arrives. No cycles. ADRs are not in the linear chain
but must precede Step 9 (Quality Attributes) and Step 10 (PRDs) when their decisions affect
those artefacts.

---

## Variant selection

Pick the variant from user intent, then follow that path in the companion's § Variants:

- **Greenfield (default)** — full spine, Step 0 → 11 in order.
- **Brownfield** (existing system, adding capability) — start at Step 3 (Capability Map); skip Steps 1–2 unless the change touches a new stakeholder or the commercial model.
- **Single feature** (no full architecture) — skip Steps 1–8; go straight to Step 10 (`spec-prd`) with the `E-NN` scope defined inline, then Step 11 (`plan-implementation`).
- **Strategy / investor / exec** — start at Step 2 (BMC); skip Steps 7–11; optionally add Personas (Step 1), a quantitative model (Step 6), or the Capability Map (Step 3).

---

## Cross-doc linking rule

Any artefact that references another uses **ID + name + relative path**, so renames of the
description text don't break the link as long as the ID is stable:

> `[C3.2 prior-authorisation classification](../03a-capability-map.md#c32)`

Artefact-type id_formats are in
[`references/artefact-types-registry.yaml`](references/artefact-types-registry.yaml); diagram
/ arc42 / sub-element IDs (`SYS-NN`, `CON-NN`, `SCN-NN`, …) and the `BC-NN` namespace rule
are in the companion's § Cross-doc ID conventions.

---

## Open Items governance (cross-cutting)

Every artefact can carry unresolved work (research questions, missing decisions, follow-up
items, deferred refactors). The canonical contract for capturing, classifying, and auditing
it is [`references/open-items-governance.md`](references/open-items-governance.md) —
mandatory for any skill whose output may emit unresolved work. In brief: the central ledger
at `docs/project-control/open-items/` is the sole authoring surface (no per-artefact local
section); every row is filed directly and is one of `doc-gap` / `decision-gap` /
`execution-item` / `tech-debt` (inline `_TODO_` placeholders are **not** open items).

---

## How the agent should use this skill

When the user invokes documentation work on a project:

1. **Detect what already exists** — `find docs -type d` to map the current state.
2. **Identify which steps are done vs missing** by checking output paths (canonical tree in the companion's § Canonical output paths).
3. **Pick the variant** (greenfield / brownfield / single-feature / strategy-only) based on user intent.
4. **Execute the next step** using the corresponding skill in its appropriate mode.
5. **Verify the output** before moving on — each step's "Output verification" criteria in the companion.
6. **Maintain cross-doc IDs** — every soft-link uses the ID + name + path format above.

When asked *"build the documentation plan"* without further context, default to:
- Confirm the variant with the user (greenfield is the default).
- Start at Step 1; ask for personas input.
- Proceed sequentially through verification checks.
- One step per session unless the user wants batch execution.

---

## Maintenance

When new skills join the kit or a step / path / ID format changes: **structural facts**
(types, IDs, paths, relationships) are authored in the clew repo first (see Provenance above)
and synced into `references/artefact-types-registry.yaml` and the spine here; the two-stage
blast-radius procedure lives in the kit's `skill-creation-sync` rule. Failing to keep the
coupled files in sync causes the Audit and Migrate modes to silently miss artefacts — the
most dangerous kind of drift.

**Change history:** the authoritative record is `git log` / `git blame` on this skill and its
coupled files; the *why* of each change is its ADR (kit ADR-0007, clew ADR-0008); the prior
digest is parked at `docs/project-control/metamodel-changelog.md` in the kit repo.
