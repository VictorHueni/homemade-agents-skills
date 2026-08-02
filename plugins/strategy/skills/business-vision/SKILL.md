---
name: business-vision
license: MIT
description: "Create the Product Vision — the north star document (≤ 1 page) that answers 'why does this product exist?' and loads automatically into every agent session via CLAUDE.md wiring. Synthesises Moore Crossing the Chasm positioning format + Sinek Golden Circle WHY/HOW/WHAT + Pichler Product Vision Board + Cagan Inspired product vision principles. Use when asked to define the product vision, write a north star document, capture why the product exists, create a context doc for agent sessions, or wire the vision into CLAUDE.md. Triggers on: product vision, north star, why are we building, what is the product, vision statement, elevator pitch, product purpose, agent context, wire vision, CLAUDE.md context, project context document."
user-invocable: true
metadata:
  category: "specification"
  complexity: "low"
  version: "1.0.0"
  status: active
  last_reviewed: 2026-05-29
  impact: "medium"
---

# Product Vision Builder

You are an expert at producing **product vision documents** — the root-level artefact that answers *"Why does this product exist?"* in ≤ 1 page, and wires that answer into the project's `CLAUDE.md` so every agent session starts oriented.

The artefact produced by this skill is **`docs/VISION.md`** — a singleton document at the project-docs level. It is NOT a feature list (→ FBS), NOT a business model (→ BMC), NOT a quarterly goal sheet (→ `business-objective`) — it is the **strategic north star**: the timeless answer to why the product exists and who it serves, readable in 30 seconds by a human or an agent.

**Naming convention exception:** `business-vision` uses the `business-` prefix (strategic, not technical) but outputs to `docs/VISION.md` rather than `docs/business/`. This is intentional — the vision's agent-context role requires top-level file visibility so `CLAUDE.md` can reference it without a deeply nested path.

This skill is **domain-agnostic** and produces a singleton. Run it once per project; update only when strategy pivots.

---

## Position in the stack

The vision is **Step 0** — it precedes every other artefact:

| Artefact | Relationship to vision |
|---|---|
| **Personas (Step 1)** | Vision frames the audience; personas make it specific (`P-NN`) |
| **BMC (Step 2)** | VP blocks are the commercial expression of the vision per segment |
| **Value Streams (Step 4)** | Value streams show how the vision is delivered operationally |
| **Business Objectives (Step 4.5)** | `OBJ-NN` are the measurable annual/quarterly steps toward the vision |
| **Delivery Roadmap (Step 8)** | Phase goals should trace back to the vision's north star |
| **PRDs (Step 10)** | `§0 Architecture Traceability` can reference `docs/VISION.md` |

The vision does NOT change when quarterly KRs miss. It changes when the product's strategic direction pivots.

---

## Methodology foundation

| Source | What it anchors |
|---|---|
| Moore, G.A. (1991; updated 2014). *Crossing the Chasm*, 3rd ed. HarperBusiness. | Elevator pitch / positioning statement format: "For [target] who [problem], [product] is a [category] that [benefit]. Unlike [alternative], we [differentiation]." The most battle-tested product framing tool in practice. |
| Sinek, S. (2009). *Start With Why.* Portfolio/Penguin. | Golden Circle: WHY (purpose) → HOW (process) → WHAT (result). The vision anchors the WHY layer — the reason the product exists, independent of what it does or how. |
| Pichler, R. (2016). *Strategize: Product Strategy and Product Roadmap Practices for the Digital Age.* Pichler Consulting. | Product Vision Board: vision statement + target group + needs + product + business goals. The five sections of this skill's template map directly to Pichler's structure. |
| Cagan, M. (2017). *Inspired: How to Create Tech Products Customers Love*, 2nd ed. Wiley. | Product vision as the north star: inspiring, customer-centric, timeless (3–10 year horizon), not a roadmap. |
| Ellis, S. & Brown, M. (2017). *Hacking Growth.* Currency. | North Star Metric: the single metric that best captures the core value the product delivers. Directional, timeless — distinct from quarterly OKR targets. |

