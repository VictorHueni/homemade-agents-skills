# Best Practices — CLAUDE.md / AGENTS.md

Synthesised from 14+ sources including [agents.md](https://agents.md), [Karpathy guidelines](https://github.com/multica-ai/andrej-karpathy-skills), [Anthropic skills best-practice docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [OpenAI Codex guidance](https://developers.openai.com/codex/learn/best-practices), and [HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md).

---

## The mental model

A CLAUDE.md / AGENTS.md is a **machine-readable project onboarding script**, not a human README. Every token loads into every session and competes with conversation history, the system prompt, and the actual work. Write for density, not completeness.

---

## The three questions every file must answer

| Question | Content |
|---|---|
| **WHAT** | Tech stack, framework versions, project structure (2–4 lines). For monorepos: how the repo is subdivided. |
| **WHY** | The purpose of the project and its major components. One sentence per component. Pointer to the product vision and/or docs navigation hub. |
| **HOW** | Exact, runnable build / test / lint commands with flags. What "done" means and how to verify it. Permission boundary: autonomous vs. approval-required actions. |

---

## What to include

**Essential — every project:**
- Behavioral posture block (see [karpathy-principles.md](karpathy-principles.md)) at the top — applies to every task
- One-sentence project description (anchors all downstream decisions)
- Stack identity: framework + runtime + major dependency versions
- Non-standard package manager or toolchain (only if it differs from the obvious default)
- Exact build / test / lint commands — runnable, with flags, no hand-waving; use CI commands as the canonical source
- Permission boundary: a table or short list of autonomous vs. approval-required actions
- Docs navigation pointer: link to `docs/INDEX.md` or `docs/VISION.md` (see [docs-index-pattern.md](docs-index-pattern.md))

**Conditional — add when relevant:**
- Monorepo layout: which subdirectory governs which package
- Security posture: where secrets live (e.g. `AWS Secrets Manager`, GitHub Actions secrets) — never their values
- Domain terminology: terms that would surprise a competent engineer unfamiliar with the codebase — one sentence per term, or a pointer to the glossary
- Non-obvious gotchas: things the agent will get wrong without explicit guidance
- Links to deeper reference files for specialised workflows (`agent_docs/migrations.md`, etc.)

**Tool mention = tool usage:** tools explicitly named in the config are used 160× more frequently than unmentioned tools. Name the test runner, linter, and script runner explicitly.

---

## Length targets

| Context | Target |
|---|---|
| Root config (production teams) | < 60 lines |
| Root config (general) | < 200–300 lines |
| Subdirectory / package-scoped file | < 100 lines |

**Why the hard limit matters:** frontier LLMs reliably follow approximately 150–200 instructions per session. Claude Code's built-in system prompt consumes ~50 slots before the project config is even read. As instruction count increases, compliance degrades **uniformly across all instructions** — not just the newest ones. A 400-line config does not give 400 compliant rules; it gives ~150 rules chosen unpredictably.

---

## Progressive disclosure

Keep the root file as an index. Move specialist context to referenced files that load on demand — zero token cost until accessed.

```
CLAUDE.md                       ← 60–150 lines: index; WHAT/WHY/HOW/permissions
agent_docs/
  building.md                   ← full deploy + build runbook
  testing.md                    ← test framework details, coverage targets
  migrations.md                 ← DB migration steps
  code-conventions.md           ← patterns the agent must match
```

In CLAUDE.md:
```markdown
## Reference docs
- Build and deploy: [agent_docs/building.md](agent_docs/building.md)
- Testing: [agent_docs/testing.md](agent_docs/testing.md)
```

**Depth limit:** keep references one level deep from the root. Agents preview nested files with `head -100` and miss content past the cutoff.

---

## File hierarchy (three scopes)

| Scope | Location | Content |
|---|---|---|
| User-global | `~/.claude/CLAUDE.md` | Cross-project behavioral preferences + working style |
| User rules | `~/.claude/rules/*.md` | Topic-scoped global rules; optional `paths:` frontmatter for language-specific rules |
| Project root | `<repo>/CLAUDE.md` or `AGENTS.md` | Team-shared standards: stack, commands, permissions, docs pointer. In source control. |
| Subdirectory | `<repo>/packages/api/CLAUDE.md` | Package-scoped overrides in monorepos. Nearest file wins; merges up with root. |

**Cross-agent portability:** maintain a single master `AGENTS.md`; have tool-specific files contain only `@AGENTS.md` to delegate. One source of truth, zero duplication.

---

## Maintenance

**Write reactively.** When the agent makes the same mistake twice: ask for a retrospective → add the minimal rule that prevents it → verify. Never add rules speculatively.

**Quarterly audit:**
- Every command still runs
- Every path still resolves
- Rules now enforced by linter/CI → remove them
- Test: run three common tasks cold; observe failures

**Never auto-generate.** `/init` output optimises for comprehensiveness over restraint: +20% cost, -3% task success (philschmid research). Write by hand.
