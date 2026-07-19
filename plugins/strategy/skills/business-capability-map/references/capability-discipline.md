# Capability Discipline — Internal Claude Guidance

This file is **not** copied into the project. It is internal guidance the
skill consults when applying the three discipline tests (noun /
tech-independence / anti-overlap), the capability-vs-others decision tree,
and the Cutter common-mistakes catalogue.

---

## The three discipline tests — run before declaring any capability complete

### 1. The noun test (TOGAF + Gonzalez)

A capability name must be a **noun phrase**. Verbs and action words indicate
a process or activity, not a capability.

| ✅ Capability (noun) | ❌ Process (verb) | Why |
|---|---|---|
| Customer Onboarding | Onboard Customers | Action word "onboard" |
| Risk Assessment | Assess Risk | Action word "assess" |
| Order Fulfilment | Fulfil Orders | Action word "fulfil" |
| Claim Adjudication | Adjudicate Claims | Action word "adjudicate" |
| Inventory Management | Manage Inventory | Action word "manage" |
| Demand Forecasting | Forecast Demand | Action word "forecast" |

**Naming formula (Cesar Gonzalez):** `Business Object + Noun`, where the noun
is typically one of: Management · Planning · Development · Support ·
Fulfilment · Assessment · Adjudication · Monitoring · Governance ·
Optimisation · Reconciliation · Registration · Forecasting · Onboarding.

**Edge case:** some legitimate capabilities use gerunds (verb-derived
nouns ending in -ing). "Onboarding", "Forecasting", "Monitoring" are nouns,
not verbs — the test passes. The trap is the imperative form ("Onboard").

### 2. The technology-independence test (TOGAF)

A capability name must NOT contain technology, vendor, system, tool, or
platform names. If the name would change when you swap an underlying tool,
it is a system or function — not a capability.

| ❌ System-named (not capability) | ✅ Capability |
|---|---|
| Salesforce Integration | Customer Relationship Management |
| SAP Finance | Financial Management |
| Tableau Reporting | Business Reporting |
| AWS Compute Provisioning | Compute Provisioning |
| Stripe Payment Processing | Payment Processing |

**Test:** if a vendor demos their product to the team and they decide to
switch, does the capability name need to change? If yes → system-named, fix it.

### 3. The anti-overlap test (Cutter)

No two capabilities in the map should overlap. Each capability appears
**once and only once**. If two capabilities seem to cover the same
territory, you must either merge them or split them differently — never
leave both standing.

**Detection cues:**
- Two capabilities have outcomes that read the same way → overlap.
- A reader cannot decide which capability to file a new outcome under → overlap.
- Two capabilities both claim the same business object as primary → overlap.

**Resolution:**
- **Merge:** if the two are genuinely the same, combine into one with a
  broader definition.
- **Resplit:** if the two cover related but distinct outcomes, redraw the
  boundary at the right level (e.g., split by lifecycle stage, by business
  object, or by outcome type).
- **Hoist:** if the overlap is because both children of one L0 do the same
  thing, the overlap may indicate a shared capability that belongs at a
  different L0 (e.g., a "Platform" L0).

---

## Capability vs Process vs Function vs Org Unit — decision tree

When triaging whether a candidate belongs in the BC Map, work through these
questions in order:

```
Is this candidate a sequence of activities with a defined start and end?
├── Yes → PROCESS — belongs in process docs, not the BC Map
│         (e.g., "Onboard a new customer", "Process a claim")
└── No
    │
    Is this candidate a group of people / a reporting line?
    ├── Yes → ORG UNIT — belongs in an organisational chart, not the BC Map
    │         (e.g., "Customer Success Team", "Risk Department")
    │         Cutter mistake #5: an LOB is not a capability.
    └── No
        │
        Is this candidate a grouping of activities by skill / expertise?
        ├── Yes → BUSINESS FUNCTION — belongs in an org-design artefact
        │         (e.g., "Engineering", "Sales", "Operations" as functional areas)
        │         Note: TOGAF and BABOK use "function" subtly differently;
        │         the safe rule is "if it sounds like a department, it's not a capability."
        └── No — likely a CAPABILITY. Proceed to:
            - Apply the noun test (name must be a noun phrase)
            - Apply the technology-independence test
            - Apply the anti-overlap test
            - Check it fits the L0 + L1 sizing heuristics
```

