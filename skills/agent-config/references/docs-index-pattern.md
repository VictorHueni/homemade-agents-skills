# Docs Index Pattern — Wiring Agents to a Living Navigation Hub

## The problem with inline path listings

The most common way projects give agents docs navigation is to embed the `docs/` tree directly in CLAUDE.md:

```markdown
## Docs structure
docs/
├── architecture/decisions/   ← ADRs
├── product-specs/prds/       ← PRDs
├── domain/                   ← Domain model
└── dev-guides/               ← Developer guides
```

This works until the first refactor. Paths listed inline go stale silently — agents treat stale content as current fact and navigate to paths that no longer exist. The fix costs a full conversation to diagnose.

**The rule:** never embed a docs path tree inline in the agent config. Point to a living index instead.

---

## The solution: docs/index.md

A `docs/index.md` is a **living navigation hub** — a single file that the agent reads to understand what documentation exists and where. Because it lives in `docs/`, it evolves with the repo. Because it is the dedicated index, it stays accurate in a way that config-embedded paths never do.

The CLAUDE.md / AGENTS.md pointer is a single line:

```markdown
Read [docs/index.md](docs/index.md) for the full documentation navigation hub.
```

That line is stable forever. The path `docs/index.md` does not change when ADRs are added or PRDs are restructured.

---

## How index.md is generated

### Kit-based projects (homemade-claude-kit)

Projects using the the `metamodel` skill's Scaffold mode skill have `docs/index.md` auto-generated and maintained. The index is a live table with ✅/🔄/⬜ status per documentation step, covering all 18 artefact types in the strategic-architecture build order. Run the `metamodel` skill's Scaffold mode Mode 3 (refresh) to regenerate it after adding new artefacts.

The the `metamodel` skill file in `~/.claude/rules/` is the **path map** that index.md reflects — it contains the canonical output paths for every artefact type, the full dependency graph (DAG), and the build order. When in doubt about where something lives, read the `metamodel` skill — it is the authoritative source. index.md is the project-specific read-out of that map.

```markdown
# Pointer for kit-based projects
Read [docs/index.md](docs/index.md) for the full documentation navigation hub.
For canonical path rules and build order, see ~/.claude/the `metamodel` skill.
```

### Non-kit projects

For projects without the kit scaffold, create a minimal `docs/index.md` manually or with the `agent-config` scaffold mode. The minimal format is a flat table:

```markdown
# Documentation Index

| File | Type | Status | Summary |
|---|---|---|---|
| [VISION.md](VISION.md) | Vision | active | Product north star and problem framing |
| [architecture/decisions/](architecture/decisions/) | ADR folder | active | Architecture decision records |
| [dev-guides/nextjs-supabase.md](dev-guides/nextjs-supabase.md) | Dev guide | active | Next.js + Supabase patterns for this project |
| [product-specs/prds/](product-specs/prds/) | PRD folder | active | Feature specifications |
```

The key columns are: file path (as a relative link), type, status, and a one-sentence summary. This is enough for an agent to know which file to read for which question.

---

## What goes in the CLAUDE.md pointer section

The pointer section in CLAUDE.md should be 1–4 lines, not a full description:

```markdown
## Documentation
- Vision and problem framing: [docs/VISION.md](docs/VISION.md)
- Full docs navigation: [docs/index.md](docs/index.md)
- Architecture decisions: [docs/architecture/decisions/](docs/architecture/decisions/)
```

Only add the third line (architecture decisions) if the agent will frequently need to reference ADRs — otherwise the index.md link is sufficient.

---

## When there is no docs/ tree

For projects with minimal or no docs/ content:

```markdown
## Documentation
_No structured docs yet. See README.md for project overview._
```

Do not fabricate an index.md for a project that has none. An empty or sparse docs/ tree does not need an index.

---

## Maintenance

`docs/index.md` should be updated when:
- A new major documentation artefact is added (new ADR, new PRD, new domain model)
- A file is moved or renamed
- The status of a major artefact changes (draft → active, active → superseded)

It should NOT be updated for every minor edit to every document — the index tracks artefact-level navigation, not individual file contents.
