#!/usr/bin/env python3
"""Gather the deterministic evidence bundle for a release note.

Read-only. Collects, for a tag range ``<since>..<until>``:

  * the breaking changes detected in the range — commits carrying a `!` type
    marker or a ``BREAKING CHANGE:`` footer — surfaced first so they cannot be
    scrolled past (detection only; the curator still writes the note),
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
# Conventional Commits allows either spelling of the breaking footer token.
_BREAKING_FOOTER_RE = re.compile(r"^BREAKING[ -]CHANGE:\s*(?P<desc>.*)$")
_FOOTER_TOKEN_RE = re.compile(r"^[A-Za-z][A-Za-z-]*:\s")
_RECORD_SEP = "\x1e"


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


def _commits(since: str, until: str) -> list[tuple[str, str]]:
    """(subject-with-hash, body) per commit in the range, newest first.

    Bodies are read, not just subjects, so ``BREAKING CHANGE:`` footers are
    visible to breaking-change detection. Records are separated by an ASCII
    record separator, which cannot occur in commit text.
    """
    try:
        out = _run(["git", "log", "--no-merges",
                    f"--format={_RECORD_SEP}%s (%h)%n%b", f"{since}..{until}"])
    except subprocess.CalledProcessError as exc:
        _fail(f"git log {since}..{until} failed — are both refs valid? ({exc.stderr.strip()})")
        return []  # unreachable
    commits = []
    for record in out.split(_RECORD_SEP):
        lines = record.strip("\n").splitlines()
        if lines and lines[0].strip():
            commits.append((lines[0].strip(), "\n".join(lines[1:])))
    return commits


def _breaking_footers(body: str) -> list[str]:
    """Text of each BREAKING CHANGE / BREAKING-CHANGE footer, wrapped lines joined."""
    found, lines, i = [], body.splitlines(), 0
    while i < len(lines):
        match = _BREAKING_FOOTER_RE.match(lines[i])
        if not match:
            i += 1
            continue
        parts, i = [match.group("desc").strip()], i + 1
        while i < len(lines) and lines[i].strip() and not _FOOTER_TOKEN_RE.match(lines[i]):
            parts.append(lines[i].strip())
            i += 1
        found.append(" ".join(p for p in parts if p))
    return found


def _breaking_entries(commits: list[tuple[str, str]]) -> list[str]:
    """Commits flagged breaking by a `!` type marker or a BREAKING CHANGE footer.

    Detection only — the curator still decides what reaches the note's
    `## Breaking changes` section and how it is worded for the reader.
    """
    entries = []
    for subject, body in commits:
        reasons = []
        match = _CONVENTIONAL_RE.match(subject)
        if match and match.group("breaking"):
            reasons.append("`!` marker")
        reasons += [f"BREAKING CHANGE: {text}" if text else "BREAKING CHANGE (no description)"
                    for text in _breaking_footers(body)]
        if reasons:
            entries.append(f"- {subject}\n  - " + "\n  - ".join(reasons))
    return entries


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
                  breaking: list[str], pr_block: str, fbs: Path, capmap: Path) -> str:
    """Assemble the Markdown evidence bundle."""
    parts = [f"# Release evidence bundle: {since}..{until}", ""]

    # First, so a breaking change cannot be missed by scrolling.
    parts += ["## Breaking changes (detected from commits)", ""]
    if breaking:
        parts += breaking + [""]
        parts += ["_Detection only — decide per entry what the reader must do, and write it into "
                  "the note's `## Breaking changes` section._", ""]
    else:
        parts += ["_No `!` markers or BREAKING CHANGE footers in range. "
                  "Check the changelog section below before concluding there are none._", ""]

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

    commits = _commits(since, args.until)
    subjects = [subject for subject, _ in commits]
    groups = _group_by_type(subjects)
    breaking = _breaking_entries(commits)
    changelog = _changelog_section(args.changelog, args.until)
    pr_block = _pr_enrichment(since, args.pr_base)
    bundle = _build_bundle(since, args.until, changelog, groups, breaking, pr_block,
                           args.fbs, args.capability_map)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(bundle, encoding="utf-8")
        print(f"gather.py: wrote evidence bundle to {args.output} "
              f"({len(subjects)} commits, {len(breaking)} breaking, "
              f"changelog {'found' if changelog else 'missing'}).")
    else:
        print(bundle)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
