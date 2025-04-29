package cache_service;

import java.util.*;
import java.util.logging.*;
import java.io.IOException;
import java.sql.SQLException;

public class CachingService {
    private static final Logger logger = Logger.getLogger(CachingService.class.getName());
    private final int maxSize;
    private final Map<Integer, Entity> cache;
    // private final SQLiteDatabase database;
    private final Database database;

    // Dependency injection for database to make it easier for mocking
    public CachingService(int maxSize, Database database) {
        this.maxSize = maxSize;
        this.cache = new LinkedHashMap<>(maxSize, 0.75f, true); // LRU behavior
        this.database = database; // Injected database dependency
        logger.info("CachingService initialized with custom Database implementation.");
    }

    public void add(Entity entity) {
        if (entity == null || entity.getId() == null) {
            throw new IllegalArgumentException("Entity or Entity ID cannot be null");
        }

        try {
            if (cache.size() >= maxSize) {
                evictLeastUsed();
            }
            cache.put(entity.getId(), entity);
            logger.info("Added entity " + entity.getId() + " to cache.");
        } catch (Exception e) {
            logger.log(Level.SEVERE, "Error adding entity to cache", e);
        }
    }

    public Entity get(int entityId) {
        try {
            if (cache.containsKey(entityId)) {
                return cache.get(entityId);  // Cache works with Integer as the key
            }
            Entity entity = database.get(entityId);  // Assuming SQLiteDatabase.get() accepts int
            if (entity != null) {
                add(entity);  // Cache it again after fetching from DB
            }
            return entity;
        } catch (Exception e) {
            logger.log(Level.SEVERE, "Error getting entity from cache/database", e);
        }
        return null;
    }

    public void remove(Entity entity) {
        try {
            cache.remove(entity.getId());  // Correct usage of Integer as ID
            database.remove(entity);
            logger.info("Removed entity " + entity.getId() + " from cache and database.");
        } catch (Exception e) {
            logger.log(Level.SEVERE, "Error removing entity", e);
        }
    }

    public void removeAll() {
        try {
            cache.clear();
            database.removeAll();
            logger.info("Removed all entities from cache and database.");
        } catch (Exception e) {
            logger.log(Level.SEVERE, "Error removing all entities", e);
        }
    }

    public void evictLeastUsed() {
        if (!cache.isEmpty()) {
            int evictedId = cache.firstEntry().getKey();  // Handle as Integer key
            Entity evictedEntity = cache.remove(evictedId);
            try {
                database.save(evictedEntity);
                logger.info("Evicted entity " + evictedId + " to database.");
            } catch (Exception e) {
                logger.log(Level.SEVERE, "Error evicting entity", e);
            }
        }
    }

    public List<Integer> getCacheKeys() {
        return new ArrayList<>(cache.keySet());  // List of Integer keys
    }

    public void clear() {
        cache.clear();
        logger.info("Cleared the cache.");
    }
}
