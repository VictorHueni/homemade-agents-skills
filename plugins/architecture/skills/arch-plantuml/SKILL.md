---
name: arch-plantuml
description: "Initialise and maintain the PlantUML diagrams workspace + Docker-based render pipeline that powers UML diagrams (sequence, class, state-machine, activity, ER, use-case) — the diagram types Mermaid renders poorly and Structurizr does not cover. One-time setup skill: scaffolds docs/architecture/diagrams/{*.puml, _theme.puml, render.sh, README.md, views/}, pins the official plantuml/plantuml Docker image, and provides a validate→render pipeline (.puml → SVG). Companion to arch-uml, which authors the diagrams going forward. Triggers on: scaffold plantuml, init plantuml, plantuml workspace, set up plantuml, plantuml render pipeline, plantuml docker, uml render pipeline, plantuml foundation, diagrams folder. NOT for C4 architecture diagrams (arch-c4 / arch-structurizr) nor GitHub-inline diagrams (Mermaid)."
version: "1.0.0"
status: active
last_reviewed: 2026-06-09
review_interval: 365d
user-invocable: true
impact: "low"
metadata:
  category: "architecture"
  complexity: "medium"
---

# PlantUML diagrams workspace + render pipeline

This is the **foundation** for every UML diagram the kit produces with PlantUML. It scaffolds the `docs/architecture/diagrams/` folder and the single-image Docker render pipeline (`.puml` → SVG). After `init` runs once, the `arch-uml` skill authors `.puml` files going forward; `arch-plantuml` does not author diagrams itself.

It is the structural twin of `arch-structurizr`:

| Structurizr pair | PlantUML pair | Role |
|---|---|---|
| `arch-structurizr` | **`arch-plantuml`** *(this skill)* | One-time scaffold: filesystem layout, pinned Docker version, render script, shared theme, conventions. |
| `arch-c4` | `arch-uml` | Per-diagram authoring: writes `.puml` files, runs `render.sh`, embeds SVGs into markdown. |

## Why PlantUML at all (the kit is Mermaid-first)

`rules/diagramming-mermaid.md` makes Mermaid the default for GitHub-inline diagrams — it renders natively on GitHub and stays diff-friendly. PlantUML earns its place **only** for the diagram types Mermaid renders poorly and Structurizr does not cover, rendered to **committed SVG** (the same pre-render trade-off `arch-structurizr` already legitimises):

- **Sequence** diagrams with rich activation/grouping/`alt`/`par` semantics
- **Class** diagrams (associations, generalization, multiplicities)
- **State-machine** diagrams (composite/nested states, history)
- **Activity** diagrams (swimlanes, fork/join)
- **Entity-Relationship** diagrams
- **Use-case** diagrams (actors, `«include»`/`«extend»`) — this finally gives `spec-use-case` a way to render the UML use-case diagrams it already references.

**Out of scope (do not duplicate existing tooling):**

| Want | Use instead |
|---|---|
| C4 context / container / component / deployment / runtime | `arch-c4` (+ `arch-structurizr` pipeline) |
| A GitHub-inline diagram that renders in the markdown itself | Mermaid (`rules/diagramming-mermaid.md`) |
| Interactive HTML board / canvas / timeline | `com-artefact-viz` |

## Why two skills instead of one

| Skill | Role | Frequency |
|---|---|---|
| `arch-plantuml` | One-time scaffold: folder, pinned Docker version, render script, shared `_theme.puml`, conventions. | Once per project (re-run only on `upgrade`). |
| `arch-uml` | Per-diagram authoring: writes one `.puml` per diagram, runs `render.sh`, embeds the SVG into the consuming markdown. | Many times — every time a diagram is needed. |

The split mirrors structurizr/c4: **authoring (`.puml` editing) is separate from generation (the Docker pipeline)**.

## What the analogy bends on (read this)

Structurizr has **one** `workspace.dsl` = one shared model that `arch-c4` keeps extending. PlantUML has **no shared model** — each diagram is an independent `.puml` file. So:

