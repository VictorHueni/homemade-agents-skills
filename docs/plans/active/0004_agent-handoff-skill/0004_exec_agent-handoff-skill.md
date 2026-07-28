---
type: Implementation Plan
title: Plan-0004 — agent-handoff skill (session context handoff, agent-loop set)
description: Build the agent-handoff skill — create/resume modes for handing an overloaded session's context to a fresh session via a validated markdown handoff doc under var/handoffs/ — plus cross-harness wiring, a write-time structural validator, and forward-compatible eval assets, per the 2026-07-28 grill-session decisions.
tags: [agent-handoff, agent-loop, context-management, handoff, skills]
timestamp: 2026-07-28T12:00:00Z
status: draft
owner: Victor Hueni
last_reviewed: 2026-07-28
review_interval: 30d
---

# Implementation Plan: agent-handoff skill

## Summary

This plan implements the `agent-handoff` skill in the `agent-loop` set: the interactive-session complement to `agent-ralph-loop`. When a session's context grows overloaded, `create` mode writes a structured, validated handoff document to `var/handoffs/<workstream-slug>/NN-<date>-<slug>.md` and ends with a paste-ready resume prompt; `resume` mode reads a handoff in a fresh session, checks repo drift against the recorded branch + HEAD sha, re-verifies inherited claims (trust-but-verify), and continues the work.

