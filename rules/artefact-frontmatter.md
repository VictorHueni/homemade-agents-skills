---
paths:
  - "docs/**"
---

# Artefact Frontmatter Convention — pointer

Every markdown file a kit skill writes under `docs/` must open with the standard OKF-superset
frontmatter block. The canonical schema — the six OKF fields (`type`, `title`, `description`,
`resource`, `tags`, `timestamp`) + kit lifecycle fields (`status`, `owner`, `last_reviewed`,
`review_interval`, supersession pair), the README/`index.md`/`log.md` exemptions and reserved
files, field rules, and default review intervals — lives at the **`metamodel` skill's
`references/artefact-frontmatter.md`** (a sibling skill directory in flat installs).

The `type:` value comes verbatim from the registry's `okf_type` field
(`references/artefact-types-registry.yaml`). Read the schema before writing any `docs/**`
artefact — do not restate or improvise it (kit ADR-0007).
