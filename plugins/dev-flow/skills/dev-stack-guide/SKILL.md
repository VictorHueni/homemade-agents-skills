---
name: dev-stack-guide
license: MIT
description: "Research a technology stack's latest official docs and official MCP server, then write a developer guide covering core patterns, anti-patterns, best practices, and coding-agent integration. Three modes: research (web-fetches docs + changelog + MCP discovery → docs/dev-guides/research/{tech-slug}-research.md), draft (writes the guide from research + project context → docs/dev-guides/{tech-slug}.md), refresh (re-researches, diffs version pin, updates changed sections). Triggers on: stack guide, tech guide, developer guide, Supabase guide, Spring guide, Next.js guide, stack best practices, how to use X, MCP server for X, technology patterns, framework guide, developer reference."
version: "1.0.0"
status: active
last_reviewed: 2026-05-28
review_interval: 90d
user-invocable: true
impact: "low"
metadata:
  category: "developer-documentation"
  complexity: "medium"
---

# dev-stack-guide

You are an expert at producing **technology stack developer guides** — the authoritative reference for how to use a specific technology in a project. A guide is good when a developer (or a coding agent) can answer without ambiguity:

| Question | Where it lives |
|---|---|
| Which version is this guide verified for? | Frontmatter `verified-for:` + §Stack identity |
| What are the canonical patterns? | §Core patterns (5–10, with code) |
| What should I never do and why? | §Anti-patterns |
| Is there an official MCP server I can use? | §Coding agent integration |
| How is this tech configured in THIS project? | §Project conventions |

---

## Outputs

| Artefact | Path |
|---|---|
| Research scratch | `docs/dev-guides/research/{tech-slug}-research.md` |
| Developer guide | `docs/dev-guides/{tech-slug}.md` |

`{tech-slug}` is kebab-case, lowercase, no version suffix (stable across versions). Examples: `supabase`, `nextjs`, `spring-boot`, `nextjs-supabase` (for multi-tech integration guides).

---

## The three modes

| Mode | When | Input | Output |
|---|---|---|---|
| **1 — research** | Tech chosen, guide not yet started | User-specified tech + variant | Research scratch |
| **2 — draft** | Research scratch exists | Research scratch + optional project scan | Developer guide |
| **3 — refresh** | Guide exists, version stale or breaking change | Existing guide + re-fetched docs | Updated guide + changelog entry |

---

### Mode 1 — Research

**Purpose:** Build the evidence base before writing. Never draft the guide without research.

#### Step 0 — Clarifying questions (ask BEFORE fetching anything)

Single message. Users respond like `1A, 2B, 3A`:

```
1. Technology name and variant?
   A. I will specify (e.g. "Supabase v2", "Next.js 14 App Router", "Spring Boot 3.x",
      "Next.js + Supabase" for an integration guide)
   B. Derive from project files — scan package.json / go.mod / build.gradle / pom.xml

2. Source verification depth?
   A. Deep — web-fetch each key source URL and verify the content exists before citing
   B. Quick — search + infer; fetch only the official docs homepage and changelog page

3. Scan project files to detect local tech configuration?
   A. Yes — read config files, detect version pins, note local conventions
   B. No — keep research generic (guide will serve multiple projects)
```

#### Research process

1. Derive `{tech-slug}` from tech name. For integration guides (e.g. Next.js + Supabase) use `{tech-a}-{tech-b}`.
2. Create `docs/dev-guides/research/` if it doesn't exist.
3. Execute each research task using WebSearch + WebFetch:

   **a. Official docs homepage** — confirm current stable version, note the exact docs URL.

   **b. Changelog / migration guide** — last 2 major or minor versions. Focus on: breaking changes, deprecations, migration hazards. Do NOT summarise features; summarise what breaks and how to fix it.

   **c. MCP server discovery** — run these searches in order, stop when found:
   1. Search `site:github.com/modelcontextprotocol/servers {tech name}`
   2. Search `"{vendor}" mcp server site:github.com`
   3. Search `"{tech name}" claude code integration official`
   4. Check the tech's own docs for an "AI" or "Claude" integration page
   
   Record: package name, install command, capabilities, source URL. If none found after all four steps, record `"none found as of {date}"` — do not fabricate.

   **d. Official CLAUDE.md / agent rules** — search `"{tech name}" CLAUDE.md site:github.com`. Check the tech's official GitHub repo root for `CLAUDE.md`, `.claude/`, or `AGENTS.md`.

   **e. Core patterns** — read the official "guides", "how-to", or "tutorials" sections. Extract 5–10 canonical patterns that cover ≥80% of real-world usage. Each pattern needs a source URL.

   **f. Anti-patterns** — read "pitfalls", "common mistakes", "migration guide", or "FAQ" sections. Blog posts are supplemental only; official source preferred.

