# Handoff: cursor pagination on the /items endpoint

**Date:** 2026-06-02
**Branch:** feat/items-cursor-pagination
**HEAD sha:** 4f2c9a1e8b3d5f60712a4c9e8d1b3a5f60712a4c
**Approx. context used:** 55%
**Chain:** items-cursor-pagination — 01 of 1

## Goal

Replace offset-based pagination on `GET /api/items` with cursor-based pagination (opaque
base64 cursor encoding `(created_at, id)`), so clients paging through a growing table don't
see duplicate or skipped rows when new items are inserted mid-page.

## Approach & key decisions

- **Cursor encoding: base64(created_at_iso + "|" + id)**, decoded and validated server-side.
  Chosen over a raw integer offset because offsets shift under concurrent inserts; chosen
  over a signed/HMAC cursor because the endpoint has no untrusted-client-tamper risk (cursor
  only controls read position, not access scope) — revisit if that changes.
- **Rejected: keyset on `id` alone.** `id` is a UUID with no ordering guarantee tied to
  insertion time, so a client couldn't get "most recent first" ordering from it.
- **Rejected: `Link` header pagination (GitHub-style).** Would require reworking every
  existing client's pagination handling in one release; opaque cursor in the response body
  is additive and backward-compatible with clients that ignore it.
- Page size stays capped at the existing `limit=50` default/max; not part of this change.

## State

Done:

- `src/api/items/pagination.py`: `encode_cursor()` / `decode_cursor()`, unit-tested.
- `src/api/items/routes.py`: `GET /api/items` now accepts `?cursor=` and returns
  `next_cursor` in the response envelope.

In progress:

- Backward-compat shim for `?offset=` clients: stubbed in `routes.py` behind a
  `deprecated_offset_param` flag, step 2 of 3 — offset-to-cursor translation on first page
  works, translation past page 1 not yet implemented.

Remaining:

- Finish offset→cursor translation past page 1.
- Add an integration test that pages through 120 seeded rows entirely via cursors and
  asserts no duplicate/skip under a concurrent insert.
- Update the API reference doc's pagination section.

## Files

- `src/api/items/pagination.py:1-64` — cursor encode/decode, the core of this change.
- `src/api/items/routes.py:112-168` — route handler, `next_cursor` construction, offset shim.
- `tests/api/items/test_pagination.py` — unit tests for the encode/decode round-trip.
- `docs/architecture/interfaces/items-api.md` — pagination contract doc, not yet updated.

## Verification

`pytest tests/api/items/test_pagination.py -q` — 8 passed, 0 failed (last run this session).

`pytest tests/api/items/test_routes.py -q -k pagination` — 1 failed:

```text
FAILED tests/api/items/test_routes.py::test_offset_shim_page_two - AssertionError:
expected 50 items starting after id=e3a1..., got 50 items starting after id=00000...
(offset shim resets to page 1 on any offset > limit)
```

This is the known-incomplete offset shim from "In progress" above, not a regression.

## Dead ends — do not retry

- Tried encoding the cursor as a raw signed integer offset into the base64 payload (keeping
  the old semantics but obscuring them). Abandoned: it re-introduces the exact skip/duplicate
  bug this change exists to fix, just hidden behind opaque encoding — the underlying ordering
  problem is unrelated to whether the offset is visible to the client.
- Tried adding a database-level `WHERE (created_at, id) > (?, ?)` keyset query directly in
  the ORM's `.filter()` without a dedicated cursor module. Abandoned after two failed
  attempts to express the tuple comparison portably across the project's supported DB
  backends (SQLite in tests vs Postgres in prod) — the standalone `pagination.py` module with
  backend-specific branches was clearer and is what's now in place.

## Constraints & gotchas

Verified facts:

- The `items` table has a unique index on `(created_at, id)` already (confirmed via
  `\d items` in the dev DB) — no migration needed for the keyset query itself.
- `test_offset_shim_page_two` is the only failing test; every other pagination test passes.

Hypotheses / open questions:

- Assuming no client depends on offset pagination returning stable results under concurrent
  inserts today — not confirmed against real client usage, only against the API contract
  doc. If a client does depend on that, the offset shim's "translate to nearest cursor" may
  produce visibly different results than before.
- Unclear whether the 50-row page cap should become configurable as part of this change or a
  separate one — leaning separate, not decided.

## Suggested skills

None identified — this is a direct code change with existing test infrastructure; no
architecture, spec, or planning skill is needed to finish it.

## Next step

Finish the offset-to-cursor translation for `offset > limit` in
`src/api/items/routes.py:150-168` so `test_offset_shim_page_two` passes, then run the full
`tests/api/items/` suite before starting the concurrent-insert integration test.
