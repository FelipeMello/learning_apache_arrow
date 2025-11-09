"""
Investment Banking Example: Slicing Arrow Arrays

Demonstrates extracting subsets of data using array slicing.
Slicing is a zero-copy operation in Arrow, making it very efficient
for working with large datasets.

Key Concepts:
- Slicing creates views, not copies (zero-copy operation)
- Can slice by start index and length, or use negative indices
- Useful for windowing operations, pagination, and data sampling
- Maintains the same data type and structure
"""
import pyarrow as pa
import pyarrow.compute as pc
from _helpers import format_currency, print_section_header

# Sample portfolio values in thousands of USD
# In production, this would come from portfolio management systems
SAMPLE_PORTFOLIO_VALUES = [1250, 2340, 1890, 3120, 1568, 2890, 2100]


def create_portfolio_array(values: list) -> pa.Array:
    """
    Create an Arrow array from portfolio values.
    
    Args:
        values: List of portfolio values
        
    Returns:
        Arrow array containing portfolio values
    """
    return pa.array(values, type=pa.float64())


def slice_array(arrow_array: pa.Array, start: int, length: int = None) -> pa.Array:
    """
    Slice an Arrow array starting from a given index.
    
    Args:
        arrow_array: The Arrow array to slice
        start: Starting index (can be negative for reverse indexing)
        length: Number of elements to include (None for all remaining)
        
    Returns:
        Sliced Arrow array (zero-copy view)
        
    Note:
        Arrow's slice() method doesn't support negative indices directly.
        This function converts negative indices to positive ones.
    """
    array_length = len(arrow_array)
    
    # Convert negative start index to positive
    if start < 0:
        start = array_length + start
        # Ensure start is not negative after conversion
        if start < 0:
            start = 0
    
    # Ensure start is within bounds
    if start > array_length:
        start = array_length
    
    # If length is None, slice to the end
    if length is None:
        return arrow_array.slice(start)
    
    # Ensure length doesn't exceed available elements
    max_length = array_length - start
    if length > max_length:
        length = max_length
    
    return arrow_array.slice(start, length)


def calculate_array_sum(arrow_array: pa.Array) -> float:
    """
    Calculate the sum of values in an Arrow array.
    
    Args:
        arrow_array: Arrow array containing numeric values
        
    Returns:
        Sum of all values in the array
    """
    return pc.sum(arrow_array).as_py()


def display_slicing_examples(portfolio_array: pa.Array) -> None:
    """
    Display various slicing examples on a portfolio array.
    
    Args:
        portfolio_array: Arrow array containing portfolio values
    """
    print_section_header("Investment Banking: Portfolio Values Slicing", width=50)
    
    print("Original Portfolio Values (USD thousands):")
    print(f"  {portfolio_array}")
    print(f"  Length: {len(portfolio_array)}")
    
    # Slice from index 1, length 3 (indices 1, 2, 3)
    sliced_middle = slice_array(portfolio_array, start=1, length=3)
    print(f"\nSliced Array (indices 1-3, length 3):")
    print(f"  {sliced_middle}")
    
    # Slice first 3 values
    first_three = slice_array(portfolio_array, start=0, length=3)
    print(f"\nFirst 3 values:")
    print(f"  {first_three}")
    
    # Slice last 3 values using negative indexing
    last_three = slice_array(portfolio_array, start=-3)
    print(f"\nLast 3 values (negative index):")
    print(f"  {last_three}")


def display_portfolio_analysis(original_array: pa.Array, sliced_array: pa.Array) -> None:
    """
    Display analysis comparing original and sliced portfolio arrays.
    
    Args:
        original_array: Original portfolio array
        sliced_array: Sliced portfolio array
    """
    print_section_header("Portfolio Analysis", width=50)
    
    original_count = len(original_array)
    sliced_count = len(sliced_array)
    original_total = calculate_array_sum(original_array)
    sliced_total = calculate_array_sum(sliced_array)
    
    print(f"Portfolio Count:")
    print(f"  Original: {original_count} portfolios")
    print(f"  Sliced:   {sliced_count} portfolios")
    
    print(f"\nTotal Portfolio Value:")
    print(f"  Original: {format_currency(original_total * 1000)} (${original_total:,.0f}K)")
    print(f"  Sliced:   {format_currency(sliced_total * 1000)} (${sliced_total:,.0f}K)")
    
    if original_count > 0:
        percentage = (sliced_count / original_count) * 100
        print(f"\nSliced represents {percentage:.1f}% of original portfolios")


def main():
    """Main execution function."""
    # Create portfolio array
    portfolio_array = create_portfolio_array(SAMPLE_PORTFOLIO_VALUES)
    
    # Display slicing examples
    display_slicing_examples(portfolio_array)
    
    # Display analysis
    sliced_array = slice_array(portfolio_array, start=1, length=3)
    display_portfolio_analysis(portfolio_array, sliced_array)


if __name__ == "__main__":
    main()
