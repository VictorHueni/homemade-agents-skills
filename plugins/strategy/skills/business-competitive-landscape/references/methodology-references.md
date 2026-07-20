# Competitive Landscape — Methodology References

This document records the canonical frameworks used to design and maintain
competitive-landscape analyses. The artefact is a synthesis of four
primary sources plus practitioner discipline — each contributes a
specific lens.

The skill produces up to 4 markdown artefacts: hub doc (Porter +
tiering), per-competitor profile (SCIP practitioner template), strategic
group map (Porter / consulting practice), value curve (Kim & Mauborgne).

---

## 1. Michael Porter — Competitive Strategy (1980)

**Used for:** the **Five Forces** framework (industry structure
analysis) and the **substitutes / new entrants** taxonomy that drives the
competitor tier table.

**Source:** Michael E. Porter, *Competitive Strategy: Techniques for
Analyzing Industries and Competitors* (Free Press, 1980). Originally
introduced in Porter's 1979 HBR article *"How Competitive Forces Shape
Strategy"*. Wikipedia overview:
[Porter's five forces analysis](https://en.wikipedia.org/wiki/Porter's_five_forces_analysis).

### Key contributions

- **Five forces** — three horizontal (substitutes, established rivals,
  new entrants) + two vertical (suppliers, buyers). Together they
  determine industry attractiveness.
- **Industry structure → conduct → performance** paradigm. Industry
  structure shapes competitive dynamics; dynamics shape firm
  performance.
- **Substitutes deserve dedicated analysis.** Porter's #1 insight:
  substitutes (different category solving the same job) are often the
  biggest threat — easy to dismiss, hard to defend against once they
  scale.
- **Strategic groups** — Porter introduced the concept that firms in
  the same industry cluster into groups with similar strategies; these
  groups face similar competitive dynamics.

### Discipline encoded in the skill

- Hub doc has Porter's Five Forces as the top-level industry-structure table.
- Competitor tier table has explicit rows for Substitutes + Potential entrants (the two forces most often skipped in practitioner reports).
- Strategic Group Map artefact derives from Porter's strategic-group concept.

---

## 2. W. Chan Kim & Renée Mauborgne — Blue Ocean Strategy (2005)

**Used for:** the **Strategy Canvas / Value Curve** framework and the
**Four Actions Framework** (Eliminate / Reduce / Raise / Create) that
breaks mirror-matching positioning.

