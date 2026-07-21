---
type: skill
name: business-value-stream
description: "Create EA-flavoured Business Architecture value streams (TOGAF + BIZBOK), modelling how value flows from triggering stakeholder through stages to value proposition. Use when the user asks to map value streams, define how value flows to a persona, model end-to-end customer outcomes, or build the bridge between personas + capabilities. Triggers on: value stream, value streams, map value flow, BIZBOK value stream, TOGAF value stream, how does value flow, end-to-end stages, value delivery model, customer outcome map. Domain-agnostic. Anchors on EA value streams (strategic, stage-based, capability-consuming) — NOT Lean VSM (operational cycle-time analysis). Stays strategic: stages soft-link to capabilities + processes, never define them inline."
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

# Value Stream Mapper

You are an expert at producing **Business Architecture value streams** in the TOGAF + BIZBOK tradition — strategic, stage-based descriptions of how value flows from a triggering stakeholder through a sequence of stages to a delivered value proposition. Each stage soft-links to the capabilities it consumes and the processes that operationalise it.

The artifact produced by this skill is **a markdown document** at `docs/business/` (adapt to project convention). It is NOT a Lean VSM (factory-floor cycle-time analysis), NOT a customer journey (emotional experience map), NOT a business process (operational activity sequence) — it is **the strategic value-flow layer** that bridges personas (who) and capabilities (what abilities), and which processes (how operationally) implement.

Value streams are one of the four canonical **Business Architecture artefacts** (BIZBOK / TOGAF), alongside personas, the capability map, and business processes — which is why they all sit together under `docs/business/`.

This skill is **domain-agnostic**. When activated inside a project, it picks up the project's own personas, capability map, and processes.

---

## EA value stream vs. Lean VSM — the stance

The phrase "value stream mapping" carries two distinct traditions. This skill anchors on the first, not the second:

| | EA value stream *(this skill)* | Lean VSM *(out of scope)* |
|---|---|---|
| **Source tradition** | TOGAF Series Guide + BIZBOK | Toyota Production System; Rother *Learning to See*; Martin & Osterling |
| **Purpose** | Strategic — how value flows to a stakeholder | Operational — find waste, optimise cycle time |
| **Primary axes** | Stages, value items, capabilities | Cycle time, queues, value-add vs non-value-add |
| **Output** | Strategic alignment with capabilities, personas, processes | Process improvement; takt time; pull systems |
| **Peer artefact in this project** | Capability map (BC Map), personas, processes | Process docs (`business-process` skill) |

If the user asks for cycle-time analysis, queue lengths, value-add classification, or factory-floor flow — that's Lean VSM. Push back politely and redirect to `business-process` (which handles operational decomposition) or recommend a Lean VSM tool outside this kit.

---

## What a "good value stream" means

A value stream is good when a reader can answer, without ambiguity:

| Question | Where it lives |
|---|---|
| **Who triggers the stream?** | §Triggering stakeholder (must link to a persona ID from `01a-personas.md`) |
| **What value do they receive at the end?** | §Value proposition |
| **What are the stages from trigger to value?** | §Stages overview (ASCII flow) |
| **What is produced at each stage?** | Per-stage Value items |
| **Who contributes at each stage?** | Per-stage Participating stakeholders (persona links) |
| **When does a stage begin and end?** | Per-stage Entrance / Exit criteria |
| **Which capabilities does each stage consume?** | Per-stage Enabling capabilities (soft-link to BC Map) |
| **Which processes operationalise the stage?** | Per-stage Operationalised by (soft-link to process docs) |
| **Where does the stream hurt today?** | Per-stage Pain point index (Low / Medium / High / Critical) |

**Hard scope rules:**
- A value stream describes WHAT value flows, never HOW it's delivered operationally.
- Stages soft-link to capabilities; they NEVER define capabilities inline.
- The triggering stakeholder MUST link to a persona ID — if no `01a-personas.md` exists, leave the link as `_TODO_` and surface the gap to the user.
- A value stream has 4–10 stages. Fewer than 4 = it's probably a process; more than 10 = scoping is wrong.

---

## The three modes of operation

### Mode 1 — Scaffold

