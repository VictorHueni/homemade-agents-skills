---
name: com-artefact-viz
description: "Render canonical kit artefacts into single-file, self-contained interactive HTML views via a shared Python pipeline and a token-driven design system. Five pluggable renderers: capability map (L0-grouped cards + directional left-axis band), delivery roadmap (phase-column timeline + walking-skeleton band + expandable per-epic features), functional breakdown structure (collapsible tree with horizontal/vertical toggle + status badges), Business Model / Lean Canvas (9-block grid), and service blueprint (a composition lens over business-process + value-stream + persona docs: a swimlane grid with the line of visibility, phase columns, pain overlays, and a cross-actor handoff spine). Styling is delegated to the project design system — renderers emit only semantic classes and var() tokens, so one CSS sheet re-themes every view. Use when the user wants a web view, visualisation, board, timeline, canvas, swimlane, or shareable HTML of a capability map, FBS, delivery roadmap, BMC, Lean Canvas, or service blueprint. Triggers on: visualise capability map, render FBS tree, roadmap timeline view, BMC canvas HTML, service blueprint, swimlane view, line of visibility, artefact visualisation, com-artefact-viz. Do NOT use for slide decks (com-slide-deck) or C4 diagrams (arch-c4)."
version: "1.0.0"
status: active
last_reviewed: 2026-05-29
review_interval: 180d
user-invocable: true
allow_implicit_invocation: true
impact: "low"
metadata:
  category: "communication"
  complexity: "medium"
---

# com-artefact-viz — Artefact Web Visualiser

Turn the kit's canonical Markdown artefacts into single-file, self-contained
interactive HTML views. The source Markdown stays the single source of truth;
each view is a **derived, regenerable read-out** — never a second place to edit
content.

This skill is a **portable toolkit**: it lives in its own versioned folder and
generates output into a project's `docs/communication/visualisations/`. It
never contains project-specific content.

```
Markdown artefact ──(parser)──> normalized model ──(renderer)──> one HTML file
   (source of truth)              scripts/parsers      scripts/renderers
```

## Supported artefacts

| Kind (`--kind`) | Source skill | Canonical path | View |
|---|---|---|---|
| `capability-map` | `business-capability-map` | `docs/business/03a-capability-map.md` | L0-grouped capability cards + directional left-axis band; importance colour-coding |
| `fbs` | `spec-functional-breakdown-structure` | `docs/product-specs/07a-fbs.md` | Collapsible tree, horizontal⇄vertical toggle, ✅/🔄/⬜ status badges + counts |
| `delivery-roadmap` | `plan-delivery-roadmap` | `docs/plans/delivery-roadmap.md` | Phase-column timeline, walking-skeleton band, pain-coded epic cards with expandable features/stories |
| `bmc` | `business-model-canvas` | `docs/business/02a-bmc.md` / `02a-lean-canvas.md` | Classic 9-block canvas grid (BMC + Lean variants), confidence colour-coding |
| `service-blueprint` | `business-process` + `business-value-stream` + `business-persona` *(composition)* | `docs/communication/visualisations/service-blueprint.html` | Swimlane grid (evidence · customer · frontstage · backstage · systems) with the **line of visibility**, value-stream phase columns, pain overlays, and a cross-actor handoff spine |

It produces **communication artefacts** (the `com-` prefix → `docs/communication/`),
mints no IDs, and is not a step in the strategic-architecture build order — it is
a supporting skill, like `com-slide-deck`.

### Service blueprint — a composition lens (multi-source)

Four of the kinds render **one** source file. `service-blueprint` is different:
it **composes several** canonical artefacts into the one cross-process,
customer-visibility view none of them gives alone — and it restates nothing.
It reads the `business-process` doc(s) for actors, systems, steps, handoffs and
pain points; drapes them under `business-value-stream` phase columns; and
**derives the only thing no source carries — the line of visibility — from
`business-persona` type** (a `Customer`/`Served` persona → customer lane; other
resolved actors → front- or back-stage by whether they exchange a data object
with the customer; system-named actors → systems lane). Actors it cannot
classify are surfaced in an **Unclassified** band with a badge — never guessed.
Because the classification is derived, **it changes no source doc**; to move an
unclassified actor, set its `Persona type` in the persona doc and re-render.

