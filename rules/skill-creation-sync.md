---
paths:
  - "skills/**"
  - ".claude/skills/**"
---

# Skill creation and cross-machine sync workflow

How to create a new Claude skill, publish it to `homemade-claude-kit`, and make it available globally via dotfiles/chezmoi.

## Where new skills live

New skills belong in `<KIT_DIR>/skills/<skill-name>/SKILL.md` (with optional `references/` and `scripts/` subdirs). All skill folders live under `skills/`; the repo root holds only `install.sh`, `README.md`, and the non-skill dirs `commands/`, `rules/`, `docs/`, `scripts/`, `var/`.

**Finding the kit:** `homemade-claude-kit` is always a sibling of the current project — the parent folder name varies by machine (`projets/` vs `projects/`). Derive it reliably from the current git root:

```bash
KIT_DIR="$(dirname "$(git rev-parse --show-toplevel)")/homemade-claude-kit"
```

## Standard skill structure

```
<KIT_DIR>/skills/<skill-name>/
  SKILL.md              # required — YAML frontmatter + Claude-facing instructions
  references/           # optional — markdown content the skill loads on demand
  scripts/              # optional — runtime helpers
  templates/            # optional — output templates
```

## Naming convention (canonical)

Skill folder name + `name:` frontmatter field must follow this exact pattern:

```
<category>-<artifact-singular>[-<verb>]
```

**Core principle:** for doc-producing skills, **the category prefix names the output folder under `docs/`**. For non-doc skills (utilities), the category prefix names the function.

### Categories (pick exactly one — required)

