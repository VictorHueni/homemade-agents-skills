# Canvas Discipline — Internal Claude Guidance

This file is **not** copied into the project. It is internal guidance the
skill consults when picking variants, applying anti-patterns, filling
blocks, and triaging cross-doc soft-links.

---

## Variant decision tree — BMC vs Lean Canvas

When the user is uncertain which variant to pick at scaffold:

```
Is the business model largely known + you're documenting / aligning stakeholders?
├── Yes → BMC (Business Model Canvas, Osterwalder/Pigneur 2010)
│         • Used by established businesses, scaling teams, executive strategy
│         • 9 blocks: KP · KA · KR · VP · CR · Ch · CS · CS$ · R$
└── No → BMC is probably wrong; the model is hypothetical
    │
    Is the focus on testing problem-solution fit before scaling?
    ├── Yes → Lean Canvas (Ash Maurya 2010)
    │         • Used by startups, early-stage products, high-uncertainty
    │         • Replaces 4 blocks: Problem / Solution / Key Metrics / Unfair Advantage
    └── No (somewhere in between)
        │
        Most common in this case: start with Lean Canvas to discover, then transfer
        validated insights to a BMC once the model is stable.
        Recommend: Lean Canvas now; convert to BMC later.
```

### Heuristics for the picker

| Project signal | Recommended variant |
|---|---|
| Existing customers + revenue + product in production | BMC |
| Pre-revenue / pre-product / pre-customer | Lean Canvas |
| Pivoting / exploring new segment / new pricing model | Lean Canvas |
| Documenting model for investor / acquirer / strategic plan | BMC |
| Communicating model to operational team / consolidating org-wide understanding | BMC |
| Internal innovation lab / new venture inside a parent company | Lean Canvas (then BMC when matured) |
| Multi-product family with one stable + one experimental product | One BMC per stable product + one Lean Canvas per experimental |

When unsure, ask the user. Don't decide silently.

---

## Block-by-block filling guidance

### Customer Segments — the specificity test

A segment is well-defined if it answers all three:
1. **Who?** (firmographic or demographic — role + organisation type)
2. **What triggers them?** (situation that makes them seek a solution)
3. **What context defines them?** (pain context, decision authority, budget)

| ❌ Bad segment | ✅ Good segment |
|---|---|
| "Customers" | (any of the others below) |
| "Businesses" | "Mid-size B2B SaaS companies (50–500 employees) with revenue between $5M–$50M facing customer churn ≥10%" |
| "Insurance companies" | "Health insurers (200K–2M lives) handling rebate reconciliation manually" |
| "Hospital staff" | "Hospital pharmacy directors managing >5K formulary items + quarterly drug-list updates" |

If the user gives a generic segment, push for specificity. One question:
*"Who specifically? What firmographic / role / trigger / pain defines them?"*

### Value Propositions — the "so that" test

A VP describes value delivered, not features. Test with the construction:
*"Our product does X **so that** the customer can Y"*. The Y is the value.

| ❌ Feature listing | ✅ Value statement |
|---|---|
| "AI-powered platform with NLP" | "Cuts hiring-decision time from 3 weeks to 3 days" |
| "Integrates with Salesforce, HubSpot, Pipedrive" | "Eliminates manual lead-data entry across the team's CRM ecosystem" |
| "Real-time dashboards" | "Surfaces the 3 deals at risk in time to save them" |

If a bullet describes a feature, transform it: "X → so that → Y" and use the Y.

### Channels — distinguish discovery vs delivery vs support

Channels often get conflated. Help the user separate:
- **Discovery channels** — how does the segment find out the product exists? (search, conferences, referrals, paid ads)
- **Evaluation / sales channels** — how do they decide to buy? (demos, free trials, RFP processes, account executives)
- **Delivery channels** — how does the product get to them? (SaaS web, API, in-person, partner integration)
- **Support channels** — how do they get help? (in-app, email, dedicated CSM, community)

A complete Channels block names at least one channel per phase. Single-channel models are fragile.

