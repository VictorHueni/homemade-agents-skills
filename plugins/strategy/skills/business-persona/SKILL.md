---
name: business-persona
description: "Create research-grounded or proto- personas using the canonical synthesis of BABOK §10.43 + Cooper goal-directed design + NNG + Pruitt & Adlin lifecycle + Lene Nielsen 10-step + Lean UX + JTBD. Use when the user asks to build personas, scaffold a personas folder, define target users, write a persona for {role}, build a persona backlog, or capture stakeholder archetypes. Triggers on: create personas, scaffold personas, build persona backlog, write a persona for, define target users, persona for {role}, identify stakeholders, who are our users, proto-persona. Domain-agnostic; works for any product type."
version: "1.0.0"
user-invocable: true
impact: "low"
metadata:
  category: "specification"
  complexity: "medium"
status: active
last_reviewed: 2026-05-29
---

# Persona Builder

You are an expert at producing **research-grounded persona artifacts** — structured archetypes of the real user groups a product serves, written so they survive design decisions, onboarding, and stakeholder engagement planning without further interviews.

The artifact produced by this skill is **a markdown document** in the project's personas folder (default `docs/business/`, adapt to project convention). It is NOT a marketing buyer-persona, NOT a one-pager poster, NOT a JTBD outcome statement on its own — it is **the descriptive source-of-truth** about who the product serves, written for product, engineering, and business-analysis consumption simultaneously.

Personas are one of the four canonical **Business Architecture artefacts** (BIZBOK / TOGAF), alongside the capability map, value streams, and business processes — which is why they all sit together under `docs/business/`.

This skill is **domain-agnostic**. The template patterns work for any product or industry; the references use abstract placeholders. When activated inside a project, the skill picks up the project's own product names, organisational vocabulary, and existing research artefacts. If `docs/VISION.md` exists at the project root, read it first — personas should reflect the vision's target audience framing and the problem the product solves.

---

## What a "good persona artifact" means

A persona artifact is good when a reader can identify, without ambiguity:

| Question | Where it lives in the doc |
|---|---|
| **Who is this person?** | §Snapshot + §Bio |
| **What design role do they play?** (primary / secondary / supplemental / served / negative) | §Header `Persona type` field |
| **What outcomes do they pursue when using the product?** | §Goals (formatted as Jobs where it fits) |
| **What blocks them today?** | §Frustrations |
| **What do they actually do in the product?** | §Key Tasks |
| **What does a typical use moment look like?** | §Scenarios |
| **What qualities of the system matter most for them?** | §System Needs |
| **How should the BA engage / collaborate with this group?** | §Stakeholder Profile (BABOK §10.43) |
| **How confident are we in this persona?** | §Research Grounding (with validation due-date for proto-personas) |

Every field must pass the **NNG design-decision-relevance test**: *"would removing this detail change a design or prioritisation decision?"* If not, omit it. This applies to optional snapshot fields (age range, primary device, primary language) — keep them only if they materially shape the product.

---

## The three modes of operation

The skill operates in one of three modes. Detect which mode the user wants from their prompt; ask if ambiguous.

### Mode 1 — Scaffold

**When:** the project has no `personas/` folder yet, or has one but is missing the canonical template + methodology references.

**Output:** ONE file in the project's chosen personas folder:
- `01a-personas.md` — hub document with introduction, kit-link methodology pointer, template, backlog scaffold, "no personas yet" placeholder.

Source from `references/template.md`. Substitute `{{product}}`, `{{domain}}`, `{{org_type_examples}}` placeholders from the project context.

**Do NOT** ship a project-side `methodology-references.md`. The canonical bibliography lives in the skill at `references/methodology-references.md` and is linked from the project doc's header. Single source of truth; no drift across projects.

**Do not** invent personas in scaffold mode. The output is the empty hub document.

### Mode 2 — Build the persona backlog

**When:** the scaffold exists but the backlog tables (Tier 1 / 2 / 3 / Negative) are empty or missing.

**Output:** populated backlog tables inserted into the existing `01a-personas.md` between the template block and the "## Personas" heading.

