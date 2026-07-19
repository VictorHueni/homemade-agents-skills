# Methodology References — Domain Model Builder

Sources synthesised by the `domain-model` skill. Cited by chapter and rule for traceability.

---

## Evans — Domain-Driven Design (2003)

Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley, 2003. ("The Blue Book")

### Chapter 5 — A Model Expressed in Software

Introduces the three core building blocks of the tactical model:

- **Entity**: an object defined primarily by its identity — not its attributes. Two entities with the same attributes are still different objects if they have different identities. The identity must be meaningful to the domain, not just a technical surrogate key.
  - Rule: "An object defined primarily by its identity is called an Entity. Entities have special modelling and design considerations. An entity is anything that has continuity through a life cycle and distinctions that matter to the user."
- **Value Object**: an object that describes some characteristic or attribute but carries no concept of identity. When you care only about the attributes of an element, classify it as a value object.
  - Rule: "When you care only about the attributes of an element of the model, classify it as a Value Object. Make it express the meaning of the attributes it conveys and give it related functionality. Treat the value object as immutable. Don't give it any identity."
- **Service**: a domain operation that does not belong on an entity or value object — it is a verb rather than a noun. Stateless. Named for an activity in the domain language.
  - Note: the existence of a domain service is not a license to move entity behaviour into services. The rich model keeps behaviour in entities.

### Chapter 6 — The Life Cycle of a Domain Object

Introduces aggregate as the lifecycle management pattern:

- **Aggregate**: a cluster of associated objects treated as a unit for the purpose of data changes.
  - Rule 1: "Each aggregate has a root and a boundary. The boundary defines what is inside the aggregate. The root is a single, specific entity contained in the aggregate."
  - Rule 2: "The root entity has global identity. Entities inside the boundary have local identity, unique only within the aggregate."
  - Rule 3: "Nothing outside the aggregate boundary can hold a reference to anything inside, except to the root entity."
  - Rule 4: "Only aggregate roots can be obtained directly with database queries. All other objects must be found by traversal of associations."
  - Rule 5: "Objects within the aggregate can hold references to other aggregate roots."
  - Rule 6: "A delete operation must remove everything within the aggregate boundary at once."
  - Rule 7: "When a change to any object within the aggregate boundary is committed, all invariants of the whole aggregate must be satisfied."

### Chapter 7 — Using the Language: An Extended Example

Demonstrates that model names must come directly from domain experts' language — not from technical or database terminology. Every object name in the model is a term from the ubiquitous language.

### Chapter 8 — Aggregates (full chapter)

The defining treatment of the aggregate pattern:

- Aggregate as consistency boundary: "A cluster of associated objects that we treat as a unit for the purpose of data changes."
- The root is the only member of the aggregate that outside objects are allowed to hold references to.
- Invariants are the non-negotiable business rules that the aggregate enforces at every state change.
- Evans is explicit: invariants must be stated in the model, not just implied by the code.

---

## Vernon — Implementing Domain-Driven Design (2013)

Vaughn Vernon, *Implementing Domain-Driven Design*. Addison-Wesley, 2013. ("The Red Book")

### Chapter 5 — Entities

- Entities must have unique identity. Vernon distinguishes five identity strategies: user-provided identity, application-generated identity, persistence-generated identity, another bounded context's identity, and identity assigned by domain expert.
- Entities should have behaviour: "An entity without behaviour that expresses domain concepts directly is an anemic domain model anti-pattern."
- Validation: entities should validate their own state. "Self-encapsulation means that all access to a field, even within a class, goes through the accessing methods."

### Chapter 6 — Value Objects

Vernon's expanded treatment of value objects:

- "Try to model most domain concepts as Value Objects. Use Entities when only identity and continuity matter."
- Value objects should not only hold data but also express domain concepts through behaviour: `Money.add(Money)`, `DateRange.overlaps(DateRange)`.
- Immutability rule: "Since a Value Object should be immutable, all its attributes are set only once during construction."
- Replace-not-mutate: "Rather than modifying a Value Object, you replace it with a new one."

### Chapter 10 — Aggregates

Vernon's four rules of aggregate design (the canonical distillation):

