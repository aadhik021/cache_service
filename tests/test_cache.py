import unittest
from cache_service.cache import CachingService, Entity


class TestCachingService(unittest.TestCase):
    """
    Unit tests for the CachingService.
    """

    def setUp(self):
        self.cache = CachingService(max_size=3)
        self.entity1 = Entity(1, "D1")
        self.entity2 = Entity(2, "D2")
        self.entity3 = Entity(3, "D3")
        self.entity4 = Entity(4, "D4")

    def test_add_and_get(self):
        """Test adding and retrieving an entity from the cache."""
        try:
            self.cache.add(self.entity1)
            result = self.cache.get(self.entity1)
            self.assertEqual(result, self.entity1)
        except Exception as e:
            self.fail(f"Exception occurred during add/get test: {e}")

    def test_clear(self):
        """Test clearing the cache without affecting the database."""
        try:
            # Add 3 entities to fill cache
            self.cache.add(self.entity1)
            self.cache.add(self.entity2)
            self.cache.add(self.entity3)

            # Add 4th to evict entity1 to DB
            self.cache.add(self.entity4)

            # Clear cache
            self.cache.clear()

            # Now entity1 should be fetched from DB
            result = self.cache.get(self.entity1)
            self.assertEqual(result, self.entity1)

        except Exception as e:
            self.fail(f"Exception occurred during clear test: {e}")

    def test_eviction_policy(self):
        """Test LRU eviction when cache exceeds max size."""
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
        """Test removing an entity from cache and database."""
        try:
            self.cache.add(self.entity1)
            self.cache.remove(self.entity1)
            result = self.cache.get(self.entity1)
            self.assertIsNone(result)
        except Exception as e:
            self.fail(f"Exception occurred during remove test: {e}")

    def test_removeAll(self):
        """Test removing all entities from cache and database."""
        try:
            self.cache.add(self.entity1)
            self.cache.add(self.entity2)
            self.cache.removeAll()
            self.assertIsNone(self.cache.get(self.entity1))
            self.assertIsNone(self.cache.get(self.entity2))
        except Exception as e:
            self.fail(f"Exception occurred during removeAll test: {e}")


if __name__ == "__main__":
    unittest.main()
