# Karpathy Behavioral Posture Principles

Derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls. These four principles went viral (91 000 GitHub stars via the [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) packaging) because they address **how an agent should reason before acting**, not what output it should produce. That distinction is why they survive the "rule breakdown" failure mode: a style rule breaks when the situation doesn't match; a posture rule applies to every situation.

**Include this block verbatim at the top of every CLAUDE.md / AGENTS.md.** It applies to every task regardless of stack, language, or project type.

---

## Verbatim block (copy into CLAUDE.md / AGENTS.md)

```markdown
## Behavioral guidelines

**Think before coding.** State assumptions explicitly. If multiple interpretations exist, present them — don't pick silently. If something is unclear, stop and ask.

**Simplicity first.** Minimum code that solves the problem. No speculative features, no abstractions for single-use code, no unrequested flexibility or error handling for impossible scenarios. If you write 200 lines and it could be 50, rewrite it. Ask: "would a senior engineer call this overcomplicated?" If yes, simplify.

**Surgical changes.** Touch only what you must. Don't improve adjacent code, comments, or formatting. Don't refactor things that aren't broken. Match existing style. If you notice unrelated dead code, mention it — don't delete it. Every changed line should trace directly to the user's request.

**Goal-driven execution.** Transform tasks into verifiable success criteria and loop until verified. "Add validation" → "Write tests for invalid inputs, then make them pass." "Fix the bug" → "Write a test that reproduces it, then make it pass." For multi-step work, state a brief plan with a verification step per increment before starting.
```

---

## Why these four and not others

These principles are durable because they encode **meta-level reasoning discipline**, not object-level style preferences:

| Principle | Problem it solves | Why it survives edge cases |
|---|---|---|
| Think before coding | Silent assumptions that lead to wrong implementations | Always applies — there are always assumptions to surface |
| Simplicity first | Over-engineering: abstractions, configs, error-handling nobody asked for | The test ("would a senior engineer say this is overcomplicated?") self-adjusts to context |
| Surgical changes | Scope creep: agents "improve" adjacent code and introduce regressions | The trace rule ("every changed line → user's request") is binary and verifiable |
| Goal-driven execution | Weak task framing ("make it work") → infinite clarification loop | Declarative goals with verification criteria let the agent loop independently |

## What these principles do NOT replace

- Project-specific commands (build, test, lint) — must still be documented explicitly
- Permission boundaries — still need a clear table of what requires human approval
- Domain terminology — non-obvious project nouns still need one-sentence definitions
- Stack identity — framework + version still must be declared

The behavioral posture block handles *how* the agent reasons; the rest of the config handles *what* it knows about the project.
