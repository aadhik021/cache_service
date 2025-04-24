package tests;

import cache_service.*;
import org.junit.Before;
import org.junit.After;
import org.junit.Test;
import static org.junit.Assert.*;

import static org.mockito.Mockito.*;
import java.sql.*;


public class TestCachingService {

    private CachingService cache;
    private Entity entity1, entity2, entity3, entity4;
    private Database mockDb;

    @Before
    public void setUp() {
        // Create mock database
        mockDb = mock(Database.class);

        // Initialize the cache with max size of 3 and mock database
        cache = new CachingService(3, mockDb);
        // cache.setDatabase(mockDb);

        entity1 = new Entity(1, "D1");
        entity2 = new Entity(2, "D2");
        entity3 = new Entity(3, "D3");
        entity4 = new Entity(4, "D4");
    }

    @Test
    public void testAddAndGet() {
        cache.add(entity1);
        Entity result = cache.get(entity1.getId());
        assertEquals(entity1, result);
    }

    @Test
    public void testClear() {
        cache.add(entity1);
        cache.add(entity2);
        cache.add(entity3);
        cache.add(entity4);
        cache.clear();

        Entity result1 = cache.get(entity1.getId());
        assertNull(result1);  // entity1 should be evicted to DB
    }

    @Test
    public void testEvictionPolicy() {
        cache.add(entity1);
        cache.add(entity2);
        cache.add(entity3);
        cache.add(entity4); // entity1 should be evicted

        assertFalse(cache.getCacheKeys().contains(entity1.getId()));
    }

    @Test
    public void testRemove() {
        cache.add(entity1);
        cache.remove(entity1);

        Entity result = cache.get(entity1.getId());
        assertNull(result);
    }

    @Test
    public void testRemoveAll() {
        cache.add(entity1);
        cache.add(entity2);
        cache.removeAll();

        assertNull(cache.get(entity1.getId()));
        assertNull(cache.get(entity2.getId()));
    }

    @Test
    public void testGetFromDbWhenNotInCache() throws Exception {
    cache.add(entity1);
    cache.add(entity2);
    cache.add(entity3);
    cache.add(entity4);
    cache.clear();  // simulate DB having entities

    when(mockDb.get(entity1.getId())).thenReturn(entity1);  // Mock DB response
    Entity result = cache.get(entity1.getId());
    assertEquals(entity1, result);
    }

    @Test
    public void testAddEntityWithNullIdRaisesError() throws Exception{
        Entity invalidEntity = new Entity(null, "Null");

        assertThrows(IllegalArgumentException.class, () -> {
            cache.add(invalidEntity);
        });

        verify(mockDb, never()).save(any());
    }


    @Test
    public void testEvictFromEmptyCacheDoesNotCrash() {
        cache.clear();
        cache.evictLeastUsed();  // shouldn't crash even if cache is empty
        assertEquals(0, cache.getCacheKeys().size());
    }

    @Test
    public void testAddDuplicateEntityDoesNotDuplicate() {
        cache.add(entity1);
        cache.add(entity1);  // Adding the same entity again
        assertEquals(1, cache.getCacheKeys().size());  // Only 1 instance should exist
    }

    @Test
    public void testCacheSizeLimitEnforced() {
        cache.add(new Entity(1, "D1"));
        cache.add(new Entity(2, "D2"));
        cache.add(new Entity(3, "D3"));
        cache.add(new Entity(4, "D4"));

        assertEquals(3, cache.getCacheKeys().size());
        assertFalse(cache.getCacheKeys().contains(1));  // entity 1 should be evicted
        assertTrue(cache.getCacheKeys().contains(4));  // entity 4 should be in cache
    }

    @Test
    public void testGetNonExistentEntityReturnsNone() {
        Entity ghostEntity = new Entity(999, "Ghost");
        Entity result = cache.get(ghostEntity.getId());
        assertNull(result);  // Entity doesn't exist in cache or DB
    }

    @Test
    public void testEntityPersistedInDb() throws Exception{
        // Fill cache to trigger eviction of entity1 (LRU)
        cache.add(entity1);
        cache.add(entity2);
        cache.add(entity3);
        cache.add(entity4);  // this will evict entity1

        // Verify that eviction caused the database.save(entity1) call
        verify(mockDb, times(1)).save(entity1);
    }

    @Test
    public void testRemoveAllClearsDatabase() throws Exception {
        cache.add(entity1);
        cache.add(entity2);
        cache.add(entity3);
        cache.add(entity4);
        cache.removeAll();

        verify(mockDb).removeAll();  // entity1 should be removed from DB
        // verify(mockDb).remove(entity2);  // entity2 should be removed from DB
    }

    @Test
    public void testMultipleEntitiesEvictedAndPersistedInDb() throws Exception {
        cache.add(new Entity(1, "D1"));
        cache.add(new Entity(2, "D2"));
        cache.add(new Entity(3, "D3"));
        cache.add(new Entity(4, "D4"));
        cache.add(new Entity(5, "D5"));

         // Both 1 and 2 should have been saved
        verify(mockDb).save(new Entity(1, "D1"));
        verify(mockDb).save(new Entity(2, "D2"));
        // Ensure no save for 3 (still in cache)
        verify(mockDb, never()).save(new Entity(3, "D3"));
    }

    @After
    public void tearDown() throws SQLException {
        // Clear mock DB calls
        reset(mockDb);
    }
}
