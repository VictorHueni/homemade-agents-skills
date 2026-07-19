<!-- doc-version: 1.0 | created: {{YYYY-MM-DD}} -->

# {{product_or_scope}} — Competitive Landscape

This document is the strategic analysis of {{product_or_scope}}'s competitive
landscape: industry structure (Porter's Five Forces), competitor tiering
(Direct / Indirect / Substitute / Potential), strategic group clustering,
and positioning (Strategy Canvas + Value Curve). Per Tier-1 competitor,
companion files in this folder carry the per-competitor deep-dive
(`CO-NN-{slug}.md`).

> **Methodology:** built using the canonical synthesis of [Porter's Five
> Forces (1979/80) + Kim & Mauborgne Blue Ocean Strategy (2005) +
> Strategic Group Mapping + SCIP practitioner
> discipline](https://github.com/VictorHueni/homemade-claude-kit/tree/main/business-competitive-landscape/references/methodology-references.md).
> The full bibliography lives with the
> [business-competitive-landscape
> skill](https://github.com/VictorHueni/homemade-claude-kit/tree/main/business-competitive-landscape)
> — single source of truth across every project.

**Industry / scope:** {{industry}}
**Last refreshed:** {{YYYY-MM-DD}}
**Reviewed by:** _TODO_ (cross-functional review — product + sales + finance)
**Next refresh:** {{YYYY-MM-DD + 90 or 180 days}}

**Scope discipline:**
- Captures **current state** of the market. Future projections go in a separate strategic doc.
- Every claim carries `Source:` + `Last verified:` + `Confidence:` ratings.
- Tier-1 (Direct) competitors get their own `CO-NN-{slug}.md` file. Tier-2/3/4 stay in tables below.

**Companion documents:**
- Personas: [link to ../01a-personas.md if exists]
- Business Capability Map: [link to ../03a-capability-map.md if exists]
- Business Model Canvas: [link to ../02a-bmc.md if exists]
- Quantitative models: [link to ../06a-models/ if exists]

---

## Executive summary + strategic implications

*Write last, after the rest of the doc is filled. 3–6 sentences max.
Lead with "so what" — what should we do given this landscape?*

[One sentence: industry attractiveness summary — most-attractive / mixed / unattractive.]

[One sentence: where competitive rivalry concentrates — direct rivals X, Y vs the broader threat from substitute Z.]

[One sentence: positioning verdict — where we stand on the value curve vs Tier-1 competitors.]

[1–2 sentences: strategic implications — what this landscape suggests we should do (Eliminate / Reduce / Raise / Create per Four Actions; defend / expand / pivot per industry attractiveness).]

---

## 1. Porter's Five Forces — Industry Structure

*Rate each force `Low / Medium / High / Very High`. The composite gives industry attractiveness (Low forces = attractive industry to be in).*

| Force | Rating | Rationale | Key drivers | Evidence sources |
|---|---|---|---|---|
| **1. Threat of new entrants** | _Low/Med/High/V.High_ | _1-sentence why_ | _2-4 drivers (capital req'd, regulation, switching cost, brand power, scale economies)_ | _URLs + dates_ |
| **2. Bargaining power of suppliers** | _TODO_ | _TODO_ | _TODO_ | _TODO_ |
| **3. Bargaining power of buyers** | _TODO_ | _TODO_ | _TODO_ | _TODO_ |
| **4. Threat of substitutes** | _TODO_ | _TODO_ | _TODO_ | _TODO_ |
| **5. Industry rivalry (existing competitors)** | _TODO_ | _TODO_ | _TODO_ | _TODO_ |

**Composite industry attractiveness:** _Attractive / Mixed / Unattractive_ — [1-sentence verdict.]

---

## 2. Competitor Tiers

*Per SCIP practitioner discipline, every competitor is assigned to a tier with explicit rationale. Tier-1 (Direct) gets a per-competitor profile file; Tier-2/3/4 stay in this table.*

### Tier 1 — Direct competitors

*Compete on the same value proposition for the same customer segment. Per-competitor deep-dive in `CO-NN-{slug}.md`.*

| Competitor | HQ | Segment served | Value proposition | Profile link | Last verified |
|---|---|---|---|---|---|
| _TODO_ | _TODO_ | _TODO_ | _TODO_ | [CO-NN-{slug}.md](CO-NN-{slug}.md) | _YYYY-MM-DD_ |

### Tier 2 — Indirect competitors

*Solve the same customer job but with a different value proposition (e.g., different category, different business model, different channel).*

| Competitor | Approach | Why indirect (not direct) | Threat horizon | Evidence |
|---|---|---|---|---|
| _TODO_ | _TODO_ | _TODO_ | _Near / Medium / Long_ | _URL + date_ |

### Tier 3 — Substitutes

*Different category but customer could choose them instead. Porter: substitutes often deserve the most attention because they're easy to dismiss.*

| Substitute | What the customer would do instead | Why customers consider it | Switching cost | Evidence |
|---|---|---|---|---|
| _TODO_ | _TODO_ | _TODO_ | _Low / Med / High_ | _URL + date_ |

### Tier 4 — Potential new entrants

*Companies not in the market today but plausibly entering. Watch them; don't fully resource defense.*

| Entrant candidate | Why they might enter | Their advantage if they do | Expected timing | Evidence |
|---|---|---|---|---|
| _TODO_ | _TODO_ | _TODO_ | _TODO_ | _URL + date_ |

---

## 3. Strategic Group Map

*Clusters competitors by similar strategies on 2 carefully-chosen dimensions. See [strategic-group-map.md](strategic-group-map.md) for the full analysis with validation map.*

**Primary dimensions:** [Dimension A] × [Dimension B]

**Groups identified:** [Group 1 name], [Group 2 name], [Group 3 name]

**Our group:** [Which strategic group we belong to, or where we sit between groups]

[Link to full strategic group analysis →](strategic-group-map.md)

---

## 4. Strategy Canvas / Value Curve

*Plots own + Tier-1 competitor value curves across the 5–8 factors of competition. See [value-curve.md](value-curve.md) for the full analysis with Four Actions Framework.*

**Factors of competition:** [Factor 1] · [Factor 2] · [Factor 3] · [Factor 4] · [Factor 5]

**Headline differentiation opportunities** (Four Actions Framework — Eliminate / Reduce / Raise / Create):
- **Eliminate:** [factors no one needs to compete on but everyone does — _TODO_]
- **Reduce:** [factors over-served by all competitors — _TODO_]
- **Raise:** [factors under-served by all competitors that customers actually want — _TODO_]
- **Create:** [factors no one offers but customers would value — _TODO_]

[Link to full value-curve analysis →](value-curve.md)

---

## 5. SWOT (own product relative to competitive landscape)

*High-level summary; per-competitor SWOT lives in each `CO-NN-{slug}.md` file.*

| Dimension | Items |
|---|---|
| **Strengths** | _TODO_ |
| **Weaknesses** | _TODO_ |
| **Opportunities** | _TODO_ |
| **Threats** | _TODO_ |

---

## Changelog

| Date | Mode | Change | Author | Reviewed by |
|---|---|---|---|---|
| {{YYYY-MM-DD}} | Scaffold | Initial scaffold | _TODO_ | _TODO_ |

---

---

# Per-Competitor Profile Template — competitor-{{slug}}.md

*One file per Tier-1 (Direct) competitor. Copy this template; replace placeholders.*

```markdown
<!-- doc-version: 1.0 | created: YYYY-MM-DD | tier: 1 | parent: competitive-landscape.md -->

# Competitor — {{Competitor name}}

Per Tier-1 competitor deep-dive. See parent
[competitive-landscape.md](competitive-landscape.md) for tier
classification + industry-structure context.

**Last verified:** YYYY-MM-DD
**Overall confidence:** Assumed | Tested | Validated
**Reviewed by:** _TODO_

---

## Basics

| Field | Value | Source | Confidence |
|---|---|---|---|
| **HQ location** | _TODO_ | _URL_ | _Assumed/Tested/Validated_ |
| **Founded** | _YYYY_ | _URL_ | _TODO_ |
| **Ownership** | _Public / Private / PE-backed / Subsidiary of X_ | _URL_ | _TODO_ |
| **Employees** | _Range (e.g. 50-200)_ | _URL_ | _TODO_ |
| **Latest funding / revenue** | _If known_ | _URL_ | _TODO_ |
| **Public / regulatory filings** | _Links_ | _TODO_ | _TODO_ |

## ICP / Target segments

*Format each segment as: "[role / firmographic] who [trigger / situation] AND [pain context]". Mirror persona-builder discipline.*

- **Segment 1:** [Specific description]
- **Segment 2:** _TODO_

## Value proposition

*What value the customer gets, not what features the product has. Use the "so that" test.*

- _TODO_

## Go-to-market motion

| Aspect | Approach | Evidence |
|---|---|---|
| **Sales model** | _PLG / Direct / Channel / Hybrid_ | _URL + date_ |
| **Primary channels** | _TODO_ | _URL + date_ |
| **Marketing motion** | _Inbound / Outbound / Brand / Community_ | _URL + date_ |
| **Partnerships** | _TODO_ | _URL + date_ |

## Pricing model

| Aspect | Detail | Evidence |
|---|---|---|
| **Model type** | _Subscription / Usage / Perpetual / Hybrid / Free + Premium_ | _URL_ |
| **Tier range (if public)** | _$X – $Y per [unit] per [period]_ | _URL_ |
| **Discounting / negotiation** | _Standard / Heavy / Custom_ | _URL_ |

## Product / capability scope

*Brief enumeration of what they do. NOT a feature checklist — the value curve handles comparison.*

- _TODO_

## SWOT — relative to **our product**

*Frame as: "[X] is a strength because they can [Y]" / "[X] is a weakness because **we** can [Z]". SWOT must be actionable.*

| Dimension | Items | Confidence |
|---|---|---|
| **Strengths** (relative to us) | _TODO_ | _TODO_ |
| **Weaknesses** (relative to us) | _TODO_ | _TODO_ |
| **Opportunities** (for them) | _TODO_ | _TODO_ |
| **Threats** (they pose to us) | _TODO_ | _TODO_ |

## Strategic implications for us

*1–3 bullets: what does this competitor's existence imply for our strategy? (Defend / expand / pivot / ignore?)*

- _TODO_

## Evidence sources

| Source | URL | Date accessed | Notes |
|---|---|---|---|
| _Company website_ | _URL_ | _YYYY-MM-DD_ | _Pricing page, product page, etc._ |
| _Press release / news_ | _URL_ | _YYYY-MM-DD_ | _TODO_ |
| _Analyst report_ | _URL_ | _YYYY-MM-DD_ | _TODO_ |
| _Regulatory filing_ | _URL_ | _YYYY-MM-DD_ | _TODO_ |
| _Customer interview / sales rep_ | _Internal note_ | _YYYY-MM-DD_ | _TODO_ |

## Changelog

| Date | Change | Source | Confidence change |
|---|---|---|---|
| YYYY-MM-DD | Initial draft | _TODO_ | All Assumed |
```

---

---

# Strategic Group Map Template — strategic-group-map.md

*Created in mode 4 (Strategic mapping). Clusters competitors on 2 strategic dimensions; validates with a second map on different dimensions.*

```markdown
<!-- doc-version: 1.0 | created: YYYY-MM-DD | parent: competitive-landscape.md -->

# Strategic Group Map — {{industry}}

Per-Porter / practitioner discipline, clusters competitors by similar
strategic choices on 2 carefully-chosen dimensions. Companies in the same
group compete more intensely with each other than with companies in
different groups.

**Caveat:** one map can mislead. A second validation map on different
dimensions is mandatory.

---

## Map 1 — Primary view

**Dimension A (horizontal):** [e.g., Price positioning: Low → Premium]
**Dimension B (vertical):** [e.g., Breadth of offering: Narrow specialist → Broad platform]

**Why these dimensions:** [1-sentence — these must be independent + strategic + measurable]

```ascii
       ▲ Broad
       │
       │           [Group 3]
       │            CompetitorE
       │            CompetitorF
       │
       │   [Group 1]
       │    CompetitorA          [Group 2]
       │    CompetitorB           CompetitorC
       │    OURPRODUCT?           CompetitorD
       │
       │
       └────────────────────────────────────────►
       Low                                 Premium
```

### Groups identified (Map 1)

| Group | Members | Shared strategic profile | Intra-group rivalry intensity |
|---|---|---|---|
| **Group 1: [Name]** | _TODO_ | _e.g., "low-cost narrow specialists"_ | _Low / Med / High_ |
| **Group 2: [Name]** | _TODO_ | _TODO_ | _TODO_ |
| **Group 3: [Name]** | _TODO_ | _TODO_ | _TODO_ |

**Our position:** [Which group we belong to, or where we sit between groups, and why.]

---

## Map 2 — Validation view

**Dimension C (horizontal):** [Different from Map 1 — e.g., Geographic scope: Single-country → Multi-region]
**Dimension D (vertical):** [Different from Map 1 — e.g., Vertical integration: Pure SaaS → Bundled hardware-software]

**Why these dimensions:** [1-sentence]

```ascii
[similar ASCII map]
```

### Groups identified (Map 2)

| Group | Members | Shared strategic profile |
|---|---|---|
| _TODO_ | _TODO_ | _TODO_ |

---

## Cross-map analysis

*Which clusters are stable across both maps? Which are artifacts of one
dimension choice? The interesting strategic groups appear consistently in
both views.*

- _TODO_

## Strategic implications

*1–3 bullets: what does the group structure suggest? (Where to play, where to avoid, where the white space is?)*

- _TODO_

## Changelog

| Date | Change | Author |
|---|---|---|
| YYYY-MM-DD | Initial draft | _TODO_ |
```

---

---

# Value Curve / Strategy Canvas Template — value-curve.md

*Created in mode 4 (Strategic mapping). Plots own + competitor value curves across the factors of competition; applies Four Actions Framework.*

```markdown
<!-- doc-version: 1.0 | created: YYYY-MM-DD | parent: competitive-landscape.md -->

# Strategy Canvas / Value Curve — {{product_or_scope}}

Per Kim & Mauborgne's *Blue Ocean Strategy*, plots how the industry
competes and where own product sits relative to Tier-1 competitors. The
horizontal axis captures factors of competition; the vertical axis
captures offering level (Low / Medium / High). Curves reveal positioning
and differentiation opportunities.

---

## Factors of competition (horizontal axis)

*5–8 factors the industry currently competes on and invests in. Derived
from Tier-1 competitor profiles + customer-perceived value drivers.*

1. **[Factor 1]** — _1-sentence what this factor means in this industry_
2. **[Factor 2]** — _TODO_
3. **[Factor 3]** — _TODO_
4. **[Factor 4]** — _TODO_
5. **[Factor 5]** — _TODO_

---

## Value curves (offering level: Low / Medium / High per factor)

| Factor | Own product | Competitor A | Competitor B | Competitor C |
|---|---|---|---|---|
| Factor 1 | _Med_ | _High_ | _Low_ | _Med_ |
| Factor 2 | _TODO_ | _TODO_ | _TODO_ | _TODO_ |
| Factor 3 | _TODO_ | _TODO_ | _TODO_ | _TODO_ |
| Factor 4 | _TODO_ | _TODO_ | _TODO_ | _TODO_ |
| Factor 5 | _TODO_ | _TODO_ | _TODO_ | _TODO_ |

### ASCII curve overlay (optional but illuminating)

```
              Factor1  Factor2  Factor3  Factor4  Factor5
High         ───●─────────────────────────────────●─────  Competitor A
                │                                  │
Medium       ───┼────●─────●──────●─────●──────────┼───  Own
                │    │     │      │     │           │
Low          ───┼────┼─────●──────●─────●───────────┼───  Competitor B
                │    │     │      │     │           │
                Factor1  Factor2  Factor3  Factor4  Factor5
```

*Plot more competitors as needed. ≥3 curves required to reveal patterns.*

---

## Four Actions Framework (Kim & Mauborgne)

*The discipline that breaks mirror-matching. For each action, identify
which factors qualify.*

### 1. Eliminate

*Which factors that the industry takes for granted should be eliminated?
Factors no one really needs but everyone competes on.*

- _TODO_

### 2. Reduce

*Which factors should be reduced well below the industry standard?
Factors over-invested in by all competitors with diminishing returns.*

- _TODO_

### 3. Raise

*Which factors should be raised well above the industry standard?
Factors all competitors under-invest in despite customer value.*

- _TODO_

### 4. Create

*Which factors should be created that the industry has never offered?
True blue-ocean opportunities — new factors of competition.*

- _TODO_

---

## Headline blue-ocean opportunity

*1–2 sentences: where is the white space? What positioning does the
Four Actions analysis suggest?*

- _TODO_

## Strategic implications

*What should we do given the value curves and the Four Actions analysis?
This drives positioning, roadmap priorities, and messaging.*

- _TODO_

## Changelog

| Date | Change | Author |
|---|---|---|
| YYYY-MM-DD | Initial draft | _TODO_ |
```
