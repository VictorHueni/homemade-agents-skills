# Design System Definition

> **This document must be completed before building any slides.**
> Every section is required. The build process and all slide authoring
> decisions depend on the tokens, components, and rules defined here.
> Copy this template to `design-system.md` in the same folder and fill
> every section. Leave nothing as a placeholder.

---

## 1. Design Philosophy

_Describe the visual identity in 2-3 sentences. What feeling should the
presentation convey? What principles guide layout and decoration choices?_

**Name**: (give the design system a short name)

**Principles** (list 3-5):

1. ...
2. ...
3. ...

---

## 2. Color Tokens

The deck uses the **project design system as its single source of truth**: the
base palette and typography are defined once in `docs/ux/tokens.css` by the
[`ux-design-system`](../../../../ux-design-system/SKILL.md) skill and inlined by
`build.py` **before** this stylesheet. **Do NOT redefine base palette values
here** — reference them with `var()` and adopt the contract token names. Run
`ux-design-system scaffold` (then `generate`) if `docs/ux/tokens.css` does not
exist yet.

### Core palette — inherited from `docs/ux/tokens.css` (do not redefine)

Use these contract names everywhere in the stylesheet and in slide partials:

| Token          | Usage                                          |
|----------------|------------------------------------------------|
| `--canvas-bg`  | Slide / page background                        |
| `--surface`    | Card and cell background                       |
| `--surface-2`  | Recessed / grouped background                  |
| `--ink`        | Primary text                                   |
| `--muted`      | Secondary text (descriptions, body)            |
| `--border`     | Card borders, dividers, separators             |
| `--accent`     | Primary accent (CTAs, highlights, labels)      |
| `--accent-ink` | Text on accent fills                           |

### Semantic state colors — inherited from `docs/ux/tokens.css`

State colours are part of the shared contract — use them directly in partials,
do not redefine:

| Token | Usage |
|---|---|
| `--success` | Positive / done |
| `--warning` | Caution / in-progress |
| `--danger` | Negative / error |
| `--info` | Informational / neutral-active |

### Deck-only tokens (define here — not in the shared sheet)

Tokens with no contract equivalent stay deck-local. Define them in `:root`:

| Token         | Usage                                          |
|---------------|------------------------------------------------|
| `--dim`       | Tertiary text (timestamps, meta, captions)     |
| `--accent-lt` | Light accent (subtle backgrounds, hover)       |
| _extended_    | Per-level / per-category colours for multi-column decks |

### Migration map (renaming an older deck onto the contract)

| Old deck token | Contract token |
|----------------|----------------|
| `--bg`         | `--canvas-bg`  |
| `--text`       | `--ink`        |
| `--card-bg`    | `--surface`    |
| `--muted`      | `--muted` (unchanged) |
| `--border`     | `--border` (unchanged) |
| `--accent`     | `--accent` (unchanged) |
| `--success` / `--warning` / `--danger` | `--success` / `--warning` / `--danger` (now in the contract) |
| `--danger-lt` | derive locally, e.g. `color-mix(in srgb, var(--danger) 14%, var(--surface))` |
| `--dim` / `--accent-lt` / extended | keep as deck-only tokens |

---

## 3. Typography

### Font Stack

Typography tokens are inherited from `docs/ux/tokens.css` — reference them,
do not redefine:

| Token         | Usage                              | Source            |
|---------------|------------------------------------|-------------------|
| `--font-sans` | Headings + body text, labels, cards | contract (inherited) |
| `--font-mono` | Code, tags, metadata, slide numbers | contract (inherited) |

If the deck needs a distinct heading face, add a **deck-only** `--font-heading`
in this stylesheet's `:root` (defaulting to `var(--font-sans)`); otherwise use
`--font-sans` for both headings and body. Set the actual font families and web-
font loading in `docs/ux/design-system.md` (and the `fonts:` block of
`config.yaml` for the Google-Fonts `<link>`), so they flow from the one source.

### Font Loading

_Specify how fonts are loaded (Google Fonts CDN, self-hosted, system fonts).
Include the exact URL or @font-face declarations needed._

```
(font loading URL or method)
```

### Type Scale

| Element              | Font    | Size  | Weight | Line-Height | Letter-Spacing |
|----------------------|---------|-------|--------|-------------|----------------|
| Hero title           | heading |       |        |             |                |
| Content slide title  | heading |       |        |             |                |
| Section label        | mono    |       |        |             |                |
| Body text            | body    |       |        |             |                |
| Card label           | body    |       |        |             |                |
| Card sublabel / meta | mono    |       |        |             |                |
| Slide number         | mono    |       |        |             |                |

