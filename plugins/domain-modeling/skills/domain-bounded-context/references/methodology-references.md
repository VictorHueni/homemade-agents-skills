# Methodology References — Bounded Context Builder

Canonical bibliography for the `domain-bounded-context` skill. This file lives in the skill only — project documents link here rather than copying the bibliography locally.

---

## Evans, Eric — *Domain-Driven Design: Tackling Complexity in the Heart of Software* (2003)

**Publisher:** Addison-Wesley. The foundational DDD text — introduced the term "Bounded Context" and the eight Context Map integration patterns.

**What this skill draws from:**

- **Chapter 14 — Maintaining Model Integrity:** the core definition of a bounded context as the boundary within which a domain model is consistent and unambiguous. Evans establishes the fundamental rule: "explicitly define the context within which a model applies." The ubiquitous language is valid only inside a BC boundary.

- **The eight integration patterns (Chapter 14):** Shared Kernel, Customer-Supplier, Conformist, Anti-Corruption Layer, Separate Ways, Open Host Service, Published Language, Big Ball of Mud. Each pattern describes a different power dynamic and translation obligation between contexts. This skill uses these eight as the complete vocabulary for the context map.

- **Ubiquitous language (Chapter 2):** the discipline that within a bounded context, every word in the code, documentation, and conversation means the same thing. The skill's BC naming test and glossary linkage are grounded here.

- **Context Map as communication device:** Evans treats the context map as a living document of inter-team relationships, not a one-time architectural diagram.

---

## Vernon, Vaughn — *Domain-Driven Design Distilled* (2016)

**Publisher:** Addison-Wesley. The most accessible DDD strategic design reference. Chapters 3 and 4 are the primary synthesis source for subdomain classification.

**What this skill draws from:**

- **Chapter 3 — Strategic Design with Subdomains:** the Core / Supporting / Generic subdomain trichotomy. Vernon's formulation: Core = the source of competitive advantage; Supporting = enables Core but doesn't differentiate; Generic = commodity, buy or outsource. The sizing heuristic of 1–3 Core subdomains per product is drawn directly from Vernon's examples.

- **Chapter 4 — Strategic Design with Context Mapping:** Vernon extends Evans' patterns with practical guidance on when to choose each one. The build-vs-buy framing (Core → build and invest; Generic → buy SaaS) is from this chapter.

- **Aggregate sizing (Chapter 5 — preview):** Vernon's rule of 3–7 aggregates per bounded context is used in Mode 4 (Refresh) as a signal for split candidacy.

---

## Vernon, Vaughn — *Implementing Domain-Driven Design* (2013)

**Publisher:** Addison-Wesley. The practitioner-depth companion to DDD Distilled.

**What this skill draws from:**

- **Deeper context mapping patterns:** Vernon elaborates on the ACL (Anti-Corruption Layer) as an active translation mechanism, not merely a wrapper. The translation layer description field in the context map template is grounded in IDDD's treatment.

- **Upstream/downstream power dynamics:** IDDD makes explicit what Evans implies — the direction of influence matters as much as the direction of data flow. A Conformist relationship is not a technical choice but a power acknowledgment.

---

## Tune, Nick — *Architecture Modernization: Sociotechnical Alignment and Meaningful Change* (2024)

**Publisher:** Manning. The most recent synthesis of strategic DDD with sociotechnical team topology.

**What this skill draws from:**

- **Sociotechnical alignment:** Tune's central thesis — that software architecture and team topology must be designed together, not sequentially. The BC → team ownership recommendation in this skill reflects Tune's framework: define the right bounded context boundaries first, then let team structure follow.

- **Domain-Driven Transformation:** Tune's modernization patterns for breaking monoliths into bounded contexts, identifying "seams" where the language changes, and managing migration risk. The Mode 4 (Refresh) guidance on split/merge candidates draws from this.

- **Wardley Mapping integration (Chapter notes):** Tune combines Wardley Maps with DDD subdomain classification, reinforcing the Core / Supporting / Generic distinction with evolutionary maturity signals.

---

## Conway, Melvin — "How Do Committees Invent?" (1968)

**Publication:** *Datamation* magazine, April 1968. The original statement of Conway's Law.

> "Any organisation that designs a system (defined broadly) will produce a design whose structure is a mirror copy of the organisation's communication structure."

**What this skill draws from:**

- The anti-pattern "BC boundary follows org chart" is the direct failure mode Conway's Law predicts when teams reverse the causal arrow. Conway's Law does not say org structure causes good architecture — it says org structure *will* manifest as architecture whether you want it to or not.

- The skill's Mode 2 Step 0 question 3 (team topology) and the per-BC team boundary recommendation field are the skill's practical response to Conway's Law: design the right boundaries, then advocate for team alignment to them.

---

## Skelton, Matthew and Pais, Manuel — *Team Topologies: Organizing Business and Technology Teams for Fast Flow* (2019)

**Publisher:** IT Revolution. The canonical reference for team cognitive load and stream-aligned team design.

**What this skill draws from:**

- **Four team types:** stream-aligned, platform, enabling, complicated-subsystem. The per-BC team boundary recommendation field maps each bounded context to the most appropriate team type.

- **Cognitive load as a design constraint:** Team Topologies argues that a team's cognitive load capacity should constrain the scope of a bounded context it owns. The skill's "cognitive load estimate" field (small / medium / large) operationalises this.

- **Inverse Conway Maneuver:** Skelton and Pais name the deliberate act of reorganising teams to produce the desired architecture. This is the proactive version of what the skill's Conway alignment note asks the user to consider.

---

## Brandolini, Alberto — EventStorming (2013–present)

**Primary source:** [eventstorming.com](https://www.eventstorming.com) + *Introducing EventStorming* (Leanpub, 2021).

**What this skill draws from:**

- **EventStorming as BC discovery input (Mode 2 option 1B):** Brandolini's technique surfaces domain events → aggregates → aggregate clusters → bounded context candidates. When an EventStorming output exists, Mode 2 reads the event clusters as strong BC boundary signals rather than deriving them solely from the capability map.

- **Hotspot identification:** EventStorming's "orange stickies" (problem areas) often correspond to poorly defined context boundaries — useful signal in Mode 4 (Refresh) for split candidates.

- **Ubiquitous language emergence:** EventStorming uses business-language event names ("OrderPlaced", "PatientAdmitted") — these are strong inputs for per-BC ubiquitous language scoping in Mode 3.

---

## Fowler, Martin — "BoundedContext" (2014)

**Source:** [martinfowler.com/bliki/BoundedContext.html](https://martinfowler.com/bliki/BoundedContext.html)

A concise practitioner explanation of bounded contexts as the primary tool for managing the complexity of large domain models. Fowler's formulation — "multiple models are in play on any large project" and the key skill is explicitly defining where each model applies — reinforces the skill's core discipline.

---

## Summary: what this skill synthesises

| Source | Primary contribution to this skill |
|---|---|
| Evans DDD (2003) | Bounded context definition, eight integration patterns, ubiquitous language |
| Vernon DDD Distilled (2016) | Core/Supporting/Generic classification, build-vs-buy, aggregate sizing preview |
| Vernon IDDD (2013) | ACL as active translation, upstream/downstream power dynamics |
| Nick Tune (2024) | Sociotechnical alignment, BC → team ownership, modernization patterns |
| Conway (1968) | Anti-pattern warning: org structure drives architecture unless deliberately countered |
| Team Topologies (2019) | Team type mapping per BC, cognitive load constraint |
| Brandolini EventStorming | Discovery input: events → aggregates → BC candidates |
| Fowler (2014) | Practitioner framing: multiple models, explicit boundaries |
