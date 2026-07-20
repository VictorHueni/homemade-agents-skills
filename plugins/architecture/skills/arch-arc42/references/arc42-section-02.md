# arc42 §2 — Architecture Constraints (embedded reference)

Extracted from the arc42 v9.0 template (July 2025). Use as the authoritative spec when writing `docs/architecture/arc42/02-constraints.md`.

Upstream: [docs.arc42.org/section-2](https://docs.arc42.org/section-2/).

---

## Content

> Any requirement that constrains software architects in their freedom of design and implementation decisions or decision about the development process. These constraints sometimes go beyond individual systems and are valid for whole organizations and companies.

## Motivation

> Architects should know exactly where they are free in their design decisions and where they must adhere to constraints. Constraints must always be dealt with; they may be negotiable.

## Form

> Simple tables of constraints with explanations. If needed you can subdivide them into technical constraints, organizational and political constraints and conventions (e.g. programming guidelines, versioning, etc.)

---

## Three constraint categories (kit taxonomy)

### Technical constraints

Constraints imposed by the technology environment — mandated languages, frameworks, platforms, or tools that the architecture must conform to.

Examples:
- Must deploy on AWS (company-wide cloud contract)
- Java 21 only (mandated by ops team)
- PostgreSQL 16 only (existing DBA infrastructure)
- Must expose a REST API (third-party integration requirement)

### Organizational constraints

Constraints imposed by the organization — team structure, timelines, budgets, partner dependencies, or regulatory bodies that govern the project.

Examples:
- Team of 3 engineers; cannot operate more than 2 services independently
- Go-live before Q4 2026 (fiscal deadline)
- All vendors must be EU-based (procurement policy)
- Data must not leave the EU (DPA requirement)

### Legal / regulatory constraints

Constraints imposed by law, regulation, or industry standards.

Examples:
- GDPR Article 17 (right to erasure) — must be implementable within 30 days
- PCI DSS SAQ D — card data must never touch application servers
- SOC 2 Type II — audit logging of all privileged actions required
- HIPAA minimum necessary principle — access control must be attribute-based

---

## Kit-specific rules for §2

1. **Constraints are facts, not opinions.** Every `CST-NN` row should cite its source (ADR, contract, regulation, org policy). If the source cannot be named, it may be a preference, not a constraint.

2. **Hard constraints vs soft constraints.** Hard constraints cannot be traded off; soft constraints can be negotiated under pressure. Flag soft constraints with a `negotiable` note — architects may revisit these during ADR deliberations.

3. **Every constraint that drove an architecture decision should cross-reference the ADR.** This prevents re-opening settled debates and makes the constraint register auditable.

4. **Do not duplicate quality attribute requirements here.** If a constraint expresses a performance target (e.g. "response time < 200ms"), it belongs in `docs/product-specs/09a-quality-attributes.md` (QA-XXNN), not §2. §2 is for constraints on the *solution space*, not targets for the *solution*.

---

## Acceptance criteria — when §2 is "done"

- [ ] `docs/architecture/arc42/02-constraints.md` exists with standard frontmatter
- [ ] All three categories (technical / organizational / legal-regulatory) are present or explicitly noted as "none"
- [ ] Each `CST-NN` row has a source citation (ADR-NNNN, regulation name, contract reference, or org policy name)
- [ ] Hard vs soft constraint distinction is noted where relevant
- [ ] No quality targets duplicated from QA register
