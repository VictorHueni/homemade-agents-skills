# Migration Report Template — util-metamodel-migration

Copy this skeleton to `var/reports/metamodel-migration/migration-{YYYY-MM-DD}.md`.

---

```markdown
<!-- migration-version: 1.0 | generated: YYYY-MM-DD | docs-root: {root} | mode: {full|structure|inventory} -->

# Metamodel Migration Report — {project} — {YYYY-MM-DD}

---

## Executive summary

| Metric | Count |
|---|---|
| Files to migrate (§1 folder mismatches) | {N} |
| Naming fixes (§2) | {N} |
| Folders to create (§3) | {N} |
| DDD migration candidates (§4) | {N} |
| Outside metamodel scope (§5) | {N} |
| **Total atomic fix blocks** | **{N}** |
| Files with inbound links affected | {N} |

**Estimated effort:** {N} copy-paste operations. Apply §1 blocks first (highest risk — inbound links). Then §2 renames. Then §3 mkdir. Run `util-metamodel-audit` after to verify compliance.

**Top 3 highest-risk migrations** (most inbound links):
1. `{file}` — {N} inbound links
2. `{file}` — {N} inbound links
3. `{file}` — {N} inbound links

---

## §1 Folder mismatches

Files detected at the wrong canonical location. Each finding is an **atomic fix block** — apply the entire block in one shell session.

{Repeat this block for each finding:}

### `{current/path/file.md}` → `{canonical/path/file.md}`

| Field | Value |
|---|---|
| Detection | {Tier 1: filename match / Tier 2: folder match / Tier 3: content signal} |
| Confidence | High / Medium / Low |
| Artefact type | `{skill-name}` |
| Inbound links | {N} files reference this |

```bash
# ── Atomic fix block ──────────────────────────────────────────────────────────
mkdir -p {canonical/directory}
git mv {current/path/file.md} {canonical/path/file.md}

# Inbound link repairs ({N} files)
# {linking-file}:{line}
sed -i 's|{old-relative-path}|{new-relative-path}|g' "{linking-file}"
# ... one sed per linking file
# ─────────────────────────────────────────────────────────────────────────────
```

{If Low confidence:} ⚠️ **Verify manually before applying** — only 1 of 3 detection tiers matched.

---

## §2 Naming issues

Files in the right folder but with naming convention violations.

| File | Current name | Canonical name | Fix |
|---|---|---|---|
| `{path/}` | `{current.md}` | `{canonical.md}` | `git mv {path/current.md} {path/canonical.md}` |

---

## §3 Missing canonical folders

Canonical metamodel directories that don't exist in this repo yet. Creating them prepares the structure for new artefacts — no content is moved.

| Canonical path | Needed for | Step | mkdir command |
|---|---|---|---|
| `docs/business/personas/` | `business-persona` outputs | Step 1 | `mkdir -p docs/business/personas` |
| `docs/business/capability-map/` | `business-capability-map` outputs | Step 2 | `mkdir -p docs/business/capability-map` |
| `docs/business/value-streams/` | `business-value-stream` outputs | Step 3 | `mkdir -p docs/business/value-streams` |
| `docs/business/05a-processes/` | `business-process` outputs | Step 4 | `mkdir -p docs/business/processes` |
| `docs/business/business-model-canvas/` | `business-model-canvas` outputs | Step 5 | `mkdir -p docs/business/business-model-canvas` |
| `docs/business/06a-models/` | `business-quantitative-model` outputs | Step 6 | `mkdir -p docs/business/models` |
| `docs/domain/` | All `domain-*` outputs | Steps 2b/2c/7b | `mkdir -p docs/domain` |
| `docs/product-specs/functional-breakdown-structure/` | `spec-functional-breakdown-structure` | Step 7 | `mkdir -p docs/product-specs/functional-breakdown-structure` |
| `docs/product-specs/delivery-roadmap/` | `plan-delivery-roadmap` | Step 8 | `mkdir -p docs/product-specs/delivery-roadmap` |
| `docs/product-specs/quality-attributes/` | `spec-quality-attributes` | Step 9 | `mkdir -p docs/product-specs/quality-attributes` |
| `docs/ops/runbooks/` | `ops-runbook` outputs | Ongoing | `mkdir -p docs/ops/runbooks` |
| `docs/ops/rcas/` | `ops-bug-rca` outputs | Ongoing | `mkdir -p docs/ops/rcas` |

Only list folders that are actually missing. Remove rows for folders that already exist.

---

## §4 DDD migration candidates

Files that predate the domain layer but contain content that belongs in `docs/domain/`. Do NOT use `git mv` — invoke the relevant domain skill to scaffold the target and import the content.

| File | Current path | Suggested destination | Confidence | Skill to invoke |
|---|---|---|---|---|
| `{file}` | `{current}` | `docs/domain/02c-glossary.md` | {H/M/L} | Run `domain-glossary` Mode 2 (seed from existing content) |
| `{file}` | `{current}` | `docs/domain/07b-models/{bc-slug}.md` | {H/M/L} | Run `domain-bounded-context` first, then `domain-model` Mode 2 |

---

## §5 Outside metamodel scope

Folders and files that are valid project documentation but have no equivalent metamodel artefact. Listed for completeness — no action needed.

| Path | Why outside scope |
|---|---|
| `{path}` | {reason — e.g. "Developer guides — not a metamodel artefact"} |

---

## Migration metadata

| Field | Value |
|---|---|
| Generated | {YYYY-MM-DD HH:MM} |
| Skill version | util-metamodel-migration v1.0.0 |
| Docs root | `{root}` |
| Mode | {full / structure / inventory} |
| Files scanned | {N} |
| Directories scanned | {N} |
| Report path | `var/reports/metamodel-migration/migration-{YYYY-MM-DD}.md` |

**Next step:** after applying all atomic fix blocks, run `util-metamodel-audit` Mode 1 to verify full metamodel compliance.
```
