<!--
=============================================================================
BUSINESS MODEL TEMPLATE — clone-and-fill
=============================================================================

Purpose: provide a consistent shape for every quantitative business model
under docs/business/06a-models/ (or the project's equivalent directory). Use
this as the starting point for every new model — TAM/SAM/SOM, recovery /
restitution funnels, savings / automation models, customer-ROI calculators,
etc.

How to use:
  1. cp template.md docs/business/06a-models/qm-NN-your-slug.md
  2. Fill placeholders marked {{LIKE_THIS}}
  3. Drop sections that genuinely don't apply (don't pad)
  4. Keep §5 sub-sections (How to read + Implicit assumptions) — those are
     the doc's quality differentiator and are mandatory

The 4-step funnel below is the canonical shape. If your model is a 3-step
funnel (e.g., TAM → SAM → SOM), collapse Steps 2 and 3 into one section.
If it's a 5+ step funnel, add steps. The template doesn't enforce four.

Render-invisible HTML comments like this one carry guidance; markdown
previewers won't show them but they survive in the raw source for the next
author.

Currency: the template uses generic "{{currency}}" placeholders. Substitute
your project's working currency (USD, EUR, GBP, etc.) when filling.
=============================================================================
-->

# {{Model Name}}

> **Phase {{N}} of {{roadmap doc}}** (e.g., `product-roadmap.md`, `gtm-plan.md`, `north-star-strategy.md`, or "none" if standalone)
>
> **Purpose:** {{One sentence — what this model computes and for whom.}}
>
> **Status:**
> - 🟢 Sections {{populated section list}}
> - 🟡 Sections {{partially populated}}
> - 🔲 Sections {{scaffolding only}}
>
> **Key remaining unknown:** {{The single highest-impact validation gap. Be specific.}}
>
> **Validation path:** {{The one interview / data pull / desk-research session that would unblock it.}}

<!--
Status rubric — use these definitions consistently across all models:
  🟢 = all numeric cells filled with cited values; assumptions table populated
  🟡 = some cells _TODO_ but bounded scenarios exist (e.g., conservative/base/aggressive)
  🔲 = pure scaffolding; structure exists, no values yet
-->

<!--
Interactive calculator callout — pick ONE of the two variants below depending
on whether a marimo / notebook / spreadsheet exists for this model. Delete
the unused variant.
-->

<!-- VARIANT A — calculator EXISTS. Use when an interactive tool is already shipped. -->

> **🧮 Interactive calculator:** [`analysis/{{slug}}.py`](../../../analysis/{{slug}}.py) (or wherever your project keeps interactive tools).
> Static export, openable without setup: [`analysis/exports/{{slug}}.html`](../../../analysis/exports/{{slug}}.html).
> Source-of-truth math (unit-tested): [`analysis/{{slug}}_math.py`](../../../analysis/{{slug}}_math.py).
> Drag the sliders to explore alternative scenarios; the §6 scenario matrix below was generated from this tool at base-case settings.

<!-- VARIANT B — calculator NOT YET BUILT. Use when only the markdown model exists. -->

> **🧮 Interactive calculator:** _Not yet built._ Planned to follow the project's existing model-calculator pattern (range sliders for the bounded inputs, scenarios re-rendered live in a per-segment table). For now §6 below is hand-computed from base-case assumptions.

---

## Table of Contents

