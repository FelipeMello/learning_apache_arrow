"""
Investment Banking Example: Saving Arrow Table to Feather File

Demonstrates persisting trading data in efficient Feather format.
Feather is Apache Arrow's on-disk format, providing fast serialization
and cross-language compatibility.

Key Concepts:
- Feather format preserves Arrow's columnar structure
- Fast read/write operations with minimal overhead
- Zero-copy operations when possible
- Cross-language compatible (Python, Java, Node.js, R)
"""
import pandas as pd
import pyarrow as pa
import pyarrow.feather as feather
from _helpers import print_section_header
from typing import Dict, Any

# Sample trading data - represents individual trades
# In production, this would come from trading systems
SAMPLE_TRADES_DATA = {
    'trade_id': [1, 2, 3],
    'symbol': ['AAPL', 'MSFT', 'GOOGL'],
    'price': [175.50, 378.25, 142.75],
    'quantity': [100, 500, 1000],
    'trade_value': [17550.00, 189125.00, 142750.00]
}

# Output file name
OUTPUT_FEATHER_FILE = 'trading_data.feather'


def create_trading_dataframe(trades_data: Dict[str, list]) -> pd.DataFrame:
    """
    Create a Pandas DataFrame from trading data.
    
    Args:
        trades_data: Dictionary with column names and data lists
        
    Returns:
        Pandas DataFrame containing trading data
    """
    return pd.DataFrame(trades_data)


def convert_to_arrow_table(dataframe: pd.DataFrame) -> pa.Table:
    """
    Convert Pandas DataFrame to Arrow Table.
    
    Args:
        dataframe: Pandas DataFrame to convert
        
    Returns:
        Arrow table with the same data
    """
    return pa.Table.from_pandas(dataframe)


def save_to_feather(arrow_table: pa.Table, filename: str) -> None:
    """
    Save an Arrow table to a Feather file.
    
    Args:
        arrow_table: Arrow table to save
        filename: Output filename for the Feather file
    """
    feather.write_feather(arrow_table, filename)


def display_original_data(dataframe: pd.DataFrame) -> None:
    """
    Display the original trading DataFrame.
    
    Args:
        dataframe: Pandas DataFrame to display
    """
    print_section_header("Investment Banking: Saving to Feather Format", width=60)
    print("\nOriginal Trading DataFrame:")
    print(dataframe)
    print(f"\nDataFrame Info:")
    print(f"  Shape: {dataframe.shape}")
    print(f"  Memory Usage: {dataframe.memory_usage(deep=True).sum() / 1024:.2f} KB")


def display_arrow_table_info(arrow_table: pa.Table) -> None:
    """
    Display information about the Arrow table.
    
    Args:
        arrow_table: Arrow table to display information for
    """
    print(f"\nArrow Table Information:")
    print(f"  Rows: {arrow_table.num_rows}")
    print(f"  Columns: {arrow_table.num_columns}")
    print(f"  Schema: {arrow_table.schema}")


def display_save_results(filename: str, arrow_table: pa.Table) -> None:
    """
    Display results of saving to Feather format.
    
    Args:
        filename: Name of the saved file
        arrow_table: Arrow table that was saved
    """
    print(f"\n✓ Arrow table saved to '{filename}'")
    print(f"  Schema: {arrow_table.schema}")
    print(f"  File format: Feather (Apache Arrow on-disk format)")
    
    print("\nBenefits of Feather Format:")
    print("  • Fast read/write operations")
    print("  • Zero-copy when possible")
    print("  • Cross-language compatible (Python, Java, Node.js)")
    print("  • Preserves Arrow's columnar structure")


def main():
    """Main execution function."""
    # Create trading DataFrame
    trades_dataframe = create_trading_dataframe(SAMPLE_TRADES_DATA)
    display_original_data(trades_dataframe)
    
    # Convert to Arrow Table
    trades_table = convert_to_arrow_table(trades_dataframe)
    display_arrow_table_info(trades_table)
    
    # Save to Feather format
    save_to_feather(trades_table, OUTPUT_FEATHER_FILE)
    display_save_results(OUTPUT_FEATHER_FILE, trades_table)


if __name__ == "__main__":
    main()