4. Write research scratch to `docs/dev-guides/research/{tech-slug}-research.md`. Apply standard artefact frontmatter per the `metamodel` skill's `references/artefact-frontmatter.md`. Add the extra fields below:

```yaml
---
type: Stack Guide
title: Research — {Tech Name}
description: Research notes on {Tech Name} informing the developer guide.
tags: []
timestamp: <ISO 8601 datetime of last change>
status: draft
owner: {git config user.name}
last_reviewed: YYYY-MM-DD
review_interval: 90d
verified-for: {tech}@{version}
docs-url: {official docs URL}
mcp-server: {package name} | none-found
mcp-source: {github URL} | n/a
---
```

5. Sections of the research scratch:

```
## 1. Stack identity
Table: Technology · Stable version · Docs URL · Changelog URL

## 2. Changelog highlights (last 2 versions)
One paragraph per version: what broke, what was deprecated, migration steps.

## 3. MCP server / coding agent integration
Package · Install command · Capabilities · Source URL · Status (official/unofficial/none)

## 4. Core patterns (from official docs)
One H3 per pattern: name · source URL · brief description · code snippet

## 5. Anti-patterns (from official warnings + migration guides)
One H3 per anti-pattern: name · source URL · problem · fix

## 6. Official agent rules / CLAUDE.md
Content if found; "none found" with search date if not.
```

#### Do NOT in Research mode

- Invent MCP servers or CLAUDE.md files that weren't found.
- State a pattern without a source URL — every pattern in §4 traces to an official doc page.
- Rate blog posts as primary sources. Official docs and official GitHub repos are tier-1.
- Skip Step 0 — tech name + version variant is mandatory input before any research begins.

---

### Mode 2 — Draft

**Purpose:** Write the developer guide from the research scratch and optional project context.

**Prerequisite:** `docs/dev-guides/research/{tech-slug}-research.md` must exist.

#### Step 0 — Clarifying questions

```
1. Project conventions style?
   A. Opinionated — scan the codebase to extract how THIS project uses the tech
   B. Minimal — leave §Project conventions as _TODO_ placeholder

2. Code examples?
   A. Snippets from this project (requires codebase read)
   B. Generic examples matching official docs patterns
```

#### Draft process

1. Read research scratch `docs/dev-guides/research/{tech-slug}-research.md`.
2. If Step 0 answer 1A: scan relevant project files (config, source files using the tech) to extract local conventions (file structure, naming patterns, client initialisation style, etc.).
3. Write `docs/dev-guides/{tech-slug}.md` using the template in [`templates/guide-template.md`](templates/guide-template.md).
4. Apply standard frontmatter per the `metamodel` skill's `references/artefact-frontmatter.md`, plus:
   - `verified-for: {tech}@{version}` (from research scratch)
   - `docs-url: {url}` (from research scratch)
5. **§Core patterns:** 5–10 named, self-contained patterns. Each needs: When to use · Code example · One-sentence rationale. Source each pattern from the research scratch.
6. **§Project conventions:** `_TODO_` + note "populate with `dev-stack-guide` Mode 2, Step 0: 1A" if minimal; populated from scan if opinionated.
7. **§Anti-patterns:** table format — 3 columns: Anti-pattern | Problem | Fix. Minimum 3 rows.
8. **§Coding agent integration:** include exact MCP package + install command (from research), or `"No official MCP server found as of {date}"`. Include CLAUDE.md / agent rules content if found in research.

#### Do NOT in Draft mode

- Skip reading the research scratch — the guide must be grounded in verified sources.
- Leave §Anti-patterns empty — if research didn't surface anti-patterns, check the migration guide manually.
- Invent code examples that aren't runnable. Annotate `// illustrative only` if not runnable.
- Copy-paste research scratch sections verbatim — the guide is synthesised and developer-readable.

---

### Mode 3 — Refresh

**Purpose:** Update an existing guide when a version is released or the `verified-for` pin is stale (> `review_interval`).

**When to trigger:**
- `verified-for:` version no longer matches current stable.
- A breaking change affects a documented pattern.
- Guide is older than `review_interval`.

#### Step 0 — Clarifying questions

```
1. Refresh scope?
   A. Version bump only — update pin + breaking changes only
   B. Full refresh — re-run research, update all sections where docs changed
   C. Single section — I will name it

2. What triggered the refresh?
   A. New major or minor version released
   B. A pattern we follow is deprecated or removed
   C. Periodic review (no known breaking changes)
```

