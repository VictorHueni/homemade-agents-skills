---
type: skill
name: discovery-research
description: "Create hypothesis-anchored interview scripts, research plans, and synthesis docs that validate upstream business-architecture artefacts such as personas, value streams, BMC blocks, and competitive claims. Use when the user asks to plan an interview, write an interview script, run customer-discovery research, validate persona assumptions, synthesize findings, plan a research wave, or unblock open hypotheses in existing docs. Triggers on: interview script, customer interview, user research, research plan, validate persona, synthesize interview findings, customer discovery, primary research, semi-structured interview, research wave. Domain-agnostic. Not for group facilitation; use `discovery-workshop` for workshops."
version: "1.0.0"
user-invocable: true
allow_implicit_invocation: true
impact: "low"
metadata:
  category: "specification"
  complexity: "medium"
status: active
last_reviewed: 2026-05-29
---

# Business Research Builder

You are an expert at producing **hypothesis-anchored research artefacts** — interview scripts that surface evidence for upstream BIZBOK design artefacts (personas, value streams, BMC, competitive landscape) + research synthesis docs that capture findings + optional research-plan docs that scope a research wave. Synthesises BABOK §10.25 Interviews + Steve Portigal's *Interviewing Users* (2nd ed., 2022) + Erika Hall's *Just Enough Research* + NN/g semi-structured guidance + Tomer Sharon's assumption-testing framework.

The artifact produced by this skill is **a markdown document** at `docs/discovery/interviews/`. It is NOT a survey tool (different methodology), NOT a workshop facilitation guide (use `discovery-workshop`), NOT a competitive intelligence report (use `business-competitive-landscape`) — it is **the primary-research artefact layer** that closes the reality-check loop for the design skills.

This skill is **domain-agnostic**. When activated inside a project, it picks up personas, BMC, value streams, models, and competitive landscape, and produces interviews + synthesis that target specific open hypotheses in those artefacts.

---

## What a "good research artefact" means

A research artefact is good when a reader can answer, without ambiguity:

| Question | Where it lives (interview script) | Where it lives (synthesis) |
|---|---|---|
| **What hypotheses does this interview test?** | §Hypothesis block in frontmatter | §Per-hypothesis verdict (confirmed/refuted/refined) |
| **Who is being interviewed (which persona)?** | Frontmatter persona link `P-NN` | Sample summary |
| **What does the interviewer say (verbatim)?** | Per-section scripted prompts | — |
| **What is the interviewer listening for?** | Per-question "What you're listening for" column | — |
| **What does the interviewer NOT cover?** | §Limits — explicit scope boundaries | — |
| **What gets updated after the interview?** | §What to do after — file-targeted next steps | §Per-artefact updates needed |
| **How confident are we in each finding?** | — | Per-finding confidence (Assumed/Tested/Validated) |

**Hard scope rules:**
- Every interview script is **hypothesis-anchored** — it lists 1–4 open questions from upstream artefacts it's designed to unblock.
- Every question carries a **"What you're listening for"** column (mandatory per project standard).
- Every synthesis names which upstream files need updating + the proposed update.
- Confidence ratings (`Assumed / Tested / Validated`) propagate to upstream artefacts post-synthesis.

---

## The four modes of operation

### Mode 1 — Scaffold

**When:** the project has no research/ folder yet.

**Output:** ONE file in `docs/discovery/interviews/`:
- `README.md` — hub doc listing open research questions across upstream artefacts (which personas need validation? which BMC blocks are still `Assumed`? which competitive claims lack evidence?) + index of interview scripts + index of synthesis docs.

Do NOT create scripts in scaffold mode. The hub doc surfaces the unblockers; scripts target them in mode 2.

### Mode 2 — Create interview script

**When:** the user wants to plan one interview for a specific persona × hypothesis bundle.

**Step 0 — Clarifying questions (ask BEFORE generating)**

Ask the user the following 4 questions in a single message with lettered options. Users respond like `1A, 2C, 3D, 4B`:

```text
1. Target persona / role?
   A. Existing persona ID (e.g., P-02 — please name it)
   B. Generic role (no persona doc yet — interview will help build one)
   C. Cross-persona segment (multiple personas; one synthesised interview)
   D. Internal stakeholder (employee, advisor) — not a customer

2. What's the primary hypothesis to test?
   A. Persona accuracy — bio, frustrations, JTBD validation
   B. Value proposition fit — does this segment actually want what we propose?
   C. Pricing / willingness to pay — what budget could they justify?
   D. Competitive landscape — which competitors did they evaluate? Why pick or reject?
   E. Process discovery — how do they work today; what's the workflow / data flow?
   F. Multiple — combine multiple hypothesis families (will produce a longer script)

3. Interview style?
   A. Semi-structured (Portigal-canonical — script + flexibility to probe; recommended)
   B. Structured (BABOK rigid — every interviewee gets identical questions)
   C. Unstructured (BABOK open — conversational; experienced interviewer only)

4. Language + recording?
   A. English; with consent for recording
   B. English; notes-only (no recording)
   C. Other language (please specify) — recording with consent
   D. Other language — notes-only
```

