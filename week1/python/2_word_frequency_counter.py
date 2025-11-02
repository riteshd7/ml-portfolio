# Sample text
text = """Machine learning is a subset of artificial intelligence. 
          Machine learning algorithms build models based on training data.
          Learning from data is the core of machine learning."""

# TODO: Create a function that:
# 1. Converts text to lowercase
# 2. Removes punctuation
# 3. Splits into words
# 4. Counts frequency of each word
# 5. Returns sorted dictionary by frequency (descending)

def word_frequency_counter(text):
    """
    Returns a dictionary with word frequencies sorted by count.
    
    Args:
        text (str): Input text to analyze
    
    Returns:
        dict: Words as keys, frequencies as values
    
    Example output:
        {'machine': 3, 'learning': 3, 'is': 2, 'data': 2, ...}
    """
    pass  # Your implementation here

# Bonus tasks:
# - Exclude common stop words ('is', 'a', 'the', 'of', 'from')
# - Return top N most frequent words
# - Handle contractions (e.g., "don't" -> "do not")
# - Create a bar plot of top 10 words