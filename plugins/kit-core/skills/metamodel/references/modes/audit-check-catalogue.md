# Check Catalogue — Audit mode

For each of the 19 checks: bash detection pattern, interpretation rules, severity, and proposed fix template. Claude reads this file during audit execution to know exactly how to run each check.

**Registry derivation (read first).** Structural facts — canonical paths, ID regexes, the
`okf_type` enum — are NEVER hardcoded in this catalogue. Derive them at the start of every
audit run by parsing this skill's `references/artefact-types-registry.yaml`:

```bash
python3 - <<'EOF'
import yaml
r = yaml.safe_load(open('<metamodel-skill-dir>/references/artefact-types-registry.yaml'))
for t in r['artefact_types']:
    print(f"{t['type']}\t{t['id_format'] or '-'}\t{t['default_path'] or '(inherits '+t.get('parent','?')+')'}\t{t['okf_type']}\t{t['review_interval']}")
EOF
```

A check below that says "derive from the registry" iterates these rows. Sub-element and
diagram IDs (`SYS-NN`, `SCN-NN`, BMC block IDs, …) are NOT registry types — their curated
table lives in Check 5 and is sourced from this skill's `references/metamodel-reference.md`
§ Cross-doc ID conventions. A handful of non-artefact foundations (`workspace.dsl`,
`render.sh`, committed C4 SVGs) are likewise curated inline where a check needs them.

---

## Check 1 — Stack progress

**What:** verifies which of the canonical output paths exist.

**Detection — derive from the registry.** For every registry entry with a non-null
`default_path`, resolve the template to a `find` probe: literal paths become exact-name
finds (`docs/VISION.md` → `find docs -maxdepth 1 -name "VISION.md"`); templated paths
(`{slug}`, `{nn}`, `{nnnn}`, `{bc-slug}`, `{date}`, `{feature}`, `{topic}`, `{tech-slug}`)
become glob probes in the template's directory (`docs/product-specs/prds/prd-{nnnn}-{feature}.md`
→ `find docs/product-specs/prds -name "prd-*.md" | head -1`). Entries with
`layout: inherits-from-parent` are covered by their parent's probe. Map each probe back to
its build-order step via the spine table in this skill's `SKILL.md`.

