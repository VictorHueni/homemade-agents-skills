# View styling — tag-driven cookbook

Styling in Structurizr is **tag-driven**. Elements carry tags; the `styles { ... }` block defines how each tag renders. The kit's seed `workspace.dsl` ships with the conventions below — extend them rather than inventing new ones to keep visual consistency across projects.

---

## Standard tag taxonomy

| Tag | Applied to | Visual effect | Used at C4 level |
|---|---|---|---|
| `internal` | Internal personas | Default Person colour (#08427B blue) | 1 |
| `external` | External people / external systems / third-party SaaS | Greyed out (#999999) | 1, 2 |
| `core` | Containers/components inside Core subdomain BCs | Highlighted core blue (#0B6FB8) | 2, 3 |
| `supporting` | Containers/components inside Supporting BCs | Default container blue | 2, 3 |
| `generic` | Containers/components inside Generic BCs (commodity) | Muted grey | 2, 3 |
| `web` | Web UI containers | Browser shape | 2 |
| `mobile` | Mobile app containers | Mobile device shape | 2 |
| `database` | Database containers | Cylinder shape | 2, 3 |
| `queue` | Message bus / event broker containers | Pipe shape | 2 |
| `cdn` | CDN deployment nodes | Cloud icon hint | 7 |
| `kubernetes` | K8s cluster deployment nodes | Container icon hint | 7 |
| `managed-database` | RDS / Cosmos / managed Postgres deployment nodes | Cylinder + cloud hint | 7 |
| `managed-queue` | MSK / SQS / managed Kafka deployment nodes | Pipe + cloud hint | 7 |

The `core` / `supporting` / `generic` subdomain tags come from `domain-bounded-context`. When adding a container, look up which BC it belongs to and apply the matching tag.

---

## When to add a new tag

Only when the existing taxonomy genuinely doesn't fit, **and** the new visual class will be reused across ≥2 elements. One-off styling deviations are noise — Structurizr is opinionated about visual consistency, and so is the kit.

If you add a new tag:
1. Add it to `arch-structurizr/references/dsl-conventions.md` §4 (tag conventions table).
2. Add a style rule to the `styles { ... }` block in `workspace.dsl`.
3. Add a row to this file's standard taxonomy table.
4. Update the kit's the `metamodel` skill's Audit mode Check 9 if applicable.

---

## Light vs dark rendering

The Structurizr export supports `-mode light|dark`:

```
docker run --rm -v $REPO:/work $IMAGE \
    export -workspace $DSL -format svg -output $VIEWS -mode dark
```

`render.sh` defaults to **light**. For dark-mode renders intended for dark-theme documentation, edit `render.sh` to add `-mode dark` or run the export step manually.

The kit does **not** produce both modes simultaneously — pick one per project. If both are needed, render to `views/light/` and `views/dark/` subdirectories and update the arc42 markdown to switch via CSS (out of scope for the skill).

---

## Layout hints

| Hint | When to use |
|---|---|
| `autolayout lr` | Default for context, container, deployment views (left-to-right; readable when 4–10 elements) |
| `autolayout tb` | Top-to-bottom; better for component views with deep dependency chains |
| `autolayout` (no direction) | Lets Structurizr pick — works for small (≤4) views |

Manual layout (`x` / `y` per element) is **forbidden** in the kit. Auto-layout is the entire point of using a model rather than hand-drawn diagrams; defeating it via manual coords means future re-renders churn unpredictably.

---

## Embedding rendered SVGs in arc42 markdown

The skill writes embed markers using relative paths from each arc42 markdown file:

```markdown
![SYS-01 System Context](../c4/views/systemContext.svg)
```

Path is relative from `docs/architecture/arc42/03-context.md` → `docs/architecture/c4/views/systemContext.svg`. The `../` walks up one folder.

For tighter integration with GitHub markdown preview, prefer SVG (text-based, scales well, diffable). PNG export is available via `-format png` if needed — adds ~30% file size and isn't text-diffable.

---

## When the rendered diagram looks bad

Causes + fixes:

| Symptom | Cause | Fix |
|---|---|---|
| Edges crossing dense areas | `autolayout lr` with too many elements | Switch to `tb` or split the view into two scoped views |
| Text overflow | Long descriptions on Person/Container | Shorten the `description` field; full prose belongs in the arc42 markdown table |
| Elements far apart with empty space | Few elements + `autolayout lr` | Drop the `lr` modifier to let Structurizr pick |
| External system buried in middle | Forgot `tags "external"` | Add the tag; greying signals "context boundary" |
| Containers all the same shade | Forgot `core`/`supporting`/`generic` tags | Add subdomain tags to surface the BC classification |
| Edges with no labels | Missing technology argument on `->` | Always pass `"<description>" "<technology>"` to relationships |

---

## Sources

- [Structurizr DSL — Styling](https://docs.structurizr.com/dsl/styling)
- [Structurizr DSL — Themes](https://docs.structurizr.com/dsl/themes) — `theme default` is the kit's baseline
- [C4 model — Notation](https://c4model.com/notation) — the visual conventions Structurizr's defaults follow
