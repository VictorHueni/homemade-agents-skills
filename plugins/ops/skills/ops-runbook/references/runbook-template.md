# Runbook Template — Procedure Type

Copy this template and fill each section. Delete sections that don't apply.
Remove all `[INSTRUCTION]` lines before saving.

---

# <Operation Title>

## Overview

[INSTRUCTION: 1–2 sentences. What does this procedure do, and when should an operator run it?
Lead with the trigger condition, not the tool. Example: "Run this after a new monthly data
publication is available. It ingests the new files, runs the detection pipeline, and updates
the search index."]

## Prerequisites

[INSTRUCTION: One row per requirement. The "How to verify" column must contain a copy-paste
command or a concrete check — not a description.]

| Requirement | How to verify |
|:------------|:-------------|
| <System or service is running> | `<copy-paste command that exits 0 if OK>` |
| <Access or credentials available> | `<command to confirm access>` |
| <Input files or data present> | `ls -lh <path>` |

## Step 1 — <Name>

[INSTRUCTION: One sentence of context if the step is non-obvious. Omit if the step title is
self-explanatory.]

[INSTRUCTION: If the command differs between environments, use labeled variants.
If only one environment applies, drop the labels.]

**<Environment A (e.g. Local)>:**

```bash
# Dry-run first if the command supports it
<command> --dry-run

# Actual execution
<command>
```

**<Environment B (e.g. Staging)>:**

```bash
<environment-specific command>
```

> **Why <choice>:** [INSTRUCTION: Add this callout only when a choice would surprise a reader.
> Example: "Running from a temp directory rather than the main inputs folder avoids colliding
> with already-ingested files — the ingest command has no duplicate guard."]

> **Warning:** [INSTRUCTION: Add this block — BEFORE the command — for any step that deletes,
> drops, wipes, overwrites, or sends external requests with side effects. Never place it after.]

### Expected output

[INSTRUCTION: Paste real sample output, trimmed to the essential lines. The operator uses this
to confirm the step succeeded without reading full logs. Never leave this empty or write
"output varies".]

```
<sample output line 1>
<sample output line 2>
```

## Step 2 — <Name>

[INSTRUCTION: Repeat the Step 1 pattern for each subsequent step. Number sequentially.
Use sub-steps (2a, 2b) only when two commands must run in a specific order within the same
logical step and separating them into distinct steps would break the narrative flow.]

## Step N — Verify

[INSTRUCTION: The final step is always a read-only verification. Show the command and what
a healthy result looks like. This step is the gate: if it passes, the procedure is done.]

```bash
<verification command>
```

### Expected output

```
<what a healthy result looks like>
```

## Step summary

[INSTRUCTION: This table is the quick-reference card for re-runs. One row per step.
If multiple environments apply, add a column per environment. Keep commands short — use
the full form in the step body above.]

| # | Step | <Environment A> | <Environment B> |
|:--|:-----|:----------------|:----------------|
| 1 | <Name> | `<short command>` | `<short command>` |
| 2 | <Name> | `<short command>` | `<short command>` |
| N | Verify | `<verify command>` | `<verify command>` |

## Troubleshooting

### <Short symptom title>

**Symptom:** <Exact error text or observable behavior. What the operator sees on screen.>

**Cause:** <Root cause. What went wrong in the system, not just "an error occurred".>

**Fix:**

```bash
<exact command to resolve the issue>
```

[INSTRUCTION: Repeat one ### block per distinct failure mode. Only document:
- Failure modes observed in practice
- Failure modes structurally guaranteed by the system (e.g., unique constraint violations
  when a duplicate is possible)
Do not invent hypothetical failures.]

## Related Documents

[INSTRUCTION: Link every document an operator would need if they get stuck.
Use the separator style already in use in existing runbooks (commonly `--`).
Add this runbook to the Related Documents section of each linked file.]

- [<Title>](<relative-path>) -- <one-line description of what it covers>
