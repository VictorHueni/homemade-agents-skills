# Architecture Research — Methodology Bibliography

> This file is the canonical methodology bibliography for the `arch-research` skill. It is referenced from each project's research notes via a single-line methodology pointer in the file header; **it is never copied into project output**. This keeps the bibliography as a single source of truth across every project.

The `arch-research` skill produces evidence-based research notes that feed ADR decisions. The format combines three distinct disciplines: structured desk research (from BABOK), citation rigour (from academic + regulatory practice), and decision-support framing (from ADR + research-spike traditions). Sources below are the canonical references for each.

---

## Structured desk research

### BABOK v3 §10.43 — Document Analysis (IIBA, 2015)

Document Analysis is the BABOK technique of extracting business analysis information from existing documentation. Its discipline applies directly to architecture research: identify relevant sources, evaluate source quality, extract findings systematically, and traceably link findings back to the documents they came from.

**Key principles imported into `arch-research`:**
- Source authority must be evaluated (the BABOK "currency, relevance, source authority" checklist → the skill's confidence rubric)
- Findings must be traceably linked to source citations (BABOK traceability requirement → the skill's per-source quote requirement)
- Documents change over time (BABOK currency requirement → the skill's `Last verified` discipline + refresh cadence)

Reference: BABOK v3 §10.43 Document Analysis (IIBA, 2015).

### Erika Hall — *Just Enough Research* (A Book Apart, 2nd ed. 2019)

Hall's "research as a small, focused activity that informs specific decisions" framing pushes against the consultancy-style "comprehensive landscape report." Every research effort should answer a specific question that changes a specific decision.

**Key principles imported:**
- Question-first research (Hall §2 "Asking the Right Questions" → the skill's mandatory Questions index + question-framing test)
- Distinguish research from reference material (Hall §1 "What is Research?" → the skill's lifecycle: Active → Frozen-on-ADR-decision)
- Reusable templates beat bespoke reports (Hall §4 "Tools and Techniques" → the skill's fixed template structure)

Reference: Hall, Erika. *Just Enough Research* (A Book Apart, 2nd edition, 2019).

---

## Architecture Decision documentation (the consumer of this research)

### Michael Nygard — "Documenting Architecture Decisions" (2011)

Nygard's original ADR essay defined the lightweight decision-record pattern that this skill's research notes feed into. The research-vs-decision separation in this skill (research informs; ADRs decide) is a direct elaboration of Nygard's separation between Context, Decision, and Consequences in an ADR.

**Key principles:**
- Decisions are records of past commitments, not future plans (Nygard's Status workflow → the skill's lifecycle)
- Context is the audit trail for the decision (Nygard's Context section → the skill's research notes that get cited from the ADR's Context)

Reference: Nygard, Michael. *Documenting Architecture Decisions* (2011). [thinkrelevance.com](https://www.thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions).

### MADR 4.x specification (Markdown Any Decision Records)

MADR is the formalised template family for ADRs in markdown. The `arch-adr` skill in this kit produces MADR 4.x-compliant ADRs. `arch-research` notes are designed to be the evidence base that MADR ADRs cite from their Context + Decision Outcome sections.

**Linkage:** the `arch-research` skill's §Findings summary table is the citation target; MADR ADRs cite specific findings via Q-anchors.

Reference: [adr.github.io/madr](https://adr.github.io/madr/).

### ThoughtWorks Technology Radar — research-spike tradition

The Technology Radar pattern of "Adopt / Trial / Assess / Hold" reflects a research-driven lifecycle where evidence is gathered before commitment. While the Radar is more lightweight than this skill's research notes, the underlying discipline (research first, decide second, document both) is shared.

Reference: [thoughtworks.com/radar](https://www.thoughtworks.com/radar).

---

## Citation discipline + source quality

### Edward Tufte — *Beautiful Evidence* (Graphics Press, 2006)

Tufte's "ev.identity" principle — every assertion is paired with the evidence supporting it, with the source visible at the point of assertion — informs the skill's requirement that every Finding cite specific sources with quoted text, not "see bibliography" references.

**Key principles imported:**
- Sourcing belongs at the point of claim, not at the end of the document (Tufte §2 → the skill's per-Q Sources consulted tables instead of one consolidated bibliography only)
- Sources should be evaluable by the reader (Tufte §3 → the skill's "exact quote OR specific section reference" requirement)

Reference: Tufte, Edward. *Beautiful Evidence* (Graphics Press, 2006).

### Wikipedia's verifiability policy + reliable source guidelines

Wikipedia's WP:V (verifiability) and WP:RS (reliable sources) policies have produced one of the most thoroughly worked-out source-quality rubrics in public knowledge work. The `arch-research` confidence rubric is loosely modelled on WP:RS's tiering (primary vs secondary vs tertiary sources, with self-published sources at the bottom).

Reference: [en.wikipedia.org/wiki/Wikipedia:Reliable_sources](https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources).

---

## Regulatory + compliance research patterns

### IAPP (International Association of Privacy Professionals) — research methodology articles

IAPP publishes methodology guidance for privacy + data-protection research, including how to handle jurisdictional uncertainty, how to weight regulator opinions vs case law, and how to track regulatory amendments.

Reference: [iapp.org/news](https://iapp.org/news/) — search "research methodology" or "regulatory tracking".

### European Data Protection Board (EDPB) — guidelines, recommendations, and best practices

The EDPB publishes structured opinions on GDPR application. The format (Question / Background / Analysis / Conclusion) closely mirrors the structure this skill imposes on per-Q research sections. EDPB opinions are themselves ★★★★★ sources for any EU-data-protection research.

Reference: [edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en](https://edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en).

### Swiss FDPIC (PFPDT / EDÖB) — published guidance

The Federal Data Protection and Information Commissioner publishes guidance on nFADP application. As the enforcement authority, FDPIC's published guidance is the ★★★★★ source for any Swiss data-protection research.

Reference: [edoeb.admin.ch/edoeb/en/home.html](https://edoeb.admin.ch/edoeb/en/home.html).

---

## Why these specific influences

The `arch-research` skill is not a generic research-notes tool. It exists for a specific purpose: produce evidence that ADRs can cite, with auditable sourcing, in a format that survives the 3–6 month lag between research and decision.

| Influence | What it solves |
|---|---|
| **BABOK Document Analysis** | Source quality evaluation + traceable findings — without this, research becomes opinion |
| **Hall "Just Enough Research"** | Question-first framing — without this, research becomes a wall of notes |
| **Nygard ADR + MADR** | The consumer of this research; the format must produce ADR-citable output |
| **Tufte ev.identity** | Citations at point of claim — without this, ADR readers can't audit |
| **Wikipedia WP:RS** | Source-tier rubric — without this, confidence ratings drift |
| **EDPB / FDPIC** | The actual ★★★★★ sources for the specific use case (CH/EU regulatory research) |

**No reference to:** academic literature review methodology (Hart 1998, Booth et al. 2008). This is because architecture research is decision-support, not contribution-to-knowledge; the discipline differs.

---

## Project-side linkage

Each research note in a project carries a single-line methodology pointer in its header:

```markdown
> **Methodology:** built using the canonical synthesis documented in the
> [arch-research skill bibliography](https://github.com/VictorHueni/homemade-claude-kit/tree/main/arch-research/references/methodology-references.md).
```

The bibliography itself is not copied into the project — it stays here, single source of truth, updatable across all projects simultaneously.
