# FBS Discipline — Internal Claude Guidance

This file is **not** copied into the project. It is internal guidance the
skill consults when applying anti-patterns, scope-violation detection,
the capability-vs-functionality-vs-feature decision tree, and status
hygiene.

---

## The six anti-patterns — run on every fill / update

### 1. Capability duplication

**Symptom:** the FBS contains strategic prose describing what a
capability *means*, restating content that belongs in the BC Map.

**Detection cues:**
- The per-capability section starts with multiple paragraphs of
  explanatory prose.
- The capability summary line is more than 1 sentence.
- "Strategic Importance" / "Boundaries" / "Outcomes" fields appear in
  the FBS — those are BC-Map fields.

**Fix:** keep capability summary to one line. Soft-link to the BC Map row
for the full definition. If the FBS doesn't have a one-liner the team
finds useful, the BC Map row probably lacks a punchy definition — fix it
there.

### 2. Roadmap drift

**Symptom:** dates, milestones, sprint numbers, quarter targets, or
release codes appear in the FBS.

**Detection cues:**
- Status column shows "Q2 2027" or "v2.0" instead of `✅ 🔄 ⬜`.
- Functionality rows include "due date" or "owner" fields.
- A "Timeline" or "Milestones" section appears.

**Fix:** strip all timeline content. Move to the roadmap doc. The FBS
shows *current state*, not *future commitments*.

### 3. Feature-spec creep

**Symptom:** functionality rows include acceptance criteria, user
stories, or detailed behavioural specs.

**Detection cues:**
- Functionality "Name" column contains "Given / When / Then" syntax.
- Rows have a "User story" or "Acceptance" field.
- The functionality is several sentences long.

**Fix:** the row name stays short (3–8 words). Detailed behavioural
spec belongs in a PRD. Add a soft-link column to the PRD if useful.

### 4. Status drift

**Symptom:** the FBS status doesn't match production reality. ✅
functionalities are actually behind a feature flag and not fully
shipped; ⬜ functionalities are actually in production.

**Detection cues:**
- The user reports that "X doesn't work but FBS says ✅".
- Recent shipped PRDs haven't been reflected in FBS status.
- Functionalities marked 🔄 have no corresponding active PRD.

**Fix:** audit periodically. The skill itself can't detect production
reality, but should warn the user to verify status during fill / update
mode. Recommend: after each PRD ships, run the FBS skill in fill mode to
promote 🔄 → ✅.

### 5. Over-decomposition

**Symptom:** L3 / L4 sub-functionalities emerging; functionality counts
per capability climbing toward 50+.

**Detection cues:**
- Functionality rows that look like implementation steps: "Initialise
  variable X", "Call API endpoint Y".
- Sub-bullets inside a functionality row.
- L3 sections appearing under L2 functionalities.

**Fix:** collapse back to L2. If the detail truly matters, it belongs
in a PRD or implementation plan, not in the FBS. If a capability has 30+
functionalities, the capability is probably too coarse at the BC Map
level — flag it.

### 6. Tech-named functionalities

**Symptom:** functionality names contain technology, vendor, system, or
tool names.

| ❌ Tech-named | ✅ System-action-named |
|---|---|
| "Build Salesforce integration" | "External-system synchronisation" |
| "Add Elasticsearch query" | "Full-text search" |
| "Migrate to Postgres 15" | "Database storage" *(no, this is a project not a functionality)* |
| "Implement OAuth2" | "User authentication" |

**Fix:** rename around what the system *does*, not how it does it.
"Migrate to Postgres 15" is a project (work package — belongs in a WBS or
plan), not a functionality. The functionality "Database storage" was
already shipped; the migration project upgrades the implementation but
doesn't add new functionality.

---

## Capability vs Functionality vs Feature vs Operation — decision tree

When triaging whether a candidate belongs in the FBS (and at what level),
work through these questions in order:

```
Is the candidate a stable, outcome-oriented business ability the org possesses?
├── Yes → CAPABILITY (belongs in BC Map; FBS soft-links by ID)
└── No
    │
    Is the candidate something the system DOES that's atomic and recognisable as one thing?
    ├── Yes → FUNCTIONALITY (FBS row at L2)
    └── No
        │
        Is the candidate a step / activity that USER does as part of a workflow?
        ├── Yes → USER STORY / SCENARIO (PRD territory)
        └── No
            │
            Is the candidate an implementation detail (API call, schema field, config option)?
            ├── Yes → not in FBS; belongs in implementation plan or code-level docs
            └── No
                │
                Is the candidate a delivery activity (sprint task, work package, milestone)?
                └── Yes → WBS / project plan / roadmap; not FBS
```

### Worked examples

| Candidate | Verdict | Why |
|---|---|---|
| "User registration" | Capability | Stable, business-outcome-oriented, owned by BC Map |
| "Validate email format" | Functionality | System does it; atomic; ships as one thing |
| "User clicks Submit, sees confirmation" | User story | User-perspective workflow → PRD |
| "Send POST to /v1/users" | Implementation detail | Code-level → not in FBS |
| "Migrate users table to UUID PKs" | Work package | Project task → WBS / plan, not FBS |
| "Full-text search across products" | Functionality | System does it; atomic |
| "Q3 search improvements" | Roadmap milestone | Not a functionality; → roadmap |
| "Search-as-you-type" | Functionality | System does it; atomic |
| "User sees results within 200ms" | Performance KPI | Operational → process doc / SLO, not FBS |

---

## Sizing decisions — internal heuristics

### L2 functionality count per capability

| Count | Diagnosis |
|---|---|
| 0–4 functionalities | Capability may be too narrow; verify it's a real capability or merge |
| 5–25 functionalities | Healthy |
| 26–40 functionalities | Capability is too coarse — likely two capabilities collapsed; split at BC Map |
| 40+ | Capability is doing too much OR you're decomposing into implementation detail |

### Total FBS functionality count

| Count | Diagnosis |
|---|---|
| <30 | Likely early-stage product; FBS will grow naturally |
| 50–500 | Healthy for active products (practitioner heuristic) |
| 500–1000 | Mature product family; consider sub-scoping by L0 (one FBS per product) |
| 1000+ | The FBS has likely absorbed PRD-level detail; audit for over-decomposition |

### L0 count (inherited from BC Map)

Should match the BC Map exactly. If FBS L0 disagrees with BC Map L0,
something is wrong — the FBS should never reorganise the strategic
hierarchy.

---

## Status hygiene — internal guidance

### Status promotion rules

- **⬜ → 🔄** when a PRD is approved that commits to delivering the functionality.
- **🔄 → ✅** when the PRD ships and the functionality is verifiably in production (not just deployed, but accessible to end users).
- **🔄 → ⬜** if a PRD is cancelled (rare; add changelog entry).
- **✅ → ⬜** if a functionality is retired (add changelog entry explaining why and when).

### Status anti-patterns

- ❌ "🚧" emoji for "in progress" — use 🔄 (planned).
- ❌ Partial-status notations like "✅ (mostly)" — pick one; if uncertain, leave 🔄.
- ❌ Promoting 🔄 → ✅ on PR merge without production deployment.
- ❌ Demoting ✅ → ⬜ silently when a feature is hidden behind a flag (note in changelog instead).

### When to audit

- After each major PRD ships (status drift check).
- Quarterly (catch slow drift).
- Before stakeholder reviews (the FBS will be cited).

---

## Capability-section guidance

### One-line capability summary

A one-line summary serves the **navigability** purpose, not the
**definition** purpose. The reader scanning the FBS should think "ah, I
remember what this capability is about" without needing to click through
to the BC Map.

| ❌ Long-form definition | ✅ Navigability one-liner |
|---|---|
| "Customer Onboarding provides the ability to register, validate, and maintain customer master data across the customer lifecycle, ensuring a single authoritative record per legal entity." | "Onboarding capability — register & validate customer records." |
| (10-line BC Map definition) | "Flagged-record visibility for reviewer-context users." |

The full definition stays in the BC Map; the FBS one-liner is the
working-memory reminder.

### Code-path annotations

Use the **package / folder granularity**, not file-level. Listing every
file in every functionality is noise; listing the package per capability
tells engineers where to look.

| ❌ File-level | ✅ Package-level |
|---|---|
| `Backend: src/users/register.py, src/users/validate.py, src/users/store.py` | `Backend: users/` |
| `Frontend: pages/auth/login.vue, pages/auth/register.vue, pages/auth/forgot.vue` | `Frontend: pages/auth/` |

When a capability spans multiple distinct packages, list them all
comma-separated. When a capability has frontend-only or backend-only
code, mark the missing side as `—` rather than `_TODO_` (the `—` signals
"this is intentional; not unknown").

---

## Quality checks before saving an FBS update

Run this mentally — don't print into the file:

- [ ] No capability definitions (just one-liner summaries) in any capability section.
- [ ] No PRD-style acceptance criteria in any functionality row.
- [ ] No roadmap dates / milestones anywhere.
- [ ] No operational metrics (latency, throughput) anywhere.
- [ ] Each functionality name describes *what the system does*, not what the user does.
- [ ] Each functionality has a unique ID (`C-N.M.FXX` pattern, never reused).
- [ ] Status reflects production reality where the user could verify.
- [ ] L2 functionality count per capability ≤ 25 (escalate if higher).
- [ ] Total functionality count ≤ ~500 (escalate if higher — consider sub-scoping).
- [ ] Methodology pointer in header links to the kit, not a local methodology-references.md.
- [ ] Capability one-liners + code paths use the right granularity.
- [ ] None of the 6 anti-patterns survived.

---

## When the user pushes back on the discipline

Acceptable fallbacks:
- VS-stage column can stay `_TODO_` (depends on value streams existing).
- Code paths can be `_TODO_` (engineering input needed).
- One-line capability summary can be `_TODO_` initially (forces the BC Map to have a punchy enough definition first).

Non-negotiable:
- No capability definitions in the FBS — that's BC Map territory; the user can soft-link, never restate.
- No PRD acceptance criteria — push to PRD.
- No roadmap dates / milestones — push to roadmap.
- The single-parent rule (every functionality has exactly one capability parent).
- Functionalities are *system actions*, not user actions or implementation steps.

If the user violates these despite pushback, ship the update with the
violation flagged in the §Changelog or §Open Items so a future reviewer
sees the compromise. (`Open Items` follows the canonical schema in
[`rules/open-items-governance.md`](../../rules/open-items-governance.md).)
