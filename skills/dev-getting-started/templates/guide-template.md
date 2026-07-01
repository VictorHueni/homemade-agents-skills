---
type: Getting Started Guide
title: Getting Started — {Project Name}
description: How to set up, run, and contribute to {Project Name}.
tags: []
timestamp: <ISO 8601 datetime of last change>
status: draft
owner: {{git config user.name}}
last_reviewed: YYYY-MM-DD
review_interval: 180d
---

# Getting Started — {Project Name}

> Audience: any developer joining this project for the first time. Follow this guide top-to-bottom — you should have a running local environment by the end.

---

## Prerequisites

Install all of these before proceeding. Exact versions matter — do not substitute with "latest".

- [ ] {Language runtime} {version} — [{install link}]({url})
- [ ] Docker {version} + Docker Compose — [docker.com/get-started](https://www.docker.com/get-started)
- [ ] {CLI tool} {version} — [{install link}]({url})
- [ ] {Access requirement — e.g. "Supabase account + project with API keys"}

---

## Clone & bootstrap

```bash
# 1. Clone the repo
git clone {repo-url}
cd {repo-name}

# 2. Install dependencies
{install command — e.g. npm install}

# 3. {Any post-install step — e.g. copy env file}
cp .env.example .env
```

---

## Environment setup

Copy `.env.example` to `.env` (if you haven't already) and fill in the following values.

| Variable | Required | Description | Where to get it |
|---|---|---|---|
| `{VAR_NAME}` | Yes | {what it does} | {source — e.g. "Supabase project settings > API"} |
| `{VAR_NAME}` | Yes | {what it does} | {source} |
| `{VAR_NAME}` | No | {what it does — consequence of leaving unset} | {source or "any string"} |

> Leave `_TODO_` for any variable whose source is unclear — add it to §Open Items below.

---

## Running locally

{One command to start everything:}

```bash
{start command — e.g. docker compose up -d / make dev / npm run dev}
```

Services started:

| Service | What it does | Port | Health check |
|---|---|---|---|
| {service-name} | {description} | `{port}` | `http://localhost:{port}/{path}` |
| {service-name} | {description} | `{port}` | — |

To restart a single service:

```bash
{per-service restart command}
```

---

## Common dev tasks

| Task | Command | When to run |
|---|---|---|
| Run all tests | `{test command}` | Before every PR |
| Run linter | `{lint command}` | Before every commit |
| Run formatter | `{format command}` | Before every commit |
| Run database migrations | `{migrate command}` | After pulling changes that include new migrations |
| Generate types / code | `{generate command}` | After modifying schema or API spec |
| Seed local database | `{seed command}` | After first clone or after dropping the database |

---

## Coding agent setup

### CLAUDE.md

This project has a `CLAUDE.md` at repo root. It loads automatically in Claude Code and contains: {summary of what CLAUDE.md covers}.

```bash
# To load it explicitly in a new session:
cat CLAUDE.md
```

### MCP servers

The following MCP servers are configured for this project in `.mcp.json`:

| Server | Purpose | How to enable |
|---|---|---|
| {server-name} | {what it provides} | {already in .mcp.json — auto-loads / or: `{install command}`} |

> If `.mcp.json` doesn't exist: `# No MCP servers configured for this project yet.`

### Tips for AI-assisted development

- {tip 1 — e.g. "Reference @docs/dev-guides/ guides in your prompts for stack-specific context"}
- {tip 2 — e.g. "Use `make test` before asking Claude to debug — include the test output"}
- {tip 3}

---

## Troubleshooting

### Port already in use

```bash
# Find what's using the port
lsof -i :{port}
# Kill it
kill -9 {PID}
```

### Missing environment variable

If the app fails with `{env var not found / undefined error}`:

1. Check that `.env` exists: `ls .env`
2. Check that the variable is set: `grep {VAR_NAME} .env`
3. If missing, add it from `.env.example`.

### Docker not running

```bash
# Check Docker daemon
docker info
# If not running: start Docker Desktop / `sudo systemctl start docker`
```

### {Project-specific issue 1}

{Description of the issue and exact fix.}

### {Project-specific issue 2}

{Description and fix.}

---

## Open Items

| OI-ID  | Type           | Summary | Source anchor | Source heading | Resolution path | Priority | Status | Owner | Due / Review date | Tracker ref |
| :----- | :------------- | :------ | :------------ | :------------- | :-------------- | :------- | :----- | :---- | :---------------- | :---------- |

_None at present._

---

## Changelog

| Date | Summary |
|---|---|
| YYYY-MM-DD | Initial guide created |
