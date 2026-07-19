# Bounded Context Discipline — Internal Claude Guidance

This file is internal guidance for Claude when running the `domain-bounded-context` skill. It is never copied into projects. It contains the integration pattern decision tree, subdomain classification guide, BC naming test, and quality checks that Claude must run before declaring any mode complete.

---

## Integration pattern decision tree

Use this tree to assign one of Evans' eight patterns to each BC-to-BC relationship. Work top to bottom; stop at the first match.

```
1. Is there NO integration between these two contexts?
   → Separate Ways. Document the isolation as a deliberate choice.

2. Do both teams share a common model subset that both contribute to?
   → Shared Kernel.
   Warning: requires high coordination. Only use when both teams are in the
   same organisation and have explicit agreement on the shared model boundary.
   Cost: every change to the kernel requires both teams to coordinate and
   both test suites to pass.

3. Does the upstream team actively maintain a stable API for the
   downstream's use, and does the downstream team have formal influence
   on the upstream roadmap (e.g., they are a customer in a planning sense)?
   → Customer-Supplier.
   The downstream team can raise requirements as a customer. The upstream
   team is expected to consider them — but retains final say.

4. Does the upstream team publish a formal, versioned, documented protocol
   for multiple downstreams (e.g., OpenAPI spec, Avro schema, event schema)?
   → Open Host Service (OHS) + Published Language (PL).
   These two often appear together: OHS = the service itself; PL = the
   formal schema it uses. They can also appear separately (OHS without a
   formal schema = just OHS; a shared schema with no service = just PL).

5. Does the upstream team NOT care about the downstream's needs, or the
   upstream is a third party / legacy system that will not change to
   accommodate the downstream?
   → Ask: can the downstream afford to let the upstream model infect it?
     A. Yes (the upstream model is clean enough, and accepting it costs little)
        → Conformist.
        Name it explicitly. Conformist is not failure — it is a rational
        choice to stop spending engineering effort on translation. Document
        the power imbalance.
     B. No (the upstream model is messy, or the downstream needs to protect
        its own model from upstream changes)
        → Anti-Corruption Layer (ACL).
        The downstream builds a translation layer that converts the upstream
        model into the downstream's own model. The upstream model never leaks
        into the downstream's domain logic.

6. Is the integration a legacy system that nobody owns and nobody can
   change, but which everything connects to?
   → Big Ball of Mud (for that legacy system).
   Do not design against a Big Ball of Mud; contain it. The downstream
   context should use an ACL to protect itself.
```

### Pattern quick-reference

| Pattern | Power dynamic | Coordination cost | Translation? |
|---|---|---|---|
| Shared Kernel | Equal | High — joint ownership | Partial — within the kernel |
| Customer-Supplier | Upstream has more power, but listens | Medium — roadmap negotiation | None — downstream consumes upstream model |
| Conformist | Upstream ignores downstream | Low — downstream just accepts | None — downstream adopts upstream model as-is |
| ACL | Downstream protects itself | Low — downstream maintains translation | Yes — full translation in the ACL |
| Open Host Service | Upstream publishes for many | Low — stable protocol | Depends — downstream may or may not translate |
| Published Language | Shared schema ownership | Medium — schema governance | Depends — both sides implement the schema |
| Separate Ways | None | None | None |
| Big Ball of Mud | Undefined / legacy | High — change is risky | Recommended — isolate behind an ACL |

### ACL translation description checklist

When ACL is chosen, the context map relationship definition MUST include a translation layer description. Verify:
- [ ] What entity/concept is translated? (e.g., upstream `userId` → downstream `MemberId`)
- [ ] What fields are mapped? (explicit, not vague)
- [ ] What is the translation direction? (upstream → downstream model only; never bidirectional for ACL)
- [ ] Where does the translation live? (adapter class, anti-corruption service, event transformer, etc.)
- [ ] What happens when the upstream changes? (is there a schema version contract, or is it monitored manually?)

---

## Subdomain classification guide

### Core subdomain

**Definition:** the bounded context where the business differentiates itself from competitors. The capability cluster that, if it disappeared, would eliminate the business's competitive advantage.

