# Claude-Internal Discipline — Domain Glossary

> This file is NEVER copied to project output. It is guidance for Claude
> when executing `domain-glossary` modes. It encodes quality tests,
> detection patterns, and deprecation rules that are not visible to users
> but must be applied silently to every term processed.

---

## Definition quality test (Evans standard)

Apply this test to every definition before writing it to the glossary. A definition passes when ALL four conditions are true.

**Condition 1 — Not circular.** The definition does not use the term itself (or a trivial variation of it).

- Fail: "A Claim is a claim submitted by a Policyholder."
- Pass: "A Claim is a formal request by a Policyholder to receive compensation under the terms of their Policy, submitted after an insured event."

**Condition 2 — Business language only.** Zero tech-jargon words. Test: would a domain expert who has never touched a codebase find this definition accurate and complete?

Words that automatically fail this test: table, row, column, field, record, database, API, endpoint, schema, foreign key, nullable, index, query, migration, ORM, framework, microservice, entity (in the JPA/Hibernate sense), model (in the Rails sense), controller, payload, JSON, UUID, timestamp, enum.

Words that are fine: status, date, amount, identifier, reference, number, type, category — these are business concepts too.

**Condition 3 — Expert agreement.** A domain expert who has never seen the codebase would agree the definition is correct. If in doubt, flag the definition with `_TODO: validate with domain expert_`.

**Condition 4 — Differentiating.** The definition distinguishes this concept from the most similar concepts in the same BC. What makes a Claim different from a Complaint? What makes an Adjuster different from an Underwriter? If the definition could apply equally to a similar concept, it is too vague.

---

## Synonym detection patterns

When seeding or enriching the glossary, actively scan for these patterns. Any synonym found must be documented as a deprecated alias or escalated to the user for a canonical term decision.

**Pattern 1 — Capitalisation variations.** "customer" (lowercase in code) vs "Customer" (in specs) vs "CUSTOMER" (in legacy database). These are not different concepts. Pick one, note the others as aliases.

**Pattern 2 — Legacy names in code comments or TODOs.** "// formerly Account, renamed to Customer in Q3 2024". The legacy name survives in comments long after the rename. Document it as a deprecated alias so future readers know what it was.

**Pattern 3 — Department-specific vocabulary.** Sales says "Prospect". Marketing says "Lead". Engineering says "Contact". Operations says "Applicant". All four might refer to the same real-world concept at different lifecycle stages — or they might be genuinely distinct concepts. Determine which and either (a) unify under one term with deprecated aliases, or (b) define each as a distinct term with a clear lifecycle relationship.

**Pattern 4 — Abbreviations and codes.** "Claim" vs "CLM" (legacy system code). "Policy" vs "POL-ID". "Invoice" vs "INV". Abbreviations from legacy systems live in database column names, CSV headers, and message queue field names. Document them as deprecated aliases.

**Pattern 5 — Plural ambiguity.** "Orders" (a collection) vs "Order" (a single entity). The glossary always uses singular. If "Orders" appears as a distinct concept (e.g., an Orders aggregate that manages a collection), define it separately and note the relationship.

**Pattern 6 — Gerund vs noun.** "Onboarding" (process) vs "Onboarding" (the state a User is in). These may be genuinely different concepts — one is a process, one is a lifecycle state. Clarify and separate if needed.

---

## Cross-context translation rules

When the same real-world concept appears in two or more bounded contexts, follow these rules.

**Rule 1 — Identical modelling → consider Shared Kernel.** If both BCs model the concept with the same attributes, the same lifecycle, and the same business rules, they may be using the same model. Ask: should these BCs share a Published Language (formal contract) or a Shared Kernel (shared code)? Document the observation in the cross-context matrix and flag it for the architecture team.

