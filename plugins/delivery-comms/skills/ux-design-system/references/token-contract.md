# Token contract

The canonical `:root` vocabulary shared by every `com-*` renderer. `tokens.css`
(generated from `design-system.md`) defines exactly these names so any consumer
can rely on them. **Names are fixed; values are free.** Renaming or dropping a
token breaks consumers; `generate_tokens.py` warns when a contract token is
missing. Projects MAY add extra tokens (kept, flagged as "not in contract").

The authoritative list also lives in `templates/tokens.template.css` — the
generator validates against it.

## Groups

### Base palette
| Token | Role |
|---|---|
| `--ink` | Primary text |
| `--muted` | Secondary text |
| `--canvas-bg` | Page background |
| `--surface` | Card / panel background |
| `--surface-2` | Recessed / group background |
| `--border` | Hairlines, dividers |
| `--accent` | Primary action, links, IDs |
| `--accent-ink` | Text on accent fills |

### Semantic state (generic — portable)
| Token | Role |
|---|---|
| `--success` | Positive / done / validated |
| `--warning` | Caution / in-progress / tested |
| `--danger` | Negative / error / critical |
| `--info` | Informational / planned / neutral-active |

These four are the ONLY semantic tokens in the project contract. Kit-domain
tokens (delivery status, pain index, confidence, strategic importance) are
**consumer-derived**: each consumer defines them in its own stylesheet as
aliases to these generics (see "Consumer-derived tokens" below), so a project
themes four portable names instead of kit jargon.

### Typography
| Token | Role |
|---|---|
| `--font-sans` | Body + UI |
| `--font-mono` | IDs, code, labels |
| `--title-size` | View / slide title size |

### Spacing & shape
| Token | Role |
|---|---|
| `--space-sm` · `--space-md` · `--space-lg` | Spacing scale |
| `--shell-max` | Max content width |
| `--card-radius` · `--btn-radius` · `--node-radius` | Corner radii |
| `--shadow` | Card elevation |

## Consumer mapping

| Contract group | Used by |
|---|---|
| Base palette, typography, spacing | `com-slide-deck`, `com-artefact-viz` (all views) |
| Semantic state (`--success/--warning/--danger/--info`) | `com-slide-deck` (state colours) + `com-artefact-viz` (via the derived tokens below) |

### Consumer-derived tokens

The contract stays generic; consumers map their domain semantics onto it in
their own bundled stylesheet (not in the project `tokens.css`). `com-artefact-viz`
defines these aliases in `templates/tokens.domain.css` so a project re-theming
`--success/--warning/--danger/--info` re-themes every view:

| Domain token (viz) | Derived from | Where |
|---|---|---|
| `--differentiator` / `--necessary` / `--commodity` | `--danger` / `--warning` / `--muted` | capability-map |
| `--status-shipped` / `--status-planned` / `--status-backlog` | `--success` / `--info` / `--muted` | fbs + roadmap |
| `--pain-critical` / `--pain-high` / `--pain-medium` / `--pain-low` | `--danger` / `--warning` / `--info` / `--muted` | roadmap |
| `--conf-assumed` / `--conf-tested` / `--conf-validated` | `--muted` / `--warning` / `--success` | bmc |

A project MAY still override a domain token directly (e.g. `--pain-critical`) if
it wants finer control, but it never has to — theming the four generics is enough.
