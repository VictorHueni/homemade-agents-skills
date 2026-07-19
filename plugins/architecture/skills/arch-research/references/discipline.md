# Architecture Research — Internal Discipline Guide

> This file is internal guidance for Claude when running the `arch-research` skill. It is never copied into project output. It encodes the confidence rubric, source-quality patterns, citation discipline, refresh cadence, question-framing test, and ADR-linkage rules that must be applied silently to every research note produced.

---

## Confidence rating rubric (5-star scale)

Every source cited in a research note must carry a star rating anchored to the *authority of the publication*, not the *agreement of the content with our hypothesis*. Confidence inflation is the #1 anti-pattern.

| Rating | Source type | Examples |
|---|---|---|
| **★★★★★** | Primary statute · official regulator publication · ISO official standard text | nFADP official text on [fedlex.admin.ch](https://www.fedlex.admin.ch/) · FDPIC published guidance · EDPB opinions · ISO 27001:2022 official standard · FOPH/BAG directives |
| **★★★★** | Major law-firm or audit-firm published guidance · standard's official commentary or implementation guide | Walder Wyss / Lenz & Staehelin / Homburger published memos · KPMG / PwC / Deloitte published whitepapers · ISO 27001 official Annex A control set documentation |
| **★★★** | Industry-association guidance · peer-reviewed compliance journal · government statistical bureau data | eHealth Suisse · FMH (Foederatio Medicorum Helveticorum) · H+ Swiss Hospital Association · BFS Hospital Statistics · IAPP peer-reviewed papers |
| **★★** | Consultancy blog post · vendor whitepaper · Stack Overflow consensus answer · technical-community blog | Auth0 blog · Supabase blog · OWASP cheat sheets · individual law-firm blog posts (vs published memos) |
| **★** | Anecdote · single-source weak signal · uncorroborated forum claim | Reddit thread · one customer's RFP excerpt · single Stack Overflow answer · LinkedIn post |

### Anti-inflation rules

- **Never rate a consultancy blog above ★★.** Even big-name firms' blogs are marketing surfaces, not authoritative guidance.
- **Never rate a vendor's claim about a competitor above ★★.** Conflict of interest.
- **A primary statute text is ★★★★★ even if it's hard to interpret.** The interpretation can be in a separate ★★★★ law-firm source; the statute itself stays ★★★★★.
- **★★★★★ requires a real URL.** PDFs behind a paywall are ★★★★ at best (the content is authoritative, but unverifiable by readers).

---

## Source quality tiers — which to prefer

When a finding is supported by multiple sources at different confidence tiers, prefer the higher-confidence source as the primary citation and use lower-tier sources for triangulation only.

**Hierarchy (highest authority first):**

1. **Primary statute** — the law itself (fedlex.admin.ch for CH, eur-lex.europa.eu for EU)
2. **Regulator interpretation** — published guidance from the body that enforces the statute (FDPIC, FOPH, EDPB)
3. **Audit body documentation** — for certifications: the ISO official standard, the auditor's published Annex A interpretation
4. **Court/tribunal decisions** — interpretations made binding through case law (rare in CH; common in EU)
5. **Law-firm or audit-firm published memos** — synthesised interpretations from accountable professionals (named author, dated, citable)
6. **Industry-association guidance** — sectoral norms (eHealth Suisse, FMH, IAPP)
7. **Peer-reviewed academic papers** — empirical research (often slow to land)
8. **Consultancy / vendor whitepapers** — interpretations with commercial interest; useful for triangulation only
9. **Community-aggregated knowledge** — Stack Overflow, OWASP cheat sheets; useful for "what's the established practice" but not for compliance claims

### When triangulation is required

A claim is **adequately sourced** at ★★★★+ when a single primary statute or regulator publication supports it.

A claim is **adequately sourced** at ★★★ when ≥2 independent industry-association sources support it without contradiction.

A claim at ★★ or below is **never adequately sourced alone** — it must be cross-checked with a higher-tier source before serving as the basis for an ADR Implication.

---

## Citation discipline (every claim verifiable)

### Rule 1 — Every source row has a real URL

If you can't link it, you can't cite it. Books, paywalled PDFs, and private documents are acceptable secondary sources but the row should note "primary URL not publicly available; verify via [accessible secondary source]".

### Rule 2 — Every source row has a `Last verified` date

The date when you opened the URL and confirmed the quoted text still appears there. **Stale dates erode the entire file's credibility** — a 2024 `Last verified` on a 2026 regulatory page is a red flag.

### Rule 3 — Every source row has an exact short quote OR specific section reference

"Per [Source X]" without a quoted claim forces readers to re-read the entire source to audit your interpretation. Acceptable quote forms:
- **Short verbatim quote:** "*Cross-border data transfers require an adequacy decision under Art. 16 nFADP.*"
- **Specific section reference:** "[Source X §4.3.2 Table 12]"
- **Specific figure/table reference:** "[Source Y Annex A.5 — Information Security Policies]"

Never just say "per [Source X]" without a locator.

### Rule 4 — Verify the citation matches the claim

Before adding a citation, ask: "If a reader opens this URL and reads the quoted text, will they agree my Finding is supported?" If the quote doesn't directly support the claim, the source isn't the right citation — find a better one or qualify the Finding.

### Rule 5 — Distinguish what the source SAYS from what it IMPLIES

A regulatory statute saying "appropriate technical measures" does NOT say "row-level security is sufficient" — the latter is interpretation. Findings can include interpretation, but interpretation must be explicitly flagged ("This research interprets 'appropriate measures' as encompassing RLS, based on the absence of any FDPIC guidance specifically excluding it...").

---

## Refresh cadence (per topic type)

| Topic type | Recommended refresh interval | Why |
|---|---|---|
| **Active legislation** (nFADP, GDPR amendments, new sectoral laws) | Every 3 months | Statutes change rarely but supporting regulator guidance evolves quickly; new EDPB opinions reshape interpretation |
| **Foundational standards** (ISO 27001:2022, ISO 27799) | Annually | Standards have multi-year revision cycles; major version bumps are rare and well-signalled |
| **Vendor capabilities** (Zitadel features, Keycloak releases, Auth0 plan changes) | Every 3 months | Vendor product surface changes weekly; pricing changes quarterly |
| **Certification programs** (HDS scope changes, EPD compliance criteria) | Every 6 months | Certification body publications are slower-moving |
| **Industry surveys** (clinic-group RFP norms, Swiss healthcare cloud adoption) | Annually | Survey data ages slowly but contractual norms evolve |
| **Case law / regulatory enforcement actions** | Every 6 months | New enforcement decisions reshape risk interpretation |
| **Frozen research** (post-ADR-decision) | Don't refresh — Supersede with a new file if landscape changes | Frozen research is historical context; modifying it falsifies the ADR's rationale |

If a research note is older than its topic-type refresh interval, treat it as **Active but unverified** and run Mode 3 Refresh before citing it in a new ADR.

---

## Question-framing test

Every question in a research note must pass three checks before being acceptable.

### Check 1 — Single + specific

The question is about ONE thing, and that thing is precise.

| Wrong | Right |
|---|---|
| "What are the data protection requirements?" | "Does nFADP Art. 8 mandate physical multi-tenancy or is logical isolation (RLS) sufficient?" |
| "Should we get certified?" | "Is ISO 27001 certification a requirement in typical Swiss clinic-group procurement RFPs?" |
| "What about GDPR?" | "Do EU clinic tenants trigger GDPR obligations beyond what nFADP already requires?" |

### Check 2 — Falsifiable

The question has a possible answer that would change the outcome. "What are best practices?" is not falsifiable; "Does best practice in Swiss healthcare SaaS use schema-per-tenant or RLS?" is.

### Check 3 — ADR-linkable

The answer would shift the preference order of options in at least one ADR. If you can't identify which ADR the answer would inform, the question is unmoored from decision-making.

---

## ADR-linkage discipline

### Rule 1 — Every Finding must have an Implication for ADRs section

If you cannot identify which ADR the Finding informs, either:
- the Finding is too vague (sharpen it), OR
- the question shouldn't be in this research note (it's exploratory; move to a personal note)

