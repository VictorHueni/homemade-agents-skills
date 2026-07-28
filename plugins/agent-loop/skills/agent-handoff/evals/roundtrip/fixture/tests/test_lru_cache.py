from src.lru_cache import LRUCache


def test_put_get_roundtrip():
    cache = LRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1
    assert cache.get("b") == 2


def test_evicts_least_recently_used():
    cache = LRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")  # "a" is now most-recently-used; "b" is least-recently-used
    cache.put("c", 3)  # should evict "b", not "a"
    assert cache.get("a") == 1
    assert cache.get("b") is None
    assert cache.get("c") == 3
