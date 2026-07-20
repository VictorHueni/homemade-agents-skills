# Use Case Methodology — the three traditions, synthesised

This is the canonical methodology reference for `spec-use-case`. It synthesises the three major use-case traditions, gives a comparison matrix, and positions use cases against adjacent requirements artefacts. It is **kit-only** — project files link here rather than copying it.

Every source is linked inline per the kit citation rule.

---

## 1. Cockburn — textual use cases (the core discipline)

Alistair Cockburn's [_Writing Effective Use Cases_ (2000)](https://www.informit.com/store/writing-effective-use-cases-9780201702255) is the canonical text. Its central idea: **a use case is a contract between stakeholders about the behaviour of a system under all conditions** — not just the happy path, but every alternate and exception path, and the guarantees that hold at the end. A [public draft of the manuscript](https://people.inf.elte.hu/molnarba/Informaciorendszerek_ELTE/Writing_effective_Use_cases_Cockburn.pdf) is available.

### Goal levels (the altitude metaphor)

Cockburn separates use cases by the **level of the goal** they serve, using an altitude/colour metaphor (the "cloud, kite, sea, fish, clam" model, summarised by [Visual Paradigm](https://guides.visual-paradigm.com/navigating-scope-the-impact-of-cloud-kite-sea-fish-clam-in-use-case-analysis/)):

| Level | Icon / colour | Meaning |
|---|---|---|
| **Summary** | ☁ cloud (white) / 🪁 kite (sky-blue) | Context-setting; spans several user goals. A few per system. |
| **User goal** | 🌊 sea level (blue) | One actor, one sitting, one goal of measurable value. **The default and most useful level.** |
| **Subfunction** | 🐟 fish (indigo) / 🦪 clam (black) | A sub-step that exists only because several user-goal use cases reuse it. |

**The sea-level test (a.k.a. the coffee-break / 2-to-20-minute test):** a user-goal use case is something the primary actor performs in *one sitting*, after which they can leave satisfied — roughly 2 to 20 minutes of effort. "Withdraw cash", "Place an order", "Submit a claim" are user goals. "Validate password" is a subfunction; "Manage the business" is a summary goal. If you can't tell the level, you can't tell whether the use case is the right size.

### Design scope

Independent of goal level, **scope** sets *what counts as "the system"*:

- **Enterprise / business** — the whole organisation as a black box, technology-agnostic.
- **System** — the software product being designed (the usual scope).
- **Subsystem** — one component inside the product.

Cockburn's advice: state scope and level in the header of every use case, because the same sentence ("the system records the order") means different things at different scopes.

### Actors and stakeholders

- **Primary actor** — the stakeholder who *initiates* the interaction to achieve the goal (in this kit, usually a persona `P-NN`).
- **Supporting actors** — external systems/services the system-under-design calls on to fulfil the goal.
- **Stakeholders and interests** — everyone whose interest the system must protect even though they are *not* at the keyboard (the business, an auditor, the data subject). The main success scenario and guarantees exist to satisfy these interests. This list is the source of the requirements; a step is justified by the stakeholder interest it protects.

### Structure: main success scenario + extensions

- **Main success scenario** — the numbered happy path, each step `Subject verb…` in active voice, alternating actor intent and system responsibility, showing "who has the ball". Typically 3–9 steps.
- **Extensions** — at *every* step, the conditions under which behaviour diverges, labelled `1a`, `2a`… each beginning with the **condition**, then the handling steps. This is where most real requirements live; thoroughness of extensions is the main quality differentiator of fully-dressed use cases.
- **Guarantees** — **minimal guarantees** hold no matter how the scenario ends (even on failure: "no money is debited without a recorded transaction"); **success guarantees** hold when the goal is achieved. Plus **preconditions** (what is true before it starts) and **trigger** (what starts it).

### Fully-dressed vs casual

Cockburn explicitly supports **two formats**: the **fully-dressed** template (all fields above) for high-stakes/complex goals, and the **casual** format (a few prose paragraphs covering the main scenario and alternatives) for low-risk goals or early discovery. Choosing the lighter format when the risk is low is part of the discipline — not every goal earns a fully-dressed use case.

---

## 2. UML use-case diagrams (the visual overview)

UML use-case diagrams (from Jacobson's [OOSE](https://en.wikipedia.org/wiki/Use_case) lineage, standardised in the [OMG UML specification](https://www.omg.org/spec/UML/)) give the *map*: **actors**, **use cases** (ellipses), the **system boundary** (the box), and three relationships. They are an index to the text, **never a replacement for it.** Reference: [Visual Paradigm — What is a Use Case Diagram](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/what-is-use-case-diagram/), [uml-diagrams.org](https://www.uml-diagrams.org/use-case.html).

| Relationship | Semantics | Direction | Runs when |
|---|---|---|---|
| **`«include»`** | Base use case **always** incorporates the included behaviour (mandatory, reusable sub-behaviour factored out) | Base → included (base depends on included) | Always, as part of the base |
| **`«extend»`** | Optional/conditional behaviour inserted at a named **extension point** in the base | Extending → base (extension depends on base) | Only when the guard condition holds |
| **Generalization** | A child use case specialises a parent (is-a) | Child → parent | Child substitutes for parent |

**The relationships are the most-abused part of UML use cases** (see [Sparx — Include vs Extend](https://www.sparxsystems.us/enterprise-architect/include-vs-extend-use-case-diagrams-ea-uml/)): teams swap `«include»` and `«extend»`, making diagrams ambiguous and test coverage inconsistent. Visual Paradigm's blunt heuristic: *"if yours contains more than 20 use cases, you are probably misusing the use case diagram"* — the diagram is a high-level overview, not a functional-decomposition tree. **Use the diagram sparingly** (optional in this skill): it earns its place when there are many actors/goals to map, not as a substitute for writing the scenarios.

---

## 3. Use-Case 2.0 (the agile delivery layer)

In 2011 Ivar Jacobson, Ian Spence, and Kurt Bittner published the [Use-Case 2.0 ebook](https://www.ivarjacobson.com/publications/white-papers/use-case-20-e-book) ([PDF](https://www.ivarjacobson.com/files/use-case_2_0_e-book_2023_0.pdf)) to adapt use cases to iterative, incremental, backlog-driven delivery — inspired by user stories. Summary references: [ACM Queue](https://queue.acm.org/detail.cfm?id=2912151), [microTOOL](https://www.microtool.de/en/knowledge-base/how-use-case-2-0-works/).

**Key concepts:**

- **Use-case narrative** — the stories of the use case, described as a set of **flows**: the **basic flow** (the main success scenario) plus **alternative flows** (each an extension run start-to-finish). Each flow is a distinct *use-case story*.
- **Use-case slice** — one or more stories grouped into a manageable, vertically-sliced delivery unit (first-to-last step). The **basic flow is the first slice**; alternative flows become further slices. This is the unit that goes on the backlog — the use-case equivalent of a user story.
- **Test cases** — *"a use-case slice must also contain a test case, just as a user story needs acceptance criteria."* Flows and slices yield test cases directly, giving test-driven design and traceable verification.

**The six principles of Use-Case 2.0:** (1) keep it simple by telling stories; (2) understand the big picture with use cases; (3) focus on value; (4) build the system in slices; (5) deliver the system in increments; (6) adapt to meet the team's needs.

**Why it matters here:** Use-Case 2.0 is the bridge that lets a single use case serve *both* the analyst (the complete behavioural contract) *and* the delivery team (a stream of sprint-sized slices with acceptance tests) — without maintaining two parallel artefacts. This skill's `slice` mode implements it.

---

## 4. Comparison matrix — when to use which

| | Textual use case (Cockburn) | UML use-case diagram | Use-Case 2.0 slice | User story |
|---|---|---|---|---|
| **Captures** | Full actor↔system scenario, all paths, guarantees | Map of actors + goals + boundary | A deliverable narrative path + its tests | A need + a conversation placeholder |
| **Granularity** | One user goal (2–20 min) | Whole system overview | One flow / increment | One thin slice of value |
| **Strength** | Exhaustive alternate/exception coverage | At-a-glance scope & relationships | Backlog-ready, test-driven | Fast, conversational, estimable |
| **Weakness** | Heavier to write; too large to estimate | Over-decomposed if misused; no detail | Needs the underlying use case first | Alternate paths easily lost |
| **Best when** | New/complex product; cost of a missed flow is high | Many actors/goals to orient stakeholders | Agile team delivering a known use case incrementally | Mature product; team shares context |

Practitioner consensus (e.g. [Mountain Goat / Cohn](https://www.mountaingoatsoftware.com/articles/advantages-of-user-stories-for-requirements), [Stellman & Greene](https://www.stellman-greene.com/2009/05/03/requirements-101-user-stories-vs-use-cases/)): **user stories describe a need; use cases describe the behaviour built to meet it.** A user story is ~10 minutes to write and estimable; a use case is an hour-plus and usually too large to estimate — which is exactly why Use-Case 2.0 slices it. They are complementary, not rivals: use cases are strongest for **new products and goals with costly alternate flows**; user stories for **mature products where stakeholders already share the model**.

---

## 5. Positioning vs the kit's requirements artefacts

| Adjacent artefact | How a use case differs | The relationship |
|---|---|---|
| **User story** | A story is a *need + placeholder for conversation*; a use case is the *worked-out behaviour with all branches*. | A use case's flows/slices *are* the stories. Use the slice mode to generate backlog items. |
| **PRD** (`spec-prd`) | A PRD scopes *what we build next* for one slice, with priority, acceptance criteria, NFRs. A use case is technology-neutral behaviour, no priority/estimate. | The PRD **references** the use case(s); the scenario grounds the acceptance criteria. Don't duplicate the scenario into the PRD. |
| **FBS** (`spec-functional-breakdown-structure`) | The FBS is a flat *registry* of what the system does, status-tracked, no scenario. | A use case **realises** FBS functionalities (`C-N.M.FXX`) and adds the *interaction* the registry cannot hold. |
| **Domain model** (`domain-model`) | The domain model is the *objects* (aggregates, events); a use case is the *behaviour over time*. | Use-case steps that change state map to **commands → domain events**; scenarios are a prime driver of aggregate boundaries and event discovery. |
| **Personas** (`business-persona`) | A persona is *who*; a use case is *what they do with the system*. | The persona is the use case's **primary actor** (`P-NN`). |

**The "does this add value or duplicate?" test:** write a use case when the interaction has **branches that matter** — alternate/exception flows whose omission is costly. For a trivial single-path behaviour, an FBS row plus a user story in a PRD is sufficient; manufacturing a fully-dressed use case for "update profile" is waste. Reserve the fully-dressed format for goals where the **cost of a missed alternate flow exceeds the cost of writing it down** (Cockburn's own criterion).

---

## Primary sources

See `methodology-references.md` for the full bibliography with editions and links.