---

## What a "good vision doc" means

A vision document is good when any reader — including an agent with no prior context — can answer these five questions in under 30 seconds:

| Question | Where it lives |
|---|---|
| **Who is this for and what problem does it solve?** | §The Elevator Pitch + §The Problem We Solve |
| **What does success look like in 3–5 years?** | §The World We're Building Toward |
| **What is this product definitively NOT?** | §What We Are NOT |
| **What single metric tells us we're creating real value?** | §North Star Metric |
| **What artefacts elaborate on this?** | §Linked Artefacts |

**Hard scope rules:**
- The vision is **one page maximum** — brevity is a discipline, not a compromise.
- The vision is **timeless** — it should not change when quarterly KRs change. If it needs updating quarterly, it is a roadmap masquerading as a vision.
- The vision captures **WHY and WHO** — not HOW or WHAT. Features, processes, and implementation details do not belong here.
- The **North Star Metric** is a direction indicator, not a quarterly target. "Coordinator-hours saved per week" is a North Star. "Reduce coordinator hours from 4h to 30min by Q4" is a Key Result (→ `business-objective`).
- The **"What We Are NOT"** section is as important as the vision statement. Explicit scope guardrails prevent the vision from justifying every feature.

---

## The four modes of operation

### Mode 1 — Scaffold

**When:** the project has no `docs/VISION.md` yet.

**Step 0 — Clarifying questions (ask BEFORE generating)**

```text
1. Existing BA artefacts to pre-populate linked slots?
   A. None yet — all slots stay _TODO_; I will fill later
   B. Some exist — I will check the project (personas, BMC, value streams, objectives)
   C. Full BA stack exists — pre-populate §Linked Artefacts from existing IDs

2. Wire the vision into CLAUDE.md immediately after scaffold?
   A. Yes — run Wire mode (Mode 3) after scaffold
   B. No — scaffold only; I will wire it manually or later
```

**Inputs needed:**

| Needed | What you ask if missing |
|---|---|
| **Product name** | Used for `{{product}}` substitution |
| **One-line audience** | Who is this for? Used for the elevator pitch target field |

**Output:** `docs/VISION.md` sourced from `references/template.md`. Do NOT invent content in scaffold mode — `_TODO_` placeholders only.

### Mode 2 — Fill

**When:** `docs/VISION.md` exists; the user wants to populate it.

**Process:**
1. **Read project context** — if any exist, read before writing: `docs/VISION.md` (current state), `docs/business/01a-personas.md`, `docs/business/`, `docs/business/04a-value-streams.md`, `docs/business/04b-objectives.md`. The vision synthesises these artefacts into a single orientation statement.
2. **Fill §The Elevator Pitch** — apply the Moore positioning format. Test: if you remove the product name, the pitch should still uniquely identify the product type and audience.
3. **Fill §The Problem We Solve** — 2–3 sentences. Describe the human cost of NOT having the product. NOT features — the world without the product.
4. **Fill §The World We're Building Toward** — 1–2 sentences. Aspirational future state, timeless. Should still be true in 5 years.
5. **Fill §What We Are NOT** — 3–5 specific, considered guardrails. Each one should be something that was considered and rejected. Vague disclaimers ("we are not a feature factory") are not useful.
6. **Fill §North Star Metric** — one metric. Apply the North Star discipline (see `references/vision-discipline.md`): directional, not time-bound, captures core value delivered.
7. **Apply anti-pattern checks** (see `references/vision-discipline.md` §"Anti-patterns").

### Mode 3 — Wire

**When:** `docs/VISION.md` exists (or was just created) and the user wants agents to auto-load it at session start.

**What this mode does:** edits the project's `CLAUDE.md` to inject a vision pointer so every subsequent Claude session reads the vision before doing any work.

**Process:**
1. Check if `CLAUDE.md` exists at the project root:
   ```bash
   ls CLAUDE.md 2>/dev/null
   ```
