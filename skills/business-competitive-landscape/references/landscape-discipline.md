# Competitive Landscape Discipline — Internal Claude Guidance

This file is **not** copied into the project. It is internal guidance the
skill consults when applying anti-patterns, framework decisions,
competitor tiering, confidence promotion, and freshness audits.

---

## The 8 anti-patterns — run on every fill / refresh

### 1. Listing competitors without tiering

**Symptom:** the hub doc has a flat list of 15 competitors with no
classification. Every competitor gets equal attention; resources are
spread thin; the highest-threat competitors don't get the deep analysis
they deserve.

**Fix:** force explicit Tier assignment with rationale.
- **Tier 1 (Direct):** same value prop + same segment → per-competitor profile
- **Tier 2 (Indirect):** same job, different value prop → hub-table row
- **Tier 3 (Substitute):** different category, same customer choice → hub-table row
- **Tier 4 (Potential entrant):** plausible future entrants → hub-table row

If the user can't articulate WHY a competitor is Tier 1 vs Tier 2, the
tiering is wrong.

### 2. SWOT-only analysis

**Symptom:** the report opens with SWOT and stops there. No industry
structure, no positioning analysis, no group clustering.

**Why it's wrong:** SWOT is downstream of industry analysis. SWOT items
make sense only when you know which forces are squeezing the industry.

**Fix:** Five Forces first; tiering second; strategic groups + value
curve third; SWOT is one layer in the per-competitor profile, not the
whole report.

### 3. Stale claims without dates

**Symptom:** competitor info that "was true" 2 years ago is presented
as current. The competitor's pricing, headcount, or product scope may
have changed completely.

**Fix:** every claim carries `Last verified: YYYY-MM-DD`. Refresh mode
(mode 5) audits all claims; anything older than 90 days (fast markets)
or 180 days (slow markets) gets re-verified.

### 4. Vague claims without evidence

**Symptom:** "Competitor X is innovative" / "Competitor Y has poor UX" /
"Competitor Z lost market share recently" — no source.

**Why it's wrong:** unverifiable claims become folklore. The strategic
decision built on them is fragile.

**Fix:** every non-trivial claim has `Source:` with a URL or named
internal note. Primary sources beat secondary; secondary beats none.

| Source quality | Examples |
|---|---|
| ⭐⭐⭐⭐⭐ Primary, recent | Competitor's website (with timestamp), press release, SEC filing, regulatory document, founder interview |
| ⭐⭐⭐⭐ Secondary, triangulated | Multiple analyst reports agreeing, customer interviews (≥3 independent) |
| ⭐⭐⭐ Single secondary | One analyst report, one customer interview |
| ⭐⭐ Internal team knowledge | Sales-rep observation, customer success report |
| ⭐ Anecdote / single weak signal | "Someone heard" — cite with caveat, mark `Assumed` |

### 5. Mirror-matching positioning ("we do X better")

**Symptom:** the positioning analysis says "we have faster onboarding"
or "we have better integration". The product competes on the same
factors as everyone else, just claiming to do them better.

**Why it's wrong:** this is **red-ocean strategy** (Kim & Mauborgne).
Marginal differentiation is fragile — competitors match it within
quarters. True differentiation changes WHICH factors matter, not the
LEVEL on existing factors.

**Fix:** apply the Four Actions Framework in `cl-03-value-curve.md`:
- What can we **Eliminate** that everyone competes on but no one needs?
- What can we **Reduce** below industry standard (less is more)?
- What can we **Raise** dramatically above industry standard where
  customers actually care but everyone under-invests?
- What can we **Create** that doesn't exist as a factor today?

If the answer to all four is "nothing", the positioning IS red-ocean
and the strategic question is whether to compete in this market at all.

### 6. Ignoring indirect / substitute competitors

**Symptom:** the report lists 5 direct competitors and stops. No
substitutes, no potential entrants.

**Why it's wrong:** Porter's #1 strategic insight. Substitutes often
become the biggest threat:
- Cameras lost to smartphones (substitute, not Canon vs Nikon)
- Taxis lost to ride-sharing (substitute, not Uber vs Lyft initially)
- Hotels lost to home-sharing (substitute, not Marriott vs Hilton)
- Print newspapers lost to social media (substitute, not NYT vs WaPo)

**Fix:** Tier 3 (Substitutes) and Tier 4 (Potential entrants) rows are
mandatory in the hub doc. If they're empty, the analysis isn't
finished.

### 7. Solo authorship

**Symptom:** one person drafted the entire report. No "Reviewed by"
field; no cross-functional input.

**Why it's wrong:** competitive intel is multi-functional knowledge.
Sales reps know what customers actually mention in evaluations. Product
managers know which competitors threaten the roadmap. Finance knows
funding patterns. Marketing knows positioning gaps. A single-author
report misses what each function sees.

