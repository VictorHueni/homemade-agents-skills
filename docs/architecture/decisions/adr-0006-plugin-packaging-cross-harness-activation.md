---
title: Plugin Packaging & Cross-Harness Activation
status: active
owner: Victor Hueni
last_reviewed: 2026-07-19
review_interval: 180d
---

# Plugin Packaging & Cross-Harness Activation

Date: 2026-07-19

## Context and Problem Statement

The kit is a flat bundle of 58 skills, 2 commands, and 11 rules, symlinked wholesale into
`~/.claude` (and, for skills, `~/.codex` + `~/.agents`) by `install.sh`. Two needs have
outgrown that shape:

1. **Selective activation** — enable or disable coherent *sets* of skills at will, instead of
   every skill being installed and ambient everywhere.
2. **Harness portability** — the same kit consumed from Claude Code, OpenAI Codex CLI, and
   OpenCode, without maintaining three configurations.

The ecosystem review (2026-07-19; see Plan-0002) found: SKILL.md is now a de-facto
cross-harness standard (Codex reads `~/.codex/skills/`, OpenCode discovers `.claude/skills`
and `.agents/skills` natively); AGENTS.md is the rules standard everywhere except Claude
Code; MCP declarations share a protocol but differ in format (JSON / TOML / `opencode.json`);
and **plugin packaging does not port at all** — Claude plugins, Codex's young plugin model,
and OpenCode's JS event-hook plugins are mutually untranslatable. Sync tools (rulesync ~1.2k★,
Ruler ~2.8k★) cover rules/MCP/command *format conversion* but have no concept of activation,
and are project-root-oriented where this kit is user-global.

## Decision Drivers

- **Native mechanisms over invented ones** — every harness-facing behaviour should ride the
  harness's own idiom, so the kit ages with the harnesses instead of fighting them.
- **One source of truth per fact** — no per-harness copies of skills, MCP definitions, or rules.
- **YAGNI for a single-maintainer kit** — machinery must be justified by recurring pain, not
  anticipated pain.
- **`install.sh` must keep working at every commit** — chezmoi-driven machines pull and
  reinstall automatically.
- **Context economy** — Codex/OpenCode load every installed skill description and every MCP
  tool schema into each session; what ships enabled must be curated.

## Considered Options

1. **Claude plugin marketplace + flattening installer + harness-native toggling (chosen).**
2. **Kit-side activation layer** (`install.sh --sets` + persisted state driving symlinks,
   generated OpenCode `permission.skill` fragments, MCP filtering). Rejected as initial
   design: stateful convergence machinery, a dual-state problem on Claude (marketplace state
   vs installer state), chezmoi interplay — for toggles whose real-world frequency is
   unproven. Recorded as the **deferred alternative**; revisit trigger: recurrent manual
   re-toggling (e.g. re-deleting the same Codex symlink globs weekly).
3. **Adopt rulesync (or Ruler) as the cross-harness engine.** Rejected for the user-global
   layer: project-root orientation, whole-file ownership of generated targets (vs
   marker-block coexistence with hand-edited files), a Node dependency in the chezmoi
   bootstrap, and no activation concept — while the genuinely duplicated surface (AGENTS.md
   concatenation + MCP format conversion) is ~80 lines. Revisit triggers below.
4. **Status quo** (flat symlinks, no sets). Fails need 1; leaves rules and MCP Claude-only.

## Decision Outcome

Chosen option: **1** — four sub-decisions:

### 1. Layout: plugin sets in a Claude marketplace

```
.claude-plugin/marketplace.json      # lists the 10 plugins
plugins/<set>/
  .claude-plugin/plugin.json
  skills/<skill-name>/…              # git-moved from skills/
  commands/<name>.md                 # where applicable
  .mcp.json                          # generated from mcp/registry.json
```

Set composition — every skill and command has exactly one home (56 skills post-Plan-0002
consolidation, 2 commands):

| Set | Skills | Commands |
|---|---|---|
| `kit-core` (always installed) | `metamodel` · `util-open-items` · `util-provenance` · `util-toolkit-doctor` | — |
| `strategy` | all 9 `business-*` · all 3 `discovery-*` | — |
| `domain-modeling` | `domain-bounded-context` · `domain-glossary` · `domain-model` | — |
| `product-spec` | `spec-functional-breakdown-structure` · `spec-prd` · `spec-quality-attributes` · `spec-use-case` · `plan-delivery-roadmap` · `plan-implementation` | — |
| `architecture` | all 9 `arch-*` | — |
| `dev-flow` | all 7 `dev-*` | `branch-cleanup-audit` |
| `agent-loop` | all 4 `agent-*` | `ralph-audit` |
| `delivery-comms` | all 3 `com-*` · `ux-design-system` | — |
| `ops` | all 3 `ops-*` | — |
| `docs-hygiene` | `util-docs-audit` · `util-docs-index` · `util-docs-lint` · `util-docs-log` | — |

### 2. Flattening contract & global name uniqueness