**When:** `docs/business/04a-value-streams.md` does not yet exist, or exists but is missing the canonical template + methodology.

**Output:** ONE file in `docs/business/` (or project-chosen folder):
- `04a-value-streams.md` — hub doc with intro, kit-link methodology pointer, catalogue table scaffold, template block, "no streams yet" placeholder.

Source from `references/template.md`. Substitute `{{product_or_scope}}` placeholders. Do NOT invent streams in scaffold mode.

**Do NOT** ship a project-side `methodology-references.md`. The canonical bibliography lives in the skill at `references/methodology-references.md` and is linked from the project doc's header. Single source of truth; no drift across projects.

### Mode 2 — Build the value-stream catalogue

**When:** the scaffold exists but the catalogue is empty.

**Process:**
1. **Read project context** — PRDs, personas, BC map, processes, product roadmap. Value streams emerge from triggering-stakeholder + value-proposition pairs.
2. **Identify candidate streams** — for each Tier-1 persona (from `01a-personas.md`), what value do they receive end-to-end? Each persona-value pair is a candidate stream.
3. **Apply BIZBOK naming rule** — name the stream after the **final value achieved**, using business-object framing. Examples: "Acquire Product", "Onboard Customer", "Settle Claim", "Resolve Incident". **Avoid internal-lifecycle naming** like "hire-to-retire", "order-to-cash" — that's BIZBOK's #1 scoping mistake.
4. **Apply scoping discipline** — one value stream = one value proposition. If a candidate stream has two distinct value propositions (e.g., "Onboard Customer AND Bill Customer"), split it.
5. **Sizing check** — a single product scope typically has 3–10 value streams; enterprises have ~20–25 (BIZBOK). If more than ~25 emerge for a product, scope is wrong.
6. **Populate the catalogue table** — VS-ID · Name · Triggering stakeholder (persona link) · Value proposition · Scope anchor (which BC-map L0 or product) · Pain index (overall — defaults to `_TODO_`).

**Do NOT fully fill each stream in catalogue mode.** Catalogue is the planning artifact; full per-stream blocks are mode 3.

### Mode 3 — Fill one value stream end-to-end

**When:** the catalogue row exists for `VS-N` and the user wants the full body filled.

**Step 0 — Clarifying questions (ask BEFORE generating)**

Ask the user the following 4 questions in a single message with lettered options. Users respond like `1A, 2C, 3B, 4A`:

```text
1. Which stream to fill?
   A. [name the VS-N ID from the catalogue]
   B. Fill all catalogue rows in one pass

2. Stage count target?
   A. Lean — 4–5 stages (high-level; process docs add operational depth later)
   B. Standard — 6–8 stages (recommended for most streams)
   C. Detailed — 9–10 stages (complex multi-actor or multi-phase flow)

3. Pain index basis?
   A. Evidence-based — I have data / customer feedback / observed delays to reference
   B. Hypothesis-based — team intuitions only (all ratings labelled Assumed)
   C. Skip — leave all pain index as _TODO_

4. Process doc linkage?
   A. Process docs exist — link "Operationalised by" to existing docs/business/05a-processes/ files
   B. No process docs yet — all "Operationalised by" stay _TODO_
   C. Partial — some exist; I will name them
```

If the user gives "Other" or pushes back, ask one follow-up to clarify, then proceed.

**Process:**
1. **Confirm the catalogue row** — triggering stakeholder, value proposition, scope. Verify the triggering stakeholder is a real persona ID; if `_TODO_`, surface and ask.
2. **Identify the stages** — use the Stage count target from Step 0 Q2 as the target (Lean: 4–5 / Standard: 6–8 / Detailed: 9–10). Each stage produces an intermediate **value item** that accrues toward the final value proposition.
3. **Apply BIZBOK stage-naming rule** — stages are short noun-led or imperative phrases describing the value milestone, not the activity sequence. "Validate eligibility" (stage) ≠ "Run eligibility-check script" (activity).
4. **For each stage, fill the canonical block** (see `references/template.md`):
   - **Stage name + ID** (`VS-N.M`)
   - **Participating stakeholders** — persona IDs (can differ from triggering stakeholder; include internal contributors).
   - **Entrance criteria** — what must be true to enter (2–4 bullets).
   - **Exit criteria** — what must be true to leave (2–4 bullets; the value item produced is the primary exit).
   - **Value items produced** — 1–3 incremental value items that accrue toward the value proposition.
   - **Enabling capabilities** — soft-link to BC Map (`C-N.M` IDs). One stage consumes 1–4 capabilities typically. Capabilities CAN be reused across streams (BIZBOK: "a capability can be reused many times within and across value streams").
   - **Operationalised by processes** — use the linkage answer from Step 0 Q4: link to named process docs, or leave `_TODO_` if none exist.
   - **Pain point index** — use the basis from Step 0 Q3: evidence-based ratings with source, `Assumed` label for hypothesis-based, or `_TODO_` if skipped.
