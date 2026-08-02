---
name: agent-issue-loop
license: MIT
disable-model-invocation: true
description: "Work a GitHub-backend issue backlog as a coding agent: validate an issue's readiness (or sweep the ready queue for drift), find and merge duplicate issues, and take a ready-for-agent issue through implement → verify → PR. Triggers on: take issue #N, work the next ready issue, next issue, validate issue readiness, validate the queue, dedupe the backlog, merge duplicate issues, tackle open issues one by one."
disallowed-tools: AskUserQuestion
user-invocable: true
metadata:
  category: "agent"
  complexity: "high"
  version: "1.0.0"
  status: active
  last_reviewed: 2026-07-20
  impact: "high"
---

# Issue Loop — validate · dedupe · take

Operate the agent-execution layer of a repo's issue backlog (the `github` open-items
backend — kit ADR-0008/0009). Three mode families, each with its own action budget:

| Family | Modes | Writes? |
| :--- | :--- | :--- |
| **A. Validate** | `validate #N`, `validate --queue` | No — proposals only |
| **B. Dedupe** | `dedupe` | Only approved merges |
| **C. Execute** | `take #N`, `next` | The taken issue + its PR |

The label contract this skill operates against is normative in
`util-open-items/references/github-backend.md` (§2a type mapping, §2b execution layer):
`type:*` · `priority:p0..p3` · `size:S|M|L` · readiness (`needs-triage` /
`ready-for-agent` / `needs-human`) · `state:in-progress|blocked`. One label per axis.

**Boundary with `util-open-items`.** That skill owns filing, triage-session promotion,
close/drop semantics, and reporting. This skill *consumes* the queue triage produces:
`validate` is the per-issue / between-sessions readiness check, `dedupe` executes what
triage-style clustering only proposes, and `take`/`next` do the work. All closures this
skill causes route through the `drop`/`close` contracts (evidenced, reasoned), never a
raw unexplained `gh issue close`.

---

## The readiness precondition (shared by every mode)

An issue is *actually* ready for an agent iff (ADR-0008 §3):

1. `### Acceptance criteria` — non-empty, observable pass/fail items, ending in a
   verification command the agent can run.
2. `### References` — non-empty code pointers (files, symbols, prior PRs, patterns).
3. A `size:` label is set.
4. The title is a self-contained one-sentence summary; the body does not depend on
   context the agent cannot reach (external services, undocumented conventions).

`ready-for-agent` is a **guarantee, not a mood** — every mode defends it.

---

## Family A — Readiness validation (read-only)

### `validate #N`

Assess one issue against the precondition. Output a pass/fail report:

- **PASS** — each criterion confirmed, plus the verification command extracted.
- **FAIL** — the exact gaps, and for near-misses a **drafted brief** (proposed
  acceptance criteria + references, inferred from the issue text and the codebase) ready
  to paste into the issue. Drafting the brief is analysis, not mutation — applying it is
  the operator's (or a triage session's) call.

### `validate --queue`

Run the same assessment over every issue currently labelled `ready-for-agent`
(`gh issue list --label ready-for-agent --state open`). For each failure, propose
**demotion** to `needs-triage` citing the failed criterion. This is the between-sessions
drift check that keeps the queue trustworthy.

**Action budget (A):** no label changes, no comments, no edits — proposals only.
Promotion/demotion is applied solely with operator approval (or by a `util-open-items`
triage session).

---

## Family B — Duplication control & merge (operator-gated)

### `dedupe`

1. **Cluster.** Scan open issues; candidate duplicate pairs by (a) the identity triple
   `(source_artefact, source_anchor, summary fingerprint)` where provenance sections
   exist (the `util-open-items` de-duplication policy), and (b) semantic similarity of
   title / body / `### Resolution path` for issues without provenance.
2. **Propose.** Output a duplicate-pairs table: canonical issue (older, or richer
   context), duplicate, evidence, and the merge plan. Also list **near-duplicates**
   (related-but-distinct) with a proposal to cross-link (`Relates to #N`) instead of
   merging.
3. **Execute (only approved pairs).** For each approved merge:
   - Comment on the canonical issue with any unique information from the duplicate
     (provenance, context, links) — nothing is lost.
   - Cross-reference both issues.
   - Close the duplicate via the **drop contract**: `gh issue close --reason "not
     planned"` with rationale comment `Duplicate of #N`.

**Action budget (B):** touches only approved pairs; always closes with a rationale;
never deletes content; never merges without the operator's explicit approval of the
table.

---

## Family C — Implementation & verification

### `take #N`

1. **Gate.** Run the Family-A validation on `#N`. If it is not labelled
   `ready-for-agent` **or** fails the precondition: **refuse**, citing exactly what is
   missing (and where to get it — a triage session or `validate`'s drafted brief).
   Never talk yourself into taking a `needs-human` or `needs-triage` issue.
2. **Claim.** Swap the readiness label for `state:in-progress` (the ADR-0008 label
   handover); assign yourself if the harness supports it.
3. **Plan.** Read every file in `### References`; honour `### Out of scope` as a hard
   boundary; restate the acceptance criteria as the work's definition of done.
4. **Implement** on a feature branch, smallest coherent change that satisfies the
   criteria.
5. **Verify.** Run the acceptance criteria's verification command(s) plus the repo's
   CLAUDE.md verification commands (build/test/lint). Do not open the PR until they
   pass — if they cannot pass (criteria wrong, environment missing), stop, comment the
   findings on the issue, restore the readiness label, and report.
6. **PR.** Open a PR whose body cites the acceptance criteria checklist (checked) and
   contains `Closes #N`. Merge closes the issue with the PR as structural evidence; the
   closing flow removes the `state:` label.
7. **Blocked?** If genuinely blocked mid-flight (external dependency, missing decision):
   swap `state:in-progress` → `state:blocked`, comment the blocker, stop. Never grind.

### `next`

1. Query the delegation queue: `gh issue list --state open --label ready-for-agent`.
2. Pick by highest `priority:` (p0 → p3); tie-break by smallest `size:` (S → M → L);
   final tie-break: oldest.
3. Run `take` on the pick. If the queue is empty, say so and suggest `validate --queue`
   or a triage session — do NOT lower the bar by picking from `needs-triage`.

**Action budget (C):** one issue per invocation; touch only the taken issue, its branch,
and its PR; never promote any issue to `ready-for-agent`; never file a new issue without
the `util-open-items` duplicate + dependency search; scope changes discovered mid-work
are filed as new issues (via `util-open-items` sync), not silently absorbed.

---

## Operator examples

```text
agent-issue-loop validate 53          # readiness report + drafted brief if near-miss
agent-issue-loop validate --queue     # drift check over every ready-for-agent issue
agent-issue-loop dedupe               # duplicate-pairs proposal table
agent-issue-loop take 61              # gate → claim → implement → verify → PR "Closes #61"
agent-issue-loop next                 # pick highest-priority smallest ready issue, take it
```

## See also

- `util-open-items/SKILL.md` — filing (sync), triage v2 (promotion/staleness), close/drop.
- `util-open-items/references/github-backend.md` — the normative label serialization.
- Kit ADR-0008 (readiness contract) + ADR-0009 (standard vocabulary) in
  `docs/architecture/decisions/`.
