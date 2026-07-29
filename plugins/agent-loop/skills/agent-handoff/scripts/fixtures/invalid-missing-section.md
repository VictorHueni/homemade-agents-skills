# Handoff: rate limit middleware rollout

**Date:** 2026-06-10
**Branch:** feat/rate-limit-middleware
**HEAD sha:** 9c3e1a7f4d6b2059817e4c3a9f6d2059817e4c3a
**Approx. context used:** 50%
**Chain:** rate-limit-middleware — 01 of 1

## Goal

Add a token-bucket rate limiter middleware in front of `/api/*` so a single client can't
starve shared capacity, without adding a new external dependency (Redis is not available in
every deployment target yet).

## Approach & key decisions

- In-process token bucket keyed by client IP, stored in a bounded LRU so memory stays flat
  under high cardinality. Chosen over a sliding-window log because the bucket is O(1) per
  request and doesn't need to retain per-request timestamps.
- Rejected a Redis-backed limiter for this pass: not every deployment target runs Redis yet,
  and the in-process approach is sufficient until multi-instance deployments need a shared
  limiter.

## State

Done:

- `src/middleware/rate_limit.py`: token bucket implementation, unit-tested.

In progress:

- Wiring the middleware into the app factory: added to the dev config, not yet added to the
  prod config.

Remaining:

- Add the prod config wiring.
- Load-test under the expected peak request rate.

## Files

- `src/middleware/rate_limit.py:1-48` — the token bucket implementation.
- `src/app_factory.py:30` — dev-config wiring, prod-config line not yet added.

## Verification

`pytest tests/middleware/test_rate_limit.py -q` — 6 passed, 0 failed (last run this session).

## Constraints & gotchas

Verified facts:

- The LRU cap is set to 10,000 keys; confirmed via a local load test that this stays under
  50MB resident memory at that cardinality.

Hypotheses / open questions:

- Assuming client IP is a good enough key for now; unclear whether requests behind the
  corporate proxy will all collapse to one IP and share a bucket unfairly.

## Suggested skills

None identified — this is a direct code change with existing test infrastructure.

## Next step

Add the prod-config wiring in `src/app_factory.py` alongside the existing dev-config line,
then re-run the full middleware test suite.