- [§1 — Inputs and Data Sources](#1-inputs-and-data-sources)
- [§2 — Step 1: {{name of top-of-funnel quantity}}](#2-step-1-name-of-top-of-funnel-quantity)
- [§3 — Step 2: {{name of filter}}](#3-step-2-name-of-filter)
- [§4 — Step 3: {{name of conversion rate}}](#4-step-3-name-of-conversion-rate)
- [§5 — Step 4: Scale by segment](#5-step-4-scale-by-segment)
  - [§5.1 How to read these numbers](#51-how-to-read-these-numbers-math-chain)
  - [§5.2 Implicit assumptions](#52-implicit-assumptions-read-this-before-quoting-any-5-number)
  - [§5.3 Named segments](#53-named-segments)
  - [§5.4 Per-segment scenarios](#54-per-segment-scenarios)
- [§6 — Scenario Matrix](#6--scenario-matrix)
- [§7 — Value capture](#7--value-capture)
- [§8 — Key Unknowns and Validation Path](#8--key-unknowns-and-validation-path)
- [§9 — Related Documents](#9--related-documents)
- [Changelog](#changelog)

---

<!--
§0 GLOSSARY — OPTIONAL.

Include only if your model uses 5+ domain-specific terms that aren't defined
in a central glossary doc. Otherwise link to the central glossary from the
frontmatter and skip §0 entirely. Don't create parallel glossaries.
-->

## 1. Inputs and Data Sources

<!--
Standard input-table format. Confidence stars use a 5-star scale anchored to
the type of evidence backing each value:

  ★★★★★ Primary government / regulator data, or verified internal data
        (with unit tests + sanity-check queries)
  ★★★★  Primary industry data (single-source authoritative — major report,
        vendor regulatory filing, official statistic)
  ★★★   Industry-published, triangulated across multiple independent sources
  ★★    Internal hypothesis / workshop output / vendor marketing —
        directional only, needs external validation
  ★     Anecdote / single-source weak signal — cite with explicit caveat
        and flag in §8 Key Unknowns

If an input itself has a counting-methodology gotcha (different sources
counting different things), give it its own §1.x sub-section.
-->

| Input | Value | Source | Confidence |
|---|---|---|---|
| {{Input name}} | {{Value}} | {{Inline link to source}} | ★★★★ |
| {{...}} | {{...}} | {{...}} | {{...}} |

### 1.1 {{Sub-section for any input that needs methodology explanation — OPTIONAL}}

---

## 2. Step 1 — {{Top of funnel quantity}}

<!--
First step of the funnel. What's the TOTAL relevant quantity before any
filtering? This is the universe of the addressable opportunity.

Examples (replace with your own):
  - Recovery model: total spend that could trigger restitutions / refunds
  - TAM model: total addressable customer count × maximum price tier
  - Savings model: total industry cost of the current manual process

Should produce a single headline figure ({{currency}}, count, or rate).

Add §2.x sub-sections for triangulation, cross-checks, or empirical
brackets when the headline figure has multiple independent sourcings.
-->

| Scenario | Assumption | Estimated value |
|---|---|---|
| Conservative | {{...}} | {{currency}} {{...}} |
| Base | {{...}} | {{currency}} {{...}} |
| Aggressive | {{...}} | {{currency}} {{...}} |

**Assumption rationale:**

{{Walk through how the bracket was derived. Cite sources inline.}}

<!--
SANITY CHECK CALLOUT — RECOMMENDED when this model's §2 derives from another
model. Compare your §2 figure against the upstream model's headline number
and note the ratio. Catches order-of-magnitude errors before they propagate.
-->

**Sanity check vs upstream:** {{Compare this §2 figure against the upstream model it derives from. If the ratio looks wrong, fix the assumption before continuing.}}

### 2.1 {{Triangulation / validation sub-section — OPTIONAL}}

---

## 3. Step 2 — {{Filter}}

<!--
Second step: what subset of the §2 quantity actually counts for this model?

Examples (replace with your own):
  - Recovery model: spend triggerable by the specific recovery mechanism
  - TAM model: reachable / serviceable subset within N years
  - Savings model: subset of cases that are automatable today
-->

| {{Filter dimension}} | Distinct {{units}} | {{Triggers / criteria}} | Est. % of §2 | {{currency}} estimate |
|---|---|---|---|---|
| {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

### 3.1 {{Per-category deep dive — OPTIONAL}}

---

## 4. Step 3 — {{Conversion rate}}

<!--
Third step: what fraction of the §3-filtered quantity flows through today?

Examples (replace with your own):
  - Recovery model: current recovery rate (e.g., 30%/50%/70% bounded)
  - TAM model: closable subset in Year 1-2 (SOM as fraction of SAM)
  - Savings model: % of cases auto-processed today

This is usually the WEAKEST input — flag it explicitly and bracket it with
scenarios. Cite the methodology for picking conservative/base/aggressive.
-->

> **Bounded scenario** (until validated by interview / data pull):

| Scenario | Assumption | Implied result |
|---|---|---|
| Conservative ({{N}}%) | {{...}} | {{...}} |
| Base ({{N}}%) | {{...}} | {{...}} |
| Aggressive ({{N}}%) | {{...}} | {{...}} |

**Why this bracket:** {{cite sources, prior incidents, or analogous benchmarks}}

---

## 5. Step 4 — Scale by segment

<!--
Final step: distribute the §4 result across customer segments. This is
where per-customer / per-tier figures appear.

Mandatory sub-sections:
  §5.1 How to read these numbers — math chain (worked example)
  §5.2 Implicit assumptions table

Optional sub-sections:
  §5.3 Named segments (top N by size)
  §5.4 Per-segment scenarios
-->

### 5.1 How to read these numbers (math chain)

<!--
Walk through the calculation from the §4 result to a per-segment figure,
using ONE concrete worked example. Show every step explicitly with both the
formula and the resulting number.
-->

**Step A — anchor the {{quantity}}.**

{{Source citation + value.}}

**Step B — derive {{intermediate quantity}}.**

```
{{intermediate}} = {{previous}} ÷ {{rate or fraction}}
                 = {{currency}} {{value}}
```

**Step C — slice by {{segmentation dimension}}.**

{{Worked example for one named segment. Show the math.}}

### 5.2 Implicit assumptions (read this before quoting any §5 number)

<!--
THIS SECTION IS MANDATORY. It must be filled BEFORE the model is shown to
any stakeholder, even if other cells are still _TODO_. Without this table
a reader cannot tell if the model's STRUCTURE is right; they only see the
numbers and assume they're trustworthy.

Every assumption that could be wrong gets a row. Be brutally honest.
  ✅ = probably correct, with reason
  ⚠️ = risky oversimplification, with specific failure mode + validation path
  ❌ = known wrong, kept as floor / ceiling pending better data
-->

| # | Assumption | What it implies | Risk |
|---|---|---|---|
| 1 | {{...}} | {{...}} | ✅ Probably right — {{reason}} |
| 2 | {{...}} | {{...}} | ⚠️ {{specific failure mode + how to validate}} |
| 3 | {{...}} | {{...}} | ⚠️ **Probably the most consequential oversimplification.** {{...}} |

**The N assumptions most worth challenging in a stakeholder conversation:** {{list by row #}}.

### 5.3 Named segments

<!--
Concrete map from the model's abstraction (tiers, deciles, cohorts) to the
actual world. List the top N players / segments by size.
-->

| Rank | Segment | Size | % share | Cumulative % | Tier label |
|---|---|---|---|---|---|
| 1 | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

### 5.4 Per-segment scenarios

<!--
The headline per-segment outputs. Format as a table the user can quote from
in a pitch sentence.
-->

| Segment | Size | Headline {{currency}} | Notes |
|---|---|---|---|
| {{...}} | {{...}} | **{{currency}} {{...}}** | {{...}} |

---

## 6. Scenario Matrix — The Pitch Anchor

<!--
3×N matrix: conservative / base / aggressive scenarios × the N segments
you care about. This is what the pitch quotes.

If you have an interactive calculator, note that this table was generated
from it at base-case settings, and re-generation is one command.
-->

> **Target:** a single defensible sentence per segment that the pitch can quote.

| {{Segment tier}} | Conservative | Base | Aggressive |
|---|---|---|---|
| {{...}} | {{currency}} {{...}} | {{currency}} {{...}} | {{currency}} {{...}} |

<!--
CALIBRATION CALLOUT — RECOMMENDED for any model that feeds the investor deck.
Compare your Base-case headline against the external expectation (investor norm,
peer benchmark, industry comparable). If you fall short, the §5.2 assumptions
either need to be more aggressive or the SOM / penetration assumption needs to
be faster. Forces honesty about whether the pitch math actually clears the bar.
-->

**Calibration vs external expectation:** {{What does an investor / peer / comparable benchmark expect to see in this cell? If Base case falls short, what specifically needs to change in §3/§4/§5 to clear the bar?}}

---

## 7. Value capture

<!--
How does the vendor / product monetize the addressable gap? This section
varies most per model because it depends on which product feeds the model.

Standard sub-sections:
  - Uplift assumption (what % of the gap can the product actually capture?)
  - WTP fraction (what fraction of recovered value does the customer pay?)
  - Headroom math (WTP ÷ list price)
  - Pricing sensitivity / band exploration
-->

Anchoring on §4's bounded scenarios:

| | Conservative | Base | Aggressive |
|---|---|---|---|
| {{Industry headline}} | {{currency}} {{...}} | **{{currency}} {{...}}** | {{currency}} {{...}} |
| Per-segment | {{currency}} {{...}} | **{{currency}} {{...}}** | {{currency}} {{...}} |
| Product capture (@ {{N}}% uplift) | {{currency}} {{...}} | **{{currency}} {{...}}** | {{currency}} {{...}} |
| Implied WTP ({{N}}% of capture) | {{currency}} {{...}} | **{{currency}} {{...}}** | {{currency}} {{...}} |
| Headroom vs proposed price | **{{N×}}** | **{{N×}}** | **{{N×}}** |

**Headline pitch sentence (base case):**

> {{One-sentence value prop using the base-case figures.}}

**Sources for the assumptions:**

- Uplift fraction: {{cite the benchmark — comparable vendor, prior project, published case study}}
- WTP fraction: {{cite the benchmark — typical recovery-SaaS ratio, contingency pricing norm, etc.}}
- Proposed price: {{cite the workshop deliverable or pricing decision}}

---

## 8. Key Unknowns and Validation Path

<!--
Honest list of every input that's still a guess. Status emojis:
  🟢 Resolved
  🟡 Bounded by triangulation (good enough for the pitch, not for the deal)
  🟠 Partial — some validation done
  🔴 Blocker — must validate before pitching
  ⚠️ Caveat — acknowledge but accept

Each row should have a concrete next step.
-->

| Unknown | Impact on model | Status | How to resolve | Priority |
|---|---|---|---|---|
| {{...}} | {{High / Medium / Low}} | 🟡 | {{1 interview / 1 data pull / 1 desk-research session}} | {{order}} |

---

## 9. Related Documents

<!--
Upstream (what this model depends on) and downstream (what depends on it).
Use relative links.
-->

- **Upstream:** [{{...}}]({{path}}) — {{relationship}}
- **Downstream:** [{{...}}]({{path}}) — {{relationship}}
- **Companion process doc:** [{{...}}]({{path}}) — {{relationship}}
- **Pitch artefact:** [{{...}}]({{path}}) — {{how the pitch uses this model}}
- **Glossary:** [Methodology terms](glossary.md) — definitions for ARR, CAC, LTV, TAM/SAM/SOM, value-capture ratio, and other methodology-imported terms used across the model set.

---

## Changelog

<!--
Time-stamped findings that materially changed the model. New entries at the
top. Prune entries older than ~12 months or migrate to git history.

Don't promote changelog entries to the frontmatter — they age into noise.
The frontmatter should always show CURRENT state, not historical updates.
-->

### {{YYYY-MM-DD}} — {{One-line summary}}

{{What changed, why, source. Cross-reference to the section(s) affected.}}
