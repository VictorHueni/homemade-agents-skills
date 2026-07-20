# Interview Techniques — Internal Claude Guidance

This file is **not** copied into the project. It is internal guidance the
skill consults when generating interview scripts, applying probing
discipline, sizing samples, and avoiding common failure modes.

---

## The probing-question hierarchy (Portigal)

When designing per-section questions, layer them:

| Level | Type | Example |
|---|---|---|
| 1 | **Open-ended** — tell-me-about | *"Tell me about the last time you had to track a price change."* |
| 2 | **Specific** — when-you-said | *"When you said 'I missed it' — what specifically happened?"* |
| 3 | **Confirming** — so-if-i-understood | *"So if I understood correctly, you waited 3 weeks before noticing — is that right?"* |
| 4 | **Counterfactual** — what-if | *"What if your system had alerted you the same day — would that have changed the outcome?"* |
| 5 | **Cross-check** — different-angle | *"You said earlier you spend 12h/week on this. If I asked you to estimate your team's total monthly hours, what would you say?"* |

**Pattern:** start with level 1, drop to level 2-3 when responses are
vague, use level 4 for hypothesis stress-testing, use level 5 to
triangulate quantifiable claims.

---

## Soft-prime → core question → cross-check (practitioner-tested pattern)

The the gold-standard hypothesis-anchored interview template pioneered a
sequence that should be reused in every quantifiable hypothesis section:

```
1. SOFT PRIME: cite an external reference or offer a range
   "An industry body published $300M restituted. Does that match your intuition,
    or feel too high / too low?"
   → Lets the interviewee react to a number without you anchoring on one.

2. CORE QUESTION: ask the direct question, offering brackets
   "On the PMs where your insurer should get a restitution — what % is actually recovered?
    Not a precise number; just intuition: 30%, 50%, 70%?"
   → The answer. Note exact words + qualifications.

3. CROSS-CHECK: ask the same metric a different way
   "On the $300M industry total, how much does your insurer recover, roughly?"
   → Back-derive the % from currency / market-share share.
   → If cross-check disagrees with core, ASK which feels more accurate and WHY.
     The reconciliation reveals the deeper truth.
```