No PRD exists; the source artefacts are the grill-session decision record (`var/reports/grill-me/2026-07-28-agent-handoff-design.md`, machine-local) and two research syntheses (`var/reports/handoff-skill/research.md`, `var/reports/skill-evals/research.md`, machine-local). The eight locked design decisions are restated as constraints in the Delivery Rules so this plan is self-contained. The kit-wide evals lane is explicitly out of scope — tracked as [#102](https://github.com/VictorHueni/homemade-claude-kit/issues/102); this plan only ships the forward-compatible pilot eval assets inside the skill.

Principles:

1. One increment equals one coherent change set.
2. Every increment has an explicit, executable test gate.
3. Portable core first, harness adapters second: the skill must work as plain markdown-in / markdown-out on Claude Code, Codex, and OpenCode before any harness-specific surface is touched. No hooks in v1 (deferred; revisit trigger: losing a session to surprise auto-compaction despite the skill existing).
4. Validator before trust: create mode never emits a handoff that `validate-handoff.py` rejects.

**Overall Status:** pending
**Current Increment:** 03

## Design constraints (locked 2026-07-28 — do not re-litigate in increments)

1. Name/placement: `agent-handoff`, `plugins/agent-loop/skills/agent-handoff/`, self-contained per the skill layout convention.
2. Storage: `var/handoffs/<workstream-slug>/NN-<date>-<slug>.md`; NN is the chain sequence number; gitignored by default with explicit opt-in commit; create mode maintains a `var/handoffs/LATEST` single-line pointer (path + status) already in v1.
3. Handoff template sections (all required): Goal (immutable) · Approach & key decisions (incl. rejected alternatives) · State (Done / In progress / Remaining) · Files (pointers, never pasted content) · Verification · Dead ends — do not retry (non-empty or literal "none") · Constraints & gotchas (verified facts vs hypotheses / open questions) · Suggested skills · Next step (single first action, imperative). Header records date, branch, HEAD sha, approximate context %. Budget ≤ ~200 lines. Evidence over prose (actual error output, not summaries of it).
4. Resume trigger v1 is fully explicit: create mode ends with a paste-ready resume prompt; the user-global rule/AGENTS.md line is passive routing knowledge only — no session-start scan directive. The skill never edits a project's AGENTS.md.
5. Resume mode drift check warns and re-verifies; it never hard-blocks.
6. Timing guidance in SKILL.md: write the handoff at 40–60% context at a semantic boundary; warn ≥80% (a degraded session writes a degraded handoff).
7. Verification: `scripts/validate-handoff.py` (Python 3 stdlib) is dual-used as create-mode write-time gate and eval grader — sections present and non-trivially populated, branch+sha header, line budget, no placeholder TODOs, secrets regex (block on hit, print offending line).
8. Eval case file ships inside the skill (`evals/evals.json`, skill-creator v2 schema + trigger block with owner-declared negatives) so the future kit-wide runner (#102) can glob `plugins/*/skills/*/evals/`.

## Increment Plan

### Increment 01: Scaffold SKILL.md with frontmatter, triggers, and mode contract

**Status:** done

Scope:

1. Create `plugins/agent-loop/skills/agent-handoff/SKILL.md`: frontmatter (`name: agent-handoff`, description with trigger phrases — handoff, hand off context, context handoff, pass context to a new session, continue in fresh session, resume handoff), the two-mode contract (create / resume), timing guidance (constraint 6), and the storage layout contract (constraint 2) including the LATEST pointer semantics and the gitignore-by-default + opt-in-commit rule.
2. State the explicit non-goals in SKILL.md: no hooks, no session-start scanning, no auto-continue, never edits project AGENTS.md, cannot clear the running session (create mode must end by instructing the operator).

Primary files:

1. `plugins/agent-loop/skills/agent-handoff/SKILL.md`

Test gate:

1. `./scripts/audit-skills.sh`
2. `for skill in plugins/*/skills/*/; do skill_name="$(basename "${skill%/}")"; name=$(grep -m1 "^name:" "$skill/SKILL.md" | sed -E 's/name: *//; s/^"//; s/"$//'); [ "$skill_name" != "$name" ] && echo "MISMATCH: folder=$skill_name name=$name"; done` — no output.

Exit criteria:

1. Skill passes the audit with folder/frontmatter name consistency.
2. SKILL.md declares both modes, the storage contract, and all five non-goals.

### Increment 02: Handoff template reference + create-mode procedure + example fixture

**Status:** done

Scope:

1. Write `references/handoff-template.md`: the canonical template (constraint 3) with per-section authoring rules — router-not-archive (pointers to files/ADRs/issues, no pasted content), evidence over prose, verified-facts vs hypotheses split, anti-padding note.
2. Write the create-mode procedure into SKILL.md: derive workstream slug (reuse an existing `var/handoffs/<slug>/` folder when the work continues a chain — next NN; else mint a new slug), record branch + `git rev-parse HEAD` + approximate context % in the header, run the validator before finishing (constraint 7 — validator lands in increment 03; reference it now), update `var/handoffs/LATEST`, ensure `var/handoffs/` is gitignored in the target project (append if missing, telling the operator), and end with the paste-ready resume prompt (constraint 4).
3. Add `references/example-handoff.md`: a realistic, complete example following the template (doubles as the validator's positive fixture in increment 03).

Primary files:

1. `plugins/agent-loop/skills/agent-handoff/references/handoff-template.md`
2. `plugins/agent-loop/skills/agent-handoff/references/example-handoff.md`
3. `plugins/agent-loop/skills/agent-handoff/SKILL.md`

Test gate:

1. `./scripts/audit-skills.sh`
2. `grep -c '^## ' plugins/agent-loop/skills/agent-handoff/references/example-handoff.md` — returns 9 (one per required template section).

Exit criteria:

1. Template and example carry all nine required sections in the locked order.
2. Create-mode procedure covers: chain continuation, header provenance, gitignore handling, LATEST update, and the terminal resume prompt.

### Increment 03: validate-handoff.py + positive/negative fixtures

**Status:** done

Scope:

1. Write `scripts/validate-handoff.py` (Python 3 stdlib only): checks all nine sections present and non-trivially populated ("Dead ends" accepts the literal "none"), header carries branch + 40-char sha + date, total ≤ 200 lines (configurable `--max-lines`), no `_TODO_`/`TBD`/placeholder markers, Next step begins with an imperative verb (word-list heuristic), secrets regexes (AWS keys, GitHub tokens, private-key blocks, `password=`/`api_key=` value patterns) → exit 1 printing the offending line. Exit 0 clean, exit 1 with one finding per line otherwise.
2. Add negative fixtures under `scripts/fixtures/`: one missing-section doc, one over-budget doc, one with a planted fake token.

Primary files:

1. `plugins/agent-loop/skills/agent-handoff/scripts/validate-handoff.py`
2. `plugins/agent-loop/skills/agent-handoff/scripts/fixtures/invalid-missing-section.md`
3. `plugins/agent-loop/skills/agent-handoff/scripts/fixtures/invalid-secret.md`

Test gate:

1. `python3 plugins/agent-loop/skills/agent-handoff/scripts/validate-handoff.py plugins/agent-loop/skills/agent-handoff/references/example-handoff.md` — exit 0.
2. `for f in plugins/agent-loop/skills/agent-handoff/scripts/fixtures/invalid-*.md; do python3 plugins/agent-loop/skills/agent-handoff/scripts/validate-handoff.py "$f" && echo "FAIL: $f passed"; done` — no FAIL lines; the secret fixture's output names the planted token line.

Exit criteria:

1. Validator accepts the example, rejects every negative fixture with a named finding, and is import-clean stdlib-only.

### Increment 04: Resume-mode procedure

**Status:** pending

Scope:

1. Write the resume-mode procedure into SKILL.md: locate the handoff (argument path > `var/handoffs/LATEST` > ask), drift check — compare recorded branch/sha to current repo, `git log --oneline <sha>..HEAD` to summarise what moved, warn and list drifted files, never hard-block (constraint 5) — then trust-but-verify: re-read every cited file:line before acting, treat "Constraints & gotchas" hypotheses as unverified, honour "Dead ends — do not retry" explicitly.
2. On successful resume: mark the handoff consumed (update `LATEST` status field) and, when the work continues, note that the next create call extends the same chain.

Primary files:

1. `plugins/agent-loop/skills/agent-handoff/SKILL.md`

Test gate:

1. `./scripts/audit-skills.sh`
2. `python3 -c "import yaml,re; t=open('plugins/agent-loop/skills/agent-handoff/SKILL.md').read(); assert yaml.safe_load(t.split('---')[1]); assert all(s in t for s in ['drift', 'Dead ends', 'LATEST'])"` — exit 0.

Exit criteria:

1. Resume mode specifies locate → drift-warn → re-verify → act → mark-consumed, with the never-hard-block rule explicit.

### Increment 05: Cross-harness wiring — rule file + AGENTS.md adapter line

**Status:** pending

Scope:

1. Add `rules/session-handoff.md` (kit rule, symlinked user-globally by install.sh): passive routing knowledge only — handoff docs live at `var/handoffs/`, resume via the agent-handoff skill; explicitly no session-start scan directive. Update `rules/skill-creation-sync.md` with the storage carve-out: `var/reports/<feature>/` = analysis artefacts, `var/handoffs/` = session state.
2. Add the equivalent single line to the AGENTS.md adapter template consumed by `scripts/gen-agents-md.py`, so Codex/OpenCode sessions get the same passive routing knowledge.

Primary files:

1. `rules/session-handoff.md`
2. `rules/skill-creation-sync.md`
3. `templates/` (the gen-agents-md source block)

Test gate:

1. `./install.sh /tmp/claude-scratch-target --verbose 2>&1 | grep -i handoff` — the skill symlink appears; no errors.
2. `python3 scripts/gen-agents-md.py --help >/dev/null 2>&1 || true` then render per its actual interface and `grep -i "var/handoffs"` the output — line present exactly once.

Exit criteria:

1. A scratch project install links `agent-handoff`; the rendered AGENTS.md block carries the routing line; no per-project file is written by the skill itself.

### Increment 06: Pilot eval case file (skill-creator v2 schema + trigger block)

**Status:** pending

Scope:

1. Write `evals/evals.json` inside the skill: ≥3 positive trigger prompts (paraphrased user speech, not description copies), ≥2 owner-declared negatives (e.g. "execute this plan autonomously" → owner `agent-ralph-loop`; "commit my changes" → owner `dev-git-commit`), and 2 behavioral evals — happy path (mid-task fixture; expectations: doc created at correct path, validator passes, resume prompt printed) and one pressure case ("we're at 95%, just /compact, skip the dead-ends section" — expectations: dead-ends section still populated, validator still run).
2. Add the behavioral fixture directory `evals/fixtures/` (small mid-task repo snapshot: a source file, a failing-test note, an in-progress edit).

Primary files:

1. `plugins/agent-loop/skills/agent-handoff/evals/evals.json`
2. `plugins/agent-loop/skills/agent-handoff/evals/fixtures/`

Test gate:

1. `python3 -c "import json; d=json.load(open('plugins/agent-loop/skills/agent-handoff/evals/evals.json')); assert len(d['trigger']['positive'])>=3; assert len(d['trigger']['negative'])>=2 and all('owner' in n for n in d['trigger']['negative']); assert len(d['evals'])>=2; assert all(e.get('files') for e in d['evals'])"` — exit 0.
2. Fixture paths referenced in `files[]` exist on disk.

Exit criteria:

1. Case file validates against the schema shape #102 will consume; the pressure case encodes the compaction-instead-of-handoff rationalization.

### Increment 07: Round-trip eval assets (pre-release lane, on-demand only)

**Status:** pending

Scope:

1. Write `evals/roundtrip/README.md`: the recipe — copy fixture, agent A works then creates a handoff via the skill, discard session, agent B (fresh) gets only doc + repo, grade mechanically: known next step completed (the fixture's failing check passes), documented dead end re-explored (grep B's transcript for the dead-end approach), turns-to-first-correct-action; pass@k over 3 trials. Mark explicitly: never in CI, run pre-release and on model upgrades.
2. Add the round-trip fixture (`evals/roundtrip/fixture/`): a mid-task mini-project with one verifiable remaining step and one seeded dead end.

Primary files:

1. `plugins/agent-loop/skills/agent-handoff/evals/roundtrip/README.md`
2. `plugins/agent-loop/skills/agent-handoff/evals/roundtrip/fixture/`

Test gate:

1. `d=$(mktemp -d) && cp -r plugins/agent-loop/skills/agent-handoff/evals/roundtrip/fixture/* "$d" && git -C "$d" init -q && ls "$d"` — fixture copies and git-inits cleanly.
2. `grep -ci "never in CI" plugins/agent-loop/skills/agent-handoff/evals/roundtrip/README.md` — ≥1.

Exit criteria:

1. An operator can run the round-trip by following the README alone; the fixture is self-contained and deterministic to set up.

### Increment 08: Release housekeeping

**Status:** pending

Scope:

1. Bump `plugins/agent-loop/.claude-plugin/plugin.json` minor version.
2. Update the skill count in `AGENTS.md` (57 → 58) and, if the repo lists agent-loop membership anywhere normative (ADR-0006 table is historical — do not edit), reflect the addition where the metamodel/docs index expects it.

Primary files:

1. `plugins/agent-loop/.claude-plugin/plugin.json`
2. `AGENTS.md`

Test gate:

1. `python3 -c "import json; json.load(open('plugins/agent-loop/.claude-plugin/plugin.json'))"` — parses; version increased.
2. `./scripts/audit-skills.sh` — clean.

Exit criteria:

1. Plugin version reflects the new skill; repo prose counts are consistent.

## Delivery Rules

1. One increment per commit.
2. **Commit scope:** `agent-handoff` — the skill/capability slug, per repo convention (cf. `com-release-note` commits). Plan reference goes in a `Refs: Plan-0004 increment NN` trailer, never the scope.
3. Each increment must be independently runnable and reversible; no increment mutates GitHub state (no `gh` calls anywhere in this plan).
4. `install.sh` test gates target scratch directories only — never the real `~/.claude` / `~/.codex` / `~/.agents` without operator approval.
5. Validator and all skill scripts are Python 3 stdlib only (kit stack rule).
6. The deferred hook layer (SessionStart reading `var/handoffs/LATEST`, dotfiles-wired) is out of scope for every increment; revisit trigger recorded in the grill session record.
7. Markdown prose is never hard-wrapped.

## Milestone Chunks (Standalone Delivery Groups)

| Milestone | Increments | Status | Coherent Outcome | Standalone Test Gate | Exit Criteria | Commit Guidance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| M1: Core skill | 01-04 | pending | agent-handoff usable end-to-end manually (create → validate → resume) | audit-skills.sh + validator passes example, rejects fixtures | Both modes fully specified; validator dual-use ready | `feat(agent-handoff): …` per increment |
| M2: Cross-harness wiring | 05 | pending | Passive routing reaches all three harnesses via existing surfaces | scratch install + rendered AGENTS.md grep | Rule + adapter line live; no per-project writes | `feat(agent-handoff): …` |
| M3: Eval assets | 06-07 | pending | Pilot evals forward-compatible with #102 + on-demand round-trip lane | evals.json schema check + fixture git-init | Case file consumable by future runner; round-trip runnable from README | `test(agent-handoff): …` |
| M4: Release | 08 | pending | Version + counts consistent | JSON parse + audit | Plugin bumped, prose counts updated | `chore(agent-handoff): …` |
