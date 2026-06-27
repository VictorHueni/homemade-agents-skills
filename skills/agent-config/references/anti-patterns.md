# Anti-Patterns — CLAUDE.md / AGENTS.md

Each anti-pattern includes its failure mode and the fix. All findings rated `high` severity in the review checklist unless noted.

---

## High severity (actively harmful)

### Credentials embedded anywhere

**Failure mode:** security incident; secret rotation requires rewriting committed history.

**Fix:** document only where secrets live and how to retrieve them programmatically. Never document values, even "placeholder" ones that might be swapped for real values later.

```markdown
# Wrong
SUPABASE_KEY=eyJhbGciOiJIUzI1NiJ9...

# Right
Secrets live in `.env.local` (local dev) and GitHub Actions secrets (CI).
See `.env.example` for required variable names.
```

---

### Code style rules a linter already enforces

**Failure mode:** agents follow the documented rule inconsistently; the linter catches violations anyway; the rule wastes token budget and degrades compliance with everything else.

**Fix:** delete the style rule from the config. Wire the linter to run automatically via a pre-commit hook or CI step. *"Never send an LLM to do a linter's job."*

---

### Inline file-system path listings

**Failure mode:** paths listed in the config go stale silently as the project evolves. Agents treat stale content as current fact. The result is navigation errors that are hard to diagnose.

```markdown
# Wrong (will go stale)
docs/
├── architecture/decisions/
├── product-specs/prds/
└── domain/

# Right (living, never stale)
Read docs/INDEX.md for the full documentation navigation hub.
```

**Fix:** wire the agent to `docs/INDEX.md` (a living file) instead of embedding the path tree inline. See [docs-index-pattern.md](docs-index-pattern.md).

---

### Task-specific instructions in the root config

**Failure mode:** instructions for the weekly reporting workflow, the database migration runbook, and the code review checklist all load every session — even when the agent is writing a unit test. Wastes token budget.

**Fix:** move task-specific content to `agent_docs/<task>.md` reference files. Link from the root config only if the task is genuinely cross-cutting.

---

### Auto-generated content left as-is

**Failure mode:** `/init`-generated configs prioritise comprehensiveness over restraint. They include boilerplate descriptions of obvious things ("Claude is an AI assistant that helps with coding") and framework-level patterns Claude already knows. Result: +20% session cost, -3% task success.

**Fix:** treat auto-generated output as a starting scaffold only. Trim aggressively — every line that doesn't carry project-specific knowledge not in Claude's training data should be deleted.

---

### Stale commands and paths

**Failure mode:** agents execute stale commands, fail, then spend multiple turns diagnosing the failure. Worse: they may succeed in unexpected ways if a command was renamed but the old name was reused for something else.

**Fix:** run a quarterly audit (`ls` on every path mentioned, execute each command in a scratch environment). Commands that appear in CI are the canonical source of truth — keep the config in sync with CI.

---

## Medium severity (sub-optimal)

### Rule lists without behavioral posture

**Failure mode:** a flat list of style preferences ("always use async/await", "prefer named exports") creates false predictability with a cliff edge — the rules break the moment the situation doesn't match, and the agent guesses.

**Fix:** add the Karpathy behavioral posture block (see [karpathy-principles.md](karpathy-principles.md)) at the top of the file. Meta-instructions about *how to reason* apply to every situation; style rules do not.

---

### Missing permission boundary

**Failure mode:** agents must guess what they're allowed to do autonomously. Some will over-ask (friction); others will silently execute destructive actions (risk).

**Fix:** include a short table — two columns: "may do without asking" vs. "requires human approval." Minimum entries: git push, package installs, file deletion, infrastructure commands.

---

### No docs navigation pointer

**Failure mode:** when `docs/` has substantial content (ADRs, PRDs, domain model, etc.) but the config doesn't point to it, the agent operates without architectural context. It may re-derive decisions that were already made, or propose implementations that contradict ADRs.

**Fix:** add a pointer to `docs/INDEX.md` or `docs/VISION.md`. See [docs-index-pattern.md](docs-index-pattern.md).

---

### Verbose stack description

**Failure mode:** three paragraphs explaining what Next.js is and how React rendering works. Claude already knows this. Every sentence explaining something Claude knows wastes a slot from the ~150-instruction budget.

**Fix:** one line per dependency. The stack identity table should be scannable in under 10 seconds.

---

## Low severity (polish)

### Missing `last_reviewed` frontmatter

Configs without a review date drift silently. Add YAML frontmatter with `last_reviewed: YYYY-MM-DD` and `review_interval: 90d`.

### No closing verification criteria

The "these guidelines are working if…" statement helps the agent self-correct over time. Add: "Fewer unnecessary changes in diffs. Clarifying questions before implementation, not after mistakes."

### No domain terminology section

Domain nouns that are non-obvious to a newcomer (not general programming knowledge — project-specific meanings) should have one-sentence definitions or a pointer to the glossary. Without them, the agent uses generic terminology and misses the codebase's naming conventions.
