---
name: discovery-workshop
description: "Plan single-session or multi-session workshops that reality-check business-architecture artefacts such as personas, BMCs, value streams, capability maps, and competitive analyses through structured group facilitation. Use when the user asks to plan a workshop, design a workshop series, align stakeholders, run a BMC workshop, design a Design Sprint, plan a discovery workshop, or synthesize workshop outputs. Triggers on: workshop, facilitation, workshop series, workshop guide, design sprint, alignment workshop, BMC workshop, discovery workshop, Liberating Structures, facilitator's guide. Domain-agnostic. Not for 1:1 interviews; use `discovery-research` for individual research sessions."
version: "1.0.0"
user-invocable: true
impact: "low"
metadata:
  category: "specification"
  complexity: "medium"
status: active
last_reviewed: 2026-05-29
---

# Business Workshop Builder

You are an expert at producing **workshop facilitation guides** in the canonical practitioner tradition: Sam Kaner's *Facilitator's Guide to Participatory Decision-Making* (Diamond of Participation), Lipmanowicz & McCandless's *Liberating Structures* (33 microstructures replacing conventional meeting formats), Strategyzer workshop kits (BMC + VPC facilitation), Jake Knapp's *Sprint* (5-day Design Sprint), Priya Parker's *The Art of Gathering* (intentional gathering), and IAF facilitator competencies.

The artifact produced by this skill is **a markdown document** at `docs/discovery/workshops/`. It is NOT a 1:1 interview script (use `discovery-research`), NOT a sales presentation, NOT a project kick-off meeting agenda — it is **the strategic-design group session** that aligns stakeholders + builds shared artefacts + reality-checks design assumptions.

This skill is **domain-agnostic**. When activated inside a project, it picks up personas, BMC, value streams, capability map, and competitive landscape, and produces workshop guides that target specific design-validation outcomes.

---

## What a "good workshop guide" means

A workshop guide is good when a reader can answer, without ambiguity:

| Question | Where it lives |
|---|---|
| **What is the workshop's objective?** | Frontmatter — one-sentence outcome statement |
| **What artefacts will exist at the end?** | §Summary of deliverables (numbered list) |
| **Who attends + what's their role?** | §Team composition + how to leverage (the "superpower" mapping per the practitioner reference) |
| **What needs to be prepared beforehand?** | §Pre-workshop checklist (materials + prints + digital + pre-read) |
| **What happens minute-by-minute?** | §Session-by-session agenda (or single-session if scope = 1) |
| **Which facilitation methods are used?** | Per-exercise — name the Liberating Structure or canonical method + timebox + flow |
| **What happens after?** | §Post-workshop actions (when × action × owner) |
| **What can go wrong?** | §Facilitation tips (Kaner Diamond stages, energy management, handling disagreements) |

**Hard scope rules:**
- Every exercise carries a **timebox** (5–60 min) and names a **canonical method** (Liberating Structures microstructure, Strategyzer canvas, Kaner technique, etc.).
- Every workshop produces **named deliverables** (numbered in the summary table).
- Every workshop has **pre-read sent N days before** (default 5 days; specify in frontmatter).
- Series workshops cross-link (W1 outputs → W2 inputs).
- The guide is meant to be **executable by a co-facilitator** without further consultation.

---

## The four modes of operation

### Mode 1 — Scaffold

**When:** the project has no workshops/ folder yet.

**Output:** ONE file in `docs/discovery/workshops/`:
- `README.md` — hub doc listing open workshop opportunities (which BA artefacts need stakeholder validation? which decisions need group alignment?) + index of past + planned workshops.

Do NOT create workshop guides in scaffold mode.

### Mode 2 — Plan a single workshop

**When:** the user wants to plan one workshop targeting a specific outcome.

**Step 0 — Clarifying questions (ask BEFORE generating)**

Ask the user the following 4 questions in a single message with lettered options. Users respond like `1A, 2C, 3D, 4B`:

```text
1. Primary workshop objective?
   A. Fill / refresh a BMC (Strategyzer canvas workshop)
   B. Persona alignment — build or validate 1-3 personas as a group
   C. Value stream mapping — group walkthrough of a customer journey
   D. Capability map L0 axis decision — strategic clustering exercise
   E. Roadmap / prioritisation — feature or initiative ranking
   F. Discovery / problem framing — pre-PRD problem definition
   G. Design Sprint (Knapp) — 5-day rapid prototyping
   H. Other: [please specify outcome]

2. Group size?
   A. Small (3-6) — co-founders / leadership / single team
   B. Medium (7-12) — cross-functional initiative team
   C. Large (13-25) — multi-team alignment
   D. Very large (25+) — requires multi-facilitator + breakout discipline

3. Duration?
   A. Half-day (3-4h) — single focused outcome
   B. Full day (6-8h) — multi-outcome or large group
   C. Multi-day (2-5 days) — Design Sprint or deep alignment
   D. Series — multiple half-days spread over weeks (use mode 3 instead)

4. Stakeholder availability + decision authority?
   A. Decision-makers attending — workshop produces binding decisions
   B. Decision-makers not present — workshop produces recommendations for later sign-off
   C. Mixed — some present, some represented by proxy
```

