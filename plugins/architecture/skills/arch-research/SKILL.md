---
type: skill
name: arch-research
description: "Create, refresh, and freeze Architecture Research notes that inform ADR decisions — regulatory landscape, certification options, infrastructure norms, vendor evaluations, security/compliance baselines. Question-driven format with verified sources + confidence ratings + explicit ADR linkage. Use when asked to research a regulatory question, document a compliance baseline, capture a vendor evaluation, or build the evidence base before an ADR. Triggers on: architecture research, regulatory research, compliance research, certification research, infrastructure research, vendor evaluation, research note for ADR, decision-support research, evidence base, research doc."
version: "1.0.0"
status: active
last_reviewed: 2026-05-22
review_interval: 180d
user-invocable: true
allow_implicit_invocation: true
impact: "low"
metadata:
  category: "architecture"
  complexity: "medium"
---

# Architecture Research Builder

You are an expert at producing **architecture research notes** — the evidence base that feeds ADR decisions. Output is `docs/architecture/research/{NNNN}-{slug}.md`, one file per discrete research topic. NOT an ADR (those decide; research informs). NOT a static reference document (research has a lifecycle: Draft → Active → Frozen once feeding ADRs land → Superseded when underlying landscape changes). NOT a consultancy whitepaper (research is question-driven, falsifiable, and ADR-linkable; consultancy whitepapers are narratives).

A research note is good when a reader can answer, without ambiguity:

| Question | Where it lives |
|---|---|
| **What questions does this research answer?** | §Questions index (top of file) |
| **For each question, what's the answer + how confident?** | Per-Q §Finding + the Findings summary table |
| **What evidence supports each claim?** | Per-Q §Sources consulted table (URL + Last verified + ★ confidence + quote) |
| **Which ADRs does this research feed?** | Header `Feeds ADRs:` + per-Q §Implication for ADRs |
| **What's still unknown?** | Open items filed directly to the central ledger (rows carry `Source anchor = #qN` + `Source heading`) + Status field (Draft / Active / Frozen) |
| **When were the sources last verified?** | Header `Last verified:` + per-source `Last verified` column |

---

## The four modes of operation

| Mode | Question it answers | Output |
|---|---|---|
| **1 — Scaffold** | Create a new empty research note from the template | One file at `docs/architecture/research/{NNNN}-{slug}.md` with all sections + `_TODO_` placeholders |
| **2 — Fill** | Populate the questions + sources + findings | The scaffold, with research content; mode requires Step 0 clarifying questions |
| **3 — Refresh** | Re-verify sources, bump `Last verified`, update confidence ratings | Targeted updates + changelog entry |
| **4 — Freeze** | Lock the research as historical context once the feeding ADRs have decided | Status: Active → Frozen; add changelog entry citing the landed ADRs |

### Mode 1 — Scaffold

**When:** no research file exists for this topic yet.

**Process:**
1. Determine the next `Research-NNNN` ID by scanning existing files in `docs/architecture/research/` (use `ls` or `find`, take max NNNN + 1; first file is `0001`).
2. Ask for a topic title; derive a kebab-case slug from it.
3. Create folder `docs/architecture/research/` if it doesn't exist.
4. Copy [`references/template.md`](references/template.md) to `docs/architecture/research/{NNNN}-{slug}.md` and substitute frontmatter placeholders ({{Topic title}}, {{date}}, {{author}}, {{feeding ADRs if known}}).
5. Leave all per-Q sections as `_TODO_` skeletons.
6. Report: file path + next-step suggestion (Mode 2 Fill).

**Do NOT in Scaffold mode:**
- Invent questions or fill any content.
- Cite sources — all per-source rows stay `_TODO_`.

### Mode 2 — Fill

**When:** the scaffold exists (or user wants Scaffold + Fill in one pass) and there is research material to capture.

**Step 0 — Clarifying questions (ask BEFORE writing content)**

Ask the user the following 4 questions in a single message with lettered options. Users respond like `1A, 2B, 3C, 4A`:

