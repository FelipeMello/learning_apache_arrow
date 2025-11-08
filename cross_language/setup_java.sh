#!/bin/bash
# Setup Java source directory for Maven

cd "$(dirname "$0")"

echo "Setting up Maven directory structure..."

# Create Maven source directory
mkdir -p src/main/java

# Move Java file to correct location
if [ -f "java_consumer.java" ]; then
    mv java_consumer.java src/main/java/
    echo "✓ Moved java_consumer.java to src/main/java/"
else
    echo "⚠ java_consumer.java not found in current directory"
fi

echo "✓ Maven directory structure ready"
echo ""
echo "Now you can run:"
echo "  mvn clean compile exec:java -Dexec.mainClass=\"java_consumer\""

