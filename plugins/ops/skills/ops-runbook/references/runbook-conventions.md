# Runbook Conventions

These rules apply to every runbook regardless of project. They are derived from what makes
operator-grade documentation actually usable under pressure.

---

## Structure

### Required sections (procedure type)

In this order:

1. `# Title` — imperative verb phrase, no trailing period
2. `## Overview` — 1–2 sentences, trigger condition + what it produces
3. `## Prerequisites` — table: Requirement | How to verify
4. Numbered steps: `## Step N — Name`
5. `## Step summary` — compact table for re-runs
6. `## Troubleshooting` — one `###` block per failure mode
7. `## Related Documents` — cross-links

### Optional sections

- `## When to use this vs. <alternative>` — when two runbooks cover overlapping territory
- `## Rollback` — if the procedure has a defined undo path
- `## Scheduling` — if the procedure is run on a schedule

---

## Commands

### Copy-paste ready

Every command must run as written. No mental assembly. No "replace X with your value".

**Wrong:**
```bash
paracel ls ingest --dir <your-input-dir>
```

**Right:**
```bash
# Get the predecessor version ID from Step 0 output
paracel ls ingest --dir /tmp/new_month_pair
```

### Placeholders

When a value is not known at write time, use `<SCREAMING_SNAKE_CASE>` and immediately follow
the command block with the source of that value:

```bash
paracel ls diff \
  --from-ls-version-id <PREDECESSOR_VERSION_ID> \
  --to-ls-version-id <NEW_VERSION_ID>
```

`PREDECESSOR_VERSION_ID` — from the pre-flight query in Step 0.
`NEW_VERSION_ID` — from the `ls_version_id` field in Step 2 output.

### Dry-run before destructive execution

Any command that supports `--dry-run`, `--check`, `--plan`, or an equivalent preview mode
must show the dry-run invocation before the real one:

```bash
# Preview: confirms exactly N items will be processed
<command> --dry-run

# Execute
<command>
```

---

## Step bodies

### Environment labeling

When a command differs between environments, use bold labels in the same step:

**Local:**
```bash
<local command>
```

**Staging:**
```bash
<staging-specific command>
```

Do not split environments into separate top-level sections — operators must be able to
follow one environment's full path without scrolling past the other.

### Expected output

Every step that modifies state (writes to DB, sends API request, restarts service, creates
files) must have a `### Expected output` subsection with a real sample.

**Rules for expected output blocks:**
- Use actual output from a real run, trimmed to the essential lines
- Show the success indicator (exit line, summary count, status field)
- Omit timestamps, run IDs, and noise unless they are part of the success signal
- If output varies by environment, show the most informative variant and note the difference

```
### Expected output

```
Ingest complete: 1 pair(s) processed
parse_ms=3032 insert_ms=7098 total_ingest_ms=10138
```
```

Never write:
- "Output varies" — find a representative sample
- "See logs for details" — extract the key lines here
- A blank `### Expected output` section

### Non-obvious choices

When a step makes a choice that would surprise a competent operator, explain it inline
with a `> **Why X:**` callout immediately after the command block and before
`### Expected output`:

```markdown
> **Why temp directory:** The ingest command has no duplicate guard — running it on a
> directory with already-ingested months will fail with a unique constraint violation.
> Isolating the new pair avoids this without modifying the source directory.
```

Do not collect these explanations in a "Notes" section at the end. The operator reads
linearly and needs the context at the moment the choice appears.

---

## Warnings for destructive operations

### Placement: before, never after

A `> **Warning:**` block must appear *before* the destructive command, not after it.

**Wrong:**
```bash
docker compose down -v
```
> **Warning:** This removes all named volumes including the database.

**Right:**
> **Warning:** The following command removes all named volumes including the database.
> Ensure you have a recent backup before proceeding.

```bash
docker compose down -v
```

### What counts as destructive

- Deletes, drops, wipes, truncates, prunes
- Restores that overwrite existing data (`pg_restore --clean`)
- Force pushes or branch deletions
- Cache purges that cannot be recovered
- External API calls with side effects (sends email, charges account, triggers deploy)

---

## Troubleshooting entries

Each `###` entry covers one distinct failure mode:

```markdown
### <Short symptom title (5–8 words)>

**Symptom:** <Exact error text or observable behavior. Quote the error message if there is one.>

**Cause:** <Root cause. What went wrong in the system.>

**Fix:**

```bash
<exact resolution command>
```
```

### What to document

Document only:
- Failure modes observed during real runs (from conversation history or incident logs)
- Failure modes that are structurally guaranteed (unique constraint when duplicate input
  is possible; connection refused when a service is healthy-checked before use)

Do not invent hypothetical failures. Generic advice ("check your logs", "ensure the
service is running") belongs in the system's primary docs, not here.

---

## Tables

### Left-align all column headers

```markdown
| Column | Column |
|:-------|:-------|
```

Not:
```markdown
| Column | Column |
|--------|--------|
```

### Prerequisites table format

| Requirement | How to verify |
|:------------|:-------------|
| Description of what must be true | `copy-paste command` |

The `How to verify` column must be actionable — a command, a URL to check, a file path to
inspect — not a description.

---

## Related Documents

Use a consistent separator. Discover which one is in use in the project's existing runbooks
(commonly `--`). Example:

```markdown
## Related Documents

- [Title](relative/path.md) -- one-line description of what it covers
- [Title](relative/path.md) -- one-line description
```

Cross-link bidirectionally: add the new runbook to the Related Documents of each linked file.

---

## Formatting rules

| Rule | Do | Don't |
|:-----|:---|:------|
| Emojis | Never | Never |
| Bold for labels | **Symptom:** **Cause:** **Fix:** **Local:** **Staging:** | Sparingly elsewhere |
| Inline code | For commands, file paths, flag names, output values | For prose |
| Callout style | `> **Why X:**` and `> **Warning:**` | `> Note:` `> Info:` |
| Step numbering | Sequential integers: Step 1, Step 2 | Step A, Step I, "First" |
| Sub-steps | Step 3a / Step 3b only when inseparable | Avoid — split into separate steps |
| Section depth | H2 (`##`) for top-level, H3 (`###`) for subsections | H4 or deeper |

---

## Step summary table

The step summary is the quick-reference card for operators re-running the procedure.
Place it after all steps, before Troubleshooting.

```markdown
## Step summary

| # | Step | Local | Staging |
|:--|:-----|:------|:--------|
| 1 | Isolate files | `cp files /tmp/new/` | `scp + docker cp` |
| 2 | Ingest | `paracel ls ingest --dir /tmp/new` | `docker compose exec api paracel ...` |
```

If only one environment applies, drop the extra column.
Keep commands short in this table — full form lives in the step body.
