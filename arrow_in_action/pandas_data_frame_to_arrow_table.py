import pyarrow as pa
import pandas as pd

# Create a pandas DataFrame
df = pd.DataFrame({
    'numbers': [1, 2, 3],
    'fruits': ['apple', 'banana', 'cherry'],
    'prices': [1.1, 2.2, 3.3]
})

# Convert pandas DataFrame to Arrow Table
arrow_table = pa.Table.from_pandas(df)

# Show the Arrow Table
print(arrow_table)