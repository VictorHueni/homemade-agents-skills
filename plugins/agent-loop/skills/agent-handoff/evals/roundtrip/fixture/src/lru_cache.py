"""Bounded LRU cache — round-trip fixture for agent-handoff evals."""

from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self._store = OrderedDict()

    def get(self, key):
        if key not in self._store:
            return None
        value = self._store[key]
        self._store.move_to_end(key)
        return value

    def put(self, key, value):
        self._store[key] = value
        if len(self._store) > self.capacity:
            self._evict_oldest()

    def _evict_oldest(self):
        # In progress: pops the most-recently-used end instead of the
        # least-recently-used one — see REMAINING_STEP.md.
        self._store.popitem(last=True)
