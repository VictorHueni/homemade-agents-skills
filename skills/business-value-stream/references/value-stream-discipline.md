# Value Stream Discipline — Internal Claude Guidance

This file is **not** copied into the project. It is internal guidance the
skill consults when applying the 7 anti-patterns, the EA-vs-Lean stance,
naming rules, and per-stage quality checks.

---

## The seven anti-patterns — run on every stream

### 1. Internal-lifecycle naming (BIZBOK #1 scoping mistake)

**Symptom:** stream names like "Hire-to-Retire", "Order-to-Cash", "Concept-
to-Cash", "Quote-to-Order", "Lead-to-Cash".

**Why it's wrong:** these names frame the stream around internal phases
("we hire, then we develop, then we retire") rather than around the value
the stakeholder receives. They make the stream brittle to organisational
change and obscure who the value is for.

**Fix:** rename around the final value achieved + business object.

| ❌ Internal-lifecycle | ✅ Value-named |
|---|---|
| Hire-to-Retire | Onboard Human Resource · Develop Talent · Retire Human Resource |
| Order-to-Cash | Acquire Product · Settle Invoice |
| Concept-to-Cash | Develop Product · Launch Product |
| Quote-to-Order | Issue Quote · Acquire Product |

If a candidate stream is genuinely about a full end-to-end lifecycle (one
person walks through the whole thing), split it — that's almost always
multiple value streams squashed together.

### 2. Confusing value stream with business process

**Symptom:** the candidate is a verb-led activity sequence with no
triggering stakeholder receiving a value proposition.

