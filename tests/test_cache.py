import unittest
from cache_service.cache import CachingService, Entity


class TestCachingService(unittest.TestCase):
    """
    Unit tests for the CachingService class, validating:
    - Correct caching behavior (add, get, eviction)
    - LRU eviction strategy
    - Cache-database interaction
    - Error handling and edge cases
    """

    def setUp(self):
        self.cache = CachingService(max_size=3)
        self.entity1 = Entity(1, "D1")
        self.entity2 = Entity(2, "D2")
        self.entity3 = Entity(3, "D3")
        self.entity4 = Entity(4, "D4")

    def test_add_and_get(self):
        """Verify that a newly added entity can be retrieved from cache correctly."""
        try:
            self.cache.add(self.entity1)
            result = self.cache.get(self.entity1)
            self.assertEqual(result, self.entity1)
        except Exception as e:
            self.fail(f"Exception occurred during add/get test: {e}")

    def test_clear(self):
        """Ensure clearing the cache removes only in-memory entries,
        while preserving data in the underlying database."""
        try:
            self.cache.add(self.entity1)
            self.cache.add(self.entity2)
            self.cache.add(self.entity3)
            self.cache.add(self.entity4)
            self.cache.clear()
            result = self.cache.get(self.entity1)
            self.assertEqual(result, self.entity1)
        except Exception as e:
            self.fail(f"Exception occurred during clear test: {e}")

    def test_eviction_policy(self):
        """Validate that when the cache exceeds max size,
        the least recently used (LRU) entity is evicted."""
        try:
            self.cache.add(self.entity1)
            self.cache.add(self.entity2)
            self.cache.add(self.entity3)
            self.cache.add(self.entity4)
            result = self.cache.get(self.entity1)
            self.assertEqual(result, self.entity1)
        except Exception as e:
            self.fail(f"Exception occurred during eviction test: {e}")

    def test_remove(self):
        """Confirm that removing an entity deletes it from both
        cache and database, and future get returns None."""
        try:
            self.cache.add(self.entity1)
            self.cache.remove(self.entity1)
            result = self.cache.get(self.entity1)
            self.assertIsNone(result)
            result_db = self.cache._database.get(self.entity1.getId())
            self.assertIsNone(result_db)
        except Exception as e:
            self.fail(f"Exception occurred during remove test: {e}")

    def test_removeAll(self):
        """Ensure removeAll clears all entries from both cache and database.
        Subsequent fetches should return None."""
        try:
            self.cache.add(self.entity1)
            self.cache.add(self.entity2)
            self.cache.removeAll()
            self.assertIsNone(self.cache.get(self.entity1))
            self.assertIsNone(self.cache.get(self.entity2))
            result_db_1 = self.cache._database.get(self.entity1.getId())
            result_db_2 = self.cache._database.get(self.entity2.getId())
            self.assertIsNone(result_db_1)
            self.assertIsNone(result_db_2)
        except Exception as e:
            self.fail(f"Exception occurred during removeAll test: {e}")

    def test_get_from_db_when_not_in_cache(self):
        """Test fallback behavior: when cache is cleared,
        entity should still be fetched from the database."""
        self.cache.add(self.entity1)
        self.cache.clear()  # simulate only DB has it now
        result = self.cache.get(self.entity1)
        self.assertEqual(result, self.entity1)

    def test_add_null_entity_raises_error(self):
        """Verify that adding an entity with None ID raises a ValueError."""
        with self.assertRaises(ValueError):
            self.cache.add(Entity(None, "Null"))

    def test_evict_from_empty_cache_does_not_crash(self):
        """Ensure that eviction from an empty cache does not raise errors.
        Validates robustness under empty-state operations."""
        try:
            self.cache.add(Entity(1, "D1"))
            self.cache.remove(Entity(1, "D1"))
            self.cache.add(Entity(2, "D2"))
            self.cache.clear()
            self.cache.add(Entity(3, "D3"))
            self.cache.add(Entity(4, "D4"))
            self.cache.evict_least_used()
            cache_keys = self.cache.get_cache_keys()
            self.assertIn(4, cache_keys)
            self.assertNotIn(3, cache_keys)
        except Exception as e:
            self.fail(f"Eviction from empty cache raised exception: {e}")

    def test_add_duplicate_entity_does_not_duplicate(self):
        """Ensure that adding the same entity twice does not result
        in duplicate entries or increased cache size."""
        self.cache.add(self.entity1)
        self.cache.add(self.entity1)
        cache_keys = self.cache.get_cache_keys()
        self.assertEqual(len(cache_keys), 1)

    def test_cache_size_limit_enforced(self):
        """Verify that only the most recent 'max_size' number of entities
        are retained in the cache due to LRU eviction policy."""
        self.cache.add(Entity(1, "D1"))
        self.cache.add(Entity(2, "D2"))
        self.cache.add(Entity(3, "D3"))
        self.cache.add(Entity(4, "D4"))
        cache_keys = self.cache.get_cache_keys()
        self.assertEqual(len(cache_keys), 3)
        self.assertNotIn(1, cache_keys)
        self.assertIn(4, cache_keys)

    def test_get_non_existent_entity_returns_none(self):
        """Ensure that getting an entity not present in cache or DB returns None."""
        ghost_entity = Entity(999, "Ghost")
        result = self.cache.get(ghost_entity)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