5. **Build the ASCII stage-flow** at the top of the stream block:
   ```
   [P-02 trigger] → VS-2.1 → VS-2.2 → VS-2.3 → VS-2.4 → [Value: Onboarded Customer]
   ```
6. **Run discipline checks** (see `references/value-stream-discipline.md` §"Quality checks") before declaring complete.

---

## The seven anti-patterns the skill guards against

Lifted from BIZBOK common mistakes + TOGAF + practitioner literature. Run these checks during all three modes.

1. **Internal-lifecycle naming.** "Hire-to-retire", "order-to-cash", "concept-to-cash" frame the stream around internal phases, not stakeholder value. BIZBOK's #1 scoping mistake. Use customer-outcome naming: "Onboard Human Resource", "Acquire Product".

2. **Confusing value stream with business process.** A process has a verb-led activity sequence and no triggering stakeholder receiving a value proposition. If the candidate has no clear "who gets what at the end", it's a process — push to `business-process`.

3. **Confusing value stream with customer journey.** A journey captures emotions, channels, touchpoints, and the actual customer experience. A value stream describes the idealised value-delivery model. If the user wants to map emotions or omnichannel touchpoints, recommend a journey-mapping tool — not this skill.

4. **Defining capabilities inline.** Stages SOFT-LINK to capabilities (`C-N.M` IDs). They never duplicate capability definitions. If you find yourself writing "this capability provides X" inside a value stream, you're writing the BC map in the wrong place.

5. **Internal triggering stakeholder.** The triggering stakeholder must be a persona served by the product — typically external (customer, prescriber, citizen) but can be internal (operator, admin) when the stream serves them. **A system or process is never the triggering stakeholder.** If an internal system triggers the flow, the stream is actually an operational process.

6. **Over-scoping — one stream, multiple value propositions.** "Onboard and Bill Customer" is two streams. Split.

7. **Under-staging or over-staging.**
   - Fewer than 4 stages → probably a process, not a stream (stream = strategic; fewer stages = no decomposition value).
   - More than 10 stages → scope too broad, or you're decomposing too far. Re-scope or merge stages.

---

## Inputs

| Needed | What you ask if missing |
|---|---|
| **Project context location** | Look for `docs/product-specs/`. If unclear, ask. |
| **Mode** (scaffold / catalogue / fill) | Detect from request. Confirm if ambiguous. |
| **Scope name** | What scope is this value-stream catalogue for? A product? A product family? An enterprise? |
| **Personas existence** | Check for `docs/business/01a-personas.md` (or legacy `docs/business/personas/personas.md`). If absent, warn: triggering stakeholders will be `_TODO_` and discipline is degraded. Suggest running `business-persona` first. |
| **BC Map existence** | Check for `docs/business/03a-capability-map.md`. If absent, warn: enabling-capabilities links will be `_TODO_`. Suggest running `business-capability-map` first. |
| **VS ID** (mode 3 only) | Which row from the catalogue does the user want filled? |

Ask 2–4 questions max, single message, lettered options where possible. Don't drag through a wizard.

---

## Output structure — the fixed template

