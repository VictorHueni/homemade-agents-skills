<!-- INTERVIEW SCRIPT TEMPLATE — copy below; replace placeholders -->

# {{Persona-or-role}} Interview — Structured Plan

A {{duration-min}}-minute interview designed to unblock the following
open questions in upstream artefacts:

1. **{{Hypothesis 1 — e.g., "recovery rate" in model §4}}** — currently `Assumed`; this interview targets `Tested`
2. **{{Hypothesis 2}}** — _TODO_
3. **{{Hypothesis 3}}** *(optional)* — _TODO_
4. **{{Hypothesis 4}}** *(optional)* — _TODO_

This single interview can flip rows {{N}}, {{M}} of the
[validation tracker]({{path-to-validation-tracker}}) from
{{from}} to {{to}}.

> **Methodology:** built using the canonical synthesis of [BABOK §10.25
> Interviews + Steve Portigal *Interviewing Users* (2022) + Erika Hall
> *Just Enough Research* + NN/g semi-structured guidance + Tomer Sharon
> assumption-testing](https://github.com/VictorHueni/homemade-claude-kit/tree/main/discovery-research/references/methodology-references.md).
> Full bibliography lives with the [discovery-research
> skill](https://github.com/VictorHueni/homemade-claude-kit/tree/main/discovery-research).

**Frontmatter:**
- **Target persona:** [P-NN link or "TBD — interview will help build one"]
- **Interview style:** Semi-structured / Structured / Unstructured
- **Duration target:** {{60-90}} min
- **Language:** {{English / French / DE / ...}}
- **Recording:** {{with consent / notes-only}}
- **Date scheduled:** _TODO_
- **Interviewee role:** _TODO_

---

## Pre-interview prep (15 min before)

| Item | Why |
|---|---|
| Confirm role: actual {{target-persona}}, not adjacent role | Wrong persona kills 80% of the value of the questions below |
| Bring upstream artefacts: {{specific files/refs}} | Lets you show numbers/claims live as anchors for "is this realistic?" |
| Have key claims memorised: {{specific values}} | The interview's central questions revolve around these |
| _TODO_: prep item 4 | _TODO_: why |
| Note: keep recording OFF unless they explicitly OK it; take notes by hand and digitise after | Most professionals won't talk freely on tape |

---

## Opening — 3 min

> *"{{Opening prompt in the interviewee's language. Always: thank them, frame
> the purpose (hypothesis testing, not pitching), promise to validate vs
> invalidate your assumptions, set the duration, ask for OK to proceed.}}"*

**Do NOT pitch the product in the first 30 minutes.** The whole point is to
extract un-coached signal.

**Ground rules:**
- Open-ended questions; let silences happen
- No leading questions ("don't you think X is bad?")
- Note exact words verbatim where possible
- Park follow-up questions; come back at the end if time

---

## Section A — {{Their workflow today}} (10 min)

**Goal:** ground truth on how {{the target activity}} actually happens today.
Without this, you can't interpret their answers in later sections.

| # | Question | What you're listening for |
|---|---|---|
| A1 | *"{{Question 1 in their language}}"* | {{What signal to extract: existence of tools, competitive intel, frequency, etc.}} |
| A2 | *"{{Question 2}}"* | {{What you're hunting}} |
| A3 | *"{{Question 3}}"* | {{Signal}} |
| A4 | *"{{Question 4}}"* | {{Signal}} |
| A5 | *"{{Question 5}}"* *(optional)* | {{Signal}} |

---

## Section B — {{Headline hypothesis}} (15 min)

**Goal:** {{the primary hypothesis to test — write the specific upstream §
or persona field this unblocks}}.

**Soft prime — don't anchor too hard:**

> *"{{Soft-prime: cite an external reference or a range, ask them to react
> rather than anchor on your number}}"*

**Core question:**

| # | Question | What you're listening for |
|---|---|---|
| B1 | *"{{The core question — the central unblocker}}"* | **The answer.** Write exact words + any qualifications. Hesitation IS signal. |
| B2 | *"{{Probing question for type / category}}"* | {{Validates breakdown / variance}} |
| B3 | *"{{Probing question for failure modes}}"* | {{Catalogue of failure modes — gold for the spec}} |
| B4 | *"{{Probing question for visibility}}"* | {{Tests assumption X}} |
| B5 | *"{{Cross-check: same metric a different way}}"* | {{If B1 and B5 disagree, the discrepancy reveals truth — ask which feels more accurate and why}} |

