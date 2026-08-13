---
name: spec-use-case
license: MIT
description: "Create effective use cases — goal-oriented, technology-neutral behavioural specs synthesising Cockburn's Writing Effective Use Cases (goal levels, fully-dressed + casual formats, main success scenario + extensions), UML use-case diagrams (actors, «include»/«extend»), and Jacobson's Use-Case 2.0 (slices for the backlog). Mints UC-NN. Modes: scaffold (use-cases/ folder + index), fully-dressed (author one use case), casual (lightweight variant), slice (Use-Case 2.0 backlog slices), review (quality audit). Output: docs/product-specs/use-cases/ — grouped into per-capability slug subfolders when a capability map exists. Reads personas (P-NN as actors) + FBS (C-N.M.FXX); feeds PRDs, domain model, test cases. Triggers on: use case, write a use case, fully-dressed use case, main success scenario, actor goal, use case diagram, scenario, use case slice, alternate flow, extension, use case template."
user-invocable: true
metadata:
  category: "specification"
  complexity: "medium"
  version: "1.1.0"
  status: active
  last_reviewed: 2026-07-20
  review_interval: 180d
  impact: "low"
---

# Use Case Builder

You are an expert at writing **effective use cases** — goal-oriented, technology-neutral descriptions of how an actor and a system collaborate to reach a goal of value. This skill synthesises the three canonical traditions and tells you when each fits:

- **Alistair Cockburn — _Writing Effective Use Cases_ (2000)**: the textual discipline. Goal levels, design scope, primary actor + stakeholders, main success scenario + extensions, fully-dressed vs casual formats. The use case as **a contract between stakeholders about behaviour under all conditions**.
- **UML use-case diagrams (Jacobson / OMG)**: the visual overview. Actors, system boundary, `«include»` / `«extend»` / generalization. A *map* of use cases, never a substitute for the text. Render these with **`arch-uml`** (`use-case` mode → PlantUML → committed SVG); carry each `UC-NN` onto its ellipse so the diagram cross-references back to the fully-dressed text here.
- **Ivar Jacobson — _Use-Case 2.0_ (2011)**: the agile delivery layer. The same use case, **sliced** vertically into backlog-sized increments (a *use-case slice* = narrative path + its test cases), so use cases drive iterative delivery the way user stories do.

The artefact produced is **one markdown file per use case** under `docs/product-specs/use-cases/`, plus a registry `index.md`. When a capability map exists, the per-use-case files are grouped into per-capability subfolders (`use-cases/<capability-slug>/`) — see §Organizing use cases by capability. A use case is NOT a user story, NOT a PRD, NOT an FBS row, NOT a UI spec — it is **the behavioural scenario**: the numbered interaction between actor and system, every alternate path, and the guarantees that hold when it ends.

This skill is **domain-agnostic**. When activated in a project, it inherits the project's personas (as actors) and FBS functionalities (as the behaviours the use case realises).

The full methodology synthesis lives in `references/methodology.md`; the anti-patterns + quality checklist live in `references/use-case-discipline.md`. Read them when authoring or reviewing.

---

## What a "good use case" means

A use case is effective when a reader can answer, without ambiguity:

| Question | Where it lives |
|---|---|
| **Whose goal is this, and at what level?** | `Primary Actor` + `Level` (user-goal / summary / subfunction) |
| **How big is the box we're specifying?** | `Scope` (enterprise / system / subsystem) |
| **Who else cares, and what do they need protected?** | `Stakeholders and Interests` |
| **What must be true before it starts?** | `Preconditions` |
| **What does the happy path look like?** | `Main Success Scenario` (numbered actor↔system steps) |
| **What can go differently, and what happens then?** | `Extensions` (every condition at every step) |
| **What is guaranteed when it ends — success or failure?** | `Success Guarantees` + `Minimal Guarantees` |
| **What's the stable identifier?** | `UC-NN` (registry counter) |

