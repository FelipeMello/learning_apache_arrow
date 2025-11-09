#!/bin/bash
# Script to run the complete cross-language Apache Arrow scenario

echo "============================================================"
echo "APACHE ARROW CROSS-LANGUAGE DATA SHARING DEMONSTRATION"
echo "============================================================"

cd "$(dirname "$0")"

# Step 1: Generate data in Python
echo -e "\n[STEP 1] Generating data in Python..."
python3 python_producer.py

if [ $? -ne 0 ]; then
    echo "Error: Failed to generate data"
    exit 1
fi

# Step 2: Consume in Python
echo -e "\n[STEP 2] Consuming data in Python..."
python3 python_consumer.py

# Step 3: Consume in Node.js
echo -e "\n[STEP 3] Consuming data in Node.js..."
if command -v node &> /dev/null; then
    if [ ! -d "node_modules" ]; then
        echo "Installing Node.js dependencies..."
        npm install
    fi
    node nodejs_consumer.js
else
    echo "Node.js not found. Skipping Node.js consumer."
fi

# Step 4: Consume in Java 25
echo -e "\n[STEP 4] Consuming data in Java 25..."
if command -v javac &> /dev/null && command -v java &> /dev/null; then
    JAVA_VERSION=$(java -version 2>&1 | head -n 1 | cut -d'"' -f2 | cut -d'.' -f1)
    if [ "$JAVA_VERSION" -ge 25 ]; then
        if command -v mvn &> /dev/null; then
            echo "Compiling with Maven..."
            mvn clean compile exec:java -Dexec.mainClass="java_consumer"
        else
            echo "Maven not found. Please compile manually:"
            echo "  javac -cp 'arrow-*.jar' java_consumer.java"
            echo "  java -cp '.:arrow-*.jar' java_consumer"
        fi
    else
        echo "Java 25 not found. Current version: $JAVA_VERSION"
        echo "Please use Java 25 (JDK 25) to run the Java consumer."
    fi
else
    echo "Java not found. Skipping Java consumer."
fi

echo -e "\n============================================================"
echo "DEMONSTRATION COMPLETE"
echo "============================================================"
echo ""
echo "This demonstrates Apache Arrow's cross-language capabilities:"
echo "  ✓ Zero-copy data sharing"
echo "  ✓ No serialization overhead"
echo "  ✓ Same data structure across languages"
echo "  ✓ High performance analytics"
echo ""

