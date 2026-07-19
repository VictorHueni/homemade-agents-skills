# Use Case Discipline — anti-patterns, decision aids, quality checklist

Internal guidance for the `spec-use-case` skill. Read before authoring (Mode 2/3) or reviewing (Mode 5). Never copied into a project.

---

## The anti-patterns catalogue

Each is a documented failure mode from the use-case literature (Cockburn's style chapter; UML diagram misuse; user-story comparison).

### A1 — UI / presentation coupling

❌ "The system displays the login screen. The user clicks the Submit button."
✅ "The user submits their credentials. The system authenticates them."

A use case names the actor's **intent** and the system's **responsibility**, never the widget or screen. The test: *could this still be true if the UI were a voice assistant, an API, or a paper form?* If not, you've coupled to presentation. Screens, buttons, fields, and layouts belong in a UI spec.

### A2 — Wrong goal level

❌ A use case "Validate email format" written as a top-level case (it's a **subfunction** — clam level).
❌ A use case "Manage the company" written with numbered steps (it's a **summary** goal — no single sitting).
✅ "Register an account" — a user goal, one sitting, the coffee-break test passes.

**Default to user-goal (sea) level.** Promote to summary only for context; demote to subfunction only when 2+ user-goal cases genuinely reuse the step. Most clam-level "use cases" should be *steps inside* a user-goal case, not cases of their own.

### A3 — Functional decomposition disguised as use cases (CRUD explosion)

❌ Four use cases "Create X", "Read X", "Update X", "Delete X" for every entity, wired together with `«include»`.
✅ One user-goal use case ("Manage my X") whose flows cover the operations, *or* — if these are genuinely just registry behaviours — FBS rows, not use cases at all.

Use cases are about **goals of value**, not database verbs. If your use-case set looks like a CRUD matrix, you've done functional decomposition. (The FBS skill deliberately *does* split CRUD into registry rows — that's its job; a use case's job is different.)

### A4 — `«include»` / `«extend»` abuse

❌ Using `«extend»` for mandatory behaviour, or `«include»` for optional behaviour; deep include trees that turn the diagram into a flowchart.
✅ `«include»` only for behaviour that **always** runs and is **reused** by 2+ cases; `«extend»` only for **conditional** behaviour at a named extension point. If in doubt, write the alternate path as an **extension in the text** instead of a diagram relationship — the text is the contract; the diagram is just a map. Keep diagrams under ~20 use cases.

### A5 — Missing or shallow extensions

❌ A fully-dressed use case with a rich main scenario and an empty Extensions section.
✅ Every step interrogated: "what else can happen here — actor error, system failure, business rule violation, timeout?"

The Extensions section is where the *real* requirements live. A fully-dressed use case with no extensions is a happy-path narrative wearing a template. For each main step, ask the four prompts: actor does something unexpected · system/service unavailable · validation/business rule fails · data is missing or stale.

### A6 — Passive voice / unclear "who has the ball"

❌ "The order is validated and a confirmation is sent." (By whom?)
✅ "The system validates the order and sends the actor a confirmation."

Every step is `Subject verb direct-object` in active voice. The reader must always know whether the actor or the system is acting. Passive voice hides the responsibility boundary that the use case exists to define.

### A7 — Use case as a feature dump / PRD

❌ Use case stuffed with priorities, estimates, acceptance criteria, NFR targets, release notes.
✅ Keep it to behaviour + guarantees. Priority/estimate/NFR live in the PRD and quality-attributes docs that *reference* the use case.

### A8 — One giant use case (no slicing)

❌ A 40-step "use case" covering an entire workflow end-to-end with every branch inline.
✅ Either it's a **summary** goal decomposed into several user-goal use cases, or it's one user-goal case sliced (Use-Case 2.0) into delivery increments. A use case the team can't deliver incrementally is too big.

---

## Decision aid — goal level

Ask, in order:
1. **Does the actor complete it in one sitting and then stop, satisfied?** → user goal (sea). Default here.
2. **Does it span several such sittings / set context for them?** → summary (cloud/kite).
3. **Is it a step that only exists because 2+ user-goal cases reuse it?** → subfunction (fish/clam).
4. **Is it a single database verb on one entity with no branching value?** → not a use case; it's an FBS row (or a step inside a user-goal case).

## Decision aid — design scope

1. **Are we describing the whole organisation, technology-agnostic?** → enterprise/business.
2. **Are we describing the software product under design?** → system (default).
3. **Are we describing one component inside the product?** → subsystem.

State both `Scope` and `Level` in the header. When they fight (e.g. an enterprise-scope subfunction), you've probably mixed two use cases — split.

## Decision aid — fully-dressed vs casual vs "not a use case"

- **Cost of a missed alternate flow is high** (money, safety, compliance, irreversible action) → fully-dressed.
- **Low risk, early discovery, exploratory** → casual (promote later if it matters).
- **Single path, no meaningful branches** → don't write a use case; an FBS row + a PRD user story suffices.

---

## Quality checklist — "is this use case effective?"

Run every box when authoring or reviewing. A use case passes only if all hold.

- [ ] **Goal-oriented** — the title is a goal the primary actor values ("Withdraw cash"), not a system function ("Process withdrawal request") and not a UI action ("Click withdraw").
- [ ] **Right level** — passes the relevant level test; user-goal cases pass the coffee-break (2–20 min, one sitting) test.
- [ ] **Scope + level stated** explicitly in the header.
- [ ] **Technology-neutral** — survives the "could this be voice / API / paper?" test; no screens, buttons, fields.
- [ ] **Primary actor named** (a persona `P-NN` where possible); supporting actors listed.
- [ ] **Stakeholders + interests** listed; every main step traces to a stakeholder interest it protects.
- [ ] **Main success scenario** is numbered, active-voice, `Subject verb object`, 3–9 steps, alternating actor/system, "who has the ball" always clear.
- [ ] **Extensions** cover every step; each starts with a condition then handling; the four failure prompts were applied.
- [ ] **Guarantees** — minimal (holds on failure) and success guarantees both stated; preconditions + trigger present.
- [ ] **Testable** — each flow yields at least one concrete test case (Use-Case 2.0 readiness).
- [ ] **No scope creep** — no priority/estimate/acceptance-criteria/NFR/algorithm/schema (those live in PRD / quality-attributes / domain model).
- [ ] **Traceable** — `Realises:` FBS IDs and persona/value-stream links present where those artefacts exist.
- [ ] **Stable ID** — `UC-NN` minted, registry updated, not reused.
