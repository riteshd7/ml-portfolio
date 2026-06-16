"""
    Exercise 2 — Password Strength Checker
    ======================================
    Goal
    ----
    Write a function that takes a password string and returns a dict describing
    how strong it is, plus a list of specific issues.

    Why this exercise
    -----------------
    Real software is mostly: take input, validate it, return structured feedback.
    This is the simplest example of that pattern. You'll do the same shape of work
    on Day 2 (validating inputs to a CLI) and Day 6 (parsing log lines).

    You should finish in 35–50 minutes.

    Specification
    ------------- 
    Implement:

        check_password(password: str) -> dict

    Returns a dict with exactly these keys:

        {
            "score":    int       # 0 to 5 — number of rules passed
            "strength": str       # "weak" | "medium" | "strong"
            "issues":   list[str] # human-readable list of failed rules
        }
    
    Rules (each pass = +1 to score)
    -------------------------------
    1. Length is at least 8 characters
    2. Contains at least one lowercase letter (a–z)
    3. Contains at least one uppercase letter (A–Z)
    4. Contains at least one digit (0–9)
    5. Contains at least one special character (anything not alphanumeric)

    Strength mapping
    ----------------
    - score 0–2 → "weak"       
    - score 3–4 → "medium"
    - score 5   → "strong"

    Issues list
    -----------
    For each failed rule, append ONE string from this exact set:

    "too short"
    "no lowercase"
    "no uppercase"
    "no digit"
    "no special character"

    If a rule passes, do NOT add anything.
    Order in the issues list must match the rule order above.

    Edge cases
    ----------
    - Empty string: score 0, strength "weak", all 5 issues
    - `None` input: raise TypeError("password must be a string")
    - Whitespace counts as a special character (it's not alphanumeric)
    Forbidden today
    ---------------
    - `re` module (do this without regex — practice raw string ops)
    - LLMs on first pass

    Allowed                                     
    -------
    - `str.isalpha`, `str.isdigit`, `str.islower`, `str.isupper`, `str.isalnum`
    - Iteration with `for ch in password:`
    - `any(...)`, `all(...)` are great here
"""

def check_password(password):
    # TODO: implement per spec above
    
    if password is None:
        raise TypeError 
    if password == "":
        score = 0
        issues = []
        issues.append("too short")
        issues.append("no lowercase")
        issues.append("no uppercase")
        issues.append("no digit")
        issues.append("no special character")
        result_dict = {}
        result_dict["score"] = 0
        result_dict["strength"] = "weak"  
        result_dict["issues"] = issues
        return result_dict

    score = 0
    issues = []
    pass_len = len(password)
    if pass_len < 8 :
        issues.append("too short")
    else:
        score += 1
        
    if any(ch.islower() for ch in password):
        score += 1
    else:
        issues.append("no lowercase")
        
    if any(ch.isupper() for ch in password):
        score += 1
    else:
        issues.append("no uppercase")

    if any(ch.isdigit() for ch in password):
        score += 1
    else:
        issues.append("no digit")

    if  any(not ch.isalnum() for ch in password):
        score += 1
    else:
        issues.append("no special character")
        


    if score < 3:
        strength = "weak"
    elif score < 5:
        strength = "medium"
    else:
        strength = "strong"

    result_dict = {}
    result_dict["score"] = score
    result_dict["strength"] = strength  
    result_dict["issues"] = issues

    return result_dict

    # ---------------------------------------------------------------------------
    # Tests — DO NOT MODIFY.                      
    # ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Strong password: meets all 5 rules
    r = check_password("Hello123!")
    assert r["score"] == 5
    assert r["strength"] == "strong"
    assert r["issues"] == []

    # Medium: 4 rules (no special char)
    r = check_password("Hello123")
    assert r["score"] == 4
    assert r["strength"] == "medium"
    assert r["issues"] == ["no special character"]

    # Medium: 3 rules
    r = check_password("hello123")
    assert r["score"] == 3
    assert r["strength"] == "medium"
    assert r["issues"] == ["no uppercase", "no special character"]

    # Weak: too short
    r = check_password("Ab1!")
    assert r["score"] == 4  # passes lower, upper, digit, special
    assert "too short" in r["issues"]
    assert r["strength"] == "medium"  # 4 rules passed

    # Empty
    r = check_password("")
    assert r["score"] == 0
    assert r["strength"] == "weak"
    assert r["issues"] == [
        "too short",
        "no lowercase",
        "no uppercase",
        "no digit",
        "no special character",
    ]

    # Whitespace counts as special
    r = check_password("Hello 12")
    assert "no special character" not in r["issues"]

    # All lowercase, no number
    r = check_password("abcdefghij")
    assert r["score"] == 2  # length, lowercase
    assert r["strength"] == "weak"

    # None input
    try:
        check_password(None)
    except TypeError:
        pass
    else:
        raise AssertionError("check_password(None) should raise TypeError")
    print("All tests passed.")
