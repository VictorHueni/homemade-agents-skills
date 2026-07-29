from src.rate_limiter import SlidingWindowLimiter


def test_allow_within_budget():
    limiter = SlidingWindowLimiter(max_events=3, window_seconds=60)
    assert limiter.allow()
    assert limiter.allow()
    assert limiter.allow()
    assert not limiter.allow()


def test_remaining_reflects_expired_events():
    clock = iter([0.0, 0.0, 90.0]).__next__
    limiter = SlidingWindowLimiter(max_events=3, window_seconds=60, clock=clock)
    limiter.allow()
    limiter.allow()
    # Both events are now 90s old, past the 60s window, so remaining() should
    # report all 3 slots free. It doesn't — see FAILING_TEST.md.
    assert limiter.remaining() == 3
