---
type: skill
name: arch-service-contract
description: "Define the external interface contract for a bounded context or a product-level API — REST resources, async events published, and commands consumed. BC-scoped (one artefact per BC-NN, ID: BC-NN.CTR-NN) or product-level spanning multiple BCs (ID: CTR-NN). Placed after the domain model (Step 7c). Derives contracts from BC-NN.AGG-NN, BC-NN.ENT-NN, BC-NN.EVT-NN. Modes: scaffold, contract-first (design from domain model outward), document-existing (reverse-engineer from code), refresh (detect drift + emit deprecation notices). Use when asked to define an API, design the interface surface, document HTTP endpoints, define event schemas, or formalise the public contract of a service. Triggers on: API design, REST API, interface contract, endpoint design, event schema, async surface, public API, service contract, HTTP API, interface surface, API surface. Output: docs/architecture/interfaces/{bc-slug}.md (BC-scoped) or docs/architecture/interfaces/{slug}.md (product-level)."
version: "1.0.0"
status: draft
last_reviewed: 2026-05-25
review_interval: 180d
supersedes: ~
superseded_by: ~
user-invocable: true
allow_implicit_invocation: true
impact: "low"
metadata:
  category: "architecture"
  complexity: "high"
---

# Interface Contract Builder — Service Contract

You are an expert at producing **stable, versioned interface contracts** — the artefacts that answer: *"what can consumers depend on when interacting with this bounded context from the outside?"*

The artefact produced by this skill is one Markdown document per bounded context:

`docs/architecture/interfaces/{bc-slug}.md` — the complete external surface of BC-NN: synchronous (REST / gRPC / SDK) + asynchronous (events published, commands consumed), error contract, versioning policy, and security surface.

This is **not an implementation guide**. It is the **stable external contract** — the boundary between the world inside BC-NN and everything outside it. Infrastructure technology (Express, FastAPI, Kafka, RabbitMQ) is irrelevant here; only the observable surface matters.

> "With a sufficient number of users of an API, it does not matter what you promise in the contract: all observable behaviors of your system will be depended on by somebody."
> — **Hyrum's Law** (Titus Winters, *Software Engineering at Google*, 2020)

This law is the primary reason interface contracts must be intentional, explicit, and versioned from day one. Every field you add, every status code you return, every event you publish is a commitment. Design the surface as if you cannot take it back — because for a sufficiently large consumer base, you cannot.

---

## What a good interface contract means

| Quality check | Pass condition |
|---|---|
| Every resource / operation / event has a `BC-NN.CTR-NN` ID | No anonymous surface elements |
| Every sync resource maps to a domain model concept | No endpoint exists without a `BC-NN.AGG-NN`, `BC-NN.ENT-NN`, or `BC-NN.EVT-NN` backing it |
| Every async event maps to a domain event `BC-NN.EVT-NN` | Events are not invented at the integration layer; they come from the domain model |
| Error contract is unified across all operations | Single RFC 7807 error schema; no per-endpoint snowflake errors |
| Versioning policy is explicit | Breaking change definition documented; deprecation timeline stated |
| Security surface is explicit | Auth mechanism named; every CTR-NN entry states its auth requirement |
| All resources use stable opaque identifiers | UUIDs, not sequential integers; never array positions |
| No implementation details visible | No database column names, no internal service names, no ORM artefacts in the contract |
| Collections have a pagination envelope | Cursor-based by default; even if the initial page size covers all data |
| Async events carry CloudEvents 1.0.3 envelope fields | `specversion`, `id`, `source`, `type`, `time`, `datacontenttype`, `data` |

---

## The four modes

Detect from the user's prompt. Ask if ambiguous.

### Mode 1 — Scaffold

**When:** the project has no `docs/architecture/interfaces/{bc-slug}.md` yet.

