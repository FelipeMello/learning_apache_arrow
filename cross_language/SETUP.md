# Setup Instructions for Cross-Language Apache Arrow

## Prerequisites

### Python
- Python 3.12+ (already installed)
- pyarrow: `pip3 install pyarrow --break-system-packages`

### Node.js
- Node.js 22 LTS (already installed)
- Install dependencies: `npm install`

### Java 25
- Java 25 (JDK 25) - already installed
- Maven (optional, for easier dependency management)

## Installation Steps

### 1. Python Setup
```bash
# Already installed, but verify:
python3 -c "import pyarrow; print(f'PyArrow version: {pyarrow.__version__}')"
```

### 2. Node.js Setup
```bash
cd /app/learning/learning_apache_arrow/cross_language
npm install
```

If you get version errors, try:
```bash
npm install apache-arrow@latest
```

### 3. Java 25 Setup

#### Option A: Using Maven (Recommended)
```bash
# Install Maven (if not installed)
# On Ubuntu/Debian:
apt-get update && apt-get install -y maven

# Then compile and run:
cd /app/learning/learning_apache_arrow/cross_language

# First, setup Maven directory structure (if not done)
mkdir -p src/main/java
# Move java_consumer.java to src/main/java/ if it's in the root

# Run with Spring Boot (recommended - much easier!):
mvn spring-boot:run

# Or compile and run as JAR:
mvn clean package
java --add-opens=java.base/java.nio=org.apache.arrow.memory.core,ALL-UNNAMED \
     --add-opens=java.base/sun.nio.ch=org.apache.arrow.memory.core,ALL-UNNAMED \
     -jar target/apache-arrow-java-consumer-1.0.0.jar

# Or with exec plugin:
mvn clean compile exec:java -Dexec.mainClass="com.example.arrow.ArrowConsumerApplication"

# Optional: Access REST API endpoints
curl http://localhost:8080/api/arrow/health
curl http://localhost:8080/api/arrow/analyze
```

#### Option B: Manual Compilation
1. Download Apache Arrow Java JARs:
   ```bash
   # Create lib directory
   mkdir -p lib
   
   # Download Arrow JARs (version 16.0.0)
   wget https://repo1.maven.org/maven2/org/apache/arrow/arrow-vector/16.0.0/arrow-vector-16.0.0.jar -O lib/arrow-vector.jar
   wget https://repo1.maven.org/maven2/org/apache/arrow/arrow-memory-core/16.0.0/arrow-memory-core-16.0.0.jar -O lib/arrow-memory-core.jar
   wget https://repo1.maven.org/maven2/org/apache/arrow/arrow-memory-netty/16.0.0/arrow-memory-netty-16.0.0.jar -O lib/arrow-memory-netty.jar
   ```

2. Compile:
   ```bash
   javac -cp "lib/*" java_consumer.java
   ```

3. Run:
   ```bash
   java -cp ".:lib/*" java_consumer
   ```

## Running the Scenario

### Step 1: Generate Data (Python)
```bash
python3 python_producer.py
```

### Step 2: Consume in Python
```bash
python3 python_consumer.py
```

### Step 3: Consume in Node.js
```bash
node nodejs_consumer.js
```

### Step 4: Consume in Java 25
```bash
# With Maven:
mvn exec:java -Dexec.mainClass="java_consumer"

# Or manually:
java -cp ".:lib/*" java_consumer
```

### Run All at Once
```bash
bash run_all.sh
```

## Troubleshooting

### Python Error: 'DataFrame' object has no attribute 'num_rows'
**Fixed**: Use `feather.read_table()` instead of `feather.read_feather()`

### Node.js Error: "Record batch compression not implemented"
**Solution**: The Feather file was saved with compression. Regenerate it without compression:
```bash
# Remove old file and regenerate
rm shared_data.feather
python3 python_producer.py
```
The producer now saves with `compression='uncompressed'` by default for cross-language compatibility.

### Node.js Error: No matching version found
**Solution**: Update package.json to use a compatible version:
```bash
npm install apache-arrow@latest
```

### Java Error: Maven not found
**Solution**: 
- Install Maven: `apt-get install -y maven`
- Or use manual compilation (see Option B above)

### Java Error: Class not found
**Solution**: Make sure all Arrow JARs are in the classpath

## Verification

After setup, verify each language can read the data:

```bash
# Python
python3 python_consumer.py

# Node.js  
node nodejs_consumer.js

# Java
java -cp ".:lib/*" java_consumer
```

All three should produce similar analysis results from the same `shared_data.feather` file!

