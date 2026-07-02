def longest_line(filepath: str) -> str:
    """Return the longest line in the file (trailing \n stripped).
    On ties, return the FIRST one. Empty file returns ''."""
    
    longest_str = ""
    
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            clean_line = line.rstrip('\n')
            
            
            if len(clean_line) > len(longest_str):
                longest_str = clean_line
                
    return longest_str


if __name__ == "__main__":
    test_filepath = "test_longest.txt"
    empty_filepath = "test_empty.txt"

    # 1. TEST: The Tie-Breaker
    with open(test_filepath, "w", encoding="utf-8") as f:
        f.write("apple\n")   # Length 5
        f.write("banana\n")  # Length 6 (First longest)
        f.write("cherry\n")  # Length 6 (Tie for longest)
    
    # We add an f-string to the error message so if it fails, you see EXACTLY what it returned
    assert longest_line(test_filepath) == "banana", f"Failed Tie-Breaker! We expected 'banana' but got '{longest_line(test_filepath)}'"

    # 2. TEST: Whitespace Preservation
    with open(test_filepath, "w", encoding="utf-8") as f:
        f.write("short\n")
        f.write("  kiwi    \n") 
        
    assert longest_line(test_filepath) == "  kiwi    ", "Failed Whitespace!"

    # 3. TEST: Empty File
    with open(empty_filepath, "w", encoding="utf-8") as f:
        pass 
        
    assert longest_line(empty_filepath) == "", "Failed Empty File!"

    print("smooth")