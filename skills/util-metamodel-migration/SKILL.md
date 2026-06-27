---
name: util-metamodel-migration
description: "Scan any existing docs/ folder structure and produce a migration report to align it with the strategic-architecture metamodel. Detects misplaced files using tiered confidence scoring (filename pattern → folder name → content signals), maps them to canonical metamodel paths, scans for inbound links that would break on move, and emits atomic fix blocks (git mv + sed commands) per file. Report-only — never modifies any file. Complement to util-metamodel-audit (audit = health check for compliant repos; migration = onboarding doctor for pre-metamodel repos). Triggers on: migrate docs, align docs to metamodel, migration doctor, docs migration, migrate folder structure, metamodel onboarding, fix docs structure, restructure docs."
version: "1.0.0"
user-invocable: true
allow_implicit_invocation: false
impact: "low"
metadata:
  category: "utility"
  complexity: "high"
status: active
last_reviewed: 2026-05-29
---

# Metamodel Migration Doctor

You are an expert at scanning existing documentation structures and producing a safe, atomic migration plan to align them with the strategic-architecture metamodel defined in `rules/metamodel.md`.

The artifact produced by this skill is **a markdown report** at `var/reports/metamodel-migration/migration-{YYYY-MM-DD}.md`. It is NOT a refactoring tool, NOT a content rewriter, NOT a link checker for already-compliant repos — it is a **one-time onboarding doctor** for repositories built before or without the metamodel.

**Report-only discipline:** this skill reads files and runs read-only detection commands. It never modifies any file. Every finding includes an atomic fix block — a copy-pasteable set of shell commands (git mv + sed) that the user can review and apply. The user decides what to apply and when.

**Complement to util-metamodel-audit:** run this skill once to migrate structure; then use `util-metamodel-audit` for ongoing health checks.

---

## What a good migration report means

| Question | Where it lives |
|---|---|
| **Which files are in the wrong canonical location?** | §1 Folder mismatches — per-file migration blocks |
| **Which file names don't follow the canonical convention?** | §2 Naming issues |
| **Which metamodel folders don't exist yet?** | §3 Missing canonical folders |
| **Which existing files look like pre-DDD domain artefacts?** | §4 DDD migration candidates |
| **Which folders/files are outside the metamodel scope?** | §5 Outside scope (Info) |
| **How confident is each detection?** | Per-finding confidence: High / Medium / Low |
| **What will break if I move this file?** | Per-file inbound link count + sed repair commands |

---

## The three modes of operation

### Mode 1 — Full scan

**When:** first-time migration assessment of a repository.

**Step 0 — Clarifying questions (ask BEFORE scanning)**

Ask the user the following 4 questions in a single message with lettered options. Users respond like `1A, 2B, 3A, 4B`:

```text
1. Docs root location?
   A. docs/ (default)
   B. Other — please specify the path

2. Flag ADR naming redundancy (e.g. 0001-adr-topic.md → 0001-topic.md)?
   A. Yes — flag as a naming issue
   B. No — accept as the project's own convention

3. Flag PRDs organised in subdirectories under docs/product-specs/?
   A. Yes — flag subdirectory organisation as misplacement (canonical = flat)
   B. No — accept subdirectory organisation

4. Severity threshold for report?
   A. All findings — Warning + Info (default)
   B. Warning only — skip Info (outside-scope + missing-folder notices)
```

**Process:**
1. Scan the docs root recursively with `find`.
2. For each file and folder, run the three-tier detection (see Detection methodology below).
3. For every file flagged for a move, run inbound link scan and compute new relative paths.
4. Assemble the report from `references/template.md`.
5. Save to `var/reports/metamodel-migration/migration-{YYYY-MM-DD}.md`.

### Mode 2 — Structure scan

**When:** quick structural check — only folder/file mismatches and missing dirs. No DDD detection, no outside-scope listing, no content signals.

Runs checks §1 + §2 + §3 only. No Step 0 needed — scans `docs/` by default.

### Mode 3 — Missing inventory

**When:** fast gap map — what canonical metamodel paths don't exist yet? No file analysis.

Outputs a single checklist: 16 metamodel steps (Step 0 Vision + 1, 2, 2b, 2c, 3, 4, 4.5, 5, 6, 7, 7b, 8, 9, 10, 11), each marked ✅ (exists) / ⬜ (missing), with the canonical path and the skill to run to create it. Discovery layer paths (`docs/discovery/{ideation,interviews,workshops}/`) are listed below the stack checklist as cross-cutting supporting artefacts. No proposed fixes — purely informational.