| Category | Maps to output folder | Examples |
|---|---|---|
| `business-` | `docs/business/` | `business-persona`, `business-capability-map`, `business-value-stream`, `business-process`, `business-model-canvas`, `business-quantitative-model` |
| `discovery-` | `docs/discovery/` (pre-formal evidence layer — ideation, interviews, workshops; cross-cutting, feeds every downstream artefact) | `discovery-idea` (→ `docs/discovery/ideation/`), `discovery-research` (→ `docs/discovery/interviews/`), `discovery-workshop` (→ `docs/discovery/workshops/`) |
| `spec-` | `docs/product-specs/` | `spec-prd`, `spec-functional-breakdown-structure`, `spec-quality-attributes`, `spec-use-case`, `spec-peer-review`, `spec-grill-me` |
| `plan-` | `docs/plans/` (build planning — specifies *intended sequence*, split from `spec-` per clew ADR-0009) | `plan-delivery-roadmap` (→ `docs/plans/delivery-roadmap.md`, epics `E-NN`), `plan-implementation` (→ `docs/plans/active/`, `Plan-NNNN`) |
| `arch-` | `docs/architecture/` (subfolders per artefact type) | `arch-adr` (writes to `docs/architecture/decisions/`) |
| `domain-` | `docs/domain/` | DDD artefacts — bounded contexts, glossary, domain model; the shared language between business and tech | `domain-bounded-context`, `domain-glossary`, `domain-model` |
| `ops-` | `docs/ops/` for doc artefacts; *(no doc folder)* for infra/devops automation | `ops-runbook` (→ `docs/ops/runbooks/`), `ops-bug-rca` (→ `docs/ops/rcas/`), `ops-terraform-exoscale` *(infra automation — scaffolds into the project's `infra/`, no `docs/ops/` output)* |
| `qa-` | `docs/qa/` (subfolders per artefact) | Quality-assurance & test layer — the *validate / test* stage of the SDLC. Produces the **tests** that verify the quality *requirements* `spec-quality-attributes` defines (`QA-XXNN`); the two are distinct (`spec-quality-attributes` = what must hold; `qa-` = how it is checked). **Reserved — no skill yet:** `qa-test-strategy` (mints `TS-NN`; was the planned `spec-test-strategy`), `qa-test-scenario` (realises `UC-NN`), `qa-test-plan`, `qa-acceptance-test`, `qa-eval-harness` |
| `dev-` | *(no doc folder — developer workflow utility)* | `dev-git-commit`, `dev-pr`, `dev-git-worktree`, `dev-ralph-loop` |
| `ux-` | `docs/ux/` (design + experience layer — project visual source of truth + UX artefacts; tokens consumed by the `com-` presentation layer; cross-cutting) | `ux-design-system` (→ `docs/ux/design-system.md` + `tokens.css`) |
| `com-` | `docs/communication/` (subfolders per artefact type, e.g. `slides/`) | `com-slide-deck` (→ `docs/communication/slides/{slug}/`) |
| `util-` | *(no doc folder — housekeeping)* | `util-docs-audit`, `util-toolkit-doctor` |

**Why this matters:** when you (or Claude) see a skill name, the prefix immediately tells you (a) which folder its output goes into, or (b) that it's a non-doc utility. No ambiguity.

### Inner-redundancy rule

If the artefact name already starts with the category word, **strip the redundancy**.

| ❌ Redundant | ✅ Clean |
|---|---|
| `business-business-process` | `business-process` |
| `business-business-model-canvas` | `business-model-canvas` |
| `arch-architecture-decision` | `arch-adr` |

### Artefact name (required)

The noun the skill produces or operates on, in **kebab-case**, **singular**. The artefact name should be the natural English noun for the deliverable, not an action verb.

- ✅ `spec-persona` (the artefact is "persona")
- ✅ `spec-business-capability-map` (the artefact is "business capability map")
- ❌ `spec-personas` (no plural)
- ❌ `spec-building-personas` (verb-phrase, not noun)

### Verb suffix (optional — only when disambiguation is required)

When **two skills share the same artefact** but differ in intent, append a verb suffix:

- `spec-prd` (creates PRDs) vs `spec-prd-review` (reviews PRDs) — different intents on the same artefact
- `spec-adr-manager` (full CRUD lifecycle) — manager verb expresses the lifecycle intent

When only ONE skill exists per artefact, **drop the verb suffix**. The "build" intent is implicit; the SKILL.md description carries the trigger words.

| ❌ Wrong (redundant verb) | ✅ Right (implicit) |
|---|---|
| `spec-persona-builder` | `spec-persona` |
| `spec-prd-creator` | `spec-prd` |
| `spec-value-stream-mapper` | `spec-value-stream` |
| `plan-implementationner` | `plan-implementation` |
| `spec-peer-reviewer` | `spec-peer-review` |
| `ops-runbook-creator` | `ops-runbook` |

### Allowed verbs (when disambiguation is needed)

| Verb | Use for |
|---|---|
| `-builder` | Creates new instances (replaces `-creator`, `-generator`) |
| `-manager` | Full CRUD lifecycle |
| `-mapper` | Links/maps between artefacts |
| `-reviewer` / `-review` | Critical review / quality assessment |
| `-auditor` / `-audit` | Read-only assessment |
| `-runner` | Executes a process |

### Anti-patterns (don't do these)

| Anti-pattern | Why | Fix |
|---|---|---|
| Missing category prefix (`docs-auditor`) | No discoverability axis | Add prefix → `util-docs-audit` |
| `-skill` suffix (`slide-builder-skill`) | Tautological | Drop suffix → `com-slide-deck` |
| `using-` prefix (`using-git-worktrees`) | Verb-led, plural noun | Reframe → `dev-git-worktree` |
| Synonym verbs (`-creator`, `-generator`, `-builder` interchangeably) | Pick-one inconsistency | Standardise on `-builder`, drop others |
| Folder name ≠ `name:` field | Hidden inconsistency | Always align both |

### Verification

When you create or rename a skill, verify name consistency:

```bash
for skill in skills/*/; do
  skill_name="$(basename "${skill%/}")"
  [ -f "$skill/SKILL.md" ] && name=$(grep "^name:" "$skill/SKILL.md" | sed -E 's/name: *//; s/^"//; s/"$//')
  [ "$skill_name" != "$name" ] && echo "MISMATCH: folder=$skill_name name=$name"
done
```

Should return zero output.

---

## SKILL.md frontmatter convention

Match existing skills like `spec-prd`:

```yaml
---
name: skill-name-kebab
description: "One sentence + 'Triggers on: phrase1, phrase2, phrase3.' Claude uses this to decide when to activate."
version: "1.0.0"
status: active          # draft | active | deprecated | superseded
last_reviewed: YYYY-MM-DD
review_interval: 180d
user-invocable: true
allow_implicit_invocation: true
impact: "low"
metadata:
  category: "specification"   # or "infrastructure", "review", etc.
  complexity: "medium"
---
```

Codex agent loaders enforce a hard limit on the frontmatter `description`
field: **1024 characters maximum**. If the description exceeds that limit, the
skill may be skipped as invalid. Keep the description trigger-focused: what the
skill does, when to use it, and a short `Triggers on:` phrase list. Move
methodology detail, examples, and edge-case scope notes into the body or
`references/` files instead of frontmatter.

Validate before committing:

```bash
ruby -e 'require "yaml"; d = YAML.load_file("SKILL.md")["description"]; puts d.length; abort("description too long") if d.length > 1024'
```

## Output artefact frontmatter (mandatory for all doc-producing skills)

Every markdown file a skill writes under `docs/` must open with the standard
five-field frontmatter block. The canonical schema, field rules, default
`review_interval` values per artefact type, and audit enforcement details live in
`rules/artefact-frontmatter.md`. Reference that file in every new skill's output
or checklist section — do not restate the schema inline.

```yaml
---
title: <instance title — not the artefact type name>
status: draft
owner: <git config user.name>
last_reviewed: YYYY-MM-DD
review_interval: Nd   # see artefact-frontmatter.md for defaults per type
---
```

## Domain-agnostic discipline (critical)

The kit is USER-GLOBAL across every project. Skills shipped here must avoid project-specific terms — no client names, industry jargon, real currencies as defaults, or segment names from the originating project. Examples in `references/` should use placeholders (`{{currency}}`, "Industry A", "top N customers"). The originating project's own scaffolds can stay project-specific; only the kit-side copy must be neutral.

Audit before pushing:

```bash
grep -niE "<project-specific terms>" SKILL.md references/*.md
```

Should return zero matches.

## Metamodel impact assessment (run before publishing any skill change)

Two mandatory stages. Never skip Stage 1 — the classification determines which updates are required and prevents both over-engineering (updating everything for a utility skill) and under-engineering (missing downstream wiring for a real metamodel artefact).

---

### Stage 1 — Classify: does this skill need metamodel integration?

Answer this question first, before any design work:

> **"Does this skill produce a new named artefact that other skills or agents need to know about and reference?"**

| Classification | Description | Examples | Stage 2 |
|---|---|---|---|
| **New metamodel step** | Produces a new artefact type with its own step in the build order; other skills should read or reference it | `business-vision` (Step 0), `business-objective` (Step 4.5) | → Stage 2A (full blast radius) |
| **Variant / refinement** | New skill for an artefact type that already exists in the metamodel; no new step, no new IDs | A second review skill for PRDs, a new canvas variant | → Stage 2B (targeted updates only) |
| **No metamodel impact** | Developer workflow, housekeeping, post-ship operational artefact with no cross-references | `dev-*`, `util-*`, `ops-runbook`, `ops-bug-rca` | → Stage 2C (skip metamodel) |

**Decision rule for "New metamodel step":** if you find yourself saying "other skills should read this doc before doing their work" or "PRDs / epics / quality attributes should reference this ID" — it's a new metamodel step.

---

### Stage 2A — Brand-new artefact step (full blast radius)

Run this **before writing a single line of the new skill** — it is a design preview, not post-hoc documentation. Present the full blast radius to the user and confirm before building.

#### Part 1: Design the skill itself

Before touching any file, answer:

1. **Output path** — where does the artefact live? Is there a naming convention exception? (e.g. `business-vision` → `docs/VISION.md` instead of `docs/business/`)
2. **IDs minted** — does it mint stable IDs (e.g. `OBJ-NN`, `KR-NN.M`) or is it a singleton (path-referenced only)?
3. **Modes** — Scaffold / Fill / Align / Refresh / Wire? What does each mode do?
4. **Reference files** — `template.md` (canonical output skeleton), `methodology-references.md` (bibliography), `{discipline}.md` (internal Claude guidance)?
5. **Special behaviours** — does any mode write to files outside `docs/` (e.g. `CLAUDE.md`)? If yes, set `impact: "medium"` not `"low"`.

#### Part 2: Blast radius map

For every brand-new artefact step, the following files require updates. Work through them in order.

**Core metamodel files (always — 7 change points in `rules/metamodel.md`):**

| Change point | What to update |
|---|---|
| Artefact table header | Update count ("The N artefacts") |
| Artefact table row | Add `\| step \| **Name** (tagline) \| \`skill-name\` \| output path \| IDs or *(singleton)* \|` |
| Build order step section | Add `### Step N` with: Skill, Prerequisites, Process (modes), Output verification criteria |
| DAG flowchart (text art) | Add node box + edges showing what it consumes (solid) and what soft-links to it (dashed) |
| ER diagram | Add entity + FK fields + relationship lines |
| Cross-doc ID conventions table | Add `\| \`ID-NN\` \| meaning \| owning skill \|` row — or note "singleton — no ID" |
| Canonical output paths | Add the output path in the correct position in the `docs/` tree |
| Prefix → folder mapping | Note any exception if the output location breaks the prefix convention |
| Maintenance coupling log | Add a dated entry listing every file updated |

**README.md (always — 4 change points):**

| Change point | What to update |
|---|---|
| Intro line | Update artefact count ("N artefacts across…") |
| Flowchart | Add node (inside or outside a subgraph based on layer) + update subgraph label + add edges |
| ER diagram | Add entity + relationships (same changes as in `rules/metamodel.md`) |
| Skill index table | Add row |

**Existing skills — upstream reads (contextual):**

For each skill that *should read the new artefact before doing its work*, add a note to its process step that checks for the new file and reads it if present. Identify these by asking: "which existing skills produce output that the new artefact depends on, or that should be consistent with it?"

Common patterns:
- New artefact is **upstream of everything** (e.g. vision) → add "read `docs/VISION.md` first" to every `business-*` + `spec-*` skill's context-reading step
- New artefact is **a mid-stack layer** (e.g. objectives) → add read note only to skills that build deliverables objectives are supposed to guide (delivery roadmap, PRDs, quality attributes)

**Existing skills — downstream references (contextual):**

For each skill whose output *should reference the new artefact's IDs or path*, add the new ID/path to:
- The `§0 Architecture Traceability` block template (PRDs, implementation plans)
- The value statement / epic template (delivery roadmap)
- The cross-references section (quality attributes)
- The soft-links table (any canvas or objectives doc)

**Audit tool (always):**

| File | Checks to update |
|---|---|
| `util-metamodel-audit/references/check-catalogue.md` | Check 1: add `find` command for new output path · Check 2: add canonical placement rule · Check 5: add ID regex + owning artefact (skip if singleton) · Check 7: add dependency enforcement rule · Check 9: add mandatory sections detection |
| `util-metamodel-migration/references/detection-signals.md` | §Filename patterns: add glob + artefact type + canonical path · §Folder name patterns: add if applicable · §Content signals: add heading pattern or ID pattern |

#### Part 3: After building — verify

```bash
# 1. Naming consistency
for skill in skills/*/; do
  skill_name="$(basename "${skill%/}")"
  [ -f "$skill/SKILL.md" ] && name=$(grep "^name:" "$skill/SKILL.md" | sed -E 's/name: *//; s/^"//; s/"$//')
  [ "$skill_name" != "$name" ] && echo "MISMATCH: folder=$skill_name name=$name"
done
# Should return zero lines (excluding non-skill folders like commands/, rules/)

# 2. Install
./install.sh

# 3. Confirm symlink
ls -la ~/.claude/skills/<new-skill-name>
```

---

### Stage 2B — Variant or refinement of existing artefact (targeted updates)

No new build order step. Run only the checks that apply:

| Changed? | Update |
|---|---|
| Output path changed | `rules/metamodel.md` canonical paths · Check 1 · §Filename patterns |
| New ID format minted | `rules/metamodel.md` ID conventions · Check 5 · §Filename patterns |
| Prerequisite added/removed | `rules/metamodel.md` DAG + build order step · Check 7 |
| Mandatory section added/renamed/removed | Check 9 · §Content signals |

---

### Stage 2C — No metamodel impact

`dev-*`, `util-*`, and `ops-*` skills that produce no metamodel artefact skip all of the above. Run only:

```bash
./install.sh   # confirm symlink created
```

---

### Worked examples

**`business-vision` (2026-05-21) — Stage 2A, singleton, naming exception:**
- New Step 0 in build order
- Singleton — no IDs, path-referenced only → skip Check 5 + skip ID conventions row (add note instead)
- Naming exception: `business-` prefix but output is `docs/VISION.md`, not `docs/business/` → document in prefix mapping table
- Wire mode writes to `CLAUDE.md` → `impact: "medium"`
- Upstream reads added to: `business-persona`, `business-model-canvas`, `business-objective`, `plan-delivery-roadmap`, `spec-prd`

**`business-objective` (2026-05-21) — Stage 2A, ID-minting:**
- New Step 4.5 in build order
- Mints `OBJ-NN` + `KR-NN.M` → add to ID conventions table + Check 5
- Downstream references added to: `plan-delivery-roadmap` (epic template), `spec-prd` (§0 traceability), `spec-quality-attributes` (KR grounding), `business-model-canvas` (VP → OBJ soft-link), `business-value-stream` (pain index note)

## Publish and install

1. Commit + push in `$KIT_DIR` — convention: `feat(<skill-name>): <title>` or `chore(<skill-name>): <title>`
2. `$KIT_DIR/install.sh` — symlinks all skills into `~/.claude/skills/`

## Cross-machine sync via chezmoi

Dotfiles hook `run_onchange_install-claude-kit.sh.tmpl` re-runs on every `chezmoi apply` *only when its rendered content changes*. The hash comment uses:

```
# claude-kit remote HEAD: {{ output "git" "ls-remote" "https://github.com/VictorHueni/homemade-claude-kit.git" "HEAD" | sha256sum }}
```

This hashes the kit's remote HEAD SHA — different on every kit commit, so chezmoi correctly re-triggers `git pull` + `install.sh`. Earlier versions hashed the literal string `"homemade-claude-kit"` which is constant; that bug was fixed 2026-05-16 (dotfiles commit `94a1bba`).

## Verification + repair

The `util-toolkit-doctor` skill audits the whole flow — chezmoi state, kit + dotfiles repo sync, `~/.claude/` symlink integrity. Invoke it if anything looks broken or after a major refactor.

## Why this matters

Skills in a project's `.claude/skills/` are project-scoped only. The kit makes them available everywhere and chezmoi-synced across machines. Never write skills directly to `~/.claude/skills/` — always go through the kit. The hardcoded `~/projets/` path in the dotfiles script only applies to the chezmoi bootstrap; for day-to-day use always derive the path from the git root.

## Repos

- Kit: <https://github.com/VictorHueni/homemade-claude-kit>
- Dotfiles: <https://github.com/VictorHueni/dotfiles>
