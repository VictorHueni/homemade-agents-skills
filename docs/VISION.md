---
type: Product Vision
title: homemade-claude-kit — Product Vision
description: The north star for homemade-claude-kit — a harness-agnostic collection of skills, rules, and MCP tooling authored once and run natively across Claude Code, Codex, and OpenCode.
tags: [vision, harness-portability, agent-tooling]
timestamp: 2026-07-20T00:00:00Z
status: active
owner: Victor Hueni
last_reviewed: 2026-07-20
review_interval: 180d
---

<!-- doc-version: 1.0 | created: 2026-07-20 -->

# homemade-claude-kit — Product Vision

> **Methodology:** Geoffrey Moore *Crossing the Chasm* (1991) positioning format · Simon Sinek *Start With Why* (2009) Golden Circle · Roman Pichler *Strategize* (2016) Product Vision Board · Marty Cagan *Inspired* (2017) · Sean Ellis *Hacking Growth* (2017) North Star Metric.
> Canonical bibliography: `~/.claude/skills/business-vision/references/methodology-references.md`

**For:** developers and solo architects who drive their work through more than one AI coding harness (Claude Code, Codex CLI, OpenCode)
**North Star:** cross-harness capability coverage — the share of authored capabilities that run natively in every harness a user has
**Companion:** [clew](https://github.com/VictorHueni/clew) (the persistence / relationship / audit half of the harness) · [ADR index](architecture/decisions/) · [active plans](plans/active/)

---

## The Elevator Pitch

> For **developers and architects who work across more than one AI coding harness** who **re-configure their skills, behavioural rules, and MCP servers separately in each tool and lose that investment every time they switch**, **homemade-claude-kit** is a **harness-agnostic agent toolkit** (skills, rules, and MCP packaged as toggleable plugin sets) that **lets one authored capability run natively everywhere from a single source of truth**.
> Unlike **per-tool config or copy-paste sync scripts**, our product **distributes each skill in the one format all three harnesses read natively (SKILL.md) and generates the per-harness adapters, so the kit ages with the harnesses instead of fighting them.**

---

## The Problem We Solve

Anyone who uses more than one AI coding harness maintains their skills, rules, and MCP servers several times over — once per tool, in incompatible config shapes — so an improvement made in one harness has to be hand-rebuilt in the others or it silently rots. The reusable methodology an agent most needs — how to build the docs stack, run a governed backlog, commit cleanly — stays trapped in whichever proprietary format it was first written for, invisible to every other tool. The result is a personal investment that never compounds because it can't travel.

---

## The World We're Building Toward

A world where an agent capability is authored once and works everywhere — where adding or switching an AI harness costs nothing because your accumulated skills, rules, and tooling come with you.

---

## What We Are NOT

*Each item below is a specific, considered rejection — a direction we looked at and explicitly decided against.*

- **Not a harness.** We do not build a coding agent or compete with Claude Code / Codex / OpenCode — we make one investment portable across them.
- **Not the system of record.** Persistence, artefact relationships, deterministic ID minting, and audit are [clew](https://github.com/VictorHueni/clew)'s job; the kit ships agent-facing tooling, not the canonical data store (ADR-0007).
- **Not a per-project config manager.** The kit is user-global (`~/.claude`, `~/.codex`, `~/.agents`); project-root sync tools like rulesync / Ruler solve a different layer (ADR-0006).
- **Not a file-owning sync engine.** Adapters are generated behind swappable interfaces into marker-delimited blocks; we never take whole-file ownership of hand-edited config.
- **Not a stateful activation layer.** Toggling sets rides each harness's own native idiom; the kit ships no activation state of its own (ADR-0006).

---

## North Star Metric

> **Cross-harness capability coverage** — the proportion of the kit's authored capabilities (skills, rules, MCP servers) that install and run natively, with no per-harness rework, in every target harness a user runs.

This is the single directional indicator that tells us the product is delivering real value over time: one authored capability, live everywhere.

It is NOT a quarterly target — those would live in Business Objectives (`KR-NN.M`) if this repo ran its own objectives spine. The North Star is timeless and directional: coverage trends toward 100% across harnesses as the harnesses themselves evolve.

---

## Linked Artefacts

| Artefact | Relationship |
|---|---|
| [ADR-0006 — Plugin Packaging & Cross-Harness Activation](architecture/decisions/adr-0006-plugin-packaging-cross-harness-activation.md) | The packaging + native-toggling strategy that realises this vision |
| [ADR-0007 — Metamodel Distribution as a Skill](architecture/decisions/adr-0007-metamodel-distribution-as-skill.md) | How the methodology travels to all three harnesses in one format |
| [ADR-0002 / ADR-0003 — Pluggable open-items backend](architecture/decisions/adr-0002-open-items-pluggable-backend-github-issues.md) | The domain-agnostic-portability principle, applied to governance |
| [clew](https://github.com/VictorHueni/clew) | The companion half of the harness — persistence, relationships, deterministic IDs, audit |
| [Active plans](plans/active/) | Plan-0002 (harness-portable kit) and Plan-0003 (agent-execution layer) execute toward this vision |

---

## Changelog

| Date | Change | Trigger |
|---|---|---|
| 2026-07-20 | Initial draft | Purpose-clarification session; reverses the prior "no VISION.md" note in `docs/index.md` |