**Fix:** the `Reviewed by` field is required. Refresh cycles (mode 5)
prompt the user to circulate the draft to sales / product / finance for
input before declaring complete.

### 8. Missing "so what"

**Symptom:** the report has tables of competitor data, force ratings,
group clusters, value curves — but no strategic implication. A reader
finishes without knowing what to do.

**Why it's wrong:** a competitive landscape that doesn't drive a
strategic decision is a research artefact, not a strategy artefact.

**Fix:** the hub doc's Executive Summary forces strategic-implication
framing:
- Industry attractiveness verdict → defend / expand / pivot
- Tier-1 rivalry concentration → where to invest in differentiation
- Strategic group structure → where to play, where to avoid
- Value curve gaps → which Four Actions move to make
- 1–2 specific recommendations for the team

---

## Framework decision tree — when to invoke which mode

```
Has the user asked for a full landscape?
├── Yes → Scaffold (mode 1), then Industry analysis (mode 2), then iterate.
└── No
    │
    Are they asking specifically about industry attractiveness?
    ├── Yes → Industry analysis mode 2 (Porter Five Forces)
    └── No
        │
        Are they asking about one competitor's specifics?
        ├── Yes → Competitor profile mode 3 (per-competitor deep-dive)
        └── No
            │
            Are they asking about positioning / differentiation?
            ├── Yes → Strategic mapping mode 4 (group map + value curve)
            └── No
                │
                Are they asking to refresh / update stale info?
                └── Yes → Refresh mode 5
```

### When to invoke Strategic Mapping (mode 4)

Mode 4 (Strategic Group Map + Value Curve) is expensive. Only invoke
when:
- ≥3 Tier-1 competitors profiled (need enough data points)
- User has a positioning question to answer (vs just inventorying competitors)
- Product is mature enough that "where to position" is the real question (not "what to build")

For early-stage products with 1–2 competitors, defer mode 4 until the
landscape has more clarity.

---

## Competitor tiering — decision tree

When triaging a competitor candidate, work through:

```
Does this competitor sell the same value proposition to the same customer segment?
├── Yes → TIER 1 (Direct)
│         → Create CO-NN-{slug}.md profile
│
└── No
    │
    Does this competitor solve the same customer job, with a different value proposition?
    ├── Yes → TIER 2 (Indirect)
    │         → Hub table row only
    │
    └── No
        │
        Is this a different category that customers might choose instead?
        ├── Yes → TIER 3 (Substitute)
        │         → Hub table row; consider deep substitute analysis if threat is high
        │
        └── No
            │
            Could they plausibly enter this market within 12-24 months?
            ├── Yes → TIER 4 (Potential entrant)
            │         → Hub table row; watch, don't deeply resource
            │
            └── No → NOT A COMPETITOR
                    (Out of scope for this landscape; revisit if context changes)
```

### Tier-1 overload

If more than 6 competitors qualify as Tier 1, the scope is wrong:
- Either the market is too broadly defined (sub-segment it)
- Or the value proposition is too generic (sharpen it)
- Or you're in a hyper-fragmented industry that needs Strategic Group analysis FIRST to surface meaningful sub-groups

---

## Strategic Group Mapping — dimension selection

Per practitioner guidance, the 2 dimensions chosen for the map make or
break the analysis. They must be:

