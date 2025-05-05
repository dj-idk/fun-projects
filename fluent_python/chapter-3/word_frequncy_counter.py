import string


def count_words(text: str):
    """
    Counts the number of occurences of a word in a given text.
    """
    text = text.lower()

    for char in string.punctuation:
        text = text.replace(char, "")

    words = text.split()
    occurences = {}
    for word in words:
        occurences.setdefault(word, 0)
        occurences[word] += 1

    return occurences


text = """
Problem Statement:
Create a function that counts the frequency of each word in a given text. The function should:
1.
Take a string of text as input
2.
Split the text into words (you can consider spaces as separators)
3.
Count how many times each word appears
4.
Return a dictionary where keys are words and values are their frequencies
"""

print(count_words(text))
