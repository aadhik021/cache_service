package cache_service;

import java.sql.*;
import java.io.File;
import java.io.IOException;
import java.util.logging.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import config.Config;

public class SQLiteDatabase implements Database {
    private static final Logger logger = Logger.getLogger(SQLiteDatabase.class.getName());
    private final String dbPath;
    private final Connection connection;

    public SQLiteDatabase() throws SQLException, IOException {
        this.dbPath = Config.getDBPath();
        if (dbPath == null || dbPath.isEmpty()) {
            throw new IllegalArgumentException("DB_PATH is not set in the .env file.");
        }

        File dbFile = new File(dbPath);
        File dbDir  = dbFile.getParentFile();
        if (dbDir != null && !dbDir.exists() && dbDir.mkdirs()) {
            logger.info("Created database directory: " + dbDir.getAbsolutePath());
        }

        this.connection = DriverManager.getConnection("jdbc:sqlite:" + dbPath);
        createTable();
    }

    private void createTable() throws SQLException {
        String sql = "CREATE TABLE IF NOT EXISTS entities ("
                   + "id INTEGER PRIMARY KEY,"
                   + "data TEXT)";
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
        }
    }

    @Override
    public void save(Entity entity) throws Exception {
        String sql = "REPLACE INTO entities (id, data) VALUES (?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setInt(1, entity.getId());
            String json = new ObjectMapper().writeValueAsString(entity.getData());
            stmt.setString(2, json);
            stmt.executeUpdate();
        } catch (com.fasterxml.jackson.core.JsonProcessingException e) {
            logger.log(Level.SEVERE, "Failed to serialize entity data", e);
            throw new SQLException("Serialization error", e);
        }
    }

    @Override
    public Entity get(int entityId) throws Exception {
        String sql = "SELECT data FROM entities WHERE id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setInt(1, entityId);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    String json = rs.getString("data");
                    Object data = new ObjectMapper().readValue(json, Object.class);
                    return new Entity(entityId, data);
                }
            }
        } catch (IOException e) {
            logger.log(Level.SEVERE, "Failed to deserialize entity data", e);
            throw new SQLException("Deserialization error", e);
        }
        return null;
    }

    @Override
    public void remove(Entity entity) throws Exception {
        String sql = "DELETE FROM entities WHERE id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setInt(1, entity.getId());
            stmt.executeUpdate();
        }
    }

    @Override
    public void removeAll() throws Exception {
        try (Statement stmt = connection.createStatement()) {
            stmt.executeUpdate("DELETE FROM entities");
        }
    }
}
