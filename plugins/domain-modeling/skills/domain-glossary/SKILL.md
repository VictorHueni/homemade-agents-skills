---
type: skill
name: domain-glossary
description: "Create and maintain the Ubiquitous Language glossary — the shared vocabulary between domain experts and developers scoped per bounded context. Each term has a stable GT-NN ID, canonical definition, examples, deprecated aliases, cross-context translations, and code convention note. Synthesises Evans Domain-Driven Design (2003) Chapter 2 + Vernon DDD Distilled (2016) Chapter 2 + Martin Fowler ubiquitous language pattern. Use when asked to define domain vocabulary, create a glossary, document ubiquitous language, deprecate synonyms, manage domain terms, or align terminology between business and engineering. Triggers on: ubiquitous language, domain glossary, domain vocabulary, shared language, term definition, domain terms, DDD glossary, terminology alignment, domain dictionary, term deprecation, glossary management. Output: docs/domain/02c-glossary.md. Scoped to bounded contexts (BC-NN from domain-bounded-context)."
version: "1.0.0"
user-invocable: true
impact: "low"
metadata:
  category: "domain"
  complexity: "medium"
status: active
last_reviewed: 2026-05-29
---

# Domain Glossary Builder

Expert at producing and maintaining the Ubiquitous Language glossary — the single source of truth for domain vocabulary. Output is `docs/domain/02c-glossary.md`. NOT a technical dictionary, NOT a database schema, NOT a marketing glossary — it is the contractual vocabulary that domain experts and developers BOTH use in every conversation, every document, every line of code, every test name. Evans: "Use the model as the backbone of a language. Commit the team to exercising that language relentlessly in all communication within the team and in the code."

---

## What a good glossary means

| Quality check | Why it matters |
|---|---|
| Is every domain concept named once and only once per bounded context? | Synonyms fracture shared understanding — two words = two mental models |
| Does every term have a definition written in business language (no tech jargon)? | Tech definitions exclude domain experts, the primary owners of the vocabulary |
| Are all known aliases explicitly deprecated? | Deprecated aliases help readers who encounter legacy code or legacy docs |
| Does every term have an example sentence showing real usage? | Abstract definitions drift; concrete sentences anchor meaning |
| Are cross-context translations (same real-world thing, different model) documented? | Undocumented translations cause integration bugs at BC boundaries |
| Are code conventions linked (this term = this class name)? | The gap between vocabulary and code is where ubiquitous language fails |
| Can a new team member understand the domain by reading this alone? | The glossary is the onboarding artefact for domain thinking |

---

## Term entry formatting (mandatory)

Every field in a term entry **must be separated from the next by one blank line**. Markdown renderers collapse adjacent `**Field:**` lines into a single run-on paragraph when no blank line separates them. This is not optional — it is a rendering requirement.

Correct:

```markdown
#### {term name} · BC-NN.GT-NN

**Status:** Active

**Definition:** [definition text]

**Example:** "[example sentence]"

**Aliases (deprecated):** [aliases or _(none)_]

**Anti-patterns:**
- [...]
```

Wrong (do not do this):

```markdown
**Status:** Active
**Definition:** [definition text]
**Example:** "[example sentence]"
**Aliases (deprecated):** [aliases]
```

Apply this rule to every term entry in every mode (Seed, Enrich, Maintain). When updating an existing term, fix missing blank lines in the surrounding entry even if the task only targets one field.

---

## Modes

### Mode 1 — Scaffold

Create an empty `02c-glossary.md` with the canonical structure, BC section stubs, and the methodology pointer. Do NOT invent terms — leave all term entries as `_TODO_`. Output: `docs/domain/02c-glossary.md` using `references/template.md` as the skeleton.

Scaffold is idempotent: if `02c-glossary.md` already exists, report its current state and skip creation.

---

### Mode 2 — Seed

Populate the glossary with an initial set of terms from existing artefacts. Requires Step 0.

**Step 0 — ask all four questions before writing a single term. Users respond in the format "1A, 2B, 3C, 4A".**

```
1. Term source for initial seeding?
   A. Capability map L1 names — every capability name becomes a candidate term (recommended)
   B. Value stream stage names + process actor names
   C. Both — capability map + value stream vocabulary combined
   D. Custom list — I will provide the initial terms

2. Bounded context scope?
   A. Seed all bounded contexts in one pass
   B. One bounded context per session — please name it (BC-NN)
   C. Core subdomain first, then Supporting, then Generic

3. Initial entry depth?
   A. Term + one-line definition only (fast; enrich later in Mode 3)
   B. Term + definition + one example sentence
   C. Full entry — definition + example + aliases + anti-patterns + cross-context

4. Alias handling for existing vocabulary?
   A. Strict — immediately mark all known aliases as deprecated with migration note
   B. Gradual — document aliases with "transitioning from" note
   C. Document only — list aliases without deprecating yet
```

