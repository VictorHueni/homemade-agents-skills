# Docker render pipeline

Single-image pipeline that turns `diagrams/*.puml` into committed SVGs using the **official [`plantuml/plantuml`](https://hub.docker.com/r/plantuml/plantuml) image** (bundles `plantuml.jar` + a JRE + Graphviz).

---

## Pin table (kit-maintained)

| Image | Pinned version | Notes |
|---|---|---|
| `plantuml/plantuml` | `1.2026.2` | Bundles `plantuml.jar`, JRE, and Graphviz (needed for class/state/activity/component/ER layout — sequence diagrams do not need it). Renders SVG directly from the jar — no headless browser. ([Docker Hub tags](https://hub.docker.com/r/plantuml/plantuml/tags)) |

**Why this image, not the server image:** `plantuml/plantuml` is the **CLI** image (entrypoint = the jar). `plantuml/plantuml-server` is a long-running web service — not what a batch render wants. Use the CLI image.

**Bump policy:** the `upgrade` mode of `arch-plantuml` is the only sanctioned way to change the pin. Bumping requires re-rendering every diagram and committing the diffs alongside the version change so a reviewer can see whether the renderer changed the visual output.

**If a pin no longer exists upstream:** edit this table, then bump every project's `render.sh` via `arch-plantuml upgrade`.

---

## Performance — image pull is the only slow step

The `plantuml/plantuml` image is a few hundred MB (vs the ~1.8 GB Structurizr `-playwright` image — PlantUML needs no Chromium). Once pulled:

- A full render of a handful of diagrams completes in **~1–3 seconds**.
- `-checkonly` validation alone runs in **under a second**.

The only slow operation is the **initial `docker pull`** (a few hundred MB, typically under a minute). After that, renders are fast.

---

## render.sh contract

One entry point, deliberately simple so the same flow works in dev + CI + an agent's shell session:

```
./docs/architecture/diagrams/render.sh [diagram-name]
```

Without `diagram-name`, every renderable `.puml` renders. With it, only the matching diagram renders (faster — one file instead of all).

### Steps (in order)

1. **Collect renderable files** — every `*.puml` in `diagrams/` **except** `_*.puml` (includes). If a `diagram-name` argument is given, narrow to that one file.
2. **Validate** — `docker run plantuml/plantuml -checkonly -failfast2 <files>`. Exit non-zero if any file fails to parse. Print the offending filename.
3. **Render to SVG** — `docker run plantuml/plantuml -tsvg -failfast2 -o <abs>/views <files>`. One `.svg` per `.puml`.
4. **List rendered views** — show the user what was produced.

### Volume mounts

Mount the **repo root** to `/work` inside the container. Use `/work/docs/architecture/diagrams/...` paths inside the container. This keeps the script portable regardless of where in the tree the user invokes it from.

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
docker run --rm --user "$(id -u):$(id -g)" -v "${REPO_ROOT}:/work" \
    "plantuml/plantuml:${PLANTUML_VERSION}" \
    -checkonly -failfast2 /work/docs/architecture/diagrams/seq-01-foo.puml
```

### The `-o` output flag

`-o /work/docs/architecture/diagrams/views` sends every SVG to `views/`. Use an **absolute** container path so output lands in one place regardless of which `.puml` is processed (a relative `-o` is resolved per-input-file directory).

### Why `--user`

Docker volume mounts default to running as root, producing root-owned SVGs the host user then can't `git clean -fd` without sudo. `--user "$(id -u):$(id -g)"` writes with the right ownership. (PlantUML's jar writes only to the `-o` dir, so this is safe.)

### Useful PlantUML flags

| Flag | Effect |
|---|---|
| `-tsvg` | Output SVG (the kit default — diff-friendlier than PNG, crisp at any zoom) |
| `-checkonly` | Parse only, no output — the validation step / `--dry-run` |
| `-failfast2` | Exit non-zero on the first syntax error (do not silently emit a broken diagram) |
| `-o <dir>` | Output directory |
| `-tpng` / `-tpdf` | Alternate formats — edit `render.sh` if a consumer needs them |
| `-darkmode` | Dark theme render — not surfaced by default |

### Exit codes

| Code | Meaning |
|---|---|
| 0 | All steps succeeded |
| 1 | A `.puml` failed validation (`-checkonly`) |
| 2 | Docker not available |
| 3 | Render failed |
| 4 | No renderable diagrams found (only `_*.puml` includes, or empty folder) |

---

## CI hook recommendations

The kit doesn't enforce CI but the pipeline is CI-friendly. Suggested GitHub Actions snippet (leave to the project to wire — do **not** ship it as part of the skill):

```yaml
- name: Validate + render PlantUML
  run: ./docs/architecture/diagrams/render.sh

- name: Detect uncommitted render drift
  run: |
    if ! git diff --quiet docs/architecture/diagrams/views/; then
      echo "Rendered SVGs differ from committed versions. Re-render locally and commit."
      git diff --stat docs/architecture/diagrams/views/
      exit 1
    fi
```

For CI performance, cache the Docker image layer (`actions/cache` on `/var/lib/docker`, keyed on the pin).

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `docker: not found` | Docker not installed or daemon not running | Install Docker; on WSL2 confirm Docker Desktop integration |
| `Unable to find image plantuml/plantuml:<pin>` after pull | Pin no longer exists upstream | Run `arch-plantuml upgrade`; bump the pin table above |
| `Error: No @startuml found` | A `_*.puml` include was passed to the renderer, or a diagram is missing its `@startuml` | `render.sh` excludes `_*.puml`; if you invoked the jar manually, drop the include from the file list |
| `Dot/Graphviz not installed` | Using a stripped image without Graphviz | The official `plantuml/plantuml` image bundles Graphviz — confirm you are on it, not a minimal fork |
| Empty / clipped SVG | Diagram too large or `skinparam dpi` too high | Split the diagram (see `puml-conventions.md` §5); check the theme |
| `Permission denied` on render.sh | Missing executable bit after a fresh clone | `chmod +x docs/architecture/diagrams/render.sh` |
| Different SVG output across machines | Pin drift (someone is on `:latest` or another tag) | Confirm both machines use the pin in this table |

---

## Why not `:latest` tags

Reproducibility. A pinned tag means the same `.puml` renders the same SVG today, next week, and in CI. `:latest` is fine for local exploration but **forbidden** in `render.sh` — `verify` mode flags it.

---

## Sources

- [`plantuml/plantuml` Docker image](https://hub.docker.com/r/plantuml/plantuml)
- [PlantUML — Command line](https://plantuml.com/command-line)
- [PlantUML — SVG output](https://plantuml.com/svg)
- [PlantUML — Preprocessing / `!include`](https://plantuml.com/preprocessing)
