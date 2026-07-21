---
type: skill
name: business-model-canvas
description: "Create a Business Model Canvas (Osterwalder/Pigneur) or Lean Canvas (Ash Maurya) — the strategic-design one-pager that consolidates customer / value / infrastructure / financial logic into 9 inter-connected blocks. Optional Value Proposition Canvas (VPC) companion per customer segment. Synthesises Business Model Generation (2010) + Value Proposition Design (2014) + Running Lean. Use when the user asks to build a business model canvas, BMC, Lean Canvas, value proposition canvas, model the commercial logic, prepare a strategic one-pager for execs/investors. Triggers on: business model canvas, BMC, Lean Canvas, value proposition canvas, VPC, model the business, strategic one-pager, commercial logic, customer-value-infrastructure model. Domain-agnostic. Soft-links to personas / capability map / value streams / processes (the BIZBOK Business Architecture stack) but stands alone. NOT a quantitative model — for TAM/SAM/SOM / ROI / savings use business-quantitative-model instead."
version: "1.0.0"
user-invocable: true
allow_implicit_invocation: true
impact: "low"
metadata:
  category: "specification"
  complexity: "medium"
status: active
last_reviewed: 2026-05-29
---

# Business Model Canvas Builder

You are an expert at producing **strategic-design canvases** in the Osterwalder/Strategyzer tradition: the **Business Model Canvas (BMC)** (Osterwalder & Pigneur, *Business Model Generation*, 2010), the **Lean Canvas** (Ash Maurya, *Running Lean*, 2010), and the **Value Proposition Canvas (VPC)** (Osterwalder, *Value Proposition Design*, 2014).

The artifact produced by this skill is **a markdown document** in the project's business-model folder (default `docs/business/`). It is NOT a quantitative model (TAM/SAM/SOM, ROI, savings — those live in the `business-quantitative-model` skill), NOT a feature spec, NOT a roadmap — it is **the strategic-design one-pager** that consolidates customer + value + infrastructure + financial logic into 9 inter-connected blocks.

This skill is **domain-agnostic**. When activated inside a project, it picks up the project's own personas, capability map, value streams, and processes, and soft-links them into the canvas blocks.

---

## BMC vs Lean Canvas — variant choice at scaffold

The skill produces **one of two canonical variants**, chosen at scaffold time:

| | **Business Model Canvas** *(Osterwalder, 2010)* | **Lean Canvas** *(Ash Maurya, 2010)* |
|---|---|---|
| **Audience** | Established businesses, scaling teams, executive strategy | Startups, early-stage products, high-uncertainty environments |
| **Purpose** | Document and refine a working business model | Test problem-solution-fit assumptions fast |
| **9 blocks** | KP · KA · KR · VP · CR · Ch · CS · CS$ · R$ | Problem · Solution · Key Metrics · Unique Value Prop · Unfair Advantage · Channels · Customer Segments · Cost Structure · Revenue Streams |
| **4 substitutions** vs BMC | — | Problem (↔ Key Partners), Solution (↔ Key Activities), Key Metrics (↔ Key Resources), Unfair Advantage (↔ Customer Relationships) |
| **Block emphasis** | Infrastructure + customer balance | Problem-first; everything emerges from the problem |
| **Pick when…** | The business model is largely known; you're documenting / aligning stakeholders | The model is hypothetical; you're discovering / pivoting |

**Rule:** one project, one canvas variant. Don't mix BMC and Lean blocks in the same doc. If you want both perspectives, create two separate files (e.g., `02a-bmc.md` and `02a-lean-canvas.md`) and cross-link.

The skill asks the user to choose at scaffold. Default suggestion: **BMC for established products, Lean Canvas for early-stage projects** — but the user picks.

---

## What a "good canvas" means

A canvas is good when a reader can answer, without ambiguity:

| Question | Where it lives (BMC) | Where it lives (Lean Canvas) |
|---|---|---|
| **Who do we serve?** | Customer Segments | Customer Segments |
| **What value do we deliver?** | Value Propositions | Unique Value Proposition |
| **What pain does it solve?** | (implicit in VP — drill into VPC) | Problem |
| **How do we solve it?** | (implicit in VP) | Solution |
| **How do we reach customers?** | Channels | Channels |
| **What kind of relationship?** | Customer Relationships | (replaced by Unfair Advantage) |
| **How do we earn?** | Revenue Streams | Revenue Streams |
| **What do we own that's hard to copy?** | (implicit in Key Resources) | Unfair Advantage |
| **What activities are essential?** | Key Activities | (replaced by Solution) |
| **What resources are essential?** | Key Resources | (replaced by Key Metrics) |
| **Who do we rely on?** | Key Partnerships | (replaced by Problem) |
| **What does it cost?** | Cost Structure | Cost Structure |
| **How do we know it's working?** | (implicit) | Key Metrics |

**Hard scope rules:**
- A canvas is the **strategic-design layer** — terse, sticky-note brevity, conversational.
- A canvas is **NOT** a feature list, a roadmap, a sales pitch, a quantitative model, or a PRD.
- Each block has **3–7 terse bullets** (sticky-note brevity). If a block needs paragraphs, the content belongs in a companion doc.
- The canvas captures **current state**. Future-state aspirations belong in a separate dated canvas (e.g., `business-model-canvas-2027.md`).
- Each block carries an optional **confidence rating** — `Assumed / Tested / Validated` — defaults to `Assumed` until evidence accumulates.

---

## The four modes of operation

### Mode 1 — Scaffold

**When:** the project has no canvas folder yet, or has one missing the canonical template.

**Step 0 — Clarifying questions (ask BEFORE generating)**

Ask the user the following 3 questions in a single message with lettered options. Users respond like `1A, 2B, 3C`:

```text
1. Variant?
   A. Business Model Canvas (BMC) — Osterwalder/Pigneur; established business or scaling team
   B. Lean Canvas — Ash Maurya; startup or high-uncertainty environment

2. Canvas timeframe?
   A. Current state only (default — captures how the model works today)
   B. Future state only (captures the aspirational model)
   C. Both — create a current-state + future-state file and cross-link them

3. Existing BA artefacts to pre-populate soft-link slots?
   A. None yet — all soft-link slots stay _TODO_
   B. Some exist — I will check the project (personas, capability map, value streams, processes)
   C. Full BA stack exists — pre-populate all soft-link slots from existing IDs
```

If the user gives "Other" or pushes back, ask one follow-up to clarify, then proceed.

**Inputs needed before generating:**

| Needed | What you ask if missing |
|---|---|
| **Scope name** | "What product / business / venture is this canvas for?" — used for `{{product_or_scope}}` substitution |

**Output:** ONE file (or two if timeframe = Both) in `docs/business/` (or project-chosen folder):
- `02a-bmc.md` (BMC) or `02a-lean-canvas.md` (Lean Canvas) — hub document with intro, kit-link methodology pointer, all 9 blocks scaffolded with `_TODO_` placeholders + confidence ratings + soft-link slots pre-populated where artefacts exist.
- If timeframe = Both: also create `business-model-canvas-future.md` (or `lean-canvas-future.md`) and cross-link the two files in each header.

Source from `references/template.md`. Substitute `{{product_or_scope}}`, `{{variant}}` placeholders. Do NOT invent block content in scaffold mode.

**Do NOT** ship a project-side `methodology-references.md`. The canonical bibliography lives in the skill at `references/methodology-references.md` and is linked from the project doc's header.

### Mode 2 — Fill blocks

**When:** the scaffold exists; the user wants to populate some or all blocks.

**Process:**
1. **Read project context** — If `docs/VISION.md` exists, read it first — the VP blocks must be the commercial expression of the vision, not independent inventions. Then read: PRDs, personas, BC map, value streams, processes, roadmap. The canvas synthesises content that lives in those other artefacts.
2. **For each block the user wants populated:**
   - Write 3–7 terse bullets (sticky-note brevity — NOT paragraphs).
   - Add the confidence rating: `Assumed` (default), `Tested` (some evidence), `Validated` (strong evidence).
   - Add soft-links to other artefacts where applicable (see §Soft-links below).
