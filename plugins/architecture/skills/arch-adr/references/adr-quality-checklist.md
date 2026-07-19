# ADR Quality Checklist

Use this checklist before finalizing an ADR.
Base conventions: MADR 4.x decision-quality guidance, adapted for repository usage.

## Decision Clarity

- The ADR captures exactly one decision.
- The problem statement is concrete and specific to the current system.
- Decision drivers are explicit and testable (cost, risk, performance, compliance, operability).

## Option Analysis

- At least two realistic options are documented.
- Each option has explicit positive and negative consequences.
- The chosen option is justified against the listed drivers, not by preference language.

## Outcome and Consequences

- The decision outcome states the chosen option clearly.
- Positive and negative consequences are both present.
- Follow-up actions or implementation implications are noted when needed.

## Traceability

- The ADR references relevant prior ADRs, RFCs, or tickets.
- Superseded/superseding relationships are explicit.
- File location and naming follow repository ADR conventions.

## Review Readiness

- The wording avoids vague terms such as "better" or "best" without criteria.
- Stakeholders and timeline context are sufficient for future readers.
- Another engineer can understand why this decision was made without external context.
