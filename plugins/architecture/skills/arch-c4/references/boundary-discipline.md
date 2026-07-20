# Boundary discipline: BBV vs domain-model vs runtime view

The single most common failure mode when writing C4 / arc42 artefacts: **re-stating the domain model inside the Building Block View, or describing aggregate state machines inside the Runtime View**. This file is the authoritative rule set that keeps the three views distinct.

When the user (or future-you) is about to write content into a BBV component card or a runtime scenario, apply the three tests below.

---

## The three views — vocabulary, scope, intent

| View | Owns | Vocabulary | Scope | Skill |
|---|---|---|---|---|
| **Domain model** (Step 7b) | Aggregates, entities, value objects, invariants, per-aggregate lifecycle state machine, commands accepted, events emitted | `BC-NN.AGG-NN`, `BC-NN.ENT-NN`, `BC-NN.VO-NN`, `BC-NN.EVT-NN`, command names | One bounded context, business-conceptual | `domain-model` |
| **Building Block View** (arc42 §5) | Containers (deployable runtime units), components (code modules within a container), static "uses" relationships | `SYS-NN`, `CON-NN`, `CMP-NN` | Whole system, technical decomposition | `arch-c4` (this skill) |
| **Runtime View** (arc42 §6) | Architecturally-relevant scenarios that **span multiple containers or aggregates** | `RV-NN`, referencing `CON-NN` / `CMP-NN` / `BC-NN.EVT-NN` / commands | Cross-component, end-to-end | `arch-runtime-view` (Milestone 2) |

---

## Test 1 — Static or dynamic?

> "If it's structure → §5 (BBV) or domain-model. If it's 'step 1 happens, then step 2' → §6 (runtime view)."

The Building Block View is **structural**: it shows what exists and what depends on what. There are no temporal sequences in §5. If you find yourself writing "first the controller receives the request, then the service validates …" — that's a runtime scenario, not a BBV component description.

Component cards in §5 should describe **responsibility** (what the component is for) and **dependencies** (what it talks to), not **behaviour over time**.

---

## Test 2 — Inside one aggregate or across multiple?

> "If a state machine fits inside one aggregate's lifecycle → `domain-model`. If the scenario crosses aggregates / containers / BCs → `arch-runtime-view`."

The `Claim` aggregate's lifecycle (`submitted → triaged → assessed → approved/rejected → paid`) belongs in `docs/domain/07b-models/claims.md`. **It must not be re-stated** in §5 or §6.

What §6 captures is *cross-aggregate* choreography: "Customer submits claim → claims-service emits `ClaimSubmitted` → notification-service sends email → audit-service appends to ledger". This scenario touches three containers and references the `BC-01.EVT-01 ClaimSubmitted` event from the domain model — but it does **not** describe the Claim aggregate's internal state machine.

---

## Test 3 — Business-conceptual or technical?

> "If it speaks the ubiquitous language only → `domain-model`. If it names Spring Boot / Postgres / Kafka / Kubernetes → §5 or §7 (deployment)."

The `Claim` aggregate's invariants are business rules: "A claim cannot be approved before triage." That's domain-model wording.

A BBV component card might say "Claim Command Handler — Fastify route that translates HTTP `POST /claims` into a `SubmitClaim` command on the Claim aggregate." That sentence is BBV: it names HTTP / Fastify (tech) and the command (cross-reference to domain). It does **not** restate the invariant.

---

## Concrete examples — right vs wrong

### Example 1 — A BBV component card

❌ **Wrong (re-stating the domain model):**

> **CMP-03 Claim Command Handler**
> Handles claim commands. The `Claim` aggregate has the invariant that a claim cannot be approved before triage. The aggregate transitions through states: submitted → triaged → assessed → approved/rejected → paid. Commands accepted: SubmitClaim, ApproveClaim, RejectClaim.

❌ Why it's wrong: invariants and lifecycle belong to `docs/domain/07b-models/claims.md`. The BBV card duplicates them (which means they'll drift the moment the domain model evolves).