### Customer Relationships *(BMC)* — types per Osterwalder

Osterwalder's six relationship types (not the only options, but a useful checklist):
1. **Personal assistance** — human-to-human at every interaction
2. **Dedicated personal assistance** — one human is dedicated to one customer / account
3. **Self-service** — no direct interaction; tools / docs do the work
4. **Automated services** — personalised at scale via algorithms
5. **Communities** — peer-to-peer interaction the company facilitates
6. **Co-creation** — customer participates in value creation (reviews, content, configuration)

A canvas often has multiple relationship types across segments — list each.

### Revenue Streams — distinguish recurring vs one-time

| Type | Examples |
|---|---|
| Recurring | Subscription, license, membership, lending interest |
| One-time | Asset sale, transaction fee, brokerage commission, advertising revenue |
| Usage-based | Per-API-call, per-transaction, per-gigabyte |
| Hybrid | Subscription + overage usage tier |

Each revenue stream should name (a) the pricing model, (b) the price point or range, (c) the segment(s) paying.

### Key Resources *(BMC)* — four canonical types

Osterwalder's classification:
1. **Physical** — facilities, machines, distribution networks
2. **Intellectual** — brands, patents, copyrights, partnerships, customer databases
3. **Human** — knowledge workers, sales force, creative teams
4. **Financial** — credit lines, cash reserves, stock options

Most software products lean intellectual + human. Note which type each bullet falls into.

### Key Activities *(BMC)* — three canonical types

1. **Production** — designing, making, delivering a product in substantial quantities or quality
2. **Problem solving** — finding solutions to individual customer problems (consulting, software development)
3. **Platform / network** — operating a platform that connects participants (marketplaces, networks)

Some businesses span multiple types — list each.

### Key Partnerships *(BMC)* — four motivations

1. **Optimisation and economy of scale** — buyer-supplier; reduce cost
2. **Reduction of risk and uncertainty** — alliances in competitive environments
3. **Acquisition of resources / activities** — capabilities one doesn't own
4. **Coopetition** — collaboration with competitors (industry standards, joint ventures)

Each partner should name the motivation.

### Cost Structure — cost-driven vs value-driven

| Type | Description |
|---|---|
| Cost-driven | Minimise cost wherever possible (low-cost airlines, no-frills SaaS) |
| Value-driven | Focus on value creation; premium pricing accepts higher cost (luxury hotels, white-glove consulting) |

Identify which one the model is, then list specific cost items.

### Lean Canvas — Problem block specificity

For Lean Canvas, the Problem block is the foundation. Each problem must:
- Be **specific** ("First-time users abandon during email verification due to 90s delivery delay" — not "slow onboarding")
- Be **verifiable** (a customer would say "yes, that's a real problem")
- Be **prioritised** (rank top 1–3; ignore the long tail)
- Include **existing alternatives** (what customers do today to solve it — Excel macros, intern labour, do nothing)

### Lean Canvas — Solution block discipline

Each solution should:
- Map to ONE specific problem (not aspirational broad solutions)
- Describe the *simplest thing* that solves it (resist over-engineering)
- Be testable (a customer could try a v1 and report whether it helps)

### Lean Canvas — Unfair Advantage discipline

Unfair Advantage is something competitors **can't easily copy or buy**. Practitioner canon: *"insider information, dream team, personal authority, community, existing customers, SEO rankings, etc."*

| ❌ Not an Unfair Advantage | ✅ Real Unfair Advantage |
|---|---|
| "Our team has experience" | "Our CTO wrote the open-source library that 80% of competitors depend on" |
| "We have great UX" | "We have an exclusive 10-year data license from the regulator that no competitor can obtain" |
| "We're cheaper" | "Our cost structure is 60% lower because we co-own the supply chain with our biggest customer" |

If the user says "we don't have one yet", note that honestly. Strategyzer canon: *"if you don't have an unfair advantage today, that's fine — note it and keep building one"*.

### Lean Canvas — Key Metrics

