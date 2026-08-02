---
name: com-release-note
license: MIT
description: "Curate a stakeholder-facing, non-technical release note from a release's raw material: the changelog plus commit and merged-PR history between two tags, and (when present) the FBS + capability map. Reorganises type-grouped changelog entries into a plain-language, benefit-first note by Product then Capability then Functionality, plus a Platform and Engineering tier for infra/CI/refactor work. Emits a committed Markdown note, a GitHub Release body, and (render mode) an A4 PDF report themed by the shared design-system tokens like com-slide-deck; degrades gracefully with no FBS. Five modes: gather, scaffold, curate, refresh, render. Use for release notes, a GitHub Release body, a release-note PDF for management, or turning a changelog into something a non-technical reader can act on. Triggers on: release note, changelog to release note, GitHub release body, release note pdf, release report, com-release-note. Do NOT use for the technical changelog itself (release-please) or slide decks (com-slide-deck)."
allowed-tools: Bash(python ${CLAUDE_SKILL_DIR}/scripts/gather.py *) Bash(python ${CLAUDE_SKILL_DIR}/scripts/render_pdf.py *)
version: "1.1.0"
status: active
last_reviewed: 2026-07-18
review_interval: 180d
user-invocable: true
impact: "low"
metadata:
  category: "communication"
  complexity: "medium"
---

# com-release-note — Stakeholder Release Note Curator

Turn a release's raw material into a **release note a non-technical reader can act on**. A commit-message parser (release-please and friends) groups changes by *type* (Features / Fixes / …) and produces the mechanical `CHANGELOG.md` — the technical ledger. This skill produces the *other* layer: a curated narrative reorganised by **Product → Capability → Functionality**, in plain language, for customers, managers, and investors.

This is a **communication artefact** (`com-` prefix → `docs/communication/`). It **mints no IDs** and is **not a build-order step** — the note is a derived, regenerable read-out; the changelog, FBS, and capability map remain the sources of truth.

```
CHANGELOG + commit/PR history + FBS + capability map ──(gather)──▶ evidence bundle ──(curate)──▶ release note + GitHub Release body
```

## Inputs

| Source | Origin | Path (default) |
|---|---|---|
| Technical changelog | `release-please` / commit parser | `CHANGELOG.md` (repo root) |
| Commit + merged-PR history | git / `gh` | `git log <since>..<until>` · `gh pr list` |
| Functional Breakdown Structure | `spec-functional-breakdown-structure` | `docs/product-specs/07a-fbs.md` |
| Capability map | `business-capability-map` | `docs/business/03a-capability-map.md` |

**Tier 1 uses the FBS product-scoped view** (`P{n} → C{n}.{m} → C{n}.{m}.F{xx}`), **not** the capability map's domain-scoped `C-N.M` — the two numbering schemes collide. Read the FBS as the primary structure; the capability map only supplies capability names/context. If the project has **no FBS**, the skill degrades gracefully (see Curate mode, Step 3b).

## Quick reference

| Task | Command |
|---|---|
| Gather the evidence bundle for a release | `python path/to/com-release-note/scripts/gather.py --since v{PREV} --until v{X.Y.Z}` |
| Scaffold a blank note into the project | copy `templates/release-note-template.md` to the output location |
| Curate the note (+ GitHub Release body) | reason over the bundle; fill the template; produce both outputs |
| Refresh for the next release | re-gather from the new prior tag, re-curate |
| Render the note to an A4 PDF report | `python path/to/com-release-note/scripts/render_pdf.py NOTE.md` (optional Playwright) |

Default output: `docs/communication/release-notes/{version}-{slug}.md` (or an existing `docs/release-notes/`).

## The five modes of operation

### Mode 1 — Gather

**When:** first step of any note; run before Scaffold/Curate so curation reasons over a clean, deterministic bundle instead of ad-hoc `git log` reads.

**Process:**
1. Determine the range: `--since` = the previous release tag (auto: `git describe --tags --abbrev=0` on the parent of the target, or ask), `--until` = the target tag or `HEAD`.
2. Run the helper (read-only — never mutates the repo, never auto-installs tooling):
   ```bash
   python path/to/com-release-note/scripts/gather.py \
     --since v{PREV} --until v{X.Y.Z} \
     --changelog CHANGELOG.md \
     --fbs docs/product-specs/07a-fbs.md \
     --capability-map docs/business/03a-capability-map.md \
     --output {scratch}/release-{X.Y.Z}-bundle.md
   ```
