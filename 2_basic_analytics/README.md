# Basic Analytics with Apache Arrow

Learn how to perform analytics operations using Apache Arrow's compute functions.

## Prerequisites

- Completed `../fundamentals/` examples
- Python 3.12+
- pyarrow installed
- Basic understanding of Arrow tables

## Example

### `basic_analytics.py`
**Difficulty**: 🟡 Intermediate  
**Time**: 15 minutes  
**What you'll learn**: 
- Using `pyarrow.compute` for analytics
- Filtering data with Arrow compute
- Computing statistics (mean, sum, etc.)
- Combining Arrow compute with Pandas for complex operations

```bash
python3 basic_analytics.py
```

## Key Operations Demonstrated

1. **Filtering**: Using `pc.filter()` to select rows based on conditions
2. **Aggregations**: Computing mean, sum, and other statistics
3. **Grouping**: Combining Arrow with Pandas for groupby operations
4. **Performance**: Fast vectorized operations

## Arrow Compute Functions

Common compute functions used:
- `pc.greater()` - Compare values
- `pc.filter()` - Filter rows
- `pc.mean()` - Calculate mean
- `pc.sum()` - Calculate sum
- `pc.min()` / `pc.max()` - Min/max values

## When to Use Arrow Compute vs Pandas

- **Use Arrow Compute** for:
  - Simple filtering and aggregations
  - Performance-critical operations
  - Large datasets

- **Use Pandas** for:
  - Complex groupby operations
  - Custom transformations
  - When you need Pandas-specific features

## Next Steps

- Try `../arrow_in_action/` for real-world examples
- Explore `../financial_analysis/` for complex analytics

