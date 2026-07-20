---
type: Use Case
title: "UC-03 — File an issue as an agent"
description: "A coding agent files unresolved work into the tracker: mandatory duplicate and dependency search, atomic labels at creation, structured body sections — never self-promoting past needs-triage."
tags: [open-items, filing, sync, github-backend]
timestamp: "2026-07-20T15:30:00Z"
status: draft
owner: "Victor Hueni"
last_reviewed: "2026-07-20"
review_interval: 180d
---

# UC-03 — File an issue as an agent

> Methodology: see the kit's `spec-use-case/references/methodology.md` (Cockburn fully-dressed format). Do not restate the method here.

| Field | Value |
|---|---|
| **Scope** | system — the backlog-execution system (github open-items backend + `util-open-items` sync) |
| **Level** | user-goal 🌊 |
| **Primary Actor** | Coding Agent (LLM-driven session, e.g. Claude Code) |
| **Supporting Actors** | GitHub (issue tracker); the calling skill/session that identified the work |
| **Realises** | _TBD_ (no FBS for the kit; contract lives in `util-open-items/SKILL.md` Mode 1) |

## Stakeholders and Interests

- **Operator** — the backlog stays one deduplicated conversation per problem: no
  second issue re-litigating an existing one, no context scattered across near-copies.
- **Triage authority** — the readiness axis stays trustworthy: nothing enters the
  delegation queue at filing time; every new issue arrives `needs-triage`.
- **Coding Agents (later sessions)** — every filed issue is queryable by labels alone
  (type, priority, size, readiness) with no body parsing, and carries its provenance
  back to the artefact that raised it.
- **Future maintainers** — related work is cross-linked at birth, so dependency chains
  are visible before anyone starts implementing.

## Preconditions

- The repo runs the `github` open-items backend (ADR-0009 label vocabulary
  bootstrapped, `backend.yml` present).
- The agent can read and write the repo's issue tracker.
- The item's fields are known: type, summary, priority, size, and — where the work was
  identified in an artefact — the provenance composite (source artefact, anchor,
  heading).

## Guarantees

- **Minimal guarantees** (hold even on failure): no duplicate issue is created — the
  search precedes any write; no issue is ever created carrying `ready-for-agent`; a
  failed write leaves the tracker unchanged and is reported, never silently swallowed.
- **Success guarantees**: exactly one new issue exists, labelled atomically at creation
  with one label per axis (mapped type, priority, size, `needs-triage`); its body uses
  the canonical section headings so the audit and the execution layer can parse it;
  related or blocking issues are linked in the body; the resulting `#N` is reported
  back to the caller.

## Trigger

A skill or agent session identifies unresolved work — while producing an artefact,
mid-implementation (UC-06 scope discovery), or as a central-only governance item — and
invokes the filing contract.

## Main Success Scenario

1. The Coding Agent assembles the item's fields: type, one-sentence summary, priority,
   size, resolution path, and provenance (or the central-only marker), plus any
   agent-execution fields (references, acceptance criteria, out of scope).
2. The agent validates the fields against the contract — the type is a legal taxonomy
   value, the provenance pair is complete or deliberately empty, readiness is left at
   its `needs-triage` default.
3. The agent searches the tracker for duplicates — by the identity triple (source
   artefact, source anchor, summary fingerprint) where provenance exists, and by
   summary otherwise — and confirms no existing issue already covers the item.
4. The agent searches for related or dependent open issues (same files, same
   subsystem, blocking work) and notes each as a cross-link (`Relates to #N` /
   `Blocked by #N`) for the body rather than duplicating their context.
5. The agent composes the issue body using the canonical section headings —
   provenance, `Resolution path`, `References`, `Acceptance criteria`,
   `Out of scope` — mirroring what the human forms produce.
6. The agent creates the issue with its labels applied atomically at creation: the
   governance type mapped to the standard vocabulary (§2a), `priority:p0..p3`,
   `size:S|M|L`, and `needs-triage`; the owner becomes the assignee where one is known.
