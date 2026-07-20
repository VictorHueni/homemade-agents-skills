# Design-system discipline

Internal guidance for the `ux-design-system` skill.

## Principles

1. **One design system per project.** `docs/ux/` holds the single visual
   source of truth. Consumers theme from it; they do not each define their own
   palette. Two design systems = drift.

2. **Author in Markdown, generate the CSS.** `design-system.md` is the human
   artefact (rationale + token tables); `tokens.css` is generated and
   machine-owned. Durable edits go in the `.md`. Mirrors the kit pattern of
   `com-slide-deck`'s `design-system.md → styles.css`.

3. **Names are the contract; values are the brand.** Every consumer relies on
   the token *names* in `references/token-contract.md`. Change values freely to
   re-brand; never rename or drop a token. Extending with extra tokens is fine.

3a. **Keep the contract generic; consumers derive domain tokens.** The project
   `tokens.css` carries only portable names — base palette, `--success/--warning/
   --danger/--info`, typography, spacing. Kit-domain vocabulary (delivery status,
   pain index, confidence, strategic importance) is **not** in the contract; each
   consumer defines those in its own stylesheet as aliases to the generics (e.g.
   `com-artefact-viz/templates/tokens.domain.css`: `--status-shipped: var(--success)`).
   This keeps a project's
   design system interoperable across the kit and the project's other tooling —
   themers touch four generic names, not kit jargon.

4. **Domain-agnostic.** Unlike Anthropic's `brand-guidelines` (which hard-codes
   Anthropic's palette), the kit is user-global, so this skill ships only
   neutral defaults and a fillable template. No real brand colour, font, or
   client name appears on the skill side — only in a project's own
   `docs/ux/`.

5. **No IDs, no links.** The design system mints no IDs and carries no FK
   references to other artefacts. It is a cross-cutting foundation, not a node
   in the artefact dependency graph. It does not appear in the ER diagram or the
   cross-doc ID conventions table.

## Boundaries — what this skill is NOT

- **Not a renderer.** It produces tokens, not HTML. Decks are `com-slide-deck`;
  artefact views are `com-artefact-viz`.
- **Not a component library.** It defines tokens (colour/type/space/shape), not
  reusable HTML/CSS components. Each consumer builds its own components *from*
  the tokens.
- **Not per-deck or per-view.** It is project-scoped (`docs/ux/`), not
  scoped to one deck folder. A deck may still keep deck-specific CSS, but it
  should source its base tokens here.

## Relationship to the consumers

Both `com-*` skills inherit this skill's `tokens.css` directly:

- **`com-artefact-viz`** auto-detects `docs/ux/tokens.css` and inlines it as
  the theme (override with `--design-system`).
- **`com-slide-deck`** — `build.py` locates `docs/ux/tokens.css` (config
  `paths.design_tokens` or auto-detect by walking up) and inlines it **before**
  the deck's `styles.css`, so base palette + typography + the generic semantic
  state tokens (`--success/--warning/--danger/--info`) flow from here. The deck
  adopts the contract names and adds only deck-only tokens. A deck with no shared
  sheet still builds standalone (backwards compatible). This unification resolved
  OI-0019.

Because both consumers rely on the contract token **names**, never rename or
drop a token; change values freely.
