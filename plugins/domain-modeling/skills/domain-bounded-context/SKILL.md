---
type: skill
name: domain-bounded-context
description: "Create a Bounded Context Map + Context Map for a project using strategic DDD. Identifies bounded contexts from the capability map, classifies each as Core / Supporting / Generic subdomain (Vernon), maps integration patterns between contexts (Evans: ACL, Shared Kernel, Customer-Supplier, Open Host Service, Published Language, Conformist). Synthesises Evans Domain-Driven Design (2003) Chapter 14 + Vernon DDD Distilled (2016) Chapter 3-4 + Nick Tune Architecture Modernization (2024). Use when asked to identify bounded contexts, define system boundaries, map context relationships, classify subdomains, or align team topology with domain boundaries. Triggers on: bounded context, context map, subdomain, DDD boundaries, domain boundaries, core domain, supporting domain, generic subdomain, context mapping, anti-corruption layer, domain-driven design boundaries. Output: docs/domain/. Soft-links to capability map (C-N.M), personas (P-NN), value streams (VS-N.M)."
version: "1.0.0"
user-invocable: true
impact: "low"
metadata:
  category: "domain"
  complexity: "high"
status: active
last_reviewed: 2026-05-29
---

# Bounded Context Builder

You are an expert at producing **strategic DDD Bounded Context Maps** — the artefacts that answer one question: *"where does the domain model change meaning, and what are the explicit relationships between those islands of meaning?"*

The artifacts produced by this skill are **two markdown documents** in the project's domain folder (default `docs/domain/`):
- `02b-bounded-contexts.md` — the catalogue of bounded contexts, their subdomain type, owned capabilities, and team ownership.
- `02b-context-map.md` — the integration pattern map showing how bounded contexts relate to each other.

This is NOT an org chart, NOT a microservices deployment diagram, NOT a data flow diagram. It is the **strategic model of where the domain model changes meaning**, expressed as named bounded contexts with explicit integration patterns between them.

This skill is **domain-agnostic**. The pattern works for any product, service, or enterprise. When activated inside a project, the skill picks up the project's existing capability map, value streams, and personas as inputs.

---

## What a good Bounded Context Map means

A bounded context map is good when a reader can answer, without ambiguity:

| Question | Where it lives |
|---|---|
| **What contexts exist and what is each responsible for?** | §Subdomain catalogue + per-BC responsibility statement |
| **Which is the Core domain (competitive advantage)?** | Subdomain type column — Core / Supporting / Generic |
| **How do contexts relate to each other (which integration pattern)?** | §Context map — named Evans pattern per relationship |
| **Which capabilities belong to which context?** | Per-BC capabilities list (C-N.M IDs) |
| **What crosses the boundary (data + events)?** | Per-relationship "what crosses the boundary" field |
| **Which team should own which context?** | Per-BC team boundary recommendation |

**Hard scope rule:** a bounded context is not a deployment unit, not a database schema, not a team. It is the **boundary within which a domain model is consistent** — where the word "Customer" (or "Order", or "Claim") means one precise thing and is owned by one model. Don't let technology or org structure drive the discovery; let the domain language drive it.

---

## The four modes of operation

The skill operates in one of four modes. Detect from the user's prompt; ask if ambiguous.

### Mode 1 — Scaffold

**When:** the project has no `docs/domain/` folder yet, or has the folder but no files.

**Output:** two empty template files:
- `02b-bounded-contexts.md` — catalogue skeleton with placeholder BC-01 / BC-02 rows.
- `02b-context-map.md` — Mermaid flowchart skeleton + relationship definition blocks.

Source from `references/template.md`. Substitute `{{product}}` placeholders. Do NOT invent bounded contexts in scaffold mode — leave the catalogue as a `_TODO_` skeleton.

**Do NOT** ship a project-side `methodology-references.md`. The canonical bibliography lives in the skill at `references/methodology-references.md` and is linked from the project doc's header. Single source of truth; no drift across projects.

### Mode 2 — Discover

**When:** the scaffold exists; the user wants to identify and name the bounded contexts from project context.

**Step 0 — Clarifying questions (ask BEFORE generating)**

Ask the user the following 4 questions in a single message with lettered options. Users respond like `1A, 2B, 3C, 4B`:

```text
1. BC discovery basis?
   A. Top-down from capability map — L0 groups → BC candidates (recommended)
   B. Event Storming output exists — domain events → aggregate clusters → BCs
   C. Hybrid — capability map + value stream boundary analysis
   D. Reverse-engineer from existing codebase module structure

2. Subdomain classification basis?
   A. Strategic intent — leadership knows which capabilities are Core competitive advantage
   B. Cost/benefit — Core = build; Supporting = build or buy; Generic = buy/SaaS
   C. Both — validate strategic intent with build-vs-buy analysis

3. Team topology (Conway's Law)?
   A. Yes — BC boundaries should suggest team ownership
   B. No — pure domain consideration; team topology handled separately
   C. Note ideal but don't constrain — document recommendation only

4. Context map evidence?
   A. I know the integration patterns — will specify per relationship
   B. Discover from existing APIs, event buses, shared databases
   C. Scaffold with _TODO_ — fill integration patterns in Mode 3
```

