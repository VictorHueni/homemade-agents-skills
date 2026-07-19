#!/usr/bin/env python3
"""Generate .vale/styles/Local/GlossaryAliases.yml from the project glossary.

Reads GT-NN entries, extracts deprecated aliases, and emits a Vale
substitution rule so Vale flags alias usage and suggests the canonical term.

Glossary entry format expected:
    #### {Term} · BC-NN.GT-NN
    ...
    **Aliases (deprecated):** *Alias1*, Alias2 (qualifier) — explanation text

The GLOSSARY path below points to the homemade-claude-kit convention
(docs/domain/02c-glossary.md). Override GLOSSARY at the top of this file if
your project uses a different glossary path.
"""

import re
import sys
from pathlib import Path

GLOSSARY = Path("docs/domain/02c-glossary.md")
OUT = Path(".vale/styles/Local/GlossaryAliases.yml")


def extract_aliases(aliases_line: str) -> list[str]:
    """Extract alias terms from an 'Aliases (deprecated):' line.

    Handles three formats seen in project glossaries:
    - *Italic alias* (optional qualifier) — explanation
    - Plain ALIAS — explanation
    - _(none)_
    """
    if re.match(r"\s*_\(none\)_", aliases_line):
        return []
    # Drop everything after the first em-dash (explanation text)
    aliases_part = re.split(r"\s+[—–]\s+", aliases_line, maxsplit=1)[0]
    result = []
    for item in aliases_part.split(","):
        item = item.strip()
        if not item:
            continue
        # Prefer the italic-wrapped term (*alias*) if present
        italic = re.match(r"\*([^*]+)\*", item)
        if italic:
            alias = italic.group(1).strip()
        else:
            # Plain text alias — strip trailing parenthetical qualifier e.g. (DE), (FR)
            alias = re.sub(r"\s*\([^)]+\)\s*$", "", item).strip()
        if alias and not alias.startswith("_"):
            result.append(alias)
    return result


if not GLOSSARY.exists():
    print("No glossary found — skipping alias rule generation.")
    sys.exit(0)

content = GLOSSARY.read_text(encoding="utf-8")
# Each term entry starts with #### heading
blocks = re.split(r"\n#### ", content)
pairs: list[tuple[str, str]] = []

for block in blocks:
    # Match: "Term Name · BC-01.GT-05"
    heading = re.match(r"(.+?)\s+·\s+BC-\d+\.GT-\d+", block)
    if not heading:
        continue
    canonical = heading.group(1).strip()

    aliases_match = re.search(r"\*\*Aliases \(deprecated\):\*\*\s*(.+)", block)
    if not aliases_match:
        continue
    for alias in extract_aliases(aliases_match.group(1)):
        pairs.append((alias.lower(), canonical))

OUT.parent.mkdir(parents=True, exist_ok=True)

if not pairs:
    # Write an inert stub so Vale doesn't error on missing Local style
    OUT.write_text(
        "extends: existence\n"
        "message: \"Deprecated alias found.\"\n"
        "level: warning\n"
        "tokens: []\n",
        encoding="utf-8",
    )
    print("No deprecated aliases in glossary — wrote inert stub.")
    sys.exit(0)

lines = [
    "extends: substitution",
    "message: \"Use '%s' instead of '%s'.\",",
    "level: warning",
    "ignorecase: true",
    "swap:",
]
for alias, canonical in pairs:
    key = f'"{alias}"' if any(c in alias for c in " :-/()") else alias
    lines.append(f"  {key}: {canonical}")

OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Generated {OUT} with {len(pairs)} alias substitution(s).")