### Mode 4 — Schema migration (v1 paths → v2 numbered flat structure)

**When:** a project was built with the v1 canonical paths (nested subfolders like `docs/business/personas/personas.md`) and needs to migrate to the v2 numbered flat structure (e.g. `docs/business/01a-personas.md`) defined in `references/path-migration-v2.md`.

**Key difference from Modes 1–3:** those modes detect and guess — they scan unknown repos and infer canonical placement using 3-tier confidence scoring. Mode 4 is deterministic — the before/after mapping is fully known from `path-migration-v2.md`, no detection needed.

**Mode 4 scope** covers three v1 → v2 transition patterns: `singleton` (most BIZBOK artefacts), `multi-slug` (domain models per BC), and `pattern-c-discovery-promote` (the discovery family was promoted from `docs/business/discovery/` + `docs/ideas/` to a single top-level `docs/discovery/{ideation,interviews,workshops}/` — see §Discovery promotion in `references/path-migration-v2.md` for the full bash block, including IDEA-NNNN renumbering of legacy ideas).

**Step 0 — Clarifying questions (ask BEFORE scanning)**

```text
1. Project docs root?
   A. docs/ (default)
   B. Other — please specify

2. Output format?
   A. Dry-run — print migration script to console and report file (default, safe)
   B. Generate an executable .sh script at var/reports/metamodel-migration/schema-v2-migration-{date}.sh

3. Verify after migration?
   A. Yes — run util-metamodel-audit Mode 1 after apply to confirm zero misplacements
   B. No — skip verification
```

**Process:**
1. **Read `references/path-migration-v2.md`** to load the full v1 → v2 mapping table. Every row with `type ≠ no-change` is a migration candidate.
2. **For each singleton candidate (`type = singleton`)**:
   a. Check if the v1 file exists in the project docs root
   b. If yes: compute the new path from the mapping
   c. Scan all docs for inbound links: `grep -rln "$(basename $v1_path)\|$v1_path" docs/ --include="*.md"`
   d. For each linking file, compute the new relative path: `python3 -c "import os; print(os.path.relpath('$v2_abs', os.path.dirname('$linker_abs')))"`
   e. Emit: `mkdir -p $(dirname $v2_path)` + `git mv $v1_path $v2_path` + `sed` repairs
3. **For domain model consolidation (`type = multi-slug`, domain models)**:
   - `find docs/domain -mindepth 2 -name "domain-model.md"` → each found file at `docs/domain/{bc-slug}/domain-model.md` → moves to `docs/domain/07b-models/{bc-slug}.md`
   - After all moves: check if any non-domain-model files remain in `docs/domain/{bc-slug}/` folders; if the folder is empty, emit `rm -rf`; if not empty, warn and skip folder deletion
4. **For discovery promotion (`type = pattern-c-discovery-promote`)** — the three v1 → v2 transitions defined in `references/path-migration-v2.md §Discovery promotion`:
   - `docs/business/discovery/interviews/` → `docs/discovery/interviews/`
   - `docs/business/discovery/workshops/` → `docs/discovery/workshops/`
   - `docs/ideas/{slug}.md` (or `docs/ideas/{domain}/{slug}.md`) → `docs/discovery/ideation/IDEA-{NNNN}-{slug}.md`
   - The ideas migration mints a sequential `IDEA-NNNN` ID per file as it moves; the original domain subfolder (if any) becomes a `domain:` frontmatter tag, not a folder.
   - After move, emit a frontmatter backfill block: add `idea_id:`, `lifecycle: captured`, `graduates_to: _TBD_`, and `domain:` (mapped from the v1 subfolder name where present — `frontend`/`backend`/`infra` → `architecture`; `design`/`dx` → `dx`; others → `product` by default).
   - Full bash block is in `references/path-migration-v2.md §Discovery promotion` — read that section before emitting the migration script.
5. **Relative path recomputation rule:** NEVER string-substitute `../` chains. When folder depth changes (e.g. depth 3 → depth 2), every inbound link's `../` count must be recomputed from scratch using `os.path.relpath()`. String substitution produces wrong paths.
6. **VISION.md special case:** `docs/VISION.md` stays at root — no move, no link rewriting. BUT check if any CLAUDE.md pointer uses a wrong path (e.g. `vision/VISION.md`) and fix it.
7. **Assemble the migration script** in atomic blocks: each file migration is one block (`mkdir` + `git mv` + all `sed` repairs for that file). If inbound links = 0, the block is just `git mv`.
8. **Save to** `var/reports/metamodel-migration/schema-v2-migration-{date}.sh` (Mode 4 output, not the same as Mode 1 markdown report).
9. **Summary:** N files to move · N links to repair · N sed commands · N warnings (non-empty bc-slug folders, CLAUDE.md issues) · N ideas re-numbered with `IDEA-NNNN` prefix (Mode 4 discovery-promote step).

