#!/usr/bin/env python3
"""Generate the commit / PR-title scope-enum from a capability map + FBS.

Read-only, pure stdlib. Derives a Conventional-Commit ``scope`` allowlist from
the project's own product vocabulary so that ``feat(<capability>): …`` reads as
plain language in the changelog and a work-item number (``feat(0121): …``) can
be rejected as out-of-enum.

Scope altitude is the **capability** (not the product): every capability maps to
one product in the FBS, so a capability scope encodes Product → Capability → (the
subject line is the functionality) — the full hierarchy — while a product-only
scope would skip the capability. Product slugs are kept too, for genuinely
cross-capability product work.

Short capability slugs: a capability whose display name is verbose can declare a
short **``scope:`` alias** in its block in the capability map; the generator emits
the alias instead of the long slugified name. When a capability has no alias and
its slugified name is too long to be a usable commit scope, the generator warns
and suggests declaring one (the fix is author-once in the capability map — never
hand-edit the emitted JSON, which the drift-gate forbids).

    ### C6.1 · Prior Authorization / Clinical Decision Support
    scope: prior-auth                    → emits `prior-auth`, not the 44-char slug

Sources (both optional; at least one must exist):
  - capability map : ``docs/business/03a-capability-map.md``  (L0 domains + products)
  - FBS            : ``docs/product-specs/07a-fbs.md``         (L0 domains + products)

Output: a byte-stable JSON document ``{"scopes": [...], "sources": [...]}`` whose
``scopes`` array is ``sorted(derived_slugs) + fixed_buckets``. commitlint reads
``require('./.commit-scopes.json').scopes``; the PR-title-lint advisory step and
the drift-gate re-run this generator and diff.

Graceful degradation: if neither source exists, print a message to stderr and
exit 2 (no enum). The caller falls back to free area/module scopes.

Exit codes:
  0  wrote / printed an enum (over-length warnings, if any, go to stderr)
  2  no capability map / FBS found (degrade to area-based scopes)
  1  unexpected error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Fixed buckets always appended after the derived, project-specific slugs. These
# cover cross-cutting change classes that map to no single capability.
FIXED_BUCKETS: tuple[str, ...] = ("platform", "infra", "ci", "deps", "chore")

# A slug longer than this is awkward to type as a commit scope → warn + suggest
# a `scope:` alias. Chosen so short capability names (`drug-discovery`, 14) pass
# and verbose ones (`prior-authorization-clinical-decision-support`, 44) trip it.
MAX_SLUG_LEN = 20

# Tokens dropped from a slug — connective words that carry no scope signal.
_STOPWORDS = frozenset({"and", "or", "the", "of", "a", "an", "to", "for", "with"})

# `## C1 · Drug Catalog …`  /  `### C2.1 · Some Capability` — capability headings.
_CAP_HEADING = re.compile(r"^#{2,4}\s+C(\d+)(?:\.\d+)*\s*[·\-–—:]\s*(.+?)\s*$")
# `| **P1** | Acme Billing | … |` — product cross-reference rows.
_PRODUCT_ROW = re.compile(r"^\|\s*\*{0,2}P(\d+)\*{0,2}\s*\|\s*([^|]+?)\s*\|")
# `- **C1** — Name of first L0 item` — L0 bullet list (template scaffold form).
_L0_BULLET = re.compile(r"^\s*[-*]\s*\*{0,2}C(\d+)\*{0,2}\s*[—\-–·:]\s*(.+?)\s*$")
# `scope: prior-auth`  /  `**scope:** prior-auth`  /  `- scope: `prior-auth`` — a
# capability's declared short commit-scope alias (within its block).
_SCOPE_ALIAS = re.compile(
    r"^\s*(?:[-*]\s*)?\*{0,2}scope\*{0,2}\s*[:=]\s*[`'\"]?([a-z0-9][a-z0-9-]*)[`'\"]?\s*\*{0,2}\s*$",
    re.IGNORECASE,
)
_ANY_HEADING = re.compile(r"^#{1,6}\s")
# How far past a capability marker to look for its `scope:` alias before giving up.
_ALIAS_SCAN_LINES = 12


def slugify(name: str) -> str:
    """Lower-case kebab slug; drops connective stopwords and bracketed notes."""
    name = re.sub(r"\[[^\]]*\]|\([^)]*\)|\{[^}]*\}", " ", name)  # strip notes/placeholders
    name = re.sub(r"&", " and ", name)
    tokens = re.split(r"[^a-z0-9]+", name.lower())
    tokens = [t for t in tokens if t and t not in _STOPWORDS]
    return "-".join(tokens)


def _strip_common_prefix(names: list[str]) -> list[str]:
    """Drop a shared leading word (a product-family name like "Acme").

    A first word common to every product name is branding, not scope signal.
    """
    firsts = [n.split() for n in names if n.split()]
    if len(firsts) < 2:
        return names
    lead = firsts[0][0].lower()
    if all(len(w) > 1 and w[0].lower() == lead for w in firsts):
        return [" ".join(w[1:]) if len(w) > 1 else " ".join(w) for w in firsts]
    return names


def _l0_name(line: str) -> str | None:
    """The L0 capability display name on this line (heading or bullet), else None."""
    m = _CAP_HEADING.match(line)
    if m:
        # L0 only (no dotted sub-level) → coarse-grained scopes.
        head_id = re.match(r"^#{2,4}\s+C(\d+)(\.\d+)*", line)
        if head_id and head_id.group(2) is None:
            return m.group(2)
        return None
    b = _L0_BULLET.match(line)
    return b.group(2) if b else None


def _find_alias(lines: list[str], start: int) -> str | None:
    """Scan a capability's block for a `scope:` alias; stop at the next marker."""
    scanned = 0
    for line in lines[start:]:
        if scanned >= _ALIAS_SCAN_LINES or _ANY_HEADING.match(line) or _L0_BULLET.match(line):
            break
        a = _SCOPE_ALIAS.match(line)
        if a:
            return a.group(1).lower()
        scanned += 1
    return None


