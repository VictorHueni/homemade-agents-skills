# Value Streams — Methodology References

This document records the canonical frameworks used to design and maintain
the [Value Streams](04a-value-streams.md). The artefact is a synthesis of two
primary sources plus practitioner guidance — each contributes a specific
lens.

The most important methodological choice up front is the **stance**: this
document encodes **EA-flavoured value streams** (TOGAF + BIZBOK), not Lean
VSM. The distinction is structural, not stylistic — see §1 below.

---

## 1. The EA-flavoured stance — TOGAF + BIZBOK, NOT Lean VSM

The phrase "value stream" carries two distinct traditions that are easily
confused. They produce different artefacts for different purposes. This
document anchors on the EA-flavoured tradition.

| Dimension | EA value stream *(this document)* | Lean VSM *(out of scope)* |
|---|---|---|
| **Source tradition** | TOGAF Series Guide + BIZBOK Guide (Business Architecture Guild) | Toyota Production System; Mike Rother, *Learning to See* (1999); Karen Martin & Mike Osterling, *Value Stream Mapping* (2014) |
| **Primary purpose** | Strategic — how value flows to a stakeholder | Operational — find waste, optimise cycle time |
| **Primary axes** | Stages, value items, capabilities consumed, participating stakeholders | Cycle time, queues, value-add vs non-value-add, takt time |
| **Output** | Strategic alignment between personas / capabilities / processes | Process improvement; flow optimisation; pull systems |
| **Audience** | Business architects, product strategists, executive sponsors | Operations leaders, continuous-improvement teams |
| **Companion artefacts** | Capability map, personas, processes | Process maps with cycle-time data, kaizen events |

**Where Lean VSM concerns belong in this project:** in process docs (the
`business-process` artefacts). Cycle times, queue depths, and
waste classification are operational concerns; they live in process docs
where the activity sequence is documented, not in this strategic catalogue.

---

## 2. TOGAF® Series Guide — Value Streams

**Used for:** the canonical structure of a value stream (stages, value
items, entrance/exit criteria, stakeholders), the capability-consumption
linkage between stages and the BC map, and the value-stream-vs-process
distinction.

