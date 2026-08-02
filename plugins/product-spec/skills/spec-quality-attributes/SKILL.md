---
name: spec-quality-attributes
description: "Create a Quality Attributes specification — the non-functional requirements registry organised by ISO/IEC 25010:2023 product quality characteristics, with measurable acceptance criteria and verification methods. Use when asked to define NFRs, quality attributes, non-functional requirements, system quality, performance targets, security requirements, usability constraints, or reliability targets. Triggers on: quality attributes, NFR, non-functional requirements, system quality, performance requirements, security requirements, usability requirements, reliability requirements, ISO 25010."
version: "1.0.0"
user-invocable: true
impact: "low"
metadata:
  category: "specification"
  complexity: "medium"
status: active
last_reviewed: 2026-05-29
---

# Quality Attributes Builder

You are an expert at producing **Quality Attributes specifications** — the
non-functional requirements registry that defines how well the system performs
its functions, as distinct from what functions it performs (FBS territory).

The artifact produced by this skill is a markdown document at
`docs/product-specs/09a-quality-attributes.md`. It is NOT a
feature registry (→ FBS), NOT an architectural decision (→ ADR), NOT a process
doc — it is the **system quality specification**: measurable, verifiable
quality requirements anchored to ISO/IEC 25010:2023.

---

## Why a separate artefact from the FBS and ADRs

| Artefact | Answers |
|---|---|
| **FBS** | What does the system do? (functional) |
| **Quality Attributes** *(this skill)* | How well does it do it? (non-functional) |
| **ADR** | Which architectural decision satisfies a quality constraint? |

Quality attributes are not functionalities — they are system-wide or
scope-bounded quality constraints that cut across multiple features. They belong
neither in the FBS (which must stay functional) nor in ADRs (which document
decisions, not requirements). They form the specification that ADRs must satisfy.

---

## ISO/IEC 25010:2023 — the organising framework

*Source: ISO/IEC 25010:2023, Systems and software engineering — Systems and
software Quality Requirements and Evaluation (SQuaRE) — Product quality model.*

The standard defines 8 top-level quality characteristics. **Functional
Suitability is excluded** from this artefact — it is covered by the FBS.
The remaining 7 apply here:

| # | Characteristic | Key question for BlocPlan |
|---|---|---|
| 1 | **Performance Efficiency** | Is it fast enough for the persona's context? |
| 2 | **Compatibility** | Does it work alongside and with other systems? |
| 3 | **Interaction Capability** | Can every persona use it effectively? (ISO 25010:2023 renamed Usability) |
| 4 | **Reliability** | Does it behave correctly and stay available under real conditions? |
| 5 | **Security** | Does it protect data and actions from unauthorised access? |
| 6 | **Maintainability** | Can a small team sustain and evolve it? |
| 7 | **Flexibility** | Can it adapt to changing deployment, scale, or integration needs? |
| 8 | **Safety** | Does it avoid unacceptable risk to stakeholders? (new in ISO 25010:2023) |

---

## Granularity discipline

### The right level

One quality attribute entry = **one ISO/IEC 25010 sub-characteristic applied
to a specific product scope** (global, or one persona group / feature domain).

Each entry must have:
- A **measurable acceptance criterion** — a threshold, percentage, or
  verifiable condition. Never a vague aspiration.
- A **verification method** — how will compliance be demonstrated (load test,
  penetration test, accessibility audit, code coverage report, manual review)?

### Anti-patterns

**Too granular (wrong):**
- One entry per API endpoint response time
- One entry per form field validation rule
- One entry per individual security check

**Too vague (also wrong):**
- "The system shall be fast"
- "The system shall be secure"
- "The system shall be easy to use"

**Right level:**
- One entry covering all surgeon portal interactions: "Interaction response
  time ≤ 3s on standard mobile connection — P-03 accesses between consultations"
- One entry covering the scheduling algorithm: "Conflict detection false-negative
  rate = 0 — a double-booking not detected at generation time is a critical
  production incident"

### The persona-context rule

Quality attributes for **Interaction Capability** and **Performance Efficiency**
must be grounded in the specific persona's context (device, network, time
pressure, cognitive load) from the personas doc. Generic "the UI shall be
usable" is not acceptable.

*Source: Bass, Clements & Kazman — Software Architecture in Practice,
4th ed. (2021) §4 — quality attribute scenarios require stimulus, environment,
response, and response measure.*

### Scope modifiers

Each entry declares its scope:

