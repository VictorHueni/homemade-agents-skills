# Use Case — methodology bibliography

Canonical sources behind `spec-use-case`. **Kit-only** — project use-case files link to this file via their header pointer; never copy it into a project's `docs/`.

## Primary

| Source | Anchors |
|---|---|
| Cockburn, A. (2000). *Writing Effective Use Cases.* Addison-Wesley. [InformIT](https://www.informit.com/store/writing-effective-use-cases-9780201702255) · [manuscript draft (PDF)](https://people.inf.elte.hu/molnarba/Informaciorendszerek_ELTE/Writing_effective_Use_cases_Cockburn.pdf) | Goal levels (cloud/kite/sea/fish/clam), design scope, primary actor + stakeholders & interests, main success scenario + extensions, guarantees, fully-dressed vs casual, the use case as a stakeholder contract, the style do's/don'ts |
| Jacobson, I., Spence, I., & Bittner, K. (2011). *Use-Case 2.0 — The Guide to Succeeding with Use Cases.* Ivar Jacobson International. [ebook](https://www.ivarjacobson.com/publications/white-papers/use-case-20-e-book) · [PDF](https://www.ivarjacobson.com/files/use-case_2_0_e-book_2023_0.pdf) · [ACM Queue summary](https://queue.acm.org/detail.cfm?id=2912151) | Use-case narrative, flows (basic + alternative), use-case slices, slices↔backlog, test cases per slice, the six principles |
| Jacobson, I. (1992). *Object-Oriented Software Engineering: A Use Case Driven Approach (OOSE).* Addison-Wesley. | Origin of use cases and actors; UML use-case lineage |
| Object Management Group. *Unified Modeling Language (UML) Specification.* [omg.org/spec/UML](https://www.omg.org/spec/UML/) | Formal semantics of actors, system boundary, `«include»`, `«extend»`, generalization |

## Supporting

| Source | Anchors |
|---|---|
| Larman, C. (2004). *Applying UML and Patterns* (3rd ed.). Prentice Hall. [InformIT](https://www.informit.com/store/applying-uml-and-patterns-an-introduction-to-object-oriented-9780131489066) | Use-case-driven OOA/D; fully-dressed vs brief vs casual formats; system-sequence diagrams from use cases |
| Fowler, M. (2003). *UML Distilled* (3rd ed.). Addison-Wesley. [martinfowler.com/books/uml](https://martinfowler.com/books/uml.html) | Pragmatic use-case-diagram guidance; caution against `«include»`/`«extend»` over-modelling |
| Wiegers, K. & Beatty, J. (2013). *Software Requirements* (3rd ed.). Microsoft Press. [Microsoft Press Store](https://www.microsoftpressstore.com/store/software-requirements-9780735679665) | Use cases within a requirements process; use cases vs functional requirements |
| IIBA. (2015). *BABOK Guide* v3 — Use Cases and Scenarios (§10.x). [iiba.org](https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/) | Business-analysis framing of use-case modelling |
| Cohn, M. — [Advantages of User Stories over Use Cases](https://www.mountaingoatsoftware.com/articles/advantages-of-user-stories-for-requirements) · Stellman & Greene — [User Stories vs Use Cases](https://www.stellman-greene.com/2009/05/03/requirements-101-user-stories-vs-use-cases/) | The use-cases-vs-user-stories positioning; need vs behaviour distinction |
| Visual Paradigm — [Use Case Diagram guide](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/what-is-use-case-diagram/) · [Cloud/Kite/Sea/Fish/Clam scope](https://guides.visual-paradigm.com/navigating-scope-the-impact-of-cloud-kite-sea-fish-clam-in-use-case-analysis/) · Sparx — [Include vs Extend](https://www.sparxsystems.us/enterprise-architect/include-vs-extend-use-case-diagrams-ea-uml/) | Practitioner reference for diagram relationships and goal-level metaphor; the "≤20 use cases per diagram" heuristic |

## Where sources disagree

- **Use cases vs user stories** — story-first agile writers (Cohn) treat use cases as heavyweight; Jacobson's Use-Case 2.0 reframes them as *complementary* (slices = stories). This skill takes the Use-Case 2.0 position: one artefact, two readings.
- **`«include»` / `«extend»` semantics** — endlessly confused in practice; the OMG spec is authoritative, but most practitioners (Fowler) advise minimising both and keeping branch logic in the **text extensions**, not the diagram. This skill follows Fowler: diagram optional, text is the contract.
