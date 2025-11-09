"""
Investment Banking Example: Loading Arrow Table from Feather File

Demonstrates fast loading of trading data from Feather format.
Feather files can be loaded quickly with minimal overhead, making them
ideal for data persistence and sharing between applications.

Key Concepts:
- Fast deserialization with minimal overhead
- Zero-copy operations when possible
- Schema preservation for type safety
- Immediate availability for analysis
"""
import pyarrow as pa
import pyarrow.feather as feather
import pyarrow.compute as pc
import pandas as pd
from _helpers import format_currency, print_section_header
from typing import Optional

# Input file name
INPUT_FEATHER_FILE = 'trading_data.feather'


def load_feather_file(filename: str) -> Optional[pa.Table]:
    """
    Load an Arrow table from a Feather file.
    
    Args:
        filename: Path to the Feather file
        
    Returns:
        Arrow table loaded from the file, or None if file not found
    """
    try:
        return feather.read_table(filename)
    except FileNotFoundError:
        return None


def display_loaded_table_info(arrow_table: pa.Table) -> None:
    """
    Display information about the loaded Arrow table.
    
    Args:
        arrow_table: Arrow table that was loaded
    """
    print(f"\n✓ Loaded Arrow Table:")
    print(f"  Rows: {arrow_table.num_rows}")
    print(f"  Columns: {arrow_table.num_columns}")
    print(f"  Schema: {arrow_table.schema}")


def display_loaded_data(arrow_table: pa.Table) -> None:
    """
    Display the loaded trading data.
    
    Args:
        arrow_table: Arrow table containing the data
    """
    # Convert to Pandas for easier display
    dataframe = arrow_table.to_pandas()
    
    print("\nLoaded Trading Data:")
    print(dataframe)


def perform_quick_analysis(arrow_table: pa.Table) -> None:
    """
    Perform quick statistical analysis on loaded data.
    
    Args:
        arrow_table: Arrow table containing trade data
    """
    if 'trade_value' not in arrow_table.column_names:
        return
    
    total_value = pc.sum(arrow_table['trade_value']).as_py()
    avg_value = pc.mean(arrow_table['trade_value']).as_py()
    max_value = pc.max(arrow_table['trade_value']).as_py()
    min_value = pc.min(arrow_table['trade_value']).as_py()
    
    print("\nQuick Analysis:")
    print(f"  Total Trade Value:   {format_currency(total_value)}")
    print(f"  Average Trade Value: {format_currency(avg_value)}")
    print(f"  Maximum Trade Value: {format_currency(max_value)}")
    print(f"  Minimum Trade Value: {format_currency(min_value)}")


def display_feather_benefits() -> None:
    """Display benefits of using Feather format."""
    print_section_header("Benefits of Feather Format", width=60)
    print("  ✓ Fast loading - no manual serialization needed")
    print("  ✓ Zero-copy operations")
    print("  ✓ Cross-language compatible")
    print("  ✓ Efficient storage format")
    print("  ✓ Schema preservation")


def display_file_not_found_error(filename: str) -> None:
    """
    Display error message when file is not found.
    
    Args:
        filename: Name of the file that was not found
    """
    print(f"\n⚠ File '{filename}' not found.")
    print("  Please run 'arrow_table_to_feather_file.py' first to create the file.")


def main():
    """Main execution function."""
    print_section_header("Investment Banking: Loading from Feather Format", width=60)
    
    # Load Feather file
    loaded_table = load_feather_file(INPUT_FEATHER_FILE)
    
    if loaded_table is None:
        display_file_not_found_error(INPUT_FEATHER_FILE)
        return
    
    # Display loaded table information
    display_loaded_table_info(loaded_table)
    
    # Display loaded data
    display_loaded_data(loaded_table)
    
    # Perform quick analysis
    perform_quick_analysis(loaded_table)
    
    # Display benefits
    display_feather_benefits()


if __name__ == "__main__":
    main()