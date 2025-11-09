"""
Investment Banking Example: Generating Large Trading Dataset

Demonstrates creating large-scale trading data for performance testing.
This example shows how to generate realistic trading datasets for
benchmarking and testing Arrow's performance on large data.

Key Concepts:
- Efficient data generation for testing
- Realistic trading data structures
- Performance measurement
- Memory usage tracking
"""
import pandas as pd
import time
from _helpers import (
    generate_trading_dataframe,
    format_memory_usage,
    format_currency,
    print_section_header
)
from _constants import STOCK_SYMBOLS, SECTORS, TRADE_TYPES

# Configuration for dataset generation
NUM_TRADES = 1_000_000
SAMPLE_SYMBOLS = STOCK_SYMBOLS[:10]  # First 10 symbols
SAMPLE_SECTORS = SECTORS[:5]  # First 5 sectors


def generate_large_dataset(num_trades: int, symbols: list, sectors: list, 
                          trade_types: list) -> tuple[pd.DataFrame, float]:
    """
    Generate a large trading dataset and measure generation time.
    
    Args:
        num_trades: Number of trades to generate
        symbols: List of stock symbols to use
        sectors: List of sectors to use
        trade_types: List of trade types to use
        
    Returns:
        Tuple of (DataFrame, generation time in seconds)
    """
    start_time = time.time()
    
    dataframe = generate_trading_dataframe(
        num_trades=num_trades,
        symbols=symbols,
        sectors=sectors,
        trade_types=trade_types,
        include_dates=True
    )
    
    generation_time = time.time() - start_time
    
    return dataframe, generation_time


def display_generation_progress(num_trades: int) -> None:
    """
    Display progress message for dataset generation.
    
    Args:
        num_trades: Number of trades being generated
    """
    print_section_header("Investment Banking: Generating Large Trading Dataset", width=60)
    print(f"\nGenerating {num_trades:,} trades...")


def display_generation_results(dataframe: pd.DataFrame, generation_time: float) -> None:
    """
    Display results of dataset generation.
    
    Args:
        dataframe: Generated DataFrame
        generation_time: Time taken for generation in seconds
    """
    print(f"\n✓ Generated {len(dataframe):,} trades in {generation_time:.4f} seconds")
    
    memory_bytes = dataframe.memory_usage(deep=True).sum()
    print(f"  Memory Usage: {format_memory_usage(memory_bytes, 'MB')}")
    print(f"  Columns: {len(dataframe.columns)}")
    
    print(f"\nSample Data (first 5 rows):")
    print(dataframe.head())


def display_dataset_summary(dataframe: pd.DataFrame) -> None:
    """
    Display summary statistics of the generated dataset.
    
    Args:
        dataframe: Generated DataFrame to summarize
    """
    print_section_header("Dataset Summary", width=60)
    
    total_trades = len(dataframe)
    unique_symbols = dataframe['symbol'].nunique()
    total_trade_value = dataframe['trade_value'].sum()
    avg_trade_value = dataframe['trade_value'].mean()
    
    print(f"  Total Trades:        {total_trades:,}")
    print(f"  Unique Symbols:      {unique_symbols}")
    print(f"  Total Trade Value:    {format_currency(total_trade_value)}")
    print(f"  Average Trade Value: {format_currency(avg_trade_value)}")


def main():
    """Main execution function."""
    # Display generation progress
    display_generation_progress(NUM_TRADES)
    
    # Generate large dataset
    trades_dataframe, generation_time = generate_large_dataset(
        num_trades=NUM_TRADES,
        symbols=SAMPLE_SYMBOLS,
        sectors=SAMPLE_SECTORS,
        trade_types=TRADE_TYPES
    )
    
    # Display generation results
    display_generation_results(trades_dataframe, generation_time)
    
    # Display dataset summary
    display_dataset_summary(trades_dataframe)


if __name__ == "__main__":
    main()