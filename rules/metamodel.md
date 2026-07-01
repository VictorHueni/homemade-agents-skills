---
paths:
  - "docs/**"
  - "rules/metamodel.md"
---

# Strategic Architecture Stack — Documentation Build Order

This rule documents the **complete strategic-architecture artefact stack**
produced by the kit's `business-*` + `spec-*` skills, the **dependency graph** between
them, and the **canonical build order** Claude should follow when starting
documentation work on any new project.

When the user says *"build the documentation stack"*, *"do the strategic
docs"*, *"start the project documentation"*, or *"follow the architecture
plan"* — this rule is the authoritative reference for **what to build, in
what order, and where to put it**.

---

## The 19 artefacts and their skills

| # | Artefact |
|---|---|
| 0 | **Product Vision** (why — the north star) |
| 1 | **Personas** (who) |
| 2 | **Business Capability Map** (what abilities) |
| 2b | **Bounded Context Map** (domain boundaries + context map) |
| 2c | **Domain Glossary** (ubiquitous language per bounded context) |
| 3 | **Value Streams** (how value flows) |
| 4.5 | **Business Objectives** (why — strategic intent) |
| 4 | **Business Processes** (operational how) |
| 5 | **Business Model Canvas** (commercial wrapper) |
| 6 | **Quantitative models** (numbers) |
| 7 | **Functional Breakdown Structure** (functionality registry) |
| 7b | **Domain Model** (entities · aggregates · value objects · domain events per BC) |
| 7c | **Interface Contract** (external API surface — sync REST/gRPC/SDK + async events) |
| 8 | **Delivery Roadmap** (Plan by Feature — delivery grouping) |
| 8.5 | **CLI Surface Contract** (CLI command tree · flag contract · exit codes · output format — only when the product exposes a user-facing CLI) |
| 9 | **Quality Attributes** (how well the system performs) |
| 9.5 | **Use Cases** (actor↔system behavioural scenarios — all paths + guarantees) |
| 10 | **PRDs** (feature specs — Build by Feature) |
| 11 | **Implementation plans** (atomic increments) |

> **Per-type structural facts** — minting skill, id-format regex, file layout, default path, review interval, and property-schema reference — live in the companion rule [`artefact-types-registry.md`](artefact-types-registry.md). This table is the build-order index (step + artefact).

**Supporting skills** (not in the main build order, used as needed):
- `arch-adr` — Architecture Decision Records → `docs/architecture/decisions/adr-{NNNN}-{slug}.md`. **Sequencing rule:** ADRs governing security, flexibility, or maintainability must be written before Step 9 (Quality Attributes) so the QA doc can reference them. All ADRs must precede Step 10 (PRDs) that depend on their decisions. Invoke ADRs as soon as an architectural choice must be made — they are not a post-hoc documentation exercise.
- `discovery-idea` — captures, refines, and graduates pre-formal ideas → `docs/discovery/ideation/IDEA-{NNNN}-{slug}.md` with a single `index.md` at folder root; mints `IDEA-NNNN` (4-digit zero-padded); each idea carries a `graduates_to:` pointer naming the downstream skill that owns the matured artefact (`spec-prd`, `arch-adr`, `business-persona`, `business-objective`, `business-model-canvas`, `arch-research`, `business-process`, or `spec-functional-breakdown-structure`); pre-Step-0 cross-cutting node — the skill itself never writes downstream artefacts, only invokes the right one at graduation
- **Agent-Centric Development Cycle** (`agent-` package — Guide → Verify → Solve; orchestrates *how the agent builds*, not *what the product is*; mints no IDs, writes no `docs/` artefacts):
  - `agent-config` — **Guide**: scaffold / review / improve `CLAUDE.md` + `AGENTS.md` (behavioural posture, token-budget discipline, docs-index wiring) so the agent works with the right context, standards, and guardrails; three modes (scaffold, review, improve)
  - `agent-grill-me` — **Verify (inner loop)**: live Socratic stress-test of a PRD / implementation plan, one question at a time; enforces domain vocabulary against `docs/domain/glossary.md`; crystallises decisions into ADRs via `arch-adr`; surfaces *thinking* gaps under questioning
  - `agent-peer-review` — **Verify (outer loop)**: static critical review of PRDs / plans → ranked findings by severity (critical / major / normal / low) with concrete remediation; surfaces *mechanical* gaps automatically; complementary to `agent-grill-me`
  - `agent-ralph-loop` — **Solve**: autonomous implementation-plan execution (implement → test → commit → repeat, one increment per iteration, fresh context each pass) via `scripts/ralph.sh`
