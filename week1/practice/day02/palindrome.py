def is_palindrome(s: str):
    """True if s reads the same forwards and backwards, ignoring case
    and non-alphabetic characters. Empty string is True."""
    ...
    """ 
    cleaned = ""                            #TRY1 
    
    for char in s:
        if char.isalpha():
            cleaned += char.lower()
    
    return cleaned == cleaned[::-1] """

    """  cleaned = ""                        #TRY2
    for char in s:
        if char.isalpha():
            cleaned += char.lower()

    return cleaned == cleaned[::-1] """


    cleaned = "".join(c.lower() for c in s if c.isalpha())
    return cleaned == cleaned[::-1] 


if __name__ == "__main__":
    print("Running tests")

    assert is_palindrome("racecar")
    assert is_palindrome("A man, a plan, a canal: Panama")
    assert is_palindrome("")
    assert not is_palindrome("hello")  
    assert is_palindrome("Was it a car or a cat I saw?")

    print("All tests passed! Your palindrome checker is bulletproof.")

