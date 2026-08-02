---
name: domain-model
license: MIT
description: "Create a tactical DDD domain model per bounded context — entities (identity + lifecycle + behaviour), value objects (immutable, equality by value), aggregates (consistency boundary + invariants + root), and domain events (past-tense business facts). Synthesises Evans Domain-Driven Design (2003) Chapters 5–8 + Vernon Implementing DDD (2013) Chapters 5–6 + Vernon DDD Distilled (2016) Chapter 5 + Fowler anemic domain model anti-pattern. Use when asked to define the domain model, document entities and aggregates, define domain events, model the business objects, or implement tactical DDD. Triggers on: domain model, aggregate, entity, value object, domain event, tactical DDD, aggregate root, invariants, domain objects, DDD model, entity model, bounded context model. Output: docs/domain/07b-models/{bc-slug}.md (one file per bounded context). Reads BC-NN from domain-bounded-context; reads GT-NN from domain-glossary; reads C-N.M.FXX from FBS."
user-invocable: true
metadata:
  category: "domain"
  complexity: "high"
  version: "1.0.0"
  status: active
  last_reviewed: 2026-05-29
  impact: "low"
---

# Domain Model Builder

Expert at producing tactical DDD domain models — the technical expression of the ubiquitous language as entities, aggregates, value objects, and domain events. Output is `docs/domain/07b-models/{bc-slug}.md`, one file per bounded context. NOT a database schema (the model shapes the schema, not the reverse), NOT a class diagram for implementation (that lives in code), NOT an ERD — it is the **conceptual model of business objects** with identity, behaviour, consistency rules, and the events they produce when their state changes.

> "The basic symptom of an Anemic Domain Model is that at first blush it looks like the real thing. There are objects, many named after the nouns in the domain space, and these objects are connected with the rich relationships and structure that true domain models have. The catch comes when you look at the behaviour, and you realize that there is hardly any behaviour on these objects, making them little more than bags of getters and setters." — Martin Fowler, *Anemic Domain Model* (2003)

This skill enforces the **rich model**. Every entity must have documented behaviour. Every aggregate must have documented invariants. Every domain event must be past-tense and business-meaningful.

---

## What a good domain model means

| Quality check | Pass condition |
|---|---|
| Every aggregate has exactly one root | Root entity named; no aggregate has zero or two roots |
| Aggregates have documented invariants | ≥2 invariants per aggregate stated in business language |
| Entities have behaviour methods | ≥1 non-getter/setter method documented per entity |
| Value objects are immutable + equality-by-value | All VO attributes listed; equality rule stated; replace-not-mutate confirmed |
| Domain events are past tense + business-meaningful | Each event name passes the naming guide checks |
| Aggregate boundaries justified | Consistency boundary rationale present for each aggregate |
| Model names match the glossary exactly | Every entity/VO/event name maps to a GT-NN glossary term |
| Model is free of infrastructure concerns | No DB columns, no API fields, no ORM annotations |

---

## Modes

### Mode 1 — Scaffold

Create an empty `{bc-slug}.md` for a bounded context. Seed section headings and the aggregate catalogue table. Do NOT invent aggregates — leave all aggregate sections as `_TODO_` placeholders.

Steps:
1. Resolve the BC slug from the bounded-contexts.md (`docs/domain/02b-bounded-contexts.md`).
2. Create `docs/domain/07b-models/{bc-slug}.md` from the template in `references/template.md`.
3. Report: file path created, reminder to run Mode 2 (Fill) to populate.

### Mode 2 — Fill

Populate a scaffolded `docs/domain/07b-models/{bc-slug}.md` with real domain model content.

#### Step 0 — Context questions (ask verbatim; user responds with letter codes, e.g. "1A, 2B, 3C, 4A")

```
1. Which bounded context to model?
   A. [name a specific BC-NN — e.g. BC-01 Claims Processing]
   B. All bounded contexts — one {bc-slug}.md per BC in one pass

2. Discovery basis for aggregates?
   A. Event Storming output — domain events → aggregate clusters → roots
   B. FBS + process docs — functionalities + actors → candidate entities → aggregates
   C. Existing code — reverse-engineer from module/class structure
   D. Design from scratch — I will describe the domain concepts

3. Aggregate boundary philosophy?
   A. Vernon strict — start with one entity per aggregate; merge only with evidence of consistency need
   B. Consistency-first — group by what must change atomically in one transaction
   C. Use-case-first — group by what a single command touches

4. Domain event coverage?
   A. All significant state transitions (comprehensive — one event per lifecycle change)
   B. Integration events only — events that cross bounded context boundaries
   C. Scaffold catalogue — list event names now, fill payload + consumers later
```

#### Fill process (after Step 0)