**Critical:** if B1 and B5 give different values (e.g., direct % vs back-derived %), ask which one feels more accurate and why. Their explanation reveals the deeper truth.

---

## Section C — {{Variance / spread / per-segment}} (10 min)

**Goal:** {{validate or refute the variance assumption — e.g., model §5.0.1
assumption N}}.

| # | Question | What you're listening for |
|---|---|---|
| C1 | *"{{Question about extremes / large vs small / experienced vs new}}"* | {{The variance hypothesis lives or dies here}} |
| C2 | *"{{Why does this variance exist?}}"* | {{Tells you what your product needs to deliver differently per segment}} |
| C3 | *"{{Is the segment networked / atomised?}}"* | {{Tests whether warm intros are possible or cold outreach only}} |
| C4 | *"{{Skew / outlier question}}"* | {{Validates whether assumption holds for their specific case}} |

---

## Section D — {{Pricing / WTP / budget}} (10 min)

**Goal:** validate the WTP / budget assumption. **This is the second-softest input in any model.**

| # | Question | What you're listening for |
|---|---|---|
| D1 | *"{{What do you spend today on the equivalent capability?}}"* | Sets the baseline. If they say "$200K/yr in FTE", a $60-120K tool is plausible. |
| D2 | *"{{Imagine a tool that does X — what budget could you justify?}}"* | The WTP unblocker. **Don't anchor with a currency figure — let them say one first.** |
| D3 | *"{{Fixed price vs contingency / variable?}}"* | Their preference tells you which pricing model survives procurement. |
| D4 | *"{{Direct sanity check: would $X/month be credible? Too high? Too low?}}"* | Reaction is the answer. |
| D5 | *"{{Have you evaluated competitor X? Why pick or reject?}}"* | Direct competitive intel — gold for the landscape doc. |

---

## Section E — {{Buying process}} (5 min)

**Goal:** {{the BABOK-canonical stakeholder + budget + cycle + proof
questions, compressed}}.

| # | Question | What you need to extract |
|---|---|---|
| E1 | *"{{Who signs?}}"* | Decision-maker title |
| E2 | *"{{What budget line?}}"* | Budget owner + line |
| E3 | *"{{What's the typical sales cycle?}}"* | Cycle months (expect 6-18 in B2B; longer in regulated) |
| E4 | *"{{What proof do you need?}}"* | POC? Reference customer? Audit? Pilot? |

---

## Closing — 5 min

> *"Une dernière question — si vous étiez à ma place, quelle est la chose
> que je devrais comprendre sur ce marché que personne d'autre ne m'a
> dit ?"*

> *"{{Equivalent in interview language}}"*

**Always ask this.** The signal is often the most valuable part of the interview.

Then:

> *"Merci. Est-ce que je peux revenir vers vous si j'ai une question de
> follow-up ? Et — il y a une ou deux personnes que je devrais
> absolument parler ?"*

→ The warm-intro ask. Worth one declined ask to get two intros if they say yes.

---

## Limits — what this interview will NOT answer

Be honest with the interviewee + with yourself + with future readers
about scope boundaries:

- **{{Limit 1 — e.g., "Total market size — that's a research / data question, not this role"}}** — covered by {{which other source}}
- **{{Limit 2 — e.g., "Strategic decisions about budgets — the analyst can give an opinion but the signature is elsewhere"}}** — separate interview with {{role}}
- **{{Limit 3}}** — {{covered by}}

---

## Post-interview synthesis template

Within 1 hour after the interview, fill this in. **Don't rely on memory beyond 24h.**

