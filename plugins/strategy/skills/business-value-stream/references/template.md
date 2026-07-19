<!-- doc-version: 1.0 | created: {{YYYY-MM-DD}} -->

# {{product_or_scope}} — Value Streams

This document is the strategic value-flow layer for {{product_or_scope}}:
the catalogue of value streams (TOGAF + BIZBOK tradition) describing **how
value flows** from a triggering stakeholder, through a sequence of stages,
to a delivered value proposition. Each stage soft-links to the capabilities
it consumes and the processes that operationalise it.

> **Methodology:** built using the canonical synthesis of [TOGAF Value Streams Guide + BIZBOK + Ulrich/Kuehn practitioner framing + Millett journey-vs-stream distinction](https://github.com/VictorHueni/homemade-claude-kit/tree/main/business-value-stream/references/methodology-references.md). The full bibliography lives with the skill — single source of truth across every project.
>
> **Stance:** EA value streams (strategic, stage-based, capability-consuming) — NOT Lean VSM (operational cycle-time analysis). See the methodology reference for the full distinction.

**Triangulation rule:**
```
Persona (who)
   │ triggers
   ▼
Value stream (how value flows to that who)
   │ stages consume
   ▼
Capabilities (what abilities)
   │ operationalised by
   ▼
Processes (how it operationally happens)
```

**Companion documents:**
- Personas: [link to 01a-personas.md if exists]
- Business Capability Map: [link to 03a-capability-map.md if exists]
- Business Processes: [link to 05a-processes/ if exists]

**Hard rules:**
- A value stream describes WHAT value flows, never HOW it's operationally delivered (processes own that).
- Stages SOFT-LINK to capabilities; they never inline capability definitions.
- The triggering stakeholder MUST link to a persona ID — if absent, surface as `_TODO_` and pursue.
- 4–10 stages per stream. Fewer = it's a process; more = scoping error.

---

## Value Stream Template

> Copy this block for each new value stream. Replace all `[…]` placeholders.
> Delete italicised guidance lines before publishing.

---

### VS-N · [Value stream name — describe the value achieved, e.g. "Acquire Product"]

*Naming rule (BIZBOK): name the stream after the **final value achieved**,
using business-object framing. Avoid internal-lifecycle naming
("order-to-cash", "hire-to-retire") — that's BIZBOK's #1 scoping mistake.*

**Triggering stakeholder:** [Persona ID + name — e.g. `P-02 · Médecin-conseil`]
**Value proposition:** [What the triggering stakeholder receives at the end of the stream. One sentence. One value, never two.]
**Scope anchor:** [Which BC-map L0 / product / domain this stream spans]
**Overall pain index:** [Low / Medium / High / Critical — aggregate of per-stage pain points]

#### Stage flow

```
[P-NN trigger] → VS-N.1 → VS-N.2 → VS-N.3 → VS-N.4 → [Value: {value proposition}]
```

#### VS-N.1 · [Stage name — value milestone, not activity]

*Stage-naming rule: stages name the value milestone, not the activity sequence.
"Validate eligibility" (stage) ≠ "Run eligibility-check script" (activity, belongs in process).*

| Field | Value |
|---|---|
| **Participating stakeholders** | [P-NN, P-MM — persona IDs from 01a-personas.md] |
| **Entrance criteria** | [What must be true to enter this stage — 2–4 bullets] |
| **Exit criteria** | [What must be true to leave — 2–4 bullets; the value item produced is the primary exit] |
| **Value items produced** | [1–3 incremental value items that accrue toward the value proposition] |
| **Enabling capabilities** | [C-N.M IDs — soft-link to 03a-capability-map.md] |
| **Operationalised by processes** | [process-name.md — soft-link to 05a-processes/, or `_TODO_`] |
| **Pain point index** | **[Low / Medium / High / Critical]** — [one-line rationale: evidence-based, not wishlist] |

#### VS-N.2 · [Stage name]

| Field | Value |
|---|---|
| **Participating stakeholders** | _TODO_ |
| **Entrance criteria** | _TODO_ |
| **Exit criteria** | _TODO_ |
| **Value items produced** | _TODO_ |
| **Enabling capabilities** | _TODO_ |
| **Operationalised by processes** | _TODO_ |
| **Pain point index** | _TODO_ |

*[Continue VS-N.3, VS-N.4, … up to ~10 stages max.]*

---

## Catalogue

*Single canonical table covering every value stream in scope. The catalogue
is the planning artifact; each row maps to one full §Value Stream block
below.*

| VS-ID | Name | Triggering stakeholder | Value proposition | Scope anchor | Pain index (overall) |
|---|---|---|---|---|---|
| VS-1 | [Stream name] | [P-NN persona] | [What the persona receives] | [BC-map L0 / product] | _TODO_ |
| VS-2 | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ |
| VS-3 | _TODO_ | _TODO_ | _TODO_ | _TODO_ | _TODO_ |

*Sizing reference:*
- *3–10 streams per product scope.*
- *~20–25 streams per enterprise (BIZBOK heuristic).*
- *If more than ~25 emerge for a single product, scope is wrong — split or push to enterprise-level map.*

---

## Value Streams

*No value streams have been filled yet. Use the template above to add each
stream as a new H3 block (within an H2 grouping if you want catalogue-style
sections) below this heading.*

<!-- Add value streams here -->

---

## Changelog

| Date | Change | Author |
|---|---|---|
| {{YYYY-MM-DD}} | Initial scaffold | _TODO_ |
