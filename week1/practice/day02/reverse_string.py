def reverse(s: str):
    """Return s reversed, WITHOUT using s[::-1] or reversed()."""
    ...

    string_reversed = ""

    for char in s :
        string_reversed = char + string_reversed
    
    return string_reversed


if __name__ == "__main__" :
    
    assert reverse("") == ""
    assert reverse("a") == "a"
    assert reverse("hello") == "olleh"
    assert reverse("ab cd") == "dc ba"
    assert reverse("areallassertionscorrect?") == "?tcerrocsnoitressallaera"

    print("smooth")
