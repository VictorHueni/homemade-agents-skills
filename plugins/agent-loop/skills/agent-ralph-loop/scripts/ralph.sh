#!/usr/bin/env bash
# ralph.sh — Autonomous Ralph Loop orchestration script
# Spawns a fresh agent per increment until all increments are done.
#
# Usage: ralph.sh <workspace-dir> [--agent claude] [--max-iterations 50] [--with-prd|--without-prd] [--with-push]

set -euo pipefail

# ─── Defaults ──────────────────────────────────────────────────────────────────
AGENT="claude"
MODEL="sonnet"
MAX_ITERATIONS=50
WORKSPACE_DIR=""
PRD_MODE="auto"
EFFECTIVE_PRD_MODE=""
PUSH_AFTER_COMMIT="false"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ITERATION_PROMPT="$SKILL_DIR/references/iteration-prompt.md"

# ─── Usage ─────────────────────────────────────────────────────────────────────
usage() {
  cat <<USAGE
Usage: $(basename "$0") <workspace-dir> [options]

Runs the Ralph Loop: spawns a fresh agent per increment until all
increments in the execution plan are done.

Arguments:
  workspace-dir         Path to the workspace (e.g., docs/plans/active/0001_my-feature)

Options:
  --agent <name>        Agent CLI (provider) to use (default: claude)
  --model <name>        Model alias or full ID to use (default: sonnet)
  --max-iterations <n>  Maximum iterations before stopping (default: 50)
  --with-prd            Require a PRD in the workspace for each iteration
  --without-prd         Ignore any PRD file and run plan-only
  --with-push           Push to remote after each successful commit (default: off)
  -h, --help            Show this help message

Examples:
  $(basename "$0") docs/plans/active/0001_my-feature
  $(basename "$0") docs/plans/active/0001_my-feature --agent claude --model opus --max-iterations 20
  $(basename "$0") docs/plans/active/0001_my-feature --model claude-sonnet-5
  $(basename "$0") docs/plans/active/0001_my-feature --with-prd
  $(basename "$0") docs/plans/active/0001_my-feature --without-prd
  $(basename "$0") docs/plans/active/0001_my-feature --with-push
USAGE
}

# ─── Argument Parsing ──────────────────────────────────────────────────────────
if [[ $# -eq 0 ]]; then
  usage
  exit 1
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --agent)
      AGENT="$2"
      shift 2
      ;;
    --model)
      MODEL="$2"
      shift 2
      ;;
    --max-iterations)
      MAX_ITERATIONS="$2"
      shift 2
      ;;
    --with-prd)
      if [[ "$PRD_MODE" == "without" ]]; then
        echo "Error: --with-prd and --without-prd are mutually exclusive" >&2
        exit 1
      fi
      PRD_MODE="with"
      shift
      ;;
    --without-prd)
      if [[ "$PRD_MODE" == "with" ]]; then
        echo "Error: --with-prd and --without-prd are mutually exclusive" >&2
        exit 1
      fi
      PRD_MODE="without"
      shift
      ;;
    --with-push)
      PUSH_AFTER_COMMIT="true"
      shift
      ;;
    -*)
      echo "Error: Unknown option '$1'" >&2
      usage
      exit 1
      ;;
    *)
      if [[ -z "$WORKSPACE_DIR" ]]; then
        WORKSPACE_DIR="$1"
      else
        echo "Error: Unexpected argument '$1'" >&2
        usage
        exit 1
      fi
      shift
      ;;
  esac
done

# ─── Validation ────────────────────────────────────────────────────────────────
if [[ -z "$WORKSPACE_DIR" ]]; then
  echo "Error: workspace-dir is required" >&2
  usage
  exit 1
fi

if [[ ! -d "$WORKSPACE_DIR" ]]; then
  echo "Error: Workspace directory not found: $WORKSPACE_DIR" >&2
  exit 1
fi

if [[ ! -f "$ITERATION_PROMPT" ]]; then
  echo "Error: Iteration prompt not found: $ITERATION_PROMPT" >&2
  exit 1
fi

# Find the exec plan in the workspace
EXEC_PLAN=$(find "$WORKSPACE_DIR" -maxdepth 1 -name '*_exec_*.md' -type f | head -1)
if [[ -z "$EXEC_PLAN" ]]; then
  echo "Error: No execution plan (*_exec_*.md) found in $WORKSPACE_DIR" >&2
  exit 1
fi

