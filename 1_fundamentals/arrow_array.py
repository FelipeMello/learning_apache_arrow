"""
Investment Banking Example: Creating Arrow Arrays

Demonstrates basic Arrow array creation with trade prices.
This is the foundation for working with Apache Arrow - arrays are the
building blocks for all Arrow data structures.

Key Concepts:
- Arrow arrays are columnar data structures optimized for analytics
- They support zero-copy operations and efficient memory usage
- Type information is preserved and can be explicitly specified
"""
import pyarrow as pa
from _helpers import format_currency, print_section_header

# Sample trade prices in USD
# In a real scenario, these would come from market data feeds
SAMPLE_TRADE_PRICES = [125.50, 234.75, 189.25, 312.00, 156.80]

def create_trade_prices_array(prices: list) -> pa.Array:
    """
    Create an Arrow array from a list of trade prices.
    
    Args:
        prices: List of trade prices (floats)
        
    Returns:
        Arrow array containing the trade prices
    """
    return pa.array(prices, type=pa.float64())


def display_array_info(arrow_array: pa.Array, title: str) -> None:
    """
    Display information about an Arrow array.
    
    Args:
        arrow_array: The Arrow array to display
        title: Title for the display section
    """
    print_section_header(title, width=50)
    print(f"Arrow Array: {arrow_array}")
    print(f"Data Type: {arrow_array.type}")
    print(f"Array Length: {len(arrow_array)}")
    print(f"Null Count: {arrow_array.null_count}")


def display_trade_prices(arrow_array: pa.Array) -> None:
    """
    Display formatted trade prices from an Arrow array.
    
    Args:
        arrow_array: Arrow array containing trade prices
    """
    print("\nTrade Prices (USD):")
    for index, price_scalar in enumerate(arrow_array, start=1):
        price_value = price_scalar.as_py()
        print(f"  Trade {index}: {format_currency(price_value)}")


def main():
    """Main execution function."""
    # Create Arrow array from sample prices
    trade_prices_array = create_trade_prices_array(SAMPLE_TRADE_PRICES)
    
    # Display array information
    display_array_info(trade_prices_array, "Investment Banking: Trade Prices Array")
    
    # Display formatted prices
    display_trade_prices(trade_prices_array)


if __name__ == "__main__":
    main()