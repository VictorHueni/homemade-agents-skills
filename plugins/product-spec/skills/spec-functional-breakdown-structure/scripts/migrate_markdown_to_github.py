#!/usr/bin/env python3
"""One-way markdown -> github migration for FBS functionality identity.

Implements ADR-0010 (docs/architecture/decisions/adr-0010-fbs-functionality-identity-
pluggable-issue-backend.md, in the consuming repo): migration is performed once, markdown ->
github only, and MUST emit a persisted C-N.M.FXX -> #N map so back-references survive the
identifier re-mint. Capability identity (C-N.M) is OUT OF SCOPE and never migrates -- it
stays markdown-authored in the BC Map, per ADR-0010's explicit boundary. There is NO reverse
path and NO concurrent two-way sync.

Pipeline:
  0. Bootstrap the `type:functionality` label idempotently.
  1. Parse every capability section's functionality table out of the FBS doc.
  2. Pass 1 -- for each row, create (or reuse, matched by the idempotency marker) a GitHub
     issue: title = functionality name (no ID prefix), body = `Capability:` line +
     `VS stage:` line (when set) + the hidden marker trailer.
  3. Pass 2 -- patch every issue CREATED in this run: rewrite any plain-text C-N.M.FXX
     mention in its resolved body to `#N` now that the batch's full map is known. The marker
     trailer is excluded from this scan by construction (the reference implementation's
     caught bug -- see references/github-backend.md SS3 -- the resolved body and the marker
     are two separate strings from the moment each issue is composed, never scanned
     together).
  4. Emit the C-N.M.FXX -> #N map.
  5. Rewrite C-N.M.FXX back-references across the docs tree to #N.

DRY-RUN BY DEFAULT. Nothing mutates GitHub or any file unless --apply is passed. FBS.md
retirement + the backend.yml flip are left to the operator (Mode 4 in SKILL.md) so issues can
be eyeballed before the markdown source of truth is frozen -- same posture as
util-open-items' Mode 7.

Project field sync (Capability / Status single-select fields) is NOT automated here -- it
needs the GraphQL field IDs for the project's own configuration, a one-time per-project
setup (see SKILL.md Mode 4). The migration prints a reminder when --project is set; the
operator applies fields after eyeballing the created issues.

stdlib only; requires the `gh` CLI authenticated against --repo.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

CAP_HEADING_RE = re.compile(r"^###\s+(C\d+(?:\.\d+)+)\s+·\s+(.+?)\s*$")
FUNC_ROW_RE = re.compile(
    r"^\|\s*(C\d+(?:\.\d+)+\.F\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$"
)
# Any C-N.M.FXX mention in resolved body text -- used by pass 2, restricted to the
# resolved-body string only (never the marker trailer -- see module docstring SS3).
XREF_RE = re.compile(r"\bC\d+(?:\.\d+)+\.F\d+\b")
NO_VALUE = {"_TODO_", "—", "-", ""}


def run(cmd: list[str], apply: bool, capture: bool = False) -> str | None:
    """Run a command. In dry-run, print intent for mutating gh calls and skip them."""
    is_read = cmd[:2] in (["gh", "issue"], ["gh", "api"]) and any(
        x in cmd for x in ("list", "view")
    )
    if not apply and not is_read:
        print(f"  DRY-RUN would run: {' '.join(cmd)}")
        return None
    res = subprocess.run(cmd, capture_output=capture, text=True)
    if res.returncode != 0:
        sys.stderr.write(f"  WARN: command failed ({res.returncode}): {' '.join(cmd)}\n")
        if capture and res.stderr:
            sys.stderr.write(f"        {res.stderr.strip()}\n")
        return None
    return res.stdout if capture else ""


def parse_fbs(path: Path) -> list[dict]:
    """Extract every non-placeholder functionality row, tagged with its enclosing
    capability. Table header/separator rows never match FUNC_ROW_RE (their first cell
    isn't C-N.M.FXX-shaped), so no special-casing is needed to skip them."""
    rows: list[dict] = []
    current_cap: str | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        cap_m = CAP_HEADING_RE.match(raw)
        if cap_m:
            current_cap = cap_m.group(1)
            continue
        row_m = FUNC_ROW_RE.match(raw)
        if row_m and current_cap:
            fid, name, status, vs_stage = row_m.groups()
            if name in NO_VALUE:
                continue
            rows.append({
                "id": fid, "capability": current_cap, "name": name,
                "status": status, "vs_stage": vs_stage,
            })
    return rows


def marker(row: dict) -> str:
    """The migration case has a pre-existing C-N.M.FXX to key off -- unlike Mode 3's
    interactive path (references/github-backend.md SS4), which derives a slug because
    no ID exists yet at authoring time."""
    return f"<!-- fbs-seed: {row['id']} -->"


def resolved_body(row: dict) -> str:
    """The FBS template carries no separate description field -- a functionality's only
    free text is its Name cell, which is also where an inline cross-reference like
    "(see also C1.2.F03)" would actually appear. Include it here (not just as the issue
    title) so pass 2 has real text to scan and patch."""
    lines = [f"Capability: {row['capability']}"]
    if row["vs_stage"] not in NO_VALUE:
        lines.append(f"VS stage: {row['vs_stage']}")
    lines.append("")
    lines.append(row["name"])
    return "\n".join(lines)


def find_existing(repo: str, row: dict) -> int | None:
    """De-dup: an open or closed issue whose body already carries this row's marker."""
    out = run(
        ["gh", "issue", "list", "-R", repo, "--state", "all",
         "--search", marker(row), "--json", "number,body", "-L", "10"],
        apply=True, capture=True,
    )
    if not out:
        return None
    try:
        for it in json.loads(out):
            if marker(row) in it.get("body", ""):
                return int(it["number"])
    except (json.JSONDecodeError, ValueError):
        pass
    return None


def create_issue(repo: str, row: dict, apply: bool) -> int | None:
    existing = find_existing(repo, row)
    if existing:
        print(f"  {row['id']} -> #{existing} (existing, reused)")
        return existing
    full_body = f"{resolved_body(row)}\n\n{marker(row)}"
    cmd = ["gh", "issue", "create", "-R", repo,
           "--title", row["name"],
           "--body", full_body,
           "--label", "type:functionality"]
    out = run(cmd, apply, capture=True)
    if not apply or not out:
        return None
    m = re.search(r"/issues/(\d+)", out.strip())
    return int(m.group(1)) if m else None


def patch_cross_references(
    repo: str, created: dict[int, dict], mapping: dict[str, int], apply: bool
) -> None:
    """Pass 2. `created` holds {issue_number: row} for issues made in THIS run only --
    reused (pre-existing) issues are not re-scanned, matching the reference implementation's
    per-run batch scope. Re-derives the resolved body from the row rather than the string
    written by create_issue, so this stays correct even if create_issue's dry-run path (which
    returns before writing) is the only thing that ran."""
    for number, row in created.items():
        body = resolved_body(row)
        def sub(m: re.Match) -> str:
            target = mapping.get(m.group(0))
            return f"#{target}" if target else m.group(0)
        patched = XREF_RE.sub(sub, body)
        if patched == body:
            continue
        full_body = f"{patched}\n\n{marker(row)}"
        run(["gh", "issue", "edit", str(number), "-R", repo, "--body", full_body], apply)
        print(f"  #{number}: cross-references resolved")


def rewrite_refs(docs: Path, mapping: dict[str, int], apply: bool, skip: str) -> None:
    if not mapping:
        return
    pattern = re.compile(r"\b(" + "|".join(re.escape(k) for k in mapping) + r")\b")
    for md in sorted(docs.rglob("*.md")):
        if skip in md.as_posix():
            continue
        text = md.read_text(encoding="utf-8")
        new, n = pattern.subn(lambda m: f"#{mapping[m.group(1)]}", text)
        if n:
            print(f"  {md}: {n} C-N.M.FXX -> #N rewrites")
            if apply:
                md.write_text(new, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", required=True, help="OWNER/NAME where issues are created")
    ap.add_argument("--fbs", default="docs/product-specs/07a-fbs.md")
    ap.add_argument("--docs", default="docs", help="tree to rewrite C-N.M.FXX back-references in")
    ap.add_argument("--map-out", default="docs/product-specs/migration-map.md")
    ap.add_argument("--project", type=int, default=None,
                     help="Project v2 number, if backend.yml sets one (prints a reminder only)")
    ap.add_argument("--apply", action="store_true", help="perform mutations (default: dry-run)")
    args = ap.parse_args()

    fbs = Path(args.fbs)
    if not fbs.is_file():
        sys.stderr.write(f"ERROR: FBS doc not found: {fbs}\n")
        return 2

    rows = parse_fbs(fbs)
    print(f"Parsed {len(rows)} functionality rows from {fbs}")
    print(f"Mode: {'APPLY' if args.apply else 'DRY-RUN (no mutations)'}\n")

    run(["gh", "label", "create", "type:functionality", "--repo", args.repo,
         "--color", "0e8a16", "--description", "FBS functionality (github backend)",
         "--force"], args.apply)

    mapping: dict[str, int] = {}
    created: dict[int, dict] = {}
    for row in rows:
        number = create_issue(args.repo, row, args.apply)
        if number is None:
            if args.apply:
                sys.stderr.write(f"  WARN: no issue number for {row['id']}\n")
            continue
        mapping[row["id"]] = number
        created[number] = row
        print(f"  {row['id']} -> #{number} ({row['status']})")

    print("\nResolving cross-references:")
    patch_cross_references(args.repo, created, mapping, args.apply)

    lines = [
        "# FBS — markdown -> github migration map",
        "",
        f"Generated {date.today().isoformat()} against `{args.repo}`. "
        "One-way; back-references rewritten to `#N`. Frozen once written -- never edited "
        "after the FBS doc is archived.",
        "",
        "| C-N.M.FXX | Issue | Status at migration |",
        "| :-------- | :---- | :------------------- |",
    ]
    for row in rows:
        n = mapping.get(row["id"])
        lines.append(f"| {row['id']} | {'#' + str(n) if n else '_FAILED_'} | {row['status']} |")
    map_text = "\n".join(lines) + "\n"
    print(f"\nMap ({len(mapping)} mapped):")
    print(map_text)
    if args.apply:
        Path(args.map_out).write_text(map_text, encoding="utf-8")
        print(f"Wrote {args.map_out}")

    print("\nRewriting back-references:")
    rewrite_refs(Path(args.docs), mapping, args.apply, skip="product-specs/migration-map.md")

    if args.project:
        print(f"\nNOTE: --project {args.project} set -- Capability/Status Project fields are "
              "NOT synced by this script. Set them via the UI or a one-time GraphQL pass "
              "after eyeballing the created issues (SKILL.md Mode 4).")

    if not args.apply:
        print("\nDRY-RUN complete. Re-run with --apply to migrate, then (operator):")
        print("  1. verify the issues + labels look right (gh issue list --label type:functionality)")
        print("  2. run plan-delivery-roadmap's Mode 3 migrate (epics depend on this map)")
        print("  3. archive docs/product-specs/07a-fbs.md (frozen snapshot) and set backend.yml: github")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
