# Docker render pipeline

Single-stage pipeline that turns `workspace.dsl` into committed SVGs using the **consolidated Structurizr tool** (single image, supersedes the EOL `structurizr-cli` / `structurizr-lite` / on-premises installations — see [Introducing Structurizr vNext](https://www.patreon.com/posts/introducing-146923136)).

---

## Pin table (kit-maintained)

| Image | Pinned version | Notes |
|---|---|---|
| `structurizr/structurizr` | `2026.05.22-playwright` | The `-playwright` variant bundles the headless Chromium runtime needed for direct SVG / PNG export. The base `2026.05.22` tag does **not** include Playwright and cannot produce SVG. ([Docker Hub tags](https://hub.docker.com/r/structurizr/structurizr/tags)) |

**Why one image, not two:** the consolidated `structurizr/structurizr` tool now exports PNG and SVG directly via a bundled headless browser ([docs/export/png-and-svg](https://docs.structurizr.com/export/png-and-svg)). The previous two-stage pipeline (`structurizr/cli` → C4-PlantUML → `plantuml/plantuml` → SVG) is no longer necessary.

**Bump policy:** the `upgrade` mode of `arch-structurizr` is the only sanctioned way to change the pin. Bumping requires re-rendering every view and committing the diffs alongside the version change so that a reviewer can see whether the renderer changed the visual output.

**If a pin no longer exists upstream:** edit this table, then bump every project's `render.sh` via `arch-structurizr upgrade`.

---

## Performance — image pull is the only slow step

The `-playwright` image bundles a Chromium runtime in the image itself (verified against `2026.05.22-playwright` — ~1.8 GB on-disk, no on-demand download). Once the image is pulled:

- A full render of 4 views completes in **~5–10 seconds** on a typical developer machine.
- Validate alone runs in **~1–2 seconds**.

The only slow operation is the **initial `docker pull`** (~1.8 GB download, ~3–5 minutes depending on bandwidth). After that, renders are fast.

CI nuance: ephemeral CI runners that wipe the image cache every job will re-pull the 1.8 GB image. Mitigations:
- Cache the Docker image layer between jobs (most CI providers support this — see §CI hook recommendations).
- Build a project-specific image extending `structurizr/structurizr:<pin>-playwright` and host it in the project's registry to skip the public-pull step.

---

## render.sh contract

The script is small and deliberately simple so the same flow works in dev + CI + an agent's shell session. One entry point:

```
./docs/architecture/c4/render.sh [view-key]
```

Without `view-key`, all views render. With it, all views still render in the same docker run (cheaper because Chromium starts once) and non-matching SVGs are then deleted.

### Steps (in order)

1. **Validate the DSL** — `docker run structurizr/structurizr validate -workspace c4/workspace.dsl`. Exit non-zero if validation fails. Print the error.
2. **Export views to SVG** — `docker run structurizr/structurizr export -workspace c4/workspace.dsl -format svg -output c4/views/`. One `.svg` per view defined in the DSL.
3. **Optional filter** — if a single `view-key` was requested, delete non-matching SVGs.
4. **List rendered views** — show the user what was produced.

### Volume mounts

Mount the **repo root** to `/work` inside the container. Use `/work/docs/architecture/c4/...` paths inside the container. This keeps the script portable regardless of where in the tree the user invokes it from.

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
docker run --rm -v "${REPO_ROOT}:/work" "structurizr/structurizr:${STRUCTURIZR_VERSION}" \
    validate -workspace /work/docs/architecture/c4/workspace.dsl
```

### Optional export flags

The `export -format svg` subcommand accepts a few extra flags ([docs/export/png-and-svg](https://docs.structurizr.com/export/png-and-svg)):

| Flag | Default | Effect |
|---|---|---|
| `-mode light\|dark` | `light` | Light or dark theme |
| `-animation true\|false` | `false` | Emit one SVG per animation step (sequence-like reveal) |

`render.sh` does not surface these to keep the contract simple. Edit `render.sh` if you need them; `arch-c4` may surface them as mode-specific options in a future version.

### Exit codes

| Code | Meaning |
|---|---|
| 0 | All steps succeeded |
| 1 | DSL validation failed |
| 2 | Docker not available |
| 3 | Export / render failed |
| 4 | No views produced (DSL has no `views { ... }` block) |

---

## CI hook recommendations

The kit doesn't enforce CI but the pipeline is CI-friendly. Suggested GitHub Actions snippet (do **not** ship as part of the skill — leave to the project to wire):

```yaml
- name: Validate + render C4
  run: ./docs/architecture/c4/render.sh

- name: Detect uncommitted render drift
  run: |
    if ! git diff --quiet docs/architecture/c4/views/; then
      echo "Rendered SVGs differ from committed versions. Re-render locally and commit."
      git diff --stat docs/architecture/c4/views/
      exit 1
    fi
```

For CI performance, cache the Docker image:
```yaml
- uses: actions/cache@v4
  with:
    path: /var/lib/docker
    key: structurizr-${{ env.STRUCTURIZR_VERSION }}
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `docker: not found` | Docker not installed or daemon not running | Install Docker; on WSL2 confirm Docker Desktop integration |
| `Unable to find image structurizr/structurizr:<pin>-playwright` after pull | Pin no longer exists upstream | Run `arch-structurizr upgrade`; bump pin table in this file |
| Initial `docker pull` takes 3+ minutes | One-time 1.8 GB image download | Expected. Renders themselves are 5–10 s after the image is cached. |
| `Parse error at line N` from structurizr validate | Brace placement or forward reference (see `dsl-conventions.md` §1) | Fix the DSL; never disable validate |
| Render produces empty SVG | View has `include *` but no elements assigned to that view's scope | Add elements to the DSL or remove the empty view |
| `Error: browserType.launch: Executable doesn't exist` | Using the **base** `2026.05.22` tag instead of `2026.05.22-playwright` | Bump pin to `-playwright` variant via `arch-structurizr upgrade` |
| `Permission denied` on render.sh | Missing executable bit after a fresh clone (some Git configs strip it) | `chmod +x docs/architecture/c4/render.sh` |
| Different SVG output across machines | Pin drift (someone is using `:latest` or a different tag) | Confirm both machines use the pin in this table |

---

## Why not `:latest` tags

Reproducibility. A pinned tag means the same DSL renders the same SVG today, next week, and in CI. `:latest` is fine for local exploration but **forbidden** in `render.sh` — `verify` mode flags it.

---

## Why no separate Playwright image?

The `structurizr/structurizr:<pin>-playwright` variant bundles Chromium + Playwright into one container. There is no need to chain a separate browser-automation image. This is the official supported path — see [docs/export/png-and-svg](https://docs.structurizr.com/export/png-and-svg).

---

## Sources

- [Introducing Structurizr vNext (consolidation announcement)](https://www.patreon.com/posts/introducing-146923136)
- [Structurizr — Commands overview (validate, export, etc.)](https://docs.structurizr.com/binaries)
- [Structurizr — PNG and SVG export](https://docs.structurizr.com/export/png-and-svg)
- [Structurizr — DSL grammar](https://docs.structurizr.com/dsl)
- [structurizr/structurizr Docker Hub](https://hub.docker.com/r/structurizr/structurizr)
