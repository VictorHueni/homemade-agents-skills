---
type: Use Case
title: "UC-05 — Deduplicate and merge issues"
description: "A coding agent clusters duplicate issues, proposes canonical/duplicate pairs, and — only after operator approval — merges context onto the canonical issue and closes duplicates with a recorded rationale."
tags: [open-items, deduplication, merge, github-backend]
timestamp: "2026-07-20T15:30:00Z"
status: draft
owner: "Victor Hueni"
last_reviewed: "2026-07-20"
review_interval: 180d
---

# UC-05 — Deduplicate and merge issues

> Methodology: see the kit's `spec-use-case/references/methodology.md` (Cockburn fully-dressed format). Do not restate the method here.

| Field | Value |
|---|---|
| **Scope** | system — the backlog-execution system (github open-items backend + `agent-issue-loop` Family B) |
| **Level** | user-goal 🌊 |
| **Primary Actor** | Coding Agent (operator-gated — every merge requires explicit approval) |
| **Supporting Actors** | Operator (approval authority); GitHub (issue tracker) |
| **Realises** | _TBD_ (contract lives in `agent-issue-loop/SKILL.md` Family B) |

## Stakeholders and Interests

- **Operator** — one conversation per problem: duplicate issues stop splitting context,
  votes, and effort across copies; and nothing is merged or closed behind their back.
- **Coding Agents** — the queue never offers the same work twice, so two sessions
  cannot independently implement the same fix.
- **Future maintainers** — a closed duplicate always says *why* it closed
  ("Duplicate of #N") and its unique context survives on the canonical issue —
  nothing is lost to the merge.

## Preconditions

- The repo runs the `github` open-items backend (ADR-0009 vocabulary).
- The agent can read the open issue set and write comments/labels/closures.
- An Operator is available to approve or reject the proposed pairs — this use case
  never runs unattended to completion.

## Guarantees

- **Minimal guarantees** (hold even on failure or abandonment): no issue is closed
  without the Operator's approval of its specific pair; no issue is closed without its
  rationale recorded; no information is deleted — the duplicate's unique context is
  preserved before its closure, or the closure does not happen; unapproved and
  rejected pairs are left untouched.
- **Success guarantees**: every approved pair is merged — the canonical issue carries
  any unique context from the duplicate, both issues cross-reference each other, and
  the duplicate is closed as not planned with "Duplicate of #N" recorded;
  near-duplicates are cross-linked, not closed; the Operator receives a report of what
  was merged, cross-linked, and skipped.

## Trigger

The Operator requests a deduplication pass, or a triage session (UC-04) flags a
duplicate cluster it will not disposition itself.

## Main Success Scenario

1. The Operator asks the Coding Agent to deduplicate the open backlog.
2. The agent scans the open issues and clusters duplicate candidates two ways: by the
   identity triple (source artefact, source anchor, summary fingerprint) where
   provenance sections exist, and by semantic similarity of title, body, and
   resolution path where they do not.
3. The agent proposes a duplicate-pairs table: for each pair, the **canonical** issue
   (the older one, or the one with richer context), the duplicate, the evidence for
   the match, and the merge plan. Near-duplicates — related but distinct — are listed
   separately with a cross-link proposal (`Relates to #N`) instead of a merge.
4. The Operator reviews the table and approves the pairs to merge (amending canonical
   choices where the agent picked wrong).
5. For each approved pair, the agent preserves the duplicate's unique information —
   provenance, context, links not already on the canonical — as a comment on the
   canonical issue.
6. The agent cross-references the two issues so each points at the other.
7. The agent closes the duplicate as **not planned** with the rationale
   "Duplicate of #N" recorded on it.
8. The agent applies the approved cross-links for near-duplicates and reports what was
   merged, what was cross-linked, and the resulting open-issue count.

## Extensions

- **2a.** The scan finds no duplicate candidates:
  - **2a1.** The agent reports the clean result (and any near-duplicates worth
    cross-linking); the use case ends successfully with nothing mutated.
- **3a.** A candidate pair is related but not the same work (shared subsystem,
  different goal):
  - **3a1.** The agent classifies it as a near-duplicate: it proposes only a mutual
    cross-link, never a merge — closing distinct work as a duplicate destroys a valid
    backlog item.
- **4a.** The Operator rejects a proposed pair:
  - **4a1.** Both issues stay open and untouched. The agent records the rejection in
    its report so the next pass does not re-propose the identical pair unchanged.
- **4b.** The Operator overrides the canonical choice (prefers the newer, richer
  issue):
  - **4b1.** The merge runs with the Operator's canonical; the direction of steps 5–7
    flips accordingly.
- **5a.** The duplicate contains no unique information (a strict subset of the
  canonical):
  - **5a1.** The agent skips the preservation comment, states so in the report, and
    proceeds to steps 6–7.
- **7a.** The closure write fails (API error, issue changed mid-flight, permissions):
  - **7a1.** The agent leaves the duplicate open, reports the failure with the pair
    listed as unfinished, and never records the pair as merged — an unevidenced or
    half-applied closure is worse than a surviving duplicate.
- **7b.** The duplicate carries a `state:in-progress` label (someone is working it):
  - **7b1.** The agent does not close it. It flags the pair for the Operator to
    resolve with the worker — merging live work is a human call.

## Technology and Data Variations

- Step 2: the identity-triple match comes from the `util-open-items` de-duplication
  policy (≥80% summary overlap plus a matching provenance half); semantic clustering
  is the fallback for tracker-native issues without provenance sections.
- Step 7: closure uses the drop contract (`gh issue close --reason "not planned"` +
  rationale comment) so the evidence is structural, exactly as UC-04's staleness drops.

## Related Information

- Contract: `agent-issue-loop/SKILL.md` Family B (action budget: only approved pairs,
  always a rationale, never delete content); de-duplication policy:
  `util-open-items/SKILL.md` §De-duplication.
- Prevention beats cure: UC-03's mandatory pre-creation search is what keeps this use
  case rare; this flow catches what slips through (parallel sessions, human filings).
- Triage (UC-04 extension 2b) hands duplicate clusters here rather than dispositioning
  them itself — one flow owns merge semantics.

## Use-Case 2.0 Slices

| Slice | Narrative | Test case(s) | Status |
|---|---|---|---|
| UC-05.S1 | Basic flow: pair proposed → approved → context preserved, duplicate closed "Duplicate of #N" | One seeded duplicate pair merged end-to-end | ⬜ |
| UC-05.S2 | Near-duplicate (3a): cross-link only, both stay open | Seeded related pair; assert links + both open | ⬜ |
| UC-05.S3 | Rejection (4a): pair untouched, rejection reported | Operator rejects; assert no mutation | ⬜ |
| UC-05.S4 | Closure failure (7a): duplicate left open, reported unfinished | Simulated failing close-write | ⬜ |
