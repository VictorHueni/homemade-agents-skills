#!/usr/bin/env bash
# ─────────────────────────────────────────────
# util-toolkit-doctor :: gather-state.sh
# ─────────────────────────────────────────────
# Read-only diagnostic. Inspects:
#   - prerequisites (chezmoi, git, gh, ssh to github.com)
#   - dotfiles repo state (~/.local/share/chezmoi)
#   - chezmoi deployed-vs-source drift
#   - kit repo state (~/projects/homemade-claude-kit)
#   - ~/.claude/skills/ and ~/.claude/commands/ symlink health
#
# Exits 0 always. The output is structured for the model to parse.
# ─────────────────────────────────────────────

set -uo pipefail

DOTFILES_REMOTE="git@github.com:VictorHueni/dotfiles.git"
KIT_REMOTE="git@github.com:VictorHueni/homemade-claude-kit.git"

DOTFILES_DIR="$HOME/.local/share/chezmoi"
KIT_DIR="$HOME/projects/homemade-claude-kit"
CLAUDE_DIR="$HOME/.claude"

# ── helpers
section() { printf '\n## %s\n' "$1"; }
ok()      { printf '  \xe2\x9c\x93 %s\n' "$1"; }       # ✓
warn()    { printf '  \xe2\x9a\xa0 %s\n' "$1"; }       # ⚠
fail()    { printf '  \xe2\x9c\x97 %s\n' "$1"; }       # ✗
info()    { printf '    %s\n' "$1"; }

repo_status() {
    # $1 = repo dir, $2 = label, $3 = expected remote
    local dir="$1" label="$2" expected="$3"

    if [ ! -d "$dir/.git" ]; then
        fail "$label: NOT INITIALIZED ($dir does not exist)"
        return
    fi
    ok "$label: exists at $dir"

    local actual_remote
    actual_remote="$(git -C "$dir" remote get-url origin 2>/dev/null || echo "")"
    if [ "$actual_remote" = "$expected" ]; then
        ok "$label: remote = $actual_remote"
    else
        warn "$label: remote mismatch (got $actual_remote, expected $expected)"
    fi

    local porcelain
    porcelain="$(git -C "$dir" status --porcelain 2>/dev/null)"
    if [ -z "$porcelain" ]; then
        ok "$label: working tree clean"
    else
        fail "$label: UNCOMMITTED CHANGES (BLOCKING)"
        printf '%s\n' "$porcelain" | sed 's/^/      /'
    fi

    git -C "$dir" fetch --quiet origin 2>/dev/null || warn "$label: fetch failed"

    local upstream ahead behind
    upstream="$(git -C "$dir" rev-parse --abbrev-ref '@{u}' 2>/dev/null || echo "")"
    if [ -n "$upstream" ]; then
        ahead="$(git -C "$dir" rev-list --count "$upstream"..HEAD 2>/dev/null || echo 0)"
        behind="$(git -C "$dir" rev-list --count HEAD.."$upstream" 2>/dev/null || echo 0)"
        if [ "$ahead" = "0" ] && [ "$behind" = "0" ]; then
            ok "$label: in sync with $upstream"
        elif [ "$ahead" != "0" ] && [ "$behind" = "0" ]; then
            warn "$label: $ahead commit(s) ahead of $upstream (push needed)"
        elif [ "$ahead" = "0" ] && [ "$behind" != "0" ]; then
            warn "$label: $behind commit(s) behind $upstream (fast-forward pull safe)"
        else
            fail "$label: DIVERGED ($ahead ahead, $behind behind from $upstream)"
        fi
    else
        warn "$label: no upstream tracking branch configured"
    fi
}

check_symlinks_in() {
    # $1 = directory, $2 = label
    local dir="$1" label="$2"

    if [ ! -d "$dir" ]; then
        warn "$label: directory does not exist"
        return
    fi

    local total=0 good=0 broken=0 not_link=0 wrong_target=0
    local entry name target
    for entry in "$dir"/* "$dir"/.[!.]*; do
        [ -e "$entry" ] || [ -L "$entry" ] || continue
        total=$((total + 1))
        name="$(basename "$entry")"

        if [ -L "$entry" ]; then
            target="$(readlink "$entry")"
            resolved="$(readlink -f "$entry" 2>/dev/null || echo "")"
            if [ ! -e "$entry" ]; then
                broken=$((broken + 1))
                fail "$label/$name → BROKEN symlink ($target)"
            elif [[ "$resolved" != "$KIT_DIR/"* ]]; then
                wrong_target=$((wrong_target + 1))
                warn "$label/$name → wrong target ($target)"
            else
                good=$((good + 1))
            fi
        else
            not_link=$((not_link + 1))
            warn "$label/$name → REAL FILE/DIR (drift; should be symlink)"
        fi
    done

    if [ "$total" = "0" ]; then
        warn "$label: empty"
    elif [ "$good" = "$total" ]; then
        ok "$label: $total entries, all symlinks resolve into $KIT_DIR"
    fi
    info "$label totals: total=$total ok=$good broken=$broken not_link=$not_link wrong_target=$wrong_target"
}

# ── header
echo "# util-toolkit-doctor report"
echo "Generated: $(date 2>/dev/null || echo unknown)"
echo "Host:      $(hostname -s 2>/dev/null || hostname 2>/dev/null || echo unknown)"
echo "User:      ${USER:-unknown}"

# ── prerequisites
section "Prerequisites"
for cmd in chezmoi git gh ssh; do
    if command -v "$cmd" >/dev/null 2>&1; then
        ok "$cmd: $(command -v "$cmd")"
    else
        fail "$cmd: NOT INSTALLED"
    fi
done

# SSH to GitHub
if command -v ssh >/dev/null 2>&1; then
    ssh_out="$(ssh -T -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=5 git@github.com 2>&1 || true)"
    if printf '%s' "$ssh_out" | grep -q "successfully authenticated"; then
        ok "ssh github.com: authenticated"
    else
        fail "ssh github.com: not authenticated ($(printf '%s' "$ssh_out" | head -1))"
    fi
fi

# ── dotfiles repo
section "Dotfiles repo"
repo_status "$DOTFILES_DIR" "dotfiles" "$DOTFILES_REMOTE"

# ── chezmoi state
section "Chezmoi deployed-vs-source state"
if command -v chezmoi >/dev/null 2>&1 && [ -d "$DOTFILES_DIR" ]; then
    cm_status="$(chezmoi status 2>/dev/null || echo "<chezmoi status failed>")"
    if [ -z "$cm_status" ]; then
        ok "chezmoi status: clean"
    else
        warn "chezmoi status has pending changes:"
        printf '%s\n' "$cm_status" | sed 's/^/      /'
        info "(run 'chezmoi diff' for details, 'chezmoi apply' to deploy)"
    fi
else
    info "skipped (chezmoi not installed or dotfiles repo missing)"
fi

# ── kit repo
section "Kit repo"
repo_status "$KIT_DIR" "kit" "$KIT_REMOTE"

# ── symlink health
section "Symlink health (~/.claude/)"
check_symlinks_in "$CLAUDE_DIR/skills"   "skills"
check_symlinks_in "$CLAUDE_DIR/commands" "commands"

# ── footer
section "Legend"
echo "  ✓ ok                — no action needed"
echo "  ⚠ warning           — auto-fixable if safe (drift, behind origin, etc.)"
echo "  ✗ blocking          — requires user confirmation (uncommitted changes, divergence, missing prereqs)"

exit 0
