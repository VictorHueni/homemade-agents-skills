# Optional — Structurizr MCP server

`arch-structurizr` + `arch-c4` work **without** the Structurizr MCP server. They shell out to `docker run structurizr/structurizr:<pin>-playwright ...` via `render.sh` (or directly via Bash) for validation and export.

The MCP server is a strictly-optional **agent-experience upgrade**. If you want it, this file explains the trade-off and how to wire it.

---

## What the MCP server adds

The official `structurizr/mcp` Docker image ([docs.structurizr.com/ai/mcp](https://docs.structurizr.com/ai/mcp)) exposes Structurizr operations as native MCP tools. From the official docs:

| MCP tool family | What it does |
|---|---|
| `dsl-validate` | Validates a DSL file or string; returns parse errors with line numbers. |
| `dsl-parse` | Parses DSL into a workspace JSON representation. |
| `dsl-inspect` | Runs Structurizr's inspection feature — surfaces missing descriptions, orphan elements, broken references. |
| `dsl-mermaid` | Exports views as Mermaid diagrams. |
| `dsl-plantuml` | Exports views as PlantUML / C4-PlantUML diagrams. |
| `server-create / read / update / delete` | Manage workspaces on a Structurizr cloud or on-prem server. |

**For Claude Code workflows the most useful tool is `dsl-validate`** — it lets the agent validate after every edit *without* a shell-out, getting structured error responses instead of parsing stderr.

---

## Trade-off

| | With MCP server | Without (the default) |
|---|---|---|
| **Validation latency** | Sub-second; native tool call | 1–3 s; Docker pull + JVM startup on cold runs |
| **Error parsing** | Structured JSON response | Parse stderr (works fine — Structurizr CLI errors are clean) |
| **Setup cost** | Add an MCP server entry to `~/.claude.json` or project settings | Zero — Docker only |
| **Renders SVG?** | No — MCP only exports to PlantUML/Mermaid intermediate; for SVG you still call `structurizr/structurizr:<pin>-playwright export -format svg` | Yes — `render.sh` does this directly |
| **Works in CI?** | Requires the MCP server running in CI | Works anywhere Docker runs |

**Recommendation:** stay with Docker + `render.sh` as the default. Add the MCP server only if you find yourself iterating heavily on DSL during long Claude Code sessions and want faster validate feedback.

---

## Setup (if you want it)

1. Pull the image:
   ```bash
   docker pull structurizr/mcp
   ```

2. Run it (foreground, port 3000):
   ```bash
   docker run -it --rm -p 3000:3000 -e PORT=3000 structurizr/mcp
   ```

   In production you'd run this as a background service (systemd / a tmux session / a separate Claude Code session).

3. Register it with Claude Code. Claude Code does not natively support HTTP MCP transport — use the `mcp-remote` wrapper. Add to your project's `.mcp.json` or user-level `~/.claude.json`:
   ```json
   {
     "mcpServers": {
       "structurizr": {
         "command": "npx",
         "args": ["-y", "mcp-remote", "http://localhost:3000/mcp"]
       }
     }
   }
   ```

4. Restart Claude Code so the new MCP server is picked up.

5. The `structurizr/*` tools should now appear in Claude Code's tool list. `arch-c4` will prefer them over `docker run` shell-outs **only if it detects them at runtime** — there is no configuration flag to set; the skill probes the available tool list.

---

## When you should *not* set this up

- Single-developer projects with infrequent DSL edits.
- CI-only workflows (no interactive agent session).
- Constrained environments where running a long-lived MCP server is awkward.

In those cases, `docker run structurizr/structurizr:<pin>-playwright validate` from `render.sh` is perfectly fine.

---

## Sources

- [Structurizr — AI / LLM usage](https://docs.structurizr.com/ai)
- [Structurizr MCP server documentation](https://docs.structurizr.com/ai/mcp)
- [structurizr/mcp Docker image](https://hub.docker.com/r/structurizr/mcp)