**Rule 2 — Different modelling → document the translation explicitly.** If BC-01 models "Customer" with an emphasis on contact history and BC-02 models "Customer" as a billing account with payment terms, these are genuinely different models of the same real-world entity. The cross-context matrix entry must explain:
- What data maps from BC-01.Customer to BC-02.Customer
- What is lost in translation (attributes that exist in one BC but not the other)
- Who owns the translation logic (upstream/downstream relationship, ACL, Open Host Service)

**Rule 3 — Same name, completely different meaning → document the divergence.** "Product" in a Catalogue BC (a thing that can be browsed and purchased) and "Product" in a Billing BC (a billable line item with a price schedule) may share a name but are different concepts. The cross-context matrix entry must make this divergence explicit to prevent accidental coupling.

**Rule 4 — Translation ownership.** Every cross-context translation has an owner — the downstream BC typically owns the translation logic (Anti-Corruption Layer). The glossary records WHO owns it, not just THAT a translation exists.

---

## Alias deprecation discipline

When a synonym is identified, follow this four-step protocol.

**Step 1 — Add a deprecated alias entry.** In the term's entry, populate the `Aliases (deprecated)` field:

```
**Aliases (deprecated):** Client (deprecated — use Customer · BC-01.GT-03)
```

**Step 2 — Add a redirect note for legacy code readers.** If the alias appears in legacy code, legacy database columns, or legacy documentation, add a note:

```
**Anti-patterns:** If you encounter "Client" in legacy code (pre-2024) or in the `legacy_clients` database table, it refers to this concept (Customer). Do not introduce new usages of "Client".
```

**Step 3 — Never delete deprecated entries.** Deprecated aliases exist precisely to help team members who encounter them in legacy systems. Deleting them removes the explanation. A deprecated entry that survives for years is working correctly.

**Step 4 — Retire when the concept no longer exists.** Retired terms (concept was removed from the domain model, not just renamed) get:

```
**Status:** Retired (2026-03-15) — the Broker concept was merged into Agent after the distribution model change. See BC-01.GT-12 Agent.
```

The Retired date and the reason for retirement are mandatory. Future readers need to know WHY, not just that it happened.

---

## Code convention note discipline

Every fully enriched term must have a code convention note. Use this format:

```
**Code convention:** `{TermName}` (class/aggregate/entity name) · `{termName}` (local variable) · `{TermNameCreated}` / `{TermNameUpdated}` / `{TermNameCancelled}` (domain events, past tense) · `{TermNameRepository}` (repository interface)
```

Rules:
- Class names use the glossary term exactly — no abbreviations, no tech suffixes (not `TermNameBean`, not `TermNameModel`).
- Domain events use the glossary term + past-tense verb: `ClaimSubmitted`, `PolicyIssued`, `PaymentProcessed`.
- Repository interfaces: `{TermName}Repository` — the interface, not the implementation.
- Commands (if using CQRS): `Submit{TermName}`, `Cancel{TermName}`, `Approve{TermName}` — imperative verb + glossary term.
- If the codebase already uses a different convention that cannot be changed immediately, note the divergence: `Code currently uses LegacyName — migration to {TermName} tracked in [issue/PR link]`.

---

## Seeding quality bar

When seeding from a capability map or value stream, not every noun is automatically a glossary term. Apply this filter before assigning a GT-NN ID:

**Include:** nouns that represent domain concepts with business meaning — things the domain experts reason about, name in conversations, and track over time.

**Exclude:**
- Pure technical nouns (database, API, service, module, function)
- Infrastructure nouns (server, queue, cache, bucket) — unless the domain itself has these concepts (e.g., a Message Queue as a domain concept in a messaging product)
- Capability map category headers (L0 labels like "Customer Management" are categories, not terms — the L1 capabilities under them are better candidates)
- Generic business words that are not specific to this domain ("data", "information", "system", "process" — these mean nothing without context)

When in doubt: if a domain expert would nod and say "yes, that's a thing we work with every day" — include it. If they would say "that's just how the engineers talk about it" — exclude it.
