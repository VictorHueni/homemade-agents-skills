# Business Capability Map — Methodology References

This document records the canonical frameworks used to design and maintain the
[Business Capability Map](03a-capability-map.md). The artefact is a
synthesis of five sources rather than a single school — each contributes a
specific lens.

---

## 1. TOGAF® G189 — Business Capabilities

**Used for:** the canonical definition of a business capability, naming
discipline (stable noun phrase, technology-independent), heat-map dimensions,
the capability-vs-process-vs-function distinction, and the "what" vs "how"
separation that underpins the entire map.

**Source:** The Open Group, *TOGAF® Series Guide: Business Capabilities*
(G189), 2021.
[Governance Foundation hosted PDF](https://governance.foundation/assets/frameworks/togaf/g189%20-%20Business%20Capbility.pdf).
Official Open Group standard page (login-walled):
[pubs.opengroup.org/togaf-standard/business-architecture/business-capabilities.html](https://pubs.opengroup.org/togaf-standard/business-architecture/business-capabilities.html).

### Key contributions

- **Definition:** a business capability is *"an ability that an organisation,
  person, or system possesses… typically expressed in general and high-level
  terms and typically requires a combination of organisation, people,
  processes, and technology to achieve."* It is the **what**, not the how.
- **Stable, technology-independent naming:** capabilities are noun phrases
  that remain stable when underlying technology, organisation, or processes
  change. If the name changes when you swap a tool, it is a system or
  function, not a capability.
- **Heat-map dimensions** (TOGAF G189 §3.4):
  - **Maturity** — current state of execution (CMM-style 1–5 scale)
  - **Effectiveness** — how well the capability delivers outcomes today
  - **Performance** — speed / throughput / cost characteristics
  - **Value contribution / cost** — strategic importance to outcomes
- **Capability vs Process:** *"a Business Capability is not a Business
  Process; it does not depict the tasks and sequence to achieve an outcome.
  However, Business Processes operationalise the Capability."*
- **Capability vs Function:** business functions group activities by the
  skills / expertise required; capabilities are the abilities delivered.

### Discipline encoded in the template

- The **noun test** at the per-capability quality-check stage.
- The **technology-independence test** at the per-capability quality-check stage.
- Maturity field made optional (politically loaded; only filled when honestly assessable).
- Strategic Importance (a synthesis of TOGAF's value-contribution dimension) made mandatory in the index.

---

## 2. Cutter — "The Business Capability Map: The Rosetta Stone of Business/IT Alignment"

**Used for:** the single-map-per-scope rule, the anti-overlap discipline,
sizing heuristics (15–25 foundation L1 capabilities), and the five common
mistakes catalogue.

**Source:** William Ulrich & Michael Rosen, *The Business Capability Map: The
Rosetta Stone of Business/IT Alignment*, Cutter Consortium, 2011.
[cutter.com/article/business-capability-map-rosetta-stone-businessit-alignment-469506](https://www.cutter.com/article/business-capability-map-rosetta-stone-businessit-alignment-469506).

### Key contributions

- **The Rosetta Stone metaphor:** the BC Map translates between "well
  understood and poorly understood communication mediums" across business
  and IT — capabilities describe *what* without exposing *where / why / how*.
- **Sizing:** L1 typically 15–25 foundation capabilities spanning the
  enterprise. L2–L3 for planning. L4–L6 only for IT mapping (out of scope
  for this template).
- **Single map per scope:** *"In one case, we worked with a financial
  institution that had multiple capability maps — one for each business
  unit. There was no effective way to view the business in aggregate."*
  Capabilities appear once and only once for a business.
- **Five common mistakes:**
  1. Confusing capabilities with processes (use the noun-vs-verb test).
  2. Using technical terminology — just because an application automates a capability is no reason to name the capability after the application.
  3. Creating multiple maps for one business.
  4. Allowing redundancy across the map.
  5. Confusing capabilities with organisational units / LOBs.

### Discipline encoded in the template

- **Anti-overlap test** at the per-capability quality-check stage.
- **L1 ≤25 total** sizing recommendation.
- **One map per scope** discipline; if multiple stakeholders want different maps, the scope is wrong.

---

## 3. SAP — Intelligent Enterprise Architecture: Defining Business Architecture

**Used for:** the level definitions (Domain → Area → Capability),
business-IT alignment framing, and the "value-flow" connection between
capabilities and processes.

**Source:** SAP Learning Hub, *Intelligent Enterprise Architecture
Fundamentals — Defining Business Architecture*.
[learning.sap.com/courses/intelligent-enterprise-architecture-fundamentals/defining-business-architecture](https://learning.sap.com/courses/intelligent-enterprise-architecture-fundamentals/defining-business-architecture).

### Key contributions

- **Definition:** business architecture is *"a representation of holistic,
  multi-dimensional business views of the following: capabilities,
  end-to-end value delivery, information, organizational structure,
  relationships among these business views and strategies, products,
  policies, initiatives, and stakeholders."*
- **Capability definition:** *"a particular ability or capacity that a
  business may possess or exchange to achieve a specific purpose or
  outcome… what the business does to generate value independent from how
  software supports it."*
- **Three levels in SAP's reference architecture:** Domain → Area →
  Capability. The template's L0+L1 maps to SAP's Domain→Area; L2 maps to
  SAP's Capability level.
- **Purpose:** capability maps support *"gaining visibility on the as-is and
  to-be operating model"* and *"aligning Business and IT priorities."*

### Discipline encoded in the template

- The L0+L1 (L2-optional) structure aligns with SAP's three-level reference.
- The "business is the owner" framing pushes the BC Map toward business
  stakeholders rather than IT teams.

---

## 4. BABOK® v3 — Stakeholder framing

**Used for:** the BC Map's role as a business-analysis artefact, the
"capability requires people, process, technology, organisation" framing
(BABOK aligns here with TOGAF), and the audience definition (BC Map is
business-owned).

**Source:** *A Guide to the Business Analysis Body of Knowledge® (BABOK®
Guide), v3*, IIBA. Used principally for the stakeholder-engagement framing
already established in the project's persona artefacts.

### Discipline encoded in the template

- Capability ownership is business-side; the soft-link footer references
  personas (built using BABOK §10.43) rather than IT roles.
- The BC Map is read primarily by business analysts and product strategists,
  with IT consumption secondary (FBS is the IT-facing peer).

---

## 5. Cesar Gonzalez — Guide to Define and Describe a Business Capability

**Used for:** the **Business Object + Noun** naming formula and the
capability-vs-process-vs-function-vs-unit decision tree.

**Source:** Cesar A Gonzalez, *Guide to Define and Describe a Business
Capability*, Medium, 2019.
[medium.com/@CAGM/guide-to-define-a-business-capability-cc07e9f81049](https://medium.com/@CAGM/guide-to-define-a-business-capability-cc07e9f81049).

### Key contributions

- **Naming formula:** `Business Object + Noun` where the noun is typically
  Management / Planning / Development / Support / Fulfilment / Assessment.
  Examples: "Customer Management", "Product Development", "Risk Assessment",
  "Order Fulfilment".
- **Distinctions:**
  - Not a Business Process (sequence of activities)
  - Not Technical Functionality (technology should enable, not define)
  - Not a Business Unit (people grouped by reporting line)
  - Not a Business Function (activities grouped by skill)
- **Core test:** a capability represents *what the business can do*;
  processes, functions, and units describe *how it gets done* or *who does
  it*.

### Discipline encoded in the template

- The **noun test** uses Gonzalez's naming formula as the positive criterion.
- The capability-vs-process-vs-function-vs-unit decision tree in the
  internal Claude guidance follows Gonzalez's four-way distinction.

---

## 6. George Miller — The Magical Number Seven, Plus or Minus Two

**Used for:** the L0 sizing heuristic (3–8 items) and the cognitive-load
rationale for why over-decomposition silently destroys a BC Map's usefulness.

**Source:** George A. Miller, *The Magical Number Seven, Plus or Minus Two:
Some Limits on Our Capacity for Processing Information*, Psychological
Review, 1956.

### Discipline encoded in the template

- **L0 = 3–8 items.** Beyond 8, the map exceeds working-memory capacity for
  most readers — the Rosetta Stone stops translating.
- **L1 = 5–12 per L0.** Within each L0 branch, the same cognitive limit
  applies when a reader is focused on one branch.

---

## Summary — what each framework contributes

| Framework | Contributes |
|---|---|
| TOGAF G189 | Capability definition; noun/tech-independence naming; heat-map dimensions; capability ≠ process ≠ function rule |
| Cutter | Single-map-per-scope; anti-overlap discipline; L1 ≤25 sizing; common-mistakes catalogue |
| SAP | Three-level reference (Domain → Area → Capability); business-IT alignment framing |
| BABOK | Business-owned audience; soft-link to personas |
| Cesar Gonzalez | Business-Object-+-Noun naming formula; capability-vs-others decision tree |
| Miller 7±2 | L0 sizing (3–8); cognitive-load rationale |

The template is not "TOGAF capability mapping" or "Cutter capability mapping"
— it is the canonical synthesis. Every section maps back to at least one
source. The Rosetta Stone insight (Cutter) is the soul of the document; TOGAF
provides the rigour; SAP provides the level structure; Gonzalez provides the
naming; BABOK provides the audience framing; Miller provides the sizing.
