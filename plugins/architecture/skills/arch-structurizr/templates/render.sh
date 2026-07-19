#!/usr/bin/env bash
#
# Render C4 views from docs/architecture/c4/workspace.dsl to docs/architecture/c4/views/*.svg
#
# Single-stage pipeline using the consolidated Structurizr tool
# (https://github.com/structurizr/structurizr — supersedes the EOL
# structurizr-cli / structurizr-lite / on-premises installations):
#
#   1. validate the DSL
#   2. export each view as SVG directly (Playwright + headless Chromium)
#
# The `-playwright` image variant bundles the headless Chromium runtime.
# On first run, Chromium is downloaded inside the container (slow first
# run; cached thereafter).
#
# Pinned version is kit-maintained — bump via `arch-structurizr upgrade`.
# Do NOT use `:latest` — reproducibility matters.
#
# Usage:
#   ./render.sh              Render all views
#   ./render.sh <view-key>   Render a single view
#   ./render.sh --dry-run    Validate DSL + confirm Docker; do not render
#
# Exit codes:
#   0  All steps succeeded
#   1  DSL validation failed
#   2  Docker not available
#   3  Export / render failed
#   4  No views produced (DSL has no `views { ... }` block)

set -euo pipefail

# ─── Pinned image (bump via `arch-structurizr upgrade`) ───────────────
# The `-playwright` variant is mandatory — it bundles the headless
# Chromium runtime needed for direct SVG export. The base
# `structurizr/structurizr:${STRUCTURIZR_VERSION}` tag CANNOT export
# SVG (Playwright executable is missing). Do not strip the suffix.
STRUCTURIZR_VERSION="{{structurizr_version}}"
IMAGE="structurizr/structurizr:${STRUCTURIZR_VERSION}-playwright"

# ─── UID/GID — write SVGs as the invoking user, not root ──────────────
# Docker volume mounts default to running as root, which produces
# root-owned files that the host user then can't `git clean -fd`
# without sudo. Pass --user so the container writes with the right
# ownership.
DOCKER_USER="$(id -u):$(id -g)"

# ─── Paths ────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if REPO_ROOT="$(git -C "${SCRIPT_DIR}" rev-parse --show-toplevel 2>/dev/null)" && [[ -n "${REPO_ROOT}" ]]; then
    :
else
    REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
fi
C4_DIR_REL="$(realpath --relative-to="${REPO_ROOT}" "${SCRIPT_DIR}")"
DSL_PATH="/work/${C4_DIR_REL}/workspace.dsl"
VIEWS_DIR="/work/${C4_DIR_REL}/views"

DRY_RUN=0
VIEW_KEY=""
for arg in "$@"; do
    case "${arg}" in
        --dry-run) DRY_RUN=1 ;;
        --help|-h)
            sed -n '3,30p' "${BASH_SOURCE[0]}" | sed 's/^# \?//'
            exit 0
            ;;
        *) VIEW_KEY="${arg}" ;;
    esac
done

# ─── 0. Docker availability ───────────────────────────────────────────
if ! docker version >/dev/null 2>&1; then
    echo "ERROR: docker not available. Install Docker and ensure the daemon is running." >&2
    exit 2
fi

# ─── 1. Validate ──────────────────────────────────────────────────────
echo "→ Validating ${C4_DIR_REL}/workspace.dsl (${IMAGE})"
if ! docker run --rm --user "${DOCKER_USER}" -v "${REPO_ROOT}:/work" "${IMAGE}" \
        validate -workspace "${DSL_PATH}"; then
    echo "ERROR: workspace.dsl failed validation. Fix the DSL before re-rendering." >&2
    exit 1
fi

if [[ "${DRY_RUN}" == "1" ]]; then
    echo "✓ Dry-run passed. DSL valid; Docker available. No render performed."
    exit 0
fi

# ─── 2. Render directly to SVG ────────────────────────────────────────
mkdir -p "${SCRIPT_DIR}/views"

echo "→ Rendering views to SVG (first run downloads Chromium inside the container; subsequent runs are fast)"
if ! docker run --rm --user "${DOCKER_USER}" -v "${REPO_ROOT}:/work" "${IMAGE}" \
        export \
            -workspace "${DSL_PATH}" \
            -format svg \
            -output "${VIEWS_DIR}"; then
    echo "ERROR: export failed." >&2
    exit 3
fi

# ─── 3. Optional single-view filter ───────────────────────────────────
# (The export command renders every view in the DSL; if a single view
# was requested, delete the others. Cheaper than per-view docker runs
# because Chromium starts once.)
if [[ -n "${VIEW_KEY}" ]]; then
    KEEP="${SCRIPT_DIR}/views/${VIEW_KEY}.svg"
    if [[ ! -f "${KEEP}" ]]; then
        echo "ERROR: view key '${VIEW_KEY}' not found in render output. Available:" >&2
        find "${SCRIPT_DIR}/views" -maxdepth 1 -name '*.svg' -printf '  %f\n' | sed 's/\.svg$//' >&2
        exit 4
    fi
    find "${SCRIPT_DIR}/views" -maxdepth 1 -type f -name '*.svg' ! -name "${VIEW_KEY}.svg" -delete
fi

# ─── 4. Detect zero-view DSL ──────────────────────────────────────────
if ! compgen -G "${SCRIPT_DIR}/views/*.svg" > /dev/null; then
    echo "ERROR: no views rendered. workspace.dsl has no \`views { ... }\` block or all views are empty." >&2
    exit 4
fi

# ─── 5. Report ────────────────────────────────────────────────────────
echo
echo "✓ Rendered views:"
find "${SCRIPT_DIR}/views" -maxdepth 1 -name '*.svg' -printf '  %f\n' | sort

echo
echo "Embed in arc42 markdown via:  ![view-key](c4/views/<view-key>.svg)"
