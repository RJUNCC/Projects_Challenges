# Challenge Question
def starts_with_vowel(word: str) -> bool:
    return word[0] in ['a', 'e', 'i', 'o', 'u']

print(starts_with_vowel('hello'))
print(starts_with_vowel('another'))