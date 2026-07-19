# index.md Template (OKF bundle root) — the Scaffold mode

This file contains:
1. The full `index.md` skeleton that the skill writes to `docs/index.md` (the OKF bundle root).
2. The bash detection commands Claude runs before generating the `index.md`
   (one per canonical artefact path).

**OKF reserved file.** `index.md` is an [OKF v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) reserved filename — a directory listing for progressive disclosure, **not** an artefact concept document. It therefore does **not** carry the standard artefact frontmatter block (`title`/`status`/`owner`/`last_reviewed`/`review_interval`). The **root** `docs/index.md` carries a minimal frontmatter block declaring only `okf_version`; any **sub-folder** `index.md` a skill emits is entirely frontmatter-free. See this skill's `references/artefact-frontmatter.md` §Reserved files.

---

## §Detection — bash commands (run before generating index.md)

Run each command. Capture the result (✅ / 🔄 / ⬜) and substitute into the template below.

```bash
# Helper function — reuse for every file-based step
check_file() {
  local path="$1"
  if [ ! -f "$path" ]; then
    echo "⬜"
    return
  fi
  local total todos ratio
  total=$(wc -l < "$path" 2>/dev/null || echo 1)
  todos=$(grep -c '_TODO_' "$path" 2>/dev/null || echo 0)
  ratio=$(( todos * 100 / total ))
  [ "$ratio" -ge 50 ] && echo "🔄" || echo "✅"
}

# Helper function — for multi-file folders (processes, models, PRDs, plans)
check_folder() {
  local pattern="$1"
  local count
  count=$(find . -path "./$pattern" 2>/dev/null | wc -l)
  [ "$count" -gt 0 ] && echo "✅" || echo "⬜"
}

# Step 0 — Product Vision
S0=$(check_file "docs/VISION.md")

# Step 1 — Personas
S1=$(check_file "docs/business/01a-personas.md")

# Step 2 — Business Model Canvas (accept either variant)
if [ -f "docs/business/02a-bmc.md" ]; then
  S2=$(check_file "docs/business/02a-bmc.md")
elif [ -f "docs/business/02a-lean-canvas.md" ]; then
  S2=$(check_file "docs/business/02a-lean-canvas.md")
else
  S2="⬜"
fi

# Step 2b — Bounded Context Map
S2B=$(check_file "docs/domain/02b-bounded-contexts.md")

# Step 2c — Domain Glossary
S2C=$(check_file "docs/domain/02c-glossary.md")

# Step 3 — Capability Map
S3=$(check_file "docs/business/03a-capability-map.md")

# Step 4 — Value Streams
S4=$(check_file "docs/business/04a-value-streams.md")

# Step 4.5 — Business Objectives
S45=$(check_file "docs/business/04b-objectives.md")

# Step 5 — Business Processes (multi-file folder)
S5=$(check_folder "docs/business/05a-processes/proc-*.md")

# Step 6 — Quantitative Models (multi-file folder)
S6=$(check_folder "docs/business/06a-models/qm-*.md")

# Step 7 — Functional Breakdown Structure
S7=$(check_file "docs/product-specs/07a-fbs.md")

# Step 7b — Domain Model (multi-file folder — one file per BC)
S7B=$(check_folder "docs/domain/07b-models/*.md")

# Step 8 — Delivery Roadmap
S8=$(check_file "docs/plans/delivery-roadmap.md")

# Step 9 — Quality Attributes
S9=$(check_file "docs/product-specs/09a-quality-attributes.md")

# Step 10 — PRDs (multi-file folder)
S10=$(check_folder "docs/product-specs/prds/prd-*.md")

# Step 11 — Implementation Plans (multi-file folder)
S11=$(check_folder "docs/plans/active/*_exec_*.md")
```

---

## §Template — docs/index.md

Substitute `{placeholders}` before writing. Status emojis come from the detection block
above. Age (days since last git commit) can be computed with:
```bash
git log -1 --format="%ci" -- {path} 2>/dev/null
```
If the file has never been committed, use "—".

The frontmatter is the OKF bundle-root declaration only (`okf_version`) — **no** artefact
frontmatter fields. The rich navigation content lives entirely in the body.

---

