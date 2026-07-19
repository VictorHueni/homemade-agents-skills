#!/usr/bin/env bash
# docs-lint.sh — deterministic docs/ quality pipeline.
#
#   dprint (format) -> vale (prose) -> lychee (links)
#
# Default is READ-ONLY (audit). With --fix, dprint writes formatting fixes
# (including un-hard-wrapping prose, since dprint.json sets textWrap=never).
# Prose (Vale) and link (lychee) findings are ALWAYS report-only — never
# auto-rewritten: rewording prose or "fixing" a URL is a human judgement call.
#
# Each tool is auto-detected: if missing it is skipped with a warning, so a
# partial lint still runs. The script aggregates across all stages and exits
# non-zero if any present tool reports issues.
#
# Rules live in the project-root configs (dprint.json, .vale.ini, lychee.toml);
# this script only orchestrates the tools. Run from the project root.
#
# Usage:  docs-lint.sh [--fix] [dir]      (dir defaults to ./docs)
set -uo pipefail   # intentionally NOT -e: run every stage, then aggregate.

FIX=0
DIR=""
for arg in "$@"; do
  case "$arg" in
    --fix) FIX=1 ;;
    -*) echo "unknown flag: $arg" >&2; exit 2 ;;
    *) DIR="$arg" ;;
  esac
done
DIR="${DIR:-docs}"

red()    { printf '\033[31m%s\033[0m\n' "$*"; }
green()  { printf '\033[32m%s\033[0m\n' "$*"; }
yellow() { printf '\033[33m%s\033[0m\n' "$*"; }
bold()   { printf '\033[1m%s\033[0m\n' "$*"; }

[ -d "$DIR" ] || { red "✗ directory not found: $DIR"; exit 2; }

rc=0       # aggregate exit code
ran=0      # did at least one linter run?

bold "==> docs-lint on '$DIR'$( [ "$FIX" -eq 1 ] && echo ' (--fix: dprint writes formatting)' )"

# [1/3] dprint — formatting. Scope comes from dprint.json "includes", not $DIR.
bold "[1/3] dprint (markdown formatting)"
if command -v dprint >/dev/null 2>&1; then
  ran=1
  if [ "$FIX" -eq 1 ]; then
    if dprint fmt; then green "    formatting applied (incl. un-hard-wrapping prose)"; else red "    dprint fmt failed"; rc=1; fi
  else
    if dprint check; then green "    formatting OK"; else red "    formatting issues above — fix with: docs-lint.sh --fix"; rc=1; fi
  fi
else
  yellow "    ⚠ dprint not on PATH — skipped (mise install / see SKILL.md)"
fi

# [2/3] vale — prose. Refresh the generated glossary-alias style first if present.
bold "[2/3] vale (prose style)"
if command -v vale >/dev/null 2>&1; then
  ran=1
  if [ -f scripts/sync_glossary_rules.py ] && [ -f docs/domain/02c-glossary.md ] && command -v python3 >/dev/null 2>&1; then
    python3 scripts/sync_glossary_rules.py || yellow "    (glossary sync skipped — non-fatal)"
  fi
  vale sync >/dev/null 2>&1 || true   # ensure Microsoft package is present
  if vale "$DIR"; then green "    prose OK"; else red "    prose findings above (report-only)"; rc=1; fi
else
  yellow "    ⚠ vale not on PATH — skipped (mise install / see SKILL.md)"
fi

# [3/3] lychee — links. lychee.toml is auto-discovered from the repo root.
bold "[3/3] lychee (link check)"
if command -v lychee >/dev/null 2>&1; then
  ran=1
  if lychee --no-progress "$DIR/**/*.md"; then green "    links OK"; else red "    dead links above (report-only)"; rc=1; fi
else
  yellow "    ⚠ lychee not on PATH — skipped (mise install / see SKILL.md)"
fi

echo
if [ "$ran" -eq 0 ]; then
  yellow "==> no linters were available — install dprint / vale / lychee (mise install)."
  exit 0
fi
if [ "$rc" -eq 0 ]; then
  green "==> docs-lint passed."
else
  red "==> docs-lint found issues (see above). Formatting is auto-fixable with --fix; prose/links are for you to resolve."
fi
exit "$rc"
