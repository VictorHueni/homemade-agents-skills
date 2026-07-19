---
title: Metamodel Distribution as a Skill
status: draft
owner: Victor Hueni
last_reviewed: 2026-07-19
review_interval: 180d
---

# Metamodel Distribution as a Skill

Date: 2026-07-19

## Context and Problem Statement

The artefact/metamodel contract — build-order spine, artefact-type registry, frontmatter
schema, open-items governance — lives in `rules/*.md`, loaded through Claude Code's
`paths:`-scoped rules mechanism. That mechanism is Anthropic-proprietary: Codex and OpenCode
never see these rules, so the kit's most valuable content is invisible in two of the three
target harnesses.

Meanwhile clew [ADR-0008](https://github.com/VictorHueni/clew/blob/main/docs/architecture/decisions/adr-0008-clew-canonical-source-of-truth-for-metamodel.md)
made clew the canonical owner of the *structural + relational* metamodel, with the kit's
copies destined to become **generated projections** (`clew metamodel export`, Phase 4). Any
distribution design must respect that ownership: the kit distributes the metamodel, it does
not own it.

The question: **in what form does the metamodel travel so that all three harnesses receive
it, without creating a second authority?**

## Decision Drivers

- **SKILL.md is the one cross-harness content format** — read natively by Claude, Codex
  (`~/.codex/skills/`), and OpenCode (first-party discovery incl. `.claude/skills` /
  `.agents/skills`).
- **Ownership follows enforcement (clew ADR-0008)** — the kit ships projections, builds no
  parallel validator, authors no structural facts first.
- **Progressive disclosure** — description ambient, body on trigger, references on demand:
  the same loading economics `paths:` rules provided, but portable.
- **Self-containment** — the bundle must survive every distribution channel (flat symlinks,
  marketplace clone, plain git clone) without external path dependencies.
- **One copy of structural facts** — the audit/scaffold/migration procedures must be unable
  to drift from the registry.

## Considered Options

1. **A self-contained `metamodel` skill with lifecycle modes (chosen).**
2. **Keep rules + convert per harness** (generate AGENTS.md variants of the metamodel rules
   via rulesync or scripts). Rejected: always-loaded cost of ~2,100 rule lines in harnesses
   without conditional loading; no on-demand reference mechanism; still Claude-shaped at the
   source.
3. **Kit-side `registry.yaml` + CI validator as the neutral home.** Rejected: re-inverts
   clew ADR-0008 (kit becomes structural authority; validator duplicates clew's enforcement
   thesis).
4. **Wait for clew Phase 3/4 and distribute nothing meanwhile.** Rejected: portability is
   needed now; the interim hand-authored projection is explicitly sanctioned by ADR-0008
   Phase 2.

## Decision Outcome

Chosen option: **1**, with seven sub-decisions:

### 1. The skill

```
skills/metamodel/
  SKILL.md                     # build-order spine (from rules/metamodel.md) + mode dispatch
  references/
    metamodel-reference.md     # DAG, ER, per-step detail (from rules/)
    artefact-types-registry.yaml   # converted from markdown table — see §4
    artefact-frontmatter.md    # OKF-superset schema (from rules/)
    open-items-governance.md   # (from rules/)
    modes/
      audit.md                 # from util-metamodel-audit
      scaffold.md              # from util-metamodel-scaffold
      migrate.md               # from util-metamodel-migration
```

The frontmatter description triggers on **stack-level intents** ("build the documentation
stack", build-order / ID-format / artefact-placement questions, "audit my docs stack",
"scaffold the docs folder", "migrate my docs") — never on per-artefact intents, which the
producing skills own. Description ≤ 1024 chars (Codex loader limit).

### 2. Naming: bare `metamodel` — documented convention exception

The `<category>-<artifact>[-<verb>]` convention cannot contain this skill: the category
registry is itself *part of the metamodel* — a prefix for the thing that defines prefixes is
circular. With the lifecycle consolidation (§3) it is also the single skill for its artefact,
so verb suffixes drop per the convention's own rule. The exception is registered in
`rules/skill-creation-sync.md` alongside the `business-vision` path exception, with the
guard: **do not repeat without an ADR**. Rejected alternatives: `util-metamodel`
(undersells the keystone; `util-` = housekeeping), `core-metamodel` (a new category for one
skill), `clew-metamodel` (product branding in the kit's grammar).

### 3. Consolidation: lifecycle operations become modes

`util-metamodel-audit`, `util-metamodel-scaffold`, `util-metamodel-migration` retire as
standalone skills and become **Audit / Scaffold / Migrate modes** (procedures in
`references/modes/`). Modes read the skill's own registry, making structural-fact
duplication impossible by construction — the check-catalogue/detection-signals copies (the
worst "maintenance coupling" rows) are eliminated. The merged skill carries
`impact: "medium"` (Scaffold's Wire step writes `CLAUDE.md`). End state: modes become thin
wrappers over `clew audit` / `clew init` / `clew migrate` when the CLI lands.

### 4. Registry format: YAML

`artefact-types-registry` converts from a markdown table to
`references/artefact-types-registry.yaml` — one entry per artefact type (`okf_type`,
`display_name`, `minting_skill`, `id_format`, `layout`, `default_path`, `review_interval`,
`property_schema_ref`, `notes`). Rationale: it is row data, not prose; modes parse it
deterministically (`python3 -c "import yaml; …"`); it is projection-shaped for
`clew metamodel export`. **The schema is designed once as clew OI-0030's answer**: canonical
`metamodel.yaml` lives clew-side; the skill's file is a verbatim copy with a provenance
header naming clew as owner. Prose contracts (`artefact-frontmatter.md`,
`open-items-governance.md`) stay markdown. Structural content is labelled *"generated
projection (future — clew ADR-0008 Phase 4); do not hand-edit to diverge from clew
`docs/metamodel/`"*.

### 5. Reference convention: name-first

Skills reference the bundle **by skill name**: *"read the `metamodel` skill's
`references/<file>` (flat installs: a sibling directory of this skill)"*. Rationale: name
lookup resolves in every channel; a bare relative path (`../metamodel/`) fails across plugin
subtrees in the marketplace channel and under physical `..` resolution through per-skill
symlinks. Rejected alternatives: cross-plugin relative paths (inverted failure mode),
duplicating references into each plugin (drift factory).

### 6. The `rules/` split

Metamodel rules (`metamodel.md`, `artefact-frontmatter.md`, `artefact-types-registry.md`,
`open-items-governance.md`) shrink to **Claude pointer stubs**: `paths:` frontmatter kept
(ambient loading preserved in Claude), body = one routing paragraph to the skill.
`metamodel-reference.md` is deleted (no `paths:` loading to preserve). Harness-agnostic
behavioural rules (`working-style`, `git-and-tools`, `writing-citations`,
`diagramming-mermaid`, `frontend-nuxt`) remain full rules and feed the AGENTS.md adapter
(ADR-0006 §4).

### 7. Relationship to clew (ADR-0008)

This ADR implements the kit side of ADR-0008's interim state: the skill's structural
references are the **hand-authored projection** Phase 2 sanctions, flipping to
`clew metamodel export` output at Phase 4 (with a kit-side CI drift check). The kit builds
no parallel enforcement. Cross-repo actions filed at Plan-0002 increment 13: close clew
OI-0030 with the §4 schema; amend Phase-4 export scope to the multi-projection set (registry
YAML + skill references + AGENTS.md stubs).

### Positive Consequences

- The metamodel travels to all three harnesses in one format, with progressive disclosure
  intact; daily UX is unchanged (producing skills pull it in by name).
- One copy of structural facts, converging on zero hand-authored copies at clew Phase 4.
- Three fewer skills; the audit family can no longer lag the registry.

### Negative Consequences

- ~30 producing skills need their references repointed (mechanical, one sweep).
- Until clew Phase 4, the YAML projection is hand-synced against clew `docs/metamodel/`
  (same single maintainer; drift window accepted by ADR-0008's own phasing).
- Ambient enforcement outside Claude is weaker: no `paths:` equivalent in Codex/OpenCode —
  mitigated by the AGENTS.md routing block, closed structurally when clew validates at
  write time.
- A named convention exception exists; guarded by the "not without an ADR" rule.

## Open Items

Cross-repo items (clew OI-0030 closure, Phase-4 export scope) filed at Plan-0002
increment 13.
