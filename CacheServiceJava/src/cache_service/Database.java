package cache_service;

import java.sql.SQLException;

public interface Database {
    void save(Entity e) throws Exception;
    Entity get(int id) throws Exception;
    void remove(Entity e) throws Exception;
    void removeAll() throws Exception;
}
