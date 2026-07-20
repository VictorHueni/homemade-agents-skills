# CLI Contract — Discipline Guide

Internal Claude guidance for the `arch-cli-contract` skill. Not copied to projects.

---

## Command taxonomy

### Noun-verb vs verb-noun: choose one and commit

**Noun-verb** (`tool <resource> <action>`):
```
kubectl get pods
kubectl delete deployment/nginx
heroku apps:create my-app
```
- Groups subcommands by the *thing being acted on*.
- Scales well: as the tool grows, `kubectl resource verb` remains discoverable.
- Discovery: type `tool resource` + TAB to see all actions on that resource.
- Best for: tools managing multiple resource types (infrastructure, admin, k8s-style).

**Verb-noun** (`tool <action> <resource>`):
```
docker run image
docker push image
npm install package
```
- Groups subcommands by *what you are doing*.
- Familiar for task-oriented tooling (install, run, build, test).
- Best for: package managers, build tools, workflow tools where actions are the primary mental model.

**Flat** (no subcommands):
```
curl https://example.com
jq '.name' file.json
```
- Single-purpose tools; one core operation; flags modify behavior.
- Best for: utilities, filters, single-purpose processors.

**Rule:** choose one taxonomy and apply it uniformly. Never mix noun-verb and verb-noun in the same tool. Document the choice in the CLI surface contract and in an ADR if non-obvious.

### Depth heuristic

| Tool size | Recommended depth | Example |
|---|---|---|
| ≤ 5 operations | Flat or 1-level | `mytool --flag action` |
| 5–20 operations | 1-level subcommands | `mytool <verb> [args]` |
| 20–100 operations | 2-level (noun-verb or verb-noun) | `mytool <noun> <verb>` |
| > 100 operations | 3-level max | `mytool <noun> <sub-noun> <verb>` |

Never go beyond 3 levels. If you need more, the tool is doing too many things.

---

## Flag and argument rules

### Argument vs flag distinction

- **Positional argument** (operand): the *primary subject* of the command — the thing being acted on. Required. Comes after all flags.
- **Flag** (option): modifies the command's behavior or provides secondary input. Optional unless documented as required.

```
mytool get ORDER_ID              # ORDER_ID is a positional argument (the subject)
mytool list --status=shipped     # --status is a flag (a filter modifier)
mytool delete ORDER_ID --force   # ORDER_ID is positional; --force is a flag
```

Flags for the *subject* of the command (e.g., `--id`) are a smell: if you find yourself writing `mytool get --id ORDER_ID`, make `ORDER_ID` a positional argument instead.

### Long and short flags

- **Always provide the long form** (`--output`, `--verbose`, `--dry-run`).
- **Short forms** (`-o`, `-v`) are aliases, not the primary form. Only add short forms for flags that are typed frequently. Do not add short forms for every flag — flag collisions are confusing.
- **Standard short aliases** (follow these; do not reassign):
  - `-h` → `--help`
  - `-v` → `--verbose` (or `--version` on the root command only)
  - `-o` → `--output`
  - `-q` → `--quiet`
  - `-f` → `--file` or `--force` (choose one per tool; document it)
  - `-n` → `--dry-run` or `--name` (common in kubectl/docker)
  - `-y` → `--yes` (skip confirmation prompts)

### Boolean flags

Boolean flags do not take a value:
```
--verbose      (not --verbose=true)
--no-color     (negation form for flags that default to true)
```

For a flag that defaults to `true` and can be disabled, the negation form is `--no-{flag}`:
```
--color / --no-color
--progress / --no-progress
```

### The `--` end-of-options marker

Every CLI must support `--` as the end-of-options marker. Everything after `--` is treated as a positional argument, not a flag. Required for passing flags to subprocesses:
```
mytool run -- --flag-for-subprocess
```

### Global flags (inherited by all subcommands)

These must be present on the root command and inherited by all subcommands:

| Flag | Type | Default | Description |
|---|---|---|---|
| `--help` / `-h` | boolean | false | Print help and exit 0 |
| `--version` | boolean | false | Print version string and exit 0. Root command only |
| `--output` / `-o` | string | `table` | Output format: `table`, `json`, `yaml` |
| `--config` | string | `~/.{tool}.yaml` | Path to config file |
| `--verbose` / `-v` | boolean | false | Enable verbose/debug output (to stderr) |
| `--quiet` / `-q` | boolean | false | Suppress all non-essential output (to stderr) |
| `--no-color` | boolean | false | Disable ANSI color output |

---

## Exit code catalogue

### Standard codes

| Code | Meaning | When to use |
|---|---|---|
| 0 | Success | Command completed successfully; no errors |
| 1 | General error | Catch-all for errors not covered by more specific codes |
| 64 | Usage error (EX_USAGE) | Wrong flags, missing required argument, conflicting options |
| 65 | Data error (EX_DATAERR) | Input data is in the wrong format |
| 66 | Input unavailable (EX_NOINPUT) | Required file or resource does not exist |
| 69 | Service unavailable (EX_UNAVAILABLE) | External API or dependency unreachable |
| 70 | Internal error (EX_SOFTWARE) | Unexpected condition; likely a bug |
| 75 | Temporary failure (EX_TEMPFAIL) | Transient error; safe to retry |
| 77 | Permission denied (EX_NOPERM) | Authenticated but not authorised for the operation |
| 78 | Configuration error (EX_CONFIG) | Config file missing, malformed, or contains invalid values |
| 130 | Interrupted by Ctrl+C | Process received SIGINT (128 + 2) |
| 131 | Interrupted by Ctrl+\ | Process received SIGQUIT (128 + 3) |

### Rules

- Exit 0 if and **only if** the operation succeeded.
- Exit non-zero for **any** failure — even partial failures.
- Document every non-zero code the tool emits in the CLI surface contract §7.
- In pipelines: a non-zero exit from any command should stop the pipeline (using `set -e` or `pipefail`). Do not absorb errors and return 0.
- For commands with `--dry-run`: dry-run should exit 0 if the *simulated* operation would succeed, non-zero if it would fail. This makes dry-run useful for validation in CI.

---

## Output contract

### stdout / stderr separation

| What | Where | Rule |
|---|---|---|
| Structured result data (the output of the command) | stdout | Always |
| Progress indicators, spinners, countdowns | stderr | Always |
| Warning messages | stderr | Always |
| Error messages | stderr | Always |
| Interactive prompts | stderr | Always |
| Debug / verbose output | stderr | Always |
| Help text (`--help`) | stdout | Exit 0 |
| Version string (`--version`) | stdout | Exit 0 |

**The pipeline test**: every byte written to stdout must be safe to pipe into another command (`| jq`, `| grep`, `| xargs`). If progress text can appear on stdout, the pipeline breaks.

### Output formats

| Format | Flag value | Content | When to use |
|---|---|---|---|
| Table | `--output table` (default) | Human-readable, aligned, with headers. Color if TTY. | Interactive terminal use |
| JSON | `--output json` | Newline-delimited JSON: one JSON object per line for lists; one object for single resources. No wrapping array for streams. | Scripting, CI, piping to `jq` |
| YAML | `--output yaml` | Standard YAML. One document per resource. | Config-style output; Kubernetes manifests |

**JSON output rules:**
- For a single resource: `{"id":"abc","name":"foo"}\n`
- For a list: one JSON object per line (NDJSON / JSON Lines format): `{"id":"a"}\n{"id":"b"}\n`. Not a JSON array `[...]` — arrays don't stream well.
- For an empty list: print nothing (empty stdout). Exit 0.
- For `--output json`, always suppress color and progress output entirely.

### Color policy

Check all three conditions before emitting any ANSI color:

```
use_color = isatty(stdout)
         && NO_COLOR not set in environment
         && TERM != "dumb"
         && output_format == "table"
```

Any condition failing → no color. This is not optional. Piped output or `--output json` must never contain ANSI escape codes.

### Empty result handling (Rule of Silence)

A command that finds no results: exits 0, prints nothing to stdout (or `[]` for `--output json`). Do not print "No results found." to stdout — that breaks pipelines. Print "No results." to stderr if informing the operator is valuable.

