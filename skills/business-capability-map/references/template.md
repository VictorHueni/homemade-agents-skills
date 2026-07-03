<!-- doc-version: 1.0 | created: {{YYYY-MM-DD}} -->

# {{product_or_scope}} — Business Capability Map

This document is the strategic "what" layer for {{product_or_scope}}: the
stable hierarchy of business capabilities (L0 + L1, with L2 only where
genuinely extensive). It does NOT contain features, functionalities, user
stories, or code organisation — those belong in the Functional Breakdown
Structure (FBS), a peer artefact that soft-references this map by capability
ID.

> **Methodology:** built using the canonical synthesis of [TOGAF G189 + Cutter "BC Map as Rosetta Stone" + SAP Business Architecture + BABOK + Cesar Gonzalez naming + Miller 7±2 sizing](https://github.com/VictorHueni/homemade-claude-kit/tree/main/business-capability-map/references/methodology-references.md). The full bibliography and framework synthesis live with the skill that generated this doc — single source of truth across every project.

**Scope discipline:**
- Capabilities answer "what does the business do?" — stable, technology-independent, noun phrases.
- L0 = the organising axis (declared below).
- L1 = the actual capabilities (5–12 per L0; ≤25 total).
- L2 = sub-capabilities, **only** when an L1 has ≥5 genuinely distinct sub-domains.
- No features, no functionalities, no code paths, no tool names — those live in the FBS.

**Companion documents:**
- Personas: [link to 01a-personas.md if exists]
- FBS: [link to functional-breakdown-structure if exists]
- Value streams / journeys: [link if exists]
- Processes: [link to docs/business/05a-processes/ if exists]

---

## L0 axis declaration

**Chosen axis:** {{L0_axis_label}}

*Options the project considered: product/service family · value stream ·
capability domain/theme · line of business · customer segment · geography ·
custom. The chosen axis shapes how every reader navigates the map; the
rationale below explains why this axis fits this scope.*

**Rationale:** [One sentence explaining why this axis was chosen over the alternatives.]

**L0 items:**

- **C1** — [Name of first L0 item]
- **C2** — [Name of second L0 item]
- **C3** — [Name of third L0 item]
- _(3–8 total — Miller's 7±2 cognitive limit)_

---

## Global overview

```
{{product_or_scope}}
│
├── C1 · [L0 item 1 name]
│   ├── C1.1 · [L1 capability name]
│   ├── C1.2 · [L1 capability name]
│   └── C1.3 · [L1 capability name]
│
├── C2 · [L0 item 2 name]
│   ├── C2.1 · [L1 capability name]
│   ├── C2.2 · [L1 capability name]
│   ├── C2.3 · [L1 capability name]
│   │   ├── C2.3.1 · [L2 sub-capability — only if extensive]
│   │   └── C2.3.2 · [L2 sub-capability]
│   └── C2.4 · [L1 capability name]
│
└── C3 · [L0 item 3 name]
    ├── C3.1 · [L1 capability name]
    └── C3.2 · [L1 capability name]
```

---

## Capability index

*Single canonical table covering every L1 capability. Strategic Importance:
`Differentiator` (where the business wins or loses) · `Necessary` (required
for operation; not a winning edge) · `Commodity` (could be outsourced /
templated without strategic loss).*

| ID | Name | L0 parent | Strategic Importance | One-line definition |
|---|---|---|---|---|
| C1.1 | [Capability name] | C1 · [L0 name] | _Differentiator / Necessary / Commodity_ | [One-line definition] |
| C1.2 | [Capability name] | C1 · [L0 name] | _TODO_ | _TODO_ |
| C2.1 | [Capability name] | C2 · [L0 name] | _TODO_ | _TODO_ |
| ... | | | | |

---

## C1 · [L0 item 1 name]

*Brief description of this L0 item — what unifies the capabilities below it.*

### C1.1 · [Capability name]

**Definition:** [1–2 sentence outcome statement. Business language. Example:
"Provides the ability to register, validate, and maintain customer master
data across the customer lifecycle, ensuring a single authoritative record
per legal entity."]

**Business object:** [The entity this capability operates on — one noun. E.g., Customer, Order, Claim, Asset.]

**Strategic importance:** **[Differentiator | Necessary | Commodity]**
[One-line rationale: e.g., "Differentiator — the precision of our customer-data layer is what unlocks the personalisation our competitors can't replicate."]

**Outcomes:**
- [Outcome 1 — what this capability produces or enables, outcome-oriented]
- [Outcome 2]
- [Outcome 3]
- [Optional outcome 4]

**Boundaries (what this is NOT):**
- [Boundary 1 — what the capability deliberately does NOT cover. Example: "Does NOT cover customer-facing communications — that lives in C2.3 Customer Engagement."]
- [Boundary 2]

**Maturity (optional):** [Initial | Developing | Defined | Managed | Optimising]
[Skip this field if the project isn't ready to assess maturity honestly.]

**Soft-links:**
- *Personas served:* [P-xx](../01a-personas.md#p-xx-name), [P-yy]
- *Value streams enabled:* [VS-x](../04a-value-streams.md#vs-x)
- *Operationalised by processes:* [proc-NN-{slug}](05a-processes/proc-NN-{slug}.md)
- *FBS row:* [C1.1 in FBS](../../product-specs/07a-fbs.md#c11)

---

### C1.2 · [Capability name]

**Definition:** _TODO_

**Business object:** _TODO_

**Strategic importance:** _TODO_

**Outcomes:**
- _TODO_

**Boundaries:**
- _TODO_

---

## C2 · [L0 item 2 name]

### C2.1 · [Capability name]

[Fill following the C1.1 pattern.]

### C2.3 · [Capability name with L2 sub-capabilities]

**Definition:** _TODO_

**Business object:** _TODO_

**Strategic importance:** _TODO_

**Outcomes:**
- _TODO_

**Boundaries:**
- _TODO_

#### L2 sub-capabilities

*L2 is broken out here because C2.3 covers ≥5 genuinely distinct
sub-domains. If you find yourself adding L2 to most L1s, lift the content
into L1 or move feature-grain detail into the FBS.*

##### C2.3.1 · [Sub-capability name]

**Definition:** _TODO_

##### C2.3.2 · [Sub-capability name]

**Definition:** _TODO_

---

## C3 · [L0 item 3 name]

[Fill following the C1 pattern.]

---

## Changelog

| Date | Change | Author |
|---|---|---|
| {{YYYY-MM-DD}} | Initial scaffold | _TODO_ |
