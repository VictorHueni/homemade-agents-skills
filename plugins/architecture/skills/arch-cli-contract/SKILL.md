---
name: arch-cli-contract
description: "Define the external CLI surface contract for a user-facing command-line tool — subcommand tree, per-command flags and arguments, output format contract, exit code catalogue, configuration precedence, and error contract. BC-scoped (one CLI per BC/service, ID: BC-NN.CLI-NN) or product-level spanning multiple BCs (ID: CLI-NN). Modes: scaffold, design (contract-first from FBS functionalities), document-existing (reverse-engineer from --help output or source), refresh (detect added/removed commands, emit changelog). Use when asked to design a CLI, document CLI commands, define subcommands and flags, specify exit codes, or formalise the surface of a command-line tool. Triggers on: CLI design, command line, subcommands, flags, CLI surface, shell tool, command interface, exit codes, CLI contract. Output: docs/architecture/interfaces/cli-{slug}.md."
version: "1.0.0"
status: draft
last_reviewed: 2026-05-25
review_interval: 180d
supersedes: ~
superseded_by: ~
user-invocable: true
allow_implicit_invocation: true
impact: "low"
metadata:
  category: "architecture"
  complexity: "medium"
---

# CLI Contract Builder

You are an expert at producing **stable, scriptable CLI surface contracts** — the artefacts that answer: *"what can operators and scripts depend on when invoking this tool?"*

The artefact produced by this skill is one Markdown document per CLI tool:

`docs/architecture/interfaces/cli-{slug}.md` — the complete external surface of the CLI: command tree, per-command synopsis, flags, arguments, output format, exit codes, configuration, and error contract.

This is **not a user manual or tutorial**. It is the **stable contract** between the tool and every script, pipeline, and human that invokes it. A CLI surface contract answers two questions: "what do I pass in?" and "what can I depend on coming out?"

> "Rule of Silence: when a program has nothing interesting to say, it should say nothing."
> — **Eric S. Raymond**, *The Art of Unix Programming* (2003), Chapter 1

> "Programs should be written first for human beings, and second for computers."
> — **CLI Guidelines**, clig.dev (2021)

These two principles sit in creative tension. The resolution: output meaningful data to stdout; route all diagnostic, progress, and error text to stderr; provide `--output json` for machines. Then silence is a feature, not a mystery.

---

## What a good CLI surface contract means

| Quality check | Pass condition |
|---|---|
| Every command has a `CLI-NN.CMD-NN` ID | No anonymous commands |
| Every command maps to a FBS functionality or use case | No command exists without a `C-N.M.FXX` or epic `E-NN` backing it |
| `--help` and `--version` are documented at the root | Both global flags present and described |
| stdout / stderr separation is explicit | stdout = structured output; stderr = diagnostics, progress, prompts |
| Exit code catalogue is complete | Every non-zero exit code documented with its meaning |
| Configuration precedence chain is documented | flag > env var > config file > default |
| Mutating commands have a `--dry-run` flag | Or a documented rationale for why it's omitted |
| Color output respects `NO_COLOR` and `isatty()` | Color never assumed; degraded gracefully in pipelines |
| `--output` flag supports machine-readable format | `json` at minimum; `table` (default) and `yaml` recommended |
| Destructive commands require explicit confirmation | `--force` or interactive prompt; never silent destruction |

---

## The four modes

Detect from the user's prompt. Ask if ambiguous.

### Mode 1 — Scaffold

**When:** no `docs/architecture/interfaces/cli-{slug}.md` exists yet.

**Steps:**
1. Ask the user for the tool name if not provided. Derive `{slug}` as kebab-case tool name (e.g., `acme-ctl`, `deploy-cli`).
2. Run `find docs/architecture/interfaces/ -name "cli-*.md" 2>/dev/null` to check for existing CLI artefacts.
3. Create `docs/architecture/interfaces/` if it does not exist.
4. Copy the template from `references/template.md`. Substitute `{{slug}}`, `{{tool-name}}`, `{{today}}` placeholders. Run `git config user.name` for `owner`.
5. Do NOT invent commands in scaffold mode. Leave the command tree and §4 as `_TODO_` skeletons.
6. Report: file path created; next step is Mode 2 (design) or Mode 3 (document-existing).

### Mode 2 — Design (contract-first)

**When:** FBS and/or delivery roadmap exist; the user wants to design the CLI surface from product functionalities outward.

#### Step 0 — Clarifying questions (one message; user responds e.g. "1A, 2B, 3A, 4A, 5B")

