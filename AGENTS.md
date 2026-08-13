# AGENTS.md

## Behavioral guidelines

**Think before coding.** State assumptions explicitly. If multiple interpretations exist, present them — don't pick silently. If something is unclear, stop and ask.

**Simplicity first.** Minimum code that solves the problem. No speculative features, no abstractions for single-use code, no unrequested flexibility or error handling for impossible scenarios. If you write 200 lines and it could be 50, rewrite it. Ask: "would a senior engineer call this overcomplicated?" If yes, simplify.

**Surgical changes.** Touch only what you must. Don't improve adjacent code, comments, or formatting. Don't refactor things that aren't broken. Match existing style. If you notice unrelated dead code, mention it — don't delete it. Every changed line should trace directly to the user's request.

**Goal-driven execution.** Transform tasks into verifiable success criteria and loop until verified. "Add validation" → "Write tests for invalid inputs, then make them pass." "Fix the bug" → "Write a test that reproduces it, then make it pass." For multi-step work, state a brief plan with a verification step per increment before starting.

These guidelines are working if: fewer unnecessary changes in diffs, clarifying questions before implementation rather than after mistakes.

---

## Project

`homemade-claude-kit` is a personal, **harness-agnostic** skill/plugin toolkit — 60 skills across 11 toggleable plugin sets (strategic-architecture docs, developer workflow, agent-execution) — authored once and installed natively into Claude Code, Codex, and OpenCode by `install.sh`, or consumed as a Claude Code marketplace (`.claude-plugin/marketplace.json`). The north star is [`docs/VISION.md`](docs/VISION.md): one authored capability, run everywhere from a single source of truth. The repo also dogfoods its own governance system: its backlog runs on the `github` open-items backend (see Domain context below).

**Stack:** Bash (`install.sh`, `scripts/`) · Python 3 stdlib (skill helper scripts under `plugins/*/skills/*/scripts/`; PyYAML available system-side for YAML validation) · YAML (skill frontmatter, GitHub Actions, `marketplace.json`) · Markdown (skills, docs, rules).
**Package manager:** none — no npm/pip project; every script is a direct interpreter invocation.

## Documentation stack (read at session start)

This project uses the homemade-claude-kit strategic-architecture metamodel.

- **Vision:** [`docs/VISION.md`](docs/VISION.md) — the north star (harness-agnostic toolkit); read it at session start to inform prioritisation and scope.
- **Index:** [`docs/index.md`](docs/index.md) — live artefact status table; run the `metamodel` skill's Scaffold Mode 3 to refresh.
- **Build order:** the `metamodel` skill — 16 steps (Vision → Implementation plans). This repo runs Step 0 (Vision) but not the full spine (it's the kit, not a product built through it) — see the note at the top of `docs/index.md`. The live surfaces here are the open-items ledger and the use-case registry, both indexed.
- **Canonical path rules, artefact registry:** the `metamodel` skill (`plugins/kit-core/skills/metamodel/`) — read it before creating or moving any `docs/**` artefact.
- **Audit:** run the `metamodel` skill's Audit mode for full health checks.
- **Scaffolded:** 2026-07-20.

Before doing any documentation work: read `docs/index.md` to know which steps are complete (✅), in progress (🔄), or not started (⬜), and which skill to invoke next.

---

## Commands

```bash
# Install / sync into ~/.claude, ~/.codex, ~/.agents. Symlinks skills+commands+rules AND
# (global installs) renders the cross-harness adapters: the AGENTS.md block for Codex/OpenCode
# and MCP configs, from templates/ + mcp/registry.json via scripts/gen-agents-md.py + gen-mcp.py.
./install.sh
./install.sh --verbose                      # per-item actions
./install.sh /path/to/project               # install into one project instead of user-global
./install.sh --claude-channel marketplace   # serve Claude via /plugin; prune ~/.claude symlinks (ADR-0006 §3)

# Regenerate per-plugin .mcp.json after editing mcp/registry.json (not run by install.sh)
python3 scripts/gen-mcp.py plugins .

# Audit skill naming, frontmatter validity, length constraints (closest thing to a linter)
./scripts/audit-skills.sh

# Validate a single skill/workflow YAML file
python3 -c "import yaml,sys; yaml.safe_load(open('<file>'))"

# Skill folder name / frontmatter name: consistency check (rules/skill-creation-sync.md)
for skill in plugins/*/skills/*/; do
  skill_name="$(basename "${skill%/}")"
  name=$(grep -m1 "^name:" "$skill/SKILL.md" | sed -E 's/name: *//; s/^"//; s/"$//')
  [ "$skill_name" != "$name" ] && echo "MISMATCH: folder=$skill_name name=$name"
done
```

No compiled build step and no automated test suite — this is a documentation + skill-definition repo. "Done" means: `audit-skills.sh` is clean, every touched YAML parses, and `install.sh` symlinks without error.

---

## What the agent may do autonomously

| Allowed without asking | Requires human approval |
|---|---|
| Read any file | `git push` / open or merge PRs |
| Edit skill/rule/doc Markdown, YAML frontmatter | Any `gh` mutation against a live repo's issues/labels/PRs — `--apply` flags on `bootstrap_labels.sh` / `backfill_execution_labels.py` / `migrate_markdown_to_github.py`, `gh issue create/edit/close` |
| Run `audit-skills.sh`, YAML validation, dry-run of any script | Running a script's `--apply` mode, or `install.sh` against a real (non-scratch) target project |
| — | Letting a background agent/fork execute a mutating action unsupervised — every live `gh --apply` / PR-merge step must happen in view of the operator, one step at a time |

## Domain context

- **open-items** — this repo's own governance backlog. It runs on the `github` backend (GitHub Issues + labels, ADR-0008/0009). Never edit its issues/labels directly — go through the `util-open-items` skill (filing, triage, close/drop) or the `agent-issue-loop` skill (validate/dedupe/take), which encode the refusal rules and evidence requirements raw `gh` calls don't.
- **metamodel** — the skill owning the canonical `docs/` build order, path map, and artefact-type registry (`plugins/kit-core/skills/metamodel/`). Read it before adding a new artefact type or moving a doc.
- **clew** ([VictorHueni/clew](https://github.com/VictorHueni/clew)) — the companion half of the harness: persistence, artefact relationships, deterministic ID minting, and audit. The kit ships agent-facing tooling; clew owns the metamodel's structural source of truth (ADR-0007), so new artefact types are authored clew-side first.
- **dotfiles** ([VictorHueni/dotfiles](https://github.com/VictorHueni/dotfiles), chezmoi) — the machine/environment layer that installs this kit: a `run_onchange_install-claude-kit.sh.tmpl` hook git-pulls this repo and runs `install.sh` on `chezmoi apply` (the kit knows nothing of dotfiles — it stays a standalone installable). **Boundary:** binaries (LSP servers, npm globals, runtimes), env vars, shell config, and harness `settings.json` live in dotfiles — never `install.sh`; the kit owns only user-global capability (skills, rules, `mcp/registry.json`). Find it with `chezmoi source-path`.
- **fork (Agent tool)** — a background subagent that inherits the caller's full conversation context. Scope fork prompts narrowly (research/read-only by default); a fork must never independently execute a mutating action (`gh --apply`, PR merge) that wasn't explicitly authorized for it to run.
