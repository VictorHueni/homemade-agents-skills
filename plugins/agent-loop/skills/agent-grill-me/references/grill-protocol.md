# Grill Protocol

Full mechanics for the `agent-grill-me` session loop.

## Confidence tracking

State a confidence number (0–100%) before the first question and update it mentally as the session progresses. Stop grilling when:

1. Confidence ≥ 90%, AND
2. You can predict the user's reaction to the next three questions you would ask

Both conditions must be met. Confidence without predictability means you've stopped asking hard enough questions. Predictability without the number means you may be falsely certain.

**Below 70%:** always attach a one-line reason — what's still unresolved or missing. The user can't help close the gap if they don't know what's missing.

## Question format

```
Q:      <one focused question — ask exactly one thing>
SOURCE: <section heading or domain rule that triggered this — "AC-3", "glossary: 'cancellation'", "no non-goals listed">
GUESS:  <your hypothesis for the answer, and the reasoning behind it>
```

Why attach a guess: the user reacts faster to a wrong guess than they generate an answer from scratch. It commits you to a hypothesis you can be visibly wrong about, which keeps you honest and accelerates the session.

Never batch questions. The third question often depends on the answer to the first; asking them all at once locks in the wrong framing.

## Priority ladder

Ask in this order — hardest gaps first:

1. **Domain language violations** — any term in the artefact that conflicts with or is absent from `docs/domain/glossary.md`. Surface immediately: *"Your glossary defines 'X' as Y, but here you're using it to mean Z — which is it?"*
2. **Missing or vague acceptance criteria / test gates** — criteria that can't be falsified, or test gates described in prose rather than executable commands.
3. **Scope ambiguity** — non-goals not listed, or a scope boundary that could be read two ways.
4. **Dependency blindspots** — "what must already exist before increment N can start?" for any increment that references external state.
5. **Reversibility gaps** — any decision whose cost of reversal is high but hasn't been acknowledged: data migrations, public API surface, external contracts.
6. **User/persona misalignment** — "who is this actually for?" when the PRD references personas without linking them or specifying which bounded context's users.
7. *(implementation plans only)* — missing `Status: pending` fields, non-atomic increments (does more than one independently testable thing), non-executable test gates, missing `**Overall Status:**` or `**Current Increment:**` header.

## Domain vocabulary guard

When the user uses any term during the session:
- **In glossary, consistent** → proceed
- **In glossary, conflicts** → surface immediately (see priority 1 above)
- **New term, recurring** → propose a canonical name and offer to add it to the glossary via `domain-glossary`

The glossary is the single source of truth. Do not maintain a parallel in-session vocabulary list — resolve to the file or propose an addition.

## Stop condition

You are done when BOTH are true:
- Confidence ≥ 90%
- You can predict the user's reaction to the next three questions you would ask

**If convergence stalls:** if you've gone five or more rounds and confidence hasn't risen meaningfully, name it: *"I've asked N questions and my confidence is still at X%. Something foundational is missing or I'm asking the wrong questions — want to step back and reframe?"*

**Why 90% not 95%:** planning documents carry inherent residual ambiguity (implementation details not yet decided, external unknowns). Holding out for 95% risks infinite sessions on hard specs. 90% is the practical threshold for "safe to proceed."

## Red flags

- More than one question in a single message
- A question without SOURCE or GUESS attached
- Accepting "whatever you think is best" as a terminal answer — re-ask with two concrete options
- Producing a spec, plan, or task list before the Phase 2 restate is confirmed
- A sophistication-signalling answer passes unchallenged ("scalable", "clean", "robust") — probe: *"If you didn't have to justify this to anyone, what would you actually do?"*
- Logging an ADR that doesn't meet all three gates — check `references/adr-criteria.md` before logging
- Batching glossary patches or artefact edits to the end — apply immediately when the decision is live

## Interaction with other skills

- **`agent-peer-review`**: run first for static mechanical gaps; run `agent-grill-me` after for Socratic depth. They are complementary, not redundant.
- **`arch-adr`**: delegate ADR creation here when a decision passes the three-gate rule. Do not write raw ADRs outside that skill — it handles numbering, format, and file placement.
- **`domain-glossary`**: delegate glossary updates here when a term is sharpened. Do not patch `docs/domain/glossary.md` directly outside that skill's conventions.
- **`plan-implementation`**: if grilling reveals the plan needs structural rebuilding (not just clarification), stop and recommend re-running `plan-implementation` with the resolved intent rather than patching in place.
