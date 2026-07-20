#!/usr/bin/env python3
"""One-time execution-label backfill for repos already on the github backend pre-ADR-0009.

Repos migrated under the ADR-0008 contract carry the retired `open-item` marker label and
the governance-derived type labels (`type:doc-gap` / `type:decision-gap` /
`type:execution-item`), with `priority` trapped in issue bodies. This script remaps them
to the ADR-0009 contract (github-backend.md §2, §2a, §2b):

  1. Old type label -> new (§2a): type:doc-gap -> type:docs,
     type:decision-gap -> type:task, type:execution-item -> type:task
     (type:tech-debt is already canonical and stays).
  2. OPEN issues with no `priority:` label: parse the body's `### Priority` form section
     (legacy `**Priority:** x` bold style also accepted) -> priority:p0..p3;
     missing/unparseable -> priority:p2 with a WARN.
  3. OPEN issues with no readiness label -> add `needs-triage`.
  4. Remove the retired `open-item` marker.

Population: every issue carrying `open-item` (open AND closed — the label remap applies
to both; priority/readiness backfill only touches OPEN issues), plus any issue carrying
one of the old type labels.

DRY-RUN BY DEFAULT. Nothing mutates GitHub unless --apply is passed. Idempotent: a second
--apply run plans zero changes. Pass --delete-retired-labels (default off) to also delete
the retired label DEFINITIONS (open-item + the three old type labels) from the repo after
all issues are processed; in dry-run this prints what would be deleted.

--selftest runs the planning logic against embedded fixture issues offline (no gh, no
network) and exits 0/1 — the substitute for a live dry-run in sandboxed environments.

stdlib only; --apply requires the `gh` CLI authenticated against --repo.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

# §2a remap: old governance-derived type labels -> ADR-0009 standard vocabulary.
TYPE_REMAP = {
    "type:doc-gap": "type:docs",
    "type:decision-gap": "type:task",
    "type:execution-item": "type:task",
}
# Ledger priority word -> label (github-backend.md §2).
PRIORITY_LABEL = {
    "critical": "priority:p0",
    "high": "priority:p1",
    "medium": "priority:p2",
    "low": "priority:p3",
}
DEFAULT_PRIORITY_LABEL = "priority:p2"
READINESS_LABELS = {"needs-triage", "ready-for-agent", "needs-human"}
MARKER = "open-item"
# Label definitions --delete-retired-labels removes from the repo.
RETIRED_LABELS = [MARKER, "type:doc-gap", "type:decision-gap", "type:execution-item"]
# Labels used as population selectors.
POPULATION_LABELS = [MARKER, "type:doc-gap", "type:decision-gap", "type:execution-item"]


def run(cmd: list[str], apply: bool, capture: bool = False) -> str | None:
    """Run a command. In dry-run, print intent for mutating gh calls and skip them."""
    is_read = cmd[:2] in (["gh", "issue"], ["gh", "label"]) and any(
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


def label_names(issue: dict) -> set[str]:
    """`gh issue list --json labels` yields label objects; fixtures may use plain strings."""
    names = set()
    for lbl in issue.get("labels", []):
        names.add(lbl["name"] if isinstance(lbl, dict) else str(lbl))
    return names


def parse_priority(body: str) -> str | None:
    """Extract the ledger priority word from an issue body.

    Accepts both shapes found in the wild on pre-ADR-0009 repos:
      form-style   ### Priority\\n\\nhigh
      legacy bold  **Priority:** high
    Returns the lowercase word if it maps to a priority label, else None.
    """
    m = re.search(r"^###\s+Priority\s*\n+\s*\**([A-Za-z]+)\**\s*$",
                  body, re.MULTILINE | re.IGNORECASE)
    if not m:
        m = re.search(r"\*\*Priority:?\*\*:?\s*([A-Za-z]+)", body, re.IGNORECASE)
    if not m:
        return None
    word = m.group(1).strip().lower()
    return word if word in PRIORITY_LABEL else None


def plan_issue(issue: dict) -> tuple[set[str], set[str], list[str]]:
    """Compute (labels to add, labels to remove, warnings) for one issue. Pure planning —
    reads only the issue dict, mutates nothing; idempotent by construction (derives the
    plan from the labels currently present)."""
    labels = label_names(issue)
    is_open = str(issue.get("state", "")).upper() == "OPEN"
    add: set[str] = set()
    remove: set[str] = set()
    warns: list[str] = []

    # 1. Old type labels -> §2a vocabulary (open and closed alike).
    for old, new in TYPE_REMAP.items():
        if old in labels:
            remove.add(old)
            if new not in labels:
                add.add(new)

    if is_open:
        # 2. Priority backfill from the body when no priority: label exists.
        if not any(l.startswith("priority:") for l in labels):
            word = parse_priority(issue.get("body") or "")
            if word:
                add.add(PRIORITY_LABEL[word])
            else:
                warns.append(
                    f"issue #{issue['number']}: no parseable '### Priority' / "
                    f"'**Priority:**' in body — defaulting to {DEFAULT_PRIORITY_LABEL}")
                add.add(DEFAULT_PRIORITY_LABEL)
        # 3. Readiness default.
        if not labels & READINESS_LABELS:
            add.add("needs-triage")

    # 4. Strip the retired marker (open and closed alike).
    if MARKER in labels:
        remove.add(MARKER)

    return add, remove, warns


def fetch_population(repo: str) -> list[dict]:
    """All issues (open AND closed) carrying the marker or an old type label,
    de-duplicated by issue number."""
    seen: dict[int, dict] = {}
    for lbl in POPULATION_LABELS:
        out = run(["gh", "issue", "list", "-R", repo, "--state", "all",
                   "--label", lbl, "--json", "number,state,labels,body", "-L", "500"],
                  apply=True, capture=True)
        if not out:
            continue
        try:
            for issue in json.loads(out):
                seen[int(issue["number"])] = issue
        except (json.JSONDecodeError, KeyError, ValueError) as exc:
            sys.stderr.write(f"  WARN: could not parse gh output for label {lbl}: {exc}\n")
    return [seen[n] for n in sorted(seen)]


def delete_retired_labels(repo: str, apply: bool) -> None:
    """Delete the retired label DEFINITIONS from the repo (only meaningful after every
    issue has been remapped — run it via --delete-retired-labels on the final pass)."""
    out = run(["gh", "label", "list", "-R", repo, "--json", "name", "-L", "200"],
              apply=True, capture=True)
    existing = set()
    if out:
        try:
            existing = {l["name"] for l in json.loads(out)}
        except (json.JSONDecodeError, KeyError):
            pass
    for lbl in RETIRED_LABELS:
        if existing and lbl not in existing:
            print(f"  retired label already absent: {lbl}")
            continue
        run(["gh", "label", "delete", lbl, "-R", repo, "--yes"], apply)


# --- selftest fixtures: the planning logic exercised offline (no gh, no network). ---

SELFTEST_CASES: list[tuple[str, dict, set[str], set[str], bool]] = [
    # (name, issue, expected add, expected remove, warn expected)
    (
        "form-style open doc-gap",
        {"number": 10, "state": "OPEN",
         "labels": [{"name": "open-item"}, {"name": "type:doc-gap"}],
         "body": "### Type\ndoc-gap\n\n### Priority\n\nhigh\n\n### Source artefact\ndocs/x.md\n"},
        {"type:docs", "priority:p1", "needs-triage"},
        {"type:doc-gap", "open-item"},
        False,
    ),
    (
        "legacy bold open execution-item",
        {"number": 11, "state": "OPEN",
         "labels": [{"name": "open-item"}, {"name": "type:execution-item"}],
         "body": "Some summary.\n\n**Priority:** medium\n\n**Owner:** victor\n"},
        {"type:task", "priority:p2", "needs-triage"},
        {"type:execution-item", "open-item"},
        False,
    ),
    (
        "closed decision-gap (label remap only — no priority/readiness backfill)",
        {"number": 12, "state": "CLOSED",
         "labels": [{"name": "open-item"}, {"name": "type:decision-gap"}],
         "body": "### Priority\n\nhigh\n"},
        {"type:task"},
        {"type:decision-gap", "open-item"},
        False,
    ),
    (
        "already-migrated issue is a no-op",
        {"number": 13, "state": "OPEN",
         "labels": [{"name": "type:tech-debt"}, {"name": "priority:p1"},
                    {"name": "needs-triage"}],
         "body": "### Priority\n\nhigh\n"},
        set(),
        set(),
        False,
    ),
    (
        "open tech-debt with unparseable priority defaults to p2 + WARN",
        {"number": 14, "state": "OPEN",
         "labels": [{"name": "open-item"}, {"name": "type:tech-debt"}],
         "body": "No structured fields here at all.\n"},
        {"priority:p2", "needs-triage"},
        {"open-item"},
        True,
    ),
]


def selftest() -> int:
    failures = 0
    for name, issue, want_add, want_remove, want_warn in SELFTEST_CASES:
        add, remove, warns = plan_issue(issue)
        problems = []
        if add != want_add:
            problems.append(f"add: got {sorted(add)}, want {sorted(want_add)}")
        if remove != want_remove:
            problems.append(f"remove: got {sorted(remove)}, want {sorted(want_remove)}")
        if bool(warns) != want_warn:
            problems.append(f"warns: got {warns or 'none'}, want warn={want_warn}")
        if problems:
            failures += 1
            print(f"FAIL {name}")
            for p in problems:
                print(f"     {p}")
        else:
            print(f"ok   {name}")
    print(f"\nselftest: {len(SELFTEST_CASES) - failures}/{len(SELFTEST_CASES)} passed")
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", help="OWNER/NAME to backfill (required unless --selftest)")
    ap.add_argument("--apply", action="store_true",
                    help="perform mutations (default: dry-run)")
    ap.add_argument("--delete-retired-labels", action="store_true",
                    help="after processing, delete the retired label definitions "
                         "(open-item + old type labels) from the repo (default: off)")
    ap.add_argument("--selftest", action="store_true",
                    help="run the planning logic against embedded fixtures (offline) and exit")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.repo:
        ap.error("--repo is required unless --selftest is given")

    print(f"Mode: {'APPLY' if args.apply else 'DRY-RUN (no mutations)'}")
    issues = fetch_population(args.repo)
    print(f"Population: {len(issues)} issue(s) carrying "
          f"{' / '.join(POPULATION_LABELS)} on {args.repo}\n")

    changed = 0
    for issue in issues:
        add, remove, warns = plan_issue(issue)
        for w in warns:
            sys.stderr.write(f"  WARN: {w}\n")
        if not add and not remove:
            print(f"  #{issue['number']}: no-op (already migrated)")
            continue
        changed += 1
        plan = " ".join([f"+{l}" for l in sorted(add)] + [f"-{l}" for l in sorted(remove)])
        print(f"  #{issue['number']} [{issue['state'].lower()}]: {plan}")
        cmd = ["gh", "issue", "edit", str(issue["number"]), "-R", args.repo]
        if add:
            cmd += ["--add-label", ",".join(sorted(add))]
        if remove:
            cmd += ["--remove-label", ",".join(sorted(remove))]
        run(cmd, args.apply)

    print(f"\n{changed} issue(s) with planned changes; "
          f"{len(issues) - changed} already conformant.")

    if args.delete_retired_labels:
        print("\nRetired label definitions "
              f"({'deleting' if args.apply else 'DRY-RUN — would delete'}):")
        delete_retired_labels(args.repo, args.apply)
    else:
        print("\nRetired label definitions kept (pass --delete-retired-labels on the "
              "final pass to remove open-item + old type labels from the repo).")

    if not args.apply:
        print("\nDRY-RUN complete. Review the plan above, then re-run with --apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
