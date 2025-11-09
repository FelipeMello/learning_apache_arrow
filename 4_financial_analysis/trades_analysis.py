"""
Financial Trades Analysis using Apache Arrow
Analyzes high-frequency trading data with performance-optimized operations
"""
import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.feather as feather
from datetime import datetime, timedelta
import time


def generate_trades_data(num_trades=1_000_000):
    """Generate realistic trading data for analysis"""
    print(f"Generating {num_trades:,} trades...")
    
    # Generate timestamps (last 30 days, millisecond precision)
    start_time = datetime.now() - timedelta(days=30)
    timestamps = [
        start_time + timedelta(
            days=np.random.random() * 30,
            hours=np.random.random() * 24,
            minutes=np.random.random() * 60,
            seconds=np.random.random() * 60,
            milliseconds=np.random.random() * 1000
        )
        for _ in range(num_trades)
    ]
    
    # Generate trading data
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX']
    
    data = {
        'timestamp': timestamps,
        'symbol': np.random.choice(symbols, size=num_trades),
        'price': np.random.uniform(50, 500, size=num_trades).round(2),
        'quantity': np.random.randint(1, 10000, size=num_trades),
        'side': np.random.choice(['BUY', 'SELL'], size=num_trades),
        'order_type': np.random.choice(['MARKET', 'LIMIT', 'STOP'], size=num_trades, p=[0.6, 0.3, 0.1]),
    }
    
    # Calculate trade value
    data['trade_value'] = data['price'] * data['quantity']
    
    return pd.DataFrame(data)


def analyze_trades_with_arrow(df):
    """Perform comprehensive trades analysis using Apache Arrow"""
    print("\n" + "="*60)
    print("TRADES ANALYSIS WITH APACHE ARROW")
    print("="*60)
    
    # Convert to Arrow Table
    start = time.time()
    arrow_table = pa.Table.from_pandas(df)
    conversion_time = time.time() - start
    print(f"\n✓ Converted to Arrow Table: {conversion_time:.4f} seconds")
    print(f"  Rows: {arrow_table.num_rows:,}")
    print(f"  Columns: {arrow_table.num_columns}")
    
    # 1. Total Trading Volume by Symbol
    print("\n1. TOTAL TRADING VOLUME BY SYMBOL")
    print("-" * 60)
    start = time.time()
    
    # Convert to pandas for grouping (Arrow compute doesn't have groupby yet)
    df_arrow = arrow_table.to_pandas()
    volume_by_symbol = df_arrow.groupby('symbol')['trade_value'].sum().sort_values(ascending=False)
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    for symbol, volume in volume_by_symbol.items():
        print(f"  {symbol}: ${volume:,.2f}")
    
    # 2. Average Trade Price by Symbol
    print("\n2. AVERAGE TRADE PRICE BY SYMBOL")
    print("-" * 60)
    start = time.time()
    
    avg_price_by_symbol = df_arrow.groupby('symbol')['price'].mean()
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    for symbol, avg_price in avg_price_by_symbol.items():
        print(f"  {symbol}: ${avg_price:.2f}")
    
    # 3. Buy vs Sell Ratio
    print("\n3. BUY vs SELL RATIO")
    print("-" * 60)
    start = time.time()
    
    # Use Arrow compute for filtering
    buy_mask = pc.equal(arrow_table['side'], pa.scalar('BUY'))
    sell_mask = pc.equal(arrow_table['side'], pa.scalar('SELL'))
    
    buy_count = pc.sum(pc.cast(buy_mask, pa.int64())).as_py()
    sell_count = pc.sum(pc.cast(sell_mask, pa.int64())).as_py()
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    print(f"  BUY trades: {buy_count:,} ({buy_count/(buy_count+sell_count)*100:.1f}%)")
    print(f"  SELL trades: {sell_count:,} ({sell_count/(buy_count+sell_count)*100:.1f}%)")
    
    # 4. High-Value Trades (> $100,000)
    print("\n4. HIGH-VALUE TRADES (> $100,000)")
    print("-" * 60)
    start = time.time()
    
    high_value_mask = pc.greater(arrow_table['trade_value'], pa.scalar(100000.0))
    high_value_trades = pc.filter(arrow_table, high_value_mask)
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    print(f"  High-value trades: {high_value_trades.num_rows:,}")
    print(f"  Percentage: {high_value_trades.num_rows/arrow_table.num_rows*100:.2f}%")
    
    # Calculate statistics on high-value trades
    high_value_df = high_value_trades.to_pandas()
    avg_high_value = high_value_df['trade_value'].mean()
    max_high_value = high_value_df['trade_value'].max()
    print(f"  Average high-value trade: ${avg_high_value:,.2f}")
    print(f"  Maximum trade value: ${max_high_value:,.2f}")
    
    # 5. Order Type Distribution
    print("\n5. ORDER TYPE DISTRIBUTION")
    print("-" * 60)
    start = time.time()
    
    order_type_counts = df_arrow['order_type'].value_counts()
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    for order_type, count in order_type_counts.items():
        print(f"  {order_type}: {count:,} ({count/len(df_arrow)*100:.1f}%)")
    
    # 6. Price Statistics
    print("\n6. PRICE STATISTICS (All Trades)")
    print("-" * 60)
    start = time.time()
    
    # Use Arrow compute for statistics
    min_price = pc.min(arrow_table['price']).as_py()
    max_price = pc.max(arrow_table['price']).as_py()
    mean_price = pc.mean(arrow_table['price']).as_py()
    std_price = pc.stddev(arrow_table['price']).as_py()
    
    analysis_time = time.time() - start
    print(f"Analysis time: {analysis_time:.4f} seconds")
    print(f"  Minimum price: ${min_price:.2f}")
    print(f"  Maximum price: ${max_price:.2f}")
    print(f"  Mean price: ${mean_price:.2f}")
    print(f"  Std deviation: ${std_price:.2f}")
    
    # 7. Save to Feather for future use
    print("\n7. SAVING TO FEATHER FORMAT")
    print("-" * 60)
    start = time.time()
    
    feather.write_feather(arrow_table, 'trades_data.feather')
    
    save_time = time.time() - start
    print(f"Saved to Feather: {save_time:.4f} seconds")
    print("  File: trades_data.feather")
    
    return arrow_table


def load_and_analyze_feather():
    """Demonstrate loading from Feather format"""
    print("\n" + "="*60)
    print("LOADING FROM FEATHER FORMAT")
    print("="*60)
    
    start = time.time()
    loaded_table = feather.read_table('trades_data.feather')
    load_time = time.time() - start
    
    print(f"✓ Loaded from Feather: {load_time:.4f} seconds")
    print(f"  Rows: {loaded_table.num_rows:,}")
    print(f"  Columns: {loaded_table.num_columns}")
    
    return loaded_table


if __name__ == "__main__":
    # Generate sample trading data
    print("="*60)
    print("FINANCIAL TRADES ANALYSIS")
    print("="*60)
    
    df = generate_trades_data(num_trades=1_000_000)
    
    # Perform analysis
    arrow_table = analyze_trades_with_arrow(df)
    
    # Demonstrate Feather loading
    loaded_table = load_and_analyze_feather()
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print("\nKey Benefits of Using Apache Arrow:")
    print("  ✓ Fast columnar operations")
    print("  ✓ Efficient memory usage")
    print("  ✓ Zero-copy conversions")
    print("  ✓ Optimized for analytical workloads")

