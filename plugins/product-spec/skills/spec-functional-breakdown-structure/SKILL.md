---
type: skill
name: spec-functional-breakdown-structure
description: "Create a Functional Breakdown Structure (FBS) — the functionality registry organised by product → capability → functionality, with status tracking (✅/🔄/⬜), optional code-path annotations, and optional value-stream-stage linkage. Synthesises BABOK §10.22 Functional Decomposition + NASA FBS + TOGAF Business Architecture + practitioner discipline. Use when the user asks to build an FBS, scaffold a functionality registry, decompose a product into functionalities, track feature status across the lifecycle, or extend a Business Capability Map with feature-level detail. Triggers on: FBS, functional breakdown structure, functionality registry, decompose product, feature inventory, what does the product do (concretely), capability-to-feature mapping, product decomposition. Domain-agnostic. Soft-links UP to the Business Capability Map (BC Map owns L0+L1 strategic; FBS adds L2 functionalities + status + code paths). Stays out of PRD/roadmap territory."
version: "1.2.0"
user-invocable: true
impact: "low"
metadata:
  category: "specification"
  complexity: "medium"
status: active
last_reviewed: 2026-05-29
---

# Functional Breakdown Structure Builder

You are an expert at producing **Functional Breakdown Structures (FBS)** — the canonical functionality registry that answers, for any product: *"does this product do X, and where in the codebase does it live?"* Synthesises BABOK §10.22 (Functional Decomposition), NASA's FBS doctrine, TOGAF's capability-to-feature mapping, and practitioner discipline from software product literature.

The artifact produced by this skill is **a markdown document** at `docs/product-specs/07a-fbs.md` (adapt to project convention). It is NOT a feature backlog, NOT a roadmap, NOT a PRD, NOT a capability map — it is **the functionality registry**: comprehensive, status-tracked, and traceable to capabilities (UP) and PRDs (DOWN).

This skill is **domain-agnostic**. When activated inside a project, it inherits the project's BC Map (capability IDs + names) and produces an FBS that extends the capability hierarchy with functionality-level detail.

---

## What "FBS" means here — pure-FBS vs hybrid-FBS

Strictly per NASA's Systems Engineering literature, a Functional Breakdown Structure is *"a structured, modular breakdown of every function that must be addressed to perform a generic mission… The FBS is not tied to any particular architectural implementation because it is a listing of the needed functions, not the elements, of the architecture."* In its pure form, an FBS contains **only functions**, organised independently of products, organisations, and technology.

In software-product orgs, "FBS" is commonly used to mean a **hybrid** structure where the top levels organise by product (or product family) and the leaf level enumerates functionalities. This hybrid mixes:
- **Product Breakdown Structure (PBS)** elements (L0 — product or domain)
- **Capability Map** elements (L1 — soft-linked from the BC Map by ID)
- **FBS-proper** elements (L2 — the functionalities)

This skill produces the **hybrid form** because it's what product/software teams actually need. The methodology references explain the distinction honestly so readers understand the trade-off.

---

## What a "good FBS" means

An FBS is good when a reader can answer, without ambiguity:

| Question | Where it lives |
|---|---|
| **What is the product's stable tooling handle?** | Per-product `` `slug: <handle>` `` code-line (third identifier — globally unique with BC Map slugs) |
| **What is the organising axis (L0)?** | §L0 axis declaration (inherited from BC Map) |
| **Which capabilities does the product cover (L1)?** | §Per-capability sections — soft-linked to BC Map by ID |
| **What functionalities realise each capability?** | Per-capability functionality table |
| **Is functionality X shipped / planned / backlog?** | Status column per functionality (✅ 🔄 ⬜) |
| **Where in the codebase does each capability live?** | Per-capability backend/frontend code-path annotations (optional) |
| **Which value-stream stage does a functionality support?** | Per-functionality VS-stage column (optional) |
| **What's the stable identifier for functionality X?** | Per-functionality ID `C1.1.F01` (capability + functionality counter) |

**Hard scope rules:**
- FBS does **NOT** define capabilities — soft-links to BC Map. If you find yourself writing a capability definition, that belongs in `business-capability-map.md`.
- FBS does **NOT** contain feature specs / acceptance criteria — those are PRD territory.
- FBS does **NOT** contain roadmap timelines, dates, or milestones — those belong in a roadmap doc.
- FBS does **NOT** include cycle-time or operational metrics — that's process-doc territory.

