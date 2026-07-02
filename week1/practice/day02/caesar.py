def caesar(text,shift):
    """Caesar cipher. Shift letters by `shift` positions (wrap a-z and A-Z).
    Non-letters pass through unchanged. Negative shift = decrypt."""
    ...
    

    result = []

    for char in text:
        if char.isalpha():
            base = ord('a') if char.islower() else ord("A")
            
            new_char = chr((ord(char) - base + shift) % 26 + base )

            result.append(new_char)
        
        else:
            result.append(char)
        
    return "".join(result)


if __name__ == "__main__":
    assert caesar("abc", 1) == "bcd"
    assert caesar("xyz", 1) == "yza"
    assert caesar("Hello, World!", 13) == "Uryyb, Jbeyq!"  # ROT13
    assert caesar("Uryyb, Jbeyq!", -13) == "Hello, World!"
    
    print("smooth")
    