# Apache Arrow Fundamentals

This directory contains fundamental examples to get started with Apache Arrow. These examples cover the basics of working with Arrow data structures.

## Prerequisites

- Python 3.12+
- pyarrow installed: `pip install pyarrow`
- Basic Python knowledge

## Examples

### 1. `arrow_array.py`
**Difficulty**: 🟢 Beginner  
**Time**: 5 minutes  
**What you'll learn**: Creating basic Arrow arrays from Python lists

```bash
python3 arrow_array.py
```

### 2. `arrow_arrays.py`
**Difficulty**: 🟢 Beginner  
**Time**: 5 minutes  
**What you'll learn**: Working with multiple Arrow arrays

```bash
python3 arrow_arrays.py
```

### 3. `arrow_table.py`
**Difficulty**: 🟢 Beginner  
**Time**: 5 minutes  
**What you'll learn**: Creating Arrow tables (multi-column data structures)

```bash
python3 arrow_table.py
```

### 4. `arrow_multiple_arrays.py`
**Difficulty**: 🟢 Beginner  
**Time**: 5 minutes  
**What you'll learn**: Creating tables from multiple arrays

```bash
python3 arrow_multiple_arrays.py
```

### 5. `arrow_python_dictionary.py`
**Difficulty**: 🟢 Beginner  
**Time**: 5 minutes  
**What you'll learn**: Converting Python dictionaries to Arrow tables

```bash
python3 arrow_python_dictionary.py
```

### 6. `arrow_tables_to_pandas_data_frame.py`
**Difficulty**: 🟢 Beginner  
**Time**: 5 minutes  
**What you'll learn**: Converting Arrow tables to Pandas DataFrames (zero-copy)

```bash
python3 arrow_tables_to_pandas_data_frame.py
```

### 7. `arrow_slice.py`
**Difficulty**: 🟢 Beginner  
**Time**: 5 minutes  
**What you'll learn**: Slicing Arrow arrays and tables

```bash
python3 arrow_slice.py
```

### 8. `arrow_filtering_metadata.py`
**Difficulty**: 🟡 Intermediate  
**Time**: 10 minutes  
**What you'll learn**: Filtering data and working with metadata

```bash
python3 arrow_filtering_metadata.py
```

## Learning Order

We recommend following this order:

1. Start with `arrow_array.py` - understand basic Arrow arrays
2. Then `arrow_table.py` - learn about multi-column structures
3. `arrow_python_dictionary.py` - convert from common Python structures
4. `arrow_tables_to_pandas_data_frame.py` - learn conversions
5. `arrow_slice.py` - data manipulation
6. `arrow_filtering_metadata.py` - more advanced operations

## Key Concepts

- **Arrow Arrays**: Single-column data structures
- **Arrow Tables**: Multi-column data structures (like DataFrames)
- **Zero-Copy**: Conversions that don't duplicate data in memory
- **Type Safety**: Arrow preserves data types across conversions

## Next Steps

After completing these fundamentals:
- Move to `../basic_analytics/` for analytics operations
- Or jump to `../arrow_in_action/` for real-world examples

