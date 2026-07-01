---
name: spec-use-case
description: "Create effective use cases — goal-oriented, technology-neutral behavioural specs synthesising Cockburn's Writing Effective Use Cases (goal levels, fully-dressed + casual formats, main success scenario + extensions), UML use-case diagrams (actors, «include»/«extend»), and Jacobson's Use-Case 2.0 (slices for the backlog). Mints UC-NN. Modes: scaffold (use-cases/ folder + index), fully-dressed (author one use case), casual (lightweight variant), slice (Use-Case 2.0 backlog slices), review (quality audit). Output: docs/product-specs/use-cases/. Reads personas (P-NN as actors) + FBS (C-N.M.FXX); feeds PRDs, domain model, test cases. Triggers on: use case, write a use case, fully-dressed use case, main success scenario, actor goal, use case diagram, scenario, use case slice, alternate flow, extension, use case template."
version: "1.0.0"
status: active
last_reviewed: 2026-06-06
review_interval: 180d
user-invocable: true
allow_implicit_invocation: true
impact: "low"
metadata:
  category: "specification"
  complexity: "medium"
---

# Use Case Builder

You are an expert at writing **effective use cases** — goal-oriented, technology-neutral descriptions of how an actor and a system collaborate to reach a goal of value. This skill synthesises the three canonical traditions and tells you when each fits:

- **Alistair Cockburn — _Writing Effective Use Cases_ (2000)**: the textual discipline. Goal levels, design scope, primary actor + stakeholders, main success scenario + extensions, fully-dressed vs casual formats. The use case as **a contract between stakeholders about behaviour under all conditions**.
- **UML use-case diagrams (Jacobson / OMG)**: the visual overview. Actors, system boundary, `«include»` / `«extend»` / generalization. A *map* of use cases, never a substitute for the text. Render these with **`arch-uml`** (`use-case` mode → PlantUML → committed SVG); carry each `UC-NN` onto its ellipse so the diagram cross-references back to the fully-dressed text here.
- **Ivar Jacobson — _Use-Case 2.0_ (2011)**: the agile delivery layer. The same use case, **sliced** vertically into backlog-sized increments (a *use-case slice* = narrative path + its test cases), so use cases drive iterative delivery the way user stories do.

The artefact produced is **one markdown file per use case** under `docs/product-specs/use-cases/`, plus a registry `index.md`. A use case is NOT a user story, NOT a PRD, NOT an FBS row, NOT a UI spec — it is **the behavioural scenario**: the numbered interaction between actor and system, every alternate path, and the guarantees that hold when it ends.

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

Do NOT invent use cases in scaffold mode. Substitute `{{product_or_scope}}`. Open the file with standard artefact frontmatter (see below).

### Mode 2 — Fully-dressed (author one use case)

**When:** the goal is high-stakes, complex, or has many alternate paths — the cost of a missed extension is high.

**Process:**
1. **Fix `Scope` + `Level`** (see above). Confirm with the user if ambiguous.
2. **Identify the primary actor** — prefer a project persona (`P-NN`); record it as the actor. Identify supporting actors (other systems/services the system calls).
3. **List stakeholders and interests** — who is *not* at the keyboard but whose interest the system must protect (the business, an auditor, the data subject).
4. **Mint the ID** — next `UC-NN` from the registry. Create `uc-NN-{slug}.md` from `templates/use-case-fully-dressed.md`.
5. **Write the Main Success Scenario** — numbered steps, each `Subject verb… ` in active voice, alternating actor intent and system responsibility. 3–9 steps is the sweet spot. Each step shows *who has the ball*.
6. **Write Extensions** — walk every step; ask "what else could happen here?" Label `1a`, `1b`, `2a`… with the *condition* then the handling steps. Missing extensions is where real requirements hide.
7. **State guarantees + preconditions + trigger.**
8. **Link** — `Realises` the FBS functionalities (`C-N.M.FXX`); reference glossary terms (`GT-NN`); note the value-stream stage if relevant.
9. **Update `index.md`** — add the registry row.
10. **Run the quality checklist** in `references/use-case-discipline.md`.

### Mode 3 — Casual (lightweight variant)

**When:** the goal is low-risk or you're early in discovery and want speed. Cockburn's casual format trades the field structure for a few prose paragraphs.

**Output:** `uc-NN-{slug}.md` from `templates/use-case-casual.md` — title + scope/level + a paragraph for the main scenario and a short paragraph (or bullet list) for the alternate paths. Still mints `UC-NN` and updates the index. Casual use cases can be **promoted to fully-dressed** later without re-numbering.