7. The agent reports the resulting issue number `#N` back to the caller, which
   references it from then on.

## Extensions

- **2a.** The type is not a legal value (neither a governance taxonomy value nor a
  tracker-native type):
  - **2a1.** The agent refuses to file, names the legal values, and asks the caller to
    reclassify. Nothing is written.
- **2b.** The caller demands the issue be filed `ready-for-agent`:
  - **2b1.** The agent refuses that part: promotion is triage-owned (ADR-0008 §3) and
    filers never self-promote. It files at `needs-triage` (steps 3–7 proceed) and tells
    the caller the route to promotion — a triage pass, or `validate`'s drafted brief.
- **3a.** The search finds an existing issue that is a duplicate (identity triple
  matches, or the summaries clearly cover the same work):
  - **3a1.** The agent creates nothing. It reports the existing issue number to the
    caller so they reference it directly.
  - **3a2.** If the duplicate is genuinely arguable, the agent surfaces both readings
    and asks the caller to decide — reference the existing issue, or insist the item is
    distinct, in which case it files and flags the pair for the deduplication flow
    (UC-05) rather than deciding alone.
- **4a.** The search finds related-but-distinct issues (same subsystem, not the same
  work):
  - **4a1.** The agent proceeds to create the new issue and cross-links each relation
    in the body (`Relates to #N`, or `Blocked by #N` when the other issue must land
    first). Related is never a reason not to file — only duplicate is.
- **6a.** The tracker write fails (API error, permissions, network):
  - **6a1.** The agent stops, reports the failure and the fully-composed item back to
    the caller so nothing is lost, and does not retry into an unknown state — the
    caller re-invokes once the tracker is reachable.
- **6b.** A label the contract names does not exist on the repo (vocabulary not
  bootstrapped):
  - **6b1.** The agent reports the missing label and points at the adoption checklist
    (UC-09, bootstrap first); it does not file an issue that would silently lose its
    classification.

## Technology and Data Variations

- Step 1: the item may carry full provenance (identified inside an artefact), or be
  **central-only** — governance work with no artefact home, filed with the
  `_central-only_` heading marker and empty anchor/artefact (governance §5.2).
- Steps 3–4: the searches run as tracker queries (`gh issue list --search`); on the
  `markdown` backend the same contract searches the ledger table instead.
- Step 6: creation goes through `gh issue create` with `--label` applied in the same
  call — atomicity is what prevents a half-labelled issue from ever being observable.

## Related Information

- Contract: `util-open-items/SKILL.md` Mode 1 (`sync`), including the refusal rules;
  serialization: `util-open-items/references/github-backend.md` §2/§2a/§2b;
  vocabulary: kit ADR-0009 §5.
- The duplicate + dependency search is a **contract obligation, not a courtesy** — it
  is why the issue forms deliberately omit a duplicate-search checkbox (ADR-0009 §4):
  agent filings are trusted to have searched.
- Human filing of the same model is UC-02 (the per-type forms); this use case is the
  agent-side twin producing the same body sections and labels.

## Use-Case 2.0 Slices

| Slice | Narrative | Test case(s) | Status |
|---|---|---|---|
| UC-03.S1 | Basic flow: fields → search clean → issue created with atomic labels | One `sync` filing on the kit repo; labels verified one-per-axis | ⬜ |
| UC-03.S2 | Duplicate found (3a): existing `#N` reported, nothing created | Re-file a known item; assert no new issue | ⬜ |
| UC-03.S3 | Related-not-duplicate (4a): created with `Relates to #N` cross-link | File an item adjacent to an open issue; assert link in body | ⬜ |
| UC-03.S4 | Refusals (2a/2b): invalid type, demanded `ready-for-agent` | Both refusal paths exercised; tracker unchanged | ⬜ |