**Steps:**
1. Resolve the BC slug from `docs/domain/02b-bounded-contexts.md`. Use the kebab-case BC name.
2. Run `find docs/architecture/interfaces/ -name "*.md" 2>/dev/null` to check for existing artefacts.
3. Create `docs/architecture/interfaces/` if it does not exist.
4. Copy the template from `references/template.md`. Substitute `{{bc-slug}}`, `{{bc-name}}`, `{{BC-NN}}`, `{{today}}` placeholders. Run `git config user.name` for `owner`.
5. Do NOT invent endpoints or events in scaffold mode. Leave §1 and §2 as `_TODO_` skeletons.
6. Report: file path created; next step is Mode 2 (contract-first) or Mode 3 (document-existing).

### Mode 2 — Contract-first

**When:** the domain model exists; the user wants to design the external surface from domain concepts outward before writing code.

#### Step 0 — Clarifying questions (one message; user responds e.g. "1A, 2A, 3C, 4A, 5C")

```
1. API scope?
   A. BC-scoped: this API is the direct external surface of one bounded context.
      ID format: BC-NN.CTR-NN — recommended for microservices and per-service APIs
   B. Product-level: this API spans or aggregates multiple BCs (BFF, API gateway, GraphQL schema).
      ID format: CTR-NN — BC-NN column in each resource entry documents which BC it delegates to

2. Which bounded context(s)?
   A. [Specific BC-NN — confirm from docs/domain/02b-bounded-contexts.md]
   B. All bounded contexts — one pass per BC
   C. Not applicable — product-level API (answer 1B)

3. Sync surface protocol?
   A. REST, Richardson Maturity Level 2 (resources + correct HTTP verbs) — recommended default
   B. REST + HATEOAS Level 3 (hypermedia _links drive state transitions)
   C. SDK / library interface (public methods + types; no HTTP)
   D. gRPC (derive service definitions from domain operations)
   E. No sync surface — async events only

4. Async surface?
   A. Publish domain events only (BC-NN.EVT-NN → external consumers)
   B. Publish events + consume commands from external producers
   C. No async surface — synchronous only

5. Versioning strategy?
   A. URL path versioning (/v1/, /v2/) — explicit, easy to route and test
   B. Accept header versioning (Accept: application/vnd.api+json;version=2) — clean URLs, harder to test in browser
   C. Additive-only — no explicit version until a breaking change forces a major version bump
```

#### Contract-first process

1. **Read the domain model** — `docs/domain/07b-models/{bc-slug}.md`. Identify:
   - Aggregates (`BC-NN.AGG-NN`) → top-level REST resource candidates (one aggregate root = one plural-noun collection)
   - Entities (`BC-NN.ENT-NN`) → sub-resource or nested resource candidates
   - Value Objects → request/response field types (no independent URL; embedded in resource representations)
   - Domain Events (`BC-NN.EVT-NN`) → async event candidates

2. **Map aggregates to REST resources** using the naming and hierarchy rules in `references/discipline.md §REST resource design`:
   - Aggregate root → `GET|POST /v1/{plural-noun}` + `GET|PATCH|DELETE /v1/{plural-noun}/{id}`
   - Child entity within aggregate boundary → `/v1/{root-plural}/{rootId}/{child-plural}`
   - Do not expose sub-resource URLs for value objects — they are embedded fields, not addressable resources

3. **Map domain operations to HTTP methods** per `references/discipline.md §HTTP method semantics`:
   - Create → `POST /v1/{resources}` (server assigns UUID; returns 201 + `Location`)
   - Read → `GET /v1/{resources}/{id}` (safe + idempotent)
   - Full replace → `PUT /v1/{resources}/{id}` (idempotent; rare — only when the business operation truly replaces the whole resource)
   - Partial mutation → `PATCH /v1/{resources}/{id}` (JSON Merge Patch, RFC 7396)
   - Remove → `DELETE /v1/{resources}/{id}` (idempotent)
   - Domain command without clean CRUD mapping → `POST /v1/{resources}/{id}/actions/{verb}` (e.g., `approve`, `cancel`, `publish`)

4. **Map domain events to async entries**. Every `BC-NN.EVT-NN` that is meaningful to external consumers becomes an `CTR-NN` async entry. Event naming: identical to the domain event name (past tense, business-meaningful). Do not invent integration-layer event names.

