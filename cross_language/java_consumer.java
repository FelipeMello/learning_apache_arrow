/**
 * Java 25 Consumer: Reads and processes Arrow data created by python_producer.py
 * Demonstrates zero-copy data access in Java 25
 * 
 * Compilation:
 *   javac -cp ".:arrow-vector-*.jar:arrow-memory-*.jar:arrow-format-*.jar" java_consumer.java
 * 
 * Execution:
 *   java -cp ".:arrow-vector-*.jar:arrow-memory-*.jar:arrow-format-*.jar" java_consumer
 * 
 * Dependencies (Maven):
 *   <dependency>
 *     <groupId>org.apache.arrow</groupId>
 *     <artifactId>arrow-vector</artifactId>
 *     <version>16.0.0</version>
 *   </dependency>
 */

import org.apache.arrow.memory.RootAllocator;
import org.apache.arrow.vector.VectorSchemaRoot;
import org.apache.arrow.vector.ipc.ArrowFileReader;
import org.apache.arrow.vector.ipc.SeekableReadChannel;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.channels.FileChannel;
import java.util.HashMap;
import java.util.Map;

public class java_consumer {
    
    private static RootAllocator allocator = new RootAllocator(Long.MAX_VALUE);
    
    public static void main(String[] args) {
        System.out.println("============================================================");
        System.out.println("JAVA 25 CONSUMER: Reading Shared Arrow Data");
        System.out.println("============================================================");
        
        String filename = "shared_data.feather";
        
        try {
            // Read Arrow data (returns reader and root)
            ArrowFileReader reader = readArrowData(filename);
            VectorSchemaRoot root = reader.getVectorSchemaRoot();
            
            // Analyze data
            analyzeWithArrow(root);
            
            // Clean up
            reader.close();
            root.close();
            allocator.close();
            
            System.out.println("\n============================================================");
            System.out.println("✓ Java 25 analysis complete!");
            System.out.println("============================================================");
            System.out.println("\nThis demonstrates:");
            System.out.println("  - Zero-copy data reading from Python-generated Arrow file");
            System.out.println("  - Same data structure accessible in Java 25");
            System.out.println("  - No serialization/deserialization overhead");
            System.out.println("  - Type-safe access to Arrow data");
            
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
            System.out.println("\nMake sure to:");
            System.out.println("  1. Run python_producer.py first to create shared_data.feather");
            System.out.println("  2. Add Apache Arrow Java dependencies to your project");
            System.out.println("  3. Use Java 25 (JDK 25)");
        }
    }
    
    private static ArrowFileReader readArrowData(String filename) throws IOException {
        System.out.println("\nReading Arrow data from: " + filename);
        
        long start = System.currentTimeMillis();
        
        File file = new File(filename);
        if (!file.exists()) {
            throw new IOException("File not found: " + filename + ". Please run python_producer.py first.");
        }
        
        FileInputStream fileInputStream = new FileInputStream(file);
        FileChannel fileChannel = fileInputStream.getChannel();
        SeekableReadChannel readChannel = new SeekableReadChannel(fileChannel);
        
        ArrowFileReader reader = new ArrowFileReader(readChannel, allocator);
        VectorSchemaRoot root = reader.getVectorSchemaRoot();
        
        // Load all batches
        while (reader.loadNextBatch()) {
            // Data is loaded into root
        }
        
        long readTime = System.currentTimeMillis() - start;
        
        System.out.println("✓ Loaded in: " + (readTime / 1000.0) + " seconds");
        System.out.println("  Rows: " + String.format("%,d", root.getRowCount()));
        System.out.println("  Columns: " + root.getSchema().getFields().size());
        System.out.println("  Schema: " + root.getSchema().toString());
        
        return reader;
    }
    
