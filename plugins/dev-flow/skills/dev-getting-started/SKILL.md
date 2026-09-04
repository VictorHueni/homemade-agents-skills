---
name: dev-getting-started
license: MIT
description: "Scaffold and populate a project-specific getting-started guide at docs/dev-guides/getting-started.md. Reads real project files (package.json, docker-compose.yml, .env.example, Makefile, CI config, CLAUDE.md) to emit exact commands for clone-to-run setup, environment variables, local dev workflow, common tasks, coding agent setup, and troubleshooting. Three modes: scaffold (creates with _TODO_ placeholders), fill (populates from project files with real commands), refresh (detects changes, updates stale sections). Triggers on: getting started guide, onboarding guide, dev setup guide, local dev guide, how to run this project, developer onboarding, setup guide, first run guide, new developer setup."
user-invocable: true
metadata:
  category: "developer-documentation"
  complexity: "low"
  version: "1.0.0"
  status: active
  last_reviewed: 2026-05-28
  review_interval: 180d
  impact: "low"
---

# dev-getting-started

You are an expert at producing **project-specific getting-started guides** — the document a developer reads on day one to go from zero to a running local environment. No web research needed: this skill reads the actual project to generate real commands, real env vars, and real service names.

A getting-started guide is good when a brand-new developer can run through it top-to-bottom without asking anyone a question.

**Output:** `docs/dev-guides/getting-started.md` (singleton per project)

---

## The three modes

| Mode | When | Process |
|---|---|---|
| **1 — scaffold** | No guide exists | Create file with _TODO_ placeholders + pre-fill what can be detected from project structure |
| **2 — fill** | Scaffold exists (or create + fill in one pass) | Read project files, populate every section with real commands |
| **3 — refresh** | Guide exists; project has changed | Re-read project files, detect stale sections, update + append changelog entry |

---

### Mode 1 — Scaffold

**Process:**

1. Create `docs/dev-guides/` folder if it doesn't exist.
2. Run a quick project scan (read-only — no user input needed yet):
   - `ls` project root to detect: `package.json`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle`, `docker-compose.yml`, `Makefile`, `justfile`, `Taskfile.yml`, `.env.example`, `CLAUDE.md`, `.mcp.json`, `.github/`, `.gitlab-ci.yml`
   - Detect primary language and runtime from the manifest file found.
3. Copy [`templates/guide-template.md`](templates/guide-template.md) to `docs/dev-guides/getting-started.md`.
4. Pre-fill what is detectable:
   - §Prerequisites: detected language + runtime (e.g. "Node.js ≥ {version from package.json `engines`}")
   - §Coding agent setup: if `CLAUDE.md` and/or `.mcp.json` exist, note them
5. Leave all undetectable sections as `_TODO_` with a comment explaining what to fill.
6. Apply standard artefact frontmatter per the `metamodel` skill's `references/artefact-frontmatter.md`.

**Do NOT in Scaffold mode:**
- Invent commands that haven't been detected from project files.
- Leave sections without `_TODO_` when content is unknown — every missing piece must be marked.

---

### Mode 2 — Fill

**Purpose:** Populate every section with accurate, project-specific content. This is the primary mode.

#### Step 0 — Clarifying questions (ask BEFORE reading files)

Single message. Users respond like `1B, 2A, 3C`:

```
1. Project type?
   A. Web app (frontend + backend, or full-stack framework like Next.js / Nuxt)
   B. API only (REST, gRPC, GraphQL)
   C. CLI tool
   D. Library / package
   E. Monorepo (multiple apps — I will list which to cover)

2. Local dev approach?
   A. Docker Compose — all services containerised
   B. Native — run services directly with language runtime
   C. Hybrid — some services in Docker, some native
   D. Cloud / remote — no local run (e.g. serverless or cloud-only dev)

3. Any setup steps that aren't captured in config files?
   A. No — everything is scripted
   B. Yes — I will describe them (e.g. "create account at X", "get API key from Y", "seed with script Z")
