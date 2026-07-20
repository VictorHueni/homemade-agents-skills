# Business Model — Logic, Sequence, and Why

This is the plain-English companion to `template.md`. Read this when you need to explain to the user *why* the template has the shape it does, or when you're about to fill a section and want to know what its job is.

The template is **domain-agnostic** — examples below use generic placeholders. Substitute your project's actual market, customers, and currency.

---

## The shape: a 4-step funnel + assumptions + scenarios + price

Every business model answers the same underlying question:

> *"Of all the money / volume / activity out there, how much can we touch, what fraction will we actually convert, what's that worth per customer, and what does that imply for our pricing?"*

That's a funnel. The template makes the funnel explicit:

```
§2 → §3 → §4 → §5         §6           §7
 ▼    ▼    ▼    ▼          ▼            ▼
TOP → FILTER → CONVERT → SEGMENT → SCENARIOS → PRICE
```

## Why each step exists

| Step | What it answers | What you're trying to NOT do |
|---|---|---|
| **§2 Top of funnel** | "What's the total relevant universe?" | Quote a market-size number without saying what *exactly* you're counting. |
| **§3 Filter** | "Of that, what subset actually applies to this mechanic?" | Conflate "total industry spend" with "the subset our product touches". Often a 10× difference. |
| **§4 Conversion rate** | "Of the subset, what fraction flows through today?" | Assume 100% — the gap between "should happen" and "does happen" IS the opportunity. |
| **§5 Segmentation** | "Distributed across which customers?" | Average across the whole market when the top few customers are most of the volume. |
| **§6 Scenarios** | "How sensitive is the answer to the assumptions?" | Pretend you know the conversion rate exactly. |
| **§7 Value capture** | "What does this imply for our pricing?" | Skip the headroom check and propose a price that doesn't survive procurement. |

---

## The two pieces that make it honest

1. **§5.2 "Implicit assumptions" table** — every shortcut you took, listed in one place, marked ✅ or ⚠️ or ❌. Without this, the reader can't tell if your model is right or wrong because they only see the numbers. **This is the most important section in the entire doc.**

2. **§8 "Key unknowns + validation path"** — every gap you couldn't fill, with the specific way to fill it (one interview, one data pull, one search). Stops the model from rotting into "we don't know but we still wrote a confident number anyway."

---

## Why this shape fits multiple model types

The user-facing question changes per model, but the funnel doesn't:

| Model type | §2 Top | §3 Filter | §4 Conversion | §5 Segment |
|---|---|---|---|---|
| **Recovery / restitution** | Total relevant spend | Triggerable subset | Recovery / capture rate | Per customer tier |
| **TAM / SAM / SOM** | All addressable orgs × products | Reachable in N years | Closable in Y1-2 | Per segment ARR |
| **Cost-savings / automation** | Total current-process cost | Automatable case subset | Auto-process / straight-through rate | Per customer savings |
| **Subscription / freemium** | Eligible user count | Free-tier converters | Upgrade-to-paid rate | Per seat / per cohort |
| **Outcome-based contracting** | Total addressable population | Eligible subset | Outcome-success rate | Per provider tier |

**The questions you ask at each step are different, but the shape of the math is identical.** That's why the template is reusable.

---

## The bits that vary per model (intentionally flexible)

- **Number of funnel steps** — 3 (TAM/SAM/SOM), 4 (recovery, savings), or 5+. Template suggests 4 but doesn't enforce.
- **§7 value-capture math** — different per product. Recovery SaaS is "% of recovered value"; subscription is "fixed license × installations"; freemium is "free → paid conversion funnel". Template gives the slot, not the math.
- **§1.x sub-sections** — domain-specific counting gotchas only appear where they matter.

## The bits that DON'T vary (mandatory)

- **Status indicator** at the top (🟢🟡🔲) so a reader knows what's trustworthy.
- **Calculator callout** (variant A if shipped, variant B if planned) so the interactive truth and the doc don't drift.
- **Table of Contents** because models reach 500+ lines and skim-reading matters.
- **§5.1 How-to-read** with ONE worked example, showing the math chain for a single concrete segment.
- **§5.2 Implicit assumptions table** — the doc's quality bar.
- **§6 Scenario matrix** with Conservative / Base / Aggressive — never a single point estimate.
- **§8 Key unknowns** with a specific validation path per row, not vague "TBD".
- **Changelog at the bottom** so frontmatter stays clean as the model evolves.

---

## The sequence you follow when filling a new model

1. **Clone the template** to `docs/business/06a-models/qm-NN-{topic}.md`.
2. **Fill §1 inputs** first — what data do you actually have? Cite each with confidence stars.
3. **Draft §5.2 assumptions** before any numeric figure. List every shortcut you're about to take.
4. **Walk down the funnel** (§2 → §3 → §4 → §5), with each step deriving from the previous one.
5. **§5.1 worked example** picking ONE concrete segment, showing every multiplication.
6. **§6 scenario matrix** by varying the §4 conversion rate (the usually-softest input).
7. **§7 value capture** — your pricing × the §5 per-segment number → headroom.
8. **§8 key unknowns** — what you still need to validate, and how.
9. **Sanity check** against an upstream model (§2 callout) and against external expectation (§6 calibration callout).

---

## Why this discipline matters

Three risks the template prevents:

1. **Misquoted numbers in the pitch deck.** Single point estimates get quoted with false precision. The Scenario matrix forces a range ("X-Y depending on conversion rate") instead of a single number.
2. **Hidden assumption rot.** Six months from now, when a key assumption has been validated, the §5.2 table tells you exactly which row to flip from ⚠️ to ✅ and which downstream numbers to recompute.
3. **Stakeholder confusion across models.** When a reader scans your library of business models, they orient to the §2-§3-§4-§5 funnel in the first one and skim §6-§7 in the rest. Without the template, every model is a new mental model.

The template is intentionally boring — that's its job. The boring shape lets the content (which is specific to each model) be the only thing that varies.
