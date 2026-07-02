def merge_alternating(path_a: str, path_b: str, output_path: str) :
    """ 
    lines_a = []
    lines_b = []

    with open(path_a , "r" , encoding = "utf-8") as file_a:
        for line in file_a:
            lines_a.append(line)

    with open(path_a , "r" , encoding = "utf-8") as file_b:
        for line in file_b:
            lines_b.append(line)

    with open(output_path, "w" , encoding = "utf-8") as output_file:
        
        if len(lines_a) > len(lines_b):
            for l in range(len(lines_b)):
                output_file.write(lines_a[l])
                output_file.write(lines_b[l])
            for m in range
    """

    with open(path_a , "r" , encoding = "utf-8") as fa,\
         open(path_b , "r" , encoding = "utf-8") as fb,\
         open(output_path , "w" , encoding = "utf-8") as fout:
        
        while True:
            line_a = fa.readline()
            line_b = fb.readline()

            if not line_a and not line_b:
                break

            if line_a:
                fout.write(line_a)
            
            if line_b:
                fout.write(line_b)


if __name__ == "__main__":
    import os
    
    file_a = "test_a.txt"
    file_b = "test_b.txt"
    file_out = "test_out.txt"
    
    # File A has 4 lines
    with open(file_a, "w", encoding="utf-8") as f:
        f.write("A1\n")
        f.write("A2\n")
        f.write("A3\n")
        f.write("A4\n")
        
    # File B only has 2 lines (it runs out first)
    with open(file_b, "w", encoding="utf-8") as f:
        f.write("B1\n")
        f.write("B2\n")
        
    # Run your function
    merge_alternating(file_a, file_b, file_out)
    
    # Check the results
    with open(file_out, "r", encoding="utf-8") as f:
        result = f.read()
        
    expected = "A1\nB1\nA2\nB2\nA3\nA4\n"
    
    assert result == expected, f"Failed! Got:\n{result}"
    
    # Clean up test files
    os.remove(file_a)
    os.remove(file_b)
    os.remove(file_out)
    
    print("smooth")