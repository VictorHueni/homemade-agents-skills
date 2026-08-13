#!/usr/bin/env python3
"""One-way markdown -> github migration for delivery-roadmap epic identity.

Implements ADR-0010's epic-side mapping (references/github-backend.md). Migration is
performed once, markdown -> github only, and MUST emit a persisted E-NN -> #N map. Runs
SECOND, after spec-functional-breakdown-structure's own migrate script -- epics attach
functionality issues as sub-issues, so those issues must already exist.

Pipeline:
  0. Bootstrap the `type:epic` label idempotently.
  1. Parse `docs/plans/delivery-roadmap.md`'s per-epic sections: ID, name, Phase, and the
     FBS-scope C-N.M.FXX list.
  2. Load the FBS migration map (docs/product-specs/migration-map.md) to resolve each scope
     entry to its issue number. An unresolved entry is a warning, not a hard failure --
     migrate FBS fully first (SKILL.md Mode 3 prerequisite).
  3. For each epic, create (or reuse, matched by an idempotency marker -- unlike Mode 2's
     interactive proposal, this migrate mode is meant to be safely re-run, so it carries one)
     an issue titled with the epic name, label `type:epic`, then attach every resolved
     functionality issue as a native sub-issue via the `addSubIssue` GraphQL mutation (the
     `gh` CLI has no sub-issue subcommand).
  4. Emit the E-NN -> #N map.
  5. Rewrite E-NN back-references across the docs tree to #N.

DRY-RUN BY DEFAULT. Nothing mutates GitHub or any file unless --apply is passed.
delivery-roadmap.md retirement + the backend.yml flip are left to the operator (Mode 3 in
SKILL.md), same posture as util-open-items' Mode 7 and the FBS migrate script.

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

EPIC_HEADING_RE = re.compile(r"^###\s+(E-\d+)\s+·\s+(.+?)\s*$")
PHASE_RE = re.compile(r"^\*\*Phase:\*\*\s*Phase\s*(\d+)\s*$")
FBS_SCOPE_ROW_RE = re.compile(r"^\|\s*(C\d+(?:\.\d+)+\.F\d+)\s*\|")
MAP_ROW_RE = re.compile(r"^\|\s*(C\d+(?:\.\d+)+\.F\d+)\s*\|\s*(#\d+|_FAILED_)\s*\|")
PLACEHOLDER_NAME_RE = re.compile(r"^\[.*\]$|^…$")


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


def parse_roadmap(path: Path) -> list[dict]:
    epics: list[dict] = []
    current: dict | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        epic_m = EPIC_HEADING_RE.match(raw)
        if epic_m:
            eid, name = epic_m.groups()
            if PLACEHOLDER_NAME_RE.match(name):
                current = None  # template skeleton row -- skip its body too
                continue
            current = {"id": eid, "name": name, "phase": None, "fbs_scope": []}
            epics.append(current)
            continue
        if current is None:
            continue
        phase_m = PHASE_RE.match(raw.strip())
        if phase_m:
            current["phase"] = int(phase_m.group(1))
            continue
        scope_m = FBS_SCOPE_ROW_RE.match(raw)
        if scope_m:
            current["fbs_scope"].append(scope_m.group(1))
    return epics


def load_fbs_map(path: Path) -> dict[str, int]:
    mapping: dict[str, int] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        m = MAP_ROW_RE.match(raw)
        if not m:
            continue
        fid, issue = m.groups()
        if issue == "_FAILED_":
            sys.stderr.write(f"  WARN: {fid} failed FBS migration -- excluded from any epic\n")
            continue
        mapping[fid] = int(issue.lstrip("#"))
    return mapping


def marker(row: dict) -> str:
    return f"<!-- roadmap-seed: {row['id']} -->"


def resolved_body(row: dict, unresolved: list[str]) -> str:
    lines = [row["name"]]
    if row["phase"] is not None:
        lines.append(f"Phase: {row['phase']}")
    if unresolved:
        lines.append(
            f"Unresolved FBS scope (not attached as sub-issues, migrate FBS first): "
            f"{', '.join(unresolved)}"
        )
    return "\n".join(lines)


def find_existing(repo: str, row: dict) -> int | None:
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


def create_epic(repo: str, row: dict, unresolved: list[str], apply: bool) -> int | None:
    existing = find_existing(repo, row)
    if existing:
        print(f"  {row['id']} -> #{existing} (existing, reused)")
        return existing
    full_body = f"{resolved_body(row, unresolved)}\n\n{marker(row)}"
    cmd = ["gh", "issue", "create", "-R", repo,
           "--title", row["name"],
           "--body", full_body,
           "--label", "type:epic"]
    out = run(cmd, apply, capture=True)
    if not apply or not out:
        return None
    m = re.search(r"/issues/(\d+)", out.strip())
    return int(m.group(1)) if m else None


def issue_node_id(repo: str, number: int) -> str | None:
    """Read-only GraphQL lookup -- always executes, dry-run or not, same posture as
    find_existing (reads are safe; only addSubIssue itself is gated by --apply)."""
    owner, name = repo.split("/", 1)
    query = (
        "query($owner:String!,$name:String!,$number:Int!){"
        "repository(owner:$owner,name:$name){issue(number:$number){id}}}"
    )
    out = run(
        ["gh", "api", "graphql", "-f", f"query={query}",
         "-F", f"owner={owner}", "-F", f"name={name}", "-F", f"number={number}"],
        apply=True, capture=True,
    )
    if not out:
        return None
    try:
        return json.loads(out)["data"]["repository"]["issue"]["id"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return None


def add_sub_issue(repo: str, epic_number: int, child_number: int, apply: bool) -> None:
    epic_id = issue_node_id(repo, epic_number)
    child_id = issue_node_id(repo, child_number)
    if not epic_id or not child_id:
        sys.stderr.write(
            f"  WARN: could not resolve node IDs for #{epic_number}/#{child_number} "
            "-- sub-issue not attached\n"
        )
        return
    mutation = (
        "mutation($issueId:ID!,$subIssueId:ID!){"
        "addSubIssue(input:{issueId:$issueId,subIssueId:$subIssueId}){issue{number}}}"
    )
    run(
        ["gh", "api", "graphql", "-f", f"query={mutation}",
         "-F", f"issueId={epic_id}", "-F", f"subIssueId={child_id}"],
        apply,
    )
    print(f"    #{child_number} attached as sub-issue of #{epic_number}")


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
            print(f"  {md}: {n} E-NN -> #N rewrites")
            if apply:
                md.write_text(new, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", required=True, help="OWNER/NAME where issues are created")
    ap.add_argument("--roadmap", default="docs/plans/delivery-roadmap.md")
    ap.add_argument("--fbs-map", default="docs/product-specs/migration-map.md",
                     help="the map spec-functional-breakdown-structure's migrate script wrote")
    ap.add_argument("--docs", default="docs", help="tree to rewrite E-NN back-references in")
    ap.add_argument("--map-out", default="docs/plans/migration-map.md")
    ap.add_argument("--apply", action="store_true", help="perform mutations (default: dry-run)")
    args = ap.parse_args()

    roadmap = Path(args.roadmap)
    fbs_map_path = Path(args.fbs_map)
    if not roadmap.is_file():
        sys.stderr.write(f"ERROR: roadmap doc not found: {roadmap}\n")
        return 2
    if not fbs_map_path.is_file():
        sys.stderr.write(
            f"ERROR: FBS migration map not found: {fbs_map_path}\n"
            "        Run spec-functional-breakdown-structure's migrate script first -- "
            "epics attach functionality issues that must already exist.\n"
        )
        return 2

    epics = parse_roadmap(roadmap)
    fbs_map = load_fbs_map(fbs_map_path)
    print(f"Parsed {len(epics)} epics from {roadmap}")
    print(f"Loaded {len(fbs_map)} functionality mappings from {fbs_map_path}")
    print(f"Mode: {'APPLY' if args.apply else 'DRY-RUN (no mutations)'}\n")

    run(["gh", "label", "create", "type:epic", "--repo", args.repo,
         "--color", "5319e7", "--description", "Delivery epic (github backend)",
         "--force"], args.apply)

    mapping: dict[str, int] = {}
    for epic in epics:
        resolved = [fbs_map[fid] for fid in epic["fbs_scope"] if fid in fbs_map]
        unresolved = [fid for fid in epic["fbs_scope"] if fid not in fbs_map]
        if unresolved:
            sys.stderr.write(f"  WARN {epic['id']}: unresolved FBS scope {unresolved}\n")

        number = create_epic(args.repo, epic, unresolved, args.apply)
        if number is None:
            if args.apply:
                sys.stderr.write(f"  WARN: no issue number for {epic['id']}\n")
            continue
        mapping[epic["id"]] = number
        print(f"  {epic['id']} -> #{number} (phase {epic['phase']}, {len(resolved)} functionalities)")

        for child in resolved:
            add_sub_issue(args.repo, number, child, args.apply)

    lines = [
        "# Delivery roadmap — markdown -> github migration map",
        "",
        f"Generated {date.today().isoformat()} against `{args.repo}`. "
        "One-way; back-references rewritten to `#N`. Frozen once written -- never edited "
        "after the roadmap doc is archived.",
        "",
        "| E-NN | Issue | Phase |",
        "| :--- | :---- | :---- |",
    ]
    for epic in epics:
        n = mapping.get(epic["id"])
        lines.append(f"| {epic['id']} | {'#' + str(n) if n else '_FAILED_'} | {epic['phase']} |")
    map_text = "\n".join(lines) + "\n"
    print(f"\nMap ({len(mapping)} mapped):")
    print(map_text)
    if args.apply:
        Path(args.map_out).write_text(map_text, encoding="utf-8")
        print(f"Wrote {args.map_out}")

    print("\nRewriting back-references:")
    rewrite_refs(Path(args.docs), mapping, args.apply, skip="plans/migration-map.md")

    if not args.apply:
        print("\nDRY-RUN complete. Re-run with --apply to migrate, then (operator):")
        print("  1. verify epics + sub-issue hierarchy (gh issue view <epic> --json subIssuesSummary)")
        print("  2. archive docs/plans/delivery-roadmap.md (frozen snapshot) and set backend.yml: github")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
