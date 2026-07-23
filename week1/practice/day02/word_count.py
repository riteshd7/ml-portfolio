import os
""" 
def word_count(filepath : str):
    with open(filepath , "r" , encoding = "utf-8") as file:
        content = file.read()
        words = content.split()
        count = len(words)
    return count
"""
"""
def word_count(filepath: str) :    #try2
    with open(filepath , "r" , encoding = "utf-8") as file :
        for line in file:
            words = line.split()
            totalwords += len(words)    
    
    return totalwords

"""
def word_count(filepath):           #try3 
    with open(filepath, "r" , encoding = "utf-8") as file : 
        totalwords = sum(len(line.split()) for line in file)
    return totalwords


##CHECKING AND ASSERTIONS FROM CLAUDE

def check_word_count(text_content: str, expected_count: int):
    """Helper to create a temp file, run the assertion, and clean up."""
    test_file = "temp_test.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(text_content)
        
    try:
        # The actual assertion
        actual_count = word_count(test_file)
        assert actual_count == expected_count, f"Expected {expected_count}, got {actual_count} for {repr(text_content)}"
    finally:
        os.remove(test_file)

# Test 1: Standard sentence
check_word_count("This is a simple test file.", 6)

# Test 2: Empty file
check_word_count("", 0)

# Test 3: Only whitespace (spaces, tabs, newlines)
check_word_count("   \n\n  \t  \n ", 0)

# Test 4: Multiple spaces and weird formatting between words
check_word_count("Word one.    Word\ntwo.\tWord three.", 6)

# Test 5: Single word
check_word_count("Supercalifragilisticexpialidocious", 1)

print("All assertions passed successfully! ✅")
print("smooth") 