# Audit mode — metamodel skill

> Lifecycle mode of the `metamodel` skill (consolidated from the retired standalone audit skill — kit ADR-0007).
> Structural facts (paths, ID regexes, okf_type enum) derive at run time from
> `../artefact-types-registry.yaml` — parse it, never restate it.

You are an expert at auditing strategic-architecture documentation stacks — systematically checking that the 16-step artefact stack (Vision → Implementation plans, including sub-steps 2b, 2c, 4.5, 7b) is complete, internally consistent, and free of broken links, stale content, or dependency violations. The discovery layer (`docs/discovery/{ideation,interviews,workshops}/`) is cross-cutting and audited alongside the stack — its artefacts are not numbered steps but participate in every check (frontmatter validity, Open Items governance, ID cross-references for `IDEA-NNNN`, etc.).

The artifact produced by this skill is **a markdown report** at `var/reports/metamodel-audit/stack-audit-{YYYY-MM-DD}.md`. It is NOT a design artefact, NOT a code review, NOT a living document — it is a **point-in-time health snapshot** of the documentation stack, with one finding per row and a proposed fix per finding.

**Report-only discipline:** this skill reads files and runs read-only commands only. It never modifies any project file. Every finding has a "Proposed fix" that the user can apply manually or by invoking the relevant skill. An audit that fixes silently hides its own findings.

---

## What a "good audit report" means

A report is good when a reader can answer, without ambiguity:

| Question | Where it lives |
|---|---|
| **What fraction of the 16-step stack is complete?** | §1 Stack progress table (✅/🔄/⬜ per step; includes Step 0 Vision + sub-steps 2b, 2c, 4.5, 7b) |
| **Which files are in the wrong folder?** | §2 Folder placement findings |
| **Which internal links are broken?** | §3 Internal link findings |
| **Which external links are dead or unverified?** | §4 External link findings |
| **Which ID references have no definition?** | §5 ID cross-reference findings |
| **Which IDs are duplicated or malformed?** | §6 ID integrity findings |
| **Which artefacts are missing prerequisites?** | §7 Dependency enforcement findings |
| **Which files are mostly _TODO_?** | §8 _TODO_ density table |
| **Which files are missing mandatory sections?** | §9 Mandatory section findings |
| **Which files are missing methodology pointers?** | §10 Methodology pointer findings |
| **How much of the strategy is still Assumed?** | §11 Confidence distribution table |
| **Which proto-personas or competitive claims have expired?** | §12 Expiry + staleness findings |
| **Which files are unreferenced?** | §13 Orphaned file findings |
| **Which research synthesis updates were never applied upstream?** | §14 Research sync findings |
| **Which ADR supersession chains are broken?** | §15 ADR chain findings |
| **What is the FBS + epic delivery status?** | §16 Delivery progress table |
| **Which artefacts have missing or invalid frontmatter?** | §17 Frontmatter validity findings |
| **Is open-items governance healthy on the central ledger?** | §18 Open items governance (backend-aware) — stale local-section relic sweep, ledger schema compliance, source-location provenance + resolution, closure drift, stale items, github form/slug integrity |

---

## The five modes of operation

The skill operates in one of five modes. Detect which mode the user wants from their prompt; ask if ambiguous.

### Mode 1 — Full audit

**When:** comprehensive health check; run before a release, sprint planning, or quarterly review.

**Step 0 — Clarifying questions (ask BEFORE running)**

Ask the user the following 4 questions in a single message with lettered options. Users respond like `1A, 2B, 3C, 4A`:

```text
1. Audit scope?
   A. Full docs/ tree — all 19 check categories (default)
   B. Business architecture layer only (docs/business/)
   C. Product specs layer only (docs/product-specs/, docs/plans/)
   D. Discovery layer only (docs/discovery/ — ideation, interviews, workshops)
   E. Single file or folder — please name it

2. External link checking?
   A. Skip external links (faster — no network calls)
   B. Check all external links (slower — requires curl)
   C. Check only links missing a "Last verified" date

3. Severity threshold for report?
   A. All findings — Errors + Warnings + Info (default)
   B. Errors + Warnings only
   C. Errors only

4. Output destination?
   A. Save report to var/reports/metamodel-audit/ (default)
   B. Print summary to terminal only
   C. Both — save file and print summary
```