**Classification signals:**
- Leadership talks about this capability as "our secret sauce" or "what makes us different."
- Competitors cannot easily replicate this — it is not available as a SaaS or OSS package (or if it is, the business's version is significantly differentiated).
- The business is willing to invest senior engineering talent here indefinitely.
- Bugs or degradation here directly threaten the business's value proposition.

**Build/buy decision:** Always build. Do not outsource. Do not use generic solutions. Invest in the best engineers, the best tooling, and continuous improvement.

**Typical count per product:** 1–3. If you are classifying more than 3 as Core, apply the smell test: is each one actually differentiated, or is the team advocating for its own domain? Push back.

---

### Supporting subdomain

**Definition:** the bounded context that enables the Core to function but does not itself differentiate the business. Necessary to operate but not a source of competitive advantage.

**Classification signals:**
- The business needs this capability, but competitors need a similar capability too.
- A good enough solution exists (build or buy), but off-the-shelf doesn't quite fit the business's specific needs.
- Engineering investment here is cost-justified but not strategically essential.
- Bugs or degradation here affect operations but don't threaten the value proposition directly.

**Build/buy decision:** Build if no off-the-shelf solution fits well enough. Consider buying/licensing if a close-enough solution exists. Do not invest disproportionate senior engineering talent here.

**Typical count per product:** 2–5.

---

### Generic subdomain

**Definition:** the bounded context handling commodity capabilities that every business in the industry needs and that are fully available as standard solutions.

**Classification signals:**
- Multiple mature SaaS/OSS products solve this problem.
- There is no competitive advantage in doing this differently from competitors.
- The business's version needs to be good enough, not best-in-class.
- Off-the-shelf solutions would serve 90%+ of the business's needs without customisation.

**Build/buy decision:** Buy SaaS. Use OSS. Do not spend strategic engineering effort building commodity capabilities. Examples: authentication, email delivery, billing/invoicing, PDF generation, analytics dashboards.

**Typical count per product:** 2–5.

---

## BC naming test

Every bounded context name must pass all three checks before the name is accepted.

### Check 1 — Business concept test

**Question:** is the name a business concept noun phrase that a domain expert who has never heard of microservices would understand?

**Test:** say this sentence aloud — *"What does the [BC name] team do?"* — and listen to the answer.
- If the answer is a business activity ("they manage how we price our services"), the name is right.
- If the answer is a technical activity ("they run the microservice that handles API calls"), the name is wrong.

**Disqualifying patterns:**
- Technology names: "API Gateway", "Message Bus", "DatabaseService", "CachingLayer"
- Infrastructure names: "CloudStorage", "SearchIndex", "Queue"
- Layer names: "Frontend", "Backend", "Middleware"
- Generic verb-object pairs without domain specificity: "DataProcessor", "EventHandler"

**Passing examples:** "Order Fulfilment", "Member Registration", "Pricing and Quoting", "Claims Adjudication", "Supply Replenishment"

---

### Check 2 — CRUD context test

**Question:** does the name describe a domain responsibility, or does it describe a CRUD operation on an entity?

**Failing pattern:** [Entity] + Management / Service / CRUD — e.g., "User Management", "Product Service", "Order CRUD"

**Why it fails:** "User Management" tells you what the context operates on but not what it does. Two contexts might both operate on Users — this name doesn't distinguish them.

**Fix:** name what the context *does* in domain terms:
- "User Management" → "Member Registration" (if focused on onboarding) or "Identity and Access" (if focused on authentication/authorisation)
- "Product Service" → "Catalogue and Listing" (if focused on product discovery) or "Inventory Management" (if focused on stock)
- "Order CRUD" → "Order Processing" or "Order Fulfilment"

---

### Check 3 — Stable under technology change test

**Question:** would this name still make sense if the team replaced all their technology (migrated from Java to Python, from REST to gRPC, from SQL to NoSQL)?

- "Pricing Engine" ✅ — stable under technology change
- "SpringBoot Pricing Microservice" ❌ — names the technology, not the domain
- "GraphQL Product API" ❌ — names the integration technology

**Why it matters:** bounded context names are meant to outlive technology decisions. They appear in team names, directory names, documentation, and discussions with business stakeholders. A stable name reduces future rename churn.

---

## Quality checks

Run all checks before declaring any mode complete.

### Structural checks

- [ ] **No unassigned capabilities** — every C-N.M from the capability map is assigned to exactly one BC. Run: `grep "C-[0-9]\+\.[0-9]\+" docs/domain/02b-bounded-contexts.md` and verify every capability ID from capability-map.md appears exactly once.
- [ ] **No double-assigned capabilities** — a capability cannot appear in two BC definitions. If it appears in both, decide: which context truly owns it? The other gets a soft-link (read) access, not ownership.
- [ ] **No two BCs claim the same concept with the same meaning** — if both BCs use "Customer" and their definitions are identical, they may need to merge or use a Published Language to align. The whole point of separate contexts is semantic independence.

### Subdomain classification checks

- [ ] **Core count 1–3** — if more than 3 BCs are classified as Core, challenge each classification. Most "Core" nominations come from team advocacy, not strategic clarity. Ask: "would the business lose its competitive advantage if this context were replaced by a third-party SaaS solution?"
- [ ] **Every subdomain type has a rationale** — "Core because we say so" is not a rationale. The rationale must reference the competitive advantage or strategic role.
- [ ] **Generic subdomains have buy/outsource candidates noted** — if a context is Generic, the closing report should mention the leading SaaS/OSS solution the team should evaluate.

### Context map checks

- [ ] **Every relationship names a pattern** — no relationship entry that reads only "BC-01 calls BC-02's API." That is a technical description, not an integration pattern.
- [ ] **Every ACL has a translation description** — if the pattern is ACL but the translation description field is empty or `_TODO_`, flag as incomplete.
- [ ] **Conformist relationships are acknowledged, not hidden** — Conformist is often the honest name for a relationship that people prefer to call Customer-Supplier (because Customer-Supplier sounds more dignified). If the downstream team has zero influence on the upstream roadmap, it is Conformist.
- [ ] **Mermaid diagram renders** — apply the diagramming-mermaid rule: quote labels containing `<br/>`, colons, commas, parens, or special characters.
- [ ] **Coupling risk is assessed** — every relationship has a coupling risk (Low / Medium / High) with rationale.

### Naming checks

- [ ] **No technology names** in any BC name.
- [ ] **No CRUD names** in any BC name.
- [ ] **Stable under technology change** — would the name still work in 5 years?

### God context check

- [ ] **No BC owns more than ~40% of all capabilities** — if one BC owns most of the capability map, it is likely a god context. Split by subdomain type or by ubiquitous language cluster.
- [ ] **No BC has more than 4 integration relationships** — more than 4 suggests the BC is acting as an orchestrator/hub, which is often a Supporting subdomain pattern or a sign that the BC is two separate contexts.

### Conway alignment check

- [ ] **Team boundary recommendation exists for each BC** — even if the team doesn't follow it immediately, document the recommendation.
- [ ] **No BC spans multiple stream-aligned teams without explicit justification** — a shared BC with split team ownership creates coordination overhead and often leads to the model diverging.

---

## Common mistakes to avoid

1. **Conflating bounded context with microservice** — a bounded context is a semantic boundary. A microservice is a deployment unit. One BC can be implemented as multiple microservices; one microservice can straddle two BCs (badly, but it happens). Discovery must be semantic first.

2. **Confusing context map with a system topology diagram** — the context map shows integration *patterns and power dynamics*, not request flows or data pipelines. It is a strategic document, not a technical one.

3. **Treating all relationships as Customer-Supplier** — Customer-Supplier requires that the downstream has *formal influence* on the upstream roadmap. If the upstream team doesn't actively incorporate downstream requirements, it is Conformist (even if it feels uncomfortable to say so).

4. **Forgetting the ubiquitous language scope** — the most powerful signal that you've found a real bounded context boundary is discovering that the same word means something different in each context. Documenting this in the glossary linkage is not optional hygiene — it is the whole point of having separate contexts.

5. **Completing Mode 3 without reading the capability map** — the capability-to-BC assignment is the structural backbone of the bounded context map. Never fill BC definitions without verifying that every C-N.M is accounted for.
