# Check Catalogue — util-metamodel-audit

For each of the 16 checks: bash detection pattern, interpretation rules, severity, and proposed fix template. Claude reads this file during audit execution to know exactly how to run each check.

---

## Check 1 — Stack progress

**What:** verifies which of the 11 canonical output paths exist.

**Detection:**
```bash
# Run for each step — adapt path per step number
find docs -maxdepth 1 -name "VISION.md" 2>/dev/null                              # Step 0
find docs/business -maxdepth 1 -name "01a-personas.md" 2>/dev/null
find docs -maxdepth 4 \( -name "business-model-canvas.md" -o -name "lean-canvas.md" \) 2>/dev/null
find docs/business -maxdepth 1 -name "03a-capability-map.md" 2>/dev/null
find docs/business -maxdepth 1 -name "04a-value-streams.md" 2>/dev/null
find docs/business -maxdepth 1 -name "04b-objectives.md" 2>/dev/null          # Step 4.5
find docs/business/05a-processes -name "proc-*.md" 2>/dev/null | head -1
find docs/business/06a-models -name "qm-*.md" 2>/dev/null | head -1
find docs/product-specs -maxdepth 1 -name "07a-fbs.md" 2>/dev/null
find docs/plans -maxdepth 1 -name "delivery-roadmap.md" 2>/dev/null   # Step 8
find docs/product-specs -maxdepth 1 -name "09a-quality-attributes.md" 2>/dev/null
find docs/product-specs/use-cases -name "uc-*.md" 2>/dev/null | head -1          # Step 9.5
find docs/product-specs/prds -name "prd-*.md" 2>/dev/null | head -1
find docs/plans/active -maxdepth 1 -name "*_exec_*.md" 2>/dev/null | head -1
find docs/domain -maxdepth 1 -name "02b-bounded-contexts.md" 2>/dev/null           # Step 2b
find docs/domain -maxdepth 1 -name "02c-glossary.md" 2>/dev/null                  # Step 2c
find docs/domain/07b-models -name "*.md" 2>/dev/null | head -1             # Step 7b (per BC)
find docs/architecture/interfaces -name "*.md" ! -name "cli-*.md" 2>/dev/null | head -1  # Step 7c (service contract, per BC)
find docs/architecture/interfaces -name "cli-*.md" 2>/dev/null | head -1                  # CLI contract (supporting skill, per tool)
find docs/architecture/c4 -name "workspace.dsl" 2>/dev/null                       # arch-structurizr foundation
find docs/architecture/c4/views -name "*.svg" 2>/dev/null | head -1               # arch-c4 rendered views (committed)
find docs/architecture/arc42 -name "02-constraints.md" 2>/dev/null               # arch-arc42 constraints mode
find docs/architecture/arc42 -name "03-context.md" 2>/dev/null                    # arch-c4 context mode
find docs/architecture/arc42 -name "04-solution-strategy.md" 2>/dev/null          # arch-arc42 solution-strategy mode
find docs/architecture/arc42 -name "05-building-blocks.md" 2>/dev/null            # arch-c4 container + component modes
find docs/architecture/arc42 -name "06-runtime-view.md" 2>/dev/null               # arch-c4 runtime mode
find docs/architecture/arc42 -name "07-deployment.md" 2>/dev/null                 # arch-c4 deployment mode
find docs/architecture/arc42 -name "08-cross-cutting-concepts.md" 2>/dev/null     # arch-arc42 cross-cutting mode
find docs/architecture/arc42 -name "11-risks.md" 2>/dev/null                      # arch-arc42 risks mode
```

**Status assignment:**
- ✅ Done — canonical file/folder found
- 🔄 In progress — file found but >50% _TODO_ content
- ⬜ Not started — no file found

**Severity:** Info

**Proposed fix template:** "Run `{skill}` Mode 1 (scaffold) to create the missing artefact."

---

## Check 2 — Folder placement

**What:** finds markdown files that exist but are not in their canonical location per the stack rule.

**Detection:**
```bash
find docs -name "*.md" | while read f; do echo "$f"; done
```
Then compare each path against the canonical map:
- `VISION.md` → must be directly under `docs/` (not nested deeper — singleton)
- `01a-personas.md` → must be at `docs/business/01a-personas.md` (flat file)
- `02a-bmc.md` / `02a-lean-canvas.md` → must be at `docs/business/` (flat file)
- `03a-capability-map.md` → must be at `docs/business/03a-capability-map.md` (flat file)
- `04a-value-streams.md` → must be at `docs/business/04a-value-streams.md` (flat file)
- `04b-objectives.md` → must be at `docs/business/04b-objectives.md` (flat file)
- `*-process.md` → must be under `docs/business/05a-processes/`
- `07a-fbs.md` → must be at `docs/product-specs/07a-fbs.md` (flat file)
- `delivery-roadmap.md` → must be at `docs/plans/delivery-roadmap.md` (flat file)
- `09a-quality-attributes.md` → must be at `docs/product-specs/09a-quality-attributes.md` (flat file)
- `uc-*.md` → must be under `docs/product-specs/use-cases/` (one file per use case + `index.md`)
- `prd-*.md` → must be under `docs/product-specs/prds/`
- `IDEA-*.md` → must be under `docs/discovery/ideation/` (filename matches `IDEA-NNNN-{slug}.md`)
- `interview-*.md`, `research-synthesis-*.md`, `research-plan-*.md` → must be under `docs/discovery/interviews/`
- `workshop-*.md`, `workshop-synthesis-*.md` → must be under `docs/discovery/workshops/`
- `*.md` under `docs/architecture/decisions/` → ADRs, correct
- `{bc-slug}.md` (no `cli-` prefix) under `docs/architecture/interfaces/` → service contract (`arch-service-contract`), correct
- `cli-{slug}.md` under `docs/architecture/interfaces/` → CLI contract (`arch-cli-contract`), correct
- `*.md` under `docs/architecture/` but NOT in `decisions/`, `interfaces/`, `research/`, `c4/`, or `arc42/` → likely misplaced architecture file
- `workspace.dsl` → must be at `docs/architecture/c4/workspace.dsl` (singleton — `arch-structurizr` foundation)
- `render.sh` → must be at `docs/architecture/c4/render.sh` (executable; `arch-structurizr` writes; `chmod +x` expected)
- `*.svg` under `docs/architecture/c4/views/` → committed C4 renders from `arch-c4`; correct
- `*.puml` under `docs/architecture/c4/` (anywhere) → intermediate PlantUML export; should be gitignored, not committed
- `02-constraints.md`, `04-solution-strategy.md`, `08-cross-cutting-concepts.md`, `11-risks.md` → must be under `docs/architecture/arc42/` (`arch-arc42` writes)
- `03-context.md`, `05-building-blocks.md`, `06-runtime-view.md`, `07-deployment.md` → must be under `docs/architecture/arc42/` (`arch-c4` writes; one file per arc42 section)
- `*.md` under `docs/architecture/arc42/` not matching the canonical eight (`02`, `03`, `04`, `05`, `06`, `07`, `08`, `11`) → likely misplaced
- `getting-started.md` → must be at `docs/dev-guides/getting-started.md` (singleton — `dev-getting-started` skill)
- `{tech-slug}.md` under `docs/dev-guides/` (no `research/` subfolder, not `getting-started.md`) → correct (`dev-stack-guide` output)
- `{tech-slug}-research.md` under `docs/dev-guides/research/` → correct (`dev-stack-guide` research scratch)
- `*.md` under `docs/dev-guides/` but NOT matching the above patterns → likely misplaced

**Severity:** Warning

**Proposed fix template:** "Move `{file}` to `{canonical_path}` and update any links pointing to the old location."

---

## Check 3 — Internal links

**What:** finds relative markdown links that resolve to non-existent files.

**Detection:**
```bash
grep -rn '\[.*\](\.\./' docs/ --include="*.md" | grep -v '^\s*<!--' | grep -v '```'
```
For each match, extract the relative path, resolve it from the source file's directory, and check existence:
```bash
# pseudo-pattern per link
source_dir=$(dirname "$source_file")
resolved=$(realpath --relative-to=. "$source_dir/$link_target" 2>/dev/null)
[ -f "$resolved" ] || echo "BROKEN: $source_file → $link_target"
```
Also check anchor fragments: if link is `file.md#section-id`, verify the heading `# Section Id` exists in `file.md`.

**Severity:** Error

**Proposed fix template:** "Update link in `{source_file}` line {N}: `{link_text}` → correct path is `{correct_path}` (or remove if target was deleted)."

---

## Check 4 — External links

**What:** finds dead external URLs and links missing a `Last verified` date.

**Detection — dead links:**
```bash
grep -roh 'https\?://[^)> "]*' docs/ --include="*.md" | sort -u | while read url; do
  status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 --location "$url" 2>/dev/null)
  [ "$status" -ge 400 ] && echo "DEAD ($status): $url"
done
```

**Detection — missing Last verified:**
```bash
# Find lines with http links NOT preceded by "Last verified" within 3 lines
grep -rn 'https\?://' docs/ --include="*.md" | grep -v 'Last verified'
```

**Severity:**
- 4xx/5xx response → Error
- 3xx permanent redirect → Warning (update the URL)
- Missing `Last verified` date → Warning

**Proposed fix template:**
- Dead link: "Replace or remove URL `{url}` in `{file}` line {N}. Suggested replacement: search for updated URL."
- Missing date: "Add `Last verified: {today}` on the line following the URL in `{file}`."

---

## Check 5 — ID cross-references

**What:** finds IDs referenced in one doc that have no definition in their owning artefact.

