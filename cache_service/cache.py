# cache_service/cache.py
import logging
from collections import OrderedDict

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


class SimulatedDatabase:
    """Simulates a database for entity storage."""

    def __init__(self):
        self._data = {}

    def save(self, entity):
        try:
            self._data[entity.getId()] = entity
        except Exception as e:
            logger.error(f"Error saving entity {entity.getId()} to database: {e}")
            raise

    def get(self, entity_id):
        try:
            return self._data.get(entity_id)
        except Exception as e:
            logger.error(f"Error getting entity {entity_id} from database: {e}")
            raise

    def remove(self, entity):
        try:
            self._data.pop(entity.getId(), None)
        except Exception as e:
            logger.error(f"Error removing entity {entity.getId()} from database: {e}")
            raise

    def removeAll(self):
        try:
            self._data.clear()
        except Exception as e:
            logger.error(f"Error removing all entities from database: {e}")
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
        self._database = SimulatedDatabase()

    def add(self, entity):
        try:
            entity_id = entity.getId()
            if entity_id in self._cache:
                self._cache.move_to_end(entity_id)
                self._cache[entity_id] = entity
            else:
                if len(self._cache) >= self._max_size:
                    lru_entity_id, lru_entity = self._cache.popitem(last=False)
                    self._database.save(lru_entity)
                    logger.info(f"Evicted entity {lru_entity_id} to database.")
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
