# Service Contract — Discipline Guide

Internal Claude guidance for the `arch-service-contract` skill. Not copied to projects.

---

## REST resource design

### Naming rules

- **Plural nouns** for resource collections: `/orders`, `/customers`, `/invoices`, `/line-items`.
- **Kebab-case** for multi-word resources: `/order-items`, `/tax-rates`. Never camelCase or snake_case in paths.
- **Domain terms from the glossary** (GT-NN): resource names must be glossary terms, not database table names. If the glossary uses "Member" but the table is `users`, the resource is `/members`.
- **No verbs in paths** (HTTP method is the verb). The only exception: `POST /{resource}/{id}/actions/{verb}` for domain commands with no clean CRUD mapping.

### Hierarchy rules

- Express **ownership** via hierarchy: `/orders/{orderId}/items` when items are members of the Order aggregate.
- Max **3 levels deep**: `/v1/{collection}/{id}/{sub-collection}`. Beyond three levels, use query params instead.
- Sub-resources for aggregate **members without independent identity** (they exist only within the parent aggregate).
- Top-level resources for **aggregates with their own identity** (they can exist without the parent in scope).
- Example decision: `Order` has `LineItems`. `LineItem` has no identity outside an order → `/orders/{id}/items`. `Order` and `Customer` are independent aggregates → `/orders` and `/customers` are both top-level.

### Identifier rules

- Always **UUID v4** (or similar opaque identifier) as the resource ID. Never expose sequential integers: they leak record counts, enable enumeration attacks, and are awkward to shard.
- IDs must be **stable**: once assigned, an ID never changes. If the resource is renamed or restructured, create a new resource type with a new ID space.
- **Never use array position** as an identifier.

### Filtering, sorting, pagination (query params only)

- Filtering: `GET /orders?status=shipped&customerId=uuid&from=2024-01-01`
- Sorting: `GET /orders?sort=created_at&order=desc` (or `sort=-created_at` for descending)
- Field selection (sparse fieldsets): `GET /orders?fields=id,status,total`
- Pagination: always query params — never in the path (`/orders/page/2` is wrong)

---

## HTTP method semantics

Per RFC 9110. **Safe** = no state change. **Idempotent** = identical result on repeated calls.

| Method | Safe | Idempotent | Primary use | Status on success | Notes |
|---|---|---|---|---|---|
| GET | yes | yes | Fetch resource or collection | 200 | Never mutate in GET |
| HEAD | yes | yes | Check existence / metadata | 200 | Same as GET, no body |
| OPTIONS | yes | yes | CORS preflight, capability discovery | 200 | Required for CORS |
| POST | no | no | Create resource; submit domain command | 201 (create) / 200 / 202 | Use `Idempotency-Key` header |
| PUT | no | yes | Full resource replacement | 200 or 204 | Rare; client owns the ID |
| PATCH | no | no | Partial resource update (JSON Merge Patch) | 200 | RFC 5789 + RFC 7396 |
| DELETE | no | yes | Remove resource | 204 or 200 | Must succeed on repeated calls |

### POST vs PUT vs PATCH decision rule

```
Creating a new resource?
  └─ Server assigns ID → POST /resources (returns 201 + Location header)
  └─ Client assigns ID → PUT /resources/{client-chosen-id} (idempotent upsert)

Modifying an existing resource?
  └─ Replacing the entire representation → PUT /resources/{id}
  └─ Changing one or more fields → PATCH /resources/{id} (JSON Merge Patch)
  └─ Executing a domain command → POST /resources/{id}/actions/{verb}
```

### Actions sub-resource pattern

Use `POST /resources/{id}/actions/{verb}` when a domain command does not map cleanly to CRUD:

```
POST /orders/{id}/actions/approve       → domain command: ApproveOrder
POST /orders/{id}/actions/cancel        → domain command: CancelOrder
POST /shipments/{id}/actions/dispatch   → domain command: DispatchShipment
```