**Plus the curated non-registry foundations** (not artefact types; keep in sync manually):
```bash
find docs/architecture/c4 -name "workspace.dsl" 2>/dev/null                       # arch-structurizr foundation
find docs/architecture/c4/views -name "*.svg" 2>/dev/null | head -1               # arch-c4 rendered views (committed)
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
Then compare each path against the canonical map, **derived from the registry**: for every
entry with a non-null `default_path`, a file matching the template's filename pattern must
sit exactly at the template's directory (literal templates → exact path; templated names →
glob within the template's directory; `inherits-from-parent` entries are covered by the
parent). Flag any `docs/**` markdown file that matches a registry filename pattern but sits
outside its template directory, and any file under a registry-owned directory that matches
no known pattern.

**Curated non-registry placement rules** (foundations + convention files, keep in sync manually):
- `*.md` under `docs/architecture/` but NOT in `decisions/`, `interfaces/`, `research/`, `c4/`, or `arc42/` → likely misplaced architecture file
- `workspace.dsl` → must be at `docs/architecture/c4/workspace.dsl` (singleton — `arch-structurizr` foundation)
- `render.sh` → must be at `docs/architecture/c4/render.sh` (executable; `arch-structurizr` writes; `chmod +x` expected)
- `*.svg` under `docs/architecture/c4/views/` → committed C4 renders from `arch-c4`; correct
- `*.puml` under `docs/architecture/c4/` (anywhere) → intermediate PlantUML export; should be gitignored, not committed
- `*.md` under `docs/architecture/arc42/` not matching the canonical eight (`02`, `03`, `04`, `05`, `06`, `07`, `08`, `11`) → likely misplaced
- `interview-*.md`, `research-synthesis-*.md`, `research-plan-*.md` → must be under `docs/discovery/interviews/`; `workshop-*.md`, `workshop-synthesis-*.md` → under `docs/discovery/workshops/`
- `{tech-slug}-research.md` under `docs/dev-guides/research/` → correct (`dev-stack-guide` research scratch); other `*.md` under `docs/dev-guides/` must match a registry pattern

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

**ID patterns and owning artefacts — two sources:**

1. **Artefact-type IDs — derive from the registry.** For every entry with a non-null
   `id_format`, the ID pattern is `\b` + `id_format` + `\b` and the owning artefact is the
   entry's `default_path` (for `inherits-from-parent` entries, the parent's `default_path`).
   Never restate these rows here — iterate the registry.

2. **Sub-element and diagram IDs — curated table** (NOT registry types; canonical source:
   this skill's `references/metamodel-reference.md` § Cross-doc ID conventions; keep in sync
   with it, not with the registry):

| ID format | Regex | Owning artefact |
|---|---|---|
| `CS-N` | `\bCS-[0-9]+\b` | `docs/business/02a-bmc.md` |
| `VP-N` | `\bVP-[0-9]+\b` | `docs/business/02a-bmc.md` |
| `CH-N` | `\bCH-[0-9]+\b` | `docs/business/02a-bmc.md` |
| `CR-N` | `\bCR-[0-9]+\b` | `docs/business/02a-bmc.md` |
| `RS-N` | `\bRS-[0-9]+\b` | `docs/business/02a-bmc.md` |
| `KA-N` | `\bKA-[0-9]+\b` | `docs/business/02a-bmc.md` |
| `KP-N` | `\bKP-[0-9]+\b` | `docs/business/02a-bmc.md` |
| `CT-N` | `\bCT-[0-9]+\b` | `docs/business/02a-bmc.md` |
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
| `*-process.md` | `## §8 KPIs` or `## KPIs`, `## §0 Master flow` | `grep -q 'KPI\|§8'` |
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
| `docs/architecture/interfaces/*.md` (not `cli-*.md`) | `## §0 Traceability`, `## §3 Error contract`, `## §4 Versioning & deprecation policy`, `## §5 Security surface`, `## Changelog` | `grep -q '§0 Traceability\|§3 Error contract'` |
| `docs/architecture/interfaces/cli-*.md` | `## §0 Traceability`, `## §2 Command catalogue`, `## §5 Output contract`, `## §7 Error contract`, `## Changelog` | `grep -q 'Command catalogue\|§7 Error contract'` |
| `docs/discovery/ideation/IDEA-*.md` | `## Problem statement`, `## Not doing`, `## Changelog`; frontmatter must include `idea_id`, `domain`, `lifecycle`, `graduates_to` | `grep -q '## Problem statement\|## Not doing'` and `grep -q '^idea_id:\|^lifecycle:\|^graduates_to:'` |
| `docs/architecture/c4/workspace.dsl` | `workspace "..."` block, `model { ... }` block, `views { ... }` block, at least one `systemContext` view | `grep -q '^workspace\|^[[:space:]]*model {\|^[[:space:]]*views {'` |
| `docs/architecture/c4/render.sh` | Pinned image (no `:latest`), `validate` step before `export`, `--user` flag on every `docker run`, exit codes documented in header | `grep -q 'STRUCTURIZR_VERSION=' && grep -q 'validate -workspace' && grep -q -- '--user'` |
| `docs/architecture/arc42/02-constraints.md` | `# 2. Architecture Constraints`, `## 2.1 Technical Constraints`, `## 2.2 Organizational Constraints`, `## 2.3 Legal and Regulatory Constraints` | `grep -q '## 2.1 Technical\|## 2.2 Organizational\|## 2.3 Legal'` |
| `docs/architecture/arc42/03-context.md` | `# 3. Context and Scope`, `## 3.1 Business Context` (with embedded `systemContext.svg`), `## 3.2 Technical Context` | `grep -q '## 3.1 Business Context\|## 3.2 Technical Context'` |
| `docs/architecture/arc42/04-solution-strategy.md` | `# 4. Solution Strategy`, `## 4.1 Technology Decisions`, `## 4.2 Top-Level Decomposition`, `## 4.3 Quality Goal` | `grep -q '## 4.1 Technology\|## 4.3 Quality Goal'` |
| `docs/architecture/arc42/05-building-blocks.md` | `# 5. Building Block View`, `## 5.1 Whitebox Overall System` with containers table including `Domain aggregates implemented` column, at least one `## 5.2.x` drill | `grep -q '## 5.1 Whitebox\|Domain aggregates implemented'` |
| `docs/architecture/arc42/06-runtime-view.md` | `# 6. Runtime View`, at least one `## 6.x` scenario subsection with `SCN-NN` ID + step table + a `<!-- arch-figure … -->` block (figure from `arch-c4` dynamic or `arch-uml sequence`). Owned by `arch-arc42` per ADR-0004; marker/figure integrity in Check 7a. | `grep -q '## 6\.\|SCN-[0-9]'` |
| `docs/architecture/arc42/07-deployment.md` | `# 7. Deployment View`, `## 7.1` overview, at least one per-environment `### Production` (or named env), Mapping table | `grep -q '## 7.1\|Mapping of building blocks'` |
| `docs/architecture/arc42/08-cross-cutting-concepts.md` | `# 8. Cross-Cutting Concepts`, `## Concept catalogue` table with `CC-NN` IDs and `Applies to` column | `grep -q '## Concept catalogue\|CC-[0-9]'` |
| `docs/architecture/arc42/11-risks.md` | `# 11. Risks and Technical Debt`, `## 11.1 Active Risks` table with `RSK-NN` IDs, `## 11.2 Technical Debt` | `grep -q '## 11.1\|RSK-[0-9]'` |

**Detection (example for process doc):**
```bash
find docs/business/05a-processes -name "proc-*.md" 2>/dev/null | while read f; do
  grep -q 'KPI\|§8' "$f" || echo "MISSING KPIs: $f"
done

# Service contracts
find docs/architecture/interfaces -name "*.md" ! -name "cli-*.md" 2>/dev/null | while read f; do
  grep -q '§0 Traceability' "$f" || echo "MISSING §0 Traceability: $f"
  grep -q '§3 Error contract' "$f" || echo "MISSING §3 Error contract: $f"
  grep -q '§4 Versioning' "$f" || echo "MISSING §4 Versioning: $f"
  grep -q '§5 Security' "$f" || echo "MISSING §5 Security surface: $f"
done

# CLI contracts
find docs/architecture/interfaces -name "cli-*.md" 2>/dev/null | while read f; do
  grep -q '§0 Traceability' "$f" || echo "MISSING §0 Traceability: $f"
  grep -q 'Command catalogue' "$f" || echo "MISSING §2 Command catalogue: $f"
  grep -q '§5 Output contract' "$f" || echo "MISSING §5 Output contract: $f"
  grep -q '§7 Error contract' "$f" || echo "MISSING §7 Error contract: $f"
done
```

Leftover local `## Open Items` tables are not a mandatory-section finding — they are a
transitional relic swept by Check 18a instead.

**Severity:** Error

**Proposed fix template:** "Add missing section `{section}` to `{file}`. Template in `{skill} audit-report-template.md §{N}`."

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

**Proposed fix template:** "Add the 2-line methodology pointer blockquote to `{file}` header. Copy from `~/.claude/skills/{skill}/audit-methodology.md` first paragraph."

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

**What:** verifies that every `docs/**/*.md` file opens with the standard artefact frontmatter block and that all required fields are present, valid, and consistent; and that the OKF reserved `index.md` files are correct — the root declares `okf_version`, and no `index.md` is stale (older than an artefact in its subtree, since a frontmatter-free index is not covered by the `review_interval` staleness check).

**Schema (canonical — defined in this skill's `references/artefact-frontmatter.md`, an OKF v0.1 superset):**
- Always present, hard-required: `type` (OKF-required), `title`, `status`, `owner`, `last_reviewed`, `review_interval`
- Always present, OKF-recommended (Warning if missing during adoption): `description`, `tags`, `timestamp`
- Conditional: `resource` present only when the artefact has an external asset; `superseded_by` required when `status: superseded`; `supersedes` present only on documents created to replace another
- Valid `status` values: `draft`, `active`, `superseded`, `deprecated`
- `type` value: must equal a canonical `okf_type` display name from this skill's `references/artefact-types-registry.yaml` (a value outside the set is tolerated by OKF but flagged Warning — "unregistered type")
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
# this skill's `references/artefact-frontmatter.md` they carry no artefact frontmatter). The root
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
  #     is derived at run time from the okf_type fields of
  #     this skill's `references/artefact-types-registry.yaml` — keep in sync when a type is added.
  #     A value outside the set is tolerated by OKF but flagged (unregistered).
  type_val=$(fm type)
  if [ -n "$type_val" ]; then
    # Derive the enum from the registry — never hardcode display names here.
    okf_types=$(python3 -c "import yaml;print('|'.join(t['okf_type'] for t in yaml.safe_load(open('<metamodel-skill-dir>/references/artefact-types-registry.yaml'))['artefact_types']))")
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

# Stale-index check. Also run standalone by Mode 4 (freshness) — see SKILL.md.
# Because index.md is frontmatter-free it is NOT covered by
# the review_interval staleness check, so verify freshness directly: an index is
# stale if any artefact in its subtree was committed more recently than the index
# itself. Uses git commit time (last-committed epoch); an uncommitted file (empty
# git time) is treated as "now" — a new uncommitted artefact correctly marks the
# index stale, and a just-regenerated index counts as fresh. `command find`
# bypasses any wrapped find (see the IMPORTANT note earlier in this check).
now=$(date +%s)
git_ct() {  # last-commit epoch of "$1", or "now" when uncommitted / untracked
  local t; t=$(git log -1 --format=%ct -- "$1" 2>/dev/null)
  [ -n "$t" ] && echo "$t" || echo "$now"
}
command find docs -name 'index.md' ! \( $EXCLUDED \) 2>/dev/null | while IFS= read -r idx; do
  dir=$(dirname "$idx")
  idx_t=$(git_ct "$idx")
  newest=0; newest_f=""
  while IFS= read -r a; do
    at=$(git_ct "$a")
    [ "$at" -gt "$newest" ] && { newest=$at; newest_f=$a; }
  done < <(command find "$dir" -name '*.md' ! -name 'index.md' ! -name 'log.md' ! -name 'README.md' ! \( $EXCLUDED \) 2>/dev/null)
  if [ -n "$newest_f" ] && [ "$newest" -gt "$idx_t" ]; then
    echo "STALE INDEX: $idx — newer artefact committed since last refresh ($newest_f); regenerate via the Scaffold mode Mode 3"
  fi
done
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
- Stale `index.md` (an artefact in its subtree was committed more recently) → Warning

**Proposed fix template:**
- Missing block: "Add standard frontmatter to `{file}` using this skill's `references/artefact-frontmatter.md` schema (OKF superset). Run `git config user.name` for owner."
- Missing `type`: "Add `type: <okf_type>` to `{file}` — use the artefact's display name from the OKF type table in this skill's `references/artefact-types-registry.yaml`."
- Unregistered type: "Change `type:` in `{file}` to a canonical `okf_type` display name, or register the new type in this skill's `references/artefact-types-registry.yaml` + this check's enum."
- Missing field: "Add `{field}:` to the frontmatter of `{file}`."
- Invalid status: "Set `status:` in `{file}` to one of: `draft`, `active`, `superseded`, `deprecated`."
- Missing `superseded_by`: "Add `superseded_by: <path-to-replacement>` to `{file}` frontmatter."
- Dead target: "Update `superseded_by` / `supersedes` path in `{file}` — target file no longer exists at `{path}`."
- Root index: "Create `docs/index.md` (OKF bundle root: `okf_version: \"0.1\"` frontmatter + navigation body) via the Scaffold mode."
- Stale index: "Regenerate `{index}` via the Scaffold mode Mode 3 (refresh) — an artefact in its subtree (`{newest_file}`) changed after the index was last updated."

