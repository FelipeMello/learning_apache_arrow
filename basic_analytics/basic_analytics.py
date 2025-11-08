import pyarrow as pa
import pyarrow.compute as pc


# Basic Analytics with Apache Arrow
# Let’s start with some basic analytics operations using Apache Arrow.

# Sample data
data = {
    'id': pa.array([1, 2, 3, 4, 5]),
    'score': pa.array([85, 92, 76, 88, 95]),
    'category': pa.array(['A', 'B', 'A', 'B', 'A'])
}
# Create Arrow Table
table = pa.table(data)


# Filter rows where score > 90
filter_mask = pc.greater(table['score'], pa.scalar(90))
filtered_table = pc.filter(table, filter_mask)

print(filtered_table.to_pandas())

# Compute mean of the "score" column
mean_result = pc.mean(table['score'])
print("Mean score:", mean_result.as_py())

import pandas as pd

# Convert to pandas for more complex grouping
df = table.to_pandas()
grouped = df.groupby('category')['score'].mean()
print("\nMean score by:", grouped)