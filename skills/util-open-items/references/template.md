# Open Items Ledger — Template & Worked Filing Example

This file shows the canonical ledger table skeleton and a worked end-to-end filing example
so an operator (or a future agent invocation) can reproduce the mechanics of `sync` mode
without reverse-engineering them from the live ledger.

The schema, taxonomy, and lifecycle live in
[`rules/open-items-governance.md`](../../rules/open-items-governance.md). This file is a
copy-pasteable template, not an independent definition.

---

## 1. Canonical ledger table skeleton

The live ledger at `docs/project-control/open-items/open-items.md` uses this header and
column order — the §4 schema, unchanged by backend:

```markdown
## Open Items

| OI-ID | Type | Summary | Source artefact | Source anchor | Source heading | Resolution path | Priority | Status | Owner | Due / Review date | Tracker ref |
| :---- | :--- | :------ | :-------------- | :------------ | :------------- | :-------------- | :------- | :----- | :---- | :---------------- | :---------- |

_None at present._ The ledger initialises empty; the first item filed by any skill will
populate it. Do not scaffold placeholder rows here — empty is the correct initial state
per §2 of the governance rule.
```

The same 12-column shape is used for every archive file under
`docs/project-control/open-items/archive/<YYYY-Q[1-4]>.md`.

---

## 2. Worked filing example

This example walks through one `sync` invocation end-to-end: a skill working on an
`arch-research` note identifies two unresolved questions and files them directly. The
central ledger starts empty.

### Before — central ledger

`docs/project-control/open-items/open-items.md`:

```markdown
## Open Items

| OI-ID | Type | Summary | Source artefact | Source anchor | Source heading | Resolution path | Priority | Status | Owner | Due / Review date | Tracker ref |
| :---- | :--- | :------ | :-------------- | :------------ | :------------- | :-------------- | :------- | :----- | :---- | :---------------- | :---------- |

_None at present._
```

### Invocations

```text
util-open-items sync --source-artefact docs/architecture/research/0003-token-auth.md \
  --source-anchor "#q3" --source-heading "Q3 — How do partners authenticate?" \
  --type decision-gap --summary "Auth model for partner API undecided" \
  --resolution-path "Open ADR on token strategy" --priority high --owner victor \
  --due 2026-06-15

util-open-items sync --source-artefact docs/architecture/research/0003-token-auth.md \
  --source-anchor "#q5" --source-heading "Q5 — What is the refresh-token threat model?" \
  --type doc-gap --summary "Threat model for refresh tokens absent" \
  --resolution-path "Extend research note §Threats" --priority medium --due 2026-07-01
```

### Filing mechanics (what the skill does, per invocation)

1. Validate `Type` against the four-value taxonomy; validate the row isn't filed already
   `closed`/`dropped` with `Tracker ref: _TBD_` (neither here — both are `open`).
2. Look up duplicates against the ledger — none found on the first call; the second call
   checks against the row the first call just created.
3. Mint the next ID: `OI-0001` for the first call, `OI-0002` for the second.
4. Append the row to the central ledger with `Source artefact`, `Source anchor`, and
   `Source heading` populated verbatim from the input.
5. Report the assigned ID back to the caller.

### After — central ledger

```markdown
## Open Items

| OI-ID   | Type          | Summary                                | Source artefact                                       | Source anchor | Source heading                                  | Resolution path                  | Priority | Status | Owner  | Due / Review date | Tracker ref |
| :------ | :------------ | :------------------------------------- | :---------------------------------------------------- | :------------ | :---------------------------------------------- | :------------------------------- | :------- | :----- | :----- | :---------------- | :---------- |
| OI-0001 | decision-gap  | Auth model for partner API undecided   | docs/architecture/research/0003-token-auth.md         | #q3           | Q3 — How do partners authenticate?              | Open ADR on token strategy       | high     | open   | victor | 2026-06-15        | _TBD_       |
| OI-0002 | doc-gap       | Threat model for refresh tokens absent | docs/architecture/research/0003-token-auth.md         | #q5           | Q5 — What is the refresh-token threat model?    | Extend research note §Threats    | medium   | open   | _TBD_  | 2026-07-01        | _TBD_       |
```

