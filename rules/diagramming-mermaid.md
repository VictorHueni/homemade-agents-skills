---
type: rule
paths:
  - "docs/architecture/**"
  - "docs/business/**"
---

# Mermaid diagrams (GitHub renderer)

GitHub's embedded Mermaid parser is stricter than the standalone Mermaid CLI. Diagrams that render locally can fail on GitHub with "Unable to render rich display / Parse error on line N."

## Flowcharts (`flowchart TD`, `flowchart LR`)

Quote any label containing `<br/>`, apostrophes, parens, colons, commas, or non-alphanumeric punctuation:

| Risky pattern | Fix |
|---|---|
| `Node[Foo<br/>Bar]` | `Node["Foo<br/>Bar"]` |
| `Diamond{Foo<br/>Bar?}` | `Diamond{"Foo<br/>Bar?"}` |
| `\|line1<br/>line2\|` (edge label) | `\|"line1<br/>line2"\|` |
| `Node[insurer's text]` (apostrophe) | `Node["insurer's text"]` |
| Labels with parens, colons, commas, special chars | `Node["text (etc)"]` |

## Sequence diagrams (`sequenceDiagram`)

Different grammar — quote-wrapping does not help. Rephrase the message text:

| Risky pattern in message | Fix |
|---|---|
| `A->>B: text1; text2` (semicolons) | Replace `;` with `+`, `and`, or `—` |
| `A->>B: (informal) text...` (leading parens) | Move qualifier inside the sentence |
| Curly braces `{...}` in message text | Replace with brackets or rephrase |

`Note over` / `Note left of` / `Note right of` blocks: `<br/>` works without quotes.

## Library choice

Stay with Mermaid (GitHub-native). PlantUML / D2 / GraphViz require pre-generated SVG/PNG and lose the diff-friendly text-source advantage.

## Mobile rendering

The GitHub mobile app (iOS + Android) does NOT render Mermaid — it shows source as a code block. Use a mobile browser instead.

## Diagnostic shortcuts

- "Parse error … Expecting SOLID_OPEN_ARROW / DOTTED_OPEN_ARROW" → sequence-diagram message-text issue (semicolon or leading paren).
- "got NEWLINE" / "got STR" → flowchart label-quoting issue.

## Pre-commit audit

```bash
# Flowcharts: any unquoted <br/> in node labels, edge labels, diamonds?
grep -nE '\|[^"|]*<br/?>[^"|]*\||\[[^"][^]]*<br/?>[^]]*\]|\{[^"{}]*<br/?>[^"{}]*\}' file.md
# Sequence diagrams: any semicolons or leading parens in messages?
grep -nE '->>|-->>' file.md | grep -E ': .*;|: \('
```
