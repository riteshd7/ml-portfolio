def line_count(filepath: str):
    """Return the number of lines in the file. Empty file returns 0."""
    ...
    
    """ count = 0                               #try1 
    
    with open(filepath, 'r') as file:
        for line in file:
            count += 1

    return count 
    """
    
    count  = 0                                  #TRY2 
    with open(filepath , "r" , encoding = "utf-8") as file :
        for line in file:
            count += 1

    return count


if __name__ == "__main__":
    from pathlib import Path
    
    print("Running tests...")
    
    #    WARNING: I changed "/tmp/lc_test.txt" to just "lc_test.txt"
    # See the explanation below to understand why!
    tmp = Path("lc_test.txt") 
    
    # Test 1: File with 3 lines
    tmp.write_text("a\nb\nc\n")
    assert line_count(str(tmp)) == 3
    
    # Test 2: Empty file
    tmp.write_text("")
    assert line_count(str(tmp)) == 0
    
    # Cleanup: Delete the temp file so it doesn't clutter your folder
    if tmp.exists():
        tmp.unlink()
        
    print("All tests passed! File reader is working.")