Never: `PUT /orders/{id}` with `{ "status": "approved" }` — this buries the command intent in a field value and loses the semantics of the operation.

---

## Status code catalogue

**2xx — Success**
| Code | Name | When to use |
|---|---|---|
| 200 | OK | Successful GET, successful PATCH or DELETE with a response body |
| 201 | Created | Successful POST that created a resource; include `Location: /v1/resources/{newId}` header |
| 202 | Accepted | Async operation accepted; not yet complete; include a polling URL or `Location` for the operation status |
| 204 | No Content | Successful DELETE or PATCH with no response body needed |

**3xx — Redirection**
| Code | Name | When to use |
|---|---|---|
| 301 | Moved Permanently | Resource URL has permanently changed; include `Location` header; update callers |
| 304 | Not Modified | Conditional GET with `If-None-Match` or `If-Modified-Since`; client cache is still valid |

**4xx — Client error** (the client sent something wrong)
| Code | Name | When to use |
|---|---|---|
| 400 | Bad Request | Request is malformed — schema validation failure, invalid JSON, unparseable value |
| 401 | Unauthorized | No valid credentials provided; client must authenticate. **Not** an authorization failure |
| 403 | Forbidden | Authenticated but not authorised for this specific operation |
| 404 | Not Found | Resource does not exist at this URI. Use for non-existent IDs. Note: consider whether *existence* itself is sensitive — returning 403 instead of 404 hides the fact that a resource exists |
| 405 | Method Not Allowed | HTTP method not supported on this path; include `Allow` header listing supported methods |
| 409 | Conflict | State conflict: duplicate idempotency key, optimistic lock version mismatch, business state prevents the operation |
| 410 | Gone | Resource permanently deleted and will never return. Use instead of 404 when you want to signal "this existed and was deliberately removed" |
| 422 | Unprocessable Entity | Request is syntactically valid but fails business rule validation (e.g., "cannot approve an already-approved order") |
| 429 | Too Many Requests | Rate limit exceeded; include `Retry-After: <seconds>` or `Retry-After: <HTTP-date>` header |

**5xx — Server error** (the server failed on a valid request)
| Code | Name | When to use |
|---|---|---|
| 500 | Internal Server Error | Unexpected server fault. Do not expose stack traces, internal errors, or service names in the body |
| 502 | Bad Gateway | Upstream dependency returned an invalid or unexpected response |
| 503 | Service Unavailable | Overloaded or in maintenance; include `Retry-After` if the expected recovery time is known |
| 504 | Gateway Timeout | Upstream dependency timed out |

**Anti-patterns:**
- Never return 200 with an error body (`{ "success": false, "error": "..." }`) — HTTP status codes exist for a reason.
- Never return 500 for client errors (validation failures are 400 or 422, not 500).
- Never return 401 for authorization failure (that is 403).
- Never expose internal details in 5xx bodies (stack traces, SQL errors, hostnames).

---

## Error contract — RFC 7807 Problem Details

### Format

```json
{
  "type": "https://api.example.com/errors/validation-failed",
  "title": "Validation Failed",
  "status": 422,
  "detail": "The 'amount' field must be a positive number.",
  "instance": "/v1/payments/txn-abc123",
  "errors": [
    {
      "field": "amount",
      "code": "MUST_BE_POSITIVE",
      "message": "Amount must be greater than zero"
    }
  ]
}
```

`Content-Type: application/problem+json`

### Field rules

- `type`: a stable URI that identifies this *class* of error. Must resolve to documentation explaining when this error occurs and how to fix it. Do not use URLs that will change.
- `title`: stable, human-readable label for the error class. Same value for all occurrences. Used for programmatic matching (not `detail`).
- `status`: mirrors the HTTP response status code. Redundant but useful when the body is deserialized without the HTTP context.
- `detail`: instance-specific explanation. May vary between occurrences. Human-readable. Never parse programmatically.
- `instance`: the URI of the specific request or resource that caused the error. Enables log correlation.
- `errors` (extension): array of per-field validation errors. Each entry has `field` (JSON path or field name), `code` (UPPER_SNAKE — stable, for programmatic handling), `message` (human-readable, for display).

