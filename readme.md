# Caching Service

A simple Python-based caching service using LRU (Least Recently Used) strategy and a simulated database.

---

## Features

- LRU caching using `OrderedDict`
- Configurable maximum size for cache
- Eviction of least-used entries to simulated database
- Simulated database for persistence
- Logging with timestamps and source
- Exception handling in all operations

---

## APIs

- `add(entity)` - Add entity to cache, evict LRU if cache is full
- `get(entity)` - Get entity from cache or DB
- `remove(entity)` - Remove entity from cache and DB
- `removeAll()` - Clear all entities from cache and DB
- `clear()` - Clear only the cache

---

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




