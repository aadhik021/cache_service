package cache_service;

import java.util.Objects;

public class Entity {
    private Integer id;  // Use Integer instead of String
    private Object data;

    public Entity(Integer id, Object data) {  // Change String to Integer
        this.id = id;
        this.data = data;
    }

    public Integer getId() {  // Change return type to Integer
        return id;
    }

    public Object getData() {
        return data;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Entity entity = (Entity) o;
        return Objects.equals(id, entity.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    @Override
    public String toString() {
        return "Entity{id=" + id + ", data=" + data + "}";  // Changed id to Integer
    }
}
