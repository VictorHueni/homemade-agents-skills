---
name: business-competitive-landscape
license: MIT
description: "Create a competitive-landscape analysis — Porter's Five Forces (industry structure) + Strategic Group Mapping (clustering) + Blue Ocean Strategy Canvas / Value Curve (positioning) + per-competitor profiles (Tier-1 depth). Synthesises Porter (1979/80) + Kim & Mauborgne (2005) + SCIP practitioner discipline. Use when the user asks to analyse competitors, map the competitive landscape, build a competitive intelligence report, score industry attractiveness, identify market positioning, or differentiate from competitors. Triggers on: competitive landscape, competitor analysis, competitive intelligence, Porter five forces, Five Forces, strategy canvas, value curve, strategic group map, competitor profile, competitive positioning, market analysis. Domain-agnostic. Soft-links to personas / capability map / value streams / BMC (BIZBOK Business Architecture stack) but stands alone. NOT a quantitative market-sizing model (use business-quantitative-model for TAM/SAM/SOM)."
user-invocable: true
metadata:
  category: "specification"
  complexity: "high"
  version: "1.0.0"
  status: active
  last_reviewed: 2026-05-29
  impact: "low"
---

# Competitive Landscape Builder

You are an expert at producing **competitive landscape analyses** in the canonical strategy-consulting tradition: **Porter's Five Forces** (industry structure), **Blue Ocean Strategy Canvas + Value Curve** (positioning), **Strategic Group Mapping** (competitor clustering), and **per-competitor profiles** (Tier-1 depth). Synthesises Michael Porter's industry-economics framework, Kim & Mauborgne's value-innovation framework, SCIP (Strategic and Competitive Intelligence Professionals) practitioner discipline, and structured competitive-profile templates.

The artifact produced by this skill is **a folder of markdown documents** at `docs/business/01b-competitive-landscape/`. It is NOT a quantitative market-sizing model (use `business-quantitative-model` for TAM/SAM/SOM), NOT a feature comparison (that's product-marketing material), NOT a sales-positioning deck (that's downstream) — it is **the strategic-analysis layer** that captures industry attractiveness, competitor positioning, and differentiation opportunities, with evidence + confidence + freshness baked in.

This skill is **domain-agnostic**. When activated inside a project, it picks up personas, capability map, value streams, BMC, and quantitative models, and soft-links them into the analysis where applicable.

---

## What a "good competitive landscape" means

A competitive landscape doc is good when a reader can answer, without ambiguity:

| Question | Where it lives |
|---|---|
| **How attractive is this industry?** | Hub doc §Porter's Five Forces (5-row table with rating per force) |
| **Who are our competitors, tiered by threat?** | Hub doc §Competitor Tiers (Direct / Indirect / Substitute / Potential) |
| **Which competitors cluster together strategically?** | `cl-02-strategic-group-map.md` (2-axis cluster diagram with rationale) |
| **How do we position vs them on the dimensions buyers care about?** | `cl-03-value-curve.md` (Strategy Canvas: factors of competition × offering level) |
| **What does Tier-1 competitor X do specifically?** | `CO-NN-{slug}.md` (one file per Tier-1 competitor) |
| **What is each claim's evidence?** | Per-claim `Source: [url]` + `Last verified: YYYY-MM-DD` |
| **How confident are we in each claim?** | Per-claim `Confidence: Assumed | Tested | Validated` |

**Hard scope rules:**
- This skill produces **strategic analysis**, not feature comparison. The unit of analysis is "how this competitor competes for value", not "do they have button X".
- Every claim about a competitor must carry an **evidence source** (URL preferred) + a **last-verified date**. Unverified claims are `Assumed` confidence only.
- The skill captures **current state of the market**. Future projections (where the market is heading) live in a separate strategic analysis or in the BMC.
- The skill does NOT predict competitor moves or scoresheet "who wins" — it surfaces structure and positioning so the user can decide.

---

## The five modes of operation

### Mode 1 — Scaffold

**When:** the project has no competitive-landscape folder yet.

**Output:** ONE file in `docs/business/01b-competitive-landscape/` (or project-chosen folder):
- `cl-01-five-forces.md` — hub document with intro, kit-link methodology pointer, empty Porter Five Forces table, empty Tier table, placeholder sections for strategic-group + value-curve references.

Source from `references/template.md`. Substitute `{{product_or_scope}}`, `{{industry}}` placeholders. Do NOT invent competitors in scaffold mode.

