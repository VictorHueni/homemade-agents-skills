---
name: business-process
description: "Create a BPMN-ready business process document. Use when the user asks to document a process, model a workflow, write a process spec, capture an as-is process, or anything BPMN-flavoured. Triggers on: create a process doc, document this process, model this workflow, BPMN, process model, business process for {X}, capture this workflow, write an as-is process, document the {Y} flow. Encodes a fixed template: Master diagram (Mermaid) → Triggers → Actors → Activities → Data Stores → Data Objects → Decisions → KPIs → Pain Points → Sources → TODOs. Domain-agnostic; works for any industry."
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

# Business Process Analyst

You are an expert at producing **BPMN-ready business process documents**: descriptive walkthroughs of how a workflow actually happens today, structured so that an analyst could reach for the doc and produce a BPMN diagram without further interviews.

The artifact produced by this skill is **a markdown document** in the project's processes folder (typically `docs/business/05a-processes/` — see project conventions). It is NOT a BPMN file, NOT a slide, NOT a strategic argument — it is **the descriptive source-of-truth** that strategic analyses, models, and product specs cite.

This skill is **domain-agnostic**. The template patterns work for any industry; the references use abstract placeholders. When activated inside a project, the skill picks up the project's own actor naming, system inventory, and KPI conventions.

---

## What "BPMN-ready" means

A doc is BPMN-ready when a reader can identify, without ambiguity:

| BPMN element | Where it lives in the doc |
|---|---|
| **Start event(s)** | §2 Triggers |
| **Pools / Lanes** | §3 Actors (each actor is one lane) |
| **Tasks / Activities** | §6 Activities (each numbered step is one task) |
| **Data Stores** | §4 Data Stores (the systems / databases / records each actor reads from or writes to) |
| **Data Objects** | §5 Data Objects (the artifacts that flow through the process — forms, claims, decisions, etc.) |
| **Gateways / Decisions** | §7 Decision points + business rules |
| **Measurable outcomes** | §8 KPIs |

The doc is also descriptive prose — it does not have to be machine-readable. But the structure should mean an analyst can sit down with the doc and a BPMN tool and produce a diagram in one session.

---

## The three modes of operation

The skill operates in one of three modes. Detect which mode the user wants from their prompt; ask if ambiguous.

### Mode 1 — Scaffold

**When:** the project has no processes folder yet, or has one but is missing a file for this specific process slug.

**Output:** ONE file at `{processes folder}/proc-NN-{slug}.md` from the canonical template — all sections present, all cells `_TODO_`. Do NOT fill actors, activities, KPIs, or any substantive content in scaffold mode.

