#!/usr/bin/env python3
"""
migrate.py — com-slide-deck: migrate a pre-design-system deck onto the shared
token contract (the `ux-design-system` skill's docs/ux/tokens.css).

Detects legacy token names in the deck's styles.css and slide partials, maps the
ones that changed to the generic contract, and either:

    python migrate.py --config CONFIG            report only (no writes; default)
    python migrate.py --config CONFIG --apply    add a backwards-compatible alias
                                                 shim to styles.css (additive, safe)
    python migrate.py --config CONFIG --rename    rewrite legacy names -> contract
                                                 names across styles.css + partials

`--apply` and `--rename` are mutually exclusive. `--apply` is the low-risk path
(no partial edits — old var(--bg) keeps working via the shim). `--rename` is the
thorough path (no shim needed afterwards). Commit the deck first; changes are
easy to review in git.

Standard library + PyYAML.
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required. Install it with: pip install pyyaml")
    sys.exit(1)

# Legacy deck token -> contract token (ONLY the names that changed).
RENAME = {
    "--bg":        "--canvas-bg",
    "--text":      "--ink",
    "--card-bg":   "--surface",
    "--font-body": "--font-sans",
}
# Legacy names with no contract equivalent — they stay deck-only (no action;
# they remain defined in the deck's styles.css and keep working).
DECK_ONLY = ["--dim", "--accent-lt", "--danger-lt", "--font-heading"]
# Base/semantic contract tokens whose VALUES belong in the design system, not in
# styles.css — used to advise moving the palette out.
CONTRACT_BASE = [
    "--ink", "--muted", "--canvas-bg", "--surface", "--surface-2", "--border",
    "--accent", "--accent-ink", "--success", "--warning", "--danger", "--info",
    "--font-sans", "--font-mono",
]

SHIM_START = "/* >>> com-slide-deck migrate: legacy-token shim >>> */"
SHIM_END = "/* <<< com-slide-deck migrate <<< */"


def tok_re(name):
    """Match a CSS custom-property name as a whole token (so --bg != --bgx)."""
    return re.compile(r"(?<![\w-])" + re.escape(name) + r"(?![\w-])")


def resolve(base, rel):
    return (base / rel).resolve()


def gather_files(base, cfg):
    paths = cfg.get("paths", {})
    styles = resolve(base, paths.get("styles_file", "design/styles.css"))
    slides_dir = resolve(base, paths.get("slides_dir", "output/slides"))
    files = []
    if styles.exists():
        files.append(styles)
    partials = []
    if slides_dir.exists():
        partials += sorted(slides_dir.glob("*.html"))
    for proto in (slides_dir.parent / "prototypes", base / "dist" / "prototypes",
                  base / "output" / "prototypes"):
        if proto.exists():
            partials += sorted(proto.glob("*.html"))
    files += partials
    return files, styles, partials


def scan(files):
    """Return {token: {path: count}} for every legacy token found."""
    found = {}
    for f in files:
        text = f.read_text(encoding="utf-8")
        for name in list(RENAME) + DECK_ONLY:
            n = len(tok_re(name).findall(text))
            if n:
                found.setdefault(name, {})[str(f)] = n
    return found


def find_tokens_css(base, cfg):
    """Mirror build.py: configured design_tokens, else walk up to docs/ux/tokens.css."""
    configured = cfg.get("paths", {}).get("design_tokens")
    if configured:
        p = resolve(base, configured)
        return p if p.exists() else None
    cur = base.resolve()
    for _ in range(8):
        cand = cur / "docs" / "ux" / "tokens.css"
        if cand.exists():
            return cand
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


def styles_defines_palette(styles):
    """True if styles.css still defines base/semantic contract values (hex, not var())."""
    if not styles.exists():
        return []
    text = styles.read_text(encoding="utf-8")
    hits = []
    for name in CONTRACT_BASE:
        m = re.search(tok_re(name).pattern + r"\s*:\s*([^;]+);", text)
        if m and "var(" not in m.group(1):
            hits.append(name)
    return hits


def rel(p, base):
    try:
        return str(Path(p).resolve().relative_to(base.resolve()))
    except ValueError:
        return str(p)


# --------------------------------------------------------------------------- #

def do_report(base, cfg, found, styles):
    print("=== com-slide-deck migrate — report ===\n")

    tokens_css = find_tokens_css(base, cfg)
    if tokens_css:
        print(f"[ok]   project design system found: {rel(tokens_css, base)}")
    else:
        print("[todo] no project design system (docs/ux/tokens.css) found.")
        print("       run first:  ux-design-system scaffold   then fill + generate")

    if not found:
        print("\n[ok]   no legacy token names detected — this deck already speaks the contract.")
        return
    print("\nLegacy tokens detected:\n")
    renamable = {t: m for t, m in found.items() if t in RENAME}
    keepers = {t: m for t, m in found.items() if t in DECK_ONLY}

    if renamable:
        print("  Changed names (need shim or rename):")
        for t, m in sorted(renamable.items()):
            where = ", ".join(f"{rel(p, base)}×{c}" for p, c in m.items())
            print(f"    {t:14s} -> {RENAME[t]:14s}  [{where}]")
    if keepers:
        print("\n  Deck-only names (no change needed — keep defining them in styles.css):")
        for t, m in sorted(keepers.items()):
            print(f"    {t}")

    palette = styles_defines_palette(styles)
    if palette:
        print("\n  [todo] styles.css still hard-codes base/semantic values for:")
        print("         " + ", ".join(palette))
        print("         move these VALUES into docs/ux/design-system.md, then "
              "`ux-design-system generate`,")
        print("         and delete them from styles.css so the deck inherits them.")

    print("\nNext:")
    print("  --apply   add a backwards-compatible shim to styles.css (no partial edits)")
    print("  --rename  rewrite the changed names across styles.css + partials")


def do_apply(base, found, styles):
    used = [t for t in RENAME if t in found]
    if not used:
        print("[apply] no changed legacy tokens in use — nothing to shim.")
        return
    if not styles.exists():
        print(f"[apply] styles.css not found: {styles}")
        return
    text = styles.read_text(encoding="utf-8")
    # remove any prior shim block
    text = re.sub(re.escape(SHIM_START) + r".*?" + re.escape(SHIM_END) + r"\n?",
                  "", text, flags=re.DOTALL)
    lines = [SHIM_START,
             "/* Legacy deck token names aliased to the contract so existing slide",
             "   partials keep working. Remove this block once partials are renamed",
             "   (or run migrate.py --rename to do that automatically). */",
             ":root {"]
    for t in used:
        lines.append(f"  {t}: var({RENAME[t]});")
    lines += ["}", SHIM_END, ""]
    shim = "\n".join(lines)
    styles.write_text(shim + "\n" + text, encoding="utf-8")
    print(f"[apply] wrote alias shim for {', '.join(used)} into {rel(styles, base)}")
    print("        rebuild with build.py; old partials now resolve to contract values.")


def do_rename(base, found, files):
    used = [t for t in RENAME if t in found]
    if not used:
        print("[rename] no changed legacy tokens in use — nothing to rename.")
        return
    total = 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        new = text
        n = 0
        for t in used:
            new, k = tok_re(t).subn(RENAME[t], new)
            n += k
        if n:
            f.write_text(new, encoding="utf-8")
            total += n
            print(f"[rename] {rel(f, base)}: {n} replacement(s)")
    print(f"[rename] done — {total} replacement(s) across {len(files)} file(s). "
          f"No shim needed.")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Migrate a deck onto the shared design-system tokens.")
    ap.add_argument("--config", required=True, help="Path to the deck's config.yaml")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--apply", action="store_true", help="Add the legacy-token alias shim to styles.css")
    g.add_argument("--rename", action="store_true", help="Rewrite legacy names -> contract names in place")
    args = ap.parse_args(argv)

    config_path = Path(args.config).resolve()
    if not config_path.is_file():
        sys.exit(f"error: config not found: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    base = config_path.parent

    files, styles, _partials = gather_files(base, cfg)
    found = scan(files)

    if args.apply:
        do_apply(base, found, styles)
    elif args.rename:
        do_rename(base, found, files)
    else:
        do_report(base, cfg, found, styles)


if __name__ == "__main__":
    main()