If the FBS doc starts to grow any of these, it has crossed scope. Pull the offending content out into its proper home and link instead.

---

## Granularity discipline — the registry principle

The FBS is a **registry**, not a story list and not a sprint backlog. Every row
must describe a discrete, independently testable system behaviour. The most
common failure mode — especially when source material (Excel, user stories,
PRDs) is provided — is translating source rows 1:1 into FBS rows, producing
either over-fragmented attributes or under-decomposed coarse entries.

### The three granularity tests

Run all three before adding or keeping any row.

**Test 1 — Independent testability (too atomic?)**
*Anchored in: INVEST criteria "I" (Independent) + "T" (Testable) — Bill Wake (2003)*

Ask: "Can this row be tested in isolation, independently of any sibling row?"

- If NO → the row is an *attribute* of another functionality and should be
  merged into it. Colour codes, enable/disable flags, name fields, and other
  entity properties are attributes — not functionalities.
- If YES → keep the row.

> Example: "Assign colour code per room" fails Test 1 — you cannot test colour
> assignment without first having a room. Merge into "Configure OR room
> (name, identifier, colour code, enabled status)".

**Test 2 — Size ceiling (too coarse?)**
*Anchored in: INVEST criterion "S" (Small) — Cohn, *User Stories Applied* (2004);
practitioner heuristic: "fits in a sprint" → ~5 days focused development*

Ask: "Could this row represent more than ~5 days of focused development?"

- If YES → the row may need splitting. Use judgement: a complex algorithm
  (schedule generation) is legitimately one row even if it takes weeks; a
  "planning views" row that bundles 8 distinct UI screens is too coarse.
- If NO → keep the row.

Note: the 5-day figure is a practitioner heuristic derived from common sprint
sizing discipline (Cohn, Schwaber & Sutherland *Scrum Guide*), not a
scientifically derived threshold. Apply with judgment, not mechanically.

> Example: "View planning grid" bundling day/week/month/semester/per-surgeon
> views fails Test 2 — split into one row per distinct view.

**Test 3 — System perspective (user-story phrasing?)**
*Anchored in: BABOK §10.22 Functional Decomposition (IIBA, 2015);
Cockburn goal-level distinction — *Writing Effective Use Cases* (2000)*

Ask: "Does this row describe what the *system does*, or what the *user can do*?"

- Rows starting with "Allow user to…", "Let the surgeon…", "Enable admin to…"
  are user-story phrasing — they belong in PRDs, not the FBS.
- Rephrase to system perspective: the subject is the system, the verb
  describes a system behaviour.
- Cockburn's goal-level model: user goals belong in use cases / user stories
  (sea-level); system functions belong in the FBS (fish/clam-level).

> ❌ "Allow surgeon to signal absence on a specific slot"
> ✅ "Absence signal intake and slot liberation"

### The attribute vs functionality rule

*Anchored in: Yourdon structured analysis — entity vs operation distinction
(Yourdon & DeMarco, *Structured Design*, 1979); Wiegers & Beatty,
*Software Requirements* 3rd ed. (2013) §feature granularity*

An **attribute** is a property of a data entity that always configures or
modifies alongside the entity itself. Attributes do not belong as separate
FBS rows — they belong as parenthetical annotations in the entity's
configuration row.

Common attribute mistakes:
- Separate rows for name, colour code, identifier, enabled/disabled status
  of the same entity → merge into one row
- Separate rows for "soft preference A" and "soft preference B" of the same
  entity when they are configured in the same UI interaction → merge

### The CRUD splitting rule

*Anchored in: RESTful resource design (Fielding, 2000); Wiegers & Beatty
(2013) §operation decomposition; BABOK §10.22 functional decomposition*

**Never merge Create, Update, and Delete into a single FBS row.** Each
CRUD operation has distinct business logic, distinct API contract, and
distinct test cases — they are independently testable and should be
independently deliverable.

**One row per CRUD operation on a significant entity:**

