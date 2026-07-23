def count_vowels(s: set):

    """ 
    cleaned = ""
    for char in s:
        cleaned += char.lower()

    vowels = ['a', 'e', 'i', 'o', 'u']
    
    vowel_counts = {}

    for char in cleaned:
        if char in vowels:
            if char in vowel_counts:
                vowel_counts[char] += 1  # It's already there, add 1 to the count
            else:
                vowel_counts[char] = 1   # First time seeing it, set the count to 1
                
    return vowel_counts
    """

    
    clean = s.lower()       #TRY 2 
    vowel = "aeiou"
    count = {}
    for c in clean:
        if c in vowel:
            if c in count.keys():
                count[c] += 1
            else:
                count[c] = 1

    return count

    #proper -   use count[char] = vowel_count.get(char, 0) + 1
    

        








if __name__ == "__main__":
    assert count_vowels("hello") == {"e": 1, "o": 1}
    assert count_vowels("AaEe") == {"a": 2, "e": 2}
    assert count_vowels("xyz") == {}
    print("smooth")