---

## 4. Canvas

| Property     | Value | Notes                                  |
|--------------|-------|----------------------------------------|
| Width        |       | in px                                  |
| Height       |       | in px (should produce 16:9 ratio)      |
| Background   |       | CSS token reference                    |
| Overflow     |       | typically `hidden`                     |
| Positioning  |       | `relative` (children use absolute)     |

---

## 5. Layout & Spacing

### Standard Regions

_Define the typical content zones within a slide._

| Region               | Position                          |
|----------------------|-----------------------------------|
| Section label        | `top: ___; left: ___;`            |
| Slide title          | `top: ___; left: ___;`            |
| Content area start   | `top: ___;` (below title)         |
| Content area padding | `left: ___; right: ___;`          |
| Slide number         | `bottom: ___; right: ___;`        |

### Spacing Scale

| Context                  | Value  |
|--------------------------|--------|
| Card gap                 |        |
| Grid gap                 |        |
| Section label to title   |        |
| Title to content         |        |
| Bottom margin (numbers)  |        |

---

## 6. Iconography

### Icon Library

| Property   | Value                                     |
|------------|-------------------------------------------|
| Library    | (e.g. Lucide, Feather, Heroicons, custom) |
| CDN URL    |                                           |
| Init call  | (e.g. `lucide.createIcons()`)             |

### Icon Usage Rules

_Define how icons are used across the deck:_

- Coloring: (monochrome / colored / inherit from parent)
- Default stroke width:
- Size ranges: (small / medium / large with px values)
- Usage in HTML: (e.g. `<i data-lucide="name"></i>`)
- What to avoid: (e.g. no emoji as primary icons, no mixing libraries)

---

## 7. Reusable Atoms

_Define the small, repeated building blocks. For each atom, provide
the CSS class name, a short description, and the CSS declaration._

### Section Label

```css
.section-label {
  /* fill in */
}
```

### Slide Title

```css
.slide-title {
  /* fill in */
}
```

### Accent Line

_Horizontal bar for visual separation._

```css
.accent-line {
  /* fill in */
}
```

### Accent Bar Left

_Full-height left edge bar on hero slides (if used)._

```css
.accent-bar-left {
  /* fill in */
}
```

### Dot Grid / Decorative Element

_Any decorative texture element (dots, lines, shapes). Remove if unused._

```css
.dot-grid {
  /* fill in */
}
```

### Slide Number

```css
.slide-number {
  /* fill in */
}
```

---

## 8. Component Library

_Define every reusable component pattern available for slide authors.
For each component, provide: name, purpose, HTML structure, and any
variant classes._

### Component: (Name)

**Purpose**: ...

**HTML**:
```html
<!-- structure -->
```

**Variants**: (list variant classes and what they change)

**Rules**: (any constraints on usage)

---

_(Copy the component block above for each component in the system.
Common components include: info card, pain/problem card, numbered list,
data table, flow lane, hub/satellite diagram, status card, tag/badge,
comparison columns, timeline, maturity ring, etc.)_

---

## 9. Link Styling

| State   | Style                                          |
|---------|-------------------------------------------------|
| Default |                                                 |
| Hover   |                                                 |
| Target  | (e.g. `target="_blank"` on all external links)  |

---

## 10. Presentation Mode

_Define the behavior when the deck enters fullscreen/presentation mode._

| Property            | Value                                    |
|---------------------|------------------------------------------|
| Background          |                                          |
| Scaling method      | (e.g. `transform: scale()` proportional) |
| Navigation keys     |                                          |
| Enter key           |                                          |
| Exit key            |                                          |
| Fullscreen API      | (yes / no)                               |

---

## 11. Do / Don't Rules

### Do

- ...
- ...
- ...

### Don't

- ...
- ...
- ...

---

## 12. Checklist Before Building

Before creating any slides, confirm all of the following are true:

- [ ] Every color token in section 2 has a hex value
- [ ] Every font in section 3 has a family, fallback, and loading method
- [ ] The type scale in section 3 is fully filled in
- [ ] Canvas dimensions in section 4 are set
- [ ] At least the section label, slide title, and slide number atoms are defined
- [ ] At least one component is documented in section 8
- [ ] Icon library is specified with CDN URL and init call
- [ ] Presentation mode behavior is documented
- [ ] `design/styles.css` contains the CSS implementing all tokens and atoms above
