# Research 0001 — Open-Items / Tech-Debt Management for Agent-Driven Execution

Date: 2026-07-20
Status: decision-support (no decision taken yet)
Context: multi-project setup, solo maintainer (team possible later), per-repo tracking
acceptable, all four agent flows desired (human points agent at issue · agent self-selects
from queue · triggered automation · batch grooming).

## 1. Problem statement

Across several projects, unresolved work (tech debt, open items) is captured in large
markdown lists. The maintainer suspects this is inefficient and wants a leaner system —
GitHub Issues, Jira, Linear, or similar — with concrete classification, description
templates, prioritization, and categorization, such that coding agents (Claude Code) can be
directed at open issues to tackle them one by one.

**Prior art in this kit.** This repo already solved a large part of this:

- `util-open-items` skill (v2.0.0) with 7 modes (sync/triage/close/drop/archive/report/migrate).
- Governance contract (`metamodel` skill, `references/open-items-governance.md`): 4-type
  taxonomy (`doc-gap`/`decision-gap`/`execution-item`/`tech-debt`), 5-state lifecycle,
  provenance triple, evidence-gated closure.
- Pluggable backend (ADR-0002): `markdown` default, `github` (Issues) opt-in per project
  (ADR-0003). **This kit repo migrated to the `github` backend on 2026-06-04** and uses it
  actively (29 open `open-item` issues as of 2026-07-20; filings as recent as 2026-07-19).

**Observed gaps in the current `github` backend (live audit, 2026-07-20):**

1. `priority` lives only in the issue body (`### Priority`) — not filterable/sortable by a
   human or an agent without parsing bodies.
2. No effort/size signal and no readiness signal — nothing marks which items are safely
   delegable to an agent vs. need a human decision first.
3. The Project (v2) read-out planned in ADR-0002 was never wired up (form `projects:` line
   still commented out).
4. ~60% of open items are stale migrated "candidate skill" backlog rows sitting
   undifferentiated next to actionable tech debt.

## 2. Research method

Three parallel research agents (2026-07-20): (a) practices/workflows of AI-driven teams,
(b) tool landscape, (c) classification/template/prioritization systems. Key sources are
cited inline below; several primary pages were proxy-blocked (403) for the agents and were
verified via multiple secondary extracts — flagged where relevant.

## 3. Key findings

### 3.1 The verdict on big markdown lists

Research supports the suspicion. Unstructured `TODO.md`-style files are a documented
anti-pattern ("no spec and thousands of incompatible formats" — tasksmd.github.io); solo
developers report moving from "sprawling Markdown specification files" to GitHub Issues
"because they evolve with the project and form a living history" (dev.to, Claude Code series).
The kit's *structured* markdown ledger is much better than a raw TODO file, but still loses
to an issue tracker on: native monotonic IDs, structural closure evidence, assignment,
per-item conversation history, and — decisive for this goal — the agent round-trip (MCP /
`gh` / native agent assignment).

### 3.2 Industry convergence (2025–2026)

- **"Assign an issue to an agent" is now a first-class primitive everywhere**: GitHub
  (Copilot coding agent GA, Agent HQ with Claude/Codex in preview), Linear (Agent
  Interaction SDK; issues are *delegated* to agents, human stays assignee), Jira (Rovo Dev).
- **Every major tracker ships an official remote MCP server** (GitHub, Linear, Atlassian) —
  the standard read/write surface for locally-run agents.
- **Anthropic's own documented recommendation is deliberately boring**: GitHub Issues +
  `gh` CLI + a `/fix-issue <n>`-style skill + the `@claude` GitHub Action; no new tracker
  (code.claude.com/docs/en/best-practices).
- A git-native agent-first tracker category appeared (beads, Backlog.md, Task Master) —
  with an equally fast community backlash favoring minimal markdown over heavyweight agent
  infrastructure (HN threads on beads).

### 3.3 What makes an issue agent-executable (evidence)

- Empirical study of Copilot-agent PRs (arXiv 2512.21426): well-formed issues merged at
  **77.1% vs 45.9%** for poor ones. Positive predictors: well-scoped, self-contained, names
  the relevant files, gives implementation guidance. Negative: reliance on context the
  agent can't reach.
- dotnet/runtime, 10 months, 878 agent PRs: success 41.7% → 67.9%; the single biggest
  lever was a repo instructions file with build/test commands (38.1% → 69%). Cleanup/
  tech-debt tasks had the highest success (84.7%).
