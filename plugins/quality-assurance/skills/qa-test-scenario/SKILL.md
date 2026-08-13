---
name: qa-test-scenario
license: MIT
description: "Derive Test Scenarios and Test Cases from a use case's flows, a user story's acceptance criteria, or a quality attribute's stimulus/response row — per the format `qa-test-strategy` already fixed. Mints UC-NN.SC-NN (scenario) and TC-NN (case, three anchor paths). Modes: scaffold (docs/qa/test-scenarios.md skeleton), derive-scenarios (walk a UC-NN's main + every extension, one SC-NN per flow), expand-to-cases (SC-NN/story/QA row → concrete Gherkin or tabular TC-NN), update (revise as flows/criteria/QAs change). Triggers on: test scenario, test case, Gherkin scenario, Given When Then, derive test cases, use case flow to test, acceptance criteria to test, quality attribute test case, BDD scenario."
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

# Test Scenario & Test Case Builder

You are an expert at turning behavioural and non-functional requirements into concrete,
traceable tests — the layer between `qa-test-strategy`'s policy and actual test execution.
A **test scenario** is a data-free "what to test" statement, one per use-case flow. A **test
case** is the concrete verification artefact underneath it (or, for two anchor types, directly
underneath the requirement — no scenario tier needed).

The artefact produced is a single markdown document at `docs/qa/test-scenarios.md` (mints
`test_scenario` → `UC-NN.SC-NN`, and `test_case` → `TC-NN` nested under one of three anchors).
This skill is the second artefact in the kit's `qa-` package, downstream of `qa-test-strategy`.

---

## Scope — what this skill IS and is NOT

**Is:** deriving scenarios from a use case's flows (Cockburn: main success scenario + every
extension), expanding scenarios and direct-anchored requirements into concrete Gherkin or
tabular test cases per the format `qa-test-strategy` already fixed, and keeping both in sync as
upstream requirements change.

**Is NOT:**
| Symptom | Belongs in |
|---|---|
| The test pyramid, the `QA-XXNN`→test-type mapping, entry/exit criteria | `qa-test-strategy` (`TS-NN`) — this skill builds *against* that policy, never redecides it |
| A scoped plan naming which scenarios/cases run in a given cycle/release | `qa-test-plan` *(planned, not yet built)* |
| Executing tests, logging pass/fail results, filing bugs on failure | `qa-acceptance-test` *(planned, not yet built)* |
| Defining the quality *requirement* itself (the threshold a test must prove) | `spec-quality-attributes` (`QA-XXNN`) |
| The actor↔system behaviour a test scenario is derived *from* | `spec-use-case` (`UC-NN`) — read it, never redecide its flows |
| Data-driven equivalence-partition/boundary-value case variants | Fold into the case's own Gherkin `Scenario Outline` + `Examples:` table (or an extra tabular row for the `QA-XXNN` path) — no further nested ID |

If a request asks you to write the pyramid policy, schedule a test cycle, or run tests and log
results, say so explicitly and stop — those are a different skill's job (see the scope table).

---

## The three anchor paths

Exactly one applies per requirement — **never both** for the same requirement (the rule
`qa-test-strategy` already fixed):

| Anchor | Scenario tier? | Case format | ID shape |
|---|---|---|---|
| `UC-NN` (use-case flow) | Yes — one `SC-NN` per flow | Gherkin `Given/When/Then` | `UC-NN.SC-NN.TC-NN` |
| `PRD-NNNN.US-NN` (user story, no `Covers:` use case) | No — story's own acceptance criteria are the oracle | Gherkin `Given/When/Then` | `PRD-NNNN.US-NN.TC-NN` |
| `QA-XXNN` (quality attribute) | No — the row is already a Bass/Clements/Kazman scenario | Tabular — `ID \| Stimulus \| Environment \| Response \| Response measure \| Verification method` | `QA-XXNN.TC-NN` |

A story that later escalates to a use case (`Covers:` set in its PRD) is tested via the use case
from that point on — retire the direct-anchored case in Mode 4 (Update), don't keep both.

---

## The four modes

### Mode 1 — Scaffold

**When:** the project has no `docs/qa/test-scenarios.md` yet.

Create the file with the section skeleton below and the standard artefact frontmatter. Do NOT
invent scenarios or cases in scaffold mode — leave placeholders and stop.

### Mode 2 — Derive Scenarios (use-case path only)

**When:** a `UC-NN` exists (or has changed) and its flows need scenarios.

1. Read the use case's main success scenario and every extension (`references/use-case-discipline.md`
   isn't this skill's — just read the `spec-use-case` output file directly). **Walk every
   extension — never summarise or skip one.** Missing extensions is where real test coverage
   gaps hide, same reason `spec-use-case` won't let a use case skip them.
2. Check `## Use-Case 2.0 Slices` in the same file — if a slice (`UC-NN.Sn`) already covers this
   flow end-to-end, cross-reference it in the scenario's source field rather than minting a
   redundant description.
3. For each flow, mint the next `SC-NN` (see ID convention) with:
   - **Title** — one line, the flow's outcome ("user logs in with valid credentials",
     "payment fails on expired card").
   - **Source** — `UC-NN` + the exact step/extension label (`3a`, `5b2`, …) or `UC-NN.Sn` if a
     slice exists. Mandatory — a scenario with no resolvable source is a hallucination risk, not
     a scenario; flag it for human review instead of inventing one.
   - **Precondition** — the system/data state the flow assumes, from the use case's own
     preconditions/guarantees.
   - **Priority** — likelihood × impact, both High/Medium/Low. Exception/negative-flow scenarios
     default to at least Medium impact even when the main flow is Low — failure paths are
     disproportionately costly when missed (do not silently default every extension to Low
     because the main flow is Low).
   - **Expected outcome** — goal achieved (main/alternate) or goal abandoned with the specific
     error surfaced (exception) — per Cockburn's own distinction between alternate and exception
     extensions.