5. **Design the error contract** using RFC 7807 Problem Details format (see `references/discipline.md §Error contract`). One shared schema for all operations.

6. **Define the versioning policy** per the user's choice from Step 0.

7. **Draft the security surface** — auth mechanism, scopes or roles per operation, rate limits.

8. **Assign CTR-NN IDs** — format depends on scope (Step 0 question 1):
   - **BC-scoped (1A):** `BC-NN.CTR-01`, `BC-NN.CTR-02`, … — monotonically increasing within the BC. Each ID is owned by one BC.
   - **Product-level (1B):** `CTR-01`, `CTR-02`, … — monotonically increasing across the product. Add a `Delegates to` field per resource entry naming the `BC-NN` that owns the underlying domain model.
   Zero-pad to two digits. One ID per discrete surface element (one per resource, one per event type, one per command subscription).

9. Write `docs/architecture/interfaces/{bc-slug}.md` using `references/template.md`.

10. Run quality checks from `references/discipline.md §Quality checks` before delivering.

### Mode 3 — Document-existing

**When:** code or an API already exists; the user wants to formalise the implicit interface as a documented artefact.

**Steps:**
1. Ask for: existing route file paths, OpenAPI spec (if any), or a cURL / Postman collection.
2. Scan the provided material for route definitions, event publish calls, and event subscription handlers.
3. For each discovered element, find the matching `BC-NN.AGG-NN`, `BC-NN.ENT-NN`, or `BC-NN.EVT-NN`. Flag surface elements with no domain model backing — these are candidates for removal, or for a new domain model entry.
4. Flag discipline violations: verb in path, inconsistent error shapes, missing status codes, undocumented auth, collection endpoints without pagination. File each directly to the central ledger via `util-open-items`.
5. Produce the artefact using `references/template.md`. Mark documented items `status: documented`; items needing review `status: review`.
6. Emit a **drift report**: surface elements found in code but absent from the domain model; domain model concepts not yet surfaced in any API or event.

### Mode 4 — Refresh

**When:** a contract exists; the system has evolved and the document may have drifted from the codebase or the domain model.

**Steps:**
1. Re-read `docs/architecture/interfaces/{bc-slug}.md` and `docs/domain/07b-models/{bc-slug}.md`.
2. **Detect additions** — new aggregates or events in the domain model without a corresponding CTR-NN entry.
3. **Detect removals** — CTR-NN entries referencing aggregates or events that no longer exist. Flag as deprecation candidates (do not delete without a deprecation period — see §4 Versioning).
4. **Detect renames** — domain model terms renamed; check CTR-NN resource and event names for drift.
5. **Detect breaking changes** — any removal or mutation of an existing CTR-NN element. Classify per `references/discipline.md §Breaking change classification`. Produce a deprecation entry for each breaking change.
6. Write targeted updates only: add new CTR-NN entries, mark deprecated entries, append a `## Changelog` row. Do NOT rewrite the entire document.

---

## The eight anti-patterns

1. **Leaking domain internals.** Aggregate IDs used as URL segments, database column names in query params, internal state machine enum values exposed as response fields. The external surface must be a deliberate translation, not a database view. The test: if you changed the ORM or the database schema, would the contract change? If yes, implementation detail is leaking.

2. **Verb in the path.** `/getOrder`, `/createUser`, `/deleteItem`. REST uses nouns as resources; the HTTP method *is* the verb. Use `DELETE /orders/{id}`, not `POST /orders/{id}/delete`. The only valid exception: domain commands with no clean resource mapping → `POST /orders/{id}/actions/approve`.

3. **Undifferentiated error responses.** Every error returns `{ "error": "something went wrong" }` with status 200 or always 500. Clients cannot programmatically distinguish a 404 from a validation error from a rate limit. Use RFC 7807 Problem Details with distinct stable `type` URIs and `code` values per error class.

4. **Pagination absent or deferred.** Any collection endpoint that returns more than a handful of items will eventually need pagination. Adding it later breaks the response shape (breaking change). Design the collection envelope in from version 1 — even if the implementation initially returns everything in one page, the `pagination` wrapper must be present so future pagination is non-breaking.