1. **Model a true invariant in a consistent boundary** — an aggregate boundary exists to enforce a business rule that must hold true at all times. Do not create an aggregate just because objects are related.
2. **Design small aggregates** — start with one entity per aggregate. Add members only when they must change atomically with the root in the same transaction. Large aggregates cause lock contention and force clients to load data they do not need.
3. **Reference other aggregates by identity** — never hold a direct object reference to another aggregate; hold its root identity only. "If you hold an object reference to another aggregate, you'll be tempted to modify it in the same transaction."
4. **Use eventual consistency outside the boundary** — if two aggregates must stay in sync after a command, use a domain event and eventual consistency. Do not span aggregate boundaries in a single transaction.

---

## Vernon — Domain-Driven Design Distilled (2016)

Vaughn Vernon, *Domain-Driven Design Distilled*. Addison-Wesley, 2016.

### Chapter 5 — Tactical Design with Aggregates

The condensed restatement of the four rules above, intended as a quick reference:

- "Rule 1: Protect business invariants inside aggregate boundaries."
- "Rule 2: Design small aggregates."
- "Rule 3: Reference other aggregates by identity only."
- "Rule 4: Update other aggregates using eventual consistency."

Vernon adds guidance on aggregate size: if you find yourself adding more than a handful of entities to a single aggregate, stop and question whether these objects truly share a consistency boundary or whether you are modelling a convenience cluster.

Domain events as the mechanism for eventual consistency: "When an aggregate completes a command that causes a state change, it publishes a domain event. Other aggregates subscribe and react, keeping their own state consistent in their own transaction."

---

## Fowler — Anemic Domain Model (2003)

Martin Fowler, "Anemic Domain Model". *martinfowler.com*, 2003. <https://martinfowler.com/bliki/AnemicDomainModel.html>

The definitive description of the anti-pattern this skill is designed to prevent:

> "The basic symptom of an Anemic Domain Model is that at first blush it looks like the real thing. There are objects, many named after the nouns in the domain space, and these objects are connected with the rich relationships and structure that true domain models have. The catch comes when you look at the behaviour, and you realize that there is hardly any behaviour on these objects, making them little more than bags of getters and setters. Indeed often these models come with design rules that say that you are not to put any domain logic in the domain objects. Instead there are a set of service objects which capture all the domain logic, carrying out all the computation and updating the model objects with the results."

Fowler identifies this as a violation of the fundamental principle of object-oriented design: encapsulation of data and behaviour together. He attributes the prevalence of the anemic model to developers who learn the noun-based structure of OO but not the behaviour-based principle.

Fowler's diagnosis: "The fundamental horror of this anti-pattern is that it's so contrary to the basic idea of object-oriented design; which is to combine data and process together."

---

## Evans on Domain Events (addendum, post-Blue-Book)

Evans did not include domain events as a first-class tactical pattern in the 2003 Blue Book. He has since acknowledged that domain events complete the tactical model and should be treated as a core building block alongside entities, value objects, and aggregates.

Key points (from conference talks and subsequent writing):
- A domain event is a record of something that happened in the domain — a business fact, not a technical notification.
- Domain events make the domain model's causal history explicit.
- Events should be named in past tense from the perspective of the domain, not the implementation.
- Events carry enough payload for consumers to act without querying back.

---

## Brandolini — Event Storming (2013–2019)

Alberto Brandolini, *Introducing EventStorming*. Leanpub, 2019. <https://www.eventstorming.com>

EventStorming is a workshop technique for discovering the domain model through domain events:

1. Start with domain events (orange stickies) — what happened?
2. Add commands (blue stickies) — what caused this event?
3. Add actors/users (yellow stickies) — who issued the command?
4. Cluster events around the aggregates that raise them (large frames).
5. Identify aggregate names from the clusters — the frame label becomes the aggregate name.
6. Identify policies (lilac stickies) — "whenever {event}, then {command}" — these become the event consumers in the domain event catalogue.

Brandolini's key insight: **naming domain events precisely forces precision about what the domain model actually does**. Vague events (`StatusUpdated`) reveal vague understanding; precise events (`ClaimApproved`, `PaymentFailed`) reveal domain knowledge.

EventStorming as input to this skill: if the project has run an Event Storming workshop, the output stickies map directly to:
- Orange stickies → `BC-NN.EVT-NN` domain events
- Frame labels → `BC-NN.AGG-NN` aggregate names
- Blue stickies → commands documented in the Command → Event table
- Lilac stickies → Consumers entries in the domain event catalogue
