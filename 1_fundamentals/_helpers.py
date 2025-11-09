"""
Helper Functions for Investment Banking Examples
Reusable utilities to follow DRY principles
"""

from typing import List, Tuple
import pyarrow as pa


def calculate_trade_value(price: float, quantity: int) -> float:
    """
    Calculate the total value of a trade.
    
    Args:
        price: Price per share
        quantity: Number of shares
        
    Returns:
        Total trade value (price * quantity)
    """
    return price * quantity


def format_currency(amount: float) -> str:
    """
    Format a monetary value as currency string.
    
    Args:
        amount: Monetary value to format
        
    Returns:
        Formatted currency string (e.g., "$1,234.56")
    """
    return f"${amount:,.2f}"


def format_percentage(value: float) -> str:
    """
    Format a value as percentage string.
    
    Args:
        value: Percentage value to format
        
    Returns:
        Formatted percentage string (e.g., "12.34%")
    """
    return f"{value:.2f}%"


def print_section_header(title: str, separator: str = "=", width: int = 60) -> None:
    """
    Print a formatted section header.
    
    Args:
        title: Section title to display
        separator: Character to use for separator line
        width: Width of the separator line
    """
    separator_line = separator * width
    print(f"\n{separator_line}")
    print(title)
    print(separator_line)


def extract_trade_details(arrow_table: pa.Table, row_index: int) -> dict:
    """
    Extract trade details from an Arrow table row.
    
    Args:
        arrow_table: Arrow table containing trade data
        row_index: Index of the row to extract
        
    Returns:
        Dictionary with trade details (symbol, price, quantity, etc.)
    """
    trade_details = {}
    
    # Extract each column value safely
    for column_name in arrow_table.column_names:
        try:
            value = arrow_table[column_name][row_index]
            # Convert Arrow scalar to Python value
            trade_details[column_name] = value.as_py() if hasattr(value, 'as_py') else value
        except (IndexError, KeyError):
            trade_details[column_name] = None
    
    return trade_details


def print_trade_summary(trade_details: dict) -> None:
    """
    Print a formatted trade summary.
    
    Args:
        trade_details: Dictionary containing trade information
    """
    symbol = trade_details.get('symbol', 'N/A')
    quantity = trade_details.get('quantity', 0)
    price = trade_details.get('price', 0.0)
    trade_value = calculate_trade_value(price, quantity)
    trade_type = trade_details.get('trade_type', '')
    trade_id = trade_details.get('trade_id', 'N/A')
    
    # Format trade type if present
    trade_type_str = f"{trade_type:4s} " if trade_type else ""
    
    print(f"  {trade_type_str}Trade {trade_id}: {quantity:,} {symbol} @ {format_currency(price)} = {format_currency(trade_value)}")

