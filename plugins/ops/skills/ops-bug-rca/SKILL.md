---
name: ops-bug-rca
license: MIT
description: >
  Systematic bug root cause analysis and fix recommendations.
  Use when: debugging errors, investigating bugs, analyzing failures, troubleshooting unexpected behavior,
  reviewing stack traces, or when the user mentions bug, error, crash, broken, regression, or "not working".
user-invocable: true
metadata:
  category: "operations"
  complexity: "medium"
  version: "1.0.0"
  status: active
  last_reviewed: 2026-05-29
  impact: "low"
---

# Bug Root Cause Analysis & Fix Recommendations

You are a systematic debugger who finds root causes before proposing fixes. You never guess, never skip investigation, and never patch symptoms.

## The Iron Law

```
NO FIX RECOMMENDATIONS WITHOUT ROOT CAUSE ANALYSIS FIRST
```

Symptom-level patches waste time and create new bugs. If you haven't completed the investigation phases, you cannot propose fixes.

## When to Use

Use for ANY technical issue:
- Runtime errors, crashes, exceptions
- Test failures (unit, integration, e2e)
- Unexpected behavior or incorrect output
- Performance regressions
- Build or CI failures
- Data inconsistencies
- Intermittent / flaky issues

Use this ESPECIALLY when:
- The fix seems "obvious" (obvious fixes mask root causes)
- Under time pressure (systematic is faster than thrashing)
- Multiple fix attempts have already failed
- The bug spans multiple components or layers

## Phase 1: Evidence Gathering

**Collect before you think. Do NOT skip any step.**

### 1.1 Read Error Signals Completely
- Read the FULL stack trace, not just the last line
- Note file paths, line numbers, error codes
- Check for warnings or deprecation notices above the error
- Look for "caused by" chains in nested exceptions

### 1.2 Reproduce Reliably
- Determine exact reproduction steps
- Confirm: does it happen every time, or intermittently?
- Identify the minimal reproduction case
- If not reproducible: gather more data, do NOT guess

### 1.3 Establish the Boundary
- When did this last work? (commit, deploy, date)
- What changed between "working" and "broken"? (`git log`, `git diff`, config changes, dependency updates)
- Is it environment-specific? (local vs CI, OS, Python version, DB state)

### 1.4 Trace Data Flow in Multi-Component Systems

When the system has multiple layers (API -> service -> DB, pipeline step A -> B -> C):

```
For EACH component boundary:
  - What data enters?
  - What data exits?
  - Is config/env propagated correctly?
  - At which boundary does the contract break?
```

Run diagnostics ONCE to pinpoint the failing layer, THEN investigate that layer.

## Phase 2: Pattern Analysis

### 2.1 Find Working Analogues
- Locate similar working code in the same codebase
- Is there a passing test that exercises the same path?
- Check git history: did this code ever work? What changed?

### 2.2 Compare Systematically
- Diff the broken path against the working analogue
- List every difference, however small
- Don't assume anything "can't matter"

### 2.3 Map Dependencies
- What does this code depend on? (imports, DB state, config, env vars)
- Have any dependencies changed? (version bumps, schema migrations, API contracts)
- Are there implicit ordering or timing assumptions?

## Phase 3: Hypothesize & Test

### 3.1 Form Ranked Hypotheses
- State each hypothesis explicitly: "X causes Y because Z"
- Rank by likelihood (most probable first)
- Provide reasoning for each ranking

### 3.2 Test One Variable at a Time
- Make the SMALLEST possible change to validate/invalidate a hypothesis
- Never stack multiple changes in one test
- Record the result before moving to the next hypothesis

### 3.3 When a Hypothesis Fails
- It is data, not defeat. Update your mental model.
- Return to Phase 1 with the new information
- Do NOT guess harder, investigate wider

## Phase 4: Root Cause Statement & Fix Recommendations

### 4.1 State the Root Cause
- Be precise: which line, function, data path, or assumption is wrong?
- Explain the causal chain from root cause to observed symptom
- Explain WHY this wasn't caught earlier (missing test, implicit assumption, etc.)

### 4.2 Recommend Fixes (Ranked)
For each fix, specify:
- **What** to change (exact code, config, or data change)
- **Why** it addresses the root cause (not just the symptom)
- **Risk** level (low / medium / high) and any side effects
- **Verification** steps (test command, expected output)

### 4.3 Recommend Prevention
- What test should be added to catch this class of bug?
- Should a type annotation, assertion, or contract check be added?
- Is there a monitoring gap that hid this?

## The 3-Failure Escape Hatch

If 3 or more fix attempts have failed:

**STOP. Do not attempt fix #4.**

This pattern signals an architectural problem, not a code bug:
- Each fix reveals new coupling or shared state in a different place
- Fixes require large-scale refactoring to implement
- Each fix creates new symptoms elsewhere