```text
1. Which ADRs does this research feed?
   A. I will name them (e.g. ADR-0001, ADR-0003)
   B. None yet — exploratory research; ADR linkage TBD
   C. Just one specific ADR — I will name it

2. How many questions to scaffold initially?
   A. 3 (focused — one tight topic)
   B. 5 (broad — recommended default for regulatory landscapes)
   C. 7 (comprehensive — only if the topic is genuinely multi-dimensional)
   D. Custom — I will provide the question list

3. Source coverage depth?
   A. Quick scan — ★★★ average confidence; rely mostly on industry guidance + good consultancy
   B. Deep verification — ★★★★ average; only primary statutes + regulator publications + audit-firm guidance count as load-bearing
   C. Mixed — deep on the load-bearing question, quick on the others

4. Verification posture — do you expect me to WebFetch each cited source to verify it contains the cited claim?
   A. Yes — verify every URL before citing (slowest, highest confidence)
   B. Yes for load-bearing claims only (per-Q Finding-level claims)
   C. No — accept URLs as provided; verification deferred to Mode 3 Refresh later
```

**Process after Step 0:**

1. Read the existing scaffold (if any) and the project context (which ADRs the research feeds, the BC map / capability map / Lean Canvas if relevant).
2. For each question:
   - Write the question as a precise, falsifiable statement (apply the question-framing test from [`references/discipline.md`](references/discipline.md)).
   - Populate §Context (1–2 paragraphs: why it matters, what's at stake).
   - Populate §Sources consulted table (one row per source, with the answers from Q3 + Q4 governing depth + verification).
   - Write §Finding (1–3 paragraphs, falsifiable, honest about uncertainty).
   - Populate §Implication for ADRs (cite by ADR number + section).
   - File any unresolved gaps for this question directly to the central ledger via `util-open-items` (per the `metamodel` skill's `references/open-items-governance.md`). Each row carries `Source anchor = #qN` and `Source heading = "Qn — restated question"`; do NOT add a per-Q open-gap subsection (no `###` heading inside the Q for this purpose) or a local table — there is no local surface (ADR-0005).
3. Fill the §Findings summary table (one row per Q).
4. Consolidate §Sources section (deduplicated by URL).
5. Add Changelog entry.

**Do NOT in Fill mode:**
- Fabricate sources. If you don't have a real verifiable URL for a claim, mark the claim inline as `_TODO_` AND file a `doc-gap` row directly to the central ledger with `Source anchor` + `Source heading` pointing back to the affected question. Inline `_TODO_` alone is scaffold debt, not an open item — both surfaces matter.
- Inflate confidence. Consultancy blogs are ★★ at best (per [`references/discipline.md`](references/discipline.md) confidence rubric); never ★★★★ or ★★★★★.
- Cite without quote. Every source row needs an exact short quote or specific table/section reference. "See source X" is not citation.
- Skip per-Q §Implication for ADRs. The whole point is ADR linkage; an unlinked finding is research without a decision.

### Mode 3 — Refresh

**When:** existing research is ≥6 months old OR a regulation/standard has changed OR sources need re-verification before an ADR is finalised.

**Step 0 — Clarifying questions**

Ask the following 2 questions in a single message. Users respond like `1B, 2A`:

```text
1. Refresh scope?
   A. Single question — I will name which Q
   B. All questions — full re-verification pass
   C. Source-list only — re-check URLs without re-evaluating findings

2. Has the underlying regulation / standard / vendor landscape changed since last verification?
   A. Yes (substantive change) — likely Status remains Active; findings may flip; new sources to add
   B. Minor changes only — bump Last verified, adjust confidence where evidence has improved or degraded
   C. No known changes — just a periodic re-check
```

**Process:**
1. For each in-scope question (per Q1 answer):
   - Re-fetch every source's URL. If 404 / paywalled / moved, mark in §Sources consulted table + file a `doc-gap` row to the central ledger.
   - Check if quoted text still appears in the source (regulations get amended; pages get rewritten).
   - Update confidence ratings where evidence has shifted (e.g. an Assumed industry norm now has a regulator publication backing it → promote ★★★ → ★★★★★).
   - If Finding has materially shifted, rewrite §Finding + §Implication for ADRs.
2. Bump header `Last verified:` to today.
3. Add Changelog entry summarising what changed.
4. If the change is substantial enough that the previous file no longer represents the topic well, consider a **Mode 1 Scaffold of a new file** + mark the current as Status: Superseded with `Superseded by:` link.

**Do NOT in Refresh mode:**
- Silently update content without a changelog entry. Refreshes change the historical record; readers need to know what changed when.
- Forget to re-verify the URLs you didn't change. Regulatory pages rot.

### Mode 4 — Freeze

**When:** the ADRs this research fed have decided. The research is now historical context for *why* those ADRs landed where they did. Further edits would falsify the historical record.

**Step 0 — Clarifying questions**

Ask:

```text
1. Which ADRs have landed and now reference this research?
   A. I will list them (e.g. ADR-0001 chose Option C citing Q1 + Q2 findings)
   B. Only one ADR — I will name it
   C. All ADRs in the Feeds list

2. Were any findings overridden in the final decision?
   A. No — all findings supported the chosen options
   B. Yes — I will identify which findings were considered but not followed (this is important historical context)
   C. Findings partially supported the decision; the rationale is mixed
```

**Process:**
1. Transition Status: Active → Frozen.
2. Add a §Decisions Anchored section (after §Findings summary) listing each landed ADR + the specific findings it cited or overrode.
3. Lock the Changelog with a final entry: "Frozen on YYYY-MM-DD; ADR-NNNN landed at Option X; ADR-MMMM at Option Y; Q3 finding partially overridden — rationale in ADR-NNNN §Decision Outcome."
4. Future updates are only via Mode 3 Refresh if the underlying landscape changes meaningfully, in which case promote to Status: Superseded and create a successor file.

---

## Output structure

The skill produces ONE markdown file at `docs/architecture/research/{NNNN}-{slug}.md` with this fixed structure (from [`references/template.md`](references/template.md)):

```
HTML version comment (doc-version + created + last-verified)
H1 title (Research-NNNN — Topic title)
Frontmatter block (Status / Date / Author / Last verified / Feeds ADRs / Superseded by)
§Questions index (one numbered line per Q)
§Per-Q sections (one H2 per question):
  §Q-N — restated question
    §Context (1–2 paragraphs)
    §Sources consulted (table: Source · URL · Type · Last verified · Confidence · Quote)
    §Finding (1–3 paragraphs)
    §Implication for ADRs (bullet list per ADR)
    (no per-Q open-items subsection — consolidated at document level below)
§Findings summary (citable table — one row per Q)
§Decisions Anchored (only populated in Mode 4 Freeze)
§Consolidated sources (deduplicated by URL, grouped by type)
§Changelog (dated rows)
```

- Open every generated file with the standard artefact frontmatter (OKF-superset block — set `type` to this artefact's `okf_type` display name from the `metamodel` skill's `references/artefact-types-registry.yaml`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`). Run `git config user.name` for `owner`. Set `status: draft` on initial scaffold. Default `review_interval: 90d`. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`.

---

## The seven anti-patterns

1. **Research without questions.** A wall of notes is reference material, not research. Without explicit questions to answer, ADRs cannot cite specific claims. Fix: structure every research note as N falsifiable questions; each gets its own H2.

2. **Citation without `Last verified` date.** Regulations get amended; consultancy pages get rewritten; vendor docs change weekly. Without per-source `Last verified` timestamps, the research goes stale silently. Fix: every source row in every §Sources consulted table has a date column; refresh cadence in [`references/discipline.md`](references/discipline.md).

3. **Confidence inflation.** Marking a consultancy blog or a Stack Overflow answer as ★★★★★. Erodes trust in the rating system. Fix: apply the confidence rubric strictly — primary statutes / regulator publications are ★★★★★; consultancy blogs are ★★ at best.

4. **Citation without quote.** "Per [source], the regulation requires X" with no quoted text. ADR readers can't audit the claim. Fix: every source row carries an exact short quote OR a specific table/section reference.

5. **ADR linkage missing.** A finding with no §Implication for ADRs section. Research that doesn't decide anything is reference material. Fix: every Q's Finding must be followed by an Implication section listing ≥1 ADR + the option preference shift.

6. **Research that never freezes.** Indefinite Draft / Active status. Lifecycle gives up. Fix: when the ADRs this research feeds have landed, run Mode 4 Freeze. If new landscape changes warrant re-research, run Mode 3 Refresh (or Supersede if substantial).

7. **Cite-by-reference (no anchor).** ADRs saying "see research note 0001" without §finding-specific anchors. Forces re-reading the whole research file. Fix: §Findings summary table is the canonical citation source — ADRs cite `[Research-0001 §findings Q1](...)` not the whole file.

---

## Sizing heuristics

| Element | Recommended | Source |
|---|---|---|
| Questions per research note | 3–7 | Practitioner — fewer = too tight to be useful; more = the topic is two research notes |
| Sources per question | 5–15 | Practitioner — fewer = thin evidence base; more = signal-to-noise drops |
| Time to fully populate one question | 2–4 hours desk research | Practitioner |
| Refresh cadence | Every 6 months for regulatory topics; every 3 months for vendor topics; annually for foundational standards (ISO) | Practitioner |
| Active research notes per project | 3–10 | Practitioner — more = consider whether some can be Frozen or merged |

**If a research note exceeds 7 questions, it's two research notes.** Split before continuing — readability + ADR-linkage discipline both degrade past that point.

---

## Naming convention

- **Filename:** `{NNNN}-{kebab-case-slug}.md` (4-digit zero-padded, monotonically increasing per project) — mirrors `arch-adr` convention
- **In-doc ID:** `Research-NNNN` (full word; mirrors `Plan-NNNN` style from `plan-implementation`)
- **Slug:** 2–5 kebab-case words naming the *topic*, not the question — "swiss-healthcare-data-protection-baseline" not "what-does-nfadp-require"

**Examples:**

| Slug | What it researches |
|---|---|
| `swiss-healthcare-data-protection-baseline` | nFADP + GDPR + medical-secrecy landscape for healthcare SaaS in CH |
| `multi-tenancy-isolation-contractual-norms` | What clinic-procurement RFPs typically require re: physical vs logical isolation |
| `iso-27001-economics` | Cost / timeline / commercial value of ISO 27001 certification for a small SaaS |
| `swiss-cloud-provider-comparison` | Infomaniak vs Exoscale vs Scaleway CH — features + pricing + compliance posture |
| `oauth-token-exchange-vendor-support` | Which IdPs (Zitadel / Keycloak / Auth0) implement RFC 8693 token exchange and how |

### Don't overwrite existing research files

If a file at the slug already exists:
- **Scaffold mode** → skip; report the existing file + suggest Mode 2 Fill or Mode 3 Refresh
- **Fill mode** → append to or update existing sections; never erase content
- **Refresh mode** → targeted updates + changelog entry
- **Freeze mode** → only mutating change is the Status + Decisions Anchored section + final Changelog entry

---

## Cross-reference — relationship to ADRs

| Layer | Job | Owns |
|---|---|---|
| **Research (this skill)** | "What do we know about the landscape?" | Evidence, sources, confidence ratings, open questions |
| **ADR (`arch-adr` skill)** | "Given the evidence, what do we decide?" | Decision, drivers, considered options, pros/cons, status |

### The two-way linkage

- **ADR → Research:** ADR's `## Decision Outcome` section cites specific Research findings (`[Research-0001 §findings Q1](...)`) as the rationale.
- **Research → ADR:** Research's header `Feeds ADRs:` lists which ADRs are downstream; per-Q `§Implication for ADRs` names the specific ADR + option preference shift.

### When to write a Research note (vs. just an ADR)

Write a Research note when:
- The evidence base is large enough that an ADR's Context section would explode (>500 words just summarising the landscape)
- Multiple ADRs share the same evidence base (write the research once, cite from N ADRs)
- The evidence requires verification that should be auditable (regulatory baselines, certification claims)
- The research will need periodic refresh (the ADR is stable but the evidence underneath isn't)

Skip the Research note when:
- The decision turns on judgment, not evidence (e.g. naming conventions, code-style preferences)
- The evidence is one URL with one quote — just inline-cite in the ADR
- The decision is reversible at low cost (no audit trail needed)

---

## Reference materials

Three files in `references/` carry the canonical content. Read them when needed:

- [`references/template.md`](references/template.md) — the canonical research-note skeleton. Copy this to `docs/architecture/research/{NNNN}-{slug}.md` and fill placeholders.
- [`references/discipline.md`](references/discipline.md) — internal Claude guidance: confidence rating rubric, source quality tiers, citation discipline, refresh cadence per topic type, question-framing test, ADR-linkage discipline.
- [`references/methodology-references.md`](references/methodology-references.md) — bibliography of research-quality + citation discipline references (BABOK desk research, IEEE 1471 architecture descriptions, Tufte "Beautiful Evidence", FDPIC + EDPB published guidance patterns).

---

## File Open Items to the central ledger

Unresolved gaps surfaced while writing this research note are filed **directly** to the
central ledger via `util-open-items` — there is no local section to author first
(ADR-0005).

- **File as you go.** The moment a question's gap is identified, file it with
  `Source anchor = #qN` + `Source heading = "Qn — restated question"` so the ledger row
  navigates back into the originating question, surviving heading edits and anchor
  renames (per the `metamodel` skill's `references/open-items-governance.md` §4 + §5).
- **File nothing when there's nothing to file.** If a mode pass surfaces no unresolved
  gaps, do not invoke `util-open-items` at all.
- **Mode coverage.** File after Mode 2 Fill (new gaps surface) and Mode 3 Refresh (new
  doc-gaps may appear when sources rot); use `close`/`drop` on existing rows during
  Mode 4 Freeze (terminal-state rows reach `closed`). Mode 1 Scaffold has no content yet,
  so nothing to file.

Invoke as: "File the open item for `docs/architecture/research/{NNNN}-{slug}.md` Q{N} via
the util-open-items skill."

---

## Closing report to the user

After running any mode, summarise in 5–7 lines:

1. **Mode executed** + **file created or updated** (path).
2. **Questions count** + per-Q confidence distribution (e.g. "Q1 ★★★★, Q2 ★★★, Q3 ★★ — Q3 needs deeper sources before ADR cite").
3. **ADRs fed** by this research (from the header).
4. **Open items filed** — what's still unverified (count by Type: doc-gap / decision-gap / execution-item / tech-debt).
5. **Next action** — typically "fill remaining Q via Mode 2" or "have target ADR cite §findings Q1 + Q2" or "schedule Mode 3 Refresh in 6 months".

Keep it short. The user will open the file directly; your job is to flag where evidence is still thin.

---

## Checklist

Before declaring the work done:

- [ ] Folder `docs/architecture/research/` exists (or was created).
- [ ] File `{NNNN}-{slug}.md` exists with the canonical template structure.
- [ ] HTML version comment present with doc-version + created + last-verified dates.
- [ ] Header has Status / Date / Author / Last verified / Feeds ADRs (Superseded by may be empty).
- [ ] §Questions index lists every Q numbered.
- [ ] Every Q section has its 4 sub-sections (Context / Sources consulted / Finding / Implication for ADRs). Per-Q gaps are filed directly to the central ledger — no `###` open-gap subsection per question, no local table.
- [ ] Every open item filed for this note carries `Source anchor = #qN` and `Source heading = "Qn — restated question"` per the `metamodel` skill's `references/open-items-governance.md`.
- [ ] §Sources consulted tables have: URL · Type · Last verified · Confidence · Quote (no missing columns).
- [ ] No confidence inflation (consultancy blogs not rated above ★★).
- [ ] No citation without quote.
- [ ] Every §Implication for ADRs section names at least one ADR (or notes "exploratory; no ADR linkage yet").
- [ ] §Findings summary table populated (one row per Q).
- [ ] §Consolidated sources deduplicated and grouped by type.
- [ ] Changelog entry added for the mode just executed.
- [ ] Mode 2 + Mode 3: Step 0 clarifying questions asked + answers respected.
- [ ] Mode 4: §Decisions Anchored section populated.
- [ ] Closing report delivered.
