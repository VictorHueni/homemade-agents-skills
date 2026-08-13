---
name: plan-delivery-roadmap
license: MIT
description: "Create a Delivery Roadmap — the Plan by Feature artefact that groups FBS functionalities into named, scoped, priority-ordered epics (E-NN), defines the MVP walking skeleton (minimum end-to-end journey), and declares per-phase goals expressed as value streams made operational. Bridges FBS (what the product does), value streams (how value flows), and PRDs (what we build next). Serves simultaneously as delivery planning tool (E-NN clusters, FBS scope, PRD links) and product roadmap (phase goals, walking skeleton, business narrative). For a solo founder or small team, one document serves both audiences. Triggers on: delivery roadmap, epic catalogue, epic list, plan by feature, group features into epics, define epics, epic planning, feature grouping, epic scope, what PRDs to write, product roadmap, phase plan, MVP slice, walking skeleton, release plan, what do we build next."
user-invocable: true
metadata:
  category: "planning"
  complexity: "medium"
  version: "1.2.0"
  status: active
  last_reviewed: 2026-08-13
  impact: "low"
---

# Delivery Roadmap Builder

You are an expert at producing **Delivery Roadmaps** — the artefact that
answers two questions simultaneously:

1. **Delivery planning (team-facing):** "Given everything in the FBS, what
   clusters together into coherent delivery units, and in what order do we
   build them?" → E-NN epics with stable IDs, FBS scope lists, PRD links.

2. **Product roadmap (stakeholder-facing):** "What does the product deliver
   at each milestone, and what can users actually DO after each phase ships?"
   → Walking Skeleton (MVP) and per-phase goal statements expressed as value
   streams made operational.

For a solo founder or small team, one document serves both audiences. When
audiences diverge (investors vs developers), extract a stakeholder copy —
the delivery roadmap remains the source of truth.

The artefact lives at `docs/plans/delivery-roadmap.md`.

---

## Methodology foundation

| Source | What it anchors |
|---|---|
| Coad, P. & De Luca, J. (1999). *Java Modeling in Color with UML.* Prentice Hall. | FDD Phase 3 "Plan by Feature" — feature set → delivery unit → milestone; the epic as a named Business Activity cluster |
| Leffingwell, D. (2011). *Agile Software Requirements.* Addison-Wesley. | Feature as programme-level delivery unit; grouping heuristics; outcome-orientation |
| Cohn, M. (2004). *User Stories Applied.* Addison-Wesley. | Epic sizing (INVEST "S"); epic as multi-sprint delivery cluster |
| Patton, J. (2014). *User Story Mapping.* O'Reilly. | Walking skeleton (release slices as phase boundaries); naming after value delivered; backbone Activities = epics |
| Beck, K. (2004). *Extreme Programming Explained*, 2nd ed. Addison-Wesley. | Walking skeleton — thin end-to-end slice that validates the architecture before filling in depth |
| BABOK v3 §9.6. IIBA (2015). | Solution scope per delivery increment; traceability from scope to requirements |

**FDD Phase 3 "Plan by Feature" — primary anchor:**
> *"For each Business Activity (feature set), identify the milestone by which
> it must be complete and its sequence relative to other feature sets."*
> — De Luca & Coad

**Walking Skeleton — MVP anchor:**
> *"A walking skeleton is a tiny implementation of the system that performs
> a small end-to-end function. It need not use the final architecture, but it
> should link together the main architectural components."*
> — Cockburn (2004), extended by Beck and Patton as the first release slice

---

## The two layers in one document

```
docs/plans/delivery-roadmap.md
│
├── §Walking Skeleton — MVP        ← PRODUCT ROADMAP LAYER
│   Hypothesis · VS anchor ·
│   FBS cut per epic · Can/Cannot
│
├── §Phase Plan                    ← PRODUCT ROADMAP LAYER
│   Phase | Epics | VS operational | Goal
│
├── §Epic Table                    ← DELIVERY PLANNING LAYER
│   E-NN | Name | VS anchor+pain |
│   Personas | FBS count | PRD | Status
│
└── §Per-epic sections             ← DELIVERY PLANNING LAYER
    Value statement · FBS scope ·
    QA-XXNN · PRD link
```

