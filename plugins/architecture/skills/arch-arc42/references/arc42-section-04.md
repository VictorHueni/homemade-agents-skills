# arc42 §4 — Solution Strategy (embedded reference)

Extracted from the arc42 v9.0 template (July 2025). Use as the authoritative spec when writing `docs/architecture/arc42/04-solution-strategy.md`.

Upstream: [docs.arc42.org/section-4](https://docs.arc42.org/section-4/).

---

## Content

> A short summary and explanation of the fundamental decisions and solution strategies, that shape system architecture. It includes:
>
> - technology decisions
> - decisions about the top-level decomposition of the system, e.g. usage of an architectural pattern or design pattern
> - decisions on how to achieve key quality goals
> - relevant organizational decisions, e.g. selecting a development process or delegating certain tasks to third parties.

## Motivation

> These decisions form the cornerstones for your architecture. They are the foundation for many other detailed decisions or implementation rules.

## Form

> Keep the explanations of such key decisions short.
>
> Motivate what was decided and why it was decided that way, how it was decided and when were these decisions made. Refer to the details in the following sections of the architecture documentation.
>
> Avoid redundancy. Refer to related sections of the document where appropriate.

---

## Kit-specific rules for §4

### §4 is a navigation aid, not a design document

The temptation is to write §4 as a second set of ADRs. Resist this: §4 should be readable in under 5 minutes and link the reader to the right ADR for each decision.

**What belongs in §4:**

| Content | Form |
|---|---|
| Technology decisions | One-line summary + `ADR-NNNN` link |
| Decomposition approach | One paragraph (microservices / modular monolith / etc.) |
| Quality goal → tactic mapping | Table (QA-XXNN → tactic name → ADR-NNNN) |
| Key organizational decisions | One-line note (e.g. "Cloud-first, no on-prem", "Outsource mobile to Agency X") |

**What does NOT belong in §4:**

- Full ADR rationale (link to the ADR instead)
- Implementation detail (belongs in §5 / §6)
- Future roadmap (belongs in delivery roadmap)
- Quality targets themselves (belong in `docs/product-specs/09a-quality-attributes.md`)

### Quality goal → tactic mapping

The most valuable unique content in §4 is explicitly answering: *for each top-N quality goal, what architectural tactic addresses it?*

| Quality goal | QA-XXNN | Architectural tactic | ADR-NNNN |
|---|---|---|---|
| Scalability | QA-PE-01 | Stateless containers + horizontal pod autoscaling | ADR-0004 |
| Data residency | QA-SE-02 | EU-only cloud regions; no CDN caching of PII | ADR-0007 |
| Testability | QA-MT-01 | Hexagonal architecture; domain logic isolated from I/O adapters | ADR-0003 |

This table is the core of §4. Everything else is supporting context.

---

## Acceptance criteria — when §4 is "done"

- [ ] `docs/architecture/arc42/04-solution-strategy.md` exists with standard frontmatter
- [ ] Decomposition approach stated in one paragraph (with `CON-NN` reference if §5 exists)
- [ ] Technology decisions table: one row per key technology choice + `ADR-NNNN` link
- [ ] Quality goal → tactic mapping table: covers all QA-XXNN items with priority ≥ `high`
- [ ] No ADR rationale re-stated — links only
- [ ] No implementation detail duplicated from §5