```markdown
# Interview synthesis — [insurer/company name], [date], [analyst initials]

## Headline finding (1 sentence)
[The most surprising or actionable thing they said]

## Section B — {{Headline hypothesis}} validation
- Their stated value: ___
- Cross-check (from B5): ___ → implies ___
- Reconciliation: [if B1 and B5 disagree, what they said about it]
- Confidence: ☐ Assumed (no change)  ☐ Tested  ☐ Validated

## Section C — Variance validation
- They believe segments differ by ___× on metric ___
- Reason: [in their words]
- Upstream assumption ___ is: ☐ confirmed  ☐ refuted  ☐ refined to: ___

## Section D — WTP validation
- Current spend: $___
- Their unprompted "I could justify $___" answer: ___
- Pricing-model preference: ___
- Reaction to specific price point: ___

## Section E — Buying process
- Decision-maker: ___
- Budget line: ___
- Sales cycle: ___ months
- Proof required: ___

## Competitive intel (Section D5 or other)
- Aware of competitors? ☐ yes (list) ☐ no
- Evaluated? ☐ yes ☐ no
- If evaluated, liked: ___; disliked: ___; rejected because: ___

## Updates to upstream artefacts

### Personas — P-NN
- [What changed about the persona from this interview]
- File update needed at: `docs/business/01a-personas.md` (specify section)

### BMC — block X
- [Confidence promotion from Assumed → Tested]
- File update needed at: `docs/business/02a-bmc.md` (specify block)

### Models — model slug
- [Input assumption recalibration: from ___ to ___]
- File update needed at: `docs/business/06a-models/qm-NN-{topic}.md` (specify section)

### Competitive landscape
- [New competitor mention / claim verification]
- File update needed at: `docs/business/01b-competitive-landscape/CO-NN-{slug}.md` (specify section)
```

---

## What to do after the interview

1. **Fill the synthesis template the same day.**
2. **Update the calculator/model defaults** — adjust the input ___, re-export, commit with `feat({{scope}}): re-anchor {{input}} to {{N}} per interview {{date}}`.
3. **Update upstream artefacts** as enumerated in the synthesis (persona § / BMC block / model § / landscape claim).
4. **Promote confidence ratings** on validated claims; demote those refuted.
5. **Update the project's `docs/discovery/interviews/README.md`** index with this interview's link + headline finding.

This single interview moves the [validation tracker]({{path}}) on {{N}} rows: {{rows-affected}}.

---

---

<!-- RESEARCH SYNTHESIS TEMPLATE — copy below; replace placeholders -->

# Research Synthesis — {{topic}} ({{date-range}})

Synthesis of N interviews + {{other methods if any}} conducted between
{{start-date}} and {{end-date}}, designed to test the following hypotheses
from upstream artefacts:

1. **{{Hypothesis 1}}** — was `Assumed`; this synthesis assigns verdict
2. **{{Hypothesis 2}}** — _TODO_
3. **{{Hypothesis 3}}** *(optional)*

