---
type: rule
paths:
  - "docs/**"
  - "rules/artefact-types-registry.md"
---

# Artefact Types Registry — pointer

The structural registry of every artefact type the kit mints — `id_format` regex, layout,
`default_path`, `review_interval`, the canonical `okf_type` display name written into each
artefact's `type:` frontmatter, and the canonical-slug contract — lives at the **`metamodel`
skill's `references/artefact-types-registry.yaml`** (a sibling skill directory in flat
installs).

Parse it deterministically (`python3 -c "import yaml; …"`) — never infer ID formats, paths,
or `okf_type` display names from memory. Skills emit `okf_type` values verbatim.

Structural facts are canonically owned by the **clew** repo (clew ADR-0008); the YAML is the
kit's projection — author new artefact types clew-side first (kit ADR-0007).