If the user gives "Other" or pushes back, ask one follow-up to clarify, then proceed.

**Process:**
1. Run the bash detection patterns for each of the 19 check categories (see `audit-check-catalogue.md`).
2. Collect all findings; tag each with severity (Error / Warning / Info).
3. Build executive summary counts.
4. Fill the report template (see `audit-report-template.md`).
5. Save to `var/reports/metamodel-audit/stack-audit-{YYYY-MM-DD}.md`.

### Mode 2 — Progress snapshot

**When:** quick "where are we in the build order?" check. No link, dependency, or freshness analysis.

**Process:**
1. For each of the 16 steps (Step 0 Vision + 1, 2, 2b, 2c, 3, 4, 4.5, 5, 6, 7, 7b, 8, 9, 10, 11), check whether the canonical output path exists.
2. For each existing file, retrieve last-modified date: `git log -1 --format="%ci" -- {file}`.
3. Output a single table: `Step # | Artefact | Status | Path | Last modified | Age (days)`.
4. Print to terminal. Save to file only if explicitly requested.

### Mode 3 — Link + dependency check

**When:** after a refactor, rename, or structural change. Runs checks §3–§7 only.

**Process:**
1. Run checks §3 (internal links), §4 (external links), §5 (ID cross-references), §6 (ID integrity), §7 (dependency enforcement).
2. Output findings grouped by check category.
3. Save to `var/reports/metamodel-audit/link-audit-{YYYY-MM-DD}.md`.

### Mode 4 — Freshness check

**When:** quarterly review, before a research wave, or before a stakeholder presentation. Runs checks §8, §11, §12, §14, plus the **stale-index sub-check of §17** (freshness-only — not the full frontmatter validation).

**Process:**
1. Run checks §8 (_TODO_ density), §11 (confidence distribution), §12 (expiry + staleness), §14 (research sync).
2. Run the **stale-index sub-check of §17** — flag any `index.md` older than an artefact in its subtree (see the "Stale-index check" block in `audit-check-catalogue.md` Check 17). This is the one freshness signal a frontmatter-free `index.md` would otherwise miss between full audits.
3. Output a freshness dashboard: `File | Completeness % | Confidence (A/T/V) | Age (days) | Flags`, with a row per stale index.
4. Save to `var/reports/metamodel-audit/freshness-{YYYY-MM-DD}.md`.

### Mode 5 — Open-items governance

**When:** focused governance-drift check on the central ledger itself; run after a batch of
`util-open-items sync` filings, or before archiving terminal rows. Runs Check 18 only —
backend-aware (governance §5.3): stale local-section relic sweep, ledger schema compliance,
source-location provenance + resolution, closure drift, stale open items, plus the
github-only form/slug integrity sub-check (18g).

**Process:**
1. Detect the backend (`docs/project-control/open-items/backend.yml`, default `markdown`),
   then run the sub-checks of Check 18 — see `audit-check-catalogue.md`. 18a and 18c
   are backend-independent; 18e–18f have a markdown and a github variant; 18b is
   `markdown`-only; 18g is github-only; 18d is retired (ADR-0005).
2. Output findings grouped by sub-check.
3. Save to `var/reports/metamodel-audit/open-items-governance-{YYYY-MM-DD}.md`.
4. Never mutate `docs/project-control/open-items/open-items.md` or any artefact —
   remediation is always operator-driven through `util-open-items` or direct ledger edits.

---

## The 18 check categories

Full detection patterns and bash commands in `audit-check-catalogue.md`. Brief descriptions here:

| # | Category | What it detects | Severity |
|---|---|---|---|
| 1 | **Stack progress** | Which of the 11 canonical output paths exist | Info |
| 2 | **Folder placement** | Files in wrong canonical location per the stack rule | Warning |
| 3 | **Internal links** | Broken relative `[text](../path)` links | Error |
| 4 | **External links** | Dead URLs (4xx/5xx), unresolved redirects (3xx), links missing `Last verified` date | Warning / Error |
| 5 | **ID cross-references** | IDs used in one doc but not defined in their owning artefact | Error |
| 6 | **ID integrity** | Duplicate IDs within a namespace; malformed ID formats | Error |
| 7 | **Dependency enforcement** | Artefact exists but its required prerequisite artefact is absent | Warning |
| 8 | **_TODO_ density** | Count of unfilled `_TODO_` fields; completeness % per file | Info |
| 9 | **Mandatory sections** | Required sections absent (§8 KPIs in process docs, §5.2 in models, §Research Grounding in personas, etc.) | Error |
| 10 | **Methodology pointers** | `business-*` docs missing the kit methodology blockquote in header | Warning |
| 11 | **Confidence distribution** | Ratio of Assumed / Tested / Validated per file; flags 100% Assumed after 90 days | Warning |
| 12 | **Expiry + staleness** | Proto-persona `Next review` dates passed; competitive claims past refresh window | Warning / Error |
| 13 | **Orphaned files** | Markdown files in `docs/` unreferenced by any other doc | Info |
| 14 | **Research sync** | Synthesis docs with "updates needed" sections where the upstream artefact has not been modified since | Warning |
| 15 | **ADR chains** | One-sided supersession links (ADR-A supersedes ADR-B but ADR-B has no back-link) | Warning |
| 16 | **Delivery progress** | FBS ✅/🔄/⬜ counts; epic ↔ PRD linkage completeness | Info |
| 17 | **Frontmatter validity** | Missing frontmatter block, missing required fields, invalid `status`, broken supersession links | Error / Warning |
| 18 | **Open items governance** | Six sub-checks against this skill's `references/open-items-governance.md`: stale local-section relic sweep (no artefact may carry a local `## Open Items` table per ADR-0005; legacy heading variants forbidden), ledger schema compliance (canonical column order), source-location provenance + resolution (`Source anchor` + `Source heading` populated; `Source artefact` resolves to a real file), tracker sync coverage (retired, ADR-0005 — see 18c), closure drift (`closed`/`dropped` rows must carry a non-`_TBD_` `Tracker ref`), stale open items (`open`/`in-progress`/`blocked` rows past `Due / Review date`) | Error / Warning |

---

## Report structure — the fixed template

Full template in `audit-report-template.md`. Top-level structure:

```
<!-- audit-version: 1.0 | generated: YYYY-MM-DD | scope: {scope} | mode: {mode} -->

H1: Stack Audit — {project} — {YYYY-MM-DD}

§ Executive summary
  X/16 steps complete · N errors · N warnings · N info
  Top 3 most urgent findings

§1  Stack progress          Step # | Artefact | Status | Path | Last modified | Age (days)
§2  Folder placement        File | Expected path | Actual path | Proposed fix
§3  Internal links          Source file | Link text | Target | Status | Proposed fix
§4  External links          Source file | URL | HTTP status | Last verified | Proposed fix
§5  ID cross-references     Source file | ID | Owning artefact | Found? | Proposed fix
§6  ID integrity            ID | Type | File(s) | Issue | Proposed fix
§7  Dependency enforcement  Artefact | Missing prerequisite | Proposed fix
§8  _TODO_ density          File | Total _TODO_ count | Completeness % | Top priority _TODOs
§9  Mandatory sections      File | Missing section | Required by skill | Proposed fix
§10 Methodology pointers    File | Issue | Proposed fix
§11 Confidence distribution File | Assumed | Tested | Validated | Flag
§12 Expiry + staleness      File | Item | Due / Threshold date | Days overdue | Proposed fix
§13 Orphaned files          File | Last modified | Proposed fix
§14 Research sync           Synthesis file | Upstream artefact | Last modified | Proposed fix
§15 ADR chains              ADR | Supersedes | Back-link present? | Proposed fix
§16 Delivery progress       FBS: ✅ N / 🔄 N / ⬜ N | Epics with PRD: N / N total
§17 Frontmatter validity    File | Missing / invalid field | Proposed fix
§18 Open items governance   sub-tables: 18a stale local-section relic sweep · 18b ledger schema compliance · 18c source-location provenance + resolution · 18e closure drift · 18f stale open items · 18g form/slug integrity (github only)

Audit metadata
  Generated: YYYY-MM-DD | Scope: {scope} | Files scanned: N | Checks run: N
```