> **Methodology:** [discovery-research kit-link methodology pointer](https://github.com/VictorHueni/homemade-claude-kit/tree/main/discovery-research/references/methodology-references.md)

---

## Sample summary

| Field | Value |
|---|---|
| **Interviews conducted** | N |
| **Date range** | {{YYYY-MM-DD}} to {{YYYY-MM-DD}} |
| **Roles interviewed** | [anonymised role + org type list, e.g., "3× pharma desk analysts at mid-size insurers; 1× medical advisor at large insurer"] |
| **Recruitment channel** | [warm intro / cold outreach / sales-rep referral / etc.] |
| **Geography** | _TODO_ |
| **Saturation reached?** | ☐ Yes (NN/g 5-interview rule met) ☐ No — N more needed |

---

## Headline findings

*3–5 most surprising or actionable insights. Lead with the most unexpected.*

1. **{{Finding 1}}** — [1-2 sentences; cite the interview quote that surfaced it]
2. **{{Finding 2}}** — _TODO_
3. **{{Finding 3}}** — _TODO_

---

## Theme clusters (affinity mapping)

*Patterns that emerged across multiple interviewees. Group quotes by theme; cluster size signals robustness.*

### Theme 1 — {{name}}

- Quote A — *"..."* (Interview X)
- Quote B — *"..."* (Interview Y)
- **Cluster size:** {{N}} out of {{N}} interviews
- **Interpretation:** _TODO_

### Theme 2 — _TODO_

---

## Per-hypothesis verdict

| Hypothesis | Verdict | Evidence | Confidence shift |
|---|---|---|---|
| {{H1}} | ☐ Confirmed ☐ Refuted ☐ Refined | Quote(s) + interview ref | Assumed → Tested |
| {{H2}} | _TODO_ | _TODO_ | _TODO_ |

---

## Per-artefact updates needed

### Personas

| Persona | Field | Old value | New value | Confidence shift |
|---|---|---|---|---|
| P-NN | {{Frustration #2}} | _Assumed: "X"_ | _Tested: "Y" — based on N corroborating quotes_ | Assumed → Tested |

### Business Model Canvas

| Block | Bullet | Old content | New content | Confidence shift |
|---|---|---|---|---|
| Customer Segments | CS-1 | _Assumed_ | _Tested — specific firmographic confirmed by 3 of 5 interviews_ | Assumed → Tested |

### Models

| Model | Input | Old value | New value | Reason |
|---|---|---|---|---|
| {{model slug}} | {{input}} | {{range}} | {{point estimate}} | {{evidence summary}} |

### Competitive landscape

| Competitor / claim | Change | Source | Confidence shift |
|---|---|---|---|
| Competitor X | Verified pricing $Y/month | Interview Z | Assumed → Tested |

---

## Confidence summary

| Status | Count before | Count after | Delta |
|---|---|---|---|
| Assumed | _TODO_ | _TODO_ | _TODO_ |
| Tested | _TODO_ | _TODO_ | _TODO_ |
| Validated | _TODO_ | _TODO_ | _TODO_ |

---

## Changelog

| Date | Change | Author |
|---|---|---|
| {{YYYY-MM-DD}} | Initial synthesis | _TODO_ |

---

---

<!-- RESEARCH PLAN TEMPLATE — copy below; replace placeholders -->

# Research Plan — {{topic}}

Scope of a research wave designed to unblock the following hypotheses
from upstream artefacts:

1. **{{Hypothesis 1}}** — currently `Assumed`; this wave aims for `Tested`
2. **{{Hypothesis 2}}** — _TODO_

> **Methodology:** [discovery-research kit-link methodology pointer](https://github.com/VictorHueni/homemade-claude-kit/tree/main/discovery-research/references/methodology-references.md)

---

## Sampling strategy

| Field | Plan |
|---|---|
| **Target N participants** | {{5-8 for first wave (NN/g saturation); 12-15 for variance}} |
| **Recruitment criteria** | [Role + firmographic + situation criteria] |
| **Recruitment channel** | [Warm intro / sales rep / LinkedIn / panel / etc.] |
| **Screener questions** | [3-5 questions to confirm fit] |
| **Incentive** | [$X / gift card / nothing — depends on B2B vs B2C] |

---

## Methods

| Method | Use case | Estimated coverage |
|---|---|---|
| Semi-structured interview | Primary — hypothesis testing | N interviews |
| Observation / contextual inquiry | Secondary — workflow validation | 1-2 sessions if possible |
| Survey | Tertiary — narrow quant validation | When you need >20 data points |
| Diary study | Rare — multi-day workflow capture | Skip unless explicitly needed |

---

## Ethics + consent

- **Recording policy:** {{with explicit consent / notes-only}}
- **Anonymisation:** participant role + org type only; no names in synthesis docs
- **Data retention:** notes kept for {{N}} months; transcripts deleted on completion
- **Withdrawal:** participant can withdraw at any point; their data removed
- **Compensation:** {{declare if any}}

---

## Timeline + budget

| Phase | Duration | Cost |
|---|---|---|
| Recruitment | {{2-4}} weeks | _TODO_ |
| Interviews | {{2-3}} weeks (1-2 per week) | _TODO_ |
| Synthesis | 1-2 weeks | — |
| **Total** | {{5-9}} weeks | _TODO_ |

---

## Success criteria

| Hypothesis | What "Tested" looks like | What would invalidate the hypothesis |
|---|---|---|
| {{H1}} | {{e.g., "3 of 5 interviewees independently confirm value X within ±20%"}} | {{e.g., "Wide spread without convergence; or systematic refutation"}} |
| {{H2}} | _TODO_ | _TODO_ |

**Stop criteria:** if saturation reached at N=5 (NN/g rule); or if hypothesis is decisively confirmed/refuted earlier.

---

## Changelog

| Date | Change | Author |
|---|---|---|
| {{YYYY-MM-DD}} | Plan drafted | _TODO_ |
