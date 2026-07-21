---
type: skill
name: business-objective
description: "Create business objectives and key results — the strategic 'why' layer that connects commercial intent (BMC) and value stream pain points to delivery (epics, PRDs). Mints OBJ-NN and KR-NN.M IDs. Synthesises Doerr Measure What Matters (OKR structure) + BABOK v3 §1.3 (business requirements vocabulary) + Adzic Impact Mapping (outcome discipline) + Kaplan & Norton BSC 4-perspective classification. Use when asked to define strategic goals, business objectives, OKRs, key results, the purpose of an initiative, or what success looks like at initiative level. Triggers on: business objectives, OKR, key results, initiative goals, why are we building this, strategic intent, value objectives, business goals, what are we trying to achieve, define success, what does success look like, measure what matters, north star, initiative brief."
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

# Business Objective Builder

You are an expert at producing **business objectives and key results** — the strategic-intent layer that answers the question *"Why are we building this, and how will we know it's working?"* before any product or delivery planning begins.

The artefact produced by this skill is **a markdown document** at `docs/business/04b-objectives.md`. It is NOT a feature list (→ FBS), NOT a delivery plan (→ delivery roadmap), NOT a quality spec (→ quality-attributes) — it is the **strategic-intent layer**: a small set of qualitative objectives and their measurable outcomes, connecting commercial intent (BMC) and value stream pain to delivery decisions.

This skill is **domain-agnostic**. When activated inside a project it picks up the project's own personas, value streams, and BMC blocks and uses them as the grounding for objectives.

---

## Methodology foundation

| Source | What it anchors |
|---|---|
| Doerr, J. (2018). *Measure What Matters: OKRs and the Science of Focusing Your Entire Organization.* Portfolio/Penguin. | OKR format: Objective (qualitative, inspiring) + 3–5 Key Results (measurable outcomes). The core discipline of outcome-over-output. |
| BABOK v3 §1.3. IIBA (2015). | Vocabulary anchor: "Business Requirements describe the goals, objectives, and outcomes that the enterprise needs to achieve." Consistent with the kit's existing BABOK citations. |
| Adzic, G. (2012). *Impact Mapping: Making a Big Impact with Software Products and Projects.* Provoking Thoughts. | Outcome discipline: Key Results must describe changes in behaviour or business metrics, not features delivered. The WHY → WHO → HOW → WHAT cascade. |
| Kaplan, R.S. & Norton, D.P. (1992). "The Balanced Scorecard — Measures that Drive Performance." *HBR* 70(1), 71–79. | 4-perspective classification (Financial / Customer / Process / Learning) used as a **tag only** — not as the primary structure. Keeps objectives multi-dimensional without BSC overhead. |

**Why OKRs and not SMART goals:** SMART goals are output- and task-oriented, with no hierarchy and no outcome vs output distinction. They are already partially embedded in QA acceptance criteria and PRD goal sections. Adding SMART goals as a standalone strategic artefact would duplicate, not add. OKRs are outcome-oriented, cascade naturally (Objective → Key Results), and are widely understood in product organisations.

**Why not pure BMM (Business Motivation Model):** BMM's 6-level hierarchy (Vision → Mission → Goal → Objective → Strategy → Tactic) is overengineered for product-level work. The kit's BMC already captures Vision/Mission loosely. This skill adds the measurable outcomes layer, not the full BMM stack.

---

## What a "good objectives doc" means

A objectives document is good when a reader can answer, without ambiguity:

| Question | Where it lives |
|---|---|
| **Why does this initiative exist?** | OBJ-NN title + "Why it matters" paragraph |
| **Whose outcomes does it serve?** | OBJ-NN linked to P-NN persona + BSC perspective |
| **How will we measure success?** | KR-NN.M table: baseline, target, measurement method |
| **Which commercial intent does this serve?** | OBJ-NN "Linked from" field → VP-NN or VS-N.M pain index |
| **Which epics trace to this objective?** | §Objective × Epic traceability matrix |
| **Are these outcomes or feature deliveries?** | Every KR must pass the outcome discipline check |

