#!/bin/bash
# Regenerate data file without compression for cross-language compatibility

cd "$(dirname "$0")"

echo "Regenerating data file without compression..."
echo "This ensures compatibility with Node.js Apache Arrow library"

# Remove old file if it exists
if [ -f "shared_data.feather" ]; then
    echo "Removing old compressed file..."
    rm shared_data.feather
fi

# Regenerate with uncompressed format
python3 python_producer.py

echo ""
echo "✓ Data file regenerated without compression"
echo "Now Node.js consumer should work:"
echo "  node nodejs_consumer.js"

