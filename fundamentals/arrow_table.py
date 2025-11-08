import pyarrow as pa

# Create an Arrow table (multiple columns)

table = pa.table({
    'column1': [1, 2, 3],
    'column2': ['a', 'b', 'c'],
})

print("Arrow Table:", table)