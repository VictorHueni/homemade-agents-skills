# Path Migration v2 — Canonical Paths Mapping Table

This file is the single source of truth for the v1 → v2 metamodel path simplification.

- **v1 paths:** nested subfolders with redundant names (e.g. `personas/personas.md`)
- **v2 paths:** numbered flat files for singletons; multi-file artefacts unchanged

Used by `util-metamodel-migration` Mode 4 to generate project migration scripts.
Used by the kit maintainer as the authoritative reference when updating skill files.

---

## Naming convention (v2)

| Context | Pattern | Example |
|---|---|---|
| Primary singleton (business / spec) | `docs/{layer}/NNa-{slug}.md` | `docs/business/01a-personas.md` · `docs/product-specs/07a-fbs.md` |
| Fractional / sub-step artefact (business) | `docs/business/NNb-{slug}.md` | `docs/business/04b-objectives.md` |
| BMC / VS companion VPC | `docs/business/NNa-vpc-{segment}.md` | `docs/business/02a-vpc-enterprise.md` |
| Domain singleton (NO step prefix on file) | `docs/domain/{slug}.md` | `docs/domain/02b-bounded-contexts.md` · `docs/domain/02c-glossary.md` |
| Domain model (per BC, step prefix on folder) | `docs/domain/07b-models/{bc-slug}.md` | `docs/domain/07b-models/scheduling.md` |
| Multi-file artefact folder (step-scoped) | `docs/business/NNa-{slug}/` | `docs/business/06a-models/{slug}.md` |
| Multi-file artefact (slug, no step prefix) | unchanged | `docs/business/05a-processes/proc-NN-{slug}.md` |
| Numbered multi-file artefact | unchanged | `docs/product-specs/prds/prd-{NNNN}-{feature}.md` |

**Rules:**
- Step numbers zero-pad to 2 digits **plus a letter** to identify ordering: `01a`, `02a`, `03a`, `04a`, `07a`, `08a`, `09a` (primary singleton at each step).
- The `a` letter is **explicit, not implicit** — `01a-personas.md` (primary), `01b-…` (secondary at the same step), `01c-…` (tertiary), etc. This avoids visual ambiguity where bare `01-` would silently mean "step 1 primary" alongside other `01b-` siblings.
- **Fractional / sub-step artefacts** in the business layer use letter increments: `04b` (between Step 4 and Step 5).
- **Domain singleton files have NO step prefix** — `docs/domain/02b-bounded-contexts.md`, `docs/domain/02b-context-map.md`, `docs/domain/02c-glossary.md`. The `docs/domain/` folder scope is the discriminator; step numbering applies to the business and spec layers only.
- **Domain model subfolder** (`docs/domain/07b-models/`) uses the step prefix on the FOLDER, not on the files inside — `{bc-slug}.md` is the scoping discriminator.
- **Multi-file artefact folders** use the step-letter prefix on the FOLDER (e.g. `06a-models/`), and the files inside follow the originating skill's own naming (`qm-NN-{topic}.md` for quantitative models — no step collision because the parent folder scopes them).
- `docs/VISION.md` stays at root regardless of numbering — agent context visibility takes priority over filesystem ordering.

---

## Full before → after mapping

