# Triage Rules — Operator Playbook

Reference for `util-open-items triage` mode. Triage proposes changes; it never mutates
the source artefact or the ledger silently. Every triage finding is operator-reviewable.

The lifecycle, schema, and taxonomy live in
the `metamodel` skill's `references/open-items-governance.md`. This file is the
day-to-day playbook for keeping the central ledger at
`docs/project-control/open-items/open-items.md` healthy.

---

## 1. What triage looks at

Triage scans every row in the live ledger that is in state `open`, `in-progress`, or
`blocked`. Terminal rows (`closed`, `dropped`) are out of scope — they are handled by
`archive` mode.

For each in-scope row, triage evaluates the four signals below and produces a finding
classified as `info`, `warn`, or `escalate`. Findings roll up into a triage report at
`var/reports/open-items/triage-YYYY-MM-DD.md` (or in-line if the operator does not ask
for a file).

---

## 2. Signal 1 — De-duplication

A row is a candidate duplicate of another ledger row when ALL of the following match:

1. `Source artefact` is identical (after rename normalisation).
2. `Source anchor` is identical OR `Source heading` is identical.
3. `Summary` shares ≥80% lexical overlap with the other row (case-insensitive,
   whitespace-normalised) OR both rows reference the same `Resolution path`.

Finding:

- **`escalate`** — both candidate rows are active (`open`, `in-progress`, `blocked`).
  Proposal: merge by dropping the newer `OI-NNNN` with `Resolution path: "Duplicate of
  OI-XXXX"` and `Tracker ref` pointing at the discussion link.
- **`warn`** — one candidate is terminal but lingering. Proposal: link the active row's
  `Resolution path` to the terminal row's `OI-NNNN` for context.

De-duplication is the highest-value triage signal because duplicate rows split owner
attention and double the apparent backlog.

---

## 3. Signal 2 — Ownerless rows

A row with `Owner: _TBD_` indicates that no one has been asked to resolve it.

Finding:

- **`warn`** when `_TBD_` persists for >14 days from the row's first appearance in the
  ledger (use the row's earliest synced timestamp; if not tracked, fall back to
  `Due / Review date` minus the artefact default of 30 days).
- **`escalate`** when `_TBD_` persists AND `Priority` is `high` or `critical`.

Proposal: name a candidate owner inferred from the source artefact's frontmatter `owner`
field. The operator approves or overrides.

---

## 4. Signal 3 — Stalled high-priority rows

Rows in `Priority: high` or `Priority: critical` with no `Tracker ref` movement signal
that the work has not progressed toward closure.

Heuristics:

- `Tracker ref: _TBD_` is the strongest signal — nothing has been opened.
- A non-`_TBD_` tracker ref pointing at a PR / ADR / plan increment that has been idle
  (no commits, no comments) for >14 days is the secondary signal. This requires the
  operator to check the linked tracker; the skill flags the candidate but cannot verify
  remote-tracker state itself.

Finding:

- **`escalate`** when `Priority` is `critical` and the row has been `open` for >7 days
  without `Tracker ref` movement.
- **`warn`** when `Priority` is `high` and the row has been `open` for >14 days without
  `Tracker ref` movement.

Proposal: surface the row in the triage report's "Escalation candidates" section with
its age and current owner. Recommend opening a tracker ref (PR / ADR / plan increment)
or downgrading priority with rationale.

---

## 5. Signal 4 — Blocked rows without exit criteria

Rows in `Status: blocked` should always state what they are blocked on in
`Resolution path`. A blocked row with no external dependency named is effectively
abandoned.

Finding:

- **`warn`** when `Status: blocked` and `Resolution path` does not name an external
  dependency (decision, evidence, third party).
- **`escalate`** when `Status: blocked` persists for >30 days without status change.

Proposal: prompt the operator to either (a) re-classify as `dropped` with a rationale,
(b) update `Resolution path` to name the blocker, or (c) escalate the blocker to the
relevant decision owner.

---

## 6. Priority assignment guidance

When the operator has to set or change `Priority`, use this rubric:

| Priority   | When to use                                                                                              |
| :--------- | :------------------------------------------------------------------------------------------------------- |
| `critical` | Blocks shipping a committed PRD, blocks a regulatory or security obligation, or blocks an active incident. |
| `high`     | Blocks the next quarter's roadmap, blocks an open ADR, or accumulates rapidly into tech debt if deferred. |
| `medium`   | Should be resolved within the next two review cycles; no immediate downstream blocker.                    |
| `low`      | Nice-to-have; resolve opportunistically. Frequent re-classification candidate for `dropped`.              |

Anti-patterns:

- **Everything is `high`.** Forces the operator to ignore priority; rebalance during
  triage by demoting at least one third of `high` rows per cycle.
- **`critical` rows that linger >7 days.** Either they are not actually critical
  (downgrade) or organisational follow-up is missing (escalate to the owning lead).

---

## 7. Owner assignment guidance

Use this order when proposing an owner during triage:

1. The `Owner` supplied when the row was filed, if any.
2. The `owner` frontmatter field of the source artefact.
3. The `Owner` of the closest related ledger row (same `Source artefact` and adjacent
   `Source anchor`).
4. `_TBD_` only as a last resort — and only when the triage report explicitly flags
   the row for owner assignment in the next cycle.

`Owner` is always a person, never a role or team — accountability cannot be diffused
without losing the close signal.

---

## 8. Reporting structure

A triage report (`var/reports/open-items/triage-YYYY-MM-DD.md`) contains:

```markdown
# Open Items Triage — YYYY-MM-DD

## Summary

- Rows scanned: N
- Escalations: N
- Warnings: N
- Infos: N

## Escalations

(table of escalation-class findings with OI-NNNN, signal, proposal)

## Warnings

(table of warn-class findings)

## De-duplication candidates

(merged proposals — pairs of OI-NNNN, recommended action)

## Owner assignment proposals

(rows with proposed owners derived from §7)

## Stalled high-priority rows

(rows surfaced by §4)
```

The report is read-only; acting on the proposals is always operator-driven through
`util-open-items sync`, `close`, `drop`, or direct artefact edits.

---

## 9. Cadence

Recommended invocation cadence (per the `metamodel` skill's `references/open-items-governance.md` §6 review cycle):

- **Weekly** for active development phases — keeps the backlog visible and prevents
  silent drift.
- **Bi-weekly** for steady-state maintenance phases.
- **Per milestone** as a hard checkpoint — every milestone exit should run triage and
  resolve all `escalate`-class findings before moving on.

`util-metamodel-audit` complements triage by reporting governance drift (missing
sections, schema violations, broken provenance) at a slower cadence (monthly or
quarterly). Triage handles operational health; audit handles structural compliance.
