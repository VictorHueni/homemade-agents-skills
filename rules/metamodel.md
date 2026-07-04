---
paths:
  - "docs/**"
  - "rules/metamodel.md"
---

# Strategic Architecture Stack — Documentation Build Order

This rule is the **imperative core**: what artefacts the kit's `business-*` / `domain-*` / `spec-*` / `plan-*` / `arch-*` skills produce, the **order** to build them, and how Claude drives that work. The heavy reference — supporting-skill catalogue, dependency graph (DAG), ER model, per-step process + output-verification, ID conventions, canonical path tree, and the maintenance-coupling contract — lives in the on-demand companion [`metamodel-reference.md`](metamodel-reference.md) (no `paths:` frontmatter, so it costs no per-session context until linked). Per-type structural facts (minting skill, id-format regex, layout, default path, review interval) live in [`artefact-types-registry.md`](artefact-types-registry.md).

When the user says *"build the documentation stack"*, *"do the strategic docs"*, *"start the project documentation"*, or *"follow the architecture plan"* — this rule is the authoritative reference for **what to build, in what order, and where to put it**.

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
| 10 | **PRDs** (feature specs — Build by Feature) | `spec-prd` | `PRD-NNNN` |
| 11 | **Implementation plans** (atomic increments) | `plan-implementation` | `Plan-NNNN` |

> The number is build order, not a strict linear chain — several artefacts are parallelisable (see the DAG in the companion). Prerequisites, process, and output-verification for each step are in [`metamodel-reference.md` § Recommended build order](metamodel-reference.md#recommended-build-order--greenfield-software-default). Supporting skills not on the spine (`arch-adr`, `arch-c4`/`arch-arc42`/`arch-uml`, `discovery-*`, `agent-*`, `ux-design-system`, `com-*`, `ops-*`, `util-*`) are catalogued in [`metamodel-reference.md` § Supporting skills](metamodel-reference.md#supporting-skills).

**Hub rule:** the Capability Map (`C-N.M`) is the hub — most artefacts soft-link to it by ID. An arrow `A → B` means *B soft-links to A by ID*; B can be scaffolded before A exists (placeholder `_TODO_`), filled when A arrives. No cycles. ADRs are not in the linear chain but must precede Step 9 (Quality Attributes) and Step 10 (PRDs) when their decisions affect those artefacts.

---

## Variant selection

Pick the variant from user intent, then follow that path in [`metamodel-reference.md` § Variants](metamodel-reference.md#variants-for-non-greenfield-projects):

- **Greenfield (default)** — full spine, Step 0 → 11 in order.
- **Brownfield** (existing system, adding capability) — start at Step 3 (Capability Map); skip Steps 1–2 unless the change touches a new stakeholder or the commercial model.
- **Single feature** (no full architecture) — skip Steps 1–8; go straight to Step 10 (`spec-prd`) with the `E-NN` scope defined inline, then Step 11 (`plan-implementation`).
- **Strategy / investor / exec** — start at Step 2 (BMC); skip Steps 7–11; optionally add Personas (Step 1), a quantitative model (Step 6), or the Capability Map (Step 3).

---

## Cross-doc linking rule

Any artefact that references another uses **ID + name + relative path**, so renames of the description text don't break the link as long as the ID is stable:

> `[C3.2 prior-authorisation classification](../03a-capability-map.md#c32)`

Artefact-type id_formats are in [`artefact-types-registry.md`](artefact-types-registry.md); diagram / arc42 / sub-element IDs (`SYS-NN`, `CON-NN`, `SCN-NN`, …) and the `BC-NN` namespace rule are in [`metamodel-reference.md` § Cross-doc ID conventions](metamodel-reference.md#cross-doc-id-conventions).

---

## Open Items governance (cross-cutting)

Every artefact can carry unresolved work (research questions, missing decisions, follow-up items, deferred refactors). The canonical contract for capturing, classifying, and auditing it is [`rules/open-items-governance.md`](./open-items-governance.md) — mandatory for any skill whose output may emit unresolved work. In brief: the central ledger at `docs/project-control/open-items/` is the sole authoring surface (no per-artefact local section); every row is filed directly and is one of `doc-gap` / `decision-gap` / `execution-item` / `tech-debt` (inline `_TODO_` placeholders are **not** open items). When a new skill produces or governs unresolved work, conform to §8 of that rule.

---

## How Claude should use this rule

When the user invokes documentation work on a project:

1. **Detect what already exists** — `find docs -type d` to map the current state.
2. **Identify which steps are done vs missing** by checking output paths (see the canonical tree in [`metamodel-reference.md` § Canonical output paths](metamodel-reference.md#canonical-output-paths)).
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

When new skills join the kit or a step / path / ID format changes, this spine table plus the downstream copies must stay in sync. The full **maintenance-coupling contract** (which audit/migration/scaffold files to update, and the DAG + ER edits) lives in [`metamodel-reference.md` § Maintenance coupling](metamodel-reference.md#maintenance-coupling); the two-stage blast-radius procedure is in [`rules/skill-creation-sync.md`](./skill-creation-sync.md). Failing to update those files after a metamodel change causes the audit and migration skills to silently miss the new artefact — the most dangerous kind of drift.

**Change history:** the intended SoT is the **clew** repo (metamodel SoT per clew ADR-0008); the prior digest is parked at [`../docs/project-control/metamodel-changelog.md`](../docs/project-control/metamodel-changelog.md) pending migration. The authoritative record is `git log` / `git blame` on this file and its coupled files; the *why* of each change is its ADR.