3. Surface the bundle to the user for a sanity check. It contains, in order: **breaking changes detected from commits** (a `!` type marker or a `BREAKING CHANGE:` / `BREAKING-CHANGE:` footer, listed first so they cannot be scrolled past), the `CHANGELOG.md` section for the target version, the commit/merged-PR subjects grouped by conventional-commit type, and pointers to the FBS + capability map (not deep-parsed — Curate reads those).
   Detection is **not** a decision: the curator still judges what each breaking change means for the reader and writes the note's `## Breaking changes` section. The detected block only guarantees the input is never silently missing — a project without a release-please `CHANGELOG.md` would otherwise leave a `!` buried in one subject line as the sole signal, and footers invisible entirely.

**Output:** a Markdown evidence bundle at a scratch path (gitignored / not committed).

### Mode 2 — Scaffold

**When:** the project has no release-note yet for this version, and you want the blank structure first (or you are setting up the two-layer model in a new project).

**Process:**
1. Resolve the output location (see **Auto-detect output location**).
2. Copy `templates/release-note-template.md` there as `{version}-{slug}.md`. Fill the frontmatter (`git config user.name` → `owner`, today → `last_reviewed`, `status: draft`); leave every `{placeholder}` / `_TODO_` untouched. **Do NOT invent content in Scaffold.**

**Output:** a `_TODO_`-marked note file ready for Curate.

### Mode 3 — Curate

**When:** the core intent — turn the evidence bundle into the finished note. This is judgement work; a human approves the narrative.

**Process:**
1. **Read the bundle** (Mode 1 output). If it does not exist, run Gather first.
2. **Read the FBS + capability map** if present.
3. **Attribute each changelog/PR entry to Product → Capability → Functionality:**
   - The commit **scope** (`feat(billing): …`) and entry text are the clues; **an FBS functionality flipping to ✅ is the strongest signal**.
   - Entries with **no product-capability home** (CI/CD, refactor, tooling, infra, perf, security) → the **Platform and engineering** tier.
   - A `fix:` entry a non-technical reader can actually notice → **Fixes and improvements**; an internal fix → Platform and engineering; dependency bumps and lint → dropped.
   - **Step 3b — graceful degradation (no FBS):** if there is no FBS, group Tier 1 by the product/area implied by commit scopes (or a single product if the repo has one), and skip the `C{n}.{m}` IDs — keep plain-language capability groupings. The note still reads correctly; it just loses the FBS ID cross-references.
