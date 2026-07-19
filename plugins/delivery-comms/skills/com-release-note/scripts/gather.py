#!/usr/bin/env python3
"""Gather the deterministic evidence bundle for a release note.

Read-only. Collects, for a tag range ``<since>..<until>``:

  * the ``CHANGELOG.md`` section for the release being noted,
  * the commit / merged-PR subjects, grouped by conventional-commit type
    (squash-merge subjects are the PR titles), and
  * pointers to the FBS + capability map (not deep-parsed here — the Curate
    step reads those to attribute entries to capabilities).

The output is a Markdown bundle written to ``--output`` (or stdout). Nothing in
the repository is mutated. ``git`` is required; ``gh`` is optional enrichment
(PR numbers/labels) and is skipped with a note if absent or unauthenticated.

Usage::

    python gather.py --since v1.1.0 --until v1.2.0 \\
        --changelog CHANGELOG.md \\
        --fbs docs/product-specs/07a-fbs.md \\
        --capability-map docs/business/03a-capability-map.md \\
        --output /tmp/release-1.2.0-bundle.md
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

# Conventional-commit types, in the order they should appear in the bundle.
_TYPE_ORDER = ["feat", "fix", "perf", "refactor", "build", "ci", "docs", "test", "style", "chore"]
_CONVENTIONAL_RE = re.compile(r"^(?P<type>[a-z]+)(?:\((?P<scope>[^)]*)\))?(?P<breaking>!)?:\s*(?P<desc>.+)$")


def _fail(message: str) -> None:
    """Print an explicit error to stderr and exit non-zero."""
    print(f"gather.py: {message}", file=sys.stderr)
    raise SystemExit(1)


def _run(cmd: list[str]) -> str:
    """Run a command and return stripped stdout, or raise CalledProcessError."""
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip()


def _require(tool: str) -> None:
    """Hard-fail with an actionable message if a required tool is absent."""
    if shutil.which(tool) is None:
        _fail(f"'{tool}' is required but not found on PATH. Install it and retry. This script never auto-installs.")


def _auto_since(until: str) -> str:
    """The most recent tag reachable before ``until`` (the previous release)."""
    try:
        return _run(["git", "describe", "--tags", "--abbrev=0", f"{until}^"])
    except subprocess.CalledProcessError:
        _fail(f"could not auto-derive --since (no tag before {until}). Pass --since explicitly.")
        return ""  # unreachable — _fail raises


def _commit_subjects(since: str, until: str) -> list[str]:
    """Commit subjects in the range, newest first (squash subjects == PR titles)."""
    try:
        out = _run(["git", "log", "--no-merges", "--format=%s (%h)", f"{since}..{until}"])
    except subprocess.CalledProcessError as exc:
        _fail(f"git log {since}..{until} failed — are both refs valid? ({exc.stderr.strip()})")
        return []  # unreachable
    return [line for line in out.splitlines() if line.strip()]


def _group_by_type(subjects: list[str]) -> dict[str, list[str]]:
    """Bucket subjects by conventional-commit type; unparseable ones go to 'other'."""
    groups: dict[str, list[str]] = defaultdict(list)
    for subject in subjects:
        match = _CONVENTIONAL_RE.match(subject)
        groups[match.group("type") if match else "other"].append(subject)
    return groups


def _changelog_section(path: Path, version: str) -> str | None:
    """Slice the CHANGELOG section whose header names ``version`` (v-prefix agnostic)."""
    if not path.is_file():
        return None
    needle = version.lstrip("v")
    lines = path.read_text(encoding="utf-8").splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith("## ") and needle in line:
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return "\n".join(lines[start:end]).strip()


def _pr_enrichment(since: str, base: str | None) -> str:
    """Optional gh-sourced merged-PR list since the prior tag; a note if gh is unavailable."""
    if shutil.which("gh") is None:
        return "_`gh` not on PATH — PR metadata is git-only (commit subjects above). Install gh for PR numbers/labels._"
    try:
        since_date = _run(["git", "log", "-1", "--format=%cs", since])
        cmd = ["gh", "pr", "list", "--state", "merged",
               "--search", f"merged:>={since_date}", "--limit", "200",
               "--json", "number,title,labels", "--template",
               "{{range .}}- #{{.number}} {{.title}}{{\"\\n\"}}{{end}}"]
        if base:  # optional: restrict to PRs merged into a specific base branch
            cmd[4:4] = ["--base", base]
        out = _run(cmd)
        return out or "_No merged PRs returned by gh for the range._"
    except subprocess.CalledProcessError as exc:
        return f"_gh enrichment skipped (not authenticated or errored): {exc.stderr.strip()}_"


def _build_bundle(since: str, until: str, changelog: str | None, groups: dict[str, list[str]],
                  pr_block: str, fbs: Path, capmap: Path) -> str:
    """Assemble the Markdown evidence bundle."""
    parts = [f"# Release evidence bundle: {since}..{until}", ""]

    parts += ["## Changelog section", ""]
    parts.append(changelog if changelog else f"_No CHANGELOG section found for {until}. Curate from commits below._")
    parts.append("")

    parts += ["## Commits / merged-PR subjects (by type)", ""]
    ordered = [t for t in _TYPE_ORDER if t in groups] + [t for t in groups if t not in _TYPE_ORDER]
    if not ordered:
        parts.append("_No commits in range._")
    for t in ordered:
        parts.append(f"### {t} ({len(groups[t])})")
        parts += [f"- {s}" for s in groups[t]]
        parts.append("")

    parts += ["## Merged PRs (gh enrichment)", "", pr_block, ""]

    parts += ["## Source artefacts (read during Curate — not parsed here)", ""]
    parts.append(f"- FBS: `{fbs}` {'(found)' if fbs.is_file() else '(MISSING — graceful-degrade path)'}")
    parts.append(f"- Capability map: `{capmap}` {'(found)' if capmap.is_file() else '(MISSING — graceful-degrade path)'}")
    parts.append("")
    return "\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Gather the evidence bundle for a release note (read-only).")
    parser.add_argument("--since", help="Previous release tag (default: most recent tag before --until).")
    parser.add_argument("--until", default="HEAD", help="Target release tag or ref (default: HEAD).")
    parser.add_argument("--changelog", default="CHANGELOG.md", type=Path, help="Path to the changelog.")
    parser.add_argument("--fbs", default=Path("docs/product-specs/07a-fbs.md"), type=Path, help="Path to the FBS.")
    parser.add_argument("--capability-map", default=Path("docs/business/03a-capability-map.md"), type=Path,
                        help="Path to the capability map.")
    parser.add_argument("--pr-base", help="Optional: restrict gh PR enrichment to this base branch (e.g. staging, main).")
    parser.add_argument("--output", type=Path, help="Write the bundle here (default: stdout).")
    args = parser.parse_args(argv)

    _require("git")
    since = args.since or _auto_since(args.until)

    subjects = _commit_subjects(since, args.until)
    groups = _group_by_type(subjects)
    changelog = _changelog_section(args.changelog, args.until)
    pr_block = _pr_enrichment(since, args.pr_base)
    bundle = _build_bundle(since, args.until, changelog, groups, pr_block, args.fbs, args.capability_map)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(bundle, encoding="utf-8")
        print(f"gather.py: wrote evidence bundle to {args.output} "
              f"({len(subjects)} commits, changelog {'found' if changelog else 'missing'}).")
    else:
        print(bundle)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