**ID patterns and owning artefacts:**

| ID format | Regex | Owning artefact |
|---|---|---|
| `P-NN` | `\bP-[0-9]{2}\b` | `docs/business/01a-personas.md` |
| `C-N.M` or `C1.1` | `\bC[0-9]+\.[0-9]+\b` | `docs/business/03a-capability-map.md` |
| `VS-N` | `\bVS-[0-9]+\b` | `docs/business/04a-value-streams.md` |
| `VS-N.M` | `\bVS-[0-9]+\.[0-9]+\b` | `docs/business/04a-value-streams.md` |
| `C-N.M.FXX` | `\bC-[0-9]+\.[0-9]+\.F[0-9]+\b` | `docs/product-specs/07a-fbs.md` |
| `BC-NN` | `\bBC-[0-9]{2}\b` | `docs/domain/02b-bounded-contexts.md` |
| `BC-NN.GT-NN` | `\bBC-[0-9]{2}\.GT-[0-9]{2}\b` | `docs/domain/02c-glossary.md` |
| `BC-NN.AGG-NN` | `\bBC-[0-9]{2}\.AGG-[0-9]{2}\b` | `docs/domain/07b-models/{bc-slug}.md` |
| `BC-NN.ENT-NN` | `\bBC-[0-9]{2}\.ENT-[0-9]{2}\b` | `docs/domain/07b-models/{bc-slug}.md` |
| `BC-NN.VO-NN` | `\bBC-[0-9]{2}\.VO-[0-9]{2}\b` | `docs/domain/07b-models/{bc-slug}.md` |
| `BC-NN.EVT-NN` | `\bBC-[0-9]{2}\.EVT-[0-9]{2}\b` | `docs/domain/07b-models/{bc-slug}.md` |
| `OBJ-NN` | `\bOBJ-[0-9]{2}\b` | `docs/business/04b-objectives.md` |
| `KR-NN.M` | `\bKR-[0-9]{2}\.[0-9]\b` | `docs/business/04b-objectives.md` |
| `E-NN` | `\bE-[0-9]{2}\b` | `docs/plans/delivery-roadmap.md` |
| `QA-[A-Z]{2}[0-9]{2}` | `\bQA-[A-Z]{2}[0-9]{2}\b` | `docs/product-specs/09a-quality-attributes.md` |
| `ADR-NNNN` | `\bADR-[0-9]{4}\b` | `docs/architecture/decisions/` |
| `Research-NNNN` | `\bResearch-[0-9]{4}\b` | `docs/architecture/research/` |
| `IDEA-NNNN` | `\bIDEA-[0-9]{4}\b` | `docs/discovery/ideation/` (filename prefix `IDEA-NNNN-{slug}.md`) |
| `CO-NN` | `\bCO-[0-9]{2}\b` | `docs/business/01b-competitive-landscape/` |
| `UC-NN` | `\bUC-[0-9]{2}\b` | `docs/product-specs/use-cases/` |
| `PRD-NNNN` | `\bPRD-[0-9]{4}\b` | `docs/product-specs/prds/prd-*.md` |
| `CS-N` | `\bCS-[0-9]+\b` | `docs/business/02a-bmc.md` |
| `VP-N` | `\bVP-[0-9]+\b` | `docs/business/02a-bmc.md` |
| `CH-N` | `\bCH-[0-9]+\b` | `docs/business/02a-bmc.md` |
| `CR-N` | `\bCR-[0-9]+\b` | `docs/business/02a-bmc.md` |
| `RS-N` | `\bRS-[0-9]+\b` | `docs/business/02a-bmc.md` |
| `KA-N` | `\bKA-[0-9]+\b` | `docs/business/02a-bmc.md` |
| `KP-N` | `\bKP-[0-9]+\b` | `docs/business/02a-bmc.md` |
| `CT-N` | `\bCT-[0-9]+\b` | `docs/business/02a-bmc.md` |
| `BC-NN.CTR-NN` | `\bBC-[0-9]{2}\.CTR-[0-9]{2}\b` | `docs/architecture/interfaces/{bc-slug}.md` |
| `CTR-NN` | `\bCTR-[0-9]{2}\b` | `docs/architecture/interfaces/{slug}.md` (product-level) |
| `BC-NN.CLI-NN` | `\bBC-[0-9]{2}\.CLI-[0-9]{2}\b` | `docs/architecture/interfaces/cli-{slug}.md` |
| `CLI-NN` | `\bCLI-[0-9]{2}\b` | `docs/architecture/interfaces/cli-{slug}.md` (product-level) |
| `CLI-NN.CMD-NN` | `\bCLI-[0-9]{2}\.CMD-[0-9]{2}\b` | `docs/architecture/interfaces/cli-{slug}.md` |
| `SYS-NN` | `\bSYS-[0-9]{2}\b` | `docs/architecture/c4/workspace.dsl` (DSL identifier `SYS_NN` in `softwareSystem` block) |
| `CON-NN` | `\bCON-[0-9]{2}\b` | `docs/architecture/c4/workspace.dsl` (DSL identifier `CON_NN` in `container` block) |
| `CMP-NN` | `\bCMP-[0-9]{2}\b` | `docs/architecture/c4/workspace.dsl` (DSL identifier `CMP_NN` in `component` block) |
| `DN-NN` | `\bDN-[0-9]{2}\b` | `docs/architecture/c4/workspace.dsl` (DSL identifier `DN_NN` in `deploymentNode` block) |
| `SCN-NN` | `\bSCN-[0-9]{2}\b` | `docs/architecture/arc42/06-runtime-view.md` (`arch-arc42` runtime mode — owns §6 + SCN-NN per ADR-0004; `arch-c4` only renders the dynamic-view SVG keyed by it) |
| `CST-NN` | `\bCST-[0-9]{2}\b` | `docs/architecture/arc42/02-constraints.md` (`arch-arc42` constraints mode) |
| `CC-NN` | `\bCC-[0-9]{2}\b` | `docs/architecture/arc42/08-cross-cutting-concepts.md` (`arch-arc42` cross-cutting mode) |
| `RSK-NN` | `\bRSK-[0-9]{2}\b` | `docs/architecture/arc42/11-risks.md` (`arch-arc42` risks mode) |

**Detection (example for P-NN):**
```bash
# Collect all P-NN references across all docs
grep -roh '\bP-[0-9]\{2\}\b' docs/ --include="*.md" | grep -oP 'P-[0-9]{2}' | sort -u > /tmp/p_refs.txt
# Collect all P-NN definitions in personas.md
grep -oh '\bP-[0-9]\{2\}\b' docs/business/01a-personas.md 2>/dev/null | sort -u > /tmp/p_defs.txt
# Find refs with no definition
comm -23 /tmp/p_refs.txt /tmp/p_defs.txt
```
Repeat for each ID type.

**Severity:** Error

**Proposed fix template:** "ID `{ID}` used in `{source_file}` is not defined in `{owning_artefact}`. Either define it there or correct the reference."

---

## Check 6 — ID integrity

**What:** finds duplicate IDs within a namespace and malformed ID formats.

**Detection — duplicates:**
```bash
# Example for P-NN in personas.md
grep -oh '\bP-[0-9]\{2\}\b' docs/business/01a-personas.md 2>/dev/null | sort | uniq -d
```

**Detection — malformed format:**
```bash
# Single-digit persona IDs (P-1 instead of P-01)
grep -roh '\bP-[0-9]\b' docs/ --include="*.md"
# Single-digit epic IDs
grep -roh '\bE-[0-9]\b' docs/ --include="*.md"
# QA IDs with wrong format
grep -roh '\bQA-[^A-Z ]' docs/ --include="*.md"
# Research IDs with wrong digit count (must be 4-digit)
grep -roh '\bResearch-[0-9]\{1,3\}\b' docs/ --include="*.md"
# Competitor IDs with wrong digit count (must be 2-digit)
grep -roh '\bCO-[0-9]\b' docs/ --include="*.md"
```

```bash
# CTR IDs with single digit (CTR-1 instead of CTR-01)
grep -roh '\bCTR-[0-9]\b' docs/ --include="*.md"
# CLI IDs with single digit (CLI-1 instead of CLI-01)
grep -roh '\bCLI-[0-9]\b' docs/ --include="*.md"
# CMD IDs with single digit (CMD-1 instead of CMD-01)
grep -roh '\bCMD-[0-9]\b' docs/ --include="*.md"
```

**Severity:** Error

**Proposed fix template:**
- Duplicate: "Renumber `{ID}` in `{file}` — two definitions of the same ID will corrupt cross-references."
- Malformed: "Fix `{ID}` in `{file}` to canonical format `{correct_format}` and update all references."

---

## Check 7 — Dependency enforcement

**What:** checks that prerequisites defined in the stack DAG exist when a downstream artefact is present.

**Dependency rules to enforce:**

