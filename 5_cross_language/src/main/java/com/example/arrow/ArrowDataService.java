package com.example.arrow;

import org.apache.arrow.memory.RootAllocator;
import org.apache.arrow.vector.VectorSchemaRoot;
import org.apache.arrow.vector.ipc.ArrowFileReader;
import org.apache.arrow.vector.ipc.SeekableReadChannel;
import org.apache.arrow.vector.Float8Vector;
import org.apache.arrow.vector.VarCharVector;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.channels.FileChannel;
import java.util.HashMap;
import java.util.Map;

/**
 * Service for reading and analyzing Apache Arrow data
 */
@Service
public class ArrowDataService {
    
    private final RootAllocator allocator = new RootAllocator(Long.MAX_VALUE);
    
    /**
     * Analyze Arrow data from a Feather file
     */
    public void analyzeArrowData(String filename) throws IOException {
        System.out.println("\nReading Arrow data from: " + filename);
        
        File file = new File(filename);
        if (!file.exists()) {
            throw new IOException("File not found: " + filename + ". Please run python_producer.py first.");
        }
        
        FileInputStream fileInputStream = new FileInputStream(file);
        FileChannel fileChannel = fileInputStream.getChannel();
        SeekableReadChannel readChannel = new SeekableReadChannel(fileChannel);
        
        try (ArrowFileReader reader = new ArrowFileReader(readChannel, allocator)) {
            VectorSchemaRoot root = reader.getVectorSchemaRoot();
            
            // Load all batches
            while (reader.loadNextBatch()) {
                // Data is loaded into root
            }
            
            long start = System.currentTimeMillis();
            System.out.println("✓ Loaded in: " + ((System.currentTimeMillis() - start) / 1000.0) + " seconds");
            System.out.println("  Rows: " + String.format("%,d", root.getRowCount()));
            System.out.println("  Columns: " + root.getSchema().getFields().size());
            System.out.println("  Schema: " + root.getSchema().toString());
            
            // Perform analysis
            performAnalysis(root);
        } finally {
            fileInputStream.close();
        }
    }
    
    /**
     * Perform comprehensive analysis on the Arrow data
     */
    private void performAnalysis(VectorSchemaRoot root) {
        System.out.println("\n============================================================");
        System.out.println("ANALYSIS USING APACHE ARROW (Spring Boot + Java 25)");
        System.out.println("============================================================");
        
        int rowCount = (int) root.getRowCount();
        
        // Get vectors with proper typing
        Float8Vector priceVector = (Float8Vector) root.getVector("price");
        Float8Vector tradeValueVector = (Float8Vector) root.getVector("trade_value");
        VarCharVector sideVector = (VarCharVector) root.getVector("side");
        VarCharVector symbolVector = (VarCharVector) root.getVector("symbol");
        
        // 1. Total trade value
        analyzeTotalTradeValue(tradeValueVector, rowCount);
        
        // 2. Average price
        analyzeAveragePrice(priceVector, rowCount);
        
        // 3. Buy vs Sell count
        analyzeBuySellRatio(sideVector, rowCount);
        
        // 4. High-value trades
        analyzeHighValueTrades(tradeValueVector, rowCount);
        
        // 5. Price statistics
        analyzePriceStatistics(priceVector, rowCount);
        
        // 6. Trade volume by symbol
        analyzeVolumeBySymbol(symbolVector, tradeValueVector, rowCount);
    }
    
    private void analyzeTotalTradeValue(Float8Vector tradeValueVector, int rowCount) {
        System.out.println("\n1. Total Trade Value");
        System.out.println("------------------------------------------------------------");
        long start = System.currentTimeMillis();
        double totalValue = 0.0;
        for (int i = 0; i < rowCount; i++) {
            totalValue += tradeValueVector.get(i);
        }
        long time = System.currentTimeMillis() - start;
        System.out.printf("  Total: $%,.2f%n", totalValue);
        System.out.println("  Analysis time: " + (time / 1000.0) + " seconds");
    }
    
