---
type: rule
---

# Session handoff — pointer

When a session's context is overloaded (rule of thumb: 40–60% context at a semantic
boundary), hand off to a fresh session with the **`agent-handoff` skill** instead of relying
on auto-compaction. Handoff documents live at `var/handoffs/<workstream-slug>/NN-<date>-<slug>.md`
in the project being worked on, with a `var/handoffs/LATEST` pointer to the most recent one.

To resume interrupted work, invoke `agent-handoff` in resume mode — it locates the handoff
(argument path, else `var/handoffs/LATEST`), warns on repo drift against the recorded branch
and HEAD sha, and re-verifies inherited claims before continuing.

This is passive routing knowledge only: nothing here scans for a handoff at session start or
triggers `agent-handoff` automatically — the skill is invoked explicitly, either by the
operator pasting the resume prompt a prior session ended with, or by asking to resume a
workstream.
