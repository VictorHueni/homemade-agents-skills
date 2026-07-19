---
name: util-docs-lint
description: "Local-first docs/ quality toolchain for Markdown — format (dprint), prose style (Vale + Microsoft), links (lychee). Tools are referenced, not installed (pinned via mise/dotfiles); rules live in project-root configs dprint.json / .vale.ini / lychee.toml. Five modes: scaffold (write root configs + .gitignore), audit (read-only dprint check + vale + lychee, ranked issues), enforce (dprint fmt writes formatting fixes incl. un-hard-wrapping prose — prose/link findings are report-only, never auto-rewritten), scaffold-ci (GitHub Actions workflow), add-glossary (Vale Local style from docs/domain/02c-glossary.md aliases). Scope: docs/**. Triggers on: docs lint, lint docs, markdown lint, dprint, vale, lychee, prose lint, dead links, link check, docs quality, audit docs, fix markdown formatting, un-hard-wrap, docs CI, scaffold docs lint."
version: "2.0.0"
user-invocable: true
allow_implicit_invocation: true
impact: "low"
metadata:
  category: "utility"
  complexity: "low"
status: active
last_reviewed: 2026-05-29
---

# util-docs-lint

Local-first Markdown quality toolchain for a project's `docs/`. This skill owns a deterministic local pipeline — `dprint` (formatting) → `vale` (prose) → `lychee` (links) — and the GitHub Actions workflow that mirrors it. Tools are **referenced, not installed**; the rules live in **project-root config files**.

Pinned/managed elsewhere (bump in your dotfiles, not here):

- `dprint`, `vale`, `lychee` — installed via **mise/dotfiles** (`~/.mise.toml`), never by this skill.

## Architecture (where things live)

- **Tool versions** → machine-global in dotfiles (`~/.mise.toml`). Not per-project, not rules.
- **Rules** → per-project at the **repo root**: `dprint.json`, `.vale.ini`, `lychee.toml`. Version-controlled with the docs they govern, so every contributor gets the same rules.
- **Canonical templates** → this skill's `templates/`. The skill copies them out; it never restates the rules inline.

## Safety rule (non-negotiable)

**`enforce` only auto-writes the mechanically safe subset — `dprint fmt` (formatting, including un-hard-wrapping prose via `textWrap: "never"`).** Prose (Vale) and link (lychee) findings are **reported, never auto-rewritten** — rewording prose or changing a URL is a human judgement call. No mode ever edits prose content.

## Companion setup (install the tools once)

The tools are referenced, not installed by this skill. Ensure they are on `PATH` via mise/dotfiles:

```bash
# in your dotfiles ~/.mise.toml [tools]:
#   dprint = "latest", vale = "latest", "ubi:lycheeverse/lychee" = "latest"
#   (lychee needs the ubi backend — its release nests the binary, breaking the default aqua shim)
mise install
dprint --version && vale --version && lychee --version
```

If a tool is absent, `audit`/`enforce` skip that stage with a warning (partial lint still runs).

## The five modes

Pick the mode from the user's intent. When ambiguous, ask.

### Mode 1 — scaffold

Stand up the rule configs in a project. Run once per project. Do not overwrite existing files without confirmation.

1. Copy the templates to the **project root**:

   | Template | Target path |
   |---|---|
   | `templates/dprint.json` | `dprint.json` |
   | `templates/.vale.ini` | `.vale.ini` |
   | `templates/lychee.toml` | `lychee.toml` |

2. Add to `.gitignore` (Vale styles are downloaded/generated, never committed):

   ```
   .vale/styles/Microsoft/
   .vale/styles/Local/
   ```

3. Pin the dprint plugin: tell the user to run `dprint config update` (pins the markdown plugin with a checksum). If dprint is absent, CI pins it on first run.
4. Finish by running **Mode 2 (audit)** so the scaffold is verified.

### Mode 2 — audit (read-only)

Run `scripts/docs-lint.sh` (defaults to `./docs`). It runs, aggregating findings (never stops on first failure):

