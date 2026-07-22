---
type: rule
paths:
  - "docs/**"
  - "rules/metamodel.md"
---

# Strategic Architecture Stack — pointer

The metamodel — build-order spine, variants, cross-doc linking rule, supporting-skill
catalogue, DAG, ER, canonical paths — is distributed by the **`metamodel` skill** (in flat
installs a sibling of every other kit skill; canonically `skills/metamodel/` in the kit).

Any work that builds, extends, audits, or navigates the documentation stack under `docs/`
starts there:

- **Spine, variants, agent workflow** — the `metamodel` skill's `SKILL.md`
- **DAG, ER, per-step process + verification, ID conventions, canonical path tree** —
  `references/metamodel-reference.md`
- **Per-type structural facts (id_format, layout, default_path, okf_type)** —
  `references/artefact-types-registry.yaml` (parse it; don't eyeball it)

Structural facts are canonically owned by the **clew** repo (clew ADR-0008); the skill ships
the projection. Do not restate metamodel content in this file — it is a pointer by design
(kit ADR-0007).