**If `--apply` (explicit opt-in only):** execute the script, then run `util-metamodel-audit` Mode 1 to verify zero misplacements. Never apply automatically — always dry-run first.

---

## Detection methodology — three-tier confidence scoring

Detection runs three tiers in order. A finding requires ≥2 tiers to agree before it's reported. Single-tier matches are flagged as Low confidence with a manual-verification note.

### Tier 1 — Filename patterns (High signal)

Scan filenames against the patterns in `references/detection-signals.md §Filename patterns`. A filename match alone gives confidence Medium; combined with Tier 2 or 3 → High.

Detection bash:
```bash
find {docs_root} -name "*.md" -o -name "*.md" | while read f; do
  base=$(basename "$f")
  # Apply each pattern from detection-signals.md §Filename patterns
  # e.g. *_prd_* → spec-prd type
done
```

### Tier 2 — Parent folder name (Medium signal)

Check the immediate parent folder name against the patterns in `references/detection-signals.md §Folder name patterns`. A folder name match alone gives confidence Low; combined with Tier 1 or 3 → Medium/High.

Detection bash:
```bash
find {docs_root} -type d | while read d; do
  folder_name=$(basename "$d")
  parent=$(dirname "$d")
  # Apply each pattern from detection-signals.md §Folder name patterns
  # e.g. runbooks/ outside docs/ops/ → ops-runbook type
done
```

### Tier 3 — Content signals (Confirmation)

Read only the **first 50 lines** of each file. Check for high-signal section headings from `references/detection-signals.md §Content signals`. Never read the full file — this keeps the scan fast on large repos.

Detection bash:
```bash
head -50 "$file" | grep -E "^#{1,3} " | while read heading; do
  # Apply each pattern from detection-signals.md §Content signals
  # e.g. "## Porter's Five Forces" → business-competitive-landscape
done
```

### Confidence rules

| Tiers matching | Confidence | Action |
|---|---|---|
| 3 of 3 | High | Report as finding, emit fix block |
| 2 of 3 | Medium | Report as finding, emit fix block, add verification note |
| 1 of 3 | Low | Report as "possible match — verify manually", no fix block |
| 0 | No detection | Skip (not a metamodel artefact) |

---

## Inbound link tracking — atomic fix blocks

For every file flagged for a move, the skill:

1. **Finds all inbound links:**
```bash
SOURCE_REL="docs/runbooks/my-runbook.md"
grep -rln "$(basename $SOURCE_REL)" {docs_root}/ --include="*.md" | while read linking_file; do
  grep -n "$SOURCE_REL\|$(basename $SOURCE_REL)" "$linking_file"
done
```

2. **Computes new relative paths** from each linking file to the new target location:
```bash
python3 -c "import os; print(os.path.relpath('$TARGET', os.path.dirname('$LINKING_FILE')))"
```

3. **Emits an atomic fix block** per file — the complete set of commands to move the file AND repair all inbound links:

```bash
# ── Migration: docs/runbooks/my-runbook.md → docs/ops/runbooks/my-runbook.md ──
# Confidence: High (filename match + folder match)
# Inbound links: 2 files

mkdir -p docs/ops/runbooks
git mv docs/runbooks/my-runbook.md docs/ops/runbooks/my-runbook.md

# Repair inbound links (2)
# docs/architecture/overview.md:45
sed -i 's|../runbooks/my-runbook.md|../ops/runbooks/my-runbook.md|g' docs/architecture/overview.md
# docs/plans/active/0042_deploy/README.md:12
sed -i 's|../../runbooks/my-runbook.md|../../ops/runbooks/my-runbook.md|g' "docs/plans/active/0042_deploy/README.md"
```

**If inbound links = 0:** the fix block contains only `mkdir -p` + `git mv`. Safe to apply immediately.
**If inbound links > 0:** apply the entire block atomically — `git mv` first, then all `sed` repairs in the same shell session.

---

## Report structure — the fixed template

Full template in `references/template.md`:

```
<!-- migration-version: 1.0 | generated: YYYY-MM-DD | docs-root: {root} | mode: {mode} -->

H1: Metamodel Migration Report — {project} — {YYYY-MM-DD}

§ Executive summary
  N files to migrate · N naming fixes · N folders to create · N DDD candidates · N outside scope
  Estimated migration effort: N atomic blocks (each = one copy-paste)

§1  Folder mismatches    Per-file migration block (see format above)
§2  Naming issues        File | Current name | Canonical name | git mv command
§3  Missing folders      Canonical path | Needed for (step + skill) | mkdir -p command
§4  DDD candidates       File | Current path | Suggested destination | Skill to run next
§5  Outside scope        File/Folder | Why outside scope | No action needed

Migration metadata
  Generated: YYYY-MM-DD | Docs root: {root} | Files scanned: N | Findings: N
```

Every §1 and §2 finding is an **atomic fix block** — complete and self-contained.
§3 findings are `mkdir -p` commands only (no content to move).
§4 findings propose which domain- skill to run after the structural migration.
§5 findings are Info only — listed for completeness, no action needed.

---

## Sizing heuristics

| Element | Recommended | Source |
|---|---|---|
| Run cadence | Once per repo (migration is one-time) | Practitioner |
| Files per atomic fix block | 1 move + N sed repairs | Design constraint |
| Confidence threshold before auto-proposing a fix | ≥ Medium (2+ tiers) | Practitioner |
| Max files to scan in one pass | No limit — but surface High/Medium findings first | Practitioner |
| After migration | Run `util-metamodel-audit` to verify compliance | Complementary skill |

---

## Finding the right output folder

Default: `var/reports/metamodel-migration/`

```bash
find . -type d -name "metamodel-migration" 2>/dev/null
```

Never write the report inside `docs/` — migration reports are not artefacts in the stack.

---

## Cross-reference — relationship to other skills

| Skill | Relationship |
|---|---|
| `util-metamodel-audit` | Run AFTER migration to verify ongoing compliance. Audit assumes metamodel compliance; migration doctor assumes pre-compliance. |
| `domain-bounded-context` | §4 DDD candidates → run this skill after moving glossary/info-model content to docs/domain/ |
| `domain-glossary` | §4 DDD candidates — glossary migration target |
| `domain-model` | §4 DDD candidates — information/domain model migration target |
| `discovery-idea` | Mode 4 `pattern-c-discovery-promote` — after moving ideas to `docs/discovery/ideation/`, run `discovery-idea` Mode 5 (maintain) to fill the backfilled `lifecycle:` / `graduates_to:` / `domain:` frontmatter fields and update the new flat `INDEX.md`. |
| `discovery-research` | Mode 4 `pattern-c-discovery-promote` — interview / synthesis / plan files are moved from `docs/business/discovery/interviews/` to `docs/discovery/interviews/` (path-only, no content rewrite). |
| `discovery-workshop` | Mode 4 `pattern-c-discovery-promote` — workshop / synthesis files moved from `docs/business/discovery/workshops/` to `docs/discovery/workshops/`. |
| `rules/metamodel.md` | The canonical source for all detection rules in references/detection-signals.md |

---

## Reference materials

Three files in `references/`:
- **`references/detection-signals.md`** — the complete tiered detection ruleset: filename patterns, folder name patterns, content signals, outside-scope patterns. Update this file when the metamodel gains new artefacts.
- **`references/template.md`** — full migration report skeleton with atomic fix block format.
- **`references/methodology-references.md`** — rationale for tiered detection, inbound link tracking, and the report-only discipline.

---

## Closing report to the user

After running any mode, summarise in 4–6 lines:

1. **Mode run** + **docs root** + **files scanned**.
2. **Finding counts** — N folder mismatches · N naming issues · N missing folders · N DDD candidates · N outside scope.
3. **Total atomic blocks** — how many copy-paste operations the full migration requires.
4. **Top 3 most impactful migrations** (files with the most inbound links — highest risk if done wrong).
5. **Report saved at** path.
6. **Next step** — "After applying all blocks, run `util-metamodel-audit` Mode 1 to verify compliance."

---

## Checklist

Before declaring the work done:

- [ ] Step 0 answered (Mode 1) or mode detected from context.
- [ ] Three-tier detection run for all files in docs root.
- [ ] Every finding has confidence level (High / Medium / Low).
- [ ] Every file-move finding has inbound link count.
- [ ] Every atomic fix block includes git mv + all sed repairs.
- [ ] No file modified — report-only discipline maintained.
- [ ] Low-confidence findings marked "verify manually" — no fix block emitted.
- [ ] §3 missing folders listed with mkdir -p commands.
- [ ] §4 DDD candidates suggest the correct domain- skill to run next.
- [ ] §5 outside-scope items listed as Info only.
- [ ] Report saved to var/reports/metamodel-migration/.
- [ ] Closing report delivered.
