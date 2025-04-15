from cache_service.cache import CachingService, Entity
import time


def main():
    print("Starting Caching Service Demo")

    # Initialize the cache with max size 3
    cache = CachingService(max_size=3)

    # Create entities
    e1 = Entity(1, "D1")
    e2 = Entity(2, "D2")
    e3 = Entity(3, "D3")
    e4 = Entity(4, "D4")

    # Add entities to cache
    print("\nAdding entities...")
    cache.add(e1)
    cache.add(e2)
    cache.add(e3)

    print("\nCache full, adding one more to trigger eviction...")
    cache.add(e4)

    print("\nTrying to get evicted entity (should be loaded from DB):")
    retrieved = cache.get(e1)
    print(f"Retrieved: {retrieved}")

    print("\nRemoving entity 2 from cache and DB...")
    cache.remove(e2)
    print(f"Entity 2 after removal: {cache.get(e2)}")

    print("\nClearing cache only (DB remains intact)...")
    cache.clear()
    print(f"Entity 4 (should be fetched from DB): {cache.get(e4)}")

    print("\nRemoving all entities from cache and DB...")
    cache.removeAll()
    print(f"Entity 1 after removeAll: {cache.get(e1)}")


if __name__ == "__main__":
    main()
