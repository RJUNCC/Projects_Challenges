def unique_squares(ls1: list, ls2: list):
    temp = set(ls1 + ls2)
    return [i**2 for i in temp]

print(unique_squares([1, 2, 3, 4], [3, 4, 5, 6]))