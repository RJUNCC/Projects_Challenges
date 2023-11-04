def contains_blue(*args):
    return "blue" in args

print(contains_blue(25, "blue"))
print(contains_blue("green", False, 37, "purple", "hello world"))
print(contains_blue("blue"))
print(contains_blue("a", 99, "blah blah blah", 1, True, False, "blue"))
print(contains_blue(1, 2, 3))