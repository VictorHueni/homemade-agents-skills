---
name: util-metamodel-scaffold
description: "Initialise the canonical docs/ folder tree for a new project, generate a live index.md navigation hub in docs/, and wire a stack pointer into CLAUDE.md. Always creates the full canonical tree — every folder costs nothing empty and the audit checks files, not folders. Triggers on: scaffold the docs, initialise the project, set up the docs folder, create the documentation structure, create the folder structure, init metamodel, build the doc tree, scaffold docs, start the documentation."
version: "1.0.0"
status: active
last_reviewed: 2026-05-25
review_interval: 180d
user-invocable: true
allow_implicit_invocation: true
impact: "low"
metadata:
  category: "utility"
  complexity: "low"
---

# Metamodel Scaffold

Initialise the canonical `docs/` folder tree, generate a live `docs/index.md` navigation
hub, and wire a stack pointer into `CLAUDE.md`. Run this skill once at the start of every
new project — before any artefact-producing skill is invoked.

The canonical folder tree and artefact paths are defined in `rules/metamodel.md`. This
skill operationalises that definition: it creates the directories, documents them in an
index.md snapshot, and tells the agent where to look. It does NOT create artefact content
— that is the job of the `business-*`, `discovery-*`, `domain-*`, `spec-*`, `arch-*`,
`ops-*`, and `com-*` skills.

**Always the full tree.** Empty folders cost nothing — git ignores them until a file
lands, and `util-metamodel-audit` checks for files, not folders. There is no variant
selection: every project gets the same structure, and only fills what it needs.

**Complement to `util-metamodel-migration`:** migration restructures an existing docs/
folder that predates the metamodel. Scaffold initialises a fresh structure. Run scaffold
on new projects; run migration on existing ones.

---

## The three modes

### Mode 1 — Full scaffold (default)

**When:** starting a new project with no existing `docs/` structure.

**Step 0 — Clarifying questions (ask BEFORE running)**

Ask the user these 2 questions in a single message. Users respond like `1A, 2A`:

```text
1. Docs root?
   A. docs/ (default)
   B. Other — please specify

2. Wire the stack pointer into CLAUDE.md after scaffold?
   A. Yes — update CLAUDE.md (or create it if absent)
   B. No — scaffold only; I will update CLAUDE.md manually
```

Also ask for the **project name** if it is not already clear from context — used in the
index.md header.

**Pre-flight check (run before creating anything):**

```bash
existing=$(find {docs_root} -name "*.md" 2>/dev/null | wc -l)
echo "Existing markdown files in {docs_root}: $existing"
```

If `{docs_root}` already contains markdown files, warn the user:

> "`docs/` already has N markdown file(s). Running scaffold will create any missing
> canonical folders and **overwrite `docs/index.md`** with a fresh status snapshot.
> Existing artefact files are NOT touched.
> If the folder structure needs restructuring (files in wrong locations), run
> `util-metamodel-migration` instead. Continue with scaffold? (Y/N)"

If the user says N, stop and suggest `util-metamodel-migration` Mode 1.
If the user says Y, proceed.

**Process:**
1. Read the full folder list from `references/folder-catalogue.md`.
2. For each folder in the list: `mkdir -p {folder}`.
3. Place a `.gitkeep` in every empty leaf folder so the tree is git-trackable.
4. Create the `docs/project-control/open-items/` control plane — see §Project-control scaffold.
5. **`.gitignore` check:**
   ```bash
   grep -q 'var/reports' .gitignore 2>/dev/null \
     || echo "SUGGEST: 'var/reports/' is not in .gitignore — generated reports should not be committed."
   ```
   Record the result; surface it in the closing report.
6. Detect the current status of each canonical artefact path (bash — same logic as
   `util-metamodel-audit` Check 1) and generate `docs/index.md` from
   `references/index-template.md`.
7. If the user chose to wire CLAUDE.md (Step 0 option 2A): apply the stack pointer update
   (see §CLAUDE.md update rules below).

**Output verification:**
- All canonical folders exist (`find {docs_root} -type d | sort`).
- `docs/index.md` exists and contains a row for every canonical artefact step.
- `docs/project-control/open-items/open-items.md` and `docs/project-control/open-items/README.md`
  exist (or were already present and skipped).
- If wired: `CLAUDE.md` contains a reference to `docs/index.md`.
- No artefact content files created — only folders, `.gitkeep` files, `docs/index.md`,
  and the `docs/project-control/open-items/` control-plane stubs.
- If `var/reports/` is absent from `.gitignore`, this was surfaced in the closing report.

---

### Mode 2 — Folders only

**When:** the user wants the directory structure but will manage index.md and CLAUDE.md
separately, or a hub doc already exists.

No Step 0 questions needed beyond docs root.

**Process:**
1. Read folder list from `references/folder-catalogue.md`.
2. `mkdir -p` each folder; place `.gitkeep` in empty leaf folders.
3. Create the `docs/project-control/open-items/` control plane if absent.
4. Report: folders created / folders already existed.

