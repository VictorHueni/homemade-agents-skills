# NFR Definition and Examples — Reference

> **Primary sources:**
> - ISO/IEC 25010:2023. *Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model.* ISO/IEC.
> - Starke, G. et al. *arc42 Quality Model* — quality.arc42.org · CC BY-SA 4.0 · github.com/arc42/quality.arc42.org-site
> - Bass, L., Clements, P. & Kazman, R. (2021). *Software Architecture in Practice*, 4th ed. Addison-Wesley.
> - Robertson, S. & Robertson, J. (2012). *Mastering the Requirements Process*, 3rd ed. Addison-Wesley.
> - BABOK v3 §9.1.4. IIBA (2015).

---

## What is a Non-Functional Requirement?

**BABOK v3 §9.1.4:**
> "Non-functional requirements describe the environmental conditions or qualities required for a solution to be effective. They do not describe what the solution does — they describe constraints on how well it does it."

**Robertson & Robertson (2012) — the fit criterion principle:**
> "Every NFR must carry a fit criterion: a measurable, testable condition that determines unambiguously whether the requirement has been satisfied. A quality statement without a fit criterion is a wish, not a requirement."

**Bass, Clements & Kazman (2021) — quality attribute scenarios:**
> "A quality attribute is a measurable or testable property of a system that indicates how well it satisfies the needs of its stakeholders. It must be expressed as a scenario with: stimulus, stimulus source, environment, artifact, response, and response measure."

**In one sentence:** an NFR defines *how well* the system performs a function — not *what* it performs. Every NFR must be falsifiable: you must be able to state "this passes" or "this fails."

---

## The arc42 Quality Model — 9 dimensions

The arc42 quality model (Starke et al., quality.arc42.org) organises 184 quality characteristics and 141 requirement scenarios across 9 dimensions. These map onto ISO/IEC 25010:2023 as follows:

| arc42 dimension | ISO/IEC 25010:2023 characteristic | Core question |
|---|---|---|
| **Efficient** | Performance Efficiency | Fast enough? Cheap enough? |
| **Flexible** | Flexibility (was Portability) | Adaptable to change? |
| **Maintainable** | Maintainability | Easy to sustain and evolve? |
| **Operable** | Maintainability (Analysability) | Easy to run and monitor? |
| **Reliable** | Reliability | Correct under all conditions? |
| **Safe** | Safety *(new in 25010:2023)* | Does it avoid unacceptable risk? |
| **Secure** | Security | Protected from unauthorised access? |
| **Suitable** | Functional Suitability | Does it do the right things? |
| **Usable** | Interaction Capability (was Usability) | Can the right people use it? |

> **Note:** *Suitable* (Functional Suitability) is handled by the FBS, not this artefact.
> *Compatible* (Compatibility) is a distinct ISO characteristic not listed as a separate arc42 dimension but covered under Flexible/Suitable.

---

## Granularity rule — the fit criterion test

Before writing any quality attribute entry, apply the Robertson & Robertson fit criterion test:

> "If you removed the acceptance criterion, would the statement still be testable?" → If yes, the criterion is wrong.
> "Could a tester produce a pass/fail verdict in isolation?" → If no, the criterion is too vague.

**Too vague (not an NFR):**
- "The system shall be fast"
- "The system shall be secure"
- "The UI shall be user-friendly"

**Too granular (configuration, not NFR):**
- "The login button shall be 44px tall"
- "The API timeout shall be set to 30 seconds"

**Right level — one characteristic × one product scope × measurable criterion:**
- "Schedule generation for a standard clinic (45 surgeons × 6 months) completes within 5 minutes on the production server (p95 over 20 consecutive runs)"
- "100% of cross-tenant data access attempts are blocked at the database layer, verified by automated penetration test suite quarterly"

---

## Examples per ISO/IEC 25010:2023 characteristic

*All examples below are inspired by arc42 quality scenarios (CC BY-SA 4.0).
Adapt acceptance criteria to your specific product context.*

---

### 1 · Performance Efficiency
*How the system performs relative to the resources it uses.*

**Sub-characteristics:** Time Behaviour · Resource Utilisation · Capacity

**Persona-context rule:** always state the persona's device and time constraint.

| Example name | Arc42 inspired by | Acceptance criterion pattern |
|---|---|---|
| **Response under load** | "Respond to 15,000 requests per workday" | "[Action] completes in ≤ [Xms] at p95 under [N] concurrent users, measured over [period]" |
| **Elastic scale-up** | "Scale up in 2 minutes" | "When traffic exceeds [X]% of baseline for [duration], platform adds capacity within ≤ [Y] minutes; p95 latency stays ≤ [Zs] throughout" |
| **Resource ceiling** | — | "Under [N] concurrent sessions, memory usage stays < [X] MB and CPU < [Y]% on [server spec]" |
| **Capacity limit** | — | "System supports [N] tenants × [M] users each with no degradation in [action] response time" |

**Measurable pattern (Bass et al. scenario structure):**
```
Stimulus:    [action or load event]
Environment: [normal / peak / stress condition]
Response:    [system completes / handles / recovers]
Measure:     [time threshold] at [percentile] over [N observations]
```