| Operation | FBS row naming | Example |
|---|---|---|
| Create | "Create [entity] ([key fields])" | "Create surgeon profile (name, specialty, contact, colour code)" |
| Update | "Update [entity]" | "Update surgeon profile" |
| Delete / Archive | "Deactivate / archive [entity]" | "Deactivate surgeon profile (archive without delete)" |
| List / Index | "List [entities] with [filter/sort]" | "List surgeons with search and filter" |
| Detail view | "Display [entity] detail" | "Display surgeon profile detail" |

**Exception — simple configuration entities:**
For configuration items with no significant business logic (e.g. a time
slot type with 2 fields, a room name), Create and Update may share a row
as "Configure [item]" when the form and validation are identical and the
operation has no side effects beyond persisting the value.

> ❌ "Create and maintain surgeon profile (name, specialty, contact, colour code, cabinet links, secretary associations)"
> — bundles Create + Update + association management in one row
>
> ✅ "Create surgeon profile (name, specialty, contact, colour code)"
> ✅ "Update surgeon profile"
> ✅ "Manage surgeon associations (cabinet links, secretary contacts)"
> ✅ "Deactivate surgeon profile (archive without delete)"

**Form field granularity:**
When an entity has a form with multiple distinct sections covering
different concerns, split by section — not by individual field.

> A surgeon profile form has two sections: identity (name, specialty,
> contact) and practice associations (cabinets, secretaries). These serve
> different use cases and may have different permissions → two rows.
> The individual fields within each section (name, specialty, email) are
> attributes of that section — not separate rows.

### The clustering rule — when source documents are provided

*Anchored in: BABOK §10.22 decomposition principle; NASA SP-2016-6105
§4.3 FBS — "functions needed, not elements of the architecture"*

When the user supplies source material (Excel, user stories, PRD draft,
interview notes), **do not translate rows 1:1**. Instead:

1. **Read all source rows** for a given capability before writing any FBS row.
2. **Group source rows by the system behaviour they describe.** Multiple user
   stories about the same underlying system action → one FBS row.
3. **Name the row from the system's perspective**, not the user story's.
4. **Parenthetical detail** (which attributes, which configurations) goes in
   the row name as a brief annotation, not as separate rows.

> Excel had 6 rows for surgeon profile fields (name, specialty, email, colour,
> cabinet, notes). The FBS gets 2 rows:
> "Create and maintain surgeon profile (identity, contact, colour, cabinet links)"
> and "Add operational notes to surgeon profile" — because notes is a
> meaningfully distinct interaction (free text, used differently by coordinators).

### Non-functional requirements do not belong in the FBS

*Anchored in: ISO/IEC 25010 (2023) quality model — functional vs
non-functional requirements are distinct; BABOK §10.22 scope boundary*

Security constraints, compliance obligations, and infrastructure requirements
(HTTPS enforcement, data residency, DPA management) are **not functionalities**
— they are system-wide quality attributes classified as non-functional
requirements under ISO/IEC 25010. They belong in ADRs, technical
specs, or compliance docs. Remove them from the FBS if found.

### Granularity sources

The three tests synthesise the following primary sources:

| Source | What it anchors |
|---|---|
| Wake, B. (2003). "INVEST in Good Stories, and SMART Tasks." XP123. https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/ | Tests 1 (Independent) and 2 (Small + Testable) |
| Cohn, M. (2004). *User Stories Applied.* Addison-Wesley. | Test 2 size ceiling; story sizing discipline |
| IIBA. (2015). *BABOK Guide* v3, §10.22 Functional Decomposition. | Tests 1, 3, clustering rule; system-perspective framing |
| Cockburn, A. (2000). *Writing Effective Use Cases.* Addison-Wesley. | Test 3; goal-level model (user vs system vs subfunction) |
| NASA. (2016). *Systems Engineering Handbook* SP-2016-6105 Rev 2, §4.3. | Clustering rule; FBS as function list, not architecture |
| Yourdon, E. & DeMarco, T. (1979). *Structured Design.* Prentice Hall. | Attribute vs functionality rule; entity/operation distinction |
| Wiegers, K. & Beatty, J. (2013). *Software Requirements* 3rd ed. Microsoft Press. | Attribute rule; feature granularity guidance |
| ISO/IEC 25010:2023. *Systems and software quality models.* | NFR exclusion rule; functional vs quality attribute boundary |

---