---

## Configuration precedence

Documented as a strict priority chain. Higher in the list wins:

```
1. Explicit flag          --output json
2. Environment variable   MYTOOL_OUTPUT=json
3. Config file            output: json  (in ~/.mytool.yaml)
4. Built-in default       table
```

**Environment variable naming convention:** `{TOOL_NAME_UPPER}_{FLAG_NAME_UPPER}` with hyphens replaced by underscores. `--output` → `MYTOOL_OUTPUT`. `--config` → `MYTOOL_CONFIG`.

**Config file location search order:**
1. Path from `--config` flag (if provided)
2. `$MYTOOL_CONFIG` env var (if set)
3. `~/.config/{tool-name}/{tool-name}.yaml` (XDG Base Directory)
4. `~/.{tool-name}.yaml` (legacy home-dir dotfile)
5. `./{tool-name}.yaml` (project-local config)

Document which search order the tool uses in §6 Configuration.

---

## Dry-run rule

Any command that:
- Deletes or modifies a resource
- Deploys, applies, or syncs infrastructure
- Sends a message, email, webhook, or notification
- Writes to a database or file system
- Charges money

**Must** have a `--dry-run` flag that:
- Validates all inputs (authentication, authorisation, schema)
- Outputs what *would* happen without making any changes
- Exits 0 if the operation would succeed, non-zero if it would fail
- Is clearly marked in the output: "DRY RUN — no changes were made"

`--dry-run` output goes to stdout in the same format as a real run, so CI pipelines can validate it.

**If `--dry-run` is deliberately omitted** (e.g., the operation is already idempotent and has no side effects), document the rationale explicitly in the command definition.

---

## Destructive command safety

Destructive commands (irreversible delete, purge, nuke, drop) must require one of:
- Interactive confirmation prompt: "Are you sure you want to delete X? [y/N]" — only when stdin is a TTY.
- Explicit `--force` or `--yes` flag — required for non-interactive (scripted) use.
- Both: interactive prompt when TTY; `--force` silences it for scripting.

When stdin is not a TTY and `--force` is absent: fail with exit 64 (usage error) and a message explaining the required flag.

**Never** have a destructive command succeed silently without confirmation or a force flag.

---

## Breaking change classification for CLI

### Non-breaking

- Adding a new subcommand
- Adding a new optional flag to an existing command
- Adding a new output field (in `--output json`) — consumers using the Tolerant Reader pattern ignore unknown fields
- Adding a new non-zero exit code for a *new* error condition not previously reachable
- Adding a new value to the `--output` flag's accepted set
- Improving help text, descriptions, or error messages

### Breaking

- Removing or renaming a subcommand
- Removing or renaming a flag (even if undocumented — Hyrum's Law)
- Changing the positional argument count or order
- Removing an output field (in `--output json`)
- Changing the type of an output field
- Changing a previously-defined exit code to mean something different
- Changing the behavior of an existing flag (same flag name, different semantics)
- Changing config file format or field names

---

## Quality checks

Run before closing any mode. Report failures with CMD-NN and rule.

| Check | How to verify |
|---|---|
| Every CMD-NN maps to a FBS functionality or epic | Cross-reference CMD list against FBS + roadmap |
| `--help` and `--version` on root command | Both present in §3 Global flags |
| stdout / stderr separation documented | §5 explicitly states what goes where |
| `--output json` supported | §5 Output formats table includes json |
| Exit code catalogue present and complete | §7 has a non-zero code entry for every documented failure mode |
| Dry-run on all mutating commands | Every command that writes/deletes has `--dry-run`, or rationale is documented |
| Destructive commands require `--force` or prompt | Check delete, purge, drop, nuke commands in CMD catalogue |
| Color policy documented | §5 mentions `NO_COLOR`, `isatty()`, `TERM=dumb` |
| Configuration precedence documented | §6 states flag > env > config file > default chain |
| `--` end-of-options supported | Noted in §3 or per-command definition |
| CMD-NN IDs monotonic, no gaps | List all; verify consecutive |