**Process after Step 0:**

1. Read capability map (`docs/business/03a-capability-map.md`) and/or value streams + process docs per the answer to Q1.
2. Extract nouns — every L1 capability name, every VS stage label, every process actor is a glossary candidate.
3. Map each candidate to its bounded context (from `docs/domain/` or `domain-bounded-context` artefact).
4. Assign GT-NN IDs sequentially within each BC section (GT-01, GT-02, …).
5. Write definitions in business language. Test each definition against the Definition Quality Test in `references/discipline.md`.
6. Identify and deprecate aliases per the answer to Q4.
7. Note obvious cross-context translations where the same real-world concept appears in multiple BCs.

---

### Mode 3 — Enrich

Deepen existing seeded terms. Targets one BC or one term at a time.

For each targeted term, add or improve:
- Definition (apply the Definition Quality Test — see `references/discipline.md`)
- Example sentence (concrete business scenario, not a code snippet)
- Aliases section (deprecated names with migration note)
- Anti-patterns (what this term is NOT; the most common confusions)
- Cross-context translations (link to the corresponding GT-NN in the other BC, explain the divergence)
- Code convention (class name, event name, variable naming rule)

Enrich is additive: never delete content, only extend or correct it.

---

### Mode 4 — Maintain

Keep the glossary aligned with the evolving domain model. This mode is a first-class recurring activity — not cleanup.

**Step 0 — Clarifying questions (ask BEFORE making any change)**

Ask the user the following 2 questions in a single message with lettered options. Users respond like `1C, 2B`:

```text
1. What triggered this maintenance run?
   A. New term emerged in a PRD, story, or conversation
   B. Synonym discovered in code review or sprint planning
   C. Bounded context was split, renamed, or merged
   D. Scheduled sprint glossary review (Core BC cadence)
   E. Event Storming or workshop produced new domain events / commands
   F. Existing docs were scanned and vocabulary drift was found

2. Scope of this maintenance pass?
   A. Single term — I will name it
   B. Single bounded context — I will name it (BC-NN)
   C. Full glossary pass — all BCs
```

If the user gives "Other" or pushes back, ask one follow-up to clarify, then proceed.

**Process per trigger type:**

- **New term (1A / 1E):** create full entry with next available `GT-NN` ID in the correct BC section; definition + example + code convention note mandatory; mark as `Active`; add changelog entry.
- **Synonym discovered (1B):** add as `Deprecated` alias to the canonical term; add a migration note ("if you see X in code, it means GT-NN Y"); add changelog entry.
- **BC restructure (1C):** update every `GT-NN` entry that referenced the changed BC; update the cross-context matrix; bump `glossary-version`; add changelog entry.
- **Sprint review (1D):** scan last sprint's PRDs, ADRs, and commit messages for nouns not in the glossary; add new terms; deprecate any aliases found; add changelog entry.
- **Vocabulary drift scan (1F):** grep the docs tree for candidate nouns (see discipline.md patterns); surface synonym clusters; propose canonical terms; add changelog entry per change.

**Changelog discipline (mandatory for every Mode 4 run):**

Every maintenance pass must add an entry to the `## Changelog` section at the bottom of `02c-glossary.md`:

```
### YYYY-MM-DD — {trigger summary}
- Added: BC-NN.GT-NN "{term}" — {one-line reason}
- Deprecated: "{alias}" → BC-NN.GT-NN "{canonical}" — {one-line reason}
- Retired: BC-NN.GT-NN "{term}" — {one-line reason}
- Updated: BC-NN.GT-NN "{term}" — {what changed}
```

Bump the `glossary-version` in the HTML comment at the top of the file for any structural change (new term, BC rename, term retirement). Patch-level edits (typo fix, example improvement) do not require a version bump.

---

## The seven anti-patterns

1. **Living with synonyms.** "Customer" and "Client" used interchangeably in the same BC = two competing mental models. Pick one, deprecate the other immediately. Every day a synonym survives, the distance between what the team says and what the code does grows.

2. **Tech-speak in definitions.** "A User is a row in the `users` table with an `email` field." Wrong. "A User is a registered person who has completed onboarding and can access the platform." Right. Domain experts do not own the schema; they own the definition.

3. **Vague definitions.** "Order: represents an order in the system." Circular. A definition must say what an Order IS in business terms, what state it can be in, and what distinguishes it from a Quote or a Contract.

4. **Glossary divorced from code.** If the code says `Account` and the glossary says `Customer`, the ubiquitous language has failed. Code naming IS glossary naming — class names, method names, event names, test names all use the glossary term exactly.