### Rule 2 — The Implication names the specific ADR + option

Wrong: "This affects ADR-0003."
Right: "Eliminates ADR-0003 Option D (database-per-tenant) as over-engineering; favours Options A (RLS) or E (Hybrid RLS + app-layer)."

### Rule 3 — When ADRs cite this research, they cite the Findings summary table

The summary table at the bottom of the research note is the canonical citation target. ADRs say:

```markdown
**Chosen option:** Option E
**Rationale:** Per [Research-0001 §findings Q1](../research/0001-swiss-healthcare-data-protection-baseline.md#findings-summary-citable-from-adrs),
RLS + application layer enforcement is the strongest auditable posture
under nFADP Art. 8.
```

Not:

```markdown
**Rationale:** See research-0001.
```

### Rule 4 — Frozen research cannot grow new Implications

Once a research note is Frozen (Mode 4), its Implications section reflects what the feeding ADRs cited. If a new ADR wants to use the same evidence, run Mode 3 Refresh first (verifying sources still hold) — don't append to the existing Implications retroactively.

---

## Common pitfalls

1. **Researching the wrong question.** Spent days on "what does nFADP say about data residency?" when the actual ADR turned on "what do clinic-group RFPs typically require?" — different question, different sources, different finding. Mitigation: run Step 0 clarifying questions to confirm the ADR linkage BEFORE filling.