**Process:**
1. **Read project context** — capability map, value streams, personas, PRDs, any Event Storming outputs or existing module structure.
2. **Identify context boundary signals** — where does the same word mean different things? (e.g., "Customer" in sales context vs. "Patient" in care context even if the underlying entity is the same person). Where does data ownership change? Where do team handoffs naturally occur? Where do value stream stages cross an organisational seam?
3. **Name the bounded contexts** — noun phrases in the ubiquitous language of that context. Business experts must understand the name without knowing what a microservice is.
4. **Assign capabilities to BCs** — each capability C-N.M goes to exactly one BC. No unassigned capabilities, no double-assigned capabilities.
5. **Classify subdomains** — Core / Supporting / Generic per context. See `references/discipline.md` §Subdomain classification guide.
6. **Produce `02b-bounded-contexts.md`** — catalogue table + per-BC definition sections.

### Mode 3 — Fill

**When:** 02b-bounded-contexts.md has the BC catalogue; the user wants to:
- Fill per-BC definition sections in full.
- Draw the context map with named integration patterns.
- Map every relationship to one of Evans' eight patterns.

**Process:**
1. For each BC, fill the canonical definition block (see `references/template.md`): responsibility statement, subdomain type + rationale, capabilities owned, ubiquitous language scope, canonical data owned, integration interfaces, team boundary recommendation.
2. For each BC-to-BC relationship, pick the integration pattern using the decision tree in `references/discipline.md`. Record: upstream / downstream, pattern name + Evans definition, what crosses the boundary, translation layer description (for ACL), technical implementation hint, coupling risk.
3. Render the Mermaid flowchart in `02b-context-map.md` with BCs as nodes and integration pattern names as edge labels.
4. Run the quality checks from `references/discipline.md` §Quality checks.

### Mode 4 — Refresh

**When:** bounded contexts and context map exist; system has evolved and boundaries need re-evaluation.

**Process:**
1. **Re-read** 02b-bounded-contexts.md and 02b-context-map.md against current capability map + codebase (if available).
2. **Flag split candidates** — BCs that have grown too large: >7 aggregates (preview), team friction at the boundary, multiple unrelated ubiquitous language clusters under one BC name.
3. **Flag merge candidates** — BCs that are too small: <2 capabilities, trivial integration (pure delegation), or context map shows it only conforms to one upstream without adding any translation.
4. **Flag pattern drift** — relationships that were ACL but the translation layer was never built (now de facto Conformist). Rename and document the debt.
5. Produce a changelog entry + recommendations section. Do NOT rewrite the whole document — targeted updates only.

---

## The eight anti-patterns

1. **God context** — one BC that owns everything. Defeats the purpose. Split by subdomain type (Core vs. Supporting) or by ubiquitous language cluster.

2. **Technology-named contexts** — "MicroserviceA", "DatabaseB", "APIGateway". Names must be business concepts. The boundary is semantic, not technical. A name that would change when you replace the database is not a bounded context.

3. **CRUD context** — "UserManagement", "OrderService", "DataCRUD". Names must reflect domain responsibility, not operations. "User Management" manages users but doesn't reveal what the domain *does*. "Identity and Access" or "Member Registration" is more precise.

4. **Same concept, same model across contexts** — if two contexts use "Customer" and mean exactly the same thing with the same fields and lifecycle, they may need to merge or explicitly share a Published Language. The point of separate contexts is that the *same word means something different* in each.

5. **Context map = "they call each other's APIs"** — every relationship must name the integration pattern (ACL? Shared Kernel? Conformist?). Unnamed integration = unknown coupling. Unknown coupling = invisible architecture debt.

6. **Conformist without acknowledging the power imbalance** — Conformist means "we accept their model; we have no say." Name it explicitly. If it's Conformist, the downstream team must not expend energy trying to change the upstream model — that effort is wasted.

7. **BC boundary follows org chart** — Conway's Law says the reverse: define the right BC boundaries first, then align teams to them. Org chart boundaries often reflect historical accidents, not domain language clusters.

8. **Too many Core subdomains** — a healthy product has 1–3 Core domains. More = the strategy is unfocused, or the classification is wrong (most "Core" nominations come from teams advocating for their own domain, not from strategic clarity). Push back hard.

---

## Sizing heuristics

| Element | Recommended | Source |
|---|---|---|
| BCs per product | 3–9 | Vernon DDD Distilled — fewer = monolith risk; more = over-decomposed |
| Core subdomains | 1–3 | Vernon — Core = competitive advantage; more = unfocused strategy |
| Supporting subdomains | 2–5 | Vernon |
| Generic subdomains | 2–5 | Vernon — prime buy/outsource candidates |
| Context map relationships per BC | 1–4 | Practitioner — more = too many integrations, high coordination cost |
| Aggregates per BC (preview) | 3–7 | Vernon aggregate design rules |