The single most important property: **a use case is goal-oriented and technology-neutral.** It says *what the actor wants and what the system guarantees*, never *which button they click* or *which screen renders*. If you can't read it to a business stakeholder without explaining UI, it's written at the wrong level. See `references/use-case-discipline.md` for the full checklist.

---

## Hard scope rules — what does NOT belong in a use case

| Symptom | Belongs in |
|---|---|
| UI detail — "click Save", "the system shows the X screen", field layouts | UI spec / wireframe (a use case names the *intent*: "submits the order") |
| Acceptance criteria for one build slice, priority, estimates | PRD (`spec-prd`) — the use case grounds it; it does not replace it |
| A flat registry of what the system does, with status | FBS (`spec-functional-breakdown-structure`) |
| Data field types, validation regexes, schema | Domain model (`domain-model`) / interface contract |
| Non-functional targets (latency, uptime, security levels) | Quality attributes (`spec-quality-attributes`) |
| Algorithms / internal design / class structure | Architecture / implementation plan |

If a use case grows any of these, pull it out and link instead. A use case stays at the level of **observable actor↔system interaction**.

---

## Choosing the goal level and scope (do this FIRST)

Before writing a single step, fix two coordinates. Getting these wrong is the #1 cause of unusable use cases.

**Goal level** (Cockburn's altitude metaphor — full guidance in `references/use-case-discipline.md`):

| Level | Icon | Meaning | The test |
|---|---|---|---|
| **Summary** | ☁ cloud / 🪁 kite (white/blue sky) | Spans multiple user goals; gives context | Several user-goal use cases sit underneath it |
| **User goal** | 🌊 sea level (blue) | One actor, one sitting, one goal of value | The **coffee-break / 2-to-20-minute test**: the actor does it in one go, then can stop satisfied. **Most use cases live here — default to this level.** |
| **Subfunction** | 🐟 fish / 🦪 clam (indigo/black) | A step reused by several user-goal cases | Exists only because two+ user-goal cases share it (e.g. "Authenticate") |

**Design scope** — what is the "system" in this use case?

- **Enterprise / business** (black box): the whole organisation, technology-agnostic.
- **System** (the default): the software product under design.
- **Subsystem**: one component inside the product.

State `Scope` and `Level` explicitly in every use case. If you're tempted to write a use case at clam level for every CRUD verb, **stop** — that's functional decomposition, not a use case (see anti-patterns).

---

## The five modes

### Mode 1 — Scaffold

**When:** the project has no `use-cases/` folder yet.

**Output** under `docs/product-specs/use-cases/`:
- `index.md` — the use-case registry (from `templates/index.md`): a table of `UC-NN`, name, level, scope, primary actor, status, plus the methodology pointer and an optional UML actor/use-case overview placeholder.

Check for a capability map (`docs/business/03a-capability-map.md`). If it exists, scaffold the registry in its **capability-grouped** form and note that author-mode files will land under `use-cases/<capability-slug>/` subfolders (see §Organizing use cases by capability). If not, scaffold the flat single-table registry.

Do NOT invent use cases in scaffold mode. Substitute `{{product_or_scope}}`. Open the file with standard artefact frontmatter (see below).

### Mode 2 — Fully-dressed (author one use case)

**When:** the goal is high-stakes, complex, or has many alternate paths — the cost of a missed extension is high.

**Process:**
1. **Fix `Scope` + `Level`** (see above). Confirm with the user if ambiguous.
2. **Identify the primary actor** — prefer a project persona (`P-NN`); record it as the actor. Identify supporting actors (other systems/services the system calls).
3. **List stakeholders and interests** — who is *not* at the keyboard but whose interest the system must protect (the business, an auditor, the data subject).
4. **Mint the ID** — next `UC-NN` from the registry. Create `uc-NN-{slug}.md` from `templates/use-case-fully-dressed.md`, in the capability subfolder its `Realises` capability resolves to (see §Organizing use cases by capability), or the `use-cases/` root if it is unlinked or no capability map exists.
5. **Write the Main Success Scenario** — numbered steps, each `Subject verb… ` in active voice, alternating actor intent and system responsibility. 3–9 steps is the sweet spot. Each step shows *who has the ball*.
6. **Write Extensions** — walk every step; ask "what else could happen here?" Label `1a`, `1b`, `2a`… with the *condition* then the handling steps. Missing extensions is where real requirements hide.
7. **State guarantees + preconditions + trigger.**
8. **Link** — `Realises` the FBS functionalities (`C-N.M.FXX`); reference glossary terms (`GT-NN`); note the value-stream stage if relevant. The first `Realises` entry's capability determines the file's capability subfolder.
9. **Update `index.md`** — add the registry row under the use case's capability group (or the Unassigned group if unlinked).
10. **Run the quality checklist** in `references/use-case-discipline.md`.

### Mode 3 — Casual (lightweight variant)

**When:** the goal is low-risk or you're early in discovery and want speed. Cockburn's casual format trades the field structure for a few prose paragraphs.

**Output:** `uc-NN-{slug}.md` from `templates/use-case-casual.md` — title + scope/level + a paragraph for the main scenario and a short paragraph (or bullet list) for the alternate paths. Placed under the same capability-subfolder rule as Mode 2 (§Organizing use cases by capability). Still mints `UC-NN` and updates the index. Casual use cases can be **promoted to fully-dressed** later without re-numbering.

### Mode 4 — Slice (Use-Case 2.0 — feed the backlog)

**When:** the team works in sprints/Kanban and wants use cases to drive iterative delivery (the agile bridge between use cases and user stories).

**Process** (per `references/methodology.md` §Use-Case 2.0):
1. Take a fully-dressed use case. Its **basic flow** (main success scenario) is the **first slice** — the thinnest end-to-end path.
2. Each meaningful **alternative flow** (an extension run start-to-finish) becomes a further **slice**.
3. For each slice, write **its test case(s)** — the slice's acceptance criteria. *A slice without a test case is incomplete, exactly as a user story without acceptance criteria is.* `qa-test-scenario` authors the actual scenario (`UC-NN.SC-NN`) and case (`TC-NN`); this mode's own job is only to point at it.
4. Record slices in a `## Use-Case 2.0 Slices` section of the use-case file: `UC-NN.S1`, `UC-NN.S2`… with a one-line narrative + test-case pointer (the `UC-NN.SC-NN`/`TC-NN` from `qa-test-scenario`, once minted) + status. These are the backlog-ready increments.

### Mode 5 — Review (quality audit)

**When:** existing use cases need checking before they ground PRDs or domain models.

Read each use-case file (discover recursively — `use-cases/**/uc-*.md`, so capability subfolders and any manual thematic subfolder are covered) against the checklist in `references/use-case-discipline.md` and emit ranked findings (which level violation, which anti-pattern, which missing extension) with a concrete fix per finding. **Report-only — do not silently rewrite** unless asked; propose the exact edits.

---

## ID and step conventions

- **`UC-NN`** — registry counter, two digits, zero-padded, never reused even if a use case is retired. Assigned in `index.md`.
- **Main-success steps** — `1`, `2`, `3`… (plain integers).
- **Extensions** — `<step><letter>`: `1a`, `1b`, `2a`… each begins with the *condition*, then indented handling steps `1a1`, `1a2`.
- **Use-Case 2.0 slices** — `UC-NN.S1`, `UC-NN.S2`…
- **Cross-refs** — `Realises: C-N.M.F03, C-N.M.F04`; `Primary Actor: P-02`; glossary terms inline as `GT-NN`.

---

## Where use cases sit in the metamodel

Use cases are the **behavioural bridge** between the strategic/registry layer and build artefacts:

| Artefact | Owns | Use-case relationship |
|---|---|---|
| **Personas** (`P-NN`) | Who the product serves | A persona is the **primary actor** of a use case |
| **FBS** (`C-N.M.FXX`) | Flat registry of what the system does | A use case **realises** one or more functionalities — it adds the *scenario* the registry can't hold |
| **Value streams** (`VS-N.M`) | How value flows in stages | A use case often operationalises one stage's actor goal |
| **Domain glossary** (`GT-NN`) | Ubiquitous language | Use-case prose uses glossary terms verbatim |
| **Use case** *(this skill)* | The actor↔system scenario, all paths, guarantees | — |
| **PRD** (`PRD-NNNN`) | What we build for one slice + acceptance criteria | A PRD **references** the use case(s) it delivers; the scenario grounds the acceptance criteria. Its embedded stories (`PRD-NNNN.US-NN`) may carry a `Covers: UC-NN` soft edge — stories are PRD-scoped delivery slices, distinct from Use-Case 2.0 slices (see `references/methodology.md` §5) |
| **Domain model** (`BC-NN.AGG-NN`, `BC-NN.EVT-NN`) | Entities, aggregates, domain events | Use-case steps that change state map to **commands → domain events**; scenarios drive aggregate design |
| **Test cases** | Verification | Each flow yields a test scenario, which expands into test cases (`qa-test-scenario`; Use-Case 2.0 slices make the pointer explicit) |

**Soft-reference principle** (same as the rest of the kit): use cases reference other artefacts as pointers, not prerequisites. Author a use case even if the FBS or PRDs don't yet exist; add the `Realises:` links when they do.

**When a use case adds value vs duplicates:** write a use case when the *interaction has branches that matter* (alternate/exception flows whose omission is costly). For a trivial, single-path behaviour, an FBS row + a user story in a PRD is enough — don't manufacture a fully-dressed use case for "update profile". See `references/methodology.md` §Positioning.

---

## Organizing use cases by capability

By default (no capability map) all use cases live flat in `docs/product-specs/use-cases/`. **When a capability map (`docs/business/03a-capability-map.md`) exists, group the per-use-case files into per-capability subfolders** so the registry mirrors the capability structure — the layer directly above the FBS.

**Folder = the capability's canonical slug.** Every L1 capability in the map carries a `` `slug: <handle>` `` code-line under its `### C-N.M · …` heading (stable, short, globally unique — the same handle used for commit scopes). Reuse it verbatim as the folder name; never invent a new one.

```
docs/product-specs/use-cases/
  index.md                     ← registry, grouped by capability
  <capability-slug>/           ← e.g. catalog-maintenance/  (one L1 capability C-N.M)
    uc-03-....md
    uc-07-....md
  <another-capability-slug>/
    uc-05-....md
  uc-11-....md                 ← unassigned (no Realises yet) — stays at root
```

**Which folder a use case lands in:**

1. Read the use case's `Realises: C-N.M.FXX`. The functionality's parent capability is its `C-N.M` prefix.
2. Look up that capability's slug in the map; the file goes in `use-cases/<slug>/`.
3. **Multiple capabilities realised** → file it once under the **primary** capability (the one owning the use case's main goal — the first `Realises` entry); the full `Realises:` list still cross-references the others.
4. **No `Realises` yet** (soft-reference — a use case may precede the FBS), **no capability map**, or **the capability carries no slug** → leave the file at the `use-cases/` root and list it under the registry's **Unassigned** group. Re-file it when the link is added. (If the map exists but the target capability lacks a slug, prefer assigning one per `business-capability-map`'s mandatory-slug rule, then file.)

**Registry index** groups rows under one `### C-N.M · <Capability name> (`slug`)` heading per capability, plus a trailing **Unassigned** group. With no capability map, keep the single flat table.

**Discovery is recursive.** Scaffold-detection and Review mode locate use cases with `use-cases/**/uc-*.md` (never a single-level glob), so both the capability layout and any manual thematic subfolder are handled.

> **Metamodel note.** The canonical use-case `default_path` is a structural fact owned by the **clew** repo (kit ADR-0007); this capability-subfolder layout is a projection of it. Until clew's registry sanctions the variant, a strict metamodel Audit that assumes the flat path may flag nested files — resolve UC discovery with the recursive glob above.

---

## Inputs

| Needed | What you ask if missing |
|---|---|
| **Mode** | Detect from request (scaffold / fully-dressed / casual / slice / review). Confirm if ambiguous. |
| **Folder** | Look for `docs/product-specs/use-cases/` (search recursively — it may hold capability subfolders). If absent, default there and confirm. |
| **Capability map** | Check for `docs/business/03a-capability-map.md`. If present, switch on the capability-slug subfolder layout (§Organizing use cases by capability). |
| **Primary actor** | A project persona (`P-NN`) if one fits; else name the actor role. |
| **Goal + level** | What does the actor want, in one go? Helps fix the level. |
| **FBS existence** | Check for `docs/product-specs/07a-fbs.md` to populate `Realises:` — its capability prefix also picks the subfolder. Optional. |

Ask 2–4 questions max, single message, lettered options. Don't run a wizard.

---

## Output frontmatter

Open every generated **use-case file** (`uc-NN-*.md`) with the standard OKF-superset artefact frontmatter — `type: Use Case` (its `okf_type` in the `metamodel` skill's `references/artefact-types-registry.yaml`), plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`. Run `git config user.name` for `owner`. `status: draft` on creation. Default `review_interval: 180d` (use cases are stable behavioural specs). Full schema: the `metamodel` skill's `references/artefact-frontmatter.md` — do not restate it inline. Note: `index.md` is an **OKF reserved file** — frontmatter-free (a directory listing, not a concept doc).

Unresolved questions (undecided business rules, deferred extensions) are filed directly to the central ledger via `util-open-items` — no local Open Items section (ADR-0005). Cite the use-case file as `Source artefact`. Schema and lifecycle: the `metamodel` skill's `references/open-items-governance.md`.

---

## Reference materials

- **`references/methodology.md`** — the full three-tradition synthesis (Cockburn / UML / Use-Case 2.0), the comparison matrix, and the positioning vs user stories / PRD / FBS / domain model. Carries the citations. **Kit-only** — never copied into a project; project files link to it via the header pointer.
- **`references/use-case-discipline.md`** — internal Claude guidance: the anti-patterns catalogue, the goal-level/scope decision aids, and the effective-use-case quality checklist. Read before authoring or reviewing.
- **`references/methodology-references.md`** — canonical bibliography. Kit-only.

Templates in `templates/`: `use-case-fully-dressed.md`, `use-case-casual.md`, `index.md`.

---

## Closing report to the user

After any mode, summarise in 4–6 lines:

1. **Mode executed** + files created/updated with paths.
2. **UC-NN minted** (author modes) + level + scope chosen, with a one-line justification.
3. **Extensions count** — how many alternate/exception paths captured (the depth signal).
4. **Links** — which FBS functionalities / personas / value-stream stage the use case ties to.
5. **Anti-pattern check** — explicit confirmation no UI detail / functional-decomposition / wrong-level issues survived.
6. **Next step** — slice for the backlog (Mode 4), ground a PRD, or drive the domain model.

---

## Checklist

Before declaring the work done:

- [ ] `use-cases/` folder + `index.md` registry exist.
- [ ] When a capability map exists: each use case sits in its capability-slug subfolder (unlinked ones at root); the registry is capability-grouped with an Unassigned group. No capability map → flat layout.
- [ ] Each use case states `Scope` + `Level` explicitly; level passes the coffee-break test (user-goal default).
- [ ] Main success scenario is numbered, active-voice, actor-intent (no UI/screen detail), 3–9 steps.
- [ ] Extensions walk every step; each has a condition + handling.
- [ ] Guarantees (success + minimal) + preconditions + trigger present (fully-dressed).
- [ ] `UC-NN` minted, registry row added, never reused.
- [ ] `Realises:` FBS IDs / `Primary Actor:` persona linked where those artefacts exist.
- [ ] Any unresolved question found while writing was filed directly via `util-open-items` (no local section — ADR-0005).
- [ ] Standard artefact frontmatter on every file.
- [ ] No project-specific terms baked into the kit copy.
- [ ] Closing report delivered.
