import re
def findEmail(s: str) -> list:
    x = re.findall(r'[\w.]+@[\w.]+.com', s)
    return x

print(findEmail("My email addresses are test1@example.com and test2@example.com"))