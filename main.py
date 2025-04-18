import time
from cache_service.cache import CachingService, Entity


def add_entities_to_cache(cache, entities):
    """Helper function to add multiple entities to cache."""
    for entity in entities:
        cache.add(entity)
        print(f"Added: {entity}")


def main():
    print("Starting Caching Service Demo")

    cache = CachingService(max_size=3)

    e1 = Entity(1, "D1")
    e2 = Entity(2, "D2")
    e3 = Entity(3, "D3")
    e4 = Entity(4, "D4")

    try:
        print("\nAdding entities...")
        add_entities_to_cache(cache, [e1, e2, e3])

        print("\nCache full, adding one more to trigger eviction...")
        cache.add(e4)

        print("\nCache after eviction:", cache.get_cache_keys())

        print("\nAdding duplicate entity with same ID...")
        cache.add(e1)
        print(f"Cache after adding duplicate entity: {cache.get_cache_keys()}")

        # Test for cache overflow
        print("\nFilling cache to maximum size...")
        cache.add(Entity(1, "D1"))
        cache.add(Entity(2, "D2"))
        cache.add(Entity(3, "D3"))
        print(f"Cache size: {len(cache.get_cache_keys())}")
        cache.add(Entity(4, "D4"))
        print(f"Cache size after overflow: {len(cache.get_cache_keys())}")

        # Test eviction after multiple additions
        print("\nEviction mechanism demonstration...")
        cache.add(Entity(1, "D1"))
        cache.add(Entity(2, "D2"))
        cache.add(Entity(3, "D3"))
        cache.add(Entity(4, "D4"))
        print(f"Cache after eviction: {cache.get_cache_keys()}")

        # Clearing and fetching from DB
        print("\nClearing cache and fetching from DB...")
        cache.clear()
        result = cache.get(e1)
        print(f"Entity 1 after clearing cache (should come from DB): {result}")

        # Adding invalid entity
        print("\nAdding invalid entity with None ID...")
        try:
            cache.add(Entity(None, "Invalid"))
        except ValueError as ve:
            print(f"Error: {ve}")

        # Test removing and fetching removed entity
        print("\nTrying to fetch removed entity (should be None)...")
        cache.remove(e3)
        print(f"Entity 3 after removal: {cache.get(e3)}")

        # Test for non-cached entity
        print("\nTrying to fetch non-existing entity (should return None):")
        non_existing = cache.get(Entity(999, "Ghost"))
        print(f"Non-existing entity: {non_existing}")

        # Test for removeAll
        print("\nRemoving all entities from cache and DB...")
        cache.removeAll()
        print(f"Entity 1 after removeAll: {cache.get(e1)}")
        print(f"Entity 2 after removeAll: {cache.get(e2)}")

        # Test for eviction from empty cache
        print("\nEvicting from empty cache (should not throw error)...")
        cache.clear()
        cache.evict_least_used()
        print("Eviction completed without errors.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