If the user gives "Other" or pushes back, ask one follow-up to clarify, then proceed.

**Process:**
1. **Read upstream artefacts** — relevant BA docs, personas, BMC, value streams, models. Identify which open decisions / assumptions the workshop will close.
2. **Create** `workshop-{slug}-{date}.md` in `docs/discovery/workshops/`.
3. **Fill the template** (see `references/template.md`):
   - **Frontmatter:** objective + duration + group + date + facilitator
   - **Team composition + superpower** mapping (per practitioner-tested pattern)
   - **Pre-workshop checklist** (materials + prints + digital + pre-read)
   - **Pre-read package** (sent N days before; default 5)
   - **Session agenda** — time-boxed exercises with canonical-method names + materials + flow
   - **Summary of deliverables** (numbered list — what exists at the end)
   - **Post-workshop actions** (when × action × owner)
   - **Facilitation tips** — pulled from Kaner Diamond + ground rules + energy management
   - **Risk / disagreement handling** (Kaner techniques: dot-voting, disagree-and-commit, parking lot)

### Mode 3 — Plan a workshop series

**When:** the user wants a multi-session workshop series (typical: 2-4 half-day sessions over 2-3 weeks).

**Process:**
1. **Ask the same Step 0 questions** but expand Q3 to "How many sessions?".
2. **Create a series file** `workshop-series-{slug}.md` that orchestrates multiple sessions + per-session files cross-linked.
3. **Fill the series template:**
   - **Series-level overview** — total duration, theme arc (e.g., W1 vision → W2 business model → W3 features)
   - **Per-session deliverables flow** — what W1 produces becomes W2's input
   - **Pacing principle** — half-days work best for first-timers; spacing 5-7 days apart lets ideas mature
   - **Pre-series pre-read** + per-session pre-reads
   - **Series-level deliverables summary** (cumulative)
   - **Series post-actions** (calendar of follow-ups)
4. **Per-session sub-files** (`workshop-series-{slug}-w1.md`, `-w2.md`, etc.) — each follows the single-workshop template (mode 2).

### Mode 4 — Workshop synthesis (post-workshop)

**When:** a workshop has happened; the user wants to capture outputs.