This sequence avoids two failure modes simultaneously:
- **Anchoring** (the interviewer's number distorts the answer)
- **Mis-estimation** (the interviewee over-confidently states a single number that doesn't survive a sanity check)

Apply this pattern to EVERY quantifiable hypothesis (recovery rates,
WTP, FTE counts, cycle times, market shares, etc.).

---

## What you're listening for — coaching column

The practitioner reference template's killer feature. For every question, the script
includes a "What you're listening for" column that articulates the
signal the interviewer should hunt — separately from the words on the
surface.

Examples (drawn from practitioner literature):

| Question category | What you're listening for |
|---|---|
| "How do you do X today?" | Existence of tools / vendor names / spreadsheet usage / manual workarounds |
| "What's broken about how you do X?" | Catalogue of failure modes — gold for product spec |
| "Who decides Y?" | Decision-maker title + organisational location |
| "How much do you spend on X?" | Anchor for WTP range — but also reveals whether it's a budget line or buried |
| "Have you tried competitor Z?" | Evaluation depth — did they POC? Bake-off? Why pick or reject? |
| "If you were me, what should I know?" | The lurking truth nobody else has said |
| "Tell me about a recent example." | Concrete signal beats abstract estimates |

**Discipline:** if the listening column is empty (`_TODO_`), the
question shouldn't ship in the script. The interviewer needs to know
what they're hunting before they ask.

---

## Sample-size guidance (NN/g + practitioner)

| Goal | Sample size | Source |
|---|---|---|
| Usability — find ~85% of issues | 5 users per persona | Nielsen (2000) |
| Persona validation — confirm bio / JTBD | 5–8 per persona | NN/g saturation |
| Persona discovery — build from scratch | 8–12 | NN/g + practitioner |
| Variance / segment difference | 12–15 (across segments) | Tomer Sharon |
| Quantitative validation | Survey N≥30, NOT interviews | Practitioner |

**Stop criteria:**
- Saturation reached (3 interviews in a row reveal no new themes)
- Hypothesis decisively confirmed or refuted earlier than planned
- Decision being informed becomes binary (no more research moves the dial)

**Do NOT** keep interviewing past saturation. The marginal interview
costs time + recruit effort + creates more synthesis work without
moving the dial.

---

## Common interviewer failure modes

### Mode 1 — Leading questions

❌ *"Don't you think the current process is broken?"*
✅ *"How would you describe the current process?"*

The leading version pre-supposes brokenness; the open version lets the
interviewee surface (or not surface) the brokenness in their own words.

### Mode 2 — Premature pitching

The first 30 minutes of any interview should be PURE EXTRACTION. No
mention of the product, no "here's what we're building", no validation
seeking. The interviewee's un-coached signal degrades the moment they
know what answer you want.

**Discipline:** the interview-script template has an explicit DO NOT
pitch warning after the opening prompt.

### Mode 3 — Confirmation bias in synthesis

The interviewer wants the hypothesis confirmed; quotes that support it
get cited; quotes that refute it get explained away. Symptoms:
- Single supporting quote treated as "the data says X"
- Refuting quotes appear in synthesis but are framed as "outliers"
- Per-hypothesis verdict is "confirmed" with cluster size of 1

**Fix:** the synthesis template's "Cluster size: N out of N" field
forces honest accounting.

### Mode 4 — Specificity → abstraction inflation

The interviewee tells a specific story; the interviewer abstracts it to
a general claim that the story doesn't support.

❌ *Quote: "Last month we missed the a specific outcome-based milestone because the indication code was wrong."* → Synthesis: *"Indication codes are a major systemic problem."*
✅ Synthesis: *"At least one interview confirmed indication-code errors cause missed P4P milestones (1/N — need more interviews to claim systemic)."*

**Discipline:** synthesis cluster-size column forces this.

### Mode 5 — Recording without consent

Always ask. Many B2B professionals decline. Have notes-only fallback
ready (handwritten + digitised within 1h is fine).

### Mode 6 — Skipping the "if you were me" closing question

This question often produces the most valuable signal of the entire
interview. The interviewee has spent 50 minutes thinking about the topic
and is most warmed-up at the end. Ask.

### Mode 7 — Skipping the warm-intro ask

Costs nothing; often produces 1-2 referrals; halves recruitment cost
for the next wave.

### Mode 8 — Delaying synthesis past 24h

Memory degrades fast. Names blur. Specific phrases get reconstructed
inaccurately. Fill the synthesis template within 1h of the interview;
write the headline finding in 1 sentence within 24h MAX.

---

## Recording + consent + transcription discipline

### Recording

- **Ask explicitly** — "I'd like to record the conversation to help me capture nuances. May I?" Most B2B professionals will decline.
- **If declined, take detailed notes by hand.** Better than half-recording.
- **If accepted, record audio only** (no video unless visual artefacts are central). Audio-only consent rates are much higher than video.

### Consent

- **Anonymisation by default** — interviewee's name does not appear in research artefacts; only role + org type ("pharma desk analyst at a mid-size insurer").
- **Withdrawal rights** — they can withdraw at any point; their data gets purged.
- **Retention** — declare how long notes / transcripts will be kept (typically 6-12 months); delete on schedule.

### Transcription

- **Manual transcription** for ≤5 interviews — preserves nuance.
- **Otter / Whisper / similar** for >5 — faster, less nuanced. Always proofread the auto-transcript.
- **Notes-only fallback** — if no recording, write up within 1h. Use the structure: verbatim quote where possible · paraphrase elsewhere · note context (silence, hesitation, tone).

---

## Cross-doc linking discipline

When the synthesis updates upstream artefacts, **cite the specific section**, not just the file:

❌ "Update personas.md"
✅ "Update `docs/business/01a-personas.md` §P-02 → Frustrations item 3: change from 'Assumed: manual reconciliation is slow' to 'Tested: manual reconciliation takes 12h/week per analyst (Interview Marc, 2026-05-23)'"

The next maintainer should be able to apply the update without
re-reading the interview.

---

## Quality checks before saving an interview script

Run this mentally — don't print into the file:

- [ ] Frontmatter names 1–4 specific upstream open questions.
- [ ] Pre-interview prep checklist has Why column filled.
- [ ] Opening scripted; DO NOT pitch warning present.
- [ ] Each section has goal + soft-prime + core question + cross-check (where applicable).
- [ ] Every question has "What you're listening for" filled (mandatory).
- [ ] §Limits section explicit; not empty.
- [ ] §Post-interview synthesis template embedded.
- [ ] §What to do after has file-§ targeted next steps.
- [ ] Closing has "if you were me" + warm-intro ask.
- [ ] Language matches the interviewee's working language (recording + ground rules in their language).

## Quality checks before saving a synthesis

- [ ] Sample summary complete (N interviews, dates, roles, channel).
- [ ] Per-hypothesis verdict assigned (Confirmed / Refuted / Refined).
- [ ] Cluster size honest (`N out of N interviews` — no inflation).
- [ ] Per-artefact updates table filled with specific § references.
- [ ] Confidence-shift column populated.
- [ ] §Open Items captured per canonical schema (actionable unresolved work for the next wave, with `Source anchor` + `Source heading` provenance); empty is acceptable. See the `metamodel` skill's `references/open-items-governance.md`.