- `arch-research` — Architecture Research notes that inform ADR decisions → `docs/architecture/research/{NNNN}-{slug}.md`; mints `Research-NNNN` in-doc ID (4-digit zero-padded, same convention as `ADR-NNNN`); lifecycle: Draft → Active → Frozen (once feeding ADRs land) → Superseded
- `arch-structurizr` — one-time foundation skill that scaffolds the Structurizr DSL workspace (`docs/architecture/c4/workspace.dsl`) and the Docker-based render pipeline (`render.sh` + pinned `structurizr/structurizr:<pin>-playwright` image); three modes: `init` (scaffold), `verify` (check Docker + DSL), `upgrade` (bump pinned version + re-render). Mints no IDs (infrastructure-only). Companion to `arch-c4`.
- `arch-c4` — author C4 diagrams via the Structurizr DSL and emit the **DSL-derived tables** for arc42 §3 (Context), §5 (Building Blocks), §7 (Deployment) as **fenced generated blocks** (`<!-- arch-c4:start/end -->` markers) under `docs/architecture/arc42/`. `arch-c4` authors **no arc42 narrative** — all prose is `arch-arc42`'s, written outside the markers. Five modes: `context` (Level 1, mints `SYS-NN`), `container` (Level 2, mints `CON-NN`), `component` (Level 3, one drill per CON-NN; mints `CMP-NN`; carries `properties.implements "BC-NN.AGG-NN"` back-reference into `domain-model` or `"none"` for tech-only components), `deployment` (per-environment, mints `DN-NN`), `runtime` (Structurizr dynamic view — **figure producer only**: renders the SVG keyed by a `SCN-NN` that `arch-arc42` mints; writes no §6 markdown). **Boundary rules:** BBV is the STATIC technical decomposition — do NOT re-state domain-model aggregate invariants. Runtime view shows HOW containers collaborate — do NOT show intra-aggregate state machines. Requires `arch-structurizr init` to have run first.
- `arch-plantuml` — one-time foundation skill that scaffolds the PlantUML diagrams workspace (`docs/architecture/diagrams/`) and the Docker-based render pipeline (`render.sh` + shared `_theme.puml` + pinned `plantuml/plantuml:<pin>` image); three modes: `init` (scaffold), `verify` (check Docker + diagrams parse), `upgrade` (bump pinned version + re-render). Mints no IDs (infrastructure-only). Companion to `arch-uml`. The PlantUML twin of `arch-structurizr`; covers the UML diagram types Mermaid renders poorly and Structurizr does not draw — **not** C4 (that is `arch-c4`).
- `arch-uml` — author UML diagrams with PlantUML; writes one `docs/architecture/diagrams/<type>-NN-<slug>.puml` per diagram, renders to committed SVG via `render.sh`, and embeds into the consuming markdown; six modes, one per type: `sequence`, `class`, `state` (aggregate lifecycle), `activity`, `er`, `use-case`. Mints **no IDs** — diagrams visualise IDs owned by upstream artefacts (`UC-NN` from `spec-use-case`, `BC-NN.AGG-NN` from `domain-model`, `PROC-NN` from `business-process`, `P-NN` from `business-persona`), carried into the diagram `title` + labels. **arc42 §6/§8 figures are pull-side:** a `sequence` may illustrate arc42 §6 and a `class`/`state`/`er` may illustrate §8, but `arch-arc42` owns the section and the embed (via its `<!-- arch-figure … -->` block) — `arch-uml` only renders the SVG and reports the path. §6 figure-source boundary: C4 dynamic for cross-container flows, UML sequence for intra-component/algorithmic detail. **Boundary rules:** not for C4 views (→ `arch-c4`); not for GitHub-inline diagrams (→ Mermaid); a class/state/ER diagram is a *view* of `domain-model`, never a second source of truth. Requires `arch-plantuml init` to have run first. The PlantUML twin of `arch-c4`.
- `arch-arc42` — **five-mode** skill that owns ALL arc42 narrative (`arch-c4` only emits the diagram + DSL-derived table blocks inside `arch-c4` markers in §3/§5/§7): `constraints` (§2, mints `CST-NN`; three-category table — technical / organizational / legal-regulatory; cites source + ADR per constraint), `solution-strategy` (§4, no new IDs; navigation aid linking ADR decisions and QA-XXNN quality goals to architectural tactics; never re-states ADR rationale), `runtime` (§6, **mints `SCN-NN`**; authors the scenario prose + step table and **pulls a figure** via a `<!-- arch-figure … -->` declared-dependency block — a C4 dynamic view from `arch-c4` for cross-container flows, or an `arch-uml sequence` for intra-component/algorithmic detail), `cross-cutting` (§8, mints `CC-NN`; eleven standard concept areas — authentication, authorisation, session, logging, tracing, error-handling, persistence, caching, i18n, transport security, feature flags; each entry names governing ADR + affected CON-NN containers; may pull an `arch-uml` state/class/ER figure), `risks` (§11, mints `RSK-NN`; four risk types — `architectural`, `technical-debt`, `dependency`, `security`; explicit boundary with ops runbooks; leaves hook for future `dev-tech-debt` skill). Output: `docs/architecture/arc42/{02,04,06,08,11}-*.md`. Reads upstream artefacts before proposing content.
- `business-competitive-landscape` — Porter Five Forces + Strategic Group Map + Value Curve + per-competitor profiles → `docs/business/01b-competitive-landscape/`; mints `CO-NN` per Tier-1 competitor profile; soft-links to personas (P-NN), BMC, capability map (C-N.M), quantitative models; run **after Step 1 (Personas)** so competitor ICPs can be mapped to persona IDs, and **before Step 2 (BMC) is filled** so competitive positioning informs the Value Propositions block rather than following it; alternatively run alongside Step 6 (quantitative models) when the primary need is competitor pricing or market-sizing data
- `discovery-research` — hypothesis-anchored interview scripts + research synthesis + research plans → `docs/discovery/interviews/`; run alongside any step where upstream artefacts carry `Assumed` claims; especially valuable after Step 1 (Personas), Step 2 (BMC), and Step 6 (Quantitative Models); synthesis feeds confidence ratings (`Assumed → Tested → Validated`) back into those artefacts; companion to `discovery-workshop` (individual reality-check vs. group reality-check) and `discovery-idea` (validates Must-be-true assumptions raised during idea refinement)
- `discovery-workshop` — workshop facilitation guides + series plans + synthesis → `docs/discovery/workshops/`; run when stakeholder alignment or group reality-checking is needed; especially valuable before Step 2 (BMC) and Step 4 (Value Streams) to build shared understanding; companion to `discovery-research` (group reality-check vs. individual reality-check); the three `discovery-*` skills share the `docs/discovery/` parent folder
- `ops-runbook`, `ops-bug-rca` — operational artefacts (post-ship)
- `util-metamodel-scaffold` — one-time initialisation: creates the canonical `docs/` folder tree (variant-aware: greenfield / brownfield / strategy-only / single-feature), generates `docs/index.md` (live navigation hub with ✅/🔄/⬜ status per step), and wires a stack pointer into `CLAUDE.md`; run once per new project before any artefact-producing skill; re-run Mode 3 to refresh `docs/index.md` after completing stack steps
- `util-docs-audit` — general doc staleness scan (file-level freshness, dead prose)
- `util-metamodel-audit` — deep metamodel compliance audit: 16 checks covering stack progress, folder placement, internal + external links, ID integrity + cross-references, dependency enforcement, _TODO_ density, mandatory sections, confidence distribution, expiry + staleness, orphaned files, research sync, ADR chains, FBS + epic delivery progress → report at `var/reports/metamodel-audit/`; report-only with proposed fix per finding; run monthly (active dev) or quarterly (maintenance)
- `util-metamodel-migration` — one-time migration doctor for repos built before the metamodel: scans any docs/ folder, detects misplaced files using tiered confidence scoring (filename → folder name → content signals), emits atomic fix blocks (git mv + sed link repairs) per file → report at `var/reports/metamodel-migration/`; report-only; run once before the first `util-metamodel-audit`
- `dev-stack-guide` — research a technology stack's latest official docs + MCP server, then write a developer guide covering core patterns, anti-patterns, best practices, and coding-agent integration; three modes: research (→ `docs/dev-guides/research/{tech-slug}-research.md`), draft (→ `docs/dev-guides/{tech-slug}.md`), refresh; no metamodel IDs — path-referenced only
- `dev-getting-started` — scaffold and populate a project-specific getting-started guide; reads project files (package.json, docker-compose, .env.example, Makefile, CLAUDE.md) to emit exact commands; three modes: scaffold, fill, refresh → `docs/dev-guides/getting-started.md`; singleton per project
- `dev-git-commit`, `dev-pr`, `dev-git-worktree` — developer workflow (commit, pull-request, worktree); the ralph loop moved to the `agent-` package (`agent-ralph-loop`)
- `ux-design-system` — project visual source of truth; authors `docs/ux/design-system.md` (brand rationale + token tables) and generates `docs/ux/tokens.css`, a canonical `:root` variable contract the `com-` presentation layer themes from (`var(--token)` only, never hard-coded colour/font/radius); modes: scaffold, generate/refresh (`design-system.md → tokens.css`); **cross-cutting foundation** — mints no IDs, carries no FK links to other artefacts, and sits outside the dependency graph (no ER entity, no ID-conventions row); scaffold it any time before producing communication artefacts. Adapts Anthropic's `brand-guidelines` skill pattern, kept domain-agnostic. Lives in the `ux-` category → `docs/ux/` (the design + experience layer); the skill name `ux-design-system` follows the standard `<category>-<artefact>` convention (the artefact is `design-system`, which does not start with the `ux` category word, so no inner-redundancy strip applies).
- `com-slide-deck` — HTML slide presentations → `docs/communication/slides/{slug}/` (one folder per deck, named after the presentation in kebab-case); `build.py` layers tokens like `com-artefact-viz` — shipped `templates/tokens.fallback.css` (zero-config defaults) → `docs/ux/tokens.css` (project override, config `paths.design_tokens` or auto-detected) → deck `styles.css` → baseline — so base palette + typography flow from the project source of truth and a standalone deck still renders — the deck adopts the contract token names, including generic semantic state (`--success/--warning/--danger/--info`); kit-domain tokens are consumer-derived (OI-0019)
- `com-artefact-viz` — renders canonical artefacts (capability map, FBS, delivery roadmap, BMC/Lean Canvas) into single-file interactive HTML views → `docs/communication/visualisations/{kind}.html`; parse→model→render pipeline (Python stdlib only) with a token-driven design system layered like `com-slide-deck` — shipped `templates/tokens.fallback.css` → shared `docs/ux/tokens.css` (auto-detected, or `--design-system`) → `templates/tokens.domain.css` (domain tokens derived from the generics); mints no IDs and is not a build-order step — a derived, regenerable read-out of artefacts that remain the source of truth; companion to `com-slide-deck`

---

## Dependency graph (DAG)

