---
title: "{{BC-NN}} {{bc-name}} — Interface Contract"
status: draft
owner: _TODO_
last_reviewed: {{today}}
review_interval: 180d
---

# {{BC-NN}} {{bc-name}} — Interface Contract

> **Methodology:** built using REST architectural constraints (Fielding 2000), HTTP semantics (RFC 9110), structured error format (RFC 7807 Problem Details), event envelope (CloudEvents 1.0.3), and Hyrum's Law stability principles. Full bibliography: [methodology-references.md](https://github.com/VictorHueni/homemade-claude-kit/tree/main/arch-service-contract/references/methodology-references.md).

**Scope:** the external surface of `{{BC-NN}} {{bc-name}}`. This document defines what external consumers can depend on. Internal implementation is not part of this contract. Any observable behaviour not documented here is not guaranteed.

**Companion documents:**
- Domain model: [../../domain/07b-models/{{bc-slug}}.md](../../domain/07b-models/{{bc-slug}}.md)
- Bounded contexts: [../../domain/02b-bounded-contexts.md](../../domain/02b-bounded-contexts.md)
- Domain glossary: [../../domain/02c-glossary.md](../../domain/02c-glossary.md)
- Quality attributes: [../../product-specs/09a-quality-attributes.md](../../product-specs/09a-quality-attributes.md)

---

## §0 Traceability

