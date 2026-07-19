# Optional — PlantUML MCP server

`arch-plantuml` + `arch-uml` work **without** any MCP server. They shell out to `docker run plantuml/plantuml:<pin> ...` via `render.sh` (or directly via Bash) for validation and render.

A PlantUML MCP server is a strictly-optional **agent-experience upgrade**. If you want it, this file explains the trade-off and how to wire it.

---

## What an MCP server adds

Several community MCP servers expose PlantUML operations as native MCP tools:

| Server | What it offers |
|---|---|
| [`infobip/plantuml-mcp-server`](https://github.com/infobip/plantuml-mcp-server) | Generate diagrams, return embeddable SVG/PNG URLs, optionally save locally; includes a prompt that auto-detects and fixes common PlantUML errors (missing tags, bad arrows, typos). |
| [`antoinebou12/uml-mcp`](https://github.com/antoinebou12/uml-mcp) | Generate many UML diagram types from natural language **or** raw PlantUML / Mermaid / Kroki; multiple output formats + local storage. |
| [`@brainstack/plantuml-mcp`](https://www.npmjs.com/package/@brainstack/plantuml-mcp) | MCP server for generating UML diagrams via PlantUML. |

For Claude Code workflows the useful capability is **encode + render-as-a-tool**: validate and render after every edit *without* a Docker shell-out, getting structured responses instead of parsing stderr. Several of these servers render via the public PlantUML web service rather than locally — note the privacy trade-off below.

---

## Trade-off

| | With MCP server | Without (the default) |
|---|---|---|
| **Render latency** | Sub-second tool call | 1–3 s Docker run (cold pull aside) |
| **Error parsing** | Structured response (some servers auto-fix) | Parse stderr (works fine — PlantUML errors name the line) |
| **Setup cost** | Add an MCP server entry to settings | Zero — Docker only |
| **Privacy** | Some servers POST your diagram source to the public plantuml.com server | Fully local — nothing leaves the machine |
| **Reproducibility** | Depends on the server's PlantUML version | Pinned image — deterministic |
| **Works in CI?** | Requires the MCP server running in CI | Works anywhere Docker runs |

**Recommendation:** stay with Docker + `render.sh` as the default — it is local, pinned, and deterministic. Add an MCP server only if you iterate heavily on `.puml` during long sessions and want faster feedback, **and** you have checked whether the server renders locally or via the public web service (the latter is unacceptable for confidential architecture).

---

## Setup (if you want it)

Setup is server-specific; follow the chosen server's README. The general Claude Code shape is an entry in the project's `.mcp.json` (or user-level config):

```json
{
  "mcpServers": {
    "plantuml": {
      "command": "npx",
      "args": ["-y", "<the-server-package-or-wrapper>"]
    }
  }
}
```

Restart Claude Code so the new server is picked up; its tools then appear in the tool list. `arch-uml` will not assume an MCP server exists — it always falls back to `render.sh`.

---

## When you should *not* set this up

- Confidential / regulated projects where diagram source must not leave the machine.
- Single-developer projects with infrequent diagram edits.
- CI-only workflows (no interactive agent session).

In those cases, `docker run plantuml/plantuml:<pin>` from `render.sh` is the right tool.

---

## Sources

- [`infobip/plantuml-mcp-server`](https://github.com/infobip/plantuml-mcp-server)
- [`antoinebou12/uml-mcp`](https://github.com/antoinebou12/uml-mcp)
- [`@brainstack/plantuml-mcp` (npm)](https://www.npmjs.com/package/@brainstack/plantuml-mcp)