## Product canonical slug — the third identifier

Every **product** carries a canonical **`slug`** alongside its display name — a **stable + readable + short** kebab handle that tooling depends on (commit scopes today; anchors, config keys, code-module names tomorrow). **The FBS is the canonical home for product slugs.** The canonical definition + invariants live in the `metamodel` skill's `references/artefact-types-registry.yaml` § Canonical slugs (the `metamodel` skill's `references/artefact-types-registry.yaml`).

**Placement + format (exact — a generator parses it):** a backtick-wrapped code-line on its own line, immediately under the heading it names:
- the FBS **H1** (`# {{product_or_scope}} — Functional Breakdown Structure`) → the overall product/scope slug;
- for a **product-family FBS** (L0 axis = product/service family), each L0 product section heading (`## CN · {Product}`) → that product's slug.

The line's full content is `` `slug: <handle>` `` — one space after the colon, kebab handle, wrapped in backticks.

**Invariants:**
- **Kebab-case**, recommended **≤ 20 characters** (`[a-z0-9]` words joined by single hyphens).
- **Globally unique** across one flat namespace shared with the BC Map's L0 domain + L1 capability slugs — no product slug may collide with any capability slug (a commit-scope allowlist must be unambiguous). Scan before assigning: `grep -RohE '`slug: [a-z0-9-]+`' docs/product-specs/07a-fbs.md docs/business/03a-capability-map.md 2>/dev/null | sort`.
- **Mandatory** — the FBS H1 must carry one; it cannot be left blank.
- **Stable** — renaming is an **ID-rename** (breaks pinned consumers), never cosmetic. Propagate to all consumers and log in the changelog.
- **Consistency:** when a product is also an L0 item in the BC Map (product axis), its slug MUST be byte-identical in both docs — it is the same identifier.

**Assisted authoring:** auto-propose `slugify(product-name)`; if it exceeds 20 chars, flag it and suggest a shorter, still-meaningful handle. Show the author to accept or shorten; it is mandatory.

---

## The three modes of operation

### Mode 1 — Scaffold

**When:** the project has no FBS folder yet, or has one missing the canonical template.

**Output:** ONE file in `docs/product-specs/` (or project-chosen folder):
- `FBS.md` — hub document with intro, kit-link methodology pointer, L0 axis declaration, ASCII tree placeholder, empty per-capability sections.

Source from `references/template.md`. Substitute `{{product_or_scope}}` and `{{L0_axis_label}}` placeholders, and assign the **product slug** under the H1 (`{{product-slug}}`): auto-propose `slugify(product-name)`, flag > 20 chars with a shorter suggestion, confirm it does not collide with any BC Map capability slug. It is mandatory even in scaffold mode. Do NOT invent functionalities in scaffold mode.

**Do NOT** ship a project-side `methodology-references.md`. The canonical bibliography lives in the skill at `references/methodology-references.md` and is linked from the project doc's header.

### Mode 2 — Build structure (auto-import from BC Map)

**When:** the scaffold exists but the per-capability sections are empty.

**Process:**
1. **Read the BC Map** at `docs/business/03a-capability-map.md`. If absent, warn and ask whether to proceed with manual capability-list entry (degrades discipline — the FBS becomes the source of truth for capability names instead of soft-linking).
2. **Import L0 + L1 wholesale** — every L0 item from the BC Map becomes an L0 section in the FBS; every L1 capability becomes a `### C-N.M · {Name}` sub-section. **Product-family case** (L0 axis = product/service family): each L0 item *is* a product — carry its `` `slug: <handle>` `` line onto the FBS L0 section heading, byte-identical to the BC Map's L0 slug (same identifier). The FBS does not re-mint capability slugs; those stay owned by the BC Map.
3. **Render the ASCII tree** at the top of the FBS, mirroring the BC Map structure but adding a functionality-count placeholder per capability:
   ```
   {{product}}
   ├── C1 · {L0 name}
   │   ├── C1.1 · {Capability name}  (functionalities: _TODO_)
   │   └── C1.2 · {Capability name}  (functionalities: _TODO_)
   └── C2 · {L0 name}
       └── ...
   ```
