# arc42 §3 — Context and Scope (embedded reference)

Extracted from the arc42 v9.0 template (July 2025). Use as the authoritative spec when writing `docs/architecture/arc42/03-context.md`.

Upstream: [docs.arc42.org/section-3](https://docs.arc42.org/section-3/).

---

## Contents

> Context and scope — as the name suggests — delimits your system (i.e. your scope) from all its communication partners (neighboring systems and users, i.e. the context of your system). It thereby specifies the external interfaces.
>
> If necessary, differentiate the business context (domain specific inputs and outputs) from the technical context (channels, protocols, hardware).

## Motivation

> The domain interfaces and technical interfaces to communication partners are among your system's most critical aspects. Make sure that you completely understand them.

## Form

> Various options:
> - Context diagrams
> - Lists of communication partners and their interfaces.

---

## §3.1 — Business Context

### Contents

> Specification of **all** communication partners (users, IT-systems, …) with explanations of domain specific inputs and outputs or interfaces. Optionally you can add domain specific formats or communication protocols.

### Motivation

> All stakeholders should understand which data are exchanged with the environment of the system.

### Form

> All kinds of diagrams that show the system as a black box and specify the domain interfaces to communication partners.
>
> Alternatively (or additionally) you can use a table. The title of the table is the name of your system, the three columns contain the name of the communication partner, the inputs, and the outputs.

**Kit application:** the C4 System Context diagram (`systemContext.svg`) is the black-box diagram; the kit always pairs it with a three-column table below, one row per communication partner.

---

## §3.2 — Technical Context

### Contents

> Technical interfaces (channels and transmission media) linking your system to its environment. In addition a mapping of domain specific input/output to the channels, i.e. an explanation which I/O uses which channel.

### Motivation

> Many stakeholders make architectural decision based on the technical interfaces between the system and its context. Especially infrastructure or hardware designers decide these technical interfaces.

### Form

> E.g. UML deployment diagram describing channels to neighboring systems, together with a mapping table showing the relationships between channels and input/output.

**Kit application:** the C4 model captures channel + protocol per relationship via the `technology` argument on `->` relationships. The arc42 §3.2 table extracts these into columns `Communication Partner / Channel / Protocol / Format`. No separate UML diagram is rendered — the System Context SVG suffices.

---

## Kit-specific rules for §3

1. **One System Context diagram per `SYS-NN`.** The kit only produces a context view for the primary system being documented. If multiple SYS-NN exist in the workspace, decide which is "the system being documented" — the others are external systems from §3's perspective.

2. **All Tier-1 personas from `business-persona` appear as actors.** If `docs/business/01a-personas.md` exists, the context view reuses `P-NN` IDs (DSL identifiers `P_NN`). Tier-2 and Tier-3 personas only appear if they are direct communication partners of the system.

3. **External systems are tagged `external`** in the DSL — drives the grey-out styling.

4. **Every relationship carries a `technology` field.** The §3.2 table is generated from this — empty technology fields make §3.2 unfillable.

5. **The §3 markdown file is overwritten on each `context` mode invocation** — not appended. The context view is the canonical single source for actors + external systems; subsequent edits regenerate it.

---

## Acceptance criteria — when §3 is "done"

- [ ] `docs/architecture/arc42/03-context.md` exists with standard frontmatter (see `rules/artefact-frontmatter.md`)
- [ ] §3.1 Business Context contains the embedded `systemContext.svg` + a table with ≥1 row per communication partner
- [ ] §3.2 Technical Context contains a channels + protocols table (one row per relationship)
- [ ] At least one Tier-1 persona appears as an actor (P-NN); if no persona file exists, document why
- [ ] No internal containers / components / aggregates appear in §3 (those belong to §5)
- [ ] All listed partners have ≥1 input or output specified (an empty row signals a discovery gap → file a `doc-gap` row to the central ledger)
