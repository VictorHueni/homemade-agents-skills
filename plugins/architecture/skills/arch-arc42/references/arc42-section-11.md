# arc42 §11 — Risks and Technical Debt (embedded reference)

Extracted from the arc42 v9.0 template (July 2025). Use as the authoritative spec when writing `docs/architecture/arc42/11-risks.md`.

Upstream: [docs.arc42.org/section-11](https://docs.arc42.org/section-11/).

---

## Content

> A list of identified technical risks or technical debts, ordered by priority.

## Motivation

> "Risk management is project management for grown-ups." (Tim Lister, Atlantic Systems Guild.)
>
> Under this topic you should summarize the known technical risks or problems. Risks usually occur in technical form. Prominently documented risks are faster found and addressed by the responsible team.

## Form

> List of risks with suggested mitigation measures.

---

## Kit taxonomy: risk types

The kit distinguishes four risk types in §11:

| Type | Description | Example |
|---|---|---|
| `architectural` | A fundamental design decision that may not hold under changed requirements or scale | "Shared database between two bounded contexts — coupling will slow independent deployments" |
| `technical-debt` | A deliberate shortcut taken to meet a deadline; known to require rework | "Auth middleware uses symmetric JWT — must migrate to asymmetric before public API launch" |
| `dependency` | Risk from an external dependency (library, SaaS, vendor, partner) | "Vendor X API v2 EOL in 6 months — migration path not yet scoped" |
| `security` | A known security gap not yet mitigated | "Admin endpoints not protected by IP allowlist in staging" |

---

## Risk scoring (kit default)

| Dimension | Values |
|---|---|
| Probability | `low` / `medium` / `high` |
| Impact | `low` / `medium` / `high` / `critical` |
| Severity | Derived: `critical` if impact=critical OR both probability+impact=high; else `high` if either=high; else `medium`; else `low` |

---

## Risk lifecycle states

| Status | Meaning |
|---|---|
| `open` | Risk identified; not yet mitigated |
| `mitigated` | Mitigation in place; monitoring for residual risk |
| `materialised` | Risk event occurred; now an incident or bug |
| `closed` | Risk fully resolved or accepted as residual |
| `accepted` | Deliberate decision to live with the risk; rationale documented |

---

## Boundary: §11 vs `dev-tech-debt`

**§11 is an architect's radar, not a debt ledger.** The distinction:

| §11 `arch-risks` | Future `dev-tech-debt` |
|---|---|
| Architectural-scope risks and deliberate shortcuts worth monitoring | Exhaustive catalogue of every code-level debt item |
| 5–20 entries, curated by the architect | Potentially hundreds of entries, maintained continuously |
| Updated quarterly or after ADR decisions | Updated sprint-by-sprint |
| Risks that, if unaddressed, threaten system quality or deliverability | Individual code smells, missing tests, outdated dependencies |

`technical-debt` rows in §11 that grow into a large catalogue should migrate to `dev-tech-debt` when that skill is available. Until then, keep §11 focused on the highest-severity items.

---

## Kit-specific rules for §11

1. **Order by severity descending.** `critical` risks at the top; `low` at the bottom.

2. **Every `technical-debt` row must have a `Remediation path`** — at minimum, the name of the epic or ADR that will address it, even if it is "not yet scheduled."

3. **Accepted risks require a rationale.** "We accept this risk because..." — not just `status: accepted`.

4. **Do not list operational risks here.** Infrastructure failure modes, disaster recovery, and on-call scenarios belong in ops runbooks (`ops-runbook`). §11 is for risks rooted in architectural decisions.

---

## Acceptance criteria — when §11 is "done"

- [ ] `docs/architecture/arc42/11-risks.md` exists with standard frontmatter
- [ ] All four risk types represented or explicitly noted as "none currently"
- [ ] Risks ordered by severity descending
- [ ] Every `technical-debt` row has a `Remediation path` (or a `decision-gap` row filed to the central ledger)
- [ ] Every `accepted` row has a rationale
- [ ] No operational (infrastructure) risks duplicated from ops runbooks