| If this exists | Then this must also exist |
|---|---|
| `docs/business/04a-value-streams.md` | `docs/business/03a-capability-map.md` (stages consume capabilities) |
| `docs/product-specs/07a-fbs.md` | `docs/business/03a-capability-map.md` (FBS inherits L0+L1) |
| `docs/plans/delivery-roadmap.md` | `docs/product-specs/07a-fbs.md` (epics group FBS functionalities) |
| `docs/product-specs/09a-quality-attributes.md` | `docs/product-specs/07a-fbs.md` (QA reads FBS differentiators) |
| Any `docs/product-specs/prds/prd-*.md` | `docs/plans/delivery-roadmap.md` (PRDs map to E-NN epics) |
| Any `docs/product-specs/prds/prd-*.md` | `docs/product-specs/09a-quality-attributes.md` (PRDs reference QA-XXNN) |
| Any `plans/active/*/` plan | Corresponding `docs/product-specs/prds/prd-*.md` |
| `docs/domain/02c-glossary.md` exists | `docs/domain/02b-bounded-contexts.md` must also exist (glossary is scoped to BCs) |
| `docs/domain/07b-models/{bc-slug}.md` exists | `docs/domain/02b-bounded-contexts.md` must exist (domain model is namespaced by BC) |
| `docs/domain/07b-models/{bc-slug}.md` exists | `docs/domain/02c-glossary.md` must exist (entity names must match glossary terms) |
| `docs/business/04b-objectives.md` exists | `docs/business/04a-value-streams.md` must also exist (objectives consume pain index from VS) |
| Any `docs/product-specs/prds/prd-*.md` | If `docs/business/04b-objectives.md` exists, the PRD should reference ≥1 `OBJ-NN` in §0 |
| `docs/architecture/interfaces/{bc-slug}.md` exists (not `cli-*.md`) | `docs/domain/07b-models/{bc-slug}.md` must also exist — service contract derives from domain model (AGG/ENT/EVT) |
| `docs/architecture/interfaces/{bc-slug}.md` exists (not `cli-*.md`) | `docs/domain/02b-bounded-contexts.md` must also exist — BC-NN namespace for CTR-NN IDs |

**Detection (example):**
```bash
[ -f "docs/product-specs/07a-fbs.md" ] && \
  [ ! -f "docs/business/03a-capability-map.md" ] && \
  echo "WARNING: FBS exists but 03a-capability-map.md missing"

[ -f "docs/domain/02c-glossary.md" ] && \
  [ ! -f "docs/domain/02b-bounded-contexts.md" ] && \
  echo "WARNING: Glossary exists but 02b-bounded-contexts.md missing"

find docs/domain/07b-models -name "*.md" 2>/dev/null | while read f; do
  [ ! -f "docs/domain/02b-bounded-contexts.md" ] && \
    echo "WARNING: Domain model exists but 02b-bounded-contexts.md missing: $f"
  [ ! -f "docs/domain/02c-glossary.md" ] && \
    echo "WARNING: Domain model exists but glossary missing: $f"
done

find docs/architecture/interfaces -name "*.md" ! -name "cli-*.md" 2>/dev/null | while read f; do
  slug=$(basename "$f" .md)
  [ ! -f "docs/domain/07b-models/${slug}.md" ] && \
    echo "WARNING: Service contract exists for '${slug}' but no domain model at docs/domain/07b-models/${slug}.md"
  [ ! -f "docs/domain/02b-bounded-contexts.md" ] && \
    echo "WARNING: Service contract exists but 02b-bounded-contexts.md missing"
done
```

**Severity:** Warning

**Proposed fix template:** "Create the missing prerequisite artefact using `{skill}` before proceeding. The downstream artefact `{file}` has soft-links that will be `_TODO_` until the prerequisite exists."

### Sub-check 7a — arc42 content-type ownership (ADR-0004)

arc42 §3/§5/§7 are co-written: `arch-c4` owns the *generated block* (diagram + DSL-derived table) inside `<!-- arch-c4:start key=… -->` / `<!-- arch-c4:end key=… -->` markers; `arch-arc42` owns all prose outside them. §6/§8 figures are pulled via a `<!-- arch-figure … -->` declared-dependency block. Verify the joins:

**Rules:**

| Condition | Check |
|---|---|
| An `arch-c4:start key=K` marker exists | A matching `arch-c4:end key=K` exists (balanced, same key) — **Error** if unbalanced |
| A `<!-- arch-figure … source=arch-uml path=P -->` block exists | `P` resolves to an existing SVG under `docs/architecture/diagrams/views/` (or is a `_TODO_` soft-reference) — **Warning** if missing |
| A `<!-- arch-figure … source=arch-c4 path=P -->` block exists | `P` resolves to an existing SVG under `docs/architecture/c4/views/` (or `_TODO_`) — **Warning** if missing |
| `source=arch-uml` but `path` is under `c4/views/` (or vice-versa) | Source/path mismatch — **Warning** |
| An `arch-figure` block carries `scenario=SCN-NN` / `concept=CC-NN` / `realises=UC-NN` | That ID resolves in its owning artefact (Check 5 reuse) — **Warning** |
| A rendered SVG under `c4/views/` or `diagrams/views/` is referenced by **no** arc42/doc embed | Orphaned figure (Check 13 reuse) — **Info** |
| An `arch-figure` SVG's mtime is newer than the consuming section's `last_reviewed` | Possible prose drift — **Info** (never Error; re-render alone fires it) |

**Detection:**
```bash
# Marker balance across arc42
for f in docs/architecture/arc42/0{3,5,7}-*.md; do
  [ -f "$f" ] || continue
  s=$(grep -c 'arch-c4:start' "$f"); e=$(grep -c 'arch-c4:end' "$f")
  [ "$s" -ne "$e" ] && echo "UNBALANCED arch-c4 markers ($s start / $e end): $f"
done
# Declared-figure paths resolve (skip _TODO_ soft-references)
grep -rhoE '<!-- arch-figure[^>]*path=([^ ]+)' docs/architecture/arc42/ 2>/dev/null \
  | grep -oE 'path=[^ ]+' | sed 's/path=//' | while read p; do
    case "$p" in *_TODO_*) continue;; esac
    [ -f "docs/architecture/$(echo "$p" | sed 's#^\.\./##')" ] || echo "FIGURE MISSING: $p"
  done
```

**Severity:** Error (unbalanced markers) · Warning (missing/mismatched figure or unresolved ID) · Info (orphan, freshness)

**Proposed fix template:** "arc42 figure/marker drift in `{file}`: {detail}. Re-run `arch-c4`/`arch-uml` to (re)produce the figure, or fix the `arch-figure` block / markers. Per ADR-0004, `arch-c4` owns content inside markers; `arch-arc42` owns the prose and the figure block."

---

## Check 8 — _TODO_ density

**What:** counts unfilled `_TODO_` placeholders per file and computes completeness %.

**Detection:**
```bash
find docs -name "*.md" | while read f; do
  todos=$(grep -c '_TODO_' "$f" 2>/dev/null || echo 0)
  total_lines=$(wc -l < "$f")
  echo "$todos $total_lines $f"
done | sort -rn
```

**Interpretation:**
- 0 _TODO_ → complete
- 1–10 _TODO_ → mostly filled; normal for active work
- >50% of lines contain _TODO_ → scaffolded but not filled; flag as Info
- Any _TODO_ in a mandatory field (§8 KPIs, §5.2 assumptions, persona `Goals`) → flag specifically

**Severity:** Info (density); Warning (mandatory field _TODO_)

**Proposed fix template:** "Fill `{field}` in `{file}` using `{skill}` Mode 2 (fill). Priority: {high/medium/low}."

---

## Check 9 — Mandatory sections

**What:** verifies that each file type contains its required sections.

**Rules per file type:**