No index.md generated. No CLAUDE.md update.

---

### Mode 3 — index.md refresh

**When:** the project already has a `docs/` structure; the user wants to regenerate
`docs/index.md` with fresh status detection (after completing several stack steps, for
example).

**Process:**
1. Detect docs root (check for existing `docs/index.md` or default to `docs/`).
2. Re-run the status detection bash commands from `references/index-template.md §Detection`.
3. Update the `> **Last refreshed:**` line in the body to today's date before writing (the reserved `index.md` carries no `last_reviewed` frontmatter field — only the root `okf_version`).
4. Overwrite `docs/index.md` with the refreshed status snapshot.
5. Report: N steps now ✅ / N steps 🔄 / N steps ⬜.

Does NOT create folders or touch CLAUDE.md.

---

## Folder creation — bash pattern

From `references/folder-catalogue.md`:

```bash
# Create the full canonical tree in one pass
mkdir -p \
  docs/business/05a-processes \
  docs/business/06a-models \
  ...   # (see full list in folder-catalogue.md)

# Place .gitkeep in leaf folders that have no content yet
find docs -mindepth 1 -type d | while read d; do
  if [ -z "$(ls -A "$d" 2>/dev/null)" ]; then
    touch "$d/.gitkeep"
  fi
done
```

**Rules:**
- Use `mkdir -p` — safe to run on existing trees; never fails if folder already exists.
- Never delete or overwrite existing files.
- Report how many folders were created vs already existed.

---

## Project-control scaffold

**Scope:** Mode 1 and Mode 2 (always).

Creates the minimal `docs/project-control/open-items/` control plane so `util-open-items`
can run `sync` immediately after the first artefact is authored. Without this structure,
the first sync fails with a missing-path error.

**Files created:**

```bash
mkdir -p docs/project-control/open-items/archive
touch docs/project-control/open-items/archive/.gitkeep
```

Then write two stub files:

**`docs/project-control/open-items/open-items.md`** — empty ledger. Copy the canonical
ledger skeleton from [`util-open-items/references/template.md`](../util-open-items/references/template.md)
§1 verbatim (title, "How rows arrive here", an empty `## Live items` table, "Status
snapshot", "See also"; `_None at present._` initial state).

**`docs/project-control/open-items/README.md`** — operator orientation. Copy the content of
the existing `docs/project-control/open-items/README.md` in the kit as-is — it is
project-agnostic and applies verbatim to any project scaffolded with this skill.

**Safety rules:**
- If `docs/project-control/open-items/open-items.md` already exists: skip creation entirely
  and report "control plane already present".
- Never overwrite an existing ledger.

---

## `.gitignore` check

Run at the end of Mode 1 (step 5). If `var/reports/` is not in `.gitignore`:

1. Surface in the closing report: "⚠️ `var/reports/` is not in `.gitignore`. Generated
   audit and migration reports should not be committed. Add to `.gitignore`:"
   ```
   var/reports/
   ```
2. Do NOT automatically modify `.gitignore` — the user may have a reason for tracking
   reports. Surface it as a suggestion, not an auto-fix.

---

## index.md generation

The index.md is a **point-in-time snapshot** — a navigation hub with live status detected
at the moment the skill runs. It is not a truly dynamic dashboard; run Mode 3 to refresh.

Full template and detection commands in `references/index-template.md`.

**Status detection per step:**

```bash
# ✅ Done        — file/folder found AND < 50% lines are _TODO_
# 🔄 In progress — file/folder found AND ≥ 50% lines are _TODO_
# ⬜ Not started — no file/folder found

check_status() {
  local path="$1"
  if [ -f "$path" ]; then
    total=$(wc -l < "$path")
    todos=$(grep -c '_TODO_' "$path" 2>/dev/null || echo 0)
    [ "$total" -gt 0 ] && ratio=$(( todos * 100 / total )) || ratio=0
    [ "$ratio" -ge 50 ] && echo "🔄" || echo "✅"
  elif [ -d "$path" ] && [ -n "$(ls "$path"/*.md 2>/dev/null)" ]; then
    echo "✅"
  else
    echo "⬜"
  fi
}
```

**index.md frontmatter:** `index.md` is an OKF reserved file, **not** an artefact concept
document, so it does **not** carry the standard artefact frontmatter block. The bundle-root
`docs/index.md` carries only the OKF version declaration:
- `okf_version: "0.1"` — the sole frontmatter field (per `rules/artefact-frontmatter.md` §Reserved files)
- any sub-folder `index.md` a skill emits is entirely frontmatter-free
- freshness is shown in the body (`> **Last refreshed:**`), refreshed by Mode 3 in seconds

---

## CLAUDE.md update rules

Mirrors the wire-mode pattern from `business-vision`.

1. Check if `CLAUDE.md` exists at the project root.
2. Check if a stack pointer is already present:
   ```bash
   grep -qi 'index\.md\|metamodel.*scaffold\|documentation stack' CLAUDE.md 2>/dev/null \
     && echo "already wired"
   ```
3. **If already wired:** report and skip. Never duplicate.
4. **If `CLAUDE.md` exists but no stack pointer:** append the following block (Edit tool,
   never overwrite):

   ```markdown

   ## Documentation stack (read at session start)

   This project uses the homemade-claude-kit strategic-architecture metamodel.

   - **Index:** [`docs/index.md`](docs/index.md) — live artefact status table; run
     `util-metamodel-scaffold` Mode 3 to refresh.
   - **Build order:** `rules/metamodel.md` — 16 steps (Vision → Implementation plans), start at Step 0 (`business-vision`); the `discovery-*` family (idea, research, workshop) is cross-cutting and runs alongside any step.
   - **Audit:** run `util-metamodel-audit` for full health checks
   - **Scaffolded:** {YYYY-MM-DD}

   Before doing any documentation work: read `docs/index.md` to know which steps are
   complete (✅), in progress (🔄), or not started (⬜), and which skill to invoke next.
   ```

5. **If `CLAUDE.md` does not exist:** create it with the block above as the only content,
   wrapped in a minimal header:

   ```markdown
   # Project Context

   ## Documentation stack (read at session start)

   This project uses the homemade-claude-kit strategic-architecture metamodel.

   - **Index:** [`docs/index.md`](docs/index.md) — live artefact status table; run
     `util-metamodel-scaffold` Mode 3 to refresh.
   - **Build order:** `rules/metamodel.md` — 16 steps (Vision → Implementation plans), start at Step 0 (`business-vision`); the `discovery-*` family (idea, research, workshop) is cross-cutting and runs alongside any step.
   - **Audit:** run `util-metamodel-audit` for full health checks
   - **Scaffolded:** {YYYY-MM-DD}

   Before doing any documentation work: read `docs/index.md` to know which steps are
   complete (✅), in progress (🔄), or not started (⬜), and which skill to invoke next.
   ```

**Safety rules:**
- NEVER overwrite or truncate an existing `CLAUDE.md`. Append only.
- NEVER duplicate the stack pointer if already present.
- If the existing `CLAUDE.md` already has a "Documentation stack" or "metamodel" section,
  ask the user whether to update it or skip.
- Always show the user exactly what was appended before closing.

---

## Sizing heuristics

| Element | Value |
|---|---|
| Run cadence | Once per project (Mode 1/2); Mode 3 as needed |
| Time to run Mode 1 | < 10 seconds (mkdir + status detection) |
| index.md refresh cadence | After completing each stack step, or before a sprint review |
| Folders created | ~22 directories (includes the three `docs/discovery/{ideation,interviews,workshops}/` folders) |

---

## Closing report to the user

After any mode, summarise in 5–6 lines:

1. **Mode run** + **docs root**.
2. **Folders created** (N new) / **already existed** (N skipped).
3. **Project-control plane** — created / already present / skipped (Mode 3).
4. **index.md** — written / refreshed / skipped; current status breakdown (✅ N / 🔄 N / ⬜ N).
5. **CLAUDE.md** — updated / created / skipped / already wired.
6. **`.gitignore`** — `var/reports/` present ✅ or missing ⚠️ (suggest the one-liner to add).

**Next step:** always `business-vision` Mode 1 (scaffold) → Mode 2 (fill) → Mode 3 (wire)
unless the user has a specific entry point in mind (e.g. jumping straight to `spec-prd`
for a single-feature engagement, or `business-capability-map` for an existing system).

---

## Reference materials

- **`references/folder-catalogue.md`** — complete folder list with `mkdir -p` commands.
- **`references/index-template.md`** — index.md skeleton and per-step status detection bash commands.
- **`references/methodology-references.md`** — rationale for the single universal tree, `.gitkeep` discipline, control-plane scope (`docs/project-control/`), and `.gitignore` policy.

---

## Checklist

Before declaring the work done:

- [ ] Step 0 answered (Mode 1) or mode detected from context.
- [ ] Pre-flight check run: docs root inspected for existing markdown files; user confirmed before proceeding if content was found.
- [ ] All canonical folders created (`mkdir -p`).
- [ ] `.gitkeep` placed in every empty leaf folder.
- [ ] Project-control plane created or already present — acknowledged in closing report.
- [ ] `.gitignore` checked; result surfaced in closing report.
- [ ] `docs/index.md` written (Modes 1 + 3) with `last_reviewed` set to today, or skipped with acknowledgement (Mode 2).
- [ ] `docs/index.md` contains a row for every canonical step.
- [ ] `docs/index.md` is the OKF bundle root: frontmatter contains only `okf_version: "0.1"` (no artefact frontmatter block, per `rules/artefact-frontmatter.md` §Reserved files).
- [ ] CLAUDE.md updated / created (Mode 1 with option 2A) or skipped with acknowledgement.
- [ ] No artefact content files created — folders + `.gitkeep` + index.md + control-plane stubs only.
- [ ] Closing report delivered with next-step recommendation.
