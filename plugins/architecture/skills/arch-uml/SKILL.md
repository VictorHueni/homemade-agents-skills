---
name: arch-uml
description: "Author and refresh UML diagrams with PlantUML — sequence, class, state-machine, activity, entity-relationship, and use-case — rendered to committed SVG via the arch-plantuml Docker pipeline. Writes one docs/architecture/diagrams/<type>-NN-<slug>.puml per diagram (each !includes the shared _theme.puml and titles the upstream ID it visualises), runs render.sh, and embeds the SVG into the consuming markdown. Six modes, one per diagram type. Prerequisite: arch-plantuml init. Mints no IDs — diagrams visualise IDs owned by spec-use-case (UC-NN), domain-model (BC-NN.AGG-NN), business-process (PROC-NN). Triggers on: sequence diagram, class diagram, state machine diagram, activity diagram, ER diagram, use case diagram, UML diagram, plantuml diagram, draw sequence, draw class diagram. NOT for C4 (arch-c4) nor GitHub-inline diagrams (Mermaid)."
version: "1.0.0"
status: active
last_reviewed: 2026-06-09
review_interval: 365d
supersedes: ~
superseded_by: ~
user-invocable: true
allow_implicit_invocation: true
impact: "low"
metadata:
  category: "architecture"
  complexity: "high"
---

# UML diagram authoring with PlantUML

Single skill, six modes — one per UML diagram type. Each diagram is an independent `.puml` file under `docs/architecture/diagrams/`; this skill writes it, renders it to SVG via `render.sh`, and (optionally) embeds the SVG into the consuming markdown.

This is the authoring twin of `arch-c4`:

| Structurizr pair | PlantUML pair | Role |
|---|---|---|
| `arch-structurizr` | `arch-plantuml` | One-time scaffold: folder, pinned Docker version, render script, shared theme. |
| `arch-c4` | **`arch-uml`** *(this skill)* | Per-diagram authoring: writes `.puml`, runs `render.sh`, embeds SVGs. |

**Prerequisite:** `arch-plantuml init` must have run. If `docs/architecture/diagrams/render.sh` doesn't exist, this skill aborts and points the user there.

---

## What this skill is NOT

- **Not for C4 diagrams.** Context / container / component / deployment / runtime are `arch-c4`'s job (via Structurizr). If the user wants "the architecture diagram," ask whether they mean C4 (→ `arch-c4`) or a UML behavioural/structural diagram (→ here). See `references/diagram-discipline.md`.
- **arc42 §6 runtime — share the section with C4 (ADR-0004).** A `sequence` diagram is a valid arc42 §6 figure, but §6 is owned by `arch-arc42`, and the figure source is governed by a boundary rule: **C4 dynamic view** (`arch-c4 runtime`) for cross-container flows tied to the C4 model; **`arch-uml sequence`** only for intra-component / algorithmic detail needing rich `alt`/`par`/`loop`/composite logic. When `arch-arc42` selects a UML sequence for §6, produce the SVG and hand the path back — it owns the §6 embed and prose.
- **Not a Mermaid replacement.** For a diagram that must render *inline* in GitHub markdown, use Mermaid (`rules/diagramming-mermaid.md`). PlantUML here renders to **committed SVG** — used when Mermaid's grammar is too thin (rich sequence `alt`/`par`, composite states, swimlane activities, full class/ER models).
- **Not an ID minter.** A diagram visualises IDs that already belong to upstream artefacts (`UC-NN`, `BC-NN.AGG-NN`, `PROC-NN`, `P-NN`). Carry them into the `title` and labels; never invent a new ID scheme. The `-NN` in the filename only orders diagrams of the same type.
- **Not a one-off renderer.** Every diagram lives as a `.puml` in the folder so it re-renders deterministically. Direct SVG hand-editing is forbidden — `arch-plantuml verify` flags drift.

---

## The six modes

| Mode | Draws | Filename prefix | Reads upstream | PlantUML element |
|---|---|---|---|---|
| `sequence` | An interaction over time between actors/participants | `seq-` | `spec-use-case` scenario, `business-process` | `participant`, `->`, `alt`/`par`/`loop` |
| `class` | Static structure: classes, attributes, associations | `class-` | `domain-model` aggregates/entities | `class`, `-->`, `--\|>`, multiplicities |
| `state` | An aggregate's lifecycle: states + transitions | `state-` | `domain-model` aggregate lifecycle | `state`, `[*] -->`, composite states |
| `activity` | A process/algorithm flow with branches + swimlanes | `act-` | `business-process` | `start`/`stop`, `if/else`, `\|swimlane\|` |
| `er` | Entity-relationship data model | `er-` | `domain-model` / schema | `entity`, `\|\|--o{` crow's-foot |
| `use-case` | Actors + use cases + `«include»`/`«extend»` | `uc-` | `spec-use-case`, `business-persona` | `actor`, `usecase`, `.>` |

Each mode follows the **same authoring workflow** below; the per-type syntax and pitfalls live in `references/puml-cheatsheet.md` and the readability rules in `references/diagram-discipline.md`.

---

## Authoring workflow (every mode)

