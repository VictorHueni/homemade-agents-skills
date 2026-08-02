---
name: agent-grill-me
description: "Interactive Socratic stress-test of a PRD or implementation plan: one focused question at a time, project domain vocabulary checked against docs/domain/glossary.md, decisions crystallised into ADRs via arch-adr. Triggers on: grill me on this PRD, grill me on this plan, stress-test this with me, question this spec, challenge my thinking, interview me about this plan."
version: "1.0.0"
status: draft
last_reviewed: 2026-06-16
review_interval: 180d
user-invocable: true
impact: "low"
metadata:
  category: "agent"
  complexity: "high"
---

# Grill Me

## Objective

Stress-test a PRD or implementation plan through a live Socratic session. Unlike `agent-peer-review` (static document scan), this skill grills the *author* one question at a time: surfacing ambiguities, enforcing domain vocabulary, and crystallising decisions into ADRs while context is live.

Use after the artefact exists and before coding starts. Pair with `agent-peer-review` for full coverage: peer-review finds mechanical gaps automatically; grill-me surfaces the thinking gaps that only emerge under questioning.

## Inputs

1. Target artefact path (PRD or implementation plan — one at a time).
2. Optional: section focus (e.g. "just the acceptance criteria" or "increment 3 only").
3. Optional: additional context paths (linked docs, schema, bounded context doc).

## Workflow

### Phase 0 — Domain load (silent, before first question)

1. Read the target artefact end-to-end.
2. Read `docs/domain/glossary.md` if it exists.
3. Read any relevant `docs/domain/bounded-contexts/` file if the artefact names a bounded context.
4. Read any ADRs linked from the artefact or referenced by it.
5. State your initial hypothesis + confidence before asking anything.

Format:
```
HYPOTHESIS: <one sentence — what you currently believe about this document's coherence and completeness>
CONFIDENCE: <N>% — <what's still unresolved or missing, if below ~70%>
```

### Phase 1 — Grilling loop

Full mechanics in `references/grill-protocol.md`.

One question at a time. Each question follows this format:
```
Q:      <one focused question>
SOURCE: <artefact section or domain rule that prompted this>
GUESS:  <your hypothesis for the answer, and why>
```

Priority ladder (hardest gaps first):
1. Domain language violations — term in the artefact conflicts with the glossary
2. Missing or vague acceptance criteria / test gates
3. Scope ambiguity — what's explicitly out of scope
4. Dependency blindspots — what must exist before this
5. Reversibility gaps — what can't be undone if wrong
6. User/persona misalignment — who is this actually for
7. *(implementation plans only)* non-atomic increments, missing `Status:` fields, non-executable test gates

**Side effects during Phase 1 — apply immediately, never batch:**
- **Term sharpened** → offer to patch `docs/domain/glossary.md` right there (via `domain-glossary` conventions)
- **Decision crystallised** → evaluate against ADR criteria (see `references/adr-criteria.md`); if all three gates pass, log via `arch-adr`
- **Gap resolved by user** → offer to patch the artefact inline

### Phase 2 — Restate (when confidence ≥ 90%)

Write back what the session established:

```
Here's what this session established:

- Scope confirmed:          <one line>
- Ambiguities resolved:     <bullet list>
- Terms clarified/added:    <term → glossary ref, or "none">
- ADRs logged:              ADR-NNNN: <title>  (or "none")
- Remaining open questions: <list or "none">

Accept / adjust?
```

Wait for an explicit confirmation — not "whatever you think" or silence.

### Phase 3 — Session record (optional)

Offer to write `var/reports/grill-me/YYYY-MM-DD-<slug>.md` with the session summary and a list of all patches applied.

## Metamodel classification

Stage 2B — variant of the spec review space. Does not add a new build order step or mint new IDs. Output = mutated PRD/plan + new ADRs (handled by `arch-adr`). No metamodel.md update required.

## Verification checklist

After the session:

- [ ] Hypothesis + confidence were stated before the first question
- [ ] Every confidence number below ~70% had a one-line reason attached
- [ ] Questions were asked one at a time, each with SOURCE and GUESS
- [ ] At least one domain-vocabulary check ran (glossary read or "no glossary found — skipped")
- [ ] All ADRs logged during the session meet the three-gate rule (see `references/adr-criteria.md`)
- [ ] Restate was written and confirmed explicitly (not just "sounds good")
- [ ] Glossary and artefact patches were applied inline during the session, not batched at the end
