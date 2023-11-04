def is_valid_PIN(s: str) -> bool:
    n = len(s)
    if (n==4 or n==6) and (s.isdigit()):
        return True
    return False

print(is_valid_PIN("1234"))
print(is_valid_PIN("12345"))
print(is_valid_PIN("a234"))
print(is_valid_PIN(""))