    private void analyzeAveragePrice(Float8Vector priceVector, int rowCount) {
        System.out.println("\n2. Average Price");
        System.out.println("------------------------------------------------------------");
        long start = System.currentTimeMillis();
        double sumPrice = 0.0;
        for (int i = 0; i < rowCount; i++) {
            sumPrice += priceVector.get(i);
        }
        double avgPrice = sumPrice / rowCount;
        long time = System.currentTimeMillis() - start;
        System.out.printf("  Average: $%.2f%n", avgPrice);
        System.out.println("  Analysis time: " + (time / 1000.0) + " seconds");
    }
    
    private void analyzeBuySellRatio(VarCharVector sideVector, int rowCount) {
        System.out.println("\n3. Buy vs Sell Count");
        System.out.println("------------------------------------------------------------");
        long start = System.currentTimeMillis();
        int buyCount = 0;
        int sellCount = 0;
        for (int i = 0; i < rowCount; i++) {
            String side = new String(sideVector.get(i));
            if ("BUY".equals(side)) {
                buyCount++;
            } else {
                sellCount++;
            }
        }
        long time = System.currentTimeMillis() - start;
        System.out.println("  BUY: " + String.format("%,d", buyCount));
        System.out.println("  SELL: " + String.format("%,d", sellCount));
        System.out.println("  Analysis time: " + (time / 1000.0) + " seconds");
    }
    
    private void analyzeHighValueTrades(Float8Vector tradeValueVector, int rowCount) {
        System.out.println("\n4. High-Value Trades (> $100,000)");
        System.out.println("------------------------------------------------------------");
        long start = System.currentTimeMillis();
        int highValueCount = 0;
        for (int i = 0; i < rowCount; i++) {
            if (tradeValueVector.get(i) > 100000.0) {
                highValueCount++;
            }
        }
        double percentage = (highValueCount * 100.0) / rowCount;
        long time = System.currentTimeMillis() - start;
        System.out.println("  Count: " + String.format("%,d", highValueCount));
        System.out.printf("  Percentage: %.2f%%%n", percentage);
        System.out.println("  Analysis time: " + (time / 1000.0) + " seconds");
    }
    
    private void analyzePriceStatistics(Float8Vector priceVector, int rowCount) {
        System.out.println("\n5. Price Statistics");
        System.out.println("------------------------------------------------------------");
        long start = System.currentTimeMillis();
        double minPrice = Double.MAX_VALUE;
        double maxPrice = Double.MIN_VALUE;
        double sum = 0.0;
        for (int i = 0; i < rowCount; i++) {
            double price = priceVector.get(i);
            if (price < minPrice) minPrice = price;
            if (price > maxPrice) maxPrice = price;
            sum += price;
        }
        double mean = sum / rowCount;
        
        // Calculate standard deviation
        double sumSquaredDiff = 0.0;
        for (int i = 0; i < rowCount; i++) {
            double diff = priceVector.get(i) - mean;
            sumSquaredDiff += diff * diff;
        }
        double stdDev = Math.sqrt(sumSquaredDiff / rowCount);
        
        long time = System.currentTimeMillis() - start;
        System.out.printf("  Min: $%.2f%n", minPrice);
        System.out.printf("  Max: $%.2f%n", maxPrice);
        System.out.printf("  Mean: $%.2f%n", mean);
        System.out.printf("  Std Dev: $%.2f%n", stdDev);
        System.out.println("  Analysis time: " + (time / 1000.0) + " seconds");
    }
    
    private void analyzeVolumeBySymbol(VarCharVector symbolVector, Float8Vector tradeValueVector, int rowCount) {
        System.out.println("\n6. Trade Volume by Symbol");
        System.out.println("------------------------------------------------------------");
        long start = System.currentTimeMillis();
        Map<String, Double> volumeBySymbol = new HashMap<>();
        for (int i = 0; i < rowCount; i++) {
            String symbol = new String(symbolVector.get(i));
            double value = tradeValueVector.get(i);
            volumeBySymbol.put(symbol, volumeBySymbol.getOrDefault(symbol, 0.0) + value);
        }
        
        // Sort by volume
        volumeBySymbol.entrySet().stream()
            .sorted(Map.Entry.<String, Double>comparingByValue().reversed())
            .forEach(entry -> 
                System.out.printf("  %s: $%,.2f%n", entry.getKey(), entry.getValue())
            );
        
        long time = System.currentTimeMillis() - start;
        System.out.println("  Analysis time: " + (time / 1000.0) + " seconds");
    }
}