**Process:**
1. **Create** `workshop-synthesis-{slug}-{date}.md` in `docs/discovery/workshops/`.
2. **Fill the template:**
   - **Attendees + roles** (with absences noted)
   - **Outputs produced** (with photos or Miro/Mural links)
   - **Decisions made** (with dot-vote results or consensus method)
   - **Follow-up commitments** (with owners + dates)
   - **Updates to upstream artefacts** (BMC blocks promoted, personas refined, value-stream stages added, etc.)
   - **What went well / what to change** for next workshop
   - **Open items** — actionable unresolved work surfaced during the workshop (questions the room could not close, decisions deferred, follow-ups for the next wave) filed directly to the central ledger via `util-open-items` (per the `metamodel` skill's `references/open-items-governance.md`; no local section — ADR-0005). Each row carries `Source anchor` + `Source heading` pointing into the synthesis (Decisions made, Follow-up commitments, etc.). File nothing if nothing actionable remains.
   - **Cross-link to series file** if applicable

---

## The Diamond of Participation (Kaner) — the core facilitation model

Every workshop session moves through 4 stages. The Diamond is the
canonical map:

```
        Divergent zone              GROAN zone              Convergent zone
                                                              ▲
        Generate possibilities  →  Struggle / messy middle  →  Refine into decisions
        ──────────────────────     ──────────────────────     ──────────────────────
        Brainstorm                 Where ideas conflict       Dot-voting
        1-2-4-All                  Diamond bottom             Decision matrices
        Crazy 8s                   Hardest to facilitate      Disagree-and-commit
        Mind mapping
```

**Why this matters:**
- Most workshop failures happen in the GROAN zone (the messy middle). Inexperienced facilitators rush through to convergence too fast OR get stuck in divergence forever.
- The skill's per-session agenda explicitly names which stage each exercise belongs to. Reviewer can spot imbalance ("we have 4 divergent exercises and 0 convergent — we won't actually decide anything").

See `references/methodology-references.md` §1 for the full Kaner framework.

---

## The 33 Liberating Structures — replacing conventional meeting formats

`references/liberating-structures.md` catalogs all 33 microstructures
with when-to-use guidance. Common picks:

| Structure | Best for | Time |
|---|---|---|
| **1-2-4-All** | Engaging everyone in idea generation (replaces brainstorm) | 12-15 min |
| **Fishbowl** | Deep dive on a controversial topic with the group listening | 30 min |
| **World Café** | Large-group exploration of multiple questions | 60-90 min |
| **Wicked Questions** | Surface paradoxes the group must navigate | 15-20 min |
| **TRIZ** | "Make it worse" — identify counterproductive behaviours to stop | 25-35 min |
| **Min Specs** | What's the minimum we must do / not do? | 30-45 min |
| **Wise Crowds** | Help one person solve a problem using the group's expertise | 30-45 min |
| **Troika Consulting** | Trio-based peer consultation | 30 min |
| **15% Solutions** | "What can you do in the next 7 days?" — surface micro-action | 20-30 min |
| **Open Space** | Self-organising agenda for large mixed groups | 90+ min |
| **What, So What, Now What** | Structured debrief / reflection / commitment | 15-20 min |

**Rule:** every exercise in the workshop agenda should name the
Liberating Structure (or other canonical method) it uses. "Brainstorm"
is too vague; "1-2-4-All on the question 'what's our riskiest
assumption'" is executable.

---

## Inputs

| Needed | What you ask if missing |
|---|---|
| **Project context location** | Look for `docs/business/`. If unclear, ask. |
| **Mode** (scaffold / single / series / synthesis) | Detect from request. Confirm if ambiguous. |
| **Upstream artefacts** | Check for personas, BMC, value streams. Workshops that target these will reference them. |
| **Workshop objective** | Step 0 Q1 |
| **Group size** | Step 0 Q2 |
| **Duration** | Step 0 Q3 |
| **Decision authority** | Step 0 Q4 |

Ask 2–4 questions max in a single message.

---

## Cross-reference — the architecture-artefact lifecycle

| Workshop output | Soft-links to / updates |
|---|---|
| BMC workshop | `docs/business/02a-bmc.md` — blocks filled / refined |
| Persona workshop | `docs/business/01a-personas.md` — proto-personas elevated to research-grounded post-workshop |
| Value stream workshop | `docs/business/04a-value-streams.md` — stages confirmed / refined |
| Capability map workshop | `docs/business/03a-capability-map.md` — L0 axis decided; L1 enumerated |
| Roadmap workshop | `docs/product-specs/` — MoSCoW prioritisation; MVP scope decided |
| Discovery workshop | `docs/discovery/interviews/` — interview themes synthesised; problem framing aligned |

Workshops are the group-reality-check counterpart to `discovery-research` (the individual reality-check). Both feed evidence back to the design skills.

---

## Common patterns to apply

1. **Half-days work best for first-time workshop participants.** 4h is the attention budget; 8h sessions lose focus. Space sessions 5-7 days apart for ideas to mature.

2. **Silent writing before discussion.** Always have participants write post-its individually BEFORE sharing aloud. Prevents the loudest voice from dominating; surfaces minority opinions.

3. **Dot-voting over debate.** When opinions diverge, vote with stickers (3-5 dots per person). Democratic, fast, no hard feelings.

4. **Timeboxing visibility.** A visible timer (phone or physical) creates focus. "Vous avez 5 minutes" beats "we'll see how it goes".

5. **Persona / role champions.** Each participant "adopts" a persona or role and represents that user's interests in all discussions. Surfaces user-needs even when no actual user is in the room.

6. **Parking lot.** Dedicated wall space for off-topic ideas. Promise to revisit. Prevents derailing.

7. **Strategyzer canvas workshop pattern** — for BMC / VPC: print A1 / A0; fill with sticky notes; one bullet per sticky; cluster within blocks; vote on most uncertain bullets; designate which bullets need post-workshop validation (= input to `discovery-research` interview scripts).

8. **Design Sprint (Knapp) — 5-day pattern** — for product discovery: Monday map, Tuesday sketch, Wednesday decide, Thursday prototype, Friday test. The skill supports this as a special-case series in mode 3.

9. **Disagree and commit.** Vote; minority commits to majority decision; revisit in 4 weeks with data. Kaner-canonical for unblocking convergence.

10. **Photograph everything within 48h.** Wall artefacts decay (post-its fall, marker fades). Photo + Miro/Mural digitisation captures the output for the synthesis.

---

## Sizing heuristics

| Element | Recommended | Source |
|---|---|---|
| Half-day duration | 3-4h | Practitioner: attention budget for first-timers |
| Exercises per half-day | 4-7 | Pacing — too few = stalls; too many = rushed |
| Time per exercise | 5-60 min | Kaner — varies by stage (divergent shorter; convergent longer) |
| Session count in a series | 2-4 (typical); 5+ for Design Sprint | Practitioner |
| Group size — single facilitator | ≤12 | IAF — beyond this, add co-facilitator + breakouts |
| Pre-read send time | 5 days before | practitioner-tested |
| Post-session digitisation | within 48h | Practitioner: post-it decay |

---

## Finding the right folder

Default: `docs/discovery/workshops/`. The parent `docs/discovery/` is shared with `discovery-research` (`docs/discovery/interviews/`) and `discovery-idea` (`docs/discovery/ideation/`) — the three skills together form the reality-check family for the design skills.

**Check first:**

```bash
find docs -type d -iname "*workshop*" 2>/dev/null
```

If a folder exists, use it. If multiple, ask. If none, default and confirm.

**Never overwrite an existing workshop file.** Each mode creates a new file; existing files are never regenerated wholesale:
- Scaffold mode → skip if `README.md` already exists (report what's there).
- Single workshop mode → always create a new `workshop-{slug}-{date}.md`; never overwrite a previous guide.
- Series mode → always create new series + per-session files; never overwrite existing sessions.
- Synthesis mode → always create a new `workshop-synthesis-{slug}-{date}.md`; never overwrite prior synthesis.

---

## Reference materials

Three files in `references/`:
- **`references/template.md`** — workshop guide (single + series) + synthesis templates
- **`references/methodology-references.md`** — canonical bibliography (Kaner, Liberating Structures, Strategyzer, Knapp, Parker, IAF). **Kit-only.**
- **`references/liberating-structures.md`** — catalog of the 33 microstructures with when-to-use guidance. Internal Claude guidance for picking exercises.

---

## File Open Items to the central ledger

While producing a workshop synthesis file, file each unresolved item directly to the
central ledger via `util-open-items` — there is no local section to author first
(ADR-0005).

- **File as you go.** Each row carries `Source anchor` + `Source heading` pointing back
  into the originating sub-section of the synthesis (Decisions made, Follow-up
  commitments, Updates to upstream artefacts, etc.), citing the synthesis file as `Source
  artefact` (per the `metamodel` skill's `references/open-items-governance.md` §4 + §5).
- **File nothing when there's nothing to file.**
- **Mode coverage.** File after Mode 4 Workshop synthesis (the only mode that surfaces
  open items). Mode 1 Scaffold, Mode 2 Plan a single workshop, and Mode 3 Plan a workshop
  series surface no actionable open items — those emerge from what the room could not
  close, a post-session observation.

Invoke as: "File the open item for
`docs/business/workshops/workshop-synthesis-{slug}-{date}.md` via the util-open-items
skill."

---

## Closing report to the user

After running any mode, summarise in 4–6 lines:

1. **Mode executed** + **files created or updated** with paths.
2. **Workshop objective + duration + group size**.
3. **Deliverables expected** (numbered).
4. **Canonical methods used** — which Liberating Structures / Strategyzer canvases / Kaner techniques the agenda calls.
5. **Cross-link opportunities** — which BA artefacts (personas, BMC, value streams) will be touched.
6. **Diamond stage balance** — does the agenda have enough convergent exercises to actually decide, or is it weighted to divergence?

---

## Checklist

Before declaring the work done:

- [ ] Folder exists or was created.
- [ ] Methodology pointer in workshop guide links to the kit's canonical bibliography.
- [ ] Frontmatter has objective + duration + group + date + facilitator.
- [ ] §Team composition + superpower table filled.
- [ ] §Pre-workshop checklist (materials + prints + digital + pre-read) present.
- [ ] Every exercise has timebox + named canonical method (Liberating Structure / Strategyzer / Kaner).
- [ ] §Summary of deliverables table populated.
- [ ] §Post-workshop actions table (when × action × owner).
- [ ] §Facilitation tips section pulled from Kaner / Liberating Structures.
- [ ] Diamond stage balance check: ≥1 convergent exercise per session (workshops without convergence don't decide).
- [ ] Open every generated file with the standard artefact frontmatter (OKF-superset block — set `type` to this artefact's `okf_type` display name from the `metamodel` skill's `references/artefact-types-registry.yaml`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`). Run `git config user.name` for `owner`. Set `status: draft` on initial scaffold. Default `review_interval: 90d`. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`.
- [ ] No project-specific terms baked in (kit version).
- [ ] Closing report delivered.
