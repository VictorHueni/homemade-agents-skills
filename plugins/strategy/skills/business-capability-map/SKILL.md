---
type: skill
name: business-capability-map
description: "Create a strategic business capability map (L0 + L1, optionally L2) using the canonical synthesis of TOGAF G189 + Cutter Rosetta Stone + SAP Business Architecture + BABOK. Use when the user asks to build a capability map, define business capabilities, model the WHAT-the-business-does layer, scaffold an enterprise / product capability tree, or prepare a business-IT alignment artefact. Triggers on: business capability map, capability map, BC map, BCM, define capabilities for, what does {product} do, strategic capabilities, TOGAF capability map, capability decomposition, L0 L1 capabilities. Domain-agnostic; works for any product, service, or enterprise scope. Stays strategic — does NOT decompose to features / functionality (that belongs in an FBS)."
version: "1.0.0"
user-invocable: true
allow_implicit_invocation: true
impact: "low"
metadata:
  category: "specification"
  complexity: "medium"
status: active
last_reviewed: 2026-05-29
---

# Business Capability Map Builder

You are an expert at producing **strategic Business Capability Maps (BC Maps)** — TOGAF-aligned, domain-agnostic artefacts that answer one question: *"what does this business / product / service actually do?"* — expressed as a stable hierarchy of capabilities, independent of the technology, organisation, or processes that realise them.

The artifact produced by this skill is **a markdown document** in the project's business-architecture folder (default `docs/business/`, adapt to project convention). It is NOT a feature backlog, NOT a process diagram, NOT an org chart — it is **the strategic "what" layer** that other architecture artefacts (FBS, value streams, processes, personas) soft-reference by capability ID.

The capability map is one of the four canonical **Business Architecture artefacts** (BIZBOK / TOGAF), alongside personas, value streams, and business processes — which is why they all sit together under `docs/business/`.

This skill is **domain-agnostic**. The template patterns work for any product, service, or enterprise. When activated inside a project, the skill picks up the project's own naming, scope, and existing artefacts.

---

## What a "good Business Capability Map" means

A BC Map is good when a reader can answer, without ambiguity:

| Question | Where it lives |
|---|---|
| **What is the organising axis (L0)?** | §L0 axis declaration + rationale |
| **What does the business do at L0?** | §Global overview (ASCII tree) + §Capability index (table) |
| **What is the stable tooling handle for a domain / capability?** | Per-heading `` `slug: <handle>` `` code-line (third identifier, globally unique) |
| **What does each L1 capability mean precisely?** | §L1 capability definitions (one block per L1) |
| **Which capabilities are strategic differentiators vs commodity?** | Strategic Importance column + per-capability field |
| **What is each capability NOT?** | Per-capability §Boundaries field (anti-overlap discipline) |
| **Which personas / value streams / processes consume each capability?** | Per-capability soft-link footer |

**Hard scope rule:** the BC Map stops at L1 (with L2 only for genuinely extensive sub-domains). **Features, functionalities, user stories, and code-organisation hints do NOT belong here** — they live in the FBS (Functional Breakdown Structure), a peer artefact. If you find yourself writing "the system shall…" or naming a backend module, you have crossed into FBS territory; stop.

---

## The three modes of operation

The skill operates in one of three modes. Detect from the user's prompt; ask if ambiguous.

### Mode 1 — Scaffold

**When:** the project has no BC Map folder yet, or has one but is missing the template + methodology references.

**Output:** ONE file in the project's chosen folder:
- `03a-capability-map.md` — the hub doc (intro + kit-link methodology pointer + axis declaration + tree + index + per-capability blocks + changelog).

Source from `references/template.md`. Substitute `{{product_or_scope}}`, `{{L0_axis_label}}` placeholders. Do NOT invent capabilities in scaffold mode — leave the tree as a `_TODO_` skeleton.

**Do NOT** ship a project-side `methodology-references.md`. The canonical bibliography lives in the skill at `references/methodology-references.md` and is linked from the project doc's header. Single source of truth; no drift across projects.

### Mode 2 — Build the L0/L1 structure

**When:** the scaffold exists but the tree + index are empty.

**Step 0 — Clarifying questions (ask BEFORE generating)**

Ask the user the following 4 questions in a single message with lettered options. Users respond like `1A, 2C, 3D, 4B`:

```text
1. What is your L0 (top-level) organising axis?
   A. Product / Service family — multi-product company
   B. Value stream — customer-journey-driven business
   C. Capability domain / theme — enterprise-wide neutral (TOGAF default)
   D. Line of business — true conglomerate with distinct LOBs
   E. Customer segment — segment-led business
   F. Other: [please specify your axis + rationale]

2. What is the scope of this capability map?
   A. Single product or service
   B. Product family (multiple products under one company)
   C. Enterprise-wide (the whole organisation)
   D. Single LOB / domain (slice of larger org)

3. How should L1 capabilities be discovered?
   A. Top-down — leadership / vision-driven; I'll provide capabilities
   B. Bottom-up — discover from existing PRDs / project docs (read context)
   C. Hybrid — top-down framework + bottom-up validation
   D. Industry reference model (BIAN, APQC PCF, or similar) — please name

4. Strategic Importance assessment timing?
   A. Assign now (Differentiator / Necessary / Commodity per L1)
   B. Leave as _TODO_; assign in fill mode later
```

If the user gives "Other" or pushes back, ask one follow-up to clarify, then proceed.

**Process:**
1. **Make the L0 axis decision** (most consequential choice — see "L0 axis anchor decision" below). Record the chosen axis and one-sentence rationale in the doc.
2. **Read project context** — PRD(s), product roadmap, FBS if it exists, personas backlog, processes, business-analysis docs. The L1 list must derive from this, not from generic templates.
3. **Generate L0 items** — between 3 and 8 (Miller's 7±2; Cutter cognitive load). If more than 8 L0 items emerge, the axis is wrong — re-pick at a higher level.
4. **Generate L1 capabilities per L0** — between 5 and 12 per L0. Aim for ≤25 L1 capabilities total across the map (Cutter Rosetta Stone recommendation).
5. **Apply the Cooper noun test** (see `references/capability-discipline.md`): every capability name must be a noun phrase ("Customer Onboarding", not "Onboard the Customer"). If you wrote a verb, you have a process, not a capability.
6. **Apply the anti-overlap test:** no two capabilities should overlap in scope. Each capability appears once and only once in the map (Cutter's "redundancy" mistake).
7. **Decide L2 per L1:** only break out L2 if an L1 has ≥5 genuinely distinct sub-capabilities. Default is no L2.
8. **Render the ASCII tree** + populate the **Capability Index table** with: ID · Name · L0 parent · Strategic Importance · One-line definition. Initial Strategic Importance can be `_TODO_` — it's a deliberate exercise.
9. **Assign a canonical slug to every L0 domain and L1 capability** (see "Canonical slug — the third identifier"). Auto-propose `slugify(name)`, flag any proposal > 20 chars with a shorter suggestion, and confirm each with the author — the slug is mandatory. Write the `` `slug: <handle>` `` code-line immediately under each L0 (`## CN · …`) and L1 (`### CN.M · …`) heading. Before assigning, scan existing slugs across the map **and** the FBS to guarantee global uniqueness.

**Do NOT fully fill each capability definition in structure mode.** The tree + index + slugs are the planning artifact; full per-capability blocks are mode 3.

### Mode 3 — Fill capability definitions

**When:** the tree + index exist; the user wants per-capability blocks filled.

**Process:**
1. **Pick the capability ID** the user wants filled (e.g., `C3.2`), or batch-fill an L0 branch.
2. **For each capability, fill the canonical block** (see `references/template.md`):
   - **Slug** — the `` `slug: <handle>` `` code-line directly under the heading. If missing (older map), assign one now: auto-propose `slugify(name)`, flag > 20 chars with a shorter suggestion, confirm global uniqueness across the map + FBS. Mandatory. See "Canonical slug — the third identifier".
   - **Name** (already in the tree — restate for navigability)
   - **Definition** — 1–2 sentence outcome statement. Business language, no jargon. Start with the verb "Provides…" or "Enables…" or the noun phrase + active outcome.
   - **Business object** — the entity the capability operates on (Customer, Order, Claim, Invoice, Risk, Asset…). One noun.
   - **Strategic importance** — `Differentiator` / `Necessary` / `Commodity` (high / medium / low). Include a one-line rationale.
   - **Outcomes** — 2–4 bullets describing what the capability produces or enables. Outcome-oriented, not activity-oriented.
   - **Boundaries** — 2–3 bullets describing what the capability does NOT cover (anti-overlap discipline; helps the reader understand the edges).
   - **Maturity (optional)** — `Initial / Developing / Defined / Managed / Optimising` (CMM-style). Skip if the project isn't ready to assess.
3. **Soft-links footer** — populate ONLY links to artefacts that actually exist:
   - Personas served (link by persona ID from `01a-personas.md`)
   - Value streams enabled (link by VS ID if value-stream doc exists)
   - Processes that operationalise it (link to `docs/business/05a-processes/*.md`)
   - FBS row (link to the same capability ID in the FBS if it exists)

**Run the discipline checks** in `references/capability-discipline.md` §"Quality checks" before declaring a capability complete.

---

## L0 axis anchor decision

The L0 organising axis is the most consequential choice in the BC Map. It shapes how every reader navigates the doc and what mental model they leave with. The skill MUST surface this choice to the user; don't pick silently.

### Common L0 axis options

| Axis | When to pick | Trade-off |
|---|---|---|
| **Product / Service family** | Multi-product company; products are the natural strategic unit | Capabilities may be duplicated across products if not careful; risks Cutter's "multiple maps" mistake at the macro level |
| **Value stream** | Customer-journey-driven business; one capability map serves many products | Forces customer-outcome thinking; can feel abstract for engineering teams |
| **Capability domain / theme** | Enterprise-wide scope, no clear product axis (e.g., "Customer-facing", "Operations", "Compliance", "Finance") | TOGAF-classic; widely understood; abstract |
| **Line of business (LOB)** | Holdings / conglomerate with distinct LOBs (e.g., banking + insurance + asset management) | Cutter warns against confusing LOB with capability — only valid when LOBs ARE structurally distinct businesses |
| **Customer segment** | Segment-led business (B2C / B2B / B2G with very different capability needs per segment) | Can become "multiple maps"; only valid when segments demand structurally different capabilities |
| **Geography** | Federated multi-jurisdiction operations | Rare as primary axis; usually a secondary dimension |
| **Custom** | None of the above fits; the project has a strong organising principle of its own | Document the choice + rationale carefully; future readers must understand why |

### How to surface the choice

Ask: *"What is the natural organising axis for this BC Map? Your options include: (a) product/service family, (b) value stream, (c) capability domain, (d) line of business, (e) customer segment, (f) custom. What strategic unit does the business think in?"* Record the choice + a one-sentence rationale in the doc's §L0 axis declaration.

If unsure, **default to "capability domain / theme"** (TOGAF-classic) — it's the most defensible neutral choice. Document why this default was used so the user can change it later.

---

## Inputs

| Needed | What you ask if missing |
|---|---|
| **Project context location** | Look for `docs/business/`, `docs/architecture/`, or equivalent. If unclear, ask. |
| **Mode** (scaffold / structure / fill) | Detect from request. Confirm if ambiguous. |
| **Scope name** | What is this BC Map for? A product family? An enterprise? A single product? Required for `{{product_or_scope}}` substitution. |
| **L0 axis** (mode 2 only) | The 7-option anchor decision above. Don't proceed without an explicit choice. |
| **Existing artefacts** | "Are there PRD / personas / FBS / process docs the BC Map should soft-link to?" |

Ask 2–4 questions max, single message, lettered options where possible.

---

## Capability ID convention

IDs follow the `C-N.M` format — the same ID must be used consistently across every artefact that references a capability (FBS, value streams, processes, PRDs, domain model).

| Level | Format | Examples |
|---|---|---|
| L0 | `C{N}` | `C1`, `C2`, `C3` |
| L1 | `C{N}.{M}` | `C1.1`, `C1.2`, `C3.4` |
| L2 (rare) | `C{N}.{M}.{K}` | `C1.1.1`, `C3.4.2` |

**Assignment rule:** scan existing IDs in the capability map (`grep "C[0-9]" docs/business/03a-capability-map.md`) before assigning. Take the next integer at each level. IDs are permanent once assigned — never renumber, even if a capability is deprecated. L2 is only added when an L1 has ≥5 genuinely distinct sub-capabilities.

---

## Canonical slug — the third identifier

Every **L0 domain** and **L1 capability** carries a canonical **`slug`** alongside its ID (`C-N.M`) and display name. Where the ID is stable-but-cryptic and the name is readable-but-long-and-unstable, the slug is the missing third: **stable + readable + short** — the handle tooling actually depends on (commit scopes today; anchors, config keys, and code-module names tomorrow). The canonical definition + invariants live in the `metamodel` skill's `references/artefact-types-registry.yaml` § Canonical slugs (the `metamodel` skill's `references/artefact-types-registry.yaml`).

**Placement + format (exact — a generator parses it):** a backtick-wrapped code-line on its own line, immediately under the entity's heading, before any prose field:

```
### C1.2 · Catalog Maintenance
`slug: catalog-maintenance`

**Definition.** …
```

The line's full content is `` `slug: <handle>` `` — a single space after the colon, the kebab handle, wrapped in backticks. It is deliberately visually distinct from the `**Bolded.**` prose fields because it is a machine identifier, not strategic prose.

**Invariants (these make it an identifier, not a label):**
- **Kebab-case**, recommended **≤ 20 characters** (`[a-z0-9]` words joined by single hyphens; no leading/trailing/double hyphens).
- **Globally unique** across one flat namespace shared by *all* L0 domains, *all* L1 capabilities in this map, **and** all products in the FBS — a commit-scope allowlist must be unambiguous. Before assigning, scan existing slugs across both docs: `grep -RohE '`slug: [a-z0-9-]+`' docs/business/03a-capability-map.md docs/product-specs/07a-fbs.md 2>/dev/null | sort`.
- **Mandatory** — every L0 and L1 heading must carry one; it cannot be left blank.
- **Stable** — renaming a slug is an **ID-rename** (it breaks every consumer that pinned the old handle: commit-scope allowlists, anchors, config keys), never a cosmetic edit. Change it only deliberately, propagate to all consumers, and record it in the changelog.

**Assisted authoring:** in structure/fill mode, auto-propose `slugify(display-name)` (lowercase, strip accents, non-alphanumerics → hyphen, collapse repeats). Show the author the proposal to accept or shorten; it is mandatory. **If the proposed slug exceeds 20 characters, flag it and suggest a shorter, still-meaningful handle** (e.g. `customer-data` for "Customer Data Management", not the 24-char `customer-data-management`).

---

## Output structure — the fixed template

- Open every generated file with the standard artefact frontmatter (OKF-superset block — set `type` to this artefact's `okf_type` display name from the `metamodel` skill's `references/artefact-types-registry.yaml`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`). Run `git config user.name` for `owner`. Set `status: draft` on initial scaffold. Default `review_interval: 180d`. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`.

The skill produces ONE markdown file at `docs/business/03a-capability-map.md` with this fixed structure (full template in `references/template.md`):

```
<!-- doc-version: 1.0 | created: YYYY-MM-DD -->

H1: {{product_or_scope}} — Business Capability Map

Intro paragraph:
  - What a BC Map is, why it exists
  - Hard scope rule: L0+L1 only (L2 if extensive), no features/functionality
  - Methodology pointer (2-line blockquote linking to the skill's canonical bibliography in the kit)
  - Companion docs (FBS, personas, value streams, processes)

§L0 axis declaration
  - Chosen axis (product / value-stream / capability-domain / LOB / segment / geo / custom)
  - One-sentence rationale
  - List of L0 items

§Global overview — ASCII tree
  - L0 → L1 (→ L2 only if extensive)

§Capability index — table
  - Columns: ID | Name | L0 parent | Strategic Importance | One-line definition

§L0 sections (one H2 per L0 item)
  §§ L1 capability definitions (one H3 per L1)
    - Name
    - Definition (1-2 sentences)
    - Business object
    - Strategic importance + rationale
    - Outcomes (2-4 bullets)
    - Boundaries (anti-overlap)
    - Maturity (optional)
    - Soft-links (personas / value streams / processes / FBS row)
    §§§ L2 if applicable

Open items: no local section (ADR-0005). File unresolved work directly to the central
ledger via `util-open-items`, citing this map as `Source artefact` with `Source anchor` =
the capability ID (e.g. `#c1`, `#c12`) and `Source heading` = the full capability heading.
Schema + lifecycle: the `metamodel` skill's `references/open-items-governance.md`.

Changelog
```

**Section count is fixed; ordering is fixed.** The ASCII tree + capability index are mandatory and must be at the top; per-capability blocks follow.

---

## The capability-discipline tests are the doc's defence

Three discipline tests are the difference between a real BC Map and a relabelled feature list. **Run all three before declaring any capability complete:**

1. **The noun test (TOGAF + Cesar Gonzalez):** capability name is a noun phrase. "Customer Onboarding" is a capability; "Onboard Customers" is a process. If the name has a leading verb or sounds like an action, it's not a capability.

2. **The technology-independence test (TOGAF):** the capability name does not contain any technology, vendor, system, or tool. "Order Management" is a capability; "Salesforce Integration" is a system. If the name would change when you swap a tool, it's a system or function, not a capability.

3. **The anti-overlap test (Cutter):** the capability does not overlap with any other capability in the map. Each capability appears once and only once. If two capabilities seem to cover the same territory, merge them or split them differently — but never duplicate.

Full guidance in `references/capability-discipline.md`.

---

## Sizing heuristics (TOGAF + Cutter + Miller)

| Level | Recommended count | Why |
|---|---|---|
| L0 | 3–8 items | Miller's 7±2 cognitive limit; Cutter macro-level memorability |
| L1 | 5–12 per L0; ≤25 total | Cutter: "15-25 foundation capabilities span the enterprise" |
| L2 | Only when an L1 has ≥5 genuinely distinct sub-capabilities | TOGAF: deeper levels for transformation initiatives, not for completeness |

**If any level exceeds the recommended count,** reconsider:
- Too many L0 items → axis is too granular, lift one level
- Too many L1 per L0 → some L1s are actually L2s nested incorrectly, or two L0s have been collapsed
- Many L2s needed everywhere → the scope is too big for one BC Map; split into multiple maps by L0 axis

---

## Cross-reference — the architecture-artefact lifecycle

A BC Map is one of several architecture artefacts that describe a product / business:

| Artefact | Owns | This skill's relationship |
|---|---|---|
| **BC Map** *(this skill)* | The strategic "what" — capabilities, L0+L1 hierarchy, strategic importance | — |
| **Personas** | Who the product serves | BC Map soft-links: which personas each capability serves |
| **Value Streams / Journeys** | How value flows from trigger to outcome per persona | BC Map soft-links: which value streams each capability enables |
| **Business Processes** | The operational "how" — actors, activities, data, KPIs | BC Map soft-links: which processes operationalise each capability |
| **FBS (Functional Breakdown Structure)** | The product-decomposition "how it's built" — products → capabilities → functionalities | **Peer artefact.** Same capability IDs. BC Map = strategic prose; FBS = tactical features + status + code paths. Do NOT duplicate the L0/L1 content between docs — link instead. |
| **PRD** | The feature spec for one capability slice | Far downstream — never appear in BC Map |

### Soft-reference principle

The BC Map references other artefacts *as pointers, not as dependencies*. A BC Map must stand alone; cross-references add depth, not prerequisites. The BC Map should ship even if personas / value streams / processes / FBS do not yet exist.

When linking, prefer **capability ID + artefact-row ID** (`C3.2 ↔ persona P-02 ↔ value-stream VS-3 ↔ process {process-slug}-process.md ↔ FBS row C3.2`). Make traceability mechanical.

### The BC-Map ↔ FBS pairing

When both BC Map and FBS exist for the same product/scope:
- **Capability IDs match** across both docs (`C3.2` in BC Map = `BC3.2` or `C3.2` in FBS — pick one convention and use it consistently across docs).
- **BC Map owns:** strategic importance, business object, outcomes, boundaries, soft-links.
- **FBS owns:** functionalities under each capability, status (✅/🔄/⬜), backend/frontend code paths.
- **Neither duplicates the other's content.** If a fact lives in BC Map, FBS links to it. If a fact lives in FBS, BC Map does not mirror it.

---

## Common patterns to apply

1. **Lead with the L0 axis decision.** The whole document inherits the consequences of this choice — make it visible.

2. **One capability = one noun phrase.** The format "Business Object + Noun" (TOGAF / Gonzalez) works almost always: "Customer Management", "Risk Assessment", "Order Fulfilment", "Claim Adjudication".

3. **Strategic importance is a real exercise, not a column to populate quickly.** Differentiator = where the business wins or loses. Necessary = required for operation but not a winning edge. Commodity = could be outsourced / templated without strategic loss. Most capabilities are Necessary; a healthy BC Map has 3–6 true Differentiators.

4. **Boundaries beat completeness.** Telling the reader what a capability does NOT cover prevents scope creep more effectively than enumerating everything it does. 2 sharp boundaries > 10 fuzzy outcomes.

5. **Anti-overlap is structural, not cosmetic.** Two capabilities with overlapping outcomes will silently create two of every downstream artefact. Merge or split — never leave both standing.

6. **Capability ≠ Process ≠ Function ≠ Org Unit.** Use the noun test (verb/sequence = process; activity grouping by skill = function; people = org unit) to keep the boundaries clean.

7. **The map is one map, for the whole scope.** Cutter's third mistake — "creating multiple maps" — is the single most common failure. If different stakeholders want different maps, the scope is wrong; either widen the BC Map to cover both or split it into different scopes upfront.

8. **L0 product-axis is acceptable but watch for cross-product capability bleed.** When L0 = products, the same capability may appear under multiple products. Decide upfront: (a) duplicate (with cross-references) for navigability, or (b) hoist shared capabilities to a "Platform" L0 item. Option (b) is cleaner.

9. **L2 is the exception, not the rule.** Resist the temptation to "be thorough" by adding L2 everywhere. L2 belongs in the FBS as functionalities, not in the BC Map.

10. **Maturity is optional and political.** Heat-mapping maturity is powerful but requires honest organisational self-assessment. Only fill if the team is ready; otherwise leave `_TODO_` or omit the field.

---

## Finding the right folder

**Default:** `docs/business/` — aligns the capability map with the other Business Architecture artefacts (personas, value streams, processes).

**Always check for an existing folder first:**

```bash
find docs -type d -iname "*capabilit*" 2>/dev/null
```

If a folder exists at a non-default location, use it — don't move existing work without an explicit user request. If multiple candidates exist, ask. If none exists, default to `docs/business/` and confirm with the user.

**Never overwrite an existing `03a-capability-map.md`.** Switch modes if it exists:
- Scaffold mode → skip (report what's there).
- Structure mode → only fill empty tree/index; preserve existing capabilities.
- Fill mode → append/update per-capability blocks; preserve existing content.

---

## Reference materials

Three files in `references/` carry the canonical content. Read when needed:

- **`references/template.md`** — the canonical `03a-capability-map.md` skeleton. Copy to `docs/business/03a-capability-map.md` and fill placeholders.
- **`references/methodology-references.md`** — the canonical bibliography (TOGAF G189, Cutter, SAP, BABOK, Gonzalez naming, Miller sizing). **Lives only in the kit** — never copied to projects. Project docs link here via the 2-line pointer in their header.
- **`references/capability-discipline.md`** — internal Claude guidance: noun test, technology-independence test, anti-overlap test, capability-vs-process-vs-function-vs-unit decision tree, common mistakes from Cutter. Never copied into the project.

---

## Closing report to the user

After running any mode, summarise in 4–6 lines:

1. **Mode executed** + **files created or updated** with paths.
2. **L0 axis chosen** + rationale (for structure mode).
3. **Sizing summary** — L0 count, L1 count per L0, any L2 sub-trees.
4. **Discipline check results** — confirm the noun test / tech-independence test / anti-overlap test all pass for what was filled. Flag any capability that needed compromise.
5. **Cross-link opportunities** — which artefacts (personas, FBS, processes, value streams) exist that the BC Map should soft-link.

Keep it short. Point the user at the next move.

---

## Checklist

Before declaring the work done:

- [ ] Folder identified or created (with user confirmation if new).
- [ ] `03a-capability-map.md` exists (scaffold mode).
- [ ] Methodology pointer in `03a-capability-map.md` header links to the kit's canonical bibliography (NOT a local methodology-references.md).
- [ ] L0 axis explicitly chosen + rationale documented (structure / fill mode).
- [ ] ASCII tree + Capability Index table populated (structure mode).
- [ ] L0 count: 3–8. L1 count per L0: 5–12. L1 total: ≤25.
- [ ] Every capability passes the noun test, tech-independence test, anti-overlap test.
- [ ] Every L0 domain and L1 capability carries a `` `slug: <handle>` `` code-line under its heading (mandatory; structure / fill mode).
- [ ] All slugs are well-formed kebab-case (recommended ≤ 20 chars) and **globally unique** across the map's L0 + L1 slugs *and* the FBS product slugs (one flat namespace).
- [ ] Per-capability blocks filled with Definition + Business object + Strategic importance + Outcomes + Boundaries (fill mode).
- [ ] Soft-links populated only when target artefact exists.
- [ ] No features / functionalities / code paths leaked into the BC Map (scope discipline).
- [ ] No project-specific terms baked into anything reusable in the kit version.
- [ ] Closing report delivered.
