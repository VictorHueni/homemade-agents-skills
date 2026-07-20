---
name: arch-structurizr
description: "Initialise and maintain the Structurizr DSL workspace + Docker-based render pipeline that powers C4 diagrams for arc42 §3 (Context), §5 (Building Blocks), and §7 (Deployment). One-time setup skill: scaffolds docs/architecture/c4/{workspace.dsl, render.sh, README.md, views/}, pins official Structurizr CLI + PlantUML Docker image versions, and provides a validate→export→render pipeline (workspace.dsl → C4-PlantUML → SVG). Companion to arch-c4, which edits the DSL going forward. Triggers on: scaffold structurizr, init structurizr, structurizr workspace, c4 workspace, set up structurizr, structurizr DSL setup, structurizr render pipeline, structurizr docker, c4 render pipeline, structurizr foundation. NOT for creating C4 model elements (that is arch-c4)."
version: "1.0.0"
status: active
last_reviewed: 2026-05-28
review_interval: 365d
supersedes: ~
superseded_by: ~
user-invocable: true
allow_implicit_invocation: true
impact: "low"
metadata:
  category: "architecture"
  complexity: "medium"
---

# Structurizr workspace + render pipeline

This is the **foundation** for every C4 / arc42-architecture diagram the kit produces. It scaffolds the Structurizr DSL workspace and the two-stage Docker render pipeline. After `init` runs once, the `arch-c4` skill edits `workspace.dsl` going forward; `arch-structurizr` does not author C4 model elements itself.

## Why two skills instead of one

| Skill | Role | Frequency |
|---|---|---|
| `arch-structurizr` | One-time scaffold: filesystem layout, pinned Docker versions, render script, conventions. | Once per project (re-run only on `upgrade`). |
| `arch-c4` | Per-view authoring: adds people, systems, containers, components, deployment nodes; runs `render.sh`; embeds SVGs into arc42 §3/§5/§7 markdown. | Many times — every time the architecture evolves. |

## Output the skill produces

```
docs/architecture/c4/
├── workspace.dsl        ← Structurizr DSL — single source of truth
├── render.sh            ← Single-image Docker pipeline (executable)
├── README.md            ← How to render locally; pinned version; view aliases
└── views/               ← Rendered SVGs (committed)
    └── .gitkeep
```

The skill does **not** create any arc42 markdown — that is `arch-c4`'s job.

## Pipeline (read this before editing render.sh)

