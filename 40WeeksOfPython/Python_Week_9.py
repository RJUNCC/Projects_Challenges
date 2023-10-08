# Problem 1
def to_int(string: str) -> int:
    string = string.replace(",", "")
    if string.isdigit():
        return int(string)
    else:
        return f"\"{string}\" is not a valid integer"
print(to_int("123")) 
print(to_int("1,234")) 
print(to_int("1,9-0awd0a0-wd234"))

def to_str(integer: int) -> str:
    return str(integer)

print(to_str(123))

# Problem 2
def lessOrEqualsZero(num: int) -> bool:
    return num <= 0

print(lessOrEqualsZero(0)) # True
print(lessOrEqualsZero(1)) # False
print(lessOrEqualsZero(-1)) # True

# Bonus
def sumStrings(string1: str, string2: str) -> str:
    string1 = string1.replace(",", "")
    string2 = string2.replace(",", "")
    if string1.isdigit() and string2.isdigit():
        return str(int(string1) + int(string2))
    else:
        return f"\"{string1}\" and/or \"{string2}\" are/is not (a) valid integer(s)"
    
print(sumStrings("123", "456")) # 579
print(sumStrings("1,234", "456")) # 1690
print(sumStrings("12374adnakjdw234", "4,56")) # "1,234" or "4,56" are not valid integers