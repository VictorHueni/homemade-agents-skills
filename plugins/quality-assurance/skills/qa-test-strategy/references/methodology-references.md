# Test Strategy — methodology bibliography

Canonical sources behind `qa-test-strategy`. **Kit-only** — project test-strategy
files link to this file via their header pointer; never copy it into a project's
`docs/`.

## Primary

| Source | Anchors |
|---|---|
| ISO/IEC/IEEE 29119-3:2021. *Software and systems engineering — Software testing — Part 3: Test documentation.* [iso.org/standard/81291.html](https://www.iso.org/standard/81291.html) | The strategy→plan→scenario→case authoring chain; canonical document set (test policy, test strategy, test plan, test case, test log) this skill's chain mirrors |
| ISTQB. *Certified Tester Foundation Level (CTFL) Syllabus* + *Standard Glossary of Terms used in Software Testing.* [istqb.org](https://www.istqb.org/) · [glossary.istqb.org](https://glossary.istqb.org/) | Test levels (unit/integration/system/acceptance), entry/exit criteria, test roles (manager/analyst/executor), defect lifecycle & severity/priority vocabulary |
| Cohn, M. (2009). *Succeeding with Agile: Software Development Using Scrum.* Addison-Wesley. Test-pyramid chapter also summarised at [martinfowler.com/bliki/TestPyramid.html](https://martinfowler.com/bliki/TestPyramid.html) (Fowler's canonical restatement) | Origin of the **test pyramid**: unit-heavy, few slow/brittle end-to-end tests |
| Dodds, K. C. (2018). *The Testing Trophy and Testing Classifications.* [kentcdodds.com/blog/the-testing-trophy-and-testing-classifications](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications) | The **testing trophy**: static analysis as a first-class layer, integration tests weighted over unit, thin E2E — the pyramid's counter-proposal for integration-boundary-heavy systems |
| Bass, L., Clements, P. & Kazman, R. (2021). *Software Architecture in Practice* (4th ed.). Addison-Wesley. | Quality-attribute scenario shape (stimulus / environment / response / response measure) — the tabular test-case format this strategy mandates for `QA-XXNN`-anchored cases |

## Supporting

| Source | Anchors |
|---|---|
| Google Testing Blog — [Just Say No to More End-to-End Tests](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html) | Independent restatement of pyramid reasoning from a large-scale test-suite maintenance perspective |
| Crispin, L. & Gregory, J. (2009). *Agile Testing: A Practical Guide for Testers and Agile Teams.* Addison-Wesley. | The Agile Testing Quadrants — classifies test types by business-facing/technology-facing and support-programming/critique-product axes; complements the pyramid/trophy allocation with a "what kind of test is this" lens |
| ISO/IEC 25010:2023. *Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model.* | The `QA-XXNN` characteristic set this strategy's mapping table verifies — canonical source lives in `spec-quality-attributes/references/nfr-definition-and-examples.md`, cited here for the mapping table's other half |
| North, D. (2006). *Introducing BDD.* [dannorth.net/introducing-bdd](https://dannorth.net/introducing-bdd/) | Given/When/Then (Gherkin) origin — the mandated format for use-case/user-story-anchored test cases |

## Where sources disagree

- **Pyramid vs. trophy** — Cohn's pyramid assumes unit tests are cheap and
  integration boundaries are stable; Dodds' trophy assumes the opposite (unit
  tests around pure logic buy little confidence when the real risk sits at
  API/DB/third-party boundaries). Neither is universally correct — this skill
  requires the project to pick one explicitly (Mode 2) and state *why*, rather
  than defaulting either way.
- **Static analysis as a "test level"** — ISTQB's classic four levels (unit /
  integration / system / acceptance) predate the trophy's promotion of static
  analysis to a first-class layer. This skill's Environments/Tooling sections
  accommodate both without forcing a project onto either taxonomy.
