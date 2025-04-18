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

✅ Entity addition and retrieval
✅ LRU eviction enforcement
✅ Removal from cache and database
✅ Cache clearing vs full wipe
✅ Fallback to DB on cache miss
✅ Handling of invalid inputs
✅ Edge cases like duplicate addition, empty eviction, or non-existent retrieval

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




