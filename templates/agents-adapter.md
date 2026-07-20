# homemade-claude-kit — agent conventions

## The documentation metamodel

This machine has the homemade-claude-kit skills installed (flat directory of `SKILL.md`
skills — Codex: `~/.codex/skills/`; OpenCode also discovers `~/.claude/skills` and
`.agents/skills`). The keystone is the **`metamodel` skill**: the canonical
strategic-architecture documentation stack — build order, artefact-type registry
(`references/artefact-types-registry.yaml` — parse it, don't guess ID formats or paths),
frontmatter schema, and open-items governance, plus Audit / Scaffold / Migrate modes.

**Before creating or editing any artefact under a project's `docs/`, read the `metamodel`
skill's references** (it is a sibling directory of every other installed skill). The
doc-producing skills (`business-*`, `spec-*`, `arch-*`, …) each point at the exact reference
files they need.

## Behavioural rules

The sections below are the kit's harness-agnostic working rules, concatenated verbatim from
`rules/` at install time.