5. **Anonymous events.** Events named `data_changed`, `entity_updated`, `state_modified`. Event names must be identical to their domain event: past tense, business-meaningful, unambiguous. `OrderShipped` not `OrderStatusChanged`. `PaymentFailed` not `PaymentEvent`.

6. **Undocumented breaking change.** Removing a field, changing a type, renaming a path segment, changing a status code for an existing scenario — all breaking changes. Without a version bump and a 90-day deprecation window, consumers break silently. Every modification must be classified as breaking or non-breaking and documented in the changelog.

7. **Authentication smuggled in.** Some operations are protected, others are not, and nothing documents which is which. Every `CTR-NN` entry must state its auth requirement explicitly. "It's obvious which endpoints need auth" is not documentation.

8. **Sync and async schemas diverge.** The async event for `OrderShipped` carries different field names than `GET /orders/{id}` for the same order. Consumers correlating events with REST responses find mismatched schemas. Field names must be consistent between sync and async representations of the same domain concept.

---

## REST resource design rules (summary)

Full decision rules in `references/discipline.md §REST resource design`.

| Rule | Correct | Wrong |
|---|---|---|
| Plural nouns for collections | `/orders` | `/order`, `/getOrders` |
| Stable opaque ID | `/orders/{uuid}` | `/orders/{sequentialInt}`, `/orders/{index}` |
| HTTP method is the verb | `DELETE /orders/{id}` | `POST /orders/{id}/delete` |
| Hierarchy reflects aggregate ownership | `/orders/{id}/items` (item inside order) | `/items?orderId={id}` |
| Actions for domain commands | `POST /orders/{id}/actions/approve` | `PUT /orders/{id}` with `"action": "approve"` in body |
| Query params for filtering | `/orders?status=shipped&sort=created_at` | `/orders/shipped` |
| Idempotency key for POST | `Idempotency-Key: <uuid>` header | Bare POST with no replay protection |

**Richardson Maturity target:** Level 2 (correct HTTP verbs + resource-per-noun) as the minimum. Level 3 (HATEOAS `_links`) when clients need to discover state transitions dynamically.

---

## Async surface rules (summary)

Full rules in `references/discipline.md §Async event surface rules`.

- Every published event derives from a `BC-NN.EVT-NN` domain event. No events invented at the integration layer.
- Event names: identical to the domain event name — `{AggregateRoot}{PastVerb}` — `OrderShipped`, `PaymentFailed`.
- CloudEvents 1.0.3 envelope required: `specversion`, `id` (UUID v4), `source`, `type` (`com.{org}.{bc-slug}.{EventName}`), `time` (ISO 8601 UTC), `datacontenttype`, `data`.
- Events are immutable once published. Schema evolution requires a new `type` string; the old type continues publishing during a migration window (≥ 90 days).
- Consumers must implement the Tolerant Reader pattern: ignore unknown fields in `data`.

---

## Finding the right folder

**Default:** `docs/architecture/interfaces/`

Check first:
```bash
find docs/architecture -type d -iname "*interface*" -o -type d -iname "*contract*" -o -type d -iname "*api*" 2>/dev/null
```

If a folder exists at a non-default location, use it. Never move existing work without an explicit user request.

**Filename:** `{bc-slug}.md` where `{bc-slug}` is the kebab-case BC name from `docs/domain/02b-bounded-contexts.md`.

**Never overwrite without reading.** If `{bc-slug}.md` already exists:
- Scaffold → skip; report what's there; suggest Mode 4 (Refresh).
- Contract-first → update unfilled `_TODO_` sections; preserve all filled content.
- Document-existing → append; update; emit drift report.
- Refresh → targeted updates + changelog entry only.

---

## Cross-reference — the architecture-artefact lifecycle

