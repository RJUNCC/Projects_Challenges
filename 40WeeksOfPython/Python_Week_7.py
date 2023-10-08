# Challenge Question
def capitalize_string(word: str) -> str:
    # ASCII way
    if ord(word[0]) > 90:
        word = word.replace(word[0], chr(ord(word[0])-32))
        return word
    else:
        return word

print(capitalize_string('hello'))
print(capitalize_string('Again'))
print(capitalize_string('Bgain'))