import pyarrow as pa
# Create a table directly from Python data
data = {
    'id': [4, 5, 6],
    'name': ['Diana', 'Eve', 'Frank'],
    'score': [88.0, 79.5, 91.2]
}

table2 = pa.table(data)

print("\nArrow Table from Dictionary:")
print(table2)