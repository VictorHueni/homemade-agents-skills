# Methodology References — Domain Glossary / Ubiquitous Language

Sources synthesised in the `domain-glossary` skill. Listed in order of primary influence.

---

## Primary sources

### Eric Evans — *Domain-Driven Design: Tackling Complexity in the Heart of Software* (2003)

**Chapter 2 — Communication and the Use of Language**

The foundational statement of Ubiquitous Language as a design practice:

> "Use the model as the backbone of a language. Commit the team to exercising that language relentlessly in all communication within the team and in the code. Use the same language in diagrams, writing, and especially speech. Iron out difficulties by experimenting with alternative expressions, which reflect alternative models. Then refactor the code, renaming classes, methods, and modules to conform to the new model. Resolve confusion over terms in conversation, in just the way we come to agree on the meanings of ordinary words."

Key tenets from Ch. 2:
- The language must be used in code, not just in documentation. If a domain concept has no name in the code, the code does not reflect the model.
- When business and developers use different words, communication is lossy — what Evans calls the "broken telephone" problem. Every handoff is a translation, and every translation loses fidelity.
- The language evolves. The team must be willing to rename code when understanding deepens, because stale names are misinformation.
- Linguistic antipatterns Evans identifies: **anemic language** (names that describe mechanics, not domain concepts), **dual ontologies** (two separate vocabularies — one for business conversations, one for code — that diverge silently over time).

**Bounded contexts and linguistic scope (Chapter 14):**
Evans introduces bounded contexts as the unit of linguistic consistency. The same word can and should mean different things in different bounded contexts. Attempting one universal glossary across all contexts creates a model that is wrong everywhere.

---

### Vaughn Vernon — *Domain-Driven Design Distilled* (2016)

**Chapter 2 — Strategic Design with Bounded Contexts and the Ubiquitous Language**

Vernon's accessible reformulation of Evans, with emphasis on:
- **Domain scenarios** as the primary elicitation technique. The team narrates what happens in the domain in plain sentences ("When a Policyholder submits a Claim, the system assigns it to an Adjuster"). Every noun and verb in those scenarios is a glossary candidate.
- The language belongs to the **domain experts first**. Developers adopt it, not the other way around.
- **Scenario testing** as a validation technique: if a domain scenario reads awkwardly with the proposed term, the term is wrong.
- Bounded context maps (Context Maps) as the mechanism for documenting cross-context relationships — the cross-context translation matrix in the glossary template is the documentation artefact for the same concept.

---

### Martin Fowler — *UbiquitousLanguage* pattern (martinfowler.com/bliki/UbiquitousLanguage.html)

Fowler's concise distillation:
- The "broken telephone" problem: when business analysts write specs in business language, developers translate to tech language, and the mapping between them exists only in one engineer's head — and leaves when they leave.
- Ubiquitous language is the antidote: a single vocabulary that both groups use in every artefact, every meeting, every commit message.
- Fowler emphasises that the language is **ubiquitous** — it must appear everywhere, not just in a glossary document that nobody reads. The glossary documents the language; the team practices it.

---

## Supporting sources

### Alberto Brandolini — EventStorming (2013–present; *Introducing EventStorming*, 2021)

EventStorming as a technique that forces ubiquitous language to emerge naturally:
- When a room full of domain experts and developers name domain events on sticky notes, naming conflicts surface immediately and visibly.
- The discipline of naming domain events in the past tense ("PolicyIssued", "ClaimSubmitted", "PaymentProcessed") forces precision — vague names like "ThingHappened" are immediately rejected by domain experts.
- EventStorming outputs are the richest source of glossary seed terms: every orange sticky note (domain event), blue sticky note (command), and yellow sticky note (aggregate) is a glossary candidate.
- Reference: Brandolini, A. (2021). *Introducing EventStorming*. Leanpub.

---

### Eric Evans — Linguistic antipatterns

Patterns Evans identified that indicate a failing ubiquitous language (scattered across *DDD* Ch. 2 and conference talks):

**Anemic language:** terms that describe what the system does mechanically rather than what the domain means. "ProcessRecord" instead of "SubmitClaim". "UpdateStatus" instead of "ApprovePolicyholder". Anemic language tells you about implementation; ubiquitous language tells you about the domain.

**Dual ontologies:** the team maintains two parallel vocabularies — one for client meetings, one for code. "The customer calls it a Policy but we call it a Contract in the code." This is not a feature; it is a defect in the model. When dual ontologies exist, every conversation between business and engineering is a translation, and translations fail silently.

**Implicit concepts:** concepts the domain experts discuss but that have no name in the code. "Oh, when the policy is in that state where it's been submitted but not yet reviewed — we just query for claims where status = 2." The unnamed state is a concept that deserves a name (e.g., "PendingReview"). Unnamed concepts cannot be reasoned about clearly.

---

### Sapir-Whorf hypothesis (linguistic relativity)

The Sapir-Whorf hypothesis (Sapir, 1929; Whorf, 1956) in its weak form states that the language available to a community influences how its members think and reason about the world. Teams that have precise, agreed-upon vocabulary for domain concepts reason more clearly about those concepts. Teams that lack precise vocabulary argue about implementation details because they cannot name what they are trying to discuss.

Applied to DDD: a team that has named "PolicyCancellationWithRefund" as a distinct concept from "PolicyLapseForNonPayment" can reason precisely about the rules governing each. A team that calls both "cancellation" will write ambiguous code and catch bugs in production.

The glossary is not bureaucracy — it is the team's cognitive infrastructure.

---

## Further reading

- Evans, E. (2003). *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley. ISBN 978-0321125217.
- Vernon, V. (2016). *Domain-Driven Design Distilled*. Addison-Wesley. ISBN 978-0134434421.
- Fowler, M. UbiquitousLanguage. martinfowler.com/bliki/UbiquitousLanguage.html
- Brandolini, A. (2021). *Introducing EventStorming*. Leanpub. eventstorming.com
- Millett, S. & Tune, N. (2015). *Patterns, Principles, and Practices of Domain-Driven Design*. Wrox. Chapter 3 — Ignoring the Lessons of History: The Spoken Language.
