# Round-trip eval — agent-handoff

**Never in CI.** This lane needs two separate agent sessions and human-graded transcript
inspection; it is not mechanically pass/fail like `scripts/validate-handoff.py` or the pilot
`evals/evals.json` cases. Run it before a release of this skill and after any model upgrade
that could change how well an agent follows a handoff document (a resume-quality regression
won't surface any other way).

## Recipe

1. **Copy the fixture** into a scratch directory and `git init` it so it looks like a normal
   mid-task repo:

   ```bash
   d=$(mktemp -d)
   cp -r evals/roundtrip/fixture/* "$d"
   git -C "$d" init -q && git -C "$d" add -A && git -C "$d" commit -qm "seed" --allow-empty
   ```

2. **Agent A** works in `$d` starting from the state described in `REMAINING_STEP.md` and
   `DEAD_END.md`. Prompt it to fix the failing test, but interrupt it partway (before the fix
   lands) and ask it to invoke the `agent-handoff` skill in create mode. Do not let it finish
   the actual fix — the point is to hand off a genuinely incomplete task.
3. **Discard the session.** Agent A's context, chat history, and any state outside the handoff
   document + repo files must not carry over.
4. **Agent B** is a fresh session, given only the repo at `$d` (with agent A's edits, if any)
   and the handoff document's path. Prompt it to resume via the `agent-handoff` skill's resume
   mode and continue the work — nothing else.

## Grading (mechanical where possible)

- **Known next step completed:** `python3 -m pytest tests/ -q` in `$d` exits 0 — agent B
  actually applied the fix `REMAINING_STEP.md` describes, not a different one.
- **Documented dead end re-explored:** grep agent B's transcript for the abandoned approach
  named in `DEAD_END.md` (`_access_times`, "separate dict", "timestamp"-based tracking). A hit
  means agent B retried something the handoff explicitly said not to — a fail regardless of
  whether B eventually self-corrected.
- **Turns-to-first-correct-action:** count agent B's turns until it makes the first edit that
  moves toward the actual fix (`popitem(last=False)` or equivalent). Lower is better; record
  the number even when the eval otherwise passes, to track drift across runs.

## Reporting

Run **3 trials** (fresh `$d`, fresh agent A, fresh agent B each time) and report pass@3 — the
fraction of trials where the "known next step completed" and "documented dead end re-explored"
checks both pass. A single trial is not a compliance signal; agent behavior in trust-but-verify
resume flows varies run to run.