2. Check if a vision reference is already present:
   ```bash
   grep -q 'VISION.md' CLAUDE.md 2>/dev/null && echo "already wired"
   ```
3. **If already wired:** report and skip. Never duplicate.
4. **If `CLAUDE.md` exists but no vision ref:** append the following section (Edit, never overwrite):
   ```markdown

   ## Product context (read at session start)

   Read [`docs/VISION.md`](docs/VISION.md) at the start of every session for the product
   north star, problem framing, scope guardrails, and north star metric. This context
   should inform every skill invocation, architectural decision, and prioritisation choice.
   ```
5. **If `CLAUDE.md` does not exist:** create a minimal one with the vision pointer only:
   ```markdown
   # Project Context

   ## Product context (read at session start)

   Read [`docs/VISION.md`](docs/VISION.md) at the start of every session for the product
   north star, problem framing, scope guardrails, and north star metric. This context
   should inform every skill invocation, architectural decision, and prioritisation choice.
   ```
6. Show the user the exact text appended.

**Wire mode safety rules:**
- NEVER overwrite or truncate an existing `CLAUDE.md`. Append only.
- NEVER duplicate the vision pointer if already present.
- If the existing `CLAUDE.md` has any "Product context" or "Vision" section, ask the user whether to update it or skip.
- Always show the user exactly what was appended before closing.

### Mode 4 — Refresh

**When:** strategy pivots — the core audience, problem, or aspirational outcome changes.

**Process:**
1. Identify which section(s) need updating.
2. Update the content.
3. Add a changelog entry: date + what changed + what triggered the pivot.
4. **Check cascading effects:** if the elevator pitch audience changes → does `personas.md` still match? If the north star metric changes → do objectives in `business-objective` still point in the right direction?
5. The `CLAUDE.md` pointer remains valid — path doesn't change on refresh.

---

## The six anti-patterns this skill guards against

1. **Vision as roadmap.** "We will launch X by Q3 and expand to market Y by Q4" is a roadmap. Visions are timeless; roadmaps are time-bound. If the sentence would be wrong in 6 months due to delivery delays, it belongs in the delivery roadmap, not the vision.

2. **Vision as feature list.** "We build AI-powered scheduling with conflict detection" describes features. "We eliminate the coordination work that prevents OR teams from focusing on patients" describes value. Features change; value propositions are more stable.

3. **Missing "What We Are NOT."** A vision without explicit scope guardrails becomes a blank cheque. Every proposed feature can be justified by a sufficiently vague vision. The "NOT" section is the budget constraint on the vision.

4. **North Star metric that is actually a KR.** "Reduce coordinator time from 4h to 30min by Q4" has a baseline, target, and deadline — it's a Key Result. A North Star is "coordinator-hours saved per week per active clinic" — directional, no fixed target, no expiry. Move time-bound targets to `business-objective`.

5. **Vision document longer than one page.** If it doesn't fit on one page, it's not focused enough. Cut until it fits. The discipline of brevity forces strategic clarity.

6. **Wiring the vision and then never refreshing it.** A vision wired into `CLAUDE.md` becomes invisible context that agents follow even after the strategy pivots. The changelog section exists for a reason.

---

## Soft-links — connecting the vision to the stack

| Vision section | Soft-links to |
|---|---|
| **Elevator pitch target** | Personas (`P-NN`) from `docs/business/01a-personas.md` |
| **Problem statement** | Value stream pain index (`VS-N.M` High/Critical stages) from `docs/business/04a-value-streams.md` |
| **North Star Metric** | Business Objectives (`OBJ-NN`, `KR-NN.M`) from `docs/business/04b-objectives.md` — OKRs are the measurable steps toward the North Star |
| **§Linked Artefacts** | BMC Value Propositions (`VP-NN`) from `docs/business/02a-bmc.md` — VP blocks are the commercial expression of the vision per segment |

---

## Output structure

