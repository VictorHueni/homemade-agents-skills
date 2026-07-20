# Methodology References — the Scaffold mode

Internal reference. Not copied to projects. Explains the rationale behind the skill's
design decisions.

---

## Why always scaffold the full tree?

An early design considered variant-aware scaffolding (greenfield / brownfield /
strategy-only / single-feature), where each variant would create a different subset of
folders. The variant model was dropped for two reasons:

1. **Empty folders are free.** Git ignores empty directories until a file lands in them.
   the Audit mode checks for *files*, not *folders* — an empty
   `docs/ops/runbooks/` on a single-feature project produces no audit findings and no
   noise. The cost of having extra empty directories is exactly zero.

2. **Variant selection adds complexity with no payoff.** A four-way configuration
   question, a promotion mechanism for growing projects, and four parallel folder lists
   to maintain — all to avoid a handful of empty directories that nobody sees.

The simpler rule: one universal structure, every project, every time. Teams fill what
they need and ignore the rest. This is the same principle as `git init` — it does not
ask whether the project is small or large.

---

## Why `.gitkeep` for empty directories?

Git does not track empty directories. A scaffold that creates only `mkdir -p` commands
leaves a structure that vanishes on `git clone` — the next developer or agent session
sees none of the intended skeleton.

`.gitkeep` is a zero-byte sentinel file that satisfies git's content-tracking requirement
without polluting the namespace with meaningful filenames. It is removed automatically when
the first real file is added to the directory (the presence of any other file makes the
`.gitkeep` redundant — skills that write to a folder do not need to delete it explicitly;
the directory continues to be tracked via its new content).

This is the same convention used in the kit's own `docs/project-control/open-items/archive/`.

---

## Why scaffold `docs/project-control/open-items/` rather than leaving it to `util-open-items`?

`util-open-items` is a **runtime operator** — skills file rows directly into the central
ledger through it as unresolved work is identified (there is no per-artefact local section
to sync from; ADR-0005 retired that step). It assumes the ledger path
(`docs/project-control/open-items/open-items.md`) already exists. When it doesn't, filing
fails with a file-not-found error before any row is processed.

The scaffold is the correct place to initialise the control plane because:
1. It runs before any artefact-producing skill, so the structure exists when needed.
2. The initial content (empty ledger with canonical schema, README) is project-agnostic
   and deterministic — it does not require operator input.
3. `util-open-items` remains the sole authoritative writer of row data; the scaffold only
   creates the structural skeleton.

The strategy-only and single-feature variants omit `docs/project-control/` because those
project types rarely produce artefact-level open items at scale. If open items are later
needed, the user can re-run scaffold Mode 2 with a larger variant (idempotent).

---

## Why not add `var/reports/` to `.gitignore` automatically?

Some teams commit audit reports deliberately — for audit trail purposes, for async review
in a pull request, or because they lack a separate CI artefact store. Auto-modifying
`.gitignore` would silently remove that option.

The skill surfaces the suggestion as a one-liner in the closing report. The operator makes
the choice. This is the same philosophy as the report-only discipline in the Audit mode
and the Migrate mode: surface findings, let the operator act.

---

## Why is `index.md` frontmatter-free (no `review_interval`)?

`index.md` is an [OKF v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
**reserved file** — a directory listing for progressive disclosure, not an artefact concept
document — so it carries no artefact frontmatter block (the bundle-root `docs/index.md` carries
only `okf_version`). It is a generated snapshot that becomes stale the moment any stack step
changes status, but its freshness is not policed by the artefact `review_interval` staleness
check; instead the body shows `> **Last refreshed:**` and the Audit mode Check 17
verifies the root `index.md` exists and declares `okf_version`.

Mode 3 regenerates `index.md` in seconds. The cost of refreshing is negligible; the cost of
a stale `index.md` misleading an agent into skipping a completed step is high — so refresh it
after every stack step.

---

## Sources

| Source | What it informs |
|---|---|
| Git documentation — gitignore(5) | `.gitkeep` convention and universal-tree rationale |
| `util-open-items/SKILL.md` | Project-control scope boundary |
| this skill's `references/open-items-governance.md` | Control-plane initialisation requirements |
| the Audit mode/scaffold-methodology.md` | Report-only / suggest-only discipline |