### Mode 4 — Slice (Use-Case 2.0 — feed the backlog)

**When:** the team works in sprints/Kanban and wants use cases to drive iterative delivery (the agile bridge between use cases and user stories).

**Process** (per `references/methodology.md` §Use-Case 2.0):
1. Take a fully-dressed use case. Its **basic flow** (main success scenario) is the **first slice** — the thinnest end-to-end path.
2. Each meaningful **alternative flow** (an extension run start-to-finish) becomes a further **slice**.
3. For each slice, write **its test case(s)** — the slice's acceptance criteria. *A slice without a test case is incomplete, exactly as a user story without acceptance criteria is.*
4. Record slices in a `## Use-Case 2.0 Slices` section of the use-case file: `UC-NN.S1`, `UC-NN.S2`… with a one-line narrative + test-case pointer + status. These are the backlog-ready increments.

### Mode 5 — Review (quality audit)

**When:** existing use cases need checking before they ground PRDs or domain models.

Read each `uc-NN-*.md` against the checklist in `references/use-case-discipline.md` and emit ranked findings (which level violation, which anti-pattern, which missing extension) with a concrete fix per finding. **Report-only — do not silently rewrite** unless asked; propose the exact edits.

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
| **PRD** (`PRD-NNNN`) | What we build for one slice + acceptance criteria | A PRD **references** the use case(s) it delivers; the scenario grounds the acceptance criteria |
| **Domain model** (`BC-NN.AGG-NN`, `BC-NN.EVT-NN`) | Entities, aggregates, domain events | Use-case steps that change state map to **commands → domain events**; scenarios drive aggregate design |
| **Test cases** | Verification | Each flow / slice yields test cases (Use-Case 2.0 makes this explicit) |

**Soft-reference principle** (same as the rest of the kit): use cases reference other artefacts as pointers, not prerequisites. Author a use case even if the FBS or PRDs don't yet exist; add the `Realises:` links when they do.

**When a use case adds value vs duplicates:** write a use case when the *interaction has branches that matter* (alternate/exception flows whose omission is costly). For a trivial, single-path behaviour, an FBS row + a user story in a PRD is enough — don't manufacture a fully-dressed use case for "update profile". See `references/methodology.md` §Positioning.

---

## Inputs

| Needed | What you ask if missing |
|---|---|
| **Mode** | Detect from request (scaffold / fully-dressed / casual / slice / review). Confirm if ambiguous. |
| **Folder** | Look for `docs/product-specs/use-cases/`. If absent, default there and confirm. |
| **Primary actor** | A project persona (`P-NN`) if one fits; else name the actor role. |
| **Goal + level** | What does the actor want, in one go? Helps fix the level. |
| **FBS existence** | Check for `docs/product-specs/07a-fbs.md` to populate `Realises:`. Optional. |

Ask 2–4 questions max, single message, lettered options. Don't run a wizard.

---

## Output frontmatter

Open every generated **use-case file** (`uc-NN-*.md`) with the standard OKF-superset artefact frontmatter — `type: Use Case` (its `okf_type` in `rules/artefact-types-registry.md`), plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`. Run `git config user.name` for `owner`. `status: draft` on creation. Default `review_interval: 180d` (use cases are stable behavioural specs). Full schema: `rules/artefact-frontmatter.md` — do not restate it inline. Note: `index.md` is an **OKF reserved file** — frontmatter-free (a directory listing, not a concept doc).

Each use-case file carries one document-level `## Open Items` section for unresolved questions (undecided business rules, deferred extensions). Initial state `_None at present._` — never scaffold placeholder rows. Schema and lifecycle: `rules/open-items-governance.md`. Chain to `util-open-items` to sync to the central ledger.

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
- [ ] Each use case states `Scope` + `Level` explicitly; level passes the coffee-break test (user-goal default).
- [ ] Main success scenario is numbered, active-voice, actor-intent (no UI/screen detail), 3–9 steps.
- [ ] Extensions walk every step; each has a condition + handling.
- [ ] Guarantees (success + minimal) + preconditions + trigger present (fully-dressed).
- [ ] `UC-NN` minted, registry row added, never reused.
- [ ] `Realises:` FBS IDs / `Primary Actor:` persona linked where those artefacts exist.
- [ ] `## Open Items` section present (initial `_None at present._`).
- [ ] Standard artefact frontmatter on every file.
- [ ] No project-specific terms baked into the kit copy.
- [ ] Closing report delivered.