# Resolve PRD path from exec plan frontmatter (prd: field)
GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo ".")
PRD_FIELD=$(awk '/^---/{c++; next} c==1 && /^prd:/{sub(/^prd:[[:space:]]*/,""); gsub(/"/,""); print; exit}' "$EXEC_PLAN")
PRD_FILE=""
if [[ -n "$PRD_FIELD" ]]; then
  PRD_FILE="$GIT_ROOT/$PRD_FIELD"
  if [[ ! -f "$PRD_FILE" ]]; then
    echo "Warning: exec plan prd: field points to non-existent file: $PRD_FILE" >&2
    PRD_FILE=""
  fi
fi

case "$PRD_MODE" in
  with)
    if [[ -z "$PRD_FILE" ]]; then
      echo "Error: --with-prd requires a prd: field in the exec plan frontmatter pointing to an existing file" >&2
      exit 1
    fi
    EFFECTIVE_PRD_MODE="with-prd"
    ;;
  without)
    PRD_FILE=""
    EFFECTIVE_PRD_MODE="without-prd"
    ;;
  auto)
    if [[ -n "$PRD_FILE" ]]; then
      EFFECTIVE_PRD_MODE="with-prd"
    else
      EFFECTIVE_PRD_MODE="without-prd"
    fi
    ;;
  *)
    echo "Error: Unsupported PRD mode '$PRD_MODE'" >&2
    exit 1
    ;;
esac

# ─── Completion Check ──────────────────────────────────────────────────────────
has_pending_increments() {
  grep -q '\*\*Status:\*\* pending' "$EXEC_PLAN" 2>/dev/null
}

has_in_progress_increments() {
  grep -q '\*\*Status:\*\* in-progress' "$EXEC_PLAN" 2>/dev/null
}

is_complete() {
  if has_pending_increments || has_in_progress_increments; then
    return 1
  fi
  return 0
}

# ─── Agent Command ─────────────────────────────────────────────────────────────
build_prompt() {
  sed \
    -e "s|{{WORKSPACE_DIR}}|$WORKSPACE_DIR|g" \
    -e "s|{{PRD_MODE}}|$EFFECTIVE_PRD_MODE|g" \
    -e "s|{{PRD_PATH}}|${PRD_FILE:-none}|g" \
    "$ITERATION_PROMPT"
}

run_agent() {
  local prompt
  prompt=$(build_prompt)

  case "$AGENT" in
    claude)
      echo "$prompt" | claude --dangerously-skip-permissions --model "$MODEL" --print 2>&1
      ;;
    *)
      echo "Error: Unsupported agent '$AGENT'. Currently supported: claude" >&2
      return 1
      ;;
  esac
}

# ─── Main Loop ─────────────────────────────────────────────────────────────────
echo "═══════════════════════════════════════════════════════════"
echo "  Ralph Loop Runner"
echo "  Workspace:  $WORKSPACE_DIR"
echo "  Exec Plan:  $EXEC_PLAN"
echo "  PRD Mode:   $EFFECTIVE_PRD_MODE"
echo "  Agent:      $AGENT"
echo "  Model:      $MODEL"
echo "  Max Iter:   $MAX_ITERATIONS"
echo "  Push:       $PUSH_AFTER_COMMIT"
echo "═══════════════════════════════════════════════════════════"
echo ""

if is_complete; then
  echo "All increments are already done. Nothing to do."
  exit 0
fi

iteration=0
while [[ $iteration -lt $MAX_ITERATIONS ]]; do
  iteration=$((iteration + 1))

  echo "───────────────────────────────────────────────────────────"
  echo "  Iteration $iteration / $MAX_ITERATIONS"
  echo "  $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  echo "───────────────────────────────────────────────────────────"

  # Check for completion before spawning
  if is_complete; then
    echo ""
    echo "All increments are done. Ralph Loop complete."
    exit 0
  fi

  # Spawn agent
  if ! run_agent; then
    echo ""
    echo "Warning: Agent exited with error. Checking plan state..." >&2
  fi

  # Push if requested
  if [[ "$PUSH_AFTER_COMMIT" == "true" ]]; then
    echo "  Pushing to remote..."
    if ! git push 2>&1; then
      echo "Warning: git push failed" >&2
    fi
  fi

  echo ""
done

# Max iterations reached
echo "═══════════════════════════════════════════════════════════"
echo "  Warning: Max iterations ($MAX_ITERATIONS) reached."
echo "  The loop stopped but increments may remain."
echo "  Check the exec plan: $EXEC_PLAN"
echo "═══════════════════════════════════════════════════════════"
exit 1
