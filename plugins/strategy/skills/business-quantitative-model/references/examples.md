# Examples — how the template gets filled for different funnel shapes

Two abstract worked examples showing how the template is instantiated for the two most common funnel shapes. The figures and segment names are placeholders — adapt to your project's actual market, currency, and customer base.

---

## Example 1 — 4-step recovery / restitution funnel

**Purpose:** quantify the annual revenue / refund / rebate that customers in a market should be claiming back from suppliers, and how much goes unclaimed today.

| Step | Filled value | Notes |
|---|---|---|
| **§2 Top of funnel** | Total relevant industry spend ≈ {{currency}} {{X}}B (some fraction of broader market) | Validate against multiple independent sources (regulator stats, industry reports, internal data) |
| **§3 Filter** | Triggerable subset by mechanism type: e.g., flat-rebate dossiers + performance-based dossiers + volume-cap dossiers | Counts can come from a verified internal dataset; per-type rates partly TODO |
| **§4 Conversion rate** | Bounded scenario: 30% / **50%** / 70% recovery rate | Often the single biggest unknown; anchor with an industry-published "recovered today" figure if available |
| **§5 Segmentation** | Per-tier breakdown: Large customers (high lives/revenue share) capture {{currency}} {{Y}}M, smaller customers proportionally less | Customer-size proxy stands in for usage proxy (assumption #3 in §5.2) |

### Key §5.2 assumptions seeded

| # | Assumption | Risk |
|---|---|---|
| 1 | Industry-published "recovered" figure reflects all market participants | ✅ Probably right if from an industry association |
| 2 | Base-case conversion rate of 50% is the right central estimate | ⚠️ Biggest single unknown — practitioner interview confirms |
| 3 | Customer-size proxy ≈ revenue / usage share | ⚠️ Often off by ±20%; per-customer usage data resolves |
| 4 | Coverage of the mechanism is uniform across customers | ✅ Mostly true when the mechanism is regulator-mandated |
| 5 | Capture quality is uniform across customer sizes | ⚠️ **Probably the most consequential oversimplification** — larger customers often have dedicated teams with better claim hygiene |
| 6 | Vendor uplift fraction is the right one | ⚠️ Placeholder until validated against a real comparable vendor |

### §6 Scenario matrix (excerpt)

| Segment | Conservative (70% recovery) | Base (50%) | Aggressive (30%) |
|---|---|---|---|
| Large | {{currency}} {{...}} | {{currency}} {{...}} | {{currency}} {{...}} |
| Mid | {{currency}} {{...}} | {{currency}} {{...}} | {{currency}} {{...}} |
| Small | {{currency}} {{...}} | {{currency}} {{...}} | {{currency}} {{...}} |

### §7 Headline pitch sentence (Base case)

> *"A customer with ~10% market share has approximately {{currency}} {{X}}M in annual recovery obligations, recovers ~{{currency}} {{X/2}}M today, and leaves ~{{currency}} {{X/2}}M on the table each year."*

---

## Example 2 — 3-step TAM / SAM / SOM funnel

**Purpose:** quantify a startup's total addressable / serviceable / obtainable market for the investor deck.

| Step | Filled value | Notes |
|---|---|---|
| **§2 TAM** | Total customer count × top-tier annual price → {{currency}} {{X}}M / yr revenue ceiling | Sanity-check vs upstream: ratio against per-customer value model from another internal doc |
| **§3 SAM** | Top N customers reachable in 3 years (~{{X}}% of total market by some proxy) | Concrete named segments preferable to abstract "top N" |
| **§4 SOM** | 2 / 4 / 6 pilots (Bear / Base / Bull) by end of Year 2 | Sales-cycle assumption (typical 12–18 months for B2B SaaS) |
| **§5 Segmentation** | Per-segment ARR: Large 2 × {{currency}} {{A}} + Mid-large 4 × {{currency}} {{B}} + Mid 2 × {{currency}} {{C}} = {{currency}} {{ARR}} steady-state | Long-tail / small segments are often out of SAM at top-tier pricing — flag this honestly |

### Key §5.2 assumptions seeded

| # | Assumption | Risk |
|---|---|---|
| 1 | Top-tier pricing is achievable | ⚠️ Biggest single unknown — procurement interview validates |
| 2 | Warm-intro coverage of named segments | ⚠️ Verify by listing actual named contacts at each target customer |
| 3 | 12–18 month sales cycle | ⚠️ Industry-standard, may not match your specific buyer profile |
| 4 | Long-tail / small segments out of SAM | ✅ Probably right at top-tier pricing |
| 5 | Flat pricing across all customer sizes | ⚠️ Probably wrong; value-based pricing could double TAM |
| 6 | One subscription per customer (no seat expansion) | ✅ Conservative — module bundling could lift ARR/customer by 1.5–2× |

### §6 Calibration vs investor expectation

Typical seed-round investor expectation: {{currency}} {{500K-1M}} ARR by Year 2-3 to justify a {{currency}} {{5-10M}} Series A. If your Base case sits below that threshold, either pricing assumption #1 needs to flex (value-based) or SOM penetration rate needs to be faster.

This callout is forced by the template; without §6's calibration prompt, the gap would have been invisible.

---

## What both examples have in common

1. **§5.2 was the highest-value section** — both surface "the most consequential oversimplification" that wouldn't be in a naive scaffold.
2. **The Base case quotable sentence** in §7 anchors the pitch deck.
3. **Bounded scenarios** in §4 + §6 prevent over-confidence in single point estimates.
4. **Upstream cross-links** make the model's dependencies explicit (a TAM model usually depends on a per-customer value model).
5. **Calculator callout** keeps the markdown narrative and the interactive truth from drifting (Variant A when shipped, Variant B "not yet built" otherwise).

---

## What to copy when filling a new model

If you're writing a **4-step funnel** (recovery / savings / conversion / restitution model), use Example 1 as the structural reference.

If you're writing a **3-step funnel** (TAM/SAM/SOM / market-sizing model), use Example 2.

If you're writing something else (e.g., a 5-step funnel for outcome-based contracting, or a 2-step model for a back-of-envelope), follow the template's section labels but add or collapse steps. The mandatory parts (§5.2 assumptions, §6 scenario matrix, §8 key unknowns, Changelog) stay regardless of funnel length.
