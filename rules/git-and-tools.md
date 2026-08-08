---
type: rule
---

# Git & tool-use discipline

## Never `git commit --amend`

Always create a new commit. Amending rewrites a hash you may have already recorded elsewhere (progress logs, PR descriptions, follow-up commits) and creates self-inconsistent history.

If a pre-commit hook fails, the commit did NOT happen — the previous commit is unchanged. Fix the issue, re-stage, and create a NEW commit. Do not `--amend` to "fold the fix in."

Exception: only if the user explicitly asks for `--amend` in the same conversation.

## Commit & PR scope vocabulary — capability, not work-item number

The scope in a Conventional Commit (`type(scope): …`) and in a squash-merged **PR title** should name **what the change advances in product terms**, drawn from the project's own vocabulary — never an internal work-item / plan number.

**Resolution order (first match wins):**

1. **Declared scope** — if the plan or task being executed declares a `Commit scope:` (e.g. in an implementation plan's Delivery Rules), use it verbatim.
2. **Capability / product vocabulary** — else, if the project has a capability map or FBS, use a **product slug** (`P-NN` → e.g. `billing`) or **capability slug** (`C-N.M` → e.g. `search`). These read as plain language in the changelog and let a stakeholder release note (`com-release-note`) attribute the change to a capability near-mechanically.
3. **Area / module** — else infer from the changed files (`auth`, `api`, `infra`, `deps`) — the sensible default for repos with no capability map.

**Never put a bare work-item / plan number in the scope** (`feat(0121): …`). It is opaque to a non-technical reader, un-attributable to a capability without a lookup, and pollutes the automated changelog. Keep the plan / increment reference in a **`Refs:` trailer** instead:

```text
feat(billing): word-level diff on plan terms

Refs: Plan-0042 increment 03
```

**Why it matters (the whole chain):** a squash-merge uses the PR title as the commit subject, so the PR-title scope is what the automated changelog groups by — and what the curated release note is built from. A capability scope makes both legible; a work-item number makes both opaque. This is why `agent-ralph-loop`, `dev-git-commit`, `dev-pr`, and `plan-implementation` all resolve the scope the same way. Mechanical enforcement (a generated scope-enum + PR-title gate) is tracked separately; **this rule is the authoring convention every skill follows.**

## A branch cut from a remote ref silently tracks it — and the danger is `pull`, not `push`

`branch.autoSetupMerge` defaults to `true`, which sets the upstream whenever a branch is created from a remote-tracking ref **regardless of a name mismatch**. So `git branch feat/x origin/staging` (or `git switch -c`) leaves `feat/x` tracking `staging`.

**The structural fix is `branch.autoSetupMerge = simple`** (Git ≥ 2.37): track only when the new branch's name matches the remote branch's name, so the intended cases still work. Set it globally in the dotfiles; a repo-local copy is a reasonable belt-and-braces pin, and it covers every worktree of that repo at once because they share one `.git/config` (absent `extensions.worktreeConfig`). Prefer this over remembering to run `git branch --unset-upstream` on every new branch — a fix that depends on recall isn't one.

**Do not claim a wrong upstream means a bare `git push` hits the upstream branch.** `push.default` defaults to `simple`, which **refuses** to push when the upstream's name differs from the local branch's: `fatal: The upstream branch of your current branch does not match the name of your current branch`, exit 128, nothing sent. Verify with `git push --dry-run` before writing that warning into any document.

The real damage is quieter: a bare `git pull` merges the upstream (e.g. the trunk) into your feature branch; `git status` reports ahead/behind against the wrong ref; and `@{u}` silently resolves to it, so `git log @{u}..` and `git diff @{u}` answer a different question than you asked.

**Anti-pattern in self:** propagating "a bare push would target the trunk" through successive handoff documents because it sounds right, when one `--dry-run` falsifies it. A plausible mechanism stated confidently is still a hypothesis until executed — and server-side branch protection may not be the backstop you assume, since `enforce_admins: false` lets a repo admin bypass it.

## Squash-merge repos: `git branch --merged` always says "not merged"

Where every PR lands as a squash commit, an absorbed branch's commits are never ancestors of the trunk, so `git branch -r --merged origin/<trunk>` reports it unmerged forever and is useless for cleanup decisions.

Judge by **tree content** instead. `git diff origin/<trunk> <branch>` (two-arg, tree-vs-tree — not `..` or `...`) is empty when the branch is byte-identical. When it isn't, the question is whether the branch holds anything the trunk lacks: `git diff origin/<trunk> <branch> --numstat | awk '$1>0 {print $3}'` lists only files with branch-side additions. Trunk-ahead deletions just mean the branch is stale, which is not a reason to keep it.

## `Edit` tool: `replace_all=True` matches the whole `old_string`, not the inner substring

`replace_all=True` replaces every literal occurrence of the exact `old_string` you provided. If `old_string` is multi-line or contains surrounding context, occurrences of the inner substring with *different* surroundings will silently survive.

After any wide-pattern `replace_all`, follow up with:

```bash
git grep -n "<inner_string>" <dir>/
```

If grep still finds the string, those are the occurrences where the wider pattern did not match. Run targeted single-occurrence Edits for them. The grep takes 5 seconds; skipping it means the next test discovers the miss for you with a less helpful error.

**Heuristic for `old_string` width:**

- **Narrow `old_string`** (just the inner substring) + grep follow-up → safer default. Risk: over-replacement if the inner string is non-unique.
- **Wide `old_string`** (with surrounding context) → only when disambiguation is required. Risk: silent misses when surrounding context varies.

Anti-pattern: assuming a multi-line `replace_all` Edit "got everything" without verification.

## `LSP findReferences`: cross-check the file count, or a cold server will lie to you

`findReferences` is the right tool for renaming a **code symbol** — it beats grep by excluding docstring/comment mentions, never matching a same-named local variable, and searching outside whatever directory scope you would have hand-picked for grep.

**But it only searches files the language server has already loaded into its program.** A cold call returns a small, plausible, silently incomplete answer with no warning that it looked at one file. Measured case: the same symbol at the same position returned **3 references in 1 file** on the first call and **47 across 13 files** once the server had loaded the surrounding package.

**Always cross-check the file count before trusting it:**

```bash
git grep -lw "<identifier>" <dirs> | wc -l     # compare against the LSP file count
```

Agreement → warm and trustworthy. Disagreement → cold: warm the server by running `findReferences` from a module that *imports* the symbol, then re-run the original query.

**Two structural limits to plan around:**

- **There is no rename operation** — the tool offers `findReferences`, `goToDefinition`, `workspaceSymbol`, hover, and call hierarchy. Enumeration is semantic; the edits are still `Edit`/`replace_all`. Never write "use LSP to rename X" into a plan as an executable instruction.
- **No language server sees inside a string literal.** For anything whose name also appears as text — SQL table names in `text()` bodies and ORM metadata, template keys, config identifiers, DI tokens — LSP is blind by construction and grep is the only completeness proof.

**The risk asymmetry decides where to spend review effort:** a missed *symbol* fails loudly (ImportError/NameError at import or collection, or a type-check error) and CI catches it; a missed *string* fails silently at runtime on whatever path happens to execute it. Budget the scrutiny on the strings, and make sure the test lane that actually executes them runs.

**Prerequisite:** the language server is usually a machine-level tool, not a project dependency. Confirm `command -v <server>` before relying on any of this and fall back to grep-only if absent — see [[toolchain-version-managed-globals]] for why a declared-and-installed server can still be missing.

## `pgrep -f <pattern>` matches the watcher itself — never poll a long job with it

`pgrep -f` matches against the **full command line** of every process, which includes the shell running the poll loop and any sibling waiter whose own command line embeds the pattern. So the canonical "wait for the job" idiom is self-satisfying:

```bash
until ! pgrep -f "make be-ci-local" >/dev/null; do sleep 10; done   # never exits
```

The loop's own `/bin/bash -c '… pgrep -f "make be-ci-local" …'` is a match, so the job finishes and the wait continues **forever**, reporting "still running" indefinitely. Measured case: a gate that had completed successfully was reported as running for four hours, and a second and third waiter armed against the same string kept confirming it — three independent sources agreeing, all reading the same reflection.

**The tell is a process that "runs" far past any plausible duration while its log stops advancing.** Compare the log's mtime against now; a job that is genuinely working writes something.

**How to apply:** wait on the *artefact*, not the process — poll for a sentinel the job appends on completion (`echo "EXIT=$?" >>"$log"`, then `until grep -q '^EXIT=' "$log"`). When you must inspect the process table, use `ps -C <exe>` (matches the executable, not the command line) or `pgrep -x`, and cross-check with the log's mtime. Capture the exit code at launch — `nohup … ; echo $? >>log` — because an exit status you never recorded cannot be recovered afterwards, and "no error text in the log" is not a verdict (see the `${PIPESTATUS[0]}` and truncated-list traps in [[sonarcloud-silent-analysis-failure]]).

**Why:** the failure is silent and self-confirming. Every check agrees the job is running, the natural response is to wait longer, and the real state — finished, possibly failed — is never read. **Anti-pattern in self:** arming a second waiter with the same pattern to double-check the first, which cannot disconfirm anything because both match themselves.