The consolidated [Structurizr vNext](https://www.patreon.com/posts/introducing-146923136) tool exports SVG directly via a bundled headless Chromium runtime, available in the `-playwright` image variant. The pipeline is a single image, two subcommands:

```
workspace.dsl
   │
   │  docker run structurizr/structurizr:<pin>-playwright
   │      validate -workspace c4/workspace.dsl
   │
   │  docker run structurizr/structurizr:<pin>-playwright
   │      export -workspace c4/workspace.dsl
   │             -format svg
   │             -output c4/views/
   ▼
c4/views/*.svg         ← committed; embedded in arc42 markdown
```

A **`validate`** step runs before `export` on every invocation. If the DSL fails validation, render does not run and the script exits non-zero with a clear error.

**First-time note:** the `-playwright` image is ~1.8 GB (Chromium runtime is bundled, not downloaded on demand). The initial `docker pull` takes 3–5 minutes; afterwards renders complete in 5–10 seconds. The base `structurizr/structurizr:<pin>` (no `-playwright` suffix) lacks Chromium and cannot export SVG — `render.sh` and `verify` mode require the Playwright variant.

The old EOL Docker images (`structurizr/cli`, `structurizr/lite`) and the old two-stage pipeline (`structurizr-cli` → C4-PlantUML → `plantuml/plantuml` → SVG) are not used — the consolidated tool replaces them ([docs/export/png-and-svg](https://docs.structurizr.com/export/png-and-svg)).

## Modes

### Mode 1 — `init` (default)

Scaffold the `docs/architecture/c4/` tree from `templates/`. Substitute the project name + description into `workspace.dsl`. Pin Docker image versions in `render.sh`. Make `render.sh` executable.

**Steps:**
1. Verify `docs/architecture/` exists (create if missing).
2. If `docs/architecture/c4/workspace.dsl` already exists, **abort** and recommend `verify` or `upgrade` instead. Never overwrite an existing DSL.
3. Resolve project name: from `docs/VISION.md` if present (read `title:` frontmatter), else from the current git remote origin name, else prompt.
4. Copy `templates/workspace.dsl` → `docs/architecture/c4/workspace.dsl` with `{{project_name}}` and `{{project_description}}` substituted.
5. Copy `templates/render.sh` → `docs/architecture/c4/render.sh` with `{{structurizr_version}}` substituted from the pin table in `references/docker-pipeline.md`. `chmod +x` it.
6. Copy `templates/c4-readme.md` → `docs/architecture/c4/README.md` with the same substitution.
7. Create `docs/architecture/c4/views/.gitkeep`.
8. Run Mode 2 (`verify`) automatically to confirm the scaffold works.
9. Warn the user that the initial `docker pull` for the `-playwright` image is ~1.8 GB (~3–5 min one-time cost); renders themselves are ~5–10 s once cached.
10. Print a closing report (see §Closing report).

### Mode 2 — `verify`

Confirm the scaffold + Docker image + DSL all work. Read-only — never edits files.

**Steps:**
1. Check that `docs/architecture/c4/workspace.dsl`, `render.sh`, `README.md`, `views/` all exist.
2. Check that `render.sh` is executable.
3. Check that `render.sh` pins the **`-playwright`** variant (not the base tag, not `:latest`). Flag deviation.
4. Check Docker availability: `docker version` returns 0.
5. Check that the pinned `structurizr/structurizr:<pin>-playwright` image is pullable: `docker image inspect structurizr/structurizr:<pin>-playwright 2>/dev/null || docker pull structurizr/structurizr:<pin>-playwright`.
6. Run `docker run --rm -v $PWD:/work structurizr/structurizr:<pin>-playwright validate -workspace /work/docs/architecture/c4/workspace.dsl`. If it fails, surface the validation error.
7. Optionally, run `./docs/architecture/c4/render.sh --dry-run`.
8. Report pass/fail per check.

### Mode 3 — `upgrade`

Bump the pinned Docker image version in `render.sh`, re-render all existing views to detect any breaking changes from the renderer.

**Steps:**
1. Read the current pin from `docs/architecture/c4/render.sh`.
2. Show the recommended new pin from `references/docker-pipeline.md` (kit-maintained pin table).
3. Ask the user to confirm the bump.
4. Edit `render.sh` to update the pin (preserve the `-playwright` suffix).
5. Run Mode 2 (`verify`) with the new pin.
6. Run `./render.sh` to re-render all views; report any view that produced different SVG output (`git diff --stat docs/architecture/c4/views/`).
7. Recommend committing the render-script bump + any re-rendered SVGs together so reviewers can correlate.

## Cross-references

- `arch-c4` (companion skill) — edits `workspace.dsl`, runs `render.sh`, embeds SVGs into arc42 markdown. Always check that `arch-structurizr init` has run first.
- `arch-adr` — infra ADRs (Docker base image policy, render-tool choice) may reference this skill's pin table.
- the `metamodel` skill — supporting-skills list entry + canonical paths for `docs/architecture/c4/`.

## Optional — Structurizr MCP server

The official `structurizr/mcp` Docker image exposes DSL validate / parse / export operations as MCP tools an agent can call directly (no shell-out). Setting it up is **optional** — `arch-structurizr` + `arch-c4` work without it via `docker run` shell calls.

See `references/mcp-optional.md` for the trade-off and setup instructions if you want the MCP path.

## Reference materials

- `references/dsl-conventions.md` — Structurizr DSL imperative grammar, brace placement, no-forward-reference rule, kit identifier conventions (`SYS_NN`, `CON_NN`, `CMP_NN`, `DN_NN`), view-key naming.
- `references/docker-pipeline.md` — render.sh contract, pinned versions, volume mount conventions, troubleshooting, CI hook recommendations.
- `references/structurizr-cheatsheet.md` — common DSL constructs (person, softwareSystem, container, component, deploymentEnvironment, relationships, views, styling, !include).
- `references/mcp-optional.md` — Structurizr MCP server setup if you want validate-as-MCP-tool.

## Closing report

After each mode, deliver:

- Mode executed (init / verify / upgrade)
- Files created or modified (list)
- Pinned versions: Structurizr CLI + PlantUML
- DSL validation result
- Next step: `arch-c4 context` (if init) or commit (if upgrade)

## Checklist

- [ ] `docs/architecture/c4/` exists with `workspace.dsl`, `render.sh`, `README.md`, `views/.gitkeep`
- [ ] `render.sh` is executable + pins the `-playwright` variant (not `:latest`, not the base tag)
- [ ] `docker version` succeeds in the verify step
- [ ] `structurizr validate` passes on the seed workspace.dsl
- [ ] Initial `render.sh` run produces at least one SVG under `views/`
- [ ] `README.md` documents the pinned version + the manual render command + the first-run Chromium download note
- [ ] User reminded that `arch-c4` is the next skill to invoke
