# arc42 §8 — Cross-Cutting Concepts (embedded reference)

Extracted from the arc42 v9.0 template (July 2025). Use as the authoritative spec when writing `docs/architecture/arc42/08-cross-cutting-concepts.md`.

Upstream: [docs.arc42.org/section-8](https://docs.arc42.org/section-8/).

---

## Content

> This section describes overall, principal regulations and solution ideas that are relevant in multiple parts (= cross-cutting) of your system. Such concepts are often related to multiple building blocks. They can include many different topics, such as
>
> - models, especially domain models
> - architecture or design patterns
> - rules for using specific technology
> - principal, often technical decisions of an overarching (= cross-cutting) nature
> - implementation rules

## Motivation

> Concepts form the basis for *conceptual integrity* (consistency, homogeneity) of the architecture. Thus, they are an important contribution to achieve inner qualities of your system.
>
> Some of these concepts cannot be assigned to individual building blocks, e.g. security has to be considered in nearly all building blocks.

## Form

> The form can be varied:
>
> - concept papers with any level of detail
> - cross-cutting model excerpts or scenarios using notations of the architecture views
> - sample implementations, especially for technical concepts
> - reference to typical usage of standard frameworks (e.g. using Hibernate for object/relational mapping)

---

## Kit taxonomy: eleven standard concept areas

The kit uses eleven canonical cross-cutting concept areas. Each maps to a `CC-NN` entry. Projects may use a subset; empty categories should still be listed with "Not applicable" to show the decision was conscious.

| CC area | Typical content |
|---|---|
| **Authentication** | How users and services prove their identity (JWT / OAuth2 / API key / mTLS) |
| **Authorisation** | How permissions are enforced (RBAC / ABAC / policy engine) |
| **Session management** | Stateless vs stateful; token expiry; refresh strategy |
| **Logging** | Structured vs unstructured; correlation IDs; log levels; sink (stdout / Loki / CloudWatch) |
| **Distributed tracing** | Trace propagation standard (W3C TraceContext / B3); instrumentation approach (OpenTelemetry) |
| **Error handling** | Error envelope format (RFC 7807 / custom); error propagation rules; retry / backoff policy |
| **Persistence** | ORM vs query builder vs raw SQL; migration tooling; connection pool config |
| **Caching** | What is cached (query results / rendered HTML / API responses); TTL; invalidation strategy |
| **Internationalisation** | i18n framework; locale negotiation; translation workflow |
| **Security (transport)** | TLS version; certificate management; mTLS for service-to-service |
| **Feature flags** | Flag store (LaunchDarkly / Unleash / config file); flag lifecycle; kill-switch policy |

---

## Kit-specific rules for §8

1. **CC concepts describe the convention, not the implementation.** "We use structured JSON logs via Pino, always emitting `correlationId`" — not the Pino configuration file.

2. **Each CC-NN entry must state which containers (CON-NN) it applies to.** If a concept applies everywhere, write "All containers." If it is container-specific, name the containers — this signals that the concept may not be truly cross-cutting and should perhaps live in §5 instead.

3. **Cross-reference the governing ADR.** Most cross-cutting decisions should be documented as ADRs (e.g. "ADR-0005: Adopt OpenTelemetry for distributed tracing"). §8 is the index; the ADR is the detail.

4. **Do not duplicate domain model content here.** Domain models, ubiquitous language, and aggregate rules belong in `docs/domain/`. Section 8 is for *technical* cross-cutting concerns, not domain concepts.

---

## Acceptance criteria — when §8 is "done"

- [ ] `docs/architecture/arc42/08-cross-cutting-concepts.md` exists with standard frontmatter
- [ ] All 11 canonical CC areas addressed (subset is fine — mark others "Not applicable" with a rationale)
- [ ] Each `CC-NN` entry lists which containers it applies to
- [ ] Each `CC-NN` entry links to the governing ADR (or files a `decision-gap` row to the central ledger)
- [ ] No domain model content duplicated from `docs/domain/`
