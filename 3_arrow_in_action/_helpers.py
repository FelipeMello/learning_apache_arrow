"""
Helper Functions for Arrow in Action Examples
Reusable utilities following DRY principles
"""

import pyarrow as pa
import pyarrow.compute as pc
import pandas as pd
import time
from typing import Dict, Any, Tuple
from datetime import datetime, timedelta
import numpy as np


def generate_trading_dataframe(num_trades: int, symbols: list, sectors: list = None,
                               trade_types: list = None, include_dates: bool = False) -> pd.DataFrame:
    """
    Generate a realistic trading DataFrame for testing.
    
    Args:
        num_trades: Number of trades to generate
        symbols: List of stock symbols to use
        sectors: List of sectors (optional, defaults to common sectors)
        trade_types: List of trade types (optional, defaults to BUY/SELL)
        include_dates: Whether to include trade dates
        
    Returns:
        Pandas DataFrame with trading data
    """
    if sectors is None:
        sectors = ['Technology', 'Finance', 'Energy', 'Consumer', 'Healthcare']
    if trade_types is None:
        trade_types = ['BUY', 'SELL']
    
    data = {
        'trade_id': range(1, num_trades + 1),
        'symbol': np.random.choice(symbols, size=num_trades),
        'price': np.random.uniform(50, 500, size=num_trades).round(2),
        'quantity': np.random.randint(10, 10000, size=num_trades),
        'sector': np.random.choice(sectors, size=num_trades),
        'trade_type': np.random.choice(trade_types, size=num_trades)
    }
    
    if include_dates:
        data['trade_date'] = [
            datetime.now() - timedelta(days=np.random.randint(0, 365))
            for _ in range(num_trades)
        ]
    
    df = pd.DataFrame(data)
    df['trade_value'] = df['price'] * df['quantity']
    
    return df


def convert_dataframe_to_arrow(dataframe: pd.DataFrame) -> Tuple[pa.Table, float]:
    """
    Convert a Pandas DataFrame to an Arrow Table and measure conversion time.
    
    Args:
        dataframe: Pandas DataFrame to convert
        
    Returns:
        Tuple of (Arrow table, conversion time in seconds)
    """
    start_time = time.time()
    arrow_table = pa.Table.from_pandas(dataframe)
    conversion_time = time.time() - start_time
    
    return arrow_table, conversion_time


def filter_high_value_trades(arrow_table: pa.Table, threshold: float) -> Tuple[pa.Table, float]:
    """
    Filter trades above a value threshold and measure filtering time.
    
    Args:
        arrow_table: Arrow table containing trade data
        threshold: Minimum trade value threshold
        
    Returns:
        Tuple of (filtered table, filtering time in seconds)
    """
    start_time = time.time()
    mask = pc.greater(arrow_table['trade_value'], pa.scalar(threshold))
    filtered_table = pc.filter(arrow_table, mask)
    filter_time = time.time() - start_time
    
    return filtered_table, filter_time


def calculate_trade_statistics(arrow_table: pa.Table) -> Tuple[Dict[str, float], float]:
    """
    Calculate statistics on trade values and measure computation time.
    
    Args:
        arrow_table: Arrow table containing trade data
        
    Returns:
        Tuple of (statistics dictionary, computation time in seconds)
    """
    start_time = time.time()
    
    statistics = {
        'total': pc.sum(arrow_table['trade_value']).as_py(),
        'average': pc.mean(arrow_table['trade_value']).as_py(),
        'maximum': pc.max(arrow_table['trade_value']).as_py(),
        'minimum': pc.min(arrow_table['trade_value']).as_py()
    }
    
    computation_time = time.time() - start_time
    
    return statistics, computation_time


def format_memory_usage(bytes_value: int, unit: str = 'MB') -> str:
    """
    Format memory usage in a human-readable format.
    
    Args:
        bytes_value: Memory usage in bytes
        unit: Target unit ('KB', 'MB', 'GB')
        
    Returns:
        Formatted memory usage string
    """
    if unit == 'KB':
        return f"{bytes_value / 1024:.2f} KB"
    elif unit == 'MB':
        return f"{bytes_value / (1024**2):.2f} MB"
    elif unit == 'GB':
        return f"{bytes_value / (1024**3):.2f} GB"
    else:
        return f"{bytes_value} bytes"


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

