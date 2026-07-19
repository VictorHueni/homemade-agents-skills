# Canonical Model Sets

This file is the catalogue the skill consults when the user wants to plan
which quantitative models a project needs — not which single model to build
next, but the **whole set** and the **order to build them in**.

The skill is domain-agnostic, but most projects fall into one of four
**venture shapes**. Each shape has a canonical set of 4–6 models with a
deterministic dependency order. Building them in that order minimises
rework: each model's outputs are the inputs the next model needs.

This file pairs with the **naming convention** documented in `SKILL.md` —
the slug self-documents what the model is for (`qm-1a-customer-roi-model.md`
tells the reader "phase 1, first model, customer ROI" without opening the
file).

---

## How to use this file

The skill enters this file from `mode: catalogue`. The decision tree is:

1. **Detect venture shape** from the project's existing artefacts (Lean
   Canvas / BMC, personas, capability map) and one disambiguation question
   to the user if needed.
2. **Emit the recommended model set** for that shape with the build order
   and DAG.
3. **Flag external gates** — models that cannot be filled until an
   architecture ADR / pilot data / pricing negotiation / regulatory
   approval lands.
4. **Stop.** Do not create any model files in this mode. The user picks
   which model to build first; switching to `mode: build` is a separate
   request.

If the project does not match any of the four shapes below, fall back to
**Shape Z — Standalone / unknown**: scaffold one model at a time without a
canonical set.

---

## Naming-convention recap

Full convention lives in `SKILL.md`. Summary:

```
qm-NN-{topic}.md
```

- **Phase 1** = per-customer value (ROI, pricing, headroom, willingness-to-pay, BoM)
- **Phase 2** = market and projection (TAM/SAM/SOM, ARR curve, GMV growth, units)
- **Phase 3** = cost, operations, and economics (CAC, unit econ, onboarding, channel)
- **Letter** = sequence within phase (`a`, `b`, `c`)
- **Topic** = 1–3 kebab-case words naming what the model computes

**Why this digit order:** *value before market before economics.* You
cannot defend a TAM until you know what one customer is worth; you cannot
target unit economics until you know price × volume; reversing the order
forces you to rebuild upstream models when downstream assumptions change.

---

## Shape A — B2B SaaS pre-pricing *(default)*

**Use when:** the venture sells a subscription or licence for ongoing
product use, to identifiable business customers, with a tiered or
per-seat / per-account pricing model.

**Heuristic detection from project artefacts:**
- Lean Canvas Revenue Streams describes annual / monthly subscription
- Customer Segments are business entities (not consumers)
- Pricing is a per-tier / per-account figure, not a take-rate or unit price

### Recommended model set

| Slug | What it computes | Depends on |
|---|---|---|
| `qm-1a-customer-roi-model.md` | Per-customer (or per-account) CHF value: time saved + revenue uplift + risk avoided, by customer-size tier | — (anchor) |
| `qm-1b-pricing-headroom-model.md` | Proposed price tier ÷ ROI from 1a = value-capture ratio; payback months; sensitivity to tier price | 1a |
| `qm-2a-tam-sam-som-model.md` | Total / Serviceable / Obtainable market in customer count and ARR | 1b (per-customer ARR is the multiplier) |
| `qm-2b-revenue-projection-model.md` | N-year ARR curve: new logos × tier mix × adoption × churn | 1b, 2a |
| `qm-3a-unit-economics-model.md` | CAC, gross margin, payback, LTV/CAC by tier | 1b, 2b, **gated on architecture / cost-base decision** |
| `qm-3b-onboarding-cost-model.md` *(optional)* | Time-to-live and onboarding labour per tier; bottleneck identification | 1a, 3a |

### DAG

```
1a customer-roi
    │
    ▼
1b pricing-headroom ────┐
    │                   │
    ▼                   │
2a tam-sam-som          │
    │                   │
    ▼                   │
2b revenue-projection ◄─┘
    │
    │   [architecture / cost-base
    │    decision must land here]
    ▼
3a unit-economics
    │
    ▼
3b onboarding-cost (optional)
```