✅ **Right (component responsibility + back-reference):**

> **CMP-03 Claim Command Handler**
> Technology: Fastify route + TypeScript command bus
> Purpose: Translates inbound HTTP claim commands into `Claim` aggregate operations.
> Domain aggregates implemented: BC-01.AGG-02 Claim
> Dependencies: CMP-04 Claim Aggregate Repository

✅ Why it's right: states the technical role + dependencies + the back-reference to the aggregate. Anyone wanting the invariants follows the link.

### Example 2 — A runtime scenario (arc42 §6)

❌ **Wrong (state-machine-only scenario):**

> **RV-01 Claim approval state transitions**
> The Claim aggregate transitions from `triaged` to `assessed` when ClaimAssessed is emitted, and from `assessed` to `approved` when ClaimApproved is emitted.

❌ Why it's wrong: this is the aggregate's internal lifecycle. It belongs to the domain model section's "Lifecycle" subsection. A runtime view that adds no cross-component information adds no value.

✅ **Right (cross-component choreography):**

> **RV-01 — Customer submits a claim, payment authorisation initiated**
> 1. P-02 Customer submits claim via CON-01 Customer Portal.
> 2. CON-01 calls CON-02 Claims API (POST /claims).
> 3. CON-02 invokes CMP-03 Claim Command Handler → CMP-04 Claim Aggregate Repository persists the aggregate (BC-01.AGG-02 Claim).
> 4. CON-02 publishes BC-01.EVT-01 ClaimSubmitted to CON-04 Event Bus.
> 5. CON-05 Notification Service consumes ClaimSubmitted and emails the customer.
> 6. CON-06 Payment Auth Service initiates pre-authorisation via SYS-02 Payment Gateway.

✅ Why it's right: every step names a participant (CON / CMP / SYS / BC); the scenario crosses three containers and an external system; nothing about the Claim aggregate's invariants is restated.

---

## The mandatory back-reference field

Every C4 Component card in arc42 §5 carries a **`Domain aggregates implemented`** column listing `BC-NN.AGG-NN` IDs. This is the structural link from BBV → domain model. The kit's audit (Check 7 in the `metamodel` skill's Audit mode) will surface CMP-NN rows missing this column.

The DSL field is `properties.implements`. Two valid forms:

| Value | Meaning |
|---|---|
| `"BC-NN.AGG-NN"` (or comma-separated list) | The component implements one or more domain aggregates |
| `"none"` | The component genuinely has no domain mapping — HTTP framework wrappers, generic middleware, observability hooks |

**Empty string `""` is NOT valid** — Structurizr DSL rejects empty property values at validation time. Always use the `"none"` sentinel for tech-only components so the absence is explicit (a quick `grep -c '"implements" "none"'` audit surfaces all tech-only components for review).

In the arc42 §5 markdown table, render `"none"` as an em-dash (`—`) in the `Domain aggregates implemented` column.

---

## Optional forward-reference from domain-model

`domain-model` aggregates may carry a **`Realised by:`** field pointing back at `CMP-NN (in CON-NN)`. This is **optional** — filled by `arch-c4` once components exist; safe to leave empty before then. The forward reference is a convenience for navigation; the canonical mapping is in BBV §5.

---

## Three-second test before writing

Before writing any sentence into a BBV component card or a runtime scenario, ask:

> "If a reader wants the business rule / invariant / lifecycle for this concept, which file should they open?"

If the honest answer is `docs/domain/07b-models/<bc>.md`, **then write a back-reference, not a re-statement.**

---

## Sources

- arc42 v9.0 §5 (Building Block View — *static* decomposition)
- arc42 v9.0 §6 (Runtime View — *scenarios* with the criterion "architectural relevance, not exhaustive coverage")
- Evans, *Domain-Driven Design* (2003), Chapter 5 — Aggregates as consistency boundaries
- C4 model — [c4model.com](https://c4model.com) — explicit on what C4 covers and doesn't
