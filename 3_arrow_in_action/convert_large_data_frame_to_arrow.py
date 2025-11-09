"""
Investment Banking Example: Converting Large Trading Dataset to Arrow

Demonstrates performance benefits of Arrow with large-scale trading data.
This example shows the complete workflow from data generation through
conversion, filtering, analysis, and back to Pandas.

Key Concepts:
- Performance measurement and benchmarking
- Efficient filtering on large datasets
- Statistical computations on filtered data
- Zero-copy conversions
- Complete workflow demonstration
"""
import pandas as pd
import numpy as np
import pyarrow as pa
import time
from _helpers import (
    generate_trading_dataframe,
    convert_dataframe_to_arrow,
    filter_high_value_trades,
    calculate_trade_statistics,
    format_memory_usage,
    format_currency,
    print_section_header
)
from _constants import STOCK_SYMBOLS, VERY_HIGH_VALUE_THRESHOLD

# Configuration
NUM_TRADES = 1_000_000
SAMPLE_SYMBOLS = STOCK_SYMBOLS[:10]  # First 10 symbols
FILTER_THRESHOLD = VERY_HIGH_VALUE_THRESHOLD


def generate_simplified_trading_data(num_trades: int, symbols: list) -> tuple[pd.DataFrame, float]:
    """
    Generate simplified trading data for performance testing.
    
    Args:
        num_trades: Number of trades to generate
        symbols: List of stock symbols to use
        
    Returns:
        Tuple of (DataFrame, generation time in seconds)
    """
    start_time = time.time()
    
    dataframe = pd.DataFrame({
        'trade_id': range(1, num_trades + 1),
        'symbol': np.random.choice(symbols, size=num_trades),
        'price': np.random.uniform(50, 500, size=num_trades).round(2),
        'quantity': np.random.randint(10, 10000, size=num_trades),
        'trade_value': np.random.uniform(1000, 5000000, size=num_trades).round(2)
    })
    
    generation_time = time.time() - start_time
    
    return dataframe, generation_time


def display_generation_results(dataframe: pd.DataFrame, generation_time: float) -> None:
    """
    Display results of data generation.
    
    Args:
        dataframe: Generated DataFrame
        generation_time: Time taken for generation
    """
    print_section_header("1. GENERATING LARGE TRADING DATASET", width=60, separator="-")
    
    print(f"✓ Generated {len(dataframe):,} trades in {generation_time:.4f} seconds")
    print(f"  DataFrame shape: {dataframe.shape}")
    memory_bytes = dataframe.memory_usage(deep=True).sum()
    print(f"  Memory usage: {format_memory_usage(memory_bytes, 'MB')}")


def display_conversion_results(arrow_table: pa.Table, conversion_time: float) -> None:
    """
    Display results of Arrow conversion.
    
    Args:
        arrow_table: Converted Arrow table
        conversion_time: Time taken for conversion
    """
    print_section_header("2. CONVERTING TO ARROW TABLE", width=60, separator="-")
    
    print(f"✓ Conversion to Arrow Table took {conversion_time:.4f} seconds")
    print(f"  Arrow Table rows: {arrow_table.num_rows:,}")
    print(f"  Arrow Table columns: {arrow_table.num_columns}")


def display_filtering_results(filtered_table: pa.Table, original_table: pa.Table, 
                              filter_time: float, threshold: float) -> None:
    """
    Display results of filtering operation.
    
    Args:
        filtered_table: Filtered Arrow table
        original_table: Original Arrow table
        filter_time: Time taken for filtering
        threshold: Filter threshold used
    """
    print_section_header(f"3. FILTERING HIGH-VALUE TRADES (> {format_currency(threshold)})", 
                        width=60, separator="-")
    
    print(f"✓ Filtering took {filter_time:.4f} seconds")
    print(f"  Filtered row count: {filtered_table.num_rows:,}")
    
    if original_table.num_rows > 0:
        percentage = (filtered_table.num_rows / original_table.num_rows) * 100
        print(f"  Percentage of total: {percentage:.2f}%")