| Field | Value |
|---|---|
| **Bounded context** | [{{BC-NN}} {{bc-name}}](../../domain/02b-bounded-contexts.md#{{bc-slug}}) |
| **Domain model** | [{{bc-slug}}.md](../../domain/07b-models/{{bc-slug}}.md) |
| **Aggregates surfaced** | _TODO_ (`BC-NN.AGG-NN`) |
| **Domain events surfaced** | _TODO_ (`BC-NN.EVT-NN`) |
| **Quality attributes** | _TODO_ (`QA-XXNN`) |
| **ADRs** | _TODO_ (`ADR-NNNN`) |
| **Current version** | v1 |
| **Versioning strategy** | _TODO_ (URL path / Accept header / additive-only) |

---

## §1 Sync surface

*Delete this section and note "No sync surface — async only" in §0 if this BC exposes no synchronous interface.*

### Resource catalogue

| CTR-NN | Resource name | Base path | Domain concept | Status |
|---|---|---|---|---|
| {{BC-NN}}.CTR-01 | _TODO_ | `/v1/_TODO_` | [AGG-NN _TODO_](../../domain/07b-models/{{bc-slug}}.md#agg-01) | draft |

---

### {{BC-NN}}.CTR-01 · [Resource name]

**Domain concept:** [{{BC-NN}}.AGG-NN · Aggregate name](../../domain/07b-models/{{bc-slug}}.md#agg-01)
**Base path:** `/v1/{resource-plural}`
**Status:** draft

#### Operations

| Method | Path | Description | Auth required | Idempotent |
|---|---|---|---|---|
| `GET` | `/v1/{resource-plural}` | List collection (paginated) | _TODO_ | yes |
| `POST` | `/v1/{resource-plural}` | Create new resource | _TODO_ | no — use `Idempotency-Key` header |
| `GET` | `/v1/{resource-plural}/{id}` | Fetch single resource by ID | _TODO_ | yes |
| `PATCH` | `/v1/{resource-plural}/{id}` | Partial update (JSON Merge Patch) | _TODO_ | no |
| `DELETE` | `/v1/{resource-plural}/{id}` | Remove resource | _TODO_ | yes |

#### Request schema — `POST /v1/{resource-plural}`

```json
{
  "field_one": "string — _TODO_ (required)",
  "field_two": "integer — _TODO_ (optional)"
}
```

Required fields: `field_one`
Optional fields: `field_two`

#### Response schema — `200 OK` / `201 Created`

```json
{
  "id": "string — UUID v4; stable; never changes after creation",
  "field_one": "string",
  "field_two": "integer | null",
  "created_at": "string — ISO 8601 UTC",
  "updated_at": "string — ISO 8601 UTC"
}
```

#### Collection response — `GET /v1/{resource-plural}`

```json
{
  "data": [
    { "...": "resource object" }
  ],
  "pagination": {
    "next_cursor": "string | null — null means end of collection",
    "prev_cursor": "string | null — null means first page",
    "limit": 25
  }
}
```

*Pagination style: cursor-based (opaque base64 token). See `references/discipline.md §Pagination`.*

#### Error responses for this resource

| HTTP status | `code` | When |
|---|---|---|
| `400` | `VALIDATION_ERROR` | Request body fails schema validation; see `errors` array |
| `401` | `UNAUTHENTICATED` | Missing or invalid credentials |
| `403` | `FORBIDDEN` | Authenticated but not authorised for this operation |
| `404` | `NOT_FOUND` | Resource ID does not exist |
| `409` | `CONFLICT` | State conflict — see `detail` for specifics |
| `422` | `UNPROCESSABLE` | Request is syntactically valid but violates a business rule |
| `429` | `RATE_LIMITED` | Rate limit exceeded; `Retry-After` header present |
| `500` | `INTERNAL_ERROR` | Server fault; retry after a delay |

All errors use the §3 Error contract format.

#### Domain actions (non-CRUD commands)

*Use `POST /v1/{resource-plural}/{id}/actions/{verb}` for domain commands that do not map cleanly to a standard method.*

| CTR-NN | Path | Domain command | Description | Auth |
|---|---|---|---|---|
| _TODO_ | `POST /v1/_TODO_/{id}/actions/_TODO_` | _TODO_ | _TODO_ | _TODO_ |

---

## §2 Async surface

*Delete this section and note "No async surface — sync only" in §0 if this BC publishes no events and consumes no commands.*

### Events published

Events this BC publishes when its internal state changes. Consumers subscribe; this BC has no knowledge of specific consumer identities.

| CTR-NN | Domain event | CloudEvents `type` | Channel / Topic | Schema version | Known consumers |
|---|---|---|---|---|---|
| {{BC-NN}}.CTR-XX | [{{BC-NN}}.EVT-NN _TODO_](../../domain/07b-models/{{bc-slug}}.md#evt-01) | `com.{org}.{{bc-slug}}._TODO_` | `_TODO_` | v1 | _TODO_ |

---

#### {{BC-NN}}.CTR-XX · [EventName]

**Domain event:** [{{BC-NN}}.EVT-NN · EventName](../../domain/07b-models/{{bc-slug}}.md#evt-01)
**CloudEvents `type`:** `com.{org}.{{bc-slug}}.EventName`
**Channel / Topic:** `_TODO_`
**Trigger:** _TODO_ — which command or aggregate state transition produces this event
**Known consumers:** _TODO_

**Envelope (CloudEvents 1.0.3):**

```json
{
  "specversion": "1.0",
  "id": "<uuid-v4 — unique per occurrence>",
  "source": "/{{bc-slug}}",
  "type": "com.{org}.{{bc-slug}}.EventName",
  "datacontenttype": "application/json",
  "time": "<ISO-8601 UTC — time the event occurred, not when it was sent>",
  "subject": "<resource-id — the primary resource this event concerns>",
  "data": {
    "_TODO_field": "_TODO_"
  }
}
```

**Payload schema:**

| Field | Type | Description | Required |
|---|---|---|---|
| `_TODO_field` | string | _TODO_ | yes |

**Stability guarantee:** this `type` string is a permanent contract. Fields in `data` will not be removed or renamed. New optional fields may be added at any time — consumers must implement the Tolerant Reader pattern and ignore unknown fields. Schema-breaking changes require a new `type` string with a 90-day migration window.

---

### Commands consumed

Messages or events this BC subscribes to from external producers.

| CTR-NN | Source BC or system | CloudEvents `type` | Channel / Topic | Handler description |
|---|---|---|---|---|
| _TODO_ | _TODO_ | _TODO_ | `_TODO_` | _TODO_ |

---

## §3 Error contract

All synchronous API errors use **RFC 7807 Problem Details** (`Content-Type: application/problem+json`).

```json
{
  "type": "https://{api-domain}/errors/{error-type-slug}",
  "title": "Human-readable error class title (stable — same value for all occurrences)",
  "status": 422,
  "detail": "Specific explanation for this occurrence — safe to show to the API consumer",
  "instance": "/v1/{resource-plural}/{id}",
  "errors": [
    {
      "field": "amount",
      "code": "MUST_BE_POSITIVE",
      "message": "The amount field must be a positive number"
    }
  ]
}
```

**Rules:**
- `type` URI is stable and documents the error class. It must resolve to documentation describing when this error occurs and how to fix it.
- `title` is stable and does not vary between occurrences of the same error class. Clients may switch on `title` but `code` is preferred.
- `detail` is instance-specific and may change. Never parse programmatically.
- `errors` array is present for validation failures; omitted for server faults and non-validation errors.
- `code` values are `UPPER_SNAKE` and are the stable contract for client error-handling logic.

### Error code catalogue

| `code` | HTTP status | Meaning |
|---|---|---|
| `VALIDATION_ERROR` | 400 | One or more request fields failed validation; see `errors` array |
| `UNAUTHENTICATED` | 401 | No valid credentials provided; re-authenticate |
| `FORBIDDEN` | 403 | Authenticated but not authorised for this operation or resource |
| `NOT_FOUND` | 404 | Resource with given ID does not exist (or existence is confidential) |
| `CONFLICT` | 409 | State conflict — duplicate idempotency key, version mismatch, or business state prevents the operation |
| `UNPROCESSABLE` | 422 | Request is syntactically valid but violates a business rule; see `detail` |
| `RATE_LIMITED` | 429 | Too many requests; `Retry-After` header states when to retry |
| `INTERNAL_ERROR` | 500 | Server fault; do not expose internal details; safe to retry after delay |

*Add BC-specific error codes below this line.*

---

## §4 Versioning & deprecation policy

**Current version:** v1
**Versioning strategy:** _TODO_ (URL path versioning `/v1/…` / Accept header / additive-only)

### Breaking vs non-breaking changes

**Non-breaking (no version bump required):**
- Adding a new optional field to a response
- Adding a new optional query parameter
- Adding a new endpoint or resource
- Adding a new error `code` to the catalogue
- Adding a new CloudEvents `type`
- Adding optional fields to an event payload

**Breaking (version bump + deprecation period required):**
- Removing any field from a response
- Renaming a field
- Changing a field's type
- Changing a URL path segment
- Changing the HTTP method for an existing operation
- Removing or renaming an error `code`
- Removing or renaming a CloudEvents `type`
- Removing a field from an event payload

### Deprecation process

1. Mark the element `status: deprecated` in this document with the deprecation date.
2. Add `Deprecation: <ISO-8601-date>` and `Sunset: <ISO-8601-date>` response headers.
3. Announce with a minimum **90-day sunset window**.
4. After sunset: remove the element, bump the major version, update this document.

---

## §5 Security surface

**Authentication mechanism:** _TODO_ (Bearer JWT / API key / mTLS / OAuth 2.0)
**Token issuer / JWKS endpoint:** _TODO_
**Rate limit:** _TODO_ requests per minute per token

| CTR-NN | Operation | Auth required | Scope / Role |
|---|---|---|---|
| _TODO_ | `_TODO_ /v1/_TODO_` | yes / no | _TODO_ |

---

## Changelog

| Date | Change | Author |
|---|---|---|
| {{today}} | Initial scaffold | _TODO_ |
