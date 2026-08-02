---
type: skill
name: ux-design-system
description: "Author a project's single visual design system once and generate the canonical token sheet every com-* artefact consumes. Adapts Anthropic's brand-guidelines pattern (a design system as a shared, on-demand resource) kept domain-agnostic: scaffolds a fillable design-system.md (brand rationale + token tables for palette, typography, spacing, and semantic tokens) and generates docs/ux/tokens.css, a :root variable contract. com-slide-deck and com-artefact-viz reference these via var() and never hard-code colour/font/radius, so editing the design system re-themes every deck and view with no renderer change. Modes: scaffold, generate/refresh. Use when the user wants to define a design system, brand tokens, theme, colour palette, typography, or shared visual style for generated decks and visualisations. Triggers on: design system, design tokens, brand guidelines, theme, colour palette, typography tokens, tokens.css. Output: docs/ux/. Mints no IDs; cross-cutting foundation for the presentation layer."
version: "1.0.0"
status: active
last_reviewed: 2026-05-29
review_interval: 180d
user-invocable: true
impact: "low"
metadata:
  category: "ux"
  complexity: "low"
---

# ux-design-system — Project Design System

Own the project's **single visual source of truth**. Author the brand once in a
human-readable `design-system.md`; generate `tokens.css`, a `:root` variable
sheet that every `com-*` artefact themes from. Change a token, regenerate, and
every slide deck and artefact visualisation re-themes — no renderer touched.

This is the kit's adaptation of Anthropic's
[`brand-guidelines`](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines)
pattern (a design system encoded as a shared, on-demand resource), kept
**domain-agnostic**: it never hard-codes a brand — it scaffolds a fillable
design system the project owns.

```
design-system.md  ──(generate_tokens.py)──>  tokens.css  ──var(--token)──>  com-slide-deck
  (authored, human)                          (:root contract)              com-artefact-viz
```

It mints no IDs and links to no other artefact. It is a **cross-cutting
foundation** for the presentation layer — scaffold it any time before producing
communication artefacts.

---

## Quick reference

| Task | Command |
|---|---|
| Scaffold the design system | `python scripts/generate_tokens.py scaffold` (creates `docs/ux/design-system.md` + `tokens.css`) |
| Regenerate tokens after editing the doc | `python scripts/generate_tokens.py generate docs/ux/design-system.md` |
| Refresh (alias) | `python scripts/generate_tokens.py refresh docs/ux/design-system.md` |

Output lives at `docs/ux/` (the `ux-` category folder — the skill name
`ux-design-system` follows the standard `<category>-<artefact>` convention).

---

## Modes

### `scaffold`

Create `docs/ux/design-system.md` (from the template — brand-rationale
placeholders + token tables pre-filled with neutral defaults) and
`docs/ux/tokens.css` (neutral defaults). Existing files are skipped, never
overwritten. `owner` is taken from `git config user.name`.

```bash
python scripts/generate_tokens.py scaffold          # -> docs/ux/...
python scripts/generate_tokens.py scaffold path/docs # custom docs root
```

### `generate` / `refresh`

Parse the `## Tokens` tables in `design-system.md` and (re)write `tokens.css`
next to it. The token **names** are the fixed contract; values are free. The
generator warns if a contract token is missing or an unknown token appears, but
keeps unknown tokens so a project can extend the palette.

```bash
python scripts/generate_tokens.py generate docs/ux/design-system.md
```

---

## Operating sequence

1. **Scaffold** (once per project): `scaffold`. This is a good early step — do
   it before the first `com-slide-deck` deck or `com-artefact-viz` view so they
   theme consistently from day one.
2. **Author** `docs/ux/design-system.md`: fill the brand rationale and set
   the token **values** (palette, typography, spacing, semantic accents). Keep
   the `Token` and `Value` columns intact; do not rename or drop tokens.
3. **Generate**: run `generate` to produce `tokens.css`.
4. **Consume** from the presentation skills:
   - `com-artefact-viz` auto-detects `docs/ux/tokens.css` (or pass
     `--design-system docs/ux/tokens.css`).
   - `com-slide-deck`'s `build.py` inlines `docs/ux/tokens.css` before the
     deck `styles.css` (config `paths.design_tokens`, or auto-detected).
5. **Refresh** whenever the brand changes — re-run `generate`; every consumer
   re-themes on its next build.

---

## The token contract

`tokens.css` defines one agreed `:root` vocabulary so any `com-*` renderer can
rely on the same variable names. The canonical names, grouped, live in
`references/token-contract.md` and in `templates/tokens.template.css` (the
generator validates against the latter). Groups: base palette · generic
semantic state (`--success/--warning/--danger/--info`) · typography · spacing &
shape. The contract stays generic on purpose — kit-domain tokens (delivery
status, pain, confidence, importance) are **consumer-derived** as aliases to the
generics (see `references/token-contract.md`), so a project themes four portable
names instead of kit jargon.

**Discipline:** renderers reference `var(--token)` only — never a literal
colour, font, or radius. A renderer that hard-codes `#3b6ef5` is a bug. That
contract is what makes the design system the single lever for re-theming.

---

## Output frontmatter

`docs/ux/design-system.md` opens with the standard OKF-superset artefact
frontmatter — `type: Design System` (its `okf_type` in the `metamodel` skill's `references/artefact-types-registry.yaml`),
plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`,
`review_interval`; default `review_interval: 180d`. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`.

`tokens.css` is a generated machine artefact (no frontmatter) — author durable
changes in the `.md`, not the `.css`.

---

## Verification checklist

1. [ ] `docs/ux/design-system.md` exists with the brand rationale filled (no `_TODO_`).
2. [ ] `generate` runs with no missing-contract-token warning.
3. [ ] `docs/ux/tokens.css` defines the full contract (`references/token-contract.md`).
4. [ ] `com-artefact-viz` auto-detects the sheet (prints "using shared design system …").
5. [ ] A token-value edit, after `generate`, visibly changes a rendered deck/view.

---

## Follow-up work

Planned enhancements for this skill — and the deferred unification of
`com-slide-deck`'s `styles.css` onto this shared `tokens.css` — are tracked as
central-only rows in `docs/project-control/open-items/open-items.md` (per
the `metamodel` skill's `references/open-items-governance.md` §9), not in this folder.

## See also

- `references/token-contract.md` — the canonical `:root` variable schema.
- `references/discipline.md` — principles and boundaries.
- `com-artefact-viz/SKILL.md` · `com-slide-deck/SKILL.md` — the consumers.
- `rules/skill-creation-sync.md` · the `metamodel` skill's `references/artefact-frontmatter.md`.