---

## Check 18 — Open items governance

**What:** verifies that the central ledger — `docs/project-control/open-items/open-items.md`
under `markdown`, or GitHub Issues under `github` — conforms to
this skill's `references/open-items-governance.md`. Since [ADR-0005](../../../docs/architecture/decisions/adr-0005-open-items-ledger-sole-authoring-surface.md)
retired the per-artefact local `## Open Items` section, there is only one surface to check —
no local-vs-ledger reconciliation is possible or needed.

It is **report-only** — findings are surfaced to the operator; remediation is always done
through `util-open-items` (sync, triage, close, archive) or direct ledger edits. The audit
never mutates the ledger, artefact bodies, or GitHub.

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
| 18a Stale local-section relic sweep | run as written | run as written (a leftover local table is a relic regardless of backend) |
| 18b Ledger schema compliance | run as written | not applicable — no literal table; see 18g |
| 18c Source-location provenance & resolution | run as written | **github variant** — reads provenance body sections via `gh`; applies only to issues that carry them |
| 18e Closure drift | scan ledger rows | **github variant** — structurally enforced; verify the closing reference exists |
| 18f Stale open items | ledger `Due / Review date` | **github variant** — open issues' Milestone due date (Project field retired — ADR-0008) |
| 18g Form / slug integrity | — | **github only** — valid `type:` label (§2a) + canonical slug fields where provenance sections are present |
| 18h Trustworthy `ready-for-agent` queue | — | **github only** — readiness-contract precondition + label hygiene on closed issues |
| 18i Axis exclusivity | — | **github only** — at most one label per axis |

