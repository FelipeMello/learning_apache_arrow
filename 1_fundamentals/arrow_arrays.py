"""
Investment Banking Example: Multiple Arrow Arrays

Demonstrates working with different data types in Arrow arrays.
Arrow supports various data types optimized for different use cases:
- Integers: For counts, IDs, quantities
- Floats: For prices, percentages, measurements
- Strings: For symbols, names, categories

Key Concepts:
- Each array has a specific type that determines storage and operations
- Type safety ensures data integrity
- Different types can be combined into tables
"""
import pyarrow as pa
from _helpers import calculate_trade_value, format_currency, print_section_header
from _constants import STOCK_SYMBOLS

# Sample trading data - in production, this would come from a database or API
SAMPLE_QUANTITIES = [100, 500, 1000]
SAMPLE_SYMBOLS = STOCK_SYMBOLS[:3]  # First 3 symbols
SAMPLE_PRICES = [175.50, 378.25, 142.75]


def create_trading_arrays(quantities: list, symbols: list, prices: list) -> tuple:
    """
    Create Arrow arrays for trading data.
    
    Args:
        quantities: List of trade quantities (integers)
        symbols: List of stock symbols (strings)
        prices: List of trade prices (floats)
        
    Returns:
        Tuple of (quantities_array, symbols_array, prices_array)
    """
    quantities_array = pa.array(quantities, type=pa.int32())
    symbols_array = pa.array(symbols, type=pa.string())
    prices_array = pa.array(prices, type=pa.float64())
    
    return quantities_array, symbols_array, prices_array


def display_arrays_info(quantities: pa.Array, symbols: pa.Array, prices: pa.Array) -> None:
    """
    Display information about multiple Arrow arrays.
    
    Args:
        quantities: Arrow array of trade quantities
        symbols: Arrow array of stock symbols
        prices: Arrow array of trade prices
    """
    print_section_header("Investment Banking: Multiple Data Types", width=50)
    
    print("Trade Quantities (shares):")
    print(f"  {quantities}")
    print(f"  Type: {quantities.type}, Length: {len(quantities)}")
    
    print("\nStock Symbols:")
    print(f"  {symbols}")
    print(f"  Type: {symbols.type}, Length: {len(symbols)}")
    
    print("\nTrade Prices (USD):")
    print(f"  {prices}")
    print(f"  Type: {prices.type}, Length: {len(prices)}")


def display_trading_summary(quantities: pa.Array, symbols: pa.Array, prices: pa.Array) -> None:
    """
    Display a formatted summary of trades combining all arrays.
    
    Args:
        quantities: Arrow array of trade quantities
        symbols: Arrow array of stock symbols
        prices: Arrow array of trade prices
    """
    print_section_header("Trading Summary", width=50)
    
    # Ensure all arrays have the same length
    array_length = min(len(quantities), len(symbols), len(prices))
    
    for index in range(array_length):
        symbol = symbols[index].as_py()
        quantity = quantities[index].as_py()
        price = prices[index].as_py()
        total_value = calculate_trade_value(price, quantity)
        
        print(f"  {symbol}: {quantity:,} shares @ {format_currency(price)} = {format_currency(total_value)}")


def main():
    """Main execution function."""
    # Create Arrow arrays from sample data
    quantities_array, symbols_array, prices_array = create_trading_arrays(
        SAMPLE_QUANTITIES, 
        SAMPLE_SYMBOLS, 
        SAMPLE_PRICES
    )
    
    # Display array information
    display_arrays_info(quantities_array, symbols_array, prices_array)
    
    # Display combined trading summary
    display_trading_summary(quantities_array, symbols_array, prices_array)


if __name__ == "__main__":
    main()