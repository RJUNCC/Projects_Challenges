def filter_positive_numbers(ls: list) -> list:
    return [i for i in ls if i > 0]

print(filter_positive_numbers([-2, -1, 0, 1, 2]))