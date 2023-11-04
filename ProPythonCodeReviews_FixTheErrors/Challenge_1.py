words = ['apple', 'banana', 'apple', 'cherry', 'cherry', 'cherry']

word_counts = {}
for word in words:
    if word not in word_counts:
        word_counts[word] = 0
    word_counts[word] = word_counts[word] + 1

most_common_word = max(word_counts, key = word_counts.get)
print(most_common_word)