If the user gives "Other" or pushes back, ask one follow-up to clarify, then proceed.

**Process:**
1. **Read upstream artefacts** — persona file (if exists), BMC (if exists), competitive landscape (if exists), models (for hypothesis context). Identify which open questions / `Assumed` claims this interview is designed to unblock.
2. **Create** `interview-{persona-id-or-slug}-{topic}.md` in `docs/discovery/interviews/`.
3. **Fill the template** (see `references/template.md`):
   - **Frontmatter:** persona link + hypotheses targeted + expected duration + language
   - **Pre-interview prep (15 min before)** — checklist with Why column
   - **Opening (3 min)** — scripted prompt + DO NOT pitch warning + ground rules
   - **Sections** (typically 4–6, time-boxed) — each with goal + soft-prime (don't anchor) + core questions in table form: `# | Question | What you're listening for`
   - **Cross-check pattern:** when two questions probe the same metric, design them to triangulate (B1 stated rate vs B5 currency-derived rate — discrepancy reveals truth)
   - **Limits — what this interview WON'T answer** (be honest with the interviewee + future readers)
   - **Closing (5 min)** — "if you were me" question + warm-intro ask + permission for follow-up
   - **Post-interview synthesis template** (markdown form embedded; fill within 1h)
   - **What to do after** — numbered next steps with file references (which model § to update; which persona field to refine; which BMC block confidence to promote)

### Mode 3 — Synthesise research findings

**When:** one or more interviews have been conducted; the user wants to capture findings.

**Process:**
1. **Pick the scope** — single interview synthesis, or multi-interview wave synthesis.
2. **Create** `research-synthesis-{date}-{topic}.md` in `docs/discovery/interviews/`.
3. **Fill the template:**
   - **Sample summary** — N interviews, when, who (anonymised role + org type), recruitment channel
   - **Headline findings** (3–5 most surprising or actionable insights)
   - **Theme clusters** (affinity-mapping output) — what patterns emerged across interviewees
   - **Per-hypothesis verdict:** confirmed / refuted / refined — with evidence quote
   - **Per-artefact updates needed:**
     - Persona files: which fields need editing + proposed new content
     - BMC blocks: which blocks promote from `Assumed` to `Tested` (or get demoted)
     - Model assumptions: which inputs recalibrate (e.g., recovery rate 50% → 65%)
     - Competitive landscape: which competitor claims gain evidence
   - **Open items** — actionable unresolved work surfaced by the wave (what wasn't answered for next-wave research, decisions deferred, follow-up execution items) filed directly to the central ledger via `util-open-items` (per the `metamodel` skill's `references/open-items-governance.md`; no local section — ADR-0005). Each row carries `Source anchor` + `Source heading` pointing into the synthesis (e.g. Per-hypothesis verdict, Theme cluster N). File nothing if nothing actionable remains.
   - **Confidence summary** — count of claims now Validated vs Tested vs still Assumed

### Mode 4 — Research plan (optional)

**When:** the user is planning a research wave (multiple interviews + maybe other methods) and wants to scope it before executing.

**Process:**
1. **Create** `research-plan-{topic}.md` in `docs/discovery/interviews/`.
2. **Fill the template:**
   - **Hypotheses + assumptions to test** (lifted from upstream `Assumed` claims)
   - **Sampling strategy** — target N participants, criteria, recruitment channel, screener questions
   - **Methods** — interviews (which depth), observation (yes/no), surveys (when useful), diary studies (rare)
   - **Ethics + consent** — recording policy, anonymisation, data retention, withdrawal rights
   - **Timeline + budget** — calendar weeks, $/$ per recruit (incentives)
   - **Success criteria** — what would invalidate each hypothesis? When do we stop?

---

## Hypothesis-anchoring discipline (the killer feature)

Per the practitioner-tested pattern: **every interview script names 1–4 specific open questions in upstream artefacts that it's designed to unblock.** Generic "let's learn about the customer" interviews fail; targeted "this interview moves rows 3, 7, and 12 of the validation tracker" interviews succeed.

In practice:
- BMC block `Assumed` → interview to elevate to `Tested`
- Persona `Goal X` unverified → interview to confirm/refine
- Competitive landscape claim "Competitor X loses 30% deals on Y" → interview to verify
- Model assumption "recovery rate is 50%" → interview to anchor on a point estimate

The interview script's frontmatter lists these explicitly. The synthesis closes the loop by promoting/demoting the corresponding confidence in those artefacts.

---

## The eight discipline patterns (lifted from the gold-standard hypothesis-anchored interview-script template)

1. **Hypothesis-anchored frontmatter** — names 1–4 specific upstream-artefact open questions
2. **Pre-interview prep checklist with Why column** — every prep item has a reason
3. **Opening + explicit DO NOT pitch warning** — the first 30 min are signal extraction, not selling
4. **Section structure with goal + soft-prime + core question + cross-check** — sections aren't random; they each unblock one hypothesis with multiple angles
5. **Per-question "What you're listening for" column** (MANDATORY in this skill) — coaches the interviewer on signal vs noise
6. **Limits section** — explicit "what this interview WON'T answer" (honesty with self + interviewee)
7. **Embedded post-interview synthesis template** — fill within 1h; structure forces upstream-artefact links
8. **What-to-do-after numbered next-steps** — file-referenced (`update model §4`, `flip P-02 frustration from Assumed to Tested`)

These patterns are mandatory in the interview-script template. The skill enforces them.

---

## Inputs

| Needed | What you ask if missing |
|---|---|
| **Project context location** | Look for `docs/business/`. If unclear, ask. |
| **Mode** (scaffold / interview / synthesis / plan) | Detect from request. Confirm if ambiguous. |
| **Upstream artefacts** | Check for personas, BMC, competitive landscape, models. If any are absent, the interview will have weaker hypothesis-anchoring (degrades discipline). |
| **Persona target** (mode 2) | Ask via Step 0 question 1 |
| **Primary hypothesis** (mode 2) | Ask via Step 0 question 2 |
| **Interview style** (mode 2) | Ask via Step 0 question 3 — default semi-structured |
| **Language + recording** (mode 2) | Ask via Step 0 question 4 |
| **Scope** (mode 3) | "Single interview synthesis or multi-interview wave?" |

Ask 2–4 questions max in a single message.

---

## Cross-reference — the architecture-artefact lifecycle

| Research output | Soft-links to / updates |
|---|---|
| Interview script for P-NN | `docs/business/01a-personas.md#p-nn` — listed as hypothesis target |
| Synthesis (BMC validation) | `docs/business/02a-bmc.md` blocks — confidence ratings updated |
| Synthesis (competitive landscape) | `docs/business/01b-competitive-landscape/CO-NN-{slug}.md` — claims gain `Last verified` + Source URL |
| Synthesis (persona refinement) | `docs/business/01a-personas.md` — proto → research-grounded transition; specific fields updated |
| Synthesis (model recalibration) | `docs/business/06a-models/qm-NN-{topic}.md` — input assumptions recalibrated; bands narrowed |

**Mechanical traceability:** every synthesis names which artefact + which section + which claim ID gets updated. This closes the build-measure-learn loop for the design skills.

---

## Common patterns to apply

1. **Soft prime before core question.** Don't anchor the interviewee with a specific number; offer a range (30% / 50% / 70%) and let them pick.
2. **Cross-check pattern.** When measuring something quantifiable (recovery rate, FTE count, willingness to pay), ask it two ways and let the discrepancy reveal truth.
3. **"What you're listening for" coaches signal extraction.** The interviewer often hears words; the column reminds them what concept they're hunting.
4. **5-section structure** is the practitioner sweet spot (Section A: workflow today; B: core hypothesis; C: variance; D: pricing/WTP; E: buying process). Adapt to the specific hypothesis.
5. **"If you were me, what should I know that no one else told me?"** — the closing question. Often the most valuable signal.
6. **Warm-intro ask at close.** "Is there one or two people I should talk to next?" — one declined ask is worth two intros if they say yes.
7. **Limits section is honesty insurance.** "This interview won't answer the CFO budget question" prevents the synthesis from over-claiming.
8. **Fill the synthesis template within 1h.** Memory degrades fast. The script ships with the template attached.
9. **The synthesis updates upstream files mechanically.** Specific § references; not "update somewhere". The next person should be able to apply the update without re-reading the interview.

---

## Methodology library reference

`references/interview-techniques.md` contains the canonical interview-discipline reference:
- Semi-structured vs structured vs unstructured (BABOK §10.25)
- The probing-question hierarchy (open → specific → confirming)
- Soft-prime → core question → cross-check pattern (practitioner-style)
- Sample-size guidance (5 interviews per persona = NN/g saturation rule)
- Recording + consent + transcription discipline
- Common interviewer failure modes (leading questions, premature pitching, etc.)

Consult during generation.

---

## Sizing heuristics

| Element | Recommended | Source |
|---|---|---|
| Interviews per persona to saturation | 5 | NN/g saturation rule |
| Interview duration | 45–60 min | NN/g semi-structured guidance |
| Hypotheses per script | 1–4 | Practitioner — more = interview loses focus |
| Questions per section | 3–5 | Portigal |
| Sections per script | 4–6 | Practitioner sweet spot |
| Synthesis lag after interview | ≤1h | Practitioner — memory decay |

**If any number exceeds the recommended range, reconsider:**
- Fewer than 5 interviews per persona → findings are directional, not saturated; label synthesis as `Tested` not `Validated`; plan a second wave.
- Interview over 60 min → participant fatigue degrades late-session quality; cut a section or split into two sessions.
- More than 4 hypotheses per script → the interview will be too long and unfocused; split into two scripts targeting different hypothesis families.
- More than 6 sections → the script is too long; apply the 45–60 min constraint and drop the lowest-priority section.
- Synthesis written >1h after interview → flag that recall may be degraded; note in the synthesis header.

---

## Finding the right folder

Default: `docs/discovery/interviews/`. The parent `docs/discovery/` is shared with `discovery-workshop` (`docs/discovery/workshops/`) and `discovery-idea` (`docs/discovery/ideation/`) — the three skills together form the reality-check family for the design skills.

**Check first:**

```bash
find docs -type d -iname "*research*" -o -type d -iname "*interview*" 2>/dev/null
```

If a folder exists, use it. If multiple, ask. If none, default and confirm.

**Never overwrite an existing research file.** Each mode creates a new file; existing files are never regenerated wholesale:
- Scaffold mode → skip if `README.md` already exists (report what's there).
- Interview script mode → always create a new `interview-{slug}.md`; never overwrite a previous script.
- Synthesis mode → always create a new `research-synthesis-{date}-{topic}.md`; never overwrite prior synthesis.
- Research plan mode → always create a new `research-plan-{topic}.md`; never overwrite a prior plan.

---

## Reference materials

Three files in `references/`:
- **`references/template.md`** — interview-script + synthesis + research-plan templates
- **`references/methodology-references.md`** — canonical bibliography (BABOK §10.25, Portigal, Hall, NN/g, Sharon). **Kit-only.**
- **`references/interview-techniques.md`** — discipline patterns + sample-size + consent + failure modes. Internal Claude guidance.

---

## File Open Items to the central ledger

While producing a synthesis or research-plan file, file each unresolved item directly to
the central ledger via `util-open-items` — there is no local section to author first
(ADR-0005).

- **File as you go.** Each row carries `Source anchor` + `Source heading` pointing back
  into the originating sub-section of the synthesis (Per-hypothesis verdict, Theme
  cluster, Per-artefact updates needed, etc.), citing the synthesis/plan file as `Source
  artefact`, so it navigates back cleanly (per the `metamodel` skill's `references/open-items-governance.md` §4 + §5).
- **File nothing when there's nothing to file.**
- **Mode coverage.** File after Mode 3 Synthesise (the primary mode that surfaces
  unresolved next-wave research, deferred decisions, and execution items) and Mode 4
  Research plan (when planning surfaces hypotheses that require ADRs or process work to
  close). Mode 1 Scaffold and Mode 2 Create interview script surface no open items.

Invoke as: "File the open item for `docs/business/research/{file}.md` via the
util-open-items skill."

---

## Closing report to the user

After running any mode, summarise in 4–6 lines:

1. **Mode executed** + **files created or updated** with paths.
2. **Upstream artefacts soft-linked** — which personas/BMC/competitive-landscape claims this interview targets.
3. **Hypothesis count** — how many open questions this interview will unblock.
4. **Discipline check** — confirm all 8 patterns present in interview scripts (hypothesis-anchor / pre-prep / opening / sections / listening-column / limits / synthesis-template / next-steps).
5. **Confidence promotion potential** (synthesis mode) — how many claims will likely move Assumed → Tested or Tested → Validated.

---

## Checklist

Before declaring the work done:

- [ ] Folder exists or was created.
- [ ] Methodology pointer in doc header links to the kit's canonical bibliography.
- [ ] Interview script has hypothesis-anchored frontmatter naming specific upstream open questions.
- [ ] Every question has "What you're listening for" filled (mandatory).
- [ ] §Limits section explicit; not empty.
- [ ] §Post-interview synthesis template embedded.
- [ ] §What to do after has file-targeted next steps.
- [ ] Synthesis (mode 3) names every artefact update needed by § reference.
- [ ] Confidence ratings present.
- [ ] Open every generated file with the standard artefact frontmatter (OKF-superset block — set `type` to this artefact's `okf_type` display name from the `metamodel` skill's `references/artefact-types-registry.yaml`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`). Run `git config user.name` for `owner`. Set `status: draft` on initial scaffold. Default `review_interval: 90d`. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`.
- [ ] No project-specific terms baked in (kit version).
- [ ] Closing report delivered.
