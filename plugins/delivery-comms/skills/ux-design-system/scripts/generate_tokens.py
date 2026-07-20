#!/usr/bin/env python3
"""
generate_tokens.py — ux-design-system skill.

Author the project design system once; generate the machine-read token sheet
every com-* renderer consumes.

Modes:
    scaffold [DOCS_DIR]      Create DOCS_DIR/design/{design-system.md, tokens.css}
                             (default DOCS_DIR=docs). Skips files that exist.
    generate SRC.md          Parse SRC.md's ## Tokens tables -> tokens.css
                             written next to it (alias: refresh).

Token names are the fixed contract (templates/tokens.template.css). Values are
free; renaming or dropping a token is flagged against the contract.

Standard library only.
"""

import argparse
import datetime
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
TEMPLATE_DIR = os.path.join(SKILL_DIR, "templates")

TOKEN_RE = re.compile(r"^--[a-z0-9-]+$")


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def contract_tokens():
    """Canonical token names, parsed from the default tokens template."""
    css = read(os.path.join(TEMPLATE_DIR, "tokens.template.css"))
    return [m.group(1) for m in re.finditer(r"^\s*(--[a-z0-9-]+)\s*:", css, re.M)]


# --------------------------------------------------------------------------- #
# Parse the authored design-system.md
# --------------------------------------------------------------------------- #

def parse_groups(md):
    """
    Return [(group_name, [(token, value), ...]), ...] from the ## Tokens section.
    A group is a ### heading followed by a table whose first column is `Token`.
    """
    # Restrict to the ## Tokens section if present.
    m = re.search(r"^##\s+Tokens\s*$(.*?)(^##\s+|\Z)", md, re.M | re.S)
    body = m.group(1) if m else md

    groups = []
    cur_name = "Tokens"
    cur = []
    lines = body.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        h = re.match(r"^###\s+(.*\S)\s*$", line)
        if h:
            if cur:
                groups.append((cur_name, cur))
                cur = []
            cur_name = h.group(1).strip()
            i += 1
            continue
        if line.strip().startswith("|"):
            # collect contiguous table rows
            tbl = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                tbl.append(lines[i])
                i += 1
            cur.extend(parse_token_table(tbl))
            continue
        i += 1
    if cur:
        groups.append((cur_name, cur))
    return groups


def parse_token_table(tbl_lines):
    if len(tbl_lines) < 2:
        return []
    def cells(l):
        return [c.strip() for c in l.strip().strip("|").split("|")]
    headers = [h.lower() for h in cells(tbl_lines[0])]
    if not headers or headers[0] != "token":
        return []
    out = []
    for line in tbl_lines[2:]:
        if re.match(r"^\s*\|[\s:|-]+\|?\s*$", line):
            continue
        c = cells(line)
        if len(c) < 2:
            continue
        token = c[0].strip().strip("`").strip()
        value = c[1].strip().strip("`").strip()
        if TOKEN_RE.match(token) and value:
            out.append((token, value))
    return out


def emit_css(groups, source_rel):
    today = datetime.date.today().isoformat()
    lines = [
        "/*",
        " * tokens.css — canonical design-system token contract.",
        " *",
        f" * GENERATED from {source_rel} by the ux-design-system skill on {today}.",
        " * Edit the token tables in design-system.md and re-run `generate`; do not",
        " * hand-edit here (changes are overwritten on refresh).",
        " *",
        " * Every com-* renderer references these variables via var() and never",
        " * hard-codes a colour/font/radius — so editing values re-themes every deck",
        " * and view with no renderer change.",
        " */",
        ":root {",
    ]
    for name, tokens in groups:
        if not tokens:
            continue
        lines.append(f"  /* ---- {name} ---- */")
        width = max((len(t) for t, _ in tokens), default=0)
        for token, value in tokens:
            lines.append(f"  {token}:{' ' * (width - len(token) + 1)}{value};")
        lines.append("")
    if lines[-1] == "":
        lines.pop()
    lines.append("}")
    return "\n".join(lines) + "\n"


def validate(groups):
    found = [t for _, toks in groups for t, _ in toks]
    contract = contract_tokens()
    missing = [t for t in contract if t not in found]
    unknown = [t for t in found if t not in contract]
    if missing:
        print(f"warning: {len(missing)} contract token(s) missing from the doc: "
              f"{', '.join(missing)}", file=sys.stderr)
    if unknown:
        print(f"warning: {len(unknown)} token(s) not in the contract (kept anyway): "
              f"{', '.join(unknown)}", file=sys.stderr)


# --------------------------------------------------------------------------- #
# Modes
# --------------------------------------------------------------------------- #

def git_user():
    try:
        return subprocess.run(
            ["git", "config", "user.name"], capture_output=True, text=True
        ).stdout.strip() or "_TODO_"
    except Exception:
        return "_TODO_"


def mode_scaffold(docs_dir):
    design_dir = os.path.join(docs_dir, "design")
    md_path = os.path.join(design_dir, "design-system.md")
    css_path = os.path.join(design_dir, "tokens.css")
    today = datetime.date.today().isoformat()
    user = git_user()

    created = []
    if not os.path.exists(md_path):
        tmpl = read(os.path.join(TEMPLATE_DIR, "design-system.template.md"))
        tmpl = (tmpl.replace("{{product_or_scope}}", "{{product_or_scope}}")
                    .replace("{{owner}}", user)
                    .replace("{{YYYY-MM-DD}}", today))
        write(md_path, tmpl)
        created.append(md_path)
    else:
        print(f"exists, skipped: {md_path}")
    if not os.path.exists(css_path):
        write(css_path, read(os.path.join(TEMPLATE_DIR, "tokens.template.css")))
        created.append(css_path)
    else:
        print(f"exists, skipped: {css_path}")

    for p in created:
        print(f"created {p}")
    if md_path in created:
        print("\nnext: fill the brand rationale + token values in design-system.md, "
              "then run:\n  python scripts/generate_tokens.py generate "
              f"{os.path.relpath(md_path)}")


def mode_generate(src):
    if not os.path.isfile(src):
        sys.exit(f"error: not found: {src}")
    md = read(src)
    groups = parse_groups(md)
    if not any(toks for _, toks in groups):
        sys.exit(f"error: no token tables found in {src} (expected '## Tokens' "
                 f"section with '| Token | Value | … |' tables).")
    validate(groups)
    css = emit_css(groups, os.path.relpath(src))
    out = os.path.join(os.path.dirname(src), "tokens.css")
    write(out, css)
    total = sum(len(toks) for _, toks in groups)
    print(f"wrote {out} ({total} tokens, {len(groups)} groups)")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Generate the design-system token sheet.")
    sub = ap.add_subparsers(dest="mode", required=True)

    s = sub.add_parser("scaffold", help="Create docs/ux/{design-system.md, tokens.css}")
    s.add_argument("docs_dir", nargs="?", default="docs")

    g = sub.add_parser("generate", aliases=["refresh"], help="design-system.md -> tokens.css")
    g.add_argument("src")

    args = ap.parse_args(argv)
    if args.mode == "scaffold":
        mode_scaffold(args.docs_dir)
    else:
        mode_generate(args.src)


if __name__ == "__main__":
    main()