1. **Independent** — not correlated. Plotting `price × premium-quality`
   is useless because they're the same axis. Plot `price × breadth-of-
   offering` instead — those genuinely vary.
2. **Strategic** — reflect a real strategic choice (not a tactical
   feature). Vertical-integration is strategic; "has SSO" is not.
3. **Measurable** — you can place each competitor on it with evidence.
4. **Tied to economics or customer value** — moves should affect
   profitability or buyer choice.

### Common dimension pairs

| Dimension A | Dimension B | When to use |
|---|---|---|
| Price positioning (Low → Premium) | Breadth of offering (Narrow → Broad) | Default starting pair; almost always informative |
| Vertical integration (Pure SaaS → Bundled) | Geographic scope (Single → Multi-region) | When supply chain or ops vary |
| Customer segment (Mass → Premium) | Distribution (Direct → Channel) | When GTM motion varies |
| Service intensity (Self-service → White-glove) | Technology approach (Off-shelf → Proprietary) | When delivery model varies |

### Validation map discipline

Always build a second map on different dimensions. The interesting
strategic groups appear in BOTH maps; clusters that only show in one
map are dimension-choice artifacts, not real strategic groups.

---

## Confidence promotion rules

Same pattern as `business-persona` and `business-model-canvas`:

- **Assumed → Tested:** at least one piece of evidence supports the
  claim. Source link present but limited (e.g., one analyst report).
- **Tested → Validated:** multiple independent sources agree. Or direct
  evidence (their pricing page, signed customers, regulatory filing).
- **Tested → Assumed (demotion):** when refresh discovers the evidence
  was stale or wrong.

### Refresh cadence by industry pace

| Industry pace | Refresh cadence | Examples |
|---|---|---|
| **Fast** (consumer tech, fintech, AI) | 60–90 days | SaaS, mobile apps, AI tools |
| **Medium** (enterprise software, B2B) | 90–180 days | CRM, ERP, security tools |
| **Slow** (regulated, capital-intensive) | 180–365 days | Healthcare regulation, insurance, pharma, utilities |
| **Very slow** (commodity, infrastructure) | 365+ days | Cement, steel, electricity grid |

---

## Per-section depth — when to go deep vs stay shallow

### Hub doc

- Five Forces: 5 rows, ~50 words rationale per force. Don't write essays.
- Tier table: tight rows; depth lives in per-competitor profile files (Tier 1).
- Executive summary: 3–6 sentences. Strategic implications, not data dump.

### Per-competitor profile

- Tier 1 only — 2–6 profiles total per landscape.
- Each profile: 500–1,500 words. More = bloat; less = inadequate.
- SWOT must be relative to OWN product, not absolute.

### Strategic group map

- 2 maps minimum (validation discipline).
- ≤4 strategic groups per map. More = dimensions too granular; re-think.

### Value curve

- 5–8 factors of competition. <5 = oversimplified; >8 = noise.
- ≥3 competitor curves (own + ≥2 competitors). With only 1 competitor, the canvas is symmetric and uninformative.
- Four Actions: minimum 1 item per action (Eliminate / Reduce / Raise / Create). If all 4 are "nothing", the positioning IS red-ocean — surface that honestly.

---

## Quality checks before saving a landscape update

Run this mentally — don't print into the file:

- [ ] Hub doc has executive summary with strategic implications.
- [ ] Porter Five Forces filled with ratings + rationale + evidence.
- [ ] Competitor Tier table has all 4 tiers (Direct / Indirect / Substitute / Potential) — none empty.
- [ ] Every claim has Source: + Last verified: + Confidence:.
- [ ] Per Tier-1 competitor profile filled (mode 3): basics + ICP + value prop + GTM + pricing + SWOT + sources.
- [ ] SWOT items framed relative to OWN product (not absolute).
- [ ] Strategic group map has 2 maps on different dimensions (mode 4).
- [ ] Value curve has ≥3 curves + Four Actions filled (mode 4).
- [ ] `Reviewed by` field is not empty (cross-functional input expected).
- [ ] None of the 8 anti-patterns survived.
- [ ] Refresh date set in the future based on industry pace.

---

## When the user pushes back on the discipline

Acceptable fallbacks:
- Tier 3 + Tier 4 rows can stay `_TODO_` initially if market is well understood
- SWOT can default to all Assumed initially
- Per-competitor profiles can be deferred (start with hub doc + Tier-1 table rows; profile later)
- Strategic mapping (mode 4) can be deferred until ≥3 Tier-1 profiles exist
- Cross-functional review can be a follow-up TODO

Non-negotiable:
- Five Forces ratings must have rationale + evidence (not just ratings)
- Competitor Tiers must be explicit (Direct / Indirect / Substitute / Potential)
- No claim without Source: + Last verified:
- Executive summary must have strategic implications, not just data summary
- Four Actions Framework (when in mode 4) — at least 1 item per action

If the user ships with violations, flag them in the Changelog so a
future reviewer sees the compromise.

---

## Open-items governance stance — Changelog-only for now

The competitive landscape is **deliberately not part of the formal `Open Items` rollout**
in the current governance increment. Unresolved work (claims awaiting verification,
deferred per-competitor profiles, missing strategic-group ratings) is captured in the
existing `## Changelog` section together with the date, evidence source, and reviewer.

Rationale:

- Competitive intel evolves continuously and most "open" items are *evidence-freshness*
  questions, not the four governance categories (`doc-gap` / `decision-gap` /
  `execution-item` / `tech-debt`) defined in
  [`rules/open-items-governance.md`](../../rules/open-items-governance.md) §2.
- The artefact already enforces `Source:` + `Last verified:` on every claim, which acts
  as a per-claim freshness ledger that the central `docs/project-control/open-items/`
  ledger would only duplicate.
- The per-competitor profile, value curve, and Five Forces sections are themselves
  rebuilt on every refresh wave, so the `Changelog` captures the meaningful change set.

When governance items of the four canonical types *do* arise (for example, a deferred
ADR on whether to enter a substitute-product category), file them directly to the
central ledger (`docs/project-control/open-items/`) citing this artefact or the relevant
ADR as `Source artefact` — never inline in this document. This stance is re-evaluated
after one rollout cycle; if competitive intel accumulates governance items that do not
fit the existing artefacts, this rule is revisited.