### Why UPPER_SNAKE for `code`?

Machine-readable codes are the stable contract for error handling logic (clients `switch` on them). UPPER_SNAKE signals "this is a constant, not a human-readable string." Error *messages* may be translated or reworded; error *codes* must not change.

---

## Pagination

### Decision: cursor-based vs offset-based

| Property | Cursor-based | Offset-based |
|---|---|---|
| Stability under concurrent writes | Yes — cursor is a pointer into a sorted index | No — items inserted/deleted shift the window |
| Arbitrary page jump | No | Yes (`?page=42`) |
| Performance | O(log n) — seek to cursor | O(n) — `OFFSET` scans + `COUNT(*)` |
| Implementation complexity | Medium (must maintain sort key in cursor) | Low |
| **Default choice** | **Recommended for most APIs** | Only when random page-number access is a product requirement |

### Cursor response envelope

```json
{
  "data": [ { "...": "resource object" } ],
  "pagination": {
    "next_cursor": "eyJpZCI6IjEyMyJ9",
    "prev_cursor": "eyJpZCI6Ijk5In0=",
    "limit": 25,
    "total": null
  }
}
```

**Rules:**
- `next_cursor` is `null` when on the last page (end of collection).
- `prev_cursor` is `null` when on the first page.
- `total` is expensive to compute (requires a full COUNT). Omit unless the product explicitly requires it. Never return `null` without documenting that `null` means "count unavailable."
- `limit` reflects the applied page size (the server's limit if the client's `?limit` exceeded the maximum).
- Cursors are opaque base64-encoded values. Clients must not parse their contents.

### Collection endpoint requirement

Every endpoint that returns an array of items — no exceptions — must return it wrapped in this envelope, even if the initial implementation always returns all items in one page. Adding the wrapper later is a breaking change.

---

## Breaking change classification

**Breaking = any change that causes a correctly-implemented consumer to fail.**

"Correctly-implemented" means: uses the Tolerant Reader pattern (ignores unknown JSON fields), does not hardcode URLs (uses documented base paths), does not switch on `detail` text (only `code` values), and does not depend on undocumented ordering.

### Non-breaking (backward compatible)

- Adding a new optional field to a response body
- Adding a new optional request query parameter
- Adding a new endpoint (new path + method combination)
- Adding a new CTR-NN entry
- Adding a new error `code` to the catalogue
- Adding a new event type (new CloudEvents `type` string)
- Adding optional fields to an event payload `data`
- Changing documentation text, `title`, or `detail` values (these are not contracts)
- Expanding the set of accepted values for a field that previously had a restrictive enum

### Breaking (requires version bump + deprecation period)