5. **One glossary for all bounded contexts.** Evans: the same word CAN mean different things in different BCs. "Product" in the Catalogue BC ≠ "Product" in the Billing BC. Scope every term to a BC. Cross-context translations handle the relationship.

6. **Glossary as a one-time document.** Ubiquitous language evolves as domain understanding deepens. A glossary written once and never touched has drifted from reality within one sprint. Mode 4 (Maintain) is a first-class activity, not cleanup.

7. **Missing cross-context translations.** When "Claim" in BC-01 corresponds to "Invoice" in BC-02, the translation must be explicit in the cross-context matrix. Undocumented translations cause integration bugs at every BC boundary.

---

## Sizing heuristics

| Element | Recommended | Source |
|---|---|---|
| Terms per bounded context | 15–50 | Practitioner — fewer = too abstract; more = too granular |
| Initial seed terms (from capability map L1) | 10–25 | Practitioner |
| Aliases per term | 0–3 | More = the vocabulary is undisciplined |
| Cross-context translations per term | 0–3 | More = the concept is too broadly shared (consider Shared Kernel) |
| Time to enrich one term fully | 5–10 min | Practitioner |
| Glossary review cadence | Every sprint for Core BC | Lean UX discipline |

---

## Finding the right folder

Default output path: `docs/domain/02c-glossary.md`.

Before writing, check for existing glossary artefacts:

```bash
find docs -type d -iname "*glossary*" -o -type d -iname "*ubiquitous*" 2>/dev/null
find docs -name "*glossary*" -o -name "*ubiquitous*" 2>/dev/null
```

Never overwrite existing content without explicit instruction:
- **Scaffold** → skip if `02c-glossary.md` already exists; report current state instead.
- **Seed** → append terms to the correct BC section; never delete existing entries.
- **Enrich** → update specific term entries in place.
- **Maintain** → mark terms as Retired or add new entries; never delete.

---

## Cross-reference — the architecture-artefact lifecycle

| Artefact | Relationship to glossary |
|---|---|
| `domain-bounded-context` (BC-NN) | Provides the namespace — every GT-NN is scoped to a BC-NN |
| Capability Map (C-N.M) | Capability names → first-class glossary terms (seed source) |
| Value Streams (VS-N.M) | Stage names + actor names → glossary candidates |
| `domain-model` (AGG/ENT/VO/EVT) | Entity and aggregate names MUST match glossary terms exactly |
| PRDs (PRD-NNNN) | PRDs use glossary terms in user stories and acceptance criteria |
| Business Process docs | Actor names + data object names → glossary candidates |

**ID cross-reference:** every glossary term carries a `BC-NN.GT-NN` composite ID. When a PRD or domain-model doc references a term, it uses this composite ID so that term renames do not silently break the link.

---

## Reference materials

This skill loads the following from `references/`:

- `template.md` — canonical `02c-glossary.md` skeleton (Scaffold mode copies this verbatim as a starting point)
- `methodology-references.md` — Evans, Vernon, Fowler, Brandolini, Sapir-Whorf sources
- `discipline.md` — Claude-internal guidance: definition quality tests, synonym detection patterns, cross-context translation rules, alias deprecation discipline

---

## Closing report

After every mode, emit a structured closing report:

```
Mode executed: [Scaffold | Seed | Enrich | Maintain]
File: docs/domain/02c-glossary.md
Terms seeded/enriched/retired: N
GT-NN IDs assigned: [GT-01 … GT-NN list]
Alias deprecations: [list term → deprecated alias pairs]
Cross-context translations added: [list BC-NN.GT-NN ↔ BC-NN.GT-NN pairs]
Code convention notes added: [list]
Next steps: [what Mode to run next, or what artefacts to update]
```

---

## Checklist (verify before closing)

- [ ] `docs/domain/` folder exists
- [ ] `02c-glossary.md` exists with the canonical structure from `template.md`
- [ ] Methodology pointer blockquote present at the top of the file
- [ ] Every BC-NN from the bounded-context map has a glossary section
- [ ] GT-NN IDs assigned sequentially within each BC section
- [ ] No living synonyms within a single BC (all aliases are deprecated)
- [ ] Every definition is in business language (zero tech-jargon words)
- [ ] Every enriched term has a code convention note
- [ ] Cross-context matrix populated for any term that spans BCs
- [ ] Mode 4: Step 0 answered before any change made
- [ ] Mode 4: changelog entry added for every term added / deprecated / retired
- [ ] Mode 4: glossary-version bumped for structural changes
- [ ] Open every generated file with the standard artefact frontmatter (OKF-superset block — set `type` to this artefact's `okf_type` display name from the `metamodel` skill's `references/artefact-types-registry.yaml`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`). Run `git config user.name` for `owner`. Set `status: draft` on initial scaffold. Default `review_interval: 180d`. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`.
- [ ] Closing report delivered