**Hard scope rules:**
- An objective document captures **WHY** (strategic intent) and **HOW WE KNOW IT'S WORKING** (KRs). It does NOT define features, epics, or how to implement.
- Key Results are **outcomes** (metric changes, behaviour changes, business results) — never outputs (features shipped, story points delivered).
- Each KR must have a **baseline** (current state), a **target** (desired state), and a **measurement method** (how you'll know the target was reached).
- Each OBJ-NN carries a **timeframe** — quarterly or annual. Objectives without timeframes are wishes.
- The document has a **changelog** — objectives evolve as evidence arrives. A static objectives doc is a dead one.

---

## The four modes of operation

### Mode 1 — Scaffold

**When:** the project has no `docs/business/` folder yet.

**Step 0 — Clarifying questions (ask BEFORE generating)**

Ask the user the following 3 questions in a single message with lettered options. Users respond like `1A, 2B, 3C`:

```text
1. Timeframe?
   A. Annual — one set of objectives for the year
   B. Quarterly — one set per quarter (label with quarter, e.g. "Q3 2026")
   C. Initiative-scoped — objectives for a specific initiative (no time expiry until initiative ends)

2. Existing BA artefacts to ground the objectives?
   A. None yet — all soft-link slots stay _TODO_
   B. Some exist — I will check the project (personas, value streams, BMC)
   C. Full BA stack exists — pre-populate "Linked from" fields from existing IDs

3. How many objectives to scaffold?
   A. 1–2 (focused / MVP phase)
   B. 3–5 (standard — recommended)
   C. Placeholder only — scaffold with one empty block, I will fill
```

If the user gives "Other" or pushes back, ask one follow-up to clarify, then proceed.

**Inputs needed:**

| Needed | What you ask if missing |
|---|---|
| **Scope name** | "What product / business / initiative is this objectives doc for?" — used for `{{product_or_scope}}` |

**Output:** `docs/business/04b-objectives.md` sourced from `references/template.md`. Substitute `{{product_or_scope}}` and `{{period}}` placeholders. Do NOT invent objective content in scaffold mode — placeholders only.

**Do NOT** ship a project-side `methodology-references.md`. The canonical bibliography lives in the skill at `references/methodology-references.md` and is linked from the project doc's header.

### Mode 2 — Fill

**When:** the scaffold exists; the user wants to populate objectives and key results.

**Process:**
1. **Read project context** — If `docs/VISION.md` exists, read it first — every objective should be a measurable annual/quarterly step toward the vision's north star, not a disconnected goal. Then read: BMC (`VP-NN` blocks), personas (`P-NN`), value streams (pain index per `VS-N.M`). Objectives synthesise content from these upstream artefacts.
2. **For each OBJ-NN block:**
   - Write a qualitative, inspiring objective title (NOT a feature description).
   - Assign a BSC perspective tag: Financial / Customer / Process / Learning.
   - Declare the owner role and timeframe.
   - Write the "Why it matters" sentence linking to commercial intent (`VP-NN`) or pain (`VS-N.M` pain index).
3. **For each KR under the objective:**
   - Write the outcome as a metric change (apply the outcome discipline check from `references/objective-discipline.md`).
   - Fill baseline, target, and measurement method.
   - Set confidence: `Assumed` (default), `Tested`, `Validated`.
4. **Apply discipline checks** (see `references/objective-discipline.md` §"Anti-patterns"): every KR must pass the outcome vs output test.

### Mode 3 — Align (traceability matrix)

**When:** the objectives doc and delivery roadmap both exist; the user wants to verify epics trace back to objectives.

**Process:**
1. Read `docs/business/04b-objectives.md` and `docs/plans/delivery-roadmap.md`.
2. For each E-NN epic, identify which OBJ-NN it serves (look for explicit references or infer from value statement + VS anchor).
3. Build or update the §Objective × Epic traceability matrix.
4. Flag epics with no OBJ-NN reference as **orphaned delivery** — work being built without a stated strategic objective.
5. Flag OBJ-NN objectives with no E-NN epic as **undelivered intent** — the objective is stated but no delivery is planned for it.
6. Flag KR-NN.M targets that are measurable thresholds and have no corresponding QA-XXNN entry — potential grounding opportunity.

### Mode 4 — Refresh

**When:** new evidence arrives (customer interviews, market data, board decision) and objectives need updating.

**Process:**
1. Identify which OBJ-NN or KR-NN.M needs updating.
2. Update the content.
3. Promote or demote confidence: `Assumed` → `Tested` → `Validated`.
4. Add a changelog entry: date + what changed + evidence source + cascading effects on epics / PRDs.
5. Re-run Align mode to check if the traceability matrix needs updating.

---

## Outcome vs output discipline

**The single most important quality gate in this skill.** Run this test on every Key Result before accepting it.

**Output (wrong — reject):**
- "Ship the confirmation module" — describes a feature delivery
- "Complete 5 user stories in Q3" — describes story points
- "Launch the mobile app" — describes a release
- "Implement the scheduling algorithm" — describes implementation

**Outcome (correct — accept):**
- "Reduce average schedule generation time from 3 working days to < 5 minutes" — measurable behaviour change
- "Increase confirmation rate from 60% to ≥ 90% within 30 days of module launch" — measurable business metric
- "Reduce coordinator time on conflict resolution from 4h/week to < 30min/week" — measurable user behaviour change
- "Achieve zero double-booking incidents in Q1 after go-live" — measurable quality outcome

**The test:** complete the sentence "We will know we succeeded when...".
- "...we shipped X" → output (wrong). Rewrite: what metric changes when the feature works?
- "...X metric changed from Y to Z" → outcome (correct).

---

## The six anti-patterns this skill guards against

1. **Objectives that are actually features.** "Build a mobile app" is a feature; "Reduce time to first value for new users from 2 weeks to 3 days" is an objective. Objectives must describe a future state, not an output.

2. **Key Results that are outputs.** "Ship module X by Q3" says nothing about whether the module worked. Every KR must be a measurable outcome.

3. **Objectives without owners.** An objective without a named owner role drifts. Someone must be accountable for pursuing each objective.

4. **Objectives without timeframes.** An objective that is "always true" is a mission statement, not an OKR. All objectives must have an explicit timeframe.

5. **Unconnected objectives.** Every OBJ-NN must trace back to a commercial intent (`VP-NN` from BMC) or a pain point (`VS-N.M` with High/Critical pain index). Objectives disconnected from commercial or user context are wishful thinking.

6. **Static objectives doc.** No changelog, no confidence-rating updates, no refresh after evidence arrives = the objectives doc dies. Objectives must evolve as the business learns.

---

## Soft-links — connecting objectives to the BA stack

| Objectives field | Soft-links to |
|---|---|
| **Vision** (upstream root) | `docs/VISION.md` (singleton) — objectives should be measurable steps toward the vision's north star metric; if VISION.md exists, add a "Linked to vision" note on each OBJ-NN |
| **"Linked from"** (OBJ-NN) | BMC Value Propositions (`VP-NN`) from `docs/business/` and/or VS pain index (`VS-N.M`) from `docs/business/04a-value-streams.md` |
| **Personas** (OBJ-NN "whose outcomes") | Personas (`P-NN`) from `docs/business/01a-personas.md` |
| **KR targets** | May ground QA acceptance criteria (`QA-XXNN`) in `docs/product-specs/09a-quality-attributes.md` |
| **§Objective × Epic matrix** | Epics (`E-NN`) from `docs/plans/delivery-roadmap.md` |
| **OBJ-NN** | Referenced in PRD `§0 Architecture Traceability` in `docs/product-specs/` |

---

## Output structure

- Open every generated file with the standard artefact frontmatter (OKF-superset block — set `type` to this artefact's `okf_type` display name from the `metamodel` skill's `references/artefact-types-registry.yaml`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`). Run `git config user.name` for `owner`. Set `status: draft` on initial scaffold. Default `review_interval: 60d`. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`.

The skill produces ONE markdown file per objectives cycle. Full template in `references/template.md`. Structure:

```
<!-- doc-version: 1.0 | created: YYYY-MM-DD | timeframe: {{period}} -->

H1: {{product_or_scope}} — Business Objectives

Intro:
  - Scope + timeframe declaration
  - What objectives are, why separate from FBS/PRD
  - Methodology pointer (kit-link)
  - Companion docs (BMC, value streams, personas, delivery roadmap)

§Confidence legend — Assumed / Tested / Validated

§Objectives (one H2 per OBJ-NN)
  Per OBJ-NN:
    - OBJ-NN — Qualitative title (inspiring, NOT a feature)
    - Perspective: Financial | Customer | Process | Learning
    - Timeframe: {{period}}
    - Owner: {{role}}
    - Why it matters: 1 sentence → VP-NN or VS pain index
    - Linked from: VP-NN · VS-N.M (pain index X/5)
    - Key Results table:
      | ID | Key Result (outcome) | Baseline | Target | Measurement method | Confidence |

§Objective × Epic traceability matrix
  | Epic | Epic name | Objective | Key Results served |
  (populated in Align mode; _TODO_ at scaffold)

§Changelog
  | Date | Change | Evidence source | Cascading effects |
```

---

## Sizing heuristics

| Element | Recommended | Source |
|---|---|
| Objectives per timeframe | 2–5 | Doerr OKR discipline |
| Key Results per objective | 3–5 | Doerr OKR discipline |
| Active timeframes per doc | 1 current + archived previous | Anti-confusion rule |
| Customer-perspective objectives | ≥ 1 (non-negotiable) | Practitioner |

**If any number exceeds the recommended range:**
- Too many objectives → the team cannot focus; reconsider scope or split by initiative.
- Too many KRs per objective → the objective is too broad; split it.
- No Customer-perspective objective → the doc is internally focused; revisit with personas in hand.

---

## Cross-reference — the architecture-artefact lifecycle

The objectives doc sits at the **strategic-intent layer**, above the delivery stack:

| Layer | Owns | Objectives relationship |
|---|---|---|
| **Personas** | Who | OBJ-NN "whose outcomes" soft-links to `P-NN` |
| **BMC** | Commercial logic | `VP-NN` blocks → inform OBJ-NN "Linked from" |
| **Value Streams** | How value flows | `VS-N.M` pain index → informs OBJ priority ordering |
| **Business Objectives** *(this skill)* | Why — strategic intent | — |
| **FBS** | What product does | Functionalities should serve OBJ-NN (traced via epics) |
| **Delivery Roadmap** | Epics | `E-NN` epics reference `OBJ-NN` in value statement |
| **Quality Attributes** | NFRs | `KR-NN.M` targets can ground `QA-XXNN` acceptance criteria |
| **PRDs** | Feature specs | `§0 Architecture Traceability` references `OBJ-NN` |

---

## Finding the right folder

Default: `docs/business/`.

**Always check first:**
```bash
find docs -type d -iname "*objective*" -o -type d -iname "*okr*" 2>/dev/null
```

If a folder exists at a non-default location, use it. If none exists, default and confirm.

**Never overwrite an existing objectives file.** Switch modes if it exists:
- Scaffold mode → skip (report what's there).
- Fill mode → append/update OBJ-NN blocks; preserve existing.
- Align mode → update §Objective × Epic traceability matrix only.
- Refresh mode → update specified OBJ-NN or KR-NN.M; add changelog entry.

---

## Reference materials

- **`references/template.md`** — canonical objectives document skeleton. Copy to `docs/business/04b-objectives.md` and fill placeholders.
- **`references/methodology-references.md`** — canonical bibliography (Doerr, BABOK, Adzic, Kaplan & Norton). **Lives only in the kit** — never copied to projects. Project docs link here via the 2-line pointer in their header.
- **`references/objective-discipline.md`** — internal Claude guidance: outcome vs output test, anti-pattern detection cues, BSC perspective decision tree, KR sizing rules, traceability alignment checks. Never copied into the project.

---

## Closing report to the user

After running any mode, summarise in 4–6 lines:

1. **Mode executed** + **files created or updated** with paths.
2. **Objectives scaffolded / filled** with OBJ-NN IDs.
3. **Outcome discipline check** — confirm every KR is an outcome, not an output. Flag any KR that failed.
4. **Confidence distribution** — how many `Assumed` / `Tested` / `Validated`.
5. **Traceability gaps** (Align mode) — orphaned epics (no OBJ-NN) and undelivered objectives (no E-NN).
6. **Cross-link opportunities** — which BA artefacts (personas, BMC, value streams, delivery roadmap) the objectives should soft-link to.

---

## Checklist

Before declaring the work done:

- [ ] Folder exists or was created.
- [ ] `04b-objectives.md` exists with all OBJ-NN blocks scaffolded (scaffold mode).
- [ ] Methodology pointer in header links to kit's canonical bibliography.
- [ ] Each filled OBJ-NN has: title, BSC perspective, timeframe, owner, "why it matters", "linked from".
- [ ] Every KR is an outcome (metric change), not an output (feature delivery) — outcome discipline test passed.
- [ ] Every KR has baseline, target, and measurement method.
- [ ] Confidence ratings set (`Assumed` default).
- [ ] 2–5 objectives total; 3–5 KRs per objective.
- [ ] At least one Customer-perspective objective present.
- [ ] §Objective × Epic traceability matrix present (may be empty at scaffold; populated in Align mode).
- [ ] §Changelog section present.
- [ ] Soft-links populated only when target artefact exists.
- [ ] No project-specific terms baked in (kit version).
- [ ] Closing report delivered.
