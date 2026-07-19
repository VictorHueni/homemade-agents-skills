# MADR 4.x Templates

Use these templates as the default ADR structure.
Source: <https://adr.github.io/madr/> and <https://github.com/adr/madr>.

## Full Template

```markdown
---
type: Architecture Decision Record
title: <short title>
description: <one-sentence summary of the decision>
tags: []
timestamp: <ISO 8601 datetime of last change>
status: draft
owner: <git config user.name>
last_reviewed: YYYY-MM-DD
review_interval: 180d
---

# <short title>

## Context and Problem Statement

<describe context and the concrete problem>

## Decision Drivers

- <driver 1>
- <driver 2>
- <driver 3>

## Considered Options

- <option 1>
- <option 2>
- <option 3>

## Decision Outcome

Chosen option: "<option x>", because <summarize why this option is best against the drivers>.

### Positive Consequences

- <benefit 1>
- <benefit 2>

### Negative Consequences

- <trade-off 1>
- <trade-off 2>

## Pros and Cons of the Options

### <option 1>

<short summary>

#### Positive

- <pro 1>
- <pro 2>

#### Negative

- <con 1>
- <con 2>

### <option 2>

<short summary>

#### Positive

- <pro 1>
- <pro 2>

#### Negative

- <con 1>
- <con 2>

### <option 3>

<short summary>

#### Positive

- <pro 1>
- <pro 2>

#### Negative

- <con 1>
- <con 2>
```

## Minimal Template

```markdown
---
type: Architecture Decision Record
title: <short title>
description: <one-sentence summary of the decision>
tags: []
timestamp: <ISO 8601 datetime of last change>
status: draft
owner: <git config user.name>
last_reviewed: YYYY-MM-DD
review_interval: 180d
---

# <short title>

## Context and Problem Statement

<describe context and problem>

## Decision Drivers

- <driver 1>
- <driver 2>

## Considered Options

- <option 1>
- <option 2>

## Decision Outcome

Chosen option: "<option x>", because <concise rationale>.

### Consequences

- Good: <benefit>
- Bad: <trade-off>
```

## Naming and Traceability Conventions

- Keep one decision per ADR.
- Prefer concrete titles that include the decision, not only the topic.
- Keep filenames stable and searchable.
- If superseding an old ADR, reference both ADR IDs explicitly.

## Frontmatter Rules

The `## Status` section is **removed** from the MADR body. Frontmatter `status` is the single source of truth — never duplicate it in the document body.

Supersession adds conditional fields to the standard OKF-superset block:

```yaml
# ADR being retired — status switches to superseded, superseded_by is added:
status: superseded
superseded_by: docs/architecture/decisions/adr-0003-use-cockroachdb.md

# Replacement ADR — created specifically to replace the above, so supersedes is added:
status: active
supersedes: docs/architecture/decisions/adr-0002-use-postgresql.md
```

the `metamodel` skill's Audit mode enforces both: flags any ADR body that still contains a `## Status` heading, and verifies that `superseded_by` / `supersedes` paths resolve to existing files with the expected counterpart status.
