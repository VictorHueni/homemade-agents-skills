# Stack Audit Report Template

Copy this skeleton to `var/reports/metamodel-audit/stack-audit-{YYYY-MM-DD}.md` and fill each section.

---

```markdown
<!-- audit-version: 1.0 | generated: YYYY-MM-DD | scope: {full|business|product-specs|custom} | mode: {full|progress|links|freshness} -->

# Stack Audit — {project} — {YYYY-MM-DD}

---

## Executive summary

| Metric | Count |
|---|---|
| Steps complete (✅) | {N} / 11 |
| Steps in progress (🔄) | {N} / 11 |
| Steps not started (⬜) | {N} / 11 |
| **Errors** | **{N}** |
| **Warnings** | **{N}** |
| Info | {N} |
| Files scanned | {N} |

**Top 3 most urgent findings:**
1. {Most critical error/warning — file + issue}
2. {Second finding}
3. {Third finding}

---

## §1 Stack progress

| Step | Artefact | Skill | Status | Path | Last modified | Age (days) |
|---|---|---|---|---|---|---|
| 1 | Personas | `business-persona` | {✅/🔄/⬜} | `docs/business/01a-personas.md` | {date} | {N} |
| 2 | Business Model Canvas | `business-model-canvas` | {✅/🔄/⬜} | `docs/business/` | {date} | {N} |
| 3 | Business Capability Map | `business-capability-map` | {✅/🔄/⬜} | `docs/business/03a-capability-map.md` | {date} | {N} |
| 4 | Value Streams | `business-value-stream` | {✅/🔄/⬜} | `docs/business/04a-value-streams.md` | {date} | {N} |
| 5 | Business Processes | `business-process` | {✅/🔄/⬜} | `docs/business/05a-processes/` ({N} files) | {date} | {N} |
| 6 | Quantitative Models | `business-quantitative-model` | {✅/🔄/⬜} | `docs/business/06a-models/` ({N} files) | {date} | {N} |
| 7 | Functional Breakdown Structure | `spec-functional-breakdown-structure` | {✅/🔄/⬜} | `docs/product-specs/07a-fbs.md` | {date} | {N} |
| 8 | Delivery Roadmap | `plan-delivery-roadmap` | {✅/🔄/⬜} | `docs/plans/delivery-roadmap.md` | {date} | {N} |
| 9 | Quality Attributes | `spec-quality-attributes` | {✅/🔄/⬜} | `docs/product-specs/09a-quality-attributes.md` | {date} | {N} |
| 10 | PRDs | `spec-prd` | {✅/🔄/⬜} | `docs/product-specs/` ({N} PRD files) | {date} | {N} |
| 11 | Implementation Plans | `plan-implementation` | {✅/🔄/⬜} | `docs/plans/active/` ({N} plans) | {date} | {N} |

**Next step:** {Step N — Artefact name — invoke `{skill}` Mode 1}

---

## §2 Folder placement

{No findings. / Table below:}

| File (actual path) | Expected path | Proposed fix |
|---|---|---|
| `{actual}` | `{canonical}` | Move to `{canonical}`; update links in `{N}` referencing files |

---

## §3 Internal links

{No findings. / Table below:}

| Source file | Line | Link text | Target | Status | Proposed fix |
|---|---|---|---|---|---|
| `{file}` | {N} | `{text}` | `{target}` | ❌ Not found | Update or remove link |

---

## §4 External links

{No findings. / Table below:}

| Source file | URL | HTTP status | Last verified | Proposed fix |
|---|---|---|---|---|
| `{file}` | `{url}` | {4xx/3xx/—} | {date / missing} | {Replace URL / Add Last verified date} |

---

## §5 ID cross-references

{No findings. / Table below:}

| Source file | ID referenced | Owning artefact | Found? | Proposed fix |
|---|---|---|---|---|
| `{file}` | `{ID}` | `{owning file}` | ❌ | Define `{ID}` in `{owning file}` or correct the reference |

---

## §6 ID integrity

{No findings. / Table below:}

| ID | Type | File(s) | Issue | Proposed fix |
|---|---|---|---|---|
| `{ID}` | `{P-NN / C-N.M / …}` | `{file}` | Duplicate / Malformed | Renumber to `{correct}` and update all references |

---

## §7 Dependency enforcement

{No findings. / Table below:}

| Artefact present | Missing prerequisite | Proposed fix |
|---|---|---|
| `{file}` | `{prerequisite path}` | Run `{skill}` to create the prerequisite |

---

## §8 _TODO_ density

| File | _TODO_ count | Est. completeness % | Priority _TODOs |
|---|---|---|---|
| `{file}` | {N} | {N}% | {field names still unfilled} |

---

## §9 Mandatory sections

{No findings. / Table below:}

| File | Missing section | Required by | Proposed fix |
|---|---|---|---|
| `{file}` | `{section name}` | `{skill}` checklist | Add section using `{skill} references/template.md §{N}` |

---

## §10 Methodology pointers

{No findings. / Table below:}

| File | Issue | Proposed fix |
|---|---|---|
| `{file}` | Missing methodology blockquote in header | Add 2-line pointer from `{skill}/references/methodology-references.md` |

---

## §11 Confidence distribution

| File | Assumed | Tested | Validated | Total | Flag |
|---|---|---|---|---|---|
| `{file}` | {N} | {N} | {N} | {N} | {⚠️ 100% Assumed >90d / —} |

---

## §12 Expiry + staleness

{No findings. / Table below:}

| File | Item | Due / Threshold date | Days overdue | Proposed fix |
|---|---|---|---|---|
| `{file}` | `{persona / competitor claim}` | {YYYY-MM-DD} | {N} | Run `{skill}` to validate or retire |

---

## §13 Orphaned files

{No findings. / Table below:}

| File | Last modified | Proposed fix |
|---|---|---|
| `{file}` | {date} | Link from `{hub doc}` if intentional; delete if obsolete |

---

## §14 Research sync

{No findings. / Table below:}

| Synthesis file | Upstream artefact | Synthesis date | Artefact last modified | Proposed fix |
|---|---|---|---|---|
| `{synthesis}` | `{artefact}` | {date} | {date} | Apply updates from synthesis §"Per-artefact updates needed" |

---

## §15 ADR chains

{No findings. / Table below:}

| ADR | Supersedes | Back-link in target? | Proposed fix |
|---|---|---|---|
| `{adr}` | `{target}` | ❌ | Add `Superseded by: [{this ADR}]({path})` to `{target}` §Status |

---

## §16 Delivery progress

**FBS status:**

| Status | Count | % of total |
|---|---|---|
| ✅ Done | {N} | {N}% |
| 🔄 In progress | {N} | {N}% |
| ⬜ Not started | {N} | {N}% |
| **Total functionalities** | **{N}** | 100% |

**Epic ↔ PRD linkage:**

| Epic | Title | PRD exists? | PRD file |
|---|---|---|---|
| `E-{NN}` | {title} | {✅ / ❌} | `{prd file / —}` |

---

## §18 Open items governance

Six sub-checks against `rules/open-items-governance.md`. Sections kept even when empty
so readers can see the check ran.

### §18a Section compliance

{No findings. / Table below:}

| File | Line | Found heading | Issue | Proposed fix |
|---|---|---|---|---|
| `{file}` | {N} | `{found heading}` | Forbidden legacy variant / Non-document-level | Rename to canonical `## Open Items` per §1 |