```
   ┌──────────────────────────────────────────────────────────────┐
   │  DISCOVERY LAYER (pre-formal evidence · cross-cutting)       │
   │                                                              │
   │   discovery-idea       discovery-research    discovery-      │
   │   (capture · refine    (1:1 interviews +     workshop        │
   │    · graduate)          synthesis)           (group facil.)  │
   │   Output: IDEA-NNNN    Output: interview/    Output: workshop│
   │   graduates_to →       synthesis docs        + synthesis docs│
   │                                                              │
   │   Routing (see "Discovery routing" below the DAG):           │
   │   • discovery-idea graduates_to → any downstream node        │
   │   • discovery-research validates Assumed claims in any node  │
   │   • discovery-workshop aligns stakeholders before any node   │
   └────────────────────────────┬─────────────────────────────────┘
                                │ feeds + validates
                                ▼
   ┌──────────────────────────────────────────────────┐
   │  business-vision (Step 0)                        │
   │  (why — the north star)                          │
   │  Output: docs/VISION.md (singleton)              │
   │  Wires to: CLAUDE.md (agent context injection)   │
   └──────────────────────┬───────────────────────────┘
                          │ soft-links to all downstream artefacts
                          │
                       ┌──┴─────────────────────┐
                       │  business-persona      │
                       │  (who we serve)        │
                       │  Output: P-NN          │
                       └──────────┬─────────────┘
                                  │
              ┌───────────────────┼──────────────────────┐
              │                   │                      │
              ▼                   ▼                      ▼
   ┌──────────────────────┐ ┌────────────────────┐ ┌──────────────────────┐
   │ business-            │ │ business-          │ │ business-            │
   │   capability-map     │◄┤   value-stream     │ │   model-canvas       │
   │ (what abilities)     │ │ (how value flows)  │ │ (commercial wrapper) │
   │ Output: C-N.M        │ │ Output: VS-N.M     │ │ Soft-links P-NN,     │
   └──────────┬───────────┘ │ Stages consume     │ │   C-N.M, VS-N,       │
              │             │   C-N.M            │ │   quant models       │
              │             └──────────┬─────────┘ └──────────────────────┘
              │                        │
              │                        ▼
              │             ┌────────────────────┐
              │             │ business-process   │
              │             │ (operational how)  │
              │             │ Operationalises    │
              │             │   a VS stage       │
              │             └────────────────────┘
              │
              │             ┌────────────────────┐
              │             │ business-          │
              │             │  quantitative-model│
              │             │ (numbers / TAM)    │
              │             └────────────────────┘
              │
              │   ┌──────────────────────────────────────────┐
              │   │ business-objective (Step 4.5)            │
              │   │ (strategic intent — why)                 │
              │   │ Output: OBJ-NN, KR-NN.M                  │
              │   │ Reads: P-NN · VS-N.M pain · VP-NN (BMC)  │
              │   │ Soft-links to: E-NN · QA-XXNN · PRD-NNNN │
              │   └──────────────────────────────────────────┘
              │
              ▼
   ┌──────────────────────┐   ┌──────────────────────────────────┐
   │ arch-service-contract     │   │ spec-functional-                 │
   │ (Step 7c)            │   │   breakdown-structure            │
   │ External interface   │   │ (what product does)              │
   │   contract per BC    │   │ Output: C-N.M.FXX                │
   │ Output: BC-NN.CTR-NN │   │ Inherits L0+L1 from              │
   │ Reads: AGG/ENT/EVT   │   │   capability map                 │
   └──────────────────────┘   └──────────┬───────────────────────┘
              │
              ▼
   ┌──────────────────────┐
   │ plan-delivery-roadmap  │
   │ (Plan by Feature)    │
   │ Output: E-NN         │
   │ Groups FBS by VS     │
   │   stage + capability │
   │ Orders by pain index │
   └──────────┬───────────┘
              │  ┌──────────────────────┐  ┌─────────────────────┐
              │  │ arch-cli-contract    │  │ arch-adr            │
              │  │ (Step 8.5 — opt.)    │  │ (architecture       │
              │  │ CLI surface contract │  │  decisions)         │
              │  │ Output: CLI-NN.CMD-NN│  │ Output: ADR-NNNN    │
              │  │ Reads: FBS + E-NN    │  │ Precedes Steps 9+10 │
              │  └──────────┬───────────┘  └──────────┬──────────┘
              │             │                         │
              ▼             ▼                         ▼
   ┌──────────────────────────────────────────┐
   │ spec-quality-attributes                  │
   │ (how well the system performs — NFRs)    │
   │ Output: QA-XXNN                          │
   │ Reads: FBS ★ → Reliability targets      │
   │ Reads: ADRs → Security/Flexibility QAs  │
   │ Reads: Personas → IC/PE QAs             │
   │ Reads: VS pain index → PE priorities    │
   └──────────────────┬───────────────────────┘
                      │
                      ▼
   ┌──────────────────────────────────────────┐
   │ spec-use-case (Step 9.5)                 │
   │ (actor↔system scenarios — all paths)     │
   │ Output: UC-NN                           │
   │ Reads: P-NN (actor) · C-N.M.FXX (realises)│
   │ Feeds: PRD · domain-model · test cases   │
   └──────────────────┬───────────────────────┘
                      │
                      ▼
   ┌──────────────────────────────────────────┐
   │ spec-prd (Build by Feature)              │
   │ Output: PRD-NNNN                         │
   │ One PRD per E-NN epic                    │
   │ References: E-NN · C-N.M.FXX · QA-XXNN  │
   │   · UC-NN                               │
   └──────────────────┬───────────────────────┘
                      │
                      ▼
   ┌──────────────────────┐
   │ spec-implementation- │
   │   plan               │
   │ (atomic increments)  │
   │ Output: Plan-NNNN    │
   │ One plan per PRD     │
   └──────────────────────┘
```

### Discovery routing — where the discovery layer feeds the DAG

The three `discovery-*` skills are cross-cutting and not drawn as individual arrows above to keep the main DAG readable. Their routing is enumerated here.

**`discovery-idea` graduation targets** (set per idea via `graduates_to:`):

| Idea graduates to | Becomes | Pre-flight check |
|---|---|---|
| `business-persona` | `P-NN` | `01a-personas.md` exists |
| `business-objective` | `OBJ-NN` (+ `KR-NN.M`) | `04b-objectives.md` exists (scaffold if not) |
| `business-model-canvas` | new BMC block entry (`VP-NN`, `CS-NN`, …) | canvas file exists |
| `business-process` | new `proc-NN-{slug}.md` | parent `VS-N.M` stage exists |
| `arch-research` | `Research-NNNN` | no prerequisite |
| `arch-adr` | `ADR-NNNN` | architectural choice still open |
| `spec-functional-breakdown-structure` | new `C-N.M.FXX` row | parent capability `C-N.M` exists |
| `spec-prd` | `PRD-NNNN` | an `E-NN` epic exists in the delivery roadmap |

**`discovery-research` validation targets** (any artefact carrying `Assumed` confidence rows):

- `business-persona` (Tier-1 proto-personas) · `business-model-canvas` blocks · `business-value-stream` pain indices · `business-quantitative-model` inputs · `business-objective` Key Result baselines

**`discovery-workshop` alignment targets** (any artefact requiring group consensus before lock-in):

- `business-vision` (north-star alignment) · `business-model-canvas` (BMC/Lean co-creation) · `business-value-stream` (journey mapping) · `business-capability-map` (L0 axis agreement) · `business-objective` (OKR setting) · `domain-bounded-context` (Event Storming → BC boundaries)

The discovery layer never **mints** the downstream artefact itself — it produces evidence (interview synth, workshop output) or a graduation pointer (ideation), which the downstream skill consumes during its Mode 2 fill pass.

### Entity-relationship view

The ER diagram shows which ID each artefact **mints** (PK) and which upstream IDs it **consumes** (FK) as cross-references — treating the documentation system as a data model.

