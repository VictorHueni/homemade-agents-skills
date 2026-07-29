---
type: rule
---

# CI/local tool parity — no CI-only tooling

When adding a CI step that introduces a new tool (linter, diff gate, load tester, scanner), always ship the local counterpart in the same change:

1. **Dev-env declaration in the dotfiles** (`VictorHueni/dotfiles`, chezmoi-managed — check the chezmoi source with `chezmoi source-path`, tools live in `dot_mise.toml` `[tools]`): check first whether the tool is already declared; if not, add it with a short rationale comment (existing entries follow this pattern) and the correct mise registry short name or aqua backend id. Commit dotfiles-side, separately from the project change.
2. **Makefile mirror in the project**: a target reproducing the CI invocation, wired into the project's local CI gate (e.g. a `*-ci-local` aggregate) when it's self-contained, or standalone when it needs external state (a base git ref, a live environment URL). Never force an external-state target into the aggregate gate — that makes the local gate network-dependent and flaky.

**Why:** a gate that only runs in CI has a feedback loop of one push+wait cycle; the local mirror makes it seconds. And a tool installed ad-hoc (`npx`, `curl | sh`, manual download) instead of declared in the dotfiles silently vanishes on the next runtime bump ([[toolchain-version-managed-globals]]) and never reaches other machines.

**Exemptions:** tools already managed by the project's own dependency system (venv/lockfile-pinned Python or npm packages) need no dotfiles entry — the lockfile is their declaration; they still deserve the Makefile mirror if CI invokes them as a gate.

**How to apply:** before writing the CI job, check the dotfiles declaration (`grep <tool> "$(chezmoi source-path)/dot_mise.toml"`); implementation-plan increments that add CI steps must carry both halves explicitly in scope — the workflow edit, the dotfiles declaration, and the Makefile mirror are one increment, not follow-ups.