### Worked examples

| Candidate | Verdict | Why |
|---|---|---|
| "Customer Onboarding" | Capability | Noun phrase; business object + noun; tech-independent |
| "Onboard Customers" | Process | Verb-led; describes a sequence |
| "Customer Success Team" | Org unit | Group of people |
| "Operations" | Business function | Grouping by skill/expertise |
| "Salesforce" | System | A tool, not an ability |
| "Risk Management" | Capability | Noun phrase; tech-independent |
| "Quarterly Risk Review" | Process | A scheduled activity sequence |
| "Risk Department" | Org unit | A reporting line |
| "Compliance Monitoring" | Capability | Noun phrase; ongoing ability |
| "Submit Compliance Report" | Process | Single bounded activity |

---

## The five Cutter common mistakes — anti-pattern catalogue

### Mistake 1: Confusing capabilities with processes

**Symptom:** the map is full of verb-led names ("Order new product",
"Reject incomplete claim", "Update customer record").

**Fix:** rename every capability as a noun phrase using the Business Object
+ Noun formula. Move the verb-led activities into process docs.

### Mistake 2: Using technical terminology

**Symptom:** capability names include systems, platforms, vendors, or
acronyms ("SAP Master Data", "AWS Cost Management", "ERP Integration").

**Fix:** strip the technology and rename around the business outcome.
"ERP Integration" → "Enterprise Data Integration" or, more often, drop
entirely (integration is a feature, not a capability).

### Mistake 3: Creating multiple maps for one business

**Symptom:** different stakeholders maintain their own capability maps —
sales has one, ops has one, finance has one. No aggregate view exists.

**Fix:** force the conversation. There is one business, therefore one BC
Map. If stakeholders demand different views, they are looking at different
*lenses* on the same map (e.g., heat-map by maturity, heat-map by sourcing) —
not different maps.

### Mistake 4: Allowing redundancy in the map

**Symptom:** "Customer Data Management" appears under both "Sales" L0 and
"Operations" L0 because both touch customer data.

**Fix:** hoist the shared capability to a Platform / Shared-Services L0,
or pick one of the two parents and have the other link/reference.

### Mistake 5: Confusing capabilities with organisational units

**Symptom:** L0 items are department names ("Marketing", "Engineering",
"Finance").

**Fix:** rename around what those departments *do*, not what they're called.
"Marketing" → "Brand Management" + "Demand Generation" + "Market Insight"
(these are capabilities; the org unit is incidental).

---

## L0 axis decision — internal heuristics

When the user is unsure which L0 axis to pick, work through these
questions:

1. **Does the business sell distinct products / services that each have
   their own customer journeys?**
   → L0 = **Product / Service family**.
   *(Risk: cross-product capability bleed. Mitigate by adding a "Platform"
   L0 for shared capabilities.)*

2. **Does the business primarily think in terms of customer journeys
   delivered to one customer segment?**
   → L0 = **Value stream**.

3. **Is the business a single product / service, or a portfolio so diverse
   that the only commonality is corporate ownership?**
   → L0 = **Capability domain / theme** (TOGAF-classic). Domains might be:
   Customer-facing · Operations · Compliance · Finance · People · Technology.

4. **Is the business a true conglomerate / holdings group with structurally
   different LOBs (e.g., banking + insurance + asset management)?**
   → L0 = **Line of business**.

5. **Does the business serve segments with structurally different
   capability needs (e.g., B2C consumer + B2B enterprise + B2G regulator)?**
   → L0 = **Customer segment**.

