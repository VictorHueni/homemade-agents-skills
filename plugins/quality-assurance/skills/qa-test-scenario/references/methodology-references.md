# Test Scenario & Test Case — methodology bibliography

Canonical sources behind `qa-test-scenario`. **Kit-only** — project test-scenario files link to
this file via their header pointer; never copy it into a project's `docs/`.

## Primary

| Source | Anchors |
|---|---|
| ISTQB. *Standard Glossary of Terms used in Software Testing.* [glossary.istqb.org](https://glossary.istqb.org/) | Test condition / test case / test scenario (synonym of "test procedure specification") definitions — the hierarchy this skill's scenario→case split is built on, adapted per the practitioner convention below since the strict glossary wording doesn't itself separate the two |
| ISO/IEC/IEEE 29119-3:2021. *Software and systems engineering — Software testing — Part 3: Test documentation.* [iso.org/standard/81291.html](https://www.iso.org/standard/81291.html) | The strategy→plan→scenario→case authoring chain `qa-test-strategy` and this skill together implement; ISO's own vocabulary uses "test procedure specification" rather than "test scenario" |
| Cockburn, A. (2001). *Writing Effective Use Cases.* Addison-Wesley. | Main success scenario + extensions (alternate/exception) — the derivation rule this skill mints one `SC-NN` from: one scenario per flow, extensions distinguished by whether the goal is still reached |
| North, D. (2006). *Introducing BDD.* [dannorth.net/introducing-bdd](https://dannorth.net/introducing-bdd/); Cucumber. *Gherkin Reference.* [cucumber.io/docs/gherkin/reference](https://cucumber.io/docs/gherkin/reference/) | Given/When/Then structure and `Scenario Outline` + `Examples:` — the case format for `UC-NN`/`PRD-NNNN.US-NN`-anchored requirements, including how data variation folds into one case without a further nested ID |
| Bass, L., Clements, P. & Kazman, R. (2021). *Software Architecture in Practice* (4th ed.). Addison-Wesley. | Quality-attribute scenario shape (stimulus / environment / response / response measure) — why a `QA-XXNN` row needs no separate scenario tier before its tabular test case |

## Supporting

| Source | Anchors |
|---|---|
| Guru99. *Test Case vs Test Scenario.* [guru99.com/test-case-vs-test-scenario.html](https://www.guru99.com/test-case-vs-test-scenario.html) | The practitioner convention (scenario = high-level, data-free; case = concrete steps + data) this skill follows where it goes beyond ISTQB's literal glossary wording |
| StickyMinds. *Use Case Derived Test Cases.* | The "one test case minimum for the main success scenario, plus one per extension" derivation rule, cited for the mechanical never-skip-a-flow instruction |
| Guru99. *Requirements Traceability Matrix.* [guru99.com/traceability-matrix.html](https://www.guru99.com/traceability-matrix.html) | Forward/backward traceability — the reason every scenario/case carries a mandatory source citation field |
| Medium/TestCaseLab; BrowserStack. *Risk-Based Testing.* | Risk = likelihood × impact — the priority field's basis, and why exception/negative flows default to at least Medium impact |

## Where sources disagree

- **"Test scenario" as ISTQB defines it vs. the practitioner convention.** ISTQB's glossary
  treats "test scenario" as a synonym of "test procedure specification" (a sequencing of
  cases), not a distinct higher-level artefact. This skill follows the widespread
  practitioner convention instead (Guru99, BrowserStack, ArtOfTesting) because that's what a
  user invoking a skill named "test scenario" expects, and because clew's canonical metamodel
  already models `test_scenario` as a distinct type upstream of `test_case`. State this
  divergence rather than presenting it as settled ISTQB terminology.