| File type | Mandatory sections | Detection pattern |
|---|---|---|
| `*-process.md` | `## §8 KPIs` or `## KPIs`, `## Open Items` (canonical document-level section per `rules/open-items-governance.md` §1; legacy variants such as the older §11 unresolved-work heading are forbidden), `## §0 Master flow` | `grep -q 'KPI\|§8'` |
| `docs/business/06a-models/*.md` | `§5.2` or `Implicit assumptions`, `§6` or `Scenario Matrix`, `§7` or `Value capture` | `grep -q '5\.2\|Implicit assumptions'` |
| `01a-personas.md` | `## Persona Backlog`, `## Personas`, `## Persona Template` | `grep -q 'Persona Backlog'` |
| `03a-capability-map.md` | `## L0 axis`, `## Global overview`, `## Capability index` | `grep -q 'L0 axis\|Capability index'` |
| `04a-value-streams.md` | `## Catalogue`, `## Value Streams` | `grep -q '## Catalogue'` |
| `07a-fbs.md` | At least one `### C` capability heading with a functionality table | `grep -q '### C[0-9]'` |
| `use-cases/uc-*.md` | `Scope` + `Level` header fields, `## Main Success Scenario`, `## Extensions` | `grep -q '## Main Success Scenario'` |
| `delivery-roadmap.md` | Epic table with `E-NN` IDs | `grep -q 'E-[0-9][0-9]'` |
| `09a-quality-attributes.md` | ISO characteristic headings (`Performance Efficiency`, `Security`, `Reliability`, etc.) | `grep -q 'Performance Efficiency\|Security\|Reliability'` |
| `docs/product-specs/prds/prd-*.md` | `§0 Architecture Traceability` or traceability block, `## Acceptance criteria` | `grep -q 'Traceability\|Acceptance'` |
| `04b-objectives.md` | At least one `OBJ-NN` heading, `## Changelog`, `## Objective × Epic` section | `grep -q 'OBJ-[0-9][0-9]\|Changelog'` |
| `VISION.md` | `## The Elevator Pitch`, `## What We Are NOT`, `## North Star Metric`, `## Changelog` | `grep -q 'Elevator Pitch\|North Star'` |
| `02b-bounded-contexts.md` | `## Subdomain catalogue`, at least one `BC-NN` entry | `grep -q 'BC-[0-9][0-9]'` |
| `02c-glossary.md` | At least one BC section, `## Changelog` | `grep -q '## Changelog'` |
| `docs/domain/07b-models/{bc-slug}.md` | `## Aggregate catalogue`, `## Domain event catalogue`, Mermaid `classDiagram` | `grep -q 'Aggregate catalogue\|classDiagram'` |
| `docs/architecture/research/*.md` | `## Questions`, `## Findings`, `## Changelog` | `grep -q '## Questions\|## Findings'` |
| `docs/business/01b-competitive-landscape/*.md` | `## Porter Five Forces`, `## Competitor Profiles` or `## CO-` heading | `grep -q 'Five Forces\|CO-[0-9]'` |
| `docs/architecture/interfaces/*.md` (not `cli-*.md`) | `## §0 Traceability`, `## §3 Error contract`, `## §4 Versioning & deprecation policy`, `## §5 Security surface`, `## Open Items`, `## Changelog` | `grep -q '§0 Traceability\|§3 Error contract'` |
| `docs/architecture/interfaces/cli-*.md` | `## §0 Traceability`, `## §2 Command catalogue`, `## §5 Output contract`, `## §7 Error contract`, `## Open Items`, `## Changelog` | `grep -q 'Command catalogue\|§7 Error contract'` |
| `docs/discovery/ideation/IDEA-*.md` | `## Problem statement`, `## Not doing`, `## Open Items`, `## Changelog`; frontmatter must include `idea_id`, `domain`, `lifecycle`, `graduates_to` | `grep -q '## Problem statement\|## Not doing'` and `grep -q '^idea_id:\|^lifecycle:\|^graduates_to:'` |
| `docs/architecture/c4/workspace.dsl` | `workspace "..."` block, `model { ... }` block, `views { ... }` block, at least one `systemContext` view | `grep -q '^workspace\|^[[:space:]]*model {\|^[[:space:]]*views {'` |
| `docs/architecture/c4/render.sh` | Pinned image (no `:latest`), `validate` step before `export`, `--user` flag on every `docker run`, exit codes documented in header | `grep -q 'STRUCTURIZR_VERSION=' && grep -q 'validate -workspace' && grep -q -- '--user'` |
| `docs/architecture/arc42/02-constraints.md` | `# 2. Architecture Constraints`, `## 2.1 Technical Constraints`, `## 2.2 Organizational Constraints`, `## 2.3 Legal and Regulatory Constraints`, `## Open Items` | `grep -q '## 2.1 Technical\|## 2.2 Organizational\|## 2.3 Legal'` |
| `docs/architecture/arc42/03-context.md` | `# 3. Context and Scope`, `## 3.1 Business Context` (with embedded `systemContext.svg`), `## 3.2 Technical Context`, `## Open Items` | `grep -q '## 3.1 Business Context\|## 3.2 Technical Context'` |
| `docs/architecture/arc42/04-solution-strategy.md` | `# 4. Solution Strategy`, `## 4.1 Technology Decisions`, `## 4.2 Top-Level Decomposition`, `## 4.3 Quality Goal`, `## Open Items` | `grep -q '## 4.1 Technology\|## 4.3 Quality Goal'` |
| `docs/architecture/arc42/05-building-blocks.md` | `# 5. Building Block View`, `## 5.1 Whitebox Overall System` with containers table including `Domain aggregates implemented` column, at least one `## 5.2.x` drill, `## Open Items` | `grep -q '## 5.1 Whitebox\|Domain aggregates implemented'` |
| `docs/architecture/arc42/06-runtime-view.md` | `# 6. Runtime View`, at least one `## 6.x` scenario subsection with `SCN-NN` ID + step table + a `<!-- arch-figure … -->` block (figure from `arch-c4` dynamic or `arch-uml sequence`), `## Open Items`. Owned by `arch-arc42` per ADR-0004; marker/figure integrity in Check 7a. | `grep -q '## 6\.\|SCN-[0-9]'` |
| `docs/architecture/arc42/07-deployment.md` | `# 7. Deployment View`, `## 7.1` overview, at least one per-environment `### Production` (or named env), Mapping table, `## Open Items` | `grep -q '## 7.1\|Mapping of building blocks'` |
| `docs/architecture/arc42/08-cross-cutting-concepts.md` | `# 8. Cross-Cutting Concepts`, `## Concept catalogue` table with `CC-NN` IDs and `Applies to` column, `## Open Items` | `grep -q '## Concept catalogue\|CC-[0-9]'` |
| `docs/architecture/arc42/11-risks.md` | `# 11. Risks and Technical Debt`, `## 11.1 Active Risks` table with `RSK-NN` IDs, `## 11.2 Technical Debt`, `## Open Items` | `grep -q '## 11.1\|RSK-[0-9]'` |

**Detection (example for process doc):**
```bash
find docs/business/05a-processes -name "proc-*.md" 2>/dev/null | while read f; do
  grep -q 'KPI\|§8' "$f" || echo "MISSING KPIs: $f"
  grep -q '^## Open Items' "$f" || echo "MISSING canonical Open Items section: $f"
done

# Service contracts
find docs/architecture/interfaces -name "*.md" ! -name "cli-*.md" 2>/dev/null | while read f; do
  grep -q '§0 Traceability' "$f" || echo "MISSING §0 Traceability: $f"
  grep -q '§3 Error contract' "$f" || echo "MISSING §3 Error contract: $f"
  grep -q '§4 Versioning' "$f" || echo "MISSING §4 Versioning: $f"
  grep -q '§5 Security' "$f" || echo "MISSING §5 Security surface: $f"
  grep -q '^## Open Items' "$f" || echo "MISSING canonical Open Items section: $f"
done

# CLI contracts
find docs/architecture/interfaces -name "cli-*.md" 2>/dev/null | while read f; do
  grep -q '§0 Traceability' "$f" || echo "MISSING §0 Traceability: $f"
  grep -q 'Command catalogue' "$f" || echo "MISSING §2 Command catalogue: $f"
  grep -q '§5 Output contract' "$f" || echo "MISSING §5 Output contract: $f"
  grep -q '§7 Error contract' "$f" || echo "MISSING §7 Error contract: $f"
  grep -q '^## Open Items' "$f" || echo "MISSING canonical Open Items section: $f"
done
```

**Severity:** Error

**Proposed fix template:** "Add missing section `{section}` to `{file}`. Template in `{skill} references/template.md §{N}`."

---

## Check 10 — Methodology pointers

**What:** verifies that `business-*` docs contain the kit methodology blockquote in their header section.

**Detection:**
```bash
find docs/business -name "*.md" | while read f; do
  grep -q 'homemade-claude-kit\|methodology-references\|canonical bibliography' "$f" || \
    echo "MISSING methodology pointer: $f"
done
```

**Severity:** Warning (doc created by hand, bypassing the skill; methodology drift risk)

**Proposed fix template:** "Add the 2-line methodology pointer blockquote to `{file}` header. Copy from `~/.claude/skills/{skill}/references/methodology-references.md` first paragraph."

---

## Check 11 — Confidence distribution

**What:** counts `Assumed`, `Tested`, `Validated` labels per file and flags stale-hypothesis patterns.

**Detection:**
```bash
find docs -name "*.md" | while read f; do
  assumed=$(grep -co '\bAssumed\b' "$f" 2>/dev/null || echo 0)
  tested=$(grep -co '\bTested\b' "$f" 2>/dev/null || echo 0)
  validated=$(grep -co '\bValidated\b' "$f" 2>/dev/null || echo 0)
  total=$((assumed + tested + validated))
  [ "$total" -gt 0 ] && echo "$assumed $tested $validated $total $f"
done
```

**Flag condition:** file is 100% Assumed AND was created more than 90 days ago (check git log creation date).

**Severity:** Warning (100% Assumed + >90 days); Info (distribution report only)

**Proposed fix template:** "Run `discovery-research` Mode 2 (interview script) targeting the Assumed bullets in `{file}` to gather evidence and promote to Tested/Validated."

---

## Check 12 — Expiry + staleness

**What:** flags artefacts overdue for review based on `last_reviewed` + `review_interval` frontmatter fields, plus proto-persona expiry and glossary changelog discipline.

**Detection — frontmatter staleness (all docs):**
```bash
today=$(date +%s)
find docs -name "*.md" | while read f; do
  last=$(grep "^last_reviewed:" "$f" 2>/dev/null | sed 's/last_reviewed: *//')
  interval=$(grep "^review_interval:" "$f" 2>/dev/null | sed 's/review_interval: *//' | grep -oP '[0-9]+')
  [ -z "$last" ] || [ -z "$interval" ] && continue
  last_ts=$(date -d "$last" +%s 2>/dev/null) || continue
  due=$(( last_ts + interval * 86400 ))
  [ "$today" -gt "$due" ] && \
    echo "OVERDUE ($(( (today - due) / 86400 ))d past): $f (last_reviewed: $last, interval: ${interval}d)"
done | sort
```

**Detection — proto-persona expiry:**
```bash
grep -n 'Next review' docs/business/01a-personas.md 2>/dev/null
# Compare each date against today; proto-personas past next-review are expired assumptions
```

**Detection — glossary changelog discipline:**
```bash
# Glossary exists but has no Changelog section → living-doc discipline missing
if [ -f "docs/domain/02c-glossary.md" ]; then
  grep -q '## Changelog' docs/domain/02c-glossary.md || \
    echo "WARNING: glossary.md missing Changelog section"
  # Changelog exists but last entry is > 30 days ago for Core BC (sprint cadence)
  last_entry=$(grep -m1 '^### [0-9]' docs/domain/02c-glossary.md 2>/dev/null | grep -oP '[0-9]{4}-[0-9]{2}-[0-9]{2}')
  [ -n "$last_entry" ] && echo "Glossary last changelog entry: $last_entry"
fi
```

