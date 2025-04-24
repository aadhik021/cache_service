# Caching Service

A Python-based caching service implementing an LRU (Least Recently Used) strategy with SQLite-backed persistence.

## Features

- LRU cache using `OrderedDict`
- Configurable cache size
- SQLite-based simulated database (`SQLDatabase`)
- Automatic eviction and DB persistence
- Fallback to DB on cache miss
- Separate methods for cache clear vs full deletion
- Robust exception handling
- Comprehensive unit tests

## APIs

- `add(entity)` - Add entity to cache, evict LRU if cache is full
- `get(entity)` - Get entity from cache or DB
- `remove(entity)` - Remove entity from cache and DB
- `removeAll()` - Clear all entities from cache and DB
- `clear()` - Clear only the cache

---

## Testing
Unit tests are defined in TestCachingService and cover:

✅ Entity addition and retrieval: Verifies correct caching and retrieval behavior.
✅ LRU eviction enforcement: Validates the eviction of the least recently used (LRU) entities.
✅ Removal from cache and database: Ensures that removal actions clear both cache and database.
✅ Cache clearing vs full wipe: Compares clearing the cache to fully wiping both the cache and database, ensuring that entities are properly evicted and cleared.
✅ Fallback to DB on cache miss: Verifies that entities, once evicted or removed from cache, can still be retrieved from the database.
✅ Handling of invalid inputs: Includes tests for invalid entity additions (e.g., None ID).
✅ Edge cases: Addresses scenarios like duplicate entity addition, eviction from an empty cache, and retrieval of non-existent entities.
✅ Eviction and persistence in the database: Confirms that evicted entities are correctly persisted in the database after cache overflow.
✅ Full cache removal (removeAll): Ensures removeAll clears both the cache and the database when entities are evicted to the database.

## Requirements

- Python 3.8 or above

---

## How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/aadhik021/cache_service.git
   cd cache_service

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate     # On Windows: venv\Scripts\activate

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt

4. **Run main demo**
    ```bash
    python main.py

5. **Run all unit tests**
    ```bash
    python -m unittest tests/test_cache.py




