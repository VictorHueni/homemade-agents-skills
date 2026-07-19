# Structurizr DSL conventions

The DSL is the **single source of truth** for every C4 view in the project. These conventions exist to keep multi-skill authoring (`arch-c4` writes; `arch-runtime-view` reads) consistent and grep-friendly.

Authoritative grammar: [docs.structurizr.com/dsl](https://docs.structurizr.com/dsl). This file lists the **kit-specific rules** layered on top of the official grammar.

---

## 1. Grammar gotchas (from upstream — easy to violate when an agent edits the DSL)

These rules come from [docs.structurizr.com/dsl/basics](https://docs.structurizr.com/dsl/basics) and bite when an LLM "tidies" code:

1. **Imperative, not declarative.** Lines are processed in order. **Forward references are not allowed** — you can't use an identifier before it has been declared.

   ❌ Wrong (forward ref):
   ```
   user -> system "Uses"
   user = person "User"
   system = softwareSystem "Backend"
   ```

   ✅ Right:
   ```
   user = person "User"
   system = softwareSystem "Backend"
   user -> system "Uses"
   ```

2. **Opening brace `{` must end its line.** Not on its own line.

   ❌ Wrong:
   ```
   model
   {
       user = person "User"
   }
   ```

   ✅ Right:
   ```
   model {
       user = person "User"
   }
   ```

3. **Closing brace `}` must be alone on its line.** Not on the line of the last statement.

   ❌ Wrong: `user = person "User" }`

   ✅ Right: `}` on its own line.

4. **Identifiers are case-sensitive Java-style.** Letters, digits, `_`. No `-`. (The display name carries hyphens; the identifier does not.)

   ❌ Wrong: `SYS-01 = softwareSystem ...`

   ✅ Right: `SYS_01 = softwareSystem "SYS-01 — Claims Portal" "..."`

5. **String values are double-quoted.** Single quotes are not accepted for string literals.

---

## 2. Kit identifier conventions

Every kit-minted ID has a matching DSL identifier so the artefact is grep-able both ways (`SYS-01` in markdown, `SYS_01` in DSL).

| Kit ID | DSL identifier | Display name | Element type |
|---|---|---|---|
| `SYS-01` | `SYS_01` | `"SYS-01 — Claims Portal"` | `softwareSystem` |
| `CON-02` | `CON_02` | `"CON-02 — Claims API"` | `container` |
| `CMP-03` | `CMP_03` | `"CMP-03 — Claim Command Handler"` | `component` |
| `DN-04` | `DN_04` | `"DN-04 — Production Kubernetes Cluster"` | `deploymentNode` |
| *(N/A — reuses P-NN)* | `P_01` | `"P-01 — Claims Handler"` | `person` |

**Numbering rule:** monotonically assigned per element type, never re-used. `arch-c4` discovers the next number by grepping the DSL.

**Why a display name that repeats the ID:** the rendered SVG diagrams must surface the kit ID so reviewers can cross-reference into arc42 markdown without opening the DSL.

---

## 3. View keys (the names rendered files will inherit)

Structurizr writes one file per view. The file name is the view *key* (the second argument when defining a view). Use these canonical keys so renders land at predictable paths:

| View key | arc42 mapping | DSL view type |
|---|---|---|
| `systemContext` | §3 Context & Scope | `systemContext` |
| `containers` | §5.1 Building Block Level 1 | `container` |
| `components-<CON-NN>` | §5.2 Building Block Level 2 (one per drilled container) | `component` |
| `deployment-<env>` | §7 Deployment View (one per environment) | `deployment` |
| `dynamic-<RV-NN>` | §6 Runtime View (one per scenario) | `dynamic` |

The renders end up at `c4/views/<view-key>.svg`. The arc42 markdown embeds them by relative path.

---

## 4. Tag conventions for styling

Tags drive the kit's styling block (defined in the seed `workspace.dsl`). Apply tags consistently:

| Tag | Applied to | Effect |
|---|---|---|
| `external` | Any element outside the system boundary | Greyed out in renders |
| `database` | Containers backed by a DB | Cylinder shape |
| `queue` | Message bus / event broker containers | Pipe shape |
| `web` | Web UI / SPA containers | Browser icon hint |
| `mobile` | Mobile app containers | Mobile-frame hint |
| `core` | Components inside Core subdomain BCs (per `domain-bounded-context`) | Highlighted colour |
| `supporting` | Components inside Supporting BCs | Neutral |
| `generic` | Components inside Generic BCs | Muted |

`arch-c4` adds these as it discovers BC classifications.

---

## 5. File layout — when to split workspace.dsl

Default: **one workspace.dsl file**. Easier diffs, easier validate, single rendering invocation.

Split (via `!include`) only when:
- The DSL exceeds ~800 lines AND
- Multiple bounded contexts have independent component models that don't cross-reference

Suggested split structure if needed:
```
c4/
├── workspace.dsl                 ← top-level (system, containers, includes per BC)
├── models/
│   ├── bc-01-claims.dsl
│   └── bc-02-policy.dsl
└── views/                        ← rendered output (unchanged)
```

`arch-c4` will not split automatically — splitting is a manual refactor.

---

## 6. The `description` field is non-optional

Every element (person, system, container, component) must have a description. Empty `""` is permitted only for elements awaiting domain modelling — and those should carry the `_TODO_` tag so the kit's audit (Check 8) can find them.

---

## 7. Sources

- [Structurizr DSL — Basics](https://docs.structurizr.com/dsl/basics)
- [Structurizr DSL — Identifiers](https://docs.structurizr.com/dsl/identifiers)
- [Structurizr — Working with AI/LLMs](https://docs.structurizr.com/ai) — text-based + version-controllable + diff-friendly is the design point that makes LLM authoring viable; the kit's conventions exist to capitalise on this.
