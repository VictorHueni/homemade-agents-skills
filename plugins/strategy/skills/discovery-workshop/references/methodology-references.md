# Business Workshop — Methodology References

This document records the canonical frameworks used to design and
maintain workshop artefacts (single workshops, multi-session series,
post-workshop synthesis). The artefact is a synthesis of six sources —
each contributes a specific lens.

The skill produces three artefact types: single-workshop guides,
multi-session series, and workshop synthesis docs.

---

## 1. Sam Kaner — *Facilitator's Guide to Participatory Decision-Making* (3rd ed., 2014)

**Used for:** the **Diamond of Participation** — the canonical group-process
map that every workshop session moves through, and the techniques to
navigate each stage.

**Source:** Sam Kaner, Lenny Lind, Catherine Toldi, Sarah Fisk, & Duane
Berger, *Facilitator's Guide to Participatory Decision-Making* (3rd ed.,
Jossey-Bass, 2014). Reference: [Goodreads listing](https://www.goodreads.com/book/show/927064.Facilitator_s_Guide_to_Participatory_Decision_Making).
Open-access summary: [Chris Corrigan — The Diamond of Participation](https://www.chriscorrigan.com/parkinglot/the-diamond-of-participation/).

### Key contributions

- **The Diamond of Participation (1996):** every workshop moves through
  four stages — **Divergent → Groan zone → Convergent → Closure**.
  Skipping the groan zone yields shallow decisions; refusing to converge
  yields no decisions.
- **Participatory decision-making principles:** full participation +
  mutual understanding + inclusive solutions + shared responsibility.
- **Techniques per stage:**
  - **Divergent:** brainstorming, mind-mapping, 1-2-4-All, silent generation
  - **Groan:** wicked questions, fishbowl, tensions surfacing
  - **Convergent:** dot-voting, decision matrices, disagree-and-commit
  - **Closure:** what-so-what-now-what, 15% solutions, commitments

### Discipline encoded in the skill

- Workshop guide template has a "Diamond stage" column on every exercise
  — facilitator can see the balance at a glance.
- Quality check at save: ≥1 convergent exercise per session (workshops
  without convergence don't decide).
- Disagreement-handling techniques (dot vote, disagree-and-commit) are
  pulled into the §Facilitation tips section.

---

## 2. Lipmanowicz & McCandless — *Liberating Structures* (2014)

**Used for:** the catalog of 33 microstructures that replace
conventional meeting formats (presentation / managed discussion / status
report / open discussion / brainstorm). Every workshop exercise should
name a Liberating Structure (or equivalent canonical method) — "let's
brainstorm" is too vague.

**Source:** Henri Lipmanowicz & Keith McCandless, *The Surprising Power
of Liberating Structures* (Liberating Structures Press, 2014). Online
canonical reference:
[liberatingstructures.com](https://www.liberatingstructures.com/).
Practitioner catalog:
[SessionLab Liberating Structures](https://www.sessionlab.com/library/liberating-structures).

### Key contributions

- **33 microstructures** — small replaceable methods that can be
  combined into any meeting agenda. Each comes with a precise structure
  (time, materials, group size, flow).
- **The five elements** every Liberating Structure specifies:
  1. **Structuring invitation** — the prompt
  2. **How space is arranged** — physical setup
  3. **How participation is distributed** — who speaks when
  4. **How groups are configured** — pairs, fours, all
  5. **Sequence of steps and time allocation** — minute-by-minute
- **The 1-2-4-All pattern** is the most-used: 1 min silent reflection,
  2 min pair discussion, 4 min foursome, then all-share. Engages
  everyone; surfaces minority views.
- **Common picks for business architecture work:**
  - **1-2-4-All** — replaces brainstorm
  - **Wicked Questions** — surfaces paradoxes
  - **TRIZ** — "make it worse" to identify counterproductive behaviours
  - **Min Specs** — minimum we must do / not do
  - **What, So What, Now What** — structured reflection / commitment

### Discipline encoded in the skill

- Every exercise in the workshop agenda names a Liberating Structure (or
  alternative canonical method).
- `references/liberating-structures.md` catalogs the 33 with when-to-use
  guidance.
- Default Liberating Structure recommendations per workshop type
  (BMC workshop, persona workshop, etc.) appear in the skill.

---

## 3. Strategyzer — Workshop Kits for BMC + VPC

**Used for:** the canvas-specific workshop facilitation patterns —
filling a Business Model Canvas or Value Proposition Canvas as a group,
with discipline on bullet-per-sticky, clustering, voting, and confidence
ratings.

**Source:** Strategyzer (Osterwalder's company) — workshop resources and
canvas-specific facilitation guides:
- [Strategyzer Library](https://www.strategyzer.com/library)
- [Business Model Canvas](https://www.strategyzer.com/library/the-business-model-canvas)
- [Value Proposition Canvas](https://www.strategyzer.com/library/the-value-proposition-canvas)

### Key contributions

- **Canvas-specific format:** print A1/A0; one sticky-note per bullet;
  cluster within blocks; vote on most-uncertain bullets.
- **"The canvas is a conversation tool, not a poster."** Workshops are
  the canonical use case.
- **Per-block facilitation prompts** — questions designed to surface
  the right content per block (CS prompts about firmographics + trigger;
  VP prompts about value-not-features; KR prompts about Differentiator
  vs Commodity).
- **Post-workshop validation list** — flag which bullets are most
  uncertain; these become the input to `discovery-research` interview
  scripts.

### Discipline encoded in the skill

- BMC / VPC workshops in the skill produce explicit "post-workshop
  validation backlog" — feeds `discovery-research` mode 2.
- One-sticky-per-bullet discipline (avoid sticky-note clusters
  representing multi-paragraph ideas).
- Confidence ratings (Assumed / Tested / Validated) carried into the
  filled canvas, consistent with `business-model-canvas` skill.

---

## 4. Jake Knapp — *Sprint* (2016): The 5-Day Design Sprint

**Used for:** the **multi-day rapid-prototyping workshop format** for
product discovery — when a single-day workshop isn't enough and a full
research wave is too slow.

**Source:** Jake Knapp, John Zeratsky, & Braden Kowitz, *Sprint: How to
Solve Big Problems and Test New Ideas in Just Five Days* (Simon &
Schuster, 2016). Originally developed at Google Ventures.

### Key contributions

- **5-day cadence:**
  - **Monday — Map** — interview experts, map the user journey, pick a long-term goal + sprint question
  - **Tuesday — Sketch** — solo divergent ideation; everyone produces 8 sketches
  - **Wednesday — Decide** — convergent: heatmap, straw poll, supervote → storyboard
  - **Thursday — Prototype** — build a realistic façade
  - **Friday — Test** — 5 user interviews; record reactions
- **Decider role** — one person has tiebreaking authority. Prevents
  consensus paralysis on Wednesday.
- **The supervote** — final convergence mechanism.
- **5 user interviews on Friday** — NN/g saturation rule applied to
  prototype testing.

### Discipline encoded in the skill

- Mode 3 (workshop series) supports the Design Sprint as a special-case
  5-session series with the canonical Monday-Friday cadence.
- Decider-role pattern surfaced in §Facilitation tips when stakes are
  high.
- Friday's user testing leverages `discovery-research` mode 2 interview
  scripts.

---

## 5. Priya Parker — *The Art of Gathering* (2018)

**Used for:** the intentional-gathering principles — why people gather,
how to define purpose, how to set hosting boundaries, how to make
gatherings memorable.

**Source:** Priya Parker, *The Art of Gathering: How We Meet and Why It
Matters* (Riverhead Books, 2018). Reference:
[priyaparker.com](https://www.priyaparker.com/).

### Key contributions

- **Purpose drives everything.** A specific purpose ("decide whether to
  pivot the Customer Segment") beats a vague purpose ("align on
  strategy").
- **Specificity is generosity.** Specific purpose → specific exercises
  → specific outcomes. Vague gatherings waste everyone's time.
- **The 8-1 rule:** spend 8× more time planning the gathering than
  hosting it. A 4h workshop deserves 30h of planning.
- **Closure principles.** Don't just end; **close**. Acknowledge what
  happened; commit to what's next; reflect on what shifted.

### Discipline encoded in the skill

- Frontmatter requires a one-sentence outcome statement (forces
  Parker-style purpose specificity).
- Closure exercise (What-So-What-Now-What from Liberating Structures)
  is mandatory at the end of every session.
- §Post-workshop actions table forces commitment articulation.

---

## 6. IAF — International Association of Facilitators (Core Competencies)

**Used for:** the professional-facilitator framing — what makes
facilitation a skill vs winging it.

**Source:** International Association of Facilitators (IAF),
[Core Facilitator Competencies](https://www.iaf-world.org/site/professional/core-competencies).

### Key contributions

- **6 competency areas:**
  1. Create collaborative client relationships
  2. Plan appropriate group processes
  3. Create + sustain a participatory environment
  4. Guide group to appropriate + useful outcomes
  5. Build + maintain professional knowledge
  6. Model positive professional attitude
- **The facilitator is neutral on content; expert on process.** Avoid
  injecting opinions; trust the group's collective intelligence.

### Discipline encoded in the skill

- §Facilitation tips includes neutrality reminders.
- Single-facilitator group-size cap at ≤12; beyond that requires co-facilitator (IAF guidance).

---

## 7. (Related but out of scope) — Open Space Technology, World Café, Theory U

- **Open Space Technology** (Harrison Owen, 1985) — self-organising
  agenda for large mixed groups. Covered as a Liberating Structure
  variant.
- **World Café** (Brown & Isaacs, 2005) — also covered as Liberating
  Structure.
- **Theory U** (Otto Scharmer, 2007) — deeper systemic change
  methodology. Out of scope; useful when stakes are exceptionally high
  (multi-organisation alignment).

---

## Summary — what each framework contributes

| Framework | Contributes |
|---|---|
| Sam Kaner | Diamond of Participation (Divergent → Groan → Convergent); decision-making techniques |
| Liberating Structures | 33 microstructures replacing conventional meeting formats |
| Strategyzer | Canvas-specific facilitation (BMC + VPC + Empathy Map); one-sticky-per-bullet discipline |
| Jake Knapp — Sprint | 5-day Design Sprint cadence; Decider role; supervote |
| Priya Parker | Purpose-driven gatherings; specificity-is-generosity; closure discipline |
| IAF | Professional facilitator competencies; neutrality on content; group-size sizing |
| Out-of-scope (Open Space / Theory U) | Awareness; possible v2 extensions |

The template is not "Kaner alone" or "Liberating Structures alone" —
it is the canonical synthesis adapted for BIZBOK Business Architecture
reality-checking. The practitioner-derived series-capable + superpower-team
+ pre-prep + deliverables-summary patterns sit on top.
