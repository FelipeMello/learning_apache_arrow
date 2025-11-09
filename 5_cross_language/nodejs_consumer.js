/**
 * Node.js Consumer: Reads and processes Arrow data created by python_producer.py
 * Demonstrates zero-copy data access in Node.js
 * 
 * Installation: npm install apache-arrow
 */

const arrow = require('apache-arrow');
const fs = require('fs');

function readArrowData(filename = 'shared_data.feather') {
    console.log(`Reading Arrow data from: ${filename}`);
    
    const start = Date.now();
    const buffer = fs.readFileSync(filename);
    const arrowTable = arrow.tableFromIPC(buffer);
    const readTime = (Date.now() - start) / 1000;
    
    console.log(`✓ Loaded in: ${readTime.toFixed(4)} seconds`);
    console.log(`  Rows: ${arrowTable.numRows.toLocaleString()}`);
    console.log(`  Columns: ${arrowTable.numCols}`);
    console.log(`  Schema:`, arrowTable.schema.toString());
    
    return arrowTable;
}

function analyzeWithArrow(arrowTable) {
    console.log('\n' + '='.repeat(60));
    console.log('ANALYSIS USING APACHE ARROW (Node.js)');
    console.log('='.repeat(60));
    
    // Get columns
    const priceColumn = arrowTable.getChild('price');
    const tradeValueColumn = arrowTable.getChild('trade_value');
    const sideColumn = arrowTable.getChild('side');
    const symbolColumn = arrowTable.getChild('symbol');
    
    const numRows = arrowTable.numRows;
    
    // 1. Total trade value
    console.log('\n1. Total Trade Value');
    console.log('-'.repeat(60));
    const start1 = Date.now();
    let totalValue = 0;
    for (let i = 0; i < numRows; i++) {
        totalValue += tradeValueColumn.get(i);
    }
    const analysisTime1 = (Date.now() - start1) / 1000;
    console.log(`  Total: $${totalValue.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`);
    console.log(`  Analysis time: ${analysisTime1.toFixed(4)} seconds`);
    
    // 2. Average price
    console.log('\n2. Average Price');
    console.log('-'.repeat(60));
    const start2 = Date.now();
    let sumPrice = 0;
    for (let i = 0; i < numRows; i++) {
        sumPrice += priceColumn.get(i);
    }
    const avgPrice = sumPrice / numRows;
    const analysisTime2 = (Date.now() - start2) / 1000;
    console.log(`  Average: $${avgPrice.toFixed(2)}`);
    console.log(`  Analysis time: ${analysisTime2.toFixed(4)} seconds`);
    
    // 3. Buy vs Sell count
    console.log('\n3. Buy vs Sell Count');
    console.log('-'.repeat(60));
    const start3 = Date.now();
    let buyCount = 0;
    let sellCount = 0;
    for (let i = 0; i < numRows; i++) {
        if (sideColumn.get(i) === 'BUY') {
            buyCount++;
        } else {
            sellCount++;
        }
    }
    const analysisTime3 = (Date.now() - start3) / 1000;
    console.log(`  BUY: ${buyCount.toLocaleString()}`);
    console.log(`  SELL: ${sellCount.toLocaleString()}`);
    console.log(`  Analysis time: ${analysisTime3.toFixed(4)} seconds`);
    
    // 4. High-value trades (> $100,000)
    console.log('\n4. High-Value Trades (> $100,000)');
    console.log('-'.repeat(60));
    const start4 = Date.now();
    let highValueCount = 0;
    for (let i = 0; i < numRows; i++) {
        if (tradeValueColumn.get(i) > 100000) {
            highValueCount++;
        }
    }
    const percentage = (highValueCount / numRows * 100).toFixed(2);
    const analysisTime4 = (Date.now() - start4) / 1000;
    console.log(`  Count: ${highValueCount.toLocaleString()}`);
    console.log(`  Percentage: ${percentage}%`);
    console.log(`  Analysis time: ${analysisTime4.toFixed(4)} seconds`);
    
    // 5. Price statistics
    console.log('\n5. Price Statistics');
    console.log('-'.repeat(60));
    const start5 = Date.now();
    let minPrice = Infinity;
    let maxPrice = -Infinity;
    let sum = 0;
    for (let i = 0; i < numRows; i++) {
        const price = priceColumn.get(i);
        if (price < minPrice) minPrice = price;
        if (price > maxPrice) maxPrice = price;
        sum += price;
    }
    const mean = sum / numRows;
    
    // Calculate standard deviation
    let sumSquaredDiff = 0;
    for (let i = 0; i < numRows; i++) {
        const diff = priceColumn.get(i) - mean;
        sumSquaredDiff += diff * diff;
    }
    const stdDev = Math.sqrt(sumSquaredDiff / numRows);
    
    const analysisTime5 = (Date.now() - start5) / 1000;
    console.log(`  Min: $${minPrice.toFixed(2)}`);
    console.log(`  Max: $${maxPrice.toFixed(2)}`);
    console.log(`  Mean: $${mean.toFixed(2)}`);
    console.log(`  Std Dev: $${stdDev.toFixed(2)}`);
    console.log(`  Analysis time: ${analysisTime5.toFixed(4)} seconds`);
    
    // 6. Trade volume by symbol
    console.log('\n6. Trade Volume by Symbol');
    console.log('-'.repeat(60));
    const start6 = Date.now();
    const volumeBySymbol = {};
    for (let i = 0; i < arrowTable.length; i++) {
        const symbol = symbolColumn.get(i);
        const value = tradeValueColumn.get(i);
        if (!volumeBySymbol[symbol]) {
            volumeBySymbol[symbol] = 0;
        }
        volumeBySymbol[symbol] += value;
    }
    
    // Sort by volume
    const sortedSymbols = Object.entries(volumeBySymbol)
        .sort((a, b) => b[1] - a[1]);
    
    const analysisTime6 = (Date.now() - start6) / 1000;
    for (const [symbol, volume] of sortedSymbols) {
        console.log(`  ${symbol}: $${volume.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`);
    }
    console.log(`  Analysis time: ${analysisTime6.toFixed(4)} seconds`);
}

if (require.main === module) {
    console.log('='.repeat(60));
    console.log('NODE.JS CONSUMER: Reading Shared Arrow Data');
    console.log('='.repeat(60));
    
    try {
        // Read Arrow data
        const arrowTable = readArrowData('shared_data.feather');
        
        // Analyze data
        analyzeWithArrow(arrowTable);
        
        console.log('\n' + '='.repeat(60));
        console.log('✓ Node.js analysis complete!');
        console.log('='.repeat(60));
        console.log('\nThis demonstrates:');
        console.log('  - Zero-copy data reading from Python-generated Arrow file');
        console.log('  - Same data structure accessible in Node.js');
        console.log('  - No serialization/deserialization overhead');
    } catch (error) {
        console.error('Error:', error.message);
        console.log('\nMake sure to:');
        console.log('  1. Run python_producer.py first to create shared_data.feather');
        console.log('  2. Install apache-arrow: npm install apache-arrow');
    }
}

