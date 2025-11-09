"""
Investment Banking Example: Converting Arrow Table to Pandas DataFrame

Demonstrates zero-copy conversion between Arrow and Pandas.
This interoperability is one of Arrow's key features - you can work
with the same data in different tools without expensive conversions.

Key Concepts:
- Arrow to Pandas conversion is zero-copy when possible
- Pandas provides rich data manipulation capabilities
- Can seamlessly switch between Arrow and Pandas as needed
- Arrow is optimized for analytics, Pandas for data manipulation
"""
import pyarrow as pa
import pandas as pd
from _helpers import calculate_trade_value, print_section_header
from _constants import STOCK_SYMBOLS

# Sample trading data
SAMPLE_TRADING_DATA = {
    'trade_id': [1, 2, 3],
    'symbol': STOCK_SYMBOLS[:3],
    'price': [175.50, 378.25, 142.75],
    'quantity': [100, 500, 1000]
}


def create_trading_table(trading_data: dict) -> pa.Table:
    """
    Create an Arrow table from trading data.
    
    Args:
        trading_data: Dictionary with column names and data lists
        
    Returns:
        Arrow table containing the trading data
    """
    return pa.table(trading_data)


def convert_to_pandas(arrow_table: pa.Table) -> pd.DataFrame:
    """
    Convert Arrow table to Pandas DataFrame (zero-copy when possible).
    
    Args:
        arrow_table: Arrow table to convert
        
    Returns:
        Pandas DataFrame with the same data
    """
    return arrow_table.to_pandas()


def add_calculated_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Add calculated columns to a DataFrame.
    
    Args:
        dataframe: Pandas DataFrame with price and quantity columns
        
    Returns:
        DataFrame with additional calculated columns
    """
    dataframe = dataframe.copy()  # Avoid modifying original
    dataframe['trade_value'] = dataframe.apply(
        lambda row: calculate_trade_value(row['price'], row['quantity']),
        axis=1
    )
    return dataframe


def display_conversion_info(arrow_table: pa.Table, pandas_df: pd.DataFrame) -> None:
    """
    Display information about Arrow to Pandas conversion.
    
    Args:
        arrow_table: Original Arrow table
        pandas_df: Converted Pandas DataFrame
    """
    print_section_header("Investment Banking: Arrow to Pandas Conversion", width=50)
    
    print("\nArrow Table:")
    print(arrow_table)
    print(f"  Rows: {arrow_table.num_rows}, Columns: {arrow_table.num_columns}")
    
    print("\nPandas DataFrame:")
    print(pandas_df)
    print(f"\nDataFrame Information:")
    print(f"  Shape: {pandas_df.shape}")
    print(f"  Data Types:")
    for column, dtype in pandas_df.dtypes.items():
        print(f"    {column}: {dtype}")


def display_enhanced_dataframe(dataframe: pd.DataFrame) -> None:
    """
    Display DataFrame with calculated columns.
    
    Args:
        dataframe: Pandas DataFrame with calculated columns
    """
    print("\nDataFrame with Calculated Trade Values:")
    print(dataframe)
    print(f"\nSummary Statistics:")
    print(f"  Total Trade Value: ${dataframe['trade_value'].sum():,.2f}")
    print(f"  Average Trade Value: ${dataframe['trade_value'].mean():,.2f}")
    print(f"  Number of Trades: {len(dataframe)}")


def main():
    """Main execution function."""
    # Create Arrow table
    arrow_table = create_trading_table(SAMPLE_TRADING_DATA)
    
    # Convert to Pandas DataFrame
    pandas_df = convert_to_pandas(arrow_table)
    
    # Display conversion information
    display_conversion_info(arrow_table, pandas_df)
    
    # Add calculated columns
    enhanced_df = add_calculated_columns(pandas_df)
    
    # Display enhanced DataFrame
    display_enhanced_dataframe(enhanced_df)


if __name__ == "__main__":
    main()