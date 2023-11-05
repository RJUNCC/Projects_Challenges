def extract_vowels(ls: list)->list:
    vowels = ['a', 'e', 'i', 'o', 'u']
    new_ls = []
    temp = ""
    for i in ls:
        for j in i:
            if j in vowels:
                temp += j
        new_ls.append(temp)
        temp = ""
    return new_ls

print(extract_vowels(["apple", "banana", "orange"]))