---
type: skill
name: util-docs-log
description: "Generate or refresh an OKF log.md for a folder — a per-directory change history materialised from git. A deterministic script renders git history for the folder's direct-child docs in the OKF-prescribed format (date-grouped, newest first, Creation/Update/Deprecation bullets with file links). One bullet per commit; non-recursive; idempotent (byte-stable given committed history). On-demand / at bundle-export — not a commit hook. Asks which folder if none is given. Triggers on: docs log, log.md, change history, folder history, directory update log, generate log, refresh log, OKF log, changelog for docs, materialize git history."
version: "1.0.0"
status: active
last_reviewed: 2026-07-01
review_interval: 180d
user-invocable: true
impact: "low"
metadata:
  category: "utility"
  complexity: "low"
---

# util-docs-log — OKF folder change-log generator

Generate or refresh an **OKF `log.md`** for a folder: a per-directory chronological change
history, **materialised from `git log`**. A deterministic script does all the work — nothing is
hand-appended — so the log is a faithful, reproducible view of git history for consumers that
don't have the repo (tarball/zip OKF bundles).

## Canonical definition

`log.md` is an [OKF v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
**reserved file** — a per-directory update history. It carries **no frontmatter**. OKF prescribes
its shape: a flat list of **date-grouped entries, newest first**; ISO 8601 `## YYYY-MM-DD`
headings; prose bullets with a leading bold action word (`**Creation**`/`**Update**`/`**Deprecation**`).
See the `metamodel` skill's `references/artefact-frontmatter.md` §Reserved files.

## Why git-derived (and why on-demand, not a hook)

- **Source of truth is git.** The log is a *view* of `git log`; commit messages are the content.
  → **Write good commit messages** — they become the log entries verbatim.
- **On-demand / at bundle-export — not a commit hook.** A git-derived log committed on every
  commit either lags by one commit or needs `--amend` (which `rules/git-and-tools.md` forbids).
  For a live git repo, `git log` *is* the log; `log.md` earns its keep only when a bundle ships
  outside git. So run this skill when you want a fresh log or before shipping a bundle.

## Boundary

- **`util-docs-index`** renders the *current-state* listing (`index.md`); **`util-docs-log`**
  renders the *history* (`log.md`). Two OKF reserved files, two skills, same per-folder scope.

## The deterministic script

`scripts/gen_log.py <folder> [--check] [--max N]` (stdlib only):
- covers the folder's **direct-child** `*.md` docs (non-recursive; excludes reserved
  `index.md`/`log.md`/`README.md`); subtree history lives in each subfolder's own `log.md`;
- **one bullet per commit** (the subject as-is) under its `## YYYY-MM-DD` heading, newest first,
  listing the folder's files it touched as inline links;
- **action label from git status**: all-added → `**Creation**`, all-deleted → `**Deprecation**`,
  else → `**Update**`;
- a commit spanning several folders appears in each affected folder's log, scoped to its files;
- **idempotent + byte-stable** (no "now" timestamps): re-running with no new commits writes nothing;
- `--check` exits 1 (writes nothing) when `log.md` is behind git history — for hooks / audit;
- `--max N` caps to the N most recent commits;
- **not a git repo** → skips with a clear message.

## Process

1. **Resolve the folder.** If the prompt names one, use it. **If not, ask which folder** (offer
   detected `docs/` subfolders). Do not guess.
2. **Run** `python3 scripts/gen_log.py <folder>` → writes/updates `log.md`.
3. **Report** how many commits/documents, and note if the folder isn't under git.

(No LLM authoring step — the content is git history. The only way to improve a log entry is a
better commit message.)

## Output format (OKF-prescribed)

```markdown
# Directory Update Log

## 2026-07-01
* **Update**: OKF layer 2 — serialise OKF frontmatter into producer skills ([01a-personas.md](01a-personas.md), [03a-capability-map.md](03a-capability-map.md)) — `224f61b`

## 2026-06-28
* **Creation**: Add bulk invoice export PRD ([prd-0003.md](prd-0003.md)) — `abc1234`
```

## Limitation

The log reflects the history of documents **currently present** in the folder (it scopes `git
log` to the current files). A document fully deleted from the folder stops appearing; capturing
removed-document history would require scanning all paths ever present and is out of scope for v1.

## Checklist

- [ ] Target folder resolved (asked the user if the prompt didn't name one).
- [ ] `gen_log.py` run; `log.md` written/updated (or clean "not a git repo" skip).
- [ ] `log.md` has no frontmatter (OKF reserved file).
- [ ] Entries are date-grouped, newest first, one bullet per commit.
- [ ] Re-run is `unchanged` (byte-stable) with no new commits.