| Scope | Meaning |
|---|---|
| **Global** | Applies to the entire product unconditionally |
| **[Persona]** | Applies to all surfaces serving that persona |
| **[Feature domain]** | Applies to a specific capability cluster |
| **Phase N** | Applies from a specific delivery phase |

---

## Modes of operation

### Mode 1 — Scaffold

Create the folder and file with ISO/IEC 25010 characteristics as H2 sections,
each with an empty table. Read the project's ADRs and FBS first to understand
which characteristics are most relevant.

### Mode 2 — Fill

Populate quality attributes from project context:
- **Personas** → Interaction Capability requirements (device, time pressure,
  learnability constraints per persona)
- **Value streams pain index** → Performance Efficiency priorities (Critical
  pain stages drive the tightest performance targets)
- **ADRs** → Security, Flexibility, Maintainability constraints already decided
- **FBS differentiators** → Reliability requirements (differentiator features
  must have zero-defect targets)
- **Business context** → Safety, Compatibility (Swiss healthcare, nFADP, OIDC)

### Mode 3 — Update

Add or revise individual attributes as architecture decisions are made or
evidence arrives. Promote confidence level (Assumed → Tested → Validated).

---

## Output structure

```
docs/product-specs/09a-quality-attributes.md

H1: {{product}} — Quality Attributes

Intro: what QAs are, why separate from FBS, ISO 25010 anchor,
methodology pointer.

§Confidence legend (Assumed / Tested / Validated)

§Per-characteristic H2 sections (7 sections, one per ISO characteristic):
  - Brief one-paragraph definition of the characteristic
  - Table of quality attributes for this product:
    | ID | Attribute | Scope | Acceptance criterion | Verification method | Confidence | ADR link |

§Changelog
```

