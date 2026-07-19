# Logic and sequence — why each section exists

This doc explains the reasoning behind the canonical template structure and the 9-step sequence for filling it. Read this when explaining the structure to the user, or when you need to defend a structural choice.

---

## The 11 sections and why they exist

### §0 — Master flow (one Mermaid diagram)

**Why:** the reader needs a 30-second mental model before they read 500 lines of prose. Without §0, every reader spends the first few sections building the mental model themselves, in different ways — which means downstream interpretations diverge.

**What good looks like:** the diagram fits on one screen. Every actor and every major decision point is named. Edges are labelled with what flows on them. If the diagram requires panning to read, it's too detailed for §0 — push detail into §6.

### §1 — What this process is

**Why:** descriptive frame, not strategic argument. Future readers will use this section to know whether they're reading the right doc. The scope statement (start point → end point) eliminates the most common cause of confusion.

**Telegraphic:** 2–3 paragraphs maximum. Detail goes into the sections below.

### §2 — Triggers

**Why:** BPMN's most fundamental concept is the Start Event. Without explicit triggers, no one can produce a BPMN diagram from the doc. Multiple triggers with branching logic are common (e.g., a single workflow with three distinct legal triggers); use a Mermaid decision tree when this is the case.

**Common error:** mixing triggers with first-step activities. A trigger is the *condition that causes the process to start*; the first activity is *what happens because the trigger fired*.

### §3 — Actors

**Why:** every BPMN pool / lane is an actor. The Authority and Decision rights columns are how you avoid the most common process-design mistake — assigning a decision to an actor who lacks the legal or contractual basis to make it. The Statutory column forces source-grounding.

**Cross-cutting actors:** some actors influence the process without owning a step (e.g., a regulatory observer, a software vendor whose product everyone uses, a pharma rep who provides templates). Include them but mark explicitly.

### §4 — Data Stores

**Why:** systems are where the actors' work lives. Without naming systems, you can't reason about data freshness, source-of-truth conflicts, or integration debt. The "Authoritative for" column is the most important — it surfaces which system *should* be canonical for each fact.

**Format / API column:** tells the BPMN modeler whether they need an arrow into a Data Store object or a Message Flow.

### §5 — Data Objects

**Why:** Data Objects are what flow between actors. They're the BPMN concept that maps to "the things on the desk" — forms, decisions, invoices, claims. Naming them explicitly means each downstream §6 step can refer to them precisely.

**Content vs. transport:** the single most common analysis error is conflating *what's in the object* with *how it travels*. When relevant, separate cleanly. Example: a Kostengutsprache form has form CONTENT (the questions, the patient data, the clinical justification) and form TRANSPORT (paper / fax / portal upload / XML message). These are governed by different bodies, evolve on different timelines, and address different pain points.

### §6 — Activities (step-by-step)

**Why:** this is the heart of the doc. Each actor's flow gets its own subsection with a sequence diagram and numbered steps. The numbered steps tell *what happens*; the sequence diagram tells *who talks to whom and in what order*.

**Why per-actor subsections (not one giant flow):** the per-actor structure maps directly to BPMN swim-lane decomposition. One section per lane = clean BPMN export. If you organise §6 chronologically across actors, you'll find the BPMN modelling unnatural.

**Failure modes per subsection:** every step has things that go wrong. Documenting failure modes is what separates an operator-grade doc from a happy-path narrative.

### §7 — Decision points + business rules

**Why:** BPMN gateways have to be grounded in rules. Without §7, the gateways in §6 sequence diagrams are floating — anyone can interpret them.

**Provenance column is the killer feature:** "rule comes from this statute / this contract / this SOP" — without provenance, rules are tribal knowledge and the process is brittle.

### §8 — KPIs (MANDATORY, never empty)

**Why:** a process without KPIs is a narrative. The KPI list defines what the process *should be measuring*; the current values tell the operator whether the process is healthy.

**Seed the list even with no current values:** the KPI definition is more valuable than the measurement. If the operator doesn't have a metric for time-to-decision, that itself is the finding — surface it as a §11 TODO.

**Why these 5 KPI patterns:**