```markdown
---
okf_version: "0.1"
---

# Documentation Stack — {Project Name}

> **Scaffolded:** {YYYY-MM-DD} · **Last refreshed:** {YYYY-MM-DD}
>
> Run the Scaffold mode Mode 3 to refresh status.
> Run the Audit mode Mode 2 for a full progress snapshot.
>
> This is the OKF bundle root `index.md` (reserved file — no artefact frontmatter).

---

## Stack progress

Status key: ✅ Done · 🔄 In progress (scaffold exists, needs filling) · ⬜ Not started

| Step | Artefact | Skill | Status | Canonical path | Last modified |
|---|---|---|---|---|---|
| 0 | Product Vision | `business-vision` | {S0} | [`docs/VISION.md`](VISION.md) | {age} |
| 1 | Personas | `business-persona` | {S1} | [`docs/business/01a-personas.md`](business/01a-personas.md) | {age} |
| 2 | Business Model Canvas | `business-model-canvas` | {S2} | [`docs/business/02a-bmc.md`](business/02a-bmc.md) | {age} |
| 2b | Bounded Context Map | `domain-bounded-context` | {S2B} | [`docs/domain/02b-bounded-contexts.md`](domain/02b-bounded-contexts.md) | {age} |
| 2c | Domain Glossary | `domain-glossary` | {S2C} | [`docs/domain/02c-glossary.md`](domain/02c-glossary.md) | {age} |
| 3 | Capability Map | `business-capability-map` | {S3} | [`docs/business/03a-capability-map.md`](business/03a-capability-map.md) | {age} |
| 4 | Value Streams | `business-value-stream` | {S4} | [`docs/business/04a-value-streams.md`](business/04a-value-streams.md) | {age} |
| 4.5 | Business Objectives | `business-objective` | {S45} | [`docs/business/04b-objectives.md`](business/04b-objectives.md) | {age} |
| 5 | Business Processes | `business-process` | {S5} | [`docs/business/05a-processes/`](business/05a-processes/) | {age} |
| 6 | Quantitative Models | `business-quantitative-model` | {S6} | [`docs/business/06a-models/`](business/06a-models/) | {age} |
| 7 | Functional Breakdown Structure | `spec-functional-breakdown-structure` | {S7} | [`docs/product-specs/07a-fbs.md`](product-specs/07a-fbs.md) | {age} |
| 7b | Domain Model | `domain-model` | {S7B} | [`docs/domain/07b-models/`](domain/07b-models/) | {age} |
| 8 | Delivery Roadmap | `plan-delivery-roadmap` | {S8} | [`docs/plans/delivery-roadmap.md`](plans/delivery-roadmap.md) | {age} |
| 9 | Quality Attributes | `spec-quality-attributes` | {S9} | [`docs/product-specs/09a-quality-attributes.md`](product-specs/09a-quality-attributes.md) | {age} |
| 10 | PRDs | `spec-prd` | {S10} | [`docs/product-specs/prds/`](product-specs/prds/) | {age} |
| 11 | Implementation Plans | `plan-implementation` | {S11} | [`docs/plans/active/`](plans/active/) | {age} |

**Summary:** ✅ {N_done} / 🔄 {N_progress} / ⬜ {N_not_started} of 16 artefact steps

**Next step:** {Step N — Artefact name} · invoke `{skill}` Mode 1 (scaffold)

---

## Supporting artefacts (run as needed — not in the linear build order)

| Artefact | Skill | Path |
|---|---|---|
| Architecture Decision Records | `arch-adr` | `docs/architecture/decisions/adr-NNNN-{slug}.md` |
| Architecture Research | `arch-research` | `docs/architecture/research/{NNNN}-{slug}.md` |
| Competitive Landscape | `business-competitive-landscape` | `docs/business/01b-competitive-landscape/` |
| Discovery Research | `discovery-research` | `docs/discovery/interviews/` |
| Discovery Workshops | `discovery-workshop` | `docs/discovery/workshops/` |
| Ops Runbooks | `ops-runbook` | `docs/ops/runbooks/{slug}.md` |
| Bug RCAs | `ops-bug-rca` | `docs/ops/rcas/{date}-{slug}.md` |
| Pre-formal Ideas | `discovery-idea` | `docs/discovery/ideation/IDEA-NNNN-{slug}.md` |
| Slide Decks | `com-slide-deck` | `docs/communication/slides/{slug}/` |
| PRD / Plan reviews | `agent-peer-review` | — (interactive, no persistent artefact) |

---

## Audit

| Tool | Purpose | Cadence |
|---|---|---|
| the Audit mode Mode 1 | Full 18-check health audit | Monthly (active) / Quarterly (maintenance) |
| the Audit mode Mode 2 | Progress snapshot | Before sprint planning |
| the Audit mode Mode 4 | Freshness check | Before research waves or presentations |
| the Scaffold mode Mode 3 | Refresh this index.md | After completing any stack step |

---

## ID conventions at a glance

| ID format | Artefact | Owning file |
|---|---|---|
| `P-NN` | Persona | `01a-personas.md` |
| `C-N.M` | Capability | `03a-capability-map.md` |
| `VS-N.M` | Value-stream stage | `04a-value-streams.md` |
| `OBJ-NN` · `KR-NN.M` | Objective · Key Result | `04b-objectives.md` |
| `BC-NN` | Bounded Context | `02b-bounded-contexts.md` |
| `BC-NN.GT-NN` | Glossary Term | `02c-glossary.md` |
| `BC-NN.AGG-NN` · `BC-NN.ENT-NN` | Aggregate · Entity | `07b-models/{bc-slug}.md` |
| `C-N.M.FXX` | Functionality | `07a-fbs.md` |
| `E-NN` | Epic | `delivery-roadmap.md` |
| `QA-XXNN` | Quality Attribute | `09a-quality-attributes.md` |
| `PRD-NNNN` | PRD | `prds/prd-NNNN-{slug}.md` |
| `ADR-NNNN` | Architecture Decision | `architecture/decisions/adr-NNNN-{slug}.md` |
```
