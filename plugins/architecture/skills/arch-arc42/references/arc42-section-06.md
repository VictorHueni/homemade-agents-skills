# arc42 §6 — Runtime View (embedded reference)

Extracted from the arc42 v9.0 template (July 2025). Use as the authoritative spec when writing `docs/architecture/arc42/06-runtime-view.md`.

Upstream: [docs.arc42.org/section-6](https://docs.arc42.org/section-6/).

---

## Content

> The runtime view describes the concrete behavior and interactions of the system's building blocks in form of scenarios from the following areas:
>
> - important use cases or features: how do building blocks execute them?
> - interactions at critical external interfaces: how do building blocks cooperate with users and neighboring systems?
> - operation and administration: launch, start-up, stop
> - error and exception scenarios

## Motivation

> You should document these scenarios where
>
> - your stakeholders need to understand how the product works
> - you can illustrate the interaction or collaboration of the system's building blocks

## Form

> There are many notations for describing scenarios, e.g.
>
> - numbered list of steps (in natural language)
> - activity diagrams or flow charts
> - sequence diagrams
> - BPMN or EPCs (event process chains)
> - state machines
> - …

---

## Kit application: Structurizr dynamic views

The kit uses Structurizr **dynamic views** (`dynamic` DSL keyword). They reuse the elements already defined in the model — no re-declaration needed — and impose an explicit step order on relationships.

```
dynamic SYS_NN "runtime-SCN-01-claim-submission" {
    include *
    autoLayout
}
```

Inside the view block, relationships are annotated with step numbers:

```
views {
    dynamic SYS_NN "runtime-SCN-01-claim-submission" {
        user -> SYS_NN "Submit claim" {
            properties { "step" "1" }
        }
        SYS_NN -> external_system "Forward to insurer" {
            properties { "step" "2" }
        }
    }
}
```

The Structurizr vNext renderer renders dynamic views as numbered sequence-style SVGs (arrows labelled with step numbers). This integrates naturally with the static container and component views in the same workspace.

---

## Quantity guidance (arc42 §6)

> Select important, interesting and/or risky scenarios. Specify only a small number of scenarios using interaction or sequence diagrams.
>
> Try to combine this overview with profiles for important use cases.

**Kit rule:** document 3–7 scenarios per system. Start with the happy paths for the most-used capabilities. Add error paths only when the error-handling design is non-trivial (e.g. saga rollback, two-phase commit, circuit breaker). Do not document every CRUD operation.

---

## Boundary rules: what does NOT belong here

| This view | Where it belongs instead |
|---|---|
| Intra-aggregate lifecycle (state machine) | `docs/domain/07b-models/{bc-slug}.md` — per-aggregate state machines |
| Infrastructure allocation | arc42 §7 (`arch-c4 deployment` mode) |
| Static decomposition | arc42 §5 (`arch-c4 container` / `component` modes) |
| Business process steps (human + system) | `docs/business/business-processes/` (`business-process` skill) |

---

## Acceptance criteria — when §6 is "done"

- [ ] `docs/architecture/arc42/06-runtime-view.md` exists with standard frontmatter (see the `metamodel` skill's `references/artefact-frontmatter.md`)
- [ ] At least 2 scenarios are documented (happy path + one non-trivial error or cross-cutting path)
- [ ] Each scenario has: title, `SCN-NN` ID, brief motivation, rendered SVG, step table
- [ ] Step table row count matches the number of annotated steps in the DSL dynamic view
- [ ] No intra-aggregate state transitions appear (those belong to domain model)
- [ ] SVG committed under `docs/architecture/c4/views/runtime-<SCN-NN>-<slug>.svg`