```mermaid
erDiagram
    VISION {
        string file PK
    }
    PERSONA {
        string P_NN PK
    }
    CAPABILITY_MAP {
        string C_NM PK
    }
    VALUE_STREAM {
        string VS_NM PK
        string P_NN FK
        string C_NM FK
    }
    BUSINESS_PROCESS {
        string slug PK
        string VS_NM FK
    }
    BMC {
        string id PK
        string P_NN FK
    }
    QUANTITATIVE_MODEL {
        string slug PK
    }
    OBJECTIVE {
        string OBJ_NN PK
        string VS_NM FK
        string P_NN FK
    }
    KEY_RESULT {
        string KR_NNM PK
        string OBJ_NN FK
    }
    FBS {
        string C_NM_FXX PK
        string C_NM FK
    }
    EPIC {
        string E_NN PK
        string C_NM_FXX FK
        string VS_NM FK
    }
    ADR {
        string ADR_NNNN PK
    }
    QUALITY_ATTRIBUTES {
        string QA_XXNN PK
        string ADR_NNNN FK
        string P_NN FK
    }
    USE_CASE {
        string UC_NN PK
        string P_NN FK
        string C_NM_FXX FK
    }
    PRD {
        string PRD_NNNN PK
        string E_NN FK
        string QA_XXNN FK
        string ADR_NNNN FK
        string UC_NN FK
    }
    IMPLEMENTATION_PLAN {
        string Plan_NNNN PK
        string PRD_NNNN FK
    }
    INTERFACE_CONTRACT {
        string BC_NN_CTR_NN PK
        string BC_NN FK
        string BC_NN_AGG_NN FK
        string BC_NN_EVT_NN FK
        string ADR_NNNN FK
    }
    CLI_SURFACE {
        string CLI_NN PK
        string BC_NN FK
    }
    CLI_COMMAND {
        string CLI_NN_CMD_NN PK
        string CLI_NN FK
        string C_NM_FXX FK
        string BC_NN_CTR_NN FK
    }
    IDEA {
        string IDEA_NNNN PK
        string graduates_to FK
        string target_id FK
    }

    PERSONA ||--o{ VALUE_STREAM : "triggers"
    PERSONA ||--o{ BMC : "Customer Segments"
    PERSONA }o--o{ QUALITY_ATTRIBUTES : "grounds IC and PE entries"
    CAPABILITY_MAP ||--o{ VALUE_STREAM : "stages consume C-NM"
    CAPABILITY_MAP ||--|| FBS : "inherits L0 and L1"
    CAPABILITY_MAP }o--o{ BMC : "Key Resources"
    VALUE_STREAM ||--o{ BUSINESS_PROCESS : "operationalised by"
    VALUE_STREAM }o--o{ QUALITY_ATTRIBUTES : "pain index drives PE"
    VALUE_STREAM }o--o{ EPIC : "VS stage anchor"
    BMC ||--o{ QUANTITATIVE_MODEL : "Revenue and Cost"
    VISION }o--o{ PERSONA : "audience scope"
    VISION }o--o{ OBJECTIVE : "objectives operationalise"
    VISION }o--o{ BMC : "VP blocks express commercially"
    VALUE_STREAM }o--o{ OBJECTIVE : "pain index informs priority"
    PERSONA }o--o{ OBJECTIVE : "whose outcomes"
    OBJECTIVE ||--o{ KEY_RESULT : "measures progress via"
    OBJECTIVE }o--o{ EPIC : "epics serve"
    KEY_RESULT }o--o{ QUALITY_ATTRIBUTES : "KR targets ground"
    FBS ||--o{ EPIC : "grouped into epics"
    FBS }o--o{ QUALITY_ATTRIBUTES : "differentiators drive Reliability"
    ADR }o--o{ QUALITY_ATTRIBUTES : "decisions inform Security and Flexibility"
    ADR }o--o{ PRD : "decisions inform architecture"
    EPIC ||--|| PRD : "one PRD per epic"
    PERSONA ||--o{ USE_CASE : "is primary actor of"
    FBS ||--o{ USE_CASE : "realised by"
    USE_CASE ||--o{ PRD : "grounds acceptance criteria"
    QUALITY_ATTRIBUTES ||--o{ PRD : "QA-XXNN in acceptance criteria"
    PRD ||--|| IMPLEMENTATION_PLAN : "one plan per PRD"
    INTERFACE_CONTRACT }o--o{ ADR : "versioning and auth decisions"
    INTERFACE_CONTRACT }o--o{ QUALITY_ATTRIBUTES : "SLA per CTR-NN"
    INTERFACE_CONTRACT }o--o{ PRD : "acceptance criteria reference CTR-NN"
    CLI_SURFACE ||--o{ CLI_COMMAND : "contains"
    CLI_SURFACE }o--o{ BOUNDED_CONTEXT : "BC scope for BC-scoped CLIs"
    CLI_SURFACE }o--o{ ADR : "taxonomy and config decisions"
    CLI_COMMAND }o--o{ FBS : "maps to C-N.M.FXX"
    CLI_COMMAND }o--o{ EPIC : "scoped by delivery phase"
    CLI_COMMAND }o--o{ QUALITY_ATTRIBUTES : "SLA per command"
    CLI_COMMAND }o--o{ PRD : "acceptance criteria reference CMD-NN"
    CLI_COMMAND }o--o{ INTERFACE_CONTRACT : "wraps CTR-NN calls"
    IDEA }o--o| PERSONA : "graduates_to"
    IDEA }o--o| OBJECTIVE : "graduates_to"
    IDEA }o--o| BMC : "graduates_to (new block entry)"
    IDEA }o--o| BUSINESS_PROCESS : "graduates_to"
    IDEA }o--o| ADR : "graduates_to"
    IDEA }o--o| FBS : "graduates_to (new C-N.M.FXX row)"
    IDEA }o--o| PRD : "graduates_to"
```

**Hard rules of the graph:**
- An arrow `A → B` means *B soft-links to A by ID*. B can be scaffolded without A existing (placeholder `_TODO_`), but the link is filled when A arrives.
- **No cycles.** B never feeds back into A.
- The capability map (BC Map) is the **hub** — most other artefacts soft-link to it by `C-N.M` ID.
- ADRs are **not in the linear chain** but must precede Step 9 (Quality Attributes) and Step 10 (PRDs) when their decisions affect those artefacts.
- `IDEA` is **upstream of everything** and **mints no downstream FK on the target** — the relationship is one-way: an idea graduates into a target artefact and stores the target's ID in `IDEA.target_id`. The target does **not** carry an `IDEA_NNNN` FK column; it back-references the originating idea by ID in its body text (e.g., PRD §0 traceability block), not as a structural foreign key. The cardinality is `}o--o|` (each idea graduates to 0..1 target; each target may originate from 0..1 ideas).

---

## Recommended build order — greenfield software (default)

When starting a new software product or venture from scratch, follow this
order. Each step has prerequisites + outputs Claude can verify before
moving on.

### Step 0 — Product Vision (why — the north star)

**Skill:** `business-vision`
**Prerequisites:** minimal project context (product name + target audience is enough to scaffold).
**Process:**
- Mode `scaffold` → create `docs/VISION.md` with `_TODO_` placeholders
- Mode `fill` → populate §Elevator Pitch (Moore format) · §Problem We Solve · §World We're Building Toward · §What We Are NOT · §North Star Metric
- Mode `wire` → append vision pointer to project `CLAUDE.md` so every agent session auto-loads the vision
- Mode `refresh` → update when strategy pivots; check cascading effects on personas, objectives, and BMC VPs
**Output verification:** `docs/VISION.md` exists; ≤ 400 words / ≤ 1 page; §Elevator Pitch uses Moore format; §North Star is directional (no baseline/target/deadline — those are KRs); ≥ 3 specific "NOT" guardrails; `CLAUDE.md` contains a vision pointer (Wire mode).

---

### Step 1 — Personas (who)

