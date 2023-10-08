# Challenge Question
def mood(mood: str = None) -> str:
    if mood != None:
        return f"Today, I am feeling {mood}"
    return f"Today, I am feeling neutral"

print(mood("Great"))
print(mood())