- Devin's sizing heuristic: tasks "a junior engineer could do in 4–8 hours" with clear
  upfront requirements and verifiable outcomes.
- Anthropic: the #1 lever is **a check the agent can run** (test suite, build, lint) so it
  iterates until pass instead of stopping at "looks done".
- Converged agent-ready issue anatomy (GitHub WRAP, Linear, Devin, Anthropic):
  1. What needs to change and why.
  2. References — files, symbols, prior PRs, patterns to imitate.
  3. Acceptance criteria, machine-checkable where possible + a verification command.
  4. Precautions / out-of-scope.
  5. One-PR size bound.
  6. Repo/environment context lives in `CLAUDE.md`/instructions file, NOT repeated per issue.
- **Over-specification is a documented anti-pattern** ("curse of instructions") — enough
  spec to orient + constraints, then iterate.

### 3.4 Classification & prioritization that survives contact with practice

- Intent taxonomies (Fowler quadrant) and 13-type academic ontologies do not survive in
  real trackers; classification is only useful as far as it changes the *action*.
- Google's tech-debt program (IEEE Software 2023): **117 objective code metrics, none
  predicted engineer-reported debt** (<1% variance explained) — human/agent judgment
  per-item beats automated debt scoring.
- Lean prioritization consensus: t-shirt size (S/M/L) + P0–P3 (or a 2×2) + a hand-ranked
  top-5. Recommended against: RICE-style score theater, planning poker for backlog items.
- Labels: prefixed groups (`type:`, `priority:`, one state axis, optional `size:`/`area:`),
  2–4 labels per issue, under ~15 total before rot.
