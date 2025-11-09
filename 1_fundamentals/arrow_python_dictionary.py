"""
Investment Banking Example: Creating Arrow Table from Python Dictionary

Demonstrates converting Python dictionaries to Arrow tables.
This is one of the most common ways to create Arrow tables, especially
when working with data from APIs, databases, or other Python sources.

Key Concepts:
- Python dictionaries map naturally to Arrow tables
- Keys become column names
- Values (lists) become column data
- All lists must have the same length
- Arrow infers types automatically but can be overridden
"""
import pyarrow as pa
from _helpers import print_section_header, extract_trade_details, print_trade_summary
from _constants import TRADE_TYPES

# Sample trading data as a Python dictionary
# This format is common when receiving data from APIs or databases
SAMPLE_TRADING_DATA = {
    'trade_id': [101, 102, 103],
    'symbol': ['TSLA', 'AMZN', 'NVDA'],
    'price': [245.30, 148.50, 485.75],
    'quantity': [200, 300, 150],
    'trade_type': TRADE_TYPES[:2] + [TRADE_TYPES[0]]  # BUY, SELL, BUY
}


def create_table_from_dictionary(data_dict: dict) -> pa.Table:
    """
    Create an Arrow table from a Python dictionary.
    
    Args:
        data_dict: Dictionary where keys are column names and values are lists
        
    Returns:
        Arrow table created from the dictionary
        
    Raises:
        ValueError: If lists in dictionary have different lengths
    """
    # Validate that all lists have the same length
    lengths = [len(value) for value in data_dict.values() if isinstance(value, list)]
    if len(set(lengths)) > 1:
        raise ValueError("All lists in dictionary must have the same length")
    
    return pa.table(data_dict)


def display_table_from_dictionary(arrow_table: pa.Table) -> None:
    """
    Display information about a table created from a dictionary.
    
    Args:
        arrow_table: The Arrow table to display
    """
    print_section_header("Investment Banking: Trading Table from Dictionary", width=50)
    
    print("\nArrow Table from Dictionary:")
    print(arrow_table)
    
    print(f"\nSchema:")
    print(f"  {arrow_table.schema}")


def display_trade_summary(arrow_table: pa.Table) -> None:
    """
    Display a formatted summary of all trades in the table.
    
    Args:
        arrow_table: Arrow table containing trade data
    """
    print("\nTrade Summary:")
    for row_index in range(arrow_table.num_rows):
        trade_details = extract_trade_details(arrow_table, row_index)
        print_trade_summary(trade_details)


def main():
    """Main execution function."""
    # Create Arrow table from Python dictionary
    trades_table = create_table_from_dictionary(SAMPLE_TRADING_DATA)
    
    # Display table information
    display_table_from_dictionary(trades_table)
    
    # Display trade summary
    display_trade_summary(trades_table)


if __name__ == "__main__":
    main()