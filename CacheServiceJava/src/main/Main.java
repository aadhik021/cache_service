package main;

import cache_service.*;
import java.util.logging.*;
import static org.mockito.Mockito.*;

public class Main {
    private static final Logger logger = Logger.getLogger(Main.class.getName());

    public static void main(String[] args) {
        try {
            System.out.println("Starting Caching Service Demo with Mocked DB");

            // Mock the Database interface
            Database mockDb = mock(Database.class);

            // Inject the mock into CachingService
            CachingService cache = new CachingService(3, mockDb);

            Entity e1 = new Entity(1, "D1");
            Entity e2 = new Entity(2, "D2");
            Entity e3 = new Entity(3, "D3");
            Entity e4 = new Entity(4, "D4");

            System.out.println("\nAdding entities...");
            cache.add(e1);
            cache.add(e2);
            cache.add(e3);

            System.out.println("\nCache full, adding one more to trigger eviction...");
            cache.add(e4);

            System.out.println("\nCache after eviction: " + cache.getCacheKeys());

            System.out.println("\nAdding duplicate entity with same ID...");
            cache.add(e1);
            System.out.println("Cache after adding duplicate entity: " + cache.getCacheKeys());

            // Demonstrate eviction again
            System.out.println("\nEviction mechanism demonstration...");
            cache.add(new Entity(1, "D1"));
            cache.add(new Entity(2, "D2"));
            cache.add(new Entity(3, "D3"));
            cache.add(new Entity(4, "D4"));
            System.out.println("Cache after eviction: " + cache.getCacheKeys());

            // Now clear and simulate DB fetch
            System.out.println("\nClearing cache and fetching from DB...");
            cache.clear();
            when(mockDb.get(1)).thenReturn(e1);  // stub the mock
            Entity result = cache.get(1);
            System.out.println("Entity 1 after clearing cache (should come from DB): " + result);

        } catch (Exception e) {
            logger.log(Level.SEVERE, "An error occurred", e);
        }
    }
}
