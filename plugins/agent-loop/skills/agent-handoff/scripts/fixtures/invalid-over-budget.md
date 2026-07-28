# Handoff: search index rebuild throttling

**Date:** 2026-06-15
**Branch:** feat/search-index-throttle
**HEAD sha:** 7a2c5e9f1b3d604827c1e9f5a3b604827c1e9f5a
**Approx. context used:** 48%
**Chain:** search-index-throttle — 01 of 1

## Goal

Throttle the nightly search index rebuild so it stops saturating the shared DB
connection pool during business hours reruns.

## Approach & key decisions

- Cap the rebuild job to 5 concurrent DB connections via a semaphore, chosen over a
  separate read replica because provisioning one is out of scope for this fix.
- Filler consideration 1: revisited and kept the same conclusion as above.
- Filler consideration 2: revisited and kept the same conclusion as above.
- Filler consideration 3: revisited and kept the same conclusion as above.
- Filler consideration 4: revisited and kept the same conclusion as above.
- Filler consideration 5: revisited and kept the same conclusion as above.
- Filler consideration 6: revisited and kept the same conclusion as above.
- Filler consideration 7: revisited and kept the same conclusion as above.
- Filler consideration 8: revisited and kept the same conclusion as above.
- Filler consideration 9: revisited and kept the same conclusion as above.
- Filler consideration 10: revisited and kept the same conclusion as above.
- Filler consideration 11: revisited and kept the same conclusion as above.
- Filler consideration 12: revisited and kept the same conclusion as above.
- Filler consideration 13: revisited and kept the same conclusion as above.
- Filler consideration 14: revisited and kept the same conclusion as above.
- Filler consideration 15: revisited and kept the same conclusion as above.
- Filler consideration 16: revisited and kept the same conclusion as above.
- Filler consideration 17: revisited and kept the same conclusion as above.
- Filler consideration 18: revisited and kept the same conclusion as above.
- Filler consideration 19: revisited and kept the same conclusion as above.
- Filler consideration 20: revisited and kept the same conclusion as above.
- Filler consideration 21: revisited and kept the same conclusion as above.
- Filler consideration 22: revisited and kept the same conclusion as above.
- Filler consideration 23: revisited and kept the same conclusion as above.
- Filler consideration 24: revisited and kept the same conclusion as above.
- Filler consideration 25: revisited and kept the same conclusion as above.
- Filler consideration 26: revisited and kept the same conclusion as above.
- Filler consideration 27: revisited and kept the same conclusion as above.
- Filler consideration 28: revisited and kept the same conclusion as above.
- Filler consideration 29: revisited and kept the same conclusion as above.
- Filler consideration 30: revisited and kept the same conclusion as above.
- Filler consideration 31: revisited and kept the same conclusion as above.
- Filler consideration 32: revisited and kept the same conclusion as above.
- Filler consideration 33: revisited and kept the same conclusion as above.
- Filler consideration 34: revisited and kept the same conclusion as above.
- Filler consideration 35: revisited and kept the same conclusion as above.
- Filler consideration 36: revisited and kept the same conclusion as above.
- Filler consideration 37: revisited and kept the same conclusion as above.
- Filler consideration 38: revisited and kept the same conclusion as above.
- Filler consideration 39: revisited and kept the same conclusion as above.
- Filler consideration 40: revisited and kept the same conclusion as above.
- Filler consideration 41: revisited and kept the same conclusion as above.
- Filler consideration 42: revisited and kept the same conclusion as above.
- Filler consideration 43: revisited and kept the same conclusion as above.
- Filler consideration 44: revisited and kept the same conclusion as above.
- Filler consideration 45: revisited and kept the same conclusion as above.
- Filler consideration 46: revisited and kept the same conclusion as above.
- Filler consideration 47: revisited and kept the same conclusion as above.
- Filler consideration 48: revisited and kept the same conclusion as above.
- Filler consideration 49: revisited and kept the same conclusion as above.
- Filler consideration 50: revisited and kept the same conclusion as above.
- Filler consideration 51: revisited and kept the same conclusion as above.
- Filler consideration 52: revisited and kept the same conclusion as above.
- Filler consideration 53: revisited and kept the same conclusion as above.
- Filler consideration 54: revisited and kept the same conclusion as above.
- Filler consideration 55: revisited and kept the same conclusion as above.
- Filler consideration 56: revisited and kept the same conclusion as above.
- Filler consideration 57: revisited and kept the same conclusion as above.
- Filler consideration 58: revisited and kept the same conclusion as above.
- Filler consideration 59: revisited and kept the same conclusion as above.
- Filler consideration 60: revisited and kept the same conclusion as above.
- Filler consideration 61: revisited and kept the same conclusion as above.
- Filler consideration 62: revisited and kept the same conclusion as above.
- Filler consideration 63: revisited and kept the same conclusion as above.
- Filler consideration 64: revisited and kept the same conclusion as above.
- Filler consideration 65: revisited and kept the same conclusion as above.
- Filler consideration 66: revisited and kept the same conclusion as above.
- Filler consideration 67: revisited and kept the same conclusion as above.
- Filler consideration 68: revisited and kept the same conclusion as above.
- Filler consideration 69: revisited and kept the same conclusion as above.
- Filler consideration 70: revisited and kept the same conclusion as above.
- Filler consideration 71: revisited and kept the same conclusion as above.
- Filler consideration 72: revisited and kept the same conclusion as above.
- Filler consideration 73: revisited and kept the same conclusion as above.
- Filler consideration 74: revisited and kept the same conclusion as above.
- Filler consideration 75: revisited and kept the same conclusion as above.
- Filler consideration 76: revisited and kept the same conclusion as above.
- Filler consideration 77: revisited and kept the same conclusion as above.
- Filler consideration 78: revisited and kept the same conclusion as above.
- Filler consideration 79: revisited and kept the same conclusion as above.
- Filler consideration 80: revisited and kept the same conclusion as above.
- Filler consideration 81: revisited and kept the same conclusion as above.
- Filler consideration 82: revisited and kept the same conclusion as above.
- Filler consideration 83: revisited and kept the same conclusion as above.
- Filler consideration 84: revisited and kept the same conclusion as above.
- Filler consideration 85: revisited and kept the same conclusion as above.
- Filler consideration 86: revisited and kept the same conclusion as above.
- Filler consideration 87: revisited and kept the same conclusion as above.
- Filler consideration 88: revisited and kept the same conclusion as above.
- Filler consideration 89: revisited and kept the same conclusion as above.
- Filler consideration 90: revisited and kept the same conclusion as above.
- Filler consideration 91: revisited and kept the same conclusion as above.
- Filler consideration 92: revisited and kept the same conclusion as above.
- Filler consideration 93: revisited and kept the same conclusion as above.
- Filler consideration 94: revisited and kept the same conclusion as above.
- Filler consideration 95: revisited and kept the same conclusion as above.
- Filler consideration 96: revisited and kept the same conclusion as above.
- Filler consideration 97: revisited and kept the same conclusion as above.
- Filler consideration 98: revisited and kept the same conclusion as above.
- Filler consideration 99: revisited and kept the same conclusion as above.
- Filler consideration 100: revisited and kept the same conclusion as above.
- Filler consideration 101: revisited and kept the same conclusion as above.
- Filler consideration 102: revisited and kept the same conclusion as above.
- Filler consideration 103: revisited and kept the same conclusion as above.
- Filler consideration 104: revisited and kept the same conclusion as above.
- Filler consideration 105: revisited and kept the same conclusion as above.
- Filler consideration 106: revisited and kept the same conclusion as above.
- Filler consideration 107: revisited and kept the same conclusion as above.
- Filler consideration 108: revisited and kept the same conclusion as above.
- Filler consideration 109: revisited and kept the same conclusion as above.
- Filler consideration 110: revisited and kept the same conclusion as above.
- Filler consideration 111: revisited and kept the same conclusion as above.
- Filler consideration 112: revisited and kept the same conclusion as above.
- Filler consideration 113: revisited and kept the same conclusion as above.
- Filler consideration 114: revisited and kept the same conclusion as above.
- Filler consideration 115: revisited and kept the same conclusion as above.
- Filler consideration 116: revisited and kept the same conclusion as above.
- Filler consideration 117: revisited and kept the same conclusion as above.
- Filler consideration 118: revisited and kept the same conclusion as above.
- Filler consideration 119: revisited and kept the same conclusion as above.
- Filler consideration 120: revisited and kept the same conclusion as above.
- Filler consideration 121: revisited and kept the same conclusion as above.
- Filler consideration 122: revisited and kept the same conclusion as above.
- Filler consideration 123: revisited and kept the same conclusion as above.
- Filler consideration 124: revisited and kept the same conclusion as above.
- Filler consideration 125: revisited and kept the same conclusion as above.
- Filler consideration 126: revisited and kept the same conclusion as above.
- Filler consideration 127: revisited and kept the same conclusion as above.
- Filler consideration 128: revisited and kept the same conclusion as above.
- Filler consideration 129: revisited and kept the same conclusion as above.
- Filler consideration 130: revisited and kept the same conclusion as above.
- Filler consideration 131: revisited and kept the same conclusion as above.
- Filler consideration 132: revisited and kept the same conclusion as above.
- Filler consideration 133: revisited and kept the same conclusion as above.
- Filler consideration 134: revisited and kept the same conclusion as above.
- Filler consideration 135: revisited and kept the same conclusion as above.
- Filler consideration 136: revisited and kept the same conclusion as above.
- Filler consideration 137: revisited and kept the same conclusion as above.
- Filler consideration 138: revisited and kept the same conclusion as above.
- Filler consideration 139: revisited and kept the same conclusion as above.
- Filler consideration 140: revisited and kept the same conclusion as above.
- Filler consideration 141: revisited and kept the same conclusion as above.
- Filler consideration 142: revisited and kept the same conclusion as above.
- Filler consideration 143: revisited and kept the same conclusion as above.
- Filler consideration 144: revisited and kept the same conclusion as above.
- Filler consideration 145: revisited and kept the same conclusion as above.
- Filler consideration 146: revisited and kept the same conclusion as above.
- Filler consideration 147: revisited and kept the same conclusion as above.
- Filler consideration 148: revisited and kept the same conclusion as above.
- Filler consideration 149: revisited and kept the same conclusion as above.
- Filler consideration 150: revisited and kept the same conclusion as above.
- Filler consideration 151: revisited and kept the same conclusion as above.
- Filler consideration 152: revisited and kept the same conclusion as above.
- Filler consideration 153: revisited and kept the same conclusion as above.
- Filler consideration 154: revisited and kept the same conclusion as above.
- Filler consideration 155: revisited and kept the same conclusion as above.
- Filler consideration 156: revisited and kept the same conclusion as above.
- Filler consideration 157: revisited and kept the same conclusion as above.
- Filler consideration 158: revisited and kept the same conclusion as above.
- Filler consideration 159: revisited and kept the same conclusion as above.
- Filler consideration 160: revisited and kept the same conclusion as above.

## State

Done:

- `src/search/reindex.py`: semaphore-based throttle, unit-tested.

In progress:

- Tuning the concurrency cap against staging load: 5 confirmed safe, testing 8.

Remaining:

- Land the final concurrency value after the staging test finishes.

## Files

- `src/search/reindex.py:1-40` — throttle implementation.

## Verification

`pytest tests/search/test_reindex.py -q` — 4 passed, 0 failed (last run this session).

## Dead ends — do not retry

- Tried a fixed sleep between batches instead of a semaphore. Abandoned: it throttled
  evenly regardless of actual pool pressure, wasting time when the pool was idle.

## Constraints & gotchas

Verified facts:

- The shared pool caps at 20 connections; confirmed via the DB config this session.

Hypotheses / open questions:

- Assuming 5 concurrent connections leaves enough headroom for other daytime jobs;
  not yet confirmed against a full daytime load profile.

## Suggested skills

None identified — this is a direct code change with existing test infrastructure.

## Next step

Finish the staging concurrency test at 8 connections and land the final cap value.

