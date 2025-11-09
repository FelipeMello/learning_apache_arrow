"""
Investment Banking Example: Creating Arrow Tables

Demonstrates creating Arrow tables from trading data.
Tables are collections of named columns (arrays) that form a structured dataset.
They are the primary data structure for working with tabular data in Arrow.

Key Concepts:
- Tables combine multiple arrays into a structured format
- Each column has a name and type
- Tables support efficient columnar operations
- Schema defines the structure and types of all columns
"""
import pyarrow as pa
from _helpers import print_section_header
from _constants import STOCK_SYMBOLS

# Sample trading data - represents individual trades
SAMPLE_TRADES = {
    'trade_id': [1, 2, 3],
    'symbol': STOCK_SYMBOLS[:3],  # First 3 symbols
    'price': [175.50, 378.25, 142.75],
    'quantity': [100, 500, 1000]
}


def create_trades_table(trades_data: dict) -> pa.Table:
    """
    Create an Arrow table from trading data dictionary.
    
    Args:
        trades_data: Dictionary with column names as keys and lists as values
        
    Returns:
        Arrow table containing the trading data
    """
    return pa.table(trades_data)


def display_table_info(arrow_table: pa.Table, title: str) -> None:
    """
    Display comprehensive information about an Arrow table.
    
    Args:
        arrow_table: The Arrow table to display
        title: Title for the display section
    """
    print_section_header(title, width=50)
    
    print("\nArrow Table:")
    print(arrow_table)
    
    print(f"\nTable Schema:")
    print(f"  {arrow_table.schema}")
    
    print(f"\nTable Dimensions:")
    print(f"  Rows: {arrow_table.num_rows:,}")
    print(f"  Columns: {arrow_table.num_columns}")
    
    print(f"\nColumn Names:")
    for column_name in arrow_table.column_names:
        column_type = arrow_table.schema.field(column_name).type
        print(f"  - {column_name}: {column_type}")


def main():
    """Main execution function."""
    # Create Arrow table from sample trading data
    trades_table = create_trades_table(SAMPLE_TRADES)
    
    # Display table information
    display_table_info(trades_table, "Investment Banking: Trading Table")


if __name__ == "__main__":
    main()