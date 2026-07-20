# Business Research — Methodology References

This document records the canonical frameworks used to design and maintain
research artefacts (interview scripts, research synthesis, research
plans). The artefact is a synthesis of five sources — each contributes a
specific lens.

The skill produces three artefact types: interview scripts
(hypothesis-anchored, semi-structured), research synthesis (post-interview
findings), and optional research plans (scoping a research wave).

---

## 1. BABOK® §10.25 — Interviews

**Used for:** the canonical interview taxonomy (structured / unstructured
/ hybrid) and the business-analysis framing of interviews as systematic
elicitation.

**Source:** *A Guide to the Business Analysis Body of Knowledge® (BABOK®
Guide), v3*, International Institute of Business Analysis (IIBA),
§10.25 "Interviews". Reference page:
[iiba.org BABOK §10.25](https://www.iiba.org/knowledgehub/business-analysis-body-of-knowledge-babok-guide/10-techniques/10-25-interviews/)
(paywalled).

### Key contributions

- **Definition:** *"An interview is a systematic approach designed to
  elicit business analysis information from a person or group of people
  by talking to the interviewee(s), asking relevant questions, and
  documenting the responses."*
- **Two types:**
  - **Structured Interview** — predefined set of questions; consistency
    across interviews; better for quantitative comparison.
  - **Unstructured Interview** — no predetermined format; questions vary
    based on responses; better for exploration.
- **Hybrid is the practitioner default** — *"business analysts may use
  a combination of the two types by adding, dropping, and varying the
  order of questions as needed."* This is what most user-research
  literature calls **semi-structured**.

### Discipline encoded in the skill

- Skill default is semi-structured (Step 0 question 3).
- Interview-script template has fixed sections (consistency) with
  per-question probing (flexibility).
- Companion §10.31 Observation is referenced for workflow-discovery
  interviews where the interviewer should also observe practice.

---

## 2. Steve Portigal — *Interviewing Users* (2nd ed., 2022)

**Used for:** the semi-structured interview technique, probing-question
discipline, analysis + synthesis patterns, and the practitioner stance
of "the interview is an act of empathy".

**Source:** Steve Portigal, *Interviewing Users: How to Uncover
Compelling Insights* (2nd ed., Rosenfeld Media, 2022).
[Publisher page](https://rosenfeldmedia.com/books/interviewing-users-second-edition/).
Sample chapter:
[Rosenfeld Media sample chapter](https://rosenfeldmedia.com/interviewing-users-second-edition-sample-chapter/).

### Key contributions

- **Semi-structured = consistency + flexibility.** The interviewer
  follows a guide but probes where the interviewee opens unexpected
  doors. Every interview is unique because the probing is unique.
- **Probing hierarchy:**
  - **Open-ended** — "Tell me about the last time you..."
  - **Specific** — "When you said X, what did you mean by..."
  - **Confirming** — "So if I understood, you're saying..."
- **The interview is an act of empathy.** The interviewer's job is to
  understand the interviewee's worldview, not to validate the
  interviewer's hypotheses.
- **Analysis + synthesis are separate skills** from interviewing.
  Portigal's 2nd edition added a full chapter on this (the bridge
  between transcripts and insights).

### Discipline encoded in the skill

- Per-question "What you're listening for" column forces the interviewer
  to articulate the signal they're hunting (Portigal-style discipline).
- Soft-prime → core question → cross-check pattern in the template
  mirrors Portigal's probing hierarchy.
- Synthesis is treated as a separate skill — its own mode (mode 3) with
  its own template, not lumped into the interview script.

---

## 3. Erika Hall — *Just Enough Research* (2nd ed., 2019)

**Used for:** the principle that research scope should match the
decision being made — not exhaustive, not absent — and the integration
of research into product development as continuous practice.

**Source:** Erika Hall, *Just Enough Research* (2nd ed., A Book Apart,
2019). Reference: [A Book Apart](https://abookapart.com/products/just-enough-research).

### Key contributions

- **"Just enough" principle.** Research should be sized to the decision
  it informs. 30 interviews for a small UX tweak is wasteful; 0
  interviews for a $1M product bet is reckless.
- **Research as continuous practice.** Not a one-time phase; integrated
  into product cycles. The build-measure-learn loop (Lean Startup)
  depends on research being lightweight enough to repeat.
- **Hypothesis-driven design.** Every research wave tests specific
  hypotheses; "let's learn about the customer" is too vague to design.

### Discipline encoded in the skill

- Hypothesis-anchored frontmatter on every interview script (every
  interview must name 1–4 specific upstream open questions it
  unblocks).
- Refresh / iteration mode (mode 3) supports continuous research, not
  one-time waves.

---

## 4. Tomer Sharon — *Validating Product Ideas* (2016) + *It's Our Research* (2012)

**Used for:** the assumption-testing framework — how to translate vague
product hypotheses into testable interview questions.

**Source:** Tomer Sharon, *Validating Product Ideas* (Rosenfeld Media,
2016) and *It's Our Research* (Morgan Kaufmann, 2012).

### Key contributions

- **Assumption auditing.** Before designing research, surface every
  assumption baked into the upstream artefact (persona, BMC, model).
  Each assumption is a candidate for testing.
- **HXD framework (Hypothesis × Experiment × Data).** For each
  hypothesis, name (1) what evidence would confirm it, (2) what
  evidence would refute it, (3) what method (interview, observation,
  prototype test) generates that evidence.
- **The 5 Whys for hypothesis testing.** Probe why each assumption was
  made — the original reasoning often reveals where the assumption is
  weakest.

### Discipline encoded in the skill

- The hypothesis-anchored frontmatter explicitly references upstream
  artefact open questions / `Assumed` claims.
- Synthesis template has a "Per-hypothesis verdict" column that maps
  back to the original hypothesis: confirmed / refuted / refined.
- Confidence ratings (Assumed / Tested / Validated) propagate from
  upstream artefacts → interview targets → synthesis verdicts → back
  to upstream artefacts.

---

## 5. Nielsen Norman Group — Practitioner Discipline

**Used for:** the saturation rule (5 interviews per persona reveals
~85% of usability issues; diminishing returns thereafter), interviewer
failure-mode catalogue, and recording / consent / transcription
discipline.

**Source:** NN/g (Nielsen Norman Group) user-research articles.
Canonical references:
- [Why You Only Need to Test with 5 Users](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/) (Jakob Nielsen, 2000)
- [User Interviews: Tutorial Resources](https://www.nngroup.com/articles/user-interviews/) — practitioner guidance
- [Interview Questions That Work](https://www.nngroup.com/articles/open-ended-questions/) — question discipline

### Key contributions

- **5-user saturation rule** for usability and persona validation. After
  5 interviews per persona, returns diminish sharply.
- **Common interviewer failure modes:**
  - Leading questions ("don't you think X is bad?")
  - Premature pitching (selling within the first 30 min)
  - Confirmation bias (only hearing what supports hypothesis)
  - Single-quote inflation (one strong quote = "the data says")
- **Recording + consent.** Always ask; many professionals decline; have
  a notes-only fallback ready.

### Discipline encoded in the skill

- Sampling guidance in research-plan template: 5–8 for first wave, 12–15
  for variance.
- Interview-script template has explicit "DO NOT pitch in the first 30
  min" warning.
- `interview-techniques.md` (kit-only) catalogues the common failure
  modes for Claude to apply when generating.

---

## 6. (Related but out of scope) — Diary studies, contextual inquiry, surveys

**Used for:** awareness only. The skill does not produce these artefacts
in v1.

- **Diary studies** (Sauer & Brown method) — useful for multi-day
  workflow capture; rare for B2B research.
- **Contextual inquiry** (Beyer & Holtzblatt, 1998) — observation +
  interview hybrid; powerful for process-discovery; consider as
  extension.
- **Surveys** (Don Dillman, *Tailored Design Method*, 2014) — useful for
  quantitative validation after qualitative themes emerge; different
  methodology canon.

These can be added as new modes if user demand emerges.

---

## Summary — what each framework contributes

| Framework | Contributes |
|---|---|
| BABOK §10.25 | Interview taxonomy (structured / semi / unstructured); business-analysis framing |
| Steve Portigal | Semi-structured discipline; probing hierarchy; synthesis as separate skill |
| Erika Hall | "Just enough" sizing; hypothesis-driven; continuous research |
| Tomer Sharon | Assumption-testing framework; HXD (Hypothesis × Experiment × Data); confidence propagation |
| Nielsen Norman Group | 5-user saturation; interviewer failure modes; recording + consent |
| Out-of-scope (diary / contextual / survey) | Awareness; possible v2 extensions |

The template is not "Portigal" or "BABOK" alone — it is the canonical
synthesis adapted for hypothesis-anchored, artefact-targeted research.
The practitioner-derived 8-pattern discipline (pre-prep with Why, soft-prime →
core → cross-check, listening column, limits, synthesis template, next
steps) sits on top.
