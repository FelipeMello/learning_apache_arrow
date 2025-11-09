"""
Investment Banking Example: Combining Multiple Arrays into a Table

Demonstrates creating a table from individual Arrow arrays.
This approach is useful when you have separate arrays that need to be
combined into a structured table, or when building tables programmatically.

Key Concepts:
- Individual arrays can be combined into a table
- Arrays must have the same length (number of rows)
- Column names are specified when creating the table
- This pattern is common when processing data from multiple sources
"""
import pyarrow as pa
from _helpers import calculate_trade_value, format_currency, print_section_header, extract_trade_details, print_trade_summary
from _constants import STOCK_SYMBOLS

# Sample trading data as separate arrays
# In production, these might come from different data sources
SAMPLE_TRADE_IDS = [1, 2, 3]
SAMPLE_SYMBOLS = STOCK_SYMBOLS[:3]
SAMPLE_PRICES = [175.50, 378.25, 142.75]
SAMPLE_QUANTITIES = [100, 500, 1000]


def create_individual_arrays(trade_ids: list, symbols: list, prices: list, quantities: list) -> tuple:
    """
    Create individual Arrow arrays for trading data.
    
    Args:
        trade_ids: List of trade identifiers
        symbols: List of stock symbols
        prices: List of trade prices
        quantities: List of trade quantities
        
    Returns:
        Tuple of (trade_ids_array, symbols_array, prices_array, quantities_array)
    """
    trade_ids_array = pa.array(trade_ids, type=pa.int32())
    symbols_array = pa.array(symbols, type=pa.string())
    prices_array = pa.array(prices, type=pa.float64())
    quantities_array = pa.array(quantities, type=pa.int32())
    
    return trade_ids_array, symbols_array, prices_array, quantities_array


def combine_arrays_into_table(trade_ids: pa.Array, symbols: pa.Array, 
                              prices: pa.Array, quantities: pa.Array) -> pa.Table:
    """
    Combine individual Arrow arrays into a structured table.
    
    Args:
        trade_ids: Array of trade identifiers
        symbols: Array of stock symbols
        prices: Array of trade prices
        quantities: Array of trade quantities
        
    Returns:
        Arrow table combining all arrays
    """
    return pa.table({
        'trade_id': trade_ids,
        'symbol': symbols,
        'price': prices,
        'quantity': quantities
    })


def display_table_from_arrays(arrow_table: pa.Table) -> None:
    """
    Display information about a table created from arrays.
    
    Args:
        arrow_table: The Arrow table to display
    """
    print_section_header("Investment Banking: Trading Table from Arrays", width=50)
    
    print("Arrow Table from Arrays:")
    print(arrow_table)
    
    print(f"\nTable Structure:")
    print(f"  Rows: {arrow_table.num_rows}")
    print(f"  Columns: {arrow_table.num_columns}")
    print(f"  Schema: {arrow_table.schema}")


def display_trade_details(arrow_table: pa.Table) -> None:
    """
    Display detailed information for each trade in the table.
    
    Args:
        arrow_table: Arrow table containing trade data
    """
    print("\nTrade Details:")
    for row_index in range(arrow_table.num_rows):
        trade_details = extract_trade_details(arrow_table, row_index)
        print_trade_summary(trade_details)


def main():
    """Main execution function."""
    # Create individual Arrow arrays
    trade_ids_array, symbols_array, prices_array, quantities_array = create_individual_arrays(
        SAMPLE_TRADE_IDS,
        SAMPLE_SYMBOLS,
        SAMPLE_PRICES,
        SAMPLE_QUANTITIES
    )
    
    # Combine arrays into a table
    trades_table = combine_arrays_into_table(
        trade_ids_array,
        symbols_array,
        prices_array,
        quantities_array
    )
    
    # Display table information
    display_table_from_arrays(trades_table)
    
    # Display individual trade details
    display_trade_details(trades_table)


if __name__ == "__main__":
    main()