1. Read `docs/domain/02b-bounded-contexts.md` for BC-NN scope + capabilities owned.
2. Read `docs/domain/02c-glossary.md` for the canonical term names — entity names MUST match GT-NN terms exactly.
3. Read `docs/product-specs/07a-fbs.md` for functionalities the BC implements — each functional group is an aggregate candidate.
3b. Read any `docs/product-specs/use-cases/uc-NN-*.md` for the BC's behaviours — each scenario step that changes state maps to a **command → domain event**; use-case scenarios are a prime driver of aggregate boundaries and event discovery (complements Event Storming).
4. Identify aggregates: apply Vernon's rules (see `references/discipline.md`). Prefer small. Start with one entity per aggregate.
5. For each aggregate: name the root, document invariants (≥2), list member entities and VOs, document the lifecycle state machine, and map commands to domain events.
6. For each entity: define identity, list domain-meaningful attributes (no infrastructure), document behaviour methods.
7. For each value object: list attributes, state equality rule, document validation invariants, confirm replace-not-mutate.
8. For each domain event: verify past tense + business meaning, document trigger, payload, consumers, and business significance.
9. Draw Mermaid classDiagram showing aggregates, entities, VOs, and relationships. (Mermaid stays the inline default. When a diagram needs richer UML grammar Mermaid lacks — composite/nested aggregate **state machines**, full class models with multiplicities + stereotypes, or crow's-foot **ER** schemas — escalate that one diagram to **`arch-uml`** (`class` / `state` / `er` mode → PlantUML → committed SVG), carrying the `BC-NN.AGG-NN` IDs into its title. The domain-model text remains the single source of truth; the diagram is a view of it.)
10. Run Mode 3 (Verify) discipline checks inline before delivering.

### Mode 3 — Verify

Run discipline checks on an existing `docs/domain/07b-models/{bc-slug}.md`. Report findings as a table.

| Check | Method |
|---|---|
| Anemic model detection | Count behaviour methods per entity; flag any entity with 0 |
| Aggregate sizing | Count entities per aggregate; flag any aggregate with >5 |
| Invariant completeness | Count invariants per aggregate; flag any with <2 |
| Event naming | Check past tense + business meaning for every EVT-NN |
| Glossary alignment | Check every entity/VO/event name against GT-NN terms |
| Infrastructure leak | Scan for DB/API/ORM terminology in model |
| Aggregate reference discipline | Check that cross-aggregate references use IDs, not object refs |

Report-only: Mode 3 produces a findings table with severity (critical / major / minor) and proposed fixes. It does NOT edit the file.

### Mode 4 — Refactor

Apply a targeted structural change to an existing domain model.

Sub-modes:
- **split**: split an aggregate that has grown too large (>5 entities or invariants that don't relate to each other)
- **merge**: merge two aggregates where the boundary has no real consistency justification
- **promote**: promote a value object to an entity when identity becomes needed (new lifecycle requirement)
- **demote**: demote an entity to a value object when it turns out to have no meaningful independent identity

Steps: identify the target element, apply the change using discipline rules, update the aggregate catalogue, update cross-references (EVT-NN payload, ENT-NN member lists), append a changelog entry, re-run Mode 3 verify.

---

## The ten anti-patterns

Sourced from Evans (2003), Vernon IDDD (2013), and Fowler (2003).

1. **Anemic domain model.** Entities with only getters/setters and no behaviour. All logic in `*Service` or `*Manager` classes. The domain objects are just data bags. Fix: move behaviour into the entities that own the data.

2. **Aggregate too large.** An aggregate that contains dozens of entities. Every command locks the entire aggregate causing contention. Fix: apply Vernon rule 2 — if you only need part of the aggregate for a given operation, the boundary is too wide.

3. **Referencing non-root entities from outside the aggregate.** External objects hold direct references to internal entities instead of the aggregate root. Bypasses the consistency boundary and allows invariant violations. Fix: all external references must go through the aggregate root.

4. **Infrastructure in the domain model.** Database column names, API field names, ORM annotations, or HTTP status codes in the domain model. The model must be pure business concepts. Fix: move persistence mapping to the infrastructure layer.

5. **Value object treated as entity.** A concept that has no meaningful identity (Money, Address, DateRange, Percentage) given a database ID and an identity lifecycle. Fix: make it a value object — immutable, equality by attributes, replaced not mutated.

6. **Entity treated as value object.** A concept with meaningful identity and lifecycle (Order, Claim, Customer) embedded as attributes or modelled as a type. Fix: give it an entity with its own identity and lifecycle.

7. **Domain event in present tense.** `CreateOrder` is a command. `OrderCreated` is a domain event. Events are facts — things that already happened. Past tense always. Fix: rename to past tense.

8. **Domain event with no business meaning.** `StatusUpdated` — updated to what? Why? By whom? Domain events must carry business significance: `OrderShipped`, `PaymentFailed`, `ClaimApproved`. Fix: rename to convey the business fact.

9. **Aggregate invariant not documented.** If you cannot state what must always be true after every command, you do not have an aggregate — you have a data container. Fix: write ≥2 invariants in business language before finalising the aggregate boundary.

10. **Model names diverge from glossary.** If the entity is called `Account` but the glossary says `Customer`, the ubiquitous language has failed. Model names ARE glossary terms. Fix: align entity/VO/event names to GT-NN terms exactly.

---

## Sizing heuristics

| Element | Recommended range | Source |
|---|---|---|
| Aggregates per bounded context | 3–7 | Vernon *DDD Distilled* — fewer = too coarse; more = too granular |
| Entities per aggregate | 1–5 | Vernon — keep aggregates small; flag >5 for review |
| Value objects per aggregate | 2–8 | Practitioner consensus |
| Domain events per aggregate | 1–5 | One per significant state transition |
| Invariants per aggregate | 2–6 | Fewer = boundary has no purpose; more = consider splitting |
| Attributes per entity | 4–12 | Domain-meaningful only; no infrastructure attributes |

---

## Finding the right folder

Default output path: `docs/domain/07b-models/{bc-slug}.md`

- `{bc-slug}` = kebab-case BC name from `docs/domain/02b-bounded-contexts.md` (e.g. `claims-processing`, `policy-management`)
- One file per bounded context
- If the bounded context folder does not yet exist, create it

Discover existing models:
```bash
find docs/domain/07b-models -name "*.md" 2>/dev/null
```

Overwrite rules:
- **Scaffold**: skip if `docs/domain/07b-models/{bc-slug}.md` already exists; warn and offer Mode 2 instead
- **Fill**: update specific aggregate/entity/VO/event sections; do not erase sections that are already filled
- **Verify**: report-only; never edit the file
- **Refactor**: targeted edits only; always append a changelog entry

---

## Cross-reference — the architecture-artefact lifecycle

| Artefact | Relationship to this model |
|---|---|
| `domain-bounded-context` (BC-NN) | Provides the namespace and scope for this model; every aggregate lives inside one BC |
| `domain-glossary` (BC-NN.GT-NN) | All entity, VO, aggregate, and event names MUST match GT-NN terms exactly |
| FBS (C-N.M.FXX) | FBS functionalities → candidate entities and aggregates; each functional group maps to an aggregate candidate |
| Value Streams (VS-N.M) | VS stage transitions → candidate domain events; each handoff is a potential `{Noun}{PastVerb}` event |
| Business Processes | Process activities and decisions → aggregate invariants and command preconditions |
| ADRs (ADR-NNNN) | Aggregate boundary decisions, event sourcing decisions, and CQRS choices → Architecture Decision Records |
| PRDs (PRD-NNNN) | PRDs should reference BC-NN.AGG-NN and BC-NN.EVT-NN in acceptance criteria |
| Implementation Plans | Increments should be scoped per aggregate or per bounded context — not per entity |
| C4 Building Block View (CMP-NN) | Each aggregate MAY carry an optional `Realised by: CMP-NN (in CON-NN)` field pointing at the C4 Component(s) that implement it. The field is filled by `arch-c4 component` once components exist; safe to leave empty before then. The canonical back-reference is the BBV's `Domain aggregates implemented` column (`properties.implements` in the DSL) — this field on the aggregate side is a convenience for navigation, not a structural foreign key. |

---

## Reference materials

- `references/template.md` — canonical `{bc-slug}.md` skeleton (output at `docs/domain/07b-models/{bc-slug}.md`)
- `references/methodology-references.md` — Evans, Vernon, Fowler, Brandolini bibliography with specific chapters and rules
- `references/discipline.md` — aggregate design rules, invariant writing guide, event naming guide, anemic model detection patterns

---

## Closing report

After each mode, deliver a report covering:

- Mode executed + bounded context modelled
- Aggregates defined (count + names + AGG-NN IDs)
- Entities + value objects + domain events (counts)
- Discipline checks: passed / failed (list failures)
- Anti-patterns detected (list which ones, which elements)
- Next steps: PRDs should now reference AGG-NN and EVT-NN in acceptance criteria; consider ADRs for boundary decisions made

---

## Checklist

- [ ] `docs/domain/07b-models/` folder exists
- [ ] `docs/domain/07b-models/{bc-slug}.md` exists for the target BC
- [ ] Aggregate catalogue table is populated (AGG-NN IDs assigned)
- [ ] Every aggregate has exactly one named root + ≥2 documented invariants
- [ ] Every aggregate has a consistency boundary rationale
- [ ] All entity names match GT-NN glossary terms exactly
- [ ] No anemic entities — every entity has ≥1 behaviour method documented
- [ ] All value objects are immutable with equality rule stated
- [ ] All domain events are past tense + carry business significance + have payload documented
- [ ] Cross-aggregate references use IDs only (not object references)
- [ ] Mermaid classDiagram present and renders correctly
- [ ] Sizing heuristics checked (aggregates 3–7 per BC, entities 1–5 per aggregate)
- [ ] Open every generated file with the standard artefact frontmatter (OKF-superset block — set `type` to this artefact's `okf_type` display name from the `metamodel` skill's `references/artefact-types-registry.yaml`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`). Run `git config user.name` for `owner`. Set `status: draft` on initial scaffold. Default `review_interval: 180d`. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`.
- [ ] Closing report delivered