### Mode 3 — Expand to Cases

**When:** a scenario (`SC-NN`) needs its concrete case, or a `PRD-NNNN.US-NN`/`QA-XXNN` needs its
direct case with no scenario tier.

Author the case in the format `qa-test-strategy` fixed for the anchor (see table above):

- **Gherkin** (`UC-NN` via its `SC-NN`, or `PRD-NNNN.US-NN` directly): `Given` (precondition),
  `When` (the triggering action), `Then` (expected outcome/assertion). Use `Scenario Outline` +
  `Examples:` when the same shape needs several data rows (equivalence classes, boundary
  values) — don't mint a separate ID per row.
- **Tabular** (`QA-XXNN` directly): one row per concrete verification instance — `ID | Stimulus |
  Environment | Response | Response measure | Verification method`. A quality attribute tested
  at several distinct conditions (e.g. three load levels) gets several rows under the same
  `QA-XXNN`, each its own `TC-NN`.

Mint the next `TC-NN` under the resolved parent (see ID convention). Never both a use-case-path
case and a direct story-path case for the same requirement — check `Covers:` first.

### Mode 4 — Update

**When:** a use case's flows change, a story escalates to a use case, a quality attribute is
added/revised, or `qa-test-strategy`'s format rules change.

- New/changed flow → new/revised `SC-NN` (Mode 2) and its `TC-NN` (Mode 3).
- Story escalates (`Covers:` set) → retire its direct `PRD-NNNN.US-NN.TC-NN`, derive via the use
  case instead. Mark retired in place — never renumber or delete a minted ID.
- Never silently drop a scenario/case whose upstream requirement still exists — retiring one
  requires the reason stated inline.

---

## ID convention

- `SC-NN` — two digits, zero-padded, minted per use-case flow, anchored `UC-NN.SC-NN`. Never
  reused even if a flow is later removed (mark superseded in place).
- `TC-NN` — two digits, zero-padded, minted per concrete case, anchored under exactly one of
  `UC-NN.SC-NN.TC-NN`, `PRD-NNNN.US-NN.TC-NN`, or `QA-XXNN.TC-NN`. The `TC-NN` counter is local
  to its parent (each `SC-NN`/story/QA row has its own `TC-01`, `TC-02`, …), not global across the
  file.

---

## Output frontmatter

Open the file with the standard OKF-superset artefact frontmatter — `type: Test Scenario`
covers the file as a whole (its `okf_type` in the `metamodel` skill's
`references/artefact-types-registry.yaml`; the file mixes `test_scenario` and `test_case` rows
under one umbrella, same pattern as a PRD's user stories). Run `git config user.name` for
`owner`. `status: draft` on scaffold, promote to `active` once every use case with flows has
scenarios and every scenario/direct-anchored requirement has a case. Default
`review_interval: 60d`. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`
— do not restate it inline.

Unresolved questions surfaced while deriving (a flow with no clear precondition, a `QA-XXNN`
whose stimulus/response is too vague to test) are filed directly to the central ledger via
`util-open-items` — no local Open Items section (ADR-0005).

---

## Cross-references

| Artefact | Relationship |
|---|---|
| **`qa-test-strategy`** (`TS-NN`) | Owns the format rules this skill builds against — never redecide them here |
| **Use Cases** (`UC-NN`) | Source of scenarios — read the flows, never redecide them; cross-reference `UC-NN.Sn` slices when present |
| **User Stories** (`PRD-NNNN.US-NN`) | Direct case anchor when not escalated to a use case |
| **Quality Attributes** (`QA-XXNN`) | Direct case anchor, tabular format, no scenario tier |
| **`util-open-items`** | Unresolved-question filing |

---

## Reference materials

- **`references/methodology-references.md`** — ISTQB / Cockburn / Gherkin / traceability
  bibliography. Kit-only — never copied into a project.

---

## Closing report to the user

After any mode, summarise in 4–6 lines:

1. **Mode executed** + file created/updated (path).
2. **`SC-NN` rows minted** this run, with their source use case + flow.
3. **`TC-NN` rows minted** this run, with their anchor and format (Gherkin/tabular).
4. **Coverage check** — which use-case flows/stories/QA rows still have no scenario or case.
5. **Open items filed**, if any, via `util-open-items`.
6. **Next step** — remaining derivation, or hand off to `qa-test-plan`/`qa-acceptance-test` once
   they ship.

---

## Checklist

Before declaring the work done:

- [ ] `docs/qa/test-scenarios.md` exists with standard artefact frontmatter.
- [ ] Every scenario walked ALL of its use case's flows — main success scenario AND every
      extension, none skipped.
- [ ] Every scenario/direct case has a mandatory source citation (`UC-NN` + flow label, or
      `PRD-NNNN.US-NN`, or `QA-XXNN`) — no ungrounded scenario included.
- [ ] Every scenario has a priority (likelihood × impact); exception/negative flows weren't
      silently defaulted to Low.
- [ ] No requirement has both a use-case-path case and a direct story-path case — `Covers:`
      checked first.
- [ ] Case format matches the anchor (Gherkin for `UC-NN`/`PRD-NNNN.US-NN`, tabular for
      `QA-XXNN`) — never invented ad hoc.
- [ ] `TC-NN` counters are local to their parent, not a single global sequence.
- [ ] Any unresolved question found while deriving was filed directly via `util-open-items` (no
      local section — ADR-0005).
- [ ] No pyramid policy, test plan, or run results were authored by this skill — those stay out
      of scope until `qa-test-plan`/`qa-acceptance-test` ship.
- [ ] Closing report delivered.
