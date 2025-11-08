import pyarrow as pa
import pandas as pd

# Create an Arrow Table
data = {
    'numbers': [1, 2, 3],
    'fruits': ['apple', 'banana', 'cherry'],
    'prices': [1.1, 2.2, 3.3]
}
arrow_table = pa.table(data)

# Convert Arrow Table to pandas DataFrame
df = arrow_table.to_pandas()

# Show the DataFrame
print(df)