2. **Filling Findings before Sources.** Writing the answer and then back-filling citations to support it. Source-first discipline: build the Sources consulted table first, then write the Finding strictly from what the sources collectively say.

3. **Confidence drift.** Marking everything ★★★★ because "that's the typical confidence range." Stars should be distributed across the rubric in any honest research; if every source is ★★★★, either you've only cited audit-firm guidance (re-balance toward primary statutes), or you've inflated everything (apply the rubric).

4. **Citing without re-reading.** Pasting a URL from memory or from a previous research note without re-fetching. URLs change; quotes get rewritten; pages get retired. Always verify on Last verified date.

5. **Letting Active research drift forever.** Active status without progress for >3 months means either the topic isn't important enough to warrant a research note (delete or merge), or the research is blocked on something specific (capture the blocker as a `decision-gap` row in §Open Items with `Source heading` naming the affected question, then re-scope).

6. **Frozen research that pretends to be Active.** After feeding ADRs decide, the research is historical. Editing it (other than Refresh → Supersede flow) falsifies the historical record. Resist the urge.

---

## Output-quality checklist (internal use)

Before declaring a Mode 2 Fill complete, verify silently:

- [ ] All N questions in §Questions index have matching H2 sections
- [ ] Each H2 has its 4 sub-sections (Context · Sources consulted · Finding · Implication for ADRs). Per-Q gaps are consolidated into the document-level §Open Items section per the `metamodel` skill's `references/open-items-governance.md` — no `###` open-gap subsection under any Q.
- [ ] Document-level §Open Items table present with the canonical schema (OI-ID · Type · Summary · Source anchor · Source heading · Resolution path · Priority · Status · Owner · Due / Review date · Tracker ref). Per-Q rows preserve provenance via `Source anchor = #qN` + `Source heading = "Qn — restated question"`.
- [ ] Every Sources table has the full column set (Source · URL · Type · Last verified · Confidence · Quote)
- [ ] No source row missing `Last verified` date
- [ ] No source row missing Quote
- [ ] No consultancy / vendor source above ★★
- [ ] Confidence distribution is realistic (not all ★★★★)
- [ ] Every Finding section has a non-empty Implication for ADRs
- [ ] §Findings summary table has one row per Q with one-sentence Finding + Confidence + Feeds
- [ ] §Consolidated sources is deduplicated by URL + grouped by type
- [ ] Changelog has an entry for the current mode + date + author
- [ ] Status field is appropriate to fill completeness (Draft if Q's still _TODO_; Active if all populated)

If any check fails, address before delivering.