- **The single most agent-relevant labeling addition is a state machine**
  (Matt Pocock's `/triage` pattern): `needs-triage` → `needs-info` | `ready-for-agent` |
  `ready-for-human` | `wontfix`. "Ready-for-agent means a brief is attached and an agent
  should take the next step." Triage runs periodically to keep that column *trustworthy*.
- Backlog hygiene: issue bankruptcy "works once, then six months later you're back";
  durable fix = intake templates + stated staleness policy + short routine triage (10–15
  min). Linear's philosophy: keep a manageable backlog; accept that low-priority items
  never get fixed and important ones resurface.

### 3.5 Failure modes to design against

| Failure | Mitigation |
| :--- | :--- |
| Agent can't build/test → unvalidated PRs | Per-repo instructions file with build/test commands (biggest measured lever) |
| Ambiguous issue → off-target PR | WRAP anatomy; only `ready-for-agent` items get delegated |
| Review bottleneck (agent PRs outrun human review) | Atomic one-PR issues; verification evidence required in PR; throttle dispatch |
| Backlog rot / untrusted queue | State labels + staleness policy + periodic agent-assisted triage |
| Mid-task scope change | Scope fully upfront; cancel and re-delegate rather than steer mid-flight |

## 4. Tool landscape summary

| Tool | Agent round-trip | Fit here |
| :--- | :--- | :--- |
| **GitHub Issues (+ optional Projects v2)** | Best-supported: `@claude` Action, Copilot/Agent-HQ assignment, official MCP, `gh` CLI | Free, where the code lives; kit backend already validated. Issue Types are org-only (label fallback already built) |
| **Linear** | Purpose-built delegation UX + MCP; **no first-party Claude Code agent** (needs Cyrus or MCP) | Best UX if a team forms; free tier caps at 250 active issues; SaaS lock-in; would be a 3rd kit backend |
| **Jira** | Rovo MCP + Rovo Dev, but AI requires paid tiers | Admin surface disproportionate for solo; ruled out |
| **beads (bd)** | `bd ready` → claim → close; git-synced graph DB | Interesting but churning (Dolt rewrite, invasive-git-hooks backlash); maturity risk |
| **Backlog.md** | Task-per-markdown-file + built-in MCP; diff-reviewable | Strong candidate to *replace the kit's markdown backend* for non-GitHub/offline projects |
| Vibe Kanban / Task Master | Local orchestration UIs | Not a durable system of record; out of scope |

No tool cheaply solves cross-repo aggregation for agents; per-repo (accepted constraint)
avoids the problem. GitHub Projects can span repos within an org if a roll-up is wanted later.

## 5. Proposed setups (pros/cons)

### Option A — GitHub-native lean: evolve the kit's `github` backend (recommended)

Keep GitHub Issues as the per-project backend; close the observed gaps with an
**agent-execution layer** on top of the existing governance layer:

1. **Labels as the queryable surface** (works on personal repos, no org needed):
   `type:*` (exists) + `priority:{p0..p3}` + `size:{S,M,L}` + state axis
   `needs-triage` / `ready-for-agent` / `needs-human` / `blocked`. Under 15 labels total.
2. **Issue form v2**: keep governance fields (type, provenance, resolution path); add the
   agent-ready fields — code pointers, acceptance criteria / verification command,
   out-of-scope. Priority moves from body to label.
3. **Delegation loop**: a `/fix-issue <n>`-style skill (fetch issue → plan → implement →
   verify → PR with `Closes #n`); agent self-selection = "pick highest-priority
   `ready-for-agent` issue"; triggered automation via the `@claude` GitHub Action;
   batch grooming = extend `util-open-items` `triage` mode to propose state-label
   promotions and staleness closures.
4. **Per-repo `CLAUDE.md` with build/test/verify commands** (the measured 38→69% lever).
5. Roll out to other GitHub-hosted projects via the existing adoption checklist +
   Mode 7 migration script.

- **Pros:** free; zero new systems; everything lives with the code; kit machinery already
  built and dogfooded; supports all four desired agent flows; markdown backend remains the
  fallback for non-GitHub projects; team-ready (GitHub collaboration is native).
- **Cons:** read-out UX is issue-list filters unless Projects v2 is added; no cross-repo
  view without an org; governance form is heavier than a plain tech-debt template (mitigable
  with a second lighter form).

### Option B — Option A + Projects v2 board (finish ADR-0002's read-out)

Add the planned Project with Status/Priority/Review-date fields as the triage/report surface.

- **Pros:** materially better human read-out (grouping, saved views); fields are API/MCP
  accessible; closest to the original ADR-0002 design.
- **Cons:** duplication between labels and Project fields (two places to update priority);
  Project automation upkeep for one person; agents work more naturally with labels.
  Sensible as a *later* additive step once label volume justifies it.

### Option C — Linear as the execution frontend (GitHub sync)

Adopt Linear per project (or one workspace, per-project teams), delegate issues to agents,
sync to GitHub.

- **Pros:** best-in-class triage inbox + delegation UX; mobile; agents-as-teammates model;
  scales smoothly to a team.
- **Cons:** Claude Code needs a third-party runner (Cyrus) or MCP-only integration; 250
  active-issue free cap across a multi-repo debt backlog; SaaS lock-in; splits the system
  of record from the code; would require building a third kit backend. Revisit if/when a
  team forms and the delegation UX earns its cost.

### Option D — Git-native agent tracker in-repo (Backlog.md; beads watched)

Replace markdown ledgers with Backlog.md task files + its MCP server per repo.

- **Pros:** highest portability (plain markdown, offline, non-GitHub remotes); everything
  reviewable as git diffs; built-in agent surface.
- **Cons:** no hosted UI/notifications; another per-repo tool; duplicates GitHub Issues
  where GitHub is available; beads specifically carries maturity/churn risk. Best scoped as
  a candidate *replacement for the `markdown` backend* on non-GitHub projects, not the
  primary system.

## 6. Recommendation

**Option A now; B as an optional later layer; D only for non-GitHub projects; C deferred
until a team exists; Jira ruled out.** Process-wise: a 15-minute agent-assisted triage on a
fixed cadence (keep the `ready-for-agent` queue trustworthy, apply a stated staleness
policy), hand-rank a top-5 instead of scoring, and treat governance items (`decision-gap`,
`doc-gap`) and delegable execution items (`execution-item`, `tech-debt` with `ready-for-agent`)
as two views over one backlog rather than two systems.

## 7. Source index (primary)

- code.claude.com/docs/en/best-practices · docs.github.com Copilot coding-agent best practices
- github.blog: WRAP; Agent HQ; issue-types/sub-issues GA · devblogs.microsoft.com dotnet/runtime CCA retrospective
- arXiv 2512.21426 (issue readiness → merge rate) · IEEE Software 2023 (Google tech-debt program)
- linear.app/developers/agents · linear.app/docs/mcp · aihero.dev `/triage` state machine
- github.com/steveyegge/beads · github.com/MrLesk/Backlog.md · basecamp.com/shapeup (bets-not-backlogs)
