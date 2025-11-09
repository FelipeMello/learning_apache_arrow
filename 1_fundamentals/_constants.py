"""
Shared Constants for Investment Banking Examples
Centralized configuration to follow DRY principles
"""

# Stock symbols commonly used in examples
STOCK_SYMBOLS = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN', 'NVDA', 'META', 'JPM', 'BAC', 'GS']

# Industry sectors
SECTORS = ['Technology', 'Finance', 'Energy', 'Consumer', 'Healthcare', 'Industrial', 'Utilities']

# Trade types
TRADE_TYPES = ['BUY', 'SELL']

# Price ranges for realistic data generation
MIN_STOCK_PRICE = 50.0
MAX_STOCK_PRICE = 500.0

# Quantity ranges
MIN_QUANTITY = 10
MAX_QUANTITY = 10000

# Trade value thresholds
HIGH_VALUE_THRESHOLD = 200000.0
VERY_HIGH_VALUE_THRESHOLD = 4000000.0

# Display formatting
CURRENCY_FORMAT = '${:,.2f}'
PERCENTAGE_FORMAT = '{:.2f}%'
SEPARATOR_LINE = "=" * 60

