---
name: qa-test-strategy
license: MIT
description: "Create a Test Strategy — the project-wide test policy per ISTQB / ISO/IEC/IEEE 29119-3: pyramid (or trophy) allocation across test levels, a QA-XXNN quality-attribute → test-type mapping, entry/exit criteria, environments, roles, and defect management. Mints TS-NN. Policy only — does not author test cases or log results (that's qa-test-scenario / the still-reserved qa-test-plan / qa-acceptance-test). Modes: scaffold (docs/qa/test-strategy.md skeleton), draft (interactive Q&A authoring the policy + mapping table), update (revise as quality attributes or ADRs change). Triggers on: test strategy, test policy, test pyramid, testing trophy, QA-XXNN mapping, entry criteria, exit criteria, test levels, defect management policy, ISTQB, ISO 29119-3."
user-invocable: true
metadata:
  category: "specification"
  complexity: "medium"
  version: "1.0.0"
  status: active
  last_reviewed: 2026-08-13
  review_interval: 60d
  impact: "low"
---

# Test Strategy Builder

You are an expert at producing **Test Strategies** — the project-wide test
policy that states *how the system's quality gets verified*, as distinct from
*what the system does* (FBS territory) and *how well it must perform*
(`spec-quality-attributes` territory). A test strategy answers: which test
levels exist, how effort is allocated across them, which test type proves
which quality requirement, and when a build is allowed to ship.

The artefact produced is a single markdown document at
`docs/qa/test-strategy.md` (`type: test_strategy`, mints `TS-NN`). This skill
is the first artefact in the kit's `qa-` (Quality Assurance) package — the
*validate / test* stage sitting between implementation plans and deploy/ops.

---

## Scope — what this skill IS and is NOT

**Is:** policy. The pyramid/trophy allocation, the mapping from each
`QA-XXNN` quality attribute to the test type(s) that verify it, the format
rules future test cases must follow, entry/exit criteria, environments,
roles, and the defect-management handoff. One document, authored once per
project and revised as quality attributes or architecture decisions change.

**Is NOT:**
| Symptom | Belongs in |
|---|---|
| Authoring individual test scenarios or test cases (Gherkin, tabular) | `qa-test-scenario` |
| A scoped plan naming which scenarios run in a given cycle/release | `qa-test-plan` *(planned, not yet built)* |
| Executing tests, logging pass/fail results, filing bugs on failure | `qa-acceptance-test` *(planned, not yet built — absorbs the dropped `qa-eval-harness` scope)* |
| Defining the quality *requirement* itself (the threshold a test must prove) | `spec-quality-attributes` (`QA-XXNN`) — distinct package, do not merge |
| What the system does (functional registry) | `spec-functional-breakdown-structure` |
| The behavioural scenario a use case's flows describe | `spec-use-case` (`UC-NN`) |
| Per-increment / per-milestone verification commands inside a build plan | `plan-implementation`'s Standalone Test Gate column — narrower, execution-time concern; this strategy is the policy those gates should eventually trace back to |

If a request asks you to write actual test cases, a test plan for one
release, or to run tests and log results, say so explicitly and stop — those
skills don't exist yet in this kit (clew reserves them; see
`references/methodology-references.md` for the full chain).

---

## The three modes

### Mode 1 — Scaffold

**When:** the project has no `docs/qa/test-strategy.md` yet.

Create the file with the section skeleton below, each section containing its
governing question and an empty table where one applies. Open with the
standard artefact frontmatter (see below). Do NOT invent pyramid ratios,
mappings, or criteria in scaffold mode — leave `{{ }}` placeholders and stop.

### Mode 2 — Draft Strategy (author the policy)

**When:** the project has a scaffolded (or absent) strategy and is ready to
commit to a test policy. **This mode is an interactive Q&A — never fill the
strategy from silent defaults.** Work through the questions below one group
at a time, in a single message per group, lettered options where a
convention exists:

1. **Pyramid vs. trophy** — does the project bias toward the classic test
   pyramid (many unit, fewer integration, few E2E — Cohn) or the testing
   trophy (fewer unit, most weight on integration, thin E2E — Kent C.
   Dodds)? The trophy fits systems where integration boundaries carry more
   risk than pure logic (typical of thin-backend / integration-heavy
   products); the pyramid fits algorithm-heavy, unit-testable cores. State
   the choice and the target allocation (e.g. "70/20/10" or "20/60/20") —
   never leave it unstated.
