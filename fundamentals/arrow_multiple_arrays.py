import pyarrow as pa

# Create individual Arrow Arrays
ids = pa.array([1, 2, 3])
names = pa.array(['Alice', 'Bob', 'Charlie'])
scores = pa.array([85.0, 92.5, 78.3])

# Combine them into a Table
table = pa.table({
    'id': ids,
    'name': names,
    'score': scores
})

print("Arrow Table from Arrays:")
print(table)