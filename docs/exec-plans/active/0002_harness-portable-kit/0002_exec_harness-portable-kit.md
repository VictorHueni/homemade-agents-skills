---
type: Implementation Plan
title: Plan-0002 — Harness-Portable Plugin Kit
description: Restructure the kit into toggleable plugin sets, package the metamodel as a self-contained cross-harness skill, and generate per-harness adapters (Claude / Codex / OpenCode) for rules, skills, and MCP.
tags: [kit, packaging, harness-portability, metamodel, plugins]
timestamp: 2026-07-19T12:00:00Z
status: draft
owner: Victor Hueni
last_reviewed: 2026-07-19
review_interval: 30d
---

# Implementation Plan: Harness-Portable Plugin Kit

## Summary

This plan transforms `homemade-claude-kit` from a Claude-oriented symlink bundle into a harness-portable toolkit with three properties:

1. **Toggleable sets** — skills grouped into coherent plugin sets that can be activated or deactivated at will: natively via a Claude Code plugin marketplace, via `permission.skill` globs in OpenCode, and via installer symlink profiles in Codex.
2. **A distributable metamodel** — the artefact/metamodel rules repackaged as a self-contained `metamodel` skill (SKILL.md is the one format all three harnesses read natively), referenced by sibling path (`../metamodel/references/…`) from every doc-producing skill. The bare, category-less name is a documented convention exception (the category registry is itself part of the metamodel). The skill absorbs `util-metamodel-audit`, `util-metamodel-scaffold`, and `util-metamodel-migration` as **Audit / Scaffold / Migrate modes**, so lifecycle operations read the skill's own references and structural-fact duplication becomes impossible by construction. Per clew [ADR-0008](https://github.com/VictorHueni/clew/blob/main/docs/architecture/decisions/adr-0008-clew-canonical-source-of-truth-for-metamodel.md), the structural references are an **interim hand-authored projection**; clew's future `clew metamodel export` (Phase 4) becomes their generator.
3. **Generated per-harness adapters** — thin, installer-generated stubs carry the ambient wiring each harness needs: Claude `paths:`-scoped pointer rules, AGENTS.md routing blocks for Codex/OpenCode, and MCP declarations emitted from one registry into the three native formats (`.mcp.json` / `config.toml` / `opencode.json`).

Source: harness-portability design conversation of 2026-07-19 (ecosystem review: rulesync, Ruler, OpenSkills, AGENTS.md standard; clew ADR-0008 alignment). No upstream PRD exists; `0002` is a provisional feature-request ID to be reused by a future PRD if one is created.

Principles:

1. One increment equals one coherent change set.
2. Every increment has an explicit test gate.
3. Decisions land as ADRs before any layout change (increments 01–02 gate everything after).
4. Content moves before layout moves — paths change once (metamodel skill before plugin folder restructure).
5. Ownership follows clew ADR-0008: the kit never becomes the structural metamodel source of truth; no parallel validator, no kit-side `registry.yaml`.
6. Symlink installation must keep working at every increment — the marketplace is an additional distribution channel, not a replacement.

**Overall Status:** pending
**Current Increment:** --

## Increment Plan

### Increment 01: ADR-0006 — Plugin Packaging & Cross-Harness Activation

**Status:** pending

Scope:

1. Record the target layout: `.claude-plugin/marketplace.json` + `plugins/<set>/` with per-set `plugin.json`, skills, commands, and `.mcp.json`.
2. Record the set composition (proposed: `kit-core`, `strategy`, `domain-modeling`, `product-spec`, `architecture`, `dev-flow`, `agent-loop`, `delivery-comms`, `ops`, `docs-hygiene`) with membership rationale.
3. Record the activation contract per harness: Claude = marketplace enable/disable; OpenCode = generated `permission.skill` deny-globs per disabled set; Codex = installer symlink profiles (`install.sh --sets`).
4. Record what deliberately does not port (Claude plugin bundle format, hooks) and why buy-vs-build resolved to installer-owned adapters over rulesync/Ruler for the user-global layer.

Primary files:

1. `docs/architecture/decisions/adr-0006-plugin-packaging-cross-harness-activation.md`

Test gate:

1. `test -f docs/architecture/decisions/adr-0006-plugin-packaging-cross-harness-activation.md`
2. `rg -n "marketplace.json|permission.skill|--sets|kit-core" docs/architecture/decisions/adr-0006-plugin-packaging-cross-harness-activation.md`