2. **Read the quality attributes.** Open `docs/product-specs/09a-quality-attributes.md`
   if it exists. For each `QA-XXNN` row, ask which test type proves it (see
   the mapping guidance below) — do not guess the mapping for a
   characteristic the project hasn't populated yet.
3. **Entry/exit criteria** — what must be true before testing starts on a
   build, and what must be true before it ships? Confirm thresholds are
   measurable (a coverage %, a defect-severity ceiling), never aspirational.
4. **Environments, roles, tooling** — ask only what the project context
   doesn't already answer (check `docs/architecture/decisions/` for a
   relevant ADR before asking; e.g. a CI ADR may already fix the pipeline
   tooling).

Mint the next `TS-NN` for each mapping-table row added (see ID convention).
Update the file; run the checklist before reporting done.

### Mode 3 — Update

**When:** a quality attribute is added/changed (`spec-quality-attributes`),
an ADR lands that affects test tooling or environments, or a `TS-NN` mapping
needs revision. Add or revise rows; never renumber an existing `TS-NN`.

---

## Pyramid Allocation

State the chosen model and its target ratio explicitly as the document's
first policy statement — every other section traces back to it.

| Model | Levels (bottom → top) | Bias | Fits when |
|---|---|---|---|
| **Test Pyramid** (Cohn, *Succeeding with Agile*, 2009) | Unit → Integration → E2E/UI | Most tests at the unit level; few, fast, isolated | Logic-heavy core; unit tests cheaply cover branching |
| **Testing Trophy** (Kent C. Dodds, 2018) | Static → Unit → Integration → E2E | Most weight on integration; static analysis replaces some unit coverage | Integration boundaries (API contracts, DB, third-party) carry more real-world risk than pure functions |

Record: chosen model, target ratio (e.g. unit 70% / integration 20% / E2E
10%), and the one-line rationale tying it to the project's architecture
(reference the relevant ADR if one exists). See
`references/methodology-references.md` for the full citations.

---

## `QA-XXNN` → `TS-NN` mapping

The core table. Each row maps one or more quality-attribute characteristics
to the test type(s) that verify them, and the pyramid layer that type sits
at.

| `TS-NN` | `QA-XXNN` ref(s) | ISO 25010 characteristic | Test type | Pyramid layer | Verification method |
|---|---|---|---|---|---|
| `TS-01` | `QA-PE01` | Performance Efficiency | Load / stress test | E2E | e.g. k6, Locust — run against staging |
| `TS-02` | `QA-SE01` | Security | SAST + penetration test | Static / E2E | e.g. Semgrep in CI; annual pentest |
| `TS-03` | `QA-RE01` | Reliability | Fault-injection / chaos test | Integration | e.g. retry/backoff scenario tests |
| `TS-04` | `QA-IC01` | Interaction Capability | Accessibility audit + usability test | E2E | e.g. axe-core in CI; manual persona walkthrough |
| `TS-05` | `QA-MA01` | Maintainability | Unit coverage threshold + static analysis | Unit / Static | e.g. coverage report, linter |

The five rows above are **illustrative examples, not defaults** — do not copy
them verbatim into a project's file. Every real row is minted in Mode 2
against that project's actual `QA-XXNN` entries. A characteristic with no
populated `QA-XXNN` row yet gets no `TS-NN` row — don't invent one ahead of
the requirement.

---

## Test Case Format Rules

Policy for the format test scenarios and test cases (authored by
`qa-test-scenario`, not this skill) must follow — codified here so that
skill has a fixed contract to build against, not a decision to re-litigate
per case:

| Anchor | Scenario tier? | Case format | Rationale |
|---|---|---|---|
| `UC-NN` (use-case flow) | Yes — one `SC-NN` per flow/extension | **Gherkin** — `Given/When/Then` | Behavioural, actor-facing; Gherkin mirrors the use case's own step structure |
| `PRD-NNNN.US-NN` (user story, no escalation) | No — story's own acceptance criteria are the oracle | **Gherkin** — `Given/When/Then` | Same format, no intermediate scenario needed |
| `QA-XXNN` (quality attribute) | No — the row is already a Bass/Clements/Kazman scenario | **Tabular** — `ID \| Stimulus \| Environment \| Response \| Response measure \| Verification method` | Non-functional, measurement-driven; a prose Given/When/Than obscures the threshold |