(18d is retired — see below.) Everything stays **report-only**; remediation routes through
`util-open-items`.

**Population (`github` — ADR-0009 §3).** The retired `open-item` marker label is NOT a
population selector: under this backend the repo's issue tracker *is* the ledger, so the
github sub-checks read **all issues**. Structural checks (18g type label, 18h, 18i) apply
to every issue; provenance/slug checks (18c, the field half of 18g) apply only to issues
whose body carries the provenance sections (`### Source artefact` / `### Source anchor` /
`### Source heading`) — `type:bug` / `type:feature` issues are tracker-native and normally
carry none. Execution-layer fields — `type`, `priority`, `size`, readiness,
`in-progress`/`blocked` — are read from **labels** via the slug map
(`util-open-items/references/github-backend.md` §2, §2a, §2b), never parsed from body
text; `type` is read back through the §2a governance mapping (`type:docs`→`doc-gap`,
`type:task`→`decision-gap`/`execution-item`, `type:tech-debt`→`tech-debt`).

### Sub-check 18a — Stale local-section relic sweep (transitional)

**What:** per ADR-0005, no artefact may carry a local `## Open Items` table any more — the
ledger is the sole authoring surface (rule §1). Any such table found outside the ledger/
archive path is a leftover from the retired contract and must be deleted, not reconciled.
This also keeps the legacy-heading-variant sweep from the pre-ADR-0005 contract, since those
variants are malformed regardless of surface.

**Detection:**

```bash
# 1. Any ## Open Items table outside the ledger + archive path is a stale relic.
rg -n '^## Open Items$' docs/ 2>/dev/null | grep -v '^docs/project-control/open-items/'

# 2. Forbidden legacy heading variants (must return zero matches, anywhere)
rg -n '^## Open / TODO$|^## Open TODOs$|^## Open questions remaining$|^## Open questions for next interview$|^## Open questions for next workshop / research wave$|^## 11\. Open TODOs' docs/ business-* arch-* spec-* domain-* ops-* com-* util-* 2>/dev/null

# 3. Legacy wording in discipline / SKILL docs
rg -n '§Open Issues|Open Issues' docs/ business-* arch-* spec-* domain-* 2>/dev/null
```

**Severity:** Error

**Proposed fix template:** "Delete the local `## Open Items` table in `{file}` — file its
rows directly to the central ledger via `util-open-items` if they are not already there,
then remove the table (this skill's `references/open-items-governance.md` §1, ADR-0005)."

### Sub-check 18b — Ledger schema compliance

**What:** the ledger table (and every archive bucket) uses the canonical column order and
column names from §4 of this skill's `references/open-items-governance.md`. Columns must not be removed or
reordered; additional informational columns are permitted only **after** `Tracker ref`.

**Detection:**

```bash
for f in docs/project-control/open-items/open-items.md docs/project-control/open-items/archive/*.md; do
  [ -f "$f" ] || continue
  header=$(awk '
    /^## Open Items[[:space:]]*$/ { in_section=1; next }
    in_section && /^## / { in_section=0 }
    in_section && /^\|/ { print; exit }
  ' "$f")
  echo "$header" | grep -qE '\|[[:space:]]*OI-ID[[:space:]]*\|[[:space:]]*Type[[:space:]]*\|[[:space:]]*Summary[[:space:]]*\|[[:space:]]*Source artefact[[:space:]]*\|[[:space:]]*Source anchor[[:space:]]*\|[[:space:]]*Source heading[[:space:]]*\|[[:space:]]*Resolution path[[:space:]]*\|[[:space:]]*Priority[[:space:]]*\|[[:space:]]*Status[[:space:]]*\|[[:space:]]*Owner[[:space:]]*\|[[:space:]]*Due / Review date[[:space:]]*\|[[:space:]]*Tracker ref' || \
    echo "SCHEMA NON-COMPLIANT: $f — header is: $header"
done
```

**Severity:** Error

**Proposed fix template:** "Restore canonical column order in `{file}`. Canonical order:
`OI-ID | Type | Summary | Source artefact | Source anchor | Source heading | Resolution
path | Priority | Status | Owner | Due / Review date | Tracker ref`. Additional columns are
allowed only after `Tracker ref`."

### Sub-check 18c — Source-location provenance & resolution

**What:** every ledger/issue row has both `Source anchor` and `Source heading` populated
(or both empty for a genuine central-only row, governance §5.2), **and** its
`Source artefact` resolves to a real file when one is cited. This subsumes the old
local-vs-ledger sync check (retired 18d below) — there is nothing left to sync against, but
a row's provenance can still point at a file that was renamed or deleted, which is exactly
what this check catches.

**Detection (`markdown`):**

```bash
for f in docs/project-control/open-items/open-items.md docs/project-control/open-items/archive/*.md; do
  [ -f "$f" ] || continue
  awk -v F="$f" '
    /^## Open Items[[:space:]]*$/ { in_section=1; row=0; next }
    in_section && /^## / { in_section=0 }
    in_section && /^\|/ {
      row++
      if (row <= 2) next
      n = split($0, cols, "|")
      oi = cols[2]; gsub(/^[[:space:]]+|[[:space:]]+$/, "", oi)
      artefact = cols[5]; gsub(/^[[:space:]]+|[[:space:]]+$/, "", artefact)
      anchor = cols[6]; gsub(/^[[:space:]]+|[[:space:]]+$/, "", anchor)
      heading = cols[7]; gsub(/^[[:space:]]+|[[:space:]]+$/, "", heading)
      if (heading == "_central-only_") next
      if (anchor == "" || anchor == "_TBD_" || heading == "" || heading == "_TBD_") {
        printf "PROVENANCE MISSING: %s row %s (OI=%s anchor=%s heading=%s)\n", F, NR, oi, anchor, heading
      }
      gsub(/`/, "", artefact)
      if (artefact != "" && system("test -f \"" artefact "\"") != 0) {
        printf "DANGLING SOURCE ARTEFACT: %s row %s (OI=%s) cites %s, which does not exist\n", F, NR, oi, artefact
      }
    }
  ' "$f"
