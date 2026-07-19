# Vision Discipline — Internal Claude Guidance

Internal reference for `business-vision` skill execution. Never copied to projects.

---

## The Moore Elevator Pitch test

Apply this test to §The Elevator Pitch before accepting it. All six slots must be specific:

| Slot | Test | Fail condition |
|---|---|---|
| **For [target]** | Name a specific persona type — not "businesses" or "users" | "enterprises", "healthcare companies", "users" are too vague |
| **who [problem]** | State the problem they have TODAY — not a future aspiration | "who want better operations" is aspirational; "who spend 3 days generating schedules manually" is a problem |
| **is a [category]** | Name the product category clearly | "platform", "solution", "tool" alone are too generic; "surgical workforce scheduling SaaS" is specific |
| **that [benefit]** | State the benefit in user terms — not a feature | "that has AI" is a feature; "that eliminates manual scheduling entirely" is a benefit |
| **Unlike [alternative]** | Name what users actually do TODAY | "unlike other tools" is not specific; "unlike Excel-based manual scheduling" is |
| **our product [differentiation]** | State what makes this specifically better | "is better" is not differentiation; "is purpose-built for surgical workforce constraints" is |

---

## North Star Metric vs Key Result discipline

The most common confusion in vision documents.

**North Star Metric (correct for `docs/VISION.md`):**
- Directional — "more is better" or "less is better," no fixed target
- Timeless — still valid in 5 years
- Captures core value delivered to the user
- No baseline/target pair, no deadline

**Key Result (belongs in `business-objective`, NOT in `VISION.md`):**
- Has a baseline value AND a target value
- Has a deadline (quarterly, annual)
- Measures progress over a specific period

| ❌ KR masquerading as North Star | ✅ True North Star |
|---|---|
| "Reduce coordinator hours from 4h to 30min by Q4" | "Coordinator-hours saved per week per active clinic" |
| "Achieve 90% surgeon confirmation rate by end of year" | "Surgeon confirmation rate across active clinics" |
| "Onboard 10 new clinics by year end" | "Active clinics running without spreadsheets" |
| "Zero double-booking incidents in Q1" | "Double-booking incidents per 1,000 scheduled procedures" |

If the candidate North Star has a deadline or a target number, it is a KR. Move it to `business-objective`.

---

## "What We Are NOT" quality checks

Each guardrail must be a **considered rejection** — not a generic disclaimer.

| ❌ Vague (useless) | ✅ Specific (useful) |
|---|---|
| "We are not a feature factory" | "We are not a general hospital management system — scope is exclusively surgical workforce coordination" |
| "We don't build for everyone" | "We are not a tool for patients — our users are clinical operations staff, not patients or prescribers" |
| "We stay focused" | "We do not replace HR or payroll systems — we integrate with them via API; we never own the employment-contract layer" |

A good "NOT" item: (a) names a direction the team was actually tempted by, (b) states clearly what the rejected scope covers, (c) helps future team members understand a decision without knowing the history.

---

## Anti-pattern detection cues

| Anti-pattern | Detection cue | Correction |
|---|---|---|
| Vision as roadmap | "by Q3", "by end of year", "this year we will" | Strip time references — vision is timeless |
| Vision as feature list | Technology or feature names as the core claim | Replace with value statements: what does the user achieve because of those features? |
| Missing NOT section | Only 1–2 guardrails, or all are vague | Add 3–5 specific, considered rejections from actual team discussions |
| North Star is a KR | Baseline + target + deadline present | Remove the target and deadline; move the time-bound version to `business-objective` |
| Too long | Document > 400 words or > 1 page | Cut ruthlessly — every sentence must earn its place |
| Jargon-heavy | Technical architecture terms, internal acronyms | Rewrite for a new team member's first day — or for an agent with no prior context |

---

## Wire mode safety checklist

Before executing Wire mode, verify:

- [ ] `docs/VISION.md` exists and has actual content (not just `_TODO_` placeholders)
- [ ] Project root path confirmed before running any file operations
- [ ] Checked for existing vision/context section: `grep -i 'vision\|north star\|product context' CLAUDE.md 2>/dev/null`
- [ ] Text to append has been shown to the user before writing
- [ ] Using Edit (append), NOT Write (overwrite) on an existing `CLAUDE.md`

After executing Wire mode, verify:

- [ ] All previously existing `CLAUDE.md` content is still present
- [ ] The vision pointer section appears exactly once
- [ ] `grep -c 'VISION.md' CLAUDE.md` returns `1`