3. **Apply discipline checks** (see `references/canvas-discipline.md` §"Quality checks"):
   - No anti-patterns survived
   - Block size is sticky-note-terse, not paragraphs
   - Customer Segments are *specific* (not "businesses")
   - Value Propositions describe *value*, not *features*

### Mode 3 — VPC companion (optional, per segment)

**When:** the user wants to drill into one Customer Segment's value-proposition fit using the Value Proposition Canvas.

**Process:**
1. **Pick the segment** — must be one of the segments listed in the main canvas's Customer Segments block.
2. **Create** `02a-vpc-{segment}.md` in the same folder.
3. **Fill the two halves:**
   - **Customer Profile** (the segment's perspective):
     - **Customer Jobs** — what they're trying to accomplish (functional, emotional, social jobs)
     - **Pains** — bad outcomes, risks, obstacles
     - **Gains** — desired outcomes, expected benefits, unexpected delights
   - **Value Map** (your offering):
     - **Products & Services** — what you offer (concrete list)
     - **Pain Relievers** — how each product/service relieves a specific customer pain
     - **Gain Creators** — how each product/service creates a specific customer gain
4. **Test for fit** — every pain reliever should map to a pain; every gain creator should map to a gain. Unaddressed pains/gains = product-market-fit gaps. Unused pain relievers / gain creators = feature bloat.

**Output:** one VPC file per segment. The main BMC.md's Value Propositions block links to each VPC file.

### Mode 4 — Refresh / pivot

**When:** new evidence arrives (interviews, market tests, traction data) and one or more blocks need updating.

**Process:**
1. **Identify the block** — which block(s) need to change?
2. **Update the bullets** with the new content.
3. **Promote / demote confidence** — bullets backed by new evidence can move from `Assumed` → `Tested` → `Validated`.
4. **Add a changelog entry** — date + summary of what changed + evidence source. The canvas is a **conversation tool**, not a static document; history matters.
5. **Check cascading effects** — a change in Customer Segments often cascades into Value Propositions, Channels, Customer Relationships. Block changes ripple.

---

## Soft-links — connecting the canvas to your BA stack

## Block IDs

Each item within a BMC block carries a stable ID — two-letter block prefix + sequential integer. Assign on first mention; never renumber.

| Block | Prefix | Example |
|---|---|---|
| Customer Segments | `CS-N` | `CS-1`, `CS-2` |
| Value Propositions | `VP-N` | `VP-1` |
| Channels | `CH-N` | `CH-1` |
| Customer Relationships | `CR-N` | `CR-1` |
| Revenue Streams | `RS-N` | `RS-1` |
| Key Resources | `KR-N` | `KR-1` |
| Key Activities | `KA-N` | `KA-1` |
| Key Partners | `KP-N` | `KP-1` |
| Cost Structure | `CT-N` | `CT-1` |

**Lean Canvas prefixes:** Problem `PR-N` · Solution `SO-N` · Key Metrics `KM-N` · Unique Value Proposition `UVP-N` · Unfair Advantage `UA-N` · (Channels, Customer Segments, Cost Structure, Revenue Streams share BMC prefixes above).

**Disambiguation note:** `KR-N` (Key Resource) differs from `KR-NN.M` (Key Result from `business-objective`) by the absence of the `.M` sub-number. When citing cross-doc, always include the block name: "Key Resource KR-1" not bare "KR-1".

---

## Soft-links

The canvas is the commercial wrapper around the BIZBOK Business Architecture artefacts. Where they exist, soft-link them:

| Canvas block | Soft-links to |
|---|---|
| **Customer Segments** | Personas (`P-NN`) from `docs/business/01a-personas.md` |
| **Value Propositions** | Value Streams (`VS-N`) from `docs/business/04a-value-streams.md` + Value Proposition Canvases (one VPC per segment) |
| **Channels** | Specific value-stream stages (`VS-N.M`) and process docs |
| **Customer Relationships** | Value-stream stages and process docs (especially support / engagement processes) |
| **Key Activities** | Business Processes from `docs/business/05a-processes/` |
| **Key Resources** | Business Capabilities (`C-N.M`) from `docs/business/03a-capability-map.md` |
| **Key Partnerships** | (No standard artefact — could link to vendor / contract docs if they exist) |
| **Revenue Streams** | Quantitative models from `docs/business/06a-models/` (e.g., TAM/SAM/SOM, savings) |
| **Cost Structure** | Quantitative models from `docs/business/06a-models/` (e.g., unit economics, cost models) |
| **Value Propositions** (downstream) | Business Objectives (`OBJ-NN`) from `docs/business/04b-objectives.md` — VP-NN blocks are the commercial intent that Step 4.5 objectives operationalise. |

**Soft-link discipline:** mention the ID + name + relative path. Don't duplicate the linked artefact's content. The canvas is a one-pager pointing to depth elsewhere.

**Lean Canvas mappings:** Problem ↔ persona pains (via VPC); Solution ↔ FBS functionalities; Key Metrics ↔ business model creator KPIs; Unfair Advantage ↔ (no standard artefact; capability map's `Differentiator`-rated capabilities are the closest fit).

---

## The eight anti-patterns the skill guards against

Lifted from Strategyzer canon + multiple practitioner sources. Run these checks during fill / refresh modes.

1. **Vagueness in any block.** "Customers" is not a segment; "Manufacturing companies with 200–2000 employees needing to diversify revenue away from a single product line" is. Push for specificity.

2. **Confusing Value Proposition with product features.** The VP describes the *value the customer gets*, not the *features the product has*. "We're an AI-powered platform" is a feature; "Cuts hiring-decision time from 3 weeks to 3 days" is a value.

3. **Listing org-units / departments as Customer Segments.** "Marketing" is a department; segments are *customers* (external buyers / users / beneficiaries). Internal org structure belongs in an org chart, not a canvas.

4. **Treating the canvas as a static document.** No changelog, no confidence-rating updates, no refresh after evidence arrives = the canvas dies. The discipline of *updating* matters more than the discipline of *creating*.

5. **Ignoring inter-block dependencies.** A change in Customer Segments cascades into Value Propositions, Channels, Customer Relationships, Revenue Streams. Treating blocks as silos misses the system. Flag cascading effects in changelog.

6. **Skipping assumption-testing.** Every `Assumed` bullet is a hypothesis. The point of the canvas is to **test those hypotheses** and promote them to `Tested` / `Validated`. A canvas where every block stays `Assumed` for months has stopped serving its purpose.

7. **Solo / silent canvas.** Strategyzer's canon: *"the canvas is a conversation tool"*. A solo draft is a starting point; without team review and challenge, it's wishful thinking dressed as strategy.

8. **Mixing current and future state.** "We sell SaaS subscriptions (current) and will pivot to usage-based pricing (future)" in the same Revenue Streams block produces a canvas that's neither accurate nor aspirational. Use one canvas per timeframe; cross-link them.

---

## Inputs

| Needed | What you ask if missing |
|---|---|
| **Folder location** | Default `docs/business/`. Ask if alternative. |
| **Variant** (BMC / Lean Canvas) | Required at scaffold. Suggest based on project type (BMC for established; Lean for startup) but user picks. |
| **Scope name** | What product / business / venture? Used for `{{product_or_scope}}` substitution. |
| **Other artefact existence** | Check for `01a-personas.md`, `03a-capability-map.md`, `04a-value-streams.md`, `05a-processes/`. If absent, soft-links will be `_TODO_`. |
| **Block to fill / refresh** (mode 2 / 4) | Which block(s)? Single, multiple, or "all"? |
| **Segment for VPC** (mode 3) | Which Customer Segment to drill into? |

Ask 2–3 questions max, single message, lettered options where possible.

---

## Output structure — the fixed template

- Open every generated file with the standard artefact frontmatter (OKF-superset block — set `type` to this artefact's `okf_type` display name from the `metamodel` skill's `references/artefact-types-registry.yaml`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`). Run `git config user.name` for `owner`. Set `status: draft` on initial scaffold. Default `review_interval: 90d`. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`.

The skill produces ONE markdown file per canvas + optional VPC companion files. Full templates in `references/template.md`. Structure for the main BMC file:

```
<!-- doc-version: 1.0 | created: YYYY-MM-DD | variant: BMC | Lean Canvas -->

H1: {{product_or_scope}} — Business Model Canvas (or Lean Canvas)

Intro paragraph:
  - Variant declaration + rationale (why BMC vs Lean Canvas)
  - Hard scope rules (canvas is strategic-design; not features / roadmap / quant)
  - Kit-link methodology pointer
  - Companion docs (BIZBOK BA stack, quantitative models, VPCs)

§Confidence legend — Assumed / Tested / Validated

§The canvas (9 blocks)
  For each block:
    - Block name + brief one-line description
    - 3-7 bullets (terse; sticky-note brevity)
    - Confidence rating (Assumed default)
    - Soft-links to other artefacts where applicable

§Value Proposition deep-dives
  - List of VPC companion files (one per segment, if created)

Open items: no local section (ADR-0005). File unresolved work directly to the central
ledger via `util-open-items`, citing this canvas as `Source artefact` with `Source anchor`
= the canvas block ID (e.g. `#cs-1`, `#vp-2`) and `Source heading` = the full block name.
Schema + lifecycle: the `metamodel` skill's `references/open-items-governance.md`.

Changelog
```

VPC companion file structure (separate file per segment):
```
H1: VPC — {{segment_name}}
§Customer Profile (Jobs / Pains / Gains)
§Value Map (Products & Services / Pain Relievers / Gain Creators)
§Fit check (does each pain reliever map to a pain? does each gain creator map to a gain?)
```

---

## Common patterns to apply

1. **Customer Segments must be specific.** Format: "[role/firmographic] who [trigger/situation] AND [pain context]". One generic noun is never a segment.

2. **Value Propositions describe value, not features.** Try the "so that…" test: *"Our product does X **so that** the customer can Y"*. The "Y" is the value.

3. **Each block has 3–7 bullets, no more.** Sticky-note brevity is the discipline. If a block needs more, it's actually two blocks or there's depth that belongs in a VPC / linked artefact.

4. **Confidence ratings move over time.** `Assumed` is the start; promote when evidence arrives. A canvas with all bullets stuck at `Assumed` after 90 days is signal that testing has stopped.

5. **The canvas is one page.** Print it on one page (real paper or one screen). If it doesn't fit, it's too verbose. Strategyzer canon.

6. **Inter-block consistency check.** Customer Segment A's Value Proposition must be reachable via the Channel(s) listed and produce Revenue Stream(s) listed. Trace one segment through the full canvas to verify coherence.

7. **VPC drill-down per high-stakes segment.** Not every segment needs a VPC — only the ones where understanding the value-fit deeply matters (your Tier-1 segments).

8. **Lean Canvas needs more discipline on Problem.** The Problem block must list 1–3 specific top problems, not generic statements. "Slow onboarding" is generic; "First-time users abandon during email verification due to 90s delivery delay" is a problem.

9. **Changelog every refresh.** Don't silently edit. Each refresh entry: date · block(s) changed · evidence source · cascading effects.

10. **Print and stick on a wall.** Strategyzer canon: the canvas is meant to be seen, debated, marked up. A markdown file in a repo is the archive; the working copy lives where the team can see it.

---

## Sizing heuristics

| Element | Recommended | Source |
|---|---|---|
| Customer Segments per canvas | 1–3 (more = split canvas) | Strategyzer practitioner |
| Value Propositions per canvas | 2–4 max | Strategyzer practitioner |
| Bullets per block | 3–7 | Sticky-note discipline |
| Active canvases per project | 1 current + optional 1 future-state | Anti-confusion rule |
| VPCs per project | 0–3 (one per Tier-1 segment) | Practitioner |

**If any number exceeds these,** reconsider:
- Too many segments → split into multiple canvases (one per market / vertical)
- Too many VPs → either segments are too coarse OR the offering is too broad; consider focus
- Bullets per block growing → push depth into linked artefacts; canvas stays terse

---

## Cross-reference — the architecture-artefact lifecycle

The canvas sits at the **commercial-strategy layer**, consolidating the BIZBOK BA stack and pointing at quantitative models:

| Layer | Owns | Canvas relationship |
|---|---|---|
| **Personas** | Who | Customer Segments soft-link by P-NN |
| **Capability Map** | What abilities | Key Resources soft-link by C-N.M |
| **Value Streams** | How value flows | Value Propositions + Channels soft-link by VS-N |
| **Processes** | Operational how | Key Activities soft-link to process docs |
| **FBS** | What product does | (No direct link; Solution in Lean Canvas hints) |
| **Business Model Canvas** *(this skill)* | Commercial logic | — |
| **VPC** *(this skill, optional)* | Segment value-fit | Drills into Value Propositions block |
| **Quantitative models** | Numbers (TAM/SAM/SOM, ROI) | Revenue Streams + Cost Structure soft-link to `docs/business/06a-models/` |

### Soft-reference principle

The canvas references other artefacts as pointers, not as dependencies. It must stand alone — readers shouldn't need to read 5 other docs to understand the canvas. Cross-references add depth, not prerequisites. Build the canvas even if other BA artefacts don't yet exist.

---

## Finding the right folder

Default: `docs/business/`. Alternatives:
- `docs/strategy/business-model-canvas/` when strategy has its own root.
- `docs/business/canvases/` when multiple canvases (BMC + Lean + Mission Model + …) co-exist.

**Always check for an existing folder first:**

```bash
find docs -type d -iname "*business-model*" -o -type d -iname "*canvas*" 2>/dev/null
```

If a folder exists at a non-default location, use it — don't move existing work without explicit user request. If multiple candidates exist, ask. If none, default and confirm.

**Never overwrite an existing canvas file.** Switch modes if it exists:
- Scaffold mode → skip (report what's there).
- Fill mode → append/update bullets in the targeted block(s); preserve existing.
- VPC mode → create a new VPC file per segment; never overwrite.
- Refresh mode → update specified block(s); add changelog entry.

---

## Reference materials

Three files in `references/` carry the canonical content. Read when needed:

- **`references/template.md`** — the canonical canvas skeleton (both BMC + Lean Canvas variants, plus VPC companion template). Copy to `{folder}/...` and fill placeholders.
- **`references/methodology-references.md`** — canonical bibliography (Osterwalder/Pigneur, Osterwalder VPC, Maurya Lean Canvas, Strategyzer resources, practitioner anti-pattern catalogues). **Lives only in the kit** — never copied to projects. Project docs link here via the 2-line pointer in their header.
- **`references/canvas-discipline.md`** — internal Claude guidance: variant decision tree, block-by-block filling guidance, 8 anti-patterns with detection cues, confidence-promotion rules. Never copied into the project.

---

## Closing report to the user

After running any mode, summarise in 4–6 lines:

1. **Mode executed** + **files created or updated** with paths.
2. **Variant chosen** (BMC / Lean Canvas) and rationale.
3. **Blocks filled vs `_TODO_`** — counts.
4. **Confidence distribution** — how many `Assumed` / `Tested` / `Validated` — flags how much remains hypothetical.
5. **Anti-pattern check** — confirm no vagueness / feature-listing / org-unit-as-segment / static-doc / sibling-block-conflict.
6. **Cross-link opportunities** — which BA artefacts (personas, capability map, value streams, processes, quant models) the canvas should soft-link to.

---

## Checklist

Before declaring the work done:

- [ ] Folder exists or was created.
- [ ] Variant explicitly chosen + recorded in doc header.
- [ ] Canvas file exists with all 9 blocks scaffolded (scaffold mode).
- [ ] Methodology pointer in header links to the kit's canonical bibliography.
- [ ] Each filled block has 3–7 terse bullets + confidence rating.
- [ ] Customer Segments are specific (not generic nouns or org units).
- [ ] Value Propositions describe value, not features.
- [ ] No current / future state mixing.
- [ ] Changelog updated for any refresh.
- [ ] VPC companion(s) created when explicitly requested (mode 3).
- [ ] Soft-links populated only when target artefact exists.
- [ ] No project-specific terms baked in (kit version).
- [ ] Closing report delivered.
