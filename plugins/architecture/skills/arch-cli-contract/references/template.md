---
title: "{Tool name} — CLI Contract"
status: draft
owner: _TODO_
last_reviewed: {{today}}
review_interval: 180d
---

# {Tool name} — CLI Contract

> **Methodology:** built on POSIX Utility Conventions (Section 12), GNU Coding Standards (Chapter 4), ESR *Art of Unix Programming* (2003), CLI Guidelines (clig.dev, 2021), 12-Factor Config, and sysexits.h exit code conventions. Full bibliography: [methodology-references.md](https://github.com/VictorHueni/homemade-claude-kit/tree/main/arch-cli-contract/references/methodology-references.md).

**Tool name:** `{toolname}`
**Scope:** the external CLI surface of `{Tool name}`. This document defines what operators and scripts can depend on. Internal implementation details are not part of this contract.

**Companion documents:**
- FBS: [../../product-specs/07a-fbs.md](../../product-specs/07a-fbs.md)
- Delivery roadmap: [../../plans/delivery-roadmap.md](../../plans/delivery-roadmap.md)
- Quality attributes: [../../product-specs/09a-quality-attributes.md](../../product-specs/09a-quality-attributes.md)

---

## §0 Traceability

| Field | Value |
|---|---|
| **Tool name** | `{toolname}` |
| **Command taxonomy** | _TODO_ (noun-verb / verb-noun / flat) |
| **FBS functionalities surfaced** | _TODO_ (`C-N.M.FXX`) |
| **Epics** | _TODO_ (`E-NN`) |
| **ADRs** | _TODO_ (`ADR-NNNN` — taxonomy choice, config format, output format) |
| **Current version** | _TODO_ (`1.0.0`) |

---

## §1 Command tree

```
{toolname} [global-flags]
├── {noun-or-verb}              # _TODO_
│   ├── {action} [flags] <arg>  # _TODO_
│   └── {action} [flags] <arg>  # _TODO_
└── {noun-or-verb}              # _TODO_
    └── {action} [flags] <arg>  # _TODO_
```

---

## §2 Command catalogue

| CMD-NN | Command path | Synopsis | FBS ref | BC-NN | Status |
|---|---|---|---|---|---|
| CLI-01.CMD-01 | `{toolname} {noun} {verb}` | _TODO_ | _TODO_ | _TODO_ | draft |

---

## §3 Global flags

Flags inherited by all subcommands.

| Flag | Short | Type | Default | Description |
|---|---|---|---|---|
| `--help` | `-h` | boolean | false | Print command help and exit 0. Output to stdout |
| `--version` | — | boolean | false | Print `{toolname} {version}` and exit 0. Root command only |
| `--output` | `-o` | string | `table` | Output format: `table` (default), `json`, `yaml` |
| `--config` | — | string | `~/.{toolname}.yaml` | Path to config file |
| `--verbose` | `-v` | boolean | false | Enable verbose output (to stderr) |
| `--quiet` | `-q` | boolean | false | Suppress all non-essential output (to stderr) |
| `--no-color` | — | boolean | false | Disable ANSI color output |

`--` (double dash) ends flag parsing. All subsequent tokens are treated as positional arguments.

---

## §4 Per-command definitions

### CLI-01.CMD-01 · `{toolname} {noun} {verb}`

**Synopsis:** `{toolname} {noun} {verb} <REQUIRED_ARG> [flags]`
**Description:** _TODO_
**FBS ref:** [_TODO_ C-N.M.FXX](../../product-specs/07a-fbs.md#TODO)
**BC delegates to:** [_TODO_ BC-NN](../../domain/02b-bounded-contexts.md#TODO)
**Status:** draft (active / planned / deprecated)

#### Arguments

| Name | Required | Description |
|---|---|---|
| `REQUIRED_ARG` | yes | _TODO_ |

#### Flags

| Flag | Short | Type | Default | Description |
|---|---|---|---|---|
| `--flag-one` | `-f` | string | — | _TODO_ |
| `--dry-run` | `-n` | boolean | false | Print what would happen without making changes. Exits 0 if operation would succeed |
| `--force` | — | boolean | false | Skip confirmation prompt (required for non-interactive use of destructive operations) |

#### Output

**Default (`--output table`):**
```
FIELD_ONE    FIELD_TWO    STATUS
value-a      value-b      active
```

**Machine-readable (`--output json`, one object per line):**
```json
{"field_one":"value-a","field_two":"value-b","status":"active"}
```

#### Exit codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | General error |
| `64` | Usage error — wrong flags or missing required argument |
| _TODO_ | _TODO_ |

#### Examples

```bash
# Basic usage
{toolname} {noun} {verb} REQUIRED_ARG

# With flag
{toolname} {noun} {verb} REQUIRED_ARG --flag-one value

# Dry run
{toolname} {noun} {verb} REQUIRED_ARG --dry-run

# Machine-readable output
{toolname} {noun} {verb} REQUIRED_ARG --output json
```

---

## §5 Output contract

### stdout / stderr separation

| What | Destination |
|---|---|
| Structured result data (the answer to the command) | **stdout** |
| Progress indicators, spinners, countdowns | **stderr** |
| Warning messages | **stderr** |
| Error messages and stack traces | **stderr** |
| Interactive prompts | **stderr** |
| Verbose / debug output | **stderr** |
| `--help` output | **stdout** |
| `--version` output | **stdout** |

### Output formats

| Format | Flag | Content |
|---|---|---|
| Table | `--output table` (default) | Human-readable, aligned columns with headers. Color when TTY |
| JSON | `--output json` | Newline-delimited JSON (NDJSON). One object per line. No wrapping array |
| YAML | `--output yaml` | Standard YAML. One document per resource |

### Color policy

Color is enabled only when all three conditions are true:

1. `stdout` is a TTY (`isatty(stdout) == true`)
2. `NO_COLOR` environment variable is NOT set
3. `TERM != "dumb"`

`--output json` and `--output yaml` always suppress color regardless of terminal state. `--no-color` flag forces color off for all formats.

### Empty result handling

A command that finds no results: exits 0, prints nothing to stdout. For `--output json`: prints nothing (not `null`, not `[]`). Non-zero output for "no results" is a design error — it breaks pipelines.

---

## §6 Configuration

### Precedence chain

```
flag (highest priority)
  └─ environment variable
       └─ config file
            └─ built-in default (lowest priority)
```

### Environment variables

| Variable | Corresponding flag | Default |
|---|---|---|
| `{TOOLNAME}_OUTPUT` | `--output` | `table` |
| `{TOOLNAME}_CONFIG` | `--config` | `~/.{toolname}.yaml` |
| `{TOOLNAME}_VERBOSE` | `--verbose` | — |
| `{TOOLNAME}_NO_COLOR` | `--no-color` | — |

### Config file format

**Search order** (first match wins):
1. Path from `--config` flag
2. `${TOOLNAME}_CONFIG` environment variable
3. `~/.config/{toolname}/{toolname}.yaml` (XDG Base Directory)
4. `~/.{toolname}.yaml` (home-dir dotfile)
5. `./{toolname}.yaml` (project-local config)

**Minimal config file:**
```yaml
output: json
# All keys map directly to long flag names with hyphens replaced by underscores
```

---

## §7 Error contract

All error messages are emitted to **stderr**. Format per GNU Coding Standards:

```
{toolname}: {error message}
```

For multi-line errors:
```
{toolname}: {primary error message}
  {additional context line 1}
  {additional context line 2}
```

### Exit code catalogue

| Code | Meaning | When emitted |
|---|---|---|
| `0` | Success | Operation completed without error |
| `1` | General error | Unclassified failure |
| `64` | Usage error | Wrong flags, missing required argument, conflicting options |
| `65` | Data error | Input data is malformed or in the wrong format |
| `66` | Input unavailable | Required file or resource does not exist |
| `69` | Service unavailable | External API or dependency unreachable |
| `70` | Internal error | Unexpected condition; likely a bug; please report |
| `75` | Temporary failure | Transient error; safe to retry |
| `77` | Permission denied | Authenticated but not authorised for this operation |
| `78` | Configuration error | Config file missing, malformed, or contains invalid values |
| `130` | Interrupted | Ctrl+C (SIGINT) received; partial operations cleaned up |

*Add tool-specific codes (3–63) below this line.*

---

## Changelog

| Date | Change | Author |
|---|---|---|
| {{today}} | Initial scaffold | _TODO_ |
