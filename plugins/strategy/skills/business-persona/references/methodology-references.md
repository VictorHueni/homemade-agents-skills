# Personas — Methodology References

This document records the canonical frameworks used to design and maintain the
[Personas](01a-personas.md). The persona artifact is a synthesis of seven sources
rather than a single school — each framework contributes a specific lens.

---

## 1. BABOK — Stakeholder List, Map, or Personas (§10.43)

**Used for:** stakeholder identification, the Influence × Impact matrix
(engagement strategy), the RACI assignment, and the formal "personas are
business-analysis artefacts" framing.

**Source:** *A Guide to the Business Analysis Body of Knowledge® (BABOK®
Guide), v3*, International Institute of Business Analysis (IIBA), Chapter 10
— Techniques, §10.43 "Stakeholder List, Map, or Personas", p. 344–347.

### Key contributions to the template

- **Stakeholder List (§10.43.1)** — exhaustive enumeration before pruning.
  Used in backlog mode to ensure no important stakeholder group is missed.
- **Stakeholder Matrix (§10.43.2, Figure 10.43.1)** — Influence × Impact
  quadrants drive the per-persona engagement strategy:

| Influence \ Impact | High | Low |
|---|---|---|
| **High** | Key players — engage regularly; work closely | Keep satisfied; may feel anxious about lack of control |
| **Low** | Supporters — show interest in their needs | Monitor; keep informed via general communications |

- **RACI Matrix (§10.43.3)** — Responsible / Accountable / Consulted /
  Informed. Used in the per-persona Stakeholder Profile section.
- **Personas definition (§10.43.4)** — "fictional character or archetype that
  exemplifies the way a typical user interacts with a product… written in
  narrative form and focused on providing insight into the goals of the group."

### Strengths and limitations

- **Strength:** identifies who must be engaged in elicitation, informs
  collaboration / communication planning.
- **Limitation:** BABOK acknowledges stakeholder analysis is iterative — a
  stakeholder's position can shift due to organisational, environmental, or
  scope changes. Re-review personas regularly.

---

## 2. Cooper — Goal-Directed Design and the Persona-Type Taxonomy

**Used for:** persona-type field (Primary / Secondary / Supplemental / Served
/ Customer / Negative), the hard rule that every product has exactly one
primary persona, and scenarios as the bridge between persona and design.

