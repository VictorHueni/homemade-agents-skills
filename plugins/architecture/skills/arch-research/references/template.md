<!-- doc-version: 1.0 | created: {{YYYY-MM-DD}} | last-verified: {{YYYY-MM-DD}} -->

# Research-{{NNNN}} — {{Topic title}}

**Status:** {{Draft | Active | Frozen | Superseded}}
**Date:** {{YYYY-MM-DD}}
**Author:** {{Author}}
**Last verified:** {{YYYY-MM-DD}}  ← bump on every Mode 3 Refresh
**Feeds ADRs:** {{ADR-NNNN (§option C) · ADR-MMMM (§drivers) · ...}}
**Superseded by:** —

<!--
LIFECYCLE LEGEND
  Draft     — actively populating; ADRs should not cite yet
  Active    — content complete enough for ADR citation; further updates allowed
  Frozen    — feeding ADRs have landed; further edits only via Mode 3 Refresh
             that promotes this file to Superseded + creates a successor
  Superseded — replaced by a newer research file; `Superseded by:` link mandatory
-->

---

## Questions index

1. {{Q1 — single specific, falsifiable question}}
2. {{Q2 — single specific, falsifiable question}}
3. {{Q3 — single specific, falsifiable question}}

<!-- Add more questions if needed. Recommended range: 3–7. If >7, split into a second research note. -->

---

## Q1 — {{restated question}}

### Context

{{1–2 paragraphs: why this question matters, what's at stake, which decision it informs. Keep concrete. Avoid generic statements.}}

### Sources consulted

| Source | URL | Type | Last verified | Confidence | Key quote / finding |
|---|---|---|---|---|---|
| {{Source name}} | [{{link text}}]({{url}}) | {{Statute / Regulator guidance / Standard / Law-firm guidance / Audit-firm guidance / Industry survey / Consultancy / Vendor publication / Academic paper}} | {{YYYY-MM-DD}} | {{★★★★★}} | "{{exact short quote OR specific §reference}}" |
| {{...}} | ... | ... | ... | {{...}} | "{{...}}" |

<!--
CONFIDENCE RUBRIC (see references/discipline.md for full rubric)
  ★★★★★ Primary statute / regulator publication (FDPIC, FOPH, EDPB, FINMA, ISO official)
  ★★★★  Major law-firm or audit-firm guidance · official standard documentation
  ★★★   Industry-association guidance · peer-reviewed compliance journal
  ★★    Consultancy blog · vendor whitepaper · Stack Overflow consensus
  ★     Anecdote · single-source weak signal — flag in §Open Items

TYPE TAXONOMY
  Use one of: Statute · Regulator guidance · Standard · Law-firm guidance ·
              Audit-firm guidance · Industry survey · Consultancy ·
              Vendor publication · Academic paper

LAST VERIFIED DATE
  When you opened the URL and confirmed the quoted text still appears there.
  Bump on every Mode 3 Refresh. Stale dates erode the entire file's credibility.
-->

### Finding

{{1–3 paragraphs synthesising the sources into a falsifiable answer to the question. Be honest about uncertainty. State the answer first, then nuance.}}

### Implication for ADRs

- **{{ADR-NNNN}}:** {{how this finding shapes option preference — e.g. "Eliminates Option D (database-per-tenant) as over-engineering given INV nFADP Art. 8 'appropriate measures' standard does not mandate physical isolation"}}
- **{{ADR-MMMM}}:** {{...}}

<!-- Unresolved gaps for this question are NOT captured here. They are consolidated into the document-level §Open Items section at the bottom of the file, with `Source anchor = #q1` and `Source heading = "Q1 — {{restated question}}"` so each row remains traceable to its originating question. See the `metamodel` skill's `references/open-items-governance.md` §1 + §4. -->

---

## Q2 — {{restated question}}

### Context

{{...}}

### Sources consulted

| Source | URL | Type | Last verified | Confidence | Key quote / finding |
|---|---|---|---|---|---|
| {{...}} | ... | ... | ... | ... | "{{...}}" |

### Finding

{{...}}

### Implication for ADRs

- **{{ADR-NNNN}}:** {{...}}

<!-- Per-Q unresolved gaps are consolidated into §Open Items at the bottom with `Source anchor = #q2` + `Source heading = "Q2 — {{restated question}}"`. -->

---

## Q3 — {{restated question}}

{{repeat structure}}

---

## Findings summary (citable from ADRs)

| Q | Finding (one sentence) | Confidence | Feeds |
|---|---|---|---|
| Q1 | {{One-sentence answer — should be quotable verbatim from an ADR}} | {{★★★★}} | {{ADR-NNNN, ADR-MMMM}} |
| Q2 | {{...}} | {{★★★}} | {{ADR-NNNN}} |
| Q3 | {{...}} | {{★★}} | {{TBD — exploratory}} |

<!--
This table is the canonical citation target for ADRs.
ADRs should cite specific cells: `[Research-NNNN §findings Q1](../research/NNNN-slug.md#findings-summary-citable-from-adrs)`
The one-sentence Finding is what gets quoted in the ADR's Decision Outcome section.
-->

---

## Decisions Anchored

<!--
ONLY populated in Mode 4 Freeze, once the feeding ADRs have landed.
List each landed ADR + the specific findings it cited or overrode.
Historical record — do not edit after Freeze.
-->

_(empty until Mode 4 Freeze)_

---

## Consolidated sources

<!--
Deduplicated by URL. Grouped by type. Single source-of-truth list at file bottom.
Mirrors the [writing-citations rule](https://github.com/VictorHueni/homemade-claude-kit/blob/main/rules/writing-citations.md):
every source has a real verifiable URL; no "see bibliography" without link.
-->

### Primary law + regulator publications

- [{{Source name}}]({{url}}) — {{1-line description}}

### Standards (ISO, IEC, etc.)

- [{{...}}]({{...}}) — {{...}}

### Law-firm / audit-firm guidance

- [{{...}}]({{...}}) — {{...}}

### Industry / association guidance

- [{{...}}]({{...}}) — {{...}}

### Vendor / consultancy material

- [{{...}}]({{...}}) — {{...}}

### Academic / peer-reviewed

- [{{...}}]({{...}}) — {{...}}

---

## Changelog

| Date | Author | Mode | Change summary |
|---|---|---|---|
| {{YYYY-MM-DD}} | {{Author}} | Scaffold | Initial scaffold. Topic: {{...}}. Questions: {{N}} planned. |
| {{YYYY-MM-DD}} | {{Author}} | Fill | Q1 + Q2 populated. Q3 deferred — sources for {{specific gap}} not yet located. Status: Draft → Active. |
| {{YYYY-MM-DD}} | {{Author}} | Refresh | Re-verified all URLs (12 of 14 still resolve; 2 moved — updated). Promoted Q2 confidence ★★★ → ★★★★ after [law-firm guidance publication](...). No findings flipped. |
| {{YYYY-MM-DD}} | {{Author}} | Freeze | ADR-0003 landed at Option E citing Q1 + Q2 findings. ADR-0004 landed at Option B; Q3 finding (cost analysis) was considered but not the deciding factor. Status: Active → Frozen. |
