# Service Contract — Methodology References

Canonical bibliography for the `arch-service-contract` skill. Lives only in the kit — never copied to projects. Project docs link here via the methodology pointer in their header.

---

## REST architectural foundations

### Fielding, Roy T. (2000)
*Architectural Styles and the Design of Network-based Software Architectures*. Doctoral dissertation, University of California, Irvine.
https://ics.uci.edu/~fielding/pubs/dissertation/top.htm

The original REST specification. Defines the six architectural constraints:

1. **Client-server** — separation of UI concerns from data storage concerns.
2. **Statelessness** — each request must contain all information necessary to understand it; session state lives entirely in the client.
3. **Cacheability** — responses must declare themselves cacheable or non-cacheable.
4. **Uniform interface** — the central feature distinguishing REST. Four sub-constraints: (a) identification of resources (URI), (b) manipulation of resources through representations, (c) self-descriptive messages, (d) hypermedia as the engine of application state (HATEOAS).
5. **Layered system** — each component sees only the immediate layer it interacts with.
6. **Code-on-demand** (optional) — servers can send executable code to clients.

**Key insight for this skill:** REST is an architectural *style*, not a protocol. "RESTful" APIs that ignore statelessness or the uniform interface constraint are not RESTful in Fielding's sense. Most production APIs are "REST-like" (Level 2 Richardson Maturity); that is sufficient for this skill's purposes.

### Richardson, Leonard & Ruby, Sam (2007)
*RESTful Web Services*. O'Reilly Media.

Introduced the vocabulary of resource-oriented design and popularised the Richardson Maturity Model (later described by Martin Fowler in his 2010 blog post *"Richardson Maturity Model"* at martinfowler.com/articles/richardsonMaturityModel.html):

- **Level 0** — HTTP as a tunnel. One URI, one method (POST). SOAP-style.
- **Level 1** — Individual resources. Multiple URIs, but still only one HTTP method.
- **Level 2** — HTTP verbs. Multiple URIs + correct HTTP method semantics (GET is safe+idempotent, POST is not idempotent, DELETE is idempotent).
- **Level 3** — Hypermedia controls (HATEOAS). Responses include `_links` that drive state transitions. Clients discover capabilities at runtime rather than hardcoding URL patterns.

**Target for this skill:** Level 2 minimum. Level 3 when clients need to discover state transitions without hardcoding URLs.

---

## HTTP standards

### IETF RFC 9110 (2022) — HTTP Semantics
https://www.rfc-editor.org/rfc/rfc9110

Replaces RFC 7230–7235. The authoritative reference for HTTP method semantics, status code semantics, headers, and content negotiation.

Key sections:
- **§9 Methods** — defines safe (no state change), idempotent (same result on repeat calls), and each method's semantics.
- **§15 Status Codes** — authoritative status code definitions (use this, not informal cheat-sheets).
- **§8 Representation Data** — content negotiation, media types.
- **§9.3.4 GET** — "safe and idempotent; retrieves a representation of the target resource."
- **§9.3.3 POST** — "not safe; not idempotent; the action performed by POST is not necessarily idempotent."
- **§9.3.5 PUT** — "idempotent; replaces the state of the target resource with the request content."
- **§9.3.6 DELETE** — "idempotent; removes the association between the target resource and its current functionality."
- **§9.3.4 PATCH** (via RFC 5789) — partial modification; neither safe nor idempotent.

### IETF RFC 7807 / RFC 9457 — Problem Details for HTTP APIs
RFC 7807 (2016): https://www.rfc-editor.org/rfc/rfc7807
RFC 9457 (2023, updates RFC 7807): https://www.rfc-editor.org/rfc/rfc9457

Defines the `application/problem+json` media type for structured error responses. Without a standard format, every API invents its own; clients cannot write generic error handlers.

**Required fields:**
- `type` (URI reference) — stable identifier for the error class; must resolve to documentation.
- `title` (string) — stable, human-readable summary; same value for all occurrences of the same error class.
- `status` (integer) — mirrors the HTTP response status code.

**Recommended fields:**
- `detail` (string) — instance-specific explanation; may vary between occurrences; not for programmatic parsing.
- `instance` (URI) — the specific URI of the request or resource that caused the error.

**Extension members** — additional properties specific to the application (e.g., `errors` array for validation details). Extension members are legal and encouraged.

### IETF RFC 5789 (2010) — PATCH Method for HTTP
https://www.rfc-editor.org/rfc/rfc5789

Defines PATCH for partial resource modifications. Key distinction: PUT replaces the entire resource representation; PATCH applies a partial change described in the request body.

Companion: **RFC 7396 (JSON Merge Patch, 2014)** — the simplest PATCH format. Request body is a partial JSON object. Fields present with non-null values are updated; fields present with `null` are deleted; fields absent are unchanged.

### IETF RFC 8288 (2017) — Web Linking
https://www.rfc-editor.org/rfc/rfc8288

Defines `Link` response headers with `rel` type values. Used for HATEOAS Level 3 navigation:
```
Link: <https://api.example.com/orders?cursor=abc>; rel="next",
      <https://api.example.com/orders?cursor=xyz>; rel="prev"
```
Standard `rel` values: `next`, `prev`, `first`, `last`, `self`, `related`.

### IETF RFC 6570 (2012) — URI Templates
https://www.rfc-editor.org/rfc/rfc6570

Defines `{variable}` syntax for parameterised URI documentation. Used for documenting path templates: `/orders/{orderId}/items/{itemId}`.

---

## API design guidelines

### Google API Design Guide (2023)
https://cloud.google.com/apis/design

Resource-oriented design applied at scale. Key patterns borrowed by this skill:

