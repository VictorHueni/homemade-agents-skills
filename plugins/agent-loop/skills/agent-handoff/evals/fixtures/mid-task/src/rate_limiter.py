"""Sliding-window rate limiter — mid-task fixture for agent-handoff evals."""

from collections import deque
from time import monotonic


class SlidingWindowLimiter:
    def __init__(self, max_events, window_seconds, clock=monotonic):
        self.max_events = max_events
        self.window_seconds = window_seconds
        self._clock = clock
        self._events = deque()

    def allow(self):
        now = self._clock()
        self._evict_expired(now)
        if len(self._events) >= self.max_events:
            return False
        self._events.append(now)
        return True

    def _evict_expired(self, now):
        cutoff = now - self.window_seconds
        while self._events and self._events[0] < cutoff:
            self._events.popleft()

    def remaining(self):
        # In progress: should evict expired events before counting, but
        # eviction isn't wired in here yet — see FAILING_TEST.md.
        return self.max_events - len(self._events)
