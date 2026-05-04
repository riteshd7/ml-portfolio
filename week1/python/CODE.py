import pandas as pd
import numpy as np


test_df = pd.DataFrame({
    'age': [25, 30, np.nan, 35, 30],
    'salary': [50000, 60000, 55000, 0, 60000],   
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Bob'],
    'constant': [1, 1, 1, 1, 1]  # Zero variance column
})



print( test_df['salary'] > 50000  )
print(test_df[test_df['name'] == 'Bob'])



print(test_df.isna())
print(test_df.isna().sum())
print(test_df.isna().sum().to_dict())

