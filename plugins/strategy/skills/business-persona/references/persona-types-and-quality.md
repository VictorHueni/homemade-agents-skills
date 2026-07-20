# Persona Types and Quality Checks — Internal Claude Guidance

This file is **not** copied into the project. It is internal guidance the
skill consults when deciding which persona type to assign, applying NNG
quality checks, and enforcing proto-persona discipline.

---

## Cooper's six persona types — decision tree

When triaging a candidate from the backlog into the right persona type, work
through these questions in order:

```
Does this person use the product directly?
├── No
│   ├── Are they affected by the product's outputs (e.g., recipient of a clinician's decision)?
│   │   ├── Yes → SERVED persona
│   │   └── No → check the next question
│   ├── Do they decide whether the product is purchased / adopted?
│   │   └── Yes → CUSTOMER persona
│   └── Otherwise → out of scope (not a persona)
│
└── Yes — they use the product
    ├── Are we INTENTIONALLY designing AGAINST their needs?
    │   └── Yes → NEGATIVE persona (document the deprioritisation)
    ├── Can their goals be met ONLY by designing specifically for them?
    │   └── Yes → PRIMARY persona (max one per product/surface)
    ├── Are their goals mostly met by the primary design, with minor accommodations?
    │   └── Yes → SECONDARY persona
    └── Do they use the product occasionally, satisfied by primary+secondary design?
        └── Yes → SUPPLEMENTAL persona
```

### Hard rules

1. **Exactly one primary per product surface.** If the team wants two primaries, they need two products. The discipline forces a real design conversation rather than a compromise.
2. **Negative personas are deliberate.** A user the product happens to underserve is not a negative persona; a negative persona is one the team has explicitly chosen to deprioritise.
3. **Served personas are not "users" but they validate outcomes.** The product is successful when its served personas get the right outcomes, even if they never see the UI.

### Examples (abstract — adapt to project)

| Scenario | Type | Why |
|---|---|---|
| Specialist clinician using a CDS tool to make a treatment decision | Primary | Tool's purpose is met only by serving them well |
| Department admin who runs reports on the same tool monthly | Supplemental | Uses it, but primary's design serves them adequately |
| Patient who receives the clinician's treatment decision | Served | Affected, doesn't use, outcome matters |
| Hospital procurement officer who signs the contract | Customer | Buys, doesn't use, addressed in sales not UX |
| Junior trainee the team has decided NOT to optimise for (use is supervised) | Negative | Intentional deprioritisation; flag to prevent scope creep |
| External regulator who audits the tool annually | Supplemental or Customer | Depends on whether they use the UI (auditor view) or just review outputs |

---

## NNG quality checks — the "would removing this change a decision?" filter

Apply this filter to every field in a persona before declaring it complete.

### Snapshot fields — keep / drop decisions

| Field | Keep when… | Drop when… |
|---|---|---|
| Role / Title | Always | Never |
| Organisation type | Always | Never |
| Age range | The product has age-sensitive UX (accessibility, regulated demographics, generational tech expectations) | Internal tools where age doesn't affect anything |
| Primary language | Product is multilingual; localisation decisions depend on it | Single-language product |
| Primary device | Cross-device UX matters (responsive, mobile-first, desktop-only) | Single-platform product or device is constrained by job context |
| Domain experience | Always — affects help-text density, defaults, error verbosity | Never |
| Usage context (voluntary / required) | Always — affects motivation, forgiveness toward errors | Never |
| Frequency of use | Always — affects discoverability, onboarding investment, retention metrics | Never |

### Bio anti-patterns

- ❌ Hobbies, family, personal life. ("Maria loves hiking on weekends.")
- ❌ Generic professional descriptions. ("She is a hard-working professional.")
- ❌ Demographics dressed as personality. ("As a millennial, Maria…")
- ✅ Day-to-day work relationship with the domain / problem.
- ✅ Concrete frequency and context. ("Maria sees ~25 patients/day; reviews coverage for ~15.")

### Goal anti-patterns

- ❌ Feature requests dressed as goals. ("Maria wants a dashboard.")
- ❌ Solutions instead of jobs. ("Maria wants a dropdown menu.")
- ❌ Goals without context. ("Maria wants to be efficient.")
- ✅ Outcomes in the persona's domain language.
- ✅ JTBD framing where it fits: "When X, I want Y, so I can Z."

### Frustration anti-patterns