4. **Pre-fill per-capability annotations** if present in the BC Map (or as `_TODO_` placeholders):
   - One-line capability summary (mirroring the BC Map's definition — kept short, references BC Map for full strategic prose)
   - Backend code paths (`_TODO_` initially)
   - Frontend code paths (`_TODO_` initially)
   - Empty functionality table

**Do NOT fully enumerate functionalities in structure mode.** Each capability table starts with one `_TODO_` placeholder row. Mode 3 fills it.

### Mode 3 — Add / update functionalities

**When:** the structure exists; the user wants to enumerate / update functionalities for one or more capabilities.

**Process:**
1. **Confirm the capability** (e.g., `C1.1` or "all of C1") the user wants populated.
2. **For each functionality, assign:**
   - **ID** — `C1.1.F01`, `C1.1.F02`, … (counter scoped under the capability; never reused or recycled even if a functionality is retired).
   - **Name** — short, function-oriented (verb-led OR noun phrase, but always describing *what the system does*, not what users do — see anti-patterns).
   - **Status** — `✅ Shipped` / `🔄 Planned` / `⬜ Backlog`. Default `⬜` when adding new rows; promote as work progresses.
   - **VS stage** (optional column) — `VS-N.M` link to value-streams.md, or `_TODO_` / `—` if value streams don't exist.
3. **For each capability section** (set once, refined over time):
   - **Backend code paths** — package/folder names where this capability's code lives.
   - **Frontend code paths** — page / component paths.
   - **One-line capability summary** — short reminder of what the capability does. **Do not** restate the BC Map definition.
4. **Run discipline checks** (see `references/fbs-discipline.md` §"Quality checks"):
   - No anti-patterns survived
   - Status reflects production reality (audit when in doubt)
   - No PRD / roadmap content crept in
   - Functionality counts are within sizing heuristics

---

## Hard scope rules — what does NOT belong in the FBS

Common scope violations and where the content actually belongs:

| Symptom | Belongs in |
|---|---|
| Capability definition / strategic prose | BC Map |
| Acceptance criteria, user stories | PRD |
| Sprint commitment, release date, milestone | Roadmap doc |
| Cycle time, latency target, throughput KPI | Process doc |
| Persona served, value proposition | Persona doc / Value-stream doc |
| Implementation plan, atomic increments | Implementation plan |
| Bug report, incident timeline | Issue tracker (Linear, Jira, GitHub) |

If you find yourself writing any of these in the FBS, pull the content into its proper home and add a soft-link from the FBS.

---

## Inputs

| Needed | What you ask if missing |
|---|---|
| **Project context location** | Look for `docs/product-specs/`. If unclear, ask. |
| **Mode** (scaffold / structure / fill) | Detect from request. Confirm if ambiguous. |
| **BC Map existence** | Check for `docs/business/03a-capability-map.md`. If absent, warn: structure mode will degrade to manual capability entry. Suggest running `business-capability-map` first. |
| **Scope name** | What product / product family / domain does this FBS cover? Used for `{{product_or_scope}}` substitution. |
| **Capability ID** (fill mode) | Which capability does the user want populated? Single ID or batch (e.g., "all of C1" or "C1.1, C1.2, C1.3"). |
| **Value-streams existence** | Check for `docs/business/04a-value-streams.md`. If absent, VS-stage column will be `_TODO_` placeholders. |

Ask 2–4 questions max, single message, lettered options where possible. Don't drag through a wizard.

---

## Output structure — the fixed template

The skill produces ONE markdown file at `{folder}/FBS.md` with this fixed structure (full template in `references/template.md`):

```
<!-- doc-version: 1.0 | created: YYYY-MM-DD -->

H1: {{product_or_scope}} — Functional Breakdown Structure

Intro paragraph:
  - What an FBS is (hybrid PBS+FBS framing)
  - Hard scope rules (no capabilities, no PRD content, no roadmap, no metrics)
  - Methodology kit-link pointer
  - Companion docs (BC Map, value-streams, PRDs, processes)

§Status legend — ✅ Shipped / 🔄 Planned / ⬜ Backlog

§L0 axis declaration — inherited from BC Map (chosen axis + rationale)

§Global overview — ASCII tree (L0 → L1 with functionality counts per capability)

§Per-L0 H2 section
  §§ Per-capability H3 section (C-N.M · {Name})
    - One-line capability summary (soft-link to BC Map by ID — DO NOT restate definition)
    - Backend: {paths or _TODO_}
    - Frontend: {paths or _TODO_}
    - Functionality table:
      | ID | Functionality | Status | VS stage |
      |---|---|---|---|
      | C-N.M.F01 | ... | ✅ | VS-2.3 |

Open items: no local section (ADR-0005). File unresolved work directly to the central
ledger via `util-open-items`, citing this FBS as `Source artefact` with `Source anchor` =
the capability or functionality ID (e.g. `#c21`, `#c21f03`) and `Source heading` = the
full heading text. Schema + lifecycle: the `metamodel` skill's `references/open-items-governance.md`.

Changelog
```

**Section count is fixed; ordering is fixed.** The ASCII tree + per-capability sections are mandatory.

- Open every generated file with the standard artefact frontmatter (OKF-superset block — set `type` to this artefact's `okf_type` display name from the `metamodel` skill's `references/artefact-types-registry.yaml`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`). Run `git config user.name` for `owner`. Set `status: draft` on initial scaffold. Default `review_interval: 90d`. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`.

---

## Sizing heuristics

| Level | Recommended count | Source |
|---|---|---|
| L0 items | 3–10 | Practitioner: "no more than ten domains, including the core product" + Miller 7±2 |
| L1 capabilities per L0 | 5–12 | Inherited from BC Map |
| L2 functionalities per capability | 5–25 | Practitioner heuristic; total can reach "a few hundred features for a grown-up product" |
| Total functionalities (FBS-wide) | 50–500 typical | Practitioner |

**Anti-explosion signals:**
- L2 going past 25 per capability → the capability is probably too coarse in the BC Map; consider splitting at the BC Map level
- L3 functionalities (sub-functionalities) emerging → you're mixing functionality with implementation detail; collapse back to L2 or move detail into PRDs
- Total >500 → the project may have outgrown a single FBS doc; consider splitting by L0 (one FBS per product / domain)

---

## Cross-reference — the architecture-artefact lifecycle

The FBS sits at the **tactical product-decomposition layer**, downstream of the strategic Business Architecture artefacts and upstream of feature delivery:

| Artefact | Owns | FBS relationship |
|---|---|---|
| **Personas** | Who the product serves | FBS doesn't link directly (value streams handle persona → capability traceability) |
| **Business Capability Map** | What abilities the business has | FBS soft-links UP by capability ID; never restates capabilities |
| **Value Streams** | How value flows persona → stages → capabilities | FBS optionally links each functionality to a VS stage |
| **Processes** | How operations happen | FBS doesn't link directly (processes operationalise capabilities, which FBS already links to) |
| **FBS** *(this skill)* | What the product does, status-tracked | — |
| **Use cases** | The actor↔system scenario (all paths) for a behaviour | A use case (`UC-NN`) *realises* one or more FBS functionalities — it adds the interaction the registry cannot hold; the FBS stays scenario-free |
| **PRD** | What we will build for one functionality slice | Per-PRD soft-link to the FBS functionality IDs it delivers |
| **Implementation plans** | How we will build it | Downstream of PRDs; no direct FBS link |

### Soft-reference principle

The FBS references other artefacts as pointers, not as dependencies. A scaffolded FBS must stand alone; cross-references add depth, not prerequisites. Build the FBS even if value streams / PRDs do not yet exist.

When linking, use stable IDs: `C1.1 ↔ value-stream VS-3.2 ↔ FBS functionality C1.1.F01 ↔ PRD-0042`. Make traceability mechanical.

---

## Common patterns to apply

1. **Functionalities are what the system does, not what users do.** "Validate email format" (functionality) ≠ "User enters email" (user story — PRD territory). The system-perspective phrasing prevents PRD/story creep.

2. **Status reflects production reality.** ✅ means "shipped and in production". If a feature is shipped behind a flag, mark it 🔄 with a note. If a feature was shipped then rolled back, mark ⬜ and add changelog. Status drift between FBS and prod is the #1 hygiene failure.

3. **One FBS row = one atomic functionality.** "Search + filter + sort" should be three rows, not one row that mixes them. The atomicity lets PRDs target one row precisely.

4. **Soft-link to BC Map, never restate.** Each capability section has a one-line summary AND a link to the BC Map row. The one-liner is a reminder, not a definition. Definitions live in the BC Map.

5. **Code paths are capability-level, not functionality-level.** Listing every functionality's exact file paths is noise; listing the package/folder per capability tells engineers where to look. Practitioner experience shows capability-level is the right granularity.

6. **VS-stage links are optional but illuminating.** When filled, the FBS becomes a traceability surface: stakeholder → value stream → stage → capability → functionality. Without VS links, the FBS is still useful as a registry — just less traceable.

7. **Retired functionalities stay in the FBS with `⬜` and a changelog note.** Don't delete history. "We used to do X" is institutional memory.

8. **The FBS is one doc per project scope.** A single product → one FBS. A product family → still one FBS, organised by product at L0. If you want per-product FBSs, the scope is wrong; widen.

9. **Status promotion is the most common edit.** ⬜ → 🔄 when a PRD commits the work; 🔄 → ✅ when the PRD ships. The skill should make this edit fast.

10. **Comments / rationale belong in the changelog, not in the row.** Functionality rows stay terse; *why* a functionality was added/changed lives in the changelog at the bottom.

---

## Finding the right folder

Default: `docs/product-specs/`. Alternatives:
- `docs/architecture/functional-breakdown-structure/` when architecture artefacts have their own root.
- `docs/<domain>/functional-breakdown-structure/` when scoped narrowly.

**Always check for an existing folder first:**

```bash
find docs -type d -iname "*functional*" -o -type d -iname "*fbs*" 2>/dev/null
```

If a folder exists at a non-default location, use it — don't move existing work without an explicit user request. If multiple candidates exist, ask. If none, default to `docs/product-specs/` and confirm.

**Never overwrite an existing `FBS.md`.** Switch modes if it exists:
- Scaffold mode → skip (report what's there).
- Structure mode → only fill empty capability sections; preserve existing ones.
- Fill mode → append/update rows in the targeted capability table.

---

## Reference materials

Three files in `references/` carry the canonical content. Read when needed:

- **`references/template.md`** — the canonical `FBS.md` skeleton. Copy to `{folder}/FBS.md` and fill placeholders.
- **`references/methodology-references.md`** — canonical bibliography (BABOK §10.22, NASA FBS, NASA WBS Handbook, TOGAF, Hackernoon practitioner guide). **Lives only in the kit** — never copied to projects. Project docs link here via the 2-line pointer in their header.
- **`references/fbs-discipline.md`** — internal Claude guidance: 6 anti-patterns, capability-vs-functionality-vs-feature decision tree, status-drift detection, sizing heuristics. Never copied into the project.

---

## Closing report to the user

After running any mode, summarise in 4–6 lines:

1. **Mode executed** + **files created or updated** with paths.
2. **L0 / L1 inheritance** — confirm count imported from BC Map (or note absence).
3. **Functionalities filled vs `_TODO_`** — counts per capability.
4. **Status distribution** (fill mode) — how many ✅ / 🔄 / ⬜ so the user sees the current shipping picture.
5. **Anti-pattern check** — explicit confirmation that no PRD / roadmap / capability-definition content leaked in.
6. **Cross-link opportunities** — value streams + PRDs the FBS should soft-link to.

---

## Checklist

Before declaring the work done:

- [ ] Folder exists or was created.
- [ ] `FBS.md` exists with intro + L0 axis + ASCII tree + per-capability sections (scaffold mode).
- [ ] Product slug present — `` `slug: <handle>` `` under the H1 (and under each L0 product section for a product-family FBS); well-formed kebab (≤ 20 chars) and **globally unique** across the FBS product slugs + BC Map L0/L1 slugs (one flat namespace).
- [ ] Methodology pointer in `FBS.md` header links to the kit's canonical bibliography.
- [ ] L0 / L1 imported from BC Map (or manual entry flagged in changelog).
- [ ] Each functionality has ID (`C-N.M.F01` pattern), name, status; optional VS-stage / code paths populated where applicable.
- [ ] No capability definitions, PRD content, or roadmap detail leaked in.
- [ ] Sizing heuristics respected (L2 ≤ 25 per capability; total ≤ ~500).
- [ ] No project-specific terms baked in (kit version).
- [ ] Closing report delivered.
