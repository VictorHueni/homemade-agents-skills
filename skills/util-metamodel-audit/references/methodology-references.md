# Methodology References — util-stack-audit

Internal reference. Not copied to projects. Explains the rationale behind each audit check category.

---

## Why audit documentation stacks?

**Link rot** degrades documentation faster than content staleness. A study of web links showed ~25% decay per year (Koehler, 2004). Internal documentation links decay even faster as files are renamed, moved, or deleted during active development. Automated link checking is the minimum viable quality gate.

**Dependency drift** — the gap between what a document claims its prerequisites are and what actually exists — silently corrupts the traceability chain. A PRD referencing `E-04` when `E-04` doesn't exist in the epic catalogue is a ghost dependency. The audit enforces the DAG defined in `rules/metamodel.md`.

**Hypothesis expiry** is the most insidious decay mode. A persona created as a proto-persona in Q1 with a 90-day review date becomes a stale assumption in Q2 — but teams continue designing to it because nothing flags it as expired. Lean UX (Gothelf, 2013) identifies this as a primary failure mode of assumption-driven design.

---

## Sources by check category

| Check | Primary source |
|---|---|
| §1 Stack progress | `rules/metamodel.md` — canonical 11-step build order |
| §2 Folder placement | `rules/metamodel.md` — canonical output paths table |
| §3 Internal links | Practitioner discipline; CommonMark link resolution spec |
| §4 External links | SCIP (Strategic and Competitive Intelligence Professionals) — link verification cadence; Koehler (2004) link decay research |
| §5 ID cross-references | BABOK §10.22 Functional Decomposition — traceability discipline; TOGAF Series Guide — artefact ID stability |
| §6 ID integrity | Practitioner discipline — ID collision = single point of failure for all cross-references |
| §7 Dependency enforcement | `rules/metamodel.md` DAG hard rules |
| §8 _TODO_ density | Practitioner discipline — completeness visibility |
| §9 Mandatory sections | Per-skill SKILL.md checklist sections (the skills define what's mandatory for their artefact) |
| §10 Methodology pointers | Kit convention — single source of truth for bibliographies |
| §11 Confidence distribution | Strategyzer (Osterwalder, 2010) — Assumed/Tested/Validated confidence discipline; Lean Startup (Ries, 2011) — validated learning |
| §12 Expiry + staleness | Lean UX (Gothelf, 2013) — proto-persona validate-or-retire (≤90 days); SCIP — competitive intelligence refresh cadence (90–180 days) |
| §13 Orphaned files | Practitioner discipline — unreferenced files are invisible; invisible = unmaintained |
| §14 Research sync | BABOK §10.25 Interviews — findings must flow back into the artefacts that motivated the research |
| §15 ADR chains | MADR (Michael Nygard, 2011) — supersession records must be bidirectional to preserve decision history |
| §16 Delivery progress | Practitioner discipline — FBS status + epic ↔ PRD coverage as a proxy for delivery completeness |
| §17 Frontmatter validity | `rules/artefact-frontmatter.md` — canonical OKF-superset schema (6 OKF fields incl. required `type`, + kit lifecycle fields) + conditional supersession fields + OKF reserved-file handling (`index.md`/`log.md`, root `okf_version`); staleness depends on `last_reviewed` + `review_interval` |
| §18 Open items governance | `rules/open-items-governance.md` — single source of truth for the central ledger as sole authoring surface, taxonomy, lifecycle, and schema. Schema compliance enforces §4. Source-location provenance enforces §4 (`Source anchor` + `Source heading` is the provenance pair, filed directly at row-creation time). Closure drift enforces §3 (closure must be evidenced via `Tracker ref`). Stale open items surface §3 lifecycle staleness without auto-closing — re-triage stays operator-driven via `util-open-items` |
