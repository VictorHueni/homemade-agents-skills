# C4 architecture workspace

This folder is the **single source of truth** for every C4 diagram in the project. Edits flow through one file (`workspace.dsl`) and render to committed SVGs via `./render.sh`.

| File / folder | What it is |
|---|---|
| `workspace.dsl` | Structurizr DSL — every model element + view defined here. Edit this; never edit the SVGs directly. |
| `render.sh` | Single-image Docker render pipeline (`structurizr/structurizr` `validate` + `export -format svg`). |
| `views/*.svg` | Rendered diagrams. **Committed.** Embedded by the arc42 markdown sections. |

The pipeline uses the consolidated **Structurizr vNext** tool (announced [here](https://www.patreon.com/posts/introducing-146923136)), which superseded the EOL `structurizr-cli` / `structurizr-lite` / on-premises installations.

---

## Quick start

```bash
# Render every view from workspace.dsl
./render.sh

# Render a single view (renders all then keeps only the matching one)
./render.sh systemContext

# Validate DSL + Docker availability without rendering
./render.sh --dry-run
```

The script requires **Docker** — no Java, no local PlantUML, no local Structurizr install.

### First-run note

The pinned image is the `-playwright` variant — it bundles headless Chromium for direct SVG export. The image itself is ~1.8 GB so the **initial `docker pull` is the only slow step (~3–5 min on first install)**. After that, renders complete in ~5–10 seconds. CI runners that wipe the image cache between jobs will re-pull — cache the image layer if this matters.

---

## Pinned version

| Tool | Pinned version |
|---|---|
| `structurizr/structurizr` | `{{structurizr_version}}-playwright` |

To bump this, invoke the **`arch-structurizr upgrade`** skill. Do not edit the pin by hand — the upgrade flow re-renders every view to surface visual diffs before you commit.

The `-playwright` suffix is **mandatory**. The base `structurizr/structurizr:<pin>` image does not bundle Chromium and cannot export SVG (you'd get an `Executable doesn't exist` error from Playwright).

---

## View key conventions

The file name of every rendered SVG is the **view key** declared in `workspace.dsl`. Keep the keys stable — they are referenced from arc42 markdown by relative path.

| View key pattern | arc42 section |
|---|---|
| `systemContext` | §3 Context & Scope |
| `containers` | §5.1 Building Block Level 1 |
| `components-<CON-NN>` | §5.2 / §5.3 Building Block Level 2 (one per drilled container) |
| `deployment-<env>` | §7 Deployment View (one per environment) |
| `dynamic-<RV-NN>` | §6 Runtime View (one per scenario, produced by `arch-runtime-view`) |

---

## How to add a new view

Open `workspace.dsl`. Inside the `views { ... }` block, add the view. Example for a new component view of `CON-02 Claims API`:

```
component CON_02 "components-CON-02" {
    include *
    autolayout lr
    description "CON-02 internal components."
}
```

Then run `./render.sh components-CON-02` to keep only that view, or `./render.sh` to render everything.

Prefer using the **`arch-c4`** skill — it handles DSL editing, ID assignment, validation, and arc42 markdown embedding in one pass.

---

## DSL grammar gotchas

The full reference is in the kit's `arch-structurizr/references/dsl-conventions.md`. The two rules that most often bite when editing the DSL:

1. **Forward references are not allowed.** Declare every identifier before using it in a relationship.
2. **Brace placement:** `{` ends a line; `}` is alone on a line.

`./render.sh` runs `validate` first; if the DSL is malformed it stops before exporting and prints the offending line.

---

## Optional rendering flags

The `export -format svg` subcommand accepts extra flags ([docs/export/png-and-svg](https://docs.structurizr.com/export/png-and-svg)):

| Flag | Default | Effect |
|---|---|---|
| `-mode light\|dark` | `light` | Light or dark theme |
| `-animation true\|false` | `false` | Emit one SVG per animation step (sequence-like reveal) |

`render.sh` does not expose these — edit it if you want dark-mode renders or step animations.

---

## CI integration (optional)

```yaml
- name: Validate + render C4
  run: ./docs/architecture/c4/render.sh

- name: Detect uncommitted render drift
  run: |
    git diff --quiet docs/architecture/c4/views/ || {
      echo "Rendered SVGs differ from committed copies. Re-render locally and commit."
      exit 1
    }
```

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `docker: not found` | Install Docker; on WSL2 confirm Docker Desktop integration. |
| `Parse error at line N` | DSL syntax — usually forward reference or brace placement. See `dsl-conventions.md`. |
| Empty SVG | View has no elements included; remove the view or add elements. |
| `Executable doesn't exist` Playwright error | You're using the base `structurizr/structurizr:<pin>` tag instead of `-playwright`. Bump via `arch-structurizr upgrade`. |
| Initial `docker pull` takes 3+ minutes | One-time 1.8 GB image download. Expected once per cache clear. Renders themselves are 5–10 s after that. |
| `Permission denied` running `render.sh` | `chmod +x render.sh` (some Git configs strip the executable bit). |
| Different SVG output between machines | Confirm both machines use the pinned version above. Bump via `arch-structurizr upgrade` if they need to converge. |