**Severity:**
- Proto-persona past next-review → Error (expired assumption)
- Competitive claim past threshold → Warning
- Process doc not updated in >180 days → Info
- Glossary missing Changelog section → Warning (living-doc discipline missing)
- Glossary changelog last entry >30 days ago → Info (may need sprint review)

**Proposed fix template:**
- Expired persona: "Run `discovery-research` Mode 2 to validate `{persona}` and update `Next review` date, or mark as retired."
- Stale competitive claim: "Run `business-competitive-landscape` Mode 5 (refresh) for `{competitor}` claim in `{file}`."
- Missing glossary changelog: "Run `domain-glossary` Mode 4 (Maintain) — add `## Changelog` section and log all terms added/retired to date."
- Stale glossary changelog: "Run `domain-glossary` Mode 4 (Maintain, trigger 1D — scheduled sprint review) for the Core BC."

---

## Check 13 — Orphaned files

**What:** finds markdown files in `docs/` that are not referenced by any other doc.

**Detection:**
```bash
find docs -name "*.md" | while read f; do
  fname=$(basename "$f")
  # Check if any other doc links to this file by filename or relative path
  count=$(grep -rl "$fname" docs/ --include="*.md" 2>/dev/null | grep -v "^$f$" | wc -l)
  [ "$count" -eq 0 ] && echo "ORPHANED: $f"
done
```

**Exclusions (never flag as orphaned):**
- Hub docs: `01a-personas.md`, `03a-capability-map.md`, `04a-value-streams.md`, `delivery-roadmap.md`, `09a-quality-attributes.md`, `07a-fbs.md`
- README.md files
- Index files

**Severity:** Info

**Proposed fix template:** "If `{file}` is intentional (e.g., a draft), add a link from the relevant hub doc. If it is obsolete, delete it or move to `docs/archive/`."

---

## Check 14 — Research sync

**What:** finds research synthesis docs that contain "updates needed" sections where the referenced upstream artefact has not been modified since the synthesis was written.

**Detection:**
```bash
# Find synthesis files with update sections
grep -rln 'Per-artefact updates\|updates needed\|artefact.*update' \
  docs/business/research/ 2>/dev/null | while read synth; do
  synth_date=$(git log -1 --format="%ct" -- "$synth" 2>/dev/null)
  # For each upstream artefact mentioned in the synthesis
  grep -oh 'docs/[^)]*\.md' "$synth" | while read upstream; do
    upstream_date=$(git log -1 --format="%ct" -- "$upstream" 2>/dev/null)
    [ -n "$upstream_date" ] && [ "$synth_date" -gt "$upstream_date" ] && \
      echo "UNSYNCED: $synth → $upstream (synthesis newer than artefact)"
  done
done
```

**Severity:** Warning

**Proposed fix template:** "Apply updates proposed in `{synthesis}` to `{upstream_artefact}`. Mark as done by adding a line `<!-- synced: {date} -->` in the synthesis."

---

## Check 15 — ADR supersession chains

**What:** finds broken or one-sided ADR supersession links in frontmatter.

ADR supersession is tracked via frontmatter fields only — there is no `## Status` body section. Two checks:
1. When a new ADR has `supersedes: <path>`, the target file must have `status: superseded` and `superseded_by:` pointing back.
2. When an ADR has `status: superseded`, it must have `superseded_by:` pointing to an existing file.

**Detection:**
```bash
find docs/architecture/decisions -name "[0-9]*.md" 2>/dev/null | while read adr; do
  # Check 1: ADR body still contains ## Status section (should have been removed)
  grep -q '^## Status' "$adr" && \
    echo "STALE BODY STATUS: $adr — ## Status section must be removed; use frontmatter status field"

  # Check 2: if supersedes: present, verify target has status: superseded + superseded_by
  supersedes_path=$(grep "^supersedes:" "$adr" 2>/dev/null | sed 's/supersedes: *//')
  if [ -n "$supersedes_path" ]; then
    target=$(find . -path "*/$supersedes_path" -o -name "$(basename $supersedes_path)" 2>/dev/null | head -1)
    if [ -n "$target" ]; then
      grep -q "^status: superseded" "$target" || \
        echo "BROKEN CHAIN: $(basename $adr) supersedes $(basename $target) but target status is not superseded"
      grep -q "^superseded_by:" "$target" || \
        echo "BROKEN CHAIN: $(basename $adr) supersedes $(basename $target) but target missing superseded_by"
    else
      echo "DEAD SUPERSEDES LINK: $(basename $adr) → $supersedes_path (file not found)"
    fi
  fi

  # Check 3: if status: superseded, superseded_by must resolve to an existing file
  if grep -q "^status: superseded" "$adr"; then
    sb_path=$(grep "^superseded_by:" "$adr" 2>/dev/null | sed 's/superseded_by: *//')
    [ -z "$sb_path" ] && echo "MISSING superseded_by: $adr has status: superseded but no superseded_by field"
    [ -n "$sb_path" ] && [ ! -f "$sb_path" ] && \
      echo "DEAD superseded_by LINK: $adr → $sb_path (file not found)"
  fi
done
```

**Severity:** Warning

**Proposed fix template:** "Set `status: superseded` and add `superseded_by: <path>` in frontmatter of `{adr_file}`. Remove any `## Status` body section."

---

## Check 16 — Delivery progress

**What:** reports FBS functionality status distribution and epic ↔ PRD linkage completeness.

**Detection — FBS status:**
```bash
fbs="docs/product-specs/07a-fbs.md"
if [ -f "$fbs" ]; then
  done=$(grep -c '✅' "$fbs" 2>/dev/null || echo 0)
  in_progress=$(grep -c '🔄' "$fbs" 2>/dev/null || echo 0)
  not_started=$(grep -c '⬜' "$fbs" 2>/dev/null || echo 0)
  echo "FBS: ✅ $done / 🔄 $in_progress / ⬜ $not_started"
fi
```

**Detection — epic ↔ PRD linkage:**
```bash
epic_count=$(grep -c '\bE-[0-9]\{2\}\b' docs/plans/delivery-roadmap.md 2>/dev/null || echo 0)
prd_count=$(find docs/product-specs/prds -name "prd-*.md" 2>/dev/null | wc -l)
echo "Epics: $epic_count | PRDs: $prd_count"
# Find epics with no corresponding PRD link
grep -oh '\bE-[0-9]\{2\}\b' docs/plans/delivery-roadmap.md 2>/dev/null | sort -u | while read epic; do
  grep -rl "$epic" docs/product-specs/prds --include="prd-*.md" 2>/dev/null | head -1 || \
    echo "NO PRD for $epic"
done
```

**Detection — domain model completeness:**
```bash
# Domain model completeness
bc_count=$(grep -c 'BC-[0-9][0-9]' docs/domain/02b-bounded-contexts.md 2>/dev/null || echo 0)
dm_count=$(find docs/domain/07b-models -name "*.md" 2>/dev/null | wc -l)
echo "Bounded contexts: $bc_count | Domain models: $dm_count"
[ "$dm_count" -lt "$bc_count" ] && echo "WARNING: $(($bc_count - $dm_count)) BC(s) missing domain model"
```

**Severity:** Info

**Proposed fix template:** "Run `spec-prd` for epic `{E-NN}` to create the missing PRD. Promote FBS rows from ⬜ → 🔄 as the PRD is written."

---

## Check 17 — Frontmatter validity

**What:** verifies that every `docs/**/*.md` file opens with the standard artefact frontmatter block and that all required fields are present, valid, and consistent.

**Schema (canonical — defined in `rules/artefact-frontmatter.md`, an OKF v0.1 superset):**
- Always present, hard-required: `type` (OKF-required), `title`, `status`, `owner`, `last_reviewed`, `review_interval`
- Always present, OKF-recommended (Warning if missing during adoption): `description`, `tags`, `timestamp`
- Conditional: `resource` present only when the artefact has an external asset; `superseded_by` required when `status: superseded`; `supersedes` present only on documents created to replace another
- Valid `status` values: `draft`, `active`, `superseded`, `deprecated`
- `type` value: must equal a canonical `okf_type` display name from `rules/artefact-types-registry.md` (a value outside the set is tolerated by OKF but flagged Warning — "unregistered type")
- **Reserved files** (`index.md`, `log.md`) are exempt from the artefact block; the root `docs/index.md` must instead declare `okf_version`

**Detection:**