done
```

**Severity:** Warning

**Proposed fix template:** "Populate `Source anchor` and `Source heading` for row
`{OI-ID}` in `{file}` (use `_central-only_` only when the row has no in-artefact origin), or
fix `Source artefact` — it currently points at a file that no longer exists (§4 of
this skill's `references/open-items-governance.md`)."

**github variant** (requires `gh` auth). Population: **all** open issues (no marker label —
ADR-0009 §3); the check applies only to issues whose body carries provenance sections.
Read the same fields from the issue body and check `source_artefact` resolves:

```bash
if [ "$backend" = "github" ]; then
  gh issue list -R "$repo" --state open --json number,body \
    -q '.[] | [(.number|tostring), (.body // "")] | @tsv' \
  | while IFS=$'\t' read -r n body; do
    # Provenance-scoped: tracker-native issues (bug/feature) carry no provenance
    # sections and are skipped, not flagged.
    echo "$body" | grep -qi 'Source artefact' || continue
    artefact=$(echo "$body" | grep -A1 -i 'source_artefact\|Source artefact' | tail -1 | xargs)
    heading=$(echo "$body" | grep -A1 -i 'source_heading\|Source heading' | tail -1 | xargs)
    [ "$heading" = "_central-only_" ] && continue
    [ -n "$artefact" ] && [ ! -f "$artefact" ] && \
      echo "DANGLING SOURCE ARTEFACT: issue #$n cites $artefact, which does not exist"
  done
fi
```

### Sub-check 18d — Retired

Tracker sync coverage (local `OI-NNNN`/`#N` vs. the central ledger) is retired: per
ADR-0005 there is no local surface left to be out of sync with. Its useful half —
verifying a row's `Source artefact` actually exists — is now covered by 18c.

### Sub-check 18e — Closure drift