Invoke it with `--proc` (repeatable), an optional `--value-stream`, and
`--personas` (a file or a folder):

```bash
python scripts/render.py --kind service-blueprint \
  --proc docs/business/05a-processes/proc-03-slot-rebooking.md \
  --value-stream docs/business/04a-value-stream.md \
  --personas docs/business/03b-personas/
```

Without `--value-stream`, phase columns fall back to the §6 step order. A
worked multi-file fixture lives in `examples/service-blueprint/`.

---

## Quick reference

| Task | Command |
|---|---|
| Render an artefact (auto-detect kind) | `python scripts/render.py docs/business/03a-capability-map.md` |
| Force the kind | `python scripts/render.py SRC.md --kind fbs` |
| Compose a service blueprint | `python scripts/render.py --kind service-blueprint --proc PROC.md --value-stream VS.md --personas PERSONAS/` |
| Theme from the shared design system | automatic — `docs/ux/tokens.css` (from the `ux-design-system` skill) is auto-detected |
| Theme with a specific sheet | `python scripts/render.py SRC.md --design-system path/to/styles.css` |
| Override the capability/FBS left-axis label | `python scripts/render.py SRC.md --left-axis-label "Customer Journey" --left-axis-arrow "→"` |
| Choose the output path | `python scripts/render.py SRC.md --out docs/communication/visualisations/capability-map.html` |
| Just print the detected kind | `python scripts/render.py SRC.md --detect` |
| Live preview while editing | `python scripts/dev_server.py docs/business/03a-capability-map.md` |

Default output: `docs/communication/visualisations/<kind>.html`.

---

## How to run it (operating sequence)

1. **Locate the source artefact.** It must be the canonical Markdown produced
   by the owning skill (see the table above). If the artefact does not exist
   yet, stop and point the user at the skill that builds it — this skill
   visualises, it does not author.
2. **Pick or confirm the design system.** Resolution order: (a) an explicit
   `--design-system PATH`; (b) the shared `docs/ux/tokens.css` produced by
   the **`ux-design-system`** skill, auto-detected if present (the view prints
   "using shared design system …"); (c) the skill's shipped defaults
   (`templates/tokens.fallback.css`). The project sheet's `:root` tokens are
   inlined over the fallback and win. Prefer the shared `ux-design-system` skill so decks and
   views theme from one source; you can still point `--design-system` at a
   `com-slide-deck` `design/styles.css`. This is the supported way to make
   every view match the project's look.
3. **Render.** Run `scripts/render.py`. One self-contained HTML file is written
   (all CSS + JS inlined — no runtime, no network, diff-friendly, shareable).
4. **Verify in a browser.** Open the file. Check the verification list below.
5. **Re-render after the source changes.** Views never drift silently because
   they carry no authored content — re-run the same command.

---

## Templating model (three layers)

The pipeline keeps parsing, structure, and styling independent so each can
evolve alone:

1. **Design tokens** — layered like `com-slide-deck`: `templates/tokens.fallback.css`
   (shipped generic contract — base palette, `--success`/`--warning`/`--danger`/
   `--info`, typography, spacing) is inlined first; the project sheet
   (`docs/ux/tokens.css` or `--design-system`) is inlined over it and wins;
   then `templates/tokens.domain.css` maps viz's domain names
   (`--status-shipped: var(--success)`, `--pain-critical: var(--danger)`, …) onto
   the generics. **Renderers reference only `var(--token)` — never a literal
   colour, font, or radius.** That contract is what makes re-theming a one-file
   operation (theme the four generics; every view follows).
2. **Base layout** — `templates/base.html.tmpl` is the shell with slots
   (`{{TITLE}}`, `{{KIND}}`, `{{META}}`, `{{TOOLBAR}}`, `{{CONTENT}}`,
   `{{DESIGN_SYSTEM_CSS}}`, `{{VIEW_CSS}}`, `{{RUNTIME_JS}}`, `{{FOOTER}}`).
   Everything is inlined into the slots → one portable file per view.