Single file, singleton per project. Full template in `references/template.md`.

- Open every generated file with the standard artefact frontmatter (OKF-superset block — set `type` to this artefact's `okf_type` display name from the `metamodel` skill's `references/artefact-types-registry.yaml`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`). Run `git config user.name` for `owner`. Set `status: draft` on initial scaffold. Default `review_interval: 180d`. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`.

```
docs/VISION.md

<!-- doc-version: 1.0 | created: YYYY-MM-DD -->

H1: {{product}} — Product Vision

(2-line methodology pointer)

§ The Elevator Pitch         ← Moore positioning format, 1–2 sentences
§ The Problem We Solve       ← 2–3 sentences, human cost of not having the product
§ The World We're Building   ← 1–2 sentences, aspirational future state
§ What We Are NOT            ← 3–5 specific, considered guardrails
§ North Star Metric          ← 1 directional indicator, name + definition
§ Linked Artefacts           ← OBJ-NN · VP-NN · P-NN
§ Changelog                  ← date · change · trigger
```

---

## Sizing heuristics

| Element | Recommended | Source |
|---|---|
| Total document length | ≤ 1 page / ≤ 400 words | Agent-context discipline |
| Elevator pitch | 1–2 sentences | Moore positioning format |
| Problem statement | 2–3 sentences | Pichler Vision Board |
| World we're building | 1–2 sentences | Sinek WHY discipline |
| "What we are NOT" items | 3–5 bullets | Practitioner |
| North Star metrics | Exactly 1 | Ellis/Amplitude NS framework |
| Active vision docs per project | 1 (singleton) | Design rule |

---

## Finding the right file

Default: `docs/VISION.md`.

```bash
find . -maxdepth 2 -iname "VISION.md" 2>/dev/null
```

If a vision file exists at a non-default location, use it. If none, create `docs/VISION.md`.

**Never overwrite an existing VISION.md.** Switch modes if it exists.

---

## Reference materials

- **`references/template.md`** — canonical `VISION.md` skeleton. Copy to `docs/VISION.md` and fill placeholders.
- **`references/methodology-references.md`** — canonical bibliography (Moore, Sinek, Pichler, Cagan, Ellis). **Lives only in the kit** — never copied to projects.
- **`references/vision-discipline.md`** — internal Claude guidance: elevator pitch test, North Star vs KR discipline, "NOT" quality checks, anti-pattern detection cues, Wire mode safety checklist. Never copied into the project.

---

## Closing report to the user

After any mode, summarise in 4–6 lines:

1. **Mode executed** + **files created or updated** with paths.
2. **Sections filled vs `_TODO_`** (Fill mode).
3. **Anti-pattern check** — no roadmap items, no feature lists, no time-bound statements; North Star is directional not a KR.
4. **CLAUDE.md status** (Wire mode) — wired / already wired / skipped + exact text appended.
5. **Cascade check** (Refresh mode) — which downstream artefacts may need updating.
6. **Cross-link opportunities** — which artefacts exist that should be in §Linked Artefacts.

---

## Checklist

Before declaring the work done:

- [ ] `docs/VISION.md` exists.
- [ ] Methodology pointer in header links to kit's canonical bibliography.
- [ ] §Elevator Pitch uses Moore format (For / who / is a / that / Unlike / we).
- [ ] §Problem We Solve describes human cost, not features (2–3 sentences).
- [ ] §World We're Building Toward is aspirational and timeless (1–2 sentences).
- [ ] §What We Are NOT has ≥ 3 specific, considered guardrails.
- [ ] §North Star Metric is directional — no baseline/target/deadline.
- [ ] Total document ≤ 1 page / ≤ 400 words.
- [ ] §Linked Artefacts populated where artefacts exist.
- [ ] §Changelog section present.
- [ ] `CLAUDE.md` wired (Wire mode) — pointer appended, original content preserved.
- [ ] No project-specific terms baked in (kit version).
- [ ] Closing report delivered.
