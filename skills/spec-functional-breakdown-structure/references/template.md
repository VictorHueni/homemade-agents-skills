<!-- doc-version: 1.0 | created: {{YYYY-MM-DD}} -->

# {{product_or_scope}} — Functional Breakdown Structure

This document is the functionality registry for {{product_or_scope}}: a
canonical, status-tracked enumeration of what the product does, organised
by the capabilities defined in the [Business Capability
Map](../../business/03a-capability-map.md). Each capability
groups the functionalities that realise it; each functionality has a
stable ID, a status (✅ Shipped / 🔄 Planned / ⬜ Backlog), and optional
soft-links to value-stream stages.

> **Methodology:** built using the canonical synthesis of [BABOK §10.22
> Functional Decomposition + NASA FBS doctrine + TOGAF Business
> Architecture +
> practitioner guidance](https://github.com/VictorHueni/homemade-claude-kit/tree/main/spec-functional-breakdown-structure/references/methodology-references.md).
> The full bibliography lives with the
> [spec-functional-breakdown-structure
> skill](https://github.com/VictorHueni/homemade-claude-kit/tree/main/spec-functional-breakdown-structure)
> — single source of truth across every project.

**Scope discipline:**
- FBS is the **functionality registry** — what the product does, status-tracked.
- FBS does NOT define capabilities — see the BC Map.
- FBS does NOT contain feature specs / acceptance criteria — see PRDs.
- FBS does NOT contain roadmap timelines / dates / milestones — see the roadmap doc.
- FBS does NOT contain operational metrics / cycle times — see process docs.

**Companion documents:**
- Business Capability Map: [link to ../../business/03a-capability-map.md if exists]
- Personas: [link to ../../business/01a-personas.md if exists]
- Value Streams: [link to ../../business/04a-value-streams.md if exists]
- Business Processes: [link to ../../business/05a-processes/ if exists]
- PRDs: [link to ../ if exists]

---

## Status legend

| Symbol | Meaning |
|---|---|
| ✅ | **Shipped** — functional in production |
| 🔄 | **Planned** — committed in an active PRD or execution plan |
| ⬜ | **Backlog** — identified, not yet committed |

---

## L0 axis declaration

**Chosen axis:** {{L0_axis_label}} *(inherited from BC Map)*

**Rationale:** [One sentence — should mirror the BC Map's rationale]

**L0 items:**
- **C1** — [Name of first L0 item]
- **C2** — [Name of second L0 item]
- **C3** — [Name of third L0 item]

---

## Global overview

*ASCII tree of products → capabilities → (functionality counts per capability).
Generated from the BC Map; counts updated as functionalities are filled in.*

```
{{product_or_scope}}
│
├── C1 · [L0 item name]
│   ├── C1.1 · [Capability name]  (functionalities: 0 ✅ · 0 🔄 · 0 ⬜)
│   └── C1.2 · [Capability name]  (functionalities: _TODO_)
│
├── C2 · [L0 item name]
│   ├── C2.1 · [Capability name]  (functionalities: _TODO_)
│   └── C2.2 · [Capability name]  (functionalities: _TODO_)
│
└── C3 · [L0 item name]
    └── C3.1 · [Capability name]  (functionalities: _TODO_)
```

---

## C1 · [L0 item 1 name]

*Brief description of this L0 item — what unifies the capabilities below it.
Should mirror the BC Map's L0 description.*

---

### C1.1 · [Capability name]

*One-line capability summary — short reminder of what the capability does.
**Do NOT restate the BC Map definition.** Link to the BC Map row for the full
definition.*

**BC Map:** [C1.1 in capability-map.md](../../business/03a-capability-map.md#c11)
**Backend:** [paths or `_TODO_`]
**Frontend:** [paths or `_TODO_`]

| ID | Functionality | Status | VS stage |
|---|---|---|---|
| C1.1.F01 | [Functionality name — what the system does] | ⬜ | _TODO_ |
| C1.1.F02 | _TODO_ | ⬜ | _TODO_ |

---

### C1.2 · [Capability name]

*One-line capability summary.*

**BC Map:** [C1.2 in capability-map.md](../../business/03a-capability-map.md#c12)
**Backend:** _TODO_
**Frontend:** _TODO_

| ID | Functionality | Status | VS stage |
|---|---|---|---|
| C1.2.F01 | _TODO_ | ⬜ | _TODO_ |

---

## C2 · [L0 item 2 name]

*Brief description of this L0 item.*

### C2.1 · [Capability name]

*One-line capability summary.*

**BC Map:** [C2.1 in capability-map.md](../../business/03a-capability-map.md#c21)
**Backend:** _TODO_
**Frontend:** _TODO_

| ID | Functionality | Status | VS stage |
|---|---|---|---|
| C2.1.F01 | _TODO_ | ⬜ | _TODO_ |

---

## Maintenance notes

- **Add a functionality:** Insert a new row in the relevant capability table with the next ID in sequence (e.g., if last row is `C1.1.F07`, new row is `C1.1.F08`). Status starts as `⬜`. IDs are never reused or recycled.
- **Promote status:** `⬜ → 🔄` when a PRD commits the work; `🔄 → ✅` when the PRD ships. Update the capability's functionality count in the ASCII tree.
- **Retire a functionality:** Mark status as `⬜` with a changelog note describing the retirement. Don't delete the row — keep history.
- **Add a capability:** Don't — add it to the BC Map first; then run this skill's structure mode to import it.
- **Reorganise L0:** Don't — change the BC Map's L0 axis first, then regenerate the FBS structure.

---

## Changelog

| Date | Change | Author |
|---|---|---|
| {{YYYY-MM-DD}} | Initial scaffold | _TODO_ |
