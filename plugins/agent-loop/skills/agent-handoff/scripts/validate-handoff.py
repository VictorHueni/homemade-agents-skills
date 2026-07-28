#!/usr/bin/env python3
"""Validate a handoff document against the agent-handoff template contract.

Used both as create mode's write-time gate and as the eval grader (constraint 7 of
Plan-0004). Exit 0: valid. Exit 1: one finding per line, printed to stderr.
"""

import argparse
import re
import sys

REQUIRED_SECTIONS = [
    "Goal",
    "Approach & key decisions",
    "State",
    "Files",
    "Verification",
    "Dead ends — do not retry",
    "Constraints & gotchas",
    "Suggested skills",
    "Next step",
]

TRIVIALLY_EMPTY = {"", "none", "none.", "none identified", "n/a"}

PLACEHOLDER_PATTERNS = [
    re.compile(r"_TODO_"),
    re.compile(r"\bTBD\b"),
    re.compile(r"\bTODO:"),
    re.compile(r"\bPLACEHOLDER\b", re.IGNORECASE),
]

IMPERATIVE_VERBS = {
    "run", "fix", "add", "update", "write", "check", "verify", "read",
    "implement", "finish", "remove", "investigate", "test", "create",
    "review", "confirm", "debug", "refactor", "reproduce", "rerun",
    "re-run", "continue", "resume", "open", "close", "merge", "revert",
    "apply", "install", "configure", "deploy", "look", "reduce", "wire",
    "replace", "extend", "validate", "delete", "rename", "move", "rotate",
}

SECRET_PATTERNS = [
    ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("GitHub token", re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}")),
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    (
        "inline password/api_key value",
        re.compile(r"(?i)\b(password|api_key)\s*=\s*['\"]?[^\s'\"]{6,}"),
    ),
]


def find_sections(lines):
    """Map each required '## ' header to its (start, end) line-index span."""
    indices = [i for i, line in enumerate(lines) if line.startswith("## ")]
    sections = {}
    for pos, idx in enumerate(indices):
        name = lines[idx][3:].strip()
        end = indices[pos + 1] if pos + 1 < len(indices) else len(lines)
        sections[name] = (idx, end)
    return sections


def check_header(lines, findings):
    header = "\n".join(lines[:15])
    if not re.search(r"\*\*Date:\*\*\s*\d{4}-\d{2}-\d{2}", header):
        findings.append("header missing '**Date:** YYYY-MM-DD'")
    if not re.search(r"\*\*Branch:\*\*\s*\S+", header):
        findings.append("header missing '**Branch:** <name>'")
    sha_match = re.search(r"\*\*HEAD sha:\*\*\s*([0-9a-f]+)", header)
    if not sha_match:
        findings.append("header missing '**HEAD sha:** <40-char sha>'")
    elif len(sha_match.group(1)) != 40:
        findings.append(
            f"header HEAD sha is {len(sha_match.group(1))} chars, expected 40"
        )


def check_sections(lines, findings):
    sections = find_sections(lines)
    for name in REQUIRED_SECTIONS:
        if name not in sections:
            findings.append(f"missing section: ## {name}")
            continue
        start, end = sections[name]
        body = "\n".join(lines[start + 1 : end]).strip()
        normalized = body.lower().strip(" .")
        if name == "Dead ends — do not retry":
            if not body:
                findings.append(
                    f"section '{name}' is empty (use the literal 'none' if nothing "
                    "was tried)"
                )
        elif normalized in TRIVIALLY_EMPTY:
            findings.append(f"section '{name}' is trivially empty")
    return sections


def check_line_budget(lines, max_lines, findings):
    if len(lines) > max_lines:
        findings.append(f"document is {len(lines)} lines, exceeds --max-lines {max_lines}")


def check_placeholders(lines, findings):
    for i, line in enumerate(lines, start=1):
        for pattern in PLACEHOLDER_PATTERNS:
            if pattern.search(line):
                findings.append(f"line {i}: placeholder marker found: {line.strip()}")


def check_next_step(lines, sections, findings):
    if "Next step" not in sections:
        return
    start, end = sections["Next step"]
    body_lines = [line for line in lines[start + 1 : end] if line.strip()]
    if not body_lines:
        return
    first_word = re.match(r"[A-Za-z-]+", body_lines[0].strip())
    if not first_word or first_word.group(0).lower() not in IMPERATIVE_VERBS:
        findings.append(
            "'Next step' does not start with a recognized imperative verb: "
            f"{body_lines[0].strip()!r}"
        )


def check_secrets(lines, findings):
    for i, line in enumerate(lines, start=1):
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                findings.append(f"line {i}: possible {label}: {line.strip()}")


def main():
    parser = argparse.ArgumentParser(description="Validate an agent-handoff document.")
    parser.add_argument("path")
    parser.add_argument("--max-lines", type=int, default=200)
    args = parser.parse_args()

    with open(args.path, encoding="utf-8") as f:
        lines = f.read().splitlines()

    findings = []
    check_header(lines, findings)
    sections = check_sections(lines, findings)
    check_line_budget(lines, args.max_lines, findings)
    check_placeholders(lines, findings)
    check_next_step(lines, sections, findings)
    check_secrets(lines, findings)

    if findings:
        for finding in findings:
            print(finding, file=sys.stderr)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
