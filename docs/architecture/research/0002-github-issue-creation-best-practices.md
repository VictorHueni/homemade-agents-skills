# Research 0002 — GitHub Issue Creation Best Practices

Date: 2026-07-20
Status: decision-support (feeds the Option A design from research 0001)
Scope: the creation/intake moment — titles, forms, routing, metadata, agent-authored
issues, creation-time automation. 2025–2026 state. Companion to
[research 0001](0001-open-items-agent-execution-setup.md).

## 1. Titles

- Consensus: short, specific, searchable symptom/outcome statements. Bugs = descriptive
  symptom ("Crash when X under Y"); tasks = imperative outcome ("Add retry to upload
  client"). Categorization belongs in labels/issue-types, not the title.
- `[BUG]`-style prefixes are treated as redundant by major repos (Vite applies a label and
  no prefix); the one legitimate niche is machine-parsed intake (rust's `[ICE]:` prefill is
  grepped by tooling). No formal "anti-pattern" edict exists — convergent practice only.
- Personal-repo caveat: issue types are **org-scoped** and unavailable on user-owned repos
  (no ETA for change), so a lightweight conventional prefix or `type:` label remains the
  substitute there.

## 2. Issue Forms (YAML) — recommendations

- Field types: `markdown` (display-only guidance), `input`, `textarea`, `dropdown`,
  `checkboxes`. Prefer `markdown` blocks over placeholder text users must delete.
- `validations.required: true` on anything you'd bounce the issue for.
- `render: shell` (or a language) on any textarea receiving logs/code — auto-fences the
  submission; the best defense against unformatted dumps.
- `id:` lowercase kebab/snake, unique; form output renders as `### <label>` sections that
  regex labelers and agents parse — ids and labels are load-bearing downstream.
- Top-level `labels:` is high-value (issues arrive pre-categorized) but labels **must
  already exist in the repo or are silently skipped**.

### Limitations table

| Limitation | Workaround |
| :--- | :--- |
| No conditional fields (show/hide per dropdown) | Separate templates per scenario; `markdown` guidance blocks |
| Cannot set labels per dropdown answer | `issues:opened` Action parsing form output (Advanced Issue Labeler) |
| `labels:` must pre-exist | Bootstrap labels first (idempotent `gh label create --force`) |
| `projects:` ignored for filers without write access | Use the Project auto-add workflow instead (docs' own recommendation) |
| `assignees:` static only | Assign via Action at `issues:opened` |
| Field size limits (broke rust's automated ICE reports) | Parallel plain-markdown template for machine intake |
| Forms are a web-UI feature — **`gh`/API-created issues bypass `validations.required` entirely** (inference, strongly implied) | Quality gate lives in the filing skill/agent prompt, not the form |

- `config.yml`: `blank_issues_enabled: false` + `contact_links` deep-linking to
  Discussions categories (Tailwind routes questions AND feature requests out — issues are
  created only post-triage).

## 3. Template set & routing

- No empirical study links template count to abandonment (flagged). Observed range:
  Tailwind = 1 form + routing; Vite ≈ 2; rust ≈ 12 (earned by contributor volume).
- Recommendation for solo/agent repos: **3–4 forms** (bug / feature-task / chore-debt,
  questions routed to Discussions); grow a template only when a category demonstrably
  accumulates malformed issues.

## 4. Body structure per issue kind

- **Bug:** expected vs actual; **required reproduction** (link or steps) with a stated
  auto-close policy (Vite: 3 days); environment captured by command (`npx envinfo`,
  `rustc --version --verbose`) into a `render` field, never free recall; pre-flight
  duplicate-search checkboxes.
- **Task/feature:** audience + action + outcome; motivation; **acceptance criteria as
  observable pass/fail checkboxes** with concrete thresholds ("page loads < 0.5s"), ending
  in a check an agent can run.
- **Tech-debt:** current state, cost/risk of leaving it, proposed direction, done-criteria.
  No canonical major-OSS debt template exists (gap — most repos fold it into chore).

## 5. Duplicate prevention

- Enforced search-before-filing via required checkbox, not trust.
- Native: GitHub duplicate detection at creation (public preview 2026-06) suggests up to 3
  similar issues while typing — **web UI only**; agents filing via API don't benefit.
- For agent filing the gate is prompt-level: `gh search issues` before `gh issue create`
  (Anthropic's own triage command: "Only mark as duplicate of OPEN issues").

## 6. Creation-time metadata

- `gh issue create --title --body --label a,b --assignee @me --milestone M --project P
  --type Bug` — atomic metadata at creation; `--project` needs the `project` OAuth scope.
- REST `POST /issues` accepts labels/assignees/milestone/type but **silently drops them
  without push access**. Projects v2 need GraphQL / newer Projects REST / GitHub MCP
  (issue-fields support landed 2026-06).
- Sub-issues: create child, then attach via the sub-issues endpoint (no single-call
  create-as-child). Personal-repo sub-issue availability unverified — test.
- Personal repos: no issue types, no org issue fields. A **free GitHub org** is the
  unlock if types/fields are wanted across projects; otherwise `type:` labels.

## 7. Agent-authored issues — patterns and norms

- Best public example: Anthropic's own triage agent contract (`triage-issue.md` +
  `claude-issue-triage.yml` in anthropics/claude-code): exactly one category label +
  lifecycle labels, "issue body text takes precedence over form selections", and a hard
  action budget — "Don't post any comments... Your only actions are adding or removing
  labels." Lesson: give issue-writing agents an explicit action budget and taxonomy, not
  open-ended judgment.
- Agents filing issues should: reproduce the repo's form section headings (`### ...`),
  cite file:line evidence, include a runnable check, search duplicates first, batch
  low-confidence findings into one reviewed issue instead of one-per-TODO.
- Community norms hardening against AI slop: curl killed its bug bounty (~20% slop
  reports); Ghostty's `AI_POLICY.md` requires disclosure + bans unverified AI output and
  drive-by PRs not tied to an accepted issue. The transferable rule for own repos:
  **verification before submission** (repro runs, evidence cited), volume is the enemy,
  not AI per se.

## 8. Creation-time automation

- **Advanced Issue Labeler** (Action): maps issue-form dropdown/checkbox answers to labels
  on `issues:opened` — the standard workaround for forms' inability to label per answer.
- AI triage on `issues:opened`: claude-code-action ships an auto-triage solution
  (label, flag needs-repro, duplicate-check).
- Projects auto-add workflow (filter e.g. `is:issue label:bug`) replaces the template
  `projects:` key.

## 9. Implications for the kit's `github` backend (Option A design inputs)

1. The current form's `title: "[OI] "` prefix is the machine-intake niche case — but the
   `open-item` label already carries that signal; the prefix can be dropped or kept only
   if something greps titles. Decide in design.
2. The priority-in-body problem has a cheaper fix than moving the dropdown out of the
   form: **keep the `priority` dropdown, add an `issues:opened` labeler action** mapping
   dropdown → `priority:` label. Same for `type`. Zero form-UX change; labels stay the
   queryable surface.
3. Because the skill files via `gh`/API, **form `required:` validations never fire for
   skill-filed issues** — the `sync` mode's own refusal rules are the real gate and must
   stay (they already validate type/terminal-status).
4. Label bootstrap must precede form deployment (silent-skip hazard) — the migration
   script's idempotent `gh label create --force` pattern extends to the new
   `priority:`/`size:`/state labels.
5. Add `render:`-style structure and acceptance-criteria/code-pointers fields to form v2
   per research 0001 §3.3.
6. A `config.yml` with `blank_issues_enabled: false` keeps ad-hoc intake on-contract in
   each adopting repo.
7. Consider a free GitHub org for the project portfolio if native issue types/fields are
   wanted; otherwise the existing `type:` label fallback stands.
8. The delegation/triage skills should adopt Anthropic's action-budget contract style.

## 10. Unverified (flagged by the research pass)

Template-count vs abandonment (no study); exact REST wording on silent label drops;
sub-issues on personal repos; API bypass of form validation (implied, not documented);
several 403-blocked primaries (github.blog changelogs, tenthirtyam.org) sourced via
search excerpts.
