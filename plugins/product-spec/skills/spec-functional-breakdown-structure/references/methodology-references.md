# Functional Breakdown Structure — Methodology References

This document records the canonical frameworks used to design and maintain
Functional Breakdown Structure artefacts. The artefact is a synthesis of
five sources rather than a single school — each contributes a specific
lens.

The most important methodological choice up front is the **stance**: this
skill produces **hybrid PBS+FBS** (the form software-product orgs need),
not pure NASA-style FBS (which is purely function-oriented). See §1 for
the distinction.

---

## 1. The "pure FBS vs hybrid FBS" stance

The phrase "Functional Breakdown Structure" has two distinct traditions
that are easily confused. They produce different artefacts for different
purposes. This skill anchors on the **hybrid form** because it's what
software-product teams actually use.

| Dimension | Pure FBS *(NASA, systems engineering)* | Hybrid FBS *(this skill)* |
|---|---|---|
| **Top level** | Pure function tree (no product reference) | Product / domain (PBS-flavoured L0) |
| **Mid level** | Sub-functions | Capabilities (soft-linked from BC Map) |
| **Leaf level** | Atomic functions | Functionalities (atomic capabilities of the product) |
| **Tied to architecture?** | **No** — "not tied to any particular architectural implementation" | **Yes** — code-path annotations bind functionalities to packages |
| **Tied to specific product(s)?** | **No** — generic mission abstraction | **Yes** — organised by product / domain |
| **Primary user** | Systems engineers, defence / aerospace | Product managers, software architects, engineering leads |
| **Companion artefact** | WBS (project deliverables) | BC Map (strategic abilities) + PRD (feature delivery) |

The hybrid form is justified for software-product contexts because:
- Most software products are tied to a specific product / domain identity.
- Engineering teams need code-path traceability that pure FBS deliberately omits.
- The capability layer (from TOGAF / BC Map) provides the strategic anchor that pure FBS lacks.

Pure FBS remains the authoritative reference for the term "FBS"; this
skill's output should be understood as a pragmatic hybrid that borrows
the FBS name for organisational continuity in software product contexts.

---

## 2. NASA — The Functional Breakdown Structure (FBS) and Its Relationship to Life Cycle Cost

**Used for:** the canonical definition of FBS, the function-vs-product distinction, the rationale for separating functions from architectural implementation.