**Skill:** `business-persona`
**Prerequisites:** Step 0 (Product Vision — if it exists, read it; personas should reflect the vision's target audience framing)
**Process:**
- Mode `scaffold` → create `docs/business/01a-personas.md`
- Mode `backlog` → identify Tier-1 / Tier-2 / Tier-3 personas with Cooper persona types
- Mode `fill-one` → write 1–3 Tier-1 personas as proto-personas (Lean UX) or research-grounded (BABOK §10.43)
**Output verification:** `01a-personas.md` exists; ≥1 Tier-1 persona filled; `P-01` through `P-NN` assigned.

### Step 2 — Business Model Canvas / Lean Canvas (commercial wrapper)

**Skill:** `business-model-canvas`
**Prerequisites:** Step 1 (personas exist for Customer Segments soft-link).
**Process:**
- Pick variant: BMC (established) or Lean Canvas (startup) at scaffold.
- Mode `scaffold` → `docs/business/02a-bmc.md` (or `docs/business/02a-lean-canvas.md`)
- Mode `fill` → populate all 9 blocks with 3–7 terse bullets + confidence rating (Assumed/Tested/Validated)
- Mode `vpc` (optional) → one VPC companion per Tier-1 segment
**Output verification:** canvas file exists; Customer Segments link to `P-NN`; ≥1 segment populated.

### Step 3 — Business Capability Map (what abilities)

**Skill:** `business-capability-map`
**Prerequisites:** Steps 1–2 (personas for context; BMC for commercial framing).
**Process:**
- Choose L0 axis (product / value-stream / capability-domain / LOB / segment / custom). Default `capability domain` if unsure.
- Mode `scaffold` → `docs/business/03a-capability-map.md`
- Mode `structure` → enumerate L0 items (3–8) + L1 capabilities (5–12 per L0; ≤25 total)
- Mode `fill` → per-capability blocks (Definition + Business Object + Strategic Importance + Outcomes + Boundaries)
**Output verification:** capability map exists; `C1` through `C-N.M` assigned; ≥6 L1 capabilities filled; each capability passes noun test + tech-independence test + anti-overlap test.

### Step 2b — Bounded Context Map (domain boundaries)

**Skill:** `domain-bounded-context`
**Prerequisites:** Step 2 (Capability Map — capabilities are the raw material for BC identification); Step 1 (Personas — personas ground the ubiquitous language scope); Step 3 (Value Streams — stage boundaries signal context boundaries; run after value streams are catalogued).
**Process:**
- Mode `discover` → read capability map + value streams; group capabilities by domain cohesion; identify boundary signals (where same word means different things; where data ownership changes; where team handoff happens); name bounded contexts
- Classify each BC: Core (competitive differentiator) / Supporting (enables Core) / Generic (commodity — buy or outsource)
- Mode `fill` → per-BC definition sections + context map with integration patterns (ACL, Shared Kernel, Customer-Supplier, Open Host Service, Published Language, Conformist)
**Output verification:** `02b-bounded-contexts.md` + `02b-context-map.md` exist; every capability `C-N.M` assigned to exactly one `BC-NN`; each BC has subdomain type + rationale; context map names integration patterns (not just "they communicate"); 1–3 Core subdomains.

### Step 2c — Domain Glossary (ubiquitous language)

**Skill:** `domain-glossary`
**Prerequisites:** Step 2b (Bounded contexts provide the namespace — one glossary section per BC).
**Process:**
- Mode `seed` → extract nouns from capability names + value stream stage names + process actor names; assign `GT-NN` IDs per BC; write one-line definitions
- Mode `enrich` → full definitions in business language + example sentences + deprecated aliases + cross-context translations + code convention notes
**Output verification:** `glossary.md` exists; every BC-NN has a glossary section; capability names have corresponding GT-NN entries; no living synonyms within a BC; definitions in business language only.
**Living document:** the glossary is never "done" — run Mode `maintain` (Step 0: trigger type + scope) every sprint for Core BC; add changelog entry for every term added, deprecated, or retired; bump `glossary-version` on structural changes.

### Step 4 — Value Streams (how value flows)

**Skill:** `business-value-stream`
**Prerequisites:** Step 1 (triggering stakeholders link to personas); Step 3 (stages consume capabilities by C-N.M ID).
**Process:**
- Mode `scaffold` → `docs/business/04a-value-streams.md`
- Mode `catalogue` → enumerate 3–10 streams per product scope, one per Tier-1 persona × value-proposition pair
- Mode `fill-one` → full stream body with 4–10 stages, each consuming 1–4 capabilities + pain index
**Output verification:** value-streams file exists; ≥1 stream fully filled; each stage links to ≥1 capability by `C-N.M` ID.

### Step 4.5 — Business Objectives (why — strategic intent)

**Skill:** `business-objective`
**Prerequisites:** Step 1 (Personas — whose outcomes the objectives serve); Step 2 (BMC — `VP-NN` Value Propositions are the commercial intent that objectives operationalise); Step 4 (Value Streams — pain index per `VS-N.M` prioritises which objectives matter most).
**Process:**
- Mode `scaffold` → create `docs/business/04b-objectives.md` with OBJ-NN placeholder blocks
- Mode `fill` → populate each OBJ-NN: qualitative title, BSC perspective tag, timeframe, owner, "why it matters" sentence linked to `VP-NN` or `VS-N.M` pain index; 3–5 Key Results per objective (outcome statements with baseline, target, measurement method)
- Mode `align` → after the delivery roadmap exists, build the §Objective × Epic traceability matrix; flag orphaned epics (no OBJ-NN) and undelivered objectives (no E-NN)
- Mode `refresh` → update KR baselines/targets when evidence arrives; add changelog entry
**Output verification:** `objectives.md` exists; ≥1 OBJ-NN filled with qualitative title + BSC perspective + timeframe + owner; every KR is an outcome (metric change), not an output (feature delivery); every OBJ-NN traces to ≥1 `VP-NN` or `VS-N.M`; 2–5 objectives total; ≥1 Customer-perspective objective.

---

### Step 5 — Business Processes (operational how)

**Skill:** `business-process`
**Prerequisites:** Step 4 (processes operationalise value-stream stages — but processes can also exist independently for non-customer-facing operations).
**Process:**
- One process doc per major operational workflow.
- Mode `scaffold` per process → `docs/business/05a-processes/proc-NN-{slug}.md`
- Fill BPMN-ready template (actors, activities, data, KPIs, decisions).
**Output verification:** each Tier-1 value-stream stage has ≥1 process doc operationalising it.

### Step 6 — Quantitative Models (numbers)

**Skill:** `business-quantitative-model`
**Prerequisites:** Step 2 (BMC's Revenue Streams + Cost Structure provide qualitative anchors); Step 1 (personas drive segmentation).
**Process:**
- One model per quantification need: TAM/SAM/SOM, savings, ROI, restitution, unit economics.
- Each model file in `docs/business/06a-models/qm-NN-{topic}.md`.
**Output verification:** ≥1 model exists; BMC's Revenue Streams + Cost Structure link to relevant models.

### Step 7 — Functional Breakdown Structure (what product does, status-tracked)

**Skill:** `spec-functional-breakdown-structure`
**Prerequisites:** Step 3 (BC Map — FBS inherits L0+L1).
**Process:**
- Mode `scaffold` → `docs/product-specs/07a-fbs.md`
- Mode `structure` → auto-import L0+L1 from BC Map; pre-fill per-capability sections
- Mode `fill` → enumerate functionalities per capability with `C-N.M.FXX` IDs + status (✅/🔄/⬜) + optional VS-stage links + code paths
**Output verification:** FBS exists; ≥1 capability has ≥1 functionality; status distribution shows initial state.

### Step 7b — Domain Model (entities · aggregates · value objects · domain events)

**Skill:** `domain-model`
**Prerequisites:** Step 2b (Bounded contexts provide BC-NN namespace); Step 2c (Glossary terms — entity names MUST match GT-NN); Step 7 (FBS — functionalities reveal candidate entities and aggregates); Step 3 (Value Stream stages — stage transitions reveal domain events).
**Process:**
- One file per bounded context: `docs/domain/07b-models/{bc-slug}.md`
- Mode `fill` → per aggregate: root, invariants, lifecycle states, command→event pairs; per entity: identity, attributes, behaviour methods; per value object: attributes, equality rule, validation invariants; per domain event: trigger, payload, consumers, business significance
- Mode `verify` → check for anemic model (entities must have behaviour); check aggregate sizing (≤5 members); check event naming (past tense + business-meaningful)
**Output verification:** one `{bc-slug}.md` per BC-NN in `docs/domain/07b-models/`; every aggregate has a named root + ≥2 documented invariants; all entity names match GT-NN glossary terms; all domain events are past tense + carry business significance; Mermaid class diagram present.

### Step 7c — Interface Contract (external API + async surface per BC)

**Skill:** `arch-service-contract`
**Prerequisites:** Step 7b (Domain Model — aggregates, entities, value objects, domain events are the raw material for the contract); Step 2c (Glossary — resource and event names must match GT-NN terms); relevant ADRs for versioning strategy, auth mechanism, and event-bus choice.
**Process:**
- Mode `scaffold` → create `docs/architecture/interfaces/{bc-slug}.md` with `_TODO_` placeholders; one file per BC
- Mode `contract-first` → read domain model (AGG-NN, ENT-NN, EVT-NN); map aggregates to REST resources; map domain events to async events; define error contract (RFC 7807), versioning policy, and security surface; assign `BC-NN.CTR-NN` IDs
- Mode `document-existing` → reverse-engineer from route files or OpenAPI specs; emit drift report (surface elements with no domain model backing)
- Mode `refresh` → detect additions, removals, renames vs. current domain model; classify breaking vs non-breaking changes; append changelog
**Output verification:** `docs/architecture/interfaces/{bc-slug}.md` exists; every CTR-NN entry maps to a `BC-NN.AGG-NN`, `BC-NN.ENT-NN`, or `BC-NN.EVT-NN`; no verb in REST paths (exception: `/actions/{verb}`); pagination envelope on all collection endpoints; RFC 7807 error contract present; versioning and security surfaces present; CTR-NN IDs monotonically assigned.

---

### Step 8 — Delivery Roadmap (Plan by Feature + Walking Skeleton + Phase Goals)

**Skill:** `plan-delivery-roadmap`
**Prerequisites:** Step 7 (FBS — VS stage links + phase tags + ★ markers); Steps 3–4 (Value Streams — pain index + value propositions); Step 1 (Personas — for walking skeleton narrative).
**Process:**
- Read FBS + value streams + personas
- Group FBS functionalities by VS stage affinity + capability cluster → E-NN epics
- Order by pain index; assign E-NN IDs in priority order
- Define Walking Skeleton: identify the primary VS to validate; select minimum functionalities per epic covering every VS stage end-to-end; write "can / cannot yet" statement
- Define Phase Plan: declare which VS streams become fully operational per phase; write one-sentence goal per phase
- Produce `docs/plans/delivery-roadmap.md`
- Coverage check: every Phase 1 FBS functionality in exactly one epic
**Output verification:** `docs/plans/delivery-roadmap.md` exists; §Walking Skeleton covers every stage of primary VS; §Phase Plan has one goal per phase expressed as VS streams operational; every epic has a value statement; ★ functionalities each anchor their own epic; sizing within 5–25 FBS rows per epic; E-NN IDs in pain-index order.

### Step 8.5 — CLI Surface Contract (only when the product exposes a CLI)

**Skill:** `arch-cli-contract`
**Prerequisites:** Step 7 (FBS — `C-N.M.FXX` functionalities map to CLI commands); Step 8 (Delivery Roadmap — `E-NN` phase tags drive `status: planned` vs `status: active` per command). ADRs for command taxonomy, config format, and output format should be written before or alongside this step.
**Process:**
- Mode `scaffold` → create `docs/architecture/interfaces/cli-{slug}.md` with `_TODO_` skeleton
- Mode `design` → read FBS + delivery roadmap; derive command tree by capability cluster; assign `CLI-NN.CMD-NN` IDs; define global flags, exit code catalogue, stdout/stderr contract, configuration precedence
- Mode `document-existing` → parse `--help` output or source; emit drift report (commands with no FBS backing; FBS functionalities not yet surfaced)
- Mode `refresh` → detect added/removed commands vs current FBS; classify breaking vs non-breaking; append changelog
**Output verification:** `docs/architecture/interfaces/cli-{slug}.md` exists; every `CLI-NN.CMD-NN` maps to a `C-N.M.FXX` or `E-NN`; `--help` and `--version` documented; stdout/stderr separation explicit; exit code catalogue present; `--dry-run` on all mutating commands; `--output json` documented; colour policy present.

---

### Step 9 — Quality Attributes (how well the system performs)

**Skill:** `spec-quality-attributes`
**Prerequisites:** Step 7 (FBS differentiators ★ drive Reliability targets); Step 8 (epic scope clarifies which QA entries apply to which delivery cluster); relevant ADRs (Security, Flexibility, Maintainability QAs reference ADR decisions); Step 1 (Personas ground IC and PE entries); Steps 3–4 (VS pain index prioritises PE entries).
**Process:**
- Mode `scaffold` → create `docs/product-specs/09a-quality-attributes.md` with ISO/IEC 25010:2023 characteristic sections
- Mode `fill` → one entry per sub-characteristic × product scope; measurable acceptance criterion + verification method; persona-grounded for IC and PE; reference ADR IDs for Security/Flexibility/Maintainability decisions
**Output verification:** file exists; ≥1 entry per relevant ISO characteristic; all entries have measurable acceptance criteria; IC/PE entries reference P-NN personas; differentiator FBS features (★) have Reliability entries.

### Step 9.5 — Use Cases (actor↔system behavioural scenarios)

**Skill:** `spec-use-case`
**Prerequisites:** Step 1 (Personas — `P-NN` become primary actors); Step 7 (FBS — `C-N.M.FXX` functionalities the use case *realises*). Optional: Steps 3–4 (a value-stream stage often supplies the trigger). Soft-linked, not blocking — author use cases even if the FBS is incomplete.
**Process:**
- Mode `scaffold` → create `docs/product-specs/use-cases/index.md` registry
- Mode `fully-dressed` → author one use case (mint `UC-NN`); fix Scope + Level first; numbered main success scenario + per-step extensions + guarantees; `Realises: C-N.M.FXX`, `Primary Actor: P-NN`
- Mode `casual` → lightweight prose variant for low-risk goals
- Mode `slice` → Use-Case 2.0 — basic flow + alternative flows become backlog-ready slices (`UC-NN.S1`…), each with a test case
- Mode `review` → quality-audit against the effective-use-case checklist (report-only)
**Output verification:** `docs/product-specs/use-cases/index.md` + `uc-NN-*.md` exist; each states Scope + Level; main success scenario numbered/active-voice/UI-free; every step has its extensions; minimal + success guarantees present; `Realises:` links resolve to FBS IDs; user-goal level passes the coffee-break test.

### Step 10 — PRDs (Build by Feature)

**Skill:** `spec-prd`
**Prerequisites:** Step 8 (one PRD per E-NN epic — scope pre-defined); Step 9 (PRDs reference `QA-XXNN` in acceptance criteria); Step 9.5 (PRDs reference the `UC-NN` use cases they deliver — the scenario grounds the acceptance criteria); relevant ADRs (PRDs do not re-open decided architectural choices).
**Process:**
- One PRD per epic: `docs/product-specs/prds/prd-NNNN-{feature}.md`
- Each PRD: §0 Architecture Traceability (E-NN, P-NN, C-N.M, QA-XXNN, UC-NN, FBS scope) · problem · goals · non-goals · user stories (persona-grounded, P-NN) · acceptance criteria · success metrics
**Output verification:** ≥1 PRD per active epic (E-NN); each PRD references its E-NN, FBS IDs, and QA IDs; FBS functionality status promoted ⬜ → 🔄; Delivery Roadmap PRD link filled.

### Step 11 — Implementation Plans (atomic increments)

**Skill:** `plan-implementation`
**Prerequisites:** Step 10 (PRDs).
**Process:**
- One plan per PRD: `docs/plans/active/{NNNN}_exec_{slug}.md`
- Each plan: numbered increments (Inc-1, Inc-2, …), each small + testable + reversible.
**Output verification:** each in-flight PRD has a corresponding plan; plan increments are atomic + testable.

### Ongoing — ADRs, runbooks, ideas, audit

Not numbered in the linear build order but sequencing matters:
- `arch-adr` → invoke as soon as an architectural choice must be made; ADRs governing security, flexibility, or maintainability must precede Step 9 (Quality Attributes); all ADRs must precede Step 10 (PRDs) that depend on their decisions
- `ops-runbook` → operational procedures captured post-ship
- `ops-bug-rca` → root cause analyses post-incident
- *(reserved)* `qa-*` → the **validate / test** stage, sitting between Step 11 (implementation plans) and deploy/ops. A reserved category with **no skill yet** (`qa-test-strategy`, `qa-test-plan`, `qa-acceptance-test`, `qa-eval-harness` → `docs/qa/`); it will produce the tests that verify the `QA-XXNN` quality requirements `spec-quality-attributes` defines — distinct from it. The lead skill `qa-test-strategy` (was the planned `spec-test-strategy`, OI-0004) covers the test pyramid + coverage + `QA-XXNN`→test-type mapping and **mints `TS-NN`** → `docs/qa/test-strategy/`; `qa-test-scenario` *realises* `UC-NN` (a use case's main + alternate + exception flows become the test scenarios; PRD acceptance criteria are the oracle; step vocabulary from the glossary `GT-NN`)

- `discovery-idea` → pre-formal idea capture, refinement, and graduation (an idea graduates to whichever downstream skill matches its matured form — `spec-prd`, `arch-adr`, `business-persona`, `business-objective`, etc.)
- `agent-*` (Agent-Centric Development Cycle) → cross-cutting agent tooling: `agent-config` (Guide — `CLAUDE.md`/`AGENTS.md`), `agent-grill-me` + `agent-peer-review` (Verify — stress-test / review PRDs & plans before implementation), `agent-ralph-loop` (Solve — autonomous increment execution); mint no IDs
- `ux-design-system` → scaffold the project visual source of truth (`docs/ux/design-system.md` → `tokens.css`) before producing any communication artefact, so every slide deck and artefact visualisation themes consistently; cross-cutting, mints no IDs, re-run `refresh` when the brand changes
- `util-docs-audit` → periodic health check (quarterly)

---

## Variants for non-greenfield projects

### Brownfield IT project (existing system, adding capability)

Start at **Step 3** (Business Capability Map), skip Steps 1–2 unless:
- The capability touches a stakeholder group not yet documented (then do Step 1 lightweight for that persona).
- The capability changes the commercial model (then do Step 2 — usually skipped).

**Sequence:** Step 3 (BC Map) → Step 4 (value stream for the affected flow) → Step 5 (process docs for the as-is operational state) → Step 2b (Bounded Context Map) → Step 2c (Glossary) → Step 7 (FBS) → Step 7b (Domain Model) → Step 8 (Delivery Roadmap) → Step 9 (Quality Attributes — at minimum Reliability entries for new differentiator features) → Step 10 (PRDs) → Step 11 (plans).

### Single feature (no full architecture work)

Skip Steps 1–8 entirely. Go straight to:
- Step 10 (`spec-prd`) for the feature — manually define the E-NN scope inline in §0.
- Step 11 (`plan-implementation`) for the plan.

Optionally: `discovery-idea` first if the feature is still hypothetical — refine it through the divergent/convergent loop, then graduate to `spec-prd`. Write relevant ADRs before the PRD if architecture decisions are open. Write domain model for the feature's aggregate (Step 7b) if the aggregate isn't already modelled.

### Strategy / investor / executive engagement only

Start at **Step 2** (BMC) for the strategic one-pager. Skip Steps 7–11 entirely. Optionally add:
- Step 1 (personas) — investors love seeing customer specificity.
- Step 6 (quantitative model) — TAM/SAM/SOM for the deck.
- Step 3 (BC Map) — only if the strategic conversation needs the capability lens.

---

## Cross-doc ID conventions

Artefact-type id_formats are defined in the structural registry [`artefact-types-registry.md`](artefact-types-registry.md). This section lists the remaining IDs — diagram, C4/arc42, and sub-element identifiers — which are not artefact types.

### Diagram & sub-element IDs (not in the artefact-types registry)

| ID format | Meaning | Owned by |
|---|---|---|
| `SYS-NN` | Software System in the C4 model (DSL identifier `SYS_NN`) — system being documented + external systems | `arch-c4` (context mode) |
| `CON-NN` | Container in the C4 model (DSL identifier `CON_NN`) — deployable runtime unit (app, service, database, message broker) | `arch-c4` (container mode) |
| `CMP-NN` | Component in the C4 model (DSL identifier `CMP_NN`) — code module inside a container; carries `properties.implements "BC-NN.AGG-NN"` back-reference into `domain-model` (or `"none"` for tech-only) | `arch-c4` (component mode) |
| `DN-NN` | Deployment Node in the C4 model (DSL identifier `DN_NN`) — infrastructure element (region, cluster, VM, managed service) | `arch-c4` (deployment mode) |
| `SCN-NN` | Runtime scenario documented in arc42 §6 — one per key use case or error path; figure is a C4 dynamic view or an `arch-uml` sequence | `arch-arc42` (runtime mode; owns §6 + SCN-NN — `arch-c4` only renders the dynamic-view SVG keyed by it) |
| `CST-NN` | Architecture constraint — technical, organizational, or legal-regulatory constraint limiting the solution space | `arch-arc42` (constraints mode) |
| `CC-NN` | Cross-cutting concept — horizontal concern applying to multiple containers (auth, logging, error-handling, persistence, caching, etc.) | `arch-arc42` (cross-cutting mode) |
| `RSK-NN` | Architectural risk or technical debt item — four types: `architectural`, `technical-debt`, `dependency`, `security` | `arch-arc42` (risks mode) |
| `Inc-N` (within a plan) | Plan increment | `plan-implementation` |

**BC-NN namespace rule:** All tactical DDD IDs are scoped to their bounded context. `BC-01.AGG-03` and `BC-02.AGG-03` are different aggregates. Cross-references must always include the BC prefix — bare `AGG-03` is ambiguous and invalid.

**Cross-doc linking rule:** any artefact that references another should use the ID + name + relative path:

> `[C3.2 KOGU prior-authorisation classification](../03a-capability-map.md#c32)` 

so that future renames (description text) don't break the link as long as the ID is stable.

---

## Canonical output paths

The `docs/` folder + infrastructure map. Per-type file paths are authoritative in [`artefact-types-registry.md`](artefact-types-registry.md).

```
docs/
├── index.md                                             ← OKF bundle root (reserved file): okf_version + live nav hub; frontmatter-free except okf_version
├── VISION.md
├── business/                                            ← Business Architecture
│   ├── 01a-personas.md
│   ├── 02a-bmc.md  (or 02a-lean-canvas.md)
│   ├── 02a-vpc-{segment}.md  (optional per CS)
│   ├── 03a-capability-map.md
│   ├── 04a-value-streams.md
│   ├── 04a-vpc-{segment}.md  (optional per VS)
│   ├── 04b-objectives.md
│   ├── 05a-processes/
│   │   └── proc-NN-{slug}.md (one per process)
│   └── 06a-models/
│       └── qm-NN-{topic}.md (one per model)
├── product-specs/                                       ← Product specs (spec-)
│   ├── use-cases/                                       ← index.md + uc-NN-{slug}.md
│   ├── 07a-fbs.md
│   ├── 09a-quality-attributes.md
│   └── prds/
│       └── prd-NNNN-{feature}.md (one per PRD)
├── plans/                                               ← Build planning (plan-)
│   ├── delivery-roadmap.md                              ← epics (E-NN)
│   └── active/
│       └── {NNNN}_exec_{slug}.md  (one per implementation plan)
├── architecture/                                        ← Architecture
│   ├── decisions/                                       ← ADRs
│   │   └── adr-{NNNN}-{slug}.md
│   ├── interfaces/                                      ← service + CLI contracts
│   │   ├── {bc-slug}.md  (BC-scoped API, one per BC)
│   │   ├── {slug}.md  (product-level API, spans BCs)
│   │   └── cli-{slug}.md  (one per CLI tool)
│   ├── c4/                                              ← arch-structurizr foundation
│   │   ├── workspace.dsl                                ← Structurizr DSL
│   │   ├── render.sh                                    ← Docker render pipeline
│   │   ├── README.md                                    ← render + pinning conventions
│   │   └── views/                                       ← rendered SVGs (committed)
│   │       ├── systemContext.svg
│   │       ├── containers.svg
│   │       ├── components-CON-NN.svg
│   │       └── deployment-{env}.svg
│   ├── diagrams/                                        ← arch-plantuml foundation
│   │   ├── _theme.puml                                  ← shared theme
│   │   ├── render.sh                                    ← Docker render pipeline
│   │   ├── README.md                                    ← render + pinning conventions
│   │   ├── {type}-NN-{slug}.puml                        ← arch-uml diagram sources
│   │   └── views/                                       ← rendered SVGs (committed)
│   └── arc42/                                           ← arch-arc42 narrative
│       ├── 02-constraints.md
│       ├── 03-context.md
│       ├── 04-solution-strategy.md
│       ├── 05-building-blocks.md
│       ├── 06-runtime-view.md
│       ├── 07-deployment.md
│       ├── 08-cross-cutting-concepts.md
│       └── 11-risks.md
├── domain/                                              ← Domain (DDD)
│   ├── 02b-bounded-contexts.md
│   ├── 02b-context-map.md
│   ├── 02c-glossary.md
│   └── 07b-models/                                      ← one file per BC
│       └── {bc-slug}.md
├── ops/                                                 ← Operations
│   ├── runbooks/
│   │   └── {slug}.md
│   └── rcas/
│       └── {YYYY-MM-DD}-{slug}.md
├── qa/                                                  ← Quality assurance & test (reserved — no skill yet)
│   ├── test-strategy/                                   ← qa-test-strategy (planned; mints TS-NN)
│   └── (test plans · acceptance & eval harnesses)
├── ux/                                                  ← Design system (cross-cutting; mints no IDs)
│   ├── design-system.md                                ← authored brand + tokens
│   └── tokens.css                                       ← generated token contract
├── communication/                                       ← Communication artefacts
│   ├── visualisations/                                 ← com-artefact-viz ({kind}.html)
│   └── slides/
│       └── {slug}/                                      ← com-slide-deck (one per deck)
│           ├── context/
│           ├── design/
│           ├── src/
│           ├── dist/
│           └── config.yaml
├── discovery/                                           ← Pre-formal evidence (cross-cutting)
│   ├── ideation/                                       ← discovery-idea
│   │   ├── index.md
│   │   └── IDEA-NNNN-{slug}.md (one per idea)
│   ├── interviews/                                     ← discovery-research
│   │   └── interview-{persona-id-or-slug}-{topic}.md · research-synthesis-{date}-{topic}.md · research-plan-{topic}.md
│   └── workshops/                                     ← discovery-workshop
│       └── workshop-{slug}-{date}.md · workshop-synthesis-{slug}-{date}.md
└── dev-guides/                                         ← Developer reference (not a metamodel step)
    ├── getting-started.md
    ├── {tech-slug}.md (one per technology)
    └── research/                                       ← research scratch
        └── {tech-slug}-research.md
```

**Prefix → folder mapping (memorise this):**

| Prefix | Folder | Note |
|---|---|---|
| `business-` | `docs/business/` | All BIZBOK Business Architecture artefacts. **Exception:** `business-vision` outputs to `docs/VISION.md` (project root level) for agent-context visibility — the only `business-` skill whose output is not under `docs/business/`. |
| `discovery-` | `docs/discovery/` | Pre-formal evidence layer — ideation, 1:1 research, group workshops. Cross-cutting; feeds every downstream artefact. Subfolders per artefact (`ideation/`, `interviews/`, `workshops/`). |
| `spec-` | `docs/product-specs/` | Product specs — FBS, quality attributes, use cases, PRDs (what the product does and how well). |
| `plan-` | `docs/plans/` | Build planning — delivery roadmap (epics `E-NN`) + implementation plans (`Plan-NNNN`). Split from `spec-` (clew ADR-0009): these specify *intended build sequence*, not the product. |
| `arch-` | `docs/architecture/` | Subfolders per artefact (e.g., `decisions/` for ADRs) |
| `domain-` | `docs/domain/` | DDD artefacts — the shared language between business and tech (bounded contexts, glossary, domain model) |
| `ops-` | `docs/ops/` | Subfolders per artefact (`runbooks/`, `rcas/`) |
| `qa-` | `docs/qa/` | Quality-assurance & test layer (test strategy, test plans, acceptance & eval harnesses). Produces the *tests* that verify the `QA-XXNN` quality requirements `spec-quality-attributes` defines — distinct from it. **Reserved category — no skill yet** (`qa-test-strategy` will mint `TS-NN`). |
| `ux-` | `docs/ux/` | Design + experience layer — project visual source of truth (`design-system.md` + generated `tokens.css`) plus UX artefacts. Cross-cutting foundation for the `com-` presentation layer. Skill: `ux-design-system` (standard `<category>-<artefact>` naming). |
| `com-` | `docs/communication/` | Communication artefacts (slide decks, presentations, artefact visualisations). Subfolders per artefact type (e.g. `slides/`, `visualisations/`). |
| `dev-` | *(no doc folder)* for workflow utilities · **exception:** `dev-stack-guide` → `docs/dev-guides/{tech-slug}.md` + `docs/dev-guides/research/`; `dev-getting-started` → `docs/dev-guides/getting-started.md` | Developer-workflow utilities; `dev-stack-guide` and `dev-getting-started` are the only `dev-` skills that write to `docs/` |
| `agent-` | *(no doc folder)* | **Agent-Centric Development Cycle** (Guide → Verify → Solve): `agent-config` (Guide), `agent-grill-me` + `agent-peer-review` (Verify), `agent-ralph-loop` (Solve). Mint no IDs; orchestrate *how the agent builds*, not *what the product is*. |
| `util-` | *(no doc folder)* | Housekeeping |

---

## Open Items governance (cross-cutting)

Every artefact in the stack can carry unresolved work — research questions, missing
decisions, follow-up items, deferred refactors. The canonical contract for capturing,
classifying, syncing, and auditing that work lives in
[`rules/open-items-governance.md`](./open-items-governance.md). It is mandatory for any
skill whose output may emit unresolved work.

Summary of the contract (full details in the dedicated rule):

- **Single section:** each artefact exposes one **document-level** `## Open Items` section.
  No nested `### Open Items` subsections, no legacy variants (`Open / TODO`, `Open
  questions remaining`, `§Open Issues`).
- **Item taxonomy:** every row is one of `doc-gap`, `decision-gap`, `execution-item`,
  `tech-debt`. Inline `_TODO_` scaffold placeholders are explicitly **not** open items.
- **Provenance:** rows that originate in a sub-section of the artefact carry both a
  `Source anchor` (short fragment identifier like `#q3`) and a `Source heading` (the full
  human-readable heading text). The pair survives anchor renames and heading edits.
- **Central control plane:** the consolidated living ledger is
  `docs/project-control/open-items/` — under `docs/` for unified navigation but in a
  dedicated `project-control/` folder because it is an operational system of record, not
  a product artefact (so product-spec audits don't sweep it). Product backlog (PRDs, FBS,
  epics) remains separate.
- **Tooling boundaries:** `util-docs-audit` stays generic. `util-open-items` performs
  ledger CRUD. `util-metamodel-audit` is report-only and verifies governance drift.

When a new skill produces or governs unresolved work, conform to §8 of
`rules/open-items-governance.md` (Skill conformance checklist) — canonical heading, schema,
provenance, sync chaining.

---

## How Claude should use this rule

When the user invokes documentation work on a project:

1. **Detect what already exists** — `find docs -type d` to map the current state.
2. **Identify which steps are done vs missing** by checking output paths above.
3. **Pick the variant** (greenfield / brownfield / single-feature / strategy-only) based on user intent.
4. **Execute the next step** using the corresponding skill in its appropriate mode.
5. **Verify the output** before moving on — each step's "Output verification" criteria.
6. **Maintain cross-doc IDs** — every soft-link should use the ID + path format above.

When asked *"build the documentation plan"* without further context, default to:
- Confirm the variant with the user (greenfield is the default).
- Start at Step 1; ask for personas input.
- Proceed sequentially through verification checks.
- One step per session unless the user wants batch execution.

This rule is the single source of truth for the strategic-architecture
build order. When new skills join the kit, update the layer table and
DAG here.

**Maintenance coupling — update these files whenever this rule changes:**

Every change to canonical paths, artefact steps, or ID formats in this file has downstream copies that must be kept in sync:

| What changed | Also update |
|---|---|
| New artefact **type**, or a change to its id_format / path / layout / skill | `rules/artefact-types-registry.md` → add or update the type's row |
| New artefact step, new canonical path | `util-metamodel-audit/references/check-catalogue.md` → Check 1 (stack progress paths) |
| New ID format (e.g. new `XX-NN` pattern) | `util-metamodel-audit/references/check-catalogue.md` → Check 5 (ID cross-reference regex patterns) |
| New prerequisite dependency in the DAG | `util-metamodel-audit/references/check-catalogue.md` → Check 7 (dependency enforcement rules) |
| New artefact step, new canonical path | `util-metamodel-migration/references/detection-signals.md` → §Filename patterns + §Folder name patterns + §Content signals |
| New mandatory section in a skill's template | `util-metamodel-audit/references/check-catalogue.md` → Check 9 (mandatory sections table) |
| New artefact step, new canonical path | `util-metamodel-scaffold/references/folder-catalogue.md` → all four variant folder lists (add to Greenfield; add to Brownfield/Strategy/Single-feature if relevant) |
| New artefact step, new canonical path | `util-metamodel-scaffold/references/index-template.md` → §Detection bash block + §Template stack-progress table (add detection command + row) |

Failing to update these files after a metamodel change will cause the audit and migration skills to silently miss the new artefact — the most dangerous kind of drift.

---

## Change history

The metamodel's change + coupling history lives in [`metamodel-changelog.md`](metamodel-changelog.md). The authoritative record is `git log` / `git blame` on this file and its coupled files; the *why* of each change is its ADR.