**Source:** The Open Group, *TOGAF® Series Guide: Value Streams*.
[pubs.opengroup.org/togaf-standard/business-architecture/value-streams.html](https://pubs.opengroup.org/togaf-standard/business-architecture/value-streams.html)
(login-walled; the practitioner literature below is open).

### Key contributions

- **Value stream addresses how to identify, define, model, and map a value
  stream to other key components of an enterprise's Business Architecture.**
- **Decomposition into stages** is the canonical structuring discipline.
- **Each stage documents:** stage description · participating stakeholders
  · entrance criteria · exit criteria · value items.
- **Value is always defined from the perspective of the stakeholder of the
  product, service, or deliverable produced by the work** — never from
  the perspective of the producing organisation.
- **Identification approach:** Define the Customer → Determine the Value
  Proposition → Map the End-to-End Stages → Identify Value-Adding and
  Non-Value-Adding Activities → Prioritise.

### Discipline encoded in the template

- The per-stage block has all canonical TOGAF fields (participating
  stakeholders, entrance criteria, exit criteria, value items).
- The triggering-stakeholder + value-proposition pair is documented at the
  stream level before any stage decomposition begins.

---

## 3. BIZBOK® Guide — Business Architecture Body of Knowledge

**Used for:** the canonical definition of a value stream, the naming
convention (final value achieved + business object), the BIZBOK common
mistakes catalogue, and the rule that **value streams are stable while
processes change**.

**Source:** Business Architecture Guild, *A Guide to the Business
Architecture Body of Knowledge® (BIZBOK® Guide)*, v10+.
[BIZBOK Guide Part 1 — Introduction (open)](https://cdn.ymaws.com/www.businessarchitectureguild.org/resource/resmgr/bizbok_10/introduction_v10_final.pdf).
Supporting paper:
[*Similar Yet Different: Value Streams and Business Processes*](https://cdn.ymaws.com/www.businessarchitectureguild.org/resource/resmgr/public_resources/bpm_paper_final_dec2019.pdf)
(BIZBOK / Business Process Management Initiative joint paper, December 2019).

### Key contributions

- **Definition:** a value stream is *"a visual depiction of how an
  organization achieves value for a given stakeholder or stakeholders
  within the context of a given set of business activities."*
- **Components:** value stream stages · triggering stakeholder · value
  proposition · entrance and exit criteria · value items that accrue ·
  stakeholders that contribute to value at each stage.
- **Naming convention:** describe the **final value achieved** and
  leverage business objects where possible. Examples: "Acquire Product",
  "Onboard Human Resource", "Settle Claim".
- **Stable vs ephemeral:** value streams are **stable** descriptions of
  the value-delivery model; **business processes** are the operational
  mechanism that implements them and change with technology and
  organisation.
- **Capabilities are reused across streams:** *"a capability can be reused
  many times within and across value streams"* — so capabilities are NOT
  scoped to a single stream; they are shared across the BC map.
- **Sizing:** an organisation typically maintains *"around 24+ value
  streams"*, with complexity (not size) driving the count.
- **#1 BIZBOK scoping mistake:** internal-lifecycle naming
  ("hire-to-retire", "order-to-cash") frames the stream around internal
  phases, not stakeholder value. Use customer-outcome naming.

### Discipline encoded in the template

- The naming rule "name after the final value, use business objects" is
  encoded in the template guidance.
- The "one value proposition per stream" rule prevents over-scoped streams.
- The "capabilities are soft-linked, never inlined" rule prevents
  capability duplication between BC map and value-stream doc.

---

## 4. William Ulrich & Whynde Kuehn — Business Architecture Practitioner Synthesis

**Used for:** the practitioner framing of how value streams cross-map to
capabilities, the "core and extended mapping" discipline, and the
business-driven-IT-transformation use case.

**Source:** William Ulrich, Whynde Kuehn, and Business Architecture Guild
Editorial Board, *Business Architecture Quick Guide*. Practitioner work
collected at:
- [Business Architecture Associates resources](https://businessarchitectureassociates.com/resources/)
- BIZBOK Guild [Editorial whitepapers](https://www.businessarchitectureguild.org/resource/resmgr/public_resources/)

### Key contributions

- **Value streams + capabilities + organisation + information form the
  four foundational dimensions of business architecture.** Each dimension
  cross-maps to the others.
- **Core mapping** = value stream → stage → capability link. **Extended
  mapping** = capability → information → organisation → process / IT
  service link.
- **Business-driven IT transformation:** value streams expose where IT
  investment will create stakeholder value; capability maps expose
  redundancies; the pairing makes investment cases concrete.

### Discipline encoded in the template

- Per-stage capability-consumption links (soft-link to BC map by ID).
- The "pain index" field (this skill's addition) provides the prioritisation
  layer for transformation decisions, in the spirit of Ulrich/Kuehn's
  business-driven-IT framing.

---

## 5. Scott Millett — Customer Journeys, Value Streams, and Business Capabilities

**Used for:** the explicit distinction between **customer journey** (actual
experience + emotions) and **value stream** (idealised value delivery), and
the warning not to conflate the two artefacts.

**Source:** Scott Millett, *Customer Journeys, Value Streams and Business
Capabilities… and how to bring them together*.
[scottmillett.medium.com](https://scottmillett.medium.com/customer-journeys-value-streams-and-business-capabilities-and-how-to-bring-them-together-7eb912937e23).

### Key contributions

- **Customer Journey** = maps experience and emotions of the customer
  before, during, and after interacting with the business / service.
  Captures the **actual** experience.
- **Value Stream** = shows how value is delivered to the customer across
  the organisation. Captures the **idealised** delivery model.
- **Business Capability** = the competencies an organisation must possess
  to deliver on strategic objectives.
- **Relationship:** value streams typically encompass multiple
  capabilities; journeys map customer touchpoints to the value streams +
  capabilities behind them.

### Discipline encoded in the template

- The skill explicitly redirects emotion-mapping / channel-mapping
  requests to journey-mapping tools (out of scope here).
- The template doesn't carry emotion / channel / touchpoint columns —
  those would conflate journey with value stream.

---

## 6. SAFe — Operational and Development Value Streams *(referenced, not adopted)*

**Used for:** awareness; the skill does NOT adopt SAFe's
operational-vs-development distinction in v1 (deferred per project
preference).

**Source:** Scaled Agile Framework,
[Operational Value Streams](https://framework.scaledagile.com/operational-value-streams/).

### Why not adopted

SAFe distinguishes:
- **Operational value streams** — how the customer receives value through
  business solutions.
- **Development value streams** — how teams build the business solutions
  that operational value streams use.

This distinction is useful in software-engineering-led organisations but
adds noise for non-tech projects and pure business-architecture work. If a
project explicitly wants the SAFe distinction, add an
`Operational / Development / Both` field to the catalogue table — but the
default template treats every stream as operational.

---

## Summary — what each framework contributes

| Framework | Contributes |
|---|---|
| TOGAF Value Streams Guide | Canonical stage structure (stakeholders, entrance/exit, value items); capability-consumption linkage; identification approach |
| BIZBOK Guide | Definition; naming convention; #1 scoping mistake catalogue; stable-vs-ephemeral rule; ~24 streams per enterprise sizing; "capabilities reused across streams" rule |
| Ulrich & Kuehn | Practitioner framing; core-and-extended mapping; business-driven-IT-transformation use case |
| Scott Millett | Journey-vs-stream distinction; warning against conflation |
| SAFe *(noted, not adopted)* | Operational/development split; available as optional extension |

The template is not "TOGAF value streams" or "BIZBOK value streams" — it
is the canonical synthesis. Every section maps back to at least one
source. The EA-vs-Lean-VSM stance is the soul of the document; TOGAF
provides the structural fields; BIZBOK provides the naming and scoping
rules; Ulrich/Kuehn provide the practitioner framing; Millett guards the
boundary with journeys.