**What:** rows whose `Status` is `closed` or `dropped` must carry a non-`_TBD_`
`Tracker ref`. Closure must be evidenced (§3 of this skill's `references/open-items-governance.md`).

**Detection:**

```bash
ledger="docs/project-control/open-items/open-items.md"
[ -f "$ledger" ] && awk -v F="$ledger" '
  /^## Open Items[[:space:]]*$/ { in_section=1; row=0; next }
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
  gh issue list -R "$repo" --state closed \
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
ledger="docs/project-control/open-items/open-items.md"
today=$(date +%s)
[ -f "$ledger" ] && awk -v F="$ledger" -v TODAY="$today" '
  /^## Open Items[[:space:]]*$/ { in_section=1; row=0; next }
  in_section && /^## / { in_section=0 }
  in_section && /^\|/ {
    row++
    if (row <= 2) next
    n = split($0, cols, "|")
    oi = cols[2]; gsub(/^[[:space:]]+|[[:space:]]+$/, "", oi)
    status = cols[10]; gsub(/^[[:space:]]+|[[:space:]]+$/, "", status)
    due = cols[12]; gsub(/^[[:space:]]+|[[:space:]]+$/, "", due)
    if (status != "open" && status != "in-progress" && status != "blocked") next
    if (due == "" || due == "_TBD_") next
    cmd = "date -d \"" due "\" +%s 2>/dev/null"
    cmd | getline due_ts
    close(cmd)
    if (due_ts == "" || due_ts == 0) next
    if (TODAY > due_ts) {
      overdue_days = int((TODAY - due_ts) / 86400)
      printf "OVERDUE %dd: %s row %s (OI=%s status=%s due=%s)\n", overdue_days, F, NR, oi, status, due
    }
  }
' "$ledger"
```

**Severity:** Warning

**Proposed fix template:** "Row `{OI-ID}` in `{file}` is `{status}` and was due
`{due date}` ({overdue days}d ago). Run `util-open-items` in `triage` mode to either
re-date, escalate priority, reassign owner, or close with a `Tracker ref`."

**github variant** (requires `gh` auth). Overdue is the **Milestone due date** on open
issues (`review_date` serialization per `github-backend.md` §2; the Project `Review date`
field was retired unwired — ADR-0008). Issues with no milestone have no review date and
are skipped:

```bash
if [ "$backend" = "github" ]; then
  today=$(date +%s)
  gh issue list -R "$repo" --state open --json number,milestone \
    -q '.[] | select(.milestone.dueOn != null) | [(.number|tostring), .milestone.dueOn] | @tsv' \
  | while IFS=$'\t' read -r n due; do
    due_ts=$(date -d "$due" +%s 2>/dev/null) || continue
    [ "$today" -gt "$due_ts" ] && echo "OVERDUE: issue #$n review date $due has passed"
  done
fi
```

### Sub-check 18g — Form / slug integrity (github only)

**What:** every open issue carries exactly one valid `type:` label from the 5-value
standard vocabulary (ADR-0009 §5; read from **labels**, never from body text or native
Issue Types — the audit reads `type` back through the §2a governance mapping, where
`type:bug`/`type:feature` are tracker-native, not governance items), and every issue whose
body carries provenance sections exposes the required slug fields. This is the github
analog of 18b/18c — it verifies conformance to the §4 slug contract (Invariant I1) so the
read-out stays machine-parseable.

**Detection** (requires `gh` auth):

```bash
if [ "$backend" = "github" ]; then
  valid="type:bug type:feature type:task type:docs type:tech-debt"
  gh issue list -R "$repo" --state open \
    --json number,labels,body \
    -q '.[] | [(.number|tostring), ([.labels[].name]|join(",")), ((.body // "")|gsub("\n";"¶"))] | @tsv' \
  | while IFS=$'\t' read -r n labels body; do
    tlabel=$(echo "$labels" | tr ',' '\n' | command grep '^type:' | head -1)
    if [ -z "$tlabel" ]; then
      echo "MISSING TYPE LABEL: issue #$n carries no type:* label"
    else
      echo "$valid" | command grep -qw -- "$tlabel" || \
        echo "INVALID TYPE LABEL: issue #$n has '$tlabel' (expected one of: $valid)"
    fi
    # Slug-field checks are provenance-scoped (ADR-0009 §2): only issues whose body
    # carries provenance sections are governance items; bug/feature issues are
    # tracker-native and skipped.
    echo "$body" | command grep -qi 'Source artefact' || continue
    echo "$body" | command grep -qi "Source heading" || \
      echo "FORM DRIFT: issue #$n body has no Source heading field"
    echo "$body" | command grep -qi "Resolution path" || \
      echo "FORM DRIFT: issue #$n body has no Resolution path field"
  done
fi
```

**Severity:** Warning

**Proposed fix template:** "Issue `#{N}` is missing `{field}` / carries type label
`{tlabel}`. Apply exactly one `type:` label from the ADR-0009 §5 vocabulary (or re-create
the issue through the per-type Issue Forms, `.github/ISSUE_TEMPLATE/1-bug.yml` …
`5-tech-debt.yml`) and restore the canonical slug fields. The form `id:` keys are the
binding contract (Invariant I1 in `util-open-items/references/github-backend.md`)."

### Sub-check 18h — Trustworthy `ready-for-agent` queue (github only)

**What:** the delegation queue (`is:open label:ready-for-agent`) is trustworthy by
construction — an issue MAY carry `ready-for-agent` only if its `### Acceptance criteria`
and `### References` body sections are non-empty AND a `size:` label is set (the ADR-0008
§3 readiness-contract precondition, restated in `github-backend.md` §2b). Any queue issue
missing one of the three is drift an agent would trip over. Second half: readiness or
`state:` labels left on **closed** issues are a hygiene finding — the closing flow removes
them at terminal state (§2b label handover), so leftovers are stale, not drift.
Report-only, like every sub-check: promotion/demotion routes through `util-open-items`
triage.

**Detection** (requires `gh` auth):

```bash
if [ "$backend" = "github" ]; then
  # Half 1 — queue precondition (ADR-0008 §3): acceptance criteria + references + size.
  gh issue list -R "$repo" --state open --label ready-for-agent \
    --json number,labels,body \
    -q '.[] | [(.number|tostring), ([.labels[].name]|join(",")), ((.body // "")|gsub("\n";"¶"))] | @tsv' \
  | while IFS=$'\t' read -r n labels body; do
    echo "$labels" | tr ',' '\n' | command grep -q '^size:' || \
      echo "QUEUE DRIFT: issue #$n is ready-for-agent but has no size: label"
    for section in "Acceptance criteria" "References"; do
      if ! echo "$body" | command grep -qi "### $section"; then
        echo "QUEUE DRIFT: issue #$n is ready-for-agent but has no '### $section' section"
      elif echo "$body" | command grep -qiE "### $section¶+_No response_"; then
        echo "QUEUE DRIFT: issue #$n is ready-for-agent but '### $section' is empty"
      fi
    done
  done

  # Half 2 — hygiene: readiness / state: labels left behind on closed issues.
  gh issue list -R "$repo" --state closed --json number,labels -L 500 \
    -q '.[] | [(.number|tostring), ([.labels[].name]|join(","))] | @tsv' \
  | while IFS=$'\t' read -r n labels; do
    stale=$(echo "$labels" | tr ',' '\n' | \
      command grep -E '^(needs-triage|ready-for-agent|needs-human|state:in-progress|state:blocked)$' | \
      paste -sd, -)
    [ -n "$stale" ] && echo "LABEL HYGIENE: closed issue #$n still carries: $stale"
  done
fi
```

**Severity:** Warning (queue precondition violated) · Info (stale labels on closed issues)

**Proposed fix template:** "Issue `#{N}` violates the `ready-for-agent` precondition
(ADR-0008 §3): missing `{acceptance criteria / references / size label}`. Run
`util-open-items` triage — either draft the missing brief and re-promote, or demote to
`needs-triage`/`needs-human`. For closed issue `#{N}`: remove the leftover
`{labels}` label(s) — the closing flow (`close`/`drop`) strips readiness/`state:` labels
at terminal state."

### Sub-check 18i — Axis exclusivity (github only)

**What:** the five label axes are mutually exclusive — no issue may carry more than one
label from the same axis (`type:*`, `priority:*`, `size:*`, the readiness trio
`needs-triage`/`ready-for-agent`/`needs-human`, `state:*`), per `github-backend.md` §2b
("one label per axis"). Two `priority:` labels make the queue sort ambiguous; two
readiness labels make routing ambiguous. Report-only.

**Detection** (requires `gh` auth):

```bash
if [ "$backend" = "github" ]; then
  gh issue list -R "$repo" --state all --json number,labels -L 500 \
    -q '.[] | [.labels[].name] as $l |
        { n: .number,
          type:  ([$l[] | select(startswith("type:"))]     | length),
          prio:  ([$l[] | select(startswith("priority:"))] | length),
          size:  ([$l[] | select(startswith("size:"))]     | length),
          ready: ([$l[] | select(. == "needs-triage" or . == "ready-for-agent" or . == "needs-human")] | length),
          state: ([$l[] | select(startswith("state:"))]    | length) } |
        select(.type > 1 or .prio > 1 or .size > 1 or .ready > 1 or .state > 1) |
        "AXIS VIOLATION: issue #\(.n) — type=\(.type) priority=\(.prio) size=\(.size) readiness=\(.ready) state=\(.state) (each must be ≤1)"'
fi
```

**Severity:** Warning

**Proposed fix template:** "Issue `#{N}` carries {count} labels on the `{axis}` axis —
keep exactly one and remove the rest (`github-backend.md` §2b: one label per axis). If
the correct value is unclear, route through `util-open-items` triage."

### Summary — Check 18 outputs

| Sub-check | Severity | Backend | What it flags |
| :-- | :-- | :-- | :-- |
| 18a Stale local-section relic sweep | Error | both | Leftover local `## Open Items` table (ADR-0005 relic); forbidden legacy headings |
| 18b Ledger schema compliance | Error | `markdown` | Missing / reordered canonical columns in the ledger or an archive bucket |
| 18c Source-location provenance & resolution | Warning | both | Empty / `_TBD_` `Source anchor`/`Source heading` (excludes `_central-only_`); `Source artefact` pointing at a nonexistent file (github: provenance-section-scoped) |
| 18d Tracker sync coverage | — | — | **Retired** (ADR-0005) — no local surface left to sync against; see 18c |
| 18e Closure drift | Error | markdown: ledger · github: closing-ref | Terminal rows / issues without evidencing `Tracker ref` |
| 18f Stale open items | Warning | markdown: `Due / Review date` · github: Milestone due date | Active rows / issues past their review date |
| 18g Form / slug integrity | Warning | **github only** | Issues missing a valid `type:` label (§2a); provenance-carrying issues missing canonical slug fields |
| 18h Trustworthy `ready-for-agent` queue | Warning · Info | **github only** | Queue issues missing acceptance criteria / references / `size:` (ADR-0008 §3); readiness/`state:` labels left on closed issues |
| 18i Axis exclusivity | Warning | **github only** | Issues carrying more than one label from the same axis |

All sub-checks are read-only; none write to `docs/project-control/open-items/`, to any
artefact, or to GitHub. Findings always route to the operator for action through
`util-open-items`.

---

## Check 19 — Capability / product slug integrity

**What:** verifies the **canonical `slug`** (the third identifier, alongside `C-N.M` and the display name — see this skill's `references/artefact-types-registry.yaml` § Canonical slugs) is **present**, **well-formed**, and **globally unique** across one flat namespace. Three concepts carry a slug: every L0 capability domain (`## CN · …`) and L1 capability (`### CN.M · …`) in `docs/business/03a-capability-map.md`, and every product (the H1, plus each L0 product section of a product-family FBS) in `docs/product-specs/07a-fbs.md`.

**Slug line contract:** a backtick-wrapped code-line on its own line, directly under the entity heading — `` `slug: <handle>` `` — parseable as `` ^\s*`slug:\s*([a-z0-9]+(?:-[a-z0-9]+)*)`\s*$ ``. Well-formed = kebab-case, `[a-z0-9]` words joined by single hyphens, no leading/trailing/double hyphens; recommended **≤ 20 chars**.

> **Wrapper-safe by construction.** All three blocks drive `awk` directly over the two
> known files — no `grep`/`find` inside loops and **no process substitution** (`<(…)`),
> which the interactive shell's wrapped `grep` mishandles (see the IMPORTANT note in Check 17).
> The slug-line recogniser matches loosely (`` `slug:…` ``) and validates the captured value,
> so a malformed value (uppercase, underscores) is reported as `MALFORMED`, not silently
> mistaken for a missing slug.

**Detection — 19a: capability-map presence + malformed + length.** Every `## CN · …` (L0) and
`### CN.M · …` (L1) heading must be followed — within 2 lines, skipping blanks — by a
well-formed slug code-line:
```bash
capmap="docs/business/03a-capability-map.md"
[ -f "$capmap" ] && awk '
  function chk(line, head,   s) {
    s=line; sub(/^[[:space:]]*`slug:[[:space:]]*/,"",s); sub(/`[[:space:]]*$/,"",s)
    if (s=="")                              { printf "MALFORMED SLUG (empty): %s (%s)\n", FILENAME, head; return }
    if (s !~ /^[a-z0-9]+(-[a-z0-9]+)*$/)    printf "MALFORMED SLUG \"%s\": %s (%s)\n", s, FILENAME, head
    else if (length(s) > 20)                printf "SLUG >20 CHARS \"%s\" (%d): %s (%s)\n", s, length(s), FILENAME, head
  }
  function flush() { if (pend!="" && !seen) printf "MISSING SLUG: %s heading \"%s\"\n", FILENAME, pend }
  /^##+[[:space:]]+C[0-9]/                  { flush(); pend=$0; seen=0; gap=0; next }
  pend!="" {
    if ($0 ~ /^[[:space:]]*$/)                     { gap++; if(gap>2){flush();pend=""}; next }
    if ($0 ~ /^[[:space:]]*`slug:.*`[[:space:]]*$/) { seen=1; chk($0,pend); pend=""; next }
    gap++; if(gap>2){flush();pend=""}
  }
  END { flush() }
' "$capmap"
```

**Detection — 19b: FBS H1 product slug (mandatory).** The FBS root product carries a slug
under the H1, before the first `## ` section:
```bash
fbs="docs/product-specs/07a-fbs.md"
[ -f "$fbs" ] && awk '
  /^#[[:space:]]/ && !h1 { h1=1; want=1; next }
  want {
    if ($0 ~ /^##[[:space:]]/)                     { print "MISSING PRODUCT SLUG: " FILENAME " (no slug under H1)"; want=0; next }
    if ($0 ~ /^[[:space:]]*`slug:.*`[[:space:]]*$/) {
      s=$0; sub(/^[[:space:]]*`slug:[[:space:]]*/,"",s); sub(/`[[:space:]]*$/,"",s)
      if (s !~ /^[a-z0-9]+(-[a-z0-9]+)*$/)          print "MALFORMED PRODUCT SLUG \"" s "\": " FILENAME
      else if (length(s)>20)                        printf "PRODUCT SLUG >20 CHARS \"%s\" (%d): %s\n", s, length(s), FILENAME
      want=0
    }
  }
  END { if (want) print "MISSING PRODUCT SLUG: " FILENAME " (no slug under H1)" }
' "$fbs"
```

**Detection — 19c: global uniqueness (one flat namespace across both files).** Emit
`(slug, heading-id)` pairs and flag any well-formed slug that names **> 1 distinct entity**.
Keying on the heading ID lets the one sanctioned repeat through — the same product appearing
as both a BC Map L0 item (product axis) and an FBS L0 section shares the same C-ID, so it is
ONE identifier, not a collision:
```bash
capmap="docs/business/03a-capability-map.md"; fbs="docs/product-specs/07a-fbs.md"
for f in "$capmap" "$fbs"; do
  [ -f "$f" ] || continue
  awk '
    /^#[[:space:]]/          { id="H1" }
    /^##+[[:space:]]+C[0-9]/ { id=$2 }   # e.g. "C1" or "C1.2"
    /^[[:space:]]*`slug:.*`[[:space:]]*$/ {
      s=$0; sub(/^[[:space:]]*`slug:[[:space:]]*/,"",s); sub(/`[[:space:]]*$/,"",s)
      if (s ~ /^[a-z0-9]+(-[a-z0-9]+)*$/) print s "\t" id
    }
  ' "$f"
done | sort -u | awk -F'\t' '{c[$1]++} END{for(s in c) if(c[s]>1) print "DUPLICATE SLUG (>1 entity): " s}'
```

**Interpretation:**
- `MISSING SLUG` / `MISSING PRODUCT SLUG` → a mandatory slug is absent. **Error.**
- `MALFORMED SLUG` → not valid kebab-case. **Error.**
- `SLUG >20 CHARS` → over the recommended ceiling. **Warning** (recommendation, not a hard limit).
- `DUPLICATE SLUG (>1 entity)` → two different domains/capabilities/products share a slug — the flat commit-scope namespace is ambiguous. **Error.**

**Severity:** Error (missing · malformed · duplicate) · Warning (> 20 chars).

**Proposed fix template:**
- Missing: "Add a `` `slug: <handle>` `` code-line under `{heading}` in `{file}` — run `business-capability-map` (fill) or `spec-functional-breakdown-structure` for an assisted `slugify(name)` proposal. The slug is a mandatory third identifier (this skill's `references/artefact-types-registry.yaml` § Canonical slugs)."
- Malformed: "Fix slug `{slug}` in `{file}` to kebab-case (`[a-z0-9]` words joined by single hyphens)."
- Over length: "Shorten slug `{slug}` in `{file}` to ≤ 20 chars while keeping it meaningful."
- Duplicate: "Slug `{slug}` names two different entities across the capability map + FBS. Rename one — this is an ID-rename: update every consumer that pinned it (commit-scope allowlist, anchors) and log it in the changelog."