### §18b Schema compliance

{No findings. / Table below:}

| File | Line | Issue | Proposed fix |
|---|---|---|---|
| `{file}` | {N} | Missing / reordered columns | Restore canonical column order: `OI-ID | Type | Summary | Source anchor | Source heading | Resolution path | Priority | Status | Owner | Due / Review date | Tracker ref` |

### §18c Source-location provenance

{No findings. / Table below:}

| File | OI-ID | Anchor | Heading | Proposed fix |
|---|---|---|---|---|
| `{file}` | `{OI-NNNN}` | `{anchor or empty}` | `{heading or empty}` | Populate both fields, or use `_central-only_` in heading if no in-artefact origin |

### §18d Tracker sync coverage

{No findings. / Table below:}

| OI-ID | Local artefact | Ledger row? | Proposed fix |
|---|---|---|---|
| `{OI-NNNN}` | `{file or —}` | {✅ / ❌} | Run `util-open-items` in `sync` mode for the local artefact, or mark ledger-only row as `_central-only_` |

### §18e Closure drift

{No findings. / Table below:}

| File | OI-ID | Status | Tracker ref | Proposed fix |
|---|---|---|---|---|
| `{file}` | `{OI-NNNN}` | `closed` / `dropped` | `_TBD_` | Record evidencing PR / ADR / plan increment / runbook via `util-open-items close` (or `drop`), or reopen the row |

### §18f Stale open items

{No findings. / Table below:}

| File | OI-ID | Status | Due / Review date | Days overdue | Proposed fix |
|---|---|---|---|---|---|
| `{file}` | `{OI-NNNN}` | `{open / in-progress / blocked}` | {YYYY-MM-DD} | {N} | Run `util-open-items` in `triage` mode to re-date, escalate, reassign, or close with a `Tracker ref` |

---

## Audit metadata

| Field | Value |
|---|---|
| Generated | {YYYY-MM-DD HH:MM} |
| Skill version | util-metamodel-audit v1.0.0 |
| Scope | {full / business / product-specs / custom} |
| Mode | {full / progress / links / freshness / open-items} |
| Files scanned | {N} |
| Checks run | {N} / 18 |
| Report path | `var/reports/metamodel-audit/stack-audit-{YYYY-MM-DD}.md` |
```
