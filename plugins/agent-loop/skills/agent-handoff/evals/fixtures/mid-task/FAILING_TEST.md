# Failing test — mid-task fixture

`python3 -m pytest tests/ -q` from this directory:

```text
.F                                                                       [100%]
=================================== FAILURES ===================================
____________________ test_remaining_reflects_expired_events ____________________

    def test_remaining_reflects_expired_events():
        clock = iter([0.0, 0.0, 90.0]).__next__
        limiter = SlidingWindowLimiter(max_events=3, window_seconds=60, clock=clock)
        limiter.allow()
        limiter.allow()
>       assert limiter.remaining() == 3
E       assert 1 == 3
E        +  where 1 = remaining()

tests/test_rate_limiter.py:19: AssertionError
=========================== short test summary info ============================
FAILED tests/test_rate_limiter.py::test_remaining_reflects_expired_events - a...
1 failed, 1 passed in 0.54s
```

`remaining()` in `src/rate_limiter.py` doesn't call `_evict_expired()` before counting, so it
undercounts free slots once events have aged out of the window. `allow()` already evicts
correctly — the fix is calling `self._evict_expired(self._clock())` at the top of
`remaining()` too.
