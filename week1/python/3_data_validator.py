def validate_dataset(data, rules=None):
    """
    Validates a pandas DataFrame for ML readiness.
    
    Args:
        data (pd.DataFrame): Input dataset
        rules (dict): Custom validation rules (optional)
    
    Returns:
        dict: Validation report with the following keys:
            - 'is_valid': Boolean
            - 'missing_values': Dict with column names and missing count
            - 'data_types': Dict with column names and types
            - 'duplicates': Number of duplicate rows
            - 'shape': Tuple (rows, columns)
            - 'warnings': List of warning messages
            - 'errors': List of error messages
    
    Example usage:
        report = validate_dataset(df)
        if report['is_valid']:
            print("Dataset is ready for ML!")
        else:
            print("Issues found:", report['errors'])
    """
    
    # TODO: Implement these checks:
    # 1. Check for missing values in each column
    # 2. Identify data types (numeric, categorical, datetime)
    # 3. Check for duplicate rows
    # 4. Validate column names (no spaces, special characters)
    # 5. Check if dataset is empty
    # 6. Identify columns with single unique value (zero variance)
    # 7. Check for extreme outliers (values > 3 std dev)
    
    pass  # Your implementation here

# Test your function with this sample data:
import pandas as pd
import numpy as np

test_df = pd.DataFrame({
    'age': [25, 30, np.nan, 35, 30],
    'salary': [50000, 60000, 55000, 0, 60000],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Bob'],
    'constant': [1, 1, 1, 1, 1]  # Zero variance column
})

# Expected warnings:
# - Missing value in 'age' column
# - Duplicate rows found
# - Zero variance column: 'constant'
# - Potential outlier in 'salary' (0 value)