**Source:** W. Chan Kim & Renée Mauborgne, *Blue Ocean Strategy: How to
Create Uncontested Market Space and Make the Competition Irrelevant*
(Harvard Business Review Press, 2005). Canonical online tool:
[Strategy Canvas — blueoceanstrategy.com](https://www.blueoceanstrategy.com/tools/strategy-canvas/).

### Key contributions

- **Strategy Canvas:** *"a central diagnostic tool and an action
  framework for building a compelling blue ocean strategy that
  graphically captures, in one simple picture, the current strategic
  landscape and the future prospects for an organization."*
- **Horizontal axis:** *"the range of factors that an industry competes
  on and invests in"* — derived from competitor profiles + customer
  research.
- **Vertical axis:** *"the offering level that buyers receive across all
  of these key competing factors."*
- **Value curve:** *"the graphic depiction of a company's relative
  performance across its industry's factors of competition."*
- **Four Actions Framework:**
  - **Eliminate** — which factors the industry takes for granted should be eliminated?
  - **Reduce** — which factors should be reduced well below industry standard?
  - **Raise** — which factors should be raised well above industry standard?
  - **Create** — which factors should be created that the industry has never offered?
- **Red ocean vs Blue ocean:** Red oceans = known market with
  established rivalry; Blue oceans = uncontested market space created
  by reframing the factors of competition.

### Discipline encoded in the skill

- `cl-03-value-curve.md` artefact has 5–8 factors of competition + own + ≥2
  competitor curves + Four Actions section as the canonical structure.
- Mode 4 explicitly forces "what to eliminate / reduce / raise / create"
  thinking to break mirror-matching ("we do X better").
- The skill warns against red-ocean strategy in the anti-pattern catalogue.

### Acknowledged limitation

Practitioner critiques exist
([Shah Mohammed — A Dated Concept](https://shahmm.medium.com/a-dated-concept-the-pitfalls-of-blue-ocean-strategys-strategy-canvas-77614dfbf22a)).
Strategy Canvas can oversimplify multi-dimensional positioning. The
skill mitigates by combining the canvas with Strategic Group Mapping
(2D clustering with validation) and per-competitor profiles (multi-dim
depth).

---

## 3. Strategic Group Mapping (Porter + Consulting Practice)

**Used for:** the **strategic-group-map.md** artefact — clusters
competitors on 2 strategic dimensions with second-map validation.

**Source:** Michael Porter, *Competitive Strategy* (1980), chapter on
strategic groups; refined into a standalone consulting tool by McKinsey,
BCG, and Bain practitioners. Practitioner reference:
[Umbrex — Strategic Group Mapping](https://umbrex.com/resources/frameworks/strategy-frameworks/strategic-group-mapping/).
Practical walkthrough:
[FasterCapital — Strategic Group Mapping](https://fastercapital.com/content/Competitive-analysis--Strategic-Group-Mapping--Strategic-Group-Mapping--Charting-the-Course-of-Competitive-Analysis.html).

### Key contributions

- **Industries are not homogeneous.** Firms cluster into strategic
  groups; intra-group rivalry is more intense than inter-group rivalry.
- **Methodology:** (1) select 2 independent strategic dimensions, (2)
  plot competitors, (3) identify clusters (groups), (4) analyse
  group-level economics + group rivalry.
- **Validate with multiple maps.** One map can mislead because dimension
  choice is consequential. Best practice: build at least 2 maps on
  different dimension pairs; interesting clusters appear consistently.
- **Common dimension pairs:** price × breadth-of-offering · vertical-
  integration × geographic-scope · customer-segment × distribution-
  model · service-intensity × technology-leadership.

### Discipline encoded in the skill

- Strategic Group Map artefact requires **2 maps on different
  dimensions** (validation step explicit in template).
- Dimension-selection guidance: "must be independent + strategic +
  measurable; tied to economics and customer value."
- Cross-map analysis section: which clusters are stable, which are
  dimension-choice artifacts.

---

## 4. SCIP — Strategic and Competitive Intelligence Professionals

**Used for:** the **per-competitor profile template** structure,
evidence-and-source discipline, and refresh-cadence guidance.

**Source:** Strategic and Competitive Intelligence Professionals (SCIP).
[scip.org/page/Competitive-Intelligence-Foundational-Tools-and-Practices](https://www.scip.org/page/Competitive-Intelligence-Foundational-Tools-and-Practices)
(member access). Aligned practitioner guidance:
[Infodesk — How to Create a Competitive Intelligence Report](https://www.infodesk.com/blog/how-to-create-a-competitive-intelligence-report-best-practices).

### Key contributions

- **Competitive intelligence = gathering + analyzing + applying
  information about competitors, markets and business environments to
  aid strategic decision-making.**
- **Report structure:** executive summary → competitor profiles →
  SWOT → market trends → actionable insights.
- **Evidence-and-source discipline:** every claim should link to a
  primary source (company website, press release, regulatory filing,
  customer interview note). Confidence ratings + freshness dates
  separate signal from noise.
- **Refresh cadence:** competitive landscapes age fast in some
  industries (tech: 90 days) and slow in others (regulated:
  180–365 days).

### Discipline encoded in the skill

- Per-competitor profile template includes Evidence sources table with URL + date.
- Every claim carries `Confidence: Assumed | Tested | Validated` per Lean UX / Strategyzer style (consistent with `business-persona` and `business-model-canvas` skills).
- Refresh mode (mode 5) exists explicitly to audit stale claims.
- Suggested next-refresh date in closing report.

---

## 5. Practitioner anti-pattern literature

**Used for:** the 8 anti-patterns the skill guards against. Lifted from
practitioner consulting / competitive-intelligence sources.

**Sources:**
- Multiple practitioner blogs cited in `landscape-discipline.md`
- SCIP foundational tools (member-walled)
- Harvard Business Review case literature

### The 8 anti-patterns encoded

1. Listing competitors without tiering
2. SWOT-only analysis (skipping industry structure)
3. Stale claims without dates
4. Vague claims without evidence
5. Mirror-matching positioning (red-ocean strategy)
6. Ignoring indirect / substitute competitors
7. Solo authorship (no cross-functional review)
8. Missing "so what" (analysis without strategic implication)

---

## 6. (Related but out of scope) — PESTEL, BCG Matrix, Wardley Maps

**Used for:** awareness only. The skill does not produce these artefacts
in v1.

- **PESTEL** (Political / Economic / Social / Technological /
  Environmental / Legal) — macro-environment analysis. Useful context
  for the Five Forces analysis but not its own artefact in this skill.
  If needed, capture in the hub's Executive Summary or in a separate
  strategic-analysis doc.
- **BCG Growth-Share Matrix** (1970) — portfolio classification (stars
  / cash cows / question marks / dogs). Useful for multi-product
  portfolio analysis; out of scope for single-product competitive
  landscape.
- **Wardley Maps** — competitive landscape mapped to evolution stages
  (genesis → custom-built → product → commodity). Powerful but
  requires significant practice; consider as a v2 extension if user
  demand emerges.

---

## Summary — what each framework contributes

| Framework | Contributes |
|---|---|
| Porter — Competitive Strategy (1980) | Five Forces (industry structure); Substitutes + New Entrants taxonomy; Strategic Group concept |
| Kim & Mauborgne — Blue Ocean Strategy (2005) | Strategy Canvas + Value Curve; Four Actions Framework (Eliminate / Reduce / Raise / Create) |
| Strategic Group Mapping (consulting practice) | 2-dimension clustering; second-map validation discipline |
| SCIP — Competitive Intelligence practitioner | Per-competitor profile template; evidence-and-source discipline; refresh cadence |
| Practitioner anti-pattern literature | 8 common-mistake catalogue |
| Related (PESTEL / BCG / Wardley) | Awareness; out of scope in v1 |

The template is not "Porter alone" or "Blue Ocean alone" — it is the
canonical synthesis. Porter provides the industry-structure rigour; Kim
& Mauborgne provide the positioning-break discipline; SCIP provides the
evidence-and-source backbone; Strategic Group Mapping provides the
clustering view. Together they cover the four questions: how attractive
is the industry · who are we competing against · how are they clustered
· how should we position vs them.