- The "single source of truth" is the **`diagrams/` folder of independent `.puml` files**, not one file.
- Visual consistency is held by a shared **`_theme.puml`** that every diagram `!include`s (the analog of Structurizr's `styles{}` block). `arch-plantuml` owns that theme; `arch-uml` authors against it.
- Files whose name starts with `_` are **includes, not diagrams** — `render.sh` never renders them.

## Output the skill produces

```
docs/architecture/diagrams/
├── _theme.puml          ← shared skinparam theme, !include'd by every diagram
├── render.sh            ← single-image Docker pipeline (executable)
├── README.md            ← how to render locally; pinned version; conventions
├── *.puml               ← individual diagrams (authored by arch-uml)
└── views/               ← rendered SVGs (committed)
    └── .gitkeep
```

The skill does **not** author any diagram — that is `arch-uml`'s job. `init` seeds **one** example diagram (`seq-00-example.puml`) purely to prove the pipeline renders, then `verify` removes nothing (the example stays as a living smoke test until `arch-uml` adds real diagrams).

## Pipeline (read this before editing render.sh)

The official [`plantuml/plantuml`](https://hub.docker.com/r/plantuml/plantuml) image bundles `plantuml.jar` + a JRE + **Graphviz** (needed for class/state/activity/component layout — sequence diagrams do not need it). One image, one pass:

```
diagrams/*.puml
   │
   │  docker run plantuml/plantuml:<pin>
   │      -checkonly -failfast2   (validate)
   │
   │  docker run plantuml/plantuml:<pin>
   │      -tsvg -failfast2 -o <abs>/views  diagrams/*.puml
   ▼
diagrams/views/*.svg     ← committed; embedded in consuming markdown
```

A **`-checkonly` validation** runs before render on every invocation. If any `.puml` fails to parse, render does not run and the script exits non-zero with the offending file.

**No Chromium, no headless browser.** Unlike the Structurizr `-playwright` image (~1.8 GB), `plantuml/plantuml` renders SVG directly from the jar. The image is a few hundred MB and a full render of a handful of diagrams completes in **~1–3 seconds** once pulled.

## Modes

### Mode 1 — `init` (default)

Scaffold the `docs/architecture/diagrams/` tree from `templates/`. Pin the Docker image version in `render.sh`. Make `render.sh` executable.

**Steps:**
1. Verify `docs/architecture/` exists (create if missing).
2. If `docs/architecture/diagrams/render.sh` already exists, **abort** and recommend `verify` or `upgrade` instead. Never overwrite an existing pipeline.
3. Copy `templates/diagrams/_theme.puml` → `docs/architecture/diagrams/_theme.puml`.
4. Copy `templates/diagrams/seq-00-example.puml` → `docs/architecture/diagrams/seq-00-example.puml` (the smoke-test diagram).
5. Copy `templates/render.sh` → `docs/architecture/diagrams/render.sh` with `{{plantuml_version}}` substituted from the pin table in `references/docker-pipeline.md`. `chmod +x` it.
6. Copy `templates/plantuml-readme.md` → `docs/architecture/diagrams/README.md` with the same substitution.
7. Create `docs/architecture/diagrams/views/.gitkeep`.
8. Run Mode 2 (`verify`) automatically to confirm the scaffold renders.
9. Print a closing report (see §Closing report) and point the user at `arch-uml` for authoring.

### Mode 2 — `verify`

Confirm the scaffold + Docker image + diagrams all render. Read-only — never edits files.

**Steps:**
1. Check that `docs/architecture/diagrams/{render.sh, README.md, _theme.puml, views/}` all exist.
2. Check that `render.sh` is executable.
3. Check that `render.sh` pins a concrete version (not `:latest`). Flag deviation.
4. Check Docker availability: `docker version` returns 0.
5. Check that the pinned `plantuml/plantuml:<pin>` image is present or pullable: `docker image inspect plantuml/plantuml:<pin> 2>/dev/null || docker pull plantuml/plantuml:<pin>`.
6. Run `./docs/architecture/diagrams/render.sh --dry-run` (validates every `.puml` with `-checkonly`). Surface any parse error with its filename.
7. Optionally run a full `./render.sh` and confirm at least one SVG lands under `views/`.
8. Report pass/fail per check.

### Mode 3 — `upgrade`

Bump the pinned Docker image version in `render.sh`, then re-render all diagrams to detect any visual change from the renderer.

**Steps:**
1. Read the current pin from `docs/architecture/diagrams/render.sh`.
2. Show the recommended new pin from `references/docker-pipeline.md` (kit-maintained pin table).
3. Ask the user to confirm the bump.
4. Edit `render.sh` to update the pin.
5. Run Mode 2 (`verify`) with the new pin.
6. Run `./render.sh` to re-render all diagrams; report any view that produced different SVG output (`git diff --stat docs/architecture/diagrams/views/`).
7. Recommend committing the render-script bump + any re-rendered SVGs together so reviewers can correlate.

## Cross-references

- `arch-uml` (companion skill) — authors `.puml` diagrams, runs `render.sh`, embeds SVGs into the consuming markdown. Always check that `arch-plantuml init` has run first.
- `arch-structurizr` / `arch-c4` — the C4 toolchain. PlantUML does **not** draw C4 here; defer to those.
- `spec-use-case` — its UML use-case diagrams are rendered by `arch-uml` through this pipeline.
- `domain-model` — class / state-machine / ER diagrams for the domain are rendered here.
- `rules/diagramming-mermaid.md` — the Mermaid-first policy; this skill is the sanctioned exception for rich UML rendered to SVG.
- the `metamodel` skill — supporting-skills list entry + canonical path `docs/architecture/diagrams/`.

## Optional — PlantUML MCP server

Community MCP servers (e.g. `infobip/plantuml-mcp-server`, `antoinebou12/uml-mcp`) expose PlantUML render / encode / lint as MCP tools an agent can call directly (no shell-out). Setting one up is **optional** — `arch-plantuml` + `arch-uml` work without it via `docker run`.

See `references/mcp-optional.md` for the trade-off and setup instructions if you want the MCP path.

## Reference materials

- `references/puml-conventions.md` — filename convention (`<type>-NN-<slug>.puml`), view-key = filename stem, the `_`-prefix include rule, `@startuml/@enduml` + `!include _theme.puml` discipline, kit cross-reference rules (carry upstream IDs in titles).
- `references/docker-pipeline.md` — render.sh contract, pinned version, volume-mount conventions, exit codes, troubleshooting, CI hook recommendations.
- `references/mcp-optional.md` — optional PlantUML MCP server setup.

## Closing report

After each mode, deliver:

- Mode executed (init / verify / upgrade)
- Files created or modified (list)
- Pinned version: `plantuml/plantuml:<pin>`
- Validation/render result (which diagrams rendered)
- Next step: `arch-uml <type>` (if init) or commit (if upgrade)

## Checklist

- [ ] `docs/architecture/diagrams/` exists with `render.sh`, `README.md`, `_theme.puml`, `views/.gitkeep`
- [ ] `render.sh` is executable + pins a concrete version (not `:latest`)
- [ ] `docker version` succeeds in the verify step
- [ ] `--dry-run` (`-checkonly`) passes on the seed diagram(s)
- [ ] Initial `render.sh` run produces at least one SVG under `views/`
- [ ] `README.md` documents the pinned version + the manual render command + the `_`-prefix include rule
- [ ] User reminded that `arch-uml` is the next skill to invoke
