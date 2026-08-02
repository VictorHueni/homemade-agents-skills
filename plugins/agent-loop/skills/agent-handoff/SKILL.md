---
name: agent-handoff
license: MIT
description: "Hand off an overloaded interactive session's context to a fresh session via a validated markdown handoff document. Two modes: create (write the handoff at var/handoffs/, end with a paste-ready resume prompt) and resume (load a handoff in a fresh session, check repo drift, re-verify inherited claims, continue the work). Triggers on: handoff, hand off context, context handoff, pass context to a new session, continue in fresh session, resume handoff."
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/validate-handoff.py *)
version: "1.0.0"
user-invocable: true
impact: "medium"
metadata:
  category: "agent"
  complexity: "medium"
status: active
last_reviewed: 2026-07-28
---

# Agent Handoff — session context handoff

## Overview

`agent-handoff` is the interactive-session complement to `agent-ralph-loop`. Ralph hands
work between fresh *iterations* of an autonomous loop; `agent-handoff` hands work between
fresh *sessions* of an interactive one, when the current session's context is running out
before the work is done. It writes a structured, validated markdown document that a new
session can read cold and continue from — without the operator re-explaining the task or
the new session re-discovering ground already covered.

The skill has two modes:

- **`create`** — run in the session that is running out of room. Writes a handoff document,
  validates it, and ends by printing a paste-ready resume prompt for the operator to give
  the next session.
- **`resume`** — run in the fresh session. Locates the handoff, checks the repo for drift
  since it was written, and re-verifies the claims it inherits before acting on them.

## Mode: create

Invoked from inside the session whose context is running low. Produces one handoff
document under the storage layout below, runs it through the write-time validator
(`scripts/validate-handoff.py`, added in a later increment of this skill), and only
finishes once the validator accepts the document. The final action is always printing a
paste-ready resume prompt — `create` mode cannot clear or restart the running session
itself; only the operator, in a new session, can do that.

### Create-mode procedure

1. **Derive the workstream slug.** If this session is continuing a workstream that already
   has a `var/handoffs/<workstream-slug>/` folder, reuse that slug and write the next `NN`
   in the chain (increment from the highest existing `NN`). Otherwise mint a new short
   kebab-case slug from the goal and start the chain at `01`.
2. **Write the document** following `references/handoff-template.md` — all nine sections,
   in order, router-not-archive, evidence over prose. Use `references/example-handoff.md`
   as the concrete reference for what "done" looks like.
3. **Record header provenance**: current date, `git branch --show-current`, full
   `git rev-parse HEAD`, and an approximate context-used percentage.
4. **Run the validator**: `python3 scripts/validate-handoff.py <path>`. Fix every reported
   finding and re-run until it exits 0 — a handoff the validator rejects is not finished.
5. **Update `var/handoffs/LATEST`** to point at the new path with status `unread`.
6. **Ensure `var/handoffs/` is gitignored** in the target project. If the project's
   `.gitignore` does not already exclude it, append `var/handoffs/` and tell the operator
   this was added — committing a handoff is an explicit per-file opt-in, never the default.
7. **End the turn** by printing a paste-ready resume prompt for the operator to give the
   next session, naming the handoff path (e.g. "Resume from
   `var/handoffs/<slug>/<NN>-<date>-<slug>.md` using the agent-handoff skill.").

## Mode: resume

Invoked from inside a fresh session that has no memory of the work described in the
handoff. Locates the relevant handoff document, compares its recorded branch and HEAD sha
against the current repo state to detect drift, and then treats every inherited claim as
unverified until re-checked against the current code — the same trust-but-verify posture
this skill's author applies to any prior-session analysis.

### Resume-mode procedure

1. **Locate the handoff.** Use the path the operator gave, if any. Otherwise read
   `var/handoffs/LATEST` and use the path it points to. If neither is available, ask the
   operator which handoff to resume.
2. **Drift check.** Compare the handoff header's recorded branch and HEAD sha against the
   current repo: `git branch --show-current` and `git rev-parse HEAD`. If they differ, run
   `git log --oneline <recorded-sha>..HEAD` to summarise what moved since the handoff was
   written, and list any files the handoff's "Files" section points at that also appear in
   that range — flag them as possibly stale. **Never hard-block on drift.** Warn, show the
   summary, and continue; the operator or the agent decides whether the drift matters.
3. **Trust-but-verify every inherited claim.** Before acting on anything the handoff states:
   - Re-read every cited `file:line` pointer in the "Files" section — don't act on the
     handoff's description of a file, act on the file's current content.
   - Treat everything in "Constraints & gotchas" marked as a hypothesis (as opposed to a
     verified fact) as still unverified; re-check it before relying on it.
   - Honour "Dead ends — do not retry" explicitly: do not re-attempt an approach listed
     there without first understanding why the prior session ruled it out.
4. **Act** on the "Next step" once drift is understood and the claims that gate it are
   re-verified.
5. **Mark the handoff consumed.** On successful resume, update `var/handoffs/LATEST`'s
   status field from `unread` to `consumed`. If the work continues past this session, note
   that the next `create` call extends the same chain (same workstream slug, next `NN`) —
   it does not start a new one.

## Timing guidance

Write the handoff proactively, not as a last resort:

- **40–60% of context used, at a semantic boundary** (an increment just finished, a
  question just answered, a subtask just closed) — the ideal window. Write mid-capacity,
  not empty-tank.
- **≥80% of context used** — write immediately even off a clean boundary; warn the operator
  that the session is degraded and the resulting handoff may be too. A handoff written from
  an overloaded session inherits that session's blind spots.

## Storage contract

Handoffs live under `var/handoffs/<workstream-slug>/NN-<date>-<slug>.md`:

- `<workstream-slug>` groups every handoff belonging to the same piece of work into one
  chain; `NN` is that chain's sequence number, starting at `01`.
- `var/handoffs/LATEST` is a single-line pointer (path + status) that `resume` mode reads
  by default when the operator does not name a specific handoff.
- `var/handoffs/` is **gitignored by default**. Handoffs are session-local working state,
  not repo history; committing one is an explicit opt-in the operator chooses per-handoff,
  never the skill's default behavior.

## Non-goals

This skill deliberately does not:

1. **Install any hook.** There is no `SessionStart` (or equivalent) wiring in v1 — the
   handoff is triggered explicitly by the operator or the model noticing context pressure,
   never by harness automation. Revisit only if a session is lost to surprise
   auto-compaction despite this skill existing.
2. **Scan for handoffs at session start.** Nothing in this skill runs unprompted; `resume`
   mode only acts when invoked.
3. **Auto-continue work.** `resume` mode re-verifies before acting; it never blindly
   replays the prior session's plan.
4. **Edit a project's `AGENTS.md`.** Passive routing knowledge (that handoffs exist and
   live under `var/handoffs/`) is carried by a kit rule file, not written per-project by
   this skill.
5. **Clear or restart the running session.** Only the operator can do that; `create` mode's
   job ends at printing the resume prompt.
