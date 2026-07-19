# Visualisation discipline

Internal guidance for `com-artefact-viz`. Principles first; the mechanics live
in `SKILL.md` and `parsing-contract.md`.

## Principles

1. **The Markdown is the source of truth.** A view is a derived read-out, never
   a second editing surface. It carries no authored content that isn't in the
   artefact, so it can always be regenerated and never drifts. If a user wants
   to "fix" something in a view, the fix belongs in the source artefact.

2. **Style is the project's, not the skill's.** Renderers emit semantic class
   names and `var(--token)` references only — never a literal colour, font,
   radius, or shadow. The default token sheet is deliberately neutral so a
   project's `--design-system` sheet themes every view by overriding `:root`.
   A renderer that hard-codes `#3b6ef5` is a bug.

3. **One self-contained file.** All CSS and JS are inlined. No build step at
   view-time, no network fetch, no runtime dependency. The output is shareable
   by sending one file and is diff-friendly enough to commit.

4. **Progressive interactivity.** Every view is valid static HTML first; the
   JS runtime only *enhances* (collapse, orientation, disclosure). A view with
   JS disabled still reads correctly.

5. **Parse defensively.** Real artefacts are half-filled. Parsers tolerate
   missing columns, placeholder cells, reordered headers, and absent sections,
   and degrade to an empty-but-valid view rather than crashing.

## Boundaries — what this skill is NOT

- **Not a slide builder.** Narrative presentations are `com-slide-deck`. This
  skill renders one artefact as one analytical view, not a sequence of slides.
- **Not an architecture diagrammer.** C4 / structurizr diagrams are `arch-c4`
  and `arch-structurizr`. This skill does not draw containers/components.
- **Not an authoring tool.** It never writes into the source artefact and never
  invents content. Authoring stays with the owning skill
  (`business-capability-map`, `plan-delivery-roadmap`, etc.).
- **Not a metamodel step.** It mints no IDs and nothing references its output.
  It is a supporting communication skill, wired like `com-slide-deck`.

## Domain-agnostic discipline

Per `rules/skill-creation-sync.md`, the kit is user-global. Templates, defaults,
and example fixtures use neutral placeholders ("Example Platform", generic
capability names) — never a real client, currency, or segment. Only a project's
own rendered output is project-specific; the skill side stays neutral.

## Re-theming recipe (most common request)

A project already using `com-slide-deck` has a design system at
`docs/communication/slides/{slug}/design/styles.css`. Pass it straight through:

```bash
python scripts/render.py docs/business/03a-capability-map.md \
  --design-system docs/communication/slides/{slug}/design/styles.css
```

Any `:root { --accent: …; --font-sans: …; }` tokens in that sheet override the
defaults, so the capability map, roadmap, FBS, and canvas all adopt the deck's
look without touching the renderers.
