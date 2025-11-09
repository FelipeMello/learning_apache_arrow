"""
Investment Banking Example: Converting Pandas DataFrame to Arrow Table

Demonstrates efficient conversion from pandas to Arrow for analysis.
This conversion is typically zero-copy, making it very efficient for
switching between pandas and Arrow as needed.

Key Concepts:
- Zero-copy conversion when data types are compatible
- Columnar format enables efficient analytics
- Cross-language interoperability
- SIMD-optimized compute operations
"""
import pyarrow as pa
import pandas as pd
import time
from _helpers import (
    convert_dataframe_to_arrow,
    format_memory_usage,
    print_section_header
)
from typing import Dict

# Sample trading data - represents portfolio trades
# In production, this would come from trading systems or databases
SAMPLE_TRADES_DATA = {
    'trade_id': [1, 2, 3, 4, 5],
    'symbol': ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN'],
    'price': [175.50, 378.25, 142.75, 245.30, 148.50],
    'quantity': [100, 500, 1000, 200, 300],
    'sector': ['Technology', 'Technology', 'Technology', 'Energy', 'Consumer']
}


def create_trading_dataframe(trades_data: Dict[str, list]) -> pd.DataFrame:
    """
    Create a Pandas DataFrame from trading data.
    
    Args:
        trades_data: Dictionary with column names and data lists
        
    Returns:
        Pandas DataFrame containing trading data
    """
    return pd.DataFrame(trades_data)


def display_dataframe_info(dataframe: pd.DataFrame) -> None:
    """
    Display information about the Pandas DataFrame.
    
    Args:
        dataframe: Pandas DataFrame to display information for
    """
    print_section_header("Investment Banking: Pandas to Arrow Conversion", width=60)
    print("\nOriginal Pandas DataFrame:")
    print(dataframe)
    print(f"\nDataFrame Information:")
    print(f"  Shape: {dataframe.shape}")
    memory_bytes = dataframe.memory_usage(deep=True).sum()
    print(f"  Memory Usage: {format_memory_usage(memory_bytes, 'KB')}")


def display_conversion_results(arrow_table: pa.Table, conversion_time: float) -> None:
    """
    Display results of the conversion operation.
    
    Args:
        arrow_table: Arrow table that was created
        conversion_time: Time taken for conversion in seconds
    """
    print_section_header("Converted to Arrow Table", width=60)
    print(arrow_table)
    print(f"\nConversion Metrics:")
    print(f"  Conversion Time: {conversion_time:.6f} seconds")
    print(f"  Arrow Table Rows: {arrow_table.num_rows}")
    print(f"  Arrow Table Columns: {arrow_table.num_columns}")
    print(f"  Schema: {arrow_table.schema}")


def display_arrow_benefits() -> None:
    """Display benefits of using Arrow format."""
    print_section_header("Benefits of Arrow Format", width=60)
    print("  ✓ Zero-copy conversion when possible")
    print("  ✓ Columnar format for efficient analytics")
    print("  ✓ Cross-language interoperability")
    print("  ✓ SIMD-optimized compute operations")
    print("  ✓ Efficient memory usage")


def main():
    """Main execution function."""
    # Create trading DataFrame
    trades_dataframe = create_trading_dataframe(SAMPLE_TRADES_DATA)
    display_dataframe_info(trades_dataframe)
    
    # Convert to Arrow Table
    arrow_table, conversion_time = convert_dataframe_to_arrow(trades_dataframe)
    display_conversion_results(arrow_table, conversion_time)
    
    # Display benefits
    display_arrow_benefits()


if __name__ == "__main__":
    main()