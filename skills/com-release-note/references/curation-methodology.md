# Curation methodology — internal guidance for `com-release-note`

Internal guidance for the skill. Principles first; the mechanics (modes, commands, output paths) live in `SKILL.md`. Read this before curating a note.

## Principles

1. **The evidence bundle is the source of truth.** Curate only from what `scripts/gather.py` collected — the changelog section, the commit/PR subjects, and the FBS/capability map. If a claim is not traceable to an entry in the bundle, it does not go in the note. Never pad a release to make it look bigger.

2. **Stakeholder voice, not commit voice.** A changelog says `feat(billing): word-level diff on plan terms`. A release note says "You can now see exactly which words changed in your plan's terms, not just that something changed." Translate every kept entry from what-the-engineer-did into what-the-reader-gets. Lead with the benefit, name the feature second.

3. **Curate, do not dump.** The automated `CHANGELOG.md` already lists everything, grouped by type. This note's whole value is *selection and re-grouping*: promote the few changes a reader cares about into `## What's new`, demote the rest into `## Platform and engineering`, and drop pure noise (dependency bumps, lint fixes) entirely. A release note that mirrors the changelog one-to-one has done no work.

4. **Attribute by capability; the FBS ✅ flip is the strongest signal.** Map each kept entry to its Product → Capability → Functionality. The commit scope and text are clues, but a functionality flipping to ✅ in the FBS this release is the highest-confidence signal that a user-facing capability advanced. When there is no FBS, group by product/area from the scopes and keep the plain-language capability names (graceful degradation) — the note still reads correctly, it just loses the ID cross-references.

5. **Scope honesty over completeness.** Describe in `## What's new` only what a non-technical reader can actually reach or act on. Operator-only tooling, staging-only changes, and internal refactors belong in `## Platform and engineering` (or an earlier release, if a surface is not yet public). A note that claims a capability the reader cannot use erodes trust in every future note.

6. **Every external claim is cited; the human owns the narrative.** Keep the private audit-trail IDs `(0137)` so any bullet can be traced back. The final narrative is judgement, not a mechanical transform — always hand it to a human for approval before flipping `status: draft → active`.

## Boundaries — what this skill is NOT

- **Not a changelog generator.** The mechanical, type-grouped `CHANGELOG.md` is produced by release-please (or an equivalent commit parser). This skill consumes that output; it never replaces it.
- **Not a raw PR summariser.** Summarising PRs one-by-one reproduces commit voice. The skill's job is cross-referencing PRs against the capability map to build a *narrative*, not a list.
- **Not a slide deck or a visualisation.** Presentation decks are `com-slide-deck`; interactive HTML views of artefacts are `com-artefact-viz`.

## Domain-agnostic discipline

The kit is user-global. Ship no project-specific product names, capabilities, currencies, or domain jargon in `SKILL.md`, the templates, or this file — use neutral placeholders (`P{n} · {Product name}`, `C{n}.{m} {Capability name}`). The default Tier-2 buckets are generic engineering categories; a project redefines them on first use. Audit before publishing:

```bash
grep -niE "<your project's product names, capabilities, domain jargon, client names>" SKILL.md templates/*.md references/*.md
```

Should return zero matches.

## When to curate vs. just ship the changelog

- **Skip curation** for routine releases with no external audience — the `CHANGELOG.md` is a fine technical record on its own.
- **Curate** when a release is externally announced, shown to non-technical stakeholders or investors, or is a milestone (a `.0`, a launch, a new public surface). The cost of the note is only justified when a human who cannot read the changelog needs to understand the release.

## Worked recipe (gather → curate)

```bash
# 1. Gather the evidence bundle for the release range (read-only)
python path/to/com-release-note/scripts/gather.py \
  --since v1.1.0 --until v1.2.0 \
  --changelog CHANGELOG.md \
  --fbs docs/product-specs/07a-fbs.md \
  --capability-map docs/business/03a-capability-map.md \
  --output /tmp/release-1.2.0-bundle.md

# 2. Read the bundle. For each entry: keep (Tier 1), demote (Tier 2), or drop (noise).
# 3. Fill templates/release-note-template.md — plain language, benefit-first, scope-honest.
# 4. Condense templates/github-release-body-template.md for the Releases page.
# 5. Report attribution counts + unmapped entries; hand to the human for approval.
```
