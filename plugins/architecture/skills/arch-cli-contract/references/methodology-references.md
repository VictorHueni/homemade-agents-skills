# CLI Contract — Methodology References

Canonical bibliography for the `arch-cli-contract` skill. Lives only in the kit — never copied to projects. Project docs link here via the methodology pointer in their header.

---

## Unix philosophy and foundational design

### Raymond, Eric S. (2003)
*The Art of Unix Programming*. Addison-Wesley.
https://www.catb.org/esr/writings/taoup/html/

The authoritative statement of Unix design principles. Key rules for CLI design:

- **Rule of Modularity**: write simple parts connected by clean interfaces. A CLI is a module in a larger pipeline.
- **Rule of Composition**: design programs to be connected with other programs. This is why stdout must carry structured output and stderr must carry operator messages.
- **Rule of Separation**: separate policy (what to do) from mechanism (how to do it). Flags choose policy; the tool provides the mechanism.
- **Rule of Silence**: when a program has nothing interesting to say, it should say nothing. Exit 0 and produce no output on success unless output is the purpose. Do not produce "Done." or "Success!" confirmations.
- **Rule of Repair**: when you must fail, fail noisily — emit a clear error to stderr and exit non-zero.
- **Rule of Parsimony**: write a big program only when nothing else will do. Single-purpose tools are better than multi-purpose ones.
- **Rule of Least Surprise**: do the least surprising thing. Follow POSIX conventions; don't invent new flag syntax.

### POSIX.1-2017 — Utility Conventions (Section 12)
https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html

The formal standard for Unix utility command-line syntax. Key conventions:

- **Option syntax**: `-c` (single character) or `--long-name` (multi-character, GNU extension).
- **Option with argument**: `-c argument` or `-cargument` (both valid for single-char options); `--name argument` or `--name=argument`.
- **`--` end of options**: all subsequent arguments are treated as operands (non-options), not flags. Every CLI must support `--`.
- **`-` as operand**: conventionally means stdin (for input) or stdout (for output).
- **Short options can be combined**: `-abc` means `-a -b -c` when none of them take an argument.
- **Operands (positional arguments)**: come after all options.

### GNU Coding Standards — Program Behavior (Chapter 4)
https://www.gnu.org/prep/standards/standards.html#Program-Behavior

GNU's standards for command-line programs. Key conventions:

- **`--help`**: every program must support `--help`; output goes to stdout; exit 0.
- **`--version`**: every program must support `--version`; outputs `program-name version-number\n` to stdout; exit 0.
- **Long option names**: GNU popularised `--long-option` syntax. Long options must be supported.
- **Error messages**: format is `program-name: message\n` to stderr. The program name prefix is critical for pipeline debugging.
- **Exit status**: 0 for success; 1 for general error; 2 for misuse of the program (wrong arguments). Do not use exit status > 2 for anything other than sysexits.h conventional codes.

---

## Modern CLI design guidelines

### Kross, Brendan; Lopes, Nina; McKinnon, Ben; Bevans, Mark (2021)
*Command Line Interface Guidelines*. clig.dev.
https://clig.dev

The most comprehensive modern CLI design guide. Key principles:

**Human-first, machine-friendly:**
- Default output is designed for humans (readable, aligned tables, color where appropriate).
- Machine output (`--output json`) is unambiguous, consistent, and parseable.
- Never conflate the two; never make the human output parseable via regex.

**stdout / stderr separation:**
- stdout: the output of the command — the data the script will process.
- stderr: informational messages for the operator — progress, warnings, prompts, debug output.
- This separation is the foundation of Unix pipeline composability.

**Color and formatting:**
- Use color to highlight important information; never use it as the only differentiator.
- Check `isatty(stdout)` before emitting color. Disable color when writing to a pipe or file.
- Respect `NO_COLOR` environment variable (no-color.org).
- Respect `TERM=dumb` — some terminals cannot render ANSI codes.

**Prompts and interactivity:**
- Interactive prompts go to stderr (they are operator messages, not output).
- When stdin is not a TTY (i.e., the program is being called non-interactively), never prompt — fail immediately with a clear error message explaining what flag is required.
- Always provide a non-interactive override (`--force`, `--yes`, `--input=FILE`) for every interactive flow.

**Exit codes:**
- 0 = success, always.
- Non-zero = failure, always.
- Document every non-zero exit code the tool can emit.

