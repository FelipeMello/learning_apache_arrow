"""
Python Producer: Creates financial data and saves to Arrow format
This data will be consumed by Python, Node.js, and Java 25
"""
import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.feather as feather
from datetime import datetime, timedelta
import time


def generate_financial_data(num_records=100_000):
    """Generate realistic financial trading data"""
    print(f"Generating {num_records:,} financial records...")
    
    # Generate timestamps (last 7 days)
    start_time = datetime.now() - timedelta(days=7)
    timestamps = [
        start_time + timedelta(
            days=np.random.random() * 7,
            hours=np.random.random() * 24,
            minutes=np.random.random() * 60,
            seconds=np.random.random() * 60
        )
        for _ in range(num_records)
    ]
    
    # Stock symbols
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX']
    
    # Generate trading data
    data = {
        'timestamp': timestamps,
        'symbol': np.random.choice(symbols, size=num_records),
        'price': np.random.uniform(50, 500, size=num_records).round(2),
        'quantity': np.random.randint(1, 10000, size=num_records),
        'side': np.random.choice(['BUY', 'SELL'], size=num_records),
    }
    
    # Calculate trade value
    data['trade_value'] = [p * q for p, q in zip(data['price'], data['quantity'])]
    
    df = pd.DataFrame(data)
    
    return df


def save_to_arrow_format(df, filename='shared_data.feather'):
    """Save DataFrame to Arrow format (Feather) for cross-language sharing"""
    print(f"\nSaving to Arrow format: {filename}")
    
    # Convert to Arrow Table
    start = time.time()
    arrow_table = pa.Table.from_pandas(df)
    conversion_time = time.time() - start
    
    print(f"✓ Converted to Arrow Table: {conversion_time:.4f} seconds")
    print(f"  Rows: {arrow_table.num_rows:,}")
    print(f"  Columns: {arrow_table.num_columns}")
    print(f"  Schema: {arrow_table.schema}")
    
    # Save to Feather format (Arrow's on-disk format)
    # Note: compression=None for cross-language compatibility (Node.js doesn't support compression)
    start = time.time()
    feather.write_feather(arrow_table, filename, compression='uncompressed')
    save_time = time.time() - start
    
    print(f"✓ Saved to Feather file: {save_time:.4f} seconds")
    print(f"  File: {filename}")
    
    # Display file size
    import os
    file_size = os.path.getsize(filename)
    print(f"  File size: {file_size / 1024 / 1024:.2f} MB")
    
    return arrow_table


def display_summary(arrow_table):
    """Display summary of the data"""
    print("\n" + "="*60)
    print("DATA SUMMARY")
    print("="*60)
    
    df = arrow_table.to_pandas()
    
    print(f"\nTotal Records: {len(df):,}")
    print(f"\nSymbol Distribution:")
    print(df['symbol'].value_counts())
    
    print(f"\nBuy/Sell Distribution:")
    print(df['side'].value_counts())
    
    print(f"\nPrice Statistics:")
    print(f"  Min: ${df['price'].min():.2f}")
    print(f"  Max: ${df['price'].max():.2f}")
    print(f"  Mean: ${df['price'].mean():.2f}")
    print(f"  Median: ${df['price'].median():.2f}")
    
    print(f"\nTrade Value Statistics:")
    print(f"  Total: ${df['trade_value'].sum():,.2f}")
    print(f"  Mean: ${df['trade_value'].mean():,.2f}")
    print(f"  Max: ${df['trade_value'].max():,.2f}")
    
    print(f"\nTime Range:")
    print(f"  From: {df['timestamp'].min()}")
    print(f"  To: {df['timestamp'].max()}")


if __name__ == "__main__":
    print("="*60)
    print("PYTHON PRODUCER: Creating Shared Arrow Data")
    print("="*60)
    
    # Generate data
    df = generate_financial_data(num_records=100_000)
    
    # Save to Arrow format
    arrow_table = save_to_arrow_format(df, 'shared_data.feather')
    
    # Display summary
    display_summary(arrow_table)
    
    print("\n" + "="*60)
    print("✓ Data ready for cross-language consumption!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Run: python3 python_consumer.py")
    print("  2. Run: node nodejs_consumer.js")
    print("  3. Run: java java_consumer.java (after compiling)")

