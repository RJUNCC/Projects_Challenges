# Challenge Questions
def filter_list(ls: list) -> list:
    new_list = [int(i) for i in ls if i.isdigit()]
    return new_list

print(filter_list(["a", "b", "c", "1", "2", "3"])) # [1, 2, 3]
print(filter_list(["a", "b", "c", "1", "2", "3", "4", "5", "6", "7", "8", "9"])) # [1, 2, 3, 4, 5, 6, 7, 8, 9]
