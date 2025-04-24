# cache_service/cache.py
import logging
from collections import OrderedDict
import sqlite3
import os
from config import DB_PATH
import json

# Configure logging
logger = logging.getLogger("CachingService")
logger.setLevel(logging.INFO)

# Console Handler
ch = logging.StreamHandler()
ch_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(ch_formatter)
logger.addHandler(ch)

# File Handler
fh = logging.FileHandler("caching_service.log")
fh.setFormatter(ch_formatter)
logger.addHandler(fh)


class Entity:
    """Simulates an entity with a unique ID."""

    def __init__(self, entity_id, data):
        self.entity_id = entity_id
        self.data = data

    def getId(self):
        return self.entity_id

    def __eq__(self, other):
        return isinstance(other, Entity) and self.entity_id == other.entity_id

    def __hash__(self):
        return hash(self.entity_id)

    def __repr__(self):
        return f"Entity(id={self.entity_id}, data={self.data})"


class SQLiteDatabase:
    """SQLite-based database for entity storage."""

    def __init__(self):
        db_dir = os.path.dirname(DB_PATH)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        self.connection = sqlite3.connect(DB_PATH)
        self._create_table()

    def _connect(self):
        return sqlite3.connect(DB_PATH)

    def _create_table(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS entities (
                    id TEXT PRIMARY KEY,
                    data TEXT
                )
            """
            )
            conn.commit()

    def save(self, entity):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "REPLACE INTO entities (id, data) VALUES (?, ?)",
                    (entity.getId(), json.dumps(entity.data)),
                )
                conn.commit()
        except Exception as e:
            logger.error(f"Error saving entity {entity.getId()} to SQLite DB: {e}")
            raise

    def get(self, entity_id):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT data FROM entities WHERE id = ?", (entity_id,))
                row = cursor.fetchone()
                if row:
                    data = json.loads(row[0])
                    return Entity(entity_id, data)
                return None
        except Exception as e:
            logger.error(f"Error getting entity {entity_id} from SQLite DB: {e}")
            raise

    def remove(self, entity):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM entities WHERE id = ?", (entity.getId(),))
                conn.commit()
        except Exception as e:
            logger.error(f"Error removing entity {entity.getId()} from SQLite DB: {e}")
            raise

    def removeAll(self):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM entities")
                conn.commit()
        except Exception as e:
            logger.error("Error removing all entities from SQLite DB: {e}")
            raise


class CachingService:
    """
    Caching service with LRU eviction and database integration.

    Methods:
        add(entity): Adds entity to the cache. Evicts LRU if over capacity.
        remove(entity): Removes entity from cache and database.
        removeAll(): Clears cache and database.
        get(entity): Retrieves entity from cache or loads from database.
        clear(): Clears cache only.
    """

    def __init__(self, max_size):
        self._max_size = max_size
        self._cache = OrderedDict()
        self._database = SQLiteDatabase()

    def get_cache_keys(self):
        return list(self._cache.keys())

    def evict_least_used(self):
        """Evict the least recently used (LRU) entity from the cache."""
        if self._cache:
            lru_entity_id, lru_entity = self._cache.popitem(last=False)
            self._database.save(lru_entity)
            logger.info(f"Evicted entity {lru_entity_id} to database.")
        else:
            logger.info("Cache is empty, nothing to evict.")

    def add(self, entity):
        try:
            entity_id = entity.getId()
            if entity_id is None:
                raise ValueError("Entity ID cannot be None")

            if entity_id in self._cache:
                self._cache.move_to_end(entity_id)
                self._cache[entity_id] = entity
            else:
                if len(self._cache) >= self._max_size:
                    self.evict_least_used()

                self._cache[entity_id] = entity

            logger.info(f"Added entity {entity_id} to cache.")
        except Exception as e:
            logger.error(f"Error adding entity {entity.getId()} to cache: {e}")
            raise

    def remove(self, entity):
        try:
            entity_id = entity.getId()
            self._cache.pop(entity_id, None)
            self._database.remove(entity)
            logger.info(f"Removed entity {entity_id} from cache and database.")
        except Exception as e:
            logger.error(
                f"Error removing entity {entity.getId()} from cache and database: {e}"
            )
            raise

    def removeAll(self):
        try:
            self._cache.clear()
            self._database.removeAll()
            logger.info("Removed all entities from cache and database.")
        except Exception as e:
            logger.error(f"Error removing all entities from cache and database: {e}")
            raise

    def get(self, entity):
        try:
            entity_id = entity.getId()
            if entity_id in self._cache:
                self._cache.move_to_end(entity_id)
                logger.info(f"Retrieved entity {entity_id} from cache.")
                return self._cache[entity_id]
            else:
                retrieved_entity = self._database.get(entity_id)
                if retrieved_entity:
                    self.add(retrieved_entity)
                    logger.info(f"Retrieved entity {entity_id} from database.")
                    return retrieved_entity
                else:
                    return None
        except Exception as e:
            logger.error(f"Error getting entity {entity.getId()}: {e}")
            raise

    def clear(self):
        try:
            self._cache.clear()
            logger.info("Cleared the cache.")
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            raise
