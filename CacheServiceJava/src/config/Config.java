package config;

import java.io.IOException;
import java.nio.file.Paths;
import io.github.cdimascio.dotenv.Dotenv;

public class Config {
    private static final Dotenv dotenv = Dotenv.load();
    
    // Get the DB_PATH from the environment variables
    public static String getDBPath() {
        return dotenv.get("DB_PATH"); // Default to ./db/entity_cache.db if not found
    }
}