**Source:** Alan Cooper, *The Inmates Are Running the Asylum* (1998), and
Cooper, Reimann & Cronin, *About Face: The Essentials of Interaction Design*
(3rd ed., 2007). Canonical online summary:
[Alan Cooper and the Goal Directed Design Process — Hugh Dubberly](https://www.dubberly.com/articles/alan-cooper-and-the-goal-directed-design-process.html).

### The six persona types

| Type | Definition | Design implication |
|---|---|---|
| **Primary** | The persona whose goals can be achieved *only* by designing specifically for them. | Maximum **one per product/surface**. THE design target. |
| **Secondary** | Mostly satisfied by the primary's interface, with minor accommodations. | Add accommodations only if they don't compromise the primary. |
| **Supplemental** | Occasionally uses the product; satisfied by primary + secondary design. | No special design effort; just don't actively exclude them. |
| **Served** | Affected by the product but does not use it directly (e.g., a patient when the product is used by a clinician). | Track their outcomes; they validate that the product produces the right results. |
| **Customer** | Buys / authorises the product but does not use it. | Address their concerns in sales / onboarding materials, not the product UX. |
| **Negative** | Explicitly NOT designed for. | Surface to prevent the team from bending to satisfy edge cases. |

### Why scenarios

Cooper's argument: a persona without scenarios is a description; a persona
with scenarios is a design tool. Scenarios force the team to imagine the
persona using the product in a specific situation, which surfaces design
questions a description alone hides.

---

## 3. Pruitt & Adlin — The Persona Lifecycle

**Used for:** the lifecycle-status field (Proto-persona / Active / Retired),
the discipline that personas have phases and need maintenance rather than
being one-shot artefacts.

**Source:** John Pruitt & Tamara Adlin, *The Persona Lifecycle: Keeping People
in Mind throughout Product Design* (2006), Morgan Kaufmann. Reference summary:
[Persona Lifecycle — ScienceDirect Topics](https://www.sciencedirect.com/topics/computer-science/persona-lifecycle).

### The five phases

1. **Family planning** — what problems are we solving, what data sources exist.
2. **Conception and gestation** — organise assumptions, turn data into information into personas.
3. **Birth and maturation** — introduce personas to the organisation.
4. **Adulthood** — use personas in design, development, evaluation, release.
5. **Lifetime achievement and retirement** — measure success of the persona effort, retire or rebuild for the next cycle.

### Mapping to the template

- "Conception and gestation" produces a **proto-persona** in our template.
- "Birth and maturation" + "adulthood" correspond to **active** lifecycle status.
- "Retirement" maps to **retired** — kept in the doc with changelog entry, not deleted.

---

## 4. Lene Nielsen — Personas: User-Focused Design (10-step process)

**Used for:** the engaging-persona style guidance (narrative, scenarios,
emotional grounding) and the 10-step process that frames data collection
through active use.

**Source:** Lene Nielsen, *Personas — User Focused Design* (Springer, Human–
Computer Interaction Series, 2nd ed. 2019).
[Springer reference](https://link.springer.com/book/10.1007/978-1-4471-4084-9).

### Nielsen's 10 steps (compressed)

1. Find users (research).
2. Build hypotheses (assumption synthesis).
3. Verify (validate against data).
4. Find patterns (cluster users into archetypes).
5. Construct personas (write the descriptions).
6. Define situations (scenarios).
7. Obtain acceptance (socialise with the team).
8. Disseminate knowledge (publish + share).
9. Create scenarios (extend with use moments).
10. Ongoing adjustment (lifecycle maintenance).

### The "engaging" persona

Nielsen contrasts the "engaging" perspective (narrative-rich, emotionally
grounded, scenario-driven) with the "goal-directed" perspective (Cooper-style,
behaviour-focused). The two are complementary; the template borrows from
both — goal-directed structure with engaging narrative quality in §Bio,
§Quote, and §Scenarios.

---

## 5. Nielsen Norman Group — Practical Persona Discipline

**Used for:** the design-decision-relevance rule of inclusion, the
recommended-fields baseline (name, photo, tagline, context, goals, quote),
and the JTBD integration guidance.

**Source:** Kate Kaplan / Aurora Harley / Page Laubheimer (NNG).
[Personas — Make the User Shine](https://www.nngroup.com/articles/persona/).
JTBD integration: [Personas vs. Jobs-to-Be-Done](https://www.nngroup.com/articles/personas-jobs-be-done/).

### Key contributions

- **Rule of inclusion:** *"don't add details that are irrelevant to the
  design."* Every field must pass the design-decision-relevance test.
- **JTBD integration:** *"instead of simply listing the persona's goals,
  consider formatting this information as jobs-to-be-done."* The template's
  §Goals section uses JTBD framing by default.
- **Definition:** *"a persona is a fictional, yet realistic, description of
  a typical or target user of the product."*

### NNG warning we encode in the template

NNG explicitly states *"personas must be based on user research."* The template
softens this to allow proto-personas (per Lean UX) but **only** if labelled
honestly and carrying an explicit `Next review` date.

---

## 6. Lean UX — Proto-Personas

**Used for:** the proto-persona discipline (assumptions are valid as a
starting point if labelled and scheduled for validation), the `Next review`
≤90-day rule.

**Source:** Jeff Gothelf & Josh Seiden, *Lean UX: Designing Great Products
with Agile Teams* (3rd ed., O'Reilly 2021).
[Using Proto-Personas for Executive Alignment](https://jeffgothelf.com/blog/using-personas-for-executive-alignment/).

### Key contributions

- **Order of operations:** assumptions → research, not research → assumptions.
- **Proto-persona definition:** persona built from team assumptions, with no
  field research, used to align stakeholders and jumpstart validation.
- **Iterative refinement:** proto-personas update as research uncovers
  conflicting characteristics.

### Discipline encoded in the template

A persona labelled `Evidence type: proto-persona (assumption)` **must** have
`Next review` ≤ 90 days from `Created`. On that date, the persona is either
upgraded to research-grounded (one or more validation methods completed) or
retired. Unmaintained proto-personas decay into folklore — the template
prevents this by making decay visible.

---

## 7. Jobs-to-be-Done — Goal Framing

**Used for:** the situation-motivation-outcome format of §Goals (NNG-endorsed
synthesis with personas).

**Sources:**
- Clayton Christensen, *The Innovator's Solution* (2003) — the foundational JTBD argument.
- Anthony Ulwick, *Jobs to be Done: Theory to Practice* (2016) — outcome-driven innovation.
- Alan Klement, *When Coffee and Kale Compete* (2016) — situation-led JTBD framing.
- [NNG: Personas vs. JTBD](https://www.nngroup.com/articles/personas-jobs-be-done/) — official synthesis position.

### Why JTBD-formatted goals

The "When X, I want Y, so I can Z" shape forces three things a flat goal
list hides:
- **When** — the situational trigger (without which the job doesn't fire).
- **I want** — the motivation (what the persona is trying to make happen).
- **So I can** — the outcome they actually care about (often different from the immediate action).

A goal written as "Confirm whether a drug is reimbursable" hides the trigger
and the outcome. As a Job — "When I'm prescribing during a 5-minute encounter,
I want to confirm coverage, so I can avoid a callback from the pharmacy and
keep the consultation moving" — the design implications surface immediately
(speed, in-context, mobile-friendly, robust to interruption).

### When JTBD framing doesn't fit

Some goals are not situational ("understand the product's full capability"
is an exploration goal, not a job). For those, bulleted goals are acceptable
— the template allows both, with JTBD as the recommended default.

---

## Summary — what each framework contributes

| Framework | Contributes |
|---|---|
| BABOK §10.43 | Stakeholder profile, Influence×Impact engagement, RACI, exhaustive listing |
| Cooper | Persona-type taxonomy (6 types), one-primary-per-product rule, scenarios |
| Pruitt & Adlin | Lifecycle status field, persona-as-living-artifact discipline |
| Lene Nielsen | Engaging narrative quality, 10-step process, scenario discipline |
| NNG | Design-decision-relevance rule, recommended fields baseline, JTBD integration guidance |
| Lean UX | Proto-persona discipline, `Next review` ≤90-day rule |
| JTBD | Situation-motivation-outcome goal framing |

The template is not "BABOK personas" or "Cooper personas" — it is the
canonical synthesis. Every section maps back to at least one of the seven
sources. When two frameworks conflict (e.g., NNG's "must be based on
research" vs Lean UX's proto-persona allowance), the template encodes the
conflict explicitly rather than hiding it: proto-personas are allowed
**only with an honest evidence label and a re-validation deadline**.