Seed §8 KPIs with 3–5 starter candidate rows (values `_TODO_`) — a process without KPIs is a narrative, not a process.
Do NOT seed §11 §Open Items with placeholder rows. §Open Items is the canonical document-level open-items section per [`rules/open-items-governance.md`](https://github.com/VictorHueni/homemade-claude-kit/blob/main/rules/open-items-governance.md); only actionable unresolved work (doc-gap / decision-gap / execution-item / tech-debt) belongs there. Inline `_TODO_` placeholders in §8 or elsewhere are scaffold debt and stay inline. Initialise §Open Items with `_None at present._`.
Update the processes index if the project has one.

### Mode 2 — Fill

**When:** the scaffold exists (or the user wants to create + fill in one pass) and the user has enough context to describe the process.

**Step 0 — Clarifying questions (ask BEFORE generating)**

Ask the user the following 4 questions in a single message with lettered options. Users respond like `1A, 2C, 3B, 4A`:

```text
1. §6 decomposition axis?
   A. Per-actor (default — one sub-section per actor / pool / lane; works for ~80% of processes)
   B. Per-variant (3+ structurally distinct sub-flows sharing the same actors)
   C. Per-channel (bifurcated into 2+ parallel channels with different actors / rules)
   D. Per-jurisdiction (same process runs differently across regions / cantons / states)
   E. Automated pipeline (no human actors — collapsed to system components)
   F. Ongoing duties (continuous loop, no defined end)

2. Process scope?
   A. End-to-end stakeholder-facing flow (external trigger → delivered outcome)
   B. Internal back-office / operational flow
   C. Regulatory submission / compliance flow
   D. Integration / system-to-system flow

3. Audience?
   A. Internal technical reference (default)
   B. Audit-facing (regulatory / compliance reader)
   C. Investor / executive-facing

4. Known actors and systems?
   A. Yes — I will provide them
   B. Partial — some known, scaffold the rest as _TODO_
   C. None yet — scaffold everything _TODO_; discover via research
```

If the user gives "Other" or pushes back, ask one follow-up to clarify, then proceed.

**Inputs needed before generating:**

| Needed | What you ask if missing |
|---|---|
| **Process slug** (kebab-case, used in filename and references) | "What should we call the file? (e.g., `customer-onboarding`, `incident-response`)" |
| **Display name** (the H1 title) | "And the human-readable display name?" |
| **One-line purpose** | "One sentence — what does this process do, and for whom?" |
| **Scope** | "What's the start point and the end point?" |

**Process:**
1. If §6 axis is not default (per-actor), document the deviation + one-sentence rationale in the doc's frontmatter blockquote.
2. Read project context to pre-fill what is knowable: persona IDs for actors, capability IDs for enabling systems, upstream / downstream process slugs.
3. Fill the template end-to-end — pre-fill known content; mark the rest `_TODO_`.
4. Seed §8 KPIs with concrete starter rows matched to the process type (see §8 KPI patterns below).
5. Add rows to §Open Items ONLY for actionable unresolved work (e.g. a known doc-gap with a real resolution path, a deferred decision blocking a downstream ADR). Do not migrate scaffold `_TODO_` placeholders into §Open Items — they are different per [`rules/open-items-governance.md`](https://github.com/VictorHueni/homemade-claude-kit/blob/main/rules/open-items-governance.md) §2. Empty §Open Items is acceptable.
6. Update the processes index if the project has one.

**Do NOT:**
- Invent actor names, KPI values, or system names — those are research. Use abstract placeholders.
- Conflate descriptive content with strategic argument — this doc says **what is**, not what should change.
- Produce a BPMN XML file — this skill produces the markdown source-of-truth.
- Skip §8 KPIs because the user "doesn't have any yet" — seed candidate rows with `_TODO_` values regardless. (These are scaffold placeholders; do NOT mirror them as §Open Items rows.)
- Leave Mermaid diagrams empty — at minimum produce a master flow (§0) and one sequence diagram per actor or phase in §6.

### Mode 3 — Update

**When:** a process doc exists and needs a targeted change: a new section, a KPI value filled, a doc-version bump, an actor added, an index row updated.

**Process:**
1. Identify the specific section(s) to change.
2. Make targeted edits only — do not regenerate the whole file.
3. Bump `doc-version` in the HTML comment for structural changes (new section, deletion, renumbering). Add `last-updated: YYYY-MM-DD` for patches without structural change.
4. Add a changelog entry for structural changes.
5. Update the processes index row if the status changes.

---

## Output structure — the fixed template

- Open every generated file with the standard artefact frontmatter (OKF-superset block — set `type` to this artefact's `okf_type` display name from `rules/artefact-types-registry.md`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`). Run `git config user.name` for `owner`. Set `status: draft` on initial scaffold. Default `review_interval: 90d`. Full schema: `rules/artefact-frontmatter.md`.

The skill produces ONE markdown file at `{processes folder}/proc-NN-{slug}.md` with this fixed structure (full template in `references/template.md`):

```
<!-- doc-version: 1.0 | created: YYYY-MM-DD -->

H1: {Process display name}

Frontmatter blockquote:
  - Audience
  - Type (descriptive operator reference — not strategic / not quantitative)
  - Companion docs (strategic analysis if exists; quantitative model if exists; upstream / downstream processes)
  - Glossary pointer if project has one

§0 Master flow — one Mermaid flowchart of the entire process at high level

§1 What this process is — descriptive frame (what is it, when it applies, why it matters operationally)

§2 Triggers — what starts this process
  Table: Trigger | Source | Frequency | Decision tree if multiple

§3 Actors — roles + responsibilities
  Table: Actor | Role | Authority | Decision rights | Statutory basis if any

§4 Data Stores — systems / databases / registries involved
  Table: System | Owner | Read by | Written by | Authoritative for | Format

§5 Data Objects — artifacts that flow through the process
  Table: Object | Created by | Consumed by | Format | Required fields | Standards reference if any

§6 Activities — step-by-step walkthrough
  §6.1 Actor A's flow (Mermaid sequence diagram + numbered steps)
  §6.2 Actor B's flow (Mermaid sequence diagram + numbered steps)
  ... per actor or per phase

§7 Decision points + business rules
  Table: Decision | Inputs | Rule | Outcome | Authority

§8 KPIs — measurable indicators (MANDATORY)
  Table: KPI | What it measures | Current value | Target / SLA | Owner | Source of measurement

§9 What's broken today — pain points (operator-grade, not strategic argument)
  Table: Pain point | Who experiences it | Where in the process | Impact

§10 Sources
  By category: primary regulatory / legal | professional society | industry | internal companion docs

§11 Open Items  (canonical document-level section per rules/open-items-governance.md §1 + §4)
  Table: OI-ID | Type | Summary | Source anchor | Source heading | Resolution path | Priority | Status | Owner | Due / Review date | Tracker ref
  Skills MAY append a `§` column AFTER `Tracker ref` for intra-doc navigation; canonical columns must not be reordered or removed.
  Only actionable unresolved work belongs here (doc-gap | decision-gap | execution-item | tech-debt). Inline `_TODO_` placeholders are NOT open items.

Changelog
```

**Section count is fixed; ordering is fixed; §8 KPIs is mandatory (never empty). §11 §Open Items is mandatory as a section but may be empty — `_None at present._` is the correct initial state when no actionable unresolved work exists. Do NOT scaffold placeholder rows there.**

**§6 Activities decomposition has 5 documented exceptions** — full detail in `references/logic-and-sequence.md` *When to break the template*. Most processes use per-actor §6 sub-sections. Use a deviation when the natural organising axis is clearly different:

| Default | When to deviate |
|---|---|
| §6 per-actor (one sub-section per actor / pool / lane) | Default — works for ~80% of processes |
| §6 per-variant (one sub-section per request type) | When 3+ structurally distinct sub-flows share the same actors — e.g., a regulatory process with new-application / renewal / special-track / removal variants |
| §6 per-channel (one sub-section per parallel channel) | When the process is fundamentally bifurcated into 2 channels with different actors / rules / data — e.g., insurer-direct vs pooled-fund rebate flows |
| §6 collapsed to system components | When there are no human actors (automated pipelines) |
| §6 as ongoing duties | When the process is a continuous loop with no defined end (monitoring, surveillance) |
| §6 per-jurisdiction | When the same process runs differently across cantons / states / countries |

**Always document the deviation in the doc's frontmatter blockquote** with a one-sentence rationale. Default to the standard per-actor template when in doubt — deviations are escape hatches for genuine misfit, not licence to redesign to taste.

---

## The §8 KPIs table is the doc's killer feature

Without §8, the doc is a narrative — useful but not operational. **Always seed §8 with concrete starter rows before declaring the scaffold complete.** Common KPI patterns by process type:

**Submission / request processes** (KG, prior auth, application workflows):
- Time-to-decision (median, p90, p95)
- Approval rate / Rejection rate / Pend rate
- First-pass completeness rate
- Statutory deadline compliance rate
- Volume per unit time + growth trend

**Operational / back-office processes** (claims processing, intake, triage):
- Throughput per FTE
- Backlog age distribution
- Re-work rate (item re-touched after initial processing)
- Manual-intervention rate
- Cost per transaction

**Clinical / decision processes** (Vertrauensarzt review, medical triage):
- Inter-reviewer concordance rate
- Decision reversal rate on appeal
- Time per case (median, by complexity)
- Auto-triage capture rate

**Customer-facing flows** (onboarding, support, sales):
- Conversion rate per stage
- Time-to-first-value
- Drop-off rate by step
- CSAT / NPS

If the user can't give you current values, seed the KPI rows anyway with `_TODO_` in the value column — the KPI list itself is more important than the numeric data, because it defines what the process should measure.

---

## Cross-reference — the 3-layer artifact lifecycle

A process doc is one of three artifact types that together describe a domain operationally:

| Layer | Job | Owns |
|---|---|---|
| **Strategic analysis** | "Why this matters / what could change" | Business case, strategic argument, product opportunity framing |
| **Process** *(this skill)* | "What happens — who, what, how, with what data" | BPMN-ready descriptive walkthrough, actors, activities, data, KPIs |
| **Model** | "How much / how big" | Quantification (TAM, savings, recovery, etc.); anchored to one analysis + observes N processes |

### The content-routing rule (one rule)

When you're uncertain where a piece of content belongs, ask three questions in order:

1. **Is it a fact about how things work today?** → process doc. (What exists, who does what, how it's applied, what it produces.)
2. **Is it an argument about why things are this way, or what could change?** → analysis doc. (Why something exists, what it tries to solve, the strategic case for changing it.)
3. **Is it a number that quantifies an opportunity?** → model doc. (Volumes, rates, financial impact, scenario sensitivity.)

**Tie-breaker test:** "Would this still be true if no one ever changed anything?" If yes → it's a fact, process owns it. If no → it's an argument (analysis) or a projection (model).

### Abstract worked example — a structured decision framework

A "structured decision framework used by a reviewer to make a categorical decision" (regulatory rubric, clinical scoring system, credit-risk grade table, claim-triage matrix — anything in this shape) gets split cleanly across the three layers:

| Content | Layer | Why |
|---|---|---|
| The framework itself (the categories, their criteria, the resulting outcomes) | **Process** §7 Decision points + business rules | Operational fact: this is the rubric being applied today |
| The reviewer's manual workflow (how they read inputs, apply the rubric, log the decision) | **Process** §6 Activities | Operational fact: this is how the work happens |
| Scope of when the rubric applies (which cases / triggers it covers) | **Process** §2 Triggers + §7 | Operational fact: defines applicability |
| The authoring body (who maintains the rubric) | **Process** §3 Actors + §10 Sources | Operational fact: who is responsible |
| Known reviewer-to-reviewer variance | **Process** §9 Pain points | Operational observation about current state |
| **Why** the framework exists (what variance problem it was created to solve) | **Analysis** | Argument about historical / strategic motivation |
| **Why** there are multiple variants of the framework (if applicable) | **Analysis** | Argument about evolutionary divergence |
| Strategic implications of category distribution (e.g., "most cases fall in categories X and Y → automation candidate") | **Analysis** | Argument about what could change |
| Path to computability / automation / restructuring | **Analysis** | Argument about future state |
| What computability / automation does **not** eliminate | **Analysis** | Strategic caveat |
| The headline rate (e.g., "80% approval rate") | **Model** input + **Analysis** strategic frame | Number → model; interpretation → analysis |
| Estimated distribution across categories | **Model** assumption | Quantification |
| Financial impact of automating selected categories | **Model** | Quantification |

The same concept appears in all three docs, but each owns a different *facet*. The process doc reader gets the operational picture; the analysis reader gets the argument; the model reader gets the numbers. None of them needs the others to make sense of their own layer.

### Soft-reference principle

The layers cross-reference each other *as pointers, not as dependencies*.

- **Each layer is independently complete.** A reader of one doc should be able to understand it without reading the others. Cross-references add depth, not prerequisites.
- **Cross-references are light.** When a process doc mentions a concept the analysis doc unpacks strategically, the process doc names it briefly + links — it does not summarise the strategic argument.
- **Linkage is many-to-many, not strict.** An analysis can spawn 0..n processes (some strategic frames have no operational process to digitise). A model is typically anchored to one analysis and may draw KPI / volume / rate inputs from one or more processes. A process can be informed by multiple analyses (cross-cutting strategic frames).
- **Do not create dependencies that block one layer on another.** If the analysis doc doesn't exist yet, the process doc still ships. If the model doc doesn't exist yet, the process doc still ships. Layers are independent artifacts, not phases of a single document.

### When in doubt — the symptom test

If you're scaffolding a process doc and you find yourself writing:

- "*Why* this matters..." → that paragraph belongs in analysis. Move it out, link to it.
- "*If this changed*..." or "*The opportunity to*..." → analysis.
- A CHF / $ / € number with a multi-year projection → model.
- A pricing tier or revenue split → model.
- "*Today the process is broken because of X*" (descriptive) → process §9 pain points.
- "*The way to fix this is Y*" (prescriptive) → analysis.

When the user asks you to produce a process doc but the conversation has been about strategy or quantification, gently surface this distinction and confirm they want the descriptive layer.

---

## Common patterns to apply

1. **Actor swim-lanes** — every Mermaid sequence diagram in §6 should put actors as named participants at the top. This makes the BPMN-pool mapping trivial.

2. **Cite the legal article for every regulatory claim.** Telegraphic style: don't paraphrase the law — link to fedlex.admin.ch (CH) or equivalent and quote when the wording matters.

3. **Distinguish format from transport.** When a process involves both *what data is in the artifact* (form content, message schema) and *how it travels* (mail, XML, API), separate the two cleanly. Conflating them is a common source of confusion (e.g., conflating SGV form content with eKOGU XML transport).

4. **"What's broken today" must map to product opportunities** *implicitly* — by being honest about pain points — but the doc itself should NOT argue for a product. Product framing lives in the analysis doc.

5. **Sources by quality tier:**
   - ★★★★★ Primary government / regulatory (the law itself, primary statistics)
   - ★★★★ Primary industry data (single-source authoritative)
   - ★★★ Industry-published, triangulated across sources
   - ★★ Internal knowledge / vendor marketing — directional
   - ★ Anecdote / single weak signal — cite with caveat

6. **Process docs are versioned via `doc-version` in the HTML comment at the top.** Bump on substantive structural changes (new section, deletion, renumbering). Add a `last-updated: YYYY-MM-DD` field when patches are made without structural change.

7. **Changelog at the bottom** captures structural changes. Patches don't need entries; section additions / deletions / renumbering do.

---

## Sizing heuristics

| Element | Recommended | Source |
|---|---|---|
| Actors per process | 2–6 | Practitioner — more signals the process is too broad |
| Activities per actor in §6 | 5–15 | Practitioner |
| KPIs in §8 | 3–8 (minimum 3 mandatory) | Practitioner — fewer = narrative, not process |
| Decision points in §7 | 1–6 | Practitioner — more signals the process should be split |
| Open Items in §11 on first scaffold | 0 (empty is correct; placeholder-only rows are forbidden per `rules/open-items-governance.md` §2) | Governance contract |

**If any number exceeds the recommended range, reconsider:**
- Too many actors (>6) → the process spans too many organisational boundaries; split into sub-processes or use a higher-level coordinator actor.
- Too many activities per actor (>15) → the actor's lane is too detailed; group related steps or decompose into a child process.
- Too few KPIs (<3) → the process has no measurable outcomes; seed candidate KPI rows even if values are `_TODO_`. (Scaffold debt, not open items — keep separate.)
- Too many decision points (>6) → the process has too much branching logic; consider whether variants deserve separate process docs.

---

## Finding the right folder

Process docs typically live in:

- `docs/business/05a-processes/` — when the project has a business/operations-oriented docs root
- `docs/operations/processes/` — for ops-heavy projects
- `docs/<domain>/processes/` — when the domain is more specific

**Always check for an existing processes folder first:**

```bash
find docs -type d -name "processes" 2>/dev/null
```

**Never overwrite an existing process file.** Switch modes if it exists:
- Scaffold mode → skip (report what's already there).
- Fill mode → open the existing file and fill empty sections; never regenerate wholesale.
- Update mode → targeted edits + changelog only.

If multiple candidates exist, ask the user. If none exists, ask whether to create one and where.

If the project has an index file (e.g., `docs/business/index.md`) listing existing processes, append a row.

---

## Reference materials

Three files in `references/` carry the canonical content. Read them when needed:

- **`references/template.md`** — the canonical process-doc skeleton. Copy this to `{processes folder}/proc-NN-{slug}.md` and fill placeholders.
- **`references/logic-and-sequence.md`** — plain-English explanation of why each section exists, how the sections map to BPMN, and the 9-step sequence you follow when filling the template.
- **`references/examples.md`** — abstract worked examples for two common process shapes (regulatory-submission process; back-office triage process), showing how the template gets filled.

---

## Sync Open Items to the central ledger

After the process file is created or updated, chain to the `util-open-items` skill to sync rows from §11 `## Open Items` into the central living ledger at `docs/project-control/open-items/open-items.md`.

- **Local first, ledger second.** The process doc's §11 table is the authoring surface; the ledger at `docs/project-control/open-items/` is the consolidated read-out. Always populate §11 first (rows carry `Source anchor` + `Source heading` pointing into the originating sub-section, e.g. `#7-decisions` + "§7 Decision points + business rules"), then invoke sync.
- **Sync preserves provenance.** `util-open-items` carries `Source anchor` and `Source heading` forward unchanged so each ledger row navigates back into the originating §-section of this process (per `rules/open-items-governance.md` §4 + §5).
- **Sync mints canonical IDs.** Local placeholder `OI-NNN` IDs are reassigned to ledger-canonical `OI-NNNN` on first sync.
- **Skip when empty.** If §11 reads `_None at present._`, do not invoke the sync. Inline `_TODO_` placeholders in §8 KPIs or elsewhere are scaffold debt — they MUST NOT be mirrored to the ledger.
- **Mode coverage.** Run sync after Mode 2 Fill and after Mode 3 Update when those modes touch §11. Mode 1 Scaffold has no actionable open items yet (§11 initialises empty), so sync is skipped.

Invoke as: "Sync open items for `{processes folder}/proc-NN-{slug}.md` via the util-open-items skill in sync mode."

---

## Closing report to the user

After generating the process file and updating any index, summarise in 4–6 lines:

1. **File created** at `{path}` (and the index updated, if applicable).
2. **What got pre-filled** vs `_TODO_` — be specific about actors, data stores, KPIs.
3. **Top 3 validation priorities** — usually the §11 TODO rows marked 🔴.
4. **Which KPI matters most** — the one that would catch the most operational drift if it moved.
5. **BPMN-readiness check** — confirm explicitly that actors, activities, data stores, data objects, triggers, and decisions are all present (even if some cells are `_TODO_`). This signals to the user that the doc is structurally complete for downstream BPMN work.

Keep it short. The user will read the file directly; your job is to point them at the next move.

---

## Checklist

Before declaring the work done:

- [ ] Folder identified or created.
- [ ] Process file exists at the correct path (scaffold / fill mode).
- [ ] §6 decomposition axis chosen and documented if non-default (fill mode).
- [ ] §0 Master flow Mermaid diagram present (not empty).
- [ ] §2 Triggers table has at least one row.
- [ ] §3 Actors table populated (or honest `_TODO_`).
- [ ] §8 KPIs table has ≥3 starter rows (even if values are `_TODO_`).
- [ ] §11 §Open Items section present with canonical schema from `rules/open-items-governance.md` §4; populated only with actionable unresolved work (or `_None at present._` if empty). No placeholder-only rows.
- [ ] No strategic argument or "what should change" content leaked into the process doc.
- [ ] No BPMN XML generated — markdown source-of-truth only.
- [ ] Processes index updated if the project has one.
- [ ] Closing report delivered.