---

### 2 · Compatibility
*Ability to coexist with other systems and exchange information.*

**Sub-characteristics:** Co-existence · Interoperability

| Example name | Acceptance criterion pattern |
|---|---|
| **Standards interoperability** | "Data export conforms to [standard version]; any compliant consumer imports it without transformation, verified against [N] reference implementations" |
| **OIDC federation** | "System federates authentication with any OIDC 1.0-compliant provider; tested with [Entra ID / Google / Okta]; time-to-login after federation config ≤ [X] minutes" |
| **Co-existence** | "Running alongside [other system] on shared infrastructure causes ≤ [X]% degradation in [metric] for either system, verified by co-deployment test" |

---

### 3 · Interaction Capability *(Usability in ISO 25010:2011)*
*Degree to which the system can be used effectively by specific users.*

**Sub-characteristics:** Appropriateness Recognisability · Learnability · Operability · User Error Protection · User Engagement · Inclusivity · User Assistance · Self-Descriptiveness

**Mandatory: every entry names the persona (P-NN) and their context.**

| Example name | Arc42 inspired by | Acceptance criterion pattern |
|---|---|---|
| **First-time onboarding** | "First-time onboarding without errors" | "In usability tests with ≥ [N] representative [P-NN] users and no facilitator guidance, ≥ [X]% complete [flow] on first attempt in ≤ [Y] minutes; SUS score ≥ [Z]" |
| **Function discoverability** | "Access find function in 3 secs" | "[P-NN] with no prior training locates [function] within [X] seconds of landing on the home screen, without documentation (measured in usability sessions, N ≥ [10])" |
| **Mobile operability** | — | "All [persona] primary actions are completable on a [Xpx]-wide screen without horizontal scrolling; verified by automated viewport test on [device list]" |
| **Error prevention** | "Expressive error messages" | "System blocks [invalid action] and surfaces an explanatory message within [X] seconds; error message contains [required fields]; verified by automated regression suite" |
| **Accessibility** | "Accessible User Interface" | "Top [N] user journeys pass WCAG 2.1 AA with zero critical violations in automated CI scan; quarterly manual audit with keyboard + screen reader completes all critical journeys with zero blockers" |

---

### 4 · Reliability
*Degree to which the system performs its functions under stated conditions.*

**Sub-characteristics:** Faultlessness · Availability · Fault Tolerance · Recoverability

**Differentiator features (★ in FBS) must have zero-defect faultlessness entries.**

| Example name | Arc42 inspired by | Acceptance criterion pattern |
|---|---|---|
| **Zero false negatives** | "Financial transactions ACID-compliant" | "[Critical function] produces zero false negatives across [test suite covering N cases]; any detected false negative blocks release within [X minutes]" |
| **Availability SLA** | "Available 7×24 with 99% uptime" | "System achieves ≥ [X]% uptime during [business hours / 24×7]; measured over rolling [30-day] window; planned maintenance excluded if ≥ [Y hours] advance notice given" |
| **Fault tolerance** | "Server fails, system continues without downtime" | "When [dependency] fails, system [response]; legitimate requests continue to be served; no data loss; verified by chaos engineering test quarterly" |
| **Recoverability** | "MTTR 12h after complete failure" | "After [failure scenario], system restores to consistent state within ≤ [X hours]; zero committed data lost; recovery procedure documented and tested [annually]" |
| **DDoS resilience** | "Withstand DDoS attack" | "System maintains ≥ [X]% uptime and ≤ [Y]ms p95 latency during simulated [N×] peak traffic attack for [duration]; false-positive block rate ≤ [Z]%" |
| **Data integrity** | "Financial transactions ACID-compliant" | "All [operation type] are atomic; simulated mid-operation node failure produces zero partial writes in [N]-iteration stress test" |

---

### 5 · Security
*Degree to which the system protects information and data.*

**Sub-characteristics:** Confidentiality · Integrity · Non-Repudiation · Accountability · Authenticity · Resistance

**Swiss healthcare context:** anchor to nFADP retention obligations and ADR-0001/ADR-0003/ADR-0004.

| Example name | Arc42 inspired by | Acceptance criterion pattern |
|---|---|---|
| **Access control** | "Access control is enforced" | "100% of access attempts to [data class] are authenticated before access is granted; unauthorised attempts are blocked and logged within [X seconds]; policy updates take effect within [Y minutes]" |
| **Cross-tenant isolation** | — | "Under full operator access to storage/DB without tenant keys, 100% of [N ≥ 20] sampled tenant records remain inaccessible; verified by quarterly audit drill" |
| **Audit trail** | "Detailed audit log" | "Every [action type] produces an append-only log entry containing: user ID, timestamp (UTC µs), action, before/after state; logs retained for [X years]; retrievable within [Y hours] of authorised request" |
| **Encrypted storage** | "Encrypted storage" | "All data at rest (DB + backups) uses AES-256 or equivalent; zero plaintext storage verified by annual storage audit" |
| **Zero-knowledge storage** | "Zero-knowledge data storage" | "Operator with full DB access cannot decrypt [N ≥ 20] randomly sampled user files without user-controlled keys; verified by quarterly audit drill; any failure blocks release within [1 business day]" |
| **Session management** | — | "Sessions expire after [X minutes] of inactivity; re-authentication required; tokens not persisted in browser storage; verified by automated security test" |
| **Intrusion resistance** | "Withstand DDoS Attack" | "System passes OWASP Top 10 assessment with zero Critical/High findings; verified by [annual penetration test / continuous DAST scan]" |