---

## 3. Worked close example

Continuing from the filing example above, the ADR has now been written and merged.

### Invocation

```text
util-open-items close OI-0001 --tracker-ref https://github.com/example/repo/pull/142
```

### Close mechanics

1. Locate `OI-0001` in `docs/project-control/open-items/open-items.md` and verify its current
   state is `open`, `in-progress`, or `blocked` (it is `open`).
2. Verify the supplied `--tracker-ref` is non-`_TBD_`.
3. Update the ledger row:
   - `Status: closed`
   - `Tracker ref: https://github.com/example/repo/pull/142`
   - `Due / Review date: 2026-05-25` (today, as the closure date).
4. Leave the row on the live ledger — it becomes archive-eligible in 30 days.

### After close — ledger row

```markdown
| OI-0001 | decision-gap | Auth model for partner API undecided | docs/architecture/research/0003-token-auth.md | #q3 | Q3 — How do partners authenticate? | Open ADR on token strategy | high | closed | victor | 2026-05-25 | https://github.com/example/repo/pull/142 |
```

---

## 4. Worked archive example

Thirty days after the closure above, the row becomes archive-eligible.

### Invocation

```text
util-open-items archive --older-than 30d
```

### Archive mechanics

1. Scan `open-items.md` for rows with `Status: closed` or `Status: dropped` and
   `Due / Review date` older than today minus 30 days.
2. Append eligible rows to `docs/project-control/open-items/archive/2026-Q2.md`, creating the
   file with the canonical 12-column header if it does not exist.
3. Only after the rows are persisted to the archive file, delete them from
   `open-items.md`.
4. Refresh the `§Status snapshot` block in `open-items.md` to reflect the new totals.

---

## 5. Field-by-field reference

The columns below are reproduced for operator convenience. The rule wins on every
conflict:

| Column              | Allowed values / format                                                                   |
| :------------------ | :---------------------------------------------------------------------------------------- |
| `OI-ID`             | Assigned at filing time: monotonic `OI-NNNN` (`markdown`) or the native issue number `#N` (`github`). Never recycled. |
| `Type`              | `doc-gap` \| `decision-gap` \| `execution-item` \| `tech-debt`.                            |
| `Summary`           | One-sentence statement of the open item. Self-contained.                                   |
| `Source artefact`   | Relative repo path to the source document, or the central-only scope marker (governance §5.2). |
| `Source anchor`     | Short fragment identifier (`#q3`, `#stage-onboarding`, `#vp-2`). Stable jump target.        |
| `Source heading`    | Full heading text the anchor resolves to. Readable provenance.                              |
| `Resolution path`   | What closing looks like (`Open ADR on token strategy`, `Schedule into refactor epic E-07`). |
| `Priority`          | `low` \| `medium` \| `high` \| `critical`.                                                  |
| `Status`            | `open` \| `in-progress` \| `blocked` \| `closed` \| `dropped`.                              |
| `Owner`             | Person accountable; `_TBD_` if unassigned.                                                  |
| `Due / Review date` | ISO 8601. For terminal states, the closure date.                                            |
| `Tracker ref`       | URL to resolving PR / ADR / plan increment / runbook / audit report; `_TBD_` while `open`. Mandatory for terminal states. |

---

## 6. Anti-patterns to refuse during sync

The `sync` mode refuses to act on:

- A row whose `Type` is not one of the four allowed values.
- A row whose `Status` is `closed` or `dropped` but whose `Tracker ref` is `_TBD_`.
- A row whose `Source anchor` and `Source heading` are supplied inconsistently — either
  both are present, or both are empty for a genuine central-only row (governance §5.2).
- A duplicate row where the caller's intent is unclear — report the existing ID and ask for
  confirmation rather than silently creating a second row.

When refusing, the skill prints the refusal reason + the conflicting row + a pointer to
the relevant section of `rules/open-items-governance.md`. It never partially files a row.