**Process:**
1. **Read project context** — PRD(s), product roadmap, functional breakdown structure (FBS), product-sense doc, README, business analysis docs. The persona backlog must derive from this, not from generic assumptions.
2. **Identify stakeholder universe** (BABOK §10.43.1 — Stakeholder List). Be exhaustive before pruning. Use the BABOK Onion Diagram framing: who interacts directly with the solution, who is in the broader organisation, who is outside.
3. **Assign each candidate a Cooper persona type** (see `references/persona-types-and-quality.md`):
   - **Primary** — the design target for one product/surface. Maximum one per product. Their goals are met by *designing for them*.
   - **Secondary** — uses the product, but their needs are mostly met by the primary's design plus minor accommodations.
   - **Supplemental** — uses the product occasionally; satisfied by primary+secondary design.
   - **Served** — affected by the product but does not use it directly (e.g., a patient when the product is used by a clinician).
   - **Customer** — buys/authorises the product but does not use it.
   - **Negative** — explicitly NOT designed for. Document them so the team knows to deprioritise their needs.
4. **Assign a tier** (priority axis, orthogonal to persona type):
   - **Tier 1** — core revenue / highest interaction depth / earliest validation needed.
   - **Tier 2** — important workflow contributor; not direct revenue driver.
   - **Tier 3** — future products, adjacent use cases, lower priority.
5. **Build the tables** with columns: `ID | Proposed name | Role / domain | Persona type | Primary product/surface | Key job outcome`.
6. **Identify negative personas + out-of-scope groups** — keep them in their own table at the bottom; document why each is out of scope.

**Do NOT** fully fill each persona in backlog mode. The backlog is the planning artifact; full personas are mode 3.

### Mode 3 — Fill one persona end-to-end

**When:** the backlog row exists for a persona ID (e.g., `P-02`) and the user wants the full persona body filled.

**Step 0 — Clarifying questions (ask BEFORE generating)**

Ask the user the following 4 questions in a single message with lettered options. Users respond like `1A, 2C, 3D, 4B`:

```text
1. Persona evidence basis?
   A. Proto-persona — assumptions-based; set Next review ≤90 days (Lean UX)
   B. Research-grounded — I have interview / observation / survey notes
   C. Hybrid — some fields evidenced, others assumed (label per-field)

2. Persona type (Cooper taxonomy — see references/persona-types-and-quality.md)?
   A. Primary — THE design target (max ONE primary per product/surface)
   B. Secondary — uses the product; design accommodates minor needs
   C. Supplemental — occasional user; satisfied by primary design
   D. Served — affected by the product but doesn't use it directly
   E. Customer — buys/authorises but doesn't use
   F. Negative — explicitly NOT designed for

3. Snapshot field inclusions (NNG design-decision-relevance test)?
   A. Minimal — Role, Org type, Domain experience, Usage frequency only
   B. Standard — above + Usage context (voluntary/required) + Primary language
   C. Full — above + Age range + Primary device (only if they affect design)

4. Goal framing?
   A. Jobs-to-be-Done — "When [trigger], I want [motivation], so I can [outcome]" (NNG-recommended)
   B. Bulleted goals — traditional outcome list
   C. Mixed — JTBD where it fits, bullets where it doesn't
```

If the user gives "Other" or pushes back, ask one follow-up to clarify, then proceed.

**Process:**
1. **Confirm mode** — proto-persona (assumption-based, Lean UX) or research-grounded (interview/observation/survey, BABOK). Both are valid; both must be **labelled honestly** in the §Research Grounding table.
2. **Pull project context** — the backlog row, plus any interviews / notes / customer feedback the user references.
3. **Fill the template** (see `references/template.md` for the canonical structure):
   - **Header:** ID, full name, tagline, persona type, tier, lifecycle status.
   - **Quote:** one sentence in the persona's own voice capturing their primary frustration, goal, or attitude. Make it specific and realistic, never generic.
   - **Snapshot:** include only dimensions that visibly affect product decisions. Skip irrelevant ones rather than padding.
   - **Bio:** 2–3 sentences grounded in the persona's day-to-day work *with the product or the problem the product solves*. Not hobbies, not personal life.
   - **Goals as Jobs (recommended):** format goals as "When [trigger/situation], I want [motivation], so I can [outcome]." This NNG-endorsed JTBD framing sharpens the same content. Fall back to bulleted goals if the situation-motivation-outcome shape does not fit.
   - **Scenarios:** 1–2 short narratives (3–5 sentences each) of the persona using the product or encountering the problem. Scenarios are the bridge between persona and design (Cooper + Nielsen). Make them specific: a triggering event, the persona's reasoning, the action they take, the outcome they care about.
   - **Frustrations:** ground in the domain, not generic UX complaints ("the app is slow" is not a persona insight — "monthly reports arrive as raw exports with no diff" is).
   - **Key Tasks:** the concrete actions the persona performs in the product. Maps directly to feature backlog / FBS functionalities.
   - **System Needs:** quality attributes (speed, accuracy, traceability, auditability, explainability, low cognitive load, bulk operation support, API access, offline capability). State *why each matters for this persona specifically*, not generically.
   - **Stakeholder Profile (BABOK §10.43.2 + RACI §10.43.3):** authority, interest, attitude (champion / supportive / neutral / sceptical / resistant), decision-making, RACI assignment, engagement strategy derived from the Influence×Interest matrix.
   - **Research Grounding:** evidence type, sample, key sources, created date, last validated, **next review date** (mandatory for proto-personas — Lean UX validate-or-retire discipline).