- *Time-to-decision* — operational latency, most commonly asked-about
- *Approval / denial / pend rate* — outcome mix, drives capacity planning
- *First-pass completeness* — quality of inbound, drives rework
- *Statutory deadline compliance* — regulatory exposure
- *Volume + growth* — capacity exposure

Adapt to process type per the SKILL.md "Common KPI patterns" guidance.

### §9 — What's broken today (pain points)

**Why:** descriptive operator-grade observations. NOT strategic argument. Each pain point names who experiences it, where in the process, and what the operational impact is.

**The discipline:** do NOT propose solutions here. Solution framing lives in an analysis doc (or a product spec). The process doc states the problem; the analysis doc argues the response.

### §10 — Sources

**Why:** every claim should trace to a source. The four categories cover the full source-quality spectrum from primary regulatory to internal companion docs.

**Source-quality stars:** use the same ★★★★★ → ★ scale from the business-quantitative-model skill for consistency across the docs lifecycle.

### §11 — Open Items

**Why:** the document-level canonical Open Items section per the `metamodel` skill's `references/open-items-governance.md` §1. Captures only **actionable unresolved work** for the process: `doc-gap` / `decision-gap` / `execution-item` / `tech-debt`. Each row uses the canonical schema (OI-ID · Type · Summary · Source anchor · Source heading · Resolution path · Priority · Status · Owner · Due / Review date · Tracker ref).

**Discipline:** inline `_TODO_` markers in the body are scaffold debt, NOT open items. Do not mirror them into §11. Empty is acceptable — `_None at present._` is the correct initial state when no actionable unresolved work exists yet. Skills MAY append a `§` column AFTER `Tracker ref` for intra-doc navigation; canonical columns must not be reordered or removed.

### Changelog

**Why:** structural changes (new section, deletion, renumbering, major scope shift) need to be visible to readers who have read prior versions. Patches don't need entries.

---

## The 9-step sequence to fill the template

Follow this order when populating a new process doc. The order matters — each step depends on what was decided in the prior step.

1. **Frontmatter + §1** — establish what this process is and what it is not. Scope: start point → end point.
2. **§3 Actors** — list every actor before you describe activities. You can't write good §6 without knowing your cast.
3. **§4 Data Stores** — list the systems each actor reads from / writes to. Some of these will surface only when writing §6, but seeding §4 early prevents activity descriptions from being vague about *where* data lives.
4. **§5 Data Objects** — list the artifacts that flow. Define content vs. transport if applicable.
5. **§2 Triggers** — now that actors and objects exist, define what starts the process. (Counter-intuitive ordering, but it works: triggers often reference actors and objects, so define those first.)
6. **§6 Activities** — write the step-by-step walkthrough per actor. This will likely surface gaps that send you back to §3, §4, §5 to update.
7. **§0 Master flow** — write the master Mermaid diagram LAST among the descriptive sections. The master diagram should reflect the §6 detail; if you draw it first, you'll constrain §6 to fit your premature picture.
8. **§7 Decision points + §8 KPIs + §9 Pain points** — these layer over §6. §7 names the rules behind the decisions in §6 sequence diagrams. §8 names what to measure to know §6 is healthy. §9 names what hurts.
9. **§10 Sources + §11 Open Items + Changelog** — close the doc with provenance. §10 is the source ladder; §11 captures actionable unresolved work per the canonical Open Items schema (NOT a dumping ground for inline `_TODO_` placeholders — those are scaffold debt and stay inline); Changelog records that this is v1.

**One common pitfall:** writing §6 before §3+§4+§5. You'll end up with vague activity descriptions ("the system sends the form to the insurer") because you haven't precisely defined "the system", "the form", or "the insurer". Define your nouns first.

---

## When to break the template

The template is opinionated but not religious. The §6 Activities section is the most common place where a strict template fight produces a worse doc than a thoughtful deviation. Five legitimate reasons to deviate:

### 1. Process has no human actors

Purely automated pipelines. Drop §3 detail to "system components" and reweight §4 Data Stores + §5 Data Objects accordingly. The §6 sequence diagrams still work — participants are services, not roles.

### 2. Process is a continuous loop with no defined end

