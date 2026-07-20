# Objective Discipline — Internal Claude Guidance

Internal reference for `business-objective` skill execution. Never copied to projects.

---

## The outcome vs output test

**Apply this test to every Key Result before accepting it.**

The test:
> "We will know we succeeded when ___________."

Fill the blank with the Key Result.

| Completion | Classification | Action |
|---|---|---|
| "...we shipped [feature]" | Output — **reject** | Rewrite: what metric changes when the feature works? |
| "...we completed [story points / tasks]" | Output — **reject** | Rewrite: what business outcome does the team's work produce? |
| "...we launched [product / module / release]" | Output — **reject** | Rewrite: what do users do differently after the launch? |
| "...we implemented [system / algorithm / process]" | Output — **reject** | Rewrite: what measurable result does the implementation produce? |
| "...[metric] changed from [baseline] to [target]" | Outcome — **accept** | Proceed |
| "...[user behaviour] increased / decreased from X to Y" | Outcome — **accept** | Proceed |
| "...[business metric] reached [threshold] and stayed there for [period]" | Outcome — **accept** | Proceed |

**Common rewrites:**

| ❌ Output KR | ✅ Outcome KR |
|---|---|
| Ship the surgeon confirmation module by Q3 | Surgeon confirmation rate rises from 60% to ≥ 90% within 30 days of launch |
| Build the scheduling algorithm | Schedule generation time falls from 3 working days to < 5 minutes |
| Launch mobile app | % of users accessing via mobile rises from 0% to ≥ 40% within 60 days |
| Complete onboarding flow | Time-to-first-value drops from 2 weeks to < 3 days for new clients |
| Implement conflict detection | Double-booking incidents reach 0/month and stay ≤ 0 for 90 consecutive days |

---

## BSC perspective classification decision tree

Tag each OBJ-NN with exactly one BSC perspective.

```
Is the primary success measure a revenue, cost, or profit metric?
  YES → Financial
  NO  ↓

Is the primary beneficiary an external customer or persona?
  YES → Customer
  NO  ↓

Is the primary change in an internal workflow, process, or operational efficiency?
  YES → Process
  NO  ↓

Is the primary change in team capability, knowledge, tooling, or organisational learning?
  YES → Learning
  NO  → Re-examine objective scope — it may be too broad or abstract
```

**Balance check:** a complete objectives set for a product should have at least one Customer-perspective objective. An objectives set with only Financial objectives ignores the user. An objectives set with only Learning objectives is not shipping.

---

## Anti-pattern detection cues

| Anti-pattern | Detection cue | Correction |
|---|---|---|
| Feature objective | "Build", "Ship", "Launch", "Implement", "Create" in the OBJ-NN title | Rewrite title as a future state: "From X to Y" or "Achieve [outcome]" |
| Output KR | "Ship", "Complete", "Launch", "Implement", "Deploy" in a KR row | Apply outcome vs output test → rewrite as metric change |
| Ambiguous KR baseline | No baseline value given | Ask: "What is the current state before this initiative?" If unknown: "Baseline: TBD (measure first)" |
| Ownerless objective | No owner role listed | Every OBJ-NN needs a named role; ask the user |
| Timeless objective | No timeframe given | Assign a timeframe: quarterly, annual, or initiative-scoped |
| Disconnected objective | No "Linked from" reference to `VP-NN` or `VS-N.M` | Flag: objective may be valid but ungrounded; ask user to link to commercial intent or pain point |
| Over-specified KR | KR describes the implementation method ("Use algorithm X to...") | Strip implementation details — KRs describe results, not methods |
| Binary all-or-nothing KR | "Zero incidents" or "100% satisfaction" as a hard target | Prefer threshold-plus-trend: "≤ 1 incident/month, trending to 0 over 90 days" |

---

## KR sizing rules

- **3–5 KRs per objective.** Fewer than 3 = the objective is under-specified. More than 5 = the objective is too broad — split it.
- **Targets should be achievable but stretching.** Doerr's 0.7 rule: if a team consistently scores 1.0 (fully achieved) on every KR, the targets are too low. A 0.6–0.7 average score on an ambitious KR is healthy.
- **Each KR must be independently verifiable.** A reviewer with access to the measurement source should be able to verify the KR without asking the team.
- **Avoid all-or-nothing KRs.** Binary pass/fail KRs turn partial wins into apparent total failures. Prefer threshold-plus-trend formulations.

---

## Align mode: traceability checks

When running Mode 3 (Align), apply these checks in order:

**Orphaned delivery (epic with no OBJ-NN):**
> An epic exists in the delivery roadmap with no reference to any OBJ-NN.
> This means work is being planned without a stated strategic reason.
> Action: ask the user to assign at least one OBJ-NN, or acknowledge it as exploratory / technical work (log as `OBJ-TECH` placeholder for traceability).

**Undelivered intent (OBJ-NN with no E-NN):**
> An objective exists with no epic planned to deliver it.
> This is a gap between stated intent and delivery planning.
> Action: either add an epic to the delivery roadmap, or explicitly note that the objective will not be pursued in this cycle (add a "Status: deferred — no epic planned" note to the OBJ-NN block).

**KR grounding a QA:**
> When a KR states a measurable threshold (e.g., "response time < 500ms", "error rate < 0.1%"), check whether a corresponding `QA-XXNN` entry exists in `docs/product-specs/09a-quality-attributes.md`.
> If not, flag: "KR-NN.M target could ground a QA-PE or QA-RE entry — consider running `spec-quality-attributes` Mode 3 (Update)."

**PRD traceability:**
> When a PRD exists (`docs/product-specs/prds/prd-NNNN-*.md`), check that `§0 Architecture Traceability` references at least one `OBJ-NN`.
> If not, flag: "PRD-NNNN has no OBJ-NN reference in §0 — the strategic 'why' of this PRD is unstated."
