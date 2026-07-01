---
name: arch-adr
description: "Create, review, update, and supersede Architecture Decision Records (ADRs) using MADR 4.x conventions. Handles full ADR lifecycle including project bootstrap (init), new ADR creation with auto-numbering, supersession as an atomic two-file operation, and quality review. Use when asked to document an architecture/technical decision, initialise the ADR directory, supersede an older ADR, or improve ADR quality."
version: "1.1.0"
status: active          # draft | active | deprecated | superseded
last_reviewed: 2026-05-22
review_interval: 180d
supersedes: ~           # path to superseded skill version, if applicable
superseded_by: ~        # path to superseding skill, if this one is retired
user-invocable: true
allow_implicit_invocation: true
impact: "low"
metadata:
  category: "specification"
  complexity: "high"
---

# MADR ADR Decision

Use this skill to produce ADRs that are explicit, auditable, and easy to revisit.

## Workflow

1. Classify the request.

   - `Init`: bootstrap the ADR directory and write the first meta-ADR. → see **Init Mode**
   - `Create`: write a new ADR from scratch with auto-numbering. → see **Create Mode**
   - `Supersede`: replace an existing ADR — atomic two-file operation. → see **Supersede Mode**
   - `Update`: revise an existing ADR and keep decision history clear.
   - `Review`: audit an ADR and return findings plus a proposed rewrite. → see **Review Mode**

2. Auto-number every new ADR.

   - Run `find docs/architecture/decisions/ -name "adr-*.md" | sort` to list existing ADRs.
   - Next number = highest existing NNNN + 1, zero-padded to 4 digits.
   - Filename: `adr-{NNNN}-{slug}.md` where slug is the title lowercased with spaces replaced by hyphens.
   - Never reuse a number, even for superseded ADRs.

3. Apply repository conventions first, then MADR structure.

   - Check for a `CONVENTIONS.md` in the ADR directory. If present, follow its naming, scoping, and style rules exactly.
   - Default location: `docs/architecture/decisions/`.
   - If the repo already has ADR style/location conventions, preserve those while ensuring MADR-quality decision content.

4. Draft using `references/madr-templates.md`.

   - Use the full template for high-impact decisions.
   - Use the minimal template for small, localized decisions.

5. Validate quality with `references/adr-quality-checklist.md`.

   - Ensure one ADR contains one decision.
   - Ensure options, trade-offs, and consequences are explicit.
   - Ensure the chosen option is justified by decision drivers.

6. Finalize for traceability.

   - Ensure title and filename are stable and searchable.
   - Keep language specific; remove vague claims like "best" without criteria.

---

## Init Mode

Use when the project has no ADR directory yet, or when setting up ADRs for the first time.

**Steps — execute in order, do not skip:**

1. Check if `docs/architecture/decisions/` exists.
   - If it exists and contains ADRs, report what's there (count + list) and what the next number would be. Stop — no files to write.
   - If it exists but is empty, proceed to step 3.
   - If it does not exist, create it.

2. Write `docs/architecture/decisions/adr-0001-record-architecture-decisions.md`:

```markdown
---
type: Architecture Decision Record
title: Record Architecture Decisions
description: Establishes the use of ADRs to capture architecturally significant decisions.
tags: []
timestamp: <ISO 8601 datetime of last change>
status: active
owner: <git config user.name>
last_reviewed: <today YYYY-MM-DD>
review_interval: 180d
---

# Record Architecture Decisions

Date: {today}

## Status

Accepted

## Context and Problem Statement

We need to track significant architectural decisions made during the evolution
of this project so that future contributors understand the reasoning behind
the current design, not just the design itself.

## Decision Drivers

- Decisions made without recorded context are hard to revisit or challenge
- New contributors lack the history needed to make consistent choices

## Considered Options

- Unstructured notes in README or wiki
- Architecture Decision Records (MADR 4.x format)

## Decision Outcome

Chosen option: "Architecture Decision Records (MADR 4.x)", because the
structured format makes drivers, options, and trade-offs explicit and
queryable.

### Positive Consequences

- Decisions are self-contained and searchable
- Supersession chains preserve the full history of a choice

### Negative Consequences

- Requires discipline to write ADRs before implementing, not after
```

3. Report: "ADR directory initialised. Next ADR will be `0002-...`."

---

## Create Mode

**Steps — execute in order:**

1. Run `find docs/architecture/decisions/ -name "adr-*.md" | sort` to determine the next number.
2. Run `git config user.name` to get the owner value.
3. Gather missing inputs: problem context, decision drivers, options, chosen option, consequences.
4. Draft using the appropriate template from `references/madr-templates.md`. The template already includes the frontmatter block — populate all five fields. Set `status: draft`.
5. Validate with `references/adr-quality-checklist.md`.
6. Write the file to `docs/architecture/decisions/adr-{NNNN}-{slug}.md`.
7. Report the filename and a one-line summary of the decision outcome.

---

## Supersede Mode

A supersession is **always a two-file atomic operation**. Both files must be written before reporting done. Never write only one.

**Steps — execute in order, never skip step 4:**

1. Ask for (or infer from context): the number of the ADR being superseded and the title of the new ADR.

2. Read the existing ADR being superseded (`docs/architecture/decisions/adr-{NNNN}-{old-slug}.md`) to understand the original decision context.

3. Determine the next number by running `find docs/architecture/decisions/ -name "adr-*.md" | sort`.

4. Run `git config user.name` to get the owner value.

5. Draft the new ADR using `references/madr-templates.md`. Populate the frontmatter with:
   - `status: draft`
   - `supersedes: docs/architecture/decisions/adr-{old-NNNN}-{old-slug}.md`

6. **Write the new ADR** to `docs/architecture/decisions/adr-{new-NNNN}-{new-slug}.md`.

7. **Update the superseded ADR's frontmatter** — two changes only:
   - Change `status:` to `superseded`
   - Add `superseded_by: docs/architecture/decisions/adr-{new-NNNN}-{new-slug}.md`

   If the superseded ADR has no frontmatter block yet, add one before the `#` title line with all five standard fields populated, plus `superseded_by`.

8. Report both files changed: new file created + old file frontmatter updated.

**Hard rule:** if step 6 cannot be completed (file not found, unreadable), stop and report the problem. Do not leave the superseded ADR with a stale "Accepted" status.

---

## Review Mode

When asked to review an ADR:

1. Report findings first, ordered by severity (`critical`, `major`, `normal`, `low`).
2. Reference exact file paths and lines when available.
3. Focus on decision quality problems:

   - missing decision drivers,
   - missing alternatives,
   - unjustified outcome,
   - unclear consequences,
   - broken traceability to prior ADRs,
   - superseded ADR not updated.

4. Provide a corrected ADR text after findings if requested.

---

## Output Rules

- Produce Markdown only.
- Keep the narrative factual and concise.
- Prefer complete ADR drafts over outlines unless the user asks for an outline.
- If inputs are incomplete and user wants speed, draft with explicit `[ASSUMPTION]` markers and list required confirmations at the end.
- All ADR files use the OKF-superset frontmatter block defined in `rules/artefact-frontmatter.md` (incl. `type: Architecture Decision Record`). The MADR templates already include it — do not omit or reorder fields.

## References

- Use `references/madr-templates.md` for canonical section structure.
- Use `references/adr-quality-checklist.md` for acceptance criteria before finalizing.
