def single_letter_count(str1: str, str2: str) -> int:
    return str1.lower().count(str2.lower())

print(single_letter_count("HelLo World", "L"))