#### Refresh process

1. Read existing guide + research scratch.
2. Re-fetch official changelog. Compare new version to `verified-for:` pin.
3. For each breaking change affecting documented patterns:
   - Update the pattern section.
   - Add deprecation callout: `> **Deprecated as of {version}:** use {new approach} instead.`
4. Re-run MCP server discovery (step 1c from Research) — MCP support changes fast.
5. Update frontmatter: `verified-for:`, `last_reviewed:`.
6. Append to guide's `## Changelog` section: `YYYY-MM-DD: refreshed for {tech}@{version} — {summary of changes}`.
7. Update research scratch: bump `verified-for:`, add research date note.

#### Do NOT in Refresh mode

- Silently change patterns without a changelog entry.
- Mark a pattern deprecated without providing the replacement.
- Skip MCP re-check.

---

## Reference materials

- [`references/research-methodology.md`](references/research-methodology.md) — source quality tiers, MCP discovery decision tree, pattern extraction heuristics, version pinning rules.
- [`templates/guide-template.md`](templates/guide-template.md) — canonical guide output template. Copy to `docs/dev-guides/{tech-slug}.md` and populate.

---

## Anti-patterns

1. **Draft without research.** Patterns written from memory, not verified docs. Fix: Mode 1 always precedes Mode 2.

2. **MCP fabrication.** Listing a package that doesn't exist. Fix: run the four-step discovery process; record "none found" if search fails.

3. **Generic §Project conventions.** Boilerplate text instead of real project scan. Fix: Mode 2 Step 0 answer 1A triggers a codebase scan.

4. **Stale guide without refresh.** `verified-for:` ≥ 90 days old. Fix: `review_interval: 90d` triggers the `metamodel` skill's Audit mode Check 10 staleness flag — run Mode 3.

5. **Pattern count creep.** More than 10 core patterns = the guide is two guides (e.g. separate `nextjs` and `nextjs-supabase`). Fix: split when patterns no longer share the same mental model.

6. **Anti-pattern table missing.** Every meaningful technology has anti-patterns. An empty table means the research was shallow. Fix: always read the migration guide — it's the richest source of anti-patterns.

---

## Checklist

**Mode 1 — Research:**
- [ ] `docs/dev-guides/research/` exists.
- [ ] `{tech-slug}-research.md` has full frontmatter including `verified-for:`, `docs-url:`, `mcp-server:`, `mcp-source:`.
- [ ] All 6 research sections populated (§6 may say "none found" if no agent rules exist).
- [ ] MCP discovery: all four search steps attempted; result recorded explicitly.
- [ ] Changelog highlights cover last 2 major/minor versions.
- [ ] Every pattern in §4 has a source URL.
- [ ] Step 0 asked and respected.

**Mode 2 — Draft:**
- [ ] Research scratch read before writing.
- [ ] `docs/dev-guides/{tech-slug}.md` has frontmatter with `verified-for:` and `docs-url:`.
- [ ] §Stack identity table complete.
- [ ] §Prerequisites is a checklist (not prose).
- [ ] §Core patterns: 5–10 named patterns, each with code + rationale.
- [ ] §Anti-patterns: table, ≥3 rows.
- [ ] §Coding agent integration: MCP entry (package + install) or explicit "none found as of {date}".
- [ ] §Resources: table with official docs + changelog + migration guide.
- [ ] Any unresolved research gap was filed directly via `util-open-items` (no local section — ADR-0005).
- [ ] Step 0 asked and respected.

**Mode 3 — Refresh:**
- [ ] `verified-for:` updated.
- [ ] `last_reviewed:` updated.
- [ ] Changelog entry appended.
- [ ] MCP server re-checked.
- [ ] Breaking changes reflected with deprecation annotations.
- [ ] Research scratch `verified-for:` bumped.

---

## Closing report

After any mode, summarise in 5 lines:

1. Mode + file(s) created or updated (path).
2. Tech + version verified for.
3. MCP server status (found with package name / not found / unchanged).
4. Pattern count + any patterns flagged as needing a runnable example.
5. Next action (e.g. "run Mode 2 draft" / "run Mode 3 refresh before {date}").

---

## File Open Items

After Mode 2 (draft) or Mode 3 (refresh), file any unresolved research gap directly to the
central ledger via `util-open-items` at `docs/project-control/open-items/` — there is no
local section to author first (ADR-0005). File nothing if there's nothing to file.
