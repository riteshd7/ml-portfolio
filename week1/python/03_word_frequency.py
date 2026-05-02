"""
Exercise 3 — Word Frequency from a File
========================================

Goal
----
Read a text file from disk, count how often each word appears, exclude common
English stop words, and return the top N most frequent words as a list of
(word, count) tuples.

Why this exercise
-----------------
This is your first encounter with file I/O — it sounds trivial but trips up
beginners (encoding, paths, the difference between `open()` and `read()`).
You'll also wrestle with sorting tuples by a non-default key, which is one of
the most common patterns in real Python.

You should finish in 50–70 minutes.

Specification
-------------
Implement two functions:

    tokenize(text: str) -> list[str]
        - Lowercases the text
        - Splits into words (a "word" is any maximal run of letters)
        - Strips punctuation
        - Returns a list of word strings
        - Empty string returns []

    top_words(filepath: str, n: int = 10, exclude_stopwords: bool = True) -> list[tuple[str, int]]
        - Reads the file at `filepath` (UTF-8)
        - Tokenizes the contents
        - If exclude_stopwords is True, removes any word in STOPWORDS (defined below)
        - Counts occurrences
        - Returns the top `n` (word, count) tuples, sorted by count DESC,
          and ties broken by word ASC (alphabetical)
        - If file doesn't exist, raise FileNotFoundError with a helpful message

Stop words to use
-----------------
STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "and", "or", "but", "if", "then", "else", "to", "of", "in", "on",
    "at", "for", "with", "from", "by", "as", "i", "you", "he", "she",
    "it", "we", "they", "this", "that", "these", "those", "my", "your",
}

Sample input file
-----------------
A sample file `sample_text.txt` is provided in the same folder as this script.
Use it for testing. (If it doesn't exist, the test will create it.)

Forbidden today
---------------
- `collections.Counter` is allowed but try writing the count loop yourself FIRST,
  then refactor to Counter. This forces you to internalize what Counter does.
- `re` is allowed but optional. `str.isalpha()` works for tokenization too.

Common pitfalls
---------------
- Forgetting `encoding="utf-8"` → mojibake on non-ASCII text
- Using `text.split()` alone — it doesn't strip punctuation, so "hello," and
  "hello" become two different tokens
- Sorting only by count and forgetting the alphabetical tiebreaker → unstable
  output across runs
"""

from pathlib import Path

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "and", "or", "but", "if", "then", "else", "to", "of", "in", "on",
    "at", "for", "with", "from", "by", "as", "i", "you", "he", "she",
    "it", "we", "they", "this", "that", "these", "those", "my", "your",
}


def tokenize(text):
    # TODO: lowercase, strip punctuation, split into words
    pass


def top_words(filepath, n=10, exclude_stopwords=True):
    # TODO: read file, tokenize, count, sort, return top n
    pass


# ---------------------------------------------------------------------------
# Tests — DO NOT MODIFY.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    here = Path(__file__).parent
    sample = here / "sample_text.txt"

    # Create a sample if missing
    if not sample.exists():
        sample.write_text(
            "The quick brown fox jumps over the lazy dog.\n"
            "The dog barks. The fox is quick. The lazy dog sleeps.\n"
            "A brown fox and a quick fox are not the same fox.\n",
            encoding="utf-8",
        )

    # tokenize tests
    assert tokenize("") == []
    assert tokenize("Hello, world!") == ["hello", "world"]
    assert tokenize("It's a test.") == ["it", "s", "a", "test"]  # apostrophes split
    assert tokenize("ONE one One") == ["one", "one", "one"]

    # top_words with stopwords excluded
    result = top_words(str(sample), n=5)
    # "fox" appears 5 times, "dog" 3, "quick" 3, "brown" 2, "lazy" 2
    # Tiebreakers: dog before quick alphabetically
    assert result[0] == ("fox", 5), f"expected fox=5, got {result[0]}"
    assert result[1] == ("dog", 3), f"expected dog=3, got {result[1]}"
    assert result[2] == ("quick", 3), f"expected quick=3, got {result[2]}"

    # Without excluding stopwords, "the" should dominate
    result_all = top_words(str(sample), n=3, exclude_stopwords=False)
    assert result_all[0][0] == "the"

    # n=0 returns empty list
    assert top_words(str(sample), n=0) == []

    # File not found
    try:
        top_words("does_not_exist.txt")
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("should raise FileNotFoundError")

    print("All tests passed.")