> **IMPORTANT — bypass shell wrappers.** Some environments (including Claude
> Code's interactive shell) wrap `grep`/`find` as bash functions that `exec`
> into a different binary. When such a wrapper is called from inside a
> `while read` subshell, the `exec` replaces the entire subshell process — the
> loop silently aborts at the first `grep` call with no error. This is why a
> previous version of this check produced empty output on a repo where every
> file in `docs/` opened with `<!-- doc-version: … -->` HTML comments instead
> of YAML frontmatter. Always invoke `grep`/`find` via `command grep` /
> `command find` (or absolute paths) inside `while`/`for` loops.

```bash
# Exclude transient/non-metamodel paths that often appear inside docs/ in real
# repos (Python virtualenvs, build caches, notebook session metadata, npm).
EXCLUDED='( -path */.venv/* -o -path */__pycache__/* -o -path */.pytest_cache/* -o -path */__marimo__/* -o -path */node_modules/* )'

# Use a tally file so the per-file subshell can update counters that survive
# the `while read` pipe-subshell boundary.
tally=$(mktemp)
printf '0 0 0\n' > "$tally"   # scanned missing_frontmatter findings

echo "=== Check 17: Frontmatter validity — starting ==="

# Exempt: README.md (tool/folder/vendor nav) + the OKF reserved files index.md
# and log.md (directory-navigation / history aids, NOT concept documents — per
# rules/artefact-frontmatter.md they carry no artefact frontmatter). The root
# docs/index.md is checked separately for okf_version below. Names are
# case-sensitive.
command find docs -name "*.md" ! -name 'README.md' ! -name 'index.md' ! -name 'log.md' ! \( $EXCLUDED \) 2>/dev/null | sort | while IFS= read -r f; do
  read scanned missing findings < "$tally"
  scanned=$((scanned + 1))

  # 1. Frontmatter block must be present — first 3 bytes must be '---'.
  # Using `head -c 3` is portable and avoids the pitfalls of
  # `head -1 | grep -q '^---'` (the grep can be a wrapped function — see
  # the IMPORTANT note above).
  first3=$(head -c 3 "$f" 2>/dev/null)
  if [ "$first3" != "---" ]; then
    echo "MISSING FRONTMATTER: $f"
    missing=$((missing + 1))
    findings=$((findings + 1))
    printf '%d %d %d\n' "$scanned" "$missing" "$findings" > "$tally"
    continue
  fi

  # Helper: read a frontmatter field, trim leading/trailing whitespace and
  # surrounding quotes. Returns empty string when the field is absent.
  fm() {
    command grep -m1 "^${1}:" "$f" 2>/dev/null \
      | sed -E "s/^${1}:[[:space:]]*//; s/[[:space:]]+\$//; s/^[\"']//; s/[\"']\$//"
  }

  # 2. All hard-required fields must exist (type is OKF-required — its absence
  #    breaks OKF conformance).
  for field in type title status owner last_reviewed review_interval; do
    command grep -q "^${field}:" "$f" || {
      echo "MISSING FIELD '${field}': $f"
      findings=$((findings + 1))
    }
  done

  # 2a. OKF-recommended fields — Warning (gentler during adoption; OKF-optional).
  for field in description tags timestamp; do
    command grep -q "^${field}:" "$f" || {
      echo "MISSING OKF FIELD (warn) '${field}': $f"
      findings=$((findings + 1))
    }
  done

  # 2b. type must be a non-empty canonical okf_type display name. The enum below
  #     mirrors the "OKF type display names" table in
  #     rules/artefact-types-registry.md — keep in sync when a type is added.
  #     A value outside the set is tolerated by OKF but flagged (unregistered).
  type_val=$(fm type)
  if [ -n "$type_val" ]; then
    okf_types="Product Vision|Persona|Business Model Canvas|Business Model Canvas Block|Business Capability|Value Stream|Value Stream Stage|Business Objective|Key Result|Business Process|Quantitative Model|Competitor Profile|Bounded Context|Glossary Term|Functionality|Domain Model|Aggregate|Entity|Value Object|Domain Event|Interface Contract|Epic|CLI Surface Contract|CLI Command|Quality Attribute|Use Case|Product Requirements Document|Implementation Plan|Architecture Decision Record|Architecture Research Note|Idea|Runbook|Bug RCA|Stack Guide|Getting Started Guide|Research Note|Workshop Note|Design System|Architecture Documentation"
    echo "$type_val" | command grep -qxE "($okf_types)" || {
      echo "UNREGISTERED type '${type_val}' (warn): $f"
      findings=$((findings + 1))
    }
  fi

  # 3. status must be one of the four allowed values
  status=$(fm status)
  case "$status" in
    draft|active|superseded|deprecated) ;;
    *) echo "INVALID STATUS '${status}': $f"; findings=$((findings + 1)) ;;
  esac

  # 4. When status: superseded, superseded_by must be present and target must exist
  if [ "$status" = "superseded" ]; then
    sb=$(fm superseded_by)
    if [ -z "$sb" ]; then
      echo "MISSING superseded_by (status is superseded): $f"
      findings=$((findings + 1))
    elif [ ! -f "$sb" ]; then
      echo "DEAD superseded_by TARGET '$sb': $f"
      findings=$((findings + 1))
    fi
  fi

  # 5. When supersedes: present, target must exist and have status: superseded
  sup=$(fm supersedes)
  if [ -n "$sup" ]; then
    if [ ! -f "$sup" ]; then
      echo "DEAD supersedes TARGET '$sup': $f"
      findings=$((findings + 1))
    elif ! command grep -q "^status:[[:space:]]*[\"']\?superseded[\"']\?" "$sup"; then
      echo "supersedes TARGET NOT SUPERSEDED '$sup': $f"
      findings=$((findings + 1))
    fi
  fi

  # 6. owner must not be empty when the field exists.
  owner=$(fm owner)
  if [ -z "$owner" ] && command grep -q "^owner:" "$f"; then
    echo "EMPTY owner: $f"
    findings=$((findings + 1))
  fi

  # 7. last_reviewed must be a valid YYYY-MM-DD date when the field exists.
  # Skip the regex check when the field is entirely absent (already flagged
  # in step 2) so we don't emit a confusing "INVALID last_reviewed ''" line
  # on top of the MISSING FIELD line.
  lr=$(fm last_reviewed)
  if [ -n "$lr" ] && ! echo "$lr" | command grep -qP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'; then
    echo "INVALID last_reviewed '${lr}': $f"
    findings=$((findings + 1))
  fi

  printf '%d %d %d\n' "$scanned" "$missing" "$findings" > "$tally"
done

# Summary — emit even when there are zero findings, so a silent stdout
# is distinguishable from "the check didn't run".
read scanned missing findings < "$tally"
echo "=== Check 17 complete: scanned=${scanned} missing_frontmatter=${missing} total_findings=${findings} ==="
rm -f "$tally"

# Reserved-file check (OKF bundle root): docs/index.md must exist and declare
# the bundle's okf_version. Sub-folder index.md / log.md files are frontmatter-
# free and intentionally not checked.
if [ -f docs/index.md ]; then
  command grep -q '^okf_version:' docs/index.md \
    || echo "ROOT index.md MISSING okf_version: docs/index.md"
else
  echo "MISSING ROOT BUNDLE INDEX: docs/index.md (OKF bundle listing + okf_version)"
fi
```

**Two defensive guarantees of this version:**

1. **Always emits a summary line.** Earlier versions produced zero stdout on a
   clean run, indistinguishable from "the loop never executed". The
   `=== Check 17 complete: scanned=N … ===` line at the end is mandatory and
   tells the operator the check actually ran and how many files it touched. If
   `scanned=0` and the repo has `*.md` files under `docs/`, that itself is a
   finding (find pattern is wrong, or a wrapper is killing the loop).

2. **Survives wrapped `grep`/`find`.** `command grep` / `command find` bypass
   any bash function or alias of the same name. This is harmless in plain
   environments and load-bearing in Claude Code's interactive shell, where
   `grep` is wrapped as a function that `exec`s into `ugrep`, replacing the
   subshell process and silently aborting the loop.

**Severity:**
- Missing frontmatter block → Error
- Missing hard-required field (`type`, `title`, `status`, `owner`, `last_reviewed`, `review_interval`) → Error
- Missing OKF-recommended field (`description`, `tags`, `timestamp`) → Warning
- Unregistered `type` value (not a canonical `okf_type`) → Warning
- Invalid `status` value → Error
- `superseded` without `superseded_by` → Error
- Dead `superseded_by` or `supersedes` target → Error
- Empty `owner` → Warning
- Invalid `last_reviewed` date format → Warning
- Root `docs/index.md` missing or without `okf_version` → Error

**Proposed fix template:**
- Missing block: "Add standard frontmatter to `{file}` using `rules/artefact-frontmatter.md` schema (OKF superset). Run `git config user.name` for owner."
- Missing `type`: "Add `type: <okf_type>` to `{file}` — use the artefact's display name from the OKF type table in `rules/artefact-types-registry.md`."
- Unregistered type: "Change `type:` in `{file}` to a canonical `okf_type` display name, or register the new type in `rules/artefact-types-registry.md` + this check's enum."
- Missing field: "Add `{field}:` to the frontmatter of `{file}`."
- Invalid status: "Set `status:` in `{file}` to one of: `draft`, `active`, `superseded`, `deprecated`."
- Missing `superseded_by`: "Add `superseded_by: <path-to-replacement>` to `{file}` frontmatter."
- Dead target: "Update `superseded_by` / `supersedes` path in `{file}` — target file no longer exists at `{path}`."
- Root index: "Create `docs/index.md` (OKF bundle root: `okf_version: \"0.1\"` frontmatter + navigation body) via `util-metamodel-scaffold`."

---

## Check 18 — Open items governance

**What:** verifies that every artefact's local `## Open Items` section conforms to
`rules/open-items-governance.md` and that the central ledger at
`docs/project-control/open-items/open-items.md` stays in sync with the artefact rows.

This is the only check category in the catalogue that spans both `docs/` and
`docs/project-control/`. It is **report-only** — findings are surfaced to the operator;
remediation is always done through `util-open-items` (sync, triage, close, archive)
or direct artefact edits. The audit never mutates the ledger or any source artefact.

The check bundles the sub-checks below, each with its own detection pattern and severity.
They run together in Mode 1 (full audit); operators wanting only governance drift can invoke
Mode 5 (open-items governance) when it lands.

### Backend awareness

Per governance §5.3 the central plane has a pluggable backend. Detect it before the
ledger-reading sub-checks:

```bash
backend_cfg="docs/project-control/open-items/backend.yml"
backend="markdown"   # default when the file is absent
[ -f "$backend_cfg" ] && backend=$(grep -oE '^backend:[[:space:]]*[a-z]+' "$backend_cfg" | awk '{print $2}')
echo "open-items backend: $backend"
```

How the sub-checks split by backend:

| Sub-check | `markdown` | `github` |
| :-- | :-- | :-- |
| 18a / 18b / 18c (local sections) | run as written | **run unchanged** — local `## Open Items` sections are always §4 markdown (Invariant I4) |
| 18d Tracker sync coverage | ledger vs local `OI-NNNN` | **github variant** — local `#N` vs Issues |
| 18e Closure drift | scan ledger rows | **github variant** — structurally enforced; verify the closing reference exists |
| 18f Stale open items | local `Due / Review date` | **github variant** — open issues' Project `Review date` field |
| 18g Form / slug integrity | — | **github only** — issue bodies carry the canonical slug fields + valid Type |

The local-section sub-checks (18a–18c) never change — only the *central read-out* differs by
backend. Everything below stays **report-only**; remediation routes through `util-open-items`.

### Sub-check 18a — Section compliance

**What:** every artefact that carries unresolved work uses the canonical document-level
`## Open Items` heading. Forbidden variants — listed in §1 of
`rules/open-items-governance.md` — must not appear anywhere in the repo's artefact files.

**Detection:**

```bash
# 1. Forbidden legacy heading variants (must return zero matches)
rg -n '^## Open / TODO$|^## Open TODOs$|^## Open questions remaining$|^## Open questions for next interview$|^## Open questions for next workshop / research wave$|^## 11\. Open TODOs' docs/ business-* arch-* spec-* domain-* ops-* com-* util-* 2>/dev/null

# 2. Non-document-level placement (### subsection forbidden per §1)
rg -n '^### Open Items$' docs/ 2>/dev/null

# 3. Legacy wording in discipline / SKILL docs
rg -n '§Open Issues|Open Issues' docs/ business-* arch-* spec-* domain-* 2>/dev/null
```

**Severity:** Error

**Proposed fix template:** "Rename `{found heading}` in `{file}` line {N} to the canonical
`## Open Items` (document-level). Migration steps in `rules/open-items-governance.md` §1."

### Sub-check 18b — Schema compliance

**What:** tables under `## Open Items` use the canonical column order and column names
from §4 of `rules/open-items-governance.md`. Columns must not be removed or reordered;
additional informational columns are permitted only **after** `Tracker ref`.

**Detection:**

```bash
# Find every ## Open Items section, capture the header row (first line beginning with |
# after the heading), and verify the column sequence.
find docs -name "*.md" -print0 | while IFS= read -r -d '' f; do
  awk '
    /^## Open Items[[:space:]]*$/ { in_section=1; next }
    in_section && /^## / { in_section=0 }
    in_section && /^\|/ {
      print FILENAME ":" NR ":" $0
      exit
    }
  ' "$f"
done | while IFS=':' read -r file line header; do
  echo "$header" | grep -qE '\|[[:space:]]*OI-ID[[:space:]]*\|[[:space:]]*Type[[:space:]]*\|[[:space:]]*Summary[[:space:]]*\|[[:space:]]*Source anchor[[:space:]]*\|[[:space:]]*Source heading[[:space:]]*\|[[:space:]]*Resolution path[[:space:]]*\|[[:space:]]*Priority[[:space:]]*\|[[:space:]]*Status[[:space:]]*\|[[:space:]]*Owner[[:space:]]*\|[[:space:]]*Due / Review date[[:space:]]*\|[[:space:]]*Tracker ref' || \
    echo "SCHEMA NON-COMPLIANT: $file line $line — header is: $header"
done
```

**Severity:** Error

**Proposed fix template:** "Restore canonical column order in `## Open Items` table at
`{file}` line {N}. Canonical order: `OI-ID | Type | Summary | Source anchor | Source
heading | Resolution path | Priority | Status | Owner | Due / Review date | Tracker ref`.
Additional columns are allowed only after `Tracker ref`."

### Sub-check 18c — Source-location provenance

**What:** every row in a local `## Open Items` table has both `Source anchor` and
`Source heading` populated. Rows that genuinely have no in-artefact origin (raised
directly at the central plane) carry the sentinel `_central-only_` in `Source heading`
and an empty `Source anchor` — these are not flagged.

**Detection:**

```bash
# For each ## Open Items table, read the data rows and check columns 4 (Source anchor)
# and 5 (Source heading) are non-blank and not _TBD_.
find docs -name "*.md" -print0 | while IFS= read -r -d '' f; do
  awk -v F="$f" '
    /^## Open Items[[:space:]]*$/ { in_section=1; row=0; next }
    in_section && /^## / { in_section=0 }
    in_section && /^\|/ {
      row++
      if (row <= 2) next   # header + separator
      n = split($0, cols, "|")
      anchor = cols[5]; gsub(/^[[:space:]]+|[[:space:]]+$/, "", anchor)
      heading = cols[6]; gsub(/^[[:space:]]+|[[:space:]]+$/, "", heading)
      oi = cols[2]; gsub(/^[[:space:]]+|[[:space:]]+$/, "", oi)
      if (heading == "_central-only_") next
      if (anchor == "" || anchor == "_TBD_" || heading == "" || heading == "_TBD_") {
        printf "PROVENANCE MISSING: %s row %s (OI=%s anchor=%s heading=%s)\n", F, NR, oi, anchor, heading
      }
    }
  ' "$f"
done
```

**Severity:** Warning

**Proposed fix template:** "Populate `Source anchor` and `Source heading` for row `{OI-ID}`
in `{file}`. The pair is the provenance contract (§4 of `rules/open-items-governance.md`).
Use `_central-only_` in `Source heading` only when the row has no in-artefact origin."

### Sub-check 18d — Tracker sync coverage

**What:** every local row whose `OI-ID` has been promoted to the canonical `OI-NNNN`
format must have a corresponding row in `docs/project-control/open-items/open-items.md`.
Rows still on a pre-sync local ID (e.g. `OI-001`, `OI-002`) are not flagged — they
indicate the artefact has not been synced yet, which is normal between edits.

**Detection:**

```bash
ledger="docs/project-control/open-items/open-items.md"
[ ! -f "$ledger" ] && echo "LEDGER MISSING: $ledger" && exit 0

# Collect every canonical OI-NNNN ID present in the ledger
grep -oh '\bOI-[0-9]\{4\}\b' "$ledger" 2>/dev/null | sort -u > /tmp/oi_ledger.txt

# Collect every canonical OI-NNNN ID referenced in artefact-local Open Items sections
find docs -name "*.md" -print0 | while IFS= read -r -d '' f; do
  awk -v F="$f" '
    /^## Open Items[[:space:]]*$/ { in_section=1; next }
    in_section && /^## / { in_section=0 }
    in_section && /^\|/ {
      if (match($0, /OI-[0-9][0-9][0-9][0-9]/)) {
        printf "%s\t%s\n", substr($0, RSTART, RLENGTH), F
      }
    }
  ' "$f"
done | sort -u > /tmp/oi_local.txt

# Local OI-NNNN IDs that are missing from the ledger → sync drift
cut -f1 /tmp/oi_local.txt | sort -u > /tmp/oi_local_ids.txt
comm -23 /tmp/oi_local_ids.txt /tmp/oi_ledger.txt | while read oi; do
  src=$(grep -P "^${oi}\t" /tmp/oi_local.txt | cut -f2 | head -1)
  echo "SYNC DRIFT: $oi present in $src but missing from $ledger"
done

# Ledger OI-NNNN IDs that have no local row → orphaned ledger entry (or _central-only_)
comm -13 /tmp/oi_local_ids.txt /tmp/oi_ledger.txt | while read oi; do
  is_central=$(grep -P "\|\s*${oi}\s*\|" "$ledger" | grep -c '_central-only_' || true)
  [ "$is_central" -eq 0 ] && echo "ORPHANED LEDGER ROW: $oi in $ledger has no matching local row"
done
```

**Severity:** Warning

**Proposed fix template:**

- Sync drift: "Run `util-open-items` in `sync` mode for `{source artefact}` so the local
  `{OI-NNNN}` row reaches `docs/project-control/open-items/open-items.md`."
- Orphaned ledger row: "Either the source artefact was deleted (close or drop the ledger
  row with `util-open-items` and record the rationale) or the row should be marked
  `_central-only_` in `Source heading` per §5 of `rules/open-items-governance.md`."