**Do NOT** ship a project-side `methodology-references.md`. The canonical bibliography lives in the skill at `references/methodology-references.md` and is linked from the project doc's header.

### Mode 2 — Industry analysis (Porter's Five Forces + Competitor Tiers)

**When:** the scaffold exists; the user wants to fill the industry-structure layer.

**Step 0 — Clarifying questions (ask BEFORE generating)**

Ask the user the following 4 questions in a single message with lettered options. Users respond like `1A, 2C, 3D, 4B`:

```text
1. Starting competitor list source?
   A. I have a named list — I'll provide the competitors
   B. Discover from project context (source docs, BMC, persona docs)
   C. Discover from market research (analyst lists, G2, Capterra, regulatory filings)
   D. Hybrid — I have some + please discover more

2. Industry pace (drives refresh cadence)?
   A. Fast — consumer tech, AI, fintech, mobile (refresh every 60-90 days)
   B. Medium — B2B enterprise software, professional services (90-180 days)
   C. Slow — regulated, healthcare, insurance, pharma (180-365 days)
   D. Very slow — commodity, infrastructure, capital-intensive (365+ days)

3. Industry / market scope?
   A. Single industry, single geography
   B. Single industry, multi-geography
   C. Multi-industry (some players cross verticals)
   D. Adjacent industries prominent (substitutes are a major axis)

4. Five Forces evidence basis?
   A. I have evidence sources (URLs, reports) for each force — ratings will be Tested/Validated
   B. I have some — others stay _TODO_ / Assumed
   C. Start from scratch — all Assumed; refresh later with evidence
```

If the user gives "Other" or pushes back, ask one follow-up to clarify, then proceed.

**Process:**
1. **Read project context** — source documents (`docs/sources/`), BMC, persona docs, market analysis if any. Identify the industry / scope. **Do not reference delivery PRDs** — they are downstream artefacts that do not yet exist when the competitive landscape is built; cite source documents instead.
2. **Fill Porter's Five Forces** (5-row table in hub doc):
   - For each force: rating (`Low / Medium / High / Very High`), one-sentence rationale, key drivers, evidence sources.
