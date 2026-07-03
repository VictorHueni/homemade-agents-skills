---
type: Stack Guide
title: {Tech Name} Developer Guide
description: Developer guide for building with {Tech Name} — patterns, anti-patterns, best practices.
tags: []
timestamp: <ISO 8601 datetime of last change>
status: draft
owner: {{git config user.name}}
last_reviewed: YYYY-MM-DD
review_interval: 90d
verified-for: {tech}@{version}
docs-url: {official docs URL}
---

# {Tech Name} Developer Guide

> Verified for **{tech}@{version}** · [Official docs]({docs-url}) · Last reviewed: YYYY-MM-DD

---

## Stack identity

| Field | Value |
|---|---|
| Technology | {name} |
| Stable version | {version} |
| Official docs | [{url}]({url}) |
| Changelog | [{changelog-url}]({changelog-url}) |
| MCP server | {package name} / none found as of {date} |
| Researched | {date} |

---

## Prerequisites

What must be installed or configured before using this technology in development.

- [ ] {prerequisite 1 — e.g. Node.js ≥ 20, Docker, Go ≥ 1.22}
- [ ] {prerequisite 2}
- [ ] {prerequisite 3 — CLIs, environment variables, access credentials}

---

## Getting started

The minimum code to have a working integration — nothing more.

```{lang}
// Minimal example: {what this does}
{minimal working code}
```

> If this is an integration guide (tech-a + tech-b), show the minimal wiring between the two here, then refer to each individual guide for deeper usage.

---

## Core patterns

The canonical usage patterns that cover ≥80% of real-world use. Each is self-contained.

### Pattern 1: {name}

**When to use:** {the situation that calls for this pattern}

```{lang}
{code example}
```

**Why this works:** {one-sentence rationale — what makes this the right approach}

---

### Pattern 2: {name}

**When to use:** {situation}

```{lang}
{code}
```

**Why this works:** {rationale}

---

<!-- Repeat for each pattern. 5 minimum, 10 maximum. -->

---

## Project conventions

How THIS project uses {tech} — opinionated defaults that differ from vanilla setup or official examples.

> _TODO_: populate by running `dev-stack-guide` Mode 2 with Step 0 answer `1A` (codebase scan). Until then, see the individual stack files in the project for conventions.

<!-- When populated, document: client initialisation style, file structure, naming patterns,
     config location, any project-specific wrappers or abstractions. -->

---

## Anti-patterns

What NOT to do — and why.

| Anti-pattern | Problem | Fix |
|---|---|---|
| {anti-pattern 1} | {why it causes issues} | {correct approach} |
| {anti-pattern 2} | {why it causes issues} | {correct approach} |
| {anti-pattern 3} | {why it causes issues} | {correct approach} |

---

## Coding agent integration

### Official MCP server

| Field | Value |
|---|---|
| Package | {package name} |
| Install | `{install command}` |
| Capabilities | {list of what the MCP server can do} |
| Source | [{github-url}]({github-url}) |
| Status | official / unofficial / none found as of {date} |

> If no official MCP server exists: `No official MCP server found as of {date}. Re-check with Mode 3 refresh or search [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers).`

### Official agent rules

{Content from official CLAUDE.md or agent integration guide, if found. Otherwise: "No official CLAUDE.md or agent rules found as of {date}."}

### Agent-friendly tips

Tips for working effectively with Claude Code in this stack:

- {tip 1 — e.g. "Add the MCP server to `.mcp.json` at project root so it loads automatically"}
- {tip 2 — e.g. "Reference this guide in CLAUDE.md with `@docs/dev-guides/{tech-slug}.md` for agent context"}
- {tip 3 — e.g. "Use pattern X when prompting the agent — it maps directly to the §Core patterns here"}

---

## Resources

| Resource | URL | Purpose |
|---|---|---|
| Official docs | [{url}]({url}) | Primary reference |
| Changelog | [{url}]({url}) | Breaking changes + new features |
| Migration guide | [{url}]({url}) | Version upgrade instructions |
| GitHub repo | [{url}]({url}) | Issues, discussions, source |

---

## Changelog

| Date | Version | Summary |
|---|---|---|
| YYYY-MM-DD | {tech}@{version} | Initial guide drafted |