**github variant** (requires `gh` auth). Under `backend: github` there is no markdown
ledger; the local `OI-ID` cell carries the issue number `#N` after sync. Verify each `#N`
resolves and each open open-item issue has a local source row:

```bash
if [ "$backend" = "github" ]; then
  repo=$(grep -oE '^repo:[[:space:]]*\S+' "$backend_cfg" | awk '{print $2}')
  # local #N references inside ## Open Items sections
  find docs -name "*.md" -print0 | while IFS= read -r -d '' f; do
    awk '/^## Open Items[[:space:]]*$/{s=1;next} s&&/^## /{s=0} s&&/^\|/{if(match($0,/#[0-9]+/))print substr($0,RSTART+1,RLENGTH-1)}' "$f"
  done | sort -u > /tmp/oi_local_gh.txt
  while read -r n; do
    gh issue view "$n" -R "$repo" --json number >/dev/null 2>&1 || \
      echo "DANGLING ISSUE REF: #$n referenced locally but not found in $repo"
  done < /tmp/oi_local_gh.txt
  # open open-item issues with no local source row — EXCLUDING _central-only_ items
  # (kit-dev work with no artefact home, §5.2/§9; they legitimately have no local row,
  # exactly as the markdown 18d variant excludes _central-only_ ledger rows).
  gh issue list -R "$repo" --label open-item --state open --json number,body \
    -q '.[] | select((.body // "") | test("_central-only_") | not) | .number' | while read -r n; do
    grep -qx "$n" /tmp/oi_local_gh.txt || \
      echo "ORPHANED ISSUE: #$n is an open open-item with no local source row"
  done
fi
```

