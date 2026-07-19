# Methodology references — arch-arc42

Sources informing the four narrative arc42 sections.

---

## arc42 template

- [arc42 v9.0 — official template](https://arc42.org/overview) — authoritative structure for all nine sections
- [arc42 section-by-section guide](https://docs.arc42.org/) — rationale and form guidance per section
- Gernot Starke & Peter Hruschka, *arc42 in Practice* (Leanpub, 2016) — worked examples

---

## §2 Constraints

- **ISO/IEC/IEEE 42010:2022** — architecture description standard; defines constraints as a first-class architecture concern
- **TOGAF ADM Phase A** — preliminary architecture: identify constraints before design begins
- **[GDPR (Regulation EU 2016/679)](https://gdpr-info.eu/)** — mandatory constraints for EU data processing
- **[PCI DSS v4.0](https://www.pcisecuritystandards.org/)** — payment card data constraints
- **[HIPAA Security Rule (45 CFR Part 164)](https://www.hhs.gov/hipaa/)** — health data constraints
- **SOC 2 Trust Services Criteria** — enterprise SaaS security and availability constraints

---

## §4 Solution Strategy

- **Gernot Starke, *Effektive Softwarearchitekturen*** (Hanser, 9th ed. 2020) — strategic architecture decisions
- **Mark Richards & Neal Ford, *Fundamentals of Software Architecture*** (O'Reilly, 2020) — architectural tactics per quality attribute
- **Bass, Clements & Kazman, *Software Architecture in Practice*** (SEI, 4th ed. 2021) — quality attribute tactics catalogue; ATAM quality goal prioritisation
- **Michael Keeling, *Design It!*** (Pragmatic Programmers, 2017) — decision-driven architecture; tactics trees

---

## §8 Cross-Cutting Concepts

- **[OpenTelemetry specification](https://opentelemetry.io/docs/specs/otel/)** — distributed tracing and metrics instrumentation
- **[W3C Trace Context](https://www.w3.org/TR/trace-context/)** — standard trace propagation header (`traceparent`)
- **[RFC 7807 — Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc7807)** — canonical error envelope for REST
- **[OAuth 2.0 (RFC 6749)](https://www.rfc-editor.org/rfc/rfc6749) + [JWT (RFC 7519)](https://www.rfc-editor.org/rfc/rfc7519)** — authentication / authorisation patterns
- **[NO_COLOR convention](https://no-color.org/)** — referenced in `arch-cli-contract`; relevant for CLI cross-cutting
- **Martin Fowler, *Patterns of Enterprise Application Architecture*** (Addison-Wesley, 2002) — session, unit of work, repository, caching patterns
- **[Feature Flags (Martin Fowler)](https://martinfowler.com/articles/feature-toggles.html)** — flag taxonomy and lifecycle

---

## §11 Risks and Technical Debt

- **ISO 31000:2018** — risk management principles and guidelines; probability × impact scoring
- **SEI ATAM (Architecture Tradeoff Analysis Method)** — identifies architectural risks, sensitivity points, and tradeoff points during review
- **Tom DeMarco & Timothy Lister, *Waltzing With Bears*** (Dorset House, 2003) — risk management for software projects; origin of the "grown-ups" quote in arc42
- **Ward Cunningham** — original technical debt metaphor (1992 OOPSLA talk): debt is a deliberate shortcut, not sloppy work
- **[OWASP Top 10](https://owasp.org/www-project-top-ten/)** — canonical security risk taxonomy; relevant for `security` risk type
- **Martin Fowler, *Refactoring*** (Addison-Wesley, 2nd ed. 2018) — technical debt classification and remediation strategies
