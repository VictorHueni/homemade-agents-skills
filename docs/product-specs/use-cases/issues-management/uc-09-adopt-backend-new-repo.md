---
type: Use Case
title: "UC-09 — Adopt the backend on a new repo"
description: "The operator installs the github open-items backend on a fresh repo in the checklist's strict order — labels first, then intake surface, then verification commands, then the backend declaration."
tags: [open-items, adoption, bootstrap, github-backend]
timestamp: "2026-07-20T15:30:00Z"
status: draft
owner: "Victor Hueni"
last_reviewed: "2026-07-20"
review_interval: 180d
---

# UC-09 — Adopt the backend on a new repo

> Casual format (Cockburn). Promote to fully-dressed without re-numbering when the goal earns it. Methodology: kit `spec-use-case/references/methodology.md`.

| **Scope** | system | **Level** | user-goal 🌊 | **Primary Actor** | Operator | **Realises** | _TBD_ (contract lives in `util-open-items/SKILL.md` §Backends — github adoption checklist) |
|---|---|---|---|---|---|---|---|

**Main scenario.** The Operator wants a new repo's issue tracker to become its
open-items ledger, and follows the adoption checklist in its stated order — the
order is load-bearing. **First**, they bootstrap the 17-label vocabulary onto the
repo (`bootstrap_labels.sh --apply`), because every later surface names those labels
and the tracker silently skips labels that do not exist. **Second**, they install
the intake surface: the five per-type issue forms, the chooser configuration that
disables blank issues, and the labeler workflow that mirrors the priority/size
answers to labels. **Third**, they ensure the repo's `CLAUDE.md` carries a
verification-commands section (build/test/lint) — the single biggest measured driver
of agent success on delegated issues. **Fourth**, they declare the backend by
writing `backend.yml` with `backend: github` and the repo coordinates. When it
succeeds, humans file through typed forms (UC-02), agents file through the sync
contract (UC-03), triage and execution operate on labels alone, and the tracker is
the repo's single live backlog from day one.

**Alternate paths.**

- Forms are installed before the labels exist → the ordering trap: submissions
  "work" but the tracker silently drops the forms' `type:`/`needs-triage` label
  entries, so issues arrive unclassified with no error anywhere. Fix by
  bootstrapping the labels, then re-labelling the orphaned issues.
- `CLAUDE.md` has no verification-commands section → adoption still functions, but
  delegated executions (UC-06) measurably under-perform: agents cannot prove their
  changes, so PRs arrive unverified. Treat step 3 as required, not optional.
- The checklist is re-run (fully or partially) → safe: the label bootstrap is
  idempotent (it creates-or-updates, never duplicates) and re-copying the templates
  overwrites in place, so a repair run converges instead of compounding.
- The repo already has a legacy backlog (a TODO list or a markdown ledger) →
  complete this checklist first, then convert through UC-10 rather than letting two
  sources of truth coexist.
- The repo wants external contributors filing issues → add the conventional
  duplicate-search checkbox to the forms at that point (deliberately omitted while
  all filers are contract-bound — ADR-0009 §4).
