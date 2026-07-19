# ADR Logging Criteria

Calibrated for use within `agent-grill-me` sessions. Consistent with `arch-adr` skill conventions.

## The three-gate rule

Log an ADR only when **all three** are true:

1. **Hard to reverse** — the cost of changing this decision later is meaningful (data migration, breaking API contract, significant rework, organisational impact).
2. **Surprising without context** — a future reader will wonder "why did they do it this way?" The decision is not the obvious default for this stack or domain.
3. **Real trade-off** — genuine alternatives existed and were weighed. You picked one for specific reasons, not because it was the only option.

If any gate is missing, skip the ADR. Record the decision as a clarification in the PRD or plan instead.

## Common false positives

| Looks like an ADR | Why it isn't | What to do instead |
|---|---|---|
| "We decided to use PostgreSQL" | Obvious default for the stack; no real trade-off surfaced | Add a note to the implementation plan |
| "We clarified that 'user' means authenticated account" | Term resolution, not a hard-to-reverse architectural decision | Patch `docs/domain/glossary.md` |
| "We agreed increment 3 comes before increment 2" | Sequencing clarification, not surprising or hard to reverse | Update the plan ordering |
| "We chose REST over GraphQL after brief discussion" | Real trade-off — but only log if the reasoning will be non-obvious to a future reader in this project's context | Judgment call; if REST is the obvious default here, skip it |

## Handing off to arch-adr

When all three gates pass, do NOT write the ADR inline. Hand off:

1. Say: *"This decision meets ADR criteria — logging now via arch-adr."*
2. Invoke `arch-adr` with:
   - **Title**: one line, imperative verb ("Use X for Y", "Adopt X over Y")
   - **Status**: `accepted`
   - **Context**: what situation forced this decision
   - **Decision**: what was chosen
   - **Alternatives considered**: what was rejected and why
   - **Consequences**: what becomes easier / harder / required as a result
3. Record the resulting ADR-NNNN reference in the Phase 2 restate.

## ADR density signal

More than two ADRs from a single grilling session is a warning sign. Either the artefact had fundamental unresolved decisions baked in (expected — surface them), or the three-gate rule is being applied too loosely (problematic — re-check each one). Pause and re-evaluate before logging a third.
