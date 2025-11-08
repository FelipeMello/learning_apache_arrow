"""
Python Consumer: Reads and processes Arrow data created by python_producer.py
Demonstrates zero-copy data access in Python
"""
import pyarrow.feather as feather
import pyarrow.compute as pc
import pyarrow as pa
import time


def read_arrow_data(filename='shared_data.feather'):
    """Read Arrow data from Feather file"""
    print(f"Reading Arrow data from: {filename}")
    
    start = time.time()
    # Read as Arrow table (not DataFrame)
    arrow_table = feather.read_table(filename)
    read_time = time.time() - start
    
    print(f"✓ Loaded in: {read_time:.4f} seconds")
    print(f"  Rows: {arrow_table.num_rows:,}")
    print(f"  Columns: {arrow_table.num_columns}")
    print(f"  Schema: {arrow_table.schema}")
    
    return arrow_table


def analyze_with_arrow_compute(arrow_table):
    """Analyze data using Arrow compute functions"""
    print("\n" + "="*60)
    print("ANALYSIS USING ARROW COMPUTE (Python)")
    print("="*60)
    
    # 1. Total trade value
    print("\n1. Total Trade Value")
    print("-" * 60)
    start = time.time()
    total_value = pc.sum(arrow_table['trade_value']).as_py()
    analysis_time = time.time() - start
    print(f"  Total: ${total_value:,.2f}")
    print(f"  Analysis time: {analysis_time:.4f} seconds")
    
    # 2. Average price
    print("\n2. Average Price")
    print("-" * 60)
    start = time.time()
    avg_price = pc.mean(arrow_table['price']).as_py()
    analysis_time = time.time() - start
    print(f"  Average: ${avg_price:.2f}")
    print(f"  Analysis time: {analysis_time:.4f} seconds")
    
    # 3. Buy vs Sell count
    print("\n3. Buy vs Sell Count")
    print("-" * 60)
    start = time.time()
    buy_mask = pc.equal(arrow_table['side'], pa.scalar('BUY'))
    sell_mask = pc.equal(arrow_table['side'], pa.scalar('SELL'))
    buy_count = pc.sum(pc.cast(buy_mask, pa.int64())).as_py()
    sell_count = pc.sum(pc.cast(sell_mask, pa.int64())).as_py()
    analysis_time = time.time() - start
    print(f"  BUY: {buy_count:,}")
    print(f"  SELL: {sell_count:,}")
    print(f"  Analysis time: {analysis_time:.4f} seconds")
    
    # 4. High-value trades (> $100,000)
    print("\n4. High-Value Trades (> $100,000)")
    print("-" * 60)
    start = time.time()
    high_value_mask = pc.greater(arrow_table['trade_value'], pa.scalar(100000.0))
    high_value_trades = pc.filter(arrow_table, high_value_mask)
    analysis_time = time.time() - start
    print(f"  Count: {high_value_trades.num_rows:,}")
    print(f"  Percentage: {high_value_trades.num_rows/arrow_table.num_rows*100:.2f}%")
    print(f"  Analysis time: {analysis_time:.4f} seconds")
    
    # 5. Price statistics
    print("\n5. Price Statistics")
    print("-" * 60)
    start = time.time()
    min_price = pc.min(arrow_table['price']).as_py()
    max_price = pc.max(arrow_table['price']).as_py()
    mean_price = pc.mean(arrow_table['price']).as_py()
    std_price = pc.stddev(arrow_table['price']).as_py()
    analysis_time = time.time() - start
    print(f"  Min: ${min_price:.2f}")
    print(f"  Max: ${max_price:.2f}")
    print(f"  Mean: ${mean_price:.2f}")
    print(f"  Std Dev: ${std_price:.2f}")
    print(f"  Analysis time: {analysis_time:.4f} seconds")


def analyze_with_pandas(arrow_table):
    """Analyze data by converting to Pandas (demonstrates zero-copy conversion)"""
    print("\n" + "="*60)
    print("ANALYSIS USING PANDAS (Zero-Copy Conversion)")
    print("="*60)
    
    # Convert to Pandas (zero-copy)
    start = time.time()
    df = arrow_table.to_pandas()
    conversion_time = time.time() - start
    print(f"\n✓ Converted to Pandas: {conversion_time:.4f} seconds (zero-copy)")
    
    # Group by symbol
    print("\n1. Trade Volume by Symbol")
    print("-" * 60)
    start = time.time()
    volume_by_symbol = df.groupby('symbol')['trade_value'].sum().sort_values(ascending=False)
    analysis_time = time.time() - start
    for symbol, volume in volume_by_symbol.items():
        print(f"  {symbol}: ${volume:,.2f}")
    print(f"  Analysis time: {analysis_time:.4f} seconds")
    
    # Average price by symbol
    print("\n2. Average Price by Symbol")
    print("-" * 60)
    start = time.time()
    avg_price_by_symbol = df.groupby('symbol')['price'].mean()
    analysis_time = time.time() - start
    for symbol, avg_price in avg_price_by_symbol.items():
        print(f"  {symbol}: ${avg_price:.2f}")
    print(f"  Analysis time: {analysis_time:.4f} seconds")


if __name__ == "__main__":
    print("="*60)
    print("PYTHON CONSUMER: Reading Shared Arrow Data")
    print("="*60)
    
    # Read Arrow data
    arrow_table = read_arrow_data('shared_data.feather')
    
    # Analyze with Arrow compute
    analyze_with_arrow_compute(arrow_table)
    
    # Analyze with Pandas (zero-copy conversion)
    analyze_with_pandas(arrow_table)
    
    print("\n" + "="*60)
    print("✓ Python analysis complete!")
    print("="*60)
    print("\nThis same data file can be read by:")
    print("  - Node.js (nodejs_consumer.js)")
    print("  - Java 25 (java_consumer.java)")
    print("  - Any other language with Arrow support")