4. **Write the note** against `templates/release-note-template.md`: a one-line theme, `## What's new` (Tier 1, plain-language benefit-first bullets), `## Fixes and improvements` (Tier 1b — what was broken and is now right, same reader-facing voice; internal fixes go to Tier 2 and noise is dropped), `## Platform and engineering` (Tier 2, the project's stable buckets), optional `## Breaking changes`, then the `**Full Changelog**: v{PREV}...v{X.Y.Z}` link. Honour every rule in the template comment (no em dashes; scope honesty; do not invent).
   **Only these four `##` headings render.** The PDF renderer matches headings on the keywords `new`, `fix`, `platform` and `breaking`; any other section is omitted from the report and reported as a warning on stderr (it will not vanish silently, but it will not print either).
5. **Produce the GitHub Release body** from `templates/github-release-body-template.md`: a condensed, screenful summary that links back to the committed note at its tag. This is the second output — do not skip it.
6. **Hand to the user for approval.** The narrative is judgement content, not mechanically verifiable. Delete the template comment blocks on finalise; flip `status: draft → active` once approved.

**Output:** the committed `docs/.../release-notes/{version}-{slug}.md` **and** the GitHub Release body text.

### Mode 4 — Refresh

**When:** a new release ships and needs its own note.

**Process:** auto-detect the prior release tag, re-run Gather for the new range, then Curate a **new** note file (never overwrite a prior release's note). If the project defined custom Tier-2 buckets in an earlier note, reuse the same buckets for continuity.

### Mode 5 — Render

**When:** the curated note is approved and needs a human-readable, nicely designed A4 PDF (a management leave-behind), styled from the same design system as the project's slide decks and artefact views.

**Process:**
1. Run the renderer against the committed note (read-only on the note; derived outputs only):
   ```bash
   python path/to/com-release-note/scripts/render_pdf.py \
     docs/communication/release-notes/{version}-{slug}.md
   ```
2. **Theming** follows the kit's shared token cascade (same layering as `com-slide-deck` / `com-artefact-viz`): `templates/tokens.fallback.css` first, then the project's `docs/ux/tokens.css` (auto-detected from the working directory; `--design-system PATH` overrides), project values winning. All layout CSS in `templates/report.html.tmpl` references `var(--token)` only — re-theme the design system and the report follows.
   `tokens.css` only ever carries font *names* (`--font-sans: 'Newsreader', Georgia, serif`) — nothing loads the actual font file, so a real brand font silently falls back to its CSS-stack fallback in headless Chromium unless the project also self-hosts it. If `docs/ux/fonts/fonts.css` exists (plain `@font-face` rules, relative `url()` to sibling font files under `docs/ux/fonts/`, using the same `font-family` names as `tokens.css` — the shape a package like `@fontsource` ships), it is auto-detected and its fonts are inlined as base64 data URIs, so the PDF needs no live network fetch. Absent file → no change, same silent degrade as the rest of the cascade. (`com-slide-deck` / `com-artefact-viz` do not yet implement this — tracked as a harmonization follow-up.)
   **`--font-report` (optional):** the report's text face is `var(--font-report, var(--font-sans, …))`, so a project whose `--font-sans` is deliberately something the report should *not* use (a reading serif chosen for decks, or a face that carries a specific meaning elsewhere in the product) can set `--font-report` and re-face the report alone, leaving every other `com-*` artefact untouched. Declare it wherever the project already hand-authors CSS the renderer picks up — `docs/ux/fonts/fonts.css` is the natural home, since it is inlined ahead of the token sheets and is the file that loads the face anyway. Undeclared → identical to before.
3. The script always writes the self-contained A4-print-styled HTML intermediate, then drives headless Chromium via **Playwright** (optional dependency — never auto-installed) for the paginated PDF. Every page carries a running head (the note's `title`, or version plus theme) and a foot (`Release note · v{X.Y.Z}` left, page position right), so a page separated from the document still identifies itself. These sit in the page-margin boxes and are a separate document from the report, so design tokens cannot reach them — they are deliberately neutral grey chrome. If Playwright is missing, the HTML is still written and the script fails the PDF step with an explicit message — open the HTML in a browser and print to PDF as the fallback.
   A **cartouche** sits directly under the summary and holds every piece of release metadata in label/value rows: period, owner, status, changelog range, a **link to the version's GitHub Release**, and the provenance line (which tool, which day, which source file). It replaces a document footer entirely, so the reader finds the links at the top rather than the end. Rows with nothing to show are omitted. The changelog row follows what the note wrote: a bare compare range (`v1.3.0...v1.4.0`, the template's convention) is an identifier and renders as code, while a Markdown link or a pasted URL renders as a live link. Markdown links render throughout the report, not only here — a `[text](url)` in any bullet becomes a real PDF link annotation, and a URL whose scheme isn't followable (`javascript:`, `data:`) prints verbatim instead of becoming a link in a distributed document. The release URL is printed in full (a bare anchor is useless on paper) and clickable in the PDF; it is derived from the repo's `remote.origin.url` plus the note's version — reading the configured value, not `git remote get-url`, so `url.*.insteadOf` rewrites cannot redirect it to a mirror. Override with `--release-url`; a note outside a repo or on a non-GitHub remote simply carries no link row.
   A **recap** follows the cartouche: a donut of the release's composition (new capabilities, platform items, fixes, breaking changes) with the total in its hole and a legend carrying every slice's count and share, plus context cards to its right for **days**, **active days**, **commits** and **lines added/removed**. Every figure is counted, never judged, so the same note always yields the same block: the section counts and the day span come from the note's own structure, while the git measures are read over the range in the note's Full Changelog line — `rev-list --count` for commits, distinct commit dates for active days, and `diff --shortstat` for lines. Note that `diff` reports the **net** difference between the two tags, not development churn: a release that adds and then removes the same file nets to zero, where summing `log --numstat` over each commit would show both. Added and removed are distinguished by sign only, never by colour, since deleted code is not inherently bad. A row whose measure is unavailable (no dates, no tags, no git) is omitted rather than guessed, and a note with no entries renders no recap. Slice colour is an **ordinal ramp of the accent hue** (the sections are tiers), validated for monotone lightness, adjacent step gaps, light-end contrast and single hue; the cards deliberately repeat nothing the donut already shows.
   The PDF contains only pages with real content: when content ends just past a page boundary, the renderer probes Chromium's real pagination and shrinks the document by the smallest amount that saves a page, down to a readability floor of 85% (logged as `scaled to N`). Past that floor the extra page is honest and is kept.
4. Verify the PDF: every section of the note is present, nothing truncated, cards not split across pages, project theme visible.

**Output:** `{note-dir}/pdf/{version}-{slug}.pdf` + `.html` (both derived and regenerable — the Markdown note stays the single source of truth; re-render after edits). Override with `--output`; `--html-only` skips the PDF step.

Two fixtures live in `examples/`: `release-note.sample.md` is a minimal note for smoke-testing the pipeline, and `release-note.complete.md` is a full worked example — three products, nine capabilities, all six default Tier-2 buckets, and three breaking changes — paired with `github-release-body.complete.md`, the condensed second output for the Releases page. Render either to see the shipped design.

## Auto-detect output location

Probe in order:
1. If `docs/release-notes/` exists → write there (respect the project's established top-level folder).
2. Else → write to `docs/communication/release-notes/` (kit `com-` convention; create it).

Never overwrite an existing note for the same version — switch to Refresh, or ask.

## Soft-links

| Note element | Links to (by ID) |
|---|---|
| Tier 1 capability bullet | FBS `C{n}.{m}.F{xx}` / capability `C-N.M` |
| Audit-trail parens `(0137)` | exec-plan / `PRD-NNNN` ID |
| Full Changelog line (note footer; PDF cartouche) | the `v{PREV}...v{X.Y.Z}` compare range |

Use ID + name + relative path for any in-repo link, so description renames don't break the link.

## Output structure

Open the committed note with the standard artefact frontmatter (OKF-superset block — set `type` to this artefact's `okf_type` display name **`Release Notes`** from the `metamodel` skill's `references/artefact-types-registry.yaml`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval: 90d`). Run `git config user.name` for `owner`; `status: draft` on scaffold, `active` on approval. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`. The GitHub Release body carries **no** frontmatter (it is not an OKF concept doc).

```
docs/communication/release-notes/{version}-{slug}.md   ← committed note (OKF frontmatter)
  # v{X.Y.Z}: {theme} ({date})
  ## What's new                 ← Tier 1: Product → Capability, plain language
  ## Fixes and improvements      ← Tier 1b: reader-visible fixes, same voice; omit if none
  ## Platform and engineering    ← Tier 2: 6 default buckets, redefinable per project
  ## Breaking changes            ← only if any
  Full Changelog: v{PREV}...v{X.Y.Z}
(paste-ready) GitHub Release body ← condensed; links back to the note at its tag
```

## Curation discipline

The judgement calls — stakeholder voice vs commit voice, curate-don't-dump, cite-every-claim, when to curate at all — live in [`references/curation-methodology.md`](references/curation-methodology.md). Read it before curating.

## Verification checklist

- [ ] Every Tier 1 bullet is plain language and benefit-first (no bare commit subjects).
- [ ] Every claim traces to a changelog/PR entry in the bundle — nothing invented.
- [ ] Scope honesty: Tier 1 holds only reader-reachable surfaces; operator/internal work is in Tier 2.
- [ ] No em dashes in the title or any heading.
- [ ] Frontmatter complete (`type: Release Notes`, owner, dates); `status: active` only after human approval.
- [ ] Both outputs produced: committed note + GitHub Release body.
- [ ] `**Full Changelog**` compare link present and correct.
- [ ] *(Render)* PDF carries every note section, cards unsplit across pages, and the project's `docs/ux/tokens.css` visibly themes it (when present).

## Dependencies

`git` and `gh` (GitHub CLI) on PATH for `scripts/gather.py`. Python 3.8+, standard library only. **Playwright** is optional, only for `scripts/render_pdf.py` PDF export (`pip install playwright && python -m playwright install chromium`); without it the renderer still writes the HTML intermediate. Scripts fail with an explicit message if a dependency is missing — they never auto-install.

## Follow-up work

Open items about this skill's own evolution go to the kit's central ledger (`docs/project-control/open-items/`) per the `metamodel` skill's `references/open-items-governance.md`, never in a local section here.

## See also

- `templates/release-note-template.md` · `templates/github-release-body-template.md` — the two outputs
- `templates/report.html.tmpl` · `templates/tokens.fallback.css` — the A4 PDF report shell + shipped token contract (Mode 5)
- `ux-design-system/SKILL.md` — the shared design system; its `docs/ux/tokens.css` is auto-detected as the report theme
- `references/curation-methodology.md` — principles, boundaries, worked recipe
- the `metamodel` skill's `references/artefact-frontmatter.md` · the `metamodel` skill's `references/artefact-types-registry.yaml` — `Release Notes` frontmatter + registry
- `dev-release-init` — the upstream release-automation skill that produces the `CHANGELOG.md` + tags this note curates
- `com-slide-deck`, `com-artefact-viz` — sibling `com-` communication skills

## Closing report to the user

After curating, report in 4–6 lines: the version + theme, where the committed note was written, that the GitHub Release body is ready to paste, how many entries mapped to Tier 1 vs Tier 2, any entries you could not confidently attribute (flag for the human), and the reminder that the narrative needs human approval before `status: active`.