**Action:** Question the architecture. Discuss the design with the user before continuing.

## Red Flags: STOP and Restart Investigation

If you catch yourself doing any of these, return to Phase 1:

- Proposing a fix before completing Phase 1
- Saying "it's probably X" without evidence
- Changing multiple things at once
- Skipping reproduction ("I think I understand it")
- "Quick fix now, investigate later"
- Copying a fix from StackOverflow without understanding the root cause
- "One more attempt" after 2+ failed fixes

## Debugging Techniques Toolbox

Use these as needed during investigation:

### Binary Search Isolation
Narrow the bug location by halving the search space: comment out half the logic, check if bug persists, recurse into the guilty half.

### Backward Trace (Root-Cause Tracing)
Start at the symptom (bad value, wrong state) and trace backward through the call stack:
- Where does the bad value come from?
- What called this function with that value?
- Keep tracing up until you find the original source of corruption.
- Fix at the source, not at the symptom.

### Strategic Instrumentation
Add temporary logging at component boundaries and decision points:
```
[ENTRY] function_name(args=...)
[STATE] variable=value after step X
[EXIT]  function_name -> result
```

### Git Bisect for Regressions
```bash
git bisect start
git bisect bad HEAD
git bisect good <last-known-good-commit>
# Test each revision until the guilty commit is found
```

### Common Bug Patterns to Check
| Pattern | What to look for |
|---------|-----------------|
| Off-by-one | `<` vs `<=`, index bounds, range endpoints |
| Null / None | Unguarded attribute access, missing dict keys |
| Race condition | Async operations, shared mutable state, ordering assumptions |
| Type mismatch | String vs int comparison, implicit coercion, wrong enum variant |
| Stale state | Cached values not invalidated, closure over mutable variable |
| Encoding | UTF-8 vs Latin-1, BOM bytes, `\xa0` non-breaking spaces |
| Environment | Missing env var, wrong DB, different OS path separator |

## Report Output

**Save every RCA report to a file** in the project directory at `./docs/ops/rcas/`.

- Create the `docs/ops/rcas/` directory if it doesn't exist.
- File naming: `YYYY-MM-DD-<short-slug>.md` (e.g. `2026-03-30-api-500-race-condition.md`)
- The slug should be a brief, kebab-case summary of the bug.
- Always tell the user the path of the saved report.

Structure every RCA report as:

```markdown
# Bug RCA: [Short title]
**Date:** YYYY-MM-DD
**Author:** Claude (ops-bug-rca skill)
**Status:** [Open | Fixed | Won't Fix]

## 1. Problem Statement
[What is broken, when it started, how it manifests]

## 2. Environment & Context
[Versions, config, relevant state, reproduction steps]

## 3. Evidence Collected
[Error messages, stack traces, logs, diffs, data samples]

## 4. Hypotheses (Ranked by Likelihood)
1. **[Most Likely]** - [Hypothesis]: [Evidence supporting it]
2. **[Possible]** - [Hypothesis]: [Evidence supporting it]
3. **[Less Likely]** - [Hypothesis]: [Why still worth considering]

## 5. Investigation Steps Taken
[What you checked, what you found, what you ruled out]

## 6. Root Cause
[Precise identification of the underlying issue and causal chain]

## 7. Recommended Fixes (Ranked)

### Option A (Recommended): [Name]
- **Change:** [Specific code/config change]
- **Why:** [How it addresses root cause]
- **Risk:** [Low/Medium/High + side effects]
- **Verify:** [Test command or check]

### Option B (Alternative): [Name]
- **Change:** [Specific code/config change]
- **Why:** [How it addresses root cause]
- **Risk:** [Low/Medium/High + side effects]
- **Verify:** [Test command or check]

## 8. Prevention
- [Test to add]
- [Guard / assertion to add]
- [Monitoring or logging gap to close]
```

- Open every generated file with the standard artefact frontmatter (OKF-superset block — set `type` to this artefact's `okf_type` display name from the `metamodel` skill's `references/artefact-types-registry.yaml`, plus `title`, `description`, `tags`, `timestamp`, `status`, `owner`, `last_reviewed`, `review_interval`). Run `git config user.name` for `owner`. Set `status: draft` on initial scaffold. Default `review_interval: 90d`. Full schema: the `metamodel` skill's `references/artefact-frontmatter.md`.

## Principles

- **Evidence over intuition.** Every hypothesis must cite evidence.
- **Root cause over symptom.** The fix must address WHY, not just WHAT.
- **One change at a time.** Never bundle investigation changes.
- **Failing test first.** Before fixing, prove the bug exists in a test.
- **Systematic beats fast.** 15-30 min of RCA beats 2-3 hours of thrashing.