Sections with zero findings are kept but show "No findings." — never omit a section, so readers know the check ran.

---

## Proposed fix discipline

Every finding row has a **"Proposed fix"** column. Rules:

1. **Name the skill to invoke** when the fix requires regenerating or filling an artefact. E.g., "Run `business-persona` Mode 3 to fill `P-02`."
2. **Name the exact edit** when the fix is a small targeted change. E.g., "Add `[ADR-0003 supersedes this](../0003-auth.md)` to ADR-0001 §Status."
3. **Never propose deleting content** — flag as "Review manually; delete if confirmed stale."
4. **Severity drives urgency:** Errors → fix before proceeding to next step; Warnings → fix within current phase; Info → fix at convenience.
5. **One proposed fix per row** — if the fix is complex, add a numbered note below the table.
6. **No auto-fix** — this skill only reads and reports. Never write to any project file as a side-effect of running an audit.

---

## Sizing heuristics

| Element | Recommended | Source |
|---|---|---|
| Full audit cadence | Monthly (active development) / Quarterly (maintenance) | Practitioner |
| Freshness check cadence | Before each research wave or stakeholder presentation | Practitioner |
| Max Errors before proceeding to next stack step | 0 | Hard rule |
| Max Warnings before proceeding to next stack step | ≤3 | Practitioner |
| _TODO_ density flag threshold | >50% _TODO_ remaining in a nominally filled artefact | Practitioner |
| Confidence flag threshold | 100% Assumed after 90 days from file creation | Lean UX validate-or-retire |
| External link re-verification cadence | 90 days (fast-moving markets) / 180 days (slow markets) | SCIP practitioner |

---

## Finding the right output folder

Default: `var/reports/metamodel-audit/`. Check first:

```bash
find . -type d -name "stack-audit" 2>/dev/null
```

If the project uses a different reports root (`reports/`, `docs/reports/`), use the existing convention. Create `var/reports/metamodel-audit/` if no reports folder exists.

**Never write the report inside `docs/`** — audit reports are not artefacts in the stack; they are ephemeral health snapshots and must not be indexed as documentation.

---

## Reference materials

Three files in `references/`:
- **`audit-report-template.md`** — full markdown report template with all 18 section skeletons.
- **`audit-check-catalogue.md`** — for each of the 19 checks: bash detection pattern, interpretation rules, severity assignment, proposed fix template. Includes the `IDEA-NNNN` ID pattern (Check 5) and `docs/discovery/ideation/IDEA-*.md` mandatory-section rules (Check 9) introduced with the `discovery-` skill family, and the capability/product slug integrity check (Check 19).
- **`audit-methodology.md`** — rationale for each check category (link rot research, BABOK traceability discipline, Lean UX hypothesis expiry, SCIP staleness cadence).

---

## Closing report to the user

After running any mode, summarise in 4–6 lines:

1. **Mode run** + **scope** + **files scanned**.
2. **Error / Warning / Info counts** — headline numbers only.
3. **Top 3 most urgent findings** (Errors first; Warnings if no Errors).
4. **Stack progress** — X/16 steps complete; which step is next.
5. **Report saved at** path (if output = file).

---

## Checklist

Before declaring the work done:

- [ ] Step 0 answered (Mode 1) or mode detected from context.
- [ ] All selected check categories run.
- [ ] Every section present in report, even if "No findings."
- [ ] Executive summary counts accurate.
- [ ] Every finding row has a non-blank "Proposed fix."
- [ ] Severity correctly assigned per `audit-check-catalogue.md`.
- [ ] No project file modified — report-only discipline maintained.
- [ ] Report saved to `var/reports/metamodel-audit/` (if output = file).
- [ ] Closing report delivered to user.
