#!/usr/bin/env bash
# exo-verify.sh — READ-ONLY live-infra inventory for post-apply verification.
#
# Lists the Exoscale resources actually deployed in the account via the `exo`
# CLI, so a human (or Claude in the skill's Verify mode) can compare them
# against the Terraform plan / config. This runs AFTER a human has applied —
# it confirms reality matches intent; it does not change anything.
#
# SAFETY (non-negotiable, mirrors the skill's plan-only contract):
#   This script calls ONLY read-only `exo ... list` subcommands. It MUST NEVER
#   call create/delete/update/scale/start/stop/reboot/reset or any other
#   mutating verb. The `exo` CLI can mutate live infrastructure; this skill's
#   use of it is restricted to inventory reads.
#
# `exo` is AUTO-DETECTED: if it is not on PATH the script warns and exits 0
# (verification is informational, never a hard gate — like the trivy stage).
# The API answers only when `exo config` has been run (or EXOSCALE_API_KEY /
# EXOSCALE_API_SECRET are exported). Per-resource calls are best-effort: an
# unsupported subcommand on a given exo version is skipped, not fatal.
#
# Usage:  exo-verify.sh [--json]
#           --json   request machine-readable output (exo --output-format json)
set -euo pipefail

OUTFLAG=()
for arg in "$@"; do
  case "$arg" in
    --json) OUTFLAG=(--output-format json) ;;
    -*) echo "unknown flag: $arg" >&2; exit 2 ;;
    *) echo "unexpected argument: $arg" >&2; exit 2 ;;
  esac
done

red()    { printf '\033[31m%s\033[0m\n' "$*"; }
green()  { printf '\033[32m%s\033[0m\n' "$*"; }
yellow() { printf '\033[33m%s\033[0m\n' "$*"; }
bold()   { printf '\033[1m%s\033[0m\n' "$*"; }

if ! command -v exo >/dev/null 2>&1; then
  yellow "⚠ exo CLI not on PATH — deployment verification SKIPPED."
  echo "  install it (mise install / see references/toolchain.md) and run 'exo config'." >&2
  exit 0
fi

bold "==> Exoscale live-infra inventory (READ-ONLY — no apply, no mutation)"
echo "    Compare this against the Terraform plan/config to confirm the deploy."
echo

# label|command — read-only list verbs only. Add new resource types here.
resources=(
  "Compute instances|exo compute instance list"
  "Security groups|exo compute security-group list"
  "Private networks|exo compute private-network list"
  "Anti-affinity groups|exo compute anti-affinity-group list"
  "Network load balancers|exo compute load-balancer list"
  "SKS clusters|exo compute sks list"
  "DBaaS services|exo dbaas list"
  "SOS buckets|exo storage list"
  "DNS domains|exo dns list"
)

for entry in "${resources[@]}"; do
  label="${entry%%|*}"
  cmd="${entry#*|}"
  bold "── $label ──"
  # shellcheck disable=SC2086
  if ! $cmd "${OUTFLAG[@]}" 2>/dev/null; then
    yellow "   (unavailable on this exo version, or none deployed / not configured)"
  fi
  echo
done

green "==> Inventory complete. This was READ-ONLY. Cross-check it against the plan."