```
1. CLI scope?
   A. BC-scoped: this CLI is a direct surface for one BC/service.
      ID format: BC-NN.CLI-NN (tool surface), BC-NN.CLI-NN.CMD-NN (commands)
      — recommended for per-service tooling (orders-cli, deploy-ctl for the deployment BC)
   B. Product-level: this CLI spans multiple BCs.
      ID format: CLI-NN (tool surface), CLI-NN.CMD-NN (commands)
      — use for unified product CLIs; BC-NN column documents which BC each command delegates to

2. Command taxonomy (how to group subcommands)?
   A. Noun-verb: tool <resource> <action>  (e.g. kubectl get pods, heroku apps:create)
      — groups by resource type; scales well as the tool grows
   B. Verb-noun: tool <action> <resource>  (e.g. docker run image, npm install pkg)
      — emphasises actions; familiar in package-manager style tools
   C. Flat: no subcommands — tool is a single-purpose utility
      (e.g. jq, grep, curl)

3. Primary audience?
   A. Developers / power users — accept terse flags; assume Unix familiarity
   B. Operators / devops — prefer explicit long flags; include --dry-run everywhere
   C. Mixed — provide both short and long flags; make --dry-run the default for destructive ops

4. Machine-readable output?
   A. --output json|yaml|table (table is the default human view)
   B. --json flag (shorthand; table by default)
   C. Not required — human-readable output only

5. Configuration?
   A. Config file + env vars + flags (12-Factor; flag overrides env overrides file overrides default)
   B. Env vars + flags only (no config file)
   C. Flags only (stateless; no persistence)
```

#### Design process

1. **Read the FBS** — `docs/product-specs/07a-fbs.md`. Group functionalities by capability cluster. Each cluster is a candidate top-level noun (Mode A) or verb group.
2. **Read the delivery roadmap** — `docs/plans/delivery-roadmap.md`. Phase-1 functionalities define the MVP command set. Later phases extend the command tree — document these as `status: planned`.
3. **Derive the command tree** using the taxonomy from Step 0. Apply rules from `references/discipline.md §Command taxonomy`.
4. **Design global flags** first: `--help`, `--version`, `--output`, `--config`, `--verbose` / `--quiet`, `--no-color`. These must exist before per-command flags.
5. **Design per-command signatures** following `references/discipline.md §Flag and argument rules`. For each command: synopsis, description, positional args (required), flags (optional), output description, exit codes.
6. **Define the exit code catalogue** using the sysexits.h conventions in `references/discipline.md §Exit code catalogue`. Document every non-zero code the tool emits.
7. **Design the output contract** per `references/discipline.md §Output contract`. Determine what goes to stdout (structured result data) vs stderr (progress, errors, prompts).
8. **Define the configuration chain** per the user's choice from Step 0 and `references/discipline.md §Configuration precedence`.
9. **Assign IDs** — format depends on scope (Step 0 question 1):
   - **BC-scoped (1A):** `BC-NN.CLI-01` for the tool surface; `BC-NN.CLI-01.CMD-01`, `BC-NN.CLI-01.CMD-02`, etc. for commands.
   - **Product-level (1B):** `CLI-01` for the tool surface; `CLI-01.CMD-01`, `CLI-01.CMD-02`, etc. for commands. Add a `BC-NN` column per command documenting which BC it delegates to.
   Zero-pad to two digits. One CMD-NN ID per command.
10. Write `docs/architecture/interfaces/cli-{slug}.md` using `references/template.md`.
11. Run quality checks from `references/discipline.md §Quality checks` before delivering.

### Mode 3 — Document-existing

**When:** the tool exists; the user wants to formalise the implicit CLI contract.

**Steps:**
1. Ask for: the tool binary name and access method (`--help` output, source file paths, man page).
2. Parse the `--help` output: extract subcommands, flags, arguments, exit codes if documented.
3. For each discovered command, find the matching FBS functionality (`C-N.M.FXX`) or epic (`E-NN`). Flag commands with no product backing — these are candidates for deprecation.
4. Flag discipline violations (see `references/discipline.md §Quality checks`): missing --dry-run on mutating ops, stdout/stderr conflation, undocumented exit codes, color without isatty() check, missing --version.
5. Produce the artefact using `references/template.md`. Mark discovered commands `status: documented`; commands needing design review `status: review`.
6. Emit a **drift report**: commands found in the tool but not in the FBS; FBS functionalities not yet surfaced as commands.

### Mode 4 — Refresh