3. **Build competitor tier table:**
   - **Direct** — competes on the same value proposition for the same customer segment.
   - **Indirect** — solves the same job but with a different value proposition.
   - **Substitute** — different category but customer could choose it instead (Porter's "substitutes").
   - **Potential entrants** — not in the market yet but plausibly entering (Porter's "new entrants").
4. **Apply discipline checks** (see `references/landscape-discipline.md`):
   - Every force rating has rationale + evidence
   - Tier classification has explicit reasoning (not just "they sell similar stuff")
   - No vague competitor descriptions ("various startups")

### Mode 3 — Competitor profile (per Tier-1 competitor)

**When:** the hub exists; the user wants to drill into one Tier-1 competitor.

**Process:**
1. **Pick the competitor** — must be one of the Tier-1 Direct or Indirect competitors listed in the hub doc.
2. **Create** `CO-NN-{slug}.md` in the same folder.
3. **Fill the canonical profile** (see `references/template.md` for the structure):
   - **Basics:** HQ, founded year, ownership (public/private/PE-backed/etc), employees, latest funding/revenue if known.
   - **ICP / Target segments:** specific firmographic + role + trigger context (mirrors the persona-builder discipline).
   - **Value proposition:** what value, not what features (mirrors BMC discipline).
   - **Go-to-market motion:** sales model (PLG / direct / channel / hybrid), marketing channels, partnerships.
   - **Pricing model:** subscription / usage / perpetual / hybrid; tier ranges if public.
   - **Product / capability scope:** brief list of what they do — NOT a feature comparison; the value-curve doc handles that.
   - **SWOT:** strengths · weaknesses · opportunities · threats (relative to **your** product).
   - **Evidence sources:** URLs + dates per claim.
   - **Confidence per section:** `Assumed / Tested / Validated`.
   - **Last verified:** YYYY-MM-DD for the whole profile.

### Mode 4 — Strategic mapping (Strategic Group Map + Value Curve)

**When:** the hub has Tier-1 competitors enumerated; the user wants the visual / positioning analyses.

**Process:**
1. **Build Strategic Group Map** (`cl-02-strategic-group-map.md`):
   - Pick 2 strategic dimensions (NOT correlated — e.g., price × breadth-of-offering, NOT price × premium-positioning).
   - Plot competitors as text-based bubbles (ASCII or markdown table with positioning).
   - Identify 2–4 strategic groups (clusters).
   - Per group: name, members, shared strategic profile, group-level rivalry.
   - **Validate with a second map** on different dimensions (per practitioner guidance — one map can mislead).
2. **Build Strategy Canvas / Value Curve** (`cl-03-value-curve.md`):
   - **Horizontal axis:** factors of competition (5–8 factors that this industry competes on and invests in — derived from Tier-1 competitor profiles).
   - **Vertical axis:** offering level on each factor (Low / Medium / High).
   - Plot value curves: own product + 2–4 key competitors.
   - Apply **Four Actions Framework** (Kim & Mauborgne): identify what to **Eliminate**, **Reduce**, **Raise**, **Create** to differentiate from competitor curves.
   - Surface the **Blue Ocean opportunities** — gaps no competitor occupies.

### Mode 5 — Refresh (re-validate stale claims)

**When:** the landscape has aged (>90 days for fast-moving markets; >180 days for slow-moving).

**Process:**
1. **Audit claim freshness** — list every claim with `Last verified` older than the threshold.
2. **Re-verify** each — confirm source still valid, data still current.
3. **Promote / demote confidence** — claims with new evidence move up; claims that contradict reality move down or get retired.
4. **Add changelog entry** — date · what changed · evidence source.

---

## The eight anti-patterns the skill guards against

1. **Listing competitors without tiering** — treating every competitor as equally important. **Fix:** explicit tier assignment with rationale; Tier-1 gets per-competitor profile, Tier-2/3 stay in the hub table.

2. **SWOT-only analysis** — going straight to SWOT without industry-structure analysis (Porter) or positioning (Strategy Canvas). **Fix:** SWOT is one layer; the hub must have industry structure first.

3. **Stale claims without dates** — competitor info that was true 2 years ago and could be wrong now. **Fix:** every claim carries `Last verified: YYYY-MM-DD`; refresh mode flags stale claims.

4. **Vague claims without evidence** — "Competitor X is innovative" with no source. **Fix:** every non-trivial claim links to a primary source (competitor website, press release, regulatory filing, analyst report).

5. **Mirror-matching positioning** ("we do X better") — Blue Ocean's #1 mistake. Competing on the same factors is red-ocean strategy; differentiation requires changing factors. **Fix:** the Four Actions Framework (Eliminate / Reduce / Raise / Create) forces non-mirror thinking.

6. **Ignoring indirect / substitute competitors** — focusing only on direct rivals. The biggest threats often come from substitutes (the iPhone disrupted the camera industry; Tesla disrupted the petrol-engine industry). **Fix:** Tier table requires substitute + potential-entrant rows.

7. **Solo authorship** — competitive intel benefits from team review (sales reps see different things than product managers). **Fix:** the doc has a "Reviewed by" field; skill prompts to involve sales/customer-facing team in refresh cycles.

8. **Missing "so what"** — analysis with no strategic implication. **Fix:** the hub doc's executive summary forces strategic-implication framing ("Given this landscape, our positioning should…").

---

## Inputs

| Needed | What you ask if missing |
|---|---|
| **Project context location** | Look for `docs/business/`. If unclear, ask. |
| **Mode** (scaffold / industry / profile / mapping / refresh) | Detect from request. Confirm if ambiguous. |
| **Industry / scope** | What industry / market is this for? Required for `{{industry}}` substitution. |
| **Competitor list** (modes 2+) | "Which competitors should I tier?" If user doesn't know, suggest desk-research approach (analyst lists, G2/Capterra, customer interviews, regulatory filings). |
| **Tier-1 competitor** (mode 3) | "Which Tier-1 competitor do you want profiled?" Must be in the hub's Tier table. |
| **Strategic dimensions** (mode 4) | "Pick 2 strategic axes for the group map" — offer common pairs (price × breadth, vertical-integration × geographic-scope, etc.). |

Ask 2–4 questions max, single message, lettered options where possible.

---

## Output structure — the canonical artefacts

The skill produces up to 4 markdown files in `docs/business/01b-competitive-landscape/`:

```
competitive-landscape/
├── competitive-landscape.md        ← hub doc — ALWAYS scaffolded first
│                                     · Executive summary + strategic implications
│                                     · Porter Five Forces table
│                                     · Competitor Tier table (Direct / Indirect / Substitute / Potential)
│                                     · Cross-links to strategic-group-map.md + value-curve.md + competitor-*.md files
│                                     · Changelog
│
├── CO-NN-{slug}.md            ← per Tier-1 competitor (mode 3)
│                                     · Basics + ICP + Value Prop + GTM + Pricing + Product scope
│                                     · SWOT (relative to own product)
│                                     · Evidence sources + confidence + last verified
│
├── strategic-group-map.md          ← (mode 4) ASCII / table cluster map
│                                     · 2 strategic dimensions
│                                     · 2–4 strategic groups identified
│                                     · Second validation map on different dimensions
│
└── value-curve.md                  ← (mode 4) Strategy Canvas
                                      · Factors of competition (horizontal)
                                      · Offering level per factor (vertical)
                                      · Own + competitor value curves
                                      · Four Actions Framework (Eliminate / Reduce / Raise / Create)
```

---

## Cross-reference — the architecture-artefact lifecycle

| Competitive-landscape element | Soft-links to |
|---|---|
| Competitor ICPs | Personas (`P-NN`) — overlap signals direct competition |
| Competitor value propositions | BMC Value Propositions block |
| Competitor capabilities | Capability Map (`C-N.M`) — where THEY have a capability YOU lack = differentiator opportunity |
| Competitor revenue / funding | Quantitative model (TAM/SAM/SOM context) |
| Industry rivalry intensity | BMC Customer Relationships (forced churn) + Channels (channel competition) |
| Documentary evidence for factual claims (current workflow, pain) | **Source documents** (`docs/sources/`) — e.g. `[PRD §1.1](../../sources/BlocPlan_PRD_v1.docx)` |

**Soft-link discipline:** mention the ID + name + relative path; don't duplicate content. The competitive landscape stands alone — cross-references add depth.

**Reference direction rule — critical:** the competitive landscape is a **strategic artefact** that sits UPSTREAM of PRDs in the documentation stack. It must NEVER reference a `prd-NNNN-{slug}.md` delivery spec — those are downstream outputs that don't yet exist when the competitive landscape is built. When citing documentary evidence from an internal source (e.g. current-state pain, market claims), reference the **source document** in `docs/sources/` directly:

```markdown
✅ [PRD §1.1 — current workflow pain](../../sources/BlocPlan_PRD_v1.docx) *(internal source)*
❌ [PRD §1.1](../../prd.md)  ← wrong: delivery spec doesn't exist yet; wrong path convention
```

For references to project artefacts, use only upstream or peer artefacts: personas, BC Map, BMC, value streams, quantitative models.

---

## Sizing heuristics

| Element | Recommended count | Source |
|---|---|---|
| Tier-1 (Direct) competitors profiled | 2–6 | Practitioner: deep profiles are expensive; focus on the most consequential |
| Tier-2 (Indirect) in hub table | 3–10 | Broader awareness without per-competitor depth |
| Tier-3 (Substitute) | 2–5 | Porter — substitutes deserve named attention |
| Tier-4 (Potential entrants) | 2–4 | Speculative but important for moat analysis |
| Strategic groups identified | 2–4 | Practitioner: more than 4 = dimensions are too granular |
| Factors of competition on value curve | 5–8 | Kim & Mauborgne: fewer = oversimplified; more = noise |
| Refresh cadence | 90 days (fast markets) / 180 days (slow markets) | SCIP practitioner |

---

## Common patterns to apply

1. **Tier explicitly, not implicitly.** "Direct" vs "Indirect" vs "Substitute" must be assigned with rationale, not assumed. The Tier classification drives investment decisions (who to track closely).

2. **Substitutes deserve their own row.** Porter's #1 insight is that substitutes are often the biggest threat. A taxi company watching other taxi companies missed Uber; a hotel chain watching other hotels missed Airbnb. List substitutes explicitly.

3. **Evidence dates matter more than evidence sources.** A 6-month-old screenshot of a competitor's pricing page is more reliable than a 3-year-old analyst report. `Last verified` is mandatory.

4. **Strategy Canvas with ≥3 competitor curves.** A canvas with own + 1 competitor is symmetric and uninformative. ≥3 reveals patterns and gaps. Aim for own + 2–4 key Tier-1 competitors.

5. **Two strategic group maps, not one.** Single-map analyses mislead. Build one on `price × breadth`, validate with one on `customer-segment × vertical-integration` (or similar). The interesting clusters appear in both.

6. **The Four Actions Framework forces blue-ocean thinking.** "We do X better than them" is red-ocean. The Four Actions (Eliminate / Reduce / Raise / Create) force questions like "what factor that everyone competes on could we drop entirely?" — that's where new market space lives.

7. **Use SWOT relative to own product, not absolute.** A competitor's "weakness" is only useful if it's a gap you can exploit. Frame SWOT items as "[X] is a weakness because **we** can [Y]".

8. **Indirect competitors are not lesser competitors.** They often have the bigger budget + brand and can enter the direct market when motivated. Microsoft was an indirect competitor to Slack until Microsoft Teams launched.

9. **Solo-drafted landscape is fragile.** Sales reps know which competitors customers actually mention; product managers know which threaten the roadmap; finance knows funding patterns. The doc lists "Reviewed by" with date — refresh requires cross-functional input.

10. **The hub doc opens with strategic implications, not data.** A reader skimming the hub should see the "so what" first — what should we do given this landscape? Data tables follow.

---

## Finding the right folder

Default: `docs/business/01b-competitive-landscape/`. Alternatives:
- `docs/business/competition/` (shorter)
- `docs/strategy/competitive-landscape/` when strategy has its own root

**Always check for an existing folder first:**

```bash
find docs -type d -iname "*competitive*" -o -type d -iname "*competition*" 2>/dev/null
```

If a folder exists at a non-default location, use it. If multiple candidates exist, ask. Default and confirm if none.

**Never overwrite existing files.** Switch modes:
- Scaffold mode → skip (report what's there).
- Industry-analysis mode → fill empty cells in existing tables; preserve existing.
- Competitor-profile mode → create new file per competitor; never overwrite.
- Mapping mode → create new files for strategic-group-map.md + value-curve.md.
- Refresh mode → update specific claims with new dates; preserve history in changelog.

---

## Reference materials

Three files in `references/` carry the canonical content:

- **`references/template.md`** — the canonical skeleton: `cl-01-five-forces.md` hub + `CO-NN-{slug}.md` profile + `cl-02-strategic-group-map.md` + `cl-03-value-curve.md`. Copy and fill.
- **`references/methodology-references.md`** — canonical bibliography (Porter 1979/1980, Kim & Mauborgne 2005, SCIP practitioner literature, Strategic Group Mapping consultancy sources). **Lives only in the kit** — never copied to projects.
- **`references/landscape-discipline.md`** — internal Claude guidance: 8 anti-patterns with detection cues, framework decision tree, tiering rules, confidence promotion, sizing heuristics. Never copied to projects.

---

## Closing report to the user

After running any mode, summarise in 4–6 lines:

1. **Mode executed** + **files created or updated** with paths.
2. **Force ratings + tier counts** (industry-analysis mode) — how many Tier-1 / Tier-2 / Tier-3 / Tier-4 identified.
3. **Confidence distribution** — % `Assumed / Tested / Validated`. Flags how much remains hypothetical.
4. **Anti-pattern check** — confirm tiering / evidence / dates / SWOT-relative all clean.
5. **Cross-link opportunities** — which BA artefacts (personas, BC Map, BMC, models) the landscape should soft-link to.
6. **Refresh schedule** — suggest next refresh date based on industry pace.

---

## Checklist

Before declaring the work done:

- [ ] Folder exists or was created.
- [ ] Hub doc `cl-01-five-forces.md` has executive summary + Porter Five Forces + Tier table (scaffold + industry-analysis modes).
- [ ] Methodology pointer in hub header links to the kit's canonical bibliography.
- [ ] Every claim has `Source:` + `Last verified:` + `Confidence:`.
- [ ] Competitor Tiers explicitly assigned with rationale (Direct / Indirect / Substitute / Potential).
- [ ] Per-Tier-1 competitor profile filled with all canonical sections (when in mode 3).
- [ ] Strategic group map has 2 dimensions + 2–4 groups + second validation map (when in mode 4).
- [ ] Value curve has 5–8 factors + own + ≥2 competitor curves + Four Actions analysis (when in mode 4).
- [ ] No anti-patterns survived: tiering / evidence / dates / SWOT-relative / Four Actions / substitutes-listed / reviewed-by / strategic-implications.
- [ ] No project-specific terms baked in (kit version).
- [ ] Open every generated file with the standard artefact frontmatter (OKF-superset block — set `type` to this artefact's `okf_type` display name from the `metamodel` skill's `references/artefact-types-registry.yaml`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`). Run `git config user.name` for `owner`. Set `status: draft` on initial scaffold. Default `review_interval: 90d`. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`.
- [ ] Closing report delivered.