4. **Audit before saving** — run the quality checks in `references/persona-types-and-quality.md` §"Quality checks" before declaring the persona complete.

---

## Inputs

| Needed | What you ask if missing |
|---|---|
| **Project context location** | Look for `docs/product-specs/`, `docs/business/`, or equivalent. If unclear, ask: "Where do product specs live in this repo? (e.g., `docs/product-specs/`)" |
| **Mode** (scaffold / backlog / fill-one) | Detect from the user's request. Confirm if ambiguous. |
| **Product / product family name** | Required for `{{product}}` substitution. Infer from README or PRD; ask if not findable. |
| **Persona ID** (fill-one mode only) | The row in the backlog the user wants filled (e.g., `P-02`). Ask if not given. |
| **Evidence basis** (fill-one mode only) | "Is this a proto-persona (your team's assumptions, validate later) or research-grounded (interview / observation / survey notes you can share)?" |
| **Existing research artefacts** (fill-one mode only) | If research-grounded: "Where are the interview / survey notes? Paste a summary or point me at the file." |

Ask 2–4 questions max, in a single message, with lettered options where possible. Don't drag the user through a wizard. If mode is obvious from context, skip the mode question.

---

## Output structure — the fixed template

- Open every generated file with the standard artefact frontmatter (OKF-superset block — set `type` to this artefact's `okf_type` display name from the `metamodel` skill's `references/artefact-types-registry.yaml`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`). Run `git config user.name` for `owner`. Set `status: draft` on initial scaffold. Default `review_interval: 180d`. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`.

The skill produces ONE markdown file at `{personas folder}/01a-personas.md` with this fixed structure (full template in `references/template.md`):

```
<!-- doc-version: 1.0 | created: YYYY-MM-DD -->

H1: {{product}} — Personas

Introduction paragraph:
  - What personas are, why they exist, who they serve
  - Methodology pointer (2-line blockquote linking to the skill's canonical bibliography in the kit)
  - NNG design-decision-relevance rule of inclusion

§Persona Template (the blueprint, copied for each new persona)
  - Header: P-NN · Name — tagline
  - Persona type / Tier / Lifecycle status fields
  - Quote
  - §Snapshot (table)
  - §Bio (2-3 sentences)
  - §Goals (as Jobs or as goals)
  - §Scenarios (1-2 narratives)
  - §Frustrations
  - §Key Tasks
  - §System Needs
  - §Stakeholder Profile (BABOK §10.43)
  - §Research Grounding (with next-review for proto-personas)

§Persona Backlog
  - §Tier 1 — Primary (table)
  - §Tier 2 — Secondary (table)
  - §Tier 3 — Tertiary (table)
  - §Negative personas (table)
  - §Out of scope (list with rationale)

§Personas
  - One H3 sub-section per persona, using the template above

Changelog
```

**Section count is fixed; ordering is fixed.** The template block is mandatory and stays at the top so any contributor can copy it without scrolling past existing personas.

---

## The Cooper persona-type field is the design-discipline anchor

Without an explicit persona type, the team has no shared signal about which persona drives design decisions. Tiers (priority) and types (design role) are **orthogonal** — a Tier 1 persona is not automatically primary, and a primary persona is not automatically Tier 1.

**Hard rule:** every product or design surface has **exactly one primary persona**. If the team wants to elevate two personas to "primary", they should split into two product surfaces — the discipline forces a real design conversation rather than a compromise that satisfies neither.

See `references/persona-types-and-quality.md` for the full Cooper taxonomy with examples and decision rules.

---

## Proto-persona vs research-grounded — the Lean UX discipline

Per Lean UX (Gothelf), proto-personas are explicitly assumption-based and valid as a starting point — but only if they carry an explicit **next-review date** and the team commits to validate or retire them on schedule.

**Proto-persona rules:**
- §Research Grounding `Evidence type` must say `"proto-persona (assumption)"` — never hide assumptions under vague "internal team knowledge".
- `Next review` field is mandatory and must be ≤ 90 days from `Created` date.
- On `Next review` date, the persona is either upgraded to research-grounded (one or more validation methods completed) or retired.

**Research-grounded rules:**
- `Evidence type` lists the method (interview / observation / workshop / survey / contextual inquiry / diary study).
- `Sample` quantifies it ("3 interviews with X at 2 organisations" — never "lots of feedback").
- `Last validated` and `Next review` track freshness — NNG recommends re-validation when user research reveals drift, typically yearly.

See `references/persona-types-and-quality.md` §"Proto-persona discipline" for full guidance.

---

## Cross-reference — the architecture-artefact lifecycle

A persona doc is one of several architecture artefacts that together describe what a product does for whom:

| Layer | Job | Owns |
|---|---|---|
| **Persona** *(this skill)* | "Who we serve, what they pursue, how we engage them" | Archetypes, goals, frustrations, scenarios, stakeholder profile |
| **Value Stream / Customer Journey** | "How value flows from trigger to outcome for one persona through processes + capabilities" | Stage sequence, trigger events, value delivered per stage |
| **Business Process** | "What happens — who, what, how, with what data" | Activities, actors, data, KPIs, decisions |
| **Functional Breakdown Structure (FBS)** | "What the product can do, organised by product → capability → functionality" | Capability map, functionality status, code-organisation hints |
| **PRD** | "What we will build for which persona and why" | Feature spec, acceptance criteria, success metrics |

### The content-routing rule

When uncertain where a piece of content belongs, ask:

1. **Is it a fact about the user (who they are, what they pursue, what frustrates them)?** → persona doc.
2. **Is it a sequence of stages the user moves through to get value?** → value stream / journey doc.
3. **Is it the operational workflow (actors, activities, data, decisions) the user participates in?** → process doc.
4. **Is it a capability or functionality the product offers?** → FBS.
5. **Is it a feature spec with acceptance criteria?** → PRD.

**Tie-breaker:** "Would this be true if no one used the product?" If yes → it's about the user or the world (persona / analysis / process). If no → it's about the product (FBS / PRD).

### Soft-reference principle

Personas reference value streams + processes + FBS *as pointers, not as dependencies*. A persona doc must stand alone; cross-references add depth, not prerequisites. Personas should ship even if value-stream / FBS docs do not yet exist.

When linking, prefer **persona ID + artefact-row ID** ("P-02 consumes BC4.3 across value-stream stage VS-3-Review"). This makes traceability mechanical when the linked artefact gets refactored.

---

## Common patterns to apply

1. **One persona = one archetype, not a category.** "Physician" is a category, not a persona. "Dr. Maria Stein, ambulatory specialist in a French-language canton" is a persona. Force specificity.

2. **Name and photo aid memorability.** NNG's recommendation: give the persona a first + last name (not just a role title). A representative photo helps the team see them as real. Use stock-photo placeholders in the template; the real project can substitute.

3. **Quote first, table second.** The quote at the top is the persona's most memorable signal. Write it last (after the rest of the persona is filled), but place it first in the document so it primes every reader.

4. **Scenarios beat tasks.** A task list is enumerable but flat. A scenario shows context, motivation, decision moment, and outcome. Aim for 1–2 scenarios per persona; cover the most representative use moments, not every use moment.

5. **Engage on the strongest evidence available.** If interview notes exist, ground the persona in direct quotes — they make the persona unforgettable. If only assumptions exist, label it proto-persona and schedule the next review.

6. **Domain frustrations, not UX complaints.** "It's slow" is a UX complaint. "I can't tell which limitation changed between editions without diffing XML manually" is a domain frustration. Domain frustrations map directly to feature opportunities.

7. **System needs are quality attributes with persona-specific rationale.** Generic "speed" is empty. "Speed: this persona checks coverage during a 5-minute patient encounter; latency above 2 seconds breaks their workflow" is actionable.

8. **Negative personas are a deliberate design tool, not a list of haters.** Cooper's negative persona is someone whose needs the product *intentionally* deprioritises. Surface them explicitly so the team doesn't bend to satisfy edge cases at the cost of the primary.

9. **Re-validate, don't re-create.** Per Pruitt & Adlin, personas have a lifecycle. When user research reveals drift, update the persona — don't start over. Track changes in the doc changelog.

10. **Quote sources at quality tier:**
    - ★★★★★ Primary interview / observation transcripts (direct, recent)
    - ★★★★ Primary survey / contextual inquiry data
    - ★★★ Vendor research, secondary studies, triangulated across sources
    - ★★ Internal team knowledge, vendor marketing — directional
    - ★ Anecdote / single weak signal — cite with caveat (proto-persona territory)

---

## Sizing heuristics

| Element | Recommended | Source |
|---|---|---|
| Tier-1 personas per product | 1–3 | Lean UX + Cooper (max 1 primary per surface) |
| Total personas in backlog | ≤8 | Practitioner — more signals scope is too broad |
| Proto-persona next-review | ≤90 days from Created | Lean UX validate-or-retire discipline |
| Goals per persona | 3–5 | NNG |
| Scenarios per persona | 1–2 | Cooper + Nielsen |
| Frustrations per persona | 3–5 | Practitioner |

**If any number exceeds the recommended range, reconsider:**
- Too many Tier-1 personas → the product is trying to serve everyone; force a primary/secondary split.
- Too many personas in backlog (>8) → the scope is too wide; tighten the target market or split by product surface.
- Proto-persona past next-review date → it has expired; validate or retire before using it in design decisions.
- Too many goals (>5) → goals are too granular; consolidate into higher-level JTBD outcomes.
- Too many scenarios (>2) → scenarios are covering edge cases; trim to the most representative use moments.

---

## Finding the right folder

**Default:** `docs/business/` — aligns personas with the other Business Architecture artefacts (capability map, value streams, processes).

**Always check for an existing folder first:**

```bash
find docs -type d -name "personas" 2>/dev/null
```

If a folder exists at a non-default location (e.g., `docs/product-specs/personas/`, `docs/<domain>/personas/`), use it — don't move existing work without an explicit user request. If multiple candidates exist, ask. If none exists, default to `docs/business/` and confirm with the user.

**Never overwrite an existing `01a-personas.md`.** If it exists, switch modes:
- Scaffold mode → skip (report what's already there).
- Backlog mode → append/update backlog tables only, preserve existing personas.
- Fill-one mode → append a new H3 sub-section under "## Personas".

---

## Reference materials

Three files in `references/` carry the canonical content. Read them when needed:

- **`references/template.md`** — the canonical `01a-personas.md` skeleton. Copy this to `{personas folder}/01a-personas.md` and fill placeholders.
- **`references/methodology-references.md`** — the canonical bibliography (BABOK §10.43, Cooper, Pruitt & Adlin, Lene Nielsen, NNG, Lean UX, JTBD). **Lives only in the kit** — never copied to projects. Project docs link here via the 2-line pointer in their header.
- **`references/persona-types-and-quality.md`** — Cooper's six persona types with decision rules, NNG quality-check anti-patterns, proto-persona discipline. Internal Claude guidance; never copied into the project.

---

## Closing report to the user

After running any mode, summarise in 4–6 lines:

1. **Mode executed** (scaffold / backlog / fill-one) and **files created or updated**, with paths.
2. **What got pre-filled** vs `_TODO_` — be specific (e.g., "filled 4 of 7 snapshot fields; bio + goals derived from PRD §3; frustrations and scenarios marked `_TODO_` pending interview notes").
3. **Persona type + lifecycle status assigned** (fill-one mode) — explicit so the user can sanity-check.
4. **Top validation priorities** — for proto-personas, the `Next review` date and the validation methods that would convert it to research-grounded.
5. **Cross-link opportunities** — if FBS / value-streams / PRDs exist, suggest the bidirectional links to add (persona ID ↔ BC ID ↔ value-stream stage).

Keep it short. The user will read the file directly; your job is to point them at the next move.

---

## Checklist

Before declaring the work done:

- [ ] Folder existed or was created (with user confirmation if new path).
- [ ] `01a-personas.md` exists in the personas folder (scaffold mode).
- [ ] Methodology pointer in `01a-personas.md` header links to the kit's canonical bibliography (NOT a local methodology-references.md).
- [ ] Backlog tables populated with Cooper persona types + tiers + negative section (backlog mode).
- [ ] Persona body filled with all required fields per the template (fill-one mode).
- [ ] Every snapshot field present passes the NNG design-decision-relevance test.
- [ ] Proto-personas have explicit `Next review` ≤ 90 days from `Created`.
- [ ] Research-grounded personas list method + sample + key sources.
- [ ] No project-specific terms baked into anything reusable — placeholders preserved.
- [ ] Closing report delivered to the user.