- ❌ Generic UX complaints. ("It's slow.", "The UI is confusing.")
- ❌ Frustrations that apply to every persona. ("She wishes things were easier.")
- ✅ Domain-specific blockers tied to current workflows.
- ✅ Frustrations that point to design opportunities without prescribing the design.

### Scenario anti-patterns

- ❌ Generic walkthrough of the product's features. ("Maria opens the app, clicks Search, types…")
- ❌ Scenarios that work for any persona.
- ✅ Specific triggering event, persona's reasoning, action taken, outcome they care about.
- ✅ Edge cases or interrupted flows where the persona's context matters.

### Quote anti-patterns

- ❌ Vague aspirations. ("I want a great experience.")
- ❌ Marketing-speak. ("This product will transform my workflow.")
- ❌ Generic dissatisfaction. ("Things are hard right now.")
- ✅ Specific, realistic, in the persona's voice.
- ✅ Captures a primary frustration, goal, or attitude in one sentence.

### Stakeholder Profile anti-patterns

- ❌ "Influence: high" with no justification.
- ❌ Engagement strategy that's a generic line ("communicate regularly").
- ✅ One-line justification for each Influence / Interest rating.
- ✅ Engagement strategy derived from the specific quadrant (e.g., "Low Influence / High Impact: keep informed via newsletter; surface their feedback to the steering committee").

---

## Proto-persona discipline (Lean UX)

Proto-personas are valid **only** when:

1. **`Evidence type` is honestly labelled** as `"proto-persona (assumption)"`. Never disguise an assumption-based persona as "based on internal team knowledge" — that's the trap that lets folklore harden into perceived fact.

2. **`Next review` ≤ 90 days from `Created`.** Lean UX rejects long-lived assumption-based personas. If the team can't validate in 90 days, the persona should not be in active use.

3. **Validation path is explicit.** The skill should record (in §Research Grounding or a TODO note) *how* the proto-persona will be validated:
   - Method: interview / survey / observation / contextual inquiry / customer-feedback review.
   - Sample target: number of participants + how to recruit.
   - Success criterion: what would invalidate the persona.

4. **On the `Next review` date, the persona transitions to one of three states:**
   - **Upgraded to active** — validation completed, evidence type changed to research-grounded, persona body updated with findings.
   - **Iterated** — partial validation showed drift; persona body updated, new `Next review` set ≤ 90 days.
   - **Retired** — validation showed the persona doesn't represent a real user group; mark `Lifecycle status: Retired` with changelog entry. Don't delete; retain for institutional memory.

### Anti-pattern: assumption laundering

The most common proto-persona failure is "assumption laundering" — labelling
team intuition as "internal knowledge" or "observed by stakeholders" to avoid
the proto-persona label. Push back when generating: ask "is there a specific
research artefact (interview transcript, survey results, observation notes)
that backs this?" If the answer is no, label as proto-persona honestly.

---

## Quality checks before saving a persona

Run this checklist (mentally — don't print it into the file):

- [ ] Persona type assigned and matches the Cooper decision tree.
- [ ] If primary: confirmed only one primary per product/surface.
- [ ] Snapshot fields all pass design-decision-relevance test.
- [ ] Bio is 2–3 sentences, domain-grounded, no hobbies / generic descriptors.
- [ ] Goals: JTBD framing where it fits, with situation + motivation + outcome.
- [ ] Scenarios: 1–2 specific narratives, not generic walkthroughs.
- [ ] Frustrations: domain-specific, not UX complaints.
- [ ] Key tasks: concrete product actions, not abstract verbs.
- [ ] System needs: quality attributes with persona-specific rationale.
- [ ] Stakeholder profile: Influence + Interest with justifications, attitude assessed, engagement strategy specific.
- [ ] Research grounding: evidence type honest, sample quantified, `Next review` set (mandatory for proto-personas).
- [ ] Quote: specific, realistic, in the persona's voice.
- [ ] No project-specific names baked into anything reusable in the methodology doc.

---

## When the user pushes back on the discipline

Some users want a quick persona without the apparatus. The default response is
to ship a proto-persona with a short `Next review` — that's the canonical
Lean UX path. Don't strip out the Stakeholder Profile or Research Grounding
sections; they're cheap to leave as `_TODO_` and force the question to be
answered eventually.

If the user explicitly says "I don't need a stakeholder profile, just give me
the persona description" — comply, but leave the section as `_TODO_` in the
output rather than deleting it. The template's value is structural; partial
fills are fine, missing sections silently is not.
