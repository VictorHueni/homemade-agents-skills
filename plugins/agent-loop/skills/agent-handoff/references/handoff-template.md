# Handoff template

The canonical structure for a `var/handoffs/<workstream-slug>/NN-<date>-<slug>.md` document.
All nine sections are required and appear in this order. `scripts/validate-handoff.py`
(added in a later increment of this skill) enforces presence, order-independent, and
non-trivial population at write time — a handoff that fails the validator is not finished.

**Anti-padding note:** shorter is better. A handoff is a router to the next session's
attention, not an archive of everything discussed. If a section has nothing to say, write
the shortest true statement ("none identified") rather than restating adjacent sections to
fill space. Target budget is ≤ ~200 lines total, enforced by the validator's
`--max-lines` check.

## Header

Before the first `##` section, record:

```markdown
# Handoff: <workstream title>

**Date:** <ISO 8601 date>
**Branch:** <git branch name>
**HEAD sha:** <full 40-char `git rev-parse HEAD`>
**Approx. context used:** <NN>%
**Chain:** <workstream-slug> — NN of ?
```

This is the drift-check anchor: `resume` mode diffs the recorded branch/sha against the
current repo state before trusting anything below it.

## `## Goal`

The immutable objective — what the work is *for*, not what's been done so far. Should not
need editing across a chain of handoffs on the same workstream; if the goal itself changed
mid-work, say so explicitly and note the prior goal.

## `## Approach & key decisions`

The chosen approach and *why*, including rejected alternatives and why they were rejected.
This is the section a fresh session most needs to avoid re-litigating settled tradeoffs.
State the decision, not the discussion that produced it.

## `## State`

Three explicit buckets — `Done`, `In progress`, `Remaining` — as short bullet lists. `In
progress` should name the exact point execution stopped at (not "working on X" but "X: step
3 of 4 done, step 4 blocked on Y").

## `## Files`

Pointers only — file paths, line ranges, ADR/issue IDs — never pasted file content. The
fresh session has full filesystem access; the handoff's job is to say *where to look*, not
to duplicate what `Read` can retrieve. This is the router-not-archive rule: a handoff that
pastes code or long excerpts has failed its purpose and will drift from the file it copied.

## `## Verification`

What test gates, commands, or manual checks confirm the current state, and their last known
result. Evidence over prose: paste the actual failing test output or command exit status,
not a summary like "the tests are failing." A fresh session re-runs the command to confirm,
but the recorded evidence tells it what to expect.

## `## Dead ends — do not retry`

Approaches tried and abandoned, with the reason each failed. Required non-empty — use the
literal text `none` if genuinely nothing was tried and abandoned. This section exists
specifically to stop a fresh session from burning a turn rediscovering a dead end the prior
session already paid for.

## `## Constraints & gotchas`

Split explicitly into two groups:

- **Verified facts** — things directly confirmed this session (a command was run, a file was
  read, a value was checked) and can be trusted without re-verification.
- **Hypotheses / open questions** — things assumed, inferred, or not yet confirmed. Mark
  these clearly; `resume` mode treats every item here as unverified until re-checked
  (trust-but-verify), so an item wrongly filed as "verified" defeats that check.

## `## Suggested skills`

Skills (by name) the next session will likely need to invoke to continue the work, if any
are known from this session's context. Omit or write "none identified" if no specific skill
applies beyond general-purpose work.

## `## Next step`

A single first action, stated as one imperative sentence ("Run the validator against the new
fixture and fix the reported line."). Not a list, not a plan — the one thing the fresh
session should do first. `scripts/validate-handoff.py` checks this section starts with an
imperative verb.