3. **Pluggable renderers** — `scripts/renderers.py` has one function per kind
   that turns a model dict into the content fragment + view-scoped CSS +
   toolbar. The **parser layer** (`scripts/parsers.py`) turns canonical
   Markdown into that model. When a source skill's output template changes,
   only the matching parser changes; renderers and templates stay put.

To add a new artefact type later: add a `parse_*` to `parsers.py` (register it
in `PARSERS` + `detect_kind`), add a `render_*` to `renderers.py` (register it
in `RENDERERS`), and add a `.sample.md` fixture under `examples/`. No template
or design-system change is needed.

---

## Behaviour notes per renderer

- **Capability map.** Hierarchy comes from the artefact's `## Global overview`
  ASCII tree (nesting derived from the `C-N.M` ID depth, robust to indentation).
  Strategic importance + one-line definitions are joined in from the
  `## Capability index` table. The **left-axis band** defaults to the declared
  L0 axis and is overridable per project via `--left-axis-label` /
  `--left-axis-arrow` (the "arrow text varies by project" requirement).
- **FBS.** Same overview tree, with functionalities attached from each
  capability's table; status maps ✅→shipped, 🔄→planned, ⬜→backlog. The
  toolbar toggles orientation (vertical⇄horizontal), expand-all, collapse-all;
  individual nodes collapse on click.
- **Delivery roadmap.** Phases become timeline columns; epics are bucketed by
  their `Phase` column (falling back to the phase-plan epic list). Epic cards
  carry a pain-coded left stripe and an expandable list of FBS scope rows
  (features/stories). The walking-skeleton band shows hypothesis + can/cannot.
- **BMC / Lean Canvas.** Blocks are placed into the classic canvas grid via
  `grid-template-areas`, with separate layouts for BMC and Lean variants; the
  alternate variant's blocks are dropped. Confidence (Assumed/Tested/Validated)
  is colour-coded. The grid collapses to two columns on narrow viewports.

---

## Verification checklist

1. [ ] Source artefact is the canonical Markdown for its kind (right path/skill).
2. [ ] `--detect` (or auto-detect) resolves the intended kind.
3. [ ] Output opens in a browser with no console errors and no missing styles.
4. [ ] Every expected element is present (groups/nodes/phases/blocks — compare to source).
5. [ ] Project design system, if supplied, visibly themes the view (`--design-system`).
6. [ ] Interactive controls work (FBS orientation + collapse; epic feature disclosure).
7. [ ] Re-rendering after a source edit reflects the change (no stale authored content).
8. [ ] *(service-blueprint)* `--proc` resolves; ≥1 customer and ≥1 frontstage/backstage lane; the three control lines sit between the right bands; any **Unclassified** actor is one whose `Persona type` is missing in the source persona doc (fix there, not in the view); phase columns match the value stream (or note the §6 fallback); handoff spine lists the cross-actor data objects.

---

## Dependencies

- Python 3.8+ (standard library only — no third-party packages, no Node).

---

## Follow-up work

Planned enhancements, deferred refinements, and decisions for this skill are
tracked as central-only rows in the kit's ledger at
`docs/project-control/open-items/open-items.md` (per `rules/open-items-governance.md`
§9) — not in this folder. This skill resolves `OI-0010` (cross-skill web
visualisations).

## See also

- `references/parsing-contract.md` — exact Markdown each parser reads, field by field.
- `references/viz-discipline.md` — design principles and boundaries (what this skill is NOT).
- `ux-design-system/SKILL.md` — the shared design system; its `docs/ux/tokens.css` is auto-detected as the theme.
- `com-slide-deck/SKILL.md` — sibling HTML builder; share its `design/styles.css` via `--design-system`.
- `rules/skill-creation-sync.md` · `rules/artefact-frontmatter.md` · `rules/diagramming-mermaid.md`.
