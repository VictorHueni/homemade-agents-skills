# Remaining step — round-trip fixture

`python3 -m pytest tests/ -q` from this directory:

```text
.F                                                                       [100%]
=================================== FAILURES ===================================
_______________________ test_evicts_least_recently_used ________________________

    def test_evicts_least_recently_used():
        cache = LRUCache(capacity=2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")  # "a" is now most-recently-used; "b" is least-recently-used
        cache.put("c", 3)  # should evict "b", not "a"
        assert cache.get("a") == 1
>       assert cache.get("b") is None
E       AssertionError: assert 2 is None
E        +  where 2 = get('b')
E        +    where get = <src.lru_cache.LRUCache object at 0x79056c84f250>.get

tests/test_lru_cache.py:19: AssertionError
=========================== short test summary info ============================
FAILED tests/test_lru_cache.py::test_evicts_least_recently_used - AssertionEr...
1 failed, 1 passed in 0.25s
```

`_evict_oldest()` in `src/lru_cache.py` calls `self._store.popitem(last=True)`, which pops the
most-recently-used end of the `OrderedDict` (recall `get()` moves accessed keys to that end via
`move_to_end`). It should pop the other end instead: `self._store.popitem(last=False)`.