Monitoring processes, evergreen reconciliation, surveillance. §1 should explicitly say "no defined end state"; §8 KPIs become the primary deliverable; §6 activities are described as ongoing duties of each actor, not numbered one-time steps.

### 3. Process spans multiple regulatory jurisdictions

The same process runs differently in different jurisdictions (cantonal variation in CH, state variation in US, EU member-state variation). Add a §3.1 jurisdiction-by-jurisdiction actor mapping; the §7 decision-rule provenance cites jurisdiction-specific sources; otherwise the single-table §3 won't capture the complexity.

### 4. Process is fundamentally variant-organised (by request type, not by actor)

**Recognise this when:** the process has 3+ structurally distinct sub-flows that share the same actors but differ in steps, decision criteria, and outcomes — and forcing them into a per-actor §6 decomposition would fragment each sub-flow across multiple actor lanes, losing narrative flow.

**Example:** a Swiss LS-admission process where the same OFSP/EAK/Swissmedic actors handle structurally different request types (new-admission ND, triennial review, special-track applications, radiation/delisting). Per-actor §6 would scatter each request type across lanes; per-variant §6 keeps each variant's narrative coherent.

**How to apply:** organise §6 sub-sections **by variant**, not by actor. Each §6.x is a complete variant walkthrough including the per-actor interactions for that variant. §3 Actors stays at the top as a unified table; §7 Decision points may need per-variant sub-sections. Mention in the frontmatter blockquote that "§6 is organised by request type, not by actor — see [variant axis] below."

**Trade-off:** loses some BPMN-pool-mapping convenience (a BPMN modeler will need to re-decompose by lane), but gains narrative readability for a domain where the variants are the primary organising axis.

### 5. Process is fundamentally channel-bifurcated

**Recognise this when:** the process has two (rarely three) parallel channels that share the same trigger and end goal but differ structurally in actors, data flows, and rules — and the channel choice itself is a first-class concept that readers must hold throughout.

**Example:** a Swiss Preismodelle rebate-flow process with Channel A (insurer-direct rebates from MAH) and Channel B (volume-based rebates pooled via Institution commune LAMal). The two channels share the trigger ("a Preismodelle drug is dispensed") and the goal ("MAH transfers rebate"), but have different actors, different visibility on the LS, different reconciliation cadences, different aggregation rules.

**How to apply:** keep the per-channel axis as the primary organising principle. §3 Actors gets a "Channel A / Channel B" column. §4 Data Stores splits by channel where systems differ. §5 Data Objects gets per-channel rows. §6 Activities subsections each describe one channel end-to-end. §7 Decision points includes the "which channel applies" gateway prominently. Mention in the frontmatter blockquote: "§6 is organised by channel (A vs B), not by actor — channel choice is a first-class concept in this process."

**Trade-off:** same as variant — loses some BPMN-pool symmetry, but a single-axis decomposition would obscure the channel differentiation that operators *need* to keep in mind constantly. The channel axis IS the operational reality.

---

**In all five cases, document the deviation in the doc's frontmatter blockquote** so future readers understand why this doc doesn't match the template precisely. Format:

```
> **Template deviation:** §6 Activities is organised by {variant / channel / etc.}
> rather than per-actor, because {one-sentence rationale}. The per-actor unified
> table appears at §3.
```

---

## Detecting which exception applies

When you're stuck deciding whether the per-actor template fits, ask:

1. **Can I name 3+ distinct sub-flows that share the same actors but differ structurally?** → Exception 4 (by variant)
2. **Are there 2 channels/paths that exist in parallel for the full process duration?** → Exception 5 (by channel)
3. **Is the process running constantly with no instance boundary?** → Exception 2 (continuous loop)
4. **Are there no human actors at all?** → Exception 1 (automated pipeline)
5. **Does the process exist in N different forms across jurisdictions?** → Exception 3 (multi-jurisdictional)
6. **None of the above?** → Use the standard per-actor template. If the per-actor structure feels awkward but doesn't match any exception, the more likely problem is that §3 Actors hasn't been worked through carefully enough — go back and refine the actor list before deciding to deviate.

When in doubt, **default to the standard template**. Deviations are escape hatches for genuine misfit, not licence to redesign the structure to taste.
