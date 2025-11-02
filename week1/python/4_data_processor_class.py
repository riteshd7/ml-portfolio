class DataProcessor:
    """
    A comprehensive data preprocessing class for ML pipelines.
    """
    
    def __init__(self, data=None, config=None):
        """
        Initialize the DataProcessor.
        
        Args:
            data (pd.DataFrame): Input dataset
            config (dict): Configuration parameters
                - 'scaling_method': 'standard', 'minmax', or 'robust'
                - 'handle_missing': 'drop', 'mean', 'median', or 'mode'
                - 'encode_categorical': True/False
        """
        self.data = data
        self.config = config or {}
        self.original_shape = None
        self.processing_history = []
        
    def load_data(self, filepath):
        """
        Load data from CSV file.
        
        Args:
            filepath (str): Path to CSV file
        
        Returns:
            self: Returns self for method chaining
        """
        # TODO: Implement data loading
        # Record original shape
        # Add to processing history
        pass
    
    def clean_data(self):
        """
        Clean the dataset (remove duplicates, fix column names).
        
        Returns:
            self: Returns self for method chaining
        """
        # TODO: Implement these cleaning steps:
        # 1. Remove duplicate rows
        # 2. Clean column names (lowercase, replace spaces with underscore)
        # 3. Remove columns with >90% missing values
        # 4. Log each action to processing_history
        pass
    
    def handle_missing_values(self, strategy='mean'):
        """
        Handle missing values based on strategy.
        
        Args:
            strategy (str): 'drop', 'mean', 'median', 'mode', or 'forward_fill'
        
        Returns:
            self: Returns self for method chaining
        """
        # TODO: Implement different strategies
        # Numeric columns: use mean/median
        # Categorical columns: use mode or 'Unknown'
        # Log the action and number of values filled
        pass
    
    def encode_categorical(self, columns=None):
        """
        Encode categorical variables.
        
        Args:
            columns (list): Specific columns to encode, or None for all
        
        Returns:
            self: Returns self for method chaining
        """
        # TODO: Implement encoding
        # Use label encoding for ordinal variables
        # Use one-hot encoding for nominal variables (<10 unique values)
        # Log the encoding method used
        pass
    
    def get_summary(self):
        """
        Get processing summary report.
        
        Returns:
            dict: Summary with before/after stats and processing history
        """
        # TODO: Return comprehensive summary including:
        # - Original shape vs current shape
        # - List of processing steps applied
        # - Columns modified/removed
        # - Data quality metrics
        pass
    
    def export_clean_data(self, filepath):
        """
        Export the processed data.
        
        Args:
            filepath (str): Output file path
        """
        # TODO: Save processed data and metadata
        pass

# Example usage to test your class:
processor = DataProcessor()
processor.load_data('sample_data.csv') \
         .clean_data() \
         .handle_missing_values(strategy='median') \
         .encode_categorical()

summary = processor.get_summary()
print("Processing complete!")
print(f"Original shape: {summary['original_shape']}")
print(f"Final shape: {summary['final_shape']}")
print(f"Steps applied: {summary['processing_history']}")

# Bonus methods to add:
# - scale_features(): Implement different scaling methods
# - detect_outliers(): Find and optionally remove outliers
# - feature_selection(): Select top K features based on correlation
# - split_data(): Split into train/test sets