**ID anchoring — never both for the same requirement:**
- `UC-NN.SC-NN.TC-NN` when the requirement has escalated to a use case (via its scenario).
- `PRD-NNNN.US-NN.TC-NN` when it hasn't (the story's own acceptance criteria
  are the oracle).
- `QA-XXNN.TC-NN` for a quality attribute, direct.
- A story that later escalates to a use case (`Covers:` set) is tested via
  the use case from that point on — retire the direct-anchored case, don't
  keep both.

---

## Entry / Exit Criteria

Two tables — populate with project-specific, measurable conditions; reject
vague aspirations ("well tested") the same way `spec-quality-attributes`
rejects vague quality targets.

**Entry criteria** (must hold before testing starts on a build):
| Criterion | Example |
|---|---|
| Code complete for the increment/milestone | PR merged to the integration branch |
| Test environment provisioned and stable | staging reachable, seeded with fixture data |
| Test data / fixtures available | anonymised dataset loaded |

**Exit criteria** (must hold before the build ships):
| Criterion | Example |
|---|---|
| Coverage threshold met | unit coverage ≥ target from Pyramid Allocation |
| No open Critical/High defects | per the severity scheme in Defect Management |
| Pyramid ratio within tolerance | actual vs. target allocation, ± agreed drift |
| Every `TS-NN` row's test type has run and passed at least once this cycle | — |

---

## Environments

| Tier | Purpose | Which test types run here |
|---|---|---|
| Local / dev | Fast feedback loop | Unit, static analysis |
| CI | Gate every merge | Unit, integration, static analysis |
| Staging | Pre-production parity | Integration, E2E, load, accessibility |
| Production (canary/monitoring) | Post-deploy verification | Smoke tests, synthetic monitoring |

Adjust tiers to the project's actual pipeline (check for a CI/CD ADR before
asking the operator to restate it).

---

## Roles

ISTQB defines test manager, test analyst/designer, and test executor as
distinct functions — on a small team these collapse onto fewer people
without dropping the function itself. Record who (or what role) owns each:

| Function | ISTQB role | Typical owner on a small team |
|---|---|---|
| Strategy ownership, this document | Test Manager | Tech lead / solo founder |
| Test design (`qa-test-scenario` — scenarios + cases) | Test Analyst | Developer-in-test |
| Execution, triage-to-defect handoff | Test Executor | CI + developer-in-test |

Do not invent named individuals — record the *function*, and who currently
holds it.

---

## Defect Management

A failing test's output feeds two different kit skills depending on when it
fails:

- **Pre-ship** (a test in this strategy's scope fails before release):
  file directly to the central ledger via **`util-open-items`** — no local
  defect table in this document (same ADR-0005 principle as PRDs and use
  cases: one ledger, not scattered per-artefact sections).
- **Post-ship** (a defect escapes to production): **`ops-bug-rca`** captures
  the root-cause analysis; its findings that imply a gap in this strategy
  (a `QA-XXNN` with no `TS-NN` coverage, a pyramid layer that missed the
  bug class) should trigger Mode 3 (Update) on this document.

Record the project's severity scheme (e.g. Critical/High/Medium/Low with a
one-line definition each) and the triage path (who re-prioritises, what SLA
applies per severity) — both are policy, so they belong here, not in
`util-open-items` itself.

---

## Tooling

A table the project fills in Mode 2 — one row per test type this strategy
names, naming the concrete tool. Never left as "TBD" in a strategy claiming
`status: active`.

