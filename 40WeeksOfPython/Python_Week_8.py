def join_strings(ls: list) -> str:
    string = ""
    for i in ls:
        string = string + i + ' '
    return string

print(join_strings(["Hello", "how", "are", "you?"]))
print(join_strings(["What's", "your", "name?"]))