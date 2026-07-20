# Research 0003 — Issue-Template Conformance Review

Date: 2026-07-20
Status: decided — findings applied same-day (ADR-0009 amendments)
Scope: fit-gap check of the kit's per-type Issue Forms against classic GitHub
issue-template best practices and real template sets from 10 major OSS repos (Vite,
Vitest, Nuxt, Astro, Next.js, React, VS Code, Rust, Kubernetes, Tailwind) plus GitHub's
official docs. Companion to research 0001/0002.

## Verdict summary

Most shipped choices fit convention or are justified variants; three findings were acted
on, the rest confirmed as leave-as-is.

## Findings → actions taken

1. **Chooser order (deviation, fixed).** Templates list alphanumerically; GitHub's docs
   recommend numeric filename prefixes to control order (Next.js `1.bug_report.yml`,
   Astro `---01-bug-report.yml`). Our unprefixed slugs put "Decision needed" second.
   → Renamed to `1-bug` / `2-feature` / `3-task` / `4-docs` / `5-tech-debt`.
2. **Metadata-first field order (deviation, fixed).** No surveyed mainstream form opens
   with dropdowns — substance (description/reproduction) always leads. → Priority/Size
   moved to the end of every form.
3. **`decision` template (deviation, dropped — operator decision).** No mainstream repo
   ships a decision template; decisions live in ADRs/RFCs. A "decision needed" item is a
   `task` whose deliverable is the decision record; non-code decisions are logged outside
   the tracker. → Type set is 5 values; `decision-gap` → `type:task`; vocabulary 17
   labels (ADR-0009 §1 amendment).
4. **Duplicate-search checkbox (intentional omission, documented).** Near-universal in
   the wild (Vite/Vitest/Nuxt/GitHub docs example) — but our filers are the operator and
   agents whose contract requires a duplicate/dependency search before creation
   (Plan-0003 increments 07/12). → Omitted; noted in every form header; add the standard
   checkbox when a repo takes external filers.

## Confirmed fits (unchanged)

- `needs-triage` template-applied label (k8s uses exactly this; Vite family uses
  `pending triage`; React `Status: Unconfirmed`).
- Plain template names without emoji (infra-repo register: k8s, vscode, rust; emoji
  common but optional).
- `render: shell` on environment fields (matches Vite/Vitest); markdown intro blocks
  (universal); form lengths (within range).
- `blank_issues_enabled: false` (dominant — 7 of 9 surveyed configs).
- No security contact link in config.yml — majors use `SECURITY.md` + private
  vulnerability reporting instead, not contact_links.
- Labels instead of native Issue Types (org-only feature; personal repos have no
  alternative — see #72).
- snake_case field ids (mainstream is kebab-case, but ours are locked to the canonical
  slugs by Invariant I1 — the audit contract outweighs the cosmetic convention).

## Acknowledged deviations kept (with rationale)

- **Priority/Size dropdowns asked of the filer.** None of the 10 surveyed mainstream
  repos asks the filer for priority or effort — it is a maintainer-side triage output
  everywhere. Kept because our filer *is* the maintainer (or an agent), and the labeler
  workflow mirrors answers to queryable labels; the claim is still subject to triage.
- **5-template chooser incl. task/tech-debt.** Mainstream choosers are bug+feature,
  splitting further by subsystem, not work-type; tech-debt templates appear only in
  internal-engineering contexts. Kept as a deliberate internal-workflow design (Rust
  ships ~7 templates; count itself is not exotic).
- **No contact_links.** Every surveyed repo has them (Discussions/Discord/docs); ours is
  empty because the repo has no Discussions/community surface. Add a Discussions link if
  ever enabled.

## Possible later touches (not done)

- "Alternatives considered" optional field on the feature form (classic
  problem/solution/alternatives triple — Vite, old GitHub default).
- Emoji in template names if the chooser ever feels flat.

## Method + caveats

Real templates fetched raw from the 10 repos (file inventories established by filename
probing — directory listings were API-blocked, so per-repo sets may be incomplete);
GitHub docs read from the github/docs source. Prevalence claims are qualitative
(10-repo sample). Key sources: GitHub docs "Configuring issue templates" (ordering,
config.yml, maintainer blank-issue escape hatch) and "Syntax for issue forms"
(labels-must-exist, duplicate-checkbox example); kubernetes.dev issue-triage guide
(`needs-triage` lifecycle); vitejs/vite + nuxt/nuxt + withastro/astro template sets.