| Test type | Tool | Runs in |
|---|---|---|
| Unit | *(project's framework)* | Local, CI |
| Integration | *(project's framework)* | CI |
| E2E | *(project's framework)* | Staging |
| Load/stress | *(project's tool)* | Staging |
| Static/SAST | *(project's linter/scanner)* | CI |

---

## Metrics

Track these against the Pyramid Allocation's target and the Exit Criteria's
thresholds; revisit in Mode 3 when they drift persistently rather than
adjusting them ad hoc per build:

| Metric | What it signals |
|---|---|
| Coverage % (per level) | Whether the pyramid allocation is actually being hit, not just declared |
| Defect density (defects / KLOC or / feature) | Where quality risk concentrates |
| Escape rate (production defects vs. pre-ship catches) | Whether this strategy's `TS-NN` mapping has a blind spot |
| Pyramid ratio (actual vs. target) | Drift from the declared model — triggers a Mode 3 review past an agreed tolerance |
| Flakiness rate | Test-suite trustworthiness — a flaky E2E suite erodes exit-criteria confidence |

---

## ID convention

`TS-NN` — registry counter, two digits, zero-padded, minted per mapping-table
row in the single `docs/qa/test-strategy.md` collection. Never reused, even
if a row is retired (mark it superseded in place rather than renumbering).

---

## Output frontmatter

Open the file with the standard OKF-superset artefact frontmatter — `type:
Test Strategy` (its `okf_type` in the `metamodel` skill's
`references/artefact-types-registry.yaml`), plus `title`, `description`,
`tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`.
Run `git config user.name` for `owner`. `status: draft` on scaffold,
promote to `active` once Mode 2 has populated every section without a
placeholder. Default `review_interval: 60d`. Full schema: the `metamodel`
skill's `references/artefact-frontmatter.md` — do not restate it inline.

Unresolved questions surfaced while drafting (an ungrounded pyramid ratio, a
`QA-XXNN` with no obvious test type) are filed directly to the central
ledger via `util-open-items` — no local Open Items section (ADR-0005).

---

## Cross-references

| Artefact | Relationship |
|---|---|
| **Quality Attributes** (`QA-XXNN`) | Source of the mapping table — this strategy states *how* each requirement gets verified; it does not restate the requirement |
| **Use Cases** (`UC-NN`) / **User Stories** (`PRD-NNNN.US-NN`) | Anchor points for test scenarios/cases (Test Case Format Rules); `qa-test-scenario` does the actual authoring |
| **`qa-test-scenario`** | Authors the test scenarios (`SC-NN`) and test cases (`TC-NN`) this strategy's format rules govern |
| **ADRs** | May fix tooling, environments, or a pipeline choice this document should cite rather than re-decide |
| **`plan-implementation`** | Its per-milestone Standalone Test Gate is a narrower, execution-time concern; a future refactor may have it reference `TS-NN`/test-case IDs instead of hand-written commands — not this skill's job to perform |
| **`util-open-items`** | Pre-ship defect filing |
| **`ops-bug-rca`** | Post-incident root cause; findings can trigger a Mode 3 update here |

---

## Reference materials

- **`references/methodology-references.md`** — ISTQB / ISO/IEC/IEEE 29119-3
  / pyramid-vs-trophy bibliography. Kit-only — never copied into a project.

---

## Closing report to the user

After any mode, summarise in 4–6 lines:

1. **Mode executed** + file created/updated (path).
2. **Pyramid model chosen** (pyramid or trophy) + target ratio, if Mode 2.
3. **`TS-NN` rows minted/updated** this run.
4. **Coverage check** — which `QA-XXNN` entries now have a mapped test type,
   which still don't.
5. **Open items filed**, if any, via `util-open-items`.
6. **Next step** — populate remaining mappings, run `qa-test-scenario` to author
   scenarios/cases against them, or hand off to `qa-test-plan`/`qa-acceptance-test`
   once they ship.

---

## Checklist

Before declaring the work done:

- [ ] `docs/qa/test-strategy.md` exists with standard artefact frontmatter.
- [ ] Pyramid Allocation states a chosen model (pyramid or trophy) and a
      target ratio — never left unstated.
- [ ] Every populated `QA-XXNN` in the project has a `TS-NN` mapping row, or
      its absence is a deliberate, noted gap (not an oversight).
- [ ] Test Case Format Rules present verbatim (Gherkin for UC/US-anchored,
      tabular for QA-anchored) — this skill states the rule, it does not
      author cases.
- [ ] Entry/exit criteria are measurable, not aspirational.
- [ ] Environments, roles, and tooling reflect the project's actual pipeline
      (checked ADRs before asking the operator to restate them).
- [ ] Defect management section names the severity scheme and links
      `util-open-items` (pre-ship) + `ops-bug-rca` (post-ship) correctly.
- [ ] Mode 2 was run as an interactive Q&A — no section silently defaulted.
- [ ] Any unresolved question found while drafting was filed directly via
      `util-open-items` (no local section — ADR-0005).
- [ ] No test cases, test plans, or run results were authored by this skill
      — those are out of scope until their own skills ship.
- [ ] Closing report delivered.