| Artefact | Relationship |
|---|---|
| **domain-bounded-context (`BC-NN`)** | Provides namespace and scope; BC slug is the filename; BC-NN is the ID prefix |
| **domain-model (`BC-NN.AGG-NN` · `BC-NN.ENT-NN` · `BC-NN.EVT-NN`)** | Primary input — every CTR-NN entry maps to a domain model concept; no CTR-NN should exist without a domain model backing |
| **domain-glossary (`BC-NN.GT-NN`)** | Resource names and event names must match GT-NN glossary terms exactly |
| **spec-quality-attributes (`QA-XXNN`)** | `QA-PE` performance entries → SLA per CTR-NN; `QA-SE` security entries → auth requirements |
| **arch-adr (`ADR-NNNN`)** | Interface design decisions → ADRs (versioning strategy, auth mechanism, pagination style, event bus choice) |
| **spec-prd (`PRD-NNNN`)** | PRDs reference `BC-NN.CTR-NN` in acceptance criteria for API-facing features |
| **domain-integration-contract (`INT-NN`, Tier-2 backlog)** | Sibling artefact: `INT-NN` covers BC-to-BC *internal* wiring patterns; `CTR-NN` covers the *external public surface* consumers outside the system depend on — different scopes, no overlap |

---

## Reference materials

- **`references/template.md`** — canonical `{bc-slug}.md` skeleton; copy and fill placeholders.
- **`references/methodology-references.md`** — full bibliography: Fielding REST dissertation, RFC 9110, RFC 7807, Hyrum's Law, CloudEvents, Richardson Maturity Model, Google API Design Guide, Postel's Law, Tolerant Reader, and more. Lives only in the kit — never copied to projects.
- **`references/discipline.md`** — internal Claude guidance: REST resource naming rules, HTTP method decision table, status code catalogue, pagination decision tree, RFC 7807 error format, breaking-change classification, async event rules, security surface checklist, quality checks. Never copied to projects.

---

## Closing report

After any mode, deliver in 6–8 lines:

1. **Mode executed** + BC-NN modelled + file path created or updated.
2. **Sync surface** — number of CTR-NN resources defined; Richardson Maturity Level target.
3. **Async surface** — events published count + commands consumed count.
4. **Error contract** — RFC 7807 schema in place (yes/no).
5. **Versioning policy** — strategy chosen; breaking change definition present (yes/no).
6. **Discipline checks** — passed / failed (list failures with CTR-NN and rule violated).
7. **Anti-patterns detected** — list which ones, which CTR-NN.
8. **Next steps** — ADRs for versioning / auth / event-bus choices; PRDs should reference CTR-NN IDs in acceptance criteria; run `spec-quality-attributes` to add SLA entries per CTR-NN.

---

## Checklist

Before declaring the work done:

- [ ] `docs/architecture/interfaces/` folder exists.
- [ ] `docs/architecture/interfaces/{bc-slug}.md` exists for the target BC.
- [ ] Standard artefact frontmatter present (OKF-superset block — set `type` to this artefact's `okf_type` display name from the `metamodel` skill's `references/artefact-types-registry.yaml`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`). Run `git config user.name` for owner. Set `status: draft` on initial scaffold. Default `review_interval: 180d`. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`.
- [ ] Every CTR-NN entry maps to a `BC-NN.AGG-NN`, `BC-NN.ENT-NN`, or `BC-NN.EVT-NN`.
- [ ] No verb in REST resource paths (exception: `/actions/{verb}`).
- [ ] All collection endpoints have a pagination envelope.
- [ ] Error contract section present; single RFC 7807-compatible schema with `type` URI, `title`, `status`, `detail`.
- [ ] Versioning policy section present; breaking vs non-breaking change defined.
- [ ] Security surface section present; auth requirement stated per CTR-NN entry.
- [ ] Async events named identically to `BC-NN.EVT-NN` domain events (past tense, business-meaningful).
- [ ] CloudEvents 1.0.3 envelope fields documented for each published event.
- [ ] No implementation details in the contract (no DB column names, no ORM annotations, no internal service names).
- [ ] CTR-NN IDs assigned monotonically; zero-padded to two digits; no gaps.
- [ ] `## Changelog` section present with at least the creation entry.
- [ ] Closing report delivered.