---

### 6 · Maintainability
*Degree of effectiveness with which the system can be modified.*

**Sub-characteristics:** Modularity · Reusability · Analysability · Modifiability · Testability

| Example name | Arc42 inspired by | Acceptance criterion pattern |
|---|---|---|
| **Algorithm test coverage** | "Test Coverage for Critical Business Logic" | "[Module] achieves ≥ [X]% branch coverage; ≥ [Y]% of high-risk business rules are linked to ≥ 1 automated test; coverage threshold breach blocks merge within [Z minutes]" |
| **Modifiability** | "Adding entity type within 5 days" | "Adding [change type] modifies ≤ [N] existing modules; ≤ [M] lines changed outside the new scope; zero existing tests require modification (Open-Closed Principle); verified by automated fitness function in CI" |
| **Observability** | "Production anomalies detectable within 2 minutes" | "Production anomaly visible on dashboards within [X minutes] of onset; all services emit structured logs with [required fields]; alerts trigger within [Y seconds] of threshold breach" |
| **Code quality gate** | "Good code readability score" | "All [scope] modules pass [static analysis tool] with zero Blocker/Critical issues; [complexity metric] ≤ [threshold]; gate enforced in CI on every merge" |
| **Solo-maintainability** | — | "A single developer can apply security patches and dependency updates without external ops support; verified by documented runbook tested [quarterly]" |

---

### 7 · Flexibility *(Portability in ISO 25010:2011)*
*Degree to which the system adapts to different environments and requirements.*

**Sub-characteristics:** Adaptability · Scalability · Installability · Replaceability

| Example name | Arc42 inspired by | Acceptance criterion pattern |
|---|---|---|
| **Cloud portability** | "Easily change cloud provider" | "System deploys to [any EU/CH cloud provider] without code changes; only infrastructure configuration differs; verified by deployment test to [≥ 2 providers]" |
| **Tenant onboarding speed** | "On-prem installation ready in 30 minutes" | "New tenant is provisioned from configuration script in ≤ [X minutes] without manual server access; verified by onboarding runbook test [quarterly]" |
| **Database replaceability** | — | "Database migrated to alternative PostgreSQL host via pg_dump/restore with ≤ [X hours] planned downtime and zero data loss; procedure documented and tested [annually]" |
| **Deployment pipeline** | "Deploy to production within 15 minutes" | "End-to-end pipeline (merge → production) completes in ≤ [X minutes] at p95; zero 5xx errors during rollout; automated rollback triggers within [Y seconds] if error rate exceeds [Z]%" |
| **Multi-language readiness** | "Localizable to several languages" | "All user-facing strings are externalised; adding a new locale requires ≤ [N] file changes with zero code modifications; verified by [locale addition test]" |

---

### 8 · Safety *(new in ISO 25010:2023)*
*Degree to which the system avoids unacceptable risk to people, business, or environment.*

**Sub-characteristics:** Operational Constraint · Risk Identification · Fail Safe · Hazard Warning · Safe Integration

*Safety attributes are most relevant in Phase 2 (patient-adjacent data). Phase 1 safety requirements are limited.*

| Example name | Acceptance criterion pattern |
|---|---|
| **Fail-safe on critical function unavailability** | "If [critical guard function] is unavailable, system [blocks operation / enters safe state] rather than proceeding; verified by dependency-kill test" |
| **Operational constraint enforcement** | "System never [dangerous action] regardless of user role or input; constraint cannot be bypassed via [UI / API / direct DB]; verified by adversarial test suite" |
| **Hazard warning** | "When [risk condition] is detected, system surfaces a blocking warning to [actor] before [consequential action] can proceed; warning persists until explicitly acknowledged; verified by scenario test" |
| **Clinical data integrity gate** | "When [patient-adjacent data] is incomplete or inconsistent, system prevents [intervention scheduling] and identifies the missing element; verified by data-completeness test suite covering [N] scenarios" |

---

## Quick reference — fit criterion vocabulary

From Robertson & Robertson (2012) — phrases that make criteria measurable:

| Vague term | Measurable replacement |
|---|---|
| "fast" | "completes in ≤ [X ms] at p[N] percentile under [load]" |
| "available" | "achieves ≥ [X]% uptime measured over rolling [30-day] window" |
| "secure" | "passes [specific test / standard] with zero [severity] findings [annually]" |
| "easy to use" | "≥ [X]% of [P-NN] users complete [task] on first attempt in ≤ [Y minutes] without guidance" |
| "recoverable" | "restores to consistent state within ≤ [X minutes] with zero committed data loss after [failure scenario]" |
| "maintainable" | "change of type [X] modifies ≤ [N] modules and takes ≤ [Y] days for a developer with [experience level]" |
