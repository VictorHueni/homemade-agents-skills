<!-- doc-version: 1.0 | created: {{YYYY-MM-DD}} -->

# {{product}} — Personas

Personas are fictional yet research-grounded archetypes that represent the
real user groups who interact with {{product}}. They exist to create a shared,
precise vocabulary for "the user" across product, engineering, and business
analysis work, and to ground feature prioritisation in concrete human needs
rather than assumptions.

> **Methodology:** built using the canonical synthesis of [BABOK §10.43 + Cooper goal-directed design + Pruitt & Adlin lifecycle + Lene Nielsen 10-step + NNG + Lean UX + JTBD](https://github.com/VictorHueni/homemade-claude-kit/tree/main/business-persona/references/methodology-references.md). The full bibliography and framework synthesis live with the skill that generated this doc — single source of truth across every project.

**Rule of inclusion (NNG):** every field in a persona must be able to answer
*"would removing this detail change a design or prioritisation decision?"* If
not, omit it.

**Cooper's hard rule:** every product or design surface has **exactly one
primary persona**. Tiers (priority) and persona types (design role) are
orthogonal — see the backlog tables below.

---

## Persona Template

> Copy this block for each new persona. Replace all `[…]` placeholders.
> Delete italicised guidance lines before publishing.

---

### P-NN · [First name Last name] — [5-word role tagline]

**Persona type:** [Primary | Secondary | Supplemental | Served | Customer | Negative]
**Tier:** [1 | 2 | 3]
**Lifecycle status:** [Proto-persona (assumption) | Active (research-grounded) | Retired]

> *"[One sentence in the persona's own words capturing their primary
> frustration, goal, or attitude toward the domain. This is the most memorable
> part of the persona — make it specific and realistic, not generic. Write it
> last, after the rest of the persona is filled.]"*

#### Snapshot

*Include only dimensions that visibly affect product decisions (NNG: would
removing this change a design or prioritisation decision?). Skip irrelevant
ones rather than padding.*

| Dimension | Value |
|---|---|
| **Role / Title** | [Job title and organisational context] |
| **Organisation type** | [e.g. {{org_type_examples}}] |
| **Domain experience** | [e.g. "X years in [domain], [frequency] [product] user"] |
| **Usage context** | [voluntary / job-required] |
| **Frequency of {{product}} use** | [e.g. daily / weekly / per-case] |
| *(optional)* **Age range** | [Use a range, never a single age. Include only if it affects design.] |
| *(optional)* **Primary language** | [Include only if the product is multilingual.] |
| *(optional)* **Primary device** | [Include only if cross-device UX matters.] |

#### Bio

*2–3 sentences. Ground the persona in their day-to-day work relationship with
the domain — not hobbies or personal life. Describe how they currently
encounter the problem {{product}} solves.*

[Two to three sentences describing who this person is professionally, what
their typical workday looks like in relation to the domain, and what brings
them to {{product}} or its problem domain.]

#### Goals (as Jobs)

*NNG-endorsed Jobs-to-be-Done framing — same content, sharper question.
Format each goal as situation-motivation-outcome. Fall back to bulleted goals
if the JTBD shape doesn't fit a particular outcome.*

- **When** [situation / trigger], **I want** [motivation], **so I can** [outcome].
- **When** […], **I want** […], **so I can** […].
- **When** […], **I want** […], **so I can** […].

#### Scenarios

*1–2 short narratives (3–5 sentences each) of the persona using {{product}}
or encountering the problem. Scenarios are the bridge between persona and
design (Cooper + Nielsen). Show a triggering event → the persona's reasoning
→ the action they take → the outcome they care about. Avoid generic walkthroughs.*

**Scenario 1: [Short title — the situation]**

[3–5 sentence narrative.]

**Scenario 2: [Short title — the situation]**

[3–5 sentence narrative.]

#### Frustrations

*Pain points and blockers they experience today — before or without {{product}}.
Ground in the domain, not generic UX complaints.*

- [Primary frustration, domain-specific]
- [Secondary frustration]
- [Optional tertiary frustration]

#### Key Tasks in {{product}}

*Concrete actions this persona performs in the product. Maps directly to
feature requirements / FBS functionalities and helps prioritise the backlog.*

- [Task 1]
- [Task 2]
- [Task 3]

