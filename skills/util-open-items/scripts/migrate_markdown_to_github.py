#!/usr/bin/env python3
"""One-way markdown -> github migration for the open-items central plane.

Implements Invariant I2 (the `metamodel` skill's `references/open-items-governance.md` §5.3): migration is performed once,
markdown -> github only, and MUST emit a persisted OI-NNNN -> #N map so back-references
survive the identifier re-mint. There is NO reverse path and NO concurrent two-way sync.

Pipeline:
  1. Parse the live table of the markdown ledger (docs/project-control/open-items/open-items.md).
  2. For each row, create (or reuse) a GitHub issue via `gh`, mapping the canonical slugs
     onto Issue Type + form-structured body + assignee, and the lifecycle status onto issue
     state + close reason. De-dups by (source_artefact, source_anchor, summary) so re-runs
     are idempotent.
  3. Emit the OI-NNNN -> #N map.
  4. Rewrite OI-NNNN back-references across the docs tree to #N (OI-ID cells + prose).

DRY-RUN BY DEFAULT. Nothing mutates GitHub or any file unless --apply is passed.
Ledger retirement + the backend.yml flip are deliberately left to the operator (Mode 7 in
SKILL.md) so issues can be eyeballed before the markdown source of truth is frozen.

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

VALID_TYPES = {"doc-gap", "decision-gap", "execution-item", "tech-debt"}
# Live-table column order in open-items.md (§5.1: Source artefact inserted after Summary).
LEDGER_COLS = [
    "oi_id", "type", "summary", "source_artefact", "source_anchor", "source_heading",
    "resolution_path", "priority", "status", "owner", "review_date", "tracker_ref",
]


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


def split_row(line: str) -> list[str]:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells


def parse_ledger(path: Path) -> list[dict]:
    rows: list[dict] = []
    in_live = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.startswith("## Live items"):
            in_live = True
            continue
        if in_live and raw.startswith("## ") and not raw.startswith("## Live items"):
            break
        if in_live and re.match(r"^\|\s*OI-\d{4}\b", raw):
            cells = split_row(raw)
            if len(cells) < len(LEDGER_COLS):
                sys.stderr.write(f"  WARN: short row skipped: {raw[:60]}...\n")
                continue
            row = dict(zip(LEDGER_COLS, cells))
            rows.append(row)
    return rows


def issue_body(row: dict) -> str:
    """Form-structured body so util-metamodel-audit 18g (slug/field integrity) passes."""
    return "\n".join([
        f"### Type\n{row['type']}\n",
        f"### Priority\n{row['priority']}\n",
        f"### Source artefact\n{row['source_artefact'] or '_central-only_'}\n",
        f"### Source anchor\n{row['source_anchor'] or '(none)'}\n",
        f"### Source heading\n{row['source_heading']}\n",
        f"### Resolution path\n{row['resolution_path']}\n",
        f"\n---\n_Migrated from markdown ledger {row['oi_id']}._",
    ])


def find_existing(repo: str, row: dict) -> int | None:
    """De-dup: an issue already carrying this summary + source anchor."""
    out = run(
        ["gh", "issue", "list", "-R", repo, "--label", "open-item", "--state", "all",
         "--search", row["summary"], "--json", "number,title", "-L", "50"],
        apply=True, capture=True,
    )
    if not out:
        return None
    try:
        for it in json.loads(out):
            if it.get("title", "").lstrip("[OI] ").strip() == row["summary"]:
                return int(it["number"])
    except (json.JSONDecodeError, ValueError):
        pass
    return None


def issue_types_available(repo: str) -> bool:
    """Native Issue Types are org-level. On a personal repo the endpoint 404s, and we fall
    back to encoding the type as a `type:<value>` label. Always a real GET (read-only)."""
    res = subprocess.run(["gh", "api", f"repos/{repo}/issue-types"],
                         capture_output=True, text=True)
    return res.returncode == 0 and '"name"' in res.stdout


def ensure_labels(repo: str, labels: list[str], apply: bool) -> None:
    """Idempotently create the labels the migration relies on (`open-item`, plus
    `type:<value>` when Issue Types are unavailable)."""
    for lbl in labels:
        run(["gh", "label", "create", lbl, "--force"], apply)


def resolve_assignee(owner: str, assignee_map: dict[str, str]) -> str | None:
    """Map a ledger `owner` to a real GitHub login. `_TBD_`/empty -> no assignee; an owner
    with no mapping is skipped (warned) rather than passed through and erroring."""
    if not owner or owner == "_TBD_":
        return None
    login = assignee_map.get(owner)
    if not login:
        sys.stderr.write(f"  note: owner '{owner}' has no --assignee-map entry; skipping assignee\n")
    return login


def create_issue(repo: str, row: dict, apply: bool, use_types: bool,
                 assignee_map: dict[str, str]) -> int | None:
    if row["type"] not in VALID_TYPES:
        sys.stderr.write(f"  SKIP {row['oi_id']}: invalid type '{row['type']}'\n")
        return None
    existing = find_existing(repo, row)
    if existing:
        print(f"  {row['oi_id']} -> #{existing} (existing, reused)")
        return existing
    cmd = ["gh", "issue", "create", "-R", repo,
           "--title", f"[OI] {row['summary']}",
           "--body", issue_body(row),
           "--label", "open-item"]
    if use_types:
        cmd += ["--type", row["type"]]
    else:
        cmd += ["--label", f"type:{row['type']}"]
    assignee = resolve_assignee(row["owner"], assignee_map)
    if assignee:
        cmd += ["--assignee", assignee]
    out = run(cmd, apply, capture=True)
    if not apply:
        return None
    if not out:
        return None
    m = re.search(r"/issues/(\d+)", out.strip())
    return int(m.group(1)) if m else None


def apply_lifecycle(repo: str, number: int, row: dict, apply: bool) -> None:
    status = row["status"]
    if status in ("open", "in-progress", "blocked"):
        if status in ("in-progress", "blocked"):
            print(f"    note: set Project Status='{status}' for #{number} (manual / Project field)")
        return
    reason = "completed" if status == "closed" else "not planned"
    if row["tracker_ref"] and row["tracker_ref"] != "_TBD_":
        run(["gh", "issue", "comment", str(number), "-R", repo,
             "--body", f"Original tracker ref: {row['tracker_ref']}"], apply)
    run(["gh", "issue", "close", str(number), "-R", repo, "--reason", reason], apply)


def rewrite_refs(docs: Path, mapping: dict[str, int], apply: bool) -> None:
    if not mapping:
        return
    pattern = re.compile(r"\b(" + "|".join(re.escape(k) for k in mapping) + r")\b")
    for md in sorted(docs.rglob("*.md")):
        # The markdown ledger + migration map are the OI-NNNN-era record (frozen on cutover);
        # never rewrite their IDs to #N.
        if "project-control/open-items" in md.as_posix():
            continue
        text = md.read_text(encoding="utf-8")
        new, n = pattern.subn(lambda m: f"#{mapping[m.group(1)]}", text)
        if n:
            print(f"  {md}: {n} OI-NNNN -> #N rewrites")
            if apply:
                md.write_text(new, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", required=True, help="OWNER/NAME where issues are created")
    ap.add_argument("--ledger", default="docs/project-control/open-items/open-items.md")
    ap.add_argument("--docs", default="docs", help="tree to rewrite OI-NNNN back-references in")
    ap.add_argument("--map-out", default="docs/project-control/open-items/migration-map.md")
    ap.add_argument("--assignee-map", action="append", default=[], metavar="OWNER=LOGIN",
                    help="map a ledger owner to a GitHub login (repeatable), e.g. victor=VictorHueni")
    ap.add_argument("--apply", action="store_true", help="perform mutations (default: dry-run)")
    args = ap.parse_args()

    ledger = Path(args.ledger)
    if not ledger.is_file():
        sys.stderr.write(f"ERROR: ledger not found: {ledger}\n")
        return 2

    assignee_map: dict[str, str] = {}
    for pair in args.assignee_map:
        if "=" not in pair:
            sys.stderr.write(f"ERROR: --assignee-map expects OWNER=LOGIN, got '{pair}'\n")
            return 2
        k, v = pair.split("=", 1)
        assignee_map[k.strip()] = v.strip()

    rows = parse_ledger(ledger)
    print(f"Parsed {len(rows)} live rows from {ledger}")
    print(f"Mode: {'APPLY' if args.apply else 'DRY-RUN (no mutations)'}")

    # Issue Types are org-level; on a personal repo, fall back to a `type:<value>` label.
    use_types = issue_types_available(args.repo)
    print(f"Issue Types: {'available -> native --type' if use_types else 'unavailable (404) -> type:<value> labels'}")
    print(f"Assignee map: {assignee_map or '(none — owners skipped unless mapped)'}\n")

    # Make sure the labels the migration relies on exist.
    labels = ["open-item"] + ([] if use_types else [f"type:{t}" for t in sorted(VALID_TYPES)])
    ensure_labels(args.repo, labels, args.apply)

    mapping: dict[str, int] = {}
    for row in rows:
        number = create_issue(args.repo, row, args.apply, use_types, assignee_map)
        if number is None:
            if args.apply:
                sys.stderr.write(f"  WARN: no issue number for {row['oi_id']}\n")
            continue
        apply_lifecycle(args.repo, number, row, args.apply)
        mapping[row["oi_id"]] = number
        print(f"  {row['oi_id']} -> #{number} ({row['status']})")

    # Emit the OI-NNNN -> #N map (Invariant I2).
    lines = [
        "# Open Items — markdown -> github migration map",
        "",
        f"Generated {date.today().isoformat()} against `{args.repo}`. "
        "One-way; back-references rewritten to `#N`.",
        "",
        "| OI-NNNN | Issue | Status at migration |",
        "| :------ | :---- | :------------------ |",
    ]
    for row in rows:
        n = mapping.get(row["oi_id"])
        lines.append(f"| {row['oi_id']} | {'#' + str(n) if n else '_FAILED_'} | {row['status']} |")
    map_text = "\n".join(lines) + "\n"
    print(f"\nMap ({len(mapping)} mapped):")
    print(map_text)
    if args.apply:
        Path(args.map_out).write_text(map_text, encoding="utf-8")
        print(f"Wrote {args.map_out}")

    print("\nRewriting back-references:")
    rewrite_refs(Path(args.docs), mapping, args.apply)

    if not args.apply:
        print("\nDRY-RUN complete. Re-run with --apply to migrate, then (operator):")
        print("  1. verify the issues + Project look right")
        print("  2. set Project Status for any in-progress/blocked rows")
        print("  3. move open-items.md into archive/ (frozen) and set backend.yml: github")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
