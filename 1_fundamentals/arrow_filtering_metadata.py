"""
Investment Banking Example: Filtering and Metadata

Demonstrates filtering trading data and accessing array metadata.
Filtering is a core operation in data analysis, and Arrow provides
efficient, vectorized filtering operations.

Key Concepts:
- Boolean masks define which elements to keep
- Filtering operations are vectorized and efficient
- Array metadata provides information about structure and content
- Multiple conditions can be combined using logical operators
"""
import pyarrow as pa
import pyarrow.compute as pc
from _helpers import format_currency, print_section_header
from _constants import HIGH_VALUE_THRESHOLD

# Sample trade prices in USD
SAMPLE_TRADE_PRICES = [125.50, 234.75, 189.25, 312.00, 156.80, 280.50, 95.30]

# Filter thresholds
HIGH_PRICE_THRESHOLD = 200.0
MID_RANGE_MIN = 150.0
MID_RANGE_MAX = 250.0


def create_trade_prices_array(prices: list) -> pa.Array:
    """
    Create an Arrow array from trade prices.
    
    Args:
        prices: List of trade prices
        
    Returns:
        Arrow array containing trade prices
    """
    return pa.array(prices, type=pa.float64())


def create_filter_mask(arrow_array: pa.Array, threshold: float, 
                      comparison: str = 'greater') -> pa.Array:
    """
    Create a boolean mask for filtering based on a threshold.
    
    Args:
        arrow_array: Arrow array to filter
        threshold: Threshold value for comparison
        comparison: Type of comparison ('greater', 'less', 'equal')
        
    Returns:
        Boolean Arrow array (mask) indicating which elements pass the filter
    """
    threshold_scalar = pa.scalar(threshold)
    
    if comparison == 'greater':
        return pc.greater(arrow_array, threshold_scalar)
    elif comparison == 'less':
        return pc.less(arrow_array, threshold_scalar)
    elif comparison == 'equal':
        return pc.equal(arrow_array, threshold_scalar)
    else:
        raise ValueError(f"Unknown comparison type: {comparison}")


def apply_filter(arrow_array: pa.Array, mask: pa.Array) -> pa.Array:
    """
    Apply a boolean mask to filter an Arrow array.
    
    Args:
        arrow_array: Arrow array to filter
        mask: Boolean mask indicating which elements to keep
        
    Returns:
        Filtered Arrow array containing only elements where mask is True
    """
    return pc.filter(arrow_array, mask)


def display_array_metadata(arrow_array: pa.Array) -> None:
    """
    Display comprehensive metadata about an Arrow array.
    
    Args:
        arrow_array: Arrow array to analyze
    """
    print_section_header("Array Metadata", width=50)
    
    print(f"Data Type: {arrow_array.type}")
    print(f"Array Length: {len(arrow_array)}")
    print(f"Null Count: {arrow_array.null_count}")
    
    # Check if array supports nulls (has null bitmap)
    # Arrays with null_count > 0 or that can have nulls will have a null bitmap buffer
    buffers = arrow_array.buffers()
    has_null_bitmap = buffers is not None and len(buffers) > 0 and buffers[0] is not None
    print(f"Has Null Bitmap: {has_null_bitmap}")
    print(f"Number of Buffers: {len(buffers) if buffers else 0}")


def display_filtering_results(original_array: pa.Array, filtered_array: pa.Array, 
                             filter_description: str) -> None:
    """
    Display results of a filtering operation.
    
    Args:
        original_array: Original unfiltered array
        filtered_array: Filtered array
        filter_description: Description of the filter applied
    """
    print(f"\n{filter_description}:")
    print(f"  {filtered_array}")
    print(f"  Original count: {len(original_array)}")
    print(f"  Filtered count: {len(filtered_array)}")
    
    if len(original_array) > 0:
        percentage = (len(filtered_array) / len(original_array)) * 100
        print(f"  Percentage kept: {percentage:.1f}%")


def create_range_filter_mask(arrow_array: pa.Array, min_value: float, 
                             max_value: float) -> pa.Array:
    """
    Create a boolean mask for values within a range.
    
    Args:
        arrow_array: Arrow array to filter
        min_value: Minimum value (inclusive)
        max_value: Maximum value (inclusive)
        
    Returns:
        Boolean mask for values in the specified range
    """
    min_mask = pc.greater_equal(arrow_array, pa.scalar(min_value))
    max_mask = pc.less_equal(arrow_array, pa.scalar(max_value))
    return pc.and_(min_mask, max_mask)


def count_matching_elements(mask: pa.Array) -> int:
    """
    Count the number of True values in a boolean mask.
    
    Args:
        mask: Boolean Arrow array
        
    Returns:
        Number of True values in the mask
    """
    return pc.sum(mask.cast(pa.int64())).as_py()


def main():
    """Main execution function."""
    # Create trade prices array
    trade_prices_array = create_trade_prices_array(SAMPLE_TRADE_PRICES)
    
    print_section_header("Investment Banking: Filtering and Metadata", width=50)
    print("Original Trade Prices:")
    print(f"  {trade_prices_array}")
    
    # Filter high-value trades
    high_value_mask = create_filter_mask(trade_prices_array, HIGH_PRICE_THRESHOLD, 'greater')
    filtered_high_value = apply_filter(trade_prices_array, high_value_mask)
    display_filtering_results(
        trade_prices_array, 
        filtered_high_value, 
        f"Filtered Array (prices > {format_currency(HIGH_PRICE_THRESHOLD)})"
    )
    
    # Display array metadata
    display_array_metadata(trade_prices_array)
    
    # Additional filtering examples
    print_section_header("Additional Filtering Examples", width=50)
    
    # Filter mid-range prices
    mid_range_mask = create_range_filter_mask(trade_prices_array, MID_RANGE_MIN, MID_RANGE_MAX)
    filtered_mid_range = apply_filter(trade_prices_array, mid_range_mask)
    display_filtering_results(
        trade_prices_array,
        filtered_mid_range,
        f"Mid-range prices ({format_currency(MID_RANGE_MIN)} - {format_currency(MID_RANGE_MAX)})"
    )
    
    # Count high-value trades
    high_value_count = count_matching_elements(high_value_mask)
    print(f"\nHigh-value trades count: {high_value_count}")


if __name__ == "__main__":
    main()