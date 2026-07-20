#!/usr/bin/env bash
# tf-check.sh — deterministic, PLAN-ONLY Terraform quality pipeline for Exoscale.
#
#   fmt -check -> validate -> tflint -> exoscale-policy -> trivy (if present) -> plan
#
# This script NEVER runs `apply`, `destroy`, `import`, or any state mutation.
# A human applies after reviewing the plan.
#
# exoscale-policy.sh is a native, dependency-free check for Exoscale-specific
# security issues (Trivy's built-in checks do not cover Exoscale, and its custom
# Rego mechanism does not reliably fire for Terraform). It always runs.
#
# trivy is AUTO-DETECTED: if on PATH, `trivy fs` runs the built-in IaC misconfig
# checks + secret detection and HIGH/CRITICAL findings fail the pipeline; if
# absent the scan is skipped with a warning (it does not block).
#
# Usage:  tf-check.sh [dir]        (dir defaults to ./infra)
#         tf-check.sh --no-plan [dir]   skip the plan stage (no creds needed)
set -euo pipefail

NO_PLAN=0
DIR=""
for arg in "$@"; do
  case "$arg" in
    --no-plan) NO_PLAN=1 ;;
    -*) echo "unknown flag: $arg" >&2; exit 2 ;;
    *) DIR="$arg" ;;
  esac
done
DIR="${DIR:-infra}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

red()    { printf '\033[31m%s\033[0m\n' "$*"; }
green()  { printf '\033[32m%s\033[0m\n' "$*"; }
yellow() { printf '\033[33m%s\033[0m\n' "$*"; }
bold()   { printf '\033[1m%s\033[0m\n' "$*"; }

require() {
  if ! command -v "$1" >/dev/null 2>&1; then
    red "✗ required tool not found on PATH: $1"
    echo "  install it (see references/toolchain.md) and re-run." >&2
    exit 127
  fi
}

[ -d "$DIR" ] || { red "✗ directory not found: $DIR"; exit 2; }

# IaC binary: Terraform (BSL) or OpenTofu (MPL-2.0, the `tofu` binary). Honour an
# explicit TF_BIN; else auto-detect — prefer terraform when present for back-compat,
# otherwise fall back to tofu. Set TF_BIN=tofu in OSS-strict projects that standardise
# on OpenTofu (see references/toolchain.md). The CLIs are flag-compatible for this pipeline.
if [ -n "${TF_BIN:-}" ]; then
  require "$TF_BIN"
elif command -v terraform >/dev/null 2>&1; then
  TF_BIN=terraform
elif command -v tofu >/dev/null 2>&1; then
  TF_BIN=tofu
else
  red "✗ neither 'terraform' nor 'tofu' found on PATH"
  echo "  install one (see references/toolchain.md), or set TF_BIN explicitly." >&2
  exit 127
fi

bold "==> IaC quality pipeline ($TF_BIN) on '$DIR' (plan-only)"

bold "[1/6] $TF_BIN fmt -check"
if "$TF_BIN" -chdir="$DIR" fmt -check -recursive -diff; then
  green "    formatting OK"
else
  red "    formatting issues above — run: $TF_BIN -chdir=$DIR fmt -recursive"
  exit 1
fi

bold "[2/6] $TF_BIN validate"
"$TF_BIN" -chdir="$DIR" init -backend=false -input=false >/dev/null
"$TF_BIN" -chdir="$DIR" validate
green "    config valid"

bold "[3/6] tflint"
if command -v tflint >/dev/null 2>&1; then
  ( cd "$DIR" && tflint --init >/dev/null && tflint --recursive )
  green "    lint clean"
else
  red "✗ tflint not found on PATH — install it (references/toolchain.md)"
  exit 127
fi

bold "[4/6] exoscale-policy (native Exoscale security checks)"
# Deterministic, dependency-free. NOT done via Trivy custom Rego: that mechanism
# does not reliably fire for Terraform (see references/toolchain.md).
bash "$SCRIPT_DIR/exoscale-policy.sh" "$DIR"

bold "[5/6] trivy (built-in misconfig + secret scan)"
if command -v trivy >/dev/null 2>&1; then
  # `fs` with both scanners = built-in IaC misconfig (generic) + secret detection
  # in one pass. Exoscale-specific gating is the native stage above.
  ( cd "$DIR" && trivy fs --scanners misconfig,secret --severity HIGH,CRITICAL \
      --exit-code 1 --skip-dirs '.terraform' . )
  green "    scan clean (no HIGH/CRITICAL findings)"
else
  yellow "    ⚠ trivy not on PATH — built-in/secret scan SKIPPED (install it to enable; references/toolchain.md)"
fi

if [ "$NO_PLAN" -eq 1 ]; then
  green "==> fmt/validate/tflint/policy/scan passed (plan skipped via --no-plan)"
  exit 0
fi

bold "[6/6] $TF_BIN plan (read-only — NO apply)"
if [ -z "${EXOSCALE_API_KEY:-}" ] || [ -z "${EXOSCALE_API_SECRET:-}" ]; then
  red "✗ EXOSCALE_API_KEY / EXOSCALE_API_SECRET not set — cannot plan."
  echo "  export them, or re-run with --no-plan to stop after lint." >&2
  exit 3
fi
# A real init is needed if a backend is configured; harmless otherwise.
"$TF_BIN" -chdir="$DIR" init -input=false >/dev/null
"$TF_BIN" -chdir="$DIR" plan -input=false -lock=false
green "==> Pipeline complete. Review the plan above, then a HUMAN runs '$TF_BIN apply'."
