"""
Helper Functions for Basic Analytics Examples
Reusable utilities following DRY principles
"""

import pyarrow as pa
import pyarrow.compute as pc
import pandas as pd
from typing import Dict, Any


def calculate_statistics(arrow_table: pa.Table, column_name: str) -> Dict[str, float]:
    """
    Calculate comprehensive statistics for a numeric column.
    
    Args:
        arrow_table: Arrow table containing the data
        column_name: Name of the column to analyze
        
    Returns:
        Dictionary with statistical measures (mean, max, min, sum)
    """
    column_array = arrow_table[column_name]
    
    return {
        'mean': pc.mean(column_array).as_py(),
        'max': pc.max(column_array).as_py(),
        'min': pc.min(column_array).as_py(),
        'sum': pc.sum(column_array).as_py()
    }


def filter_table_by_threshold(arrow_table: pa.Table, column_name: str, 
                              threshold: float, comparison: str = 'greater') -> pa.Table:
    """
    Filter an Arrow table based on a column threshold.
    
    Args:
        arrow_table: Arrow table to filter
        column_name: Name of the column to filter on
        threshold: Threshold value for comparison
        comparison: Type of comparison ('greater', 'less', 'equal')
        
    Returns:
        Filtered Arrow table
    """
    column_array = arrow_table[column_name]
    threshold_scalar = pa.scalar(threshold)
    
    if comparison == 'greater':
        mask = pc.greater(column_array, threshold_scalar)
    elif comparison == 'less':
        mask = pc.less(column_array, threshold_scalar)
    elif comparison == 'equal':
        mask = pc.equal(column_array, threshold_scalar)
    else:
        raise ValueError(f"Unknown comparison type: {comparison}")
    
    return pc.filter(arrow_table, mask)


def group_by_sector(dataframe: pd.DataFrame, value_column: str = 'trade_value') -> pd.DataFrame:
    """
    Group trading data by sector and calculate aggregations.
    
    Args:
        dataframe: Pandas DataFrame with sector and value columns
        value_column: Name of the column to aggregate
        
    Returns:
        DataFrame with sector-level aggregations
    """
    return dataframe.groupby('sector')[value_column].agg(['mean', 'sum', 'count'])


def format_currency(amount: float) -> str:
    """
    Format a monetary value as currency string.
    
    Args:
        amount: Monetary value to format
        
    Returns:
        Formatted currency string
    """
    return f"${amount:,.2f}"


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