**Signals:**
- Handle `SIGINT` (Ctrl+C) gracefully. Clean up temporary state. Exit with code 130 (128 + signal 2).

---

## Configuration and environment

### Wiggins, Adam (2011) — The Twelve-Factor App
https://12factor.net/config (Factor III: Config)

Store config in the environment. Config that varies between environments (dev, staging, production) should come from environment variables, not hardcoded in code or committed config files.

**Precedence rule for CLIs** (extends 12-Factor):
```
explicit flag > environment variable > config file > built-in default
```
This ordering is canonical for CLI tools. Higher priority sources override lower. Document this chain explicitly in the contract.

---

## Exit codes

### sysexits.h — BSD exit code conventions
Originally from BSD Unix (`/usr/include/sysexits.h`). Widely adopted as the standard for machine-readable exit code semantics.

| Code | Constant | Meaning |
|---|---|---|
| 0 | EX_OK | Successful termination |
| 64 | EX_USAGE | Command line usage error — wrong flags, missing required argument |
| 65 | EX_DATAERR | Data format error — input data was incorrect |
| 66 | EX_NOINPUT | Cannot open input — file does not exist or is not readable |
| 67 | EX_NOUSER | Addressee unknown — user does not exist |
| 68 | EX_NOHOST | Host name unknown — host does not exist |
| 69 | EX_UNAVAILABLE | Service unavailable — external dependency unreachable |
| 70 | EX_SOFTWARE | Internal software error — unexpected condition |
| 71 | EX_OSERR | System error — OS-level failure (fork, signal, etc.) |
| 72 | EX_OSFILE | Critical OS file missing |
| 73 | EX_CANTCREAT | Cannot create output file |
| 74 | EX_IOERR | Input/output error |
| 75 | EX_TEMPFAIL | Temporary failure — caller may retry |
| 76 | EX_PROTOCOL | Remote error in protocol |
| 77 | EX_NOPERM | Permission denied |
| 78 | EX_CONFIG | Configuration error — config file missing or malformed |
| 130 | — | Terminated by Ctrl+C (SIGINT — 128 + 2) |
| 131 | — | Terminated by Ctrl+\ (SIGQUIT — 128 + 3) |

**Practical advice**: use sysexits.h codes for categories; define tool-specific codes in the 3–63 range for domain errors. Document all non-zero codes in the CLI surface contract.

---

## Output standards

### Kehoe, Ines (2018) — NO_COLOR
https://no-color.org

When the environment variable `NO_COLOR` is set (to any value, including empty string), command-line software must not add ANSI color escape codes to output. No exceptions.

Implementation check before emitting any color:
```python
import os, sys
use_color = sys.stdout.isatty() and "NO_COLOR" not in os.environ and os.environ.get("TERM") != "dumb"
```

### ECMA-48 (1991) — Control Functions for Coded Character Sets
The standard defining ANSI escape codes (e.g., `\e[32m` for green, `\e[0m` for reset). Relevant to know which codes are widely supported; terminal support is not universal.

---

## Design patterns referenced

### Cobra (Go) — CLI framework conventions
https://github.com/spf13/cobra

The dominant Go CLI framework (used by kubectl, Hugo, GitHub CLI, Docker CLI). Establishes:
- Noun-verb command structure: `cobra add command-name`.
- Persistent flags (inherited by sub-commands) vs local flags (command-only).
- `--completion` flag for shell autocompletion scripts.

### Click (Python) — CLI framework conventions
https://click.palletsprojects.com

Decorator-based Python CLI framework. Establishes:
- Context-aware help generation.
- Argument vs option distinction: arguments are positional (required); options are `--flag` (optional).
- Multi-value options with `nargs`.
- `@click.confirmation_option` pattern for destructive operations.

### kubectl command design (Kubernetes, 2014–present)
https://kubernetes.io/docs/reference/kubectl/

The most widely deployed noun-verb CLI. Key lessons:
- `kubectl <verb> <noun>` — `kubectl get pods`, `kubectl delete deployment/nginx`.
- `--output` / `-o` for format selection: `json`, `yaml`, `wide`, `name`, custom columns.
- `--dry-run=client` for validation without server-side execution.
- `--watch` / `-w` for long-running stream output.
- Exit code 1 on any error; exit code 0 only on full success.