**When:** the CLI contract exists; the tool has been updated and the contract may have drifted.

**Steps:**
1. Re-read `docs/architecture/interfaces/cli-{slug}.md` and the current FBS / roadmap.
2. **Detect additions** — new FBS functionalities without corresponding CLI-NN.CMD-NN entries. These are gaps to add.
3. **Detect removals** — CLI-NN.CMD-NN entries for FBS rows that have been dropped. Mark as `status: deprecated` with a removal date.
4. **Detect flag changes** — flags renamed or removed. Classify per `references/discipline.md §Breaking change classification`.
5. **Detect exit code drift** — new non-zero exit codes added to the code but absent from the catalogue. Add them with meaning.
6. Write targeted updates only: add new entries, mark deprecated entries, append a `## Changelog` row. Do NOT rewrite the entire document.

---

## The seven anti-patterns

1. **Stdout / stderr conflation.** Progress bars, log lines, and error messages written to stdout. Anything written to stdout that is not the structured result of the command breaks pipelines. `grep $(mytool list) file.txt` silently includes progress text in the grep input. Hard rule: stdout for the result; stderr for everything the *operator* needs to see but the *script* should not process.

2. **Silent failure.** The command exits 0 on error, or exits non-zero with no message. POSIX: any non-zero exit signals failure. The operator or calling script cannot distinguish success from failure without inspecting stdout. Rule of Silence (ESR) means silence on success — it does not mean silence on failure.

3. **Missing `--dry-run` on mutating commands.** Any command that deletes, deploys, modifies infrastructure, or sends messages must have a `--dry-run` flag that executes all validation and prints what would happen without making changes. Without it, every operator must either trust the command or build a test environment.

4. **Color in pipelines.** ANSI escape codes written to stdout without checking `isatty()` and `NO_COLOR`. `mytool list | jq '.[0]'` produces `\e[32m{"id":"abc"}\e[0m` — jq fails. Rule: check `isatty(stdout)` before emitting color; also check the `NO_COLOR` environment variable (no-color.org) and `TERM=dumb`.

5. **Undocumented exit codes.** The tool exits 2 for one type of error and 3 for another, but the contract says nothing beyond 0 and 1. CI pipelines switch on exit codes; undocumented non-zero values force consumers to reverse-engineer the tool's behavior.

6. **Flag name inconsistency.** The tool uses `--file` in one command and `--filename` in another; `--output` in some and `--format` in others. Global flags must be global. Per-command flags for similar concepts must use the same name.

7. **Destructive default.** `mytool delete resource-name` deletes immediately with no confirmation prompt and no `--force` requirement. Destructive operations must require either an interactive confirmation prompt (when the terminal is a TTY) or an explicit `--force` / `--yes` flag (when non-interactive).

---

## Flag and argument rules (summary)

Full rules in `references/discipline.md §Flag and argument rules`.

| Rule | Correct | Wrong |
|---|---|---|
| Long flags for all options | `--output json` | `-o json` only |
| Short flags only for the most-used options | `-o` as alias for `--output` | Short flag for every option |
| Mandatory global flags | `--help`, `--version` on root command | Either absent |
| Positional args for the primary subject | `mytool get ORDER_ID` | `mytool get --id ORDER_ID` |
| Flags for modifiers and options | `mytool list --status=shipped` | `mytool list shipped` (ambiguous) |
| `--` ends flag parsing | `mytool run -- --flag-for-subprocess` | Not supported |
| Boolean flags do not take values | `--verbose`, not `--verbose=true` | `--verbose=true` |
| Destructive ops require `--force` or prompt | `mytool delete ID --force` | `mytool delete ID` (immediate) |

---

## Output contract rules (summary)

Full rules in `references/discipline.md §Output contract`.

- **stdout** = the structured result of the command (the data the calling script will process).
- **stderr** = diagnostics, progress, warnings, prompts — the data the operator needs, the script ignores.
- **Default output**: human-readable table or text — designed to be read, not parsed.
- **Machine output**: `--output json` emits newline-delimited JSON (one object per line for lists) to stdout. `--output yaml` for config-style output. Scripts should always use `--output json`.
- **Color**: conditional on `isatty(stdout)` AND `NO_COLOR` not set AND `TERM != "dumb"`. Always off for `--output json` and `--output yaml`.
- **Progress and spinners**: always to stderr; suppressed with `--quiet`.
- **Empty output**: a command that finds no results exits 0 and prints nothing (Rule of Silence). A `--output json` empty result is `[]`, not a missing line.

---

