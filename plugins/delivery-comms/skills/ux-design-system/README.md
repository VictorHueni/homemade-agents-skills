# ux-design-system

The project's single visual source of truth. Author the brand once in
`design-system.md`; generate `tokens.css`, the `:root` variable sheet every
`com-*` artefact themes from.

```
design-system.md  ──generate──>  tokens.css  ──var(--token)──>  com-slide-deck
 (authored, human)               (:root contract)               com-artefact-viz
```

Adapts Anthropic's
[`brand-guidelines`](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines)
pattern (design system as a shared, on-demand resource), kept domain-agnostic —
it scaffolds a fillable design system rather than hard-coding a brand.

## Usage

```bash
# Scaffold docs/ux/{design-system.md, tokens.css} (neutral defaults)
python scripts/generate_tokens.py scaffold

# After editing the token values in design-system.md, regenerate the CSS
python scripts/generate_tokens.py generate docs/ux/design-system.md
```

Then the presentation skills theme from it:

```bash
# com-artefact-viz auto-detects docs/ux/tokens.css
python ../com-artefact-viz/scripts/render.py docs/business/03a-capability-map.md
```

## Layout

```
ux-design-system/
  SKILL.md                       Claude-facing instructions
  README.md                      This file
  templates/
    design-system.template.md    Authored doc skeleton (rationale + token tables)
    tokens.template.css          Canonical :root defaults (the contract)
  scripts/
    generate_tokens.py           scaffold + generate/refresh (md -> css)
  references/
    token-contract.md            The canonical token names, grouped
    discipline.md                Principles and boundaries
  examples/
    design-system.sample.md      A filled example
```

Output: `docs/ux/` (the `ux-` category folder; the skill name `ux-design-system`
follows the standard `<category>-<artefact>` convention). Python 3.8+, stdlib only.
