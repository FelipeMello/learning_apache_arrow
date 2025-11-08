# Spring Boot Integration Guide

## Java Version Compatibility

**Important**: This project is compiled for **Java 21** for Spring Boot compatibility, but can run on **Java 25** runtime. Spring Boot 3.4.0 doesn't yet support Java 25 class files (version 69), so we compile with Java 21 target while using Java 25 features at runtime.

## Why Spring Boot?

Spring Boot makes the Java consumer much easier to work with:

✅ **Automatic Dependency Management** - No manual JAR management  
✅ **Configuration Management** - Easy property-based configuration  
✅ **Dependency Injection** - Clean, testable code structure  
✅ **Auto-Configuration** - JVM arguments handled automatically  
✅ **REST API Support** - Optional web endpoints for analysis  
✅ **Better Error Handling** - Spring's exception handling  
✅ **Production Ready** - Easy to package as executable JAR  

## Project Structure

```
src/main/java/com/example/arrow/
├── ArrowConsumerApplication.java    # Main Spring Boot application
├── ArrowDataService.java            # Service for Arrow data analysis
└── ArrowDataController.java        # REST API controller (optional)

src/main/resources/
└── application.properties           # Spring Boot configuration
```

## Running the Application

### Option 1: Spring Boot Maven Plugin (Easiest)
```bash
mvn spring-boot:run
```

### Option 2: Executable JAR
```bash
# Build
mvn clean package

# Run
java --add-opens=java.base/java.nio=org.apache.arrow.memory.core,ALL-UNNAMED \
     --add-opens=java.base/sun.nio.ch=org.apache.arrow.memory.core,ALL-UNNAMED \
     -jar target/apache-arrow-java-consumer-1.0.0.jar
```

### Option 3: Exec Plugin
```bash
mvn clean compile exec:java -Dexec.mainClass="com.example.arrow.ArrowConsumerApplication"
```

## Configuration

Edit `src/main/resources/application.properties`:

```properties
# Arrow data file location
arrow.data.file=shared_data.feather

# Server port (if using web endpoints)
server.port=8080

# Logging
logging.level.com.example.arrow=INFO
```

## REST API Endpoints (Optional)

If you want to use the REST API, the web server will start on port 8080:

### Health Check
```bash
curl http://localhost:8080/api/arrow/health
```

Response:
```json
{
  "status": "UP",
  "service": "Apache Arrow Consumer",
  "framework": "Spring Boot",
  "java_version": "25"
}
```

### Analyze Data
```bash
curl http://localhost:8080/api/arrow/analyze?filename=shared_data.feather
```

## Benefits Over Plain Java

| Feature | Plain Java | Spring Boot |
|---------|-----------|-------------|
| Dependency Management | Manual JARs | Maven/Gradle |
| Configuration | Hard-coded | Properties files |
| Code Structure | Monolithic | Layered (Service/Controller) |
| Error Handling | Try-catch everywhere | @ExceptionHandler |
| Testing | Manual setup | @SpringBootTest |
| Packaging | Manual classpath | Executable JAR |
| JVM Arguments | Manual | Auto-configured |

## Key Components

### ArrowConsumerApplication
Main Spring Boot application class. Uses `CommandLineRunner` to automatically run analysis on startup.

### ArrowDataService
Service layer that handles all Arrow data operations:
- Reading Feather files
- Performing analytics
- Type-safe vector access

### ArrowDataController (Optional)
REST controller providing HTTP endpoints for:
- Health checks
- Data analysis triggers

## Customization

### Add More Analysis Methods
Extend `ArrowDataService` with new methods:

```java
public void analyzeCustomMetric(VectorSchemaRoot root) {
    // Your custom analysis
}
```

### Add Configuration Properties
In `application.properties`:
```properties
arrow.analysis.threshold=100000
arrow.analysis.enable-detailed-stats=true
```

Access in service:
```java
@Value("${arrow.analysis.threshold}")
private double threshold;
```

### Disable Web Server
If you don't need REST API, remove `spring-boot-starter-web` dependency.

## Troubleshooting

### JVM Arguments Not Applied
Spring Boot Maven plugin should handle this automatically. If not, check `pom.xml` configuration.

### Port Already in Use
Change port in `application.properties`:
```properties
server.port=8081
```

### File Not Found
Ensure `shared_data.feather` exists in the working directory, or specify full path in `application.properties`.

## Next Steps

- Add more REST endpoints for specific analytics
- Add caching with Spring Cache
- Add metrics with Micrometer
- Add database persistence
- Add async processing with @Async

