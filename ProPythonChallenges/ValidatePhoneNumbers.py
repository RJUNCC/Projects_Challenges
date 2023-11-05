import re

def validate_phone_numbers(num: str) -> bool:
    x = re.findall(r'\d\d\d-\d\d\d-\d\d\d\d', num)
    if x:
        return True
    return False

print(validate_phone_numbers("123-456-7890"))