| Step | Artefact | v1 path (old) | v2 path (new) | Type |
|---|---|---|---|---|
| 0 | Product Vision | `docs/VISION.md` | `docs/VISION.md` | no-change |
| 1 | Personas | `docs/business/personas/personas.md` | `docs/business/01a-personas.md` | singleton |
| 2 | Business Model Canvas | `docs/business/business-model-canvas/business-model-canvas.md` | `docs/business/02a-bmc.md` | singleton |
| 2 | Lean Canvas (variant) | `docs/business/business-model-canvas/lean-canvas.md` | `docs/business/02a-lean-canvas.md` | singleton |
| 2 | BMC Value Proposition Canvas | `docs/business/business-model-canvas/value-proposition-canvas-{segment}.md` | `docs/business/02a-vpc-{segment}.md` | multi-slug |
| 2b | Bounded Contexts | `docs/domain/bounded-contexts/bounded-contexts.md` | `docs/domain/02b-bounded-contexts.md` | singleton |
| 2b | Context Map | `docs/domain/bounded-contexts/context-map.md` | `docs/domain/02b-context-map.md` | singleton |
| 2c | Domain Glossary | `docs/domain/glossary/glossary.md` | `docs/domain/02c-glossary.md` | singleton |
| 3 | Capability Map | `docs/business/capability-map/capability-map.md` | `docs/business/03a-capability-map.md` | singleton |
| 4 | Value Streams | `docs/business/value-streams/value-streams.md` | `docs/business/04a-value-streams.md` | singleton |
| 4 | VS Value Proposition Canvas | `docs/business/value-streams/value-proposition-canvas-{segment}.md` | `docs/business/04a-vpc-{segment}.md` | multi-slug |
| 4b | Business Objectives | `docs/business/objectives/objectives.md` | `docs/business/04b-objectives.md` | singleton |
| 5 | Business Processes | `docs/business/processes/{slug}-process.md` | `docs/business/05a-processes/proc-NN-{slug}.md` | multi-file folder |
| 6 | Quantitative Models | `docs/business/models/{slug}.md` | `docs/business/06a-models/qm-NN-{topic}.md` | multi-file folder |
| 6 (supporting) | Competitive Landscape | `docs/business/competitive-landscape/competitive-landscape.md` | `docs/business/01b-competitive-landscape/cl-NN-{slug}.md` + `CO-NN-{slug}.md` for competitor profiles | singleton-folder (Pattern B inside) |
| 7 | FBS | `docs/product-specs/functional-breakdown-structure/FBS.md` | `docs/product-specs/07a-fbs.md` | singleton |
| 7b | Domain Model (per BC) | `docs/domain/{bc-slug}/domain-model.md` | `docs/domain/07b-models/{bc-slug}.md` | multi-file folder |
| 8 | Delivery Roadmap | `docs/product-specs/delivery-roadmap/delivery-roadmap.md` | `docs/plans/delivery-roadmap.md` | singleton |
| 9 | Quality Attributes | `docs/product-specs/quality-attributes/quality-attributes.md` | `docs/product-specs/09a-quality-attributes.md` | singleton |
| 10 | PRDs | `docs/product-specs/{NNNN}_prd_{feature}.md` | `docs/product-specs/prds/prd-{NNNN}-{feature}.md` | pattern-b-rename |
| 11 | Implementation Plans | `docs/plans/active/{NNNN}_{slug}/` | `docs/plans/active/{NNNN}_exec_{slug}.md` | pattern-b-rename |
| 8† | Delivery Roadmap (pre-ADR-0009 `spec-` location) | `docs/product-specs/08a-delivery-roadmap.md` | `docs/plans/delivery-roadmap.md` | plan-split-move |
| 11† | Implementation Plans (pre-ADR-0009 `spec-` location) | `docs/exec-plans/active/{NNNN}_exec_{slug}.md` | `docs/plans/active/{NNNN}_exec_{slug}.md` | plan-split-move |
| — | ADRs | `docs/architecture/decisions/{NNNN}-{slug}.md` | `docs/architecture/decisions/adr-{NNNN}-{slug}.md` | pattern-b-rename |
| — | Ops Runbooks | `docs/ops/runbooks/{slug}.md` | `docs/ops/runbooks/{slug}.md` | no-change |
| — | Ops RCAs | `docs/ops/rcas/{YYYY-MM-DD}-{slug}.md` | `docs/ops/rcas/{YYYY-MM-DD}-{slug}.md` | no-change |
| — | Ideas | `docs/ideas/{slug}.md` or `docs/ideas/{domain}/{slug}.md` | `docs/discovery/ideation/IDEA-{NNNN}-{slug}.md` + flat `INDEX.md` (domain becomes a frontmatter tag, not a subfolder) | pattern-c-discovery-promote |
| — | Discovery Research | `docs/business/discovery/interviews/` | `docs/discovery/interviews/` | pattern-c-discovery-promote |
| — | Discovery Workshops | `docs/business/discovery/workshops/` | `docs/discovery/workshops/` | pattern-c-discovery-promote |

---

## Mode 4 implementation notes

### Variable substitution rules

When matching v1 paths containing variables:

| Variable | What it matches | v2 treatment |
|---|---|---|
| `{slug}` | kebab-case file name (e.g. `my-process`) | Pass through unchanged |
| `{segment}` | customer segment slug | Pass through unchanged |
| `{bc-slug}` | bounded context slug (e.g. `scheduling`) | In v2 domain models: **becomes the filename** — `docs/domain/my-bc/domain-model.md` → `docs/domain/07b-models/my-bc.md` |
| `{NNNN}` | 4-digit zero-padded number | Pass through unchanged |
| `{YYYY-MM-DD}` | date string | Pass through unchanged |

### Relative path recomputation

When a file moves, all inbound `[text](path)` links must be recomputed. **Do NOT string-substitute `../` chains** — the depth change makes simple substitution wrong.

