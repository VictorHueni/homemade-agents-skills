# Open Items — migrated to the GitHub backend (2026-06-04)

> **This markdown ledger is retired.** As of **2026-06-04** this repo runs the **`github`**
> open-items backend (see [`backend.yml`](./backend.yml) and
> [`rules/open-items-governance.md`](../../../rules/open-items-governance.md) §5.3). Open
> items now live as **GitHub Issues** — there is no longer a live markdown ledger here
> (one backend per project; never both). Since **2026-07-20** (kit ADR-0009) the whole
> tracker is the ledger: the former `open-item` marker label is retired and issues use
> the standard `type:` vocabulary.

## Where open items live now

- **Live read-out:** the issue tracker —
  <https://github.com/VictorHueni/homemade-claude-kit/issues>, driven by the label axes
  (`type:` / `priority:` / `size:` / readiness / `state:`); closed issues are the archive.
- **Authoring:** the per-type issue forms (`1-bug` … `5-tech-debt` in the chooser).
- **Operating manual:** `util-open-items/SKILL.md` (`backend: github`) +
  `util-open-items/references/github-backend.md`.

## Identity translation (the OI-NNNN → #N map)

The one-way `markdown → github` migration (Mode 7) re-minted every `OI-NNNN` as a GitHub
issue number `#N`. The mapping is preserved in
[`migration-map.md`](./migration-map.md), and the full pre-migration markdown ledger is
frozen at [`archive/2026-Q2-pre-github-migration.md`](./archive/2026-Q2-pre-github-migration.md).

For example: `OI-0032` (the "generalise the github backend?" decision) is now
[#36](https://github.com/VictorHueni/homemade-claude-kit/issues/36), still open.

## Reverting

This was a deliberate, one-way cutover. To return to the `markdown` backend, restore
`archive/2026-Q2-pre-github-migration.md` to this path, delete `backend.yml`, and close the
migrated issues — the `migration-map.md` gives the `#N → OI-NNNN` correspondence.