The §Walking Skeleton and §Phase Plan speak in business language (personas,
outcomes, value streams). The §Epic Table and §Per-epic sections speak in
delivery language (E-NN, C-N.M.FXX, QA-XXNN). Same document, two registers.

---

## What an epic is

**Is:** a named cluster of FBS functionalities that delivers recognisable
value to a specific persona when complete; specified in a single PRD;
has a stable E-NN ID.

**Is not:** a capability (BC Map), a user story (PRD), a sprint
(implementation plan), or a value stream (value stream doc).

**Sizing:** 5–25 FBS functionalities, 2–8 weeks of focused development.
Functionalities under a capability marked `Differentiator` (BC Map Strategic Importance —
see `business-capability-map`'s Strategic Importance column) always anchor their own epic;
this is a BC Map lookup, not a per-functionality marker (★ is shorthand for it in this
skill's prose, not a column that exists on FBS rows).

---

## What a walking skeleton is

A walking skeleton is a **horizontal slice across multiple epics** that makes
one complete value stream operational end-to-end. It is:

- The minimum set of functionalities from multiple epics that allows the
  primary persona to complete one end-to-end journey without workarounds
- Defined by a value stream (VS-N), NOT by an epic boundary
- The hypothesis-test vehicle for the core product value proposition

It is NOT:
- A vertical completion of any single epic
- The minimum possible feature
- An internal prototype

**Walking skeleton ≠ MVP:** conceptually identical here. Both mean the
minimum deployable product that validates the primary hypothesis with a
real user on a real workflow.

**Coverage rule:** every VS stage of the target value stream must have
≥ 1 functionality in the walking skeleton. If any stage is uncovered,
the persona cannot complete the journey — the skeleton is broken.

---

## Backends

Which functionality inventory this skill reads from is a **serialization** choice, per
`adr-0010` (in the consuming repo's `docs/architecture/decisions/`, e.g. the kit) — the same
`docs/product-specs/backend.yml` that `spec-functional-breakdown-structure` reads:

- **`markdown`** (default) — Mode 1 reads `docs/product-specs/07a-fbs.md` and enumerates
  `C-N.M.FXX` rows into epics, exactly as described below.
- **`github`** — Mode 2 reads the existing functionality-issue inventory
  (`type:functionality`-labelled issues) and **proposes** an epic grouping over it, rather
  than enumerating from a markdown table. This is a genuine workflow inversion: under
  `markdown`, functionalities and epics are both authored here; under `github`,
  functionalities are already born in the tracker by `spec-functional-breakdown-structure`,
  and this skill's job is to propose and create the epic layer over them.

**Declaration** — no separate file; this skill reads the same `backend.yml` FBS declares:

```yaml
backend: github          # markdown (default) | github
repo: owner/name         # github only
project: 3                # optional — Project v2 number
```

**Operational github mapping.** Before running Mode 2, read
[`references/github-backend.md`](references/github-backend.md) — the epic-side mapping,
what's mechanically derivable from the functionality inventory (including differentiator
anchoring, resolved via the BC Map's Strategic Importance column — no GitHub primitive
needed) vs what still needs operator confirmation (phase only — no GitHub primitive carries
it, see the reference doc §5), and
[`../spec-functional-breakdown-structure/references/github-backend.md`](../spec-functional-breakdown-structure/references/github-backend.md)
for the functionality-side mapping this mode reads as its input.

---

## Mode 1 — Generate (`backend: markdown`)

### Step 0 — Read all upstream artefacts

```bash
cat docs/VISION.md 2>/dev/null                                     # optional: read if exists — phase goals should connect to vision north star
cat docs/product-specs/07a-fbs.md
cat docs/business/03a-capability-map.md                            # Strategic Importance column — differentiator anchoring
cat docs/business/04a-value-streams.md
cat docs/business/01a-personas.md
cat docs/product-specs/09a-quality-attributes.md                   # optional
```

**From FBS extract:**
- Every C-N.M.FXX with VS stage link, phase tag (Phase 1/2/3)
- Total count by phase

**From the BC Map extract:**
- Strategic Importance per capability (`Differentiator` / `Necessary` / `Commodity`) — a
  functionality's differentiator status is its parent capability's, not a column on the FBS
  row itself.

**From value streams extract:**
- Pain index per VS stage (Critical → High → Medium → Low)
- Triggering persona per VS
- Value proposition per VS (vocabulary for phase goal statements)

**From personas extract:**
- P-NN name and role (for "what P-NN can do" narrative)
- Primary device + usage context (for walking skeleton framing)

### Step 1 — Group FBS into epics

Apply these heuristics in order:

1. **VS stage affinity** — functionalities with the same VS stage link
   cluster together. Functionalities with `—` attach to the most
   contextually relevant capability domain epic.

2. **Capability domain coherence** — within a VS stage group, check
   whether functionalities span multiple L0 domains. If they span
   configuration domains (C1 + C2), they may form one setup epic.

3. **Differentiator anchoring** — any functionality whose parent capability is marked
   `Differentiator` (BC Map Strategic Importance) anchors its own epic. Never merge such a
   functionality into a secondary epic.

4. **Phase boundary** — Phase 2 functionalities always form separate
   epics from Phase 1 functionalities.

5. **Sizing check** — < 5 rows: consider merging. > 25 rows: split by
   VS stage or capability boundary.

### Step 2 — Name each epic

Name after the **value delivered**, not the features implemented.
Test: "When this epic ships, [persona] can [outcome]."

| ❌ Feature-oriented | ✅ Value-oriented |
|---|---|
| "Configuration Module" | "Clinic & Workforce Configuration" |
| "Schedule Algorithm" | "Semester Schedule Generation" |
| "Notifications" | "Surgeon Confirmation Loop" |

### Step 3 — Order by priority

1. Critical pain stages first
2. High pain stages next
3. Prerequisites (setup/config epics) before features they enable
4. Same pain level → Phase 1 before Phase 2

Assign E-NN IDs in priority order. IDs are **permanent** — never recycled.

### Step 4 — Define the Walking Skeleton

1. **Identify the primary VS to validate** — the one with the most
   Critical-pain stages whose end-to-end completion proves the core
   hypothesis.

2. **Select the minimum functionalities per epic** needed to cover
   every stage of that VS. This is a horizontal cut — not epic
   completion.

3. **Run the coverage check** — every VS stage of the target VS must
   have ≥ 1 functionality in the cut. Flag any uncovered stage.

4. **Write the "can / cannot yet" statement** — what the primary
   persona can accomplish after the walking skeleton ships, and what
   is explicitly deferred to Phase 1 completion.

### Step 5 — Define the Phase Plan

For each phase:
- **Which epics are complete**
- **Which value streams become fully operational** — meaning all their
  stages are covered by shipped functionalities. Not "partially" — fully.
- **One-sentence goal** completing: "After this phase, [P-NN] can
  [end-to-end outcome] without [current workaround]."

### Step 6 — Write the delivery roadmap

Produce the full document per the output structure below.

### Step 7 — Coverage check

Verify every Phase 1 FBS functionality appears in exactly one epic:

```bash
grep -o "C[0-9]\.[0-9]\.F[0-9][0-9]" \
  docs/plans/delivery-roadmap.md | sort | uniq | wc -l
```

Compare to Phase 1 FBS total. Flag orphaned functionalities.

---

## Mode 2 — Propose epics from backend (`backend: github`)

Read [`references/github-backend.md`](references/github-backend.md) before running this
mode. Steps not listed here are identical to Mode 1 — only the functionality source and the
epic-creation target change.

### Step 0 — Read the functionality inventory

```bash
gh issue list --repo <repo> --label type:functionality --state all --json number,title,body
```

Parse each issue's `Capability: C-N.M` line (always present) and `VS stage: VS-N.M` line
(present when set). Read `docs/business/03a-capability-map.md` for Strategic Importance per
capability, and `docs/business/04a-value-streams.md` and `docs/business/01a-personas.md`
exactly as Mode 1 — all three stay markdown regardless of the FBS backend.

### Step 1 — Group the inventory into proposed epics

Apply VS-stage affinity, capability-domain coherence, differentiator anchoring, and the
sizing check mechanically (same heuristics as Mode 1 Step 1; §3 of the reference doc marks
these as backend-derivable — differentiator anchoring resolves via each functionality's
`Capability:` line against the BC Map's Strategic Importance, no GitHub primitive needed). Do
**not** attempt to infer phase boundary — no GitHub primitive carries it and no existing
roadmap doc exists yet to read it from (reference doc §5, the one genuinely open gap). Present
the mechanically-grouped proposal to the operator and ask, per proposed group: "which phase
does this group belong to?" Fold the answer back into the grouping before proceeding — this is
a **proposal**, not a batch import; the operator reviews before anything is created.

### Steps 2–5 — Name, order, walking skeleton, phase plan

Identical to Mode 1 Steps 2–5. Ordering (Step 3) still reads pain index from value streams,
unaffected by backend. Phase Plan (Step 5) uses the operator-confirmed phase from Step 1
above, not an inferred column.

### Step 6 — Create the epics and write the roadmap

1. For each confirmed group, create the epic issue and attach its member functionality
   issues as native sub-issues per `references/github-backend.md` §4.
2. Write `docs/plans/delivery-roadmap.md`'s narrative sections (Walking Skeleton hypothesis,
   Phase Plan goals, "can/cannot yet") exactly as Mode 1 — these have no GitHub primitive and
   stay authored prose.
3. Render §Epic Table and §Per-epic §FBS-scope tables as a **read-out** of the just-created
   GitHub structure (epic issue number, its sub-issues, each sub-issue's `Capability:`/`VS
   stage:` lines) rather than hand-authoring them — they are a snapshot, regenerable by
   re-running this step.

### Step 7 — Coverage check

```bash
gh issue list --repo <repo> --label type:functionality --state all --json number | jq length
```

Compare against the total count of functionality issues attached as sub-issues across every
created epic (`gh issue view <epic> --json subIssuesSummary`, summed). Flag any functionality
issue not attached to exactly one epic.

---

## Output structure

```markdown
<!-- doc-version: 1.0 | created: YYYY-MM-DD -->

# {{product}} — Delivery Roadmap

Intro: dual purpose (delivery plan + product roadmap), methodology
pointer, companion docs (FBS, VS, QA, personas).

---

## Walking Skeleton — MVP

**Hypothesis to validate:** [core product assumption — one sentence]
**Value stream delivered end-to-end:** [VS-N · Name](link) — Pain: Critical

| Epic | MVP functionalities | Deferred to Phase 1 |
|---|---|---|
| E-NN | C-N.M.FXX · … | [what is skipped and why] |

**After MVP ships, [P-NN] can:**
1. [Concrete action 1]
2. [Concrete action 2]
…

**After MVP ships, [P-NN] cannot yet:**
- [Deferred capability] → Phase 1 (E-NN complete)

---

## Phase Plan

| Phase | Epics | Value streams fully operational | Goal |
|---|---|---|---|
| **MVP** | E-NN (partial) … | VS-N (thin slice) | [outcome sentence without current workaround] |
| **Phase 1** | E-01 → E-NN complete | VS-N · VS-M · VS-P | [outcome sentence] |
| **Phase 2** | + E-NN | + VS-Q | [outcome sentence] |
| **Phase 3** | [TBD] | [TBD] | [outcome sentence] |

---

## Epic Table

| ID | Epic name | VS anchor | Pain | Personas | Capabilities | FBS rows | Phase | PRD | Status |
|---|---|---|---|---|---|---|---|---|---|
| E-01 | … | [VS-N.M](link) | Critical | [P-NN](link) | [C-N.M](link) | N | 1 | _TODO_ | ⬜ |

---

## Epics

### E-01 · [Name]

**Value statement:** When this epic ships, [P-NN] can [outcome].
**Objective:** [OBJ-NN · Objective title](link to objectives.md) *(if objectives doc exists)*
**VS anchor:** [VS-N.M · Stage name](link) — Pain: Critical / High / Medium
**Personas:** [P-NN](link)
**Capabilities:** [C-N.M](link to BC Map)
**Phase:** Phase N
**PRD:** _TODO_
**Quality attributes in scope:** [QA-XXNN] (if QA doc exists)
**Sizing:** N functionalities — within / below / above range (5–25)

**FBS scope:**

| ID | Functionality | Status |
|---|---|---|
| C-N.M.FXX | … | ⬜ |

---

## Changelog

| Date | Change | Author |
|---|---|---|
| YYYY-MM-DD | Initial generation | … |
```

- Open every generated file with the standard artefact frontmatter (OKF-superset block — set `type` to this artefact's `okf_type` display name from the `metamodel` skill's `references/artefact-types-registry.yaml`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`). Run `git config user.name` for `owner`. Set `status: draft` on initial scaffold. Default `review_interval: 60d`. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`.

---

## Epic ID convention

`E-NN` — two-digit zero-padded, assigned in priority order, permanent.
Retired epics: marked ❌ with a note; row preserved, ID not reused.
PRDs reference epics as `E-NN · [name]` in §0 Architecture Traceability.

**Under `backend: github`:** identity is the epic issue's `#N` (native, never recycled);
`E-NN` minting is retired for that project, mirroring `C-N.M.FXX`'s retirement on the
functionality side. PRDs reference epics as `#N` instead.

---

## Discipline checks

Before declaring complete:

- [ ] Every Phase 1 FBS functionality in exactly one epic (coverage check run)
- [ ] Walking skeleton covers every stage of target VS end-to-end (no broken stages)
- [ ] "Cannot yet" block is explicit — no false completeness in MVP framing
- [ ] Every epic has a value statement ("when this ships, P-NN can…")
- [ ] Every epic references ≥1 OBJ-NN (when objectives doc exists at `docs/business/04b-objectives.md`)
- [ ] Phase goals express VS streams operational, not feature lists
- [ ] Functionalities under a `Differentiator` (BC Map Strategic Importance) capability each anchor their own epic
- [ ] E-NN IDs in pain-index priority order (Critical before High before Medium)
- [ ] Sizing within 5–25 FBS rows per epic (outliers flagged)
- [ ] Phase 2 epics listed after all Phase 1 epics

**Under `backend: github`** (Mode 2), in addition to the backend-independent checks above:
- [ ] Every proposed epic's phase question was put to the operator, never inferred (`references/github-backend.md` §5 — the one genuinely open gap; differentiator anchoring is resolved via the BC Map, not asked)
- [ ] Every functionality issue attached as a sub-issue of exactly one epic (coverage check run)
- [ ] §Epic Table / §FBS-scope tables in `delivery-roadmap.md` are a fresh read-out, not stale from a prior run

---

## Reference materials

Two files carry the `github`-backend content. Read before running Mode 2:

- **`references/github-backend.md`** — the epic-side mapping (this skill). Never copied into the project.
- **`../spec-functional-breakdown-structure/references/github-backend.md`** — the functionality-side mapping Mode 2 reads as input. Never copied into the project.

---

## Cross-references

| Reads | Why |
|---|---|
| FBS — `docs/product-specs/07a-fbs.md` (`markdown` backend) or `type:functionality`-labelled issues (`github` backend, per `backend.yml`) | Primary input — every functionality lands in an epic |
| Value streams (`VS-N.M` pain index + value proposition per VS) | Epic priority + phase goal vocabulary |
| Personas (`P-NN` device + context) | Walking skeleton "can/cannot yet" narrative |
| Quality attributes (`QA-XXNN`) | Optional — which QA entries apply per epic scope |
| Business objectives (`OBJ-NN` + `KR-NN.M`) | Optional — epics reference `OBJ-NN` in value statement; traceability matrix links each E-NN to the objective it serves |

| Feeds | How |
|---|---|
| PRDs | One PRD per epic; PRD §0 references `E-NN` + FBS scope list |
| Implementation plans | Via PRD → epic chain |
| ADRs | Architectural decisions reference which epics they unblock |