### Why this order

- **1a before everything:** every monetisation model needs a per-customer
  CHF figure. Skip this and downstream numbers are anchored to nothing.
- **1b before TAM:** TAM-in-ARR is per-customer ARR × customer count.
  Without a tested price, TAM monetisation is theatre.
- **2a before 2b:** the projection needs a market ceiling. Building
  projection first encourages "hockey stick by assumption."
- **3a gated late:** unit economics depend on infrastructure / serving
  cost shape, which usually depends on an architecture decision the
  project hasn't made yet. Scaffold the structure early; fill the
  numbers once the cost base is locked.
- **3b optional:** important operationally but rarely investor-facing.
  Defer until at least one real onboarding cycle has happened.

### Common skips and tweaks

- **No competitor identified:** skip 2a's top-down TAM; replace with
  a bottom-up **named-account roster** (especially when the market is
  small enough to enumerate by name — under ~200 accounts).
- **Pre-pricing, no signed contract:** 1b becomes the price-negotiation
  artefact, not a standalone calculation. Build 1a and 1b together.
- **Single product, single segment:** drop the per-tier dimension in 1a
  and 1b until segmentation matters.

---

## Shape B — Savings / recovery / restitution

**Use when:** the venture's value lever is recovering money the customer
is currently leaving on the table — unclaimed rebates, overpaid taxes,
unbilled services, leaked revenue, fraud loss.

**Heuristic detection from project artefacts:**
- Lean Canvas Problem block describes a leak / gap / missed-recovery
- Revenue model is contingent (success fee, % of recovered amount) or
  fixed-fee against a quantified leak
- Customer Segments are entities currently losing the recoverable amount

### Recommended model set

| Slug | What it computes | Depends on |
|---|---|---|
| `qm-1a-baseline-leak-model.md` | The volume / CHF of the gap in the current state (volumes × unit value × leak rate) | — (anchor; process-derived) |
| `qm-1b-recovery-rate-model.md` | Recoverable fraction of the baseline leak, segmented by mechanism | 1a |
| `qm-2a-customer-savings-model.md` | Per-customer CHF restitution = leak share × recovery rate | 1a, 1b |
| `qm-2b-tam-savings-model.md` | Total addressable savings = customer count × per-customer savings | 2a |
| `qm-3a-value-capture-model.md` | Vendor share of recovered savings (success fee %, fixed-fee headroom) | 2a |
| `qm-3b-unit-economics-model.md` *(optional)* | CAC, gross margin, payback under the recovery revenue model | 3a |

### DAG

```
1a baseline-leak
    │
    ▼
1b recovery-rate
    │
    ▼
2a customer-savings ─┐
    │                │
    ▼                │
2b tam-savings       │
    │                │
    ▼                │
3a value-capture ◄───┘
    │
    ▼
3b unit-economics (optional)
```

### Why this order

- **Baseline first:** without a defensible leak volume the entire
  funnel is hypothetical.
- **Recovery rate second:** the most consequential assumption in any
  recovery model — almost always wrong on the first pass.
- **Per-customer before total:** the per-customer figure is what the
  sales conversation actually uses; TAM is the investor-facing
  multiplication.
- **Value capture last:** pricing is downstream of the savings number,
  not upstream. Fix the savings first, then negotiate the share.

---

## Shape C — Marketplace / take-rate

**Use when:** the venture operates a two-sided market and earns revenue
as a take-rate on transactions between supply and demand sides.

**Heuristic detection:**
- Lean Canvas Customer Segments describes two distinct sides (e.g.,
  buyers + sellers, riders + drivers)
- Revenue Streams describes a percentage or per-transaction fee
- Key Metrics include GMV, take rate, liquidity (matched fraction)

### Recommended model set

| Slug | What it computes | Depends on |
|---|---|---|
| `qm-1a-gmv-per-transaction-model.md` | Average transaction value × frequency by segment | — |
| `qm-1b-take-rate-headroom-model.md` | Sustainable take-rate vs competitor benchmarks; price elasticity by side | 1a |
| `qm-2a-tam-gmv-model.md` | Total addressable GMV (TAM in transaction volume, not customer count) | 1a |
| `qm-2b-liquidity-projection-model.md` | Supply/demand balance over time; matched fraction by cohort | 1a, 2a |
| `qm-3a-unit-economics-model.md` | Per-side CAC, payback by cohort, cross-side subsidy economics | 1b, 2b |

### Notes

- **Two-sided unit economics:** CAC is segmented by side, not by tier.
  Acquiring supply usually has different economics from acquiring demand.
- **Cold-start asymmetry:** 2b is the most consequential model — most
  marketplace failures are liquidity failures, not pricing failures.
- **No 3b in this shape:** onboarding cost is a per-side concern folded
  into 3a.

---

## Shape D — Hardware / physical product

**Use when:** the venture sells a physical good with a bill of materials,
landed cost, channel margin, and warranty obligations.

**Heuristic detection:**
- Lean Canvas Cost Structure includes BoM / manufacturing / logistics
- Revenue Streams describes unit sales at an MSRP, not a subscription
- Channels include distributors / retailers / direct shipping

### Recommended model set

| Slug | What it computes | Depends on |
|---|---|---|
| `qm-1a-bom-cogs-model.md` | Bill of materials, landed cost per unit, scale curve | — |
| `qm-1b-pricing-headroom-model.md` | MSRP vs perceived value vs BoM; gross margin per unit | 1a |
| `qm-2a-tam-units-model.md` | Addressable unit volume by segment / geography | — |
| `qm-2b-revenue-projection-model.md` | Units × ASP × channel mix over time | 1b, 2a |
| `qm-3a-channel-economics-model.md` | Distributor / retailer margin; direct-vs-channel break-even | 1b, 2b |
| `qm-3b-warranty-cost-model.md` *(optional)* | Service / warranty reserves; failure-rate sensitivity | 1a, 2b |

### Notes

- **Hardware is COGS-first:** unlike SaaS, the cost per unit is a
  primary input, not a downstream concern. 1a comes before everything.
- **Channel economics matter early:** direct-vs-distributor decisions
  shape pricing; build 3a as soon as 1b and 2b exist.
- **Warranty reserves are real money:** ignore at investor's peril
  once the product is in market.

---

## Shape Z — Standalone / unknown

**Use when:** no shape above fits, or the project only ever needs one
quantitative model.

**Workflow:** skip `mode: catalogue` entirely. Go straight to
`mode: build` with the user's specified model purpose. Use the
project's own slug convention if it already has one; otherwise pick a
descriptive kebab-case slug without a phase prefix (e.g.,
`market-sizing-model.md`).

---

## Disambiguation question

If the venture shape is not detectable from project artefacts, ask the
user one question:

> Which best describes how this venture earns revenue?
>
> **a.** Subscription / licence for ongoing product use (B2B SaaS) → Shape A
> **b.** Share of money the customer recovers / saves (success fee, restitution, savings) → Shape B
> **c.** Take-rate on transactions between two sides of a market → Shape C
> **d.** Unit sales of a physical product → Shape D
> **e.** None of the above / one-off model → Shape Z

---

## When to deviate from the canonical set

The canonical sets are starting points, not contracts. Deviate when:

- **The project's strategic question is competitor-specific, not
  market-specific** — replace `qm-2a-tam-sam-som-model.md` with a
  competitor-displacement model anchored to the `business-competitive-landscape`
  output.
- **The market is enumerable by name** (under ~200 accounts) — replace
  top-down `2a` with a bottom-up named-account roster.
- **A pilot client / signed customer exists pre-build** — `1a` becomes
  the deal-closing artefact for that specific customer, then generalises
  to segments.
- **The project is regulated** — add a compliance-cost model (typically
  `3c`) before claiming gross-margin numbers.

Always document deviations in the project's models index so the
absence of a canonical model is intentional, not forgotten.

---

## Cross-reference

- Naming convention details: `../SKILL.md` § Naming convention
- Funnel-shape templates: `template.md`
- Worked examples: `examples.md`
- Step sequence within a single model: `logic-and-sequence.md`
