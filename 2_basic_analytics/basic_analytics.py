"""
Investment Banking Example: Basic Analytics with Apache Arrow

Demonstrates filtering, aggregation, and statistical operations on trading data.
This example shows how Arrow's compute functions enable efficient analytics
operations on large datasets.

Key Concepts:
- Vectorized operations for fast computations
- Efficient filtering with boolean masks
- Statistical aggregations using Arrow compute
- Combining Arrow and Pandas for complex operations
"""
import pyarrow as pa
import pandas as pd
from _helpers import (
    calculate_statistics,
    filter_table_by_threshold,
    group_by_sector,
    format_currency,
    print_section_header
)
from typing import Dict

# Sample trading data - represents portfolio trades
# In production, this would come from trading systems or databases
SAMPLE_TRADING_DATA = {
    'trade_id': pa.array([1, 2, 3, 4, 5]),
    'trade_value': pa.array([125000, 234000, 189000, 312000, 156000]),
    'sector': pa.array(['Technology', 'Finance', 'Technology', 'Energy', 'Finance'])
}

# Filter threshold for high-value trades
HIGH_VALUE_THRESHOLD = 200000.0


def create_trades_table(trading_data: dict) -> pa.Table:
    """
    Create an Arrow table from trading data.
    
    Args:
        trading_data: Dictionary with column names and Arrow arrays
        
    Returns:
        Arrow table containing the trading data
    """
    return pa.table(trading_data)


def display_original_data(arrow_table: pa.Table) -> None:
    """
    Display the original trading data.
    
    Args:
        arrow_table: Arrow table containing trading data
    """
    print_section_header("Investment Banking: Basic Analytics", width=60)
    print("\nOriginal Trading Table:")
    print(arrow_table.to_pandas())


def display_filtered_trades(arrow_table: pa.Table, threshold: float) -> None:
    """
    Display high-value trades filtered by threshold.
    
    Args:
        arrow_table: Arrow table containing trading data
        threshold: Minimum trade value threshold
    """
    print_section_header("1. FILTERING: High-Value Trades", width=60)
    print(f"Filtering trades with value > {format_currency(threshold)}")
    
    filtered_table = filter_table_by_threshold(
        arrow_table, 
        'trade_value', 
        threshold, 
        'greater'
    )
    
    print(f"\nFiltered Results ({filtered_table.num_rows} trades):")
    print(filtered_table.to_pandas())


def display_statistical_analysis(arrow_table: pa.Table) -> None:
    """
    Display statistical analysis of trade values.
    
    Args:
        arrow_table: Arrow table containing trading data
    """
    print_section_header("2. STATISTICAL OPERATIONS", width=60)
    
    statistics = calculate_statistics(arrow_table, 'trade_value')
    
    print("Trade Value Statistics:")
    print(f"  Mean Trade Value:  {format_currency(statistics['mean'])}")
    print(f"  Max Trade Value:   {format_currency(statistics['max'])}")
    print(f"  Min Trade Value:   {format_currency(statistics['min'])}")
    print(f"  Total Trade Value: {format_currency(statistics['sum'])}")


def display_sector_analysis(arrow_table: pa.Table) -> None:
    """
    Display sector-level aggregation analysis.
    
    Args:
        arrow_table: Arrow table containing trading data
    """
    print_section_header("3. GROUPING BY SECTOR", width=60)
    
    # Convert to Pandas for complex grouping operations
    dataframe = arrow_table.to_pandas()
    sector_analysis = group_by_sector(dataframe, 'trade_value')
    
    print("\nTrade Value by Sector:")
    print(sector_analysis)
    
    print("\nSector Summary:")
    for sector, row in sector_analysis.iterrows():
        print(f"  {sector:15s}: "
              f"Mean={format_currency(row['mean'])}, "
              f"Total={format_currency(row['sum'])}, "
              f"Count={int(row['count'])}")


def display_analysis_summary() -> None:
    """Display summary of completed analysis."""
    print_section_header("Analysis Complete!", width=60)
    print("  ✓ Filtered high-value trades")
    print("  ✓ Calculated comprehensive statistics")
    print("  ✓ Grouped and analyzed by sector")


def main():
    """Main execution function."""
    # Create Arrow table from sample data
    trades_table = create_trades_table(SAMPLE_TRADING_DATA)
    
    # Display original data
    display_original_data(trades_table)
    
    # Filter high-value trades
    display_filtered_trades(trades_table, HIGH_VALUE_THRESHOLD)
    
    # Calculate statistics
    display_statistical_analysis(trades_table)
    
    # Group by sector
    display_sector_analysis(trades_table)
    
    # Display summary
    display_analysis_summary()


if __name__ == "__main__":
    main()