6. **Default when unsure** → **Capability domain / theme**. It is the
   most defensible neutral choice; the user can change later.

**Anti-pattern:** picking L0 = org unit ("Marketing", "Engineering"). This
is Cutter mistake #5. If the user proposes org-unit L0, push back and ask
what those departments *do*.

---

## Sizing decisions — heuristics for L1 explosion

If you find yourself generating more than 12 L1 capabilities under a single
L0, something is wrong. Possible diagnoses:

| Diagnosis | Fix |
|---|---|
| The L0 actually contains two L0s collapsed into one | Split L0 into two |
| Several of the L1s are really L2s nested incorrectly | Hoist some L1s into a wrapper L1, demote the rest to L2 |
| The scope of the whole map is too big for one map | Reconsider scope; split into multiple BC Maps by sub-scope |
| You are mixing capability granularity (some L1s are large, some are small) | Re-level so all L1s have comparable granularity |

If you find yourself generating L2 sub-capabilities everywhere:
- You are over-decomposing. L2 is the exception, not the rule.
- Probable cause: leaking into feature-grain detail that belongs in the
  FBS, not the BC Map.
- Action: stop, move the feature-grain content to the FBS (or flag the
  need for one), and keep the BC Map at L1.

---

## Strategic importance — how to assess honestly

Strategic Importance is a real exercise, not a column to populate quickly.
The three levels:

- **Differentiator** — this is where the business wins or loses. Loss of
  this capability = loss of competitive position. Typically 3–6 capabilities
  in a healthy BC Map.
- **Necessary** — required to operate, but no one wins on this capability.
  Most capabilities (60–70%) fall here.
- **Commodity** — could be outsourced, templated, or replaced by an
  off-the-shelf solution without strategic loss. Typically 20–30%.

**Common mistakes:**
- Marking everything as Differentiator → you have not made a real choice.
- Marking everything as Necessary → you have a healthy map but have not
  asked the strategic question.
- Marking by enthusiasm rather than evidence → ask "what evidence would
  change my mind?" If none, the rating is not strategic.

**Rationale field is mandatory.** A Strategic Importance rating without a
one-sentence rationale is fragile and will not survive the next strategy
review.

---

## Quality checks before saving a capability

Run this checklist mentally — don't print it into the file:

- [ ] Name is a noun phrase (noun test).
- [ ] Name contains no technology / vendor / system (tech-independence test).
- [ ] No other capability in the map overlaps in scope (anti-overlap test).
- [ ] Capability is not actually a process (verb-led) / function (skill grouping) / org unit (people grouping).
- [ ] Definition is 1–2 sentences, outcome-oriented, business language.
- [ ] Business object is a single noun.
- [ ] Strategic importance has a one-line rationale.
- [ ] Outcomes are 2–4 bullets, outcome-oriented (not activities).
- [ ] Boundaries are explicit (anti-overlap discipline visible to the reader).
- [ ] Soft-links populated only when target artefact exists.
- [ ] No feature names, no functionality names, no code paths leaked in.

---

## When the user pushes back on the discipline

Some users want a quick capability map without the apparatus. Acceptable
fallbacks:

- Strategic Importance can stay `_TODO_` initially (it's a real exercise).
- Maturity can be omitted entirely (politically loaded).
- Soft-links can stay empty if the target artefacts don't exist.

Non-negotiable:
- The noun test. A verb-led capability name is a process and breaks the BC
  Map's purpose.
- The technology-independence test. A tool-named capability is a system.
- The anti-overlap test. Duplicate capabilities silently create duplicate
  downstream artefacts.

If the user pushes to violate any of these, push back once with the source
(TOGAF / Cutter). If they insist, ship the doc with the violation flagged
in the §Open Items / Changelog so a future reviewer sees the compromise.
(`Open Items` follows the canonical schema in
the `metamodel` skill's `references/open-items-governance.md`.)