def _capability_slugs(text: str) -> set[str]:
    """L0 capability slugs, preferring an in-block `scope:` alias over the name."""
    slugs: set[str] = set()
    lines = text.splitlines()
    for i, line in enumerate(lines):
        name = _l0_name(line)
        if name is None:
            continue
        slugs.add(_find_alias(lines, i + 1) or slugify(name))
    return {s for s in slugs if s}


def _product_slugs(text: str) -> set[str]:
    """Product slugs from `**P1** | Name` rows, with common-prefix strip."""
    names: list[str] = []
    for line in text.splitlines():
        m = _PRODUCT_ROW.match(line)
        if m:
            raw = re.sub(r"\[[^\]]*\]|\([^)]*\)|\*+", " ", m.group(2)).strip()
            if raw and raw.lower() not in {"name", "product"}:
                names.append(raw)
    names = _strip_common_prefix(names)
    return {s for s in (slugify(n) for n in names) if s}


def derive_scopes(sources: list[Path]) -> tuple[list[str], list[str]]:
    """Return (ordered scope-enum, warnings). Warnings flag over-long derived
    slugs that should get a short `scope:` alias in the capability map."""
    derived: set[str] = set()
    for path in sources:
        text = path.read_text(encoding="utf-8")
        derived |= _capability_slugs(text)
        derived |= _product_slugs(text)
    ordered = sorted(derived)
    ordered += [b for b in FIXED_BUCKETS if b not in derived]
    warnings = [
        f"scope '{s}' ({len(s)} chars) is long for a commit scope — declare a short "
        "`scope:` alias in the capability map (author-once; do not edit the JSON)."
        for s in sorted(derived)
        if len(s) > MAX_SLUG_LEN
    ]
    return ordered, warnings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Generate the commit scope-enum.")
    ap.add_argument("--capability-map", default="docs/business/03a-capability-map.md")
    ap.add_argument("--fbs", default="docs/product-specs/07a-fbs.md")
    ap.add_argument("--out", default="-", help="output path, or '-' for stdout (default)")
    args = ap.parse_args(argv)

    sources = [Path(p) for p in (args.capability_map, args.fbs) if Path(p).is_file()]
    if not sources:
        print(
            "gen-commit-scopes: no capability map or FBS found "
            f"({args.capability_map}, {args.fbs}); "
            "no scope-enum generated — fall back to area/module scopes.",
            file=sys.stderr,
        )
        return 2

    try:
        scopes, warnings = derive_scopes(sources)
    except OSError as exc:  # unreadable source
        print(f"gen-commit-scopes: {exc}", file=sys.stderr)
        return 1

    for w in warnings:
        print(f"gen-commit-scopes: {w}", file=sys.stderr)

    doc = {"scopes": scopes, "sources": sorted(str(p) for p in sources)}
    payload = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"

    if args.out == "-":
        sys.stdout.write(payload)
    else:
        Path(args.out).write_text(payload, encoding="utf-8")
        print(f"gen-commit-scopes: wrote {len(scopes)} scopes → {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
