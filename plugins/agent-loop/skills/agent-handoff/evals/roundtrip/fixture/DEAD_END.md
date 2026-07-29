# Dead end already explored — round-trip fixture

Before landing on the current `_evict_oldest()` shape, a side-table approach was tried and
abandoned in this session:

Tracking access order with a separate `self._access_times` dict (key → monotonic timestamp,
updated on every `get()`/`put()`), then having `_evict_oldest()` scan that dict for the
smallest timestamp and pop the matching key from `self._store`.

Abandoned: this introduces a second source of truth that can drift from `_store`'s actual
order (e.g. if a key is evicted from `_store` but its entry in `_access_times` is never
cleaned up), and it requires updating both structures on every access instead of one.
`OrderedDict` already tracks insertion/access order for free via `move_to_end()` — the bug
here is only in which end `popitem()` targets (see `REMAINING_STEP.md`), not in how order is
tracked. Do not reintroduce a parallel `_access_times` structure to fix this.