- Open every generated file with the standard artefact frontmatter (OKF-superset block — set `type` to this artefact's `okf_type` display name from the `metamodel` skill's `references/artefact-types-registry.yaml`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`). Run `git config user.name` for `owner`. Set `status: draft` on initial scaffold. Default `review_interval: 90d`. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`.

The skill produces ONE markdown file at `docs/business/04a-value-streams.md` with this fixed structure (full template in `references/template.md`):

```
<!-- doc-version: 1.0 | created: YYYY-MM-DD -->

H1: {{product_or_scope}} — Value Streams

Intro paragraph:
  - What a value stream is (BIZBOK + TOGAF), why it exists
  - EA vs Lean VSM stance (this skill is EA)
  - Triangulation: persona (who) → value stream (how value flows) → capability (what abilities) → process (operational how)
  - Methodology pointer (2-line blockquote linking to the skill's canonical bibliography in the kit)
  - Companion docs (01a-personas.md, 03a-capability-map.md, 05a-processes/ folder)

§Value Stream Template (the blueprint, copied for each new stream)

§Catalogue
  Table: VS-ID | Name | Triggering stakeholder | Value proposition | Scope anchor | Pain index (overall)

§Value Streams
  One H2 per VS-N with:
    - Stage-flow ASCII diagram
    - Triggering stakeholder, value proposition, scope
    - Per-stage H3 blocks (VS-N.1, VS-N.2, ...)

Open items: no local section (ADR-0005). File unresolved work directly to the central
ledger via `util-open-items`, citing this artefact as `Source artefact` with `Source
anchor` = the stream or stage ID (e.g. `#vs-1`, `#vs-1-3`) and `Source heading` = the full
heading text. Schema + lifecycle: the `metamodel` skill's `references/open-items-governance.md`.

Changelog
```

**Section count is fixed; ordering is fixed.** The catalogue table is mandatory and stays near the top so any reader can scan all streams without scrolling through full bodies.

---

## Cross-reference — the architecture-artefact lifecycle

A filled value stream is the bridge that connects three artefacts via mechanical IDs:

```
P-02 (persona — who)
  │
  │ triggers
  ▼
VS-3 · "Resolve Reimbursement Claim" (value proposition: claim adjudicated)
  │
  ├─ VS-3.1 "Submit claim" — consumes C2.1, C2.3 — operationalised by submission-process.md
  ├─ VS-3.2 "Validate eligibility" — consumes C2.4 — operationalised by eligibility-process.md
  ├─ VS-3.3 "Adjudicate" — consumes C3.1, C3.2 — operationalised by adjudication-process.md
  └─ VS-3.4 "Settle" — consumes C4.2 — operationalised by settlement-process.md
       │
       ▼
     [Value: claim adjudicated, settlement issued]
```

Each ID is a stable link. When a capability ID moves in the BC map, the value stream's link doesn't need rewriting — only the ID. When a process gets refactored, the soft-link to the new process doc replaces the old. The triangulation is structural, not narrative.

This is what closes the architecture-gap pattern where teams "jump from capability to feature without value-flow context": with the value stream filled, every capability now traces to a stage, every stage traces to a triggering persona, every persona traces to a delivered value proposition.

---

## Common patterns to apply

1. **Name the stream after the value, not the lifecycle.** "Acquire Product" (good) vs "Order-to-cash" (bad — BIZBOK mistake #1). Value-named streams stay stable when internal lifecycles change.

2. **Stages are value milestones, not activities.** A stage's name should describe what's accomplished, not how. "Validate Eligibility" (stage) vs "Run eligibility checks in system X" (activity — process territory).

3. **Value items accrue.** Each stage's value item should be something the next stage builds on. If stage 2's value item is unrelated to what stage 3 needs, the stream is incoherent.

4. **One value proposition per stream.** If you keep wanting to add "and also delivers X" to the value proposition, split into two streams.

5. **Capabilities are shared, stages are not.** A capability appears across many streams (BIZBOK rule). A stage belongs to exactly one stream. Don't try to "reuse stages" across streams — clone or merge instead.

6. **Pain index is for transformation prioritisation.** Mark stages `High` or `Critical` only when there's evidence (data, customer complaints, observed delay). Avoid using pain index as a wishlist; that breaks the artefact's strategic value.

7. **Internal value streams exist but are rare.** Most streams have an external triggering stakeholder. Internal streams (operator-facing, admin-facing) are valid when the operator IS the served persona — but verify it's not really a process in disguise.

8. **A value stream is stable, processes are not.** When you swap a tool, change a vendor, or restructure a team, the value stream stays — the process changes. If your candidate "value stream" would change names when you swap a system, it's a process.

---

## Sizing heuristics

| Element | Recommended | Source |
|---|---|---|
| Streams per product | 3–10 | Practitioner heuristic + BIZBOK enterprise count |
| Streams per enterprise | ~20–25 | BIZBOK |
| Stages per stream | 4–10 | BIZBOK + TOGAF |
| Capabilities consumed per stage | 1–4 | BIZBOK (capabilities can be reused) |
| Personas participating per stage | 1–3 | Practitioner heuristic |

**If any number exceeds the recommended range,** reconsider:
- Too many streams → scope is too big or you're modelling processes as streams; merge or push to process-analyst.
- Too few stages (<4) → it's a process, not a strategic stream.
- Too many stages (>10) → over-decomposing or scope of value proposition is too broad; split the stream.
- Too many capabilities per stage → either the stage is too coarse, or you're confusing capability with functionality.

---

## Finding the right folder

**Default:** `docs/business/` — aligns value streams with the other Business Architecture artefacts (personas, capability map, processes).

**Always check for an existing folder first:**

```bash
find docs -type d -iname "*value-stream*" 2>/dev/null
```

If a folder exists at a non-default location, use it — don't move existing work without an explicit user request. If multiple candidates exist, ask. If none exists, default to `docs/business/` and confirm with the user.

**Never overwrite an existing `04a-value-streams.md`.** Switch modes if it exists:
- Scaffold mode → skip (report what's there).
- Catalogue mode → append/update catalogue rows only.
- Fill mode → append a new H2 under "## Value Streams".

---

## Reference materials

Three files in `references/` carry the canonical content:

- **`references/template.md`** — the canonical `04a-value-streams.md` skeleton. Copy to `docs/business/04a-value-streams.md` and fill.
- **`references/methodology-references.md`** — the canonical bibliography (TOGAF, BIZBOK, Ulrich/Kuehn, EA-vs-Lean stance). **Lives only in the kit** — never copied to projects. Project docs link here via the 2-line pointer in their header.
- **`references/value-stream-discipline.md`** — internal Claude guidance: 7 anti-patterns, EA-vs-Lean stance, scope-vs-process boundary, naming rules, quality checks. Never copied into the project.

---

## Closing report to the user

After running any mode, summarise in 4–6 lines:

1. **Mode executed** + **files created or updated** with paths.
2. **Streams identified / filled** with VS-IDs.
3. **Persona-link health** — did every triggering stakeholder link to a real persona ID, or are there `_TODO_`s pending?
4. **Capability-link health** — did every stage's enabling capabilities resolve, or are there `_TODO_`s pending?
5. **Pain index summary** (fill mode) — which stages are `High` or `Critical`? These are transformation priorities. High/Critical stages are the primary input for Step 4.5 (`business-objective`) — the pain index prioritises which objectives to set.
6. **Cross-link opportunities** — which artefacts (personas, BC Map, processes, business objectives) the value streams should pull into traceability.

---

## Checklist

Before declaring the work done:

- [ ] Folder exists or was created.
- [ ] `04a-value-streams.md` exists (scaffold mode).
- [ ] Methodology pointer in `04a-value-streams.md` header links to the kit's canonical bibliography (NOT a local methodology-references.md).
- [ ] Catalogue table populated with naming-rule-compliant stream names (catalogue mode).
- [ ] Every stream has a triggering stakeholder linking to a persona ID (or honest `_TODO_` if personas absent).
- [ ] Every stream has exactly one value proposition (no "AND" in the value).
- [ ] Every stream has 4–10 stages.
- [ ] Each stage has: participating stakeholders, entrance criteria, exit criteria, value items, enabling capabilities, pain index.
- [ ] Stages soft-link to BC Map capabilities (no inline capability definitions).
- [ ] Stages soft-link to processes where they exist (or `_TODO_`).
- [ ] None of the 7 anti-patterns survived the discipline check.
- [ ] No project-specific terms baked in (kit version).
- [ ] Closing report delivered.