def display_statistics_results(statistics: dict, stats_time: float) -> None:
    """
    Display statistical analysis results.
    
    Args:
        statistics: Dictionary with statistical measures
        stats_time: Time taken for statistics calculation
    """
    print_section_header("4. CALCULATING STATISTICS", width=60, separator="-")
    
    print(f"✓ Statistics calculated in {stats_time:.4f} seconds")
    print(f"  Total filtered trade value:   {format_currency(statistics['total'])}")
    print(f"  Average filtered trade value: {format_currency(statistics['average'])}")
    print(f"  Maximum filtered trade value: {format_currency(statistics['maximum'])}")


def display_pandas_conversion_results(dataframe: pd.DataFrame, conversion_time: float) -> None:
    """
    Display results of Pandas conversion.
    
    Args:
        dataframe: Converted Pandas DataFrame
        conversion_time: Time taken for conversion
    """
    print_section_header("5. CONVERTING BACK TO PANDAS", width=60, separator="-")
    
    print(f"✓ Conversion to pandas DataFrame took {conversion_time:.4f} seconds")
    print(f"  Filtered DataFrame shape: {dataframe.shape}")


def display_performance_summary(timings: dict) -> None:
    """
    Display comprehensive performance summary.
    
    Args:
        timings: Dictionary with timing information for each operation
    """
    print_section_header("PERFORMANCE SUMMARY", width=60)
    
    total_time = sum(timings.values())
    
    print(f"  Data generation:     {timings['generation']:.4f} seconds")
    print(f"  Arrow conversion:    {timings['conversion']:.4f} seconds")
    print(f"  Filtering:           {timings['filtering']:.4f} seconds")
    print(f"  Statistics:          {timings['statistics']:.4f} seconds")
    print(f"  Pandas conversion:   {timings['pandas_conversion']:.4f} seconds")
    print(f"  Total time:          {total_time:.4f} seconds")


def display_arrow_benefits() -> None:
    """Display key benefits of Apache Arrow."""
    print_section_header("KEY BENEFITS OF APACHE ARROW", width=60)
    print("  ✓ Columnar format enables fast filtering")
    print("  ✓ SIMD-powered compute functions for analytics")
    print("  ✓ Zero-copy conversion when possible")
    print("  ✓ Efficient memory usage")
    print("  ✓ Excellent for large-scale in-memory operations")


def main():
    """Main execution function."""
    print_section_header("Investment Banking: Large Dataset Conversion and Analysis", width=60)
    
    # 1. Generate large trading dataset
    trades_dataframe, generation_time = generate_simplified_trading_data(
        NUM_TRADES, 
        SAMPLE_SYMBOLS
    )
    display_generation_results(trades_dataframe, generation_time)
    
    # 2. Convert to Arrow Table
    arrow_table, conversion_time = convert_dataframe_to_arrow(trades_dataframe)
    display_conversion_results(arrow_table, conversion_time)
    
    # 3. Filter high-value trades
    filtered_table, filter_time = filter_high_value_trades(arrow_table, FILTER_THRESHOLD)
    display_filtering_results(filtered_table, arrow_table, filter_time, FILTER_THRESHOLD)
    
    # 4. Calculate statistics
    statistics, stats_time = calculate_trade_statistics(filtered_table)
    display_statistics_results(statistics, stats_time)
    
    # 5. Convert back to Pandas
    start_time = time.time()
    filtered_dataframe = filtered_table.to_pandas()
    pandas_conversion_time = time.time() - start_time
    display_pandas_conversion_results(filtered_dataframe, pandas_conversion_time)
    
    # Performance summary
    timings = {
        'generation': generation_time,
        'conversion': conversion_time,
        'filtering': filter_time,
        'statistics': stats_time,
        'pandas_conversion': pandas_conversion_time
    }
    display_performance_summary(timings)
    
    # Display benefits
    display_arrow_benefits()


if __name__ == "__main__":
    main()