### Sub-check 18e — Closure drift

**What:** rows whose `Status` is `closed` or `dropped` must carry a non-`_TBD_`
`Tracker ref`. Closure must be evidenced (§3 of `rules/open-items-governance.md`).

**Detection:**

```bash
ledger="docs/project-control/open-items/open-items.md"

# Closure drift in artefact-local sections
find docs -name "*.md" -print0 | while IFS= read -r -d '' f; do
  awk -v F="$f" '
    /^## Open Items[[:space:]]*$/ { in_section=1; row=0; next }
    in_section && /^## / { in_section=0 }
    in_section && /^\|/ {
      row++
      if (row <= 2) next
      n = split($0, cols, "|")
      oi = cols[2]; gsub(/^[[:space:]]+|[[:space:]]+$/, "", oi)
      status = cols[9]; gsub(/^[[:space:]]+|[[:space:]]+$/, "", status)
      tracker = cols[12]; gsub(/^[[:space:]]+|[[:space:]]+$/, "", tracker)
      if ((status == "closed" || status == "dropped") && (tracker == "" || tracker == "_TBD_")) {
        printf "CLOSURE DRIFT: %s row %s (OI=%s status=%s tracker=%s)\n", F, NR, oi, status, tracker
      }
    }
  ' "$f"
done

# Same check against the central ledger (Source artefact is column 4 there → tracker is column 13)
if [ -f "$ledger" ]; then
  awk -v F="$ledger" '
    /^## Live items[[:space:]]*$/ { in_section=1; row=0; next }
    in_section && /^## / { in_section=0 }
    in_section && /^\|/ {
      row++
      if (row <= 2) next
      n = split($0, cols, "|")
      oi = cols[2]; gsub(/^[[:space:]]+|[[:space:]]+$/, "", oi)
      status = cols[10]; gsub(/^[[:space:]]+|[[:space:]]+$/, "", status)
      tracker = cols[13]; gsub(/^[[:space:]]+|[[:space:]]+$/, "", tracker)
      if ((status == "closed" || status == "dropped") && (tracker == "" || tracker == "_TBD_")) {
        printf "CLOSURE DRIFT: %s row %s (OI=%s status=%s tracker=%s)\n", F, NR, oi, status, tracker
      }
    }
  ' "$ledger"
fi
```

**Severity:** Error

**Proposed fix template:** "Row `{OI-ID}` in `{file}` is `{status}` but `Tracker ref` is
`_TBD_`. Either record the resolving PR / ADR / plan increment / runbook URL via
`util-open-items` in `close` (or `drop`) mode, or re-open the row by setting status back
to `open` / `in-progress` / `blocked`."

**github variant** (requires `gh` auth). Closure is structurally enforced (you close an
issue *via* a reference), so this rarely fires — but a `completed` issue with no linked PR
has no evidencing `tracker_ref`:

```bash
if [ "$backend" = "github" ]; then
  gh issue list -R "$repo" --label open-item --state closed \
    --json number,stateReason,closedByPullRequestsReferences \
    -q '.[] | select(.stateReason=="COMPLETED" and (.closedByPullRequestsReferences|length==0)) | .number' \
  | while read -r n; do
    echo "CLOSURE EVIDENCE MISSING: #$n closed as completed with no linked PR (tracker_ref)"
  done
fi
# `dropped` = closed as "not planned"; it needs a rationale comment, not a PR — review manually.
```

### Sub-check 18f — Stale open items (overdue review)

**What:** rows whose `Status` is `open`, `in-progress`, or `blocked` and whose
`Due / Review date` has passed are overdue. This is not auto-closure — operators must
re-triage via `util-open-items`. Surfacing them in the audit is the trigger.

**Detection:**

```bash
today=$(date +%s)
find docs -name "*.md" -print0 | while IFS= read -r -d '' f; do
  awk -v F="$f" -v TODAY="$today" '
    /^## Open Items[[:space:]]*$/ { in_section=1; row=0; next }
    in_section && /^## / { in_section=0 }
    in_section && /^\|/ {
      row++
      if (row <= 2) next
      n = split($0, cols, "|")
      oi = cols[2]; gsub(/^[[:space:]]+|[[:space:]]+$/, "", oi)
      status = cols[9]; gsub(/^[[:space:]]+|[[:space:]]+$/, "", status)
      due = cols[11]; gsub(/^[[:space:]]+|[[:space:]]+$/, "", due)
      if (status != "open" && status != "in-progress" && status != "blocked") next
      if (due == "" || due == "_TBD_") next
      # parse YYYY-MM-DD into epoch via system date
      cmd = "date -d \"" due "\" +%s 2>/dev/null"
      cmd | getline due_ts
      close(cmd)
      if (due_ts == "" || due_ts == 0) next
      if (TODAY > due_ts) {
        overdue_days = int((TODAY - due_ts) / 86400)
        printf "OVERDUE %dd: %s row %s (OI=%s status=%s due=%s)\n", overdue_days, F, NR, oi, status, due
      }
    }
  ' "$f"
done
```

**Severity:** Warning

**Proposed fix template:** "Row `{OI-ID}` in `{file}` is `{status}` and was due
`{due date}` ({overdue days}d ago). Run `util-open-items` in `triage` mode to either
re-date, escalate priority, reassign owner, or close with a `Tracker ref`."

**github variant** (requires `gh` auth). Overdue is the Project `Review date` field on open
issues. Field name follows the project's configuration — adjust the `-q` selector to match:

```bash
if [ "$backend" = "github" ]; then
  project=$(grep -oE '^project:[[:space:]]*[0-9]+' "$backend_cfg" | awk '{print $2}')
  owner=$(echo "$repo" | cut -d/ -f1)
  today=$(date +%s)
  gh project item-list "$project" --owner "$owner" --format json \
    -q '.items[] | select(.status!="Done") | [(.content.number|tostring), (.["reviewDate"] // "")] | @tsv' 2>/dev/null \
  | while IFS=$'\t' read -r n due; do
    [ -z "$due" ] && continue
    due_ts=$(date -d "$due" +%s 2>/dev/null) || continue
    [ "$today" -gt "$due_ts" ] && echo "OVERDUE: issue #$n review date $due has passed"
  done
fi
```

### Sub-check 18g — Form / slug integrity (github only)

**What:** every open `open-item` issue was created from the canonical form, carries a valid
Issue Type, and exposes the required slug fields in its body. This is the github analog of
18b/18c — it verifies the issue conforms to the §4 slug contract (Invariant I1) so the
read-out stays machine-parseable.

**Detection** (requires `gh` auth):

```bash
if [ "$backend" = "github" ]; then
  valid="doc-gap decision-gap execution-item tech-debt"
  gh issue list -R "$repo" --label open-item --state open \
    --json number,issueType,body \
    -q '.[] | [(.number|tostring), (.issueType.name // "none"), (.body|gsub("\n";"¶"))] | @tsv' \
  | while IFS=$'\t' read -r n itype body; do
    echo "$valid" | grep -qw "$itype" || \
      echo "INVALID TYPE: issue #$n has Issue Type '$itype' (expected one of: $valid)"
    echo "$body" | grep -qi "Source heading" || \
      echo "FORM DRIFT: issue #$n body has no Source heading field"
    echo "$body" | grep -qi "Resolution path" || \
      echo "FORM DRIFT: issue #$n body has no Resolution path field"
  done
fi
```

**Severity:** Warning

**Proposed fix template:** "Issue `#{N}` is missing `{field}` / has Issue Type `{itype}`.
Re-create it through `.github/ISSUE_TEMPLATE/open-item.yml` or edit it to restore the
canonical slug fields. The form `id:` keys are the binding contract (Invariant I1 in
`util-open-items/references/github-backend.md`)."

### Summary — Check 18 outputs

| Sub-check | Severity | Backend | What it flags |
| :-- | :-- | :-- | :-- |
| 18a Section compliance | Error | both | Forbidden legacy headings; non-document-level `### Open Items` |
| 18b Schema compliance | Error | both | Missing / reordered canonical columns in `## Open Items` tables |
| 18c Source-location provenance | Warning | both | Empty / `_TBD_` `Source anchor` or `Source heading` (excludes `_central-only_`) |
| 18d Tracker sync coverage | Warning | markdown: ledger ↔ local · github: Issues ↔ local | `OI-NNNN` (or `#N`) out of sync between local sections and the central read-out |
| 18e Closure drift | Error | markdown: ledger · github: closing-ref | Terminal rows / issues without evidencing `Tracker ref` |
| 18f Stale open items | Warning | markdown: `Due / Review date` · github: Project field | Active rows / issues past their review date |
| 18g Form / slug integrity | Warning | **github only** | Open-item issues with invalid Type or missing canonical slug fields |

All sub-checks are read-only; none write to `docs/project-control/open-items/`, to any source
artefact, or to GitHub. Findings always route to the operator for action through
`util-open-items`. The local-section checks (18a–18c) are backend-independent; 18d–18f have a
markdown and a github variant; 18g runs only under the `github` backend.