#### System Needs

*Quality attributes that matter most for this persona, with persona-specific
rationale. Choose from: speed, accuracy, traceability, explainability,
auditability, low cognitive load, bulk operation support, API access, offline
capability, or others.*

- **[Quality 1]:** [why it matters for this persona specifically]
- **[Quality 2]:** [why it matters]
- **[Quality 3]:** [why it matters]

#### Stakeholder Profile (BABOK §10.43)

*Dimensions for business-analysis planning — stakeholder engagement,
collaboration strategy, RACI assignment. See the BABOK §10.43 entry in the [skill's methodology reference](https://github.com/VictorHueni/homemade-claude-kit/tree/main/business-persona/references/methodology-references.md).*

| BABOK dimension | Assessment |
|---|---|
| **Authority in domain of change** | [high / medium / low — with one-line justification] |
| **Interest in the initiative** | [high / medium / low — with one-line justification] |
| **Attitude toward {{product}}** | [champion / supportive / neutral / sceptical / resistant] |
| **Decision-making authority** | [What decisions they can / can't make in the project context] |
| **RACI on initiative** | [R / A / C / I — for which activities] |

*Engagement strategy* (derived from BABOK Figure 10.43.1 Stakeholder Matrix —
Influence × Impact):

[One sentence describing how to engage this persona, e.g., "High Influence /
High Impact — engage regularly, work closely to ensure agreement and support."]

#### Research Grounding

*State explicitly what evidence backs this persona. A proto-persona
(assumption-based) is valid per Lean UX, but must carry an explicit `Next
review` date ≤ 90 days from `Created`. NNG recommends re-validating
research-grounded personas yearly or when research reveals drift.*

| Field | Value |
|---|---|
| **Evidence type** | [qualitative interview / observation / workshop / survey / contextual inquiry / diary study / **proto-persona (assumption)**] |
| **Sample** | [e.g. "3 interviews with [role] at 2 organisations" — quantify, never "lots of feedback"] |
| **Key sources** | [initials or roles of people interviewed, or "internal team assumption"] |
| **Created** | [YYYY-MM-DD] |
| **Last validated** | [YYYY-MM-DD or "not yet validated"] |
| **Next review** | [YYYY-MM-DD — **mandatory** for proto-personas, ≤90 days from Created] |

---

## Persona Backlog

Identified user groups across {{product}}. Each row maps to one future
persona to be built using the template above. **Cooper persona type** and
**tier** are orthogonal — type defines design role, tier defines priority.

### Tier 1 — Primary (core revenue, highest interaction depth)

| ID | Proposed name | Role / domain | Persona type | Primary product/surface | Key job outcome |
|---|---|---|---|---|---|
| P-01 | _TODO_ | _TODO_ | _Primary_ | _TODO_ | _TODO_ |

### Tier 2 — Secondary (important workflow, not direct revenue driver)

| ID | Proposed name | Role / domain | Persona type | Primary product/surface | Key job outcome |
|---|---|---|---|---|---|
| _TODO_ | _TODO_ | _TODO_ | _Secondary_ | _TODO_ | _TODO_ |

### Tier 3 — Tertiary (future products or adjacent use cases)

| ID | Proposed name | Role / domain | Persona type | Primary product/surface | Key job outcome |
|---|---|---|---|---|---|
| _TODO_ | _TODO_ | _TODO_ | _Supplemental / Served / Customer_ | _TODO_ | _TODO_ |

### Negative personas (explicitly NOT designed for)

*Per Cooper, negative personas surface user groups the team intentionally
deprioritises. Documenting them prevents bending the product to satisfy edge
cases at the cost of the primary.*

| ID | Proposed name | Role / domain | Why deprioritised |
|---|---|---|---|
| _TODO_ | _TODO_ | _TODO_ | _TODO_ |

### Out of scope

*User groups not modelled because they fall outside the product's scope
entirely (not the same as negative — these are people the product is not
trying to serve at all).*

- **[Group]** — [reason out of scope, with reference to product-scope doc]

---

## Personas

*No personas have been filled yet. Use the template above to add each persona
as a new H3 section below this heading.*

<!-- Add personas here -->

---

## Changelog

| Date | Change | Author |
|---|---|---|
| {{YYYY-MM-DD}} | Initial scaffold | _TODO_ |