`install.sh` projects `plugins/*/skills/*` into one **flat** directory per harness
(`~/.claude/skills`, `~/.codex/skills`, `~/.agents/skills`; commands → `~/.claude/commands`).
Plugin structure is invisible outside Claude. Consequently **skill names must be globally
unique across all plugins** — guaranteed today by the category-prefix naming convention,
now an explicit constraint. Cross-skill references are **name-first** (see ADR-0007), never
cross-plugin relative paths.

### 3. Activation: harness-native, no kit-side state

The kit ships **no activation state**. Toggling a set uses each harness's own idiom:

| Harness | Toggle idiom | MCP follows? |
|---|---|---|
| Claude Code | `/plugin` enable/disable (marketplace channel) | Yes — per-plugin `.mcp.json` |
| OpenCode | `permission.skill` deny-globs, one line per set (prefix naming: `"business-*": "deny"`) — documented snippet, hand-pasted | No — manual |
| Codex CLI | symlink-glob removal (`rm ~/.codex/skills/{business,discovery}-*`) — documented, with the caveat that any `install.sh` re-run restores | No — manual |

**One channel per machine (Claude):** a machine consumes the kit via the marketplace *or*
via `~/.claude/skills` symlinks, never both. The choice is recorded once with
`install.sh --claude-channel <marketplace|symlink>` (persisted in `var/claude-channel`,
per-clone/per-machine, gitignored, default `symlink`); in `marketplace` mode every installer
run — including flag-less chezmoi re-runs — skips and prunes the Claude skills/commands
links while leaving `~/.codex`, `~/.agents`, rules, adapters, and MCP generation untouched.
This is a binary channel fact, not per-set activation state (the deferred Option 2 stays
deferred). `util-toolkit-doctor` warns on a dual-channel conflict and names the remedy.

### 4. Adapters & MCP: thin, generated, guarded

- **AGENTS.md**: `install.sh` renders a static, marker-delimited block (metamodel routing +
  concatenated behavioural rules) into `~/.codex/AGENTS.md` and the OpenCode global
  instructions file; user content outside markers is never touched.
- **MCP**: one committed registry (`mcp/registry.json`; entries carry `owning_set` and an
  `enabled` flag — committed configuration, not runtime state) generates all three formats:
  per-plugin `.mcp.json`, a `[mcp_servers.*]` TOML marker-block for `~/.codex/config.toml`,
  an `mcp` block for `opencode.json`. Seed selection:

| Tier | Server | Set | Notes |
|---|---|---|---|
| Always-on | Chrome DevTools (`chrome-devtools-mcp`, Google) | `dev-flow` | front-end debugging: console, network, performance |
| Always-on | Context7 | `dev-flow` | live library docs; no CLI equivalent |
| Always-on | Playwright (`microsoft/playwright-mcp`) | `delivery-comms` | verify HTML decks/viz; demotion candidate if browser-server overlap with Chrome DevTools ever bites |
| Opt-in (`enabled: false`) | GitHub (official) | `dev-flow` | `gh` CLI covers ~90% (CLI-first) |
| Opt-in | Terraform (HashiCorp) | `ops` | single-skill use |
| Project-scoped (not in the user-global registry) | PostgreSQL — Postgres MCP Pro (`crystaldba/postgres-mcp`) | — | databases are per-project; declare in the project's own `.mcp.json` / `opencode.json` when it makes sense, `--access-mode=restricted` as the starting mode. (Codex caveat: `config.toml` is global-only — enable there deliberately.) Anthropic's reference server is archived (July 2025, SQLi); PGDG ships none — revisit if an official server appears |
| Absent by design | Web search (harness-native search is relied on: Claude WebSearch, Codex built-in; OpenCode coverage varies by provider — accepted) · PlantUML/Structurizr (Docker per `arch-plantuml/references/mcp-optional.md`) · filesystem/git/memory (harness-native) · **clew** (future `kit-core` entry once its MCP mode lands) | | |

- **Guardrails**: generators live behind `scripts/gen-*` interfaces, swappable for rulesync
  without touching the kit's contract. Revisit triggers for adopting rulesync: per-target
  rule *variants*, a **fourth** harness, or converting *content* rather than generating
  wiring.

### Positive Consequences

- Claude gets true plugin toggling (skills + commands + MCP per set); Codex/OpenCode get the
  full kit through formats they read natively; skills need zero conversion anywhere.
- No state machinery, no dual-state reconciliation, no new dependencies; custom surface is
  ~80 lines of generation behind swappable interfaces.
- MCP servers are declared once, propagated three ways, and curated (3 always-on, 2
  documented opt-ins, PostgreSQL as a documented project-scoped recipe).

### Negative Consequences

- Codex/OpenCode sessions carry all ~56 installed skill descriptions unless manually
  trimmed; the deferred activation layer is the remedy if that pain becomes recurrent.
- Manual toggles on Codex do not survive reinstalls (chezmoi re-runs restore pruned links).
- Two Claude consumption channels (marketplace vs symlinks) exist during transition;
  mitigated by the one-channel rule + doctor warning.

## Open Items

Filed at Plan-0002 increment 13: the deferred `--sets` activation layer (with revisit
trigger) and any set-membership disputes arising from this ADR's review.
