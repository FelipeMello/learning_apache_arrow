import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import time


# Using Apache Arrow with Larger Datasets
# Let’s look at a real example of how fast and effective Arrow can be when loading, filtering, and analyzing a large dataset.

# 1 Generate a large DataFrame with a million rows
df = pd.DataFrame({
    'id': range(1, 1_000_001),  # assuming a dataset with a million rows
    'value': np.random.randint(1, 1000, size=1_000_000),
    'category': np.random.choice(['A', 'B', 'C'], size=1_000_000)
})

# 2 Convert the DataFrame to an Arrow Table
start = time.time()
arrow_table = pa.Table.from_pandas(df)
end = time.time()
print(f"Conversion to Arrow Table took {end - start:.4f} seconds")

# 3 Filter rows where 'value' > 990
start = time.time()
filtered_table = pc.filter(arrow_table, pc.greater(arrow_table['value'], pa.scalar(990)))
end = time.time()

# 4 Result summary
print(f"Filtering took {end - start:.4f} seconds")
print(f"Filtered row count: {filtered_table.num_rows}")


# 5 Convert the filtered Arrow Table to a pandas DataFrame (zero copy)
start = time.time()
filtered_df = filtered_table.to_pandas()
end = time.time()
print(f"Conversion to pandas DataFrame took {end - start:.4f} seconds")

# Arrow’s columnar format and SIMD-powered compute functions make it an excellent choice for large-scale in-memory operations. And thanks to zero-copy conversion, moving back to pandas is fast and efficient.

# For workflows where you load data before Arrow conversion, this course on streamlined data ingestion with pandas can optimize your pipeline.