    private static void analyzeWithArrow(VectorSchemaRoot root) {
        System.out.println("\n============================================================");
        System.out.println("ANALYSIS USING APACHE ARROW (Java 25)");
        System.out.println("============================================================");
        
        int rowCount = (int) root.getRowCount();
        
        // Get vectors
        var priceVector = root.getVector("price");
        var tradeValueVector = root.getVector("trade_value");
        var sideVector = root.getVector("side");
        var symbolVector = root.getVector("symbol");
        
        // 1. Total trade value
        System.out.println("\n1. Total Trade Value");
        System.out.println("------------------------------------------------------------");
        long start1 = System.currentTimeMillis();
        double totalValue = 0.0;
        for (int i = 0; i < rowCount; i++) {
            totalValue += tradeValueVector.getObject(i).doubleValue();
        }
        long analysisTime1 = System.currentTimeMillis() - start1;
        System.out.printf("  Total: $%,.2f%n", totalValue);
        System.out.println("  Analysis time: " + (analysisTime1 / 1000.0) + " seconds");
        
        // 2. Average price
        System.out.println("\n2. Average Price");
        System.out.println("------------------------------------------------------------");
        long start2 = System.currentTimeMillis();
        double sumPrice = 0.0;
        for (int i = 0; i < rowCount; i++) {
            sumPrice += priceVector.getObject(i).doubleValue();
        }
        double avgPrice = sumPrice / rowCount;
        long analysisTime2 = System.currentTimeMillis() - start2;
        System.out.printf("  Average: $%.2f%n", avgPrice);
        System.out.println("  Analysis time: " + (analysisTime2 / 1000.0) + " seconds");
        
        // 3. Buy vs Sell count
        System.out.println("\n3. Buy vs Sell Count");
        System.out.println("------------------------------------------------------------");
        long start3 = System.currentTimeMillis();
        int buyCount = 0;
        int sellCount = 0;
        for (int i = 0; i < rowCount; i++) {
            String side = sideVector.getObject(i).toString();
            if ("BUY".equals(side)) {
                buyCount++;
            } else {
                sellCount++;
            }
        }
        long analysisTime3 = System.currentTimeMillis() - start3;
        System.out.println("  BUY: " + String.format("%,d", buyCount));
        System.out.println("  SELL: " + String.format("%,d", sellCount));
        System.out.println("  Analysis time: " + (analysisTime3 / 1000.0) + " seconds");
        
        // 4. High-value trades (> $100,000)
        System.out.println("\n4. High-Value Trades (> $100,000)");
        System.out.println("------------------------------------------------------------");
        long start4 = System.currentTimeMillis();
        int highValueCount = 0;
        for (int i = 0; i < rowCount; i++) {
            if (tradeValueVector.getObject(i).doubleValue() > 100000.0) {
                highValueCount++;
            }
        }
        double percentage = (highValueCount * 100.0) / rowCount;
        long analysisTime4 = System.currentTimeMillis() - start4;
        System.out.println("  Count: " + String.format("%,d", highValueCount));
        System.out.printf("  Percentage: %.2f%%%n", percentage);
        System.out.println("  Analysis time: " + (analysisTime4 / 1000.0) + " seconds");
        
        // 5. Price statistics
        System.out.println("\n5. Price Statistics");
        System.out.println("------------------------------------------------------------");
        long start5 = System.currentTimeMillis();
        double minPrice = Double.MAX_VALUE;
        double maxPrice = Double.MIN_VALUE;
        double sum = 0.0;
        for (int i = 0; i < rowCount; i++) {
            double price = priceVector.getObject(i).doubleValue();
            if (price < minPrice) minPrice = price;
            if (price > maxPrice) maxPrice = price;
            sum += price;
        }
        double mean = sum / rowCount;
        
        // Calculate standard deviation
        double sumSquaredDiff = 0.0;
        for (int i = 0; i < rowCount; i++) {
            double diff = priceVector.getObject(i).doubleValue() - mean;
            sumSquaredDiff += diff * diff;
        }
        double stdDev = Math.sqrt(sumSquaredDiff / rowCount);
        
        long analysisTime5 = System.currentTimeMillis() - start5;
        System.out.printf("  Min: $%.2f%n", minPrice);
        System.out.printf("  Max: $%.2f%n", maxPrice);
        System.out.printf("  Mean: $%.2f%n", mean);
        System.out.printf("  Std Dev: $%.2f%n", stdDev);
        System.out.println("  Analysis time: " + (analysisTime5 / 1000.0) + " seconds");
        
        // 6. Trade volume by symbol
        System.out.println("\n6. Trade Volume by Symbol");
        System.out.println("------------------------------------------------------------");
        long start6 = System.currentTimeMillis();
        Map<String, Double> volumeBySymbol = new HashMap<>();
        for (int i = 0; i < rowCount; i++) {
            String symbol = symbolVector.getObject(i).toString();
            double value = tradeValueVector.getObject(i).doubleValue();
            volumeBySymbol.put(symbol, volumeBySymbol.getOrDefault(symbol, 0.0) + value);
        }
        
        // Sort by volume
        volumeBySymbol.entrySet().stream()
            .sorted(Map.Entry.<String, Double>comparingByValue().reversed())
            .forEach(entry -> 
                System.out.printf("  %s: $%,.2f%n", entry.getKey(), entry.getValue())
            );
        
        long analysisTime6 = System.currentTimeMillis() - start6;
        System.out.println("  Analysis time: " + (analysisTime6 / 1000.0) + " seconds");
    }
}

