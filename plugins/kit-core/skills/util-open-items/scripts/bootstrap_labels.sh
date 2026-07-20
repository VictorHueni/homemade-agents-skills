#!/usr/bin/env bash
# bootstrap_labels.sh — idempotent bootstrap of the open-items label vocabulary.
#
# Creates (or normalizes) the 17 canonical labels of the open-items github
# backend on a target repo via `gh label create --force`. Idempotent: re-runs
# are no-ops except that colors/descriptions are normalized back to canon.
#
# Source of truth for the vocabulary (names, colors, descriptions):
#   docs/architecture/decisions/adr-0009-standard-issue-vocabulary-github-backend.md §5
# Backend mechanics (axes, exclusivity, query patterns):
#   plugins/kit-core/skills/util-open-items/references/github-backend.md §2b
#
# IMPORTANT: run this BEFORE installing the issue forms — GitHub issue forms
# silently skip labels that do not exist on the repo.
#
# Usage:
#   bootstrap_labels.sh --repo OWNER/NAME [--apply]
#
# Dry-run by default (prints the planned gh commands, mutates nothing, needs
# neither gh nor network). Pass --apply to execute; --apply requires an
# authenticated `gh` CLI.
set -euo pipefail

# ADR-0009 §5 canonical label vocabulary — the ONE place to edit labels.
# Format: name|color|description  (color without leading '#', gh convention)
LABELS='type:bug|D73A4A|Something is broken
type:feature|A2EEEF|New user-facing capability
type:task|1D76DB|Concrete work item — not a feature, not broken
type:docs|C5DEF5|Documentation missing, wrong, or unclear
type:tech-debt|023B95|Deliberate structural shortcut to pay back
priority:p0|B60205|Critical — drop everything
priority:p1|D93F0B|High — this cycle
priority:p2|FBCA04|Medium — scheduled
priority:p3|FEF2C0|Low — opportunistic
size:S|EDEDED|Small — hours, single-file scale
size:M|BFBFBF|Medium — a focused day, few files
size:L|878787|Large — consider splitting before delegation
needs-triage|D4C5F9|Untriaged — not yet routed (creation default)
ready-for-agent|0E8A16|Brief complete — an agent may take this
needs-human|F9D0C4|Valid, but requires a human decision/work
state:in-progress|006B75|Actively being worked (replaces readiness label)
state:blocked|000000|Blocked on an external dependency'

usage() {
  cat >&2 <<'EOF'
Usage: bootstrap_labels.sh --repo OWNER/NAME [--apply]

Bootstraps the 17-label open-items vocabulary (ADR-0009 §5) on a repo.

  --repo OWNER/NAME  Target repository (required).
  --apply            Actually run gh label create --force (requires gh).
                     Without it: dry-run — print planned commands, mutate nothing.
EOF
  exit 2
}

repo=""
apply=0
while [ "$#" -gt 0 ]; do
  case "$1" in
    --repo)
      [ "$#" -ge 2 ] || usage
      repo="$2"
      shift 2
      ;;
    --apply)
      apply=1
      shift
      ;;
    -h|--help)
      usage
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      usage
      ;;
  esac
done

[ -n "$repo" ] || usage

if [ "$apply" -eq 1 ] && ! command -v gh >/dev/null 2>&1; then
  printf 'ERROR: --apply requires the gh CLI, which was not found on PATH.\n' >&2
  printf 'Install it (https://cli.github.com/) and authenticate (gh auth login),\n' >&2
  printf 'or drop --apply to preview the planned commands.\n' >&2
  exit 1
fi

count=0
while IFS='|' read -r name color desc; do
  [ -n "$name" ] || continue
  count=$((count + 1))
  if [ "$apply" -eq 1 ]; then
    printf 'apply: %s\n' "$name"
    if ! gh label create "$name" --repo "$repo" --color "$color" \
        --description "$desc" --force; then
      printf 'ERROR: gh label create failed for %s on %s (see gh output above).\n' \
        "$name" "$repo" >&2
      exit 1
    fi
  else
    printf 'plan: gh label create %q --repo %q --color %q --description %q --force\n' \
      "$name" "$repo" "$color" "$desc"
  fi
done <<EOF
$LABELS
EOF

if [ "$apply" -eq 1 ]; then
  printf '%d labels created/normalized on %s.\n' "$count" "$repo"
else
  printf '%d labels planned for %s.\n' "$count" "$repo"
  printf 'dry-run: nothing mutated (pass --apply to execute).\n'
fi
