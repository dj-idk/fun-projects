from collections import Counter

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
words_list = text.split()
words_list = [word.strip() for word in words_list]

print(Counter(words_list))
print(Counter(words_list).most_common(3))