## Finding the right folder

**Default:** `docs/architecture/interfaces/`

**Filename:** `cli-{slug}.md` where `{slug}` is the kebab-case tool name.

The `cli-` prefix distinguishes CLI surface files from API surface files in the same folder.

Check first:
```bash
find docs/architecture -name "cli-*.md" 2>/dev/null
```

**Never overwrite.** If `cli-{slug}.md` already exists:
- Scaffold → skip; report what's there; suggest Mode 4 (Refresh).
- Design → update `_TODO_` sections; preserve all filled content.
- Document-existing → append; update; emit drift report.
- Refresh → targeted updates + changelog entry only.

---

## Cross-reference — the architecture-artefact lifecycle

| Artefact | Relationship |
|---|---|
| **spec-functional-breakdown-structure (`C-N.M.FXX`)** | Primary input — each CLI command should map to one or more FBS functionalities |
| **plan-delivery-roadmap (`E-NN`)** | Epic groupings drive command release phases; Phase 1 epics define the MVP command set |
| **domain-bounded-context (`BC-NN`)** | Each command typically delegates to one BC; document which BC per command |
| **spec-quality-attributes (`QA-XXNN`)** | `QA-PE` entries → response time SLA per command; `QA-US` entries → help text quality standards |
| **arch-adr (`ADR-NNNN`)** | CLI design decisions → ADRs (taxonomy choice noun-verb vs verb-noun; config file format; output format strategy) |
| **spec-prd (`PRD-NNNN`)** | PRDs for CLI-facing features reference `CLI-NN.CMD-NN` IDs in acceptance criteria |
| **arch-service-contract (`BC-NN.CTR-NN`)** | CLI commands often wrap service contract calls; each command can reference the CTR-NN it delegates to |

---

## Reference materials

- **`references/template.md`** — canonical `cli-{slug}.md` skeleton; copy and fill placeholders.
- **`references/methodology-references.md`** — full bibliography: POSIX Utility Conventions, GNU Coding Standards, ESR *Art of Unix Programming*, CLI Guidelines (clig.dev), 12-Factor Config, sysexits.h, NO_COLOR. Lives only in the kit.
- **`references/discipline.md`** — internal Claude guidance: command taxonomy rules, flag naming conventions, exit code catalogue, output contract rules, configuration precedence, quality checks. Never copied to projects.

---

## Closing report

After any mode, deliver in 6–8 lines:

1. **Mode executed** + tool name + file path created or updated.
2. **Command count** — total CLI-NN.CMD-NN entries; breakdown by status (active / planned / deprecated).
3. **Output contract** — stdout/stderr separation explicit (yes/no); `--output json` supported (yes/no).
4. **Exit codes** — number of non-zero codes documented.
5. **Configuration** — precedence chain documented (yes/no); config file format stated (yes/no).
6. **Discipline checks** — passed / failed (list failures with CMD-NN and rule violated).
7. **Anti-patterns detected** — list which ones, which commands.
8. **Next steps** — ADRs for command taxonomy and config format choices; PRDs should reference CLI-NN.CMD-NN IDs; spec-quality-attributes for performance SLA per command.

---

## Checklist

Before declaring the work done:

- [ ] `docs/architecture/interfaces/` folder exists.
- [ ] `docs/architecture/interfaces/cli-{slug}.md` exists.
- [ ] Standard artefact frontmatter present (OKF-superset block — set `type` to this artefact's `okf_type` display name from the `metamodel` skill's `references/artefact-types-registry.yaml`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`). Run `git config user.name` for owner. Set `status: draft` on initial scaffold. Default `review_interval: 180d`. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`.
- [ ] Every CLI-NN.CMD-NN entry maps to a FBS functionality (`C-N.M.FXX`) or epic (`E-NN`).
- [ ] `--help` and `--version` documented as global flags.
- [ ] stdout / stderr separation explicit in §5 Output contract.
- [ ] `--output json` (or equivalent machine-readable flag) documented.
- [ ] Exit code catalogue present; every non-zero code documented.
- [ ] `--dry-run` present on all mutating commands (or explicit rationale for omission).
- [ ] Destructive commands require `--force` or interactive confirmation documented.
- [ ] Color output policy documented: `NO_COLOR`, `isatty()`, `TERM=dumb`.
- [ ] Configuration precedence chain documented in §6.
- [ ] CLI-NN.CMD-NN IDs assigned monotonically; no gaps.
- [ ] `## Changelog` section present with at least the creation entry.
- [ ] Closing report delivered.