**Detection cues:**
- Name starts with a verb in imperative form ("Process the claim", "Run
  payroll").
- No clear "who gets what at the end".
- Concerns sequence of activities rather than value milestones.

**Fix:** push to the `business-process` skill. Value streams are
strategic; processes are operational.

### 3. Confusing value stream with customer journey

**Symptom:** the candidate captures emotions, touchpoints, channels, pain
moments, or "moments of truth" experienced by a customer.

**Why it's wrong:** journeys capture **actual** experience; value streams
describe the **idealised** value-delivery model. They're complementary
artefacts but structurally different.

**Detection cues:**
- The candidate has columns for emotion / channel / touchpoint.
- The candidate orders content by chronological experience moments rather
  than by value milestones.
- The candidate asks "how does the customer feel here?" rather than "what
  value is produced here?"

**Fix:** redirect to a journey-mapping tool or skill. Don't try to encode
emotion / channel data in this template; it conflates two artefacts.

### 4. Defining capabilities inline

**Symptom:** a stage's body contains capability definitions ("the
Authentication capability provides…") instead of soft-linking to the BC
map by ID.

**Why it's wrong:** the BC map is the canonical source of truth for
capability definitions. Inlining duplicates content and creates drift.

**Fix:** replace with soft-link by capability ID (`C-N.M`). If the BC map
doesn't exist yet, leave the link as `_TODO_` and surface the gap; don't
write the capability definition here.

### 5. Internal triggering stakeholder

**Symptom:** the triggering stakeholder is a system, a process, an
internal scheduler, or "the team."

**Why it's wrong:** a value stream's triggering stakeholder must be a
persona — typically external (the customer, the user, the citizen) but
occasionally internal (the operator, the admin) when the stream serves
them as the recipient of value.

**Detection cues:**
- Triggering stakeholder is "the system" or "a scheduled job".
- Triggering stakeholder is a department name ("Finance", "Operations").
- The "value proposition" is internal efficiency rather than value
  delivered to a person.

**Fix:** if the trigger is a system, the candidate is a process, not a
value stream. If the trigger is a department, find the persona inside that
department who actually receives the value.

### 6. Over-scoping — one stream, multiple value propositions

**Symptom:** the value proposition contains "AND" or describes two
unrelated outcomes ("Onboard customer AND set up billing AND collect first
payment").

**Why it's wrong:** a value stream has one value proposition (BIZBOK). If
the candidate carries multiple, it's actually multiple streams squashed
together — they'll have different stages, different stakeholders, and
different optimisation profiles.

**Fix:** split into multiple streams. They can share early stages if the
work is genuinely shared, but each stream has its own value proposition.

### 7. Under-staging or over-staging

| Symptom | Diagnosis | Fix |
|---|---|---|
| Fewer than 4 stages | Probably a process, not a strategic stream | Push to process-analyst skill |
| More than 10 stages | Over-decomposing or scope too broad | Merge stages or split stream |
| Stages that all look like activities | Confused with process | Rename stages as value milestones |
| One stage dominates (90% of the stream's work) | Stage granularity is wrong | Re-balance: either split the big stage or merge the small ones |

---

## The EA-vs-Lean-VSM stance — when the user pushes for Lean concepts

Some users will ask for value-stream content that is genuinely Lean VSM,
not EA. The skill should detect this and respond.

**Lean VSM requests sound like:**
- "Add cycle times to each stage"
- "Mark value-add vs non-value-add steps"
- "What's the takt time for this stream?"
- "Show me the queue between stages"
- "Where's the waste in this flow?"

**Response template:**
> *"Those are Lean VSM concerns — cycle time, waste, value-add classification.
> This skill produces EA-flavoured value streams (TOGAF + BIZBOK), which
> are strategic, not operational. If you want operational analysis with
> cycle times and waste identification, that's process-doc territory —
> consider extending the relevant process doc with timing data, or use a
> Lean VSM tool. The value stream stays at the strategic layer."*

**Don't refuse to engage.** Offer the redirection clearly. If the user
insists, you can add a `Cycle time (typical)` field to a specific stage as
a courtesy — but warn that you're crossing into process territory and the
data will go stale unless owned by the operations team.

---

## L0 / catalogue decisions — internal heuristics

### Stream identification approach

When asked to identify candidate streams from project context, work through:

1. **For each Tier-1 persona, what end-to-end value does the product deliver
   to them?** Each persona × value pair is a candidate stream.
2. **For each Tier-2/3 persona, is there a distinct value flow, or does it
   piggy-back on a Tier-1 stream?** Piggy-backers can be supplemental
   participants; only model their own stream if the value proposition is
   distinct.
3. **For each major product offering, what value does the product produce?**
   This is a complementary identification axis — start with personas, but
   cross-check against products to catch streams personas didn't surface.
4. **For regulated / cross-organisation flows, who else is a triggering
   stakeholder?** Regulators, oversight bodies, and partners can trigger
   streams too.

### Stream count sanity check

After identification:

| Count | Diagnosis |
|---|---|
| 0–2 streams | Almost certainly under-identified. Re-interview project context. |
| 3–10 streams | Healthy for a product scope. |
| 11–20 streams | Reasonable for a complex product or small enterprise. |
| 20–25 streams | Standard for an enterprise (BIZBOK heuristic). |
| 25+ streams | Scope too broad OR you're modelling processes as streams. Re-scope. |

### When to anchor on "scope" rather than "stream"

For very large enterprises, the catalogue may need scoping by domain
("Customer-facing streams", "Internal-operations streams", "Regulatory-
compliance streams"). Add an L0 grouping on top of VS-N IDs if the
catalogue exceeds ~25 streams. Otherwise, the flat catalogue is fine.

---

## Stage-naming rules (BIZBOK + TOGAF)

A stage's name describes the **value milestone**, not the activity
sequence. The Litmus test: can a reader say what's "true" at the end of
the stage, in terms the triggering stakeholder cares about?

| ✅ Stage (value milestone) | ❌ Activity (process material) |
|---|---|
| Validate Eligibility | Run eligibility-check script |
| Acquire Approval | Submit form to approver |
| Settle Payment | Process payment transaction |
| Confirm Receipt | Send confirmation email |
| Onboard Account | Create user record + set up billing |

**Naming heuristics:**
- Short verb-led phrases work ("Validate", "Acquire", "Settle", "Confirm").
- Noun phrases work ("Eligibility Validation", "Payment Settlement").
- Avoid technology / system names ("Run SAP transaction X" is process detail).
- Avoid org-unit names ("Finance reviews" → "Reviewed by Finance" → "Approval").

---

## Capability-consumption per stage

Each stage consumes 1–4 capabilities typically. Heuristic for "how many
capabilities per stage":

| Count | Diagnosis |
|---|---|
| 0 | Stage doesn't consume anything → not a real stage; merge with neighbour |
| 1–4 | Healthy |
| 5+ | Stage is too coarse, OR you're confusing capability with functionality (e.g., listing every system involved); re-check BC map IDs |

**Capabilities are shared across streams.** If a capability appears in one
stream, it can appear in many — that's a feature, not duplication. Don't
try to "give each stream its own capability set"; that violates BIZBOK and
breaks the BC map's anti-overlap discipline.

---

## Pain index — how to assess honestly

The pain-point index is a transformation-prioritisation field. Use the
scale honestly:

- **Low** — stage works well; no significant complaints; not a candidate for transformation investment.
- **Medium** — known frictions but not critical; transformation candidate if budget allows.
- **High** — material pain affecting throughput, customer satisfaction, or cost; transformation candidate now.
- **Critical** — stage is broken; transformation is urgent; failing the stage materially threatens the value proposition.

**Anti-patterns:**
- Marking everything `High` → no prioritisation signal; reset.
- Marking by feeling, not evidence → ask "what's the data?" If none, mark `_TODO_` until evidence is available.
- Avoiding `Critical` → the field exists precisely to surface these. Use it when warranted.

**One-line rationale is mandatory.** A pain rating without a rationale
("High because customer says so") is fragile and won't survive scrutiny.

---

## Quality checks before saving a value stream

Run this mentally — don't print into the file:

- [ ] Stream name describes the final value achieved (not internal lifecycle).
- [ ] Exactly one value proposition (no "AND").
- [ ] Triggering stakeholder is a persona ID (or honest `_TODO_`).
- [ ] 4–10 stages (no fewer, no more).
- [ ] Each stage name is a value milestone, not an activity.
- [ ] Each stage has all six fields (participating stakeholders, entrance, exit, value items, capabilities, processes) or honest `_TODO_`.
- [ ] Capabilities are soft-linked, never inlined.
- [ ] Pain index uses the 4-level scale with one-line rationale.
- [ ] No Lean VSM concepts (cycle time, waste, takt) snuck in.
- [ ] No customer journey concepts (emotions, channels, touchpoints) snuck in.
- [ ] None of the 7 anti-patterns survived.

---

## When the user pushes back on the discipline

Acceptable fallbacks:
- Pain index can stay `_TODO_` (it's an evidence-based exercise).
- Operationalised-by-processes can stay `_TODO_` (depends on process docs existing).
- Participating stakeholders can list role names if persona IDs don't yet exist (with `_TODO_` flag).

Non-negotiable:
- The triggering-stakeholder must be a person (persona or named role), not a system.
- The naming rule (value achieved, not internal lifecycle).
- The 4–10 stages rule.
- No Lean VSM and no customer-journey content in this artefact.

If the user violates these despite pushback, ship with the violation
flagged in the §Changelog or §Open Items so a future reviewer sees the
compromise. (`Open Items` follows the canonical schema in
the `metamodel` skill's `references/open-items-governance.md`.)
