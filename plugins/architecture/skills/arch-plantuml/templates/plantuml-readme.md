# PlantUML diagrams workspace

This folder is the **single source of truth** for every PlantUML (UML) diagram in the project. Each diagram is one `.puml` file; they render to committed SVGs via `./render.sh`.

| File / folder | What it is |
|---|---|
| `*.puml` | Individual UML diagrams (sequence, class, state, activity, ER, use-case). Edit these; never edit the SVGs directly. |
| `_theme.puml` | Shared skinparam theme **`!include`d** by every diagram. Edit it to re-theme every diagram at once. Starts with `_` → never rendered on its own. |
| `render.sh` | Single-image Docker render pipeline (`plantuml/plantuml` — `-checkonly` validate + `-tsvg` render). |
| `views/*.svg` | Rendered diagrams. **Committed.** Embedded by the consuming markdown. |

This is the foundation scaffolded by **`arch-plantuml`**. Diagrams are authored by the **`arch-uml`** skill. For C4 architecture diagrams use `arch-c4` instead; for GitHub-inline diagrams use Mermaid.

---

## Quick start

```bash
# Render every diagram
./render.sh

# Render a single diagram (stem or filename)
./render.sh seq-01-claim-submission

# Validate every diagram + Docker availability without rendering
./render.sh --dry-run
```

The script requires **Docker** — no Java, no local PlantUML, no local Graphviz install (all bundled in the image).

### First-run note

The pinned `plantuml/plantuml` image is a few hundred MB, so the **initial `docker pull` is the only slow step** (usually under a minute). After that, a full render completes in ~1–3 seconds.

---

## Pinned version

| Tool | Pinned version |
|---|---|
| `plantuml/plantuml` | `{{plantuml_version}}` |

To bump this, invoke the **`arch-plantuml upgrade`** skill. Do not edit the pin by hand — the upgrade flow re-renders every diagram to surface visual diffs before you commit.

---

## Conventions

- **Filenames:** `<type>-NN-<slug>.puml` (e.g. `seq-01-claim-submission.puml`, `class-01-claims-domain.puml`, `state-01-claim-lifecycle.puml`, `uc-01-claims-portal.puml`). The filename stem *is* the SVG name and the embed path.
- **The `_` prefix means "include, not diagram."** `_theme.puml` (and any `_*.puml`) is pulled in via `!include` and is never rendered.
- **Every diagram** opens with `@startuml`, then `!include _theme.puml`, then a `title` that carries the upstream ID (e.g. `UC-01`, `BC-01.AGG-02`) so diagrams cross-reference the artefacts they visualise.

Full conventions: the kit's `arch-plantuml/references/puml-conventions.md`.

---

## How to add a new diagram

Prefer the **`arch-uml`** skill — it handles the filename convention, the theme include, layout discipline, and embedding the SVG into the consuming markdown in one pass.

Manually: create `diagrams/<type>-NN-<slug>.puml`:

```plantuml
@startuml
!include _theme.puml
title <ID> — <human name>

' ... diagram body ...

@enduml
```

Then run `./render.sh <type>-NN-<slug>` (single) or `./render.sh` (all).

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `docker: not found` | Install Docker; on WSL2 confirm Docker Desktop integration. |
| `No @startuml found` | You passed an `_*.puml` include to the renderer, or a diagram is missing `@startuml`. `render.sh` excludes includes automatically. |
| Empty / clipped SVG | Diagram too large — split it (one concern per file). |
| `Permission denied` running `render.sh` | `chmod +x render.sh` (some Git configs strip the executable bit). |
| Different SVG output between machines | Confirm both use the pinned version above. Bump via `arch-plantuml upgrade` to converge. |

CI integration, exit codes, and the full pipeline contract live in the kit's `arch-plantuml/references/docker-pipeline.md`.