1. `dprint check` — formatting (scope from `dprint.json` includes).
2. `vale docs/` — prose against Microsoft style (+ `Local` glossary aliases if present); refreshes the generated alias style first.
3. `lychee 'docs/**/*.md'` — links, using root `lychee.toml`.

Each tool auto-detected; missing → skipped with a warning. Exits non-zero if any present tool reports issues. Surface ranked findings (formatting → prose → links) with file/line and the fix; for formatting issues, offer **Mode 3**.

### Mode 3 — enforce (writes formatting only)

Run `scripts/docs-lint.sh --fix`. `dprint fmt` writes formatting fixes — normalises emphasis/lists/whitespace/tables **and un-hard-wraps prose** (`textWrap: "never"` collapses hard-wrapped paragraphs to single lines). Vale and lychee still run **read-only** in the same pass and report. Per the Safety rule, prose and links are never auto-modified.

### Mode 4 — scaffold-ci

Write the GitHub Actions workflow that mirrors the local pipeline. Copy `templates/docs-lint.yml` → `.github/workflows/docs-lint.yml` (create `.github/workflows/` if needed). Three jobs on any `docs/**` change: `format` (dprint), `prose` (Vale + Microsoft via reviewdog inline comments), `links` (lychee-action, fails on dead links). Remind the user to commit the root configs too — CI reads the same `dprint.json` / `.vale.ini` / `lychee.toml`.

### Mode 5 — add-glossary

Run after `docs/domain/02c-glossary.md` exists with `**Aliases (deprecated):**` entries.

1. Ensure `scripts/sync_glossary_rules.py` is present (copy from this skill's `scripts/` if not).
2. Add `, Local` to `BasedOnStyles` in `.vale.ini`: `BasedOnStyles = Microsoft, Local`.
3. The local pipeline and CI now generate `.vale/styles/Local/GlossaryAliases.yml` from the glossary's deprecated aliases (one substitution rule per alias → "Use '{Canonical}' instead of '{alias}'.") on every run.

## Reference materials

- `scripts/docs-lint.sh` — the local pipeline (auto-detect, `--fix`).
- `scripts/sync_glossary_rules.py` — generates the Vale `Local` alias style from the glossary.
- `templates/dprint.json` — formatting rules (`textWrap: "never"`, asterisk emphasis, `docs/**` scope).
- `templates/.vale.ini` — prose style (Microsoft, `MinAlertLevel = warning`).
- `templates/lychee.toml` — link rules (2xx + 429 accepted, loopback excluded, fragments off).
- `templates/docs-lint.yml` — the CI mirror.

## Tuning the rules (per project, in the root configs)

- **Stricter prose:** lower `MinAlertLevel` in `.vale.ini` from `warning` to `suggestion` to surface the full Microsoft set (Passive, Wordiness, ComplexWords, …), or raise to `error` to make prose block.
- **Different prose style:** swap `Packages`/`BasedOnStyles` to `Google` etc.
- **Link anchors:** add `include_fragments = "full"` to `lychee.toml` to verify in-page `#anchor` targets (string value — lychee errors on a boolean).
- **Scope:** widen `dprint.json` `includes` and the vale/lychee paths beyond `docs/**` if desired.

## Anti-patterns

- Putting rules in `~/.mise.toml` (it pins versions only) or restating rule values in this `SKILL.md` (templates are the source of truth).
- Committing `.vale/styles/Microsoft/` or `.vale/styles/Local/` (downloaded/generated).
- Auto-rewriting prose or links (forbidden — Safety rule).
- Using `textWrap: "always"` (re-hard-wraps prose — the opposite of the project rule).

## Checklist (before handoff)

- [ ] Root configs present: `dprint.json`, `.vale.ini`, `lychee.toml`; `.gitignore` covers `.vale/styles/`.
- [ ] `docs-lint.sh` runs clean (or findings surfaced); formatting auto-fixed via `--fix` if asked.
- [ ] dprint plugin pinned (`dprint config update`).
- [ ] If CI wanted: workflow scaffolded and root configs committed.
- [ ] If glossary exists: `add-glossary` wired and `Local` style generating.