1. **Pre-flight.** Confirm `docs/architecture/diagrams/render.sh` + `_theme.puml` exist. If not, stop and point the user at `arch-plantuml init`.
2. **Read the upstream artefact** if present (the "Reads upstream" column). Carry its IDs forward — they go in the diagram `title` and on the relevant elements. If the upstream artefact doesn't exist yet, proceed (soft-reference) and note it in the closing report.
3. **Pick the filename.** `<prefix>-NN-<slug>.puml`. Find the next `NN` by listing existing files of that prefix (e.g. `ls diagrams/seq-*.puml`). Two-digit, zero-padded. Slug is kebab-case.
4. **Write the `.puml`.** Always in this shape:
   ```plantuml
   @startuml
   !include _theme.puml
   title <UPSTREAM-ID> — <human name>

   ' ... body (see references/puml-cheatsheet.md for the type) ...

   @enduml
   ```
   Do **not** write a name after `@startuml` (it overrides the output filename). Apply the layout discipline in `references/diagram-discipline.md` — fewest crossings, one concern per diagram, left-to-right or top-down deliberately.
5. **Validate + render.** Run `./docs/architecture/diagrams/render.sh <prefix>-NN-<slug>`. It runs `-checkonly` first; if the `.puml` doesn't parse, fix it before continuing. On success it writes `views/<prefix>-NN-<slug>.svg`.
6. **Embed (if there's a consuming doc).** Add the SVG to the markdown that needs it, by relative path. Typical consumers:
   - use-case diagram → `docs/product-specs/use-cases/` (alongside the `spec-use-case` file or its `index.md`)
   - class / state / ER → `docs/domain/` (the `domain-model` artefacts), **or arc42 §8** cross-cutting concepts
   - sequence → the scenario's home (`docs/product-specs/use-cases/` or a `business-process` doc), **or arc42 §6** runtime view
   - activity → the `business-process` doc

   Embed syntax (path is relative to the consuming markdown):
   ```markdown
   ![seq-01 — Claim submission](../../architecture/diagrams/views/seq-01-claim-submission.svg)
   ```

   **arc42 consumers are pull-side (ADR-0004).** When the consumer is an arc42 §6 or §8 section, **`arch-arc42` owns the embed** — it writes the `<!-- arch-figure … -->` declared-dependency block and the surrounding prose. In that case `arch-uml` does **not** edit the arc42 file: render the SVG, then report its path (and the `SCN-NN`/`CC-NN`/`UC-NN` it was given) back to `arch-arc42`, which wires it in.

   If there is no obvious consumer, leave the SVG in `views/` and report its path — the user wires it in.
7. **Report** (see §Closing report).

---

## When PlantUML, when Mermaid, when C4 (decide before drawing)

| The diagram is… | Tool | Why |
|---|---|---|
| C4 context/container/component/deployment/runtime | `arch-c4` | Structurizr owns the C4 model + views |
| Must render inline in a GitHub `.md` | Mermaid | GitHub-native, no pre-render step |
| A rich UML diagram (composite states, `alt`/`par` sequences, swimlane activities, full class/ER models) | **`arch-uml`** | Mermaid's grammar is too thin; render to SVG |
| A simple flow/sequence that Mermaid handles fine | Mermaid | Keep it inline + diff-friendly |

The deciding question: *does this need PlantUML's richer grammar, and is a committed SVG acceptable?* If no to either, prefer Mermaid. Full rationale: `references/diagram-discipline.md`.

---

## Reference materials

- `references/puml-cheatsheet.md` — copy-paste-able PlantUML fragments per diagram type (sequence, class, state, activity, ER, use-case), each pre-wired with `!include _theme.puml` and a `title`.
- `references/diagram-discipline.md` — readability + layout best practices (fewest crossings, one concern per diagram, deliberate direction, legend placement) and the hard boundaries vs `arch-c4`, Mermaid, and `domain-model`.

Pipeline + conventions live in the companion skill: `arch-plantuml/references/{puml-conventions.md, docker-pipeline.md}`.

---

## Closing report

After authoring a diagram, deliver:

- Mode + diagram type
- File written: `docs/architecture/diagrams/<name>.puml`
- Render result: `views/<name>.svg` (or the validation error)
- Upstream IDs visualised (`UC-NN`, `BC-NN.AGG-NN`, `PROC-NN`, `P-NN`) — and any that were missing
- Where the SVG was embedded (or "left in views/ — wire it into <doc>")
- Next step: another diagram, or re-render all via `./render.sh`

---

## Checklist

- [ ] `arch-plantuml init` has run (`render.sh` + `_theme.puml` present); else aborted with a pointer
- [ ] Filename follows `<type>-NN-<slug>.puml`; `NN` is the next free number for that type
- [ ] `.puml` opens `@startuml` → `!include _theme.puml` → `title` with the upstream ID
- [ ] No name written after `@startuml` (filename drives the output)
- [ ] One concern per diagram; layout discipline applied (see `diagram-discipline.md`)
- [ ] `render.sh <name>` validated (`-checkonly`) and produced the SVG
- [ ] SVG embedded into the consuming markdown by relative path (or its path reported)
- [ ] No new ID scheme invented; upstream IDs carried verbatim
- [ ] Closing report delivered