```

#### File reading strategy

Read these files in order, extracting information for each guide section:

| File | What to extract |
|---|---|
| `package.json` | `engines.node` (runtime version), `scripts` (dev, test, build, lint, format), `name` (project name) |
| `go.mod` | Go version, module name |
| `pom.xml` / `build.gradle` / `mvnw` | Java / Kotlin version (from `<maven.compiler.release>` or `sourceCompatibility`), build/test/verify commands - always run via the wrapper (`./mvnw`), never a bare `mvn` |
| `Cargo.toml` | Rust edition, binary name, `cargo` commands |
| `docker-compose.yml` / `docker-compose.dev.yml` | Services list, port mappings, depends_on order, volume mounts |
| `.env.example` / `.env.template` | Required env vars, with descriptions if commented |
| `Makefile` / `justfile` / `Taskfile.yml` | Named tasks: which ones are used daily (dev, test, lint, migrate, seed) |
| `README.md` | Any setup instructions not captured elsewhere; project overview sentence |
| `.github/workflows/*.yml` / `.gitlab-ci.yml` | CI setup commands; install + test commands used in CI = the canonical way |
| `CLAUDE.md` | Agent setup instructions, memory pointers, MCP server list |
| `.mcp.json` | MCP servers configured for this project |
| `.tool-versions` / `.nvmrc` / `.node-version` / `.python-version` / `mise.toml` / `.sdkmanrc` / `<maven.compiler.release>` (pom.xml) | Exact runtime version pins |

#### Fill process

For each guide section, read the relevant files above and emit:

1. **§Prerequisites** — explicit list with exact versions. No ranges — the developer should install the exact pinned version. Include: language runtime, Docker (if used), CLIs (project-specific), access tokens or API keys needed before running.

2. **§Clone & bootstrap** — exact shell commands in order. Include `git clone`, `cd`, package install, any post-install hooks. Use the CI commands as the canonical source (what passes CI is what works).

3. **§Environment setup** — for every variable in `.env.example`:
   - Name + example value (if safe) or placeholder (`YOUR_SECRET_HERE`)
   - One-sentence description of what it controls
   - Where to get the value (e.g. "from your Supabase project settings > API")
   - Whether it's required or optional (with the consequence of leaving it unset)

4. **§Running locally** — for each service in `docker-compose.yml` (or equivalent): service name, what it does, which port it exposes, health-check URL if available. One command to start everything, one command per service to restart individually.

5. **§Common dev tasks** — list from `Makefile`/`package.json scripts`/`justfile`. For each task: command, what it does, when to run it. Group: testing, linting, migration, generation, seeding.

6. **§Coding agent setup** — read `CLAUDE.md` and `.mcp.json`. Emit: CLAUDE.md location and summary, list of MCP servers with their purpose, any project-specific agent instructions.

7. **§Troubleshooting** — ask the user (Step 0 answer 3B) for undocumented gotchas. Always include: port already in use (how to find and kill), env var missing (error message + fix), Docker not running (check command + fix). Add project-specific ones from Step 0.

#### Do NOT in Fill mode

- Invent commands. If a script doesn't appear in the project files, it doesn't belong here.
- Paraphrase `.env.example` — extract and list every variable exactly as named.
- Skip Step 0 — the three answers change which sections are populated and how.
- Leave any section with more than one `_TODO_` unexplained. Every `_TODO_` needs a comment explaining what to fill and where to find the info.

---

### Mode 3 — Refresh

**Purpose:** Keep the guide accurate after the project evolves.

**When to trigger:**
- A new service was added to `docker-compose.yml`.
- New env vars appeared in `.env.example`.
- `Makefile` / scripts changed significantly.
- `CLAUDE.md` or `.mcp.json` was updated.
- Guide is older than `review_interval`.

#### Step 0 — Clarifying questions

```
1. What changed? (check all that apply)
   A. New dependencies or runtime version
   B. New env vars or secrets
   C. New services or changed ports
   D. New dev tasks or changed scripts
   E. Agent setup changed (CLAUDE.md / MCP servers)
   F. Unknown — do a full re-scan

2. Are there undocumented manual steps that should be added?
   A. No
   B. Yes — I will describe them
```

#### Refresh process

1. Re-read all project files listed in the file reading strategy above.
2. Diff against the current guide content.
3. For each section where content has changed:
   - Update the section with accurate current content.
   - Add a `> **Updated YYYY-MM-DD:** {what changed}` callout at the top of the updated section.
4. Update frontmatter `last_reviewed:`.
5. Append to `## Changelog`: `YYYY-MM-DD: {summary of changes}`.

---

## Anti-patterns

1. **Invented commands.** Commands that appear in the guide but not in any project file. If it breaks on a fresh machine, the guide is wrong. Fix: every command traces to a file in the project.

2. **Partial env var list.** `.env.example` has 12 vars; the guide documents 8. Fix: iterate every line in `.env.example` — no skipping "obvious" ones.

3. **Prose instructions instead of shell commands.** "Install the dependencies" instead of `npm install`. Fix: every bootstrap step is a shell command the developer can copy-paste.

4. **Missing troubleshooting section.** Every project has gotchas. Fix: always include at least the three universal troubleshooting entries (port conflict, missing env var, Docker not running) plus project-specific ones from Step 0.

5. **No coding agent setup section.** `CLAUDE.md` and `.mcp.json` exist but the guide doesn't mention them. Fix: always check for these files and document the agent setup — it's one of the most valuable parts of the guide for AI-assisted development.

6. **Stale after project evolution.** Guide was filled once and never refreshed. Fix: `review_interval: 180d` triggers the `metamodel` skill's Audit mode Check 10 staleness flag — run Mode 3.

---

## Checklist

**Mode 1 — Scaffold:**
- [ ] `docs/dev-guides/` exists.
- [ ] `getting-started.md` created with full frontmatter.
- [ ] Detected runtime/language pre-filled in §Prerequisites.
- [ ] `CLAUDE.md` and `.mcp.json` presence noted in §Coding agent setup (if found).
- [ ] All undetectable sections marked with `_TODO_` + explanation comment.

**Mode 2 — Fill:**
- [ ] Step 0 asked and respected.
- [ ] Every `.env.example` variable documented in §Environment setup.
- [ ] Every Docker service listed with port + health-check URL (if applicable).
- [ ] §Common dev tasks covers: install, dev server, test, lint, migrate (where applicable).
- [ ] §Coding agent setup documents `CLAUDE.md` + `.mcp.json` content (if files exist).
- [ ] §Troubleshooting has ≥3 entries (the three universal ones at minimum).
- [ ] No invented commands — every command traces to a project file.
- [ ] Frontmatter `last_reviewed:` set to today.

**Mode 3 — Refresh:**
- [ ] All project files re-read.
- [ ] Changed sections updated with callout note.
- [ ] `last_reviewed:` updated.
- [ ] Changelog entry appended.

---

## Closing report

After any mode, summarise in 4 lines:

1. Mode + file path.
2. Sections populated vs. remaining `_TODO_`.
3. Key findings (e.g. "12 env vars documented, 2 Docker services, 1 MCP server found").
4. Next action (e.g. "fill §Project-specific gotchas with your team's known issues" or "refresh in 180 days").
