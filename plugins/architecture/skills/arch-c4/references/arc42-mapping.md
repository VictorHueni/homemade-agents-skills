# C4 ↔ arc42 mapping

Exact correspondence between C4 abstractions and arc42 sections, plus the gaps the kit fills with markdown templates.

---

## The three covered sections

### arc42 §3 — Context and Scope

**C4 contribution:** Level 1 (System Context) diagram is embedded as `systemContext.svg`.

**Additional markdown content the kit writes:**

- **§3.1 Business Context** — table with columns `Communication Partner` / `Inputs` / `Outputs`, one row per actor + external system. Rendered SVG is the visual; the table is the prose. arc42 explicitly recommends this dual representation.
- **§3.2 Technical Context** — table with columns `Communication Partner` / `Channel` / `Protocol` / `Format`. Derives from the `relationship technology` field on each C4 relationship (e.g. `"HTTPS/JSON"`, `"Kafka protocol"`).

**Pitfall to avoid:** describing internal containers in §3. §3 is **black-box** — only the system being documented + its partners. Containers belong to §5.

---

### arc42 §5 — Building Block View

**Three levels, mapped directly to C4 Containers and Components:**

| arc42 sub-section | C4 view | Markdown structure |
|---|---|---|
| §5.1 Whitebox Overall System | Container view (`containers.svg`) | Embedded SVG + Motivation paragraph + "Contained Building Blocks" table (one row per CON-NN) + "Important Interfaces" (optional, lists CTR-NN if `arch-service-contract` exists) |
| §5.2 Level 2 | One Component view per drilled container (`components-CON-NN.svg`) | One sub-subsection per drilled container. Each has: embedded SVG + "Purpose / Responsibility" + "Components" table (one row per CMP-NN with `Domain aggregates implemented` column) |
| §5.3 Level 3 | Deeper Component views if needed | Same structure as §5.2; used when a sub-component itself warrants drilling — rare |

**Mandatory `Domain aggregates implemented` column on §5.2 component tables:** every CMP-NN row must list which `BC-NN.AGG-NN` aggregates it implements (or be explicitly empty for technical components like HTTP wrappers). This is the **boundary back-reference** from BBV into `domain-model`. See `boundary-discipline.md`.

**Pitfalls to avoid:**

- **Re-stating the domain model in §5.** Aggregates, entities, value objects, and domain events live in `docs/domain/07b-models/{bc-slug}.md`. §5 names CMP-NN components (e.g. "Claim Command Handler") and says *which aggregates they implement* — it does **not** re-describe the aggregates' invariants or commands.
- **Drilling all the way to L3 for every container.** Skip routine CRUD / off-the-shelf containers. arc42 explicitly says: "Prefer relevance over completeness."
- **Single huge §5 file.** §5.2.x sub-subsections are appended on each `component` mode invocation, but if the file exceeds ~600 lines consider splitting one drilled container into its own file and linking.

---

### arc42 §7 — Deployment View

**C4 contribution:** one Deployment view per environment (`deployment-production.svg`, `deployment-staging.svg`, …).

**Additional markdown content:**

- **§7.1 Infrastructure Level 1** — high-level deployment overview (typically what fits on one diagram).
- **§7.x Per-environment subsection** — embedded SVG + Motivation paragraph + "Quality and/or Performance Features" (SLA targets, scaling parameters) + "Mapping of Building Blocks to Infrastructure" (one row per `CON-NN` instance: name / deployment node / instance count / region).

**Pitfalls to avoid:**

- **One deployment view tries to cover all environments.** Use one C4 deployment view per `deploymentEnvironment` in the DSL — staging and production differ in instance counts, node sizes, regions.
- **Treating Docker containers as C4 containers.** A C4 Container is a runtime *role* (the Claims API as a service). When deployed, one C4 Container may run as multiple Docker containers (3 pods of `claims-api`) — that multiplicity belongs in §7, not §5.

---

## The arc42 sections this skill does NOT cover

| arc42 § | Owning skill (current or planned) |
|---|---|
| §1 Introduction and Goals | `business-vision` + `business-objective` |
| §2 Architecture Constraints | `arch-constraints` (Milestone 2) |
| §4 Solution Strategy | `arch-solution-strategy` (Milestone 2) |
| §6 Runtime View | `arch-runtime-view` (Milestone 2) — uses **dynamic** C4 views, not static |
| §8 Cross-cutting Concepts | `arch-cross-cutting` (Milestone 2) |
| §9 Architecture Decisions | `arch-adr` (existing) |
| §10 Quality Requirements | `spec-quality-attributes` (existing) + `qa-test-strategy` (planned; mints `TS-NN`) |
| §11 Risks and Technical Debt | `arch-risks` (Milestone 2) + `dev-tech-debt` (user's separate workstream) |
| §12 Glossary | `domain-glossary` (existing) |

---

## When the user asks for "the arc42 doc"

The kit's split-file approach (`docs/architecture/arc42/03-context.md`, `05-building-blocks.md`, etc.) is intentional — each section evolves on its own cadence and Git diffs stay readable. If a stitched single-file view is needed (executive handoff, audit), a future `arch-arc42-stitch` skill can compile them. Until then, point users to `docs/architecture/arc42/` as the directory containing the architecture sections.