Exit criteria:

1. The full plugin-set membership (all current skills + 2 commands assigned) is enumerated with no orphans.
2. The three activation mechanisms are specified precisely enough to implement increments 08–13 without further design decisions.

### Increment 02: ADR-0007 — Metamodel Distribution as a Skill

**Status:** pending

Scope:

1. Record `metamodel` as the distribution vehicle for the artefact/metamodel contract: SKILL.md spine + self-contained `references/`, with lifecycle operations as modes (Audit / Scaffold / Migrate, procedures in `references/modes/`).
2. Record the naming decision: bare `metamodel`, a **documented exception** to the `<category>-<artifact>` convention — rationale: the category registry is itself part of the metamodel, so no category can contain it; consolidation makes it the single skill for the artefact, so verb suffixes drop per the convention's own rule. The exception is registered in `rules/skill-creation-sync.md` (prefix-mapping exceptions, as for `business-vision`).
3. Record the consolidation: `util-metamodel-audit`, `util-metamodel-scaffold`, `util-metamodel-migration` retire as standalone skills and become modes; merged skill carries `impact: "medium"` (Scaffold's Wire step writes `CLAUDE.md`); their future is thin wrappers over `clew audit` / `clew init` / `clew migrate`.
4. Record the sibling-path reference convention (`../metamodel/references/…`) replacing `rules/…` references in skills, and why it resolves identically in all three harnesses.
5. Record the `rules/` split: metamodel rules shrink to Claude `paths:`-scoped pointer stubs; harness-agnostic behavioural rules (`working-style`, `git-and-tools`, `writing-citations`, `diagramming-mermaid`, `frontend-nuxt`) stay and later feed AGENTS.md generation.
6. Cross-reference clew ADR-0008: structural references are an interim hand-authored projection, flipped to `clew metamodel export` output at clew Phase 4; the kit builds no parallel enforcement.

Primary files:

1. `docs/architecture/decisions/adr-0007-metamodel-distribution-as-skill.md`

Test gate:

1. `test -f docs/architecture/decisions/adr-0007-metamodel-distribution-as-skill.md`
2. `rg -n "metamodel|sibling|ADR-0008|projection" docs/architecture/decisions/adr-0007-metamodel-distribution-as-skill.md`

Exit criteria:

1. The fact-class boundary (structural = clew-owned projection · semantic = per-skill · behavioural = rules/AGENTS.md) is stated unambiguously.
2. The ADR names the exact files moving into `references/`, the exact rules remaining, and the three retired `util-metamodel-*` skills.
3. The naming exception is recorded with its rationale and its registration point in `skill-creation-sync.md`.

### Increment 03: Scaffold the `metamodel` Skill

**Status:** pending

Scope:

1. Create `skills/metamodel/SKILL.md`: body = the build-order spine from `rules/metamodel.md`; frontmatter description triggers on stack-level intents ("build the documentation stack", build-order/ID-format/artefact-placement questions) — not on per-artefact intents owned by producing skills.
2. Move `rules/metamodel-reference.md`, `rules/artefact-types-registry.md`, `rules/artefact-frontmatter.md`, `rules/open-items-governance.md` verbatim into `skills/metamodel/references/`.
3. Label structural sections "generated projection (future — clew ADR-0008 Phase 4); do not hand-edit to diverge from clew `docs/metamodel/`".
4. Keep the frontmatter description under the 1024-character Codex loader limit.

Primary files:

1. `skills/metamodel/SKILL.md`
2. `skills/metamodel/references/metamodel-reference.md`
3. `skills/metamodel/references/artefact-types-registry.md`
4. `skills/metamodel/references/artefact-frontmatter.md`
5. `skills/metamodel/references/open-items-governance.md`

Test gate:

1. `test -f skills/metamodel/SKILL.md && ls skills/metamodel/references/ | wc -l`
2. `ruby -e 'require "yaml"; d = YAML.load_file("skills/metamodel/SKILL.md")["description"]; abort("too long") if d.length > 1024'`
3. `./install.sh --quiet && test -L ~/.claude/skills/metamodel`

Exit criteria:

1. The skill is self-contained: no reference inside `skills/metamodel/` points outside its own folder.
2. Moved reference content is byte-identical to the source rules (frontmatter `paths:` blocks stripped).

### Increment 04: Reduce Metamodel Rules to Claude Pointer Stubs

**Status:** pending

Scope:

1. Replace the bodies of `rules/metamodel.md`, `rules/artefact-frontmatter.md`, `rules/artefact-types-registry.md`, `rules/open-items-governance.md` with short pointer stubs: keep `paths:` frontmatter, body = one paragraph routing to `metamodel` (skill name + reference file).
2. Delete `rules/metamodel-reference.md` (content lives in the skill; it had no `paths:` loading to preserve).
3. Delete `rules/skill-creation-sync.md`'s duplicated schema restatements where they now point into the skill (pointer edits only — full rewrite is increment 07).

Primary files:

1. `rules/metamodel.md`
2. `rules/artefact-frontmatter.md`
3. `rules/artefact-types-registry.md`
4. `rules/open-items-governance.md`

Test gate:

1. `for f in rules/metamodel.md rules/artefact-frontmatter.md rules/artefact-types-registry.md rules/open-items-governance.md; do test $(wc -l < $f) -lt 40 || echo "FAIL $f"; done`
2. `rg -l "metamodel. skill|../metamodel/" rules/ | wc -l` — returns ≥ 4 (stubs route to the skill)
3. `test ! -f rules/metamodel-reference.md`

Exit criteria:

1. Each stub still carries valid `paths:` frontmatter so Claude ambient loading is preserved.
2. No stub restates schema content — pointers only.

### Increment 05: Repoint Skill Cross-References to the Sibling Path

**Status:** pending

Scope:

1. Sweep every `skills/*/SKILL.md` + `references/` file replacing `rules/metamodel.md`, `rules/metamodel-reference.md`, `rules/artefact-types-registry.md`, `rules/artefact-frontmatter.md`, `rules/open-items-governance.md` references with `../metamodel/SKILL.md` / `../metamodel/references/…` equivalents.
2. Verify per `rules/git-and-tools.md`: after the wide replace, grep for surviving inner-substring occurrences.

Primary files:

1. `skills/*/SKILL.md` (~30 files)
2. `skills/*/references/*.md` (where they cite rules paths)

Test gate:

1. `rg -n "rules/metamodel|rules/artefact-types-registry|rules/artefact-frontmatter|rules/open-items-governance" skills/ --glob '!skills/metamodel/**' | wc -l` — returns 0
2. `rg -l "\.\./metamodel/" skills/ | wc -l` — > 20 files use the sibling path

Exit criteria:

1. Zero skill references into `rules/` for metamodel content; behavioural-rule references (`git-and-tools`, `working-style`) untouched.
2. Spot-check: `spec-prd` resolves ID format, canonical path, and frontmatter entirely through `../metamodel/`.

### Increment 06: Fold Audit / Scaffold / Migrate into Modes

**Status:** pending

Scope:

1. Add `references/modes/audit.md`, `references/modes/scaffold.md`, `references/modes/migrate.md` to the `metamodel` skill, porting the procedures from `util-metamodel-audit`, `util-metamodel-scaffold`, `util-metamodel-migration`; rewrite each so path/ID/dependency checks and the canonical tree derive at run time from the skill's own `references/artefact-types-registry.md` rows — no hardcoded per-artefact commands.
2. Extend `metamodel/SKILL.md` with a mode-dispatch section (Reference · Audit · Scaffold · Migrate) and fold the mode trigger phrases into the frontmatter description (still ≤ 1024 chars); set `impact: "medium"` (Scaffold's Wire step writes `CLAUDE.md`).
3. Delete `skills/util-metamodel-audit/`, `skills/util-metamodel-scaffold/`, `skills/util-metamodel-migration/` (installer prune removes their symlinks).
4. Repoint every reference to the three retired skills across `skills/`, `commands/`, and `rules/` at the corresponding mode.

Primary files:

1. `skills/metamodel/SKILL.md`
2. `skills/metamodel/references/modes/audit.md`
3. `skills/metamodel/references/modes/scaffold.md`
4. `skills/metamodel/references/modes/migrate.md`
5. `skills/util-metamodel-audit/` · `skills/util-metamodel-scaffold/` · `skills/util-metamodel-migration/` (deleted)

Test gate:

1. `ls skills/metamodel/references/modes/ | wc -l` — 3; `test ! -d skills/util-metamodel-audit && test ! -d skills/util-metamodel-scaffold && test ! -d skills/util-metamodel-migration`
2. `rg -n "util-metamodel-(audit|scaffold|migration)" skills/ rules/ commands/ | wc -l` — 0
3. `rg -n "artefact-types-registry" skills/metamodel/references/modes/ | wc -l` — ≥ 3 (modes derive from the registry)
4. `ruby -e 'require "yaml"; d = YAML.load_file("skills/metamodel/SKILL.md")["description"]; abort("too long") if d.length > 1024'`
5. `./install.sh --quiet && test ! -e ~/.claude/skills/util-metamodel-audit`

Exit criteria:

1. One skill owns the metamodel lifecycle; no second copy of structural facts exists anywhere in the kit.
2. The "Maintenance coupling" burden for new artefact types drops to: registry row + README (verified by reading the updated procedure).
3. Smoke test: "audit my docs stack" and "scaffold the docs folder" both trigger the `metamodel` skill in the correct mode.

### Increment 07: Blast-Radius Housekeeping for the Metamodel Move

**Status:** pending

Scope:

1. Rewrite `rules/skill-creation-sync.md`: new canonical reference convention (sibling path), updated Stage 2 blast-radius tables (rows pointing at moved files), removal of retired update points, and the registered naming exception for bare `metamodel` (rationale + "do not repeat this without an ADR").
2. Update `README.md`: rules table (stubs + skill), skill index (add `metamodel`, drop the three retired `util-metamodel-*` rows).
3. Update `scripts/audit-skills.sh` if it asserts rules paths.

Primary files:

1. `rules/skill-creation-sync.md`
2. `README.md`
3. `scripts/audit-skills.sh`

Test gate:

1. `rg -n "metamodel-reference.md" rules/ README.md scripts/ | rg -v "metamodel" | wc -l` — 0
2. `bash scripts/audit-skills.sh` — exits 0

Exit criteria:

1. A contributor following `skill-creation-sync.md` end-to-end touches only files that still exist.
2. Naming-consistency check returns zero mismatches.

### Increment 08: Plugin Marketplace Layout

**Status:** pending

Scope:

1. Create `.claude-plugin/marketplace.json` listing the sets from ADR-0006.
2. Create `plugins/<set>/.claude-plugin/plugin.json` per set; `git mv` each skill folder into its set's `plugins/<set>/skills/`; move `commands/branch-cleanup-audit.md` → `plugins/dev-flow/commands/`, `commands/ralph-audit.md` → `plugins/agent-loop/commands/`.
3. `kit-core` receives `metamodel` + the remaining `util-*` skills + ownership of the rules stubs story.

Primary files:

1. `.claude-plugin/marketplace.json`
2. `plugins/*/.claude-plugin/plugin.json` (10 files)
3. `plugins/*/skills/**` (moved), `plugins/*/commands/*.md` (moved)

Test gate:

1. `python3 -c "import json;json.load(open('.claude-plugin/marketplace.json'))"`
2. `for p in plugins/*/; do python3 -c "import json;json.load(open('$p/.claude-plugin/plugin.json'))" || echo "FAIL $p"; done`
3. `test $(find plugins/*/skills -maxdepth 1 -mindepth 1 -type d | wc -l) -eq $(ls -d plugins/*/skills/*/ | wc -l) && test ! -d skills`
4. `find plugins -name SKILL.md | wc -l` — equals post-consolidation skill count (57: 59 original − 3 retired + `metamodel`)

Exit criteria:

1. Every skill and command has exactly one home; `skills/` and `commands/` no longer exist at repo root.
2. Marketplace add from the local clone succeeds in Claude Code and each set is individually toggleable (manual verification, recorded in progress notes).

### Increment 09: Installer Update for the Plugin Layout

**Status:** pending

Scope:

1. Update `install.sh` skill discovery from `skills/*/` to `plugins/*/skills/*/`, and command discovery to `plugins/*/commands/*.md`; keep symlink + prune semantics identical.
2. Prune logic recognises and removes stale links to old `skills/*` paths.

Primary files:

1. `install.sh`

Test gate:

1. `./install.sh --verbose` into a temp target: `./install.sh /tmp/kit-test && find /tmp/kit-test/.claude/skills -maxdepth 1 | wc -l` — equals skill count + 1
2. Re-run is idempotent: second run prints "No changes."

Exit criteria:

1. Symlink installation works from the new layout for `~/.claude`, `~/.codex`, `~/.agents` and project targets.
2. Stale links from the pre-move layout are pruned automatically.

### Increment 10: Set Activation Profiles (`--sets`)

**Status:** pending

Scope:

1. Add `install.sh --sets <csv>|--all-sets` with persisted state in `var/enabled-sets` (gitignored); default = all sets; `kit-core` cannot be disabled.
2. Symlink only enabled sets' skills/commands; prune links of disabled sets on re-run.

Primary files:

1. `install.sh`
2. `.gitignore`

Test gate:

1. `./install.sh --sets kit-core,dev-flow /tmp/kit-test2 && test ! -e /tmp/kit-test2/.claude/skills/business-vision && test -L /tmp/kit-test2/.claude/skills/dev-git-commit`
2. `./install.sh --sets kit-core,dev-flow,strategy /tmp/kit-test2 && test -L /tmp/kit-test2/.claude/skills/business-vision`

Exit criteria:

1. Toggling a set on/off via re-run adds/prunes exactly that set's links in all skill targets.
2. State survives re-runs without flags (chezmoi hook compatibility).

### Increment 11: AGENTS.md Adapter Generation

**Status:** pending

Scope:

1. Add a generator step to `install.sh`: render `templates/agents-adapter.md` (metamodel routing paragraph + enabled-set summary + concatenated harness-agnostic rules) into a marker-delimited block of `~/.codex/AGENTS.md` and the OpenCode global instructions file, creating files if absent, replacing only the marked block otherwise.

Primary files:

1. `install.sh`
2. `templates/agents-adapter.md` (new)

Test gate:

1. `HOME=/tmp/kit-home ./install.sh && rg -n "metamodel" /tmp/kit-home/.codex/AGENTS.md`
2. Run twice; `rg -c "BEGIN homemade-claude-kit" /tmp/kit-home/.codex/AGENTS.md` — exactly 1 (idempotent block replace)

Exit criteria:

1. Codex/OpenCode sessions receive the metamodel routing + behavioural rules without any Claude-specific mechanism.
2. User content outside the markers is never touched.

### Increment 12: MCP Registry and Per-Harness Generation

**Status:** pending

Scope:

1. Create `mcp/registry.json`: server name → command/transport/env + owning set(s), seeded with the ADR-0006 selection (e.g. GitHub → `dev-flow`, PlantUML/Structurizr → `architecture`, Playwright → `delivery-comms`).
2. Generate per-set `plugins/<set>/.mcp.json` (Claude), a `[mcp_servers.*]` TOML fragment for `~/.codex/config.toml` (marker-delimited), and an `mcp` JSON fragment for OpenCode, filtered to enabled sets.

Primary files:

1. `mcp/registry.json`
2. `install.sh` (or `scripts/gen-mcp.py` invoked by it)
3. `plugins/*/.mcp.json` (generated, committed for marketplace consumers)

Test gate:

1. `python3 -c "import json;json.load(open('mcp/registry.json'))"`
2. `HOME=/tmp/kit-home ./install.sh --sets kit-core,dev-flow && rg -n "mcp_servers" /tmp/kit-home/.codex/config.toml`
3. Disable `dev-flow`, re-run: GitHub server absent from generated fragments.

Exit criteria:

1. One registry drives all three declaration formats; no hand-maintained per-harness MCP config remains.
2. MCP servers follow set activation.

### Increment 13: OpenCode Set-Toggle Fragment

**Status:** pending

Scope:

1. Generate the `permission.skill` deny-glob block for disabled sets (prefix patterns, e.g. `"business-*": "deny"`) into the OpenCode global config, marker-delimited, per enabled-set state.
2. Document the mechanism + manual override in the adapter template.

Primary files:

1. `install.sh` (generator step)
2. `templates/agents-adapter.md`

Test gate:

1. `HOME=/tmp/kit-home ./install.sh --sets kit-core,dev-flow && python3 -c "import json;c=json.load(open('/tmp/kit-home/.config/opencode/opencode.json'));assert c['permission']['skill'].get('business-*')=='deny'"`

Exit criteria:

1. Disabling a set in one place (`--sets`) deactivates it in all three harnesses through their native mechanisms.

### Increment 14: Toolkit Doctor Learns the New Layout

**Status:** pending

Scope:

1. Update `util-toolkit-doctor` checks: plugin layout paths, `var/enabled-sets` state, marker blocks present in adapter files, MCP fragments consistent with registry + state, stale pre-move symlinks flagged.

Primary files:

1. `plugins/kit-core/skills/util-toolkit-doctor/SKILL.md` (+ its references)

Test gate:

1. `rg -n "enabled-sets|marketplace.json|AGENTS.md" plugins/kit-core/skills/util-toolkit-doctor/ | wc -l` — ≥ 3

Exit criteria:

1. Doctor detects and explains: missing set state, drifted adapter blocks, orphaned old-layout links.

### Increment 15: README Rewrite and Open-Item Filing

**Status:** pending

Scope:

1. Rewrite `README.md` around the three-harness story: plugin-set table (replacing the flat skill index grouping), install paths per harness (marketplace vs `install.sh --sets`), adapter/MCP generation overview.
2. File open items (GitHub backend, per ADR-0002/0003): (a) clew cross-repo — amend OI-0030 with the multi-projection export requirement (kit registry markdown + `metamodel/references/` + AGENTS.md stubs); (b) revisit issue #53 (kit-as-OKF-bundle) against the new layout; (c) any deferred set-membership disputes from ADR-0006 review.

Primary files:

1. `README.md`
2. GitHub issues (via `util-open-items`, `backend: github`)

Test gate:

1. `rg -n "plugins/|--sets|marketplace" README.md | wc -l` — ≥ 3
2. `rg -n "skills/business-vision|^\\| .util-. \\|" README.md | wc -l` — 0 stale pre-move paths

Exit criteria:

1. README install instructions reproduce a working three-harness setup from scratch.
2. All deferred work is in the ledger with source anchors into this plan.

## Delivery Rules

1. One increment per commit; never `git commit --amend` (per `rules/git-and-tools.md`).
2. **Commit scope:** `packaging` — area slug (no capability map governs the kit itself; resolution rule 3). Plan reference goes in a `Refs: Plan-0002 increment NN` trailer, never the scope.
3. Each increment must leave `./install.sh` working — symlink consumers (chezmoi machines) may pull at any commit.
4. Increments 01–02 (ADRs) require explicit user approval before increment 03 starts; increment 08's set composition executes ADR-0006 as approved.
5. Manual harness verifications (marketplace toggle, Codex/OpenCode discovery) are recorded in `progress.txt` in this workspace.
6. Out of scope: clew Phase 3/4 implementation (`metamodel.yaml`, `clew metamodel export`), `qa-*` skills, hooks portability.

## Milestone Chunks (Standalone Delivery Groups)

| Milestone | Increments | Status | Coherent Outcome | Standalone Test Gate | Exit Criteria | Commit Guidance |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| M1: Decisions | 01–02 | pending | Both ADRs active; layout + boundaries approved | `rg -l "status: active" docs/architecture/decisions/adr-000[67]*.md` | User-approved ADR pair | `docs(packaging): …` |
| M2: Metamodel skill | 03–07 | pending | Metamodel distributable as one self-contained skill with Audit/Scaffold/Migrate modes; rules = Claude stubs; zero duplicate structural facts | Increment 05 + 06 gates green; PRD smoke test through sibling paths | Skills resolve metamodel via `../metamodel/` in all three harnesses; mode smoke tests pass | `feat(packaging): …` |
| M3: Marketplace | 08–09 | pending | Kit consumable as a Claude plugin marketplace with per-set toggling; symlink install unaffected | Increment 08 gate 4 + increment 09 idempotency gate | Marketplace add + set toggle verified manually | `feat(packaging): …` |
| M4: Cross-harness | 10–13 | pending | One `--sets` state drives skills, rules routing, and MCP in Claude, Codex, and OpenCode | Increment 13 gate (single toggle, three harnesses) | Set disable propagates to all harness-native configs | `feat(packaging): …` |
| M5: Close-out | 14–15 | pending | Doctor + README match reality; deferred work in the ledger | Increment 15 gates | Fresh-machine setup reproducible from README | `docs(packaging): …` |
