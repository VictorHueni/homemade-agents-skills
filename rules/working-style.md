---
type: rule
---

# Working style preferences

## Default to sequential, not parallel plan execution

When laying out a multi-plan initiative, recommend a single critical path (e.g. `01 → 01b → 02 → 03a → 03b → 04`) even when plans are architecturally parallelisable.

- Architectural dependency graphs should still show *what is parallelisable* for completeness.
- The *recommended execution order* collapses parallel plans onto one critical path.
- When asked "which plans can run in parallel?" — answer architecturally, but note the sequential preference.
- Only suggest parallel phases if I explicitly opt in.

**Why:** I want a single thread of state to reason about. Parallel execution lets subtle dependency violations manifest as silent regressions when two plans land in non-deterministic order.

## Trust but verify prior-context claims

Before acting on any "fix X that was identified earlier" instruction — tracker entry, memory file, prior-conversation analysis, plan increment referencing a past state — verify the premise against current code first.

One of:

- `git grep -n "<symbol>" <src-dir>/` to verify production callers exist
- `Read` the cited file:line to verify the code matches the description
- `\d <table>` (psql) to verify schema state
- `git log --follow <file>` to see if the file was recently restructured

The verification costs < 1 minute; the cost of acting on a false premise is 15 min to several hours. Snapshots in time go stale silently — refactors and adjacent commits invalidate claims between writing and acting.

**Special case — workaround vs structural fix:** when a memory describes a *workaround* for a problem, ask whether the underlying problem still exists or was structurally fixed. Prefer routing structural issues to architectural fixes over papering over them.

**Anti-pattern in self:** finding myself drafting code to address an issue I have not yet verified is live. Stop, verify, then act — or discover the issue does not exist.

## Reuse the project's own automation — it is a probe, not just DRY

When a task needs an operation the project already automates (a Makefile target, a task-runner recipe, a script under `scripts/`), reach for the existing entry point before writing a fresh equivalent — even when the fresh one would be three lines and the existing one needs a wrapper.

The reason is not code duplication. A bespoke command is written against the *new* path's assumptions, so it satisfies them by construction and tells you nothing. The existing automation was written against the *old* path's assumptions, so pointing it somewhere new is what makes a stale assumption fail loudly. Reuse is the cheapest available test of whether the project's automation still means what it says.

**How to apply:** find the existing target first (`grep` the Makefile/taskfile for the verb, read the recipe end to end — not just its name). Then, before adopting it, check that its semantics actually match your case: what does it destroy, what does it assume is already running, what identity does each line resolve and by which mechanism. Where the semantics differ, adopt it anyway *with the constraint written down at the call site* rather than forking a private copy. Where a step is currently a bare copy-pasted command in prose or docs, that is a missing target — add it, so the next caller inherits the fix instead of the string.

**Watch for mixed resolution inside one recipe.** The highest-value defects this surfaces are lines that resolve the same identity by different mechanisms — one step going through the orchestrator (which reads its own env file) and the next through a raw CLI call (which reads the shell environment). While only one instance of the resource exists, both resolve to it and the inconsistency is invisible; introduce a second instance and the recipe operates on two different things mid-run. Guard such targets to fail closed on a mismatch rather than trusting the caller.

**Why:** the failure mode of the bespoke shortcut is silence — it works, ships, and leaves the latent defect armed for whoever next runs the real target. Measured case: reusing an existing dump/restore pair instead of hand-rolling the equivalent exposed a live cross-instance data-loss path in a recipe nobody had reason to suspect, because two adjacent lines disagreed about which instance they addressed. **Anti-pattern in self:** writing a small bespoke command because wiring up the existing target "needs a wrapper anyway" — the wrapper is the cheap part; the assumptions the existing target carries are the whole point.

## Wait for async propagation before deleting or retrying

When a change goes through a system that applies it asynchronously — DNS (especially DNSSEC-signed zones that re-sign on a schedule), CDN cache invalidation, certificate issuance, queue/worker processing, eventual-consistency stores — a write that the API reports as `success` but that is not yet observable downstream is usually **mid-propagation, not broken**. Wait and re-observe before mutating again.

**How to apply:** after a successful write, poll the downstream observable (e.g. `dig` against the authoritative source, not just the management API) on an interval for several minutes before concluding failure. Confirm whether the record/resource is actually *malformed* (read it back via a detail endpoint) versus simply *not yet published* (e.g. the zone serial / SOA has not bumped). Only delete-and-recreate when readback proves the stored value is wrong — never to "kick" a propagation delay.

**Why:** delete-and-recreate churn on a slow-applying system destroys the in-flight change, resets the propagation clock, and can leave a worse intermediate state (e.g. a half-formed CAA record briefly blocking cert issuance) — all to fix a problem that would have resolved itself in a few minutes. **Anti-pattern in self:** seeing a just-written record not yet visible via `dig`, assuming the write was malformed, and deleting it — when waiting one more cycle would have shown it propagate.

## Comment like a senior dev — intent and *why*, never narration or history

Write code comments the way a senior engineer does: sparingly, and only where they add signal the code itself cannot carry. A comment earns its place when it explains **intent, the *why*, a non-obvious algorithm or design decision, a tradeoff, an invariant, or a gotcha** — the things a reader cannot recover by reading the code. Match the surrounding file's comment density; do not out-comment the code around you.

**Do not write:**

- **Wordy / narrating comments** that restate what the next line plainly does (`// increment i`, `// loop over the users`, `// set the flag to true`). If the code already says it, the comment is noise that rots and lies as the code changes.
- **History / changelog comments in code** — `// was: X`, `// previously used Y, switched to Z`, `// changed 2026-… to fix …`, `// removed the old approach`, `// TODO(old)` tombstones. Code history lives in `git log`, commit messages, and ADRs — never inline. A comment describes the code **as it is now**, not how it got here. When you replace code, delete its comment too; do not leave a marker explaining what used to be there.

**How to apply:** before writing any comment, ask "does this explain *why*, or just *what*?" — keep the former, delete the latter. Prefer one crisp sentence on the reasoning over a paragraph narrating the mechanics. Never annotate a diff inside the code (that is what the commit message is for).

**Why:** high-signal intent comments are the only kind worth maintaining — they capture reasoning that would otherwise be lost. Wordy comments and inline history duplicate what the code and git already say, bloat the file, and drift out of sync until they actively mislead. **Anti-pattern in self:** annotating an edit with "// previously this did X" or narrating each line to show my work — the diff and the commit message already carry that; the code should read clean.

## Never hard-wrap markdown prose

Write markdown paragraphs, blockquotes, and list items as single long lines — no forced line breaks at ~80–90 characters.

**Why:** Hard-wrapped lines create noisy diffs, look like broken sentences when rendered, and get re-wrapped by editors anyway. Let the editor handle visual soft-wrapping; the file should have one line per logical paragraph.

**How to apply:** Applies to every markdown file — docs, reports, skill outputs, research notes. Tables and fenced code blocks are unaffected (they have their own line structure).
