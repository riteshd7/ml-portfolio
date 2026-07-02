def dedupe_lines(input_path: str, output_path: str):
    
    seen = set()
    unique_lines = []

    with open(input_path , "r" , encoding="utf-8") as infile :
        for line in infile:
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)
            
    with open(output_path , "w" , encoding = "utf-8") as outfile :
        for line in unique_lines:
            outfile.write(line)
    
    return len(unique_lines)


if __name__ == "__main__":
    import os
    
    test_in = "test_in.txt"
    test_out = "test_out.txt"
    
    # Create a test file with duplicate lines
    with open(test_in, "w", encoding="utf-8") as f:
        f.write("apple\n")
        f.write("banana\n")
        f.write("apple\n")    # Duplicate!
        f.write("cherry\n")
        f.write("banana\n")   # Duplicate!
        
    # Run the function
    lines_written = dedupe_lines(test_in, test_out)
    
    # Check 1: Did it return the correct count? (apple, banana, cherry = 3)
    assert lines_written == 3, f"Expected 3 lines, got {lines_written}"
    
    # Check 2: Did it write the correct lines in the right order?
    with open(test_out, "r", encoding="utf-8") as f:
        result_lines = f.read()
        
    expected = "apple\nbanana\ncherry\n"
    assert result_lines == expected, "Output file contents did not match exactly!"
    
    # Clean up test files
    os.remove(test_in)
    os.remove(test_out)
    
    print("smooth")