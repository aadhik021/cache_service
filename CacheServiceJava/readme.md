# Java Caching Service with LRU Eviction 

This project demonstrates a caching service with LRU eviction, utilizing SQLite for persistence. It also includes unit tests to validate the cache behavior, eviction policy, and interactions with a mock database for testing purposes.

## Features:
- `CachingService` core class with LRU eviction and CRUD operations.
- `Entity` class to represent cacheable objects.
- `Database` interface for backend abstraction.
- `SQLiteDatabase` class (optional) for persistence using JDBC.
- Unit tests using JUnit and Mockito.
- Configurable via environment variables using `dotenv-java`.
---

## 📁 Project Structure

```
CacheServiceJava/
├── .vscode/
├── bin/                    # Compiled class files output directory
├── db/                     # SQLite database files (optional)
├── lib/                    # External JARs (e.g., SQLite JDBC, Mockito, JUnit)
├── mockito-extensions/     # Mockito configuration
│   └── org.mockito.plugins.MockMaker
├── src/
│   └── cache_service/
│       ├── CachingService.java
│       ├── Database.java
│       ├── Entity.java
│       └── SQLiteDatabase.java
├── config/Config.java
├── main/Main.java
├── tests/TestCachingService.java
└── .env                    # Environment configurations
```
## 🛠️ Compile and Run Java Project (Without Maven)

This guide explains how to compile and run your Java application and unit tests using the command line with dependencies managed manually via the `lib/` folder.

---

### 🔹 Step 1: Create `sources.txt`

Use the following command (Windows-specific `dir` version):

```bat
dir /s /b src\*.java > sources.txt
```

This recursively finds all `.java` files and lists them in `sources.txt`.

---

### 🔹 Step 2: Compile All Source Files

Compile everything (main + tests) using:

```bat
javac -cp "lib/*" -d bin @sources.txt
```

**Explanation:**
- `-cp "lib/*"` includes all required JARs.
- `-d bin` outputs compiled classes to the `bin/` directory.
- `@sources.txt` provides a list of all `.java` source files.

---

### 🔹 Step 3: Run the Main Class

Run the compiled application:

```bat
java -cp ".;bin;lib/*" main.Main
```

> 🔸 Replace `main.Main` with your actual fully qualified class name (package + class name).

---

### 🔹 Step 4: Compile Individual Test File (Optional)

If you want to compile the test class separately:

```bat
javac -cp "lib/*;bin" -d bin src\tests\TestCachingService.java
```

---

### 🔹 Step 5: Run JUnit Test

```bat
java -cp "lib/*;bin" org.junit.runner.JUnitCore tests.TestCachingService
```

> 🔸 Replace `tests.TestCachingService` with your actual test class’s fully qualified name if different.

---

### ✅ Notes

- Use `";"` as the classpath separator on **Windows**. Use `":"` on **Linux/macOS**.
- Make sure the `bin/` directory exists before running these commands. You can create it using:

```bat
mkdir bin
```