**Source:** NASA Technical Reports Server (NTRS),
[The Functional Breakdown Structure (FBS) and Its Relationship to Life
Cycle Cost](https://ntrs.nasa.gov/citations/20130012526).

### Key contributions

- **Definition:** *"The Functional Breakdown Structure (FBS) is a
  structured, modular breakdown of every function that must be addressed
  to perform a generic mission."*
- **Function vs Product distinction:** *"Unlike a Work Breakdown
  Structure (WBS), the FBS is a function-oriented tree, not a
  product-oriented tree. The FBS details not products, but operations or
  activities that should be performed."*
- **Architecture-independence:** *"The FBS is not tied to any particular
  architectural implementation because it is a listing of the needed
  functions, not the elements, of the architecture."*
- **Purpose:** *"By approaching the systems engineering problem from the
  functional view, instead of the element or hardware view"* designers
  gain *"full accountability of all functions required"* and can identify
  *"missing or redundant elements,"* enabling valid life-cycle cost
  comparisons.

### Discipline encoded in the template

- The FBS is the functionality **registry** (comprehensive, status-tracked) — not a project plan, not a feature spec, not a roadmap.
- Functionalities are phrased as *what the system does*, not *what the product looks like*.
- The skill stays out of architectural-implementation detail (no class names, no API endpoint signatures, no schema definitions inside the FBS).

---

## 3. BABOK® §10.22 — Functional Decomposition

**Used for:** the hierarchical decomposition discipline (single-parent rule), the stopping criterion, the decomposition objectives, the representation options.

**Source:** *A Guide to the Business Analysis Body of Knowledge® (BABOK®
Guide), v3*, International Institute of Business Analysis (IIBA),
Chapter 10 — Techniques, §10.22 "Functional Decomposition".
[IIBA reference page](https://www.iiba.org/knowledgehub/business-analysis-body-of-knowledge-babok-guide/10-techniques/10-22-functional-decomposition/)
(paywalled).

### Key contributions

- **Purpose:** functional decomposition helps manage complexity and
  reduce uncertainty by breaking down processes, systems, functional
  areas, or deliverables into their simpler constituent parts and
  allowing each part to be analyzed independently.
- **Single-parent rule:** *"Any sub-component can have only one parent
  component when developing the functional hierarchy."*
- **Stopping criterion:** functions are further broken down into
  sub-functions until all elements are at their most basic level. The
  decomposition objectives drive the depth.
- **Representation:** hierarchical lists, tree diagrams, indented tables.
  This skill uses indented tables for the per-capability functionality
  enumeration, with an ASCII tree at the top for navigation.

### Discipline encoded in the template

- Each functionality has exactly one parent capability (single-parent rule).
- Stopping criterion = "the row is a stable, distinct, atomic functionality the engineering team would recognise as one thing to ship". Going deeper means leaving FBS for PRD / implementation-plan territory.
- The template uses both representations: ASCII tree (overview) + per-capability tables (detail).

---

## 4. TOGAF — Capability + Functional View

**Used for:** the soft-link discipline between functionality and capability (FBS extends but does not redefine BC Map), the rule that capability maps are NOT functional decompositions.

**Source:** The Open Group, *TOGAF® Standard*, Phase B — Business
Architecture.
[Open Group TOGAF Business Capability](https://pubs.opengroup.org/togaf-standard/business-architecture/business-capabilities.html)
(login-walled — open practitioner literature available).

### Key contributions

- **Capability ≠ Functional decomposition:** *"It's important to note
  that a capability map is not a functional decomposition of the
  enterprise. Once defined, the business capability map provides a
  self-contained view of the business that is independent of the current
  organizational structure, business processes, IT systems and
  applications, and the product or service portfolio."*
- **Functional decomposition is downstream:** TOGAF positions
  capability mapping as the strategic layer; functional decomposition
  occurs when capabilities are mapped to applications, systems, and
  product features. The FBS sits in this downstream position.
- **Capability-to-functionality is a "mapping back"**, not a
  decomposition — *"mapping business capabilities back to these domains
  will provide greater insight into alignment and optimization."*

### Discipline encoded in the template

- FBS **soft-links** to BC Map by capability ID; never restates the capability definition.
- The hybrid FBS form (with capabilities at L1) is explicitly framed as a *mapping back* from capabilities to product functionalities, not a re-decomposition of capabilities.
- The kit's BC-Map skill and FBS skill use matching capability IDs (`C1.1`, `C1.2`, …) so the mapping is mechanical.

---

## 5. NASA WBS Handbook — Hierarchical Decomposition Discipline

**Used for:** the discipline that the breakdown is product-oriented at top levels, the rule about sub-dividing work content into manageable elements, and the warning that WBS and FBS are complementary but distinct.

**Source:** NASA, *NASA Work Breakdown Structure (WBS) Handbook*
(NASA/SP-3404).
[NASA WBS Handbook PDF](https://ntrs.nasa.gov/api/citations/20200000300/downloads/20200000300.pdf).

### Key contributions

- **WBS structure:** *"the typical space flight system WBS is product
  oriented, beginning with the end product at the highest level (such as
  spacecraft) and subdividing the work content into lower-level elements
  until sufficient detail is achieved for management purposes."*
- **WBS vs FBS:** they are complementary tools. FBS handles *what
  functions must exist*; WBS handles *what work must be performed*. This
  skill produces an FBS (functions / functionalities), not a WBS (work
  packages / sprints / milestones).
- **Hierarchical-decomposition rigour:** every element has a single
  parent; the tree is exhaustive at each level; nothing escapes the
  hierarchy.

### Discipline encoded in the template

- The skill rejects WBS-style content (project deliverables, work packages, milestones, sprint commitments).
- Sub-dividing stops at the functionality level — going further (L3 / L4 sub-functionalities) usually means crossing into implementation detail (PRD / plan territory).

---

## 6. Practitioner discipline — *Know Your Product: A Practical Guide to Functional Decomposition*

**Used for:** the sizing heuristics, the anti-patterns, the three-tier framing (domain → feature → operation), the warning against over-architecture.

**Source:** Hackernoon practitioner article,
[*Know Your Product: A Practical Guide to Functional
Decomposition*](https://hackernoon.com/know-your-product-a-practical-guide-to-functional-decomposition).

### Key contributions

- **Sizing:** *"no more than ten domains, including the core product"*
  — informs the L0 ≤ 10 heuristic.
- **Volume guidance:** *"it's okay to have a few hundred features for a
  grown-up product"* — informs the total ≤ ~500 functionalities heuristic.
- **Three-tier framing:** domain → feature → operation (in practitioner
  terms). Maps to L0 → L1 capability → L2 functionality in this skill's
  language.
- **Anti-patterns identified:**
  - *Over-architectural thinking*: treating integrations as a separable domain rather than business-flow-dependent features.
  - *Special casing*: creating exceptions that "show some incoherence in the idea and may lead to other special cases".
  - *Circular dependencies*: "a bad decision, but still possible".

### Discipline encoded in the template

- Sizing heuristics (L0 ≤ 10, L2 ≤ 25, total ≤ ~500) come directly from this source.
- The skill's anti-pattern catalogue extends the practitioner's three with FBS-specific patterns (capability duplication, status drift, roadmap creep).

---

## Summary — what each framework contributes

| Framework | Contributes |
|---|---|
| Pure FBS vs Hybrid FBS stance | The honest distinction between NASA's function-tree and the software-product industry's hybrid form |
| NASA NTRS FBS paper | Canonical FBS definition; function-vs-product separation; architecture-independence principle |
| BABOK §10.22 | Functional decomposition technique; single-parent rule; stopping criterion |
| TOGAF | Capability-to-functionality mapping rule; capability map ≠ functional decomposition; FBS as downstream artefact |
| NASA WBS Handbook | Hierarchical-decomposition rigour; WBS-vs-FBS distinction (this skill produces FBS, not WBS) |
| Hackernoon practitioner | Sizing heuristics; anti-pattern catalogue (over-architecting, special-casing, circular dependencies) |

The template is not "pure NASA FBS" or "pure BABOK functional
decomposition" — it is the canonical synthesis adapted for software
product contexts. Every section maps back to at least one source. The
hybrid-FBS stance is the soul of the document; NASA provides the rigour;
BABOK provides the decomposition discipline; TOGAF provides the
upstream-capability soft-link rule; the practitioner literature provides
the sizing and the anti-patterns.
