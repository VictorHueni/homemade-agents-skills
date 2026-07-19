---
name: util-docs-audit
description: "Scan repository documentation for stale, outdated, and dead docs. Use this skill whenever the user asks to audit documentation, check docs freshness, find outdated docs, detect dead documentation, review doc health, or mentions stale docs, doc rot, documentation drift, or docs cleanup. Also trigger when the user says things like are my docs up to date, which docs need updating, or scan docs for problems."
status: active
last_reviewed: 2026-05-29
version: "1.0.0"
user-invocable: true
impact: "low"
---

# Documentation Auditor

Scan a repository's documentation to detect stale, outdated, and dead docs. Produce a prioritized report with actionable recommendations.

## Overview

Documentation rot is one of the most common problems in codebases. This skill performs a multi-signal analysis to find docs that have drifted from the code they describe, references that point to things that no longer exist, and content that hasn't been touched in so long it's likely inaccurate.

## Scope and Boundaries

This skill is intentionally **generic**. It looks at file-level signals — stale dates, outdated references, dead docs, broken links, drift between prose and code — across any documentation directory in any kind of repository. It does not know about the strategic-architecture metamodel, the open-items governance contract, the central living ledger, or any cross-artefact dependency rule.

That separation is deliberate. Stack-aware governance lives in dedicated tools:

- **This skill (`util-docs-audit`)** — generic doc rot only: stale, outdated, dead docs. **Not a stack-governance tracker.** It does not enforce the open-items schema, does not verify ledger provenance, does not flag closure drift, and does not check metamodel build-order placement.
- **`util-metamodel-audit`** — report-only stack-aware compliance audit: central-ledger schema compliance, source-anchor / source-heading provenance, closure drift, dependency enforcement, ID integrity. Authoritative for any check that depends on the `metamodel` skill's `references/open-items-governance.md` or the `metamodel` skill.
- **`util-open-items`** — operational CRUD for the central living ledger at `docs/project-control/open-items/`: sync, triage, close, drop, archive, report. The only sanctioned writer of the ledger.

If a user asks "are my open items in sync with the ledger?" or "is my docs structure metamodel-compliant?" — route to `util-metamodel-audit`. If they ask "fix this open item" or "roll up open items" — route to `util-open-items`. This skill stays out of those workflows so the two governance tools remain the single source of truth for stack-aware checks.

## How It Works

The audit runs in three phases. Each phase feeds into the final report.

### Phase 1 — Discovery

Identify all documentation files in the repository. Documentation lives in many places:

- Dedicated docs directories (`docs/`, `documentation/`, `wiki/`, `.github/`)
- Markdown files at the repo root (`README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, etc.)
- Inline doc directories within packages/modules
- Files with extensions: `.md`, `.mdx`, `.rst`, `.txt`, `.adoc`, `.asciidoc`
- Auto-generated doc directories (identify but flag separately)

Run the discovery script to get a structured inventory:

```bash
python3 ~/.claude/skills/util-docs-audit/scripts/discover_docs.py <repo_root>
```

This outputs a JSON list of all doc files with metadata (path, size, last modified date, last commit date, last commit author).

### Phase 2 — Staleness Analysis

For each discovered doc file, evaluate staleness using multiple signals. A doc is not stale just because it's old — stability is fine. Staleness means the doc *should* have been updated but wasn't.

#### Signal 1: Code-to-Doc Drift (highest weight)

Compare the doc's last meaningful update against changes in the code it references. Steps:

1. Extract referenced paths from the doc: file paths, import statements, class/function names, API endpoints, CLI commands, config keys.
2. Use `git log` to check if those referenced code artifacts have changed since the doc was last updated.
3. If referenced code changed significantly after the doc's last update → **high staleness signal**.

```bash
# Get last commit date for a doc file
git log -1 --format="%ai" -- <doc_path>

# Get commits to referenced code files since that date
git log --since="<doc_last_date>" --oneline -- <code_path>
```

#### Signal 2: Broken References

Scan for references that point to things that no longer exist:

- **Dead links**: Internal links (`[text](./path)`, `[text](#anchor)`) pointing to missing files or anchors.
- **Dead code references**: Mentions of functions, classes, modules, CLI flags, env vars, or config keys that no longer exist in the codebase.
- **Dead URLs**: External URLs that return 404 or are unreachable (check a sample, not all — be respectful of rate limits).
- **Stale version references**: Pinned version numbers for dependencies that have moved on significantly.

```bash
python3 ~/.claude/skills/util-docs-audit/scripts/check_references.py <repo_root> <doc_path>
```

#### Signal 3: Temporal Staleness

Time-based signals, weighted lower than drift signals but still useful:

- **Last updated date**: How long since the doc was last committed. More than 12 months without an update in an active repo is a yellow flag. More than 24 months is a red flag.
- **Velocity mismatch**: Compare the doc's update frequency against the update frequency of the code directory it sits in. If the code directory gets 50 commits/quarter but the doc gets 0, that's suspicious.
- **Orphan detection**: The doc's parent directory or related module was deleted or renamed, but the doc remains.

#### Signal 4: Content Quality Signals

Quick heuristic checks:

- **TODO/FIXME/HACK markers** left in documentation.
- **"Coming soon" / "TBD" / "WIP"** placeholders that were never filled.
- **Deprecated API usage**: References to APIs or patterns the project has officially deprecated.
- **Screenshot/image references** pointing to missing files.

### Phase 3 — Report Generation

Produce a structured report. The report has three sections:

#### Section 1: Summary Dashboard

```
📊 Documentation Health Report
Repository: <name>
Scan Date: <date>
Total doc files: <N>
  🔴 Critical (likely outdated): <N>
  🟡 Warning (possibly stale):  <N>
  🟢 Healthy:                   <N>
  ⚪ Skipped (auto-generated):  <N>
```

#### Section 2: Critical & Warning Items (sorted by severity)

For each flagged doc, include:

```
### 🔴 path/to/doc.md
**Staleness Score**: 8.5/10
**Last Updated**: 2024-01-15 (14 months ago)
**Signals**:
  - Code drift: 23 commits to referenced files since last doc update
  - Broken refs: 3 internal links point to moved/deleted files
  - Contains 2 TODO placeholders
**Referenced code changes**:
  - src/auth/oauth.ts: 12 commits (refactored OAuth flow)
  - src/config/settings.py: 5 commits (added new config keys)
**Suggested action**: Review and update sections on OAuth configuration
```

#### Section 3: Recommendations

Prioritized list of actions:

1. **Immediate fixes** — broken links, dead references (easy wins)
2. **Content updates needed** — docs with significant code drift
3. **Candidates for removal** — orphaned docs with no clear purpose
4. **Structural improvements** — missing docs for undocumented modules

## Output Format

Save the report to `docs-audit-report.md` in the repo root (or wherever the user specifies). If the user asks for JSON output, also produce `docs-audit-report.json` with structured data.

## Configuration

The user can customize the audit by providing context:

- **Scope**: Scan the whole repo or specific directories
- **Thresholds**: Custom staleness thresholds (default: 12 months warning, 24 months critical)
- **Exclusions**: Patterns to skip (e.g., `node_modules/`, `vendor/`, auto-generated API docs)
- **Focus areas**: "Focus on the API docs" or "check the onboarding guides"

## Usage Examples

**Example 1 — Full repo scan:**
```
User: "Audit all the docs in this repo"
→ Run discovery on repo root, analyze all found docs, produce full report.
```

**Example 2 — Targeted scan:**
```
User: "Check if our API documentation is still accurate"
→ Focus discovery on docs/api/ or similar, cross-reference with src/api/ code changes.
```

**Example 3 — Quick health check:**
```
User: "Which docs haven't been updated in over a year?"
→ Run just the temporal staleness check, skip deep analysis, produce lightweight report.
```

**Example 4 — Dead docs hunt:**
```
User: "Find any dead or orphaned documentation"
→ Focus on broken references, orphan detection, and missing-file checks.
```

## Important Notes

- Always run `git log` commands from the repo root.
- Be mindful of large repos — if there are hundreds of doc files, sample or batch the analysis. Give the user progress updates.
- Auto-generated docs (from tools like Javadoc, Sphinx, TypeDoc) should be flagged separately. Their staleness is a build pipeline issue, not a content issue.
- CHANGELOG files and release notes are inherently time-bound — don't flag them as stale just because they reference old versions.
- When checking external URLs, limit to a small sample (max 10-20) to avoid hammering external servers.
- The staleness score is a heuristic, not a ground truth. Always present findings as "likely stale" or "possibly outdated", not definitive judgments.
