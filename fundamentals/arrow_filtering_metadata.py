import pyarrow as pa
import pyarrow.compute as pc

arr = pa.array([10, 20, 30, 40, 50])

# Create a boolean mask: Keep elements > 25
mask = pc.greater(arr, pa.scalar(25))

# Apply the filter
filtered = pc.filter(arr, mask)

print("Filtered Array (values > 25):", filtered)

print("Array Type:", arr.type)
print("Array Length:", len(arr))
print("Null Count:", arr.null_count)
print("Is Null Bitmap Buffers:", arr.buffers())