Pirate metrics (AARRR) checklist:
- **Acquisition** — how do users find us?
- **Activation** — do they have a good first experience?
- **Retention** — do they come back?
- **Revenue** — how do we monetise?
- **Referral** — do they tell others?

A complete Key Metrics block names at least one metric per stage relevant to the model.

---

## The 8 anti-patterns — detection cues and fixes

### 1. Vagueness in any block

**Detection:** generic nouns, no specifics, no firmographics, no numbers, no roles.

**Fix:** ask one question to push for specificity (see Customer Segments §above for the format). If the user can't be specific, mark as `Assumed` and add to the changelog as "needs interview / research before pivoting on this".

### 2. Confusing Value Proposition with product features

**Detection:** VP bullets describe the product, not the customer outcome. Listing technology, integrations, UI characteristics.

**Fix:** the "so that" test. Transform each feature bullet into a value bullet.

### 3. Listing org-units as Customer Segments

**Detection:** segment names are internal departments ("Marketing team", "Engineering org", "Operations"). These are *part of a buying organisation*, not segments themselves.

**Fix:** ask "is this a customer organisation, or a department inside one?". If the latter, the segment is the *parent organisation* with the buying decision authority.

### 4. Treating the canvas as a static document

**Detection:** no changelog entries for >90 days, no confidence-rating updates, every block still `Assumed` after months of operation.

**Fix:** prompt the user during refresh mode — what tested / validated since the last update? Add changelog entries even for "no change observed since N interviews".

### 5. Inter-block silos

**Detection:** changes to Customer Segments don't propagate to Value Propositions / Channels / Revenue Streams. A segment is added but no VP, no channel, no revenue stream serves it.

**Fix:** run the inter-block coherence check (trace one segment through every block — every segment must have at least one VP, one channel, one revenue stream). Flag any orphan segments.

### 6. Skipping assumption-testing

**Detection:** all bullets at `Assumed` confidence months into the project. No validation activity referenced in changelog.

**Fix:** identify the riskiest `Assumed` bullets (typically Customer Segments specificity, the first Value Proposition, the first Channel). Recommend testing methods: interviews, prototype tests, smoke tests, MVP launches. Promote confidence as evidence arrives.

### 7. Solo / silent canvas

**Detection:** only one author in the changelog. No "reviewed by" notes. No team discussion artefacts referenced.

**Fix:** Strategyzer canon — *"the canvas is a conversation tool"*. Recommend a canvas review session (15–30 min) with team members representing customer-facing roles, engineering, finance. Each block gets one challenger.

### 8. Mixing current and future state

**Detection:** bullets mixing "today we do X" with "in 2 years we will do Y". Future-state aspirations sneaking into present-state blocks.

**Fix:** one canvas per timeframe. If future-state is important, scaffold a second dated canvas (`business-model-canvas-2027.md`) — explicitly. Cross-link from the current canvas's intro.

---

## When to recommend VPC drill-down

Not every customer segment needs a VPC. Heuristics for when to recommend:

| Recommend VPC | Skip VPC |
|---|---|
| Tier-1 segment (highest revenue or strategic importance) | Tier-2 / Tier-3 / supplemental segment |
| Product-market fit is uncertain for this segment | PMF is well-established |
| Considering a pivot or new VP for this segment | VP is stable |
| Investor / acquirer due diligence on this segment | Operational documentation only |
| Designing a new segment-specific feature | Maintenance of existing features |

In practice: 0–3 VPCs per project. More than 3 segments needing depth = signal the project's scope is too broad; consider splitting the BMC by sub-business.

---

## Confidence promotion rules

Bullets move through confidence states with evidence:

- **Assumed → Tested:** at least one interview, prototype test, smoke test, or analogous experiment has provided some evidence supporting the bullet. Not conclusive but directionally positive.
- **Tested → Validated:** strong evidence — multiple data points, paying customers, traction metrics, repeated wins. Confidence is high; the bullet is unlikely to be wrong.
- **Validated → Tested:** demotion is rare but legitimate when evidence contradicts the previous validation (a segment that paid stops paying, a channel that worked stops working).
- **Tested → Assumed:** rare; usually because the test conditions changed materially.

**Anti-pattern:** promoting to Validated without strong evidence. The default should be conservative — when uncertain, stay at Tested.

---

## Soft-link mapping cheat-sheet

When the corresponding BA artefact exists, the canvas links to it:

| Canvas block | Soft-link target | Format |
|---|---|---|
| Customer Segments | Personas | `[P-NN persona-name](../01a-personas.md#p-nn)` |
| Value Propositions | Value streams + VPCs | `[VS-N stream-name](../04a-value-streams.md#vs-n)` + `[VPC for CS-1](02a-vpc-cs-1.md)` |
| Channels | Value-stream stages | `[VS-N.M stage-name](../04a-value-streams.md#vs-nm)` |
| Customer Relationships *(BMC)* | Support / engagement processes | `[proc-NN-{slug}](../05a-processes/proc-NN-{slug}.md)` |
| Key Activities *(BMC)* | Processes | `[proc-NN-{slug}](../05a-processes/proc-NN-{slug}.md)` |
| Key Resources *(BMC)* | Capabilities | `[C-N.M capability-name](../03a-capability-map.md#c-nm)` |
| Key Partnerships *(BMC)* | (no standard artefact — link to vendor / contract docs if exist) | (free-form) |
| Revenue Streams | Quantitative models | `[TAM/SAM/SOM](../06a-models/...)` |
| Cost Structure | Cost / unit-economics models | `[Cost model](../06a-models/...)` |
| Problem *(Lean)* | Persona pains + VPC | `[Persona pain](../01a-personas.md#p-nn) + [VPC pain](02a-vpc-cs-1.md#pains)` |
| Solution *(Lean)* | FBS functionalities | `[FBS C1.1.F01](../../product-specs/07a-fbs.md#c11f01)` |
| Key Metrics *(Lean)* | Quantitative models | `[Metrics model](../06a-models/...)` |
| Unfair Advantage *(Lean)* | Differentiator-rated capabilities | `[C-N.M (Differentiator)](../03a-capability-map.md#c-nm)` |

Use these formats consistently so cross-doc traceability is mechanical.

---

## Quality checks before saving a canvas update

Run this mentally — don't print into the file:

- [ ] Variant explicitly recorded in header (BMC or Lean Canvas).
- [ ] Each block has 3–7 terse bullets (sticky-note brevity).
- [ ] Customer Segments are specific (firmographic + trigger + context).
- [ ] Value Propositions describe value, not features ("so that" test).
- [ ] No org-units listed as Customer Segments.
- [ ] No current/future-state mixing in any block.
- [ ] Confidence rating present per block; default `Assumed` if not explicit.
- [ ] Soft-links populated only when target artefact exists.
- [ ] Inter-block coherence: every Customer Segment traces to ≥1 VP, ≥1 Channel, ≥1 Revenue Stream.
- [ ] Changelog updated for any refresh (date · block · evidence · cascading effects).
- [ ] None of the 8 anti-patterns survived.

---

## When the user pushes back on the discipline

Acceptable fallbacks:
- Confidence ratings can default to `Assumed` and stay there in v1; the discipline is recording rather than always-validating.
- Soft-links can stay `_TODO_` if BA artefacts don't exist yet.
- VPC drill-down can be deferred — not every segment needs one.

Non-negotiable:
- Variant choice (BMC vs Lean) — must be declared, not mixed.
- Customer Segments specificity — generic nouns are not allowed.
- Value Proposition as value, not features — the "so that" test.
- Sticky-note brevity — 3–7 bullets max per block; depth in linked artefacts.
- One canvas = one timeframe (current OR future, not both).

If the user violates these despite pushback, ship with the violation
flagged in the §Changelog or §Open Items so a future reviewer sees the
compromise. (`Open Items` follows the canonical schema in
the `metamodel` skill's `references/open-items-governance.md`.)