- Removing any field from a response body (even a field with no documented consumers — Hyrum's Law)
- Renaming a field in a response body
- Changing a field's type (e.g., string to integer, even if values are currently numeric strings)
- Changing a URL path segment (even a typo fix)
- Changing the HTTP method for an existing operation
- Removing an endpoint
- Changing the HTTP status code returned for an existing scenario
- Removing or renaming an error `code` value (clients switch on these)
- Removing or renaming a CloudEvents `type` string
- Removing a required field from an event payload
- Making a previously optional response field required in requests
- Changing sort order of collection results when that order was observed by consumers (Hyrum's Law)

### The Hyrum's Law corollary

Even changes that are theoretically non-breaking may be breaking in practice. If you change an observable behavior — response ordering, JSON key ordering, precision of floating-point values, whitespace in strings — treat it as a breaking change and provide a migration period.

---

## Async event surface rules

### Event naming

- Identical to the domain model `BC-NN.EVT-NN` name. No translation or renaming at the integration layer.
- Pattern: `{AggregateRoot}{PastVerb}` — `OrderShipped`, `PaymentFailed`, `CustomerRegistered`.
- Never: `order_update`, `shipment_event`, `data_changed`, `entity_modified`.
- Tip: if you cannot easily say what *specifically* happened from the event name alone, rename it.

### CloudEvents envelope — all fields

| Field | Type | Required | Value |
|---|---|---|---|
| `specversion` | string | yes | always `"1.0"` |
| `id` | string | yes | UUID v4; unique per event occurrence |
| `source` | URI | yes | `/bc-slug` — identifies the producing bounded context |
| `type` | string | yes | `com.{org}.{bc-slug}.{EventName}` in reverse-domain notation |
| `datacontenttype` | string | recommended | `"application/json"` |
| `time` | RFC 3339 | recommended | UTC timestamp of when the event *occurred* (not when it was sent) |
| `subject` | string | optional | identifier of the primary resource the event concerns (e.g., the order ID) |
| `data` | object | conditional | the domain event payload |

### Schema evolution for events

Events are immutable contracts. To change a published event schema:

1. Create a new `type` string: `com.acme.order-fulfilment.OrderShippedV2`.
2. Begin publishing both the old and new type simultaneously.
3. Notify consumers of the migration window (minimum 90 days).
4. After migration window: stop publishing the old type; remove it from the contract.
5. Never mutate the payload of an existing `type` — consumers that have cached or stored events will process them with the old schema.

---

## Security surface checklist

For every CTR-NN entry, verify and document:

- [ ] **Authentication mechanism** named: Bearer JWT / API key / mTLS / OAuth 2.0 client credentials / none
- [ ] **For JWT**: issuer URL, JWKS endpoint, and required claims documented
- [ ] **For API keys**: key rotation policy and key lifetime documented
- [ ] **For OAuth 2.0**: required scopes listed per operation
- [ ] **401 vs 403**: 401 = unauthenticated (no valid credentials); 403 = authenticated but not authorised. Do not return 401 when the user is authenticated but lacks permission.
- [ ] **Rate limits**: requests-per-window per token (or per IP for unauthenticated endpoints); `Retry-After` header behaviour documented
- [ ] **Sensitive fields**: no tokens, passwords, or PII logged; error bodies never leak internal information
- [ ] **CORS**: if applicable, allowed origins documented
- [ ] **Idempotency keys**: POST operations that should be replay-safe use `Idempotency-Key` request header

---

## Quality checks

Run these before closing any mode. Report failures as a table with: check name, CTR-NN, severity (critical / major / minor), proposed fix.

| Check | How to verify |
|---|---|
| Every CTR-NN maps to a domain concept | Cross-reference CTR-NN list against BC-NN.AGG/ENT/EVT; flag any with no domain model backing |
| No verb in REST paths (except /actions/) | Scan path segments for: get, create, update, delete, list, fetch, remove, search |
| Pagination envelope on all collection endpoints | Every GET endpoint returning an array has the `data` + `pagination` wrapper |
| Error contract is a single unified schema | Only one error format in §3; no per-endpoint custom error shapes |
| Versioning policy present with breaking change definition | §4 non-empty; breaking vs non-breaking distinction present |
| Security surface non-empty; auth stated per CTR-NN | §5 non-empty; auth column filled for every CTR-NN entry in the operations table |
| All async events map to BC-NN.EVT-NN | Cross-reference CTR-NN async list against domain model events |
| Event names are past tense and business-meaningful | Manual check: does the name state what happened? Is it past tense? |
| CloudEvents envelope fields present per event | `specversion`, `id`, `source`, `type`, `time`, `datacontenttype`, `data` |
| No implementation details in contract | Scan for: column, table, schema, controller, model, orm, database, repo, entity (ORM sense) |
| CTR-NN IDs are monotonic, zero-padded, no gaps | List all; verify consecutive; flag any skip |
| All collection responses use cursor pagination | No `?page=N&per_page=M` offset pagination unless explicitly documented as intentional |