- **Standard methods**: List, Get, Create, Update, Delete — maps directly to HTTP method semantics.
- **Custom methods** (`/actions/{verb}`): for operations that don't map to standard CRUD — `Cancel`, `Approve`, `Publish`, `BatchGet`.
- **Standard fields**: `name` (resource name), `parent`, `page_token`, `filter`, `order_by`, `page_size`.
- **Long-running operations**: `Operation` resource with `done: bool` and `response` / `error` fields.
- **Error model**: `google.rpc.Status` — `code` (gRPC status), `message` (human-readable), `details` (typed extension payloads).

### Microsoft REST API Guidelines (2016, ongoing)
https://github.com/microsoft/api-guidelines

Microsoft's internal REST guidelines made public. Relevant patterns:

- **Versioning via `api-version` query parameter** — `GET /orders?api-version=2024-01-01`. Date-based versions make deprecation timelines explicit.
- **Consistent error format** — `{ "error": { "code": "UPPER_SNAKE", "message": "...", "innererror": {...} } }`.
- **PATCH semantics** with JSON Merge Patch.
- **Long-running operations** with `Operation-Location` response header.
- **Delta links** — cursors for incremental sync (`@odata.deltaLink`).

### Stripe API Design (reference implementation)
https://stripe.com/docs/api

Widely cited as the benchmark for developer-experience-first REST API design. Key patterns:

- **Idempotency keys**: `Idempotency-Key: <uuid>` request header on POST operations. Server records the key and returns the same response on replay within 24 hours.
- **Event-driven webhooks**: consistent event envelope `{ "id": "evt_...", "type": "payment_intent.succeeded", "object": "event", "data": {...} }`.
- **Expansions**: `?expand[]=customer` to include related objects inline rather than requiring a second request.
- **Consistent pagination cursor**: `has_more: bool`, `data: []`, `url: string`.

---

## Stability and contract principles

### Winters, Titus; Manshreck, Tom; Wright, Hyrum (eds.) (2020)
*Software Engineering at Google: Lessons Learned from Programming over Time*. O'Reilly Media. Chapter 1.
https://abseil.io/resources/swe-book

**Hyrum's Law** (coined by Hyrum Wright): *"With a sufficient number of users of an API, it does not matter what you promise in the contract: all observable behaviors of your system will be depended on by somebody."*

Practical consequences for API design:
- Adding a field is a commitment you may never be able to remove.
- The ordering of items in a list response will be depended upon even if undocumented.
- The exact format of error messages will be parsed by someone.
- Latency characteristics become contracts for SLAs.

Design the surface as if every observable behavior is permanent.

### Postel, Jon (1981) — Robustness Principle
RFC 793, §2.10: *"Be conservative in what you do, be liberal in what you accept from others."*

**Modern qualification** (RFC 9110 §2.5, 2022): liberal acceptance of malformed input creates protocol ambiguity and security vulnerabilities. The principle is best interpreted as: be strict about what you produce (conservative output), and accept well-formed variations gracefully (not malformed input).

For API design: emit canonical, well-typed, consistently structured responses. Do not accept ambiguous or underspecified request formats that may be interpreted differently by different server versions.

### Fowler, Martin (2011) — Tolerant Reader
https://martinfowler.com/bliki/TolerantReader.html

Consumers should extract only the fields they need and ignore fields they do not recognise. This enables producers to add new optional fields in minor versions without coordinating consumer upgrades.

**The Tolerant Reader test**: if your consumer would throw an exception or fail on encountering an unknown JSON field, the consumer is too brittle. Fix the consumer, not the API.

### Preston-Werner, Tom (2013) — Semantic Versioning 2.0.0
https://semver.org

`MAJOR.MINOR.PATCH`.
- MAJOR: breaking changes (incompatible API changes).
- MINOR: new backward-compatible functionality.
- PATCH: backward-compatible bug fixes.

Applied to APIs: any change that causes a correctly-implemented consumer (one that uses the Tolerant Reader pattern) to fail is a MAJOR (breaking) change requiring a version bump.

---

## Async / event-driven surface

### CloudEvents 1.0.3 (CNCF, 2023)
https://cloudevents.io / https://github.com/cloudevents/spec

Standard envelope for event metadata, solving the problem of every event system inventing its own envelope fields.

Required attributes: `specversion` (always `"1.0"`), `id` (UUID v4; unique per occurrence), `source` (URI identifying the producer BC), `type` (reverse-domain string: `com.{org}.{bc}.{EventName}`), `datacontenttype` (`"application/json"`).

Optional but recommended: `time` (ISO 8601 UTC timestamp of event occurrence), `subject` (identifier of the resource the event concerns).

`data` carries the domain event payload; its structure is defined per `type`.

### Hohpe, Gregor & Woolf, Bobby (2003)
*Enterprise Integration Patterns: Designing, Building, and Deploying Messaging Solutions*. Addison-Wesley.
https://www.enterpriseintegrationpatterns.com

Canonical vocabulary for async messaging. Patterns relevant to the async surface contract:

- **Event Message** — notification that something happened; no reply expected. Most domain events are Event Messages.
- **Command Message** — request for a specific action; the sender expects a result.
- **Dead Letter Channel** — messages that cannot be delivered or processed go to a dead letter queue; document this in the async surface contract.
- **Idempotent Receiver** — a consumer that can safely process the same message multiple times; required when at-least-once delivery is guaranteed.

### AsyncAPI 3.0 (2023)
https://www.asyncapi.com/docs/reference/specification/v3.0.0

Machine-readable specification format for async APIs. Conceptually: channels (named logical message streams), operations (publish or subscribe), messages (schema + headers), servers (broker connection details).

This skill outputs Markdown, not AsyncAPI YAML. However, the AsyncAPI vocabulary (`channel`, `operation`, `subscribe`, `publish`, `message schema`) informs the template structure and terminology.
