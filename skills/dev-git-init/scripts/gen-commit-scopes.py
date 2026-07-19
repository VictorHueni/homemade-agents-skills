#!/usr/bin/env python3
"""Generate the commit / PR-title scope-enum from a capability map + FBS.

Read-only, pure stdlib. Derives a Conventional-Commit ``scope`` allowlist from
the project's own product vocabulary so that ``feat(<capability>): …`` reads as
plain language in the changelog and a work-item number (``feat(0121): …``) can
be rejected as out-of-enum.

Primary source — first-class canonical slugs. Each L0 domain, L1 capability, and
product declares a ```slug: <handle>``` code-line under its heading (owned by the
capability map + FBS; see the `metamodel` skill's `references/artefact-types-registry.yaml` § Canonical slugs,
audited for presence + global-uniqueness + kebab format by ``util-metamodel-audit``
Check 19). Slugs are short, kebab, and globally unique *by construction upstream*,
so the generator just harvests them — it never derives or shortens. A developer
scopes at whichever declared altitude fits (capability, product, or L0 domain);
all resolve to a Product → Capability home via the FBS. A malformed (non-kebab)
declaration is reported to stderr and skipped, never silently emitted.

    ### C1.6 · Prior Authorization / Clinical Decision Support
    `slug: prior-auth`                   → harvested verbatim

Degradation: on a repo that predates the slug convention (no ```slug:``` lines),
fall back to slugifying capability / product *names* and nudge the operator to
declare first-class slugs (the fix is always upstream — never hand-edit the
emitted JSON, which the drift-gate forbids).

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

# A slug longer than this is awkward to type as a commit scope → warn. Chosen so
# short handles (`catalog-maintenance`, 19) pass and a long slugified name (40+
# chars, e.g. a five-word capability title) trips it.
MAX_SLUG_LEN = 20

# Tokens dropped from a slug — connective words that carry no scope signal.
_STOPWORDS = frozenset({"and", "or", "the", "of", "a", "an", "to", "for", "with"})

# `## C1 · Some Domain`  /  `### C2.1 · Some Capability` — capability headings.
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

# First-class canonical slug: `` `slug: <kebab>` `` on its own line under an L0 / L1 /
# product heading (owned by the capability map + FBS; see artefact-types-registry.md
# § Canonical slugs, enforced by util-metamodel-audit Check 19). Recognised loosely,
# then validated as kebab, so a malformed value is reported rather than silently missed.
_SLUG_DECL = re.compile(r"^\s*`slug:\s*(.+?)\s*`\s*$")
_KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


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


def _declared_slugs(text: str) -> tuple[set[str], list[str]]:
    """Harvest first-class `` `slug: <handle>` `` declarations (L0 / L1 / product).

    These are the canonical identifiers the capability map + FBS now own. Loosely
    recognise the line, then validate kebab-case so a malformed value is reported
    (not silently dropped) — mirroring how audit Check 19 distinguishes MISSING
    from MALFORMED.
    """
    slugs: set[str] = set()
    warnings: list[str] = []
    for line in text.splitlines():
        m = _SLUG_DECL.match(line)
        if not m:
            continue
        val = m.group(1)
        if _KEBAB.match(val):
            slugs.add(val)
            if len(val) > MAX_SLUG_LEN:
                warnings.append(f"declared slug '{val}' ({len(val)} chars) exceeds {MAX_SLUG_LEN} — shorten it in the source doc.")
        else:
            warnings.append(f"malformed slug '{val}' (not kebab-case) — fix it in the source doc; skipped.")
    return slugs, warnings


def derive_scopes(sources: list[Path]) -> tuple[list[str], list[str]]:
    """Return (ordered scope-enum, warnings).

    Primary path: harvest the first-class canonical slugs the capability map + FBS
    declare. Degradation path (a repo that predates the slug convention — no `slug:`
    lines at all): fall back to slugifying capability / product names, warning that
    slugs should be added.
    """
    declared: set[str] = set()
    warnings: list[str] = []
    for path in sources:
        text = path.read_text(encoding="utf-8")
        s, w = _declared_slugs(text)
        declared |= s
        warnings += w

    if declared:
        ordered = sorted(declared) + [b for b in FIXED_BUCKETS if b not in declared]
        return ordered, sorted(set(warnings))

    # No first-class slugs anywhere → degrade to name-derived scopes.
    fallback: set[str] = set()
    for path in sources:
        text = path.read_text(encoding="utf-8")
        fallback |= _capability_slugs(text)
        fallback |= _product_slugs(text)
    ordered = sorted(fallback) + [b for b in FIXED_BUCKETS if b not in fallback]
    warns = [
        f"scope '{s}' ({len(s)} chars) is long — declare a `slug:` under its heading "
        "(see artefact-types-registry.md § Canonical slugs)."
        for s in sorted(fallback)
        if len(s) > MAX_SLUG_LEN
    ]
    warns.append(
        "no `slug:` declarations found — using name-derived scopes as a fallback; "
        "add first-class slugs to the capability map / FBS."
    )
    return ordered, sorted(set(warns))


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
