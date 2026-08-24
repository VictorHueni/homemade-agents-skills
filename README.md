# homemade-claude-kit

A personal, harness-portable toolkit — 60 composable skills for business architecture,
domain modeling, product specification, and developer workflow, packaged as **11 toggleable
plugin sets** and consumable from **Claude Code, OpenAI Codex CLI, and OpenCode**.

Three design pillars (kit [ADR-0006](docs/architecture/decisions/adr-0006-plugin-packaging-cross-harness-activation.md) / [ADR-0007](docs/architecture/decisions/adr-0007-metamodel-distribution-as-skill.md)):

1. **SKILL.md is the portability layer** — all three harnesses read it natively; `install.sh` flattens `plugins/*/skills/*` into one directory per harness. No conversion, ever.
2. **The metamodel travels as a skill** — the `metamodel` skill carries the documentation-stack contract (build order, YAML type registry, frontmatter schema, open-items governance + Audit/Scaffold/Migrate modes). Structural facts are canonically owned by [clew](https://github.com/VictorHueni/clew) (clew ADR-0008); the kit ships the projection.
3. **Toggling is harness-native** — the kit ships no activation state; each harness uses its own idiom (see § Toggling a set).

---

## Plugin sets

| Set | Purpose | Skills |
|---|---|---|
| `kit-core` | Always on — the metamodel keystone + cross-cutting operators | `metamodel` · `util-open-items` · `util-provenance` · `util-toolkit-doctor` |
| `strategy` | Business architecture + discovery evidence | `business-vision` · `business-persona` · `business-model-canvas` · `business-capability-map` · `business-value-stream` · `business-objective` · `business-process` · `business-quantitative-model` · `business-competitive-landscape` · `discovery-idea` · `discovery-research` · `discovery-workshop` |
| `domain-modeling` | Strategic + tactical DDD | `domain-bounded-context` · `domain-glossary` · `domain-model` |
| `product-spec` | Specs + build planning | `spec-functional-breakdown-structure` · `spec-prd` · `spec-use-case` · `plan-delivery-roadmap` · `plan-implementation` |
| `quality-assurance` | Test strategy, scenarios, cases — the validate/test stage | `spec-quality-attributes` · `qa-test-strategy` · `qa-test-scenario` |
| `architecture` | Decisions, contracts, diagrams, arc42 | `arch-adr` · `arch-research` · `arch-service-contract` · `arch-cli-contract` · `arch-structurizr` · `arch-c4` · `arch-plantuml` · `arch-uml` · `arch-arc42` |
| `dev-flow` | Developer workflow (+ `branch-cleanup-audit` command) | `dev-git-init` · `dev-git-commit` · `dev-pr` · `dev-git-worktree` · `dev-release-init` · `dev-stack-guide` · `dev-getting-started` |
| `agent-loop` | Guide → Verify → Solve agent cycle (+ `ralph-audit` command) | `agent-config` · `agent-grill-me` · `agent-peer-review` · `agent-ralph-loop` |
| `delivery-comms` | Presentation layer | `com-slide-deck` · `com-artefact-viz` · `com-release-note` · `ux-design-system` |
| `ops` | Post-ship operations | `ops-runbook` · `ops-bug-rca` · `ops-terraform-exoscale` |
| `docs-hygiene` | Documentation housekeeping | `util-docs-audit` · `util-docs-index` · `util-docs-lint` · `util-docs-log` |

Per-skill purpose lives in each `plugins/<set>/skills/<name>/SKILL.md` frontmatter description.

---

## Install

### Claude Code — marketplace channel (recommended)

```bash
# In Claude Code:
/plugin marketplace add VictorHueni/homemade-claude-kit
# then enable the sets you want in /plugin
```

Each plugin bundles its skills, commands, and MCP servers (`plugins/<set>/.mcp.json`) — a
set toggle carries all three. **One channel per machine:** after adopting the marketplace,
record it once —

```bash
cd ~/projects/homemade-claude-kit && ./install.sh --claude-channel marketplace
```

— every later `install.sh` run (including chezmoi's) then skips and prunes the
`~/.claude/skills` + `~/.claude/commands` links while still serving Codex/OpenCode, rules,
adapters, and MCP. Revert with `--claude-channel symlink`. The choice persists in
`var/claude-channel` (per machine, gitignored); `util-toolkit-doctor` warns if both channels
end up live.

### All harnesses — symlink channel

```bash
git clone git@github.com:VictorHueni/homemade-claude-kit.git ~/projects/homemade-claude-kit
cd ~/projects/homemade-claude-kit && ./install.sh
```

A global run:

- symlinks all skills (flat) into `~/.claude/skills`, `~/.codex/skills`, `~/.agents/skills` (OpenCode discovers the latter two natively) and commands into `~/.claude/commands`;
- symlinks the Claude rules into `~/.claude/rules`;
- renders the **AGENTS.md adapter** (metamodel routing + behavioural rules, marker-delimited) into `~/.codex/AGENTS.md` and `~/.config/opencode/AGENTS.md`;
- projects **`mcp/registry.json`** into `~/.codex/config.toml` (`[mcp_servers.*]` marker block) and `opencode.json`'s `mcp` key.

`./install.sh /path/to/project` installs into a single project instead (skills/commands/rules only). Re-run after `git pull` — idempotent, prunes retired skills, never touches your content outside its marker blocks.

## Update

```bash
cd ~/projects/homemade-claude-kit && git pull   # chezmoi machines do this automatically
# symlinks point here — install.sh re-runs only regenerate adapters/MCP
```

---

## Toggling a set

The kit ships no activation state — use each harness's native idiom (ADR-0006):

| Harness | Toggle | MCP follows? |
|---|---|---|
| **Claude Code** | `/plugin` → enable/disable the set | ✅ automatic (per-plugin `.mcp.json`) |
| **OpenCode** | Paste deny-globs into `opencode.json` — one line per set thanks to prefix naming: `"permission": { "skill": { "business-*": "deny", "discovery-*": "deny" } }` (that line disables `strategy`) | manual |
| **Codex CLI** | Remove the set's symlinks: `rm ~/.codex/skills/{business,discovery}-*` — **caveat:** any `install.sh` re-run (incl. the chezmoi hook) restores them | manual |

If you find yourself re-deleting the same Codex globs weekly, that's the recorded trigger to
build the deferred `--sets` activation layer (see the open-items ledger).

## MCP servers

`mcp/registry.json` is the single source of truth: 3 always-on (Chrome DevTools, Context7 →
`dev-flow`; Playwright → `delivery-comms`), 2 documented opt-ins (GitHub, Terraform — flip
`enabled` and re-run `scripts/gen-mcp.py plugins` + `./install.sh`), and a **project-scoped
PostgreSQL recipe** (Postgres MCP Pro — declare per project, not user-globally). Web search
is deliberately absent: harness-native search is relied on.

---

## Adding a skill

1. Create `plugins/<set>/skills/<skill-name>/SKILL.md` — naming + set placement per [`rules/skill-creation-sync.md`](./rules/skill-creation-sync.md); reference the metamodel **name-first** ("the `metamodel` skill's `references/<file>`").
2. Structural metamodel changes (new artefact type, ID, path) are authored **clew-side first** (clew ADR-0008), then synced into the `metamodel` skill's registry YAML.
3. Run `./install.sh` and `bash scripts/audit-skills.sh`.
4. Commit and push.

## Backlog

Open items live as GitHub Issues labelled `open-item` —
<https://github.com/VictorHueni/homemade-claude-kit/issues?q=label%3Aopen-item>
(authored via the Open Item form; contract: the `metamodel` skill's
`references/open-items-governance.md`).

## Rules

Claude-side conventions in `rules/` (symlinked to `~/.claude/rules`); the behavioural ones
also feed the generated AGENTS.md adapter for Codex/OpenCode:

| Rule file | Covers |
|---|---|
| `rules/artefact-frontmatter.md` | **Pointer stub** → the `metamodel` skill's `references/artefact-frontmatter.md` (kit ADR-0007) |
| `rules/skill-creation-sync.md` | Skill naming (incl. registered exceptions), set placement, reference convention, blast-radius procedure |
| `rules/metamodel.md` | **Pointer stub** → the `metamodel` skill (spine, variants, references) |
| `rules/artefact-types-registry.md` | **Pointer stub** → the `metamodel` skill's `references/artefact-types-registry.yaml` (clew-owned projection, clew ADR-0008) |
| `rules/open-items-governance.md` | **Pointer stub** → the `metamodel` skill's `references/open-items-governance.md` |
| `rules/git-and-tools.md` | Git discipline, Edit tool usage *(→ AGENTS.md adapter)* |
| `rules/working-style.md` | Sequential plans, trust-but-verify *(→ AGENTS.md adapter)* |
| `rules/diagramming-mermaid.md` | Mermaid diagram pitfalls *(→ AGENTS.md adapter)* |
| `rules/frontend-nuxt.md` | Nuxt UI v4 / Vue 3.5 / Reka UI *(→ AGENTS.md adapter)* |
| `rules/writing-citations.md` | Citation discipline *(→ AGENTS.md adapter)* |