If a BC has >4 integration relationships, examine whether it is playing the role of a hub/orchestrator that belongs in a Supporting subdomain (or is actually two BCs that were merged incorrectly).

---

## Finding the right folder

**Default:** `docs/domain/`

**Always check for an existing folder first:**

```bash
find docs -type d -iname "*bounded*" -o -type d -iname "*context*" 2>/dev/null
```

If a folder exists at a non-default location, use it — don't move existing work without an explicit user request. If multiple candidates exist, ask.

**Never overwrite an existing file.** Switch modes if files exist:
- Scaffold → skip (report what's there).
- Discover → update catalogue only; preserve existing BC definitions.
- Fill → append/update BC definition sections; preserve existing content.
- Refresh → targeted updates + changelog entry.

---

## Cross-reference — the architecture-artefact lifecycle

| Artefact | Relationship |
|---|---|
| **Capability Map (C-N.M)** | Primary input — capabilities → BC candidates; strategic importance → subdomain type classification |
| **Personas (P-NN)** | Personas ground the ubiquitous language scope per context — different personas may live in different contexts |
| **Value Streams (VS-N.M)** | Stage boundaries signal context boundaries — a handoff between VS stages often coincides with a context boundary |
| **domain-glossary (GT-NN)** | Each BC scopes one section of the domain glossary — the same word defined differently in BC-01 vs BC-02 is the glossary's core responsibility |
| **domain-model (AGG-NN etc)** | Each BC owns one domain model — aggregates, entities, and value objects in the domain model belong inside their BC boundary |
| **ADRs (ADR-NNNN)** | Context map decisions → ADRs; capture the rationale for each non-obvious pattern choice (why ACL instead of Conformist? why Shared Kernel?) |
| **PRDs (PRD-NNNN)** | PRDs reference BC-NN to scope their feature delivery — a PRD is always scoped to one (or at most two) bounded contexts |

### Soft-reference principle

The bounded context map references other artefacts as pointers, not dependencies. It should stand alone even if the capability map or personas don't yet exist — use `_TODO_` placeholders for C-N.M and P-NN links.

When linking, use ID + name + relative path: `[BC-02 Order Fulfilment](02b-bounded-contexts.md#bc-02)` so future renames don't break the link.

---

## Reference materials

Three files in `references/` carry the canonical content. Read when needed:

- **`references/template.md`** — the canonical `02b-bounded-contexts.md` + `02b-context-map.md` skeletons. Copy to the target folder and fill placeholders.
- **`references/methodology-references.md`** — the canonical bibliography (Evans, Vernon, Nick Tune, Conway, Team Topologies, Brandolini). **Lives only in the kit** — never copied to projects. Project docs link here via the 2-line methodology pointer in their header.
- **`references/discipline.md`** — internal Claude guidance: integration pattern decision tree, subdomain classification guide, BC naming test, quality checks. Never copied into the project.

---

## Closing report to the user

After running any mode, summarise in 5–7 lines:

1. **Mode executed** + **files created or updated** with paths.
2. **BC count by subdomain type** — N Core / N Supporting / N Generic.
3. **Context map** — number of relationships mapped; integration patterns used.
4. **Capability coverage** — every capability C-N.M assigned to a BC; any unassigned flagged.
5. **Discipline checks passed** — no god context, Core count 1–3, all relationships named, no CRUD/tech BC names.
6. **Next steps** — domain-glossary (scope ubiquitous language per BC), domain-model (define aggregates per BC), ADRs for non-obvious pattern choices.

Keep it short. Point the user at the next move.

---

## Checklist

Before declaring the work done:

- [ ] Folder identified or created (with user confirmation if new).
- [ ] `02b-bounded-contexts.md` exists.
- [ ] `02b-context-map.md` exists.
- [ ] Methodology pointer in `02b-bounded-contexts.md` header links to the kit's canonical bibliography (NOT a local methodology-references.md).
- [ ] Every capability C-N.M assigned to exactly one BC — no unassigned, no double-assigned.
- [ ] Every BC has: subdomain type (Core / Supporting / Generic) + one-sentence rationale.
- [ ] No BC has a technology name or CRUD operation name.
- [ ] Core subdomain count: 1–3.
- [ ] `02b-context-map.md` names the integration pattern for every relationship — no anonymous "they call each other".
- [ ] Every ACL relationship has a translation layer description.
- [ ] Conway's Law alignment noted (team boundary recommendation per BC).
- [ ] Mermaid flowchart renders without parse errors (see diagramming-mermaid rule).
- [ ] No project-specific terms baked into anything reusable in the kit version.
- [ ] Open every generated file with the standard artefact frontmatter (OKF-superset block — set `type` to this artefact's `okf_type` display name from the `metamodel` skill's `references/artefact-types-registry.yaml`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`). Run `git config user.name` for `owner`. Set `status: draft` on initial scaffold. Default `review_interval: 180d`. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`.
- [ ] Closing report delivered.