- Open every generated file with the standard artefact frontmatter (OKF-superset block — set `type` to this artefact's `okf_type` display name from the `metamodel` skill's `references/artefact-types-registry.yaml`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`). Run `git config user.name` for `owner`. Set `status: draft` on initial scaffold. Default `review_interval: 60d`. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`.

---

## Quality attribute ID convention

`QA-[characteristic-prefix][NN]`

| Characteristic | Prefix |
|---|---|
| Performance Efficiency | PE |
| Compatibility | CO |
| Interaction Capability | IC |
| Reliability | RE |
| Security | SE |
| Maintainability | MA |
| Flexibility | FL |
| Safety | SA |

Examples: `QA-PE01`, `QA-SE03`, `QA-IC02`

---

## Per-characteristic guidance

### Performance Efficiency

*ISO/IEC 25010:2023 sub-characteristics: Time Behaviour, Resource Utilisation, Capacity*

Focus on the persona's context, not the server metric in isolation:
- Time Behaviour: how long does the critical action take in the persona's actual
  usage context (device, network, time available)?
- Capacity: what is the maximum realistic load (clinics × surgeons × concurrent
  users)?

Anchor to value stream pain index: Critical-pain stages drive the tightest
response targets.

### Compatibility

*Sub-characteristics: Co-existence, Interoperability*

Relevant primarily for:
- OIDC / OAuth 2.0 federation (ADR-0004)
- Future Opale integration (Phase 3, FBS C6.3 territory)
- Data export formats (CSV, PDF — FBS C6.4.F04)

### Interaction Capability

*Sub-characteristics: Appropriateness Recognisability, Learnability,
Operability, User Error Protection, User Engagement, Inclusivity,
User Assistance, Self-Descriptiveness*

**Must be written per persona.** The surgeon portal (P-03, mobile,
3-minute interaction window) has radically different requirements from
the admin planning grid (P-01, desktop, dense information environment).
Generic usability requirements are not acceptable here.

### Reliability

*Sub-characteristics: Faultlessness, Availability, Fault Tolerance, Recoverability*

Differentiator features (★ in FBS) require the most stringent faultlessness
targets — a conflict detection false negative or a missed confirmation is a
critical production incident with clinical consequences.

### Security

*Sub-characteristics: Confidentiality, Integrity, Non-Repudiation,
Accountability, Authenticity, Resistance*

In Swiss healthcare context, anchor security requirements to:
- nFADP (Swiss Federal Act on Data Protection, 2023) obligations
- Cross-tenant data isolation (ADR-0003)
- Authentication mechanism chosen (ADR-0004)
- Audit trail completeness (regulatory traceability)

### Maintainability

*Sub-characteristics: Modularity, Reusability, Analysability,
Modifiability, Testability*

For a solo founder, Testability and Modifiability are the most critical.
The scheduling algorithm (FBS C3.1, C3.2) must be fully unit-testable.
Operational complexity must be sustainable without a dedicated ops team
(constrain Operability — ADR-0001 Q1 context).

### Flexibility

*Sub-characteristics: Adaptability, Scalability, Installability,
Replaceability — ISO 25010:2023 expanded Portability into Flexibility*

Anchor to ADR-0001 open decisions: architecture options have very different
vendor portability profiles. Data residency constraints (nFADP) are a
Flexibility requirement (Installability / Adaptability to different regions).

### Safety

*Sub-characteristics: Operational Constraint, Risk Identification, Fail Safe,
Hazard Warning, Safe Integration — new in ISO 25010:2023*

For Phase 1 (no patient data), Safety requirements are low. For Phase 2
(patient-adjacent data, intervention scheduling), a failed double-booking
detection or a missed pre-op checklist item has patient safety implications.
Flag Phase 2 Safety requirements early.

---

## Cross-references

| What links here | Why |
|---|---|
| **ADRs** | Each architecture decision satisfies one or more QA requirements. Link bidirectionally: QA entry → ADR, ADR → QA entry. |
| **FBS differentiators** (★) | Differentiator features have zero-defect Reliability targets. |
| **Personas** | Interaction Capability and Performance Efficiency are persona-grounded. |
| **Value stream pain index** | Critical-pain stages drive Performance Efficiency priorities. |
| **Business objectives** (`KR-NN.M`) | Key Results that state measurable thresholds (e.g. "response time < 500ms") can ground QA-PE or QA-RE acceptance criteria. When filling QAs, check `docs/business/04b-objectives.md` for KR targets that should become QA entries. Link bidirectionally: QA entry → KR-NN.M. |

Quality attributes must NOT appear in the FBS. If a functional capability
has a quality constraint (e.g. "conflict detection must have zero false
negatives"), the constraint goes here; the functional behaviour goes in the FBS.

---

## Reference materials

- **`references/nfr-definition-and-examples.md`** — canonical NFR definition (BABOK, Robertson, Bass), arc42-inspired examples per ISO/IEC 25010:2023 characteristic, and fit criterion vocabulary. **Read this before filling any quality attribute entry.** Lives only in the kit — never copied to projects.

---

## Sources

| Source | What it anchors |
|---|---|
| ISO/IEC 25010:2023. *Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model.* ISO/IEC. | Primary organising framework — all 8 characteristics + sub-characteristics |
| ISO/IEC 25010:2011. Previous version, still widely cited. | Historical context; most industry references use the 2011 version |
| Bass, L., Clements, P. & Kazman, R. (2021). *Software Architecture in Practice*, 4th ed. Addison-Wesley. | Quality attribute scenarios (stimulus/environment/response/measure); architectural tactics per characteristic |
| Rozanski, N. & Woods, E. (2012). *Software Systems Architecture*, 2nd ed. Addison-Wesley. | Quality attribute profiles; cross-cutting concerns in architecture viewpoints |
| Robertson, S. & Robertson, J. (2012). *Mastering the Requirements Process*, 3rd ed. Addison-Wesley. | Planguage for precise quality attribute specification (fit criteria) |
| BABOK v3 §9.1.4. IIBA (2015). | Non-functional requirement classification; distinction from functional requirements |
| Fielding, R. (2000). *Architectural Styles and the Design of Network-based Software Architectures.* PhD thesis, UC Irvine. | REST constraints as a Compatibility / Interoperability quality model |

---

## Checklist

Before declaring the work done:

- [ ] Folder and file created
- [ ] ISO/IEC 25010 characteristic structure present (7 H2 sections)
- [ ] Each entry has: ID (QA-XXNN), attribute name, scope, acceptance criterion, verification method, confidence, ADR link if applicable
- [ ] Acceptance criteria are measurable (threshold, %, verifiable condition) — never vague aspirations
- [ ] Interaction Capability entries are persona-grounded (P-NN)
- [ ] Performance Efficiency entries reference value stream pain index where applicable
- [ ] KR-NN.M targets that specify measurable thresholds have corresponding QA-XXNN entries (check `docs/business/04b-objectives.md` if it exists)
- [ ] Differentiator FBS features have Reliability entries
- [ ] Security entries reference nFADP and relevant ADRs (0001, 0003, 0004)
- [ ] No functional requirements leaked in (→ FBS)
- [ ] No architectural decisions leaked in (→ ADRs)
- [ ] Methodology pointer links to this skill's sources section
