import re

def startsWithHello(s: str) -> bool:
    x = re.findall(r'^Hello', s) 
    if x:
        return True
    return False

print(startsWithHello("Hello my name"))
print(startsWithHello("No Hello my name"))