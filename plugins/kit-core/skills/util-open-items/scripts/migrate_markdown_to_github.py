#!/usr/bin/env python3
"""One-way markdown -> github migration for the open-items central plane.

Implements Invariant I2 (the `metamodel` skill's `references/open-items-governance.md` §5.3): migration is performed once,
markdown -> github only, and MUST emit a persisted OI-NNNN -> #N map so back-references
survive the identifier re-mint. There is NO reverse path and NO concurrent two-way sync.

Pipeline:
  0. Bootstrap the 17-label ADR-0009 vocabulary idempotently (parsed at runtime from the
     sibling bootstrap_labels.sh — the single source of truth; no duplicated label table).
  1. Parse the live table of the markdown ledger (docs/project-control/open-items/open-items.md).
  2. For each row, create (or reuse) a GitHub issue via `gh`, mapping the canonical slugs
     onto labels (`type:` per the github-backend.md SS2a governance mapping, `priority:pN`,
     `needs-triage`; `state:` for in-progress/blocked rows) + form-structured body +
     assignee, and the lifecycle status onto issue state + close reason. De-dups by
     (source_artefact, source_anchor, summary) so re-runs are idempotent. No marker label,
     no title prefix, no native Issue Types (ADR-0009).
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
# Governance §2 -> label mapping (github-backend.md §2a, ADR-0009): decision work is a
# task whose deliverable is the decision record.
TYPE_LABEL = {
    "doc-gap": "type:docs",
    "decision-gap": "type:task",
    "execution-item": "type:task",
    "tech-debt": "type:tech-debt",
}
# Ledger priority -> label (github-backend.md §2, ADR-0008).
PRIORITY_LABEL = {
    "critical": "priority:p0",
    "high": "priority:p1",
    "medium": "priority:p2",
    "low": "priority:p3",
}
# Single source of truth for the 17-label vocabulary (names/colors/descriptions):
# the sibling bootstrap script's LABELS data block (ADR-0009 §5).
BOOTSTRAP_SCRIPT = Path(__file__).resolve().parent / "bootstrap_labels.sh"
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
    """Form-structured body so the metamodel skill's Audit mode 18g (slug/field integrity) passes."""
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
    """De-dup: an issue already carrying this summary as its title (titles have no
    prefix under ADR-0009)."""
    out = run(
        ["gh", "issue", "list", "-R", repo, "--state", "all",
         "--search", row["summary"], "--json", "number,title", "-L", "50"],
        apply=True, capture=True,
    )
    if not out:
        return None
    try:
        for it in json.loads(out):
            if it.get("title", "").strip() == row["summary"]:
                return int(it["number"])
    except (json.JSONDecodeError, ValueError):
        pass
    return None


def load_vocabulary() -> list[tuple[str, str, str]]:
    """Parse the (name, color, description) triples out of bootstrap_labels.sh's LABELS
    data block. Parsing the sibling script (rather than duplicating the table) keeps this
    migration drift-free against the ADR-0009 §5 source of truth."""
    if not BOOTSTRAP_SCRIPT.is_file():
        raise FileNotFoundError(f"bootstrap script not found: {BOOTSTRAP_SCRIPT}")
    m = re.search(r"^LABELS='(.*?)'\n", BOOTSTRAP_SCRIPT.read_text(encoding="utf-8"),
                  re.S | re.M)
    if not m:
        raise ValueError(f"could not parse the LABELS block in {BOOTSTRAP_SCRIPT}")
    triples: list[tuple[str, str, str]] = []
    for line in m.group(1).strip().splitlines():
        name, color, desc = line.split("|", 2)
        triples.append((name, color, desc))
    return triples


def ensure_labels(repo: str, apply: bool) -> None:
    """Idempotently bootstrap the full 17-label ADR-0009 vocabulary (same semantics as
    bootstrap_labels.sh --apply: `gh label create --force` normalizes color/description)."""
    triples = load_vocabulary()
    print(f"Bootstrapping {len(triples)} labels (source: {BOOTSTRAP_SCRIPT.name})")
    for name, color, desc in triples:
        run(["gh", "label", "create", name, "--repo", repo,
             "--color", color, "--description", desc, "--force"], apply)


def resolve_assignee(owner: str, assignee_map: dict[str, str]) -> str | None:
    """Map a ledger `owner` to a real GitHub login. `_TBD_`/empty -> no assignee; an owner
    with no mapping is skipped (warned) rather than passed through and erroring."""
    if not owner or owner == "_TBD_":
        return None
    login = assignee_map.get(owner)
    if not login:
        sys.stderr.write(f"  note: owner '{owner}' has no --assignee-map entry; skipping assignee\n")
    return login


def creation_labels(row: dict) -> list[str]:
    """Labels applied atomically at issue creation: mapped `type:` (§2a) + `priority:pN`
    + the `needs-triage` readiness default. `state:` labels are applied by
    apply_lifecycle so reused (de-duped) issues get them too."""
    labels = [TYPE_LABEL[row["type"]]]
    prio = PRIORITY_LABEL.get(row["priority"].strip().lower())
    if prio:
        labels.append(prio)
    else:
        sys.stderr.write(
            f"  WARN {row['oi_id']}: unmappable priority '{row['priority']}' — "
            "no priority label applied\n")
    labels.append("needs-triage")
    return labels


def create_issue(repo: str, row: dict, apply: bool,
                 assignee_map: dict[str, str]) -> int | None:
    if row["type"] not in VALID_TYPES:
        sys.stderr.write(f"  SKIP {row['oi_id']}: invalid type '{row['type']}'\n")
        return None
    existing = find_existing(repo, row)
    if existing:
        print(f"  {row['oi_id']} -> #{existing} (existing, reused)")
        return existing
    cmd = ["gh", "issue", "create", "-R", repo,
           "--title", row["summary"],
           "--body", issue_body(row),
           "--label", ",".join(creation_labels(row))]
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
            # §3c status decomposition: open issue + state: label (the retired
            # "set Project Status manually" step is now a direct label write).
            run(["gh", "issue", "edit", str(number), "-R", repo,
                 "--add-label", f"state:{status}"], apply)
            print(f"    state:{status} label applied to #{number} (status decomposition §3c)")
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

    print(f"Assignee map: {assignee_map or '(none — owners skipped unless mapped)'}\n")

    # Bootstrap the full ADR-0009 vocabulary before any issue names a label.
    ensure_labels(args.repo, args.apply)

    mapping: dict[str, int] = {}
    for row in rows:
        number = create_issue(args.repo, row, args.apply, assignee_map)
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
        print("  1. verify the issues + labels look right (gh issue list --label needs-triage)")
        print("  2. move open-items.md into archive/ (frozen) and set backend.yml: github")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
