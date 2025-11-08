# Cross-Language Data Sharing with Apache Arrow

This scenario demonstrates Apache Arrow's powerful capability to share data seamlessly between different programming languages without serialization overhead.

## Scenario Overview

We'll create a financial dataset in Python, then read and process it in:
- **Python** (data producer)
- **Node.js** (data consumer)
- **Java 25** (data consumer)

All three languages will work with the same Arrow data format, enabling zero-copy data sharing.

## Why This Matters

Traditional data sharing between languages requires:
- Serialization (JSON, CSV, Protocol Buffers)
- Deserialization overhead
- Memory duplication
- Performance penalties

Apache Arrow provides:
- **Zero-copy reads** - No serialization needed
- **Standardized format** - Same memory layout across languages
- **High performance** - Direct memory access
- **Language interoperability** - Share data between Python, R, Java, C++, JavaScript, etc.

## Files in This Scenario

1. `python_producer.py` - Creates financial data and saves to Arrow format
2. `python_consumer.py` - Reads and processes Arrow data in Python
3. `nodejs_consumer.js` - Reads and processes Arrow data in Node.js
4. `java_consumer.java` - Reads and processes Arrow data in Java 25
5. `shared_data.feather` - Arrow data file (Feather format) shared across languages

## Data Format

The shared dataset contains financial trading data:
- `timestamp` - Trade timestamp
- `symbol` - Stock symbol
- `price` - Trade price
- `quantity` - Trade quantity
- `trade_value` - Calculated value (price * quantity)
- `side` - BUY or SELL

## Setup

See [SETUP.md](SETUP.md) for detailed installation instructions for each language.

Quick setup:
- **Python**: Already installed (`pyarrow`)
- **Node.js**: `npm install` (uses apache-arrow@^16.0.0)
- **Java 25**: Requires Maven or manual JAR setup (see SETUP.md)

## Usage

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
npm install  # First time only
node nodejs_consumer.js
```

### Step 4: Consume in Java 25 (Spring Boot)
```bash
# With Spring Boot Maven plugin (recommended):
mvn spring-boot:run

# Or compile and run JAR:
mvn clean package
java --add-opens=java.base/java.nio=org.apache.arrow.memory.core,ALL-UNNAMED \
     --add-opens=java.base/sun.nio.ch=org.apache.arrow.memory.core,ALL-UNNAMED \
     -jar target/apache-arrow-java-consumer-1.0.0.jar

# Or with exec plugin:
mvn clean compile exec:java -Dexec.mainClass="com.example.arrow.ArrowConsumerApplication"

# Optional: Access REST API (if web server is enabled)
curl http://localhost:8080/api/arrow/health
curl http://localhost:8080/api/arrow/analyze
```

### Run All at Once
```bash
bash run_all.sh
```

## Benefits Demonstrated

1. **Zero-Copy**: Data is written once, read by multiple languages without conversion
2. **Performance**: Direct memory access, no serialization overhead
3. **Consistency**: Same data structure across all languages
4. **Scalability**: Works with datasets from MB to TB
5. **Type Safety**: Preserves data types across language boundaries

