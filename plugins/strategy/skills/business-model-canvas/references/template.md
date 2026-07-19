<!-- doc-version: 1.0 | created: {{YYYY-MM-DD}} | variant: {{BMC | Lean Canvas}} -->

# {{product_or_scope}} — {{Business Model Canvas | Lean Canvas}}

This document is the strategic-design canvas for {{product_or_scope}}: the
one-page synthesis of customer, value, infrastructure, and financial
logic.

> **Methodology:** built using the canonical synthesis of [Osterwalder &
> Pigneur's Business Model Generation (2010) + Osterwalder's Value
> Proposition Design (2014) + Ash Maurya's Lean Canvas + Strategyzer
> practitioner
> discipline](https://github.com/VictorHueni/homemade-claude-kit/tree/main/business-model-canvas/references/methodology-references.md).
> The full bibliography lives with the
> [business-model-canvas
> skill](https://github.com/VictorHueni/homemade-claude-kit/tree/main/business-model-canvas)
> — single source of truth across every project.

**Variant chosen:** {{BMC | Lean Canvas}}
**Rationale:** [One sentence — typically "BMC because the model is largely known and we're documenting/aligning stakeholders" OR "Lean Canvas because the model is hypothetical and we're discovering/pivoting"]

**Scope discipline:**
- Canvas is **strategic-design**, sticky-note brevity — NOT a feature list, roadmap, sales pitch, or quantitative model.
- Each block has **3–7 bullets**. If a block needs paragraphs, push depth to a companion doc (VPC, BC Map, value-streams).
- Canvas captures **current state**. Future-state aspirations belong in a separate dated canvas.
- Each block carries a **confidence rating** — default `Assumed`; promote with evidence.

**Companion documents:**
- Personas: [link to ../01a-personas.md if exists]
- Business Capability Map: [link to ../03a-capability-map.md if exists]
- Value Streams: [link to ../04a-value-streams.md if exists]
- Business Processes: [link to ../05a-processes/ if exists]
- Quantitative models: [link to ../06a-models/ if exists]
- Value Proposition Canvases: [list of `02a-vpc-{segment}.md` files in this folder]

---

## Confidence legend

| Rating | Meaning |
|---|---|
| **Assumed** | Working hypothesis. No external evidence. The default at first draft. |
| **Tested** | Some evidence accumulated (interviews, prototypes, small experiments). Not yet validated at scale. |
| **Validated** | Strong evidence (market data, paying customers, traction metrics). High confidence. |

---

## The canvas

> NOTE: keep bullets terse. Sticky-note brevity. If a bullet needs explanation, the content belongs in a linked companion doc, not in the canvas.

---

### 1 · Customer Segments

*Who are we creating value for? Who are our most important customers?
Format each bullet as: "[role/firmographic] who [trigger/situation] AND
[pain context]" — never just a generic noun.*

- **CS-1** — [Specific segment description, e.g. "Mid-size health insurers (200K–2M lives) handling rebate reconciliation manually"]
- **CS-2** — _TODO_

**Confidence:** Assumed
**Soft-links:** [Personas P-NN](../01a-personas.md#p-nn) (where defined)

---

### 2 · Value Propositions
> *(Lean Canvas: this is called "Unique Value Proposition")*

*What value do we deliver to each customer segment? Which customer
problems are we solving? What bundles of products and services are we
offering to each segment? "Our product does X **so that** the customer
can Y" — the Y is the value.*

- **VP-1** for [CS-1] — [Value statement: what they get; not what features the product has]
- **VP-2** for [CS-2] — _TODO_

**Confidence:** Assumed
**Soft-links:** [Value streams VS-N](../04a-value-streams.md#vs-n) · [VPC drill-downs](#value-proposition-deep-dives) (where created)

---

### 3 · Channels
*(BMC block — Lean Canvas variant uses the same block)*

*Through which channels do our customer segments want to be reached? Are
we reaching them now? Which channels work best? Which are most
cost-efficient? How are we integrating them with customer routines?*

- [Channel 1 — e.g. "Direct sales via account-executive team"]
- _TODO_

**Confidence:** Assumed
**Soft-links:** [Value-stream stages VS-N.M](../04a-value-streams.md) (customer-facing stages) · [Processes](../05a-processes/)

---

### 4 · Customer Relationships *(BMC only)*

> **BMC variant only.** Lean Canvas replaces this block with §4'
> *Unfair Advantage* — see below.

*What type of relationship does each segment expect us to establish and
maintain? Personal assistance / dedicated / self-service / automated /
communities / co-creation?*

- **For [CS-1]** — [Relationship type, e.g. "Dedicated CSM + monthly business reviews"]
- _TODO_

**Confidence:** Assumed
**Soft-links:** [Processes](../05a-processes/) (support, account-management processes)

---

### 4' · Unfair Advantage *(Lean Canvas only)*

> **Lean Canvas variant only.** BMC uses §4 *Customer Relationships*
> instead.

*What do we have that competitors can't easily copy or buy? Insider
information, dream team, personal authority, community, existing
customers, SEO rankings, etc. Strategyzer canon: "if you don't have an
unfair advantage today, that's fine — note it and keep building one".*

- [Unfair advantage 1]
- _TODO_

**Confidence:** Assumed
**Soft-links:** [Differentiator-rated capabilities in BC Map](../03a-capability-map.md) (where applicable)

---

### 5 · Revenue Streams
*(both variants)*

*For what value are customers really willing to pay? How are they paying
now? How would they prefer to pay? How much does each revenue stream
contribute to overall revenues?*

- [Revenue stream 1 — e.g. "Annual subscription, tiered by users (CHF 12K–60K/yr)"]
- _TODO_

**Confidence:** Assumed
**Soft-links:** [TAM/SAM/SOM / ROI model](../06a-models/) (where exists)

---

### 6 · Key Resources *(BMC only)*

> **BMC variant only.** Lean Canvas replaces this block with §6'
> *Key Metrics* — see below.

*What key resources do our value propositions require? Our distribution
channels? Customer relationships? Revenue streams? Physical / intellectual
/ human / financial?*

- [Key resource 1 — e.g. "Proprietary rule-extraction engine + curated training dataset"]
- _TODO_

**Confidence:** Assumed
**Soft-links:** [Capabilities C-N.M](../03a-capability-map.md) — especially Differentiator-rated

---

### 6' · Key Metrics *(Lean Canvas only)*

> **Lean Canvas variant only.** BMC uses §6 *Key Resources* instead.

*What are the key activities and numbers that tell us we're on track?
Acquisition, Activation, Retention, Revenue, Referral (Pirate metrics
AARRR). North-star metric.*

- [Metric 1 — e.g. "Monthly Active Insurers (MAI)"]
- [Metric 2 — e.g. "Restitution recovery rate"]
- _TODO_

**Confidence:** Assumed
**Soft-links:** [Quantitative models](../06a-models/) where the metrics are computed

---

### 7 · Key Activities *(BMC only)*

> **BMC variant only.** Lean Canvas replaces this block with §7'
> *Solution* — see below.

*What key activities do our value propositions require? Production /
problem-solving / platform-network? Activities that directly enable the
value proposition.*

- [Key activity 1 — e.g. "Monthly LS data ingestion + diff detection"]
- _TODO_

**Confidence:** Assumed
**Soft-links:** [Business processes](../05a-processes/) · [Capabilities](../03a-capability-map.md)

---

### 7' · Solution *(Lean Canvas only)*

> **Lean Canvas variant only.** BMC uses §7 *Key Activities* instead.

*The simplest thing that solves the top problems. List the top features
or capabilities that solve each problem. Resist over-engineering.*

- [Top problem 1] → [Solution 1 — e.g. "Auto-extract limitation rules from XML, surface diff per edition"]
- [Top problem 2] → [Solution 2]
- _TODO_

**Confidence:** Assumed
**Soft-links:** [FBS functionalities](../../product-specs/07a-fbs.md) that realise the solution

---

### 8 · Key Partnerships *(BMC only)*

> **BMC variant only.** Lean Canvas replaces this block with §8'
> *Problem* — see below.

*Who are our key partners? Suppliers? Strategic alliances? Joint ventures?
Coopetition? What key resources / activities are we acquiring from
partners?*

- [Partner 1 — e.g. "Cloud infrastructure: AWS / Azure"]
- [Partner 2 — e.g. "Data licensing: [authoritative source / regulator / industry body]"]
- _TODO_

**Confidence:** Assumed
**Soft-links:** [Vendor contracts / DPAs / partner docs] (where they exist)

---

### 8' · Problem *(Lean Canvas only)*

> **Lean Canvas variant only.** BMC uses §8 *Key Partnerships* instead.

*Top 1–3 problems the customer has today. Each should be specific and
verifiable (someone would say "yes, that's a real problem I have").
Generic statements like "slow processes" don't count.*

- **Problem 1** — [Specific problem with evidence, e.g. "Pharma desk analysts at insurers manually reconcile rebate claims, ~12h/wk per analyst"]
- **Problem 2** — _TODO_
- **Problem 3** — _TODO_

**Existing alternatives:**
- [What customers do today to solve these problems — e.g. "Excel macros + email + intern labour"]

**Confidence:** Assumed
**Soft-links:** [Persona frustrations / pains](../01a-personas.md) · [VPC pain detail](#value-proposition-deep-dives)

---

### 9 · Cost Structure
*(both variants)*

*What are the most important costs inherent in our business model? Which
key resources / activities are most expensive? Fixed vs variable?
Cost-driven vs value-driven?*

- [Cost item 1 — e.g. "Engineering team (8 FTE × CHF 200K = CHF 1.6M/yr)"]
- _TODO_

**Confidence:** Assumed
**Soft-links:** [Cost / unit-economics model](../06a-models/) (where exists)

---

## Value Proposition Deep-dives

*Per-segment Value Proposition Canvases (VPCs) drill into the fit between
each Customer Segment and the Value Proposition serving them. Create one
VPC per Tier-1 segment where understanding the fit deeply matters.*

| Segment | VPC file |
|---|---|
| [CS-1 name] | [02a-vpc-cs-1.md](02a-vpc-cs-1.md) (if created) |
| [CS-2 name] | _TODO_ — run skill in VPC mode to create |

---

## Inter-block coherence check

> *Trace one Customer Segment through the full canvas to verify
> coherence. Repeat for each segment. Document any gaps below.*

**For CS-1 [name]:**
- Reachable via channels: [list channels that serve this segment]
- Relationship type: [CR block entry] *(BMC)* / Unfair advantage: [UA] *(Lean Canvas)*
- Value proposition: [VP-1] addresses [their job/pain]
- Revenue stream: [R-N] captures payment from this segment

If any of these is missing or `_TODO_`, the canvas has a coherence gap.

---

## Changelog

> *Every refresh adds an entry. Date · block(s) changed · evidence
> source · cascading effects on other blocks.*

| Date | Block(s) | Change | Evidence | Cascading effects |
|---|---|---|---|---|
| {{YYYY-MM-DD}} | All | Initial scaffold | _TODO_ | _TODO_ |

---

---

# VPC Companion Template — 02a-vpc-{{segment-slug}}.md

*Use this template for the optional VPC companion file. One file per
customer segment where the value-fit deserves drill-down. Drop this
section when scaffolding the main canvas; it's reproduced separately for
each VPC file the skill creates.*

```markdown
<!-- doc-version: 1.0 | created: YYYY-MM-DD | parent: 02a-bmc.md | segment: CS-N -->

# VPC — {{segment_name}}

This Value Proposition Canvas drills into the fit between Customer
Segment [CS-N] and the Value Proposition serving it. See the parent
[02a-bmc.md](../02a-bmc.md) (or `02a-lean-canvas.md`) for context.

**Segment:** [CS-N · short name]
**Value Proposition:** [VP-N · short name]

---

## Customer Profile

### Customer Jobs
*Tasks customers are trying to perform, problems they're trying to solve,
needs they're trying to satisfy. Functional / emotional / social jobs.
Rank by importance.*

- **J-1 (important)** — [Job description]
- **J-2 (important)** — _TODO_
- **J-3 (moderate)** — _TODO_

### Pains
*Bad outcomes, risks, obstacles. Negative experiences while doing the
job. Rank by intensity.*

- **P-1 (extreme)** — [Pain description]
- **P-2 (moderate)** — _TODO_
- **P-3 (mild)** — _TODO_

### Gains
*Desired outcomes, expected benefits, things that would delight.*

- **G-1 (essential)** — [Gain description]
- **G-2 (expected)** — _TODO_
- **G-3 (unexpected delight)** — _TODO_

---

## Value Map

### Products & Services
*Concrete list of what you offer.*

- **PS-1** — [Product / Service]
- **PS-2** — _TODO_

### Pain Relievers
*How each product / service relieves a specific customer pain. Each pain
reliever should map to a pain in the Customer Profile.*

- **PR-1 → P-1** — [How PS-N relieves Pain N]
- **PR-2 → P-2** — _TODO_

### Gain Creators
*How each product / service creates a specific customer gain. Each gain
creator should map to a gain in the Customer Profile.*

- **GC-1 → G-1** — [How PS-N creates Gain N]
- **GC-2 → G-2** — _TODO_

---

## Fit check

| Customer side | Value side | Fit? |
|---|---|---|
| P-1 [pain] | PR-1 [reliever] | ✅ / ⚠ / ❌ |
| P-2 [pain] | _TODO_ | ❌ — **unaddressed pain** |
| G-1 [gain] | GC-1 [creator] | ✅ |
| G-2 [gain] | _TODO_ | ❌ — **unaddressed gain** |
| _(no pain)_ | PR-3 [reliever] | ⚠ — **unused pain reliever (feature bloat?)** |

**Fit summary:**
- **Unaddressed pains:** [list — product-market-fit gaps]
- **Unaddressed gains:** [list — opportunity for delight]
- **Unused pain relievers / gain creators:** [list — possible feature bloat]

---

## Changelog

| Date | Change | Evidence |
|---|---|---|
| {{YYYY-MM-DD}} | Initial draft | _TODO_ |
```