Instead, for each linking file `L` and each moved file `F`:
```python
import os
new_rel = os.path.relpath(F_new_abs, os.path.dirname(L_abs))
# Replace old_rel with new_rel in L
```

Depth change examples:
- `docs/business/personas/personas.md` (depth 3) → `docs/business/01a-personas.md` (depth 2)
  - A link from `docs/product-specs/07a-fbs.md` was `../business/personas/personas.md`
  - After move: `../business/01a-personas.md` (loses one `../`)
- `docs/domain/glossary/glossary.md` (depth 3) → `docs/domain/02c-glossary.md` (depth 2)
  - A link from `docs/domain/07b-models/scheduling.md` was `../glossary/glossary.md`
  - After move: `../02c-glossary.md`

### Domain model consolidation (special case)

The v1 pattern `docs/domain/{bc-slug}/domain-model.md` creates one folder per BC.
The v2 pattern `docs/domain/07b-models/{bc-slug}.md` consolidates into a single step-prefixed folder.

Detection:
```bash
find docs/domain -mindepth 2 -name "domain-model.md" | while read f; do
  bc_slug=$(basename $(dirname "$f"))
  echo "mv: $f -> docs/domain/07b-models/${bc_slug}.md"
done
```

Also check for other files in the `docs/domain/{bc-slug}/` folders before deleting them.
If any non-domain-model files are present, report as a warning and skip folder deletion.

### Discovery promotion (special case — `pattern-c-discovery-promote`)

The v1 layout placed two discovery artefacts under `docs/business/discovery/` and pre-PRD
ideas under `docs/ideas/`. The v2 layout promotes all three to a single top-level
`docs/discovery/` so the cross-cutting discovery family is co-located:

| v1 source | v2 destination |
| :-- | :-- |
| `docs/business/discovery/interviews/` | `docs/discovery/interviews/` |
| `docs/business/discovery/workshops/` | `docs/discovery/workshops/` |
| `docs/ideas/{slug}.md` or `docs/ideas/{domain}/{slug}.md` | `docs/discovery/ideation/IDEA-{NNNN}-{slug}.md` |

Detection + move:
```bash
# Move discovery artefacts up one level
[ -d docs/business/discovery ] && git mv docs/business/discovery docs/discovery

# Move flat ideas
if [ -d docs/ideas ]; then
  mkdir -p docs/discovery/ideation
  # Assign sequential IDEA-NNNN IDs as files are moved
  idx=1
  find docs/ideas -name "*.md" -type f | while read f; do
    slug=$(basename "$f" .md)
    # Strip any pre-existing IDEA-NNNN prefix to avoid double-prefixing
    slug=$(echo "$slug" | sed -E 's/^IDEA-[0-9]{4}-//')
    printf -v id "IDEA-%04d" $idx
    git mv "$f" "docs/discovery/ideation/${id}-${slug}.md"
    idx=$((idx + 1))
  done
  # Remove any leftover empty domain subfolders
  find docs/ideas -mindepth 1 -type d -empty -delete 2>/dev/null
  rmdir docs/ideas 2>/dev/null
fi

# Frontmatter backfill required after move:
#   - Add idea_id: IDEA-NNNN matching the filename prefix
#   - Add lifecycle: captured (or refining if §Ideas section exists; ready if §Decision exists)
#   - Add graduates_to: _TBD_ for operator to fill on next refine pass
#   - Add domain: <product|business|architecture|process|dx|ops> from the v1 subfolder name
#     (frontend/backend/infra → architecture; design/dx → dx; others → product by default)
```

Link rewrites (sed pass after move):
```bash
# In every docs/**/*.md, rewrite stale references:
sed -i -E \
  -e 's|docs/business/discovery/interviews|docs/discovery/interviews|g' \
  -e 's|docs/business/discovery/workshops|docs/discovery/workshops|g' \
  -e 's|docs/ideas/|docs/discovery/ideation/|g' \
  $(find docs -name '*.md')
```

Skill rename (one-shot — only affects projects that hardcoded the old skill names in
CLAUDE.md or in custom slash commands; the kit's own skill folders have already been
renamed):
- `business-research` → `discovery-research`
- `business-workshop` → `discovery-workshop`
- `spec-idea` → `discovery-idea`

### VISION.md — no action needed

`docs/VISION.md` stays at the root. No move, no link rewriting for VISION.md itself.
However, if Mode 4 finds any link pointing to `docs/VISION.md` using a nested path
(e.g. `../VISION.md` from inside `docs/business/`), verify the relative path is still
correct after the business-layer files move (it should be, since VISION.md doesn't move).
