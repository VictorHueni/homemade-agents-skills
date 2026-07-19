#!/usr/bin/env bash
# ─────────────────────────────────────────────
# Homemade Agent Skills — Install / Sync
# ─────────────────────────────────────────────
# Usage:
#   ./install.sh [--verbose|--quiet]
#   ./install.sh [--verbose|--quiet] /path/to/project
#
# Run again after git pull to pick up new skills or commands automatically.
# ─────────────────────────────────────────────

set -euo pipefail
shopt -s nullglob

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERBOSE=0
QUIET=0
TARGET_ROOT=""

usage() {
    cat <<'EOF'
Usage:
  ./install.sh [--verbose|--quiet]
  ./install.sh [--verbose|--quiet] /path/to/project

Options:
  -v, --verbose  Print per-item actions.
  -q, --quiet    Suppress normal output; only errors are shown.
  -h, --help     Show this help.
EOF
}

log() {
    if (( !QUIET )); then
        echo "$@"
    fi
}

log_verbose() {
    if (( VERBOSE && !QUIET )); then
        echo "$@"
    fi
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -v|--verbose)
            VERBOSE=1
            ;;
        -q|--quiet)
            QUIET=1
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --)
            shift
            [[ $# -le 1 ]] || { echo "error: expected at most one project path" >&2; exit 1; }
            [[ $# -eq 0 ]] || TARGET_ROOT="$1"
            break
            ;;
        -*)
            echo "error: unknown option: $1" >&2
            usage >&2
            exit 1
            ;;
        *)
            [[ -z "$TARGET_ROOT" ]] || { echo "error: expected at most one project path" >&2; exit 1; }
            TARGET_ROOT="$1"
            ;;
    esac
    shift
done

if [[ -n "$TARGET_ROOT" ]]; then
    CLAUDE_BASE="$TARGET_ROOT/.claude"
    CODEX_BASE="$TARGET_ROOT/.codex"
    AGENTS_BASE="$TARGET_ROOT/.agents"
    log_verbose "Installing into project: $TARGET_ROOT"
else
    CLAUDE_BASE="$HOME/.claude"
    CODEX_BASE="$HOME/.codex"
    AGENTS_BASE="$HOME/.agents"
    log_verbose "Installing globally:"
    log_verbose "  skills   -> $CLAUDE_BASE, $CODEX_BASE, $AGENTS_BASE"
    log_verbose "  commands -> $CLAUDE_BASE"
    log_verbose "  rules    -> $CLAUDE_BASE"
fi

CLAUDE_SKILLS_TARGET="$CLAUDE_BASE/skills"
CODEX_SKILLS_TARGET="$CODEX_BASE/skills"
AGENTS_SKILLS_TARGET="$AGENTS_BASE/skills"
COMMANDS_TARGET="$CLAUDE_BASE/commands"
RULES_TARGET="$CLAUDE_BASE/rules"

mkdir -p "$COMMANDS_TARGET" "$RULES_TARGET"
for skills_target in "$CLAUDE_SKILLS_TARGET" "$CODEX_SKILLS_TARGET" "$AGENTS_SKILLS_TARGET"; do
    mkdir -p "$skills_target"
done

# Sync *.md files from a source subdir: install symlinks + prune orphans.
# Usage: sync_files <src_subdir> <target_dir> <label> <changed_var> <pruned_var> <unchanged_var>
sync_files() {
    local src="$1" target="$2" label="$3"
    local -n _chg="$4" _prun="$5" _same="$6"

    [[ -d "$src" ]] || return 0

    for src_file in "$src"/*.md; do
        local name link desired resolved
        name="$(basename "$src_file")"
        link="$target/$name"
        desired="$(realpath --relative-to="$(dirname "$link")" "$src_file")"
        resolved="$(realpath "$link" 2>/dev/null || true)"

        if [[ -L "$link" ]] && [[ -n "$resolved" ]] && [[ "$resolved" == "$(realpath "$src_file")" ]]; then
            _same=$(( _same + 1 ))
            continue
        fi

        if [[ -L "$link" ]] || [[ -f "$link" ]]; then
            rm -f "$link"
        elif [[ -d "$link" ]]; then
            rm -rf "$link"
        fi

        ln -s "$desired" "$link"
        log_verbose "  ↻ $label: $name"
        _chg=$(( _chg + 1 ))
    done

    for link in "$target"/*.md; do
        local name resolved
        name="$(basename "$link")"
        resolved="$(realpath "$link" 2>/dev/null || true)"
        if [[ -L "$link" ]] && [[ "$resolved" == "$src/"* ]] && [[ ! -f "$src/$name" ]]; then
            rm "$link"
            log_verbose "  ✗ pruned $label: $name"
            _prun=$(( _prun + 1 ))
        fi
    done
}

# ── Skills: each top-level dir containing SKILL.md → symlinked directory
# Usage: sync_skills <target_dir> <changed_var> <pruned_var> <unchanged_var>
sync_skills() {
    local target="$1"
    local -n _chg="$2" _prun="$3" _same="$4"

    for skill_dir in "$SCRIPT_DIR"/plugins/*/skills/*/; do
        local skill_name link desired resolved
        skill_name="$(basename "${skill_dir%/}")"
        [[ -f "$skill_dir/SKILL.md" ]] || continue

        link="$target/$skill_name"
        desired="$(realpath --relative-to="$(dirname "$link")" "$skill_dir")"
        resolved="$(realpath "$link" 2>/dev/null || true)"

        if [[ -L "$link" ]] && [[ -n "$resolved" ]] && [[ "$resolved" == "$(realpath "$skill_dir")" ]]; then
            _same=$(( _same + 1 ))
            continue
        fi

        if [[ -L "$link" ]]; then
            rm "$link"
        elif [[ -d "$link" ]]; then
            rm -rf "$link"
        elif [[ -e "$link" ]]; then
            rm -f "$link"
        fi

        ln -s "$desired" "$link"
        log_verbose "  ↻ skill: $skill_name"
        _chg=$(( _chg + 1 ))
    done

    for link in "$target"/*; do
        local skill_name resolved
        skill_name="$(basename "$link")"
        if [[ -L "$link" ]]; then
            resolved="$(realpath "$link" 2>/dev/null || true)"
        else
            resolved=""
        fi
        if [[ -L "$link" ]] && [[ "$resolved" == "$SCRIPT_DIR/"* ]] && ! compgen -G "$SCRIPT_DIR/plugins/*/skills/$skill_name" > /dev/null; then
            rm "$link"
            log_verbose "  ✗ pruned skill: $skill_name"
            _prun=$(( _prun + 1 ))
        fi
    done
}

prune_legacy_repo_container() {
    local root="$1" repo_name="$2" container="$1/$2"
    local -n _prun="$3"

    [[ -e "$container" ]] || return 0

    if [[ -L "$container" ]]; then
        rm "$container"
        log_verbose "  ✗ pruned legacy repo skill container: $repo_name"
        _prun=$(( _prun + 1 ))
        return 0
    fi

    [[ -d "$container" ]] || return 0

    local child resolved
    for child in "$container"/*; do
        [[ -e "$child" ]] || continue
        [[ -L "$child" ]] || return 0
        resolved="$(realpath "$child" 2>/dev/null || true)"
        [[ -n "$resolved" && "$resolved" == "$SCRIPT_DIR/"* ]] || return 0
    done

    rm -rf "$container"
    log_verbose "  ✗ pruned legacy repo skill container: $repo_name"
    _prun=$(( _prun + 1 ))
}

changed_skills=0
pruned_skills=0
unchanged_skills=0

sync_skills "$CLAUDE_SKILLS_TARGET" changed_skills pruned_skills unchanged_skills
prune_legacy_repo_container "$CODEX_BASE/skills" "$(basename "$SCRIPT_DIR")" pruned_skills
sync_skills "$CODEX_SKILLS_TARGET" changed_skills pruned_skills unchanged_skills
prune_legacy_repo_container "$AGENTS_BASE/skills" "$(basename "$SCRIPT_DIR")" pruned_skills
sync_skills "$AGENTS_SKILLS_TARGET" changed_skills pruned_skills unchanged_skills

# ── Commands and Rules: *.md files symlinked from their source subdir
changed_commands=0; pruned_commands=0; unchanged_commands=0
changed_rules=0;    pruned_rules=0;    unchanged_rules=0

for cmd_dir in "$SCRIPT_DIR"/plugins/*/commands; do
    [[ -d "$cmd_dir" ]] || continue
    sync_files "$cmd_dir" "$COMMANDS_TARGET" "command" changed_commands pruned_commands unchanged_commands
done
sync_files "$SCRIPT_DIR/rules"    "$RULES_TARGET"    "rule"    changed_rules    pruned_rules    unchanged_rules

if (( !QUIET )); then
    total_changes=$(( changed_skills + pruned_skills + changed_commands + pruned_commands + changed_rules + pruned_rules ))
    if (( total_changes == 0 )); then
        echo "No changes."
    else
        echo "Sync complete. skills: $changed_skills changed, $pruned_skills pruned; commands: $changed_commands changed, $pruned_commands pruned; rules: $changed_rules changed, $pruned_rules pruned."
    fi
fi
