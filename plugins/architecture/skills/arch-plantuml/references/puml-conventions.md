# PlantUML conventions

The `docs/architecture/diagrams/` folder is the **single source of truth** for every PlantUML diagram in the project. These conventions keep multi-skill authoring (`arch-uml` writes; consuming skills embed) consistent and grep-friendly.

Authoritative grammar: [plantuml.com](https://plantuml.com). This file lists the **kit-specific rules** layered on top of the official syntax.

---

## 1. File naming — `<type>-NN-<slug>.puml`

One diagram per file. The filename encodes the diagram type, an ordering number, and a slug:

| Diagram type | Prefix | Example filename | Renders to |
|---|---|---|---|
| Sequence | `seq-` | `seq-01-claim-submission.puml` | `views/seq-01-claim-submission.svg` |
| Class | `class-` | `class-01-claims-domain.puml` | `views/class-01-claims-domain.svg` |
| State machine | `state-` | `state-01-claim-lifecycle.puml` | `views/state-01-claim-lifecycle.svg` |
| Activity | `act-` | `act-01-claim-triage.puml` | `views/act-01-claim-triage.svg` |
| Entity-relationship | `er-` | `er-01-claims-schema.puml` | `views/er-01-claims-schema.svg` |
| Use case | `uc-` | `uc-01-claims-portal.puml` | `views/uc-01-claims-portal.svg` |
| Component / object *(rare — prefer C4)* | `comp-` / `obj-` | `comp-01-...` | `views/comp-01-...svg` |

- **`NN`** is a two-digit, zero-padded ordering counter **per type** (`seq-01`, `seq-02`, …). It is **not** a metamodel ID — it only orders diagrams of the same type. `arch-uml` finds the next number by listing existing files of that prefix.
- **The view key is the filename stem.** PlantUML writes `views/<stem>.svg`, so the filename *is* the embed path. Keep filenames stable — the consuming markdown references them by relative path.
- Slugs are kebab-case, lowercase, no spaces.

---

## 2. The `_`-prefix include rule (critical)

Any file whose name starts with `_` is an **include fragment, not a renderable diagram**:

- `_theme.puml` — the shared skinparam theme.
- `_<name>.puml` — any other shared fragment (reusable participant lists, macros).

`render.sh` **never renders `_*.puml`** (they have no `@startuml`/`@enduml` and would error). Includes are pulled into a diagram with `!include`.

---

## 3. Diagram skeleton — every `.puml` looks like this

```plantuml
@startuml
!include _theme.puml
title UC-01 — Claims Portal (use case diagram)

' ... diagram body ...

@enduml
```

Rules:
1. **`@startuml` / `@enduml` wrap every diagram.** Exactly one pair per renderable file.
2. **`!include _theme.puml` is the first line after `@startuml`.** It pulls in the shared theme so every diagram looks consistent. The path is relative to the `.puml` file, so a bare `_theme.puml` works (both live in `diagrams/`).
3. **`title` carries the upstream ID + a human name.** See §4.
4. Do **not** put a filename after `@startuml` (e.g. `@startuml foo`) — it overrides the output name and breaks the view-key convention. Let the filename drive the output.

---

## 4. Cross-references — diagrams visualise other artefacts' IDs

`arch-uml` mints **no IDs of its own**. A PlantUML diagram visualises IDs that already belong to upstream artefacts. Carry those IDs verbatim into the diagram so a reader can cross-reference:

| Diagram | Carries | Owning skill |
|---|---|---|
| Use case (`uc-`) | `UC-NN` in the `title` and on each use-case ellipse; `P-NN` on actors | `spec-use-case`, `business-persona` |
| State machine (`state-`) | `BC-NN.AGG-NN` aggregate in the `title` | `domain-model` |
| Class (`class-`) | Aggregate / entity names from the domain model | `domain-model` |
| ER (`er-`) | Entity names; note the bounded context in the `title` | `domain-model` |
| Sequence (`seq-`) | The scenario / use-case reference in the `title` | `spec-use-case`, `business-process` |
| Activity (`act-`) | The process ID (`PROC-NN`) in the `title` | `business-process` |

**Soft-reference principle** (same as the rest of the kit): a diagram references upstream IDs as labels, not as hard prerequisites. Author a diagram even if the upstream artefact is informal; add the IDs to titles/labels when they exist.

---

## 5. One concern per diagram

PlantUML will happily render a 40-actor use-case diagram or a 60-class model — and it will be unreadable. Keep each `.puml` to **one coherent concern** (one scenario, one bounded context's aggregates, one aggregate's lifecycle). If a diagram needs scrolling to read, split it into two numbered files of the same type. Layout discipline lives in `arch-uml`'s `references/diagram-discipline.md`.

---

## 6. When to split vs keep one folder

Default: **one flat `diagrams/` folder**. Easy globbing, one render invocation, predictable view keys.

Sub-folders are only worth it past ~25 diagrams; if you split, keep `render.sh` and `_theme.puml` at the `diagrams/` root and have it recurse. `arch-plantuml` does not split automatically — splitting is a manual refactor.

---

## 7. Sources

- [PlantUML — Command line](https://plantuml.com/command-line) — `-tsvg`, `-o`, `-checkonly`, `-failfast2`.
- [PlantUML — Preprocessing (`!include`)](https://plantuml.com/preprocessing) — include semantics, relative paths.
- [PlantUML — Sequence / Class / State / Activity / Use-case syntax](https://plantuml.com) — per-type grammar.
