# Research Methodology — dev-stack-guide

Internal Claude reference. Not copied to projects. Covers source quality tiers, MCP discovery decision tree, pattern extraction heuristics, version pinning strategy, and anti-pattern sourcing.

---

## Source quality tiers

| Tier | Examples | Use for | Max confidence |
|---|---|---|---|
| **1 — Primary (load-bearing)** | Official docs · Official GitHub repo · Official changelog / migration guide | Core patterns, version facts, MCP server, deprecation notices | ★★★★★ |
| **2 — Official adjacent** | Official blog posts · Official YouTube / conference talks by maintainers | Patterns still being formalised, architectural rationale | ★★★★ |
| **3 — Community recognised** | GitHub Discussions marked as answered by maintainer · Official RFC / proposals | Emerging patterns not yet in docs | ★★★ |
| **4 — Community** | Stack Overflow · Reddit · blog posts by non-maintainers | Confirmation of anti-patterns, gotchas | ★★ |
| **5 — Anecdotal** | Twitter/X threads, Discord, personal blogs | Do not cite directly — use only to identify where to look in official docs | ★ |

**Rule:** every pattern in a published guide must trace to Tier 1 or Tier 2. Tier 3–5 are useful for discovering topics to look up in Tier 1, never for the citation itself.

---

## MCP server discovery decision tree

Run these steps in order. Stop at the first positive result.

```
Step 1: Search `site:github.com/modelcontextprotocol/servers {tech name}`
        → This is the official community MCP server index.
        → If found: record package name, README link, capabilities.

Step 2: Search `{vendor name} mcp-server site:github.com`
        → Vendors often publish under their own org (e.g. github.com/supabase/mcp-server-supabase).
        → If found: verify it is maintained by the vendor (check org ownership).

Step 3: Search `{tech name} modelcontextprotocol OR "mcp server" site:github.com`
        → Community forks + third-party implementations.
        → If found: flag as unofficial — note the maintainer + last-commit date.

Step 4: Check the tech's official docs for an "Integrations", "AI", or "Claude" page.
        → Some vendors document their MCP server in their own docs without publishing to the central index.

Step 5: Search `"{tech name}" claude code integration`
        → Catch any newer integrations not indexed above.

If all 5 steps return nothing: record `mcp-server: none-found` + `mcp-source: n/a` + date.
```

**Never fabricate an MCP package name.** An incorrect package is worse than no package — it breaks agent setup silently.

---

## Pattern extraction heuristics

When reading official docs to extract core patterns:

1. **Target "how-to" and "guides" sections**, not "reference" sections. Reference docs describe APIs; guides show idiomatic usage.

2. **A pattern is canonical if the official docs show it as the first or recommended example.** If it's buried under "advanced usage", it's not a core pattern.

3. **5–10 patterns per guide.** Use the following selection criteria:
   - Covers the most common entry point (initialisation, authentication, first query/call)
   - Covers the most common operation type (CRUD, subscription, event handling)
   - Covers the most common error case (connection failure, auth error, rate limit)
   - Covers the recommended testing approach (mocking, integration, contract)
   - Covers the recommended configuration approach (env vars, config files, DI)

4. **Integration guides (tech-a + tech-b):** extract patterns for the interaction surface specifically. Do not re-document each tech's own patterns — reference the individual guides instead.

5. **Code examples:** prefer the language used in the target project (detected from project scan in Mode 2). If generic, use the language the official docs use for their primary examples.

---

## Anti-pattern sourcing

The richest sources of anti-patterns, in order:

1. **Official migration guide** — explicitly documents what changed and why the old approach was wrong.
2. **Official "common mistakes" / "FAQ" / "troubleshooting" sections** — these are documented precisely because they are common.
3. **Changelog "breaking changes" section** — implies the old way was acceptable before but is now wrong.
4. **Official GitHub issues marked "documented" or "known limitation"** — confirms the anti-pattern is real and acknowledged.

Anti-patterns sourced from Tier 4 community sources (blog posts, Reddit) must be cross-checked against official docs before inclusion. If they cannot be confirmed in Tier 1/2, omit them from the guide — include in §Open Items as a `doc-gap` instead.

---

## Version pinning strategy

- **`verified-for:` in frontmatter** — always the exact stable version at research time (e.g. `supabase@2.39.8`, `spring-boot@3.2.5`). Not a range, not `^version`.
- **`review_interval: 90d`** — triggers `util-metamodel-audit` Check 10 staleness flag. Refresh cadence:
  - Actively maintained tech with monthly releases: 60d
  - Stable tech with quarterly releases: 90d (default)
  - Foundational tech with annual releases: 180d
- **In code examples:** follow the tech's own version convention. If the official docs use `^version`, use that in examples — but pin the specific version in the frontmatter separately.
- **When the guide spans multiple major versions:** split into separate guide files or create a §Compatibility section noting which patterns apply to which version range.

---

## Research scratch lifecycle

| State | Meaning | Trigger |
|---|---|---|
| `status: draft` | Research in progress; not yet consumed by a guide | Mode 1 scaffold |
| `status: active` | Research complete; guide has been drafted from it | Mode 2 draft |
| `status: refreshed` | Research re-run for a new version; guide updated | Mode 3 refresh |
| `status: archived` | Tech is no longer used in the project; guide superseded | Manual action |

The research scratch is NOT a published document — it is internal scaffolding. It does not need to follow the full open-items governance lifecycle. Gaps discovered during research that may not be resolved before Mode 2 runs should still be filed directly to the central ledger (`doc-gap`, citing this scratch file as `Source artefact`) rather than lost — there is no local section to hold them.
