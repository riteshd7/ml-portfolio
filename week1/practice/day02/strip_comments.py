def strip_comments(filepath: str) -> str:
    """Read a Python file. Return its contents with full-line comments and
    trailing inline comments removed. Preserve blank lines.

    A 'comment' is anything from a # to end of line. Be careful: a # inside
    a string literal is NOT a comment. For today's exercise, you can ignore
    string literals (just strip everything from # onward)."""
    ...

    with open(filepath , "r" , encoding = "utf-8") as file :

        lines = file.read().split('\n')

        clean_lines = []    
        for line in lines:
            clean_line = line.split('#', 1)[0] 
            clean_lines.append(clean_line)

    return '\n'.join(clean_lines) 


    #ASSERTIONS FROM GEMINI

if __name__ == "__main__":

    test_filepath = "test_script.py"
    with open(test_filepath, "w", encoding="utf-8") as f:
        f.write("x = 10\n")                           # Normal line
        f.write("# A full-line comment\n")            # Full comment
        f.write("y = 20   # An inline comment\n")     # Inline comment
        f.write("\n")                                 # Blank line
        f.write("z = 30")                             # Normal line
        
    # 2. Run your function
    result = strip_comments(test_filepath)
    
    # 3. The Expected Result 
    # (This assumes you used the version WITH .rstrip() to clean spaces)
    expected_result = "x = 10\n\ny = 20\n\nz = 30"
    
    # 4. The Assertion
    assert result == expected_result, f"Failed! Got:\n{result}"
    
    print("smooth")

