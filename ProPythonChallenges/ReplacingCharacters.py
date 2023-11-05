import re
def repChar(s: str) -> str:
    return re.sub("\d", "#", s)

print(repChar("1234 Main St"))
print(repChar("Main 1234 St"))