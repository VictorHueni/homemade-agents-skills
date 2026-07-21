---
type: rule
paths:
  - "docs/**"
---

# Open Items Governance — pointer

The cross-cutting open-items contract — central ledger at `docs/project-control/open-items/`
as the sole authoring surface (ADR-0005), item taxonomy (`doc-gap` / `decision-gap` /
`execution-item` / `tech-debt`), lifecycle states, the canonical column schema, provenance
fields (`Source anchor` + `Source heading`), central-only rows, the pluggable
`markdown` | `github` backend (ADR-0002/0003), and the skill-conformance checklist — lives
at the **`metamodel` skill's `references/open-items-governance.md`** (a sibling skill
directory in flat installs).

Operate the ledger through the `util-open-items` skill. Inline `_TODO_` placeholders are NOT
open items. Read the contract before filing, closing, or auditing unresolved work (kit
ADR-0007).
