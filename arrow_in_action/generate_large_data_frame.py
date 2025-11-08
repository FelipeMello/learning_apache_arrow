import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import time

df = pd.DataFrame({
    'id': range(1, 1_000_001),  # assuming a dataset with a million rows
    'value': np.random.randint(1, 1000, size=1_000_000),
    'category': np.random.choice(['A', 'B', 'C'], size=1_000_000)
})