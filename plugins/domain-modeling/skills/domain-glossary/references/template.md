<!-- glossary-version: 1.0 | created: YYYY-MM-DD -->

# {product} — Ubiquitous Language Glossary

> **Methodology:** Evans *Domain-Driven Design* (2003) Ch. 2 — Ubiquitous Language +
> Vernon *DDD Distilled* (2016) Ch. 2 — Developing the Ubiquitous Language +
> Fowler UbiquitousLanguage pattern (martinfowler.com).
> Every term in this file IS the identifier in code, tests, events, and conversations.

---

## How to use this glossary

1. **One term per concept per bounded context** — if you find two words for the same thing in the same BC, one of them is wrong and must be deprecated here.
2. **These terms ARE the identifiers in code** — class names, method names, event names, test names, and variable names all use the glossary term exactly as written.
3. **If business and engineering use different words for the same thing, this glossary wins** — escalate disagreements to the team, update here, update in code.
4. **Evolves continuously** — obsolete terms are marked Retired (never deleted); new terms are added here before they appear in code.

---

## Quick index

<!-- Alphabetical; each entry links to its #bc-nn-gt-nn anchor -->
<!-- Update this table whenever a term is added, retired, or renamed. -->

| Term | BC | ID | Status |
|---|---|---|---|
| _TODO_ | _TODO_ | _TODO_ | _TODO_ |

---

## {BC-01 Name}

> **Subdomain type:** Core | Supporting | Generic
> **BC reference:** [BC-01 {Name}](02b-bounded-contexts.md#bc-01)
> **Owner team:** _TODO_

---

#### {term name} · BC-01.GT-01

**Status:** Active

**Definition:** [1–2 sentences, business language only — no database terms, no framework names, no API terms. A domain expert who has never seen the codebase must agree this is correct.]

**Example:** "[A real sentence showing this term in use within the domain — e.g., 'When a {term} is submitted, the underwriting team reviews it within 48 hours.']"

**Aliases (deprecated):** _(none)_ <!-- or: "Client (deprecated — use Customer)" -->

**Anti-patterns:**
- This term is NOT [common confusion 1]
- This term is NOT [common confusion 2]

**Cross-context:**
- BC-02.GT-NN "[corresponding term name]" — [brief explanation of how the same real-world concept is modelled differently in BC-02]

**Code convention:** `{TermName}` (class) · `{termName}` (variable) · `{TermNameCreated}` (domain event)

**First referenced:** [artefact name + date, e.g., "Capability Map C2.1 · 2026-01-15"]

---

#### {term name} · BC-01.GT-02

**Status:** Active

**Definition:** _TODO_

**Example:** _TODO_

**Aliases (deprecated):** _TODO_

**Anti-patterns:** _TODO_

**Cross-context:** _TODO_

**Code convention:** _TODO_

**First referenced:** _TODO_

---

<!-- Repeat BC-01 term blocks for all terms in BC-01 -->

---

## {BC-02 Name}

> **Subdomain type:** Core | Supporting | Generic
> **BC reference:** [BC-02 {Name}](02b-bounded-contexts.md#bc-02)
> **Owner team:** _TODO_

---

#### {term name} · BC-02.GT-01

**Status:** Active

**Definition:** _TODO_

**Example:** _TODO_

**Aliases (deprecated):** _TODO_

**Anti-patterns:** _TODO_

**Cross-context:** _TODO_

**Code convention:** _TODO_

**First referenced:** _TODO_

---

<!-- Repeat for additional BCs as needed -->

---

## Cross-context translation matrix

> When the same real-world concept is modelled differently in two or more bounded contexts,
> the translation must be explicit here. Undocumented translations cause integration bugs.

| Real-world concept | BC-01 term (GT-NN) | BC-02 term (GT-NN) | Divergence note |
|---|---|---|---|
| _TODO_ | _TODO_ | _TODO_ | _TODO_ |

---

## Changelog

| Date | Mode | Change summary | Author |
|---|---|---|---|
| YYYY-MM-DD | Scaffold | Initial skeleton created | _TODO_ |
