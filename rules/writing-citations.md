---
type: rule
paths:
  - "docs/architecture/**"
  - "docs/business/**"
  - "docs/communication/**"
  - "docs/discovery/**"
  - "**/bibliography.yaml"
---

# Citations & sources

Two distinct rules for citation handling — the two channels never substitute for each other.

## Markdown docs (analysis, models, READMEs, specs)

Every source mention gets a direct inline link: `[Source name](https://...)`. Never write "see bibliography" or bare source names. Applies to every figure, every citation, every external reference — including sources that are also in a slide bibliography.

## Pitch-deck / slide `bibliography.yaml`

Add an entry only when the source is actually cited in a slide. Do NOT pre-populate with sources that *might* be useful — bibliography reflects current slide content, not the broader research corpus. Cleaning the file to "sources currently used in slides only" is an explicit, user-requested operation.

**Why:** The bibliography is a slide-build artefact (the slide builder validates each cited source against it). The markdown research docs are the upstream knowledge base. Mixing the two channels causes bloat (yaml entries for unused sources) and broken citations (markdown sources without URLs because the writer assumed the bibliography had them).

## Conversational responses (agent-to-user)

Every factual claim, statistic, or figure stated in a conversation must include at least a source name. Whenever the source has a public URL, include it as a direct inline link. When the source is a paper, include the arXiv ID or canonical identifier. Never write bare numbers without attribution.

**Examples:**
- "Harness change improved SWE-bench from 6.7% → 68.3% (Pi Research)"
- "95% of enterprise pilots saw no measurable ROI (MIT, cited by VFuture Media)"
- "Frontier LLMs achieve 15-35% container escape rates (SandboxEscapeBench, arXiv 2603.02277)"

**Why:** Numbers without sources are indistinguishable from hallucination. Attributing every figure lets the user verify, trust, or challenge the claim. This applies whether the user asked for research or the fact is stated in passing.
