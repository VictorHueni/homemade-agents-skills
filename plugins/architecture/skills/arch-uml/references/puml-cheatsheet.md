# PlantUML cheatsheet (per diagram type)

Copy-paste-able fragments for the six diagram types `arch-uml` produces. Every fragment opens `@startuml` → `!include _theme.puml` → `title`, per the kit convention (`arch-plantuml/references/puml-conventions.md`). Replace the placeholder IDs/names.

Authoritative reference: [plantuml.com](https://plantuml.com). This file is the **subset** the kit uses, pre-wired to the conventions.

---

## 1. Sequence (`seq-NN-<slug>.puml`)

Interaction over time. Use `alt`/`par`/`loop`/`opt` for branches — this richness is the main reason to pick PlantUML over Mermaid for sequences.

```plantuml
@startuml
!include _theme.puml
title seq-01 — Customer submits a claim (realises UC-01)

actor "P-02 — Customer" as customer
participant "Customer Portal" as portal
participant "Claims API" as api
database "Claims DB" as db
queue "Event Bus" as bus

customer -> portal : Submit claim
activate portal
portal -> api : POST /claims
activate api
api -> db : Persist Claim aggregate
alt valid claim
    api -> bus : Publish ClaimSubmitted
    api --> portal : 201 Created
else validation failed
    api --> portal : 422 Unprocessable
end
deactivate api
portal --> customer : Confirmation / error
deactivate portal

@enduml
```

Notes:
- `actor`/`participant`/`database`/`queue`/`boundary`/`control`/`entity` give different shapes.
- `->` solid (call), `-->` dashed (return). `activate`/`deactivate` draw the execution bar.
- Group blocks: `alt … else … end`, `loop … end`, `par … end`, `opt … end`, `group <label> … end`.
- Keep it readable: see `diagram-discipline.md` — a sequence over ~12 messages usually wants splitting.

---

## 2. Class (`class-NN-<slug>.puml`)

Static structure. Carry domain-model aggregate/entity names verbatim.

```plantuml
@startuml
!include _theme.puml
title class-01 — Claims domain (BC-01 Claims)

class Claim {
    +ClaimId id
    +Money amount
    +ClaimStatus status
    +submit()
    +approve()
}

class ClaimLine {
    +LineId id
    +Money amount
}

class Claimant {
    +ClaimantId id
    +String name
}

Claim "1" *-- "1..*" ClaimLine : contains
Claim "1" --> "1" Claimant : filed by
Claim ..|> Auditable

@enduml
```

Relationship arrows:
| Syntax | Meaning |
|---|---|
| `A --> B` | Association (A knows B) |
| `A *-- B` | Composition (B is part of A; dies with it) |
| `A o-- B` | Aggregation (B referenced by A; independent life) |
| `A --\|> B` | Generalization (A extends B) |
| `A ..\|> B` | Realization (A implements interface B) |
| `A ..> B` | Dependency |

Multiplicities go in quotes near each end: `A "1" --> "0..*" B`.

---

## 3. State machine (`state-NN-<slug>.puml`)

One aggregate's lifecycle. Title the aggregate ID.

```plantuml
@startuml
!include _theme.puml
title state-01 — Claim lifecycle (BC-01.AGG-02 Claim)

[*] --> Draft
Draft --> Submitted : submit()
Submitted --> UnderReview : assign()
UnderReview --> Approved : approve()
UnderReview --> Rejected : reject()
Approved --> Paid : disburse()
Rejected --> [*]
Paid --> [*]

state UnderReview {
    [*] --> Triaging
    Triaging --> Investigating : needsInfo()
    Investigating --> Triaging : infoReceived()
}

@enduml
```

Notes:
- `[*]` is the initial/final pseudo-state.
- Composite (nested) states: `state Name { ... }` — a key reason to use PlantUML over Mermaid here.
- Transition labels are the events/commands (`event() [guard] / action`).

---

## 4. Activity (`act-NN-<slug>.puml`)

Process/algorithm flow. Use the **new** activity syntax (`start`/`stop`, `:action;`) — not the deprecated `(*)` syntax. Swimlanes with `|Lane|`.

```plantuml
@startuml
!include _theme.puml
title act-01 — Claim triage (PROC-03)

|Customer|
start
:Submit claim;

|Claims API|
:Validate claim;
if (valid?) then (yes)
    :Persist claim;
    :Publish ClaimSubmitted;
else (no)
    :Return validation error;
    stop
endif

|Claims Handler|
:Triage claim;
if (needs investigation?) then (yes)
    :Open investigation;
else (no)
    :Approve;
endif
:Notify customer;
stop

@enduml
```

Notes:
- `:text;` is an action; `if (cond?) then (label) … else (label) … endif`; `fork`/`fork again`/`end fork` for parallelism.
- `|Lane|` switches the swimlane for subsequent actions.

---

## 5. Entity-relationship (`er-NN-<slug>.puml`)

Data model with crow's-foot multiplicities. Note the bounded context in the title.

```plantuml
@startuml
!include _theme.puml
title er-01 — Claims schema (BC-01 Claims)

entity Claim {
    * id : uuid <<PK>>
    --
    * claimant_id : uuid <<FK>>
    * amount : numeric
    * status : text
    created_at : timestamptz
}

entity ClaimLine {
    * id : uuid <<PK>>
    --
    * claim_id : uuid <<FK>>
    * amount : numeric
}

entity Claimant {
    * id : uuid <<PK>>
    --
    name : text
}

Claim ||--o{ ClaimLine : has
Claimant ||--o{ Claim : files

@enduml
```

Crow's-foot ends: `||` exactly one · `o{` zero-or-many · `|{` one-or-many · `o|` zero-or-one. `*` marks a mandatory attribute; `--` separates the key block from the rest.

---

## 6. Use case (`uc-NN-<slug>.puml`)

Actors + use cases + relationships. Carry `UC-NN` (from `spec-use-case`) on each ellipse and `P-NN` (from `business-persona`) on actors — this is the diagram that finally renders what `spec-use-case` already describes.

```plantuml
@startuml
!include _theme.puml
title uc-01 — Claims Portal (use cases UC-01…UC-04)
left to right direction

actor "P-02 — Customer" as customer
actor "P-01 — Claims Handler" as handler

rectangle "Claims Platform" {
    usecase "UC-01\nSubmit a claim" as UC01
    usecase "UC-02\nTrack claim status" as UC02
    usecase "UC-03\nTriage a claim" as UC03
    usecase "UC-04\nAuthenticate" as UC04
}

customer --> UC01
customer --> UC02
handler --> UC03

UC01 ..> UC04 : <<include>>
UC03 ..> UC04 : <<include>>

@enduml
```

Notes:
- `«include»` (mandatory sub-use-case) and `«extend»` (optional extension) are drawn with `..>` + a `<<include>>` / `<<extend>>` label.
- `left to right direction` usually reads better than the top-down default for use-case diagrams.
- Keep the `UC-NN` label on the ellipse so a reviewer can jump to the fully-dressed use case in `spec-use-case`.

---

## Shared idioms (all types)

- **Legend:** `legend right … endlegend` for a key. The theme styles it.
- **Notes:** `note right of X : text` / `note over X, Y : text`.
- **Direction:** `left to right direction` (use-case, some activity) vs the top-down default.
- **Never** put a name after `@startuml` — the filename owns the output name (see `puml-conventions.md`).
- **Always** `!include _theme.puml` as the first line after `@startuml`.
