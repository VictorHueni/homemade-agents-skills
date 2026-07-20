# The C4 model (Simon Brown)

The C4 model is a hierarchical way to describe a software system's **static** structure. Read this once before authoring any mode; refer back for level-specific rules.

Authoritative reference: [c4model.com](https://c4model.com).

---

## The four levels

| Level | Name | What it shows | When to draw it |
|---|---|---|---|
| 1 | **System Context** | One system in scope + every person and external system it talks to (black-box) | Always. The "everyone" diagram. |
| 2 | **Container** | Inside a single software system: deployable units (apps, services, databases, message brokers) and their relationships | Almost always (skip only if the system is a single binary with no dependencies — rare). |
| 3 | **Component** | Inside a single container: components (modules / packages / classes) and their relationships | For containers that are **complex, surprising, risky, or critical**. Skip routine CRUD services. |
| 4 | **Code** | UML class diagrams inside one component | Almost never — the code itself is the authoritative source. |

The kit produces Levels 1, 2, and 3. **Level 4 is intentionally not modelled** — the C4 model itself recommends skipping it in most cases, and the kit follows that recommendation.

---

## The five element types

| Element | Levels where it appears | What it represents |
|---|---|---|
| **Person** | 1 | Human actor (end user, operator, admin) |
| **Software System** | 1 | The system in scope (white box at L1) and external systems (black box) |
| **Container** | 1, 2 | A runtime / deployment unit — an app, a service, a database, a message broker. **NOT** Docker containers specifically; the word predates Docker. |
| **Component** | 1, 2, 3 | A module or class inside a container. **NOT** a UI component or a React component. |
| **Code** | 4 | A class, function, type (skipped by the kit) |

Plus **Relationship** (a directed edge between any two elements, with description + technology label).

---

## C4 vocabulary clashes

| Word | C4 meaning | Common other meaning to avoid confusion with |
|---|---|---|
| "Container" | A runtime unit (Spring Boot app, Postgres database, Kafka cluster) | A Docker container — *not* the same thing. A C4 container often runs as multiple Docker containers in production. |
| "Component" | A code-level module inside a C4 Container | A UI component (Vue / React component) — *not* the same. C4 Components are server-side modules. |
| "System" | A whole software system in scope (e.g. "Claims Platform") | A "system" in OS / distributed-systems sense |

When writing the arc42 markdown, the kit always disambiguates: "C4 container" not just "container", "C4 component" not just "component".

---

## When to stop drilling

arc42 §5 wisdom captures this exactly:

> "Prefer relevance over completeness. Specify important, surprising, risky, complex or volatile building blocks. Leave out normal, simple, boring or standardised parts of your system." — arc42 §5.2

Heuristics:

- **Stop at Level 2** for: stateless CRUD services, simple frontends, off-the-shelf databases / brokers, third-party SaaS containers.
- **Drill to Level 3** for: aggregate-rich domain services, complex orchestration, services with non-obvious internal structure, services that have been a source of past bugs / incidents.
- **Never drill to Level 4** unless the component itself is so complex that text + types in the code aren't enough — in 10 years of C4 usage this is extremely rare.

---

## Quality checks (apply after every mode)

| Check | Pass condition | How to verify |
|---|---|---|
| One source of truth | Every C4 element is defined exactly once in `workspace.dsl` | grep for the DSL identifier; should match exactly one `=` assignment |
| Identifier consistency | Display name carries the kit ID; DSL identifier is the same number with underscore | `SYS_01` ↔ `"SYS-01 — Name"` |
| Description present | Every element has a non-empty description | `validate` step + manual scan |
| Relationships have technology labels | Every `->` has a description + technology argument | DSL inspection |
| External boundary correct | Anything outside the primary system is tagged `external` | DSL tag scan |
| Component-to-aggregate mapping | Every `component` has `properties.implements` set (even to `""` if intentionally empty) | DSL property scan |
| View key naming | Each view's key matches the canonical pattern | See `arch-c4` SKILL.md modes table |

---

## C4 vs arc42 — where they overlap and where they don't

| arc42 section | C4 covers? | Gap |
|---|---|---|
| §3 Context & Scope | ✅ Yes — Level 1 maps directly | arc42 §3.2 also wants channels + protocols per partner — C4 captures via `relationship technology` field |
| §5 Building Block View Level 1 | ✅ Yes — C4 Container view | arc42 wants a "Motivation" sentence and a "Contained Building Blocks" table; C4 only renders the diagram |
| §5 Building Block View Level 2/3 | ✅ Yes — C4 Component view | arc42 black-box template adds "Quality characteristics", "Open issues" — C4 doesn't natively model these |
| §7 Deployment View | ✅ Yes — C4 Deployment view | arc42 wants per-environment "Quality and/or Performance Features" + "Motivation" — C4 doesn't natively model these |
| §6 Runtime View | ❌ No — C4 is static | C4 has *dynamic views* but the kit treats arc42 §6 as `arch-runtime-view`'s domain |
| §2 Constraints | ❌ No | `arch-constraints` (Milestone 2) |
| §4 Solution Strategy | ❌ No | `arch-solution-strategy` (Milestone 2) |
| §8 Cross-cutting Concepts | ❌ No | `arch-cross-cutting` (Milestone 2) |

The arc42 markdown templates this skill writes fill the gaps that C4 doesn't natively cover — tables for motivation, quality characteristics, and per-environment performance features.

---

## Sources

- [The C4 model — Abstractions](https://c4model.com/abstractions)
- [The C4 model — Notation](https://c4model.com/notation)
- [Structurizr DSL](https://docs.structurizr.com/dsl) — how the kit serialises C4 models
- arc42 v9.0 template — embedded under `references/arc